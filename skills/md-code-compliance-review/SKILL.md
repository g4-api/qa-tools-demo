---
name: md-code-compliance-review
description: Review, score, and automatically repair Markdown files against md-vanilla-style, including CommonMark structure, metadata-only YAML, readable body text, deterministic line enumeration, tables, links, and fences. Use after any .md file is created or changed; repeat until every file scores 100 and the bundled linter reports zero errors.
---

# Markdown Code Compliance Review

## Purpose

Review and repair Markdown through a deterministic cycle until the artifact is flawless.

Read the complete `md-vanilla-style/SKILL.md` before reviewing.
When an owning skill defines an artifact-specific template, validate both contracts.

## Inputs

- One or more changed `.md` files.
- The owning artifact contract, when applicable.
- Any referenced requirement, traceability, or test files needed to validate links and IDs.

## Review cycle

For each file:

1. Run `scripts/lint_markdown.py <file>`.
2. Review every rubric dimension.
3. Produce a score and concrete findings.
4. Repair all findings when automatic execution is authorized by the owning workflow.
5. Run the linter and review again.
6. Repeat until the file scores 100 and the linter returns zero errors.

Do not lower the gate, average multiple files, or declare a file flawless while any violation remains.

## Rubric

| Dimension | Weight |
| --- | ---: |
| YAML boundary and artifact contract | 15 |
| Heading hierarchy, MD041, and document structure | 15 |
| Spacing and source cleanliness | 10 |
| Line enumeration and stable IDs | 20 |
| Lists, tables, and fences | 10 |
| Prose clarity and readability | 15 |
| Links and references | 5 |
| Completeness and internal consistency | 10 |

Score each dimension from 0 to 100 and calculate the weighted total.
Any concrete rule violation makes the total less than 100.

## Flawless gate

A file passes only when:

- the weighted score is exactly 100,
- the linter exits successfully with zero errors,
- YAML exists only in permitted frontmatter,
- the first nonblank body line after optional frontmatter is the document's single level-one heading,
- all required ordered records are enumerated without gaps, and
- the owning artifact contract is satisfied.

## Output contract

Always report one table per file:

```markdown
| Markdown dimension | Weight | Score | Findings |
| --- | ---: | ---: | --- |
| YAML boundary and artifact contract | 15 | 100 | None |
| Heading hierarchy, MD041, and document structure | 15 | 100 | None |
| Spacing and source cleanliness | 10 | 100 | None |
| Line enumeration and stable IDs | 20 | 100 | None |
| Lists, tables, and fences | 10 | 100 | None |
| Prose clarity and readability | 15 | 100 | None |
| Links and references | 5 | 100 | None |
| Completeness and internal consistency | 10 | 100 | None |
| **Markdown compliance** | **100** | **100** | **PASS** |
```

For a failing review, list exact line numbers in Findings and set the final status to FAIL. Do not use vague findings.

## Hard constraints

- Do not pass a file below 100.
- Do not omit line numbers from a failure finding.
- Do not leave YAML or serialized step objects in a QA artifact body.
- Do not omit the per-file score table.
- Do not suppress linter errors.
- Do not pass MD041 or a document with no single level-one body heading.
- Do not pass MD060 table-pipe spacing violations.
- Do not pass code whose nested indentation is not a multiple of four spaces.
- Do not change domain meaning merely to satisfy formatting.

## Completion condition

Complete only when every in-scope Markdown file has a 100 score, zero linter errors, and a delivered per-file score table.
