# Defect Contract

## Required content

Create these readable sections in order:

1. Summary.
2. Problem Statement.
3. Environment.
4. Preconditions.
5. Steps to Reproduce.
6. Expected Result.
7. Actual Result.
8. Impact.
9. Evidence.
10. Analysis Summary.
11. Relevant References.
12. Attachments.

Enumerate every environment fact, precondition, reproduction step, expected result, actual observation, impact, evidence
reference, analysis fact, related reference, and attachment. Use `None` only when an optional collection is empty.

## Quality rules

1. Write a concise summary that identifies the affected capability, condition, and observed failure.
2. State the problem using observed behavior, not a speculative root cause.
3. Copy reproduction facts from the finalized test and execution journal.
4. Make every reproduction step atomic and executable.
5. Keep expected and actual results separate and directly comparable.
6. Describe user or system impact without inventing severity or frequency.
7. Reference evidence by stable path, link, timestamp, or identifier.
8. Include analysis classification and confidence as analysis, not observation.
9. Include story, requirement, test, execution, repository, documentation, and related-defect references when available.
10. Never include credentials, access tokens, personal data unrelated to reproduction, or hidden reasoning.

## Metadata

For a persistent Markdown defect artifact, keep YAML only in frontmatter. Use these fields:

| Field | Type | Rule |
| --- | --- | --- |
| `id` | String | Draft identifier until Jira returns a real key. |
| `jiraKey` | String or null | Set only from a validated successful response. |
| `status` | String | `drafted`, `created`, or `failed`. |
| `storyId` | String | Owning story identifier. |
| `testId` | String | Failed test identifier. |
| `executionId` | String | Source execution identifier. |
| `step` | Integer | Failed authored step number. |
| `requirements` | Array of strings | Stable affected requirement identifiers. |
| `createdAt` | String | Observed ISO 8601 timestamp. |
| `updatedAt` | String | Observed ISO 8601 timestamp. |

## Receipt

Return these values to the execution skill:

1. Status.
2. Final summary.
3. Jira key when created.
4. Internal identifier when returned.
5. Direct link when returned.
6. Local artifact path when written.
7. Execution, test, step, and requirement references.
8. Failure reason when status is `failed`.
