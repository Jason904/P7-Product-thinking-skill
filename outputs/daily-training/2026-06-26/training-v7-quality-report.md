# Training V7 Quality Report - 2026-06-26

## 结论

本轮 2026-06-26 端到端盲测通过。当前 Hermes P7+ skill 包已经可以从当日来源搜索、候选池构建、深度 MD 生成、结构校验、reader HTML 生成，到浏览器烟测形成完整闭环。

需要诚实说明：这次证明的是“在今天换新 case 后可以稳定跑出 V3/V6 级别结构和接近当前 reader 体验的输出”，不是证明未来永远不需要人工审阅。对 Insight 高低的最终把关仍建议保留人工抽查，但目前自动化链路已经具备可重复运行基础。

## 本轮生成物

- `training-v7-raw.md`
- `training-v7-reader.html`
- `source-notes-v7.md`
- `v7-smoke-desktop-fixed.png`
- `v7-smoke-mobile-fixed.png`

## 今日 deep case

| Case | 标题 | 角色 | Insight Audit |
| --- | --- | --- | ---: |
| Case A | OpenRouter MCP Server 模型路由进入 Agent 工具链 | 外部变化 / AI 基础设施 / 模型治理 | 96/100 |
| Case B | Runway Agent 2.0 从生成资产走向营销实验闭环 | 产品 / 商业趋势 / Creative AI workflow | 97/100 |
| Case C | Vercel Eve 文件系统优先的 Durable Agent 框架 | 个人壁垒 / GitHub open-source / Agent workflow | 96/100 |

## 来源使用证据

| 来源通道 | 结果 |
| --- | --- |
| Search API / Web Search | 已用；回到 OpenRouter、Runway、Anthropic、IBM、Hugging Face 等官方或 primary source。 |
| AI HOT | 已用；调用 2026-06-26 daily 与 selected items，发现 Runway、Claude Code、Anthropic Economic Index、Codex mobile GA 等信号。 |
| GitHub / Open-source | 已用；查询 vercel/eve、PixelRAG、MiMo-Code、Omnigent、claude-code release 等。 |

## 自动校验证据

| 检查项 | 结果 |
| --- | --- |
| `validate_hermes_output.py --mode daily training-v7-raw.md` | PASS |
| `render_training_reader_html.py training-v7-raw.md` | PASS，生成 `training-v7-reader.html` |
| `python3 -m py_compile render_training_reader_html.py` | PASS |
| `python3 -m unittest test_hermes_output_validator.py test_render_training_reader_html.py` | PASS，28 tests OK |
| `verify_hermes_skill.py skill` | PASS |

## 浏览器烟测证据

| 检查项 | 结果 |
| --- | --- |
| 本地 HTTP 打开页面 | PASS，页面标题为 `P7+ 产品思维每日训练 - 2026-06-26` |
| 控制台错误 | 0 errors / 0 warnings |
| DOM 内容 | 12 个 candidate cards，10 个 radar cards，3 个 case cards，38 个外链 |
| 移动端横向溢出 | 初测发现 `document.scrollWidth=424`、`clientWidth=390`；已修复 renderer 后复测为 `document.scrollWidth=390`、`clientWidth=390` |
| 表格移动端表现 | 保留局部横向滚动，页面整体不再横滑 |

## 本轮发现并修复的问题

问题：移动端页面出现约 34px 横向溢出。

根因：Markdown 表格设置了较大的 `min-width`，虽然外层 `.table-wrap` 有 `overflow-x:auto`，但内部 table 的可滚动宽度仍会计入文档横向 scrollWidth。

修复：在 reader HTML renderer 中增加整体横向隐藏和表格局部滚动约束：

- `html { overflow-x: hidden; }`
- `body { overflow-x: hidden; }`
- `.table-wrap { max-width: 100%; min-width: 0; overscroll-behavior-inline: contain; }`

影响：这是 renderer 层修复，以后每日生成的 HTML 都会继承，不是只修今天的 HTML。

## 距离目标还差什么

| 维度 | 当前状态 | 剩余差距 |
| --- | --- | --- |
| 内容搜索 | 已能三源抓取、回 primary source、降级未核验信息 | 需要把 AI HOT item 详情、GitHub trending、官方来源抽取流程进一步脚本化，减少人工拼接 |
| MD 质量 | 本轮 3 个 case 均达到 validator 和 Insight Audit 高分 | Insight 高低仍需人工抽查，尤其要避免高分表格自评过度乐观 |
| HTML 生成 | 已能生成当前 reader 结构、移动端可打开、表格不撑宽 | 视觉高级感仍可继续打磨，但不阻塞“稳定生成当前版本” |
| 质量治理 | validator + unit tests + browser smoke 已跑通 | 可增加自动截图 diff、链接可达性抽检、候选池来源完整性审计 |

## 最终判断

当前 skill 已经达到“可以稳定生成当前版本 HTML 的端到端基础水平”。如果目标是正式每日使用，建议下一步把本轮 V7 流程固化进 SKILL.md / framework / templates：

- 每日输出固定落入 `outputs/daily-training/YYYY-MM-DD/`
- 默认生成 `training-*-raw.md`、`training-*-reader.html`、`source-notes-*`、`quality-report`
- HTML 只在聊天里给链接
- 保留 validator、unit tests、browser smoke 作为质量门禁
- 对 Insight 高低设置人工抽查机制，而不是完全依赖自评分
