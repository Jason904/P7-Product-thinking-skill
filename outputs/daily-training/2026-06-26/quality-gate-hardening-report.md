# Quality Gate Hardening Report

Date: 2026-06-27

## What Changed

This patch turns the V7 regression into deterministic checks.

## New Gates

1. Markdown anti-regression gate in `scripts/validate_hermes_output.py`
   - Rejects repeated boilerplate/template phrasing across daily deep cases.
   - Rejects high Insight scores when the 8 问 section is too thin.
   - Rejects high Insight scores when the Insight overview is too thin.
   - Forces Quality Review Rubric scores to disclose validation failures.

2. Reader HTML completeness gate in `scripts/validate_training_reader_html.py`
   - Requires at least 3 rendered deep cases.
   - Requires each deep case to render 8 8-question cards.
   - Requires each 8-question card to contain non-empty fields for:
     - 目的
     - 分析方法
     - 为什么用这个方法
     - 推导过程
     - 阶段结论
     - 如何影响下一步

3. Skill workflow update
   - Daily mode now requires:
     - `validate_hermes_output.py`
     - `render_training_reader_html.py`
     - `validate_training_reader_html.py`
   - Markdown PASS is explicitly not treated as HTML/content-completeness PASS.

## Regression Evidence

V6 still passes the Markdown validator:

```text
PASS: Hermes output conforms to the requested contract.
```

V7 now fails the Markdown validator with concrete reasons:

```text
Daily deep cases repeat boilerplate/template phrase 9 times: 它把最终结论进一步压实为可验证的行动取舍
Deep case 1: high Insight score 96/100 requires 8-question depth >= 1800 chars; found 1662
Deep case 2: high Insight score 97/100 requires 8-question depth >= 1800 chars; found 1474
Deep case 2: high Insight score 97/100 requires Insight overview >= 340 chars; found 314
Deep case 3: high Insight score 96/100 requires 8-question depth >= 1800 chars; found 1622
Quality Review Guardrail: Case Asset Card 可复用度 must be at most 3 when validation fails
```

V6 and the fixed V7 reader HTML both pass the new HTML completeness validator:

```text
PASS: Hermes reader HTML contains complete rendered reasoning fields.
```

This means the current V7 HTML no longer has empty 8 问 cards, but the V7 Markdown content is still not acceptable as V6-level Insight quality.

## Test Results

```text
python3 -m unittest tests/test_hermes_output_validator.py
Ran 27 tests - OK

python3 -m unittest tests/test_render_training_reader_html.py
Ran 5 tests - OK

python3 tests/verify_hermes_skill.py skill
PASS

python3 -m py_compile validate_hermes_output.py validate_training_reader_html.py render_training_reader_html.py
PASS
```

## Current Judgment

The skill package is stronger than before, but the content-generation standard is still not fully proven stable.

What is now proven:

- V6-level sample can still pass.
- V7-style high-score thin reasoning will be blocked.
- Empty rendered 8 问 fields will be blocked.
- The daily workflow now distinguishes Markdown structure, HTML completeness, and human Insight quality.

What remains:

- Rewrite or regenerate V7 content so it passes the new gates honestly.
- Add deeper semantic quality checks if future regressions appear, especially for case-specific evidence, buyer/adoption logic, and non-generic Insight Audit evidence.

