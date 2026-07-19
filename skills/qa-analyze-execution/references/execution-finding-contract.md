# Execution Finding Contract

## Finding identity

Represent each distinct execution problem as one finding. Assign a receipt-local `FIND-###` identifier beginning with
`FIND-001`. Do not persist the identifier into the execution journal or any remote system.

## Required fields

Return every finding with these fields:

| Field | Rule |
| --- | --- |
| Finding | Receipt-local `FIND-###` identifier. |
| Severity | Exactly one allowed severity. |
| Category | Exactly one allowed category. |
| Status | `Open`, `Resolved`, or `Unknown`. |
| Problem | One concise, factual statement of the problem. |
| Impact | Recorded effect on behavior, coverage, execution reliability, or decision quality. |
| Affected scope | Execution, test, authored step, requirement, environment, and build when applicable. |
| Evidence grade | Exactly one allowed evidence grade. |
| Evidence | Direct links, stable paths, line numbers, timestamps, or `None available`. |
| Defects | Verified or recorded defect keys and links, or `None`. |
| Analysis | Classification and confidence when analysis exists, or `Not analyzed`. |
| Next action | One recorded or evidence-supported advisory action. |

Do not omit an optional reference silently. Use `None`, `Not recorded`, or `Unverified` to preserve the distinction.

## Categories

Select exactly one category:

- `Product defect`
- `Environment`
- `Configuration`
- `Prerequisite or test data`
- `Test definition`
- `Requirement ambiguity`
- `Tester action`
- `Evidence gap`
- `Execution process`
- `Xray synchronization`
- `Traceability`
- `Unresolved analysis`

Use the failure-analysis classification when one exists. Do not replace an evidence gap with a more specific category
unless the evidence supports it.

## Severity

Apply severity from recorded impact, not from confidence or emotional wording:

| Severity | Use when |
| --- | --- |
| `Critical` | Recorded evidence identifies a release-blocking safety, security, irreversible data-loss, or regulatory impact. |
| `High` | Required product behavior failed, an execution-critical path is blocked, or authoritative local and Xray outcomes materially conflict. |
| `Medium` | A step is blocked, skipped, pending analysis, or materially unverifiable; synchronization failed or is partial; an environment, configuration, or prerequisite issue prevents a reliable result. |
| `Low` | A non-material warning, metadata inconsistency, stale reference, or evidence-quality issue does not invalidate the overall result. |
| `Info` | A resolved historical problem or notable condition has no remaining recorded execution impact. |

Never assign `Critical` without explicit impact evidence. Prefer the lower supported severity when impact is unclear and
state the missing evidence.

## Evidence grades

Select exactly one grade:

| Grade | Rule |
| --- | --- |
| `Verified` | The referenced artifact or remote record was inspected and directly supports the claim. |
| `Corroborated` | At least two independent recorded sources consistently support the claim. |
| `Unverified` | The journal references the source, but it could not be inspected or authenticated. |
| `Inference` | The conclusion is reasoned from verified facts but is not directly observed. Label it explicitly. |

Confidence from a failure analysis does not replace the finding evidence grade.

## Status

- Use `Open` when the execution records an unresolved effect or required follow-up.
- Use `Resolved` only when a verified later record confirms resolution.
- Use `Unknown` when the available records do not establish the current state.

Do not infer resolution from a completed execution, closed journal, Jira workflow status, or passed retry alone unless the
records explicitly connect the resolution to the finding.

## Deduplication key

Treat records as one finding only when they share the same grounded problem and affected cause or external defect. Use
this comparison order:

1. Verified defect key or external incident identifier.
2. Failure-analysis classification and verified cause.
3. Test identifier, authored step, environment, build, and matching observed behavior.

Keep separate findings when root cause, impact, status, or evidence materially differs. Preserve every affected execution
and step in the combined scope.

## Ordering

Order findings by:

1. Severity: `Critical`, `High`, `Medium`, `Low`, then `Info`.
2. Authored step number when findings share a severity.
3. Recorded chronology when no authored step applies.

The reviewer may deduplicate findings across executions but must preserve all affected execution references.
