# P2C-0 Shadow-only Daily Integration Report

## Summary

P2C-0 is complete as a shadow-only daily integration. `scripts/run_daily_shadow_integration.py` connects a daily training Markdown artifact, source notes, generated reader HTML, the local semantic reviewer, governance validation, shadow decision output, per-run report output, and REVIEW/FAIL failure packaging.

The integration is intentionally not a formal P2C publishing path.

## Boundary

- not formal P2C
- not live LLM reviewer
- no public site update
- no user notification
- no automatic publishing
- human confirmation required
- shadow PASS is not formal PASS
- `formal_publish_allowed` is always `false`

## Scenarios

- PASS scenario: `outputs/daily-training/2026-06-28/training-v8-pass.md`
- REVIEW scenario: `outputs/daily-training/2026-06-28/training-v8-review-boilerplate.md`
- Shared source notes: `outputs/daily-training/2026-06-28/source-notes-p2b3.md`
- Reader HTML is generated inside each shadow run only and is not a public website artifact.

## Decision Matrix

| Scenario | reviewer_decision | shadow_publish_allowed | formal_publish_allowed | human_confirmation_required | failure_package_required | failure_package_created |
| --- | --- | --- | --- | --- | --- | --- |
| PASS | PASS | true | false | true | false | false |
| REVIEW | REVIEW | false | false | true | true | true |

## Output Artifacts

PASS run:

- `docs/quality/rubric-v2.1/shadow-runs/2026-06-28/p2c0-pass/training.md`
- `docs/quality/rubric-v2.1/shadow-runs/2026-06-28/p2c0-pass/reader.html`
- `docs/quality/rubric-v2.1/shadow-runs/2026-06-28/p2c0-pass/source-notes.md`
- `docs/quality/rubric-v2.1/shadow-runs/2026-06-28/p2c0-pass/reviewer-output.json`
- `docs/quality/rubric-v2.1/shadow-runs/2026-06-28/p2c0-pass/claim-evidence-map.json`
- `docs/quality/rubric-v2.1/shadow-runs/2026-06-28/p2c0-pass/failure-objects.json`
- `docs/quality/rubric-v2.1/shadow-runs/2026-06-28/p2c0-pass/shadow-review-result.yaml`
- `docs/quality/rubric-v2.1/shadow-runs/2026-06-28/p2c0-pass/shadow-generation-log.yaml`
- `docs/quality/rubric-v2.1/shadow-runs/2026-06-28/p2c0-pass/shadow-run-report.md`

REVIEW run:

- `docs/quality/rubric-v2.1/shadow-runs/2026-06-28/p2c0-review/training.md`
- `docs/quality/rubric-v2.1/shadow-runs/2026-06-28/p2c0-review/reader.html`
- `docs/quality/rubric-v2.1/shadow-runs/2026-06-28/p2c0-review/source-notes.md`
- `docs/quality/rubric-v2.1/shadow-runs/2026-06-28/p2c0-review/reviewer-output.json`
- `docs/quality/rubric-v2.1/shadow-runs/2026-06-28/p2c0-review/claim-evidence-map.json`
- `docs/quality/rubric-v2.1/shadow-runs/2026-06-28/p2c0-review/failure-objects.json`
- `docs/quality/rubric-v2.1/shadow-runs/2026-06-28/p2c0-review/shadow-review-result.yaml`
- `docs/quality/rubric-v2.1/shadow-runs/2026-06-28/p2c0-review/shadow-generation-log.yaml`
- `docs/quality/rubric-v2.1/shadow-runs/2026-06-28/p2c0-review/shadow-run-report.md`

## Failure Package

The REVIEW scenario generated a failure package at:

`docs/quality/rubric-v2.1/shadow-runs/2026-06-28/p2c0-review/shadow-failure-package/`

Package files:

- `source-manifest.yaml`
- `reviewer-output.json`
- `claim-evidence-map.json`
- `failure-objects.json`
- `shadow-review-result.yaml`
- `repair-actions.yaml`
- `package-manifest.yaml`

## Test Result

Command:

```bash
python3 -m unittest \
  tests.test_rubric_v21_governance \
  tests.test_rubric_v21_adversarial \
  tests.test_rubric_v21_anchor_quality \
  tests.test_rubric_v21_calibration_replay \
  tests.test_rubric_v21_reviewer_generator \
  tests.test_rubric_v21_p2b0_local_reviewer \
  tests.test_rubric_v21_live_reviewer_samples \
  tests.test_rubric_v21_live_reviewer_v7 \
  tests.test_rubric_v21_live_reviewer_stability \
  tests.test_rubric_v21_live_reviewer_cross_samples \
  tests.test_rubric_v21_live_reviewer_p2b3 \
  tests.test_rubric_v21_live_reviewer_p2b3_samples \
  tests.test_rubric_v21_shadow_review \
  tests.test_rubric_v21_p2c0_shadow_integration
```

Result:

```text
...........................................................................................................................................................
----------------------------------------------------------------------
Ran 155 tests in 470.246s

OK
```

Targeted P2C-0 result:

```text
.........
----------------------------------------------------------------------
Ran 9 tests in 2.076s

OK
```

## Git Policy

Runtime shadow artifacts are written under `docs/quality/rubric-v2.1/shadow-runs/`, which is already covered by `.gitignore`.

No generated `shadow-runs/` artifacts or zip files should be committed. The intended tracked files are the P2C-0 integration script, test file, and this report.

## Next Step

If P2C-0 is accepted, the recommended next step is P2C-1: continuous 3-day shadow-only observation without publishing.
