# Jira Defect Tool Contract

## Tool selection

Use the available Atlassian Jira tool whose live schema explicitly creates an issue. Prefer `jira_create_issue` when that
exact tool is available. Do not guess a tool name, use a generic HTTP request, or substitute an Xray mutation tool.

Stop before mutation when no Jira create-issue tool is available.

## Schema inspection

Immediately before constructing the payload:

1. Inspect the selected tool's current input schema.
2. Confirm that it supports the explicit project, summary, issue type, and description.
3. Confirm the exact property names and required properties.
4. Confirm the accepted custom-field shapes when custom fields are requested.
5. Build a fresh object containing only schema-supported properties.
6. Validate the candidate payload against the inspected schema.

Never forward defect frontmatter, the execution journal, or an arbitrary local object directly to the tool.

## Required semantic values

Require these semantic values even when the tool uses different property names:

| Value | Rule |
| --- | --- |
| Project | Use the explicit approved Jira destination. |
| Summary | Use the final defect summary. |
| Issue type | Use `Bug`; stop when that type is unavailable. |
| Description | Render the approved readable defect content in the format accepted by the tool. |

Include priority, labels, components, versions, assignee, links, and custom fields only when grounded, approved, and
supported by the inspected schema. Do not manufacture defaults.

## Approval

The tester's approval to create the defect authorizes a payload derived exclusively from recorded execution facts, the
analysis response, and the explicit destination. Request new approval when synchronization introduces a new material value,
chooses between duplicate handling options, or changes the approved meaning.

## Response validation

Treat creation as successful only when the response contains the non-empty issue key and every other value required by the
live output contract. Record an identifier or link only when returned or deterministically documented by the tool contract.

Return `failed` on a tool error, invalid response, permission failure, or ambiguous creation result. Never retry a mutation
that may have succeeded until Jira is searched for the candidate issue.
