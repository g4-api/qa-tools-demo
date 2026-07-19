---
name: qa-author-defects
description: >-
  Draft a complete defect from an approved product-defect analysis, collect available execution and requirement context,
  validate exact Jira Bug and issue-link payloads, create the defect after applicable approval, verify its mandatory link
  to the originating Xray Test, and return a synchronization receipt. Use only after manual failure analysis recommends
  a product defect and the tester explicitly approves defect creation.
---

# QA Author Defects

## Purpose

Create a complete, evidence-grounded defect with minimal tester effort, synchronize it to Jira, and verify its association
with the originating Xray Test.

Own the defect draft, Jira Bug creation, defect-to-Test issue link, read-back verification, and returned receipt. Do not
determine root cause, change the test or requirement, or update the execution journal.

## Required resources

Read these resources completely before drafting or synchronizing:

- [Defect contract](references/defect-contract.md)
- [Jira defect tool contract](references/jira-defect-tool-contract.md)

Copy [the defect template](assets/defect-template.md) when a persistent local draft is required.

Before creating or changing a defect Markdown file, read and apply `md-vanilla-style`. After every write, invoke
`md-code-compliance-review` and repair the file until it scores 100 with zero linter errors.

## Preconditions

Proceed only when all conditions are true:

1. The tester explicitly approved defect creation.
2. `qa-analyze-test-failure` classified the result as `product-defect`.
3. The failed execution, originating Xray Test key, and step are identifiable.
4. The explicit Jira destination project is known.

Return control without mutation when a precondition is missing. Do not broaden approval or infer a destination project.

## Automatic collection

Collect available facts before asking the tester:

1. Requirement and story references.
2. Originating Xray Test key, specification, setup, data, steps, and expected results.
3. Execution identifier, timestamps, actual result, and execution history.
4. Environment, build, configuration, and prerequisite facts.
5. Analysis classification, confidence, reasoning, and evidence references.
6. Relevant documentation, source references, repository links, and related defects.
7. Available screenshots, recordings, logs, traces, and console output references.

Ask only for material missing evidence or a required destination value that cannot be obtained safely.

## Drafting

Produce the defect sections required by the defect contract. Keep reproduction steps atomic and numbered. Preserve facts
from the execution record without embellishment. Distinguish analysis from directly observed behavior.

Search existing defects before creation when the available Jira tools support it. If a likely duplicate exists, show it
to the tester and ask whether to link or proceed. Never create a duplicate silently.

## Synchronization

1. Inspect the live Jira create-issue schema.
2. Select issue type `Bug` in the explicit destination project.
3. Construct a fresh payload from the schema allowlist.
4. Include only supported fields and correctly shaped custom fields.
5. Validate required properties, types, nested objects, and property allowlists.
6. Use the prior approval only when every payload value derives from approved execution facts and destination values.
7. Show the exact payload and request approval when a new material value or choice is required.
8. Execute the exact Jira create-issue tool.
9. Validate the returned key, identifier, and link when the tool contract provides them.
10. Preserve the validated Bug key as the recovery anchor; never create the Bug again during link recovery.
11. Inspect the live Jira issue-link and issue-read schemas.
12. Search for the required `Defect` relationship between the originating Xray Test and the created Bug.
13. Create the relationship only when the equivalent relationship does not already exist.
14. Read both issues back and verify the link type, issue keys, and direction.
15. Return a defect receipt to `qa-execute-manual-tests`.

The approved operation is successful only when Bug creation and link verification both succeed. Creating a Bug without a
verified originating-Test relationship is a partial result, not success.

## Association and recovery

Use the canonical semantic relationship defined by the Jira defect tool contract. The originating Xray Test is the source,
the created Bug is the target, and the supported Jira link type is `Defect`.

The tester's defect-creation approval covers this mandatory relationship when all values derive from the approved failure
context. Do not request a second approval merely to establish or verify it.

Before every link mutation, search or read the relevant Jira issues. If an equivalent link already exists, skip mutation
and verify it. After a timeout or ambiguous response, read Jira before retrying. Never recreate the Bug or duplicate the
link during recovery.

## Local artifact boundary

Store a persistent defect artifact, when requested, under:

```text
<STORY-ID>/executions/<EXECUTION-ID>/defects/<DEFECT-ID-OR-DRAFT-ID>.md
```

Use metadata-only YAML frontmatter and readable Markdown body text. Do not store a Jira request payload in the body.

Do not modify `requirements.md`, `traceability.md`, test files, or `journal.md`. Return references and the validated receipt
so the execution skill can update its journal.

## Xray boundary

Do not call `new_xray_test`, `update_xray_test`, or `new_xray_test_plan`. Those tools manage test definitions and plans,
not product defects or execution results.

## Completion

Complete with one receipt status:

- `created-and-linked` with a validated defect key and verified originating-Test relationship,
- `created-unlinked` with the created defect key, exact association failure, and recovery action,
- `drafted` when the approved local artifact exists but external creation did not run, or
- `failed` with the exact failure reason and no invented identifier.

Only `created-and-linked` is successful. Return the final summary, association receipt, and execution, test, step, and
requirement references to the execution skill.
