# Reviewer Generation Protocol

## Execution Order

1. Load Rubric v2.1 directory.
2. Load sample `source-manifest.yaml`.
3. Read every real source file listed in the manifest.
4. Record each input file path, byte count, and SHA-256 hash.
5. Generate governance payloads.
6. Run existing validator functions:
   - `validate_reviewer_output`
   - `validate_claim_evidence_map`
   - `validate_failure_object`
7. Write `validator-result.yaml`.
8. Write `generation-log.yaml`.
9. Compare generated result against P1 golden expectations.

## Required Output Fields

`generation-log.yaml` must include:

- `sample_id`
- `created_at`
- `prompt_version`
- `generation_method`
- `recorded_generation`
- `not_live_llm_review`
- `input_files`
- `output_paths`
- `validator_result`
- `self_review_policy`

`validator-result.yaml` must include:

- `sample_id`
- `validator_status`
- `reviewer_errors`
- `claim_evidence_map_errors`
- `failure_object_errors`
- `daily_decision`
- `publish_allowed`
- `failure_types`
- `failure_categories`
- `golden_comparison`

## Golden Comparison

For V3 / V6 / V7, compare:

- daily decision
- publish permission
- case decisions
- S-level item status
- expected failure types
- caps applied

## Failure Classes

The generator must keep these categories separate:

- content quality failure
- HTML rendering integrity failure
- source evidence failure
- self-review inflation

## Self-Review Rule

Original `Insight Quality Audit`, self-review tables, and quality scores in the generated training draft are reviewed content. They are never release authority.

## Current P2A Constraint

The current generator is recorded, not live:

```yaml
recorded_generation: true
not_live_llm_review: true
```

P2A remains recorded replay only. Evidence-derived local reviewer work starts at P2B-0, and stability / no-audit stress starts at P2B-1. Neither stage is a live LLM reviewer.
