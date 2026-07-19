---
sourceType: jira
source: GAR-2
storyKey: GAR-2
title: Feature 1 - Requirements Decomposition Engine
link: https://qa-webinar.atlassian.net/browse/GAR-2
retrievedAt: 2026-07-19
depthMode: full
---

# Feature 1 - Requirements Decomposition Engine

## Atomic testable requirements

1. **REQ-000:** The engine accepts story input supplied as a Markdown document.
2. **REQ-001:** The engine accepts story input supplied as Jira story text.
3. **REQ-002:** The engine produces atomic, independently testable requirements from the input.
4. **REQ-003:** The engine output includes business rules derived from the input.
5. **REQ-004:** The engine output includes non-functional requirements derived from the input.
6. **REQ-005:** The engine explicitly lists gaps and ambiguities instead of inventing answers.

## Acceptance criteria

1. **AC-000** (`REQ-000`, `REQ-001`): Input can be provided as Markdown or as Jira story text.
2. **AC-001** (`REQ-002`, `REQ-003`, `REQ-004`): Output includes atomic requirements, business rules,
    and non-functional requirements.
3. **AC-002** (`REQ-005`): Gaps and ambiguities are explicitly listed in the output.

## Business rules

1. The engine decomposes input the same way whether the source is Markdown or Jira story text.
2. Every atomic requirement produced by the engine is independently testable.
3. The engine grounds all output in the input and never invents content the source does not state.
4. Unstated or contradictory input is recorded as a gap rather than resolved silently.

## Candidate test conditions

### Positive conditions

1. A Markdown story source is decomposed into atomic, testable requirements (`REQ-000`, `REQ-002`).
2. A Jira story-text source is decomposed into atomic, testable requirements (`REQ-001`, `REQ-002`).
3. The decomposition output includes business rules and non-functional requirements (`REQ-003`,
    `REQ-004`).
4. An incomplete source yields an explicit list of gaps and ambiguities (`REQ-005`).

### Negative conditions

1. A combined multi-behaviour statement is not accepted as a single atomic requirement (`REQ-002`).
2. Content that the source does not state is not emitted as a requirement, rule, or NFR (`REQ-003`,
    `REQ-004`).
3. An ambiguity in the source is not silently resolved into a concrete requirement (`REQ-005`).

### Edge conditions

1. A source that states no non-functional requirement reports that absence rather than inventing one
    (`REQ-004`, `REQ-005`).
2. A source containing two contradictory statements records the contradiction as a gap (`REQ-005`).

## Non-functional requirements

1. The engine produces consistent decomposition output across Markdown and Jira sources.
2. The engine keeps decomposed requirements traceable back to the originating input.

## Gaps and open questions

1. The story does not define the input schema or fields expected from the Markdown or Jira source.
2. The story does not define an acceptance threshold for when a requirement is "atomic" or "testable".
3. The story does not specify which non-functional requirement categories the output must cover.
4. The story does not state the output format or structure the engine must emit.
5. The story does not define how the engine distinguishes a genuine gap from missing optional content.
