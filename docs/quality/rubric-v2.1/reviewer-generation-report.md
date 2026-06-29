# Reviewer Generation Report

## Scope

P2A validates the reviewer-payload generation boundary for real historical samples. It does not connect the daily publishing pipeline and does not claim live semantic reviewer stability.

## Generation Mode

- `recorded_generation: true`
- `not_live_llm_review: true`
- Method: read real source files, record file hashes, replay P1 calibration payloads, then run the existing Rubric v2.1 governance validator.
- Self-review / Insight Quality Audit text is treated as reviewed content, not as release authority.

## Sample Results

| Sample | Decision | Publish | Validator | Output |
| --- | --- | --- | --- | --- |
| `v3_target` | `PASS` | `True` | `PASS` | `docs/quality/rubric-v2.1/generated-replay/v3_target` |
| `v6_target` | `PASS` | `True` | `PASS` | `docs/quality/rubric-v2.1/generated-replay/v6_target` |
| `v7_failure` | `FAIL_DAILY` | `False` | `FAIL` | `docs/quality/rubric-v2.1/generated-replay/v7_failure` |

## Real Samples

- `v3_target`: reads `outputs/daily-training/2026-06-25/training-v3.md` and should PASS.
- `v6_target`: reads `training-v6-raw.md`, `training-v6-reader.html`, source notes and quality report; should PASS.
- `v7_failure`: reads `training-v7-raw.md`, `training-v7-reader.html`, source notes and regression audit; must not PASS.

## Generated Artifacts

Each sample directory under `docs/quality/rubric-v2.1/generated-replay/` contains:

- `reviewer-output.json`
- `claim-evidence-map.json`
- `failure-objects.json`
- `generation-log.yaml`
- `validator-result.yaml`

## Semantic Boundary

The current generator is a recorded/mock generator. It proves file ingestion, trace logging, payload materialization, validator execution, and golden comparison wiring. It does not prove that a live LLM can independently read Markdown/HTML and generate the same payload.

## Human Confirmation Still Needed

- Whether the recorded P1 fixture judgments remain semantically acceptable after future Rubric updates.
- Whether live Markdown-to-payload generation can match the recorded judgments across more unseen days.
- Whether P2B should broaden the replay set before P2C daily pipeline integration.

## Next Gate

Proceed to P2B only after live or semi-live reviewer generation can reproduce V3/V6 PASS and V7 non-PASS without relying on recorded fixture payloads.
