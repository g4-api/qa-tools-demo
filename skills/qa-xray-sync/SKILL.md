---
name: qa-xray-sync
description: Create or update Manual tests in Xray from local test-case files via an Xray/Atlassian MCP, link them to their Jira story or requirement, resolve conflicts by diff, and reconcile the internal AGENT-### id to the real Xray key in the filename, frontmatter, and traceability index. Use when locally authored test cases must be pushed into Xray or kept in sync with it.
---

# QA Xray Sync

## Purpose

This skill pushes locally authored Manual test files into Xray and closes the ID lifecycle by replacing internal `AGENT-###` identifiers with real Xray keys.

It is MCP-agnostic: it resolves the actual Xray/Atlassian MCP tools at runtime rather than assuming a fixed API.

This skill must:
1. resolve the sync target and confirm the Xray destination,
2. detect MCP capabilities at runtime,
3. classify each local test as create, update, conflict, or skip,
4. show a sync plan and wait for approval,
5. execute create/update and requirement-coverage linking,
6. resolve conflicts by diff with the user,
7. reconcile IDs and report the results.

## Use this skill when

Use this skill when the task is about:
- creating new Xray tests from local test files
- updating existing Xray tests from local changes
- linking tests to a Jira story or requirement for coverage
- reconciling internal IDs with real Xray keys
- syncing a single finalized test mid-loop for `qa-orchestrate-test-cases`

## Batch and single-test modes

This skill runs in two modes:

- **Batch** — sync a whole `<STORY-ID>/tests/` set. Standalone use presents the full sync plan and waits for approval.
- **Single test** — sync exactly one finalized test. Used by `qa-orchestrate-test-cases` between the review-fix step and the Git commit, so the commit can carry the real Xray key. In this mode the orchestrator's single upfront approval authorizes the sync; classify and sync just that one test, then update its IDs.

In both modes, conflicts are always surfaced to the user and never overwritten silently.

Do not use this skill to author, score, or loop test cases. Those belong to the create / review / orchestrate skills.

## Operating philosophy

Test artifacts are first-class code files, and Xray is the system of record for their execution. Local files are the authoring source of truth; syncing is a deliberate, reviewed, outward-facing write, never an automatic side effect.

## Interaction contract

1. **Load** — triggered by the user prompt, or offered by `qa-orchestrate-test-cases` on success.
2. **Ask guiding questions** — resolve only what the prompt did not set.
3. **Show a sync plan** — the per-test action classification.
4. **Wait for approval** — mandatory, because this writes to an external system.
5. **Execute** — push, link, resolve conflicts, reconcile IDs.

Conflicts are always surfaced to the user. Nothing is overwritten silently.

## Guiding questions to resolve at load

Ask only the ones the prompt left open:

1. **Sync target** — which `<STORY-ID>`/`tests/` set (or which specific tests) to sync.
2. **Xray destination** — project and Test Repository folder/path.
3. **MCP reachability** — confirm the Xray/Atlassian MCP is available; if not, stop and report.

## MCP capability resolution

- Resolve the available Xray/Atlassian MCP tools at runtime; do not hardcode tool names.
- Detect whether the target behaves like Xray Cloud (for example preconditions as linked entities, Test Repository folder paths) or Xray Server/Data Center.
- If the platform behavior cannot be inferred from the available tools, ask the user.

## Sync classification

For each local test file, classify the action:

- **CREATE** — no `xrayKey` in frontmatter. The test does not yet exist in Xray.
- **UPDATE** — has an `xrayKey`, and the local file differs from the Xray test, with no server-side divergence since last sync.
- **CONFLICT** — has an `xrayKey`, and the Xray test changed on the server since last sync.
- **SKIP** — has an `xrayKey`, and local and server are equal.

Present this classification as the sync plan and wait for approval before executing.

## Execution

### Create

1. Map the local frontmatter and steps to the Xray Manual test structure.
2. Push the create through the MCP.
3. Capture the returned Xray key.
4. Rename `AGENT-###.md` to `<XRAYKEY>.md`.
5. Set `xrayKey` and `id` in the frontmatter to the Xray key.
6. Record the `AGENT-### -> <XRAYKEY>` mapping in `traceability.md`.

### Update

- Treat the local file as the source of truth for non-conflicting fields.
- Push the changed fields and steps through the MCP.

### Conflict

- Show a diff between the local file and the Xray test.
- Ask the user how to resolve per test (keep local, keep server, or merge).
- Never overwrite a conflicting test without explicit user direction.

### Link to story

- Create requirement-coverage links between each test and its Jira story or requirement, based on `coveredRequirements` and `storyKey`.
- This is push plus link only. Do not pull server-side changes back into local files.

## ID lifecycle closure

- After a successful create, the internal `AGENT-###` identity is retired.
- The real Xray key becomes the identity in the filename, the `id` and `xrayKey` frontmatter, and `traceability.md`.
- Keep `coveredRequirements` intact so requirement traceability survives the swap.

## Report

After execution, report:

- created tests with their new Xray keys and old `AGENT-###` ids
- updated tests
- linked coverage
- skipped tests
- unresolved conflicts, if any

## Hard constraints

- Do not push without approval.
- Do not overwrite a conflicting test without explicit user direction.
- Do not pull server changes back into local files.
- Do not hardcode MCP tool names; resolve them at runtime.
- Do not author, score, or loop test cases here.
- Do not leave a created test with a stale `AGENT-###` filename or frontmatter.
- Do not break `coveredRequirements` traceability during the ID swap.

## Completion condition

This skill is complete when every in-scope test has been created, updated, skipped, or explicitly left as an unresolved conflict; all created tests carry their real Xray key in filename, frontmatter, and `traceability.md`; and the sync report has been delivered.
