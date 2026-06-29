# P2B-0 本地语义 Reviewer 去配置化加固报告

## 本轮边界

- 仍然是 `local_semantic_reviewer`，不是 live LLM reviewer。
- 不接入 P2C，不接入每日自动发布。
- `SAMPLE_CONFIGS.expected_decision` 只作为测试预期，不进入 reviewer decision 数据流。

## Evidence-derived Decision

Case 判定来自 Markdown 中可观察到的三类证据：3 个 deep case、每个 case 的 8 问字段完整性，以及分析方法、六层总结、PREP/SCQA、Case Asset Card 的最低语义结构。
Daily 判定由三个 case decision、failure objects 和 governance validator 结果聚合，禁止读取 expected decision。
原文中的 Insight Quality Audit 只作为被审对象，不作为放行依据。

## Audit 依赖边界

有 audit 时，历史审计用于增强 `DISCONNECTED_8Q_CHAIN` 等需要纵向比较的判断。
无 audit 时，reviewer 仍可检查跨 Case 的模板重复、相对深度失衡、self-review 高分冲突与 HTML 8 问锚点完整性。
无 audit 的启发式证据不足以独立证明完整因果质量，因此必须输出 uncertainty boundary；不能因此给 PASS。

## V3 / V6 PASS 证据

V3/V6 的 PASS 不再来自 source existence。每个 deep case 必须实际满足 8/8 有效问题和完整语义模块；V6 reader HTML 还必须保留 24 个 8 问锚点。

## 当前结果

| Sample | Decision | Publish | Failure types |
| --- | --- | --- | --- |
| `v3_target` | `PASS` | `True` | `` |
| `v6_target` | `PASS` | `True` | `` |
| `v7_failure` | `FAIL_DAILY` | `False` | `BOILERPLATE_REASONING, CASE_DEPTH_IMBALANCE, REVIEW_EVIDENCE_INVALID, DISCONNECTED_8Q_CHAIN` |
| `v7_failure_no_audit` | `REVIEW` | `False` | `BOILERPLATE_REASONING, CASE_DEPTH_IMBALANCE, REVIEW_EVIDENCE_INVALID` |

## 下一步判断

下一步是 P2B-1 stability / no-audit stress，用输入扰动和缺少辅助 audit 的场景验证不误放坏样本、不误杀好样本。
当前不具备进入 P2C 的证据。

本次报告由 `--no-audit=false` 运行更新；本次直接运行样本： `v3_target, v6_target, v7_failure`。
