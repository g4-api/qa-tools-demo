---
name: qa-execute-manual-tests
description: >-
  Guide a tester through a new or resumed manual test execution in guided or bulk mode, persist an execution journal,
  collect observations and evidence references, compare actual and expected results, delegate mismatches for analysis,
  and resume after approved defect creation. Use when a finalized manual test must be run, continued, blocked, or closed.
---

# QA Execute Manual Tests

## Purpose

Run a finalized manual test with the tester while preserving execution continuity and human control.

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
3. Tester identity when the execution record requires it.
4. Environment and build references.
5. Existing execution identifier when resuming.

Load the test specification, requirements, traceability, linked documentation, execution history, linked defects,
environment information, and available evidence references. Treat the test and requirement files as read-only.

## Startup

1. Search `<STORY-ID>/executions/` for the requested execution or an unfinished execution of the selected test.
2. Classify the run as new or resumed.
3. For a new run, mint the next story-scoped `EXEC-###` identifier and copy the journal template.
4. For a resumed run, load the journal and continue from its recorded next action.
5. Always ask the tester to select guided or bulk mode, showing the recorded mode when resuming.
6. Explain that the tester may switch modes after any recorded result.

Do not silently create a second active execution for the same tester and test. Show the unfinished execution and ask
whether to resume it or begin a distinct run.

## Guided mode

1. Present exactly one unresolved step.
2. Show its step number, objective or action, test data, expected results, and relevant notes.
3. Wait for the tester's observation and evidence references.
4. Compare the observation with the expected results, requirement, and linked documentation.
5. If they match, record `Passed`, checkpoint the journal, and present the next unresolved step.
6. If they do not match, record `Analysis pending`, checkpoint the journal, and invoke `qa-analyze-test-failure`.
7. Present the analysis and ask the tester to approve the next action.
8. Record the tester's decision before continuing.

Never present the next step before the current result and next action are recorded.

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
product defect. Pass the approved defect handoff. Record only the returned receipt; do not draft or synchronize the
defect directly.

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

The available Xray tools create and update test definitions and Test Plans. They do not create Test Executions or update
test-run results. Never call `new_xray_test`, `update_xray_test`, or `new_xray_test_plan` to persist execution state.

Keep execution state local until dedicated Xray execution tools and exact contracts are available.

## Completion

Complete when every step has a tester-owned terminal result and the journal status is `completed`, or when the tester
explicitly blocks or ends the run and the journal records the reason and next action.

Return the execution identifier, test identifier, status, result counts, linked defects, journal path, and next action.
