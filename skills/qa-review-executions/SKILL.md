---
name: qa-review-executions
description: >-
  Convert one or more normalized execution-analysis receipts into a concise, evidence-linked management or reviewer
  assessment. Use when a manager, reviewer, release owner, or auditor asks about execution outcome, risk, recurring
  problems, defects, evidence, coverage, readiness, or recommended follow-up across one or more test runs.
---

# QA Review Executions

## Purpose

Answer the reviewer's question and deliver a short, accurate view of every problem found across the selected executions.

Consume analysis receipts; do not independently change findings, investigate new root causes, or mutate execution state.

## Required resources

Read these resources completely before reviewing:

- [Execution finding contract](../qa-analyze-execution/references/execution-finding-contract.md)
- [Evidence verification rules](../qa-analyze-execution/references/evidence-verification-rules.md)

Use [the manager execution review template](assets/manager-execution-review-template.md) as the output structure. Do not
copy placeholder values into the response.

## Inputs

Require one or more receipts from `qa-analyze-execution`. Each receipt must identify its journal, outcome, completeness,
findings, reviewed sources, and unavailable sources.

Reject a receipt that:

1. Omits required finding fields.
2. Presents inference as verified evidence.
3. Contains a material claim with no evidence reference or explicit evidence gap.
4. Claims a local or remote mutation occurred during analysis.

Return the invalid receipt to `qa-analyze-execution` for correction. Do not repair it by inventing values.

Use the fixed account configured with the Personal Access Token (PAT) when a permitted read-only link check is required.
Never ask for a username, tester identity, password, PAT, cookie, or authorization header.

## Review workflow

1. Extract the reviewer's exact question and requested scope.
2. Validate every analysis receipt.
3. Deduplicate findings according to the execution finding contract.
4. Preserve all affected execution, test, step, requirement, environment, and build references in a merged finding.
5. Calculate the management risk using the deterministic rules below.
6. Answer the reviewer's exact question in one to three sentences.
7. Render the execution snapshot.
8. Render every deduplicated problem in severity order.
9. Render all material evidence gaps and one recommended next action.

Do not truncate the problem inventory. Merge true duplicates into one row, but never hide a lower-severity, resolved, or
uncertain finding.

## Risk rules

Assign one overall risk from the selected scope:

| Risk | Rule |
| --- | --- |
| `Red` | At least one open `Critical` finding exists, or an open `High` finding invalidates required behavior, an execution-critical path, or authoritative outcome consistency. |
| `Amber` | No `Red` condition exists, but an open `Medium` finding, incomplete step, analysis gap, material missing evidence, or failed or partial Xray synchronization remains. |
| `Green` | No open `Critical`, `High`, or `Medium` finding exists; execution results are complete and internally consistent; and requested synchronization is confirmed or was not required. |

When the receipts are too incomplete to support `Green`, assign `Amber` and state the exact limitation. Do not average
severity, confidence, pass rate, or execution count into the risk.

## Problem consolidation

Deduplicate by verified defect or incident identifier first, then by grounded cause and matching observed behavior. A
single merged problem must retain:

1. Every affected execution and test.
2. The highest supported severity.
3. The least resolved status across the affected scope.
4. All non-duplicate evidence, defect, log, and source links.
5. Contradictory evidence and scope-specific differences.

Use `Open` before `Unknown`, and `Unknown` before `Resolved`, when a merged status differs. Do not merge merely because
two findings share a category or similar summary.

## Output rules

Keep the report short and factual:

1. Lead with the direct answer to the user's request.
2. State scope, recorded outcome, and risk in a compact snapshot.
3. Always include `Execution problems`, even when the value is `None identified`.
4. Give one table row per deduplicated problem.
5. Use descriptive direct links for verified defects, evidence, logs, and sources.
6. Mark inaccessible or unverified references explicitly instead of omitting them.
7. End with exactly one recommended management action unless the user requested multiple decision options.

Use this problem table:

| Severity | Problem and impact | Affected scope | Evidence and sources | Defect | State and action |
| --- | --- | --- | --- | --- | --- |

Keep analysis classification and confidence visible when they materially qualify a finding. Do not include internal
reasoning, raw payloads, long log excerpts, or implementation detail that does not change a reviewer decision.

## Artifact boundary

Return the report in the conversation by default. Persist a report only when the user explicitly requests a file and
provides or approves its destination.

When persisting a Markdown report, apply `md-vanilla-style`, run `md-code-compliance-review`, and require a score of 100
with zero linter errors. Never update an execution journal while saving a review.

## Hard constraints

- Do not modify journals, tests, requirements, defects, Jira, Xray, source, evidence, or configuration.
- Do not reclassify a failure without a corrected `qa-analyze-execution` receipt.
- Do not claim readiness from pass counts alone.
- Do not omit a problem because it was resolved, has low severity, lacks a defect, or complicates the summary.
- Do not construct or display an unverified link as though it were authoritative.
- Do not ask for authentication identity or credentials.
- Do not bury the direct answer below the problem inventory.

## Completion condition

Complete when the user's exact question is answered, risk is deterministically assigned, every distinct finding is
represented once with its evidence state and links, limitations are explicit, and one concise next action is returned.
