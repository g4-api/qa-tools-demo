---
name: qa-xray-sync
description: Create or update Manual tests, Test Plans, Test Executions, Test associations, manual step outcomes, and Test Run statuses in Xray Cloud through dedicated MCP tools; validate every closed-schema payload, link coverage, reconcile internal AGENT-### ids, and return execution receipts. Use when local tests or completed execution journals must be synchronized with Xray.
---

# QA Xray Sync

## Purpose

Push locally authored Manual tests and execution journals into Xray Cloud, create planning and execution entities, and
close the test ID lifecycle by replacing internal `AGENT-###` identifiers with real Xray keys.

Use only the dedicated Xray tools in the routing table. Never substitute generic Jira issue tools. Read
[references/xray-tool-contracts.md](references/xray-tool-contracts.md) completely before planning or executing a
mutation.

This skill must:

1. resolve the sync target and explicit Xray destination,
2. inspect the exact required Xray tool contract,
3. classify each local test as CREATE, UPDATE, CONFLICT, or SKIP when synchronizing definitions,
4. construct and validate a closed-schema payload,
5. establish authorization from the direct request or owning orchestrator,
6. execute the exact routed Xray tool,
7. resolve conflicts with the user,
8. reconcile IDs only after a valid successful response, and
9. report the results.

## Supported operations

- Create a new Xray test from a local test file.
- Update an existing Xray test from local changes.
- Create a new Xray Test Plan from approved plan inputs.
- Create a Test Execution with its initial Tests and wait for registered Test Runs.
- Add Tests to an existing Test Execution and wait for registered Test Runs.
- Add Test Executions to an existing Test Plan.
- Record one-based manual step outcomes and update the final Test Run status.
- Link tests to a Jira story or requirement for coverage.
- Reconcile internal IDs with real Xray keys.
- Sync one finalized test inside `qa-orchestrate-test-cases`.

Do not use this skill to author, score, or loop test cases. Those belong to the create, review, and orchestrate skills.

## Batch and single-test modes

- **Batch**: sync a whole `<STORY-ID>/tests/` set. Present a complete sync plan only when the request asks for one or
  when a destination, conflict, or destructive action requires a new decision.
- **Single test**: sync exactly one finalized test. The orchestrator's upfront approval authorizes the payload only
  when it is derived exclusively from the approved test artifact and destination.
- **Test Plan**: create exactly one plan from explicitly approved inputs.
- **Execution**: create or resume one Test Execution, associate its Test and optional Test Plan, replay journal step
  results, and apply the Test Run status.

In every mode, surface conflicts and missing values. Never overwrite silently or invent a payload value.

## Interaction contract

1. Load the skill from the user request or orchestrator handoff.
2. Resolve only inputs the request did not set.
3. Inspect the exact mutation contract.
4. Treat a direct request to create, update, add, or synchronize an Xray entity as authorization for the exact
   non-destructive mutations required by that request.
5. Show the classification, exact tool name, and payload before execution only when the user requested a plan or when a
   required value is not already approved or derivable.
6. Validate again immediately before execution.
7. Call the exact tool, validate its response, and reconcile local state.

Do not request a duplicate approval for values derived only from finalized artifacts, execution journals, configured
destinations, or earlier tool responses. Stop when execution requires a new destination, destructive action, or conflict
resolution that the request did not authorize.

Use the MCP server's preconfigured PAT authentication. Never ask for, accept in a payload, display, or persist a username,
password, PAT, Basic-authentication value, or authorization header.

## Inputs to resolve

For test sync, resolve:

1. the `<STORY-ID>/tests/` set or specific test,
2. the explicit Jira project key and optional Test Repository destination, and
3. Xray MCP reachability.

For Test Plan creation, resolve:

1. required `project` and `summary`, and
2. only requested optional `description`, `jql`, `context`, and `customFields`.

For execution synchronization, resolve:

1. the finalized Xray Test key and execution journal,
2. either an existing Test Execution key or the project and summary required for creation,
3. an optional Test Plan key, and
4. only execution environments and custom fields already recorded or explicitly supplied.

Do not derive `project` silently from `storyKey`. Ask when the approved destination does not provide it.

## Exact tool routing

Use this routing without exceptions:

| Operation | Exact mutation tool |
| --- | --- |
| CREATE test | `new_xray_test` |
| UPDATE test | `update_xray_test` |
| CREATE Test Plan | `new_xray_test_plan` |
| ADD Tests to Test Plan | `add_xray_tests_to_plan` |
| CREATE Test Execution | `new_xray_execution` |
| ADD Tests to Test Execution | `add_xray_tests_to_execution` |
| ADD Test Executions to Test Plan | `add_xray_test_executions_to_plan` |
| UPDATE Test Run Step | `update_xray_execution_step` |
| UPDATE Test Run status | `update_xray_test_run_status` |

- Never use a generic Jira create/update issue tool for these operations.
- Never replace a required tool with another Xray tool or a generic Jira issue-link operation.
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

- Read YAML only from the metadata frontmatter. Parse Test Specifications, Test Setup, Steps, and Test Teardown from
  the readable Markdown body.
- In each action section, treat the top-level ordered item labeled Action as one Xray action and its nested ordered
  Expected results as that action's `expectedResults` array.
- Require action and expected-result numbering to start at `1`, remain gapless, and restart in each section. Stop on
  ambiguous nesting or missing labels.
- Construct a fresh payload from the selected tool's allowlist. Never pass parsed frontmatter, Markdown syntax, or a
  local artifact object directly.
- Follow `references/xray-tool-contracts.md` to the letter, including different `customFields` shapes for create and update.
- Enforce `additionalProperties: false` at the top level and in every closed nested object.
- Convert each explicitly numbered Expected results list to an array containing at least one string. Never split prose
  heuristically or send a scalar expected result.
- Omit absent optional properties. Do not send `null`, manufacture defaults, or infer content.
- For create calls, send `customFields` as an array of objects containing only string `name` and string `value`.
- For update calls, send `customFields` as a string-valued object. Reject duplicate source names instead of overwriting
  silently.
- Incorporate readable Test data into the corresponding `action`; no mutation schema accepts a separate data property.
- Validate all required properties, types, nested required properties, minimum array lengths, and property allowlists
  immediately before the tool call.
- When the interaction contract requires a plan, show the exact validated payload. Otherwise, record the exact validated
  payload immediately before the authorized call. Do not request another approval when every value is derived from
  approved inputs. Redact a value only when it is actually secret.
- For execution payloads, follow the execution schemas in the bundled contract and map only recorded terminal journal
  results. Never synthesize a Test result from the Test Execution Jira status or description.

## Execution

### Create a test

1. Parse the approved metadata-only YAML frontmatter and readable enumerated Markdown body into a fresh
   `new_xray_test` payload.
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

### Synchronize an execution

1. Read the complete execution journal and require a real Xray Test Jira key.
2. When no Test Execution exists, call `new_xray_execution` with the Test key in `testKeys`.
3. When a Test Execution already exists but lacks the Test, call `add_xray_tests_to_execution`.
4. When a Test Plan key is present, call `add_xray_test_executions_to_plan` with the resolved Test Execution key.
5. Replay each terminal authored step through `update_xray_execution_step` using its one-based authored step number.
6. Map `Passed` to `PASSED` and `Failed` to `FAILED` for step status updates.
7. Leave `Blocked`, `Skipped`, `Analysis pending`, and `Not run` unchanged unless an explicit Xray status mapping is
   configured.
8. After all steps have terminal results, call `update_xray_test_run_status` with `PASSED` when every step passed or
   `FAILED` when any step failed.
9. Validate every response envelope and return the synchronization receipt defined by the execution handoff contract.

The creation and association tools wait for Test Run registration internally. Do not add ad hoc sleeps or poll generic
Jira fields. Stop on an error envelope and report the exact failed tool; do not continue with later mutations.

### Resolve a conflict

- Show a field-level diff between the local file and Xray test.
- Ask the user to keep local, keep server, or merge for that test.
- Never overwrite a conflict without explicit direction.

### Link coverage

- After a successful mutation, create requested requirement-coverage links based on `coveredRequirements` and
  `storyKey` with the appropriate available link tool.
- Keep link calls separate from test definition and Test Plan mutation payloads because their closed schemas do not
  accept link fields.
- Do not pull server-side changes into local files.

## Report

Report:

- created tests with new Xray keys, links, and old `AGENT-###` ids,
- updated tests and links,
- created Test Plans and links,
- created or updated Test Executions, associated Tests, associated Test Plans, and Test Run identifiers,
- confirmed one-based step updates and the final Test Run status,
- linked coverage,
- skipped tests, and
- unresolved conflicts or failures.

## Hard constraints

- Do not mutate Xray without authorization from the direct request or owning orchestrator.
- Do not use any mutation tool except the exact tool mandated by the routing table.
- Do not call a mutation until its payload passes the bundled closed-schema contract.
- Do not accept YAML or serialized step objects in a test body.
- Do not sync a test that has not passed `md-code-compliance-review` with a score of 100 and zero linter errors.
- Do not overwrite a conflicting test without explicit user direction.
- Do not pull server changes into local files.
- Do not author, score, or loop test cases here.
- Do not reconcile an ID from an invalid or failed response.
- Do not ask for authentication identity or credentials; use the preconfigured PAT transport.
- Do not represent Test Execution membership with generic Jira links or description text.
- Do not treat HTTP success as mutation success when the response contains an error envelope.
- Do not leave a successfully created test with a stale `AGENT-###` filename or frontmatter.
- Do not break `coveredRequirements` traceability during an ID swap.

## Completion condition

Complete when every in-scope operation is created, updated, synchronized, skipped, or explicitly unresolved; every
successful response passed output validation; created tests carry real Xray keys in filename, frontmatter, and
traceability; requested execution results have a complete receipt; and the sync report is delivered.
