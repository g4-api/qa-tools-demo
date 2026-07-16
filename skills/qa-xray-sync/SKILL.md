---
name: qa-xray-sync
description: Create or update Manual tests and create Test Plans in Xray Cloud through the exact new_xray_test, update_xray_test, and new_xray_test_plan MCP tools; validate every closed-schema payload, link tests to requirements, and reconcile internal AGENT-### ids to real Xray keys. Use when local test cases must be pushed to Xray, existing Xray tests must be updated, or a new Xray Test Plan must be created.
---

# QA Xray Sync

## Purpose

Push locally authored Manual test files into Xray Cloud, create Test Plans, and close the test ID lifecycle by replacing internal `AGENT-###` identifiers with real Xray keys.

Use the three exact Xray mutation tools. Never substitute generic Jira issue tools. Read [references/xray-tool-contracts.md](references/xray-tool-contracts.md) completely before planning or executing a mutation.

This skill must:

1. resolve the sync target and explicit Xray destination,
2. inspect the exact required Xray tool contract,
3. classify each local test as CREATE, UPDATE, CONFLICT, or SKIP,
4. construct and validate a closed-schema payload,
5. show the exact tool and payload in a sync plan and wait for approval,
6. execute the exact create, update, or Test Plan tool,
7. resolve conflicts with the user,
8. reconcile IDs only after a valid successful response, and
9. report the results.

## Supported operations

- Create a new Xray test from a local test file.
- Update an existing Xray test from local changes.
- Create a new Xray Test Plan from approved plan inputs.
- Link tests to a Jira story or requirement for coverage.
- Reconcile internal IDs with real Xray keys.
- Sync one finalized test inside `qa-orchestrate-test-cases`.

Do not use this skill to author, score, or loop test cases. Those belong to the create, review, and orchestrate skills.

## Batch and single-test modes

- **Batch**: sync a whole `<STORY-ID>/tests/` set. Standalone use presents the complete sync plan and waits for approval.
- **Single test**: sync exactly one finalized test. The orchestrator's upfront approval authorizes the payload only when it is derived exclusively from the approved test artifact and destination.
- **Test Plan**: create exactly one plan from explicitly approved inputs.

In every mode, surface conflicts and missing values. Never overwrite silently or invent a payload value.

## Interaction contract

1. Load the skill from the user request or orchestrator handoff.
2. Resolve only inputs the request did not set.
3. Inspect the exact mutation contract.
4. In standalone mode, show the classification, exact tool name, and exact candidate payload.
5. In standalone mode, wait for approval because the operation writes to an external system.
6. Validate again immediately before execution.
7. Call the exact tool, validate its response, and reconcile local state.

The orchestrator's single upfront approval replaces the standalone approval only for pre-approved single-test and Test Plan operations. Stop if execution would require a new unapproved value.

## Inputs to resolve

For test sync, resolve:

1. the `<STORY-ID>/tests/` set or specific test,
2. the explicit Jira project key and optional Test Repository destination, and
3. Xray MCP reachability.

For Test Plan creation, resolve:

1. required `project` and `summary`, and
2. only requested optional `description`, `jql`, `context`, and `customFields`.

Do not derive `project` silently from `storyKey`. Ask when the approved destination does not provide it.

## Exact tool routing

Use this routing without exceptions:

| Operation | Exact mutation tool |
|---|---|
| CREATE test | `new_xray_test` |
| UPDATE test | `update_xray_test` |
| CREATE Test Plan | `new_xray_test_plan` |

- Never use a generic Jira create/update issue tool for these operations.
- Never replace one required tool with another Xray tool.
- Stop and report the exact missing tool when it is unavailable.
- Treat these contracts as Xray Cloud contracts. Do not silently adapt them to Xray Server or Data Center.

## Contract inspection

Before constructing a mutation payload:

1. Read `references/xray-tool-contracts.md`.
2. If `get_xray_tool_metadata` is available, call it with the selected exact mutation tool name.
3. Verify that the returned `name` matches exactly and that its input schema agrees with the bundled contract.
4. Stop without mutating Xray if the live schema and bundled contract differ.

## Sync classification

For each local test file:

- **CREATE**: no `xrayKey`; call `new_xray_test`.
- **UPDATE**: has an `xrayKey`, differs from the Xray test, and has no server-side divergence; call `update_xray_test`.
- **CONFLICT**: has an `xrayKey` and the Xray test changed independently; show a diff and ask how to resolve it.
- **SKIP**: local and server values are equal, or an update would contain `key` alone; do not call a mutation tool.

## Payload construction and validation

- Construct a fresh payload from the selected tool's allowlist. Never pass parsed frontmatter or a local artifact object directly.
- Follow `references/xray-tool-contracts.md` to the letter, including different `customFields` shapes for create and update.
- Enforce `additionalProperties: false` at the top level and in every closed nested object.
- Preserve `expectedResults` as an array containing at least one string. Never send a scalar expected result.
- Omit absent optional properties. Do not send `null`, manufacture defaults, or infer content.
- For create calls, send `customFields` as an array of objects containing only string `name` and string `value`.
- For update calls, send `customFields` as a string-valued object. Reject duplicate source names instead of overwriting silently.
- Incorporate optional local `data` into the corresponding human-readable `action`; no mutation schema accepts `data`.
- Validate all required properties, types, nested required properties, minimum array lengths, and property allowlists immediately before the tool call.
- In standalone mode, show the exact validated payload in the approval plan. In orchestrated mode, record the exact validated payload immediately before the call; do not request another approval when every value is derived from approved inputs. Redact a value only when it is actually secret.

## Execution

### Create a test

1. Map the approved artifact into a fresh `new_xray_test` payload.
2. Require string `project` and string `scenario`.
3. Validate and call `new_xray_test`.
4. Require non-empty string `id`, `key`, and `link` in the response.
5. Rename `AGENT-###.md` to `<XRAYKEY>.md`.
6. Set `xrayKey` and `id` in frontmatter to the returned key.
7. Record `AGENT-### -> <XRAYKEY>` in `traceability.md`.

Do not reconcile any local identifier when the call or response validation fails.

### Update a test

1. Treat the local file as the source of truth for non-conflicting supported fields.
2. Build a fresh `update_xray_test` payload with `key` plus only changed supported fields.
3. Classify a payload containing `key` alone as SKIP.
4. Validate and call `update_xray_test`.
5. Require non-empty string `id`, `key`, and `link` in the response.

### Create a Test Plan

1. Build a fresh `new_xray_test_plan` payload from the approved inputs.
2. Require string `project` and string `summary`.
3. Include only requested optional `description`, `jql`, `context`, and create-shaped `customFields`.
4. Validate and call `new_xray_test_plan`.
5. Require non-empty string `id`, `key`, and `link` in the response.
6. Report the returned values.

### Resolve a conflict

- Show a field-level diff between the local file and Xray test.
- Ask the user to keep local, keep server, or merge for that test.
- Never overwrite a conflict without explicit direction.

### Link coverage

- After a successful mutation, create requested requirement-coverage links based on `coveredRequirements` and `storyKey` with the appropriate available link tool.
- Keep link calls separate from the three mutation payloads because their closed schemas do not accept link fields.
- Do not pull server-side changes into local files.

## Report

Report:

- created tests with new Xray keys, links, and old `AGENT-###` ids,
- updated tests and links,
- created Test Plans and links,
- linked coverage,
- skipped tests, and
- unresolved conflicts or failures.

## Hard constraints

- Do not push without the applicable approval.
- Do not use any mutation tool except the exact tool mandated by the routing table.
- Do not call a mutation until its payload passes the bundled closed-schema contract.
- Do not overwrite a conflicting test without explicit user direction.
- Do not pull server changes into local files.
- Do not author, score, or loop test cases here.
- Do not reconcile an ID from an invalid or failed response.
- Do not leave a successfully created test with a stale `AGENT-###` filename or frontmatter.
- Do not break `coveredRequirements` traceability during an ID swap.

## Completion condition

Complete when every in-scope operation is created, updated, skipped, or explicitly unresolved; every successful response passed output validation; created tests carry real Xray keys in filename, frontmatter, and traceability; and the sync report is delivered.
