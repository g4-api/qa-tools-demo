---
name: qa-decompose-requirements
description: Read a requirement source (a document or a Jira user story via the Atlassian MCP) and decompose it into structured, traceable, testable requirements that downstream test-case skills can consume. Use when a QA engineer needs to turn a story, spec, or acceptance criteria into atomic requirements, business rules, candidate test conditions, NFRs, and an explicit gaps list before any test cases are written.
---

# QA Decompose Requirements

## Purpose

This skill turns a raw requirement source into a clean, decomposed, traceable requirements artifact.

It is the first stage of the QA test authoring suite. Its output is the single source of truth that
`qa-create-test-cases`, `qa-review-test-cases`, and `qa-orchestrate-test-cases` consume.

This skill must:
1. resolve the requirement source (document or Jira user story),
2. retrieve the full context for that source,
3. confirm with the user that the retrieved context is complete,
4. decompose the source into atomic, testable, ID-tagged requirements,
5. surface gaps and open questions instead of inventing answers,
6. persist the decomposition as a first-class artifact (or output it inline on request).

Before writing or changing any `.md` artifact, read and apply `md-vanilla-style`. After each write, invoke
`md-code-compliance-review`, run its linter, repair every finding, and repeat until the file scores 100 with zero linter
errors.

This skill does not write test cases. It prepares the ground for them.

## Use this skill when

Use this skill when the task is about:
- reading a Jira user story (by key, via the Atlassian MCP) and breaking it down for QA
- reading a requirements document or spec and breaking it down for QA
- producing atomic testable requirements with stable traceability IDs
- extracting acceptance criteria, business rules, candidate test conditions, and NFRs
- identifying missing information before test design starts
- refreshing or refactoring an existing `requirements.md` when the source changed

Do not use this skill to author, score, or sync test cases. Route those to the test-case skills and `qa-xray-sync`.

## Operating philosophy

Test artifacts are first-class code files. Treat requirements decomposition with the same rigor as source code: atomic
units, stable identifiers, explicit traceability, no invented behavior, and review-before-execute discipline. Bring the
developer's state of mind to QA.

## Interaction contract

This skill is interactive. It always follows this base flow:

1. **Load** — the skill is triggered by the user prompt.
2. **Ask guiding questions** — resolve only what the prompt did not already specify. Never assume when the answer changes
    the output.
3. **Show a plan** — describe exactly what will be retrieved, decomposed, and written.
4. **Wait for approval** — do not write or fetch destructive changes before the user approves.
5. **Execute** — perform the decomposition and persist artifacts.

Whenever the skill is in doubt about scope, source completeness, depth, or IDs, it must stop and ask the user rather than
guess.

## Guiding questions to resolve at load

Ask only the ones the prompt left open:

1. **Source** — Is the input a Jira issue key through Atlassian MCP or a document path or URL? If it is a document, resolve
    its format and location.
2. **Jira pull scope** — Default to the story description, acceptance-criteria field, linked or child issues, and comments.
    Confirm this scope before pulling. After retrieval, show what was pulled and confirm it is complete.
3. **Depth** — If the user did not specify, present two choices:
    - **Lightweight** — atomic testable requirements plus acceptance criteria.
    - **Full breakdown + traceability** — adds business rules, positive, negative, and edge candidate test conditions,
        non-functional requirements, and a gaps list.
    Both modes attach IDs.
4. **Workspace root** — Default to `./qa-workspace` and persist by default. Do not write files when the user requests
    in-conversation-only output.
5. **Scope** — Single story/document, or a batch/epic. In batch mode, keep each item in its own story folder.

## Source retrieval

### Jira source

- Use the Atlassian MCP to fetch the issue by key.
- After confirming pull scope, retrieve: description, acceptance criteria, linked/child issues, and comments.
- Present a short summary of what was retrieved and ask the user to confirm completeness before decomposing.
- Never fabricate acceptance criteria or requirements that are not grounded in the retrieved content. Treat missing
    content as a gap, not an invention.

### Document source

- Read the document from the provided path or URL.
- If the document is large or multi-section, confirm which section(s) are in scope.
- Treat headings, acceptance criteria, and business rules already present in the document as authoritative.

## Decomposition output

### Folder and file layout

```text
<workspace-root>/
  <STORY-ID>/
    requirements.md
```

- `<STORY-ID>` is the Jira or Xray story key when available, such as `PROJ-123`. Otherwise, assign a story-scoped internal
    `AGENT-S###` identifier starting at `AGENT-S000`.
- In batch mode, each source gets its own `<STORY-ID>` folder.
- When a real Jira or Xray story key becomes known for an internal `AGENT-S###` folder, rename the folder and update the
    metadata header to the real key.

### `requirements.md` contents

Use YAML only for metadata frontmatter. After frontmatter, use the exact metadata `title` as the single level-one heading
and first nonblank body line. Render every requirement, criterion, rule, condition, NFR, gap, and question as readable
enumerated Markdown in the body.

The file must contain, in order:

1. **YAML metadata frontmatter**
    1. `sourceType` (`jira` or `document`)
    2. `source` (Jira key or document path/URL)
    3. `storyKey`
    4. `title`
    5. `link`, when available
    6. `retrievedAt`
    7. `depthMode`
2. **Atomic testable requirements**
    1. Number every requirement from `1` without gaps.
    2. Put exactly one requirement on each ordered-list item.
    3. Include a stable `REQ-###` ID, story-scoped and starting at `REQ-000`.
    4. Keep every requirement independently testable and unambiguous.
3. **Acceptance criteria**
    1. Number every criterion from `1` without gaps.
    2. Map each criterion explicitly to the `REQ-###` IDs it validates.
4. **Business rules** *(Full mode only)*
5. **Candidate test conditions** *(Full mode only)*
    1. Group conditions as positive, negative, and edge.
    2. Number every condition within its group.
    3. Reference the `REQ-###` IDs each condition exercises.
6. **Non-functional requirements** *(Full mode only)*
7. **Gaps and open questions**
    1. Number every ambiguity, omission, or contradiction.
    2. Raise each item to the user; never resolve it silently.

Example boundary:

````markdown
---
sourceType: jira
source: PROJ-123
storyKey: PROJ-123
title: Reject invalid credentials
retrievedAt: 2026-07-17
depthMode: full
---

# Reject invalid credentials

## Atomic testable requirements

1. **REQ-000:** The system rejects an invalid password.
2. **REQ-001:** The system does not create an authenticated session after rejection.

## Acceptance criteria

1. **AC-001** (`REQ-000`): An invalid password produces the approved error response.
2. **AC-002** (`REQ-001`): No authenticated session cookie is returned.
````

Do not place YAML, serialized objects, or machine payloads after the closing frontmatter marker.

## ID rules (traceability backbone)

- Requirements use internal `REQ-###` IDs, story-scoped, stable, starting at `REQ-000`.
- Story folders use the Jira/Xray key when known, otherwise internal `AGENT-S###`.
- These IDs are the traceability backbone consumed downstream: test cases reference `REQ-###` IDs.
- When a story or item later exists in Jira or Xray, replace the internal ID with the real ID everywhere it appears,
    including file content and filenames, for end-to-end consistency.

## Hard constraints

- Do not invent requirements, acceptance criteria, or business rules that are not grounded in the source.
- Do not write body content as YAML; YAML is metadata frontmatter only.
- Do not emit a body whose first nonblank line is not the single level-one heading matching metadata `title`.
- Do not complete while `md-code-compliance-review` reports a score below 100 or any linter error.
- Do not skip the confirm-completeness step after retrieving a Jira source.
- Do not write test cases in this skill.
- Do not assign expressive/prose filenames; identity comes from IDs.
- Do not proceed past the plan step without user approval.
- Do not resolve gaps silently — list them and ask.
- Do not persist files when the user requested in-conversation-only mode.

## Completion condition

This skill is complete when:
- the decomposition exists (persisted under `<workspace-root>/<STORY-ID>/requirements.md`, or delivered inline on request),
- every requirement has a stable `REQ-###` ID,
- acceptance criteria are mapped to requirement IDs,
- gaps and open questions are explicitly listed,
- every ordered record is visibly enumerated,
- the Markdown score is 100 with zero linter errors,
- and the user has been pointed to `qa-create-test-cases` as the next stage.
