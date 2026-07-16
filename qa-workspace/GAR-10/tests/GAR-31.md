---
id: GAR-31
xrayKey: GAR-31
type: Manual
summary: Validate score-delta completeness and reproducibility
priority: High
categories: [traceability, scoring]
severity: Critical
customFields: []
folder: GAR/Traceability
testSets: []
coveredRequirements: [REQ-002, REQ-003]
storyKey: GAR-10
status: synced
---

## Test Specifications
Ensure delta reports include before/after score changes for all impacted tests and remain deterministic for repeated identical runs.

## Test Setup
```yaml
- action: Seed affected tests with baseline and updated scores and stable input fixtures.
  expectedResults:
    - All impacted tests have baseline and current score values.
```

## Steps
```yaml
- action: Execute report generation twice using identical inputs and execution settings.
  data: fixed fixture set and execution seed
  expectedResults:
    - Two report outputs are generated successfully.
- action: Validate score-delta section for each impacted test.
  data: impacted test list with expected before/after values
  expectedResults:
    - Every impacted test includes before and after score values.
    - Reported score deltas match expected numeric differences.
- action: Compare the two generated outputs byte-for-byte.
  data: report output A and report output B
  expectedResults:
    - Outputs are identical in ordering and content.
```

## Test Teardown
```yaml
- action: Clear seeded score fixtures.
  expectedResults:
    - No test score fixtures remain.
```
