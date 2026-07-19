---
id: GAR-59
xrayKey: GAR-59
xrayLink: https://qa-webinar.atlassian.net/browse/GAR-59
type: Manual
summary: Approved tests synchronize to Xray, map to their story, and produce a coverage and PR package
priority: High
categories: [lifecycle, sync, coverage]
severity: Critical
customFields: []
folder: /GAR/GAR-1
testSets: []
coveredRequirements: [REQ-003, REQ-004]
storyKey: GAR-1
status: draft
---

# Test Case: [GAR-59](https://qa-webinar.atlassian.net/browse/GAR-59)

## Test Specifications

Verify the delivery half of the lifecycle. An approved test case is synchronized to Xray and mapped to
its Jira story, an unapproved test case is withheld from synchronization, and the completed run produces
a coverage summary and a review-ready pull-request package that reports any shortfall. This test covers
`REQ-003` and `REQ-004`.

## Test Setup

1. **Action:** Open a workspace holding one test case approved by the review stage and one test case
    rejected by it.

    **Expected results:**

    1. The workspace loads and both test cases are visible.
    2. Exactly one test case is marked as approved.

2. **Action:** Record the current Xray test count for the target project.

    **Expected results:**

    1. The Xray test count is reported and recorded.

## Steps

1. **Action:** Start a synchronization run against the workspace.

    **Expected results:**

    1. The run completes and reports a synchronization result.
    2. The result reports exactly one test as synchronized.

2. **Action:** Read the synchronization entry for the approved test case.

    **Expected results:**

    1. The entry reports a real Xray key for the approved test case.
    2. The approved test case is mapped to the Jira story it was authored from.

3. **Action:** Read the synchronization entry for the rejected test case.

    **Expected results:**

    1. The rejected test case is absent from the synchronized set.
    2. The result states that the test case was withheld because it was not approved.

4. **Action:** Read the Xray test count and compare it against the recorded value.

    **Test data:** The workspace held exactly one approved test case before the run.

    **Expected results:**

    1. The Xray test count increased by exactly `1`.

5. **Action:** Open the coverage summary produced by the completed run.

    **Expected results:**

    1. The summary lists every decomposed requirement of the story.
    2. The summary names the test cases covering each requirement.
    3. The summary marks any requirement that no test case covers.
    4. The summary reports a coverage percentage for the story.

6. **Action:** Open the review-ready pull-request package produced by the completed run.

    **Expected results:**

    1. The package includes the coverage summary.
    2. The package includes the per-test review scores.
    3. The package reports the synchronized Xray keys.

## Test Teardown

1. **Action:** Remove the synchronized Xray test and discard the coverage summary and the package.

    **Expected results:**

    1. The Xray test count matches the recorded pre-run value.
    2. No artifact produced by this test remains in the workspace.
