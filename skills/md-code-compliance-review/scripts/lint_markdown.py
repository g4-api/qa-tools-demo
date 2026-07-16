#!/usr/bin/env python3
"""Dependency-free structural linter for Markdown artifacts."""

from __future__ import annotations

import re
import sys
from pathlib import Path


MAX_LINE_LENGTH = 125
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+\S")
ORDERED_PATTERN = re.compile(r"^(\s*)(\d+)\.\s+\S")


def add_error(errors: list[str], line_number: int, message: str) -> None:
    """Append one line-addressable error."""

    errors.append(f"line {line_number}: {message}")


def parse_fence(line: str) -> tuple[str, str] | None:
    """Return a fence marker and info string using a linear scan."""

    if not line or line[0] not in {"`", "~"}:
        return None

    marker_character = line[0]
    marker_length = 1
    while marker_length < len(line) and line[marker_length] == marker_character:
        marker_length += 1

    if marker_length < 3:
        return None

    info = line[marker_length:]
    if marker_character == "`" and "`" in info:
        return None

    return line[:marker_length], info


def is_table_delimiter(line: str) -> bool:
    """Return whether a line is a table delimiter using linear cell checks."""

    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]

    cells = stripped.split("|")
    if len(cells) < 2:
        return False

    for cell in cells:
        value = cell.strip()
        if value.startswith(":"):
            value = value[1:]
        if value.endswith(":"):
            value = value[:-1]
        if len(value) < 3 or any(character != "-" for character in value):
            return False

    return True


def lint_frontmatter(lines: list[str], errors: list[str]) -> int:
    """Validate optional YAML frontmatter and return the body start index."""

    if not lines or lines[0] != "---":
        return 0

    try:
        closing_index = lines.index("---", 1)
    except ValueError:
        add_error(errors, 1, "YAML frontmatter is not closed")
        return len(lines)

    if closing_index == 1:
        add_error(errors, 2, "YAML frontmatter is empty")

    return closing_index + 1


def lint_fences(lines: list[str], body_start: int, errors: list[str]) -> set[int]:
    """Validate fences and return line indexes contained in fenced blocks."""

    fenced_lines: set[int] = set()
    opening: tuple[str, int, str] | None = None

    for index in range(body_start, len(lines)):
        line = lines[index]
        fence = parse_fence(line)
        if opening is None:
            if fence is None:
                continue
            marker, info = fence
            language = info.strip()
            if not language:
                add_error(errors, index + 1, "opening code fence has no language")
            if language.lower() in {"yaml", "yml"}:
                add_error(errors, index + 1, "YAML is permitted only in frontmatter")
            opening = (marker, index, language.lower())
            fenced_lines.add(index)
            continue

        fenced_lines.add(index)
        marker, opening_index, language = opening
        if line == marker:
            opening = None
            continue
        if language == "json" and line.strip():
            indentation = len(line) - len(line.lstrip(" "))
            if indentation % 4:
                add_error(
                    errors,
                    index + 1,
                    "JSON code indentation is not a multiple of four spaces",
                )

    if opening is not None:
        _, opening_index, _ = opening
        add_error(errors, opening_index + 1, "code fence is not closed")

    return fenced_lines


def lint_headings(
    lines: list[str], body_start: int, fenced_lines: set[int], errors: list[str]
) -> None:
    """Validate heading hierarchy and surrounding blank lines."""

    previous_level = 0
    for index in range(body_start, len(lines)):
        if index in fenced_lines:
            continue
        match = HEADING_PATTERN.match(lines[index])
        if not match:
            continue
        level = len(match.group(1))
        if previous_level and level > previous_level + 1:
            add_error(errors, index + 1, "heading level skips an intermediate level")
        previous_level = level
        if index > body_start and lines[index - 1].strip():
            add_error(errors, index + 1, "heading is not preceded by a blank line")
        if index + 1 < len(lines) and lines[index + 1].strip():
            add_error(errors, index + 1, "heading is not followed by a blank line")


def lint_enumeration(
    lines: list[str], body_start: int, fenced_lines: set[int], errors: list[str]
) -> None:
    """Validate ordered-list numbering independently at each indentation level."""

    expected_by_indent: dict[int, int] = {}

    for index in range(body_start, len(lines)):
        if index in fenced_lines:
            continue
        match = ORDERED_PATTERN.match(lines[index])
        if not match:
            stripped = lines[index].strip()
            if HEADING_PATTERN.match(lines[index]) or (
                stripped and not lines[index].startswith((" ", "\t"))
            ):
                expected_by_indent.clear()
            continue

        indent = len(match.group(1).replace("\t", "    "))
        number = int(match.group(2))
        expected = expected_by_indent.get(indent, 1)
        if number != expected:
            add_error(errors, index + 1, f"ordered item is {number}; expected {expected}")
        expected_by_indent[indent] = number + 1
        for stale_indent in [value for value in expected_by_indent if value > indent]:
            del expected_by_indent[stale_indent]


def lint_tables(
    lines: list[str], body_start: int, fenced_lines: set[int], errors: list[str]
) -> None:
    """Validate table delimiters and column counts."""

    for index in range(body_start + 1, len(lines)):
        if index in fenced_lines or "|" not in lines[index]:
            continue
        stripped = lines[index].strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = stripped.split("|")[1:-1]
            if any(not cell.startswith(" ") or not cell.endswith(" ") for cell in cells):
                add_error(
                    errors,
                    index + 1,
                    'table pipe is missing adjacent space for style "compact" (MD060)',
                )
        if not is_table_delimiter(lines[index]):
            continue
        header_columns = lines[index - 1].count("|")
        delimiter_columns = lines[index].count("|")
        if header_columns != delimiter_columns:
            add_error(errors, index + 1, "table delimiter column count differs from header")


def lint_line_length(
    lines: list[str], body_start: int, fenced_lines: set[int], errors: list[str]
) -> None:
    """Validate prose line length while exempting tables, links, and code."""

    for index in range(body_start, len(lines)):
        line = lines[index]
        if index in fenced_lines or len(line) <= MAX_LINE_LENGTH:
            continue
        stripped = line.strip()
        if stripped.startswith("|") or "http://" in line or "https://" in line:
            continue
        add_error(
            errors,
            index + 1,
            f"line exceeds the {MAX_LINE_LENGTH}-character limit",
        )


def lint_file(path: Path) -> list[str]:
    """Return all structural errors for one Markdown file."""

    errors: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ["line 1: file is not valid UTF-8"]

    if not text.endswith("\n"):
        errors.append("line EOF: file must end with one newline")
    if text.endswith("\n\n"):
        errors.append("line EOF: file has more than one trailing newline")

    lines = text.splitlines()
    for index, line in enumerate(lines, start=1):
        if line.rstrip(" \t") != line:
            add_error(errors, index, "trailing whitespace")
        if "\t" in line:
            add_error(errors, index, "tab character")

    body_start = lint_frontmatter(lines, errors)
    fenced_lines = lint_fences(lines, body_start, errors)
    lint_headings(lines, body_start, fenced_lines, errors)
    lint_enumeration(lines, body_start, fenced_lines, errors)
    lint_tables(lines, body_start, fenced_lines, errors)
    lint_line_length(lines, body_start, fenced_lines, errors)
    return errors


def main(arguments: list[str]) -> int:
    """Lint input paths and return a process exit code."""

    if not arguments:
        print("Usage: lint_markdown.py <file.md> [file.md ...]", file=sys.stderr)
        return 2

    failed = False
    for raw_path in arguments:
        path = Path(raw_path)
        if path.suffix.lower() != ".md" or not path.is_file():
            print(f"{path}: not a Markdown file", file=sys.stderr)
            failed = True
            continue
        errors = lint_file(path)
        if errors:
            failed = True
            print(f"{path}: FAIL")
            for error in errors:
                print(f"  {error}")
        else:
            print(f"{path}: PASS")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
