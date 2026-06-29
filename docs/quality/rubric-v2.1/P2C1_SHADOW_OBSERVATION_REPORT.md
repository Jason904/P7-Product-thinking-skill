# P2C-1 Shadow-only Observation Report

## Summary

P2C-1 shadow-only observation ledger is complete. The implementation adds a policy file and a ledger script that records a 3-day shadow-only window, classifies observation status, records failure-package and human-confirmation state, and keeps all promotion authority disabled.

P2C-1 is not formal P2C and does not publish.

## Boundary

- not formal P2C
- no public site update
- no user notification
- no automatic publishing
- no live LLM reviewer
- human confirmation required
- shadow PASS is not formal PASS
- `formal_publish_allowed` is always `false`

## Observation Policy

Policy path:

`docs/quality/rubric-v2.1/p2c1-shadow-observation-policy.yaml`

Rules:

- `required_days: 3`
- `eligible_for_p2c2` defaults to `false`
- REVIEW / REWRITE / FAIL / PUBLISH_BLOCK days block P2C-2
- missing `shadow-review-result.yaml`, `reader.html`, `source-notes.md`, or `reviewer-output.json` blocks P2C-2
- any source result with `public_site_updated=true` blocks P2C-2
- any source result with `user_notification_sent=true` blocks P2C-2
- any source result with `live_llm_review=true` blocks P2C-2
- any source result with `formal_publish_allowed=true` blocks P2C-2

Observation statuses:

- `OBSERVATION_READY`: three days are present and boundary checks pass, but human confirmation still blocks automatic promotion.
- `OBSERVATION_BLOCKED`: at least one day has REVIEW/FAIL, missing artifacts, forbidden flags, or invalid publish authority.
- `OBSERVATION_INCOMPLETE`: fewer than three shadow days were observed.

## Scenarios

- all PASS shadow-only window
- REVIEW blocked window
- incomplete window
- missing shadow result
- forbidden public site update
- forbidden user notification
- forbidden live LLM review
- human confirmation required even when all days are confirmed in the fixture
- runtime ledger ignored by git

## Decision Matrix

| Scenario | observation_status | eligible_for_p2c2 | formal_publish_allowed | human_confirmation_required | blocked_reason |
| --- | --- | --- | --- | --- | --- |
| all PASS shadow-only window | OBSERVATION_READY | false | false | true | Human confirmation is still required. Shadow PASS is not formal PASS. |
| REVIEW blocked window | OBSERVATION_BLOCKED | false | false | true | REVIEW day blocks P2C-2. |
| incomplete window | OBSERVATION_INCOMPLETE | false | false | true | Observed 2/3 required shadow days. |
| missing shadow result | OBSERVATION_BLOCKED | false | false | true | missing `shadow-review-result.yaml` |
| public site update | OBSERVATION_BLOCKED | false | false | true | `public_site_updated=true` is forbidden |
| user notification | OBSERVATION_BLOCKED | false | false | true | `user_notification_sent=true` is forbidden |
| live LLM review | OBSERVATION_BLOCKED | false | false | true | `live_llm_review=true` is forbidden |

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
  tests.test_rubric_v21_p2c0_shadow_integration \
  tests.test_rubric_v21_p2c1_shadow_observation
```

Result:

```text
....................................................................................................................................................................
----------------------------------------------------------------------
Ran 164 tests in 505.655s

OK
```

Targeted P2C-1 result:

```text
.........
----------------------------------------------------------------------
Ran 9 tests in 0.607s

OK
```

## Git Policy

Runtime ledgers are written under `docs/quality/rubric-v2.1/shadow-runs/`, which is already ignored by `.gitignore`.

The intended tracked files are:

- `scripts/run_shadow_observation_ledger.py`
- `tests/test_rubric_v21_p2c1_shadow_observation.py`
- `docs/quality/rubric-v2.1/p2c1-shadow-observation-policy.yaml`
- `docs/quality/rubric-v2.1/P2C1_SHADOW_OBSERVATION_REPORT.md`

No runtime `shadow-runs/` artifacts or zip files should be committed.

## Next Step

If P2C-1 is accepted, the next step is P2C-1 commit confirmation. This is not P2C-2.
