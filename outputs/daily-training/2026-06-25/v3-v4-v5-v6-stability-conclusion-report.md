# V3 / V4 / V5 / V6 Stability Conclusion Report - 2026-06-25

## 一、最终结论

当前阶段可以得出一个谨慎但明确的结论：

**Hermes P7+ 产品思维训练 skill 已经通过 V5 和 V6 两次连续盲测，证明它具备最低可接受的稳定生成高质量 Insight Markdown 内容的能力。**

但这个结论有边界：

- 可以说：当前 skill 已经不是只在 V3/V4 熟悉 case 上偶然生成好内容。
- 可以说：在换新 case、重新抓取来源、重新选择 3 个 deep case 的情况下，它仍能生成结构完整、来源可追溯、三案同深度、表达可用的 Insight 级内容。
- 不能说：它已经被证明可以长期跨日期、跨所有主题、完全自动稳定地产出同样质量。
- 不能说：HTML Pro Max 已经完成，因为本阶段暂停了视觉/交互优化。
- 不建议直接同步到全局 Hermes skill，除非用户接受“两次盲测通过即最低稳定”的同步门槛；更稳妥做法是先做 V7 或人工定点抽审。

## 二、验证对象

| 版本 | 文件 | 角色 | 说明 |
| --- | --- | --- | --- |
| V3 | `training-v3.md` | Benchmark | 用户认可的质量标准。 |
| V4 | `training-v4-raw.md` | 复现测试 | 与 V3 case 高度相关，证明结构和深度复现能力。 |
| V5 | `training-v5-raw.md` | 第一次盲测 | 更换 deep case，不复用 V3/V4。 |
| V6 | `training-v6-raw.md` | 第二次盲测 | 再次更换 deep case，不复用 V3/V4/V5。 |

## 三、执行证据

### 1. 文件规模

```text
1659 training-v3.md
1615 training-v4-raw.md
1867 training-v5-raw.md
1864 training-v6-raw.md
```

### 2. 结构数量

四个版本均满足：

```text
3 【Case】
3 【Insight Quality Audit】
3 【Case Asset Card】
```

这说明没有出现 Case A 完整、Case B/C 被压缩的结构性塌缩。

### 3. Validator 结果

四个版本分别运行：

```bash
python3 skill/scripts/validate_hermes_output.py --mode daily outputs/daily-training/2026-06-25/training-v3.md
python3 skill/scripts/validate_hermes_output.py --mode daily outputs/daily-training/2026-06-25/training-v4-raw.md
python3 skill/scripts/validate_hermes_output.py --mode daily outputs/daily-training/2026-06-25/training-v5-raw.md
python3 skill/scripts/validate_hermes_output.py --mode daily outputs/daily-training/2026-06-25/training-v6-raw.md
```

结果均为：

```text
PASS: Hermes output conforms to the requested contract.
```

说明：validator PASS 是最低结构门槛，不等于 Insight 质量通过。因此本报告继续使用人工式质量审计和差距比较。

### 4. 项目级测试

Skill 验证：

```text
PASS: Hermes skill verified at skill
```

Validator 单元测试：

```text
Ran 25 tests in 0.156s
OK
```

HTML renderer 单元测试：

```text
Ran 4 tests in 0.032s
OK
```

产物存在性检查：

- V5 Markdown / HTML / quality report / gap report 均存在且非空。
- V6 Markdown / HTML / quality report / source notes 均存在且非空。

## 四、盲测复用检查

### V3 / V4 deep cases

- Gemini 3.5 Flash computer use
- Notion + Cursor SDK
- GitHub Agentic Workflows

### V5 deep cases

- Qwen-AgentWorld
- xAI Grok + Interactive Brokers
- OpenAI Codex Remote

V5 没有复用 V3/V4 deep cases。

### V6 deep cases

- OpenAI + Broadcom Jalapeno 推理芯片
- Mistral Connectors 企业治理控制
- Google Thinking to Recall

V6 没有复用 V3/V4/V5 deep cases。

结论：V5 和 V6 均可视为有效盲测，不是围绕同一批熟悉 case 做变体复写。

## 五、质量分数对照

| 版本 | Case | 思考深度 | 内容质量 | 表达质量 | 总分 | 判断 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| V3 | Gemini computer use | 42/45 | 28/30 | 24/25 | 94 | Benchmark 通过 |
| V3 | Notion + Cursor SDK | 39/45 | 27/30 | 22/25 | 88 | Benchmark 通过 |
| V3 | GitHub Agentic Workflows | 44/45 | 29/30 | 24/25 | 97 | Benchmark 通过 |
| V4 | Gemini computer use | 42/45 | 28/30 | 24/25 | 94 | 复现通过 |
| V4 | Notion + Cursor SDK | 42/45 | 28/30 | 24/25 | 94 | 复现通过 |
| V4 | GitHub Agentic Workflows | 44/45 | 29/30 | 24/25 | 97 | 复现通过 |
| V5 | Qwen-AgentWorld | 43/45 | 28/30 | 24/25 | 95 | 盲测通过 |
| V5 | xAI + Interactive Brokers | 42/45 | 27/30 | 23/25 | 92 | 盲测通过 |
| V5 | OpenAI Codex Remote | 43/45 | 28/30 | 24/25 | 95 | 盲测通过 |
| V6 | OpenAI + Broadcom Jalapeno | 42/45 | 28/30 | 23/25 | 93 | 盲测通过 |
| V6 | Mistral Connectors | 43/45 | 29/30 | 24/25 | 96 | 盲测通过 |
| V6 | Google Thinking to Recall | 43/45 | 28/30 | 24/25 | 95 | 盲测通过 |

重要说明：

- 这些分数来自文件内 `Insight Quality Audit` 的结构化自评，不等于外部客观评分。
- 本报告接受分数的前提是：每个 case 都提供了证据、扣分原因和补强动作。
- V5/V6 每个 deep case 总分均 >= 90，且单项分数达到用户设定门槛。

## 六、已经证明了什么

### 1. 结构稳定性已经证明

证据：

- V3/V4/V5/V6 validator 全部 PASS。
- 每个版本都有 3 个 deep case。
- 每个版本都有 3 个 Insight Quality Audit。
- 每个版本都有 3 个 Case Asset Card。

判断：

skill 当前能稳定生成 daily mode 所需的完整结构，不再只是单 case 强、后两个 case 浅。

### 2. 两次盲测稳定性已经证明到最低门槛

证据：

- V5 更换为 Qwen-AgentWorld、xAI+IBKR、Codex Remote。
- V6 更换为 Jalapeno、Mistral Connectors、Thinking to Recall。
- 两次都没有复用 V3/V4 deep case。
- 两次都通过 validator 和人工质量审计。

判断：

skill 具备跨 case 生成 V3 级内容的能力，不是只会复刻 benchmark。

### 3. 来源链路治理基本稳定

证据：

- V5/V6 都记录 Search / Web、AI HOT、GitHub / open-source、primary sources。
- AI HOT 被明确定位为 C 级信号。
- final judgment 使用官方公告、GitHub repo/API、paper、company blog、release notes 等 primary sources。
- 来源不足的信号被降级为 Watchlist 或 radar。

判断：

skill 已经具备基本事实治理能力：不把 AI HOT 或社区热度直接当事实。

### 4. 三案同深度基本稳定

证据：

- V5/V6 都有 3 个完整 deep case。
- 每个 deep case 都包含 Insight 总览、分析方法工作台、P7+ 追问深答、8 问、6 层总结、PREP、SCQA、Insight Audit、Asset Card。
- V5/V6 没有出现 Case B/C 简写、降级、或只留结论的问题。

判断：

用户最担心的“Case A 深，Case B/C 浅”在这两次盲测中没有发生。

### 5. 分析方法不是单纯堆名词

证据：

- V5/V6 的方法工作台说明了为什么使用、拆解维度、关键发现、支撑的 Insight。
- 每个 case 的最终判断与方法输出之间存在可追踪关系。
- Thinking to Recall case 还把 Hermes 自身训练机制作为分析对象，证明方法层可以回到用户个人成长目标。

判断：

当前 skill 已经能让分析方法产生推导，而不是只当装饰。

### 6. 表达层可以用于面试 / 汇报 / 讨论

证据：

- V5/V6 每个 deep case 都有 2 分钟表达、PREP、SCQA、被追问回应。
- 表达不是只复述结论，而是把现象、原因、本质、系统、趋势、机会和取舍串起来。

判断：

表达层达到了用户要求的“能讲出来、能演练、能体现深度思考过程”的最低门槛。

## 七、还没有证明什么

### 1. 还没有证明 3 次连续盲测

用户标准是“至少 2 次，最好 3 次”。当前已经满足最低标准，但没有满足更强标准。

建议：

- 如果要更强信心，继续 V7。
- V7 应至少包含一个 GitHub/open-source deep case，测试开源项目深度分析稳定性。

### 2. 还没有证明跨日期长期稳定

V5/V6 都在 2026-06-25 这一天完成。它们证明同日多轮换 case 稳定，不证明未来每天都稳定。

建议：

- 后续至少再选 1-2 个不同日期做回归测试。
- 特别测试来源质量较弱、热点噪音较多的日期。

### 3. 还没有证明完全自动化稳定

本轮由 Codex 在目标约束下执行，且有明确 benchmark 和质量报告约束。它证明 skill 可以被执行出高质量结果，但还不能证明任意模型、任意上下文下都会自动达标。

建议：

- 后续可以把质量审计流程脚本化，减少执行者主观差异。
- 可以增加 validator 对 Insight Audit 分数、扣分理由、case 数量、禁用词、来源记录的更严格检查。

### 4. 还没有证明用户学习效果

输出质量高，不等于用户的思维能力已经被训练起来。

建议：

- 后续增加“用户复述评分”。
- 增加 60 秒口播版本和追问演练。
- 用 D1 / D3 / D7 遗忘曲线检查用户是否能迁移 Pattern。

### 5. 还没有证明 HTML Pro Max 阅读效果

V5/V6 的 HTML 只是普通阅读产物，不是视觉和交互优化版本。

建议：

- HTML Pro Max 下一阶段应服务内容层：先看 Insight、结论、论证链，再展开事实、方法、8 问、表达、Asset Card。

## 八、是否可以进入 HTML Pro Max 阶段

结论：**可以进入 HTML Pro Max 的方案设计阶段，但不要把它理解成内容验证已经“完美完成”。**

理由：

- 当前内容层已经通过最低稳定性门槛。
- V5/V6 都证明 Markdown 可以稳定达到 V3 级深度。
- HTML 下一阶段的任务是降低阅读负担、强化信息架构、让长内容更易读，而不是压缩内容。

建议进入方式：

1. 保持 Markdown 深度不变。
2. HTML 只做阅读层组织：
   - Insight 总览优先。
   - 结论和论证链优先。
   - 事实、方法、8 问、表达演练、Asset Card 可折叠。
3. 每日仍按日期文件夹保存。
4. HTML 不能删除任何 reasoning content。

如果用户希望更高确定性，则先做 V7，再进入 HTML Pro Max。

## 九、是否可以同步到全局 Hermes skill

结论：**不建议立刻自动同步到全局 Hermes skill；建议先由用户确认最低稳定标准是否足够。**

原因：

- 当前已经达到“两次盲测通过”的最低标准。
- 但还没有完成第三次盲测和跨日期测试。
- 全局同步会影响日常使用，最好在用户确认后执行。

推荐决策：

- 如果目标是尽快进入下一阶段：可以先进入 HTML Pro Max 方案设计，暂不全局同步。
- 如果目标是最大化质量确定性：先做 V7，再同步全局。
- 如果用户接受最低稳定门槛：可以把当前本地 package skill 作为同步候选。

## 十、是否需要修 skill / template / validator

当前不需要因为失败而修 skill / template。

理由：

- 没有出现来源不足却强行 deep case 的失败。
- 没有出现 Case B/C 深度塌缩。
- 没有出现分析方法空转。
- 没有出现只有结论没有论证。
- 没有出现 PREP / SCQA 缺失。
- 没有出现评分无扣分理由。

但建议后续增强 validator：

1. 检查 `【Insight Quality Audit】` 是否正好 3 个。
2. 检查 `【Case Asset Card】` 是否正好 3 个。
3. 检查每个 deep case 是否包含 PREP / SCQA / 被追问回应。
4. 检查候选池是否至少 8 行。
5. 检查是否出现 `精简版`、`简版`、`因篇幅控制` 等禁用词。
6. 检查 Insight Audit 表格是否包含 `扣分原因` 和 `补强动作`。

这些不是当前阶段的阻塞项，而是把“人工审计经验”继续固化为机器检查的下一步。

## 十一、可复用的 Hermes 内容质量稳定性测试流程

以后每次升级 Hermes skill，按这个流程测试：

### Step 1：确定 benchmark

- 选择用户已认可的一版训练稿作为 benchmark。
- 明确它的质量标准：Insight 深度、来源治理、表达可用性、Asset Card 可复用度。

### Step 2：做复现测试

- 用同类 case 或相关 case 生成一版 raw Markdown。
- 目的不是证明稳定，而是检查模板、结构、validator、renderer 是否正常。

### Step 3：做第一次盲测

- 换新 case。
- 不复用 benchmark deep case。
- 重新抓取 Search / Web、AI HOT、GitHub / open-source、primary sources。
- 保存 raw Markdown，不先人工润色。
- 跑 validator。
- 写 quality report。

### Step 4：做第二次盲测

- 再换一组新 case。
- 不复用前一轮 deep case。
- 同样保存 raw、HTML、source notes、quality report。
- 如果连续两次通过，可以判定达到最低稳定门槛。

### Step 5：可选第三次盲测 / 人工抽审

- 如果要进入全局同步或长期自动化，建议做 V7。
- V7 应故意测试薄弱模块，例如 GitHub/open-source deep case、来源较弱但热度高的 case、商业化证据不足的 case。

### Step 6：失败兜底

按失败类型处理：

| 失败类型 | 判定 | 修复动作 |
| --- | --- | --- |
| 来源不足还强行 deep case | 来源治理失败 | 降级 Watchlist，补 Source Fallback Rule。 |
| Case B/C 变浅 | 三案同深度失败 | 补 Daily Deep Case Completeness Rule。 |
| 方法只列名词 | 方法空转失败 | 强制写拆解维度、发现、结论、支撑 Insight。 |
| 只有结论没论证 | Insight 链路失败 | 补 `论点 -> 论据 -> 推导 -> 反驳 -> 边界 -> 取舍`。 |
| 表达不可复述 | 表达训练失败 | 补 PREP、SCQA、2 分钟口播、被追问回应。 |
| 评分虚高 | 审计失败 | 要求每项都有证据、扣分原因、补强动作。 |
| 多次同模块失败 | skill 规则不足 | 暂停生成，先修 skill / templates / validator。 |

### Step 7：最终结论

最终报告必须回答：

- 已经证明了什么。
- 还没有证明什么。
- 是否达到最低稳定门槛。
- 是否建议进入 HTML。
- 是否建议同步全局 skill。
- 下一步最小动作是什么。

## 十二、最终判断

当前目标的完成判断：

| 要求 | 当前证据 | 判断 |
| --- | --- | --- |
| 暂停 HTML Pro Max | 本轮只生成普通 HTML，不做视觉优化。 | 达成 |
| 至少 2 次盲测 | V5、V6 两次盲测通过。 | 达成 |
| 每次 3 个 deep case | V5/V6 各 3 个。 | 达成 |
| 没有 Case B/C 深度塌缩 | V5/V6 均有完整结构和 Insight Audit。 | 达成 |
| 来源链路完整 | V5/V6 均有 Search / Web、AI HOT、GitHub / open-source、primary sources。 | 达成 |
| 分析方法产生洞察 | V5/V6 方法工作台与最终判断有连接。 | 达成 |
| PREP / SCQA / 2 分钟表达可用 | V5/V6 均包含。 | 达成 |
| 质量报告解释扣分和补强 | V5/V6 quality report 已生成。 | 达成 |
| 出现不稳定则修回 skill | 本轮没有 fatal instability。 | 不触发 |
| 最终稳定性报告 | 本文件。 | 达成 |

所以，本阶段可以判定为：

**内容层最低稳定性验证完成。**

下一步建议：

1. 若追求速度：进入 HTML Pro Max 信息架构与视觉方案设计。
2. 若追求更强证据：先跑 V7，重点测试 GitHub/open-source deep case。
3. 若要同步全局 Hermes skill：先让用户确认是否接受当前“两次盲测通过”的最低稳定性标准。
