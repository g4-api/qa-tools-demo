---
name: qa-orchestrate-test-cases
description: Drive the end-to-end, self-correcting QA loop that authors readable Manual Xray Markdown test cases one at a time, enforces flawless md-* compliance plus a greater-than-95 QA score, emits a complete scoring table after each test cycle, optionally syncs to Xray, commits, and opens a pull request. Use for full automated test-authoring or refactoring runs.
---

# QA Orchestrate Test Cases

## Purpose

This skill is the "orchestrate" stage of the create / review / orchestrate trio. It owns the automated, end-to-end quality loop.

It processes tests one at a time to completion, then opens a pull request.

This skill must:
1. resolve the run target and parameters,
2. get a single upfront approval,
3. run the sequential per-test loop with no further prompts,
4. commit each finalized test and, when enabled, sync it to Xray first,
5. stop on success, on the iteration cap, on a real blocker, or on a sync/commit failure,
6. emit a detailed final report,
7. open the pull request through `qa-github-pr`.

## Use this skill when

Use this skill when the task is about:
- authoring a full set of test cases from a requirements decomposition end to end
- refactoring or fixing an existing set of tests up to the quality gate
- running the automated create/review/fix loop with commits and a PR
- getting a final scored report over a story's tests

Do not use this skill for a single one-off create or a single one-off score; use `qa-create-test-cases` or `qa-review-test-cases` directly for those.

## Operating philosophy

Test artifacts are first-class code files. This skill treats the authoring loop like a build-and-test cycle: for each test, generate, score against a hard gate, fix the failing unit, sync, and commit, with full traceability, then open a PR for human review.

## The gate

Every test must score strictly greater than 95 on the `qa-review-test-cases` weighted rubric, score exactly 100 under `md-code-compliance-review`, and have zero Markdown linter errors. The gates are per test.

## Interaction contract

1. **Load** — triggered by the user prompt.
2. **Ask guiding questions** — resolve only what the prompt did not set.
3. **Show a plan** — target, cap, standard, report level, Xray toggle, and Git/PR target.
4. **Wait for a single approval.**
5. **Run the automated loop** — no further prompts until success, cap, a real blocker, or a sync/commit failure.

The single upfront approval is scoped to authorize the whole run: per-test create/review/fix, optional per-test Xray sync, per-test Git commits, the batch meta commit, and the final pull request. After approval, do not ask for approval between steps.

## Guiding questions to resolve at load

Ask only the ones the prompt left open:

1. **Target** — which `<STORY-ID>`/`requirements.md`, or which existing `tests/` set to refactor.
2. **Coverage depth** — if unset, delegate to the `qa-create-test-cases` coverage matrix step.
3. **Review standard** — default General best practice; the user may choose ISTQB or ISTQB + ISO/IEC/IEEE 29119. Fixed for the session once the loop starts.
4. **Iteration cap** — default 6, per test.
5. **Final-report detail** — default: per-test scores plus REQ-to-test coverage summary. The user may choose a full per-dimension matrix plus run stats, or a summary table only.
6. **Xray sync** — whether to sync each finalized test to Xray. Enable only if the user asks and the Xray MCP is available; otherwise skip sync and keep internal `AGENT-###` ids.
7. **Xray Test Plan** — whether to create a Test Plan after test sync; if enabled, resolve its project, summary, and requested optional fields up front.
8. **Git/PR target** — the GitHub repository and base branch used by `qa-git-commit` and `qa-github-pr`.

## Coverage planning

Before the loop, derive the ordered list of tests to author from the decomposition (via `qa-create-test-cases` coverage planning). The loop then processes that list one test at a time.

Before processing tests, apply `md-vanilla-style` and the `md-code-compliance-review` repair cycle to `requirements.md` and `traceability.md`. Do not start a test while either file is below 100 Markdown compliance or has a linter error.

## Sequential per-test loop

Run this loop after approval. For each planned test, in order:

1. **Create** — invoke `qa-create-test-cases` to write or update one test using YAML metadata frontmatter and readable, enumerated Markdown body text.
2. **Markdown review-fix** — invoke `md-code-compliance-review`. Route every finding to `qa-create-test-cases`, rerun the linter, and repeat until Markdown is 100 with zero errors.
3. **QA review-fix** — invoke `qa-review-test-cases`. If QA is at or below 95, route issues to `qa-create-test-cases`, then restart at Markdown review because every content fix must be revalidated by both gates.
4. **Per-test scoring table** — immediately show the complete final table for this test, including every QA dimension, QA weighted total, Markdown compliance score, Markdown linter error count, iteration count, and PASS status. This table is mandatory and cannot be deferred to the final report.
5. **Xray sync** *(if enabled and available)* — invoke `qa-xray-sync` for this single test. A new test must call `new_xray_test`; an existing changed test must call `update_xray_test`. The sync skill parses the readable enumerated Markdown, validates the exact closed-schema payload, executes the call, and updates IDs.
6. **Post-sync Markdown check** — when sync changes the filename, frontmatter, or traceability file, rerun Markdown compliance on every changed `.md` file and require 100 with zero errors.
7. **Commit** — invoke `qa-git-commit` to commit the finalized test to `qa/<STORY-ID>-tests`. The commit carries the real Xray key when sync ran, otherwise the `AGENT-###` id.
8. **Next** — move to the next planned test.

After all tests are finalized and committed:

1. **Test Plan** *(if enabled)* — invoke `qa-xray-sync` to create it through `new_xray_test_plan` with its exact validated payload.
2. **Batch meta commit** — invoke `qa-git-commit` for flawless `requirements.md` and `traceability.md`.
3. **Pull request** — invoke `qa-github-pr` to open one detailed, ready-for-review PR.

Track per-test iteration counts and per-step changes for the final report.

### Refactor / fix runs

When the target is an existing `tests/` set, start each test at Markdown review, then run QA review, fixes, both rechecks, the mandatory per-test scoring table, sync, and commit as above.

## Stop conditions

### Success

Every test passes both gates, every per-test scoring table was shown, every Markdown artifact is flawless, all commits are in place, and the PR is opened. Emit the final report.

### Iteration cap

A test's per-test cap is reached while QA remains at or below 95, Markdown remains below 100, or linter errors remain. Stop at that test, show its current complete scoring table and blocking issues, note earlier finalized tests, and hand back to the user.

### Real blocker

If a fix requires information that is missing or genuinely ambiguous (for example a needed requirement does not exist), pause the loop:
- route missing-requirement blockers to `qa-decompose-requirements`,
- otherwise ask the user.
Resume the loop after the blocker is resolved.

### Sync or commit failure

If a per-test Xray sync or Git commit fails, stop the loop at that test. Report what succeeded so far, including the tests already committed and the branch state, and hand back to the user. Do not skip past the failure.

## Final report

Default detail level is per-test scores plus a REQ-to-test coverage summary.

The final report is additive. It never replaces the complete scoring table already emitted at the end of each per-test cycle.

### Per-test + coverage (default)

```markdown
Loop complete. All tests exceed 95, are committed, and a PR is open.

Iterations: <n> (per-test cap <cap>)
Branch: qa/<STORY-ID>-tests
PR: <url>

| Test | QA Score | Markdown Score | Linter Errors | Xray Key | Status |
|---|---:|---:|---:|---|---|
| <id> | <0-100> | 100 | 0 | <key or -> | PASS |

Coverage (REQ -> tests):
| REQ | Tests |
|---|---|
| REQ-000 | <ids> |
```

### Full matrix + run stats (on request)

Adds a per-dimension score table per test and a per-iteration change log.

### Summary table only (on request)

Use only the aggregate per-test pass table and overall status in the final report. This option does not suppress the mandatory complete table emitted during each test cycle.

If the run stopped early, replace the header with a clear failure header, list the blocking issues or failure cause, and show which tests were already finalized and committed.

## Hard constraints

- Do not ask for approval between loop steps after the single upfront approval.
- Do not stop before every test exceeds 95 unless the cap, a real blocker, or a sync/commit failure is hit.
- Do not advance a test below 100 Markdown compliance or with any Markdown linter error.
- Do not put YAML anywhere in a test body; only metadata frontmatter may be YAML.
- Do not defer or omit the complete scoring table at the end of each per-test cycle.
- Do not continue silently past the iteration cap or past a sync/commit failure.
- Do not sync to Xray when the user did not enable it or the MCP is unavailable.
- Do not create or update an Xray test or create a Test Plan outside `qa-xray-sync`; that skill owns exact tool routing and schema validation.
- Do not edit test files directly; route fixes through `qa-create-test-cases`.
- Do not score tests directly; scoring belongs to `qa-review-test-cases`.
- Do not commit or open PRs directly; use `qa-git-commit` and `qa-github-pr`.
- Do not open the PR before all finalized tests and the meta files are committed.
- Do not invent requirements; route missing-requirement blockers to `qa-decompose-requirements`.

## Completion condition

This skill is complete when either:
- every planned test exceeds 95, each is committed, the meta commit is in place, the PR is open, and the final report is emitted, or
- the loop stopped at a stuck test, a real blocker, or a sync/commit failure, and a report of committed-so-far progress was handed back to the user.
