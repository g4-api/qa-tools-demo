# Story Metadata
- source: Jira
- story_key: GAR-10
- title: Story: Deterministic Traceability Delta Reports per Iteration
- link: https://qa-webinar.atlassian.net/browse/GAR-10
- retrieval_date: 2026-07-16
- depth_mode: full breakdown + traceability

# Atomic Testable Requirements
- REQ-000: The system shall record requirement-to-test mapping deltas for each review/fix iteration.
- REQ-001: The system shall separate delta output into added, removed, and modified mapping groups.
- REQ-002: The system shall include before/after score deltas for each affected test in each iteration report.
- REQ-003: The system shall produce deterministic delta output for identical input and execution context.

# Acceptance Criteria Mapping
- AC-001 -> REQ-000: Each review/fix iteration records requirement-to-test mapping deltas.
- AC-002 -> REQ-001: Added, removed, and modified test links are clearly separated.
- AC-003 -> REQ-002: The report includes before/after score deltas per affected test.
- AC-004 -> REQ-003: The output is reproducible for the same inputs.

# Business Rules
- BR-001: Iteration index must be monotonically increasing per story run.
- BR-002: A modified mapping is any REQ-to-test association where either side changed compared with previous iteration.

# Candidate Test Conditions
## Positive
- TC-P-001 (REQ-000): Valid iteration emits at least one delta record.
- TC-P-002 (REQ-001): Mixed changes are correctly categorized into all three groups.

## Negative
- TC-N-001 (REQ-002): Missing prior score for a changed test is reported as an explicit data-quality error.
- TC-N-002 (REQ-003): Non-deterministic ordering is detected and fails reproducibility check.

## Edge
- TC-E-001 (REQ-001): Iteration with zero changes emits empty but present delta groups.
- TC-E-002 (REQ-002): Large batch of affected tests keeps all score deltas complete.

# Non-Functional Requirements
- NFR-001: Delta report generation should complete in under 2 seconds for up to 500 changed mappings.
- NFR-002: Output ordering should be stable and deterministic.

# Gaps and Open Questions
- Clarify whether deterministic output is required across different runtime environments or only within the same environment.
- Confirm expected behavior when previous iteration data is partially unavailable.