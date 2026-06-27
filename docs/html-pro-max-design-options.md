# Hermes HTML Pro Max Design Options

## 1. Decision Context

Current content layer has passed minimum stability verification. The next question is not "how to make the HTML prettier", but:

```text
What reading experience best trains P7+ Insight, expression, and reusable product-thinking assets?
```

The design must serve Hermes' core loop:

```text
看见 case -> 快速建立认知 -> 看见核心 Insight -> 理解推导过程 -> 学会表达 -> 沉淀资产 -> 后续复习
```

## 2. Decision Criteria

Use these criteria to compare design directions.

| 维度 | 问题 | 权重建议 |
| --- | --- | ---: |
| Insight 清晰度 | 是否能第一眼看懂每个 case 的本质判断？ | 20 |
| 深度推理承载 | 是否能完整承载方法、8问、反面论证、边界条件？ | 20 |
| 表达训练价值 | 是否能帮助用户面试 / 汇报 / 讨论时讲出来？ | 18 |
| 资产化能力 | 是否能把 case 变成可复用 Pattern / Asset Card？ | 15 |
| 阅读负担控制 | 是否能降低长文压力，而不牺牲信息质量？ | 12 |
| 来源可信感 | 是否让事实等级、来源链路、待验证假设清楚？ | 8 |
| 实现复杂度 | 是否适合在当前 renderer 上稳定实现？ | 7 |

Total: 100.

## 3. Option A: Executive Insight Brief

### Core Idea

把每日训练设计成一份高密度 executive briefing。第一屏直接给出：

- 今日 3 个 deep case
- 每个 case 的一句话 Insight
- 最高价值 Pattern
- 分数与风险
- 做 / 不做 / 先验证

### Information Architecture

```text
Daily Brief
-> Case Insight Cards
-> Why These Cases
-> Source Confidence
-> Deep Case Details
-> Asset Cards
```

### Best For

- 快速知道今天值不值得读。
- 面试前快速复习。
- 从大量内容中抓核心判断。

### Strengths

- 第一屏价值很强。
- 阅读压力低。
- 很适合每日默认打开。
- 能强化“结论先行”。

### Weaknesses

- 可能让用户只看结论，不看推导。
- 8 问和分析方法容易被藏深。
- 对“刻意训练思维过程”的支持不够强。

### Risk

如果执行过头，会把 Hermes 变回“高质量新闻摘要”，背离训练深度。

### Score

| 维度 | 分数 | 说明 |
| --- | ---: | --- |
| Insight 清晰度 | 5 | 第一屏最强。 |
| 深度推理承载 | 3 | 深度内容会变成次级层。 |
| 表达训练价值 | 4 | 适合提炼口播，但不一定训练推导。 |
| 资产化能力 | 3 | Asset 可展示，但不是主线。 |
| 阅读负担控制 | 5 | 最轻。 |
| 来源可信感 | 4 | Source strip 容易做清楚。 |
| 实现复杂度 | 4 | 当前 renderer 可较快升级。 |

Weighted score: 82 / 100.

## 4. Option B: Deep Reasoning Workbook

### Core Idea

把 HTML 设计成“P7+ 思维训练工作簿”。重点不是快看，而是让用户一步步看见：

```text
事实 -> 方法 -> 追问 -> 推导 -> 反驳 -> 取舍 -> 表达
```

### Information Architecture

```text
Case Workspace
-> Insight Board
-> Evidence Layer
-> Method Workbench
-> P7+ Deep Questions
-> 8-Question Timeline
-> Mechanism / System / Counterargument
-> Final Judgment
-> Expression Practice
-> Asset Card
```

### Best For

- 深度学习 P7+ 思考方式。
- 理解“结论是怎么推出来的”。
- 训练用户自己下次也能这么分析。

### Strengths

- 最贴合 Hermes 的核心训练目标。
- 对 8 问、6 层、分析方法最友好。
- 能把思考过程显性化。
- 最能保护内容深度。

### Weaknesses

- 初看会重。
- 页面需要很强的折叠、导航和进度设计。
- 如果视觉层不克制，会显得复杂。

### Risk

如果没有好的 overview，用户会被长文压住，打开后不知道先看哪里。

### Score

| 维度 | 分数 | 说明 |
| --- | ---: | --- |
| Insight 清晰度 | 4 | 需要配 Insight Board 才强。 |
| 深度推理承载 | 5 | 最强。 |
| 表达训练价值 | 4 | 有完整推导基础。 |
| 资产化能力 | 4 | 能解释 Pattern 来源。 |
| 阅读负担控制 | 3 | 需要交互降低负担。 |
| 来源可信感 | 5 | Evidence Layer 很适合做清楚。 |
| 实现复杂度 | 3 | 需要更细的解析和组件。 |

Weighted score: 86 / 100.

## 5. Option C: Interview Rehearsal Cockpit

### Core Idea

把 HTML 设计成“表达训练驾驶舱”。每个 case 的重点是：

- 2 分钟表达
- PREP
- SCQA
- 被追问时如何回答
- 记忆点
- 可迁移面试题

### Information Architecture

```text
Case Summary
-> Speaking Version
-> PREP
-> SCQA
-> Follow-up Q&A
-> Evidence Backup
-> Asset Card
```

### Best For

- 面试前演练。
- 汇报前准备。
- 把深度思考变成可讲的话。

### Strengths

- 高度贴合用户“我要能跟别人说出来”的目标。
- 能直接提升表达复用。
- 可做成练习模式。

### Weaknesses

- 容易弱化分析过程。
- 用户可能背答案，而不是训练思考。
- 对来源和方法工作台承载不足。

### Risk

如果它成为默认体验，会让 Hermes 偏向“话术库”，不是“判断力训练系统”。

### Score

| 维度 | 分数 | 说明 |
| --- | ---: | --- |
| Insight 清晰度 | 4 | 口播表达清楚。 |
| 深度推理承载 | 3 | 推理可能被压到后面。 |
| 表达训练价值 | 5 | 最强。 |
| 资产化能力 | 4 | 面试题迁移强。 |
| 阅读负担控制 | 4 | 很容易读。 |
| 来源可信感 | 3 | 不是主线。 |
| 实现复杂度 | 4 | tabs / cards 即可实现。 |

Weighted score: 81 / 100.

## 6. Option D: Knowledge Asset OS

### Core Idea

把 HTML 设计成“案例资产库”。重点不是当天读完，而是沉淀：

- Case Asset Card
- reusable Pattern
- Watchlist
- review priority
- migration to projects
- interview question mapping

### Information Architecture

```text
Asset Dashboard
-> Pattern Library
-> Case Asset Cards
-> Watchlist
-> Review Queue
-> Full Analysis
```

### Best For

- 长期积累个人案例库。
- 面试素材库。
- 项目方法论沉淀。
- 复习和遗忘曲线。

### Strengths

- 最贴合“个人职业壁垒”。
- 能把每日训练变成复利资产。
- 很适合后续做 Notion / Obsidian / local knowledge base。

### Weaknesses

- 不适合作为每日首次阅读默认界面。
- 当天 case 的深度推理过程可能被后置。
- 实现上需要更强的数据抽取。

### Risk

如果过早做成资产库，会跳过“今天如何学会思考”的过程。

### Score

| 维度 | 分数 | 说明 |
| --- | ---: | --- |
| Insight 清晰度 | 3 | 更偏长期资产。 |
| 深度推理承载 | 4 | 可链接回原文，但不是主体验。 |
| 表达训练价值 | 4 | 面试迁移强。 |
| 资产化能力 | 5 | 最强。 |
| 阅读负担控制 | 4 | 资产卡轻量。 |
| 来源可信感 | 3 | 需要额外设计。 |
| 实现复杂度 | 2 | 需要结构化抽取和跨天索引。 |

Weighted score: 78 / 100.

## 7. Option E: Hybrid Insight Learning Workspace

### Core Idea

把 A/B/C/D 合并成一个分层体验：

```text
默认先看 Executive Insight Brief
进入 case 后是 Deep Reasoning Workbook
表达区使用 Interview Rehearsal Cockpit
结尾沉淀 Knowledge Asset Card
```

This is not four products. It is one workflow with four reading modes:

- Scan
- Deep Read
- Rehearse
- Asset

### Information Architecture

```text
Daily Overview
-> 3 Case Insight Cards
-> Case Workspace
   -> Insight Board
   -> Evidence
   -> Method Workbench
   -> P7+ Questions
   -> 8Q Timeline
   -> Mechanism / System / Counterargument
   -> Expression Tabs
   -> Asset Card
-> Practice And Review
```

### Best For

- 当前 Hermes 的完整目标。
- 同时服务理解、深读、表达、沉淀。
- 未来扩展到每日默认 HTML。

### Strengths

- 最平衡。
- 不牺牲深度。
- 默认阅读负担可控。
- 支持用户不同场景：今天学、面试前讲、之后复习。

### Weaknesses

- 设计和实现复杂度最高。
- 需要非常清晰的组件边界。
- 第一版必须克制，不能一次做太多交互。

### Risk

如果直接做 full version，容易变复杂。需要先做 MVP：

```text
Daily Overview + Case Insight Cards + Case Workspace + Expression Tabs + Asset Panel
```

### Score

| 维度 | 分数 | 说明 |
| --- | ---: | --- |
| Insight 清晰度 | 5 | Overview + Insight Cards 解决。 |
| 深度推理承载 | 5 | Workbook 保留完整深度。 |
| 表达训练价值 | 5 | Rehearsal cockpit 解决。 |
| 资产化能力 | 5 | Asset panel 解决。 |
| 阅读负担控制 | 4 | 需要好的折叠和模式切换。 |
| 来源可信感 | 5 | Evidence layer 可清晰呈现。 |
| 实现复杂度 | 2 | 复杂，需要分阶段。 |

Weighted score: 93 / 100.

## 8. Evaluation Matrix

| 方案 | Insight 清晰度 | 深度推理承载 | 表达训练价值 | 资产化能力 | 阅读负担控制 | 来源可信感 | 实现复杂度 | 综合判断 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| A Executive Insight Brief | 5 | 3 | 4 | 3 | 5 | 4 | 4 | 快速好读，但深度训练不足 |
| B Deep Reasoning Workbook | 4 | 5 | 4 | 4 | 3 | 5 | 3 | 最贴近思维训练，但需要强导航 |
| C Interview Rehearsal Cockpit | 4 | 3 | 5 | 4 | 4 | 3 | 4 | 表达最强，但可能变话术库 |
| D Knowledge Asset OS | 3 | 4 | 4 | 5 | 4 | 3 | 2 | 长期价值强，但不适合作为默认首屏 |
| E Hybrid Insight Learning Workspace | 5 | 5 | 5 | 5 | 4 | 5 | 2 | 最符合 Hermes 全目标，建议分阶段实现 |

## 9. Recommendation

Recommended direction:

```text
Choose Option E as the final product direction,
but implement it in the order A -> B -> C -> D.
```

This means:

1. First build the Executive Insight Brief so the page immediately becomes easier to read.
2. Then build the Deep Reasoning Workbook to preserve Hermes' core training value.
3. Then build the Rehearsal Cockpit to serve interview / discussion expression.
4. Finally build Asset OS features after daily HTML is stable.

## 10. Decision Questions For User

Before implementation, align on these decisions:

### Decision 1: What should be the default first-screen priority?

Option 1:

```text
Insight first: show today's 3 case cards and core judgments.
```

Option 2:

```text
Learning path first: show how to read and train through the cases.
```

Recommendation: Option 1.

Reason: The user needs fast cognitive entry before deep reading.

### Decision 2: What should be the default case state?

Option 1:

```text
All cases show Insight Board, deeper sections collapsed.
```

Option 2:

```text
Only Case A open, Case B/C collapsed.
```

Option 3:

```text
All cases fully open.
```

Recommendation: Option 1.

Reason: It avoids Case B/C becoming invisible while still controlling reading load.

### Decision 3: Should PREP / SCQA be visible by default?

Option 1:

```text
Show as tabs inside each case.
```

Option 2:

```text
Hide under Rehearsal mode.
```

Recommendation: Option 1 for desktop, Option 2 for mobile.

Reason: Expression is a core user goal, but mobile needs density control.

### Decision 4: Should Asset Cards appear near the end of each case or in a separate Asset mode?

Option 1:

```text
Keep at end of each case.
```

Option 2:

```text
Also summarize all Asset Cards in a daily Asset section.
```

Recommendation: Option 2.

Reason: It preserves context and also helps long-term review.

### Decision 5: How much visual polish is appropriate?

Option 1:

```text
Professional minimalist reading workspace.
```

Option 2:

```text
AI-native dashboard with stronger visual effects.
```

Option 3:

```text
Editorial long-form reading page.
```

Recommendation: Option 1.

Reason: Hermes is a serious training product, not a marketing artifact or visual demo.

## 11. MVP Proposal

The first Pro Max prototype should include only:

1. Daily overview.
2. Three case insight cards.
3. Source status strip.
4. Case workspace with:
   - Insight Board open.
   - Evidence collapsed.
   - Method Workbench collapsed.
   - 8Q timeline collapsed.
   - Expression tabs visible.
   - Asset Card panel visible.
5. Left nav and mobile case tabs.

Do not include yet:

- cross-day asset database
- search
- copy/export
- self-scoring after rehearsal
- Notion/Obsidian export
- animated transitions beyond simple expand/collapse

## 12. Final Position

The best direction is:

```text
Hermes HTML Pro Max = Insight-first daily reading workspace + deep reasoning workbook + expression rehearsal + asset capture
```

This matches the user's goal:

- content depth remains intact
- reading burden becomes manageable
- thinking process is visible
- expression practice is explicit
- case output becomes reusable career asset

Implementation should start from Option E MVP, not from visual styling alone.
