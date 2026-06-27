# Failure Feedback Loop

Use this reference whenever Hermes daily training, Markdown validation, HTML rendering, visual reading, or user review reveals instability. The goal is not to patch one output. The goal is to improve the skill so future runs become more stable.

## Required Loop

1. **失败登记**  
   Record the failed artifact, user-visible symptom, affected stage, severity, and why the output cannot be called stable.

2. **失败归因**  
   Classify the root cause into one or more buckets:
   - 案例选择失败
   - 事实来源失败
   - 推理深度失败
   - 表达模板化失败
   - HTML 渲染失败
   - 视觉阅读失败
   - 验收流程失败

3. **规则回流**  
   Update the smallest durable rule surface that would have prevented the failure:
   - `SKILL.md` for mandatory workflow.
   - `references/framework.md` for reasoning and quality standards.
   - `references/templates.md` for required output shape.
   - renderer or validator scripts when the failure is deterministic.

4. **测试回流**  
   Add at least one regression test for every severe failure. The test must fail before the fix and pass after the fix.

5. **复测回归**  
   Re-run the relevant validators and tests:
   - Markdown validator for content completeness.
   - HTML validator for rendered completeness.
   - Skill verifier for package consistency.
   - Targeted unit tests for the failed behavior.

6. **失败处理**  
   Do not publish the daily HTML link or claim stability while a required gate fails. Choose one path:
   - 修改内容
   - 降低评分
   - 重做案例
   - 修脚本
   - 修技能规则
   - 记录为待核验并移出最终判断

## Severity

| 级别 | 判断标准 | 处理 |
| --- | --- | --- |
| P0 | 网页或 Markdown 缺少核心训练内容 | 阻断发布，必须修复并回流测试 |
| P1 | 高分内容浅、模板化、事实支撑不足 | 阻断“稳定通过”结论，必须修复或降分 |
| P2 | 阅读体验或导航影响理解但内容完整 | 修复后复测视觉和交互 |
| P3 | 文案瑕疵、不影响训练判断 | 记录，批量处理 |

## Exit Criteria

A failure is closed only when:

- The failure is recorded in `references/failure-cases.md`.
- The root cause is named, not only the symptom.
- At least one rule or script was updated, or the record explains why no rule change is appropriate.
- At least one regression test or verification command covers the failure.
- The relevant commands pass.
- The next generated artifact no longer shows the same failure.

If these are not true, the failure is still open.
