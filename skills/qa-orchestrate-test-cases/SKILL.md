---
name: qa-orchestrate-test-cases
description: Drive the end-to-end, self-correcting QA loop that authors Manual Xray test cases one at a time - create, review-fix to greater-than-95, optional per-test Xray sync, ID update, and Git commit - then a batch meta commit and a detailed pull request. Use when a QA engineer wants a full automated run from a requirements decomposition (or an existing test set) through committed, review-ready test artifacts.
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

Every test must score strictly greater than 95 on the `qa-review-test-cases` weighted rubric. The gate is per test.

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
7. **Git/PR target** — the GitHub repository and base branch used by `qa-git-commit` and `qa-github-pr`.

## Coverage planning

Before the loop, derive the ordered list of tests to author from the decomposition (via `qa-create-test-cases` coverage planning). The loop then processes that list one test at a time.

## Sequential per-test loop

Run this loop after approval. For each planned test, in order:

1. **Create** — invoke `qa-create-test-cases` to write (or update) the single test.
2. **Review-fix** — invoke `qa-review-test-cases` to score it; if at or below 95, route its issues back to `qa-create-test-cases` and re-review. Repeat until the test exceeds 95 or the per-test iteration cap is reached.
3. **Xray sync** *(if enabled and available)* — invoke `qa-xray-sync` for this single test, then let it update the IDs (filename, frontmatter, traceability).
4. **Commit** — invoke `qa-git-commit` to commit the finalized test to `qa/<STORY-ID>-tests`. The commit carries the real Xray key when sync ran, otherwise the `AGENT-###` id.
5. **Next** — move to the next planned test.

After all tests are finalized and committed:

6. **Batch meta commit** — invoke `qa-git-commit` for `requirements.md` and `traceability.md`.
7. **Pull request** — invoke `qa-github-pr` to open one detailed, ready-for-review PR.

Track per-test iteration counts and per-step changes for the final report.

### Refactor / fix runs

When the target is an existing `tests/` set, start each test at the review step (review -> fix -> re-review) instead of fresh creation, then sync/commit as above.

## Stop conditions

### Success

Every test exceeds 95 and is committed, the meta commit is in place, and the PR is opened. Emit the final report.

### Iteration cap

A test's per-test cap is reached while still at or below 95. Stop the loop at that test. Report it as a stuck test with its blocking issues, note which earlier tests were already finalized and committed, and hand back to the user. Do not silently continue.

### Real blocker

If a fix requires information that is missing or genuinely ambiguous (for example a needed requirement does not exist), pause the loop:
- route missing-requirement blockers to `qa-decompose-requirements`,
- otherwise ask the user.
Resume the loop after the blocker is resolved.

### Sync or commit failure

If a per-test Xray sync or Git commit fails, stop the loop at that test. Report what succeeded so far, including the tests already committed and the branch state, and hand back to the user. Do not skip past the failure.

## Final report

Default detail level is per-test scores plus a REQ-to-test coverage summary.

### Per-test + coverage (default)

```markdown
Loop complete. All tests exceed 95, are committed, and a PR is open.

Iterations: <n> (per-test cap <cap>)
Branch: qa/<STORY-ID>-tests
PR: <url>

| Test | Final Score | Xray Key | Status |
|---|---:|---|---|
| <id> | <0-100> | <key or -> | PASS |

Coverage (REQ -> tests):
| REQ | Tests |
|---|---|
| REQ-000 | <ids> |
```

### Full matrix + run stats (on request)

Adds a per-dimension score table per test and a per-iteration change log.

### Summary table only (on request)

Just the per-test pass table and overall status.

If the run stopped early, replace the header with a clear failure header, list the blocking issues or failure cause, and show which tests were already finalized and committed.

## Hard constraints

- Do not ask for approval between loop steps after the single upfront approval.
- Do not stop before every test exceeds 95 unless the cap, a real blocker, or a sync/commit failure is hit.
- Do not continue silently past the iteration cap or past a sync/commit failure.
- Do not sync to Xray when the user did not enable it or the MCP is unavailable.
- Do not edit test files directly; route fixes through `qa-create-test-cases`.
- Do not score tests directly; scoring belongs to `qa-review-test-cases`.
- Do not commit or open PRs directly; use `qa-git-commit` and `qa-github-pr`.
- Do not open the PR before all finalized tests and the meta files are committed.
- Do not invent requirements; route missing-requirement blockers to `qa-decompose-requirements`.

## Completion condition

This skill is complete when either:
- every planned test exceeds 95, each is committed, the meta commit is in place, the PR is open, and the final report is emitted, or
- the loop stopped at a stuck test, a real blocker, or a sync/commit failure, and a report of committed-so-far progress was handed back to the user.
