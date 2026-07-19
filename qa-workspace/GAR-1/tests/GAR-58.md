---
id: GAR-58
xrayKey: GAR-58
type: Manual
summary: Requirements decompose into atomic statements that yield structured, review-scored test cases
priority: High
categories: [lifecycle, authoring, review]
severity: Critical
customFields: []
folder: /GAR/GAR-1
testSets: []
coveredRequirements: [REQ-000, REQ-001, REQ-002]
storyKey: GAR-1
status: draft
---

# Requirements decompose into atomic statements that yield structured, review-scored test cases

## Test Specifications

Verify the authoring half of the lifecycle. A requirement source is decomposed into atomic, testable
statements; manual test cases are generated from those statements with a consistent structure and
metadata shape; and each generated test case is review-scored against an explicit quality threshold.
This test covers `REQ-000`, `REQ-001`, and `REQ-002`.

## Test Setup

1. **Action:** Open a requirement source that states two distinct behaviours in a single sentence.

    **Expected results:**

    1. The requirement source loads and the combined sentence is visible.

## Steps

1. **Action:** Start a decomposition run against the loaded requirement source.

    **Expected results:**

    1. The run completes and reports a decomposition result.
    2. The combined sentence is split into two separate requirement statements.
    3. Each resulting statement describes exactly one behaviour.

2. **Action:** Read each decomposed statement and check that it can be verified on its own.

    **Expected results:**

    1. Each statement carries a stable identifier matching the `REQ-###` pattern.
    2. Each statement is verifiable without depending on another statement.

3. **Action:** Generate manual test cases from the decomposition result.

    **Test data:** The decomposition result holds the two statements produced in step 1.

    **Expected results:**

    1. The run completes and reports at least one generated test case per statement.
    2. Each generated test case declares a summary, a type, and at least one step.
    3. Each generated test case cites the requirement identifiers it covers.

4. **Action:** Compare the structure and metadata fields of the generated test cases against each other.

    **Expected results:**

    1. Every generated test case exposes the same metadata field set.
    2. Every generated test case orders its metadata fields identically.
    3. Every generated test case renders its steps under the same section headings.

5. **Action:** Start a review-scoring run against the generated test cases.

    **Test data:** The review stage applies an explicit quality threshold to the weighted score.

    **Expected results:**

    1. The run completes and reports one score per generated test case.
    2. Each reported score is compared against the explicit threshold.
    3. Each test case is marked as passing or failing according to that comparison.

6. **Action:** Read the review result for a test case whose score does not exceed the threshold.

    **Expected results:**

    1. The test case is not marked as approved.
    2. The review result reports the issues that held the score below the threshold.

## Test Teardown

1. **Action:** Discard the decomposition result, the generated test cases, and the review results.

    **Expected results:**

    1. No artifact produced by this test remains in the workspace.
