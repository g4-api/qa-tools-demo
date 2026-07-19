---
id: GAR-85
jiraKey: GAR-85
status: created
storyId: GAR-2
testId: GAR-79
executionId: EXEC-001
step: 3
requirements:
  - REQ-001
  - REQ-002
createdAt: 2026-07-19T11:34:14+03:00
updatedAt: 2026-07-19T11:34:56+03:00
---

# Defect

## Summary

Requirements Decomposition Engine emits duplicate `REQ-###` identifiers, so decomposed requirements are
not uniquely and stably identified.

## Problem Statement

When a Jira story that states two distinct behaviours in one sentence is decomposed, the engine produces
requirements in which some `REQ-###` identifiers repeat across different requirements. Identifiers are
expected to be stable and unique so each requirement is independently traceable and verifiable.

## Environment

1. Environment: None specified.
2. Build: None specified.

## Preconditions

1. A Jira story whose story text states two distinct behaviours in a single sentence is available.
2. The decomposition engine is reachable and accepts Jira story-text input.

## Steps to Reproduce

1. Open a Jira story whose story text states two distinct behaviours in a single sentence.
2. Start a decomposition run against the loaded Jira story text.
3. Read the atomic requirements produced from the combined sentence.
4. Inspect the `REQ-###` identifier assigned to each produced requirement.

## Expected Result

1. Each produced requirement carries a stable identifier matching the `REQ-###` pattern.
2. Each `REQ-###` identifier is unique so every requirement is independently verifiable.

## Actual Result

1. Some produced requirements share the same `REQ-###` identifier.
2. Because identifiers repeat, the affected requirements are not independently and unambiguously
    traceable.

## Impact

1. Duplicate identifiers break requirement-to-test traceability for the affected requirements.
2. Downstream test authoring and coverage mapping cannot reliably reference a single requirement by id.

## Evidence

1. None.

## Analysis Summary

1. Classification: Product defect.
2. Confidence: 74 percent.
3. Reasoning: Setup and the surrounding steps passed, establishing valid preconditions, environment, and
    data; under those valid conditions the engine emitted repeated identifiers, which contradicts the
    stable, unique identifier behaviour required by `REQ-002` and the authored expected result.

## Relevant References

1. Story: `GAR-2`.
2. Requirements: `REQ-001`, `REQ-002`.
3. Test: `GAR-79`.
4. Execution: `EXEC-001`.
5. Xray Test Execution: `GAR-84`.

## Attachments

1. None.
