---
name: qa-git-commit
description: Commit a finalized test-case file, or the batch requirements/traceability meta files, to a per-story branch on a GitHub repository via a GitHub MCP resolved at runtime. Use to version-control QA test artifacts one commit per finalized test, with Conventional Commit messages that carry the test and requirement IDs.
---

# QA Git Commit

## Purpose

This skill commits QA test artifacts to a per-story branch on GitHub, one commit per finalized test, plus a batch meta commit before the pull request.

It is MCP-agnostic: it resolves the GitHub MCP tools at runtime. A GitHub MCP commits file content to a branch on the remote repository via API; there is no assumption of a local working tree.

This skill must:
1. resolve the GitHub MCP, the target repository, and the base branch,
2. ensure the per-story branch exists,
3. commit the finalized file content with a Conventional Commit message,
4. skip when there is nothing to commit,
5. report the commit result.

## Use this skill when

Use this skill when the task is about:
- committing a finalized test file after it passes the quality gate
- committing the requirements and traceability meta files before a PR
- creating or checking out the per-story branch
- version-controlling QA artifacts as first-class code

Do not use this skill to author, score, sync to Xray, or open a pull request. The PR belongs to `qa-github-pr`.

## Operating philosophy

Test artifacts are first-class code files, so they get first-class version control: a clean history with one meaningful commit per finalized test, carrying stable IDs for traceability.

## Interaction contract

- **Inside the orchestrated loop**: runs non-interactively. The single upfront approval from `qa-orchestrate-test-cases` authorizes commits and branch creation.
- **Standalone**: confirm the target repository and branch before committing.

## Guiding questions to resolve at load

Ask only the ones the prompt left open:

1. **Repository** — the target GitHub repository (`owner/name`). The `qa-workspace` is not necessarily the repository.
2. **Base branch** — the branch the story branch is created from (for example `main`).
3. **MCP reachability** — confirm the GitHub MCP is available; if not, stop and report.

## Branch management

- The per-story branch is `qa/<STORY-ID>-tests`.
- On the first commit for a story, ensure the branch exists; create it from the base branch if missing.
- All commits for a story go to that branch.

## Commit triggers and granularity

### Per finalized test

Commit a single test only after it passed the greater-than-95 QA gate, scored 100 under `md-code-compliance-review`, has zero Markdown linter errors, emitted its complete per-test scoring table, updated its IDs, and completed any Xray sync. The commit therefore carries readable Markdown and the real Xray key when sync ran.

### Batch meta

Commit `requirements.md` and `traceability.md` as a single meta commit before the pull request is opened, only after both files score 100 with zero Markdown linter errors.

Skip any commit when the target content is unchanged.

## Commit message convention

Use Conventional Commits.

- Per-test commit:

  ```text
  test(<STORY-ID>): <XRAYKEY or AGENT-ID> <summary> (covers REQ-000, REQ-001)
  ```

- Batch meta commit:

  ```text
  chore(<STORY-ID>): update requirements & traceability
  ```

Keep the subject concise. Use the real Xray key in the message when the test has been synced; otherwise use the internal `AGENT-###` id.

## Execution

1. Resolve the MCP, repository, and base branch.
2. Ensure the story branch exists.
3. Read the finalized local file content.
4. Verify YAML is confined to metadata frontmatter and verify the recorded Markdown gate is 100 with zero errors.
5. Commit that content to the story branch through the MCP with the correct message.
6. Report the commit (branch, message, committed path, resulting SHA if available).

## Failure handling

- If the commit fails, report the failure clearly and do not pretend it succeeded.
- Inside the orchestrated loop, a commit failure stops the loop; the orchestrator owns the stop-and-report behavior.

## Hard constraints

- Do not hardcode MCP tool names; resolve them at runtime.
- Do not open a pull request here.
- Do not author, score, or sync test cases here.
- Do not commit unchanged content.
- Do not use non-Conventional-Commit messages.
- Do not commit a synced test using its old `AGENT-###` id when a real Xray key exists.
- Do not commit any Markdown artifact below 100 Markdown compliance or with a linter error.
- Do not commit a test before its complete per-test scoring table was emitted.

## Completion condition

This skill is complete when the requested content has been committed to `qa/<STORY-ID>-tests` (or correctly skipped as unchanged) and the commit result has been reported.
