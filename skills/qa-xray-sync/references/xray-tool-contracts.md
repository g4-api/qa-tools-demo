# Xray mutation tool contracts

Read this file before constructing any Xray mutation call.
These contracts come from the authoritative definitions in `Mcp.Xray.Domain/Definitions`.

## Mandatory routing

| Operation | Exact tool | Required inputs |
| --- | --- | --- |
| Create a test | `new_xray_test` | `project`, `scenario` |
| Create a Test Plan | `new_xray_test_plan` | `project`, `summary` |
| Update a test | `update_xray_test` | `key` |
| Add Tests to a Test Plan | `add_xray_tests_to_plan` | `key`, `jql` |
| Create a Test Execution | `new_xray_execution` | `project`, `summary`, `testKeys` |
| Add Tests to a Test Execution | `add_xray_tests_to_execution` | `executionKey`, `testKeys` |
| Add Test Executions to a Test Plan | `add_xray_test_executions_to_plan` | `testPlanKey`, `testExecutionKeys` |
| Update a Test Run Step | `update_xray_execution_step` | `executionKey`, `testKey`, `stepNumber`, one outcome |
| Update a Test Run status | `update_xray_test_run_status` | `executionKey`, `testKey`, `status` |

Do not substitute a generic Jira issue tool or a differently named Xray tool for these operations.

All input schemas are closed at the top level (`additionalProperties: false`).
Never forward a local artifact object directly.
Construct a new allowlisted payload for the selected tool.

Authentication is preconfigured through the MCP server's Personal Access Token (PAT) transport. None of these tools
accept authentication properties. Never add a username, password, PAT, cookie, Basic-authentication value, or
authorization header to a payload.

## `new_xray_test`

Allowed top-level properties:

| Property | Type | Rules |
| --- | --- | --- |
| `project` | string | Required Jira project key. |
| `scenario` | string | Required human-readable test title. |
| `testSpecifications` | string | Optional detailed specification. |
| `categories` | array of strings | Optional. |
| `priority` | string | Optional. |
| `severity` | string | Optional. |
| `tolerance` | number | Optional. Do not send a numeric string. |
| `customFields` | array | Optional. Every item must contain only string `name` and string `value`; both are required. |
| `testSetup` | array | Optional structured step array. |
| `steps` | array | Optional structured step array. |
| `testTeardown` | array | Optional structured step array. |

Every structured step item must contain only:

```json
{
    "action": "string",
    "expectedResults": [
        "one or more strings"
    ]
}
```

Both properties are required, and `expectedResults` must contain at least one item.

Example:

```json
{
    "project": "PROJ",
    "scenario": "Reject an invalid password",
    "testSpecifications": "Verify that invalid credentials do not create a session.",
    "categories": [
        "authentication",
        "negative"
    ],
    "priority": "High",
    "severity": "Major",
    "steps": [
        {
            "action": "Submit the login form with a valid username and an invalid password.",
            "expectedResults": [
                "The request is rejected.",
                "No authenticated session is created."
            ]
        }
    ]
}
```

## `new_xray_test_plan`

Allowed top-level properties:

| Property | Type | Rules |
| --- | --- | --- |
| `project` | string | Required Jira project key. |
| `summary` | string | Required human-readable Test Plan title. |
| `description` | string | Optional. |
| `jql` | string | Optional test-selection JQL. |
| `context` | object | Optional arbitrary key-value data. Values may be string, number, integer, boolean, object, array, or null. |
| `customFields` | array | Optional. Every item must contain only string `name` and string `value`; both are required. |

Example:

```json
{
    "project": "PROJ",
    "summary": "Authentication regression",
    "description": "Regression plan for authentication stories.",
    "jql": "key in (PROJ-101, PROJ-102)",
    "context": {
        "environment": "staging",
        "browser": "Chrome"
    },
    "customFields": [
        {
            "name": "Test Level",
            "value": "System"
        }
    ]
}
```

## `add_xray_tests_to_plan`

Allowed top-level properties:

| Property | Type | Rules |
| --- | --- | --- |
| `key` | string | Required existing Test Plan Jira key. |
| `jql` | string | Required query selecting the Tests added to the Test Plan. |

## `new_xray_execution`

Allowed top-level properties:

| Property | Type | Rules |
| --- | --- | --- |
| `project` | string | Required Jira project key. |
| `summary` | string | Required human-readable Test Execution summary. |
| `testKeys` | array of strings | Required, unique, and non-empty. |
| `description` | string | Optional. |
| `testEnvironments` | array of strings | Optional unique environment names. |
| `customFields` | array | Optional create-shaped custom fields with string `name` and JSON-compatible `value`. |

Accept success only when the response contains non-empty string `id`, `key`, and `link`; arrays `testKeys`,
`testRunIds`, `createdTestEnvironments`, and `warnings` must also be present. The tool waits for every Test Run before
returning success.

Example:

```json
{
    "project": "PROJ",
    "summary": "Authentication manual execution",
    "testKeys": [
        "PROJ-101"
    ],
    "testEnvironments": [
        "staging"
    ]
}
```

## `add_xray_tests_to_execution`

Allowed top-level properties:

| Property | Type | Rules |
| --- | --- | --- |
| `executionKey` | string | Required existing Test Execution Jira key. |
| `testKeys` | array of strings | Required, unique, and non-empty. |

Accept success only when the response contains non-empty `executionId` and `executionKey`; arrays `testIds`,
`testKeys`, `testRunIds`, and `warnings` must also be present. The tool waits for every requested Test Run before
returning success.

## `add_xray_test_executions_to_plan`

Allowed top-level properties:

| Property | Type | Rules |
| --- | --- | --- |
| `testPlanKey` | string | Required existing Test Plan Jira key. |
| `testExecutionKeys` | array of strings | Required, unique, and non-empty. |

Accept success only when the response contains non-empty `testPlanId` and `testPlanKey`; arrays `testExecutionIds`,
`testExecutionKeys`, and `warnings` must also be present.

## `update_xray_execution_step`

Allowed top-level properties:

| Property | Type | Rules |
| --- | --- | --- |
| `executionKey` | string | Required Test Execution Jira key. |
| `testKey` | string | Required Test Jira key. |
| `stepNumber` | integer | Required one-based authored step number. |
| `actualResult` | string | Optional observed result; empty clears the current value. |
| `comment` | string | Optional execution comment; empty clears the current value. |
| `status` | string | Optional Xray Test Run Step status. |
| `iterationRank` | string | Optional data-set iteration rank. |

Require at least one of `actualResult`, `comment`, or `status`. The tool waits for Test Run registration before selecting
the opaque step identifier. Accept success only when the response contains execution, Test, Test Run, and step identities
together with the one-based `stepNumber` and `warnings`.

## `update_xray_test_run_status`

Allowed top-level properties:

| Property | Type | Rules |
| --- | --- | --- |
| `executionKey` | string | Required Test Execution Jira key. |
| `testKey` | string | Required Test Jira key. |
| `status` | string | Required Xray Test Run status name or identifier. |

Accept success only when the response contains non-empty execution, Test, and Test Run identities plus the non-empty
status value confirmed by Xray.

## `update_xray_test`

Allowed top-level properties:

| Property | Type | Rules |
| --- | --- | --- |
| `key` | string | Required existing Xray test key. |
| `scenario` | string | Optional replacement title. |
| `testSpecifications` | string | Optional replacement specification. |
| `categories` | array of strings | Optional replacement list. |
| `priority` | string | Optional. |
| `severity` | string | Optional. |
| `tolerance` | number | Optional. |
| `customFields` | object | Optional string-valued field map. This is not the array shape used by the create tools. |
| `testSetup` | array | Optional replacement structured step array. |
| `steps` | array | Optional replacement structured step array. |
| `testTeardown` | array | Optional replacement structured step array. |

The three structured arrays use the same item shape as `new_xray_test`.
Send only fields intended to change.
Do not call the tool with `key` alone; classify that case as `SKIP`.

Example:

```json
{
    "key": "PROJ-101",
    "scenario": "Reject invalid credentials",
    "customFields": {
        "Test Level": "System"
    },
    "steps": [
        {
            "action": "Submit invalid credentials.",
            "expectedResults": [
                "Authentication is rejected."
            ]
        }
    ]
}
```

## Local-to-tool mapping

| Local test artifact | Create payload | Update payload |
| --- | --- | --- |
| Explicit sync destination `project` | `project` | Not accepted; omit. |
| `summary` | `scenario` | `scenario` when changed. |
| `## Test Specifications` | `testSpecifications` | `testSpecifications` when changed. |
| `labels` or `categories` | `categories` | `categories` when changed. |
| `priority` | `priority` | `priority` when changed. |
| `severity` | `severity` | `severity` when changed. |
| `tolerance` | `tolerance` | `tolerance` when changed. |
| Local custom-field list | `customFields` array | Convert to a string-valued object; reject duplicate names. |
| Numbered actions under `## Test Setup` | `testSetup` | `testSetup` when changed. |
| Numbered actions under `## Steps` | `steps` | `steps` when changed. |
| Numbered actions under `## Test Teardown` | `testTeardown` | `testTeardown` when changed. |
| `xrayKey` | Not accepted; omit. | `key`. |
| `id`, `type`, `folder`, `testSets`, `coveredRequirements`, `storyKey`, `status`, `data` | Not accepted; omit. | Not accepted; omit. |

Read YAML only from metadata frontmatter.
For each Markdown action, remove enumeration and presentation labels.
Incorporate optional Test data into the human-readable `action`.
Convert the nested numbered Expected results list into `expectedResults`.
No mutation schema accepts a separate data property.
Reject gaps, ambiguous nesting, missing labels, or unnumbered results.
Never split prose heuristically.

## Validation sequence

Before every mutation:

1. Select the exact tool from the mandatory routing table.
2. Inspect live metadata when `get_xray_tool_metadata` is available.
    1. Call it with the selected exact tool name.
    2. Verify that the returned `name` and input schema agree with this contract.
    3. Stop on a mismatch.
3. Construct a fresh payload using only the selected tool's allowlist.
4. Verify required properties, primitive types, nested required properties, and `expectedResults` minimum length.
5. Verify that no additional property remains at any closed-object level.
6. Record the exact payload.
    1. Show it when the interaction contract requires a plan or unresolved-value decision.
    2. Otherwise, record it immediately before the authorized call.
    3. Redact secrets when applicable.
7. Invoke the exact mutation tool.
8. Accept success only when the result contains non-empty string `id`, `key`, and `link`.

For non-create execution tools, apply the operation-specific success fields documented above instead of the generic
`id`, `key`, and `link` rule. Treat an `error` and `message` envelope as failure even when transport status is successful.
