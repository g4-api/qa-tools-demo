# Story Metadata
- source: Jira
- story_key: GAR-12
- title: Story: Story-Level Exit Criteria Dashboard for QA Readiness
- link: https://qa-webinar.atlassian.net/browse/GAR-12
- retrieval_date: 2026-07-16
- depth_mode: full breakdown + traceability

# Atomic Testable Requirements
- REQ-000: The dashboard shall show quality gate status for all tests linked to the story.
- REQ-001: The dashboard shall include a coverage table mapping REQ IDs to finalized test IDs.
- REQ-002: The dashboard shall list open blockers and unresolved requirement gaps.
- REQ-003: The dashboard output shall be directly usable in pull request descriptions without further formatting.

# Acceptance Criteria Mapping
- AC-001 -> REQ-000: Dashboard shows gate status for all tests under the story.
- AC-002 -> REQ-001: Coverage table maps REQ IDs to finalized test IDs.
- AC-003 -> REQ-002: Open blockers and unresolved requirement gaps are listed.
- AC-004 -> REQ-003: Output is PR-ready and consumable without additional formatting.

# Business Rules
- BR-001: A story cannot be marked ready if any linked test has status fail or score <=95.
- BR-002: Coverage rows must be sorted by requirement ID.

# Candidate Test Conditions
## Positive
- TC-P-001 (REQ-000): All passing tests display pass status in dashboard.
- TC-P-002 (REQ-001): Coverage table contains complete REQ-to-test mapping.

## Negative
- TC-N-001 (REQ-002): Missing blocker details trigger dashboard validation warning.
- TC-N-002 (REQ-003): Non-PR-safe formatting is detected and rejected.

## Edge
- TC-E-001 (REQ-001): Requirement with multiple tests lists all linked test IDs.
- TC-E-002 (REQ-000): Story with zero tests is displayed as not ready with explicit rationale.

# Non-Functional Requirements
- NFR-001: Dashboard render time should be under 1 second for up to 300 tests.
- NFR-002: Exported markdown should preserve table formatting in common PR platforms.

# Gaps and Open Questions
- Confirm which blocker severities must appear by default in the dashboard.
- Confirm whether archived tests should be excluded from readiness status.