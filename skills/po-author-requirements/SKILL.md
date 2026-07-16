---
name: po-author-requirements
description: Turn an epic-level prompt into a scoped epic-feature-story requirements tree, then optionally create it in an existing Jira project via the Atlassian MCP. Use when a product owner wants to break down an epic (for example "login screen") into features and stories, drive the scope to full clarity, review the tree, and push it into Jira. Requires the target Jira project up front for creation; a missing project is a hard blocker.
---

# PO Author Requirements

## Purpose

This skill is a product-owner tool that sits upstream of the QA test suite. It breaks an epic down into a feature and story tree, and can create that tree in Jira.

The Story keys it creates become the `STORY-ID`s that `qa-decompose-requirements` later works from.

This skill must:
1. drive the scope to full clarity from an epic-level prompt,
2. plan the epic-feature-story tree and get approval,
3. build the tree in context only, not in a file,
4. ask whether to create it in Jira and on which project,
5. detect and confirm the issue-type mapping,
6. create the tree in Jira and report the created keys.

## Use this skill when

Use this skill when the task is about:
- breaking an epic into features and stories
- authoring a requirements tree from a product prompt
- creating epics, features, and stories in Jira
- preparing stories that the QA suite will later decompose into tests

Do not use this skill to write test cases, decompose an existing story, or sync tests to Xray. Those belong to the QA suite.

## Scope of this skill

This skill authors requirements. It does not author tests. After creation, hand the Story keys to `qa-decompose-requirements`.

## Interaction contract

1. **Load** — triggered by an epic-level prompt (for example "login screen").
2. **Scope to 100%** — ask guiding questions until the scope is fully clear.
3. **Show the tree plan** — the proposed epic, features, and stories.
4. **Wait for approval** (gate 1) before building the tree.
5. **Build the tree in context** — in conversation only, no file.
6. **Ask about Jira creation and project** (gate 2) — including the target project.
7. **Create** — only after the creation is confirmed.

Whenever the scope, mapping, or target is unclear, stop and ask. Do not guess.

## Stage 1 — Scope to 100 percent

Start from the epic prompt and drive a scoping conversation using this checklist. The user may trim any dimension that does not apply.

- **Epic goal** — the outcome the epic delivers.
- **In scope / out of scope** — explicit boundaries.
- **Personas** — who uses this and why.
- **Key flows** — the main journeys the epic must support.
- **Constraints** — technical, business, regulatory, or platform limits.
- **NFRs** — performance, security, accessibility, and similar expectations.
- **Success criteria** — how done and good are judged.

Continue until the scope is unambiguous. Missing information becomes a question to the user, never an assumption.

## Stage 2 — Tree plan and approval

Present the proposed tree:

- the **epic** with a one-line intent,
- its **features**, each with a one-line intent,
- each feature's **stories**, each with a one-line intent.

Use temporary readable references for discussion only, for example `E1`, `F1.1`, `S1.1.1`. These are not persisted and are not Jira keys.

Wait for approval before building the tree. This is gate 1.

## Stage 3 — Build the tree in context

On approval, produce the full tree in the conversation only. Do not write a file.

For each node, author:

- **Epic** — summary and description.
- **Feature** — summary and description.
- **Story** — summary and description, with acceptance criteria folded into the description.

Fields are summary and description only. Extra fields such as labels or priority are optional and are not added unless the user asks.

## Stage 4 — Ask about Jira creation and project

Ask whether to create the tree in Jira, and on which project.

### Project is a hard blocker

- If the user did not specify the Jira project in the prompt, the skill must ask for it. This is a hard blocker. Do not proceed with creation without an explicit project.
- The project must already exist. Verify existence through the Atlassian MCP before creating.
- If the named project does not exist, stop and ask the user for a valid project. Do not create a project.

If the user does not want to create the tree in Jira, stop after delivering the in-context tree.

## Stage 5 — Detect and confirm issue-type mapping

Before creating, resolve the target project's real issue types through the MCP and propose a mapping:

- **Epic** maps to the project's epic-level issue type.
- **Feature** maps to a `Feature` issue type when one exists, otherwise to `Story`.
- **Story** maps to `Story`, or to `Sub-task` when the feature level already consumed the story type.

Confirm the mapping with the user before creating. If the project's hierarchy cannot support three distinct levels, explain the options and let the user choose.

## Stage 6 — Create in Jira

Show exactly what will be created, then create in hierarchy order:

1. Create the **epic**.
2. Create each **feature** with its parent set to the epic.
3. Create each **story** with its parent set to its feature.

Use the MCP's parent or epic-link mechanism, resolved at runtime, to connect children to parents. Populate summary and description only.

After creation, report:

- the created epic key,
- the created feature keys under it,
- the created story keys under each feature,
- the full hierarchy.

## Stage 7 — Handoff

The created Story keys are the `STORY-ID`s for the QA suite. Offer to hand off to `qa-decompose-requirements` for test authoring.

## Hard constraints

- Do not proceed to Jira creation without an explicit, existing project.
- Do not create a Jira project.
- Do not write the requirements tree to a file; it is context-only.
- Do not add fields beyond summary and description unless the user asks.
- Do not hardcode MCP tool names; resolve them at runtime.
- Do not author test cases here.
- Do not create issues before the tree plan is approved and the creation is confirmed.
- Do not assume the issue-type mapping; detect and confirm it.

## Completion condition

This skill is complete when either:
- the scoped epic-feature-story tree has been delivered in context and the user declined Jira creation, or
- the tree has been created in Jira under an existing project, the created keys and hierarchy have been reported, and the handoff to `qa-decompose-requirements` has been offered.
