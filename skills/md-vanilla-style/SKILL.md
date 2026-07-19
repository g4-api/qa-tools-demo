---
name: md-vanilla-style
description: Author or revise clear, structurally valid Markdown files with strict CommonMark spacing, heading hierarchy, readable prose, deterministic line enumeration, metadata-only YAML frontmatter, and clean tables, lists, links, and code fences. Use whenever requirements, traceability, test cases, reports, or other .md artifacts are created or changed.
---

# Markdown Vanilla Style

## Purpose

Create readable Markdown that is structurally correct, consistently enumerated, and easy to review as source text.

Apply this skill whenever a `.md` file is created or changed.
When another skill defines an artifact template, follow that template and apply these rules to its Markdown representation.

## Document structure

- Use exactly one level-one heading in every document, including documents with YAML frontmatter.
- Make the first nonblank body line after optional YAML frontmatter that level-one heading (MD041).
- Increase heading depth by one level at a time. Never jump from `##` to `####`.
- Keep one blank line before and after headings, lists, tables, block quotes, and fenced blocks.
- End every file with exactly one newline.
- Do not leave trailing spaces or tab characters.
- Do not use raw HTML when Markdown can express the same structure.

## YAML boundary

- Use YAML only for metadata frontmatter when the owning artifact requires it.
- Start frontmatter on the first line with `---` and close it with the next standalone `---`.
- Treat frontmatter as metadata for MD041; require the first nonblank line after it to be the document's level-one heading.
- Keep all content after the closing marker as readable Markdown.
- Do not place YAML, JSON, or serialized object blocks in the body merely to store document content.
- Use fenced data formats in the body only when the document is explicitly teaching or demonstrating that format.

## Line enumeration

Enumerate every ordered, actionable, or traceable record explicitly.

- Number procedure steps from `1` without gaps or duplicate numbers.
- Number setup actions, main test steps, expected results, teardown actions, acceptance criteria,
    business rules, candidate test conditions, gaps, and open questions.
- Preserve stable domain IDs such as `REQ-001` or `AGENT-001`; the visible ordinal and stable ID serve different purposes.
- Restart numbering at `1` under each new section or parent item.
- Use nested ordered lists for child results or substeps. Indent nested items by four spaces.
- Never use an unnumbered bullet where execution order, evaluation order, or one-to-one traceability matters.

Example:

```markdown
1. Submit valid credentials.
    1. The account page opens.
    2. A session cookie is created.
2. Sign out.
    1. The session is invalidated.
```

## Prose and readability

- Write direct, complete sentences.
- Use one idea or action per enumerated line.
- Prefer active voice and concrete nouns.
- Define acronyms on first use unless they are universal in the target domain.
- Avoid filler, vague qualifiers, and duplicated statements.
- Keep paragraphs focused and reasonably short.
- Keep source lines readable; prefer approximately 120 characters, except tables, links, and unavoidable identifiers.

## Lists and tables

- Put a blank line before and after every list.
- Use ordered lists for sequences and traceable records; use bullets only for unordered sets.
- Keep list-marker style consistent within a list.
- Use tables only for compact comparisons or exact mappings.
- Give every table a header row and delimiter row.
- Use compact table pipes with one space on both sides of every cell value, including delimiter cells.
- Keep every row at the same column count.
- Align numeric columns to the right when useful.

## Links and code

- Use descriptive link labels instead of bare URLs.
- Verify local relative links exist.
- Use backticks for identifiers, field names, file names, and literal values.
- Give every fenced code block a language identifier.
- Indent nested code content by four spaces per nesting level.
- Balance every opening fence with a matching closing fence.
- Do not use a code fence for ordinary prose or artifact content.

## QA artifact profile

When authoring QA artifacts:

- Keep requirement and test metadata in YAML frontmatter only when the owning skill requires metadata.
- Follow the owning artifact's identity-heading contract. A test case may use its stable ID as the level-one heading while
    retaining its scenario in metadata.
- Render specifications, setup, test steps, test data, expected results, teardown, coverage,
    and review findings as readable Markdown.
- Enumerate each requirement and criterion while retaining its stable ID.
- Enumerate every setup action, test step, expected result, and teardown action.
- Keep expected results observable and place them as a nested ordered list beneath the action they evaluate.
- Never persist an Xray request payload or step object as YAML in the Markdown body.

## Completion check

Before considering a Markdown write complete:

1. Run `md-code-compliance-review` on every changed `.md` file.
2. Run its bundled linter.
3. Fix every reported violation.
4. Repeat until the compliance score is 100 and the linter reports zero errors.
