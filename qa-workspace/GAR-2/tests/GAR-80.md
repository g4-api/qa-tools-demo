---
id: GAR-80
xrayKey: GAR-80
xrayLink: https://qa-webinar.atlassian.net/browse/GAR-80
type: Manual
summary: Decomposition output includes grounded business rules and non-functional requirements
priority: High
categories: [decomposition, business-rules, nfr]
severity: Critical
customFields: []
folder: /GAR/GAR-2
testSets: []
coveredRequirements: [REQ-003, REQ-004]
storyKey: GAR-2
status: draft
---

# Test Case: [GAR-80](https://qa-webinar.atlassian.net/browse/GAR-80)

## Test Specifications

Verify that the decomposition output includes business rules and non-functional requirements derived
from the input, and that both are grounded in the source. When the source states a non-functional
requirement it appears in the output, and when the source states none the output reports the absence
rather than inventing one. This test covers `REQ-003` and `REQ-004`.

## Test Setup

1. **Action:** Open a story source that states one business rule and one non-functional requirement.

    **Expected results:**

    1. The source loads and both the business rule and the non-functional requirement are visible.

## Steps

1. **Action:** Start a decomposition run against the loaded source.

    **Expected results:**

    1. The run completes and reports a decomposition result.
    2. The result exposes a distinct business rules section and a distinct non-functional requirements
        section.

2. **Action:** Read the business rules produced from the source.

    **Expected results:**

    1. The business rule stated in the source appears in the business rules section.
    2. Every listed business rule traces to a statement present in the source.

3. **Action:** Read the non-functional requirements produced from the source.

    **Expected results:**

    1. The non-functional requirement stated in the source appears in the non-functional requirements
        section.
    2. Every listed non-functional requirement traces to a statement present in the source.

4. **Action:** Decompose a second source that states no non-functional requirement and read its output.

    **Test data:** The second source contains functional behaviour only and states no non-functional
    requirement.

    **Expected results:**

    1. The non-functional requirements section is empty or marked as none.
    2. No non-functional requirement absent from the second source is invented in the output.

## Test Teardown

1. **Action:** Discard both decomposition results produced by this test.

    **Expected results:**

    1. No artifact produced by this test remains in the workspace.
