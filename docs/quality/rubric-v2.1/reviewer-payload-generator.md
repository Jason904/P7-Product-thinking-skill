# Reviewer Payload Generator

## Purpose

P2A tests whether real training artifacts can be read and converted into Rubric v2.1 governance payload files:

- `reviewer-output.json`
- `claim-evidence-map.json`
- `failure-objects.json`
- `generation-log.yaml`
- `validator-result.yaml`

This stage does not integrate the daily publishing pipeline.

## Current Mode

The current implementation is a recorded generator:

- `recorded_generation: true`
- `not_live_llm_review: true`
- `generation_method: recorded_fixture_replay`

It reads real source files, records file hashes and byte counts, replays the P1 calibration payload for that real sample, and then runs the existing P1 governance validator.

## Inputs

Each real sample is defined by the existing calibration `source-manifest.yaml`.

Required:

- `source_markdown`

Optional:

- `source_html`
- `source_records`
- historical audit / quality report
- Rubric v2.1 docs, schemas, anchors, and validator

## Outputs

Generated output is written to:

```text
docs/quality/rubric-v2.1/generated-replay/{sample_id}/
```

Each sample directory contains:

```text
reviewer-output.json
claim-evidence-map.json
failure-objects.json
generation-log.yaml
validator-result.yaml
```

## Real Samples

- `v3_target`: expected PASS
- `v6_target`: expected PASS
- `v7_failure`: expected FAIL_DAILY / PUBLISH_BLOCK / REVIEW, never PASS

## Non-Goals

- Do not change Rubric v2.1.
- Do not change the P1 governance validator unless a clear bug is found.
- Do not claim live LLM review quality.
- Do not connect daily auto publishing.
- Do not use original self-review scores as release evidence.

## Boundary

P2A proves the file-to-payload-to-validator path. It does not prove automatic semantic review from Markdown. That is the next stage.
