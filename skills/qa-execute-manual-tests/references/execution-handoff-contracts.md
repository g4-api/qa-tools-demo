# Execution Handoff Contracts

## Analysis request

Pass these fields from `qa-execute-manual-tests` to `qa-analyze-test-failure`:

| Field | Required | Meaning |
| --- | --- | --- |
| Execution identifier | Yes | Stable `EXEC-###` identifier. |
| Test identifier | Yes | Finalized test identifier. |
| Step number | Yes | Authored step that produced the mismatch. |
| Expected results | Yes | Exact authored expected results. |
| Actual result | Yes | Tester's observation without reinterpretation. |
| Requirement references | Yes | Applicable stable requirement identifiers. |
| Environment reference | Yes | Environment and build facts. |
| Evidence references | No | Available screenshots, logs, traces, or recordings. |
| Documentation references | No | Relevant linked documentation. |
| Source references | No | Relevant source or configuration locations. |
| Prior executions | No | Comparable execution records. |
| Existing defects | No | Possible related or duplicate defects. |

Do not serialize this handoff into the journal as YAML or JSON. Record the returned analysis as readable execution facts.

## Analysis response

Require the analysis skill to return:

1. One allowed classification.
2. Confidence from 0 through 100.
3. Concise reasoning.
4. Supporting evidence references.
5. Missing evidence.
6. Possible duplicate defects.
7. Exactly one advisory next action.

Reject and rerun an analysis response that invents evidence, omits required fields, or attempts to change execution state.

## Defect request

Pass these fields to `qa-author-defects` only after explicit tester approval:

| Field | Required | Meaning |
| --- | --- | --- |
| Approval | Yes | Explicit approval to create a defect from the recorded facts. |
| Analysis response | Yes | Product-defect classification and supporting analysis. |
| Execution reference | Yes | Journal and execution identifier. |
| Test and step references | Yes | Reproduction source. |
| Requirement references | Yes | Affected expected behavior. |
| Environment and build | Yes | Reproduction environment. |
| Evidence references | No | Available supporting artifacts. |
| Destination project | Yes | Explicit Jira project destination. |

## Defect receipt

Require `qa-author-defects` to return:

1. Status: `created`, `drafted`, or `failed`.
2. Defect key when created.
3. Internal identifier when returned by the tool.
4. Direct link when returned by the tool.
5. Final summary.
6. Linked execution, test, and requirement references.
7. Failure reason when status is `failed`.

Record the receipt in the journal. Never infer a successful creation from a partial or invalid response.
