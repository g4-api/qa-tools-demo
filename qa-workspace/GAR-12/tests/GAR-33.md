---
id: GAR-33
xrayKey: GAR-33
type: Manual
summary: Validate blocker visibility and PR-ready output format
priority: Medium
categories: [dashboard, reporting]
severity: Major
customFields: []
folder: GAR/Readiness
testSets: []
coveredRequirements: [REQ-002, REQ-003]
storyKey: GAR-12
status: synced
---

## Test Specifications
Ensure the dashboard reports open blockers and unresolved requirement gaps and exports PR-ready markdown without manual cleanup.

## Test Setup
```yaml
- action: Seed story with open blockers, requirement gaps, and representative dashboard data.
  expectedResults:
    - Blockers and gaps are persisted for the story.
```

## Steps
```yaml
- action: Render dashboard and inspect blocker and gap sections.
  data: seeded blocker and gap records
  expectedResults:
    - Open blockers are listed with clear status and identifier.
    - Unresolved requirement gaps are listed and distinguishable from blockers.
- action: Export dashboard output in markdown format.
  data: export destination for PR body
  expectedResults:
    - Export includes headings, tables, and lists with valid markdown syntax.
    - Export does not require additional manual formatting before PR use.
- action: Paste exported markdown into PR preview context.
  data: markdown preview renderer
  expectedResults:
    - Layout remains readable and structurally correct.
```

## Test Teardown
```yaml
- action: Delete seeded blockers and gap fixtures.
  expectedResults:
    - No temporary blocker or gap data remains.
```
