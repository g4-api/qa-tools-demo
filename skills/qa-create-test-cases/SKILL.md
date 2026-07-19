---
name: qa-create-test-cases
description: Generate, update, or refactor Manual Xray test cases from a requirements decomposition, as first-class per-test Markdown files with YAML frontmatter that map cleanly onto Xray's Manual test structure. Use when a QA engineer needs to author new test cases, extend coverage, or fix/refactor existing test files derived from requirements.md.
---

# QA Create Test Cases

## Purpose

This skill authors Manual Xray test cases from a `requirements.md` decomposition. It is the "create" stage of the
create / review / orchestrate trio.

Each test case is a first-class code file: atomic, ID-named, individually reviewable, and shaped so `qa-xray-sync` can
construct an exact `new_xray_test` or `update_xray_test` payload without guessing.

This skill must:
1. resolve the requirements source and working mode,
2. propose a coverage matrix and resolve coverage depth,
3. resolve the field template,
4. show a plan and wait for approval,
5. write or update one file per test case,
6. maintain the story-level traceability index.

Before writing or changing `requirements.md`, `traceability.md`, or a test `.md` file, read and apply
`md-vanilla-style`. After each write, invoke `md-code-compliance-review`, run its linter, fix every finding, and repeat
until the file scores 100 with zero linter errors.

This skill does not score test quality and does not sync to Xray. Scoring is owned by `qa-review-test-cases`; the loop is
owned by `qa-orchestrate-test-cases`; sync is owned by `qa-xray-sync`.

## Use this skill when

Use this skill when the task is about:
- creating new Manual test cases from a decomposed requirement
- extending coverage (positive / negative / edge) for existing requirements
- updating, refactoring, or fixing existing test-case files
- shaping test cases to match Xray's Manual test structure
- keeping requirement-to-test traceability current

Do not use this skill to score test quality, run the review loop, or create/update tests in Xray.

## Operating philosophy

Test artifacts are first-class code files. Author them with the developer's state of mind: atomic units, stable
identifiers, explicit traceability, no invented behavior, and review-before-execute discipline. Identity comes from IDs,
never from prose filenames.

## Interaction contract

This skill is interactive when run standalone. It always follows this base flow:

1. **Load** — triggered by the user prompt.
2. **Ask guiding questions** — resolve only what the prompt did not already specify.
3. **Show a plan** — the coverage matrix, test count, IDs, and field template.
4. **Wait for approval**.
5. **Execute** — write or update test files and the traceability index.

Whenever in doubt about coverage depth, fields, or whether to create vs update, stop and ask the user.

When invoked by `qa-orchestrate-test-cases`, this skill may run with pre-approved parameters and skip its own approval
gate, because the orchestrator owns the loop.

## Guiding questions to resolve at load

Ask only the ones the prompt left open:

1. **Requirements source** — which `<STORY-ID>/requirements.md` (or inline requirements) to work from.
2. **Coverage depth** — if the prompt did not state a level, build a proposed coverage matrix for each `REQ-###` by
    positive, negative, and edge candidate types. Ask the user to pick the depth before generating.
3. **Field template** — default to the full field set and let the user confirm or trim it. Only the mandatory Xray fields
    are hard-required.
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

Each test file is readable Markdown with one YAML metadata frontmatter block. YAML ends at the closing frontmatter marker;
do not use YAML or serialized step objects in the body. After frontmatter, use the exact `summary` value as the single
level-one heading and first nonblank body line.

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

# <required summary>

## Test Specifications
<detailed test purpose, scope, and acceptance behavior>

## Test Setup

1. **Action:** <setup action>

    **Expected results:**

    1. <observable setup result>

## Steps

1. **Action:** <single test action>

    **Test data:** <optional input data; folded into the action during Xray sync>

    **Expected results:**

    1. <first observable result>
    2. <second observable result>

## Test Teardown

1. **Action:** <teardown action>

    **Expected results:**

    1. <observable teardown result>
````

Omit an optional setup or teardown section when it has no items. Number actions from `1` without gaps and restart at `1`
in each section. Number expected results from `1` beneath their owning action. Keep test data as readable Markdown, not
YAML; `qa-xray-sync` folds it into the action because the mutation schemas have no `data` property.

### Mandatory fields (never optional)

- `summary`
- one level-one body heading that exactly matches `summary`
- `type: Manual`
- at least one numbered step with a non-empty Action and one or more numbered Expected results

Everything else is template-configurable. When the prompt does not specify a field template, default to the full set and
let the user confirm or trim it.

### Step-authoring rules

- steps are ordered, numbered, and atomic; one clear Action per step
- Action states what the tester does; optional Test data holds inputs; every numbered Expected result is verifiable
- avoid compound steps that hide multiple assertions
- negative and edge cases must make the failure/boundary condition explicit
- custom-field `name` and `value` entries are strings; names are unique within a test
- `tolerance` is a number, never a numeric string

## Xray mutation compatibility

- `qa-xray-sync` maps `summary` to `scenario`.
- The level-one body heading is the readable document title and is not forwarded as a mutation property.
- It parses numbered Test Setup, Steps, and Test Teardown actions plus their nested numbered Expected results into the
    identically purposed Xray arrays.
- It maps `categories`, `priority`, `severity`, `tolerance`, and `customFields` only when present.
- It obtains `project` from the explicit approved sync destination; do not derive it silently from `storyKey`.
- Local-only fields (`id`, `xrayKey` on create, `type`, `folder`, `testSets`, `coveredRequirements`, `storyKey`, `status`,
    and `data`) are never forwarded as top-level mutation properties.
- Preserve each authored Expected results list exactly so sync never has to split prose heuristically.

## Markdown compliance gate

- Apply `md-vanilla-style` to every generated or changed `.md` artifact.
- Require the first nonblank body line after frontmatter to be the single level-one heading (MD041).
- Invoke `md-code-compliance-review` after each write or fix.
- Treat a score below 100 or any linter finding as a failed write.
- Fix formatting without changing domain meaning, then repeat the review.
- Hand the Markdown score and findings to the orchestrator for the current per-test cycle.

## Coverage and traceability

- Every test's `coveredRequirements` links back to `REQ-###` IDs in `requirements.md`.
- Maintain `traceability.md` as a REQ-ID to test-ID matrix so coverage gaps are visible to `qa-review-test-cases` and
    `qa-orchestrate-test-cases`.
- Do not create a test that covers no requirement. If a needed test has no matching requirement, raise it as a gap and
    route back to `qa-decompose-requirements`.
- In `traceability.md`, keep YAML metadata in frontmatter only. Render the matrix as a Markdown table with a leading `#`
    enumeration column, followed by Requirement and Tests columns.
- After traceability frontmatter, use its metadata `title` as the single level-one heading before level-two sections.
- Number traceability rows from `1` without gaps and rerun Markdown compliance whenever IDs or mappings change.

## Update / refactor / fix mode

- Detect existing test files in `<STORY-ID>/tests/`.
- Update in place, preserving `id` and `xrayKey`; never duplicate an existing test to make a change.
- Re-derive steps, fix fields, or refactor structure while keeping identity and traceability intact.
- If a refactor splits or merges tests, update `traceability.md` and clearly report the ID changes.

## ID lifecycle

- New tests mint internal `AGENT-###` IDs, story-scoped, starting at `AGENT-000`.
- `qa-xray-sync` later replaces the internal ID with the real Xray key in the filename and the `xrayKey`/`id` frontmatter
    for end-to-end traceability.

## Hard constraints

- Do not invent behavior that is not grounded in `requirements.md`.
- Do not use expressive filenames; the filename is the ID.
- Do not duplicate a test to update it.
- Do not create tests with no covered requirement.
- Do not omit mandatory fields.
- Do not emit a test or traceability body whose first nonblank line is not its single level-one heading.
- Do not put YAML anywhere except metadata frontmatter.
- Do not omit action, expected-result, criterion, or requirement enumeration.
- Do not complete a write below 100 Markdown compliance or with any linter error.
- Do not proceed past the plan step without approval when running standalone.
- Do not score test quality or sync to Xray here.

## Completion condition

This skill is complete when:
- every requested test case exists as a file in `<STORY-ID>/tests/`,
- each file carries all mandatory fields and valid steps,
- `coveredRequirements` and `traceability.md` are consistent,
- every changed Markdown file scores 100 with zero linter errors,
- and the user is pointed to `qa-review-test-cases` (or the orchestrator continues the loop).
