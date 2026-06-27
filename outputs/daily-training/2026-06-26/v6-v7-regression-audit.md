# V6 vs V7 Regression Audit

Date: 2026-06-26

## Executive Conclusion

V7 cannot be honestly called "stable V6-level output" yet.

The current chain passes structure checks, but it does not yet prove content quality or reader HTML completeness. The earlier "end-to-end blind test passed" conclusion should be downgraded to:

> Structure pipeline passed; quality pipeline and HTML content-completeness checks were insufficient.

## Evidence

| Check | V6 | V7 | Judgment |
| --- | ---: | ---: | --- |
| Raw Markdown size | 52,863 chars / 1,865 lines | 48,164 chars / 1,543 lines | V7 is materially shorter. Not automatically bad, but needs quality explanation. |
| Case 2 size | 15,154 chars | 11,392 chars | V7 Case 2 is much thinner. |
| Case 2 8-question section | 2,476 chars | 1,474 chars | V7 8-question reasoning depth regressed. |
| Case 2 Insight overview | 491 chars | 314 chars | V7 top-level insight is less developed. |
| Repeated boilerplate phrase | 0 | 9 across all deep cases | V7 has obvious templating smell. |
| Validator result | PASS | PASS | Validator is too structural; it missed quality regression. |
| Skill package verification | PASS | PASS | Skill verification does not prove daily output quality. |
| Original V7 HTML 8-question rendering | Complete source in MD, but empty cards in reader | Failed before renderer fix | Renderer lost inline field values such as `目的：...`. |

## Root Cause

### 1. Renderer format bug

V6 used this field style:

```text
目的：
识别 connector governance 影响的决策链。
```

V7 used this field style:

```text
目的：识别核心利益相关人和实际受影响对象。
```

The renderer only recognized label-only lines, so V7's 8-question fields were dropped in HTML. The Markdown had content, but the reader surface hid it.

Status: fixed in `skill/scripts/render_training_reader_html.py` and covered by `tests/test_render_training_reader_html.py`.

### 2. Validator gap

`validate_hermes_output.py --mode daily` checks required markers and score structure. It does not currently verify:

- rendered HTML contains non-empty 8-question field values;
- every deep case has V6-level case-specific reasoning;
- repeated boilerplate is absent;
- Insight Quality Audit scores are backed by non-generic evidence;
- V7 scores are calibrated against actual depth.

### 3. Content generation regression

V7 Case 2 is conceptually on the right topic, but its reasoning is more generic than V6 Case 2.

V6 Case 2 shows concrete product mechanics:

- IT/admin, security, compliance, developers, procurement and business users are separated.
- Connectors are connected to service accounts, multi-account access, debugging, workflows and governance.
- The 8 questions repeatedly push from product feature to adoption gate, purchase gatekeeper and enterprise risk.

V7 Case 2 is weaker:

- "founder, solo marketer, brand team..." is listed, but the power/decision relationship is not deeply unpacked.
- "营销实验闭环" is directionally right, but the proof is thin: not enough product mechanics, adoption constraints, buyer economics or ROI evidence.
- Several field answers are valid but short: "核心损失是学习速度", "瓶颈是业务闭环", "系统变量决定 adoption".
- The case self-scores 97/100, which is inflated relative to the depth shown.

## Acceptance Judgment

Current status:

- Source-to-MD structure: acceptable but not enough.
- MD quality stability: not yet stable at V6 standard.
- HTML rendering: critical 8-question bug fixed, but the renderer needs a stronger completeness audit.
- End-to-end claim: should be changed from "passed" to "partially passed with quality regressions."

Estimated distance to target:

| Layer | Current Level | Target Level | Gap |
| --- | --- | --- | --- |
| Source search and candidate pool | 75% | 90%+ | Needs reproducible source log and source-grade enforcement. |
| MD structure | 90% | 95%+ | Mostly stable. |
| Insight depth | 70% | 90%+ | Biggest gap. V7 proves quality can drift. |
| Expression quality | 75% | 90%+ | PREP/SCQA exists, but not always deep enough. |
| HTML reader rendering | 80% after fix | 90%+ | Needs automated completeness and visual checks. |
| Quality governance | 60% | 90%+ | Current validator misses the issues the user cares about most. |

## Required Remediation

1. Add a rendered-HTML completeness gate.
   - For each deep case, assert 8 question cards exist.
   - Assert each card has non-empty `目的 / 分析方法 / 为什么用这个方法 / 推导过程 / 阶段结论 / 如何影响下一步`.
   - Assert no empty field cards are generated.

2. Add content anti-boilerplate checks.
   - Reject repeated generic phrases across cases.
   - Reject audit evidence such as "已覆盖关键机制" when it does not cite concrete case content.

3. Add V6-depth calibration.
   - Every deep case should meet minimum depth bands for key sections.
   - Case-specific evidence must appear in 8-question derivations, not only generic framework language.
   - Scores above 95 must require unusually strong evidence, not merely complete structure.

4. Re-audit V7 manually before accepting it.
   - V7 Case 2 should be deepened or downgraded.
   - The current 97/100 score should not stand unless the case is rewritten with stronger product mechanics, buyer/adoption logic, ROI proof and expression quality.

5. Update the Skill after the audit.
   - The skill should explicitly say that validator pass does not equal quality pass.
   - Daily mode must run structure validation, renderer validation, HTML completeness validation and Insight quality audit before claiming stable output.

