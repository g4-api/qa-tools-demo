---
name: qa-github-pr
description: Open one detailed, ready-for-review pull request for a completed QA test-authoring cycle, from the per-story branch to the base branch, via a GitHub MCP resolved at runtime. The PR body is assembled from the requirement source, per-test list, coverage matrix, final score table, and Xray links. Use when a story's test cases are finalized, committed, and ready for human review.
---

# QA GitHub PR

## Purpose

This skill opens a single, detailed pull request at the end of a QA test-authoring cycle.

It is MCP-agnostic: it resolves the GitHub MCP tools at runtime.

This skill must:
1. resolve the GitHub MCP, repository, story branch, and base branch,
2. assemble a detailed PR body from the run artifacts,
3. open the PR as ready for review,
4. report the PR link.

## Use this skill when

Use this skill when the task is about:
- opening the pull request after a story's tests are finalized and committed
- producing a detailed, review-ready PR description for QA test artifacts

Do not use this skill to commit files, author, score, or sync tests. Commits belong to `qa-git-commit`.

## Interaction contract

- **Called by the orchestrator** at cycle end: the single upfront approval authorizes opening the PR.
- **Standalone**: show the PR title, base, and body, and confirm before opening.

## Guiding questions to resolve at load

Ask only the ones the prompt left open:

1. **Repository** — the target GitHub repository (`owner/name`).
2. **Branches** — the story branch `qa/<STORY-ID>-tests` and the base branch to target.
3. **MCP reachability** — confirm the GitHub MCP is available; if not, stop and report.

## Preconditions

- The story branch exists and carries the committed test files.
- The batch meta commit (`requirements.md`, `traceability.md`) is in place.

If commits are missing, stop and route back to `qa-git-commit`.

## PR content

Open the PR from `qa/<STORY-ID>-tests` to the base branch, marked ready for review (not draft).

Assemble the PR body from the run artifacts:

- **Requirement source** — Jira key or document link, and the story title.
- **Summary** — what the cycle produced (number of tests, coverage depth, standard used).
- **Tests** — a list, each with its Xray key, original `AGENT-###` id, and summary.
- **Coverage matrix** — REQ-to-test mapping from `traceability.md`.
- **Quality** — the final per-test score table from `qa-review-test-cases`, confirming every test exceeds 95.
- **Xray links** — links to the synced tests, when sync ran.
- **Run stats** — iteration count, and anything left as a noted gap.

## Execution

1. Resolve the MCP, repository, and branches.
2. Verify the story branch has the expected commits.
3. Build the PR title and detailed body.
4. Open the PR as ready for review through the MCP.
5. Report the PR URL and number.

## PR title convention

```text
QA: <STORY-ID> manual test cases
```

## Hard constraints

- Do not hardcode MCP tool names; resolve them at runtime.
- Do not open the PR as a draft; it must be ready for review.
- Do not open a PR when required commits are missing.
- Do not commit, author, score, or sync here.
- Do not open more than one PR per story cycle.
- Do not omit the coverage matrix or the final score table from the body.

## Completion condition

This skill is complete when a single ready-for-review PR from `qa/<STORY-ID>-tests` to the base branch exists with the full detailed body, and its URL has been reported.
