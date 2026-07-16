---
id: GAR-30
xrayKey: GAR-30
type: Manual
summary: Validate deterministic delta categorization per iteration
priority: High
categories: [traceability, reporting]
severity: Major
customFields: []
folder: GAR/Traceability
testSets: []
coveredRequirements: [REQ-000, REQ-001]
storyKey: GAR-10
status: synced
---

## Test Specifications
Verify each review/fix iteration produces a delta report and correctly categorizes mapping changes into added, removed, and modified groups.

## Test Setup
```yaml
- action: Prepare prior and current iteration requirement-to-test mapping snapshots with known add/remove/modify changes.
  expectedResults:
    - Snapshot data is loaded and baseline checks pass.
```

## Steps
```yaml
- action: Run delta generation for the current iteration.
  data: prior snapshot id and current snapshot id
  expectedResults:
    - Delta report is produced for the iteration.
    - Report contains added, removed, and modified sections.
- action: Compare each emitted delta entry against expected mapping transitions.
  data: expected transition table
  expectedResults:
    - All add/remove/modify entries match expected transitions exactly.
    - No entry appears in more than one category.
```

## Test Teardown
```yaml
- action: Remove temporary snapshot fixtures.
  expectedResults:
    - Test environment returns to clean state.
```
