---
id: GAR-29
xrayKey: GAR-29
type: Manual
summary: Validate ID reconciliation on success and rollback on failure
priority: High
categories: [xray-sync, id-lifecycle]
severity: Critical
customFields: []
folder: GAR/XraySync
testSets: []
coveredRequirements: [REQ-002, REQ-003]
storyKey: GAR-11
status: synced
---

## Test Specifications
Ensure successful create operations reconcile AGENT IDs to Xray keys while failed sync attempts do not partially mutate local identifiers.

## Test Setup
```yaml
- action: Create local test files with AGENT IDs and baseline traceability entries.
  expectedResults:
    - Local artifacts are present with AGENT identifiers.
```

## Steps
```yaml
- action: Execute a successful new test sync for one local AGENT file.
  data: valid create payload and reachable endpoint
  expectedResults:
    - Returned Xray key is persisted in frontmatter.
    - File name is renamed from AGENT id to Xray key.
- action: Execute a failing sync for another local AGENT file.
  data: intentionally invalid update payload
  expectedResults:
    - Sync call fails with explicit error classification.
    - Failed file retains original AGENT filename and identifiers.
- action: Validate traceability records after both operations.
  data: traceability matrix before and after
  expectedResults:
    - Successful test mapping is updated to Xray key.
    - Failed test mapping remains unchanged.
```

## Test Teardown
```yaml
- action: Revert test environment to baseline files.
  expectedResults:
    - Temporary files and mappings are removed.
```
