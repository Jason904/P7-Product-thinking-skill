# P2B-1 Stability / No-Audit Stress Report

## Boundary

- Stage: P2B-1 stability / no-audit stress.
- Reviewer: local semantic reviewer.
- Not a live LLM reviewer.
- Does not enter P2C and does not connect to the daily production chain.
- This stage does not enter P2C.
- P1 recorded payloads are not used as generation results.

## Purpose

This stage checks whether input perturbations and missing auxiliary audit inputs cause bad samples to be mistakenly released or good samples to be incorrectly hard-failed.

## Results

| Scenario | Base | Decision | Publish | Failure origin | Output |
| --- | --- | --- | --- | --- | --- |
| `v7_failure_no_audit_should_not_pass` | `v7_failure` | `REVIEW` | `False` | content_quality, input_missing, self_review_inflation | `docs/quality/rubric-v2.1/generated-replay/stability/v7_failure_no_audit_should_not_pass` |
| `v7_failure_without_self_review_should_not_pass` | `v7_failure` | `REWRITE_MODULE` | `False` | content_quality | `docs/quality/rubric-v2.1/generated-replay/stability/v7_failure_without_self_review_should_not_pass` |
| `v7_failure_without_reader_html_should_not_pass_or_review` | `v7_failure` | `FAIL_DAILY` | `False` | content_quality, input_missing, self_review_inflation | `docs/quality/rubric-v2.1/generated-replay/stability/v7_failure_without_reader_html_should_not_pass_or_review` |
| `v7_failure_without_source_notes_should_not_pass_or_review` | `v7_failure` | `FAIL_DAILY` | `False` | content_quality, input_missing, self_review_inflation | `docs/quality/rubric-v2.1/generated-replay/stability/v7_failure_without_source_notes_should_not_pass_or_review` |
| `v3_without_self_review_should_still_pass_or_review_not_fail` | `v3_target` | `PASS` | `True` | none | `docs/quality/rubric-v2.1/generated-replay/stability/v3_without_self_review_should_still_pass_or_review_not_fail` |
| `v6_without_quality_report_should_still_pass_or_review_not_fail` | `v6_target` | `PASS` | `True` | input_missing | `docs/quality/rubric-v2.1/generated-replay/stability/v6_without_quality_report_should_still_pass_or_review_not_fail` |
| `case_order_changed_should_not_change_daily_decision` | `v6_target` | `PASS` | `True` | none | `docs/quality/rubric-v2.1/generated-replay/stability/case_order_changed_should_not_change_daily_decision` |
| `repeated_run_same_input_should_be_deterministic` | `v6_target` | `PASS` | `True` | none | `docs/quality/rubric-v2.1/generated-replay/stability/repeated_run_same_input_should_be_deterministic` |

## Interpretation

- V7 perturbations must remain non-PASS; if they fail, the report separates content-quality failures from missing-input risk.
- V3/V6 perturbations may become REVIEW when auxiliary evidence is missing, but they must not become FAIL_DAILY unless the evidence loss creates a defensible hard block.
- Case-order perturbation verifies that the daily decision does not depend on case ordering.
- Repeated-run perturbation verifies deterministic reviewer behavior after removing timestamp fields.
