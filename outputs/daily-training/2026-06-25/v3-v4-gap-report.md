# V3 vs V4 Raw 差距报告 - 2026-06-25

## 一、测试目标

本次测试不是为了再写一篇 polished 训练稿，而是验证新版 Hermes skill 在重新抓取来源后，能否稳定生成接近 `training-v3.md` 的内容质量。

测试对象：

- V3 benchmark：`training-v3.md`
- V4 raw：`training-v4-raw.md`

验收重点：

1. 结构合约是否稳定通过 validator。
2. 来源链路是否完整，是否使用 Search / AI HOT / GitHub。
3. 三个 deep case 是否都达到 Insight 级，而不是 Case A 深、Case B/C 浅。
4. 内容是否保留过程和结论：论点、论据、推导、反驳、回应、取舍。
5. 表达是否能用于面试、汇报和日常讨论。

## 二、执行证据

### 1. 文件生成

V4 raw 已保存：

`/Users/jiangsheng/Vibe_Coding/p7+思维skill/hermes-p7-product-thinking-package/outputs/daily-training/2026-06-25/training-v4-raw.md`

文件行数：

```text
1615 training-v4-raw.md
```

### 2. Validator 结果

V4 raw daily validator：

```text
PASS: Hermes output conforms to the requested contract.
```

V3 benchmark daily validator：

```text
PASS: Hermes output conforms to the requested contract.
```

Skill package quick validate：

```text
Skill is valid!
```

### 3. 结构检查结果

V4 raw 中检测到：

- 3 个完整 `【Case】`
- 3 个 `【Insight Quality Audit】`
- 3 张 `Case Asset Card`
- 8-13 个候选 case，实际为 10 个
- Search API / Web Search、AI HOT、GitHub / Open-source 三个来源通道均记录为已使用

## 三、V3 vs V4 分数对照

说明：下表是文件内 `Insight Quality Audit` 的自评得分，不等于外部客观评分。它适合作为结构化自检依据，但最终仍要结合人工抽审判断真实 Insight 深度。

| Case | V3 思考深度 | V3 内容质量 | V3 表达质量 | V3 总分 | V4 思考深度 | V4 内容质量 | V4 表达质量 | V4 总分 | 差距判断 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Gemini 3.5 Flash computer use | 42/45 | 28/30 | 24/25 | 94 | 42/45 | 28/30 | 24/25 | 94 | 基本持平 |
| Notion + Cursor SDK | 39/45 | 27/30 | 22/25 | 88 | 42/45 | 28/30 | 24/25 | 94 | V4 明显补强 |
| GitHub Agentic Workflows | 44/45 | 29/30 | 24/25 | 97 | 44/45 | 29/30 | 24/25 | 97 | 基本持平 |

## 四、质量差距判断

### 1. 来源质量

V4 相比 V3 的提升：

- 候选池中为每个 case 增加了“一句话描述、溯源链接、为什么是这个分数、处理方式”。
- AI HOT 权重被正确处理：提高关注权重，但不直接升级事实等级。
- V4 使用 AI HOT daily API 和 selected items API，来源记录更具体。
- GitHub case 补充了 GitHub API activity 作为开发者信号，但明确说明 star / fork / commit 不能等于商业成功。

剩余风险：

- Figma 等 C 级来源仍只能放 Watchlist，不能进 deep case。
- GitHub adoption 数据仍不足，GitHub Agentic Workflows 的长期判断仍需继续观察企业案例。

### 2. 思考深度

V4 达标点：

- 三个 case 都完成了从现象到本质的重构：
  - Gemini：从 computer use 能力升级，重构为企业执行授权系统。
  - Notion + Cursor：从产品集成，重构为业务对象执行权迁移。
  - GitHub：从自动化功能，重构为 agent work 被工程治理系统吸收。
- 三个 case 都有底层矛盾、因果机制、系统关系、反面论证和边界条件。
- 三个 case 都给出了明确做 / 不做 / 先验证。

V4 仍弱于理想状态的地方：

- 一些反面论证还可以加入真实反例，例如开放式 computer use 成功案例、低上下文产品接 agent 失败案例、GitHub workflow 采用失败案例。
- 趋势推演已经有阶段，但还缺更多外部采用数据支持时间节奏。

### 3. 表达质量

V4 达标点：

- 每个 case 都有六层表达、PREP、SCQA、被追问时回答。
- 记忆点更明确：
  - “能力默认化，治理稀缺化”
  - “协作对象开始拥有执行能力”
  - “Prompt 是技能，Workflow 是壁垒”

V4 可继续提升点：

- Case A 的 2 分钟表达还可以更短、更像真实面试口播。
- Case B 的表达已经比 V3 更清晰，但可以继续加一张“Notion / Cursor / GitHub 三方价值分工”的图，留给 HTML 阶段处理。

## 五、结论

当前结论：V4 raw **初步证明新版 skill 可以稳定生成 V3 级结构与接近 V3 的 Insight 深度**。

但这个结论有一个重要限制：这不是完全盲测。生成 V4 前，我已经读取过 V3 作为 benchmark，并且今天三个 deep case 与 V3 高度重叠。因此它证明的是：

- 新版 skill 的结构合约稳定；
- 质量治理字段稳定；
- 在同类 case 上可以复现 V3 深度；
- 来源链路和候选池说明比 V3 更完整。

它还不能完全证明：

- 换一天、换三组 case 后仍稳定；
- 没有 V3 作为显性 benchmark 时仍稳定；
- HTML 生成后阅读体验仍能承载这种长内容。

## 六、下一步建议

建议下一步按这个顺序推进：

1. 先人工抽审 V4 的三个高风险点，不全文重读：
   - Case A：治理机会是否真的比开放式代操更优。
   - Case B：object-bound agent 的洞察是否足够支撑 Hermes HTML 迁移。
   - Case C：多 gate Hermes pipeline 是否就是下一版 skill 的核心产品形态。

2. 如果人工抽审认可 V4 raw，则把 V3.1 Insight 标准固化进 skill 的 daily mode。

3. 再做 HTML 信息架构：
   - 首屏：Insight 总览、三 case 结论、来源可信度。
   - 第二层：候选池和选择理由。
   - 第三层：每个 case 的论证链路、8 问、方法工作台。
   - 第四层：表达演练和 Case Asset Card。
   - 侧栏：来源、Watchlist、Quality Audit、复习优先级。

4. 再做 renderer / daily folder pipeline：
   - `YYYY-MM-DD/training.md`
   - `YYYY-MM-DD/training.html`
   - `YYYY-MM-DD/sources.json`
   - `YYYY-MM-DD/quality-report.md`

5. 最后再考虑是否把项目包 skill 安装或同步到全局 skill。

## 七、我的判断

这次 V4 raw 的最大价值是证明：你要求的“信息质量优先于阅读负担”是可执行的。现在的问题不再是 skill 能不能写出长内容，而是要继续治理三件事：

- Insight 是否真有穿透力；
- 内容是否能持续溯源；
- HTML 是否能让长内容变得更好读，而不是把深度变成负担。

我建议暂时不要急着进入视觉层。先对 V4 raw 做一次人工定点抽审。如果这三个核心洞察你认可，我们再把它们变成 HTML 信息架构。
