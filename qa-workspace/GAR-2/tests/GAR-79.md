---
id: GAR-79
xrayKey: GAR-79
xrayLink: https://qa-webinar.atlassian.net/browse/GAR-79
type: Manual
summary: Jira story-text input decomposes into atomic requirements consistent with the Markdown path
priority: High
categories: [decomposition, authoring, jira]
severity: Critical
customFields: []
folder: /GAR/GAR-2
testSets: []
coveredRequirements: [REQ-001, REQ-002]
storyKey: GAR-2
status: draft
---

# Test Case: [GAR-79](https://qa-webinar.atlassian.net/browse/GAR-79)

## Test Specifications

Verify that the decomposition engine accepts a story supplied as Jira story text and produces atomic,
independently testable requirements the same way the Markdown path does. A Jira story that states two
distinct behaviours in one sentence is split into separate requirements, each requirement is verifiable
on its own, and content the story does not state is not emitted. This test covers `REQ-001` and
`REQ-002`.

## Test Setup

1. **Action:** Open a Jira story whose story text states two distinct behaviours in a single sentence.

    **Expected results:**

    1. The Jira story text loads and the combined sentence is visible.

## Steps

1. **Action:** Start a decomposition run against the loaded Jira story text.

    **Expected results:**

    1. The run completes and reports a decomposition result.
    2. The result is produced from the Jira story text without a source error.

2. **Action:** Read the atomic requirements produced from the combined sentence.

    **Expected results:**

    1. The combined sentence is split into two separate requirement statements.
    2. Each resulting statement describes exactly one behaviour.

3. **Action:** Inspect the identifier and verifiability of each produced requirement.

    **Expected results:**

    1. Each requirement carries a stable identifier matching the `REQ-###` pattern.
    2. Each requirement is verifiable on its own without depending on another requirement.

4. **Action:** Decompose the same behaviours expressed as a Markdown source and compare the two results.

    **Test data:** The Markdown source and the Jira story state the same two combined behaviours.

    **Expected results:**

    1. Both sources yield the same count of atomic requirements.
    2. Each Jira-derived requirement matches a Markdown-derived requirement in behaviour.

## Test Teardown

1. **Action:** Discard both decomposition results produced by this test.

    **Expected results:**

    1. No artifact produced by this test remains in the workspace.
