---
id: GAR-82
xrayKey: GAR-82
xrayLink: https://qa-webinar.atlassian.net/browse/GAR-82
type: Manual
summary: Contradictory source input is recorded as a gap and is not silently resolved
priority: High
categories: [decomposition, gaps, negative]
severity: Critical
customFields: []
folder: /GAR/GAR-2
testSets: []
coveredRequirements: [REQ-002, REQ-005]
storyKey: GAR-2
status: draft
---

# Test Case: [GAR-82](https://qa-webinar.atlassian.net/browse/GAR-82)

## Test Specifications

Verify that when the source contains two contradictory statements the engine records the contradiction
as a gap rather than silently choosing one interpretation, and that a non-atomic combined statement is
not accepted as a single requirement. This exercises the boundary between valid decomposition and
gap reporting. This test covers `REQ-002` and `REQ-005`.

## Test Setup

1. **Action:** Open a story source that contains two directly contradictory statements about the same
    behaviour.

    **Expected results:**

    1. The source loads and both contradictory statements are visible.

## Steps

1. **Action:** Start a decomposition run against the loaded contradictory source.

    **Expected results:**

    1. The run completes and reports a decomposition result.
    2. The result exposes a distinct gaps and open questions section.

2. **Action:** Read how the contradiction was handled in the output.

    **Expected results:**

    1. The contradiction between the two statements is listed as a gap or open question.
    2. Neither contradictory statement is emitted as a resolved atomic requirement.

3. **Action:** Confirm the engine did not pick one side of the contradiction on its own.

    **Test data:** The two statements assert opposite outcomes for the same behaviour.

    **Expected results:**

    1. The output does not present either outcome as the decided requirement.
    2. The output attributes the unresolved decision to the tester rather than the engine.

4. **Action:** Add a non-atomic sentence that combines two behaviours and decompose the source again.

    **Expected results:**

    1. The combined sentence is not accepted as a single atomic requirement.
    2. The combined sentence is either split into atomic requirements or listed as a gap.

## Test Teardown

1. **Action:** Discard every decomposition result produced by this test.

    **Expected results:**

    1. No artifact produced by this test remains in the workspace.
