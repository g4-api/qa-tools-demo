---
name: qa-create-test-cases
description: Generate, update, or refactor Manual Xray test cases from a requirements decomposition, as first-class per-test Markdown files with YAML frontmatter that map cleanly onto Xray's Manual test structure. Use when a QA engineer needs to author new test cases, extend coverage, or fix/refactor existing test files derived from requirements.md.
---

# QA Create Test Cases

## Purpose

This skill authors Manual Xray test cases from a `requirements.md` decomposition. It is the "create" stage of the create / review / orchestrate trio.

Each test case is a first-class code file: atomic, ID-named, individually reviewable, and shaped so `qa-xray-sync` can construct an exact `new_xray_test` or `update_xray_test` payload without guessing.

This skill must:
1. resolve the requirements source and working mode,
2. propose a coverage matrix and resolve coverage depth,
3. resolve the field template,
4. show a plan and wait for approval,
5. write or update one file per test case,
6. maintain the story-level traceability index.

This skill does not score test quality and does not sync to Xray. Scoring is owned by `qa-review-test-cases`; the loop is owned by `qa-orchestrate-test-cases`; sync is owned by `qa-xray-sync`.

## Use this skill when

Use this skill when the task is about:
- creating new Manual test cases from a decomposed requirement
- extending coverage (positive / negative / edge) for existing requirements
- updating, refactoring, or fixing existing test-case files
- shaping test cases to match Xray's Manual test structure
- keeping requirement-to-test traceability current

Do not use this skill to score test quality, run the review loop, or create/update tests in Xray.

## Operating philosophy

Test artifacts are first-class code files. Author them with the developer's state of mind: atomic units, stable identifiers, explicit traceability, no invented behavior, and review-before-execute discipline. Identity comes from IDs, never from prose filenames.

## Interaction contract

This skill is interactive when run standalone. It always follows this base flow:

1. **Load** — triggered by the user prompt.
2. **Ask guiding questions** — resolve only what the prompt did not already specify.
3. **Show a plan** — the coverage matrix, test count, IDs, and field template.
4. **Wait for approval**.
5. **Execute** — write or update test files and the traceability index.

Whenever in doubt about coverage depth, fields, or whether to create vs update, stop and ask the user.

When invoked by `qa-orchestrate-test-cases`, this skill may run with pre-approved parameters and skip its own approval gate, because the orchestrator owns the loop.

## Guiding questions to resolve at load

Ask only the ones the prompt left open:

1. **Requirements source** — which `<STORY-ID>/requirements.md` (or inline requirements) to work from.
2. **Coverage depth** — if the prompt did not state a level, build a proposed coverage matrix (each `REQ-###` by candidate case type: positive / negative / edge) and ask the user to pick the depth before generating.
3. **Field template** — default to the full field set; let the user confirm or trim. Only the mandatory Xray fields are hard-required.
4. **Mode** — create-new, or update / refactor / fix existing test files.

## Folder and file layout

```text
<workspace-root>/
  <STORY-ID>/
    requirements.md
    traceability.md
    tests/
      AGENT-000.md
```

- Test files live in `<STORY-ID>/tests/`, one file per test case.
- Filename is the ID: internal `AGENT-###` (story-scoped, starting at `AGENT-000`), replaced by the Xray key after sync.
- `traceability.md` lives at the story root and is maintained by this skill.

## Test-case file format

Each test file is Markdown with a YAML frontmatter block.

````markdown
---
id: AGENT-000            # internal; replaced by xrayKey after sync
xrayKey: null            # filled by qa-xray-sync
type: Manual
summary: <required>
priority: <configurable>
categories: []           # configurable; maps to Xray categories
severity: <configurable>
tolerance: <number or omit>
customFields: []         # configurable [{name: <string>, value: <string>}]
folder: <repo/path>      # configurable (Xray Test Repository path)
testSets: []             # configurable
coveredRequirements: [REQ-000]   # traceability -> requirements.md
storyKey: PROJ-123
status: draft
---

## Test Specifications
<detailed test purpose, scope, and acceptance behavior>

## Test Setup
```yaml
- action: <setup action>
  expectedResults:
    - <observable setup result>
```

## Steps
```yaml
- action: <single test action>
  data: <optional input data; folded into action during Xray sync>
  expectedResults:
    - <observable result>
```

## Test Teardown
```yaml
- action: <teardown action>
  expectedResults:
    - <observable teardown result>
```
````

Omit an optional setup or teardown section when it has no items. `expectedResults` is always an array of one or more strings, never a scalar. `data` is local authoring metadata and is folded into `action` during sync because the mutation schemas have no `data` property.

### Mandatory fields (never optional)

- `summary`
- `type: Manual`
- at least one step with a non-empty `action` and a non-empty `expectedResults` array

Everything else is template-configurable. When the prompt does not specify a field template, default to the full set and let the user confirm or trim.

### Step-authoring rules

- steps are ordered and atomic; one clear `action` per step
- `action` states what the tester does; optional `data` holds inputs; every `expectedResults` item is verifiable
- avoid compound steps that hide multiple assertions
- negative and edge cases must make the failure/boundary condition explicit
- custom-field `name` and `value` entries are strings; names are unique within a test
- `tolerance` is a number, never a numeric string

## Xray mutation compatibility

- `qa-xray-sync` maps `summary` to `scenario`.
- It maps the Test Specifications, Test Setup, Steps, and Test Teardown sections to their identically purposed Xray fields.
- It maps `categories`, `priority`, `severity`, `tolerance`, and `customFields` only when present.
- It obtains `project` from the explicit approved sync destination; do not derive it silently from `storyKey`.
- Local-only fields (`id`, `xrayKey` on create, `type`, `folder`, `testSets`, `coveredRequirements`, `storyKey`, `status`, and `data`) are never forwarded as top-level mutation properties.
- Preserve the authored expected-results arrays exactly so sync never has to split prose heuristically.

## Coverage and traceability

- Every test's `coveredRequirements` links back to `REQ-###` IDs in `requirements.md`.
- Maintain `traceability.md` as a REQ-ID to test-ID matrix so coverage gaps are visible to `qa-review-test-cases` and `qa-orchestrate-test-cases`.
- Do not create a test that covers no requirement. If a needed test has no matching requirement, raise it as a gap and route back to `qa-decompose-requirements`.

## Update / refactor / fix mode

- Detect existing test files in `<STORY-ID>/tests/`.
- Update in place, preserving `id` and `xrayKey`; never duplicate an existing test to make a change.
- Re-derive steps, fix fields, or refactor structure while keeping identity and traceability intact.
- If a refactor splits or merges tests, update `traceability.md` and clearly report the ID changes.

## ID lifecycle

- New tests mint internal `AGENT-###` IDs, story-scoped, starting at `AGENT-000`.
- `qa-xray-sync` later replaces the internal ID with the real Xray key in both the filename and the `xrayKey`/`id` frontmatter, for end-to-end traceability.

## Hard constraints

- Do not invent behavior that is not grounded in `requirements.md`.
- Do not use expressive filenames; the filename is the ID.
- Do not duplicate a test to update it.
- Do not create tests with no covered requirement.
- Do not omit mandatory fields.
- Do not proceed past the plan step without approval when running standalone.
- Do not score test quality or sync to Xray here.

## Completion condition

This skill is complete when:
- every requested test case exists as a file in `<STORY-ID>/tests/`,
- each file carries all mandatory fields and valid steps,
- `coveredRequirements` and `traceability.md` are consistent,
- and the user is pointed to `qa-review-test-cases` (or the orchestrator continues the loop).
