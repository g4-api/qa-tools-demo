---
id: GAR-87
jiraKey: GAR-87
status: created-and-linked
storyId: GAR-2
testId: GAR-78
executionId: EXEC-002
step: 2
requirements:
  - REQ-000
  - REQ-002
jiraLinkType: Defect
jiraLinkDirection: test-created-defect
jiraLinkStatus: verified
jiraLinkVerifiedAt: 2026-07-20T21:12:18+03:00
createdAt: 2026-07-20T21:11:51+03:00
updatedAt: 2026-07-20T21:12:18+03:00
---

# Defect

## Summary

The Requirements Decomposition Engine does not split a combined multi-behaviour Markdown sentence into
two atomic requirements, so a single requirement continues to carry two behaviours.

## Problem Statement

When a Markdown story source states two distinct behaviours in a single sentence, the decomposition engine
leaves the sentence as one combined requirement instead of producing two atomic, independently testable
requirements.

## Environment

1. Environment: Local / Dev.
2. Build: None specified.

## Preconditions

1. A Markdown story source whose text states two distinct behaviours in a single sentence is available.
2. The decomposition engine is reachable and accepts Markdown input.

## Steps to Reproduce

1. Open a Markdown story source whose text states two distinct behaviours in a single sentence.
2. Start a decomposition run against the loaded Markdown source.
3. Read the atomic requirements produced from the combined sentence.

## Expected Result

1. The combined sentence is split into two separate requirement statements.
2. Each resulting statement describes exactly one behaviour.

## Actual Result

1. The combined sentence stayed as a single combined requirement.
2. No split into two separate single-behaviour statements was produced.

## Impact

1. A combined multi-behaviour requirement is not independently testable, violating the atomicity required by
    `REQ-002`.
2. Downstream test authoring and per-behaviour coverage cannot reference a single atomic requirement.

## Evidence

1. None.

## Analysis Summary

1. Classification: Product defect.
2. Confidence: 70 percent.
3. Reasoning: The passing setup and main step 1 established valid preconditions, data, and a successful
    engine run; under those valid conditions the engine still left the combined sentence unsplit,
    contradicting the atomic-requirement behaviour required by `REQ-002` and the authored expected result.
    The same test passed in `EXEC-000`, and no build identifier was captured, so a regression or a local
    build or configuration issue cannot be fully excluded.

## Relevant References

1. Story: `GAR-2`.
2. Requirements: `REQ-000`, `REQ-002`.
3. Test: `GAR-78`.
4. Execution: `EXEC-002`.
5. Xray Test Execution: `GAR-86`.
6. Related defect, not a duplicate: `GAR-85` (duplicate `REQ-###` identifiers for Jira story-text input).

## Jira Association

1. Originating Xray Test: `GAR-78`.
2. Created Bug: `GAR-87`.
3. Link type: `Defect`.
4. Direction: Test `created` Bug.
5. Verification status: Verified.
6. Read-back evidence: `GAR-78` shows `GAR-87` as its inward `created by` issue, and `GAR-87` shows `GAR-78`
    as its outward `created` issue, both under Defect link type id `10007`.

## Attachments

1. None.
</content>
</invoke>
