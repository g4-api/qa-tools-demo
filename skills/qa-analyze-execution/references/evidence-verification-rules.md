# Evidence Verification Rules

## Verification order

Verify material claims using the strongest available source in this order:

1. Execution journal observations, decisions, and receipts.
2. Finalized test steps and exact expected results.
3. Approved requirements and traceability records.
4. Evidence files, logs, traces, screenshots, recordings, and console output.
5. Read-only Jira, Xray, repository, documentation, or monitoring records.
6. Comparable prior executions.

Record contradictory evidence and missing evidence that could change a conclusion.

## Local references

For a local file reference:

1. Resolve the path without modifying the file.
2. Confirm that the target exists.
3. Cite the exact path.
4. Add a line number for relevant text when available.
5. Add a log timestamp or event identifier when it is more precise than a line number.

Mark the reference `Unverified` when the file is missing, inaccessible, ambiguous, or changed so that the cited content
cannot be located.

## Remote references

For Jira, Xray, repository, documentation, or monitoring references:

1. Prefer a direct link returned by the system or already recorded in a verified artifact.
2. Use a read-only lookup when the relevant connector is available.
3. Verify that the returned identifier matches the requested object.
4. Record the returned state, warning, timestamp, or version needed for the claim.
5. Preserve the direct link without embedding credentials or temporary authorization data.

Derive a browse link only when both the base URL and object key are verified from configuration or a tool response and
the route is deterministic. Otherwise report the key without manufacturing a link.

## Defect links

A defect key alone proves only that the journal recorded a key. Treat its state and content as unverified until the local
defect receipt or remote defect was inspected.

When accessible, verify:

1. Defect key and direct link.
2. Summary and affected behavior.
3. Workflow state and resolution.
4. Execution, test, step, and requirement relationship.

Report a possible duplicate only when recorded analysis or matching verified evidence supports the relationship.

## Source links

Prefer a verified repository link pinned to a commit and line when the repository remote and revision are available.
Otherwise cite the local source path and line number. Do not fabricate a web URL from a local path or assume the current
branch is the execution build.

## Evidence safety

- Never display a PAT, password, cookie, authorization header, session token, or private key.
- Redact secrets before quoting a log or configuration value.
- Exclude personal data unrelated to the execution problem.
- Use short excerpts or event summaries; link to the source instead of reproducing large logs.
- Do not alter evidence to make sources agree.

## Missing and conflicting evidence

When a material source cannot be verified:

1. Name the missing or inaccessible source.
2. State which claim remains unsupported.
3. Assign `Unverified` or `Inference` according to the finding contract.
4. Recommend the smallest evidence-collection action that could resolve the uncertainty.

When sources conflict, present both records, prefer neither silently, and explain which decision remains unsafe.
