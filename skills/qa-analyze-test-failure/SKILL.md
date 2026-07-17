---
name: qa-analyze-test-failure
description: >-
  Investigate and classify an unexpected manual test result from requirements, expected and actual behavior, evidence,
  environment, documentation, source, prior executions, and existing defects. Use when manual execution finds a mismatch
  and needs a read-only, evidence-grounded explanation and advisory next action without changing execution or creating a defect.
---

# QA Analyze Test Failure

## Purpose

Determine the most probable explanation for one unexpected manual test result. Produce analysis only.

Do not modify an execution, test, requirement, environment, source file, configuration, or external system. Do not create
or draft a defect.

## Required resource

Read [the failure classification rubric](references/failure-classification-rubric.md) completely before classifying a result.

## Input contract

Require the analysis request defined by
`qa-execute-manual-tests/references/execution-handoff-contracts.md`. Stop and return `insufficient-evidence` when expected
or actual behavior is absent. Never fill missing fields with assumptions presented as facts.

## Investigation order

Inspect available evidence in this order:

1. Exact expected and actual results for the failed step.
2. Applicable requirement and acceptance behavior.
3. Test preconditions, setup, data, and prior steps.
4. Environment, build, configuration, and dependencies.
5. Linked product documentation and known limitations.
6. Relevant logs, traces, screenshots, recordings, and console output.
7. Relevant source code and configuration references.
8. Comparable previous executions.
9. Existing defects and possible duplicates.

Distinguish direct evidence from inference. Cite file paths, line numbers, log timestamps, issue keys, or evidence references
when available.

## Classification

Select exactly one classification from the rubric. Do not classify a mismatch as a product defect merely because the
expected and actual results differ.

Assign a confidence percentage from 0 through 100. Confidence measures support for the classification, not severity or
business impact.

## Recommendation

Select exactly one advisory next action:

- repeat the test,
- collect additional evidence,
- update the test in a separate authoring process,
- raise a defect after tester approval,
- clarify the requirement,
- fix the environment,
- fix the configuration, or
- satisfy the missing prerequisite.

The tester approves the next action. Do not execute it.

## Output contract

Return these sections in readable text:

1. Classification.
2. Confidence percentage.
3. Reasoning.
4. Supporting evidence.
5. Missing evidence.
6. Possible duplicate defects.
7. Recommended next action.

Use `None` when an optional section has no grounded value. Never invent evidence or suppress contradictory evidence.

## Completion

Complete when one evidence-grounded classification, confidence percentage, and advisory action are returned to the
execution skill without changing any state.
