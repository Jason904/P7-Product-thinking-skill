# V3 / V4 / V5 Gap Report - 2026-06-25

## 一、对比目标

本报告用于回答一个核心问题：

当前 Hermes skill 是否已经能稳定生成用户想要的高质量 Insight 内容？

对比对象：

- V3 benchmark：`training-v3.md`
- V4 raw：`training-v4-raw.md`
- V5 blind test：`training-v5-raw.md`

## 二、结构与验证证据

| 文件 | 行数 | deep case | Insight Audit | Asset Card | Validator | 说明 |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| training-v3.md | 1659 | 3 | 3 | 3 | PASS | benchmark，高质量参考。 |
| training-v4-raw.md | 1615 | 3 | 3 | 3 | PASS | 与 V3 case 高度相关，证明复现能力。 |
| training-v5-raw.md | 1867 | 3 | 3 | 3 | PASS | 新 case 盲测，证明力强于 V4。 |

Validator 证据：

```text
PASS: Hermes output conforms to the requested contract.
PASS: Hermes output conforms to the requested contract.
PASS: Hermes output conforms to the requested contract.
```

## 三、deep case 是否复用

| 版本 | deep case 主题 | 是否复用 V3/V4 deep case | 证明力 |
| --- | --- | --- | --- |
| V3 | Gemini computer use；Notion + Cursor SDK；GitHub Agentic Workflows | 不适用 | benchmark |
| V4 | Gemini computer use；Notion + Cursor SDK；GitHub Agentic Workflows | 是，高度重合 | 证明结构和复现，不证明盲测稳定 |
| V5 | Qwen-AgentWorld；xAI+IBKR；Codex Remote | 否 | 第一次真实盲测证据 |

V5 中旧 case 只出现在排除列表和遗忘曲线复盘，不属于 deep case 复用。

## 四、质量分数对照

| 版本 | Case | 思考深度 | 内容质量 | 表达质量 | 总分 | 判断 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| V3 | Gemini computer use | 42/45 | 28/30 | 24/25 | 94 | V3 级 |
| V3 | Notion + Cursor SDK | 39/45 | 27/30 | 22/25 | 88 | V3 级 |
| V3 | GitHub Agentic Workflows | 44/45 | 29/30 | 24/25 | 97 | V3 级 |
| V4 | Gemini computer use | 42/45 | 28/30 | 24/25 | 94 | V3 级 |
| V4 | Notion + Cursor SDK | 42/45 | 28/30 | 24/25 | 94 | V3 级 |
| V4 | GitHub Agentic Workflows | 44/45 | 29/30 | 24/25 | 97 | V3 级 |
| V5 | Qwen-AgentWorld | 43/45 | 28/30 | 24/25 | 95 | V3 级 |
| V5 | xAI+Interactive Brokers | 42/45 | 27/30 | 23/25 | 92 | V3 级 |
| V5 | OpenAI Codex Remote | 43/45 | 28/30 | 24/25 | 95 | V3 级 |

说明：以上分数是文件内 Insight Quality Audit 的结构化自评，不等于外部客观评分。本报告结合人工审计给出判断。

## 五、来源质量差距

| 维度 | V3 | V4 | V5 |
| --- | --- | --- | --- |
| Search / Web | 有 | 有，记录更明确 | 有，重新抓取且回原文 |
| AI HOT | 有 | 有，使用 daily + selected API | 有，使用 daily + selected API |
| GitHub / Open-source | 有 | 有，GitHub API 更明确 | 有，Qwen repo + repo search + OpenAI Agents Python |
| Primary source | 有 | 有 | 有 |
| C 级来源治理 | 有 | 更明确 | 更明确，OpenRouter 降级 Watchlist |

差距判断：

- V5 的来源治理达到 V4 水平。
- V5 的 deep case 不依赖 V3/V4 case，因此盲测价值更高。
- V5 仍有最新 case 的天然限制：商业采用、实际产品流程、用户数据不足。

## 六、Insight 深度差距

### V3

优势：

- Case 选择与用户讨论高度贴合。
- 三个 case 的核心 Insight 经过多轮打磨。
- 适合作为 benchmark。

限制：

- 部分候选池说明和链接溯源不如 V4/V5 完整。

### V4

优势：

- 结构、来源、质量审计显著增强。
- 与 V3 主题高度一致，复现深度较稳。

限制：

- 不是严格盲测；不能证明换 case 后仍稳定。

### V5

优势：

- 三个 deep case 全部更换。
- 三案都形成了非新闻复述的抽象：
  - Qwen-AgentWorld：环境反馈层。
  - xAI+IBKR：金融决策前工作台。
  - Codex Remote：工程控制平面。
- 每案都有反面论证、边界条件、做 / 不做 / 先验证。

限制：

- Case B 的实际产品流程和监管细节仍需补证。
- Case C 的效率提升仍需用户实验验证。
- 只有一次盲测，不能证明稳定。

## 七、三案同深度检查

| 检查项 | V5 Case A | V5 Case B | V5 Case C | 结论 |
| --- | --- | --- | --- | --- |
| Fact Confidence Table | 有 | 有 | 有 | 通过 |
| Insight 总览 | 有 | 有 | 有 | 通过 |
| 分析方法工作台 | 有 | 有 | 有 | 通过 |
| P7+ 追问深答 | 有 | 有 | 有 | 通过 |
| 8 问显性推理 | 有 | 有 | 有 | 通过 |
| 反面论证与边界 | 有 | 有 | 有 | 通过 |
| 6 层总结 | 有 | 有 | 有 | 通过 |
| PREP / SCQA | 有 | 有 | 有 | 通过 |
| Insight Audit | 95 | 92 | 95 | 通过 |
| Case Asset Card | 有 | 有 | 有 | 通过 |

结论：V5 没有出现 Case A 深、Case B/C 浅的问题。

## 八、是否证明稳定

当前不能说已经稳定。

已经证明：

- 当前 skill 在 V5 新 case 上可以生成 V3 级内容。
- 结构合约、来源记录、三案同深度、质量审计可以在盲测中保持。
- 分析方法可以产生洞察，而不是只堆名词。
- 表达层可用于面试 / 汇报 / 讨论。

尚未证明：

- 连续多次换 case 后仍然稳定。
- 不同来源强弱组合下仍然能正确降级 / 换 case。
- 如果 Case B/C 信息弱，skill 是否会稳定触发兜底机制。
- HTML Pro Max 是否能承载长内容阅读。

## 九、下一步判断

建议继续 V6 盲测，而不是进入 HTML Pro Max。

V6 要故意提高难度：

- 换一组完全不同 deep case。
- 至少包含一个来源较弱但热度高的 case，测试是否会正确降级。
- 至少包含一个 GitHub / open-source case，测试 GitHub 判断是否不只看 star。
- 继续保存 raw Markdown、HTML、quality report、gap report。

通过条件：

- V6 validator PASS。
- 三案总分均不低于 90，或若低于 90，要有充分扣分和补强。
- 三案都没有模板填充感。
- 至少一个 case 的反面论证能真正改变取舍判断。

## 十、阶段结论

V5 把证据从“V4 可以复现 V3”推进到了“新 case 盲测也可以达到 V3 级”。

但稳定性目标还没有完成。当前最严谨的结论是：

Hermes skill 已经显示出稳定生成高质量 Insight 内容的能力倾向；V5 是强正向证据。但至少还需要 V6 再次盲测通过，最好 V7 也通过，才能判断当前阶段目标完成，并决定是否进入 HTML Pro Max 和全局 skill 同步。
