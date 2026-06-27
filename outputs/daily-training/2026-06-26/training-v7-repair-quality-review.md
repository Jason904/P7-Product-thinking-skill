# Training V7 Repair Quality Review

Date: 2026-06-27

## Repair Objective

Repair `training-v7-raw.md` itself, not merely lower scores or bypass validation.

The repaired V7 must:

- pass the Markdown quality gate;
- pass the reader HTML completeness gate;
- remove repeated boilerplate;
- deepen all three deep cases to V6-like reasoning depth;
- make Insight Quality Audit evidence case-specific rather than generic.

## Source Recheck

The repair preserved the original source set and used the primary-source direction already recorded in V7:

- OpenRouter MCP Server: https://openrouter.ai/blog/announcements/openrouter-mcp-server/
- OpenRouter MCP docs: https://openrouter.ai/docs/mcp-server
- Runway Agent 2.0: https://runwayml.com/news/introducing-agent-2
- Vercel Eve GitHub: https://github.com/vercel/eve
- Vercel Eve docs: https://eve.dev/docs

AI HOT remains a signal source only. Final judgment rests on official/blog/docs/GitHub sources already referenced in the Markdown.

## What Was Repaired

### Case A: OpenRouter MCP Server

Before:

- 8 问 section was 1,662 chars.
- P7+ follow-up conclusions repeated boilerplate.
- Insight Audit evidence was generic.

After:

- 8 问 section is 2,950 chars.
- Added deeper reasoning on provider risk, budget governance, spend cap, auditability, benchmark vs real-task mismatch, runtime governance, and enterprise adoption.
- Replaced generic Audit rows with concrete evidence tied to model-selection governance.

Manual judgment:

- Insight quality: pass.
- Remaining risk: adoption and enterprise security acceptance still need real data.

### Case B: Runway Agent 2.0

Before:

- 8 问 section was 1,474 chars.
- Insight overview was 314 chars.
- Score was inflated at 97/100.
- The case said "marketing experiment loop" but did not fully prove the loop.

After:

- 8 问 section is 2,712 chars.
- Insight overview is 429 chars.
- Score recalibrated to 95/100.
- Added reasoning on marketer roles, ad metrics, brand consistency, creative fatigue, attribution, CTR/CVR/ROAS, experiment matrix, data permissions, and learning-loop speed.

Manual judgment:

- Insight quality: pass.
- Strongest improvement: the case now explains why "素材生成" is not the core; "增长实验学习速度" is the core.
- Remaining risk: public ROI / adoption evidence is still limited.

### Case C: Vercel Eve

Before:

- 8 问 section was 1,622 chars.
- P7+ follow-up conclusions repeated boilerplate.
- Audit evidence was generic.

After:

- 8 问 section is 2,984 chars.
- Added reasoning on filesystem-first as authoring interface, instructions/tools/skills/channels/schedules, personal workflow architecture, maintainability, reviewability, handoff, deployment, and long-term personal moat.
- Replaced generic Audit rows with concrete evidence tied to durable agent workflow architecture.

Manual judgment:

- Insight quality: pass.
- Strongest improvement: the case now serves the user's personal growth goal, not just open-source trend watching.
- Remaining risk: Eve still needs examples, releases, issue quality, and real production usage to prove long-term standard status.

## Automatic Gate Results

```text
python3 scripts/validate_hermes_output.py --mode daily outputs/daily-training/2026-06-26/training-v7-raw.md
PASS: Hermes output conforms to the requested contract.

python3 scripts/render_training_reader_html.py outputs/daily-training/2026-06-26/training-v7-raw.md
outputs/daily-training/2026-06-26/training-v7-reader.html

python3 scripts/validate_training_reader_html.py outputs/daily-training/2026-06-26/training-v7-reader.html
PASS: Hermes reader HTML contains complete rendered reasoning fields.
```

Regression tests:

```text
python3 -m unittest tests/test_hermes_output_validator.py tests/test_render_training_reader_html.py
Ran 32 tests - OK

python3 tests/verify_hermes_skill.py skill
PASS
```

## Manual Insight Review

| Case | Insight Depth | Evidence Quality | Reasoning Chain | Expression Value | Final Manual Result |
| --- | --- | --- | --- | --- | --- |
| OpenRouter MCP | 4.6/5 | 4.4/5 | 4.6/5 | 4.5/5 | Pass |
| Runway Agent 2.0 | 4.4/5 | 4.2/5 | 4.5/5 | 4.4/5 | Pass |
| Vercel Eve | 4.5/5 | 4.3/5 | 4.6/5 | 4.5/5 | Pass |

Manual conclusion:

V7 is now acceptable as a repaired training sample. It is not proof that the skill is permanently stable, but this specific artifact now meets the strengthened standard:

- no repeated boilerplate;
- all 3 deep cases are materially deeper;
- Runway's score is no longer inflated;
- Insight Audit rows now contain concrete case evidence;
- generated HTML preserves the reasoning content.

## Remaining Non-Blocking Risks

- All three cases still rely on early product/repo signals; long-term adoption remains unproven.
- The next stability test should generate a fresh V8 from new cases rather than further polishing V7.
- Future gates should add a semantic check for generic Insight Audit evidence, not only repeated known phrases.

