# Failure Classification Rubric

## Decision order

Evaluate classifications in this order to avoid defaulting prematurely to a product defect:

1. Confirm that expected and actual results are both present and comparable.
2. Confirm that prerequisites, setup, data, and tester actions match the test.
3. Confirm that the intended environment and configuration were used.
4. Compare the expected result with the requirement and current documentation.
5. Inspect direct product evidence, prior executions, and known defects.
6. Select the best-supported classification and disclose competing explanations.

## Classifications

| Classification | Use when | Do not use when |
| --- | --- | --- |
| `product-defect` | The product contradicts grounded required behavior under valid conditions. | Setup, evidence, or intent remains materially uncertain. |
| `environment-issue` | Infrastructure, service availability, test data, or environment health caused the result. | Product behavior reproduces across valid environments. |
| `configuration-issue` | A setting, feature flag, permission, or deployment configuration caused the result. | The configuration matches the required baseline. |
| `missing-prerequisite` | A required precondition, dependency, account state, or setup action was absent. | All documented prerequisites were satisfied. |
| `incorrect-expected-result` | The test expectation conflicts with a clear requirement or current approved behavior. | The requirement supports the authored expectation. |
| `requirement-ambiguity` | Available requirements support multiple reasonable interpretations. | One interpretation is clearly authoritative. |
| `tester-mistake` | Direct evidence shows that the recorded action, data, or sequence differed from the test. | The conclusion relies on speculation about the tester. |
| `insufficient-evidence` | Available facts cannot support another classification responsibly. | Direct evidence supports a more specific classification. |

## Confidence guidance

| Range | Meaning |
| ---: | --- |
| 90–100 | Direct, consistent evidence supports the classification and excludes credible alternatives. |
| 70–89 | Strong evidence supports the classification, but a credible alternative remains. |
| 40–69 | Partial evidence supports the classification; important confirmation is missing. |
| 0–39 | Evidence is sparse or contradictory; prefer `insufficient-evidence`. |

Do not use an arbitrary confidence threshold to prevent tester-approved defect creation. Explain uncertainty and let the
tester decide after seeing the analysis.

## Evidence rules

1. Label an inference as an inference.
2. Cite the source of every material supporting fact.
3. List evidence that contradicts the selected classification.
4. Identify missing evidence that could change the classification.
5. Check existing defects before recommending a new defect.
6. Never fabricate logs, source behavior, environment state, timestamps, or issue status.
