---
name: qa-analyze-execution
description: >-
  Analyze one manual-test execution journal and its test, requirement, defect, evidence, log, source, and Xray references
  to return a complete read-only inventory of execution problems. Use when an execution, journal, Test Run, or individual
  run needs evidence-grounded findings for management review, audit, release assessment, or follow-up analysis.
---

# QA Analyze Execution

## Purpose

Inspect one execution and return normalized, evidence-grounded findings without changing local or remote state.

Find every recorded execution problem, including resolved problems and data-quality gaps. Do not summarize findings for
management, modify the journal, create a defect, synchronize Xray, or change the test definition.

## Required resources

Read these resources completely before analysis:

- [Execution finding contract](references/execution-finding-contract.md)
- [Evidence verification rules](references/evidence-verification-rules.md)
- [Execution journal contract](../qa-execute-manual-tests/references/execution-journal-contract.md)
- [Execution handoff contracts](../qa-execute-manual-tests/references/execution-handoff-contracts.md)

Read the
[failure classification rubric](../qa-analyze-test-failure/references/failure-classification-rubric.md) when an
unexpected result lacks a completed analysis or the recorded analysis conflicts with its evidence.

## Inputs

Require one execution journal. Resolve related artifacts from recorded references and the story workspace:

1. Finalized test specification and applicable authored step numbers.
2. Story, requirement, and traceability artifacts.
3. Evidence, logs, traces, screenshots, recordings, and source references.
4. Linked defect artifacts, Jira keys, direct links, and recorded defect states.
5. Xray Test Execution, Test Run, step-result, status, and warning receipts.
6. Comparable prior executions when they are in scope or materially explain recurrence.

Use the fixed account configured with the Personal Access Token (PAT) for permitted read-only remote lookups. Never ask
for a username, tester identity, password, PAT, cookie, or authorization header. Never display or persist credentials.

## Investigation workflow

1. Validate the journal structure against the execution journal contract.
2. Reconcile journal metadata, context, step results, decisions, defects, next action, and Xray receipt.
3. Compare every authored test step with its recorded execution result.
4. Inspect every referenced requirement, evidence artifact, log, source location, defect, and Xray object that is
   available through read-only access.
5. Identify every problem category described below, including resolved and low-severity findings.
6. Verify each material claim and link according to the evidence verification rules.
7. Invoke `qa-analyze-test-failure` only for an unresolved mismatch that has the required handoff fields.
8. Normalize each distinct problem through the execution finding contract.
9. Return one analysis receipt to the caller.

Do not stop after finding the first failure. Review the entire execution and disclose evidence that contradicts a
finding.

## Problems to detect

Inspect for all of these conditions:

1. Product behavior that contradicts a grounded requirement or expected result.
2. Environment, configuration, prerequisite, test-data, or tester-action problems.
3. Incorrect, ambiguous, outdated, or changed test expectations and requirements.
4. `Failed`, `Blocked`, `Skipped`, `Analysis pending`, or `Not run` step results.
5. A `Passed` result whose observation or evidence contradicts an expected result.
6. Missing observations, missing required evidence, inaccessible artifacts, or unsupported conclusions.
7. Missing defect links, unresolved defects, likely duplicates, or defect state inconsistent with the journal.
8. Xray synchronization failures, partial receipts, warnings, missing Test Runs, or status differences between local and
   Xray records.
9. Journal inconsistencies, including invalid status transitions, nonterminal steps in a completed execution, stale
   `currentStep`, missing decisions, or timestamps that do not support the recorded sequence.
10. Test-definition drift after execution started and traceability gaps affecting the result.
11. Recurring or intermittent behavior supported by comparable executions.

Treat a missing or unverifiable record as a data-quality finding when it prevents a reliable conclusion. Do not convert
absence of evidence into evidence of product failure.

## Failure-analysis boundary

Use an existing recorded failure analysis when it satisfies the execution handoff contract. When a mismatch remains
unclassified and the complete handoff can be built, invoke `qa-analyze-test-failure` and include its read-only response as
analysis evidence.

When expected behavior, actual behavior, or another required handoff value is absent, classify the issue as an evidence
gap. Do not ask the manager to reproduce tester observations and do not invent a root cause.

## Receipt

Return these sections in readable text:

1. Execution identity and journal path.
2. Recorded execution outcome and result counts.
3. Analysis completeness: `complete` or `limited` with the exact limitation.
4. Findings conforming to the execution finding contract, or `None identified`.
5. Sources reviewed with verified paths or links.
6. Sources unavailable or unverified.

Assign `FIND-001`, `FIND-002`, and subsequent identifiers in severity order, then authored-step and chronological order.
The identifiers are local to the receipt and do not modify the journal.

## Hard constraints

- Remain read-only across the workspace, Jira, Xray, source repositories, and evidence systems.
- Do not update `journal.md`; only `qa-execute-manual-tests` owns that file.
- Do not create, draft, edit, transition, or link a defect.
- Do not call an Xray mutation or generic Jira mutation.
- Do not report a remote object as verified from its identifier alone.
- Do not omit resolved, low-severity, contradictory, or evidence-quality problems.
- Do not present inference as fact or assign impact unsupported by recorded evidence.
- Do not expose secrets or unrelated personal data from logs or configuration.

## Completion condition

Complete when the full execution has been inspected, every distinct grounded problem is represented once, every material
claim carries its evidence grade and references, limitations are explicit, and the read-only receipt is returned.
