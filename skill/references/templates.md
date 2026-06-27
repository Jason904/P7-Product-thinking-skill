# Hermes Output Templates

Use these templates for daily training, single-case training, answer diagnosis, and asset capture.

## 每日训练模式

### Daily Artifact Contract

Daily mode should produce a dated folder:

```text
outputs/daily-training/YYYY-MM-DD/
```

Save the full Markdown first, validate it with `scripts/validate_hermes_output.py`, render the matching reader HTML file with `scripts/render_training_reader_html.py`, then validate the rendered page with `scripts/validate_training_reader_html.py`. Use `scripts/render_training_html.py` only for legacy compatibility checks. The Markdown remains the source of truth. The HTML is the reading surface: it may add navigation, folding, tables, source badges, and visual hierarchy, but it must not delete or thin the reasoning content.

Important: Markdown validation proves the source structure. Reader HTML validation proves that 8 问 reasoning fields and other required reasoning content survived rendering. Neither replaces human Insight review.

When the user asks for daily training, the chat reply should contain only the HTML link after artifacts are generated and validated. Include extra explanation only when the user asks for logs, debugging, or comparison.

### HTML Reader Redesign Contract

Before linking the daily HTML, run an existing-project redesign pass:

- Audit the current page first: navigation friction, table of contents usability, title/body distinction, case block rhythm, typography, whitespace, mobile layout, horizontal overflow, touch target size, and visual fatigue.
- Preserve the information architecture: daily folder, source status, candidate pool, Case A/B/C order, anchors, tables, and complete Markdown reasoning.
- Upgrade the reading interface: use clear headings, grouped navigation, active states, readable line length, chunked sections, mobile-first controls, and interaction that serves reading rather than decoration.
- If a design issue will repeat every day, update the renderer or template instead of hand-editing only one HTML file.
- If `redesign-existing-projects` and `design-taste-frontend` are available, use them together for the audit and redesign standard.
- Run `scripts/validate_training_reader_html.py` after rendering and before sharing the link. Empty 8 问 cards or missing field content are release blockers.
- Verify desktop and mobile rendering before reporting success. The page should have no horizontal overflow and should not rely on scroll-jank patterns such as `window.addEventListener('scroll')`.

### Daily Output Contract Lock

Daily mode must use the exact section headings and table headers below.

Do not paraphrase, translate, rename, omit, or reorder required headings.

Required daily headings:

```text
## 零、来源通道使用情况
## 一、今日候选 case 池 + Case Selection Score
## 二、今日深度 case 选择理由
## 三、今日雷达简报
## 四、今日 3 个深度 case
## 五、今日自主训练题
## 六、旧 case 复现 / 遗忘曲线回顾
## 七、今日训练复盘
```

Required source-channel table header:

```text
| 来源通道 | 状态 | 用途 | 限制与降级处理 |
```

Required candidate-pool table header:

```text
| Case | 类型 | 来源 | 事实等级 | 相关性 | 信号强度 | 训练价值 | 可验证性 | 资产化价值 | 总分 | 处理方式 |
```

Required radar brief table header:

```text
| 标题 | 类型 | 一句话结论 | 为什么值得看 | 链接 | 后续动作 |
```

Required Quality Review Rubric table header:

```text
| 维度 | 分数 1-5 | 简评 | 下一步如何补强 |
```

Do not change:

- `case` to `案例`
- `一句话结论` to `一句话判断`
- `旧 case 复现` to `旧案例复现`
- `今日 3 个深度 case` to `今日 3 个深度案例`
- `【Case Asset Card】` to `【Case Asset Card 简版】`

If any required heading, table header, or field name is changed, the output should be treated as structurally invalid.

### 零、来源通道使用情况

Record all required source attempts before selecting cases. If a channel is unavailable, name the incomplete information, downgrade affected claims to `待核验` or `待验证假设`, and state whether those claims can support final judgment.

| 来源通道 | 状态 | 用途 | 限制与降级处理 |
| --- | --- | --- | --- |
| Search API / Web Search | 已使用 / 不可用 | | |
| AI HOT | 已使用 / 不可用 | | |
| GitHub / Open-source | 已使用 / 不可用 | | |

Keep this validator-compatible header. Make the existing narrative cells auditable:

- In `用途`, record the `实际调用 / 查询词` and how the result affected candidate discovery.
- In `限制与降级处理`, record `是否回原文核验`, which original URL or primary source was checked, and which signals remain unverified.
- Explicitly list `仍待核验的信号`; do not imply that an inaccessible source had no signals.
- For AI HOT, distinguish the LLM-generated summary from the original source reached through its `url` field.

### 一、今日候选 case 池 + Case Selection Score

Generate 8-13 candidates across AI hotspots, product cases, industry change, competitor moves, user/business problems, interview prompts, business trends, AI Eval/Gate, Agent/Workflow/Skill, GitHub/open-source signals, 3D AI, AI psychology, and the user's projects.

| Case | 类型 | 来源 | 事实等级 | 相关性 | 信号强度 | 训练价值 | 可验证性 | 资产化价值 | 总分 | 处理方式 |
| ---- | ---- | ---- | -------- | ------ | -------- | -------- | -------- | ---------- | ---- | -------- |
|      |      |      |          |        |          |          |          |            |      |          |

### Case Selection Score 阈值说明

| 总分 | 默认处理方式 | 说明 |
| ---: | --- | --- |
| 21-25 | 深度分析候选 | 优先进入 Case A / B / C 深度选择池 |
| 17-20 | 雷达简报 / Watchlist | 有价值，但不一定适合当天深度分析 |
| 13-16 | 轻量观察 | 只保留一句话判断，除非与用户项目高度相关 |
| 12 以下 | 暂不处理 | 默认不进入训练内容 |

注意：

- 总分最高不自动入选。
- 必须保证 Case A / B / C 三类训练目标均衡。
- 高热度但低可验证性的 case 应降级为 Watchlist。
- 热度一般但训练价值 / 资产化价值高的 case 可以优先进入深度分析。

### 二、今日深度 case 选择理由

```text
【今日深度 case 选择理由】

Case A：
选择原因：
训练目标：
没有选择更热 case 的原因：

Case B：
选择原因：
训练目标：
没有选择更热 case 的原因：

Case C：
选择原因：
训练目标：
没有选择更热 case 的原因：
```

### 三、今日雷达简报

Use for valuable signals that do not enter deep analysis.

| 标题 | 类型 | 一句话结论 | 为什么值得看 | 链接 | 后续动作 |
| ---- | ---- | ---------- | ------------ | ---- | -------- |
|      |      |            |              |      |          |

### 四、今日 3 个深度 case

Daily mode requires exactly 3 complete deep cases:

- Case A：外部变化类
- Case B：产品 / 商业 / 开源趋势类
- Case C：个人壁垒类

Each of the 3 deep cases must use the full single-case flow below.

Do not compress Case B or Case C into a summary.

Do not write:

- `精简版`
- `简版`
- `核心判断版`
- `Case Asset Card 简版`
- `因篇幅控制，只做简版`
- `因篇幅控制，聚焦核心`
- `以下为简要分析`

If the output is long, shorten the text inside each subsection, but keep every required subsection and field.

For each deep case, output the following full structure:

1. Case 背景与训练目标
2. Fact Confidence Table
3. P6+ 第一反应提醒
4. V3.1 Insight 总览
5. 异常信号
6. V3.1 分析方法工作台
7. P7+ 追问深答
8. 8 问显性推理
9. 分析方法总表
10. 底层矛盾与因果机制
11. 系统关系与价值迁移
12. 反面论证与边界条件
13. 6 层结构化总结
14. 最终判断与取舍
15. P7+ 面试 / 汇报表达版本
16. Insight Quality Audit
17. 训练复盘
18. Case Asset Card

Before finishing each deep case, check that `【Case Asset Card】` includes these exact fields:

```text
Case 名称：
所属方向：
一句话现象：
一句话本质：
核心矛盾：
关键系统关系：
价值流向：
做 / 不做 / 先验证：
可复用 Pattern：
可迁移到我的哪个项目：
可迁移到哪类面试题：
2 分钟表达版本：
未来 Watchlist：
关注对象：
关注指标：
Watchlist 状态：
资产等级：
资产等级说明：
复习优先级：
```

Do not use `【Case Asset Card 简版】`.

If facts are insufficient for a selected deep case, still output every required section and mark missing information as `待验证假设`.

V3.1 daily deep cases must be Insight-level. Reading burden is not a reason to thin Case B or Case C. HTML can later hide or fold sections, but Markdown must preserve reasoning depth.

### 五、今日自主训练题

Pause here and do not provide the answer until the user responds.

```text
【今日自主训练题】

Case：
必要事实材料：

请你先回答 8 问：
1. 谁？
2. 在哪？
3. 损失什么？
4. 想得到什么？
5. 为什么卡住？
6. 谁共同作用？
7. 未来怎么变？
8. 价值流向哪里？

先不要急着写方案。
你答完后，我会从 P6+ / P7 / P7+ 的角度帮你诊断。
```

### 六、旧 case 复现 / 遗忘曲线回顾

Use available history if present. If no old cases exist, generate a Pattern recall prompt.

- D0: full new case learning.
- D1: restate yesterday's case in one sentence each for phenomenon, essence, opportunity, do / don't / validate-first.
- D3: redo the 8 问 from memory.
- D7: turn the case into a 2-minute interview answer.
- D14: abstract the reusable Pattern.

### 七、今日训练复盘

Include:

- 今天主要训练了什么能力
- 今天最重要的 P7+ 思维动作
- 今天最容易犯的 P6+ 错误
- 今天沉淀了哪些 Case Asset Card
- 哪些进入 Watchlist
- 明天建议复习什么

### Quality Review Rubric

请对今天 3 个深度 case 做 1-5 分质量自评。

| 维度 | 分数 1-5 | 简评 | 下一步如何补强 |
| --- | ---: | --- | --- |
| 事实可靠性 | | | |
| 本质抽象深度 | | | |
| 系统关系清晰度 | | | |
| 趋势推演可信度 | | | |
| 机会判断质量 | | | |
| 取舍明确度 | | | |
| 验证方案可执行性 | | | |
| Case Asset Card 可复用度 | | | |

规则：

- 低于 4 分的项，必须写具体的`下一步如何补强`。
- 这个 Rubric 用来检查推理质量，不替代 validator。
- Validator 检查结构；Quality Review Rubric 检查思考质量和资产化价值。

Additional guardrails:

- If any deep case is summarized instead of fully analyzed, `本质抽象深度`, `系统关系清晰度`, and `Case Asset Card 可复用度` cannot exceed 3.
- If fewer than 3 complete `【Case Asset Card】` sections are produced, `Case Asset Card 可复用度` cannot exceed 3.
- If any Case Asset Card misses required fields, `Case Asset Card 可复用度` cannot exceed 3.
- If the output would fail validator due to missing required headings or table headers, `Case Asset Card 可复用度` cannot exceed 3.
- If any C-level or D-level source is used to support final judgment, `事实可靠性` cannot exceed 3.
- If any required source channel is unavailable and the limitation is not explained, `事实可靠性` cannot exceed 3.
- The Quality Review Rubric must identify structural incompleteness honestly. It should not claim 4 or 5 points when required sections are missing.
- Quality Review Rubric is not a self-praise section; it must identify what is incomplete and how to fix it.

## Failure Feedback Record Template

When a severe regression is found, add a record to `references/failure-cases.md` using this exact structure:

```text
## <失败标题>

【失败编号】

【问题现象】

【用户影响】

【根因归类】

【根因判断】

【回流动作】

【规则回流】

【测试回流】

【门禁处理】

【失败处理策略】

【复测证据】

【验收状态】

【下次遇到同类问题】
```

Rules:

- A severe failure cannot be closed by editing only the daily Markdown or HTML artifact.
- `【回流动作】` must say which durable surface changed: skill rule, framework, template, validator, renderer, or test.
- `【测试回流】` must name at least one regression test or verification command.
- `【复测证据】` must record PASS / FAIL status for the relevant commands.
- Run `python3 scripts/validate_failure_feedback.py references/failure-cases.md` before marking the failure closed.

## 单 case 训练模式

### 1. Case 背景与训练目标

```text
【Case】

【类型】

【背景事实】

已确认事实：
-

行业观点：
-

个人推断：
-

待验证假设：
-

【信息来源】

【为什么值得分析】

【本次训练目标】
```

### 2. Fact Confidence Table

| 事实 | 来源 | 事实等级 | 是否可用于最终判断 | 是否需要继续核验 |
| ---- | ---- | -------- | ------------------ | ---------------- |
|      |      |          |                    |                  |

Fact level rules:

- A level requires an official or primary source.
- A-level sources include official announcement, official documentation, product page, release notes, GitHub repo, paper original, API documentation, or company official blog.
- B level can include authoritative media, founder/public executive statements, official demo, credible interviews, or reputable secondary reporting.
- C level includes AI HOT summaries, community discussion, blogger interpretation, 公众号文章, secondary analysis, user experience reports, or unofficial evaluation.
- D level includes unverified rumors, screenshots, anonymous claims, group-chat claims, or claims without source.

Original-source verification does not automatically upgrade a claim to A level.

If AI HOT links to a 公众号文章, blogger post, newsletter, media article, community post, or user experience report, the claim remains B/C depending on credibility, not A.

AI HOT summaries are always C-level signals until the underlying claim is verified through an official or primary source.

Unknown rollout scope, unconfirmed user numbers, roadmap claims, unreleased capabilities, pricing claims, funding claims, and company-strategy claims must remain `待验证假设` unless supported by A/B-level evidence.

C-level facts can guide candidate selection, radar brief, or Watchlist, but cannot independently support final judgment.

D-level facts cannot support final judgment.

### 3. P6+ 第一反应提醒

```text
【P6+ 第一反应】
一个执行型产品经理可能会直接想：

【这个思路对在哪里】
它有价值的地方是：

【这个思路为什么不够】
它的问题不是错，而是太早进入：

【P7+ 刹车动作】
先不问“怎么做”，而要先问：
```

### 4. V3.1 Insight Layer

Each deep case must include these sections before or around the 8 问. They are mandatory in daily mode and recommended in single-case mode.

```text
【V3.1 Insight 总览】

一句话 Insight：

核心判断：

行动取舍：
- 做：
- 不做：
- 先验证：

【异常信号】

【V3.1 分析方法工作台】

| 分析方法 | 为什么用 | 拆解维度 | 关键发现 | 支撑的 Insight |
| --- | --- | --- | --- | --- |

【P7+ 追问深答】

追问：
深度回答：
推导依据：
可能反驳：
回应反驳：
阶段结论：
对最终判断的影响：

【底层矛盾与因果机制】

【系统关系与价值迁移】

【反面论证与边界条件】
```

Rules:

- Do not list P7+ questions without answers.
- Each major claim should follow `论点 → 论据 → 推导 → 可能反驳 → 回应反驳 → 小结论`.
- Use analysis methods to generate insight, not as labels. Omit any method that does not strengthen the final insight.
- Method count is not fixed. Quality is more important than quantity.

### 4.1 Insight Quality Audit

Every deep case must include a detailed audit after the expression section and before training review.

```text
【Insight Quality Audit】

核心 Insight：

评分表：

| 一级维度 | 子项 | 分值 | 得分 | 证据 | 扣分原因 | 补强动作 |
| --- | --- | ---: | ---: | --- | --- | --- |
| 思考深度 | 问题重构 | 8 | | | | |
| 思考深度 | 底层矛盾 | 8 | | | | |
| 思考深度 | 因果机制 | 8 | | | | |
| 思考深度 | 系统关系 | 7 | | | | |
| 思考深度 | 反面论证 / 边界条件 | 7 | | | | |
| 思考深度 | 取舍判断 | 7 | | | | |
| 内容质量 | 事实可靠性 | 7 | | | | |
| 内容质量 | 背景解释 | 5 | | | | |
| 内容质量 | 信息颗粒度 | 6 | | | | |
| 内容质量 | 方法使用质量 | 6 | | | | |
| 内容质量 | 趋势与机会信息 | 6 | | | | |
| 表达质量 | 结论先行 | 5 | | | | |
| 表达质量 | 结构清晰 | 5 | | | | |
| 表达质量 | 推导可读 | 5 | | | | |
| 表达质量 | 口头表达 | 5 | | | | |
| 表达质量 | 记忆点 | 5 | | | | |

思考深度小计：/45

内容质量小计：/30

表达质量小计：/25

总分：/100

Insight 等级：
- 5 分 Insight / training-v3 标准 / 4 分待补强 / 3 分重写 / Watchlist

是否达到 training-v3 标准：
- 是 / 否

主要扣分点：
-

下一步补强：
-
```

Rules:

- Do not output unexplained scores. Every row needs evidence, deduction reason, and improvement action.
- `training-v3 标准` requires total score >= 85, 思考深度 >= 38/45, 内容质量 >= 25/30, 表达质量 >= 21/25.
- If the case is mostly news summary, total score cannot exceed 70.
- If there is no causal mechanism, total score cannot exceed 78.
- If methods are only listed and do not produce insight, total score cannot exceed 80.
- If expression cannot be spoken in an interview or discussion, total score cannot exceed 82.

### 5. 8 问显性推理

For every question, include:

```text
目的：
分析方法：
为什么用这个方法：
推导过程：
阶段结论：
如何影响下一步：
```

Questions:

1. 谁？这个问题到底是谁的问题？区分使用者、付费者、决策者、受益者、受损者、阻碍者和影响采用者。
2. 在哪？这个问题发生在什么具体场景？区分任务、流程阶段、频率、刚需、风险和企业/个人场景。
3. 损失什么？当前谁付出了什么成本？看时间、金钱、人力、认知、沟通、决策、风险、机会和信任成本。
4. 想得到什么？用户或企业真正想获得什么收益？看更快、更便宜、更稳定、更高转化、更低风险、更强控制力。
5. 为什么卡住？真正矛盾是什么？用 `表面上是 X，本质上是 Y` 或 `某类用户想要 X，但因为 Y，导致 Z 无法达成`。
6. 谁共同作用？识别推力、阻力、瓶颈、放大器、反馈和价值控制点。
7. 未来怎么变？从系统变量推演：`现在 → 阶段 1 → 阶段 2 → 长期形态`。
8. 价值流向哪里？判断谁创造、传递、捕获价值，以及入口、数据、流程、工具链、标准、评测或治理控制点。

### 6. 分析方法总表

Only list analysis methods actually used.

| 环节 | 分析方法 | 为什么使用 | 得到什么结论 | 对后续判断的价值 |
| ---- | -------- | ---------- | ------------ | ---------------- |
|      |          |            |              |                  |

### 7. 6 层结构化总结

Use this expression order:

```text
【现象】
我观察到：

【原因】
它不是由单一因素导致，而是：
其中最核心的驱动是：

【本质】
表面上是：
本质上是：
一句话本质判断：

【系统】
关键参与因素包括：
核心系统关系是：
推力：
阻力：
瓶颈：
放大器：

【趋势】
我判断它会从：
现在 → 阶段 1 → 阶段 2 → 长期形态
长期趋势是：

【机会】
最大机会不在：
而在：
因为：
```

### 8. 最终判断与取舍

```text
【核心判断】

【应该做什么】

【不应该做什么】

【先验证什么】

【关键假设】

【验证指标】

【最小可行方案】

【长期机会】

【最大风险】
```

### 9. P7+ 面试 / 汇报表达版本

```text
如果我在面试或汇报中表达，我会这样说：

“我会从六层来看这个问题。
第一，现象上……
第二，原因上……
第三，本质上，这不是 X，而是 Y。
第四，系统上……
第五，趋势上……
第六，机会判断上……

所以我的最终判断是……
不应该优先做……
而应该先验证……”
```

Also include:

```text
【PREP 表达版本】

Point 观点：

Reason 理由：

Example 例证：

Point 回收：

【SCQA 表达版本】

Situation：

Complication：

Question：

Answer：

【被追问时的回答】
追问：
回答：
```

### 10. 训练复盘

```text
【训练能力】

【P6+ 易犯错误】

【P7+ 正确思路】

【可复用 Pattern】

【迁移方式】
```

### 10. Case Asset Card

```text
【Case Asset Card】

Case 名称：

所属方向：

一句话现象：

一句话本质：

核心矛盾：

关键系统关系：

价值流向：

做 / 不做 / 先验证：

可复用 Pattern：

可迁移到我的哪个项目：
- 可以写具体项目；如果暂时无法迁移，允许写：暂无 / 待观察。

可迁移到哪类面试题：

2 分钟表达版本：

未来 Watchlist：

关注对象：
-

关注指标：
- 产品是否继续迭代
- GitHub star / fork / release / issue 是否持续增长
- 是否出现付费客户 / 企业案例
- 是否出现竞品跟进
- 是否出现官方论文 / 技术突破
- 是否出现负面风险或监管事件

Watchlist 状态：
- 持续跟踪 / 下周复查 / 等待官方发布 / 等待 GitHub 增长验证 / 等待商业化数据 / 暂停关注

资产等级：
- A / B / C

资产等级说明：
- A：可直接进入面试素材库 / 项目方法论库 / 个人知识库核心库。
- B：可以进入知识库，但需要补事实、补数据或补案例。
- C：仅作为观察记录，暂不作为关键判断资产。

复习优先级：
- 高 / 中 / 低
```

## 用户答案诊断模式

When the user submits their own analysis, diagnose against P6+ / P7 / P7+.

```text
【你的答案当前更像】
P6+ / P7 / P7+

【做得好的地方】

【主要短板】

【如果升级到 P7，应该补什么】

【如果升级到 P7+，应该补什么】

【改写后的 P7+ 版本】
```

Diagnosis standards:

- P6+: jumps to solutions, focuses on functions/process/execution, assumes the problem is real, lacks value judgment and tradeoffs.
- P7: judges importance, separates user/business value, prioritizes, proposes validation metrics, explains do/don't.
- P7+: redefines the problem, abstracts the core contradiction, sees systems, infers trends, judges value flow, makes strategic tradeoffs, and turns the case into a reusable Pattern.
