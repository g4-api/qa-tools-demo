---
name: qa-orchestrate-execution-review
description: >-
  Orchestrate concise, read-only management analysis of manual-test executions by resolving journal scope, invoking one
  evidence-grounded analysis per execution, and aggregating all problems with defect, log, evidence, source, and Xray
  links. Use for natural-language requests to review, compare, audit, assess risk, explain outcome, or summarize one or
  more executions, tests, stories, builds, or environments.
---

# QA Orchestrate Execution Review

## Purpose

Coordinate execution discovery, analysis, and management review while keeping the entire workflow read-only.

Answer the user's stated question first, then always add the full deduplicated execution-problem inventory. Delegate
single-execution investigation to `qa-analyze-execution` and presentation to `qa-review-executions`.

## Boundaries

Own scope resolution, workflow coordination, receipt validation, and final handoff. Do not analyze root cause directly,
edit a journal, create a defect, synchronize Xray, or change any execution artifact.

Use the fixed account configured with the Personal Access Token (PAT) for permitted read-only Jira and Xray lookups. Never
ask for a username, tester identity, password, PAT, cookie, Basic-authentication value, or authorization header. Never
display or persist credentials.

## Scope resolution

Resolve scope from the user's request in this order:

1. Explicit journal path or `EXEC-###` identifier.
2. Xray Test Execution key.
3. Test identifier or Xray Test key.
4. Story identifier.
5. Build, environment, date range, or recorded execution status.

Search only relevant `qa-workspace/<STORY-ID>/executions/<EXEC-ID>/journal.md` locations and recorded Xray references.
Include every journal matching the resolved scope.

When multiple matches are expected by the request, analyze all of them. Ask one concise scope question only when
different reasonable interpretations would materially change the report. Do not ask for values that can be resolved from
the workspace or read-only systems.

## Workflow

1. Extract the user's exact question and requested filters.
2. Resolve all matching execution journals without changing them.
3. Report an exact blocker when no journal or accessible execution record matches the scope.
4. Invoke `qa-analyze-execution` once for each matching journal.
5. Require every analysis receipt to conform to the execution finding contract.
6. Return an invalid or incomplete receipt to the analyzer for correction.
7. Invoke `qa-review-executions` with the user's question, resolved scope, and all valid receipts.
8. Validate that the final review answers the question and includes every distinct problem.
9. Return the concise review to the user.

Keep execution order deterministic: story identifier, execution identifier, then journal path. Do not analyze the same
journal twice because it matched more than one filter.

## Direct-answer requirement

The final review must begin with the answer to the user's specific request. Examples include:

- whether the execution passed,
- what blocks release readiness,
- which failures recur,
- which defects remain open,
- whether Xray matches the local journal, or
- what changed between builds.

After that answer, always include the snapshot, `Execution problems`, evidence gaps, and recommended action required by
`qa-review-executions`. A narrow question changes the lead answer, not the completeness of the problem inventory.

## Receipt validation

Before aggregation, require each analyzer receipt to contain:

1. Execution identity and journal path.
2. Recorded outcome and result counts.
3. Analysis completeness and limitations.
4. Every normalized finding or `None identified`.
5. Reviewed and unavailable source references.

Reject a receipt that invents a link, hides contradictory evidence, omits a non-passed or incomplete step, or reports a
mutation. Rerun only the affected analyzer; do not discard valid receipts for other executions.

## Read-only external access

Use Jira, Xray, repository, documentation, and monitoring connectors only for read-only verification required by the
analysis skills. Never call create, update, transition, link, comment, delete, synchronize, or result-setting operations.

When a remote record is unavailable, preserve its recorded key or reference as unverified and continue when a useful
limited review remains possible. State the limitation instead of asking for credentials.

## Failure handling

- When one journal is malformed, analyze the remaining journals and report the malformed journal as an execution-process
  problem when its scope is still identifiable.
- When a referenced artifact is unavailable, return a limited analysis with an evidence-gap finding.
- When all journals are unavailable, stop with the searched scope and exact missing source.
- When remote verification fails, do not retry with credentials supplied through conversation.
- When an analyzer or reviewer returns an invalid receipt, rerun that skill with the violated contract named explicitly.

## Hard constraints

- Keep the complete workflow read-only.
- Do not update `journal.md`; only `qa-execute-manual-tests` owns journal writes.
- Do not invoke `qa-author-defects` or any mutation tool.
- Do not substitute generic Jira issue links for Xray execution membership or Test Run state.
- Do not infer success from a completed journal, Jira issue status, HTTP status, or GraphQL transport status alone.
- Do not omit problems outside the narrow wording of the user's question.
- Do not ask for authentication identity or credentials; PAT transport and its account identity are preconfigured.
- Do not produce a long narrative when the evidence fits the required compact structure.

## Completion condition

Complete when scope is explicit, every matching journal has a valid analysis receipt or named limitation, the user's
question is answered first, all distinct execution problems and relevant links are included, risk is stated, and one
concise recommended action is returned.
