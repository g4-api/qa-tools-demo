---
name: qa-execute-manual-tests
description: >-
  Guide a tester through a new or resumed manual test execution in guided or bulk mode, persist an execution journal,
  collect observations and evidence references, compare actual and expected results, optionally synchronize the run to
  Xray Cloud, delegate mismatches for analysis, and resume after approved defect creation. Use when a finalized manual
  test must be run, continued, synchronized, blocked, or closed.
---

# QA Execute Manual Tests

## Purpose

Run a finalized manual test while preserving execution continuity, concise tester interaction, and human control.

Own tester interaction, step progression, result recording, and the execution journal. Do not determine root cause,
author defects, change test definitions, or participate in the authoring review loop.

## Required resources

Read these resources completely before starting an execution:

- [Execution journal contract](references/execution-journal-contract.md)
- [Execution handoff contracts](references/execution-handoff-contracts.md)

Copy [the execution journal template](assets/execution-journal-template.md) for a new execution.

Before creating or changing a journal, read and apply `md-vanilla-style`. After every write, invoke
`md-code-compliance-review` and repair the journal until it scores 100 with zero linter errors.

## Inputs

Resolve only values the request did not provide:

1. Finalized test file and test identifier.
2. Story identifier and requirement references.
3. Environment and build references.
4. Existing execution identifier when resuming.
5. Optional Xray Test Plan or Test Execution destination when synchronization was requested.

Load the test specification, requirements, traceability, linked documentation, execution history, linked defects,
environment information, and available evidence references. Treat the test and requirement files as read-only.

## Authentication identity

Use the fixed account identity configured with the Personal Access Token (PAT) as the journal tester. Never ask for a
tester name, username, password, or PAT. Never read, decode, display, or persist the PAT.

When the configured account exposes no non-secret display value, record `configured-pat-account` as the stable tester
identity. Treat authentication as environment-owned state rather than an execution input.

## Startup

1. Search `<STORY-ID>/executions/` for the requested execution or an unfinished execution of the selected test.
2. Classify the run as new or resumed.
3. For a new run, mint the next story-scoped `EXEC-###` identifier and copy the journal template.
4. For a resumed run, load the journal and continue from its recorded next action.
5. Select guided mode when the request says `step by step`, `guided`, or gives no mode.
6. Select bulk mode when the request says `bulk`, `all steps`, or an equivalent unambiguous phrase.
7. Preserve the recorded mode when resuming unless the tester explicitly requests a switch.
8. Explain that the tester may switch modes after any recorded result.

Do not silently create a second active execution for the same tester and test. Show the unfinished execution and ask
whether to resume it or begin a distinct run.

## Guided mode

1. Present exactly one unresolved step.
2. Show its step number, objective or action, test data, expected results, and relevant notes.
3. Accept a concise result or a detailed observation with evidence references.
4. Normalize a standalone `pass` as `Passed`, observation `Tester reported pass.`, and evidence `None`.
5. Require an actual observation when the tester reports failure without describing what happened.
6. Compare the observation with the expected results, requirement, and linked documentation.
7. If they match, record `Passed`, checkpoint the journal, and present the next unresolved step.
8. If they do not match, record `Analysis pending`, checkpoint the journal, and invoke `qa-analyze-test-failure`.
9. Present the analysis and ask the tester to approve the next action.
10. Record the tester's decision before continuing.

Never present the next step before the current result and next action are recorded.

Treat concise responses as an explicit interaction grammar:

- `pass` records the complete passed result described above without another evidence question.
- `fail: <observation>` records `Analysis pending` with evidence `None` unless evidence follows.
- `blocked: <reason>` and `skip: <reason>` provide the reason required for the corresponding human-control decision.
- A response containing evidence paths or links preserves those references exactly.

Do not invent an observation beyond the fixed `Tester reported pass.` normalization or infer evidence that was not
provided.

## Bulk mode

1. Present every remaining step in its authored order.
2. Ask for the overall result, per-step results, failed step numbers, observations, and evidence references.
3. Map the response to each remaining step without inventing missing results.
4. Ask for clarification when a step cannot be mapped unambiguously.
5. Record and checkpoint all mapped results.
6. Invoke `qa-analyze-test-failure` independently for each mismatched step.
7. Present each analysis and obtain a tester decision for each affected step.

Do not let an overall result replace individual step results.

## Unexpected results

Build the exact analysis handoff defined in the handoff contract. Invoke `qa-analyze-test-failure` without changing the
test, requirement, environment, or execution result.

After analysis, ask the tester to choose the next action. Supported decisions are:

- repeat the step,
- collect additional evidence,
- fix the environment or configuration,
- clarify the requirement,
- request a separate test-authoring update,
- approve defect creation,
- block the execution, or
- end the execution.

Invoke `qa-author-defects` only when the tester explicitly approves creation and analysis classifies the result as a
product defect. Pass the originating Xray Test key and the complete approved defect handoff. Record only the returned
receipt; do not draft, synchronize, or link the defect directly.

Accept `created-and-linked` as the only successful defect receipt. When the receipt is `created-unlinked`, checkpoint the
created Bug key, relationship failure, and recovery action, then return control to `qa-author-defects` for idempotent link
recovery. The existing tester approval remains valid while recovery introduces no new material value. Never create a
replacement Bug or treat a readable test reference as a Jira relationship.

When analysis identifies an incorrect expected result or needed test change, return a recommendation for a separate
`qa-create-test-cases` refactoring run. Never invoke the authoring pipeline from the active execution.

## Journal ownership

Checkpoint the journal after every tester response, analysis result, decision, defect receipt, mode change, and status
change. Persist execution facts only. Do not store conversational filler or hidden reasoning.

Record timestamps from the available system clock. Never invent a timestamp, tester observation, evidence reference,
environment value, analysis conclusion, or defect identifier.

Only this skill may update the execution journal. The analysis skill is read-only, and the defect skill returns a receipt.

## Human control

Ask the tester before:

1. Skipping a step.
2. Blocking the execution.
3. Ending an incomplete execution.
4. Creating a defect.
5. Replacing an existing execution mode.

The tester owns these decisions. This skill owns workflow consistency and persistence.

## External-system boundary

Keep execution state local unless the tester explicitly requests Xray creation or synchronization. A direct request such
as `create execution on Xray` authorizes the required non-destructive execution mutations; do not ask for duplicate
approval when all payload values come from the journal, finalized test, configured destination, or tool responses.

Invoke `qa-xray-sync` for Xray persistence and pass the journal as read-only source data. Require the sync skill to return
a receipt; only this skill writes that receipt into the journal.

For a new Xray-backed execution:

1. Call `new_xray_execution` with every in-scope Test key so Xray creates real Test Runs.
2. Call `add_xray_test_executions_to_plan` when a Test Plan destination was supplied.
3. Record each terminal authored step through `update_xray_execution_step` using the one-based authored step number.
4. Call `update_xray_test_run_status` after every terminal local Test result is known.
5. Persist the returned execution key, Test Run identifier, confirmed step, status, and warnings in the journal.

For an existing Xray Test Execution, call `add_xray_tests_to_execution` before recording results. Never represent Xray
execution membership with a generic Jira issue link or a description-only summary. Stop with the exact missing tool when
a required dedicated mutation is unavailable.

## Completion

Complete when every step has a tester-owned terminal result and the journal status is `completed`, or when the tester
explicitly blocks or ends the run and the journal records the reason and next action.

When Xray synchronization was requested, complete only after the journal contains a successful receipt or an explicit
sync failure with its next action.

When the tester approved a product defect, complete only after its receipt is `created-and-linked`, or after the journal
records a tester-owned decision to end or block the execution with the unresolved association and its next action.

Return the execution identifier, test identifier, status, result counts, Xray execution receipt, linked defects, journal
path, and next action.
