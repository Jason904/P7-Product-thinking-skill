# P2B-2 Cross-Sample Local Reviewer Report

## Boundary

- Stage: P2B-2 cross-date / cross-topic real sample replay.
- Reviewer: local semantic reviewer.
- Not a live LLM reviewer.
- Does not enter P2C and does not connect to the daily production chain.
- P1 governance validator is not modified by this stage.
- Self-review tables and historical audit reports are evidence inputs only, not release authority.

## Historical Sample Availability

- Real sample count: 6.
- Covered dates: 2026-06-25, 2026-06-26.
- Date coverage status: INSUFFICIENT_REAL_HISTORY
- Current repository only contains real daily-training outputs for two dates. No synthetic fixture is used to pretend third-date coverage.

## P2B-3 Readiness

- P2B-3 status: `READY_WITH_2026_06_28_SUPPLEMENT`.
- P2B-2 corpus date count: 2 / required >= 3 for P2B-3.
- P2B-2 corpus REVIEW / borderline expected sample count: 0 / required >= 2 for P2B-3.
- P2B-3 supplement sample count: 3.
- Combined real date count: 3 / required >= 3.
- Combined REVIEW / borderline expected sample count: 2 / required >= 2.
- Synthetic fixtures are not allowed to satisfy these counts.
- P2B-2 original 6-sample corpus remains insufficient by itself; P2B-3 uses the explicit 2026-06-28 supplement when present.

### P2B-3 Blockers

- None when the 2026-06-28 P2B-3 supplement is present and green.

## Results

| Sample | Date | Expected | Decision | Publish | Failure origin | Output |
| --- | --- | --- | --- | --- | --- | --- |
| `2026_06_25_training_v2` | `2026-06-25` | `FAIL` | `REWRITE_CASE` | `False` | content_quality | `docs/quality/rubric-v2.1/generated-replay/cross-samples/2026_06_25_training_v2` |
| `2026_06_25_training_v3` | `2026-06-25` | `PASS` | `PASS` | `True` | none | `docs/quality/rubric-v2.1/generated-replay/cross-samples/2026_06_25_training_v3` |
| `2026_06_25_training_v4_raw` | `2026-06-25` | `PASS` | `PASS` | `True` | none | `docs/quality/rubric-v2.1/generated-replay/cross-samples/2026_06_25_training_v4_raw` |
| `2026_06_25_training_v5_raw` | `2026-06-25` | `PASS` | `PASS` | `True` | none | `docs/quality/rubric-v2.1/generated-replay/cross-samples/2026_06_25_training_v5_raw` |
| `2026_06_25_training_v6_raw` | `2026-06-25` | `PASS` | `PASS` | `True` | none | `docs/quality/rubric-v2.1/generated-replay/cross-samples/2026_06_25_training_v6_raw` |
| `2026_06_26_training_v7_raw` | `2026-06-26` | `FAIL` | `FAIL_DAILY` | `False` | content_quality, self_review_inflation | `docs/quality/rubric-v2.1/generated-replay/cross-samples/2026_06_26_training_v7_raw` |

## PASS Samples

- `2026_06_25_training_v3`
- `2026_06_25_training_v4_raw`
- `2026_06_25_training_v5_raw`
- `2026_06_25_training_v6_raw`

## REVIEW / REWRITE Hold Samples

- `2026_06_25_training_v2`: cannot auto-release because `INCOMPLETE_8Q_FIELDS, PREP_NOT_USABLE`.

## FAIL Samples

- `2026_06_26_training_v7_raw`: `FAIL_DAILY` with `BOILERPLATE_REASONING, CASE_DEPTH_IMBALANCE, REVIEW_EVIDENCE_INVALID, DISCONNECTED_8Q_CHAIN`.

## Manual Confirmation

- No sample is released because of self-review score.
- No sample is released because of historical audit alone.
- Third-date coverage requires additional real historical daily-training output before this can be claimed as full cross-date validation.
