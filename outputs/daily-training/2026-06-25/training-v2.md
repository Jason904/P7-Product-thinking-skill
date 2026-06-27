# Hermes P7+ 每日训练 - 2026-06-25

> 内容层 V2 说明：这一版先服务“读懂与复盘”，不是最终视觉稿。保留 validator 需要的表格和字段，同时增加候选 case 卡片、溯源链接、评分解释、分析方法展开和具体趋势阶段。`使用模型：` 是当前模板字段；阅读时请理解为 `分析方法：`。

## 零、来源通道使用情况

| 来源通道 | 状态 | 用途 | 限制与降级处理 |
| --- | --- | --- | --- |
| Search API / Web Search | 已使用 | 实际调用 / 查询词：OpenAI Codex June 2026、GitHub Agentic Workflows、Gemini 3.5 Flash computer use、Cursor Notion SDK、AI agent workflow release notes。用于核验官方公告、产品页、GitHub Changelog 和研究博客。 | 是否回原文核验：是。已核验 Google Keyword、Cursor Blog、GitHub Changelog、OpenAI 官方页面、Google Research、GitHub Release。仍待核验的信号：部分媒体和 AI HOT 二手摘要不进入最终判断。 |
| AI HOT | 已使用 | 实际调用 / 查询词：`/api/public/items?mode=selected&since=2026-06-24T00:00:00+08:00`。用于发现今天的高热信号：Gemini computer use、Notion + Cursor SDK、Figma Config、OpenRouter ZDR、Mistral Connectors、xAI + Interactive Brokers。 | 是否回原文核验：部分已回原文核验。AI HOT 摘要只作为 C 级信号；影响深度 case 的 Google、Cursor、GitHub 已回官方原文。仍待核验的信号：Figma、OpenRouter、部分 X 消息只进入雷达或 Watchlist。 |
| GitHub / Open-source | 已使用 | 实际调用 / 查询词：GitHub API repository search、GitHub Release、GitHub Changelog、OSSInsight Trending AI。用于识别 agent workflow、开源 agent 版本演进和开发者生态信号。 | 是否回原文核验：是。GitHub Agentic Workflows 使用 GitHub Changelog；Hermes Agent 使用 GitHub Release API。仍待核验的信号：OSSInsight 只作趋势发现，不独立支撑最终判断。 |

## 一、今日候选 case 池 + Case Selection Score

| Case | 类型 | 来源 | 事实等级 | 相关性 | 信号强度 | 训练价值 | 可验证性 | 资产化价值 | 总分 | 处理方式 |
| ---- | ---- | ---- | -------- | ------ | -------- | -------- | -------- | ---------- | ---- | -------- |
| Gemini 3.5 Flash 内置 computer use | 外部变化类 | Google Keyword 官方博客 + AI HOT | A | 5 | 5 | 5 | 5 | 4 | 24 | 深度分析 |
| Notion 使用 Cursor SDK 嵌入编码智能体 | 产品 / 商业趋势类 | Cursor Blog 官方文章 + AI HOT | A | 5 | 4 | 5 | 5 | 4 | 23 | 深度分析 |
| GitHub Agentic Workflows 公测 | 个人壁垒类 | GitHub Changelog 官方公告 | A | 5 | 5 | 5 | 5 | 5 | 25 | 深度分析 |
| OpenAI Codex role-specific plugins 与 Sites | 产品化趋势类 | OpenAI 官方公告 | A | 5 | 4 | 4 | 5 | 4 | 22 | Watchlist |
| OpenAI Codex 6 月 Changelog：goals 与 personality | AI Coding 体验类 | OpenAI Developers Changelog | A | 4 | 3 | 4 | 5 | 3 | 19 | 雷达简报 |
| NousResearch Hermes Agent v0.17.0 | GitHub / 开源趋势类 | GitHub Release API | A | 4 | 4 | 4 | 5 | 4 | 21 | Watchlist |
| Mistral Connectors 权限与 scope 控制 | Agent 治理类 | AI HOT + Mistral 官网可见标题 | B | 4 | 4 | 4 | 3 | 4 | 19 | Watchlist |
| Google Research：Thinking to recall | 研究趋势类 | Google Research Blog | A | 4 | 4 | 4 | 5 | 3 | 20 | 雷达简报 |
| xAI Grok + Interactive Brokers | 金融 AI 产品类 | xAI News + AI HOT | A | 3 | 4 | 4 | 4 | 4 | 19 | Watchlist |
| Figma Config 2026 AI canvas / workflow skill | 设计工具趋势类 | AI HOT + The Decoder 二手报道 | C | 4 | 4 | 4 | 2 | 4 | 18 | Watchlist |

### Case Selection Score 阈值说明

| 总分 | 默认处理方式 | 说明 |
| ---: | --- | --- |
| 21-25 | 深度分析候选 | 优先进入 Case A / B / C 深度选择池 |
| 17-20 | 雷达简报 / Watchlist | 有价值，但不一定适合当天深度分析 |
| 13-16 | 轻量观察 | 只保留一句话判断，除非与用户项目高度相关 |
| 12 以下 | 暂不处理 | 默认不进入训练内容 |

### 候选 case 快速认知卡片

> 阅读目的：这部分不是为了让你记住分数，而是让你快速知道“这是什么、为什么值得看、从哪里来、为什么这个处理方式”。AI HOT 精选会提高关注权重，但不会自动提高事实等级；事实等级仍以官方原文、GitHub、论文原文等 primary source 为准。

#### 候选 1：Gemini 3.5 Flash 内置 computer use

- 一句话认知：Google 将 computer use 从独立能力推进到 Gemini 3.5 Flash 的内置工具，开发者可以在 API / 企业平台里调用跨应用操作能力。
- 为什么值得看：它代表 agent 从“能调用工具”进一步靠近“能操作真实工作环境”，核心训练点是企业如何授权、约束和审计 agent。
- 来源链接：
  - AI HOT 精选：https://aihot.virxact.com/items/cmqsl6c5y042hslfu74apxkap
  - 原始来源：https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-computer-use-gemini-3-5-flash
- AI HOT 权重：高。它是今日精选，说明信号热度和编辑判断都较强。
- 事实等级：A。核心事实来自 Google 官方博客；AI HOT 摘要只作为 C 级发现信号。
- 评分解释：
  - 相关性 5：直接命中 Agent / Workflow / 企业自动化治理方向。
  - 信号强度 5：computer use 进入主模型能力层，代表能力默认化。
  - 训练价值 5：能训练“能力强不等于企业可用”的 P7+ 判断。
  - 可验证性 5：有官方原文支撑核心事实。
  - 资产化价值 4：可沉淀为 computer use 企业落地判断框架。
- 处理方式：深度分析。它适合做 Case A，因为它是外部能力边界变化。

#### 候选 2：Notion 使用 Cursor SDK 嵌入编码智能体

- 一句话认知：Notion 把 Cursor coding agent 接入文档、讨论和数据库任务，让协作空间里的需求可以直接触发工程执行。
- 为什么值得看：它不是“Notion 会写代码”，而是 agent 从独立 IDE / CLI 迁移到业务对象内部。
- 来源链接：
  - AI HOT 精选：https://aihot.virxact.com/items/cmqsjydyy03s2slfu0akeh868
  - 原始来源：https://cursor.com/blog/notion
- AI HOT 权重：高。AI HOT 将它列入今日 AI 产品精选，说明它有跨产品工作流意义。
- 事实等级：A。核心事实来自 Cursor 官方博客；Notion 侧采用数据仍待核验。
- 评分解释：
  - 相关性 5：高度贴合 AI Coding、SDK、Workflow 和协作产品。
  - 信号强度 4：不是模型突破，但显示 agent 进入 host product 的路径。
  - 训练价值 5：能训练“入口、上下文、执行、验收”四层关系判断。
  - 可验证性 5：官方文章给出清晰集成叙述。
  - 资产化价值 4：可迁移到 Hermes HTML 阅读器的“内容对象绑定操作”设计。
- 处理方式：深度分析。它适合做 Case B，因为它是产品 / 商业 / SDK 平台化趋势。

#### 候选 3：GitHub Agentic Workflows 公测

- 一句话认知：GitHub 让用户用自然语言 Markdown 定义 agent workflow，并编译到 Actions 执行系统中。
- 为什么值得看：它把 agent 从聊天和单次代码生成拉进 runner、policy、安全扫描、safe outputs 和 review gate。
- 来源链接：
  - AI HOT 精选：未进入本次 AI HOT 选中列表；由 Search / GitHub 官方源发现。
  - 原始来源：https://github.blog/changelog/2026-06-11-github-agentic-workflows-is-now-in-public-preview/
  - GitHub Next：https://github.com/githubnext/agentics
- AI HOT 权重：低。不是 AI HOT 当日精选，但官方源强、与用户项目高度相关。
- 事实等级：A。核心事实来自 GitHub 官方 Changelog 和 GitHub repo。
- 评分解释：
  - 相关性 5：直接命中 Skill / Workflow / Gate / AI Coding governance。
  - 信号强度 5：GitHub 把 agent workflow 放入 Actions 体系，平台意义强。
  - 训练价值 5：能训练“会用 agent”到“会设计治理系统”的跃迁。
  - 可验证性 5：官方公告完整。
  - 资产化价值 5：可直接迁移为 Hermes daily pipeline 方法论。
- 处理方式：深度分析。它适合做 Case C，因为它最能沉淀个人壁垒。

#### 候选 4：OpenAI Codex role-specific plugins 与 Sites

- 一句话认知：OpenAI 将 Codex 从通用 coding agent 扩展到按角色封装的工作流插件和可发布站点能力。
- 为什么值得看：它与“skill + workflow + HTML 输出”方向高度相关，能启发 Hermes 最终发布形态。
- 来源链接：
  - AI HOT 精选：未在本次 AI HOT 列表中发现。
  - 原始来源：https://openai.com/index/codex-for-every-role-tool-workflow/
- AI HOT 权重：低。非 AI HOT 当日精选，但官方来源强。
- 事实等级：A。来自 OpenAI 官方页面。
- 评分解释：
  - 相关性 5：直接关联你的 skill 合并和 HTML 发布目标。
  - 信号强度 4：产品包装变化明确，但不是单一深度 case 最佳训练对象。
  - 训练价值 4：可训练“角色化 workflow 产品化”。
  - 可验证性 5：官方可核验。
  - 资产化价值 4：可进入 Watchlist，后续服务 Hermes renderer。
- 处理方式：Watchlist。今天先不深挖，避免 3 个 case 全部集中在 Codex 生态。

#### 候选 5：OpenAI Codex 6 月 Changelog：goals 与 personality

- 一句话认知：Codex 在 6 月继续增强目标追踪、长任务协作和个性化体验。
- 为什么值得看：它和你正在使用的 Codex 工作流相关，但更偏体验迭代，不如 GitHub Agentic Workflows 适合训练治理判断。
- 来源链接：
  - AI HOT 精选：未在本次 AI HOT 列表中发现。
  - 原始来源：https://developers.openai.com/codex/changelog
- AI HOT 权重：低。非 AI HOT 当日精选。
- 事实等级：A。来自 OpenAI 官方 Changelog。
- 评分解释：
  - 相关性 4：与 Codex 使用体验相关。
  - 信号强度 3：属于连续迭代，不是结构性变化。
  - 训练价值 4：能训练“agent 协作产品体验”的判断。
  - 可验证性 5：官方可核验。
  - 资产化价值 3：更适合雷达，不适合当天深度。
- 处理方式：雷达简报。作为 Codex 使用策略信号保留。

#### 候选 6：NousResearch Hermes Agent v0.17.0

- 一句话认知：Hermes Agent 发布 v0.17.0，扩展触达渠道、后台子任务、团队控制台和 agent runtime 能力。
- 为什么值得看：它展示开源 agent 系统如何从工具扩展到团队运行系统。
- 来源链接：
  - AI HOT 精选：未在本次 AI HOT 列表中发现。
  - 原始来源：https://github.com/NousResearch/hermes-agent/releases/tag/v2026.6.19
- AI HOT 权重：低。非 AI HOT 当日精选，但 GitHub release 是 primary source。
- 事实等级：A。来自 GitHub Release。
- 评分解释：
  - 相关性 4：与 agent runtime 和个人工具系统相关。
  - 信号强度 4：release 规模较大，但仍需观察真实采用。
  - 训练价值 4：可训练开源 agent 产品化判断。
  - 可验证性 5：release 可核验。
  - 资产化价值 4：可进入工具系统 Watchlist。
- 处理方式：Watchlist。下周看 issue、PR、安装反馈后再决定是否深挖。

#### 候选 7：Mistral Connectors 权限与 scope 控制

- 一句话认知：Mistral 为 connectors 增加更多管理控制、API key scope 和多账号相关能力。
- 为什么值得看：它说明企业 agent 的连接器不只是“接得上”，还要“控得住”。
- 来源链接：
  - AI HOT 精选：https://aihot.virxact.com/items/cmqs9eic7012cslfuu3w4io4c
  - 原始来源：https://mistral.ai/news/more-control-over-connectors
- AI HOT 权重：中。AI HOT 选中，但网页抽取信息不完整，需继续核验细节。
- 事实等级：B。可见官方页面标题和产品方向，但当前样本未完整核验全文。
- 评分解释：
  - 相关性 4：贴合 enterprise connectors 和 agent governance。
  - 信号强度 4：连接器权限是企业采用关键。
  - 训练价值 4：可训练“接入能力 vs 管控能力”的判断。
  - 可验证性 3：需要补全文细节或官方 docs。
  - 资产化价值 4：适合放进治理 Watchlist。
- 处理方式：Watchlist。等补完官方细节后可升级为深度 case。

#### 候选 8：Google Research Thinking to recall

- 一句话认知：Google Research 讨论推理如何帮助 LLM 释放参数化知识。
- 为什么值得看：它可以为 Hermes 的“显性推理训练”提供研究侧支撑。
- 来源链接：
  - AI HOT 精选：https://aihot.virxact.com/items/cmqsbr8l701ndslfu2kei9qhy
  - 原始来源：https://research.google/blog/thinking-to-recall-how-reasoning-unlocks-parametric-knowledge-in-llms
- AI HOT 权重：中。AI HOT 选中，且 Google Research 是 primary source。
- 事实等级：A。来自 Google Research 官方博客。
- 评分解释：
  - 相关性 4：与 Hermes 显性推理机制有关。
  - 信号强度 4：研究发现有启发，但不是产品化事件。
  - 训练价值 4：可训练“推理为什么有用”的元认知。
  - 可验证性 5：官方研究博客可核验。
  - 资产化价值 3：适合作为理论卡片，不适合作今日深度业务 case。
- 处理方式：雷达简报。作为 Pattern 理论依据保留。

#### 候选 9：xAI Grok + Interactive Brokers

- 一句话认知：Grok 接入 Interactive Brokers，用自然语言进行组合分析、情景建模，并生成交易相关指令。
- 为什么值得看：金融是高风险 agent 场景，能训练“执行边界、确认责任、合规控制”的判断。
- 来源链接：
  - AI HOT 精选：https://aihot.virxact.com/items/cmqst0js5060tslfu7s6uxjhf
  - 原始来源：https://x.ai/news/grok-interactive-brokers
- AI HOT 权重：中。AI HOT 选中，但分数不算最高；适合 Watchlist。
- 事实等级：A。来自 xAI 官方 News。
- 评分解释：
  - 相关性 3：金融场景不是当前主线，但对高风险 agent 有启发。
  - 信号强度 4：从分析走向交易执行，信号强。
  - 训练价值 4：能训练责任、合规和人类确认。
  - 可验证性 4：官方可核验，但真实用户反馈待观察。
  - 资产化价值 4：可做高风险 agent 案例库。
- 处理方式：Watchlist。等待真实使用反馈和合规说明。

#### 候选 10：Figma Config 2026 AI canvas / workflow skill

- 一句话认知：Figma 被报道在 Config 2026 推进代码、动画、3D、shader 和 workflow skill 等画布能力。
- 为什么值得看：它和 Hermes HTML 阅读器相关：内容结构可能不只是文本，而是可操作设计对象。
- 来源链接：
  - AI HOT 精选：https://aihot.virxact.com/items/cmqsbrhhm01o1slfu2kei9qhy
  - 原始来源：https://the-decoder.com/figma-bets-on-human-judgment-at-config-2026-while-the-ai-powering-its-canvas-belongs-to-someone-else
- AI HOT 权重：高。AI HOT 分数高，但目前主要来源是二手报道。
- 事实等级：C。当前样本没有核验 Figma 官方原文，不能支撑最终判断。
- 评分解释：
  - 相关性 4：与设计工具、HTML 阅读体验和 workflow skill 有关。
  - 信号强度 4：如果官方确认，信号很强。
  - 训练价值 4：可训练“设计工具如何产品化 AI 工作流”。
  - 可验证性 2：缺官方原文，必须降级。
  - 资产化价值 4：适合观察，不适合支撑今天深度判断。
- 处理方式：Watchlist。等待 Figma 官方资料后再升级。

## 二、今日深度 case 选择理由

【今日深度 case 选择理由】

Case A：
选择原因：Gemini 3.5 Flash 把 computer use 从独立能力变成主模型内置工具，代表 agent 能力进入默认模型栈。
训练目标：训练“模型能力产品化边界”判断，识别能力、场景、安全、企业采用之间的系统关系。
没有选择更热 case 的原因：OpenAI GPT-5.5 Instant 信号更热，但今天可形成 P7+ 资产的关键不是聊天体验，而是跨应用执行能力如何被治理。

Case B：
选择原因：Notion 通过 Cursor SDK 把编码 agent 嵌入协作产品，体现 agent 从外部工具变成业务对象内部动作。
训练目标：训练“平台 SDK 如何成为他人产品能力层”的商业与产品化判断。
没有选择更热 case 的原因：Figma Config 话题更热，但可核验性较弱，且今日更适合分析已经有官方技术叙述的嵌入式 agent 案例。

Case C：
选择原因：GitHub Agentic Workflows 把自然语言任务、Actions、runner、policy、安全检查串成治理闭环，最贴合用户正在做的 skill / workflow / gate 方向。
训练目标：训练“个人壁垒如何从会用 agent 升级到会设计 agent 治理系统”。
没有选择更热 case 的原因：Hermes Agent v0.17.0 开源发布很适合观察，但更偏工具扩展；GitHub 案例更能沉淀到用户自己的 daily skill 发布系统。

## 三、今日雷达简报

| 标题 | 类型 | 一句话结论 | 为什么值得看 | 链接 | 后续动作 |
| ---- | ---- | ---------- | ------------ | ---- | -------- |
| OpenAI Codex role-specific plugins | 产品化趋势 | Codex 正从 coding tool 变成按角色封装的工作工具。 | 对“skill + app + workflow”打包方式有直接参考价值。 | https://openai.com/index/codex-for-every-role-tool-workflow/ | Watchlist：观察 product design plugin 和 Sites 如何影响 Hermes HTML 化。 |
| NousResearch Hermes Agent v0.17.0 | GitHub / 开源趋势 | 开源 agent 正把触达渠道、后台子任务和团队控制台作为增长方向。 | 可对照个人 skill 如何从单次输出升级为运行系统。 | https://github.com/NousResearch/hermes-agent/releases/tag/v2026.6.19 | 下周复查 release 后的 issue、PR、安装反馈。 |
| Google Research Thinking to recall | 研究趋势 | 推理可能帮助模型释放参数化知识，而不只是解决复杂数学题。 | 对 Hermes 的显性推理训练有理论支撑，但不是产品发布。 | https://research.google/blog/thinking-to-recall-how-reasoning-unlocks-parametric-knowledge-in-llms | 作为理论素材进入 Pattern 库。 |
| xAI Grok + Interactive Brokers | 金融 AI 产品 | 投资组合分析到交易指令的闭环，显示金融 agent 正在靠近执行层。 | 高风险场景能训练“确认、责任、边界”的产品判断。 | https://x.ai/news/grok-interactive-brokers | 等待真实用户反馈和合规说明。 |
| Figma Config 2026 AI canvas | 设计工具趋势 | 设计工具开始把代码、动画、3D、工作流技能放进画布。 | 与 Hermes HTML 阅读器的“内容结构即界面组件”相关。 | https://the-decoder.com/figma-bets-on-human-judgment-at-config-2026-while-the-ai-powering-its-canvas-belongs-to-someone-else | 因来源为二手报道，等待 Figma 官方页面再升级事实等级。 |

## 四、今日 3 个深度 case

【Case】

【类型】
Case A：外部变化类。

【背景事实】

已确认事实：
- Google 于 2026-06-24 在 The Keyword 发布“Introducing computer use in Gemini 3.5 Flash”，称 computer use 已成为 Gemini 3.5 Flash 的内置工具。
- Google 表示开发者可通过 Gemini API 和 Gemini Enterprise Agent Platform 使用该能力，并提到面向企业场景的安全措施。

行业观点：
- AI HOT 将该事件列为今日精选信号，并将其归为 AI 模型 / agent 能力演进。

个人推断：
- 这说明 computer use 正从单点模型能力进入主流模型默认能力层，企业采用的核心问题会从“能不能操作电脑”转向“能不能被安全治理”。

待验证假设：
- Google 宣称的长周期企业自动化表现仍需要第三方 benchmark、客户案例和失败率数据验证。

【信息来源】
- Google Keyword：https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-computer-use-gemini-3-5-flash/
- AI HOT item：https://aihot.virxact.com/items/cmqsl6c5y042hslfu74apxkap

【为什么值得分析】
它不是一个普通模型更新，而是 agent 执行能力进入默认模型栈的信号。P7+ 训练点在于判断能力边界、安全边界和企业落地路径。

【本次训练目标】
训练从“模型功能发布”推导到“企业工作流控制点”的判断。

【Case 快速认知】
阅读场景提示：当你看到“模型新增可执行能力”时，不要先问能做什么 demo，而要先问它进入什么系统、谁会承担风险、什么边界内可以授权。

- 这是什么：Gemini 3.5 Flash 把 computer use 变成内置能力，意味着模型可以在受支持环境中理解界面并执行操作。
- 这为什么重要：能力从单独模型 / demo 进入主模型栈后，开发者采用门槛下降，企业风险治理要求上升。
- 今天要学什么：判断一个“强能力”什么时候只是功能更新，什么时候会变成工作流基础设施。
- 本 case 的阅读抓手：不要盯着“会不会点屏幕”，要盯着“谁敢授权它点、点错了谁负责、怎么停、怎么审计”。

| 事实 | 来源 | 事实等级 | 是否可用于最终判断 | 是否需要继续核验 |
| ---- | ---- | -------- | ------------------ | ---------------- |
| Gemini 3.5 Flash 内置 computer use | Google 官方博客 | A | 是 | 否 |
| 可通过 Gemini API 和企业 Agent Platform 使用 | Google 官方博客 | A | 是 | 否 |
| 提供用户确认敏感操作、检测间接提示注入后停止等安全机制 | Google 官方博客 | A | 是 | 关键企业采用效果仍需后续案例 |
| AI HOT 认为这是今日高热 AI 模型信号 | AI HOT 摘要 | C | 否 | 是 |

【P6+ 第一反应】
一个执行型产品经理可能会直接想：Google 又发了一个更强的 computer use，可以拿来做自动化测试、网页操作和办公自动化。

【这个思路对在哪里】
它抓住了能力提升和场景扩展，尤其是浏览器、移动端、桌面环境中的跨应用操作。

【这个思路为什么不够】
它的问题不是错，而是太早进入功能想象，没有先判断企业为什么之前不敢把 computer use 放进真实流程。

【P7+ 刹车动作】
先不问“怎么做”，而要先问：当 agent 能操作电脑后，企业真正购买的是执行能力，还是可控、可审计、可回滚的执行边界？

1. 谁？这个问题到底是谁的问题？
目的：区分能力使用者、风险承担者和购买者。
使用模型：利益相关者地图。
为什么用这个模型：computer use 会影响开发者、企业管理员、安全团队、业务负责人和最终用户。
推导过程：开发者想要更快构建 agent，业务团队想减少重复操作，安全团队担心提示注入和不可逆操作，企业管理员需要权限与审计。
阶段结论：真正的用户不是单一开发者，而是“想把 agent 放进真实业务流程的企业团队”。
如何影响下一步：场景判断必须从 demo 转向企业工作流。

2. 在哪？这个问题发生在什么具体场景？
目的：识别 computer use 从展示能力到刚需场景的迁移。
使用模型：场景分层。
为什么用这个模型：浏览器、移动端、桌面和企业应用的风险密度不同。
推导过程：低风险场景是文档整理和信息抓取，中风险场景是软件测试和跨系统录入，高风险场景是资金、权限、删除和对外发送。
阶段结论：最先规模化的不是开放式桌面代操，而是受限环境中的连续测试和知识工作。
如何影响下一步：成本收益要按风险等级拆开。

3. 损失什么？当前谁付出了什么成本？
目的：判断为什么这个能力有商业价值。
使用模型：成本结构分析。
为什么用这个模型：agent 能力只有减少真实成本才会进入预算。
推导过程：企业今天在跨应用流程中付出人力切换成本、测试回归成本、手动检查成本、权限沟通成本和错误修复成本。
阶段结论：Gemini 的机会不只是节省点击，而是降低长流程执行和验证的边际成本。
如何影响下一步：收益必须落在更快、更稳、更可控。

4. 想得到什么？用户或企业真正想获得什么收益？
目的：避免把“自动操作”误判为核心价值。
使用模型：JTBD。
为什么用这个模型：企业雇佣 computer use 不是为了看模型动鼠标，而是完成跨系统任务。
推导过程：企业想得到连续软件测试、跨系统资料整理、应用巡检、知识工作执行和异常提示。
阶段结论：它的 JTBD 是“把需要人看屏幕、判断、操作的流程变成可监督执行”。
如何影响下一步：核心矛盾会落到自动化和控制之间。

5. 为什么卡住？真正矛盾是什么？
目的：抽象核心矛盾。
使用模型：约束理论。
为什么用这个模型：computer use 的瓶颈通常不在能力，而在风险约束。
推导过程：模型可以执行动作，但企业不能接受未经确认的敏感操作；模型可以读屏，但页面中可能有间接提示注入；模型可以跨应用，但权限边界会变模糊。
阶段结论：表面上是模型能不能操作电脑，本质上是执行型 agent 能不能被治理。
如何影响下一步：系统关系要围绕安全控制点展开。

6. 谁共同作用？识别推力、阻力、瓶颈、放大器、反馈和价值控制点。
目的：看清能力扩散的系统。
使用模型：系统思维。
为什么用这个模型：模型方、平台方、企业安全、开发者和业务流程相互制约。
推导过程：推力是模型原生能力和企业自动化需求；阻力是安全风险、权限误用、责任归属；瓶颈是可审计执行；放大器是 API、企业平台和参考实现。
阶段结论：价值控制点从模型参数迁移到 agent runtime、policy、confirmation 和 audit log。
如何影响下一步：趋势推演要关注治理层标准化。

7. 未来怎么变？从系统变量推演。
目的：判断这类能力未来形态。
使用模型：S 曲线。
为什么用这个模型：computer use 从早期 demo 到企业平台会经历采用曲线。
推导过程：现在是模型内置化；阶段 1 是受限沙箱和浏览器自动化；阶段 2 是企业平台接入权限、审计和确认；长期形态是多应用工作流 agent 成为企业操作系统的一部分。
阶段结论：未来竞争点会从“谁能操作”变成“谁能被放心授权”。
如何影响下一步：机会判断要避开纯能力包装。

8. 价值流向哪里？判断谁创造、传递、捕获价值。
目的：定位商业机会。
使用模型：价值链分析。
为什么用这个模型：computer use 涉及模型、API、企业平台、浏览器环境、工作流工具和安全治理。
推导过程：模型创造通用能力，API 和企业平台传递能力，治理层捕获企业信任价值，业务流程拥有真实 ROI。
阶段结论：最大价值流向可监督执行平台，而不只是模型调用。
如何影响下一步：最终判断必须包含做、不做、先验证。

| 环节 | 使用模型 | 为什么使用 | 得到什么结论 | 对后续判断的价值 |
| ---- | -------- | ---------- | ------------ | ---------------- |
| 谁 | 利益相关者地图 | 区分使用者和风险承担者 | 企业团队是核心对象 | 避免只面向开发者 demo |
| 场景 | 场景分层 | 区分风险等级 | 软件测试和知识工作先落地 | 确定早期采用路径 |
| 成本 | 成本结构分析 | 量化企业价值 | 降低跨应用执行与验证成本 | 支撑商业判断 |
| 矛盾 | 约束理论 | 找瓶颈 | 治理是核心约束 | 指向机会控制点 |
| 系统 | 系统思维 | 看相互作用 | 价值在 runtime 与 audit | 建立趋势判断 |
| 趋势 | S 曲线 | 推演阶段 | 从能力内置到企业授权 | 判断长期机会 |

【分析方法展开】

| 分析方法 | 适用场景 | 关键分析维度 | 本 case 的具体用法 | 得到的结论 |
| ---- | ---- | ---- | ---- | ---- |
| 利益相关者地图 | 一个能力会改变多方责任时使用 | 使用者、付费者、风险承担者、管理员、受影响者 | 区分开发者、业务团队、安全团队、企业管理员 | 核心用户不是开发者个人，而是想把 agent 放进业务流程的企业团队 |
| 场景分层 | 能力可进入多个风险场景时使用 | 任务频率、风险等级、可回滚性、是否涉及权限 / 资金 / 对外发送 | 将 computer use 分成低风险资料处理、中风险测试录入、高风险资金权限动作 | 早期应先进入低风险高频流程，而不是开放式桌面代操 |
| 成本结构分析 | 判断企业是否愿意付费时使用 | 时间、人力、沟通、错误修复、风险、机会成本 | 拆出跨应用操作、回归测试、手动检查、权限沟通成本 | 价值不只是省点击，而是降低长流程执行和验证成本 |
| 约束理论 | 能力很强但落地慢时使用 | 最大瓶颈、风险约束、组织约束、技术约束 | 将瓶颈定位为敏感操作、提示注入、权限边界、审计责任 | 产品机会在治理和授权，而不是继续堆能力 |
| 系统思维 | 多方互相制约时使用 | 推力、阻力、瓶颈、放大器、反馈、控制点 | 分析模型、API、企业平台、安全团队和业务流程的作用 | 价值控制点会迁移到 runtime、policy、confirmation 和 audit log |
| S 曲线 | 判断能力扩散阶段时使用 | 早期采用、扩散条件、平台化阶段、成熟形态 | 从模型内置化推演到受控沙箱、企业平台、跨应用操作系统 | 竞争点会从“谁能操作”变成“谁能被放心授权” |

【现象】
我观察到：Google 把 computer use 内置到 Gemini 3.5 Flash，并给出 API、企业平台和安全机制。

【原因】
它不是由单一因素导致，而是：模型多模态理解、工具调用、企业自动化需求和 agent 安全治理共同推进。
其中最核心的驱动是：agent 能力要从展示走进真实业务流程。

【本质】
表面上是：Gemini 又增强了电脑操作能力。
本质上是：模型厂商正在把“可执行 agent”变成默认能力，同时把安全控制前置。
一句话本质判断：这不是 computer use 功能问题，而是企业是否敢授权 agent 进入真实工作流的问题。

【系统】
关键参与因素包括：模型厂商、API 平台、企业 Agent Platform、安全团队、开发者、业务流程负责人。
核心系统关系是：能力越强，越需要确认、沙箱、审计和权限边界。
推力：跨应用自动化 ROI。
阻力：提示注入、敏感操作、责任归属。
瓶颈：企业级可控性。
放大器：API、参考实现、客户案例、平台集成。

【趋势】
我判断它会从：
- 现在：Gemini 3.5 Flash 内置 computer use，开发者可以通过 API / 企业平台接触这类能力。
- 阶段 1：computer use 先在低风险、高频、可回滚的任务里扩散，例如软件测试、资料整理、网页巡检、表单核对。
- 阶段 2：企业开始要求权限分级、敏感动作确认、执行日志、异常停止、人工接管和审计报表。
- 长期形态：computer use 成为企业自动化平台的底层能力，但售卖时必须和 policy、confirmation、audit、rollback 绑定。
长期趋势是：agent computer use 会成为企业自动化平台的基础能力，但必须与安全和审计一起被产品化。

【机会】
最大机会不在：包装一个能点屏幕的 demo。
而在：建立可监督、可确认、可回滚的跨应用执行工作流。
因为：企业愿意为稳定和可控付费，而不是为不可控能力冒险。

【核心判断】
这不是模型功能升级问题，而是企业执行授权系统问题。最大机会不在通用 computer use demo，而在可控执行、审计、确认和失败处理。所以不应该优先做开放式桌面代操，而应该先验证低风险高频流程中的可控执行闭环。

【应该做什么】
围绕软件测试、资料整理、表单录入、流程巡检等低风险场景设计受控 agent。

【不应该做什么】
不要直接进入资金、权限、删除、发送等高风险动作。

【先验证什么】
验证在限定环境里，agent 是否能稳定完成任务、触发敏感动作确认、记录审计日志并在异常时停止。

【关键假设】
企业采用 computer use 的关键不是能力上限，而是风险下限。

【验证指标】
任务完成率、人工接管率、敏感动作误触发率、提示注入拦截率、审计日志可追溯率。

【最小可行方案】
选一个内部网页巡检或文档检查流程，限定权限，记录每步动作，敏感操作必须确认。

【长期机会】
沉淀企业 agent 执行标准，包括 task spec、policy、confirmation、audit、rollback。

【最大风险】
能力先行导致事故，反而让企业关闭 agent 权限。

如果我在面试或汇报中表达，我会这样说：

“我会从六层来看这个问题。
第一，现象上，Google 把 computer use 内置到 Gemini 3.5 Flash。
第二，原因上，企业需要跨应用自动化，但不敢把不可控 agent 放进真实流程。
第三，本质上，这不是模型会不会点屏幕的问题，而是企业是否敢把 agent 授权进真实工作流的问题。
第四，系统上，模型能力、企业平台、安全团队、业务流程和审计机制共同作用。
第五，趋势上，computer use 会从 demo 进入受控工作流。
第六，机会判断上，最大机会不在开放式代操，而在可治理执行平台。

所以我的最终判断是，应该先验证低风险高频流程中的可控执行闭环。
不应该优先做高风险自动操作。
而应该先验证权限、确认、审计和失败处理。”

【训练能力】
从模型发布抽象企业采用约束。

【P6+ 易犯错误】
把“能操作电脑”直接等同于“能落地商业化”。

【P7+ 正确思路】
先看谁承担风险，再看什么场景能授权。

【可复用 Pattern】
可执行能力产品化 = 能力边界 + 风险分级 + 人类确认 + 审计回放 + 失败停止。

【迁移方式】
迁移到 Hermes HTML 生成器：不要只生成页面，要记录来源、结构、校验和发布状态。

【Case Asset Card】

Case 名称：Gemini 3.5 Flash 内置 computer use

所属方向：Agent / Computer Use / 企业自动化治理

一句话现象：Google 将 computer use 变成 Gemini 3.5 Flash 的内置能力。

一句话本质：这不是能力展示，而是 agent 执行能力进入可治理企业工作流的开始。

核心矛盾：企业想要自动执行，但又不能接受不可控、不可审计、不可回滚的执行。

关键系统关系：模型能力越强，企业对权限、确认、审计、失败处理的要求越高。

价值流向：从模型调用流向受控 runtime、企业平台、安全策略和高频工作流。

做 / 不做 / 先验证：做低风险受控流程；不做开放式高风险代操；先验证完成率、接管率和审计可追溯。

可复用 Pattern：可执行 agent 的产品化路径是先限制边界，再扩大授权。

可迁移到我的哪个项目：
- Hermes daily HTML 发布系统：先保证 Markdown validator、来源记录和发布状态，再追求自动发布。

可迁移到哪类面试题：如何判断 computer use agent 的企业落地机会？

2 分钟表达版本：Gemini computer use 的关键不是让模型会操作电脑，而是让企业相信它能在有边界的情况下执行。我的判断是，先落地低风险高频场景，用确认、审计和失败停止建立信任，再逐步扩展授权。

未来 Watchlist：观察 Google 是否公布企业采用案例、事故率、安全最佳实践和平台 API 细节。

关注对象：
- Google Gemini API、Gemini Enterprise Agent Platform、Browserbase、UiPath、企业自动化案例。

关注指标：
- 产品是否继续迭代
- GitHub star / fork / release / issue 是否持续增长
- 是否出现付费客户 / 企业案例
- 是否出现竞品跟进
- 是否出现官方论文 / 技术突破
- 是否出现负面风险或监管事件

Watchlist 状态：
- 持续跟踪

资产等级：
- A

资产等级说明：
- A：可直接进入面试素材库 / 项目方法论库 / 个人知识库核心库。

复习优先级：
- 高

【Case】

【类型】
Case B：产品 / 商业 / 开源趋势类。

【背景事实】

已确认事实：
- Cursor 于 2026-06-25 发布文章，介绍 Notion 使用 Cursor SDK 在产品中嵌入编码 agent。
- Cursor 文章称用户可以在 Notion 文档、讨论串或数据库任务中调用 Cursor，并由 Cursor 规划、构建、测试、验证并打开 PR。

行业观点：
- AI HOT 将该事件列为今日 AI 产品信号，认为它体现产品内嵌 coding agent 的趋势。

个人推断：
- 这标志着 coding agent 从 IDE / CLI 工具转向业务协作产品的内部动作，SDK 成为平台化控制点。

待验证假设：
- Notion 用户实际采用率、付费转化、失败率、权限边界和企业管理员控制细节仍需后续数据。

【信息来源】
- Cursor Blog：https://cursor.com/blog/notion
- AI HOT item：https://aihot.virxact.com/items/cmqsjydyy03s2slfu0akeh868

【为什么值得分析】
它展示了“agent 不是独立目的地，而是嵌进用户已有工作流”的产品化路径。

【本次训练目标】
训练 SDK / workflow / host product 三方关系判断。

【Case 快速认知】
阅读场景提示：当你看到“某个产品接入某个 AI SDK”时，不要只看多了一个按钮，而要问谁控制入口、谁控制上下文、谁控制执行、谁控制验收。

- 这是什么：Notion 通过 Cursor SDK 让文档、讨论串、数据库任务可以直接触发 coding agent。
- 这为什么重要：coding agent 不再只存在于 IDE / CLI，而是进入用户已有协作空间。
- 今天要学什么：判断 AI SDK 集成是真价值，还是表层嵌入。
- 本 case 的阅读抓手：需求在哪里产生，agent 在哪里执行，结果在哪里验收，状态如何回写。

| 事实 | 来源 | 事实等级 | 是否可用于最终判断 | 是否需要继续核验 |
| ---- | ---- | -------- | ------------------ | ---------------- |
| Notion 使用 Cursor SDK 嵌入编码 agent | Cursor 官方博客 | A | 是 | Notion 官方细节仍可补充 |
| Cursor 能从 Notion 场景执行规划、构建、测试、验证并打开 PR | Cursor 官方博客 | A | 是 | 实际失败率待验证 |
| AI HOT 将其归为今日 AI 产品信号 | AI HOT 摘要 | C | 否 | 是 |
| 用户会高频在 Notion 中分配编码任务 | 个人推断 | C | 否 | 是 |

【P6+ 第一反应】
一个执行型产品经理可能会直接想：Notion 接入 Cursor，所以 Notion 以后可以直接写代码。

【这个思路对在哪里】
它看到了协作工具与 coding agent 结合的场景机会。

【这个思路为什么不够】
它的问题不是错，而是把集成理解成一个功能入口，没有看到 SDK 如何改变产品边界和价值捕获。

【P7+ 刹车动作】
先不问“怎么做”，而要先问：为什么 coding agent 要进入 Notion，而不是让用户继续回到 Cursor / IDE？

1. 谁？这个问题到底是谁的问题？
目的：确定嵌入式 agent 服务的是谁。
使用模型：利益相关者地图。
为什么用这个模型：Notion 场景中有任务提出者、工程执行者、reviewer、产品经理和团队管理员。
推导过程：产品经理在 Notion 写需求，工程师在代码库执行，reviewer 关注 PR 质量，管理员关注权限和成本。
阶段结论：核心用户不是单个程序员，而是跨职能协作团队。
如何影响下一步：场景要从“写代码”转向“协作中的任务流转”。

2. 在哪？这个问题发生在什么具体场景？
目的：判断 agent 嵌入点。
使用模型：用户旅程。
为什么用这个模型：Notion 是需求、讨论、数据库和任务管理入口。
推导过程：需求在文档中出现，讨论在 thread 中发生，任务在数据库里分配，代码变更在 GitHub PR 中闭环。
阶段结论：Notion 的价值在于成为任务意图入口，而不是替代 IDE。
如何影响下一步：成本分析要看上下文切换。

3. 损失什么？当前谁付出了什么成本？
目的：找到集成的 ROI。
使用模型：成本结构分析。
为什么用这个模型：SDK 嵌入必须减少真实协作成本。
推导过程：团队今天要把 Notion 需求复制到工程系统，解释上下文，分派任务，等待实现，回到 Notion 汇报结果。
阶段结论：最大成本是上下文搬运、任务翻译和状态同步。
如何影响下一步：收益不是代码速度，而是协作闭环速度。

4. 想得到什么？用户或企业真正想获得什么收益？
目的：抽象 JTBD。
使用模型：JTBD。
为什么用这个模型：用户不是要“在 Notion 写代码”，而是要让需求到 PR 更短。
推导过程：PM 想把需求直接变成工程动作，工程师想减少重复澄清，团队想要任务状态可见。
阶段结论：JTBD 是“让协作空间里的意图自动进入工程执行系统”。
如何影响下一步：核心矛盾转向协作上下文与工程执行之间的断裂。

5. 为什么卡住？真正矛盾是什么？
目的：找到产品化瓶颈。
使用模型：因果树。
为什么用这个模型：集成是否成功取决于多层原因。
推导过程：Notion 有上下文但没有代码执行环境；Cursor 有执行环境但不一定拥有完整业务上下文；GitHub 有变更闭环但不承载需求讨论。
阶段结论：表面上是 Notion 加了 coding agent，本质上是协作上下文与代码执行环境的桥接。
如何影响下一步：系统分析要看谁控制入口、runtime 和交付物。

6. 谁共同作用？识别推力、阻力、瓶颈、放大器、反馈和价值控制点。
目的：看清商业系统。
使用模型：价值链。
为什么用这个模型：Cursor、Notion、GitHub、团队流程共同分配价值。
推导过程：Notion 控制需求入口，Cursor 控制 agent runtime，GitHub 控制代码交付，团队流程控制验收。
阶段结论：SDK 是 Cursor 把自身能力嵌入他人产品的价值传递层。
如何影响下一步：趋势会指向 agent infrastructure 平台化。

7. 未来怎么变？从系统变量推演。
目的：判断嵌入式 agent 的演进。
使用模型：情景推演。
为什么用这个模型：不同 host product 会产生不同 agent 入口。
推导过程：现在是 Notion 调用 Cursor；阶段 1 是更多协作工具嵌入 coding agent；阶段 2 是业务对象自动触发 agent；长期形态是每个工作对象都可绑定专属 agent。
阶段结论：agent 会从独立工具变成对象级能力。
如何影响下一步：机会判断要看 SDK 与 host product 关系。

8. 价值流向哪里？判断谁创造、传递、捕获价值。
目的：判断商业控制点。
使用模型：战略定位。
为什么用这个模型：平台生态中价值捕获不一定在入口方。
推导过程：Notion 捕获协作入口价值，Cursor 捕获执行能力价值，GitHub 捕获代码交付价值，团队流程捕获业务产出。
阶段结论：最大价值流向能同时掌握上下文、执行和验证的 agent workflow 层。
如何影响下一步：最终判断要避免只做浅层集成。

| 环节 | 使用模型 | 为什么使用 | 得到什么结论 | 对后续判断的价值 |
| ---- | -------- | ---------- | ------------ | ---------------- |
| 谁 | 利益相关者地图 | 识别跨职能使用者 | 用户是协作团队 | 避免只服务工程师 |
| 场景 | 用户旅程 | 找入口和闭环 | Notion 是意图入口 | 明确集成价值 |
| 成本 | 成本结构分析 | 识别协作损耗 | 上下文搬运成本高 | 形成 ROI 判断 |
| 矛盾 | 因果树 | 找断点 | 上下文与执行断裂 | 指向 SDK 价值 |
| 系统 | 价值链 | 看价值捕获 | SDK 是传递层 | 判断平台化趋势 |
| 趋势 | 情景推演 | 推演 host product | 对象级 agent 增多 | 指导机会选择 |

【分析方法展开】

| 分析方法 | 适用场景 | 关键分析维度 | 本 case 的具体用法 | 得到的结论 |
| ---- | ---- | ---- | ---- | ---- |
| 利益相关者地图 | 一个集成影响跨职能团队时使用 | 任务提出者、执行者、reviewer、管理员、成本承担者 | 拆出 PM、工程师、reviewer、团队管理员 | 用户不是单个工程师，而是跨职能协作团队 |
| 用户旅程 | 分析工具嵌入点时使用 | 意图产生、任务分配、执行、验收、反馈回写 | 将 Notion 文档、thread、database、GitHub PR 连成一条旅程 | Notion 的价值是任务意图入口，不是替代 IDE |
| 成本结构分析 | 判断 SDK 集成 ROI 时使用 | 上下文搬运、任务翻译、等待、沟通、返工 | 分析从 Notion 需求到工程 PR 的切换成本 | 最大成本是上下文搬运和状态同步 |
| JTBD | 功能表象容易误导时使用 | 用户雇佣产品完成什么进步 | 将“在 Notion 写代码”改写为“让需求更短路径到 PR” | 真实任务是让协作空间里的意图进入工程执行系统 |
| 因果树 | 找集成价值断点时使用 | 表层原因、二层原因、根因、可改变因素 | 分析 Notion 有上下文、Cursor 有执行、GitHub 有交付 | 本质是协作上下文与代码执行环境的桥接 |
| 价值链 | 多平台共同分配价值时使用 | 入口、runtime、交付物、验收、商业捕获 | 分析 Notion、Cursor、GitHub、团队流程各自控制点 | 最大价值流向能掌握上下文、执行和验证的 workflow 层 |

【现象】
我观察到：Notion 通过 Cursor SDK 将 coding agent 放进文档、讨论和数据库任务中。

【原因】
它不是由单一因素导致，而是：协作工具拥有上下文，coding agent 拥有执行能力，团队需要更短的需求到 PR 链路。
其中最核心的驱动是：工作意图不想再离开原生协作空间。

【本质】
表面上是：Notion 接入 Cursor。
本质上是：agent 能力通过 SDK 成为其他产品的内部执行层。
一句话本质判断：这不是 Notion 写代码功能问题，而是 coding agent 从工具入口迁移到业务对象内部的问题。

【系统】
关键参与因素包括：Notion、Cursor、GitHub、PM、工程师、reviewer、管理员。
核心系统关系是：谁拥有上下文，谁拥有执行，谁拥有验收，谁就能影响价值捕获。
推力：减少需求到 PR 的摩擦。
阻力：权限、安全、失败处理、工程责任归属。
瓶颈：agent 执行质量和团队信任。
放大器：SDK、模板、MCP、自动触发规则。

【趋势】
我判断它会从：
- 现在：Notion 通过 Cursor SDK 把 coding agent 接入文档、讨论和数据库任务。
- 阶段 1：更多协作工具会把 agent 作为“任务执行者”嵌入到文档、issue、表格行、评论线程中。
- 阶段 2：业务对象会开始绑定模板、权限、验收标准、自动触发规则和状态回写。
- 长期形态：agent 不再是用户打开的独立工具，而是每个工作对象可调用的执行层。
长期趋势是：agent 会从“打开一个工具”变成“在业务对象上触发一次可验收执行”。

【机会】
最大机会不在：给每个工具加一个 AI 按钮。
而在：把业务对象、上下文、执行、验证和状态同步做成一个闭环。
因为：用户真正想要的是任务完成，而不是切换工具。

【核心判断】
这不是 Notion 增加 AI 编码入口问题，而是业务协作对象变成 agent 执行入口的问题。最大机会不在表层集成，而在上下文、执行、验证和状态同步闭环。所以不应该优先做一个孤立按钮，而应该先验证一个从需求文档到 PR 的端到端任务链。

【应该做什么】
先选需求文档、bug 修复、轻量脚本和文档更新等可验证任务做闭环。

【不应该做什么】
不要让 agent 在缺少验收标准和权限边界时自动改大范围代码。

【先验证什么】
验证 Notion 上下文是否足以让 agent 生成正确计划、打开 PR、通过测试并把状态回写。

【关键假设】
用户愿意在协作工具中发起 coding task，因为上下文已经在那里。

【验证指标】
任务从创建到 PR 的时间、澄清次数、PR 通过率、人工修改比例、状态回写准确率。

【最小可行方案】
选择“文档中的小 bug / 文案修改 / 测试补充”作为首批任务类型，设置模板和验收条件。

【长期机会】
建立“业务对象绑定 agent”的平台能力，让每个需求、issue、文档、表格行都能触发受控执行。

【最大风险】
host product 获得入口，agent provider 被替换；或者 agent 质量不稳导致团队不再信任自动任务。

如果我在面试或汇报中表达，我会这样说：

“我会从六层来看这个问题。
第一，现象上，Notion 通过 Cursor SDK 嵌入 coding agent。
第二，原因上，团队协作上下文在 Notion，但代码执行在 Cursor 和 GitHub。
第三，本质上，这不是 Notion 增加一个 AI 功能的问题，而是业务对象成为 agent 执行入口的问题。
第四，系统上，Notion 控制上下文，Cursor 控制执行，GitHub 控制交付。
第五，趋势上，agent 会越来越嵌入工作对象，而不是停留在独立工具。
第六，机会判断上，最大机会不在按钮集成，而在上下文到 PR 的闭环。

所以我的最终判断是，应该先验证端到端任务链。
不应该优先做大范围自动代码修改。
而应该先验证计划、测试、PR 和状态回写。”

【训练能力】
从产品集成抽象平台控制点。

【P6+ 易犯错误】
只看到“Notion 能写代码”，没有看到 SDK 和对象级 agent 的价值流向。

【P7+ 正确思路】
先判断入口、上下文、执行、验收分别被谁控制。

【可复用 Pattern】
嵌入式 agent 产品化 = host context + agent runtime + delivery system + status loop。

【迁移方式】
迁移到 Hermes HTML：Markdown section 不只是文本，而是页面组件的上下文对象。

【Case Asset Card】

Case 名称：Notion 使用 Cursor SDK 嵌入编码智能体

所属方向：AI Coding / SDK 平台化 / 协作工作流

一句话现象：Notion 通过 Cursor SDK 在文档、讨论和数据库任务里调用 coding agent。

一句话本质：agent 正从独立工具入口迁移到业务对象内部。

核心矛盾：协作工具拥有上下文，编码工具拥有执行力，但任务完成需要两者闭环。

关键系统关系：Notion 控制意图入口，Cursor 控制执行 runtime，GitHub 控制交付物，团队流程控制验收。

价值流向：从 IDE 单点效率流向跨工具工作流完成率。

做 / 不做 / 先验证：做小范围端到端任务；不做无边界大改；先验证 PR 质量和状态回写。

可复用 Pattern：对象级 agent = 在业务对象上绑定可验证执行。

可迁移到我的哪个项目：
- Hermes daily HTML 阅读器：每个 Markdown section 都可以被当作业务对象，绑定证据、推理、资产卡和发布状态。

可迁移到哪类面试题：如何评估一个 AI SDK 集成是否真正有产品价值？

2 分钟表达版本：Notion + Cursor 的重点不是把 AI 按钮放进 Notion，而是让协作空间里的需求直接进入工程执行闭环。真正的价值是减少上下文搬运，并通过计划、测试、PR 和状态回写形成闭环。

未来 Watchlist：关注 Notion 官方说明、企业权限、模板生态、任务成功率和竞品跟进。

关注对象：
- Cursor SDK、Notion AI、GitHub PR workflow、MCP 模板、协作工具 agent 集成。

关注指标：
- 产品是否继续迭代
- GitHub star / fork / release / issue 是否持续增长
- 是否出现付费客户 / 企业案例
- 是否出现竞品跟进
- 是否出现官方论文 / 技术突破
- 是否出现负面风险或监管事件

Watchlist 状态：
- 下周复查

资产等级：
- A

资产等级说明：
- A：可直接进入面试素材库 / 项目方法论库 / 个人知识库核心库。

复习优先级：
- 高

【Case】

【类型】
Case C：个人壁垒类。

【背景事实】

已确认事实：
- GitHub 于 2026-06-11 在 Changelog 宣布 GitHub Agentic Workflows 进入 public preview。
- GitHub 表示用户可用自然语言 Markdown 定义自动化，系统编译为标准 Actions YAML，并复用现有 runner group 和 policy constraints。
- GitHub 公告提到默认只读权限、sandboxed container、Agent Workflow Firewall、safe outputs 和 threat detection 等安全设计。

行业观点：
- GitHub 将其定位为 issue triage、CI failure analysis、documentation updates 等 reasoning-based tasks 的自动化方式。

个人推断：
- 这对个人职业壁垒的启发是：会写 prompt 不够，能设计 agent workflow、review gate、policy 和审计闭环才是更高层能力。

待验证假设：
- 公测阶段的稳定性、企业实际采用规模、复杂多仓库变更成功率需要后续验证。

【信息来源】
- GitHub Changelog：https://github.blog/changelog/2026-06-11-github-agentic-workflows-is-now-in-public-preview/
- GitHub Next agentics repository：https://github.com/githubnext/agentics
- AI HOT item：未进入本次 AI HOT 精选列表；本 case 由 GitHub 官方源和用户长期关注方向共同提升优先级。

【为什么值得分析】
它几乎就是用户正在做的 skill / workflow / gate 系统的行业版本：自然语言任务不是终点，进入可执行、可治理、可审计的工程流水线才是壁垒。

【本次训练目标】
训练从“会使用 AI coding”升级到“会设计 agent governance”的个人壁垒判断。

【Case 快速认知】
阅读场景提示：当你看到“AI 自动做工程任务”时，不要只问它能不能做，而要问它是否进入了已有工程治理系统：谁定义任务、谁执行、谁限制权限、谁验证输出、谁负责事故。

- 这是什么：GitHub Agentic Workflows 让自然语言 Markdown workflow 编译进 Actions 执行体系。
- 这为什么重要：它把 agent 从聊天式建议放进 runner、policy、safe outputs、threat detection 和 review gate。
- 今天要学什么：个人壁垒不只是会用 AI coding，而是会把 AI coding 变成可复用、可验证、可审计的工作流。
- 本 case 的阅读抓手：看 agent 是否有 spec、execution、validation、review、publish、archive 的闭环。

| 事实 | 来源 | 事实等级 | 是否可用于最终判断 | 是否需要继续核验 |
| ---- | ---- | -------- | ------------------ | ---------------- |
| GitHub Agentic Workflows 进入 public preview | GitHub Changelog | A | 是 | 否 |
| 自然语言 Markdown 可编译为 Actions YAML | GitHub Changelog | A | 是 | 否 |
| 复用 runner group 与 policy constraints | GitHub Changelog | A | 是 | 否 |
| 公测阶段企业 adoption 会快速扩大 | 个人推断 | C | 否 | 是 |

【P6+ 第一反应】
一个执行型产品经理可能会直接想：GitHub 做了一个自动 triage 和修 CI 的 AI 功能，开发者以后更省事。

【这个思路对在哪里】
它看到了自动化任务和工程效率提升。

【这个思路为什么不够】
它的问题不是错，而是没有看到 GitHub 把 agent 放进 Actions、policy、runner、安全扫描和输出校验里。

【P7+ 刹车动作】
先不问“能自动做什么”，而要先问：为什么 GitHub 要把 agent workflow 编译成 Actions，而不是只提供聊天式 Copilot？

1. 谁？这个问题到底是谁的问题？
目的：识别谁需要 agent workflow。
使用模型：利益相关者地图。
为什么用这个模型：工程自动化涉及开发者、维护者、平台团队、安全团队和管理者。
推导过程：开发者需要少做重复任务，维护者需要 triage，平台团队需要标准化，安全团队需要权限和扫描，管理者需要可度量效率。
阶段结论：核心对象是需要在组织内规模化 agent 的工程平台团队。
如何影响下一步：场景要落在标准化工程流程。

2. 在哪？这个问题发生在什么具体场景？
目的：找 agent workflow 的高价值入口。
使用模型：场景分层。
为什么用这个模型：不是所有 coding task 都适合自动 agent。
推导过程：issue triage、CI failure analysis、documentation updates、dependency maintenance、routine reporting 都是高频低边界任务。
阶段结论：最适合公测的场景是标准明确、可验证、可回滚的工程任务。
如何影响下一步：成本分析要围绕重复工程劳动。

3. 损失什么？当前谁付出了什么成本？
目的：判断为什么 GitHub 要产品化这个能力。
使用模型：成本结构分析。
为什么用这个模型：工程组织会为重复工作、等待和上下文切换付费。
推导过程：团队在 triage、CI 排障、文档更新和合规检查上消耗时间，且这些工作分散在仓库、Actions、PR 和安全工具之间。
阶段结论：损失不是单个开发者时间，而是组织级工程吞吐与注意力。
如何影响下一步：收益要看治理和复用。

4. 想得到什么？用户或企业真正想获得什么收益？
目的：抽象真实收益。
使用模型：JTBD。
为什么用这个模型：企业不是想“让 AI 自动乱改代码”，而是想把重复判断变成可管理流程。
推导过程：平台团队想定义一次、复用多仓库；安全团队想保留 policy；开发者想少处理重复事项。
阶段结论：JTBD 是“把 reasoning-based engineering work 变成可复用、可治理的 workflow”。
如何影响下一步：核心矛盾转向自治和控制。

5. 为什么卡住？真正矛盾是什么？
目的：找本质矛盾。
使用模型：约束理论。
为什么用这个模型：agent coding 的瓶颈不是生成 PR，而是信任 PR。
推导过程：聊天式 agent 可以给建议，但无法稳定复用；脚本可以复用，但缺少推理；GitHub 的做法是把自然语言、Actions、runner、policy 和安全扫描连接起来。
阶段结论：表面上是工程自动化，本质上是把 agent 推理纳入已有治理系统。
如何影响下一步：系统关系要看 gate。

6. 谁共同作用？识别推力、阻力、瓶颈、放大器、反馈和价值控制点。
目的：看清治理系统。
使用模型：系统思维。
为什么用这个模型：agent workflow 是多个安全与执行层共同作用。
推导过程：推力是重复任务自动化；阻力是不可信变更；瓶颈是权限与输出安全；放大器是 Actions 生态、runner、prebuilt workflows、community discussion。
阶段结论：控制点在 workflow spec、runner policy、safe outputs、threat detection 和 review gate。
如何影响下一步：趋势要看 agent workflow 标准化。

7. 未来怎么变？从系统变量推演。
目的：判断个人壁垒方向。
使用模型：价值迁移。
为什么用这个模型：AI coding 的价值会从个体使用技巧迁移到组织流程设计。
推导过程：现在是个人用 coding agent；阶段 1 是团队定义工作流；阶段 2 是组织建立 workflow catalogue；长期形态是 agent governance 成为工程平台岗位核心能力。
阶段结论：个人壁垒从“会提示”迁移到“会设计可审计 agent 系统”。
如何影响下一步：机会判断要回到用户自己的 skill 系统。

8. 价值流向哪里？判断谁创造、传递、捕获价值。
目的：定位价值控制点。
使用模型：业务价值模型。
为什么用这个模型：GitHub 既有代码入口，也有 Actions、policy 和安全工具。
推导过程：agent 创造推理能力，Actions 传递执行能力，policy 和 firewall 捕获信任价值，组织流程捕获效率价值。
阶段结论：最大价值流向能把 AI 执行纳入组织治理的工作流平台。
如何影响下一步：最终判断要产出个人方法论。

| 环节 | 使用模型 | 为什么使用 | 得到什么结论 | 对后续判断的价值 |
| ---- | -------- | ---------- | ------------ | ---------------- |
| 谁 | 利益相关者地图 | 看组织采用者 | 平台团队是关键用户 | 个人壁垒从工具使用升级 |
| 场景 | 场景分层 | 找适合自动化任务 | 高频可验证任务先落地 | 指导切入点 |
| 成本 | 成本结构分析 | 看组织损耗 | 重复工程劳动浪费吞吐 | 支撑 ROI |
| 矛盾 | 约束理论 | 找瓶颈 | 信任比生成更关键 | 指向 gate |
| 系统 | 系统思维 | 识别治理组件 | spec、policy、safe outputs 是控制点 | 可迁移到 Hermes |
| 趋势 | 价值迁移 | 看个人壁垒 | 从 prompt 到 governance | 形成职业资产 |

【分析方法展开】

| 分析方法 | 适用场景 | 关键分析维度 | 本 case 的具体用法 | 得到的结论 |
| ---- | ---- | ---- | ---- | ---- |
| 利益相关者地图 | 工程自动化影响组织多角色时使用 | 开发者、维护者、平台团队、安全团队、管理者 | 区分谁想省事、谁要标准化、谁承担安全风险 | 关键用户是工程平台团队，而不是单个开发者 |
| 场景分层 | 判断哪些任务适合 agent 自动化时使用 | 高频、低边界、可验证、可回滚、责任清晰 | 拆出 issue triage、CI failure analysis、docs update、依赖维护 | 早期场景应是标准明确、可回滚的工程任务 |
| 成本结构分析 | 判断组织为什么购买自动化时使用 | 重复劳动、等待、上下文切换、返工、审计成本 | 分析 triage、CI 排障、文档更新和合规检查的组织成本 | 损失不是个人时间，而是组织级工程吞吐 |
| JTBD | 避免把 agent 误判为聊天工具时使用 | 用户真正雇佣 agent 完成什么进步 | 将“让 AI 做任务”改写成“把重复工程判断变成可管理流程” | 企业要的是可复用 workflow，不是一次性建议 |
| 约束理论 | 自动化看似有用但难规模化时使用 | 最大瓶颈、信任、权限、输出安全、事故责任 | 分析为什么生成 PR 不等于可以自动合并 | 瓶颈是信任与治理，不是生成能力 |
| 系统思维 | 多个治理组件共同作用时使用 | spec、runner、policy、firewall、safe outputs、review gate | 将 GitHub Actions、policy、security 和 reviewer 放进同一系统 | 控制点在 workflow spec 和 gate，而不在 prompt |
| 价值迁移 | 判断个人职业壁垒变化时使用 | 能力从哪里迁移到哪里、谁捕获新价值 | 从个人 prompt skill 推演到组织 workflow catalogue | 未来壁垒是会设计可审计 agent 系统 |

【现象】
我观察到：GitHub Agentic Workflows 允许用自然语言 Markdown 定义 agent workflow，并编译进 Actions 执行体系。

【原因】
它不是由单一因素导致，而是：企业需要自动化 reasoning-based engineering work，同时不能绕过已有权限、runner、安全和 review 流程。
其中最核心的驱动是：agent 必须进入组织治理体系才可能规模化。

【本质】
表面上是：GitHub 增加了自动 triage、CI 分析和文档更新能力。
本质上是：AI agent 被工程化为可复用、可执行、可审计的 workflow。
一句话本质判断：这不是 AI 自动写代码问题，而是 agent 推理如何进入工程治理系统的问题。

【系统】
关键参与因素包括：GitHub Actions、agent workflow Markdown、runner groups、policy constraints、firewall、safe outputs、threat detection、reviewer。
核心系统关系是：自然语言定义任务，Actions 执行任务，policy 限制权限，safe outputs 和 threat detection 降低风险。
推力：工程重复任务自动化。
阻力：不可控代码变更。
瓶颈：组织信任和安全审核。
放大器：GitHub 生态、prebuilt workflows、企业案例。

【趋势】
我判断它会从：
- 现在：GitHub Agentic Workflows 以 public preview 形式，把自然语言 workflow 放进 Actions 执行体系。
- 阶段 1：组织会先把 issue triage、CI failure analysis、documentation updates 等低风险任务做成预置 workflow。
- 阶段 2：团队会形成 workflow catalogue，并给不同仓库、runner、权限和输出类型配置 policy。
- 长期形态：agent workflow、review gate、security scan、audit log 会成为工程平台的标准基础设施。
长期趋势是：agent workflow catalogue 会成为工程组织的基础设施，个人 PM / engineer 的壁垒会转向设计这些 workflow 与 gate。

【机会】
最大机会不在：自己手动把 agent 用得很熟。
而在：把高频工作沉淀成可复用、可审计、可验证的 workflow。
因为：组织购买的是稳定产出和风险控制，不是个人炫技。

【核心判断】
这不是 GitHub 新增自动化功能问题，而是 AI agent 被纳入工程治理的问题。最大机会不在单次让 agent 写代码，而在把 triage、CI、docs、review、publish 变成可复用 workflow。所以不应该优先追求更强的 prompt，而应该先验证 workflow spec、validator、review gate 和发布记录。

【应该做什么】
把个人高频任务拆成 workflow：生成、校验、渲染、发布、记录、复盘。

【不应该做什么】
不要让 agent 绕过 validator、review gate 或发布记录。

【先验证什么】
验证一个自然语言任务能否稳定产出结构化文件，并通过 deterministic validator。

【关键假设】
个人竞争力会从会用 AI 工具，转向会设计 AI 工作流和治理闭环。

【验证指标】
工作流重复成功率、validator 通过率、人工返工率、发布失败率、可追溯记录完整率。

【最小可行方案】
以 Hermes daily 为样本，定义 `generate-md → validate → render-html → publish → archive` 的日期文件夹流水线。

【长期机会】
形成个人 AI PM Operating System：所有训练、分析、发布和复盘都可追溯、可复用、可审计。

【最大风险】
只追求视觉或自动化速度，忽略事实核验和结构校验，导致训练资产不可用。

如果我在面试或汇报中表达，我会这样说：

“我会从六层来看这个问题。
第一，现象上，GitHub Agentic Workflows 把自然语言 workflow 编译进 Actions。
第二，原因上，工程组织需要自动化，但不能绕过 policy 和安全。
第三，本质上，这不是 AI 自动写代码的问题，而是 agent 推理进入工程治理系统的问题。
第四，系统上，workflow spec、runner、policy、safe outputs、threat detection 和 reviewer 共同作用。
第五，趋势上，AI coding 会从个人工具转向组织级 workflow catalogue。
第六，机会判断上，最大机会不在更会 prompt，而在会设计可审计 workflow。

所以我的最终判断是，应该把个人高频任务沉淀成可验证 workflow。
不应该优先追求无边界自动执行。
而应该先验证 spec、validator、gate 和发布记录。”

【训练能力】
从行业产品发布反推个人能力壁垒。

【P6+ 易犯错误】
把 GitHub 的功能看成效率工具，而不是工程治理范式变化。

【P7+ 正确思路】
判断价值控制点在哪里：不是 agent 本身，而是 workflow、policy、gate 和审计。

【可复用 Pattern】
Agent Governance Loop = Spec → Execute → Validate → Review → Publish → Archive。

【迁移方式】
直接迁移到 Hermes：每日训练必须变成日期文件夹、MD、HTML、sources、case-pool、publish 记录的完整闭环。

【Case Asset Card】

Case 名称：GitHub Agentic Workflows 公测

所属方向：AI Coding / Agent Workflow / Review Gate / 工程治理

一句话现象：GitHub 让自然语言 agent workflow 进入 Actions 执行体系。

一句话本质：agent 正被工程化为可复用、可执行、可审计的 workflow。

核心矛盾：组织想要 AI 自动化，但必须保留权限、策略、审计和安全检查。

关键系统关系：Markdown spec 定义任务，Actions 执行任务，policy 和 firewall 控制风险，safe outputs 和 threat detection 增加信任。

价值流向：从个人 coding skill 流向组织级 workflow catalogue 和治理能力。

做 / 不做 / 先验证：做可验证 workflow；不做无审计自动执行；先验证 validator、review gate 和发布记录。

可复用 Pattern：Spec → Execute → Validate → Review → Publish → Archive。

可迁移到我的哪个项目：
- Hermes P7+ daily training：把每日训练做成日期文件夹和 HTML 发布流水线。

可迁移到哪类面试题：AI coding 时代，产品经理或工程负责人如何建立个人与组织壁垒？

2 分钟表达版本：GitHub Agentic Workflows 的关键不是自动做几个工程任务，而是把 agent 放进 Actions、policy、安全扫描和 review gate。它说明未来的壁垒不是会 prompt，而是会把 AI 变成可治理工作流。

未来 Watchlist：跟踪 public preview 的企业案例、prebuilt workflow 增长、security incident、Actions 集成变化。

关注对象：
- GitHub Agentic Workflows、GitHub Actions、GitHub Next agentics、企业工程平台团队。

关注指标：
- 产品是否继续迭代
- GitHub star / fork / release / issue 是否持续增长
- 是否出现付费客户 / 企业案例
- 是否出现竞品跟进
- 是否出现官方论文 / 技术突破
- 是否出现负面风险或监管事件

Watchlist 状态：
- 持续跟踪

资产等级：
- A

资产等级说明：
- A：可直接进入面试素材库 / 项目方法论库 / 个人知识库核心库。

复习优先级：
- 高

## 五、今日自主训练题

【今日自主训练题】

Case：
Hermes daily training 默认生成 HTML 链接，并按日期文件夹归档。

必要事实材料：
- 当前 Hermes skill 已经有 Markdown 模板和 validator。
- 新目标要求每日产物包括 MD、HTML、sources、case-pool、publish 记录。
- HTML 视觉和交互必须贴合 Hermes Markdown 结构，而不是普通 Markdown 美化。

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

## 六、旧 case 复现 / 遗忘曲线回顾

今天无已登记旧 case 可自动抽取，因此使用 Pattern recall：

- D0：请复述今天的核心 Pattern：Agent Governance Loop = Spec → Execute → Validate → Review → Publish → Archive。
- D1：明天用一句话复述 Gemini computer use 的本质、Notion + Cursor 的本质、GitHub Agentic Workflows 的本质。
- D3：三天后重做 GitHub Agentic Workflows 的 8 问。
- D7：一周后把“agent 治理系统”整理成 2 分钟面试回答。
- D14：两周后抽象成你的 Hermes HTML 发布系统方法论。

## 七、今日训练复盘

- 今天主要训练了什么能力：从 AI agent 产品发布中识别能力边界、工作流入口、治理控制点和个人壁垒。
- 今天最重要的 P7+ 思维动作：不把 agent 当功能，而是看它进入什么系统、被谁授权、如何验证、如何审计。
- 今天最容易犯的 P6+ 错误：看到 computer use、SDK、workflow 就直接想做功能，不先看风险、入口、价值流向和验证闭环。
- 今天沉淀了哪些 Case Asset Card：Gemini 3.5 Flash computer use、Notion 使用 Cursor SDK、GitHub Agentic Workflows。
- 哪些进入 Watchlist：OpenAI Codex role plugins、Hermes Agent v0.17.0、Mistral Connectors、xAI + Interactive Brokers、Figma Config AI canvas。
- 明天建议复习什么：复习 GitHub Agentic Workflows，并把它迁移成 Hermes daily 文件夹 + HTML 发布流水线的设计约束。

### Quality Review Rubric

| 维度 | 分数 1-5 | 简评 | 下一步如何补强 |
| --- | ---: | --- | --- |
| 事实可靠性 | 4 | 三个深度 case 均由官方或 primary source 支撑，AI HOT 只作信号。 | 补充更多企业真实采用数据和失败案例。 |
| 本质抽象深度 | 5 | 三个 case 都抽象到 agent 能力进入治理系统这一主线。 | 保持后续案例间的差异度，避免主题重复。 |
| 系统关系清晰度 | 5 | 已明确模型、SDK、host product、Actions、policy、audit 的系统关系。 | 后续 HTML 化时可用可视化组件增强系统关系。 |
| 趋势推演可信度 | 4 | 趋势从能力内置、对象级 agent、workflow governance 展开，方向清晰。 | 需要补更多连续时间序列和竞品数据。 |
| 机会判断质量 | 5 | 明确机会不在功能包装，而在可验证、可治理、可复用工作流。 | 下一步把机会落实到 Hermes renderer 设计。 |
| 取舍明确度 | 5 | 每个 case 都包含做、不做、先验证。 | 继续加强“不做”的负面案例证据。 |
| 验证方案可执行性 | 4 | 验证指标可执行，但还缺真实任务基线。 | 用今天的 Markdown 样本跑 HTML renderer 原型后补基线。 |
| Case Asset Card 可复用度 | 5 | 三张卡均可迁移到 Hermes daily HTML 发布系统和面试素材。 | 后续进入个人知识库时补标签与复习日期。 |
