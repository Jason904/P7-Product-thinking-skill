# Rubric v2.1 P1 Replay Package

## Purpose

This package is for external review of the Rubric v2.1 P1 Calibration Replay. It lets a reviewer independently verify that the governance validator is executable, calibration replay fixtures exist, real samples are traceable, synthetic fixtures are clearly marked, and the replay tests can reproduce the expected pass/fail behavior.

## Included Files

- `docs/quality/rubric-v2.1/`
  - `rubric-v2.1.md`
  - `rubric-enums.yaml`
  - `rubric-score-anchors.yaml`
  - `reviewer-output.schema.json`
  - `claim-evidence-map.schema.json`
  - `failure-object.schema.json`
  - `calibration-tests.yaml`
  - `repair-rerun-map.yaml`
  - `validator-check-map.yaml`
  - `rubric_governance_validator.py`
  - `calibration-replay-report.md`
  - `fixtures/calibration/`
- Tests:
  - `tests/test_rubric_v21_governance.py`
  - `tests/test_rubric_v21_adversarial.py`
  - `tests/test_rubric_v21_anchor_quality.py`
  - `tests/test_rubric_v21_calibration_replay.py`
- Real sample source files under `outputs/daily-training/`.

## Real Samples

- `v3_target`
  - source markdown: `outputs/daily-training/2026-06-25/training-v3.md`
  - source html: not available in repository
  - source/audit record: `outputs/daily-training/2026-06-25/training-v3.md`
- `v6_target`
  - source markdown: `outputs/daily-training/2026-06-25/training-v6-raw.md`
  - source html: `outputs/daily-training/2026-06-25/training-v6-reader.html`
  - source records:
    - `outputs/daily-training/2026-06-25/source-notes-v6.md`
    - `outputs/daily-training/2026-06-25/training-v6-quality-report.md`
- `v7_failure`
  - source markdown: `outputs/daily-training/2026-06-26/training-v7-raw.md`
  - source html: `outputs/daily-training/2026-06-26/training-v7-reader.html`
  - source/audit records:
    - `outputs/daily-training/2026-06-26/source-notes-v7.md`
    - `outputs/daily-training/2026-06-26/v6-v7-regression-audit.md`
    - `outputs/daily-training/2026-06-26/quality-gate-hardening-report.md`

## Synthetic Fixtures

- `empty_8q`
  - `synthetic_fixture: true`
  - `not_real_sample_replay: true`
- `news_summary`
  - `synthetic_fixture: true`
  - `not_real_sample_replay: true`
- `inflated_self_review`
  - `synthetic_fixture: true`
  - `not_real_sample_replay: true`
- `human_preference`
  - `synthetic_fixture: true`
  - `not_real_sample_replay: true`

## Test Commands

Run from the extracted package root:

```bash
python3 -m unittest tests.test_rubric_v21_governance
python3 -m unittest tests.test_rubric_v21_adversarial
python3 -m unittest tests.test_rubric_v21_anchor_quality
python3 -m unittest tests.test_rubric_v21_calibration_replay
python3 -m unittest tests.test_rubric_v21_governance tests.test_rubric_v21_adversarial tests.test_rubric_v21_anchor_quality tests.test_rubric_v21_calibration_replay
```

## Expected Results

```text
Ran 72 tests
OK
```

## Known Boundary

This replay validates governance payload behavior.
It does not prove that an automatic semantic reviewer can independently read full Markdown and generate correct reviewer-output payloads.
That belongs to the next stage: Markdown-to-reviewer-payload generation.
