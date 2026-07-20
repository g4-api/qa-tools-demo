---
id: AGENT-000
xrayKey: null
xrayLink: null
type: Manual
summary: Conforming manual test file exposes objective, preconditions, steps, and expected results
priority: High
categories: [authoring, structure, metadata]
severity: Critical
customFields: []
folder: /GAR/GAR-3
testSets: []
coveredRequirements: [REQ-000, REQ-001, REQ-002, REQ-003]
storyKey: GAR-3
status: draft
---

# Test Case: AGENT-000

## Test Specifications

Verify that a conforming manual test case file carries all four mandatory sections and is accepted as
complete. The file must state a test objective, list its preconditions as a test setup, present ordered
execution steps, and state expected results for those steps. This test covers `REQ-000`, `REQ-001`,
`REQ-002`, and `REQ-003`.

## Test Setup

1. **Action:** Open a manual test case file that was authored against the standardized format.

    **Expected results:**

    1. The file opens and its metadata frontmatter and body sections are readable.

## Steps

1. **Action:** Read the objective section of the test case file.

    **Expected results:**

    1. The file states a single test objective that describes what the test verifies.

2. **Action:** Read the preconditions stated as the test setup.

    **Expected results:**

    1. The file lists at least one precondition as an ordered test-setup action.

3. **Action:** Read the execution steps of the test case file.

    **Expected results:**

    1. The file presents the steps as an ordered list numbered from one without gaps.
    2. Each step states exactly one tester action.

4. **Action:** Read the expected results attached to the steps.

    **Expected results:**

    1. Every step carries at least one numbered expected result.
    2. Each expected result is stated as an observable outcome.

5. **Action:** Confirm that all four mandatory sections are present together.

    **Expected results:**

    1. The objective, preconditions, steps, and expected results are all present in the same file.
    2. The file is accepted as a conforming, complete test case.

## Test Teardown

1. **Action:** Close the test case file without changing it.

    **Expected results:**

    1. The file remains unchanged after the review.
</content>
