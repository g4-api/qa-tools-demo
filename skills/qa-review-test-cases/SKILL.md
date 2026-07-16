---
name: qa-review-test-cases
description: Score Manual Xray test-case files against a fixed weighted QA rubric, apply a strict per-test greater-than-95 gate, and route issues back to qa-create-test-cases without editing files. Use when test cases must be audited, scored, or checked for coverage, clarity, verifiability, and Xray-structure compliance, either standalone or as the scoring stage inside qa-orchestrate-test-cases.
---

# QA Review Test Cases

## Purpose

This skill is the "review" stage of the create / review / orchestrate trio. It scores each Manual test-case file, decides pass or fail against a strict per-test gate, and routes issues back to the owning create skill.

This skill is a pure scorer and reporter. It never edits test files.

This skill must:
1. load the test files, requirements, and traceability index,
2. score every test on the fixed weighted rubric,
3. apply the per-test greater-than-95 gate,
4. produce a per-test score table and per-dimension detail for failing tests,
5. route each issue to `qa-create-test-cases`,
6. emit a clear pass or fail contract that the orchestrator can act on.

For every test, also invoke `md-code-compliance-review` in report-only mode after reading `md-vanilla-style`. Run the Markdown linter and treat its result as a separate flawless gate. Route Markdown fixes to `qa-create-test-cases`; this review skill remains read-only.

## Use this skill when

Use this skill when the task is about:
- scoring or auditing existing Manual test cases
- checking requirement coverage and traceability
- checking step clarity, verifiability, and Xray-structure compliance
- deciding whether test cases meet the quality gate
- feeding the automated fix loop driven by `qa-orchestrate-test-cases`

Do not use this skill to author or fix tests, or to sync to Xray. Fixes belong to `qa-create-test-cases`; sync belongs to `qa-xray-sync`.

## Standard anchoring

By default this skill anchors its expectations to **General best practice** for test design and documentation.

If the user selects a standard, anchor terminology and technique expectations to it instead:
- **ISTQB** — ISTQB glossary and test-design techniques (for example equivalence partitioning, boundary value analysis, decision tables, state transition).
- **ISTQB + ISO/IEC/IEEE 29119** — the above plus ISO/IEC/IEEE 29119 documentation structure and coverage expectations.

The chosen standard is fixed for the session once execution starts.

## Execution mode

- **Standalone**: may present its findings interactively for a one-off audit.
- **Inside the orchestrated loop**: runs non-interactively. It scores, reports, and routes without asking for approval, because `qa-orchestrate-test-cases` owns the automated create/review/fix cycle that repeats until the goal is met.

## Inputs

- `<STORY-ID>/tests/*.md` — the Manual test files.
- `<STORY-ID>/requirements.md` — the decomposed requirements and `REQ-###` IDs.
- `<STORY-ID>/traceability.md` — the requirement-to-test matrix.
- `md-vanilla-style` — the mandatory Markdown authoring contract.
- `md-code-compliance-review` — the Markdown scoring contract and linter.

## Fixed rubric

Score each test on every dimension from 0 to 100, then compute the weighted total.

| Dimension | Weight |
|---|---:|
| Requirement coverage & traceability | 20 |
| Step atomicity & clarity | 15 |
| Expected-result verifiability | 15 |
| Negative/edge coverage | 15 |
| Xray-structure compliance | 15 |
| Field completeness | 10 |
| Data adequacy | 5 |
| Consistency / no duplication | 5 |

### Weights

Weights are fixed by default. Do not ask the user to change them.

If the user asks to change a weight, guide them, apply the new weights for this session only, and require that the weights still sum to 100.

### Dimension meaning

- **Requirement coverage & traceability** — the test maps to real `REQ-###` IDs; coverage gaps in `traceability.md` count against the story.
- **Step atomicity & clarity** — one clear action per step; unambiguous wording.
- **Expected-result verifiability** — every step's expected result is observable and checkable.
- **Negative/edge coverage** — invalid, boundary, and error conditions are exercised where relevant.
- **Xray-structure compliance** — frontmatter and structured setup/step/teardown shapes can map to the exact Xray mutation schemas; every step has `action` and a non-empty `expectedResults` array; mandatory fields are present.
- **Field completeness** — configured template fields are populated and valid.
- **Data adequacy** — optional local `data`, or the `action` itself, provides sufficient realistic inputs without introducing an unsupported top-level Xray property.
- **Consistency / no duplication** — no contradictory or duplicated tests; consistent terminology and IDs.

## Gate

Every test must score strictly greater than 95 on its weighted total.

A single test at or below 95 fails the whole story. A Markdown score below 100 or any Markdown linter error also fails that test. Both gates are per test, not aggregate.

## Scoring guidance

- **96–100**: production-ready, no material issues
- **85–95**: usable but with real gaps that must be fixed to pass the gate
- **60–84**: significant issues remain
- **0–59**: major structural or coverage problems

Scores must reflect real quality, not optimism.

## Output contract

Always emit a complete scoring table for each reviewed test. Do not replace per-test tables with an aggregate table.

```markdown
### <test-id> scoring table

| Dimension | Weight | Score | Status |
|---|---:|---:|---|
| Requirement coverage & traceability | 20 | <0-100> | PASS or FAIL |
| Step atomicity & clarity | 15 | <0-100> | PASS or FAIL |
| Expected-result verifiability | 15 | <0-100> | PASS or FAIL |
| Negative/edge coverage | 15 | <0-100> | PASS or FAIL |
| Xray-structure compliance | 15 | <0-100> | PASS or FAIL |
| Field completeness | 10 | <0-100> | PASS or FAIL |
| Data adequacy | 5 | <0-100> | PASS or FAIL |
| Consistency / no duplication | 5 | <0-100> | PASS or FAIL |
| **QA weighted total** | **100** | **<0-100>** | **PASS or FAIL** |
| Markdown compliance | Gate: 100 | <0-100> | PASS or FAIL |
| Markdown linter errors | Gate: 0 | <count> | PASS or FAIL |
| **Per-test result** | — | — | **PASS or FAIL** |

Issues (route to qa-create-test-cases):

1. <dimension and exact actionable issue; include Markdown line number when applicable>

**Adjustments Needed**: true or false
```

Set Per-test result to PASS only when QA weighted total is strictly greater than 95, Markdown compliance is exactly 100, and Markdown linter errors equal zero. Issues must be concrete enough for `qa-create-test-cases` to fix without re-analysis.

After all per-test tables, begin the machine-readable decision with exactly one of:

```text
Complies with all rules. All tests exceed 95 and all Markdown files are flawless.
```

```text
Does not comply. One or more tests failed the QA or Markdown gate.
```

## Routing rules

- All fixable issues route to `qa-create-test-cases`.
- Markdown issues route to `qa-create-test-cases` with exact file line numbers from `md-code-compliance-review`.
- A coverage gap with no matching requirement routes to `qa-decompose-requirements`, because the missing requirement must exist before a test can cover it.

## Hard constraints

- Do not edit test files.
- Do not author or delete tests.
- Do not sync to Xray.
- Do not pass a story while any test is at or below 95.
- Do not pass a test below 100 Markdown compliance or with any Markdown linter error.
- Do not change rubric weights unless the user explicitly asks, and never break the sum-to-100 rule.
- Do not emit vague issues; every issue must be actionable.
- Do not omit the complete scoring table for any test.

## Completion condition

This skill is complete for a run when it has emitted a valid pass or fail contract with every per-test score table. The story is only cleared when the decision states:

```text
Complies with all rules. All tests exceed 95 and all Markdown files are flawless.
```
