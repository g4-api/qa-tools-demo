---
id: GAR-32
xrayKey: GAR-32
type: Manual
summary: Validate dashboard gate status and coverage mapping
priority: High
categories: [dashboard, readiness]
severity: Major
customFields: []
folder: GAR/Readiness
testSets: []
coveredRequirements: [REQ-000, REQ-001]
storyKey: GAR-12
status: synced
---

## Test Specifications
Verify the story-level dashboard renders accurate test gate states and complete REQ-to-test coverage mappings.

## Test Setup
```yaml
- action: Seed story with tests across pass and fail gate states and a complete requirement mapping.
  expectedResults:
    - Story dataset is available with deterministic gate outcomes.
```

## Steps
```yaml
- action: Open dashboard for target story.
  data: story key GAR-12
  expectedResults:
    - Dashboard loads successfully.
    - All linked tests are listed with their gate status.
- action: Validate gate-status aggregation rules.
  data: expected readiness state based on seeded scores
  expectedResults:
    - Story readiness is fail when any test is <=95.
    - Story readiness is pass only when all tests are >95.
- action: Validate coverage mapping table.
  data: expected REQ-to-test matrix
  expectedResults:
    - Every requirement is present in the table.
    - Each row lists correct finalized test IDs.
```

## Test Teardown
```yaml
- action: Remove seeded dashboard test data.
  expectedResults:
    - Dashboard fixtures are fully cleared.
```
