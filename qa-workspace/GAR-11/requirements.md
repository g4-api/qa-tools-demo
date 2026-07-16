# Story Metadata
- source: Jira
- story_key: GAR-11
- title: Story: Exception-Safe Xray Sync Recovery Workflow
- link: https://qa-webinar.atlassian.net/browse/GAR-11
- retrieval_date: 2026-07-16
- depth_mode: full breakdown + traceability

# Atomic Testable Requirements
- REQ-000: The system shall classify sync failures into validation, transport, and schema mismatch categories.
- REQ-001: The system shall provide actionable recovery steps including next action and impacted test IDs.
- REQ-002: The system shall reconcile local AGENT IDs to Xray keys after successful create operations.
- REQ-003: The system shall prevent partial local identifier mutation when sync fails.

# Acceptance Criteria Mapping
- AC-001 -> REQ-000: Sync errors are classified by validation, transport, and schema mismatch causes.
- AC-002 -> REQ-001: Recovery instructions include exact next action and impacted test IDs.
- AC-003 -> REQ-002: Successful creates always reconcile local AGENT IDs to Xray keys.
- AC-004 -> REQ-003: Failed sync attempts never partially mutate local identifiers.

# Business Rules
- BR-001: Error classification must be mutually exclusive for a single failure event.
- BR-002: Recovery guidance must include at least one executable next step.

# Candidate Test Conditions
## Positive
- TC-P-001 (REQ-000): Validation error is classified correctly.
- TC-P-002 (REQ-002): Successful create renames local test ID to returned Xray key.

## Negative
- TC-N-001 (REQ-001): Missing impacted test IDs causes recovery output validation failure.
- TC-N-002 (REQ-003): Mid-operation failure attempts partial rename and is rolled back.

## Edge
- TC-E-001 (REQ-000): Unknown error shape falls back to explicit schema mismatch classification.
- TC-E-002 (REQ-003): Multi-test batch where one test fails leaves all unresolved tests unchanged.

# Non-Functional Requirements
- NFR-001: Recovery generation should complete within 1 second after error detection.
- NFR-002: Identifier reconciliation should be atomic per test file.

# Gaps and Open Questions
- Confirm whether transport timeout and DNS failures must map to the same transport category.
- Confirm if rollback should preserve temporary logs or remove them after failure.