# QA Testing Tools — Skill Suite

A set of seven interactive skills for manual QA in VS Code + AI: turn requirements into
Xray-ready Manual test cases, quality-gate them with an automated review loop, sync them into
Xray, and version-control the results through per-test commits and a review-ready PR.

The skills live in [`skills/`](skills/).

## Guiding principle

Test artifacts are **first-class code files** — atomic, ID-named, individually reviewable,
version-controllable, and traceable. Bring the developer's state of mind to QA.

## The skills

| # | Skill | Role |
|---|---|---|
| 1 | `qa-decompose-requirements` | Read a document or Jira story (Atlassian MCP) and decompose it into atomic, ID-tagged, testable requirements. |
| 2 | `qa-create-test-cases` | Author / update / refactor Manual Xray test cases from the requirements, one file per test. |
| 3 | `qa-review-test-cases` | Score each test on a fixed weighted rubric; enforce the per-test **>95** gate; report and route (never edits files). |
| 4 | `qa-orchestrate-test-cases` | Drive the sequential per-test loop (create→review-fix→sync→commit) until every test **>95**, then batch-commit meta and open a PR. |
| 5 | `qa-xray-sync` | Create/update tests in Xray via MCP (batch or single-test), link to the story, and swap internal IDs for real Xray keys. |
| 6 | `qa-git-commit` | Commit each finalized test (and the meta files) to `qa/<STORY-ID>-tests` via a GitHub MCP, one commit per test. |
| 7 | `qa-github-pr` | Open one detailed, ready-for-review PR when the cycle completes. |

## Flow

```
requirement (doc / Jira)
        │
        ▼
[1] qa-decompose-requirements ──► requirements.md
        │
        ▼
[4] qa-orchestrate-test-cases  (single approval, then automated)
        │  plan coverage, then FOR EACH test:
        │   [2] qa-create-test-cases ──► tests/AGENT-###.md
        │   [3] qa-review-test-cases ──► score; fix ↺ until > 95
        │   [5] qa-xray-sync (if asked/available) ──► real Xray key, update IDs
        │   [6] qa-git-commit ──► commit finalized test
        │   next test
        │
        │  then: [6] batch meta commit (requirements.md, traceability.md)
        ▼
   detailed report ──► [7] qa-github-pr ──► ready-for-review PR
```

Skills 2, 3, 5, 6, 7 can also be run standalone; skill 4 is the normal entry point for a full run.

## Upstream (product): `po-author-requirements`

A product-owner skill that feeds the QA suite. From an epic-level prompt (e.g. "login screen")
it drives scope to 100%, plans an **epic → feature → story** tree, builds it **in context only
(no file)**, then optionally creates it in an **existing** Jira project via the Atlassian MCP
(a missing project is a hard blocker). The Story keys it creates become the `STORY-ID`s that
`qa-decompose-requirements` works from.

```
epic prompt ──► [po-author-requirements] ──► epic/feature/story in Jira ──► Story keys
                                                                              │
                                                                              ▼
                                                              [1] qa-decompose-requirements …
```

It uses the `po-` prefix (product), distinct from the `qa-` test suite.

## Shared interaction contract

Every skill: **user prompt → skill loads → ask guiding questions → show a plan → wait for
approval → execute.** Skills stop and ask whenever they are in doubt. The orchestrator takes
a *single* upfront approval and then runs the fix loop automatically to the goal.

## Workspace & ID conventions

```
<workspace-root>/            # default ./qa-workspace (hybrid: persist by default, inline on request)
  <STORY-ID>/                # Jira/Xray story key, else internal AGENT-S###
    requirements.md          # decomposition + REQ-### traceability IDs
    traceability.md          # REQ-ID → test-ID matrix
    tests/
      AGENT-000.md           # one Manual test per file; Markdown + YAML frontmatter
```

- **Requirements** get stable `REQ-###` IDs (story-scoped, from `REQ-000`).
- **Tests** get internal `AGENT-###` IDs (story-scoped, from `AGENT-000`).
- On Xray sync, the internal ID is **replaced** by the real Xray key in the filename,
  frontmatter, and `traceability.md` — closing the loop end to end.

## Standards

Review anchors to **General best practice** by default; the user may select **ISTQB** or
**ISTQB + ISO/IEC/IEEE 29119** per run.

---

# Reference: Jira `additional_fields` parsing

Reference notes for the Jira-facing skills (`qa-decompose-requirements`, `qa-xray-sync`) when
creating or updating issues through the Atlassian MCP wrapper.

## How `additional_fields` is parsed (what the code does)

* It lower-cases each key and looks it up in a **field map** (from `_generate_field_map()`).
* It treats keys that **start with `customfield_`** as **direct Jira field IDs** (skips the map).
* It **ignores** `parent`, `assignee`, and `components` inside `additional_fields` (they’re handled elsewhere).
* It formats a few known fields (`priority`, `labels`, `fixVersions/versions/components`, `reporter`, `duedate`, `datetime` types). Everything else is sent **as-is**, so you must supply the correct Jira shape for that field’s schema.

---

## Custom fields — two safe ways

### By **ID** (always works)

Use the exact Jira ID (e.g., `customfield_10081`).

> Note: `custom_111` won’t work. It must be `customfield_#####`.

```json
"additional_fields": {
    "customfield_10081": "High business impact", // Text field
    "customfield_10082": 3.5, // Number field
    "customfield_10083": {
        "value": "EMEA"
    }, // Single select
    "customfield_10084": [
        {
            "value": "iOS"
        },
        {
            "value": "Web"
        }
    ], // Multi select
    "customfield_10085": {
        "accountId": "abc123"
    }, // User picker (Cloud)
    "customfield_10086": "2025-09-15", // Date (YYYY-MM-DD)
    "customfield_10087": "2025-09-15T13:00:00Z" // DateTime (ISO-8601)
}
```

### By **name** (if your field map exposes it)

If `_generate_field_map()` maps names → IDs, you can pass the **field’s display name** (case-insensitive). The code will resolve it.

```json
"additional_fields": {
    "Business Impact": "High",
    "Region": {
        "value": "EMEA"
    },
    "Platforms": [
        {
            "value": "iOS"
        },
        {
            "value": "Web"
        }
    ]
}
```

> If a key isn’t in the map **and** doesn’t start with `customfield_`, you’ll see “Ignoring unrecognized field …” in logs.

---

## `issueLinks` format (and directionality)

The code will lower-case your key and map `issueLinks` → `issuelinks` (if present in the map). It doesn’t reformat the value, so you must provide the proper Jira structure:

```json
"additional_fields": {
    "issueLinks": [
        {
            "type": { "name": "Relates" },
            "inwardIssue": { "key": "ADN-4" }
        }
    ]
}
```

**Direction matters** for some link types:

```json
{
    "issueLinks": [
        {
            "type": {
                "name": "Blocks"
            },
            "outwardIssue": {
                "key": "ADN-4"
            }
        }
    ]
}
```

* `"type": {"name":"Blocks"}`

  * Use **`outwardIssue`** if the new issue **blocks** the target.
  * Use **`inwardIssue`** if the new issue **is blocked by** the target.

Examples:

```json
{
    "issueLinks": [
        {
            "type": {
                "name": "Blocks"
            },
            "outwardIssue": {
                "key": "ADN-4"
            }
        }
    ]
}
// New issue IS BLOCKED BY ADN-4
{
    "issueLinks": [
        {
            "type": {
                "name": "Blocks"
            },
            "inwardIssue": {
                "key": "ADN-4"
            }
        }
    ]
}
```

> Heads-up: Some Jira Cloud configs **don’t allow** setting `issuelinks` during **create**. If you get a 400 for links specifically, create the issue first, then call the link endpoint (your MCP server may expose a `link_issue` helper).

---

## Putting it together

### Sub-task (use `parent` as a **string** outside `additional_fields`, per your wrapper)

```json
{
    "project_key": "ADN",
    "summary": "Enforce password policy on reset",
    "issue_type": "Sub-task",
    "description": "...",
    "parent": "ADN-4", // <- your wrapper converts this to {"key": "..."}
    "additional_fields": {
        "customfield_10081": "High business impact",
        "labels": [
            "security",
            "passwords"
        ],
        "fixVersions": [
            "Q4-2025"
        ], // strings become {"name": "..."} via formatter
        "issueLinks": [
            {
                "type": {
                    "name": "Relates"
                },
                "inwardIssue": {
                    "key": "ADN-12"
                }
            }
        ]
    }
}
```

### Task (no `parent`; link via `issueLinks`)

```json
{
    "project_key": "ADN",
    "summary": "Implement password reset request via email/SMS",
    "issue_type": "Task",
    "description": "...",
    "additional_fields": {
        "labels": "auth, reset, notifications", // comma string -> ["auth","reset","notifications"]
        "priority": "High", // becomes {"name":"High"}
        "issueLinks": [
            {
                "type": {
                    "name": "Relates"
                },
                "inwardIssue": {
                    "key": "ADN-4"
                }
            }
        ],
        "customfield_10086": "2025-09-15", // Date
        "customfield_10087": "2025-09-15T13:00:00Z"
    }
}
```

---

## Quick checklist

* ✅ For **custom fields**, prefer `customfield_#####`. Names work only if your field map includes them.
* ✅ Don’t put `parent`, `assignee`, or `components` inside `additional_fields` (the code skips them).
* ✅ For `issueLinks`, provide the exact Jira shape; choose `inwardIssue`/`outwardIssue` to match the link type’s direction.
* ✅ For `labels`, you can pass a list or a comma-separated string (the formatter will split it).
* ✅ For `priority`, pass a string name or a dict with `name`/`id`.
* ✅ For `datetime` schema fields, pass an ISO timestamp string; the formatter will attempt to normalize.

If you hit a specific field error, log the field’s **schema** (from `get_field_by_id`) and shape the value accordingly.
