# Failure Case Registry

## V7 内容退坡与网页空壳回流样本

【失败编号】  
HERMES-FB-2026-06-26-V7

【问题现象】  
- 用户在 `training-v7-reader.html#case-2` 看到 `8 问推理`只有结构卡片，内容为空，属于“8 问推理为空壳”。  
- 原始 V7 Markdown 曾出现“高分但内容浅”：多个 95 分以上 case 的 8 问推理和 Insight 总览不足以支撑分数。  
- 原始 V7 Markdown 曾出现“模板套话重复”：同一句结论性套话在多个深度 case 中反复出现。  
- 端到端盲测被误判为通过，说明验收流程没有把 Markdown 完整性、HTML 完整性和人工 Insight 审查分开处理。

【用户影响】  
- 用户无法通过网页看到完整推理过程，训练目标被破坏。  
- 用户会误以为 skill 已稳定生成高质量内容，但实际只通过了部分结构检查。  
- 对“每日训练是否可靠”的信任下降。

【根因归类】  
- 推理深度失败。  
- 表达模板化失败。  
- HTML 渲染失败。  
- 验收流程失败。

【根因判断】  
- 内容层：skill 对高分内容的深度约束不够硬，导致分数高于真实推理质量。  
- 表达层：没有拦截跨 case 重复的模板化结论。  
- 渲染层：reader 解析器没有完整支持 8 问字段的写法差异，导致 Markdown 有内容但 HTML 空壳。  
- 验收层：把端到端生成成功误当作质量通过，没有强制运行 HTML 内容完整性检查。

【回流动作】  
- 在 `validate_hermes_output.py` 增加高分深度门禁：高分 case 必须有足够的 8 问推理和 Insight 总览。  
- 在 `validate_hermes_output.py` 增加模板套话重复拦截。  
- 在 `render_training_reader_html.py` 修复 8 问字段解析，让 `目的：内容`与`目的：`换行内容都可被识别。  
- 新增 `validate_training_reader_html.py`，校验每个深度 case 的 8 问卡片和字段是否真实渲染。  
- 新增 `validate_failure_feedback.py`，校验失败回流登记是否完整。

【规则回流】  
- `SKILL.md`：每日 HTML 工作流必须先校验 Markdown，再渲染，再校验 reader HTML。  
- `references/framework.md`：补充失败回流闭环，要求严重失败必须登记、归因、回流规则、补测试、复测。  
- `references/templates.md`：补充失败案例登记模板。  
- `references/failure-feedback.md`：沉淀长期失败回流机制。  
- `references/failure-cases.md`：登记当前 V7 失败样本。

【测试回流】  
- `test_hermes_output_validator.py` 覆盖高分但内容浅、模板套话重复、质量自评与结构失败矛盾。  
- `test_render_training_reader_html.py` 覆盖 8 问字段解析和空字段 HTML 拦截。  
- `test_failure_feedback_loop.py` 覆盖失败回流文件、V7 样本和回流登记校验。  
- `verify_hermes_skill.py` 覆盖技能包必须包含失败回流机制、脚本和 V7 样本。

【门禁处理】  
- Markdown 未通过 `validate_hermes_output.py`：阻断发布。  
- HTML 未通过 `validate_training_reader_html.py`：阻断发布。  
- 失败登记未通过 `validate_failure_feedback.py`：不能关闭失败样本。  
- 人工 Insight 审查未达到标准：不能宣称稳定生成高质量内容。

【失败处理策略】  
- 如果内容浅：重写推理链或降低 Insight 分数。  
- 如果模板化：替换为 case-specific 论点、论据、推导和边界条件。  
- 如果 HTML 空壳：修 renderer，并补 HTML 完整性测试。  
- 如果验收误判：补验收命令和失败回流记录。

【复测证据】  
- `python3 -m unittest tests.test_hermes_output_validator`：PASS。  
- `python3 -m unittest tests.test_render_training_reader_html`：PASS。  
- `python3 -m unittest tests.test_failure_feedback_loop`：PASS。  
- `python3 skill/scripts/validate_failure_feedback.py skill/references/failure-cases.md`：PASS。  
- `python3 tests/verify_hermes_skill.py skill`：PASS。

【验收状态】  
当前记录用于关闭 V7 同类失败的机制缺口。只有当上述命令在当前工作树中真实通过时，状态才可视为 PASS。

【下次遇到同类问题】  
- 先定位属于内容层、模板层、渲染层、视觉层还是验收层。  
- 先补失败测试，再修规则或脚本。  
- 修复后必须同时跑 Markdown 校验、HTML 校验、失败回流校验和技能包复测。  
- 不允许只修当天文档后宣称 skill 已稳定。
