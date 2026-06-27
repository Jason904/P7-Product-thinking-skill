# Training V5 Quality Report - 2026-06-25

## 一、结论先行

V5 是本轮稳定性验证的第 1 次盲测。它已经证明：在不复用 V3/V4 三个 deep case 的情况下，当前 Hermes skill 可以生成一篇结构完整、来源链路完整、三案同等深度、达到 training-v3 门槛的 raw Markdown。

但这还不能证明“稳定”。根据目标标准，至少需要连续 2 次，最好 3 次盲测通过，才能判断 skill 已经稳定。当前结论应表述为：

- V5 通过结构 validator。
- V5 通过本轮人工质量审计。
- V5 支持“skill 有能力在新 case 上产出 V3 级内容”的初步判断。
- V5 不足以单独证明长期稳定，需要继续 V6/V7。

## 二、本次是否为盲测

是。V5 重新抓取今日 / 近期候选 case，并明确排除了 V3/V4 的三个 deep case：

- Gemini 3.5 Flash computer use
- Notion + Cursor SDK
- GitHub Agentic Workflows

核查结果：

- V5 deep case 1：Qwen-AgentWorld。
- V5 deep case 2：xAI Grok + Interactive Brokers。
- V5 deep case 3：OpenAI Codex Remote。

旧 case 只出现在开头排除列表和遗忘曲线回顾区，不作为 deep case 复用。

## 三、执行证据

### 1. 文件生成

- Markdown：`outputs/daily-training/2026-06-25/training-v5-raw.md`
- HTML：`outputs/daily-training/2026-06-25/training-v5-raw.html`

文件规模：

```text
1867 lines training-v5-raw.md
114K  training-v5-raw.md
142K  training-v5-raw.html
```

结构数量：

```text
3 【Case】
3 【Insight Quality Audit】
3 【Case Asset Card】
10 candidate cases
```

### 2. Validator 结果

```text
PASS: Hermes output conforms to the requested contract.
```

同轮核查 V3/V4/V5：

```text
PASS: Hermes output conforms to the requested contract.
PASS: Hermes output conforms to the requested contract.
PASS: Hermes output conforms to the requested contract.
```

说明：validator PASS 只证明结构门槛，不证明 Insight 质量。

### 3. Skill 与脚本测试

项目级验证：

```text
PASS: Hermes skill verified at skill
```

Validator 单元测试：

```text
Ran 25 tests in 0.129s
OK
```

HTML renderer 单元测试：

```text
Ran 4 tests in 0.026s
OK
```

测试限制：

- 系统 `python3 -m pytest` 不可用，报错为 `No module named pytest`。
- 已改用测试文件内置的 `unittest.main()` 直接运行，测试通过。

## 四、来源通道是否完整

| 来源通道 | 本次状态 | 证据 | 质量判断 |
| --- | --- | --- | --- |
| Search API / Web Search | 完整 | 查询 Qwen-AgentWorld、xAI+IBKR、Codex Remote、Mistral Connectors；回到官方 / 论文 / GitHub 原文。 | 达标 |
| AI HOT | 完整 | 调用 `/api/public/daily/2026-06-25` 和 `/api/public/items?mode=selected&since=...`。 | 达标；仅作为 C 级信号。 |
| GitHub / Open-source | 完整 | GitHub API 查询 Qwen-AgentWorld、created-after agent repos、openai-agents-python。 | 达标；star/fork 未被当作最终事实。 |
| Primary sources | 完整 | Qwen GitHub/arXiv/blog，xAI News，IBKR press release，OpenAI Developers，Mistral News。 | 达标 |

来源治理结论：

- AI HOT 作为候选信号和关注权重来源使用，没有直接支撑最终判断。
- Qwen-AgentWorld 和 xAI+IBKR 都有 AI HOT 信号与 primary source 双重支撑。
- Codex Remote 没有进入 AI HOT 今日精选，但有 OpenAI 官方来源，且与 Case C 个人壁垒目标高度相关。
- OpenRouter MCP 因官方页面核验不稳，被降级为 Watchlist，符合来源兜底策略。

## 五、候选池质量评估

候选池共 10 个 case，符合 8-13 个要求。

优点：

- 每个 case 都有一句话描述、溯源链接、评分解释和处理方式。
- 覆盖 Agent world model、金融 agent、AI Coding workflow、enterprise connectors、GitHub governance、MCP、Eval、AI Coding 组织实践。
- Case Selection Score 使用了阈值处理，不是只按最高分选择。
- 热点但可验证性不足的 OpenRouter MCP 被降级 Watchlist。
- 与 V4 重复度高的 GitHub Copilot / Mistral 被放入雷达或 Watchlist，避免 deep case 主题重复。

不足：

- 部分 Watchlist 仍依赖 AI HOT / 公众号 / 二手来源，不能用于最终判断。
- 候选池中产品采用、商业化和用户留存数据普遍不足，这是最新 case 的天然限制。

## 六、三个 deep case 逐案评分

| Case | 思考深度 | 内容质量 | 表达质量 | 总分 | 是否达标 | 人工审计判断 |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| Qwen-AgentWorld | 43/45 | 28/30 | 24/25 | 95/100 | 是 | Insight 成立，机制清楚，机会判断可迁移。 |
| xAI Grok + Interactive Brokers | 42/45 | 27/30 | 23/25 | 92/100 | 是 | Insight 成立，但监管和产品实际流程仍需补证据。 |
| OpenAI Codex Remote | 43/45 | 28/30 | 24/25 | 95/100 | 是 | Insight 成立，和用户个人成长目标高度相关。 |

### Case A：Qwen-AgentWorld

核心 Insight：
Agent 的稀缺资源正在从 action generation 迁移到可复现、可控、可评测的环境反馈层。

成立理由：

- 事实层有 GitHub、arXiv、Qwen blog 支撑。
- 推导链完整：真实执行风险高 → 需要低风险模拟 → 模拟反馈可作为训练 / 预检 / eval gate → 价值迁移到环境和失败样本。
- 反面论证成立：模拟可能失真；因此先验证 simulation-to-real 相关性。
- 表达可用于面试：从模型发布重构为 agent 可靠性基础设施。

扣分点：

- 缺少社区复现实验和真实企业任务数据。
- 需要后续观察 repo 活跃、二次项目和 benchmark 复现。

### Case B：xAI Grok + Interactive Brokers

核心 Insight：
金融 agent 的早期机会不在自动交易，而在 broker 内可解释、可审批、可追责的决策前工作台。

成立理由：

- 事实层有 xAI 与 IBKR 官方来源支撑。
- 推导链完整：账户上下文降低决策摩擦 → 订单指令接近执行 → 金融风险要求确认 / 解释 / 审计 → 机会落在决策前工作台。
- 反面论证成立：这可能只是营销集成，用户授权和监管仍待验证。
- 表达能用于产品讨论：明确做 / 不做 / 先验证。

扣分点：

- 产品实际界面、确认机制、合规说明暂未完全核验。
- 商业效果和用户采用数据不足。

### Case C：OpenAI Codex Remote

核心 Insight：
AI Coding 的个人壁垒正在从会用 agent 迁移到会设计可远程治理、可审查、可恢复、可复盘的工程控制平面。

成立理由：

- 事实层有 OpenAI 官方开发者文章支撑。
- 推导链完整：agent 异步执行增强 → 人类控制节点变重要 → goal/worktree/approval/review/test 成为控制平面 → 个人壁垒迁移到 workflow governance。
- 与用户当前目标强相关：Hermes V5/V6/V7 盲测本身就是质量治理流程。
- 表达有迁移性：Prompt 是技能，workflow governance 是壁垒。

扣分点：

- 还缺少用户级真实效率数据。
- 需要用 V6/V7 继续验证这个 workflow governance 判断。

## 七、表达质量评估

V5 每个 case 都包含：

- 6 层结构化表达。
- 2 分钟表达版本。
- PREP 表达版本。
- SCQA 表达版本。
- 被追问时的回答。

可用性判断：

- 面试可用：是。
- 汇报可用：是。
- 日常讨论可用：是。
- 复习记忆可用：是。

主要不足：

- 三个 case 的 2 分钟表达仍略长，后续可在 HTML 或复习卡中追加 60 秒版本。
- Case B 的监管边界表达还可以更精炼。

## 八、与 V3/V4 的差距

V5 相比 V3：

- 优点：候选池说明和来源治理更完整；AI HOT 溯源和 Watchlist 降级更明确；三个新 case 没有依赖 V3 原 case。
- 持平：三案都有 Insight 总览、方法工作台、P7+ 追问、8 问、PREP/SCQA、Asset Card。
- 风险：V5 是 raw 生成，部分表达更长；Case B 的监管和产品实际流程证据弱于 V3 中已有官方技术说明的 case。

V5 相比 V4：

- 优点：V5 是更接近真实盲测的证据，因为 deep case 全部更换。
- 持平：结构 validator、三案同深度、来源记录、质量审计都通过。
- 风险：V4 的 case 与 V3 benchmark 高度相关，质量更容易对齐；V5 证明力更强，但只有一次。

## 九、是否达到稳定性标准

当前 V5 单次结果：达到。

整体稳定性结论：尚未完成证明。

原因：

- 用户目标要求至少连续 2 次，最好 3 次盲测通过。
- 当前只有 V5 一次真正盲测通过。
- 需要继续 V6/V7，观察是否仍能保持三案同深度、来源完整、方法不空转、表达可用。

## 十、失败风险与兜底判断

本次没有 fatal failure，但发现以下稳定性风险：

| 风险 | 当前表现 | 兜底策略 |
| --- | --- | --- |
| 最新 case 来源不足 | OpenRouter MCP 官方页面核验不稳。 | 已降级 Watchlist，不进入 deep case。 |
| Case B 监管事实不足 | xAI+IBKR 有官方来源，但流程细节不足。 | 保留为待验证假设，不把自动交易当事实。 |
| Case C 不是 AI HOT 精选 | Codex Remote 未由 AI HOT 今日精选触发。 | 用 OpenAI 官方来源与个人壁垒相关性支撑选择。 |
| 自评分虚高风险 | 每个 case 都写了扣分原因和补强动作。 | V6/V7 继续人工审计，不能只看分数。 |
| Markdown 长度继续增加 | V5 1867 行，信息质量优先。 | HTML 阶段再解决阅读负担，不在内容层压缩。 |

## 十一、下一步应该修什么

当前不建议马上修 skill / template / validator。

理由：

- V5 已通过结构 validator。
- 三案同深度没有塌缩。
- 分析方法没有明显空转。
- PREP / SCQA / 2 分钟表达都存在并可用。

更合理的下一步：

1. 继续 V6 盲测，换一组新 case。
2. V6 仍通过后，再做 V7 或进入人工定点抽审。
3. 如果 V6/V7 出现同一模块失败，再回写 skill / templates / validator。

## 十二、当前质量结论

V5 可以判定为：单次盲测通过，质量达到 V3 级。

但不能判定为：skill 已经稳定。

更准确的阶段结论是：

当前 Hermes skill 已经具备生成高质量 Insight 内容的能力；V5 是第一个强证据。但稳定性还需要 V6/V7 连续盲测证明。下一步应该继续盲测，而不是进入 HTML Pro Max。
