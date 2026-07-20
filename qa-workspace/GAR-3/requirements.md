---
sourceType: jira
source: GAR-3
storyKey: GAR-3
title: Feature 2 - Structured Manual Test Authoring
link: https://qa-webinar.atlassian.net/browse/GAR-3
retrievedAt: 2026-07-20
depthMode: full
---

# Feature 2 - Structured Manual Test Authoring

## Atomic testable requirements

1. **REQ-000:** A manual test case file states a test objective or specification.
2. **REQ-001:** A manual test case file states its preconditions as a test setup.
3. **REQ-002:** A manual test case file states its execution steps in explicit order.
4. **REQ-003:** A manual test case file states expected results for its steps.
5. **REQ-004:** The test case file format links a test to the requirement identifiers it covers.
6. **REQ-005:** The test case naming convention is deterministic, so the same test yields the same
    identifier.
7. **REQ-006:** The test case naming convention yields an identifier that is unique across tests.

## Acceptance criteria

1. **AC-000** (`REQ-000`, `REQ-001`, `REQ-002`, `REQ-003`): Each test includes an objective,
    preconditions, steps, and expected results.
2. **AC-001** (`REQ-004`): The file format supports traceability to requirement identifiers.
3. **AC-002** (`REQ-005`, `REQ-006`): The naming convention is deterministic and unique.

## Business rules

1. Every manual test case file carries the same four mandatory sections: objective, preconditions,
    steps, and expected results.
2. A test case file that omits any mandatory section is non-conforming.
3. Every manual test case records the requirement identifiers it covers in a traceable field.
4. A test that covers more than one requirement records every covered requirement identifier.
5. The naming convention derives an identifier deterministically from stable test inputs.
6. Two distinct tests never resolve to the same identifier.

## Candidate test conditions

### Positive conditions

1. A conforming test file that contains objective, preconditions, steps, and expected results is
    accepted as complete (`REQ-000`, `REQ-001`, `REQ-002`, `REQ-003`).
2. A test file records the requirement identifier it covers so the requirement traces to the test
    (`REQ-004`).
3. Generating an identifier for the same test twice yields the same identifier (`REQ-005`).

### Negative conditions

1. A test file that omits a mandatory section is reported as non-conforming (`REQ-000`, `REQ-001`,
    `REQ-002`, `REQ-003`).
2. A new test that would reuse an existing identifier is not accepted as unique (`REQ-006`).

### Edge conditions

1. A test that covers several requirements records every covered requirement identifier rather than
    only the first (`REQ-004`).

## Non-functional requirements

1. The test case file format stays consistent across every authored manual test.
2. The test case identifiers remain traceable back to the covered requirements.

## Gaps and open questions

1. The story does not define the concrete metadata schema each test file must carry.
2. The story does not define the exact algorithm that derives a deterministic identifier.
3. The story does not state whether traceability is expressed as frontmatter metadata or inline text.
4. The story does not define how a duplicate identifier is detected or rejected.
5. The story does not state which mandatory sections, if any, may be empty for a valid test.
</content>
