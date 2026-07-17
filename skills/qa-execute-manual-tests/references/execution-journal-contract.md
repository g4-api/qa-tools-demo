# Execution Journal Contract

## Location and identity

Store each execution independently:

```text
qa-workspace/
  <STORY-ID>/
    executions/
      <EXECUTION-ID>/
        journal.md
        defects/
        evidence/
```

Mint `EXEC-###` identifiers within the story, starting at `EXEC-000`. Never overwrite or reuse an identifier.

## Ownership

`qa-execute-manual-tests` is the only writer of `journal.md`. Other skills return handoffs or receipts to the execution
skill and must not edit the journal.

Authored tests, requirements, and traceability files are immutable inputs during execution.

## Metadata

Keep YAML only in frontmatter. Require these fields:

| Field | Type | Rule |
| --- | --- | --- |
| `executionId` | String | Stable `EXEC-###` identifier. |
| `storyId` | String | Owning story identifier. |
| `testId` | String | Finalized local or Xray test identifier. |
| `status` | String | One allowed execution status. |
| `mode` | String | `guided` or `bulk`. |
| `currentStep` | Integer or null | Next unresolved authored step. |
| `startedAt` | String | Observed ISO 8601 timestamp. |
| `updatedAt` | String | Observed ISO 8601 timestamp. |
| `tester` | String | Fixed non-secret identity configured with the PAT, or `configured-pat-account`. |
| `environment` | String | Environment reference or concise identifier. |
| `xrayExecutionKey` | String or null | Xray Test Execution key after synchronization, otherwise null. |

Allowed execution statuses are:

- `not-started`,
- `in-progress`,
- `blocked`,
- `ended`, and
- `completed`.

## Body

Keep the body readable Markdown. Require these sections in order:

1. `# Execution Journal`.
2. `## Execution Context`.
3. `## Xray Synchronization`.
4. `## Step Results`.
5. `## Linked Defects`.
6. `## Decisions`.
7. `## Next Action`.

Enumerate every context fact, step result, defect, decision, and next action. Preserve authored step numbers inside their
result records. Restart visible numbering at `1` under every section.

For each step result, record:

1. Authored step number.
2. Result status.
3. Tester observation.
4. Evidence references or `None`.
5. Analysis classification and confidence when analysis ran.
6. Tester decision.
7. Recorded timestamp.

Allowed step results are `Not run`, `Passed`, `Failed`, `Blocked`, `Skipped`, and `Analysis pending`.

For Xray synchronization, record:

1. Sync status: `Not requested`, `Pending`, `Synchronized`, or `Failed`.
2. Test Execution key or `None`.
3. Test Run identifier or `None`.
4. Last confirmed one-based authored step or `None`.
5. Confirmed Test Run status or `None`.
6. Xray warnings or `None`.

Only `qa-execute-manual-tests` writes synchronization receipts into the journal. Never persist PAT values, authorization
headers, or Basic-authentication material.

## Persistence rules

1. Checkpoint after every tester response or delegated-skill return.
2. Update `updatedAt` only from an observed system time.
3. Keep earlier facts; append corrections as decisions instead of silently rewriting history.
4. Store references to evidence instead of embedding binary content.
5. Store no hidden reasoning, unnecessary conversation, credentials, tokens, or unrelated personal data.
6. Run Markdown compliance after every write and require score 100 with zero linter errors.

## Resume rules

1. Load metadata, step results, decisions, and next action.
2. Verify that the referenced test still exists.
3. Detect whether the test definition changed after execution started.
4. Stop and ask the tester when a definition change makes continuation ambiguous.
5. Resume from `currentStep` only after journal consistency is confirmed.
