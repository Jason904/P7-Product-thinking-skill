# P2B-0 Evidence-Derived Local Reviewer Samples Report

## Boundary

This is a local semantic reviewer, not a live LLM reviewer.
It proves three-sample evidence-derived local semantic replay only and does not prove cross-date generalization.
It does not enter P2C daily production.
Expected decisions in sample configuration are test oracles only and never feed reviewer decisions.
Next stage is P2B-1 stability / no-audit stress, not P2C daily production integration.

## Results

| Sample | Decision | Publish | Validator | Output |
| --- | --- | --- | --- | --- |
| `v3_target` | `PASS` | `True` | `PASS` | `docs/quality/rubric-v2.1/generated-replay/v3_target_live` |
| `v6_target` | `PASS` | `True` | `PASS` | `docs/quality/rubric-v2.1/generated-replay/v6_target_live` |
| `v7_failure` | `FAIL_DAILY` | `False` | `PASS` | `docs/quality/rubric-v2.1/generated-replay/v7_failure_live` |
