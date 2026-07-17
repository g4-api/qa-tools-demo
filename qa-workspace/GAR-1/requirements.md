---
sourceType: jira
source: GAR-1
storyKey: GAR-1
title: Mock Epic - Unified Test Case Lifecycle for QA Artifacts
link: https://qa-webinar.atlassian.net/browse/GAR-1
retrievedAt: 2026-07-17
depthMode: full
---

## Atomic testable requirements

1. **REQ-000:** Requirements can be decomposed into atomic, testable statements.
2. **REQ-001:** Manual test cases are generated with consistent structure and metadata.
3. **REQ-002:** Test cases are review-scored against an explicit quality threshold.
4. **REQ-003:** Approved tests can be synchronized with Xray and mapped to Jira stories.
5. **REQ-004:** A final coverage summary and a review-ready pull-request package can be produced.

## Acceptance criteria

1. **AC-000** (`REQ-000`): A requirement source yields statements that are each atomic and testable.
2. **AC-001** (`REQ-001`): Generated manual test cases share a consistent structure and metadata shape.
3. **AC-002** (`REQ-002`): Each test case carries a review score judged against an explicit threshold.
4. **AC-003** (`REQ-003`): An approved test is synchronized to Xray and mapped to its Jira story.
5. **AC-004** (`REQ-004`): The workflow produces a coverage summary and a review-ready package.

## Business rules

1. The workflow runs end to end: decompose, author, review, synchronize, then package.
2. A test case reaches synchronization only after it is approved by the review stage.
3. Traceability links generated test cases back to the decomposed requirements.
4. The workflow never invents requirements that the source does not state.

## Candidate test conditions

### Positive conditions

1. A requirement source is decomposed into atomic, testable statements (`REQ-000`).
2. Generated test cases share one structure and metadata shape (`REQ-001`).
3. A scored test case reports its score against the explicit threshold (`REQ-002`).
4. An approved test is synchronized to Xray and mapped to its story (`REQ-003`).
5. A completed run produces a coverage summary and a review-ready package (`REQ-004`).

### Negative conditions

1. A non-atomic or untestable statement is not accepted as a decomposed requirement (`REQ-000`).
2. A test case that fails the quality threshold is not treated as approved (`REQ-002`).
3. An unapproved test case is not synchronized to Xray (`REQ-002`, `REQ-003`).

### Edge conditions

1. A test case scoring exactly at the threshold is judged by the explicit rule (`REQ-002`).
2. A run whose requirements are only partly covered reports the shortfall in its summary (`REQ-004`).

## Non-functional requirements

1. The workflow improves QA consistency and traceability across runs.
2. The workflow reduces cycle time for test authoring and review.
3. The workflow increases confidence in coverage before release.

## Gaps and open questions

1. The epic does not state the numeric value of the explicit quality threshold.
2. The epic does not define what "consistent structure and metadata" requires concretely.
3. The epic does not state which Jira link type maps a synchronized test to its story.
4. The epic does not define the contents of the review-ready pull-request package.
5. The epic states three business-value outcomes without measurable targets, so they are not
    independently testable as written.
