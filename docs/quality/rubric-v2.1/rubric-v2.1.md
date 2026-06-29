# Rubric v2.1 可执行质量治理协议

本文档定义高阶产品思维每日训练的内容质量评审协议。它不是普通打分表，而是用于拦截新闻摘要型内容、空壳 8 问、方法名堆砌、事实不支撑判断、高分虚高、Case 深度不一致、HTML 丢内容和生成者自评诱导放行的治理规则。

## 文件职责

| 文件 | 职责 |
| --- | --- |
| `rubric-v2.1.md` | 人类可读评审协议 |
| `rubric-enums.yaml` | item、failure、decision、repair、gate、check type 的唯一枚举源 |
| `rubric-score-anchors.yaml` | 每个观察项的 0 到满分评分锚点、坏模式、满分要求和封顶条件 |
| `reviewer-output.schema.json` | 独立评审输出结构和分数生命周期校验 |
| `claim-evidence-map.schema.json` | 核心判断和证据绑定结构 |
| `failure-object.schema.json` | 失败类型、修复目标、发布阻断和重试预算结构 |
| `calibration-tests.yaml` | 好坏样本、临界样本、人工偏好样本的预期断言 |
| `repair-rerun-map.yaml` | 每类修复后必须重跑哪些门禁 |
| `validator-check-map.yaml` | 哪些检查机器做、哪些启发式做、哪些 AI 做、哪些用户判断 |

## 0. 唯一命名锁定

所有实现必须引用 `rubric-enums.yaml`。同一个概念只能有一个 ID。

禁止出现同义字段：

| 禁止写法 | 正式 ID |
| --- | --- |
| `eightq_validity` / `8q_reasoning` | `thinking.eightq_reasoning_validity` |
| `core_claim_fact_support` | `content.fact_support_core_claim` |
| `method_insight` | `thinking.method_insight_generation` |
| `final_tradeoff` | `thinking.final_tradeoff_validation` |

如果 reviewer prompt、schema、validator、calibration fixture 中出现未登记枚举，视为 `REVIEWER_OUTPUT_INVALID`。

## 1. 判定优先级

评审必须按以下顺序执行。后面的规则不能覆盖前面的硬失败。

| 顺序 | 环节 | 输入 | 输出 | 失败动作 |
| ---: | --- | --- | --- | --- |
| 1 | 硬门禁 | Markdown、来源记录、HTML、枚举文件 | G0-G8 状态 | 失败即阻断发布 |
| 2 | 一票否决 | 伪造来源、核心事实无 A/B 证据、HTML 核心丢失 | `PUBLISH_BLOCK` | 不进入发布 |
| 3 | 封顶规则 | failure_type、证据强度、样本类型 | item/account/global cap | 限制最高分 |
| 4 | 逐项锚点评分 | 原文证据、观察项、评分锚点 | raw_score | 形成原始分 |
| 5 | 扣分规则修正 | 缺失项、套话、边界不足 | adjusted_score | 记录扣分原因 |
| 6 | 关键项底线 | S/A/B 观察项 | item decision | 低于底线触发修复或阻断 |
| 7 | 质量账户阈值 | account_final_score | account decision | 不允许跨账户补偿 |
| 8 | 总分阈值 | case_final_total | case decision | 不允许跨 Case 补偿 |
| 9 | 二审触发 | 临界分、冲突、证据不足 | second_review | 仅解决争议 |
| 10 | 最终状态 | 全部门禁和评审结果 | PASS / REVIEW / FAIL | 决定发布、重试、回流 |

Second review is not an override mechanism. It is only a dispute-resolution mechanism.

二审不能覆盖：

- 硬门禁失败
- S 级 FAIL
- 核心事实没有 A/B 证据
- HTML 核心内容丢失
- 空壳 8 问
- 来源不可追溯
- 用户已标记的严重 Bad Case

## 2. Case-level / Daily-level 聚合协议

每日训练固定 3 个 deep case。每个 case 独立 100 分评审。

核心原则：禁止跨 Case 补偿。Daily 发布不是三篇平均分游戏，而是三个深度 case 都必须独立达到训练质量。

```json
{
  "case_score_policy": "each_deep_case_scored_independently_100",
  "daily_score_policy": "no_cross_case_compensation",
  "daily_decision_rule": "all_cases_must_pass",
  "publish_allowed_rule": "daily_pass_and_g6_g7_g8_pass"
}
```

规则：

- 每个 Case 必须独立满足 `thinking_depth >= 38`、`content_quality >= 25`、`expression_quality >= 21`、`total >= 85`。
- Daily 不用平均分决定发布。
- 任一 Case `REVIEW`，Daily 为 `REVIEW`。
- 任一 Case `FAIL_DAILY` 或 `PUBLISH_BLOCK`，Daily 为失败。
- Case A 高分不能补偿 Case B/C 的 S 级失败、账户低分或证据不足。
- G6/G7/G8 任一失败，即使内容分达标，也不能发布 HTML。

## 3. 质量账户和权重

每个观察项只能有一个 `primary_account`。`secondary_tags` 可用于解释，但不计分，避免重复计分。

### thinking_depth = 45

| item_id | 等级 | 分值 | 最低通过 | 核心判断 |
| --- | --- | ---: | ---: | --- |
| `thinking.p6_to_p7_reframe` | A | 3 | 2 | 是否刹住 P6+ 第一反应并说明对与不足 |
| `thinking.problem_reframing` | A | 5 | 4 | 是否把现象重构成真实产品/系统问题 |
| `thinking.eightq_reasoning_validity` | S | 6 | 4 | 8 问是否有效、连续、非空壳 |
| `thinking.causal_mechanism` | S | 7 | 5 | 是否解释变量之间的传导机制 |
| `thinking.system_relation_value_flow` | A | 5 | 4 | 是否看清参与方、推力、阻力、价值流 |
| `thinking.counterfactual_boundary` | A | 5 | 4 | 是否说明判断何时不成立 |
| `thinking.trend_projection` | A | 4 | 3 | 是否有阶段推演，不是泛泛趋势 |
| `thinking.final_tradeoff_validation` | S | 5 | 4 | 是否给出做/不做/先验证和验证路径 |
| `thinking.method_insight_generation` | A | 5 | 4 | 方法是否真的生成洞察 |

### content_quality = 30

| item_id | 等级 | 分值 | 最低通过 | 核心判断 |
| --- | --- | ---: | ---: | --- |
| `content.fact_support_core_claim` | S | 8 | 6 | 核心判断是否由 A/B 证据支撑 |
| `content.source_traceability` | A | 5 | 4 | 来源是否可追溯到原文或本地 source record |
| `content.case_specificity_context` | A | 5 | 4 | 是否有足够具体场景、对象、变量 |
| `content.claim_evidence_alignment` | S | 5 | 4 | 证据是否真正支撑判断而非只被提到 |
| `content.uncertainty_boundary` | A | 3 | 2 | 是否区分事实、观点、推断、假设 |
| `content.information_density` | B | 4 | 3 | 信息密度是否足够支撑学习 |

### expression_quality = 25

| item_id | 等级 | 分值 | 最低通过 | 核心判断 |
| --- | --- | ---: | ---: | --- |
| `expression.conclusion_first` | A | 4 | 3 | 是否结论先行且不是空话 |
| `expression.structure_readability` | B | 4 | 3 | 是否结构清晰、模块标题服务阅读 |
| `expression.prep_scqa_quality` | B | 5 | 3 | PREP/SCQA 是否可真实表达 |
| `expression.interview_followup_resilience` | A | 4 | 3 | 是否能承接追问 |
| `expression.case_asset_card_transfer` | B | 5 | 3 | Asset Card 是否可迁移和复用 |
| `expression.memory_point_pattern` | B | 3 | 2 | 是否沉淀记忆点和 Pattern |

## 4. G-Valid 最低可检规则

硬门禁分三层：

- G-Exist：模块存在。
- G-Complete：字段完整。
- G-Valid：达到最低有效标准。

### 8 问 G-Valid

- 有效问数 >= 7/8。
- 每问至少包含：问题本身、目的、分析方法、为什么使用该方法、推导过程、阶段结论、如何影响下一步。
- 连续推进关系 >= 5 处。
- 空泛回答数量 <= 1。
- 同质化套话数量 <= 1。
- 阶段结论缺失数量 <= 1。
- “如何影响下一步”缺失数量 <= 1。

### 分析方法工作台 G-Valid

- 每个方法必须有：为什么使用、分析维度、推导过程、发现、如何影响最终判断。
- `method_name_only_count = 0`。
- `valid_method_count >= 1`。
- 至少一个方法必须改变或深化判断。

### PREP / SCQA G-Valid

- PREP 必须包含 Point、Reason、Evidence、Point reinforced。
- SCQA 必须包含 Situation、Complication、Question、Answer。
- 必须含具体 case 证据和最终行动判断。
- 不能只是复制正文。

### Case Asset Card G-Valid

- 必须包含 case 名称、一句话现象、一句话本质、核心矛盾、关键系统关系、价值流向、做/不做/先验证、可复用 Pattern、迁移对象、Watchlist 状态、资产等级。
- 不能只是摘要复述。
- 资产等级必须有原因。

## 5. 分数生命周期

每个 item、account、case 都必须可复算。

逐项评分必须引用 `rubric-score-anchors.yaml`。评分锚点不是形容词判断，而是先勾选该 item 的 `objective_checks`，再选择满足全部 `required_checks` 的最高分。不能因为文字“看起来深入”而越过客观检查项给高分。

```json
{
  "raw_score": 5,
  "caps_applied": [
    {
      "cap_type": "item_cap",
      "reason": "evidence_sufficiency = PARTIAL",
      "max_allowed_score": 3
    }
  ],
  "capped_score": 3,
  "deductions_applied": [
    {
      "reason": "missing validation path",
      "points": 1
    }
  ],
  "adjusted_score": 2,
  "final_score": 2
}
```

账户层和 Case 层：

```json
{
  "account_raw_score": 42,
  "account_cap_applied": {
    "cap_type": "account_cap",
    "reason": "NO_COUNTERFACTUAL_BOUNDARY",
    "max_allowed_score": 34
  },
  "account_final_score": 34,
  "case_raw_total": 88,
  "case_global_cap_applied": {
    "cap_type": "global_cap",
    "reason": "NEWS_SUMMARY_ONLY",
    "max_allowed_score": 70
  },
  "case_final_total": 70
}
```

计算顺序：

1. item raw_score 按锚点初评。
2. item cap 后得到 capped_score。
3. 扣分规则后得到 adjusted_score。
4. final_score 等于 adjusted_score。
5. item final_score 汇总到账户 raw score。
6. account cap 后得到 account_final_score。
7. 三个 account_final_score 汇总为 case_raw_total。
8. global cap 后得到 case_final_total。
9. case_final_total 进入 case decision。

Reviewer Output Validator 必须校验：

- `capped_score <= raw_score`
- `adjusted_score <= capped_score`
- `final_score == adjusted_score`
- `final_score <= max_score`
- `final_score <= item cap`
- `account_raw_score == sum(item.final_score)`
- `account_final_score <= account_raw_score`
- `case_final_total <= case_raw_total`
- global cap 生效时 `case_final_total <= cap`

公式不一致时：

- `reviewer_output_valid = false`
- `failure_type = REVIEW_EVIDENCE_INVALID`
- 不能进入发布判断

## 6. Evidence Object v2

Evidence Object v2 必须记录证据强度，不允许“原文提到了”直接等于“证据足够”。

```json
{
  "item_id": "thinking.causal_mechanism",
  "raw_score": 5,
  "capped_score": 3,
  "adjusted_score": 3,
  "final_score": 3,
  "max_score": 7,
  "anchor_matched": "3分：有原因解释，但机制链条不完整",
  "required_evidence_points": [
    {
      "point": "成本下降如何影响产品形态",
      "support_level": "SUFFICIENT"
    },
    {
      "point": "企业为什么愿意付费",
      "support_level": "PARTIAL"
    }
  ],
  "item_evidence_sufficiency": "PARTIAL",
  "positive_evidence": [
    {
      "quote": "原文具体句子",
      "location": "Case A / 第7问 / 第2段",
      "supports_what": "证明作者提到了成本下降",
      "evidence_sufficiency": "PARTIAL",
      "why_insufficient": "没有解释成本如何传导到产品形态和付费意愿"
    }
  ],
  "missing_evidence": [
    "缺少成本下降到产品形态变化的传导链"
  ],
  "deduction_reason": "有趋势判断，但缺少因果机制",
  "why_not_higher": "没有形成完整变量链，因此不能给 4 分",
  "repair_action": "rewrite_causal_chain",
  "decision": "REWRITE_MODULE"
}
```

证据强度规则：

- 对同一个 required claim，取最能支撑该 claim 的证据强度。
- 对不同 required claim，分别判断 sufficiency。
- 如果某个必要 claim 缺证据，则 item_sufficiency 降级。
- 不能因为一条附加弱证据存在，就拖低已经被充分证据支撑的 claim。
- 也不能因为一条强证据存在，就覆盖其他未支撑部分。

封顶规则：

- `SUFFICIENT`：不封顶。
- `PARTIAL`：最高 `floor(max_score * 0.7)`。
- `INSUFFICIENT`：最高 2 分。
- `MISSING`：0 分。

取整统一向下取整。例如 max_score = 7，PARTIAL 最高 `floor(7 * 0.7) = 4`；max_score = 5，PARTIAL 最高 `floor(5 * 0.7) = 3`。

## 7. Claim Evidence Map

每个 Case 至少 1 个、最多 3 个 core claim。每个 core claim 必须绑定 supporting facts。

```json
{
  "claim_id": "case_a_core_claim_01",
  "claim_text": "最大机会不在一次性生成内容，而在企业级工作流治理",
  "claim_type": "core_judgment",
  "supporting_facts": [
    {
      "fact": "官方 release 提供了企业治理功能",
      "source": {
        "title": "Official release note",
        "url": "https://example.invalid/release",
        "source_type": "official_doc",
        "published_at": "2026-06-27",
        "accessed_at": "2026-06-27",
        "fact_confidence": "A"
      },
      "supports_claim_how": "证明该方向正在被产品化"
    }
  ],
  "support_level": "PARTIAL",
  "unsupported_parts": [
    "商业付费意愿仍缺少直接证据"
  ],
  "decision_impact": "supports final_tradeoff"
}
```

规则：

- A/B 级证据必须有可追溯链接或本地 source record。
- C/D 级事实不得支撑 core_claim。
- 如果 source object 缺 url、title 或 confidence，Claim Evidence Map 不得判定 `SUFFICIENT`。
- 有来源表不等于核心判断被支持；必须说明 `supports_claim_how`。

## 8. S/A/B 失败动作

S 级不是只看分数，而是看失败类型。

| failure_type | primary_decision | repair_action | publish_allowed | retry_allowed |
| --- | --- | --- | --- | --- |
| `NO_AB_EVIDENCE_FOR_CORE_CLAIM` | `REPLACE_CASE` | `replace_case` | false | true |
| `C_OR_D_FACT_SUPPORTS_CORE_CLAIM` | `PUBLISH_BLOCK` | `supplement_sources` 或 `replace_case` | false | true |
| `EMPTY_8Q_REASONING` | `PUBLISH_BLOCK` | `rewrite_8q_reasoning` | false | true |
| `DISCONNECTED_8Q_CHAIN` | `FAIL_DAILY` | `rewrite_8q_reasoning` | false | true |
| `WEAK_CAUSAL_CHAIN` | `REWRITE_MODULE` | `rewrite_causal_chain` | false | true |
| `NO_CAUSAL_MECHANISM` | `FAIL_DAILY` | `rewrite_causal_chain` | false | true |
| `NO_FINAL_TRADEOFF` | `FAIL_DAILY` | `rewrite_tradeoff_validation` | false | true |
| `NO_VALIDATION_PATH` | `REWRITE_MODULE` | `rewrite_tradeoff_validation` | false | true |
| `HTML_CONTENT_LOSS` | `PUBLISH_BLOCK` | `repair_html_renderer` | false | true |
| `REVIEWER_OUTPUT_INVALID` | `USER_REVIEW_REQUIRED` | `request_human_review` | false | false |

Decision FSM：

```text
PUBLISH_BLOCK
> FAIL_DAILY
> REPLACE_CASE
> REWRITE_CASE
> REWRITE_MODULE
> USER_REVIEW_REQUIRED
> REVIEW
> PASS_WITH_MINOR_REPAIR
> PASS
```

`decision_state` 表示当前审查状态。`repair_action` 表示下一步修复动作。`publish_allowed` 表示是否允许发布。

```json
{
  "decision_state": "FAIL_DAILY",
  "publish_allowed": false,
  "repair_action": "rewrite_8q_reasoning",
  "retry_allowed": true,
  "retry_budget": {
    "max_retries_per_gate": 2,
    "current_retry_count": 1,
    "retry_allowed": true
  }
}
```

`FAIL_DAILY` 不等于永不修复。它只表示当前版本不能发布。是否允许自动重试由 `retry_allowed` 和 `retry_budget` 决定。

## 9. 封顶规则升级

封顶分四类：

| 类型 | 作用范围 | 示例 | 动作 |
| --- | --- | --- | --- |
| item cap | 单个观察项 | 证据 PARTIAL | 限制 item final_score |
| account cap | 单个账户 | 缺少反事实边界 | 限制 thinking_depth |
| global cap | 整个 case | 新闻摘要型内容 | 限制 case_final_total |
| publish block | 发布状态 | HTML 丢内容、伪造来源 | `publish_allowed = false` |

封顶不等于自动 FAIL；但 publish block 一定不能发布。

## 10. 修复后重跑规则

任何内容修复都不能只局部改完直接发布。凡是影响推理链、事实、表达、HTML 的修复，都必须重跑对应下游门禁。

硬规则：

```json
{
  "content_changed": true,
  "html_stale": true,
  "must_rerender_html": true,
  "must_rerun_gates": ["G6", "G7", "G8"]
}
```

任何 Markdown 内容修复都会使已有 HTML 失效。不能复用旧 HTML。

示例：

| repair_target | 必须重跑 |
| --- | --- |
| `rewrite_8q_reasoning` | G3、G5、rubric_scoring、G6、G7、G8 |
| `supplement_sources` | G1、G4、G5、rubric_scoring、G6、G7、G8 |
| `repair_html_renderer` | G6、G7、G8 |
| `replace_case` | G1-G8 全链路 |

## 11. Reviewer Output Validator

评审者自身也必须被校验。评审无效时不能进入发布判断。

必须校验：

- 必填字段存在。
- score 在 0-max 范围内。
- `final_score` 符合 cap 和扣分公式。
- `evidence_sufficiency` 是枚举值。
- `decision_state` 是枚举值。
- S 级 FAIL 正确触发 publish block。
- REVIEW 必须带 repair_action。
- 未满分必须带 why_not_higher。
- Claim Evidence Map 必须有 source object。

如果 reviewer 输出无效：

- 不能使用该 reviewer 分数。
- 必须重新生成 reviewer 输出。
- 连续 2 次 reviewer 输出无效，触发 `USER_REVIEW_REQUIRED`。

## 12. Calibration Tests

校准不是“看看效果”，而是自动断言 Rubric 是否有效。

四类 fixture：

- hard_fail：应直接失败或发布阻断。
- soft_repair：应 REVIEW、REWRITE_MODULE 或 PASS_WITH_MINOR_REPAIR。
- good_pass：目标好样本应 PASS。
- human_preference：需要用户本人裁决。

V3/V6/V7 使用方式：

- V3 是目标内容质量样本，期望 PASS，允许最多 2 个轻微修复，不允许 S 级失败。
- V6 是目标 HTML + 内容完整样本，期望 PASS，不允许 HTML 丢内容。
- V7 是失败样本，必须触发 `EMPTY_8Q_REASONING`、`DISCONNECTED_8Q_CHAIN` 或 `BOILERPLATE_REASONING`，不得发布。
- 新闻摘要样本必须触发 global cap 70，不能 PASS。
- 虚高自评样本必须触发 `SELF_REVIEW_INFLATION` 或 `REVIEW_EVIDENCE_INVALID`。

Rubric 既要 bad sample fail，也要 good sample pass with explanation。否则它只是“什么都拦”的不可用治理。

## 13. Validator / AI Reviewer / Human 边界

检查项必须标注 check_type。

| check_type | 适合检查 |
| --- | --- |
| machine_check | 模块是否存在、字段是否存在、字段是否为空、HTML 是否丢核心内容、分数公式是否一致 |
| heuristic_check | 高重复、套话密度、来源对象是否缺字段 |
| llm_review | 是否形成推理链、方法是否产生洞察、因果机制是否完整、PREP 是否可表达 |
| human_review | 用户职业资产偏好、严重 Bad Case 是否关闭、是否符合用户个人成长目标 |

目标不是把所有事情自动化，而是不要把主观判断伪装成机器确定性。

## 14. 生成者自评不得作为放行依据

每日训练稿中的 `Insight Quality Audit`、质量审查、自评结论只能作为被审对象，不能作为放行依据。

Reviewer prompt 必须显式忽略原文自评分数。评审者必须基于原文证据、来源、推理链和输出结构独立判断。

如果原文自评高分但独立评审低分：

- 记录 `SELF_REVIEW_INFLATION`。
- 不得发布。
- 进入 reviewer prompt 和 calibration set 回流。

## 15. 最终放行定义

每日内容只有同时满足以下条件，才允许发布：

1. 三个 deep case 全部独立 PASS。
2. 每个 case 独立满足账户通过线和总分通过线。
3. 无 S 级阻断项。
4. 无一票否决项。
5. reviewer output valid。
6. G6/G7/G8 全部 PASS。
7. 当前 HTML 不是 stale。
8. 未触发用户人工裁决。

最终目标：

```text
坏样本必拦；
好样本能过；
临界样本会复审；
修复后会复测；
评审无效会重跑；
Case 之间不能互相补偿；
自评不能诱导放行；
HTML 丢内容不能发布。
```
