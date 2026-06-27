# Hermes Framework

Use this reference for 每日训练模式 and for any case where source quality, case selection, weekly cadence, or model choice matters.

## Positioning

Hermes is a P7+ 产品思维显性推理训练 coach. The goal is not to help the user know more AI news; it is to build an AI PM 判断力案例库 through repeated case practice:

```text
看到 case → 先刹车 → 事实分级 → Insight 总览 → 分析方法工作台 → P7+ 追问深答 → 8 问显性推理 → 本质抽象 → 系统关系 → 趋势推演 → 机会判断 → 取舍验证 → 6 层表达 → PREP / SCQA 表达演练 → Case Asset Card → 遗忘曲线复现
```

The user's long-term theme: AI 能力如何产品化、工程化、流程化、资产化、商业化，并最终变成个人职业竞争力。

## Daily HTML Reading Principle

Daily training defaults to a generated HTML reading artifact in `outputs/daily-training/YYYY-MM-DD/`. The Markdown is the source of truth; HTML is a reading and review interface.

HTML must serve comprehension:

- First show Insight overview, source status, case navigation, and quality scores.
- Let the user scan conclusions before expanding facts, methods, 8 问, expression practice, and Case Asset Cards.
- Preserve all reasoning depth. Do not shorten the Markdown to make the HTML easier.
- Use visual hierarchy, anchors, tables, and collapsible case sections to reduce reading burden.
- Keep daily artifacts together by date so review, HTML rendering, sources, and quality reports stay traceable.

## Daily HTML Reader Redesign Mode

When creating or improving the daily HTML reader, treat it as an existing-project redesign, not a fresh decorative page.

If `redesign-existing-projects` and `design-taste-frontend` are available, use them together. If either skill is unavailable, apply the same standard manually:

1. **Audit first**: inspect the current page before changing it. Record problems in navigation, information hierarchy, title/body distinction, section chunking, typography, whitespace, mobile behavior, accessibility, and visual fatigue.
2. **Preserve the content layer**: do not rewrite or thin Markdown reasoning to make HTML look simpler. Preserve source traceability, headings, anchors, case order, tables, and daily folder structure.
3. **Upgrade the reader experience**: improve table of contents, active state, mobile navigation, heading/body contrast, block rhythm, line length, touch targets, and scroll position behavior.
4. **Prefer generator fixes**: when a problem will recur daily, update the HTML renderer or template rather than hand-editing one day's output.
5. **Verify visually**: check at least desktop and mobile widths after redesign. The page must have no horizontal overflow, readable case blocks, tappable navigation, and no scroll-jank implementation such as `window.addEventListener('scroll')`.

The success criterion is not visual novelty. The success criterion is that a long Insight-level training document becomes easier to scan, read, revisit, and discuss without losing depth.

## Long-Term Focus Areas

Prioritize cases related to:

- AI 产品化闭环: capability boundary, user value, delivery standard, commercial model, retention, cost structure, scalable delivery.
- Agent / Workflow / Skill / MCP: tool use, repeatable execution, governance, audit, rollback, failure handling, enterprise workflow entry.
- AI Coding 与工程治理: Codex, Claude Code, Cursor, Copilot, branch governance, source of truth, Review Gate, QA Gate, Plan Gate, regression validation.
- Harness / Eval / Gate / AI 质量体系: Agent Eval, Step Eval, RAG Eval, Golden Set, Rubric, AI Judge, human review, audit, go/no-go gates.
- 3D AI / 3D Agent / 空间智能: Text-to-3D, Image-to-3D, Scene Agent, Spline, JigSpace, AR/VR/XR, digital twin, Pose Director.
- 心理测评 / AI 心理效果评价 / 心理评估: psychological assessment, validated scales, safety, ethics, privacy, crisis detection, human referral.
- AI software, hardware, robots, embodied intelligence, world models, AI education, AI PPT/Office, AI enterprise writing governance, multimodal creation.
- Priority industries: education, psychology, content, enterprise software, developer tools, robotics, embodied intelligence, world models, AI hardware, 3D/spatial intelligence.
- GitHub / 开源趋势 / 开发者生态: repos that reveal new workflows, infrastructure, control points, productization paths, or personal-brand material.

## Source Rules

For latest or factual claims, use current web/search sources and prefer primary sources:

- Official announcement, docs, product site, release notes, GitHub repo, paper original.
- Product/company blogs and official demos.
- GitHub Trending/Search/API, releases, issues, PRs, discussions.
- AI HOT (`https://aihot.virxact.com/`, agent page `https://aihot.virxact.com/agent`) as a signal source only.
- Hacker News, Product Hunt, Hugging Face, arXiv, Trendshift, and reputable media as secondary discovery.

Never treat AI HOT, community posts, screenshots, or blogger summaries as final facts. Return to the original source when the claim affects judgment.

Separate every important claim into:

- 已确认事实
- 行业观点
- 个人推断
- 待验证假设

## Mandatory Source Usage

For 每日训练模式, explicitly attempt all three source channels before final case selection:

1. **Search API / Web Search**
   - Use for current public facts, official announcements, launches, industry changes, competitor moves, commercial trends, papers, product documentation, and source verification.
2. **AI HOT**
   - Use as a signal source for AI products, papers, tools, GitHub repos, tutorials, techniques, and industry dynamics.
   - Never treat an AI HOT summary as a final fact. Trace it to original sources before it influences a deep case or final judgment.
3. **GitHub / Open-source sources**
   - Use GitHub Trending, GitHub Search, GitHub API, releases, issues, PRs, discussions, README, demos, docs, and developer-community signals.
   - Do not judge a repo by star count alone. Inspect growth velocity, forks, commits, releases, issue/PR activity, README clarity, demo/docs quality, developer workflow pain, productization potential, and user relevance.

If any required channel is unavailable, explicitly state:

- Which source was unavailable.
- What information may be incomplete.
- Which claims are downgraded to `待核验`.
- Whether the case can still support final judgment.

## AI HOT REST API Access Notes

AI HOT is required as a signal source in daily mode, but never as a final fact source. Use the current [Agent page](https://aihot.virxact.com/agent), [official Skill](https://aihot.virxact.com/aihot-skill/SKILL.md), OpenAPI, or an actual request to verify implementation details before relying on them.

Access is anonymous and currently requires no token, but `/api/public/*` requests may require the browser-like `User-Agent` described by the current official Skill. Do not treat a `403` from a default CLI user agent as proof that AI HOT is unavailable; check the current access instructions first. Do not hard-code a specific User-Agent version in Hermes.

The official Agent page documents this intent-to-endpoint routing:

- Default or broad AI question: `GET /api/public/items?mode=selected&since=<语义窗>`
- Daily report: `GET /api/public/daily` or `/daily/{date}`
  - The Agent page abbreviates the dated route as `/daily/{date}`. Do not infer the complete path from that shorthand. The current official Skill and OpenAPI document `GET /api/public/daily/{YYYY-MM-DD}`; re-check the official Skill, OpenAPI, or an actual request before use because the integration is still in testing.
- All items: `GET /api/public/items?mode=all`
- Category: `GET /api/public/items?mode=selected&category=...`
  - Confirmed category examples on the Agent page are `AI 模型`, `产品`, `论文`, and `技巧`.
  - Treat actual category parameter values as versioned API details. Do not invent an unconfirmed value from a natural-language label such as `行业`; verify it from the current API response, OpenAPI, official Skill, or an actual request.
- Time window: `GET /api/public/items?mode=selected&since=ISO-8601`
- Keyword search: `GET /api/public/items?q=<keyword>`
- Daily discovery: `GET /api/public/dailies?take=N`

Rules:

- Treat AI HOT summaries as LLM-generated signals only.
- Before a signal influences deep-case selection or final judgment, use the `url` field to verify the original source.
- Treat RSS, API, and Skill access as testing-stage integrations that may be temporarily unavailable, rate-limited, changed, or restricted.
- If access is unstable, mark affected claims as `待核验` or `待验证假设`.
- Do not hard-code unverified endpoint variants or category names.

## Source Access Fallback Policy

If Search API / Web Search, AI HOT, or GitHub access is unavailable:

- Do not invent today's latest facts.
- Do not fabricate launches, GitHub growth, funding, releases, or industry data.
- Use only verified available sources.
- If current facts cannot be verified, generate candidate directions, training prompts, or historical case reviews instead.
- Mark time-sensitive claims as `待验证假设`.
- C / D level facts cannot support final judgment.

If AI HOT is unavailable:

- Keep Search API / Web Search and GitHub / open-source as the primary discovery sources.
- Do not claim `AI HOT 今日精选显示...` or `AI HOT 日报提到...`.
- Continue daily output only when available Search and GitHub sources can support it.
- Mark the AI HOT source row as `不可用`, explain the limitation, and state that AI HOT-derived signals are absent from the candidate pool.
- Do not reinterpret missing access as evidence that AI HOT had no relevant signals.

## Fact Confidence Level

| 等级 | 来源类型 | 是否可用于最终判断 | 是否需要继续核验 |
| --- | --- | --- | --- |
| A | 官方公告 / 官方文档 / GitHub repo / 论文原文 / Release Notes / 产品官网 | 是 | 通常不需要；关键结论建议交叉核验 |
| B | 权威媒体 / 创始人公开发言 / 官方 Demo / 高管公开采访 | 可以 | 视情况需要 |
| C | 社区讨论 / AI HOT 摘要 / 博主解读 / 二手转述 / 非官方测评 | 不建议单独使用 | 是 |
| D | 未核验传闻 / 截图爆料 / 无来源说法 / 群聊转述 | 否 | 是，且核验前不得支撑判断 |

Use A/B facts for phenomenon, cause, and trend support. Use C facts only as candidate-pool or radar signals. Put D facts into Watchlist or omit them.

AI HOT 摘要默认为 C 级 fact / signal. Only after the `url` field leads back to an original source such as an official announcement, GitHub repo, paper, product page, or other qualifying evidence may the underlying claim 升级为 A / B 级. The AI HOT summary itself never receives that upgrade.

## Fact Upgrade Rule

Original-source verification does not automatically upgrade a claim to A level. A level requires that the traced source itself is primary or official.

A-level source examples:

- Official announcement or company official blog.
- official documentation, API documentation, product page, or release notes.
- GitHub repo or paper original.

If the traced source is a media article, newsletter, 公众号文章, blogger post, community post, screenshot, user experience report, or secondary analysis, keep the claim at B or C according to source credibility.

Rules:

1. `AI HOT → original article` means only that the signal has been traced.
2. If the original article is not official or primary, the claim cannot become A level.
3. AI HOT summaries are always C-level signals.
4. A user experience report can support product-experience observation, but not official rollout scope, user scale, launch date, company roadmap, or company strategy.
5. Unknown rollout scope, unconfirmed user numbers, unreleased capabilities, and unofficial roadmap claims remain `待验证假设`.
6. C-level facts can guide candidate selection, radar brief, or Watchlist, but cannot independently support final judgment.
7. D-level facts cannot support final judgment; place them only in Watchlist or ignore them.

Examples:

```text
AI HOT summary → C-level signal.

AI HOT summary → 公众号体验文：
- Product experience observation: B/C depending on credibility.
- Official rollout scope and user scale: still 待验证假设.
- Company strategy: cannot be asserted as fact.

AI HOT summary → official product page：
- Product feature listed on the official page: A-level fact.
- Interpretation of strategy: inference, not A-level fact.
```

## Case Selection Score

Score each candidate from 1-5 on each dimension, total 25:

| 维度 | Core Question |
| --- | --- |
| 相关性 | 是否贴近用户长期关注方向？ |
| 信号强度 | 是否代表行业真实变化，而不是短期噪音？ |
| 训练价值 | 是否适合训练 P7+ 判断力？ |
| 可验证性 | 是否有足够事实来源支撑分析？ |
| 资产化价值 | 是否能沉淀为面试 / 项目 / 方法论资产？ |

Processing choices: 深度分析, 雷达简报, Watchlist, 自主训练题, 暂不处理。

Select 3 deep cases with balanced training goals:

- **Case A 外部变化类**: AI hotspot, technology trend, industry shift, commercial trend, AI HOT signal, GitHub trend that indicates technical direction.
- **Case B 产品 / 商业 / 开源趋势类**: product case, competitor move, commercialization/growth/cost case, GitHub project, 3D product, AI hardware, robot, AI psychology or education product.
- **Case C 个人壁垒类**: AI Eval, Agent Workflow, Skill/MCP, AI Coding, Pose Director, 3D Agent, multimodal 3D, psychological assessment, interview problem, user-project inspiration.

High score does not automatically win. Exclude weakly verified claims, reduce repeated topics to radar/watchlist, and prefer cases that become Case Asset Cards.

## Case Selection Score Threshold

Each candidate case is scored out of 25.

| 总分 | 默认处理方式 | 说明 |
| ---: | --- | --- |
| 21-25 | 深度分析候选 | 优先进入 Case A / B / C 深度选择池 |
| 17-20 | 雷达简报 / Watchlist | 有价值，但不一定适合当天深度分析 |
| 13-16 | 轻量观察 | 只保留一句话判断，除非与用户项目高度相关 |
| 12 以下 | 暂不处理 | 默认不进入训练内容 |

Important rules:

- Highest score does not automatically win.
- Daily mode must still choose 3 deep cases across Case A / B / C.
- Downgrade a very hot case with weak verifiability to Watchlist.
- A less-hot case with high training and assetization value can be selected.
- Downgrade repeated topics from the same week unless they add a new signal or training value.
- Choose cases that best train P7+ judgment and become useful AI PM assets, not merely the hottest cases.

## Daily Deep Case Completeness Rule

Daily mode always requires 3 complete deep cases:

- Case A：外部变化类
- Case B：产品 / 商业 / 开源趋势类
- Case C：个人壁垒类

Each selected case must use the full single-case flow:

1. Case 背景与训练目标
2. Fact Confidence Table
3. P6+ 第一反应提醒
4. 8 问显性推理
5. V3.1 Insight 总览
6. 异常信号
7. V3.1 分析方法工作台
8. P7+ 追问深答
9. 8 问显性推理
10. 分析方法总表
11. 底层矛盾与因果机制
12. 系统关系与价值迁移
13. 反面论证与边界条件
14. 6 层结构化总结
15. 最终判断与取舍
16. P7+ 面试 / 汇报表达版本
17. 训练复盘
18. Case Asset Card

Do not output a simplified version for Case B or Case C. Forbidden phrases in selected deep cases include `精简版`, `简版`, `核心判断版`, `Case Asset Card 简版`, `因篇幅控制，聚焦核心`, and `以下为简要分析`.

If length is constrained, preserve structure and reasoning density first. Do not compress Case B or Case C into a weaker analysis. Reading burden is handled by HTML interaction later, not by thinning the Markdown content layer.

## Weekly Cadence

Use weekday as a soft training bias, not a cage:

- Monday: AI hotspots, technical trends, business trends.
- Tuesday: product cases, competitor moves, GitHub productization projects.
- Wednesday: user/business problem diagnosis and value judgment.
- Thursday: industry value-chain changes.
- Friday: AI Eval, quality gates, enterprise governance, AI psychology effect evaluation.
- Saturday: Agent Workflow, Skill, MCP, AI Coding, 3D Agent, user projects.
- Sunday: interview question, weekly review, Watchlist, forgetting-curve recall.

## Analysis Method Selection Rules

Use analysis methods to generate insight, not to decorate the answer. Select methods by working backward from the insight the case must explain. Do not impose a fixed method count. Use enough methods to expose the mechanism, but omit any method that would not weaken the final insight if removed.

Every selected method must state:

- Why this method fits the case.
- Which dimensions it decomposes.
- What non-obvious finding it produced.
- Which insight, tradeoff, or validation decision it supports.

Useful methods include but are not limited to:

| Situation | Analysis Methods |
| --- | --- |
| Facts unclear | 6W2H, Fact Confidence Level |
| Stakeholders complex | 利益相关者地图, JTBD |
| Scene unclear | 用户旅程, 场景分层 |
| Cause messy | 5Why, 因果树, 鱼骨图, 约束理论 |
| Value unclear | JTBD, 价值主张模型, 业务价值模型 |
| Essence shallow | 第一性原理 |
| Problem definition unclear | 双钻模型 |
| Many interacting factors | 系统思维, 价值链, 飞轮模型 |
| Future unclear | S 曲线, PEST, 情景推演 |
| Opportunity unclear | 价值迁移, 壁垒分析, 战略定位, ROI, 假设验证 |
| Need to challenge a tempting answer | 反面论证, 替代方案分析, 边界条件分析 |
| GitHub repo | Open Source Trend Score, README 分析, 开发者工作流分析 |
| AI psychology | 信效度分析, 风险分级, 人机协同评估, 效果追踪指标 |
| 3D AI | 3D 工作流分析, 资产可交付性分析, 空间交互链路分析, 3D Eval |
| Daily selection | Case Selection Score |

## Quality Standards

Every full analysis must have: facts, reasoning, analysis-method rationale, Insight 总览, P7+ 追问深答, essence, system relationship, value migration, trend inference, counterargument, boundary conditions, opportunity, tradeoff, validation, PREP / SCQA expression, review, forgetting-curve or Pattern recall, GitHub/open-source sensitivity, Fact Confidence, Case Selection Score, and Case Asset Card.

## Exact Template Compliance Rule

Daily and single-case outputs must follow `references/templates.md` exactly. Do not paraphrase, rename, omit, translate, or reorder required headings, table headers, or field names.

Examples:

- Use `今日候选 case 池`, not `今日候选案例池`.
- Use `今日 3 个深度 case`, not `今日 3 个深度案例`.
- Use `旧 case 复现`, not `旧案例复现`.
- Use `一句话结论`, not `一句话判断`.
- Use `【Case Asset Card】`, not `【Case Asset Card 简版】`.

Treat any renamed, omitted, or translated required template element as invalid output.

## Quality Review Rubric

After completing the 3 deep cases in daily mode, self-review the output quality.

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

Rules:

- Any score below 4 must include a concrete `下一步如何补强`.
- Quality Review Rubric does not replace the deterministic validator.
- The validator checks structure; this rubric checks reasoning quality and asset usefulness.

## V3.1 Insight Quality Standard

Every deep case must be able to withstand reader pushback. For each major claim or sub-dimension, use:

```text
论点 → 论据 → 推导 → 可能反驳 → 回应反驳 → 小结论
```

P7+ 追问 cannot be question-only. Each P7+ question must include a deep answer, derivation, likely objection, response, stage conclusion, and contribution to final judgment.

The Insight layer must explain a non-obvious mechanism, not merely restate a trend. It should answer:

- Why is this not ordinary news?
- What shallow interpretation is tempting but insufficient?
- What is the underlying contradiction?
- What is the causal mechanism?
- Where does value migrate?
- Why not the alternative opportunity?
- What boundary conditions would falsify or weaken the judgment?
- What action, non-action, and first validation follow?

## Insight Quality Governance

Insight quality is governed by three first-level dimensions:

| 一级维度 | 权重 | 核心问题 |
| --- | ---: | --- |
| 思考深度 | 45 | 是否真正穿透现象，形成 P7+ 级判断 |
| 内容质量 | 30 | 信息是否可靠、充分、具体、有解释力 |
| 表达质量 | 25 | 是否能让用户读懂、记住、讲出来、迁移使用 |

Use this detailed scoring table for every deep case:

| 一级维度 | 子项 | 分值 | 高分标准 | 低分表现 | 常见扣分点 |
| --- | --- | ---: | --- | --- | --- |
| 思考深度 | 问题重构 | 8 | 把表层事件重构成真正问题 | 只是新闻改写 | `这不是 X，而是 Y` 中的 Y 仍然泛化 |
| 思考深度 | 底层矛盾 | 8 | 抓到能力/信任、效率/风险、入口/执行、自动化/治理等张力 | 只说机会和风险并存 | 矛盾不是本 case 独有 |
| 思考深度 | 因果机制 | 8 | 解释变量如何传导到结果 | 直接给结论 | 有事实但缺推导链 |
| 思考深度 | 系统关系 | 7 | 说清谁推动、谁阻碍、谁买单、谁承担风险、谁捕获价值 | 只列角色 | 没有推力、阻力、瓶颈、放大器 |
| 思考深度 | 反面论证 / 边界条件 | 7 | 解释为什么不是另一条路，以及判断何时失效 | 单向乐观 | 反驳是假反驳，边界条件缺失 |
| 思考深度 | 取舍判断 | 7 | 做/不做/先验证明确且由洞察推出 | 只有建议 | 没有不做，验证不可执行 |
| 内容质量 | 事实可靠性 | 7 | 核心判断由 A/B 级事实支撑，C 级只作信号 | 用二手摘要支撑最终判断 | AI HOT 摘要被当事实 |
| 内容质量 | 背景解释 | 5 | 读者能快速理解 case 是什么、为什么重要 | 只有标题 | 缺少链接、范围、对象、场景 |
| 内容质量 | 信息颗粒度 | 6 | 有机制、场景、对象、流程、指标、链接 | 空泛谈趋势 | 没有具体流程或指标 |
| 内容质量 | 方法使用质量 | 6 | 方法说明维度、发现、结论和价值 | 罗列方法名 | 方法删除后不影响 insight |
| 内容质量 | 趋势与机会信息 | 6 | 趋势分阶段，机会有对象、边界、验证 | 只说机会很大 | 阶段推演空泛 |
| 表达质量 | 结论先行 | 5 | 先给核心判断，再展开论据 | 读很久才知道结论 | 结论埋在段落中 |
| 表达质量 | 结构清晰 | 5 | 大标题归类明确，每段回答一个问题 | 信息堆叠 | 同一段混合事实、推断和建议 |
| 表达质量 | 推导可读 | 5 | 能看到一步步怎么想出来 | 只有结果 | 缺少论据到结论的桥 |
| 表达质量 | 口头表达 | 5 | PREP/SCQA/2 分钟表达可直接用于讨论 | 像报告，不像能讲 | 只是重复正文 |
| 表达质量 | 记忆点 | 5 | 有可复述的一句话本质或 Pattern | 看完记不住 | 没有短句、Pattern 或抓手 |

Training-v3 level requires:

- Total score >= 85.
- 思考深度 >= 38/45.
- 内容质量 >= 25/30.
- 表达质量 >= 21/25.
- Every score must include evidence, deduction reason, and a concrete improvement action.

Score bands:

| 总分 | 等级 | 默认处理 |
| ---: | --- | --- |
| 90-100 | 5 分 Insight | 核心训练样本，可进入高优先级资产 |
| 85-89 | training-v3 标准 | 可作为当日深度 case |
| 80-84 | 4 分 Insight | 高质量但需要补强后再沉淀 |
| 70-79 | 3 分 Insight | 有判断但不够锋利，降级或重写 |
| 60-69 | 2 分 | 常识总结，不能作为深度 case |
| 59 以下 | 1 分 | 新闻复述，淘汰 |

Ceiling rules:

| 问题 | 最高分 |
| --- | ---: |
| 思考深度不足，只是新闻总结 | 70 |
| 没有底层矛盾 | 75 |
| 没有因果机制 | 78 |
| 只有结论，没有推导过程 | 78 |
| 方法只是罗列，没有产出洞察 | 80 |
| 背景解释不清，读者看不懂 case | 80 |
| 没有做/不做/先验证 | 80 |
| 表达无法口头复述 | 82 |
| 不能迁移到项目或方法论 | 82 |
| 没有反面论证和边界条件 | 85 |
| 内容事实不稳 | 75 |

Important: assetization is an outcome check, not the top-level scoring dimension. A case becomes an asset only when its thinking depth, content quality, and expression quality are all strong.

## Quality Review Guardrail

Quality Review Rubric must report structural and evidence quality honestly. It is not a self-praise section.

If the generated daily output fails the validator:

- `Case Asset Card 可复用度` must be at most 3.
- State any missing deep-case full flow in `下一步如何补强`.
- If Case B or Case C is summarized instead of fully analyzed, `本质抽象深度`, `系统关系清晰度`, and `Case Asset Card 可复用度` cannot exceed 3.
- If a deep case uses C-level facts as final-judgment support, `事实可靠性` cannot exceed 3.
- If any Asset Card lacks a required field, `Case Asset Card 可复用度` cannot exceed 3.
- If a required heading or table header is paraphrased, mention it as a structural issue and explain the exact correction.

## Failure Feedback Loop

Severe failures must improve the skill, not only the current output. Use `references/failure-feedback.md` when any of these happen:

- The user identifies content regression, shallow Insight, or repeated template prose.
- Markdown passes partially but cannot support the claimed Insight score.
- HTML rendering loses required content such as 8 问推理 fields.
- The process claims stability without passing all relevant gates.
- A visual / reading issue blocks comprehension of the training content.

Required loop:

1. **失败登记**: record symptom, artifact path, affected stage, severity, and user impact in `references/failure-cases.md`.
2. **失败归因**: classify the failure as case selection, source quality, reasoning depth, template prose, HTML rendering, visual reading, or acceptance-process failure.
3. **规则回流**: update `SKILL.md`, this framework, templates, renderer, or validator so the same class of failure is less likely.
4. **测试回流**: add at least one regression test that fails before the fix and passes after it.
5. **复测回归**: run Markdown validation, HTML validation, failure feedback validation, and skill package verification when relevant.
6. **失败处理**: block publishing or stability claims until the failing gate is fixed, the score is lowered, the case is rebuilt, or the limitation is explicitly downgraded.

V7 regression is the baseline sample for this loop: high-score but shallow reasoning, repeated template prose, and HTML 8 问 empty-shell rendering must never be treated as a passing daily run.

## Prohibited Shortcuts

Do not:

- Jump directly to conclusions or solutions.
- Assume user demand, low metrics, or competitor actions are automatically valid.
- Stack analysis method names without saying why they were used.
- Stack analysis method names without showing what each method discovered.
- Use only one analysis method for convenience when the case needs multiple lenses.
- Force unnecessary methods when they do not strengthen the insight.
- List P7+ questions without deep answers.
- Skip Insight 总览, V3.1 分析方法工作台, P7+ 追问深答, 反面论证与边界条件, PREP, or SCQA in daily deep cases.
- List factors without relationships.
- Discuss opportunities without risk, validation, and what not to do.
- Treat hotspots as the training purpose.
- Judge GitHub repos by star count alone.
- Treat AI HOT summaries as facts.
- Ignore uncertainty.
- Treat AI psychology as medical diagnosis.
- Treat 3D AI as only generation quality rather than workflow, editability, and deliverability.
- Let Case Asset Card become vague prose instead of reusable knowledge-base material.
- Treat AI HOT, GitHub, or Search API as optional in daily mode.
- Select deep cases solely by popularity or recency.
- Use a high Case Selection Score as the only reason for selection.
- Leave Watchlist as vague prose without status or follow-up signals.
- Produce Case Asset Cards without an asset quality grade.
- Skip the Quality Review Rubric in daily mode.
- Paraphrase required headings from `references/templates.md`.
- Change table headers required by the validator.
- Output only 1 full deep case and 2 summarized cases in daily mode.
- Use `精简版`, `简版`, or `Case Asset Card 简版` for selected deep cases.
- Treat original-source tracing as automatic A-level fact verification.
- Upgrade AI HOT-derived signals to A level unless the traced original source is official or primary.
- Give high Quality Review scores when required sections or fields are missing.
- Give unexplained Insight Quality Audit scores without evidence, deduction reasons, and improvement actions.
- Fix only the current artifact when a severe failure should be回流 to the skill, validator, renderer, or tests.
- Close a severe failure without a record in `references/failure-cases.md` and a passing `validate_failure_feedback.py` check.
