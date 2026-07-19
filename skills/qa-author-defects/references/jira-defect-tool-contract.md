# Jira Defect Tool Contract

## Tool selection

Use the available Atlassian Jira tool whose live schema explicitly creates an issue. Prefer `jira_create_issue` when that
exact tool is available. Do not guess a tool name, use a generic HTTP request, or substitute an Xray mutation tool.

Also resolve live Jira tools whose schemas explicitly create an issue link and read issue relationships. Prefer an exact
tool name only when it exists and its inspected schema confirms the required operation. Do not infer link behavior from a
generic issue-update tool.

Stop before mutation when no Jira create-issue tool is available. After Bug creation, return `created-unlinked` when the
required link or read-back operation is unavailable.

## Schema inspection

Immediately before constructing the payload:

1. Inspect the selected tool's current input schema.
2. Confirm that it supports the explicit project, summary, issue type, and description.
3. Confirm the exact property names and required properties.
4. Confirm the accepted custom-field shapes when custom fields are requested.
5. Build a fresh object containing only schema-supported properties.
6. Validate the candidate payload against the inspected schema.

Never forward defect frontmatter, the execution journal, or an arbitrary local object directly to the tool.

## Required creation values

Require these semantic values even when the tool uses different property names:

| Value | Rule |
| --- | --- |
| Project | Use the explicit approved Jira destination. |
| Summary | Use the final defect summary. |
| Issue type | Use `Bug`; stop when that type is unavailable. |
| Description | Render the approved readable defect content in the format accepted by the tool. |

Include priority, labels, components, versions, assignee, and custom fields only when grounded, approved, and supported by
the inspected schema. Do not manufacture defaults or encode the mandatory relationship as description text.

## Required relationship

Every created Bug must have this Jira issue relationship:

| Value | Rule |
| --- | --- |
| Link type | Use the supported Jira link type whose exact name is `Defect`. |
| Source issue | Use the originating Xray Test key from the approved execution handoff. |
| Target issue | Use the validated key of the created Jira Bug. |
| Direction | Preserve the Jira direction rendered as the Test `created` the Bug. |

Inspect Jira's supported link-type metadata before mutation. Map source, target, inward, and outward properties according
to the live schema; do not guess property names or reverse the issues to fit an assumed payload.

## Relationship sequence

1. Inspect the issue-link mutation schema and the issue-read schema.
2. Confirm that the exact `Defect` link type and required direction are supported.
3. Read or search the originating Test and created Bug for an equivalent relationship.
4. Skip creation when the same link type, issue pair, and direction already exist.
5. Build a fresh link payload containing only schema-supported properties.
6. Validate required properties, types, nested objects, and property allowlists.
7. Execute the exact issue-link mutation only when the relationship is missing.
8. Read the relationship back from Jira.
9. Verify the exact link type, originating Test key, created Bug key, and direction.

Description text, local references, labels, remote links, and Xray execution membership do not satisfy this relationship.

## Approval

The tester's approval to create the defect authorizes the Jira Bug and its mandatory originating-Test relationship when
both derive exclusively from recorded execution facts, the analysis response, and the explicit destination. Request new
approval when synchronization introduces a new material value, chooses between duplicate handling options, or changes the
approved meaning.

## Response validation

Treat Bug creation as valid only when the response contains the non-empty issue key and every other value required by the
live output contract. Record an identifier or direct issue URL only when returned or deterministically documented by the
tool contract.

Return `created-and-linked` only after read-back verifies the required relationship. Return `created-unlinked` when the Bug
exists but the relationship cannot be created or verified. Return `failed` when Bug creation fails or remains ambiguous.

Never retry a mutation that may have succeeded until Jira is searched for the candidate issue or relationship. Once a Bug
key is validated, retain it and recover only the missing relationship; never create a replacement Bug to repair linking.
