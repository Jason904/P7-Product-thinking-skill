# Rubric v2.1 Calibration Replay Report

## Sample Inventory

```yaml
sample_inventory:
  v3_target:
    source_exists: true
    markdown_path: outputs/daily-training/2026-06-25/training-v3.md
    html_path: null
    source_record_path:
    - outputs/daily-training/2026-06-25/training-v3.md
    note: Real historical target-quality content sample; no dedicated V3 HTML/source-notes
      file exists in repo.
  v6_target:
    source_exists: true
    markdown_path: outputs/daily-training/2026-06-25/training-v6-raw.md
    html_path: outputs/daily-training/2026-06-25/training-v6-reader.html
    source_record_path:
    - outputs/daily-training/2026-06-25/source-notes-v6.md
    - outputs/daily-training/2026-06-25/training-v6-quality-report.md
    note: Real target-quality sample used for reader/content completeness comparison.
  v7_failure:
    source_exists: true
    markdown_path: outputs/daily-training/2026-06-26/training-v7-raw.md
    html_path: outputs/daily-training/2026-06-26/training-v7-reader.html
    source_record_path:
    - outputs/daily-training/2026-06-26/source-notes-v7.md
    - outputs/daily-training/2026-06-26/v6-v7-regression-audit.md
    - outputs/daily-training/2026-06-26/quality-gate-hardening-report.md
    note: Real failure sample; reviewer payload intentionally preserves the known
      V7 Case B 8Q regression as a validator-visible cap violation.
  empty_8q:
    source_exists: false
    markdown_path: null
    html_path: null
    source_record_path: []
    note: synthetic_fixture=true; not_real_sample_replay=true.
  news_summary:
    source_exists: false
    markdown_path: null
    html_path: null
    source_record_path: []
    note: synthetic_fixture=true; not_real_sample_replay=true.
  inflated_self_review:
    source_exists: false
    markdown_path: null
    html_path: null
    source_record_path: []
    note: synthetic_fixture=true; not_real_sample_replay=true.
  human_preference:
    source_exists: false
    markdown_path: null
    html_path: null
    source_record_path: []
    note: synthetic_fixture=true; not_real_sample_replay=true; only the user can resolve
      this decision.
```

## Replay Summary

| sample | type | expected | actual | publish_allowed | validator_errors | result |
|---|---|---|---|---:|---:|---|
| v3_target | real | PASS | PASS | true | 0 | OK |
| v6_target | real | PASS | PASS | true | 0 | OK |
| v7_failure | real | ['FAIL_DAILY', 'PUBLISH_BLOCK'] | FAIL_DAILY | false | 3 | OK |
| empty_8q | synthetic | ['FAIL_DAILY', 'PUBLISH_BLOCK'] | PUBLISH_BLOCK | false | 0 | OK |
| news_summary | synthetic | ['FAIL_DAILY'] | FAIL_DAILY | false | 0 | OK |
| inflated_self_review | synthetic | ['FAIL_DAILY', 'PUBLISH_BLOCK'] | FAIL_DAILY | false | 0 | OK |
| human_preference | synthetic | USER_REVIEW_REQUIRED | USER_REVIEW_REQUIRED | false | 0 | OK |

## Notes

- V3/V6/V7 are real historical artifacts found under `outputs/daily-training/`.
- Empty 8Q, news summary, inflated self-review, and human preference samples are synthetic fixtures because no standalone historical artifacts exist in the repository.
- Synthetic fixtures are explicitly marked with `synthetic_fixture: true` and `not_real_sample_replay: true` in `source-manifest.yaml`.
- This replay validates payload governance behavior; it does not replace future semantic LLM review of full Markdown content.

## Mismatch Analysis

No replay mismatch was found in this run.

If a future replay row returns `CHECK`, classify it as one of:

- Rubric issue: the validator allows or blocks behavior that contradicts Rubric v2.1.
- Fixture issue: the sample manifest, failure objects, caps, or expected decision are incorrectly encoded.
- Reviewer payload issue: the payload score lifecycle, evidence sufficiency, claim map, or daily decision is inconsistent with the sample.

Current classification: all rows are `OK`, so no repair action is required for this replay package.
