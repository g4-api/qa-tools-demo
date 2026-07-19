---
id: GAR-81
xrayKey: GAR-81
xrayLink: https://qa-webinar.atlassian.net/browse/GAR-81
type: Manual
summary: An incomplete source yields an explicit list of gaps and ambiguities
priority: High
categories: [decomposition, gaps, ambiguity]
severity: Critical
customFields: []
folder: /GAR/GAR-2
testSets: []
coveredRequirements: [REQ-005]
storyKey: GAR-2
status: draft
---

# Test Case: [GAR-81](https://qa-webinar.atlassian.net/browse/GAR-81)

## Test Specifications

Verify that the decomposition engine explicitly lists gaps and ambiguities when the source is
incomplete, instead of inventing answers. A source that omits required detail produces an enumerated
gaps list that names each omission, and an ambiguous phrase is raised as an open question rather than
resolved into a concrete requirement. This test covers `REQ-005`.

## Test Setup

1. **Action:** Open a story source that omits a required detail and contains one ambiguous phrase.

    **Expected results:**

    1. The source loads and both the omission and the ambiguous phrase are visible.

## Steps

1. **Action:** Start a decomposition run against the loaded incomplete source.

    **Expected results:**

    1. The run completes and reports a decomposition result.
    2. The result exposes a distinct gaps and open questions section.

2. **Action:** Read the gaps and open questions produced from the source.

    **Expected results:**

    1. The gaps and open questions section is non-empty.
    2. The omitted required detail is listed as a gap.
    3. Each listed gap is individually enumerated.

3. **Action:** Locate how the ambiguous phrase was handled in the output.

    **Test data:** The ambiguous phrase in the source has more than one reasonable interpretation.

    **Expected results:**

    1. The ambiguous phrase is raised as an open question.
    2. The ambiguous phrase is not resolved into a concrete requirement.

4. **Action:** Compare the atomic requirements against the omitted detail.

    **Expected results:**

    1. No requirement supplies a value for the omitted detail that the source does not state.

## Test Teardown

1. **Action:** Discard the decomposition result produced by this test.

    **Expected results:**

    1. No artifact produced by this test remains in the workspace.
