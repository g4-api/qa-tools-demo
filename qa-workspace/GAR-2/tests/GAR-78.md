---
id: GAR-78
xrayKey: GAR-78
xrayLink: https://qa-webinar.atlassian.net/browse/GAR-78
type: Manual
summary: Markdown story input decomposes into atomic, independently testable requirements
priority: High
categories: [decomposition, authoring, markdown]
severity: Critical
customFields: []
folder: /GAR/GAR-2
testSets: []
coveredRequirements: [REQ-000, REQ-002]
storyKey: GAR-2
status: draft
---

# Test Case: [GAR-78](https://qa-webinar.atlassian.net/browse/GAR-78)

## Test Specifications

Verify that the decomposition engine accepts a story supplied as a Markdown document and produces
atomic, independently testable requirements. A Markdown source that states two distinct behaviours in
one sentence is split into separate requirements, each requirement is verifiable on its own, and content
the source does not state is not emitted. This test covers `REQ-000` and `REQ-002`.

## Test Setup

1. **Action:** Open a Markdown story source whose text states two distinct behaviours in a single
    sentence.

    **Expected results:**

    1. The Markdown source loads and the combined sentence is visible.

## Steps

1. **Action:** Start a decomposition run against the loaded Markdown source.

    **Expected results:**

    1. The run completes and reports a decomposition result.
    2. The result is produced from the Markdown source without a format error.

2. **Action:** Read the atomic requirements produced from the combined sentence.

    **Expected results:**

    1. The combined sentence is split into two separate requirement statements.
    2. Each resulting statement describes exactly one behaviour.

3. **Action:** Inspect the identifier and verifiability of each produced requirement.

    **Expected results:**

    1. Each requirement carries a stable identifier matching the `REQ-###` pattern.
    2. Each requirement is verifiable on its own without depending on another requirement.

4. **Action:** Compare the produced requirements against the content of the Markdown source.

    **Test data:** The Markdown source states only the two behaviours combined in the setup sentence.

    **Expected results:**

    1. Every produced requirement traces to a statement present in the Markdown source.
    2. No requirement introduces a behaviour that the Markdown source does not state.

## Test Teardown

1. **Action:** Discard the decomposition result produced by this test.

    **Expected results:**

    1. No artifact produced by this test remains in the workspace.
