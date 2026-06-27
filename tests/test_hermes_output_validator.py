#!/usr/bin/env python3
"""Regression tests for the Hermes output conformance validator."""

from __future__ import annotations

import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


VALIDATOR_PATH = Path(__file__).resolve().parents[1] / "skill" / "scripts" / "validate_hermes_output.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_hermes_output", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Cannot import validator at {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SINGLE_CASE_OK = """
【Case】
AI 3D Agent 从生成模型走向空间工作流
【类型】
3D AI / Agent Workflow
【背景事实】
已确认事实：官方文档显示产品支持场景编辑。
行业观点：开发者正在关注可控工作流。
个人推断：价值会从单次生成迁移到可交付链路。
待验证假设：企业愿意为验收能力付费。
【信息来源】
官方文档、GitHub repo
【为什么值得分析】
它能训练从生成能力到产品化系统的判断。
【本次训练目标】
判断 3D AI 的价值控制点。

| 事实 | 来源 | 事实等级 | 是否可用于最终判断 | 是否需要继续核验 |
| ---- | ---- | -------- | ------------------ | ---------------- |
| 支持场景编辑 | 官方文档 | A | 是 | 否 |

【P6+ 第一反应】
一个执行型产品经理可能会直接想：做一个 text-to-3D 生成功能。
【这个思路对在哪里】
它有价值的地方是：抓到了生成效率。
【这个思路为什么不够】
它的问题不是错，而是太早进入：功能方案。
【P7+ 刹车动作】
先不问“怎么做”，而要先问：谁在什么场景损失最大？

【V3.1 Insight 总览】

一句话 Insight：AI 3D 的机会不在一次性生成，而在可编辑、可复用、可交付的空间工作流。

核心判断：这不是 3D 生成问题，而是空间工作流交付问题。

行动取舍：
- 做：编辑、验收、导出工作流。
- 不做：只堆生成效果。
- 先验证：企业是否愿意为验收效率付费。

【异常信号】
异常点是 3D AI 从生成初稿进入编辑、验收和发布链路。

【V3.1 分析方法工作台】

| 分析方法 | 为什么用 | 拆解维度 | 关键发现 | 支撑的 Insight |
| --- | --- | --- | --- | --- |
| JTBD | 找真实雇佣任务 | 生成、编辑、验收、发布 | 用户买的是稳定交付 | 机会在工作流 |

【P7+ 追问深答】

追问：为什么不是单次生成？
深度回答：企业采用需要可控交付，单次生成不能解决验收和复用。
推导依据：工作流成本集中在修改、沟通、验收。
可能反驳：生成质量提高后就够了。
回应反驳：生成质量提高降低初稿成本，但不会消除验收责任。
阶段结论：价值控制点在可交付工作流。
对最终判断的影响：优先做编辑、验收和导出闭环。

【底层矛盾与因果机制】
底层矛盾是低成本生成和可控交付之间的张力。

【系统关系与价值迁移】
价值从模型生成流向编辑、验收、治理和发布。

【反面论证与边界条件】
如果生成模型能直接输出企业可验收资产，工作流机会会被压缩。

【8 问显性推理】

1. 谁？
目的：识别核心对象。
分析方法：利益相关者地图。
为什么用这个方法：对象复杂。
推导过程：区分设计师、企业培训团队、付费者。
阶段结论：核心对象是企业内容团队。
如何影响下一步：进入场景判断。
2. 在哪？
目的：定位关键场景。
分析方法：场景分层。
为什么用这个方法：3D 发生在工作流阶段。
推导过程：建模、编辑、验收、发布逐段拆。
阶段结论：关键场景是编辑和验收。
如何影响下一步：看成本。
3. 损失什么？
目的：识别成本。
分析方法：成本结构分析。
为什么用这个方法：要判断付费动力。
推导过程：修改成本、沟通成本、验收成本最高。
阶段结论：最大成本是不可控。
如何影响下一步：看收益。
4. 想得到什么？
目的：明确收益。
分析方法：JTBD。
为什么用这个方法：用户买的是任务完成。
推导过程：用户要稳定交付，不只是生成。
阶段结论：收益是可编辑、可复用、可交付。
如何影响下一步：找矛盾。
5. 为什么卡住？
目的：抽象矛盾。
分析方法：第一性原理。
为什么用这个方法：避免停留在功能。
推导过程：表面上是生成质量，本质上是交付控制。
阶段结论：这不是一次性生成 3D 资产，而是把空间意图转化为可编辑、可复用、可交付的 3D 工作流。
如何影响下一步：看系统因素。
6. 谁共同作用？
目的：识别系统关系。
分析方法：系统思维。
为什么用这个方法：多角色共同作用。
推导过程：推力是模型进步，阻力是验收难，瓶颈是编辑控制，放大器是企业内容需求。
阶段结论：价值控制点在工作流。
如何影响下一步：推演趋势。
7. 未来怎么变？
目的：判断演化路径。
分析方法：S 曲线。
为什么用这个方法：技术采纳分阶段。
推导过程：现在 → AI 辅助生成 → AI 辅助编辑 → 3D Agent 工作流 → 空间内容基础设施。
阶段结论：长期是空间工作流。
如何影响下一步：判断价值流向。
8. 价值流向哪里？
目的：判断价值捕获。
分析方法：价值迁移。
为什么用这个方法：要找利润池。
推导过程：价值从资产生成流向编辑、验收、治理和发布。
阶段结论：最大机会不在一次性生成一个 3D 模型，而在空间工作流。
如何影响下一步：形成取舍。

| 环节 | 分析方法 | 为什么使用 | 得到什么结论 | 对后续判断的价值 |
| ---- | -------- | ---------- | ------------ | ---------------- |
| 对象 | 利益相关者地图 | 对象复杂 | 企业内容团队是核心对象 | 决定场景 |

【现象】
我观察到：AI 3D 从生成资产进入工作流。
【原因】
它不是由单一因素导致，而是：模型能力、企业内容需求、验收压力共同作用。
其中最核心的驱动是：交付压力。
【本质】
表面上是：生成 3D 模型。
本质上是：空间意图的可控交付。
一句话本质判断：这不是 3D 生成问题，而是空间工作流交付问题。
【系统】
关键参与因素包括：用户、模型、编辑器、验收、发布。
核心系统关系是：生成降低初稿成本，验收压力提升工作流价值。
推力：模型能力提升。
阻力：不可控。
瓶颈：编辑和验收。
放大器：企业内容需求。
【趋势】
我判断它会从：
现在 → AI 生成 → AI 编辑 → 3D Agent 工作流
长期趋势是：空间内容自动化生产系统。
【机会】
最大机会不在：一次性生成。
而在：可编辑、可复用、可交付的空间工作流。
因为：它更接近价值控制点。

【核心判断】
这不是 X 问题，而是 Y 问题。
【应该做什么】
做：编辑、验收、导出工作流。
【不应该做什么】
不做：只堆生成效果。
【先验证什么】
先验证：企业是否愿意为验收效率付费。
【关键假设】
验收能力影响采购。
【验证指标】
任务成功率、返工率、交付时间。
【最小可行方案】
用 3D Eval + 编辑器闭环验证。
【长期机会】
空间工作流基础设施。
【最大风险】
模型输出不可控。

如果我在面试或汇报中表达，我会这样说：
“我会从六层来看这个问题。第一，现象上……所以我的最终判断是……不应该优先做……而应该先验证……”

【PREP 表达版本】

Point 观点：AI 3D 的价值控制点在空间工作流。
Reason 理由：企业要的是可编辑、可复用、可交付，而不是一次性生成。
Example 例证：培训内容团队需要反复修改、验收和导出。
Point 回收：所以应该先验证编辑和验收闭环。

【SCQA 表达版本】

Situation：AI 3D 生成能力正在提升。
Complication：企业交付仍卡在编辑、验收和复用。
Question：机会应该落在生成模型还是工作流？
Answer：应该落在可交付空间工作流。

【被追问时的回答】
追问：生成质量提高后还需要工作流吗？
回答：仍然需要，因为企业交付要看可控修改、验收责任和发布标准。

【Insight Quality Audit】

核心 Insight：AI 3D 的机会不在一次性生成，而在可交付空间工作流。

评分表：

| 一级维度 | 子项 | 分值 | 得分 | 证据 | 扣分原因 | 补强动作 |
| --- | --- | ---: | ---: | --- | --- | --- |
| 思考深度 | 问题重构 | 8 | 7 | 从生成重构为工作流交付 | 场景仍较抽象 | 补真实企业案例 |
| 思考深度 | 底层矛盾 | 8 | 7 | 识别生成效率与可控交付矛盾 | 反例不足 | 补竞品对照 |
| 思考深度 | 因果机制 | 8 | 7 | 解释生成到验收的价值迁移 | 数据不足 | 补客户数据 |
| 思考深度 | 系统关系 | 7 | 6 | 覆盖用户、模型、编辑器、验收 | 采购角色不足 | 补采购视角 |
| 思考深度 | 反面论证 / 边界条件 | 7 | 6 | 说明生成直出时判断失效 | 边界较短 | 补更多边界 |
| 思考深度 | 取舍判断 | 7 | 7 | 做 / 不做 / 先验证明确 | 暂无 | 保持 |
| 内容质量 | 事实可靠性 | 7 | 6 | 使用官方文档假设 | 来源样例较少 | 补链接 |
| 内容质量 | 背景解释 | 5 | 4 | 说明 3D 工作流场景 | 背景略短 | 补上下文 |
| 内容质量 | 信息颗粒度 | 6 | 5 | 有编辑、验收、导出 | 指标较少 | 补指标 |
| 内容质量 | 方法使用质量 | 6 | 5 | 方法支撑判断 | 方法较少 | 补价值链 |
| 内容质量 | 趋势与机会信息 | 6 | 5 | 有阶段推演 | 节奏不够细 | 补时间线 |
| 表达质量 | 结论先行 | 5 | 5 | 先给核心判断 | 暂无 | 保持 |
| 表达质量 | 结构清晰 | 5 | 5 | 模块完整 | 暂无 | 保持 |
| 表达质量 | 推导可读 | 5 | 4 | 8 问展示过程 | 可以更深 | 补论据 |
| 表达质量 | 口头表达 | 5 | 4 | PREP / SCQA 可讲 | 口播略短 | 补表达 |
| 表达质量 | 记忆点 | 5 | 4 | 工作流交付可复述 | 金句不强 | 提炼短句 |

思考深度小计：40/45

内容质量小计：25/30

表达质量小计：22/25

总分：87/100

Insight 等级：
- training-v3 标准

是否达到 training-v3 标准：
- 是

主要扣分点：
- 来源样例和真实企业数据不足。

下一步补强：
- 补充真实产品链接、客户案例和可量化验收指标。

【训练能力】
系统判断。
【P6+ 易犯错误】
只做生成功能。
【P7+ 正确思路】
先判断价值控制点。
【可复用 Pattern】
生成能力进入企业场景后，价值迁移到治理和可交付工作流。
【迁移方式】
迁移到 Pose Director。

【Case Asset Card】
Case 名称：AI 3D Agent 从生成模型走向空间工作流
所属方向：3D AI
一句话现象：AI 3D 开始进入场景编辑。
一句话本质：这不是 X，而是 Y。
核心矛盾：想低成本生成，但需要可控交付。
关键系统关系：生成降低初稿成本 → 验收压力上升 → 工作流价值提升。
价值流向：从模型生成流向工作流控制。
做 / 不做 / 先验证：做工作流；不做纯生成；先验证验收付费。
可复用 Pattern：AI 生成价值向工作流迁移。
可迁移到我的哪个项目：Pose Director。
可迁移到哪类面试题：AI 产品壁垒判断。
2 分钟表达版本：我会从现象、本质、系统、趋势、机会表达。
未来 Watchlist：3D Eval、场景编辑、AR / VR 发布。
关注对象：3D Eval 与场景编辑产品。
关注指标：产品迭代、GitHub star / fork / release / issue、付费客户、竞品、论文与风险。
Watchlist 状态：持续跟踪。
资产等级：A。
资产等级说明：可直接进入面试素材库。
复习优先级：高。
"""


DAILY_CASE_A = SINGLE_CASE_OK.replace(
    "AI 3D Agent 从生成模型走向空间工作流",
    "Case A 外部变化类：AI 3D 工作流",
)
DAILY_CASE_B = SINGLE_CASE_OK.replace(
    "AI 3D Agent 从生成模型走向空间工作流",
    "Case B 产品开源类：AI 3D 工作流",
)
DAILY_CASE_C = SINGLE_CASE_OK.replace(
    "AI 3D Agent 从生成模型走向空间工作流",
    "Case C 个人壁垒类：AI 3D 工作流",
)
DAILY_DEEP_CASES = "\n".join((DAILY_CASE_A, DAILY_CASE_B, DAILY_CASE_C))

SUMMARY_CASES_B_C = """
【Case Asset Card】
Case 名称：B
做 / 不做 / 先验证：做；不做；先验证。
关注对象：B repo。
关注指标：产品迭代、GitHub 增长、付费客户、竞品、论文、风险。
Watchlist 状态：下周复查。
资产等级：B。
资产等级说明：需要补数据。
复习优先级：中。
【Case Asset Card】
Case 名称：C
做 / 不做 / 先验证：做；不做；先验证。
关注对象：C 评估框架。
关注指标：产品迭代、GitHub 增长、付费客户、竞品、论文、风险。
Watchlist 状态：等待官方发布。
资产等级：B。
资产等级说明：需要补效果数据。
复习优先级：高。
"""


DAILY_OK = f"""
## 零、来源通道使用情况
| 来源通道 | 状态 | 用途 | 限制与降级处理 |
| -------- | ---- | ---- | ---------------- |
| Search API / Web Search | 已使用 | 核验官方公告与产品发布 | 无 |
| AI HOT | 已使用 | 发现 AI 产品与论文信号 | 仅作信号，已回溯原始来源 |
| GitHub / Open-source | 已使用 | 核验 repo、release、issue / PR 与开发者信号 | 无 |

## 一、今日候选 case 池 + Case Selection Score
| Case | 类型 | 来源 | 事实等级 | 相关性 | 信号强度 | 训练价值 | 可验证性 | 资产化价值 | 总分 | 处理方式 |
| ---- | ---- | ---- | -------- | ------ | -------- | -------- | -------- | ---------- | ---- | -------- |
| A | AI 热点 | 官方博客 | A | 5 | 5 | 5 | 5 | 5 | 25 | 深度分析 |
| B | GitHub repo | GitHub | A | 5 | 4 | 5 | 5 | 5 | 24 | 深度分析 |
| C | 心理评估 | 官方文档 | A | 5 | 4 | 5 | 5 | 5 | 24 | 深度分析 |
| D | 3D AI | 产品官网 | A | 5 | 4 | 4 | 5 | 5 | 23 | 雷达简报 |
| E | AI Coding | Release Notes | A | 5 | 4 | 4 | 5 | 4 | 22 | Watchlist |
| F | Eval | 论文 | A | 5 | 4 | 5 | 5 | 4 | 23 | 自主训练题 |
| G | 商业趋势 | 媒体 | B | 4 | 4 | 4 | 4 | 4 | 20 | 雷达简报 |
| H | Agent Workflow | GitHub | A | 5 | 5 | 5 | 5 | 5 | 25 | 暂不处理 |

### Case Selection Score 阈值说明
| 总分 | 默认处理方式 | 说明 |
| ---- | ------------ | ---- |
| 21-25 | 深度分析候选 | 优先进入 Case A / B / C 深度选择池 |
| 17-20 | 雷达简报 / Watchlist | 有价值，但不一定适合当天深度分析 |
| 13-16 | 轻量观察 | 只保留一句话判断 |
| 12 以下 | 暂不处理 | 默认不进入训练内容 |

【今日深度 case 选择理由】
Case A：
选择原因：外部变化强。
训练目标：趋势推演。
没有选择更热 case 的原因：更热但事实弱。
Case B：
选择原因：产品化潜力强。
训练目标：开源产品化。
没有选择更热 case 的原因：总分不是唯一标准。
Case C：
选择原因：个人壁垒强。
训练目标：心理效果评价。
没有选择更热 case 的原因：需 A/B/C 均衡。

## 三、今日雷达简报
| 标题 | 类型 | 一句话结论 | 为什么值得看 | 链接 | 后续动作 |
| ---- | ---- | ---------- | ------------ | ---- | -------- |
| D | 3D AI | 进入工作流 | 和 Pose Director 相关 | https://example.com | Watchlist |

## 四、今日 3 个深度 case
{DAILY_DEEP_CASES}

【今日自主训练题】
Case：F
请你先回答 8 问：
1. 谁？
2. 在哪？
3. 损失什么？
4. 想得到什么？
5. 为什么卡住？
6. 谁共同作用？
7. 未来怎么变？
8. 价值流向哪里？

## 六、旧 case 复现 / 遗忘曲线回顾
D1：复述旧 case 的现象、本质、机会、做 / 不做 / 先验证。

## 七、今日训练复盘
今天主要训练了什么能力：判断力。
今天最重要的 P7+ 思维动作：先刹车。
今天最容易犯的 P6+ 错误：直接做方案。
今天沉淀了哪些 Case Asset Card：A/B/C。
哪些进入 Watchlist：D。
明天建议复习什么：A。

### Quality Review Rubric
| 维度 | 分数 1-5 | 简评 | 下一步如何补强 |
| ---- | -------: | ---- | ------------ |
| 事实可靠性 | 5 | 主要结论均有 A/B 级来源 | 无需补强 |
| 本质抽象深度 | 4 | 已从功能上升到价值控制点 | 无需补强 |
| 系统关系清晰度 | 4 | 推力和瓶颈清晰 | 无需补强 |
| 趋势推演可信度 | 3 | 长期信号仍少 | 下周复查 release 与客户案例 |
| 机会判断质量 | 4 | 价值流向明确 | 无需补强 |
| 取舍明确度 | 5 | 做、不做与先验证明确 | 无需补强 |
| 验证方案可执行性 | 4 | 指标可执行 | 无需补强 |
| Case Asset Card 可复用度 | 4 | 可进入知识库 | 无需补强 |
"""


DIAGNOSIS_OK = """
【你的答案当前更像】
P6+ / P7 / P7+ 诊断坐标：当前更像 P7
【做得好的地方】
能区分用户价值和业务价值。
【主要短板】
本质抽象不够。
【如果升级到 P7，应该补什么】
补验证指标和优先级。
【如果升级到 P7+，应该补什么】
补系统关系、趋势推演、价值流向和战略取舍。
【改写后的 P7+ 版本】
这不是功能优化问题，而是价值控制点迁移问题。应该做治理，不应该先堆功能，先验证付费意愿。
"""


class HermesOutputValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = load_validator()

    def _inflate_insight_audit_to_perfect_score(self, text: str) -> str:
        def replace_score(match):
            return f"{match.group(1)}{match.group(2)}{match.group(3)}"

        inflated = text
        inflated = __import__("re").sub(
            r"(\| [^|]+ \| [^|]+ \| (\d+) \| )\d+(\s*\|)",
            replace_score,
            inflated,
        )
        inflated = inflated.replace("思考深度小计：40/45", "思考深度小计：45/45")
        inflated = inflated.replace("内容质量小计：25/30", "内容质量小计：30/30")
        inflated = inflated.replace("表达质量小计：22/25", "表达质量小计：25/25")
        inflated = inflated.replace("总分：87/100", "总分：100/100")
        return inflated

    def test_single_case_accepts_complete_3d_output(self) -> None:
        result = self.validator.validate_text(SINGLE_CASE_OK, mode="single", domains=["3d"])
        self.assertEqual([], result.errors)

    def test_single_case_rejects_missing_fact_confidence(self) -> None:
        broken = SINGLE_CASE_OK.replace("| 事实 | 来源 | 事实等级 | 是否可用于最终判断 | 是否需要继续核验 |", "")
        result = self.validator.validate_text(broken, mode="single", domains=["3d"])
        self.assertTrue(any("Fact Confidence" in error for error in result.errors))

    def test_single_case_rejects_solution_first_output(self) -> None:
        broken = "【应该做什么】\n先做功能。\n" + SINGLE_CASE_OK
        result = self.validator.validate_text(broken, mode="single", domains=["3d"])
        self.assertTrue(any("P6+ brake" in error or "solution-first" in error for error in result.errors))

    def test_3d_domain_rejects_generation_only_output(self) -> None:
        broken = SINGLE_CASE_OK.replace("可编辑、可复用、可交付", "效果更逼真、更高清、更快速")
        broken = broken.replace("3D Eval", "生成质量")
        result = self.validator.validate_text(broken, mode="single", domains=["3d"])
        self.assertTrue(any("3D" in error for error in result.errors))

    def test_psychology_domain_rejects_clinical_diagnosis(self) -> None:
        text = SINGLE_CASE_OK + "\n可以诊断为重度抑郁，并给出治疗方案。"
        result = self.validator.validate_text(text, mode="single", domains=["psychology"])
        self.assertTrue(any("clinical" in error or "诊断" in error for error in result.errors))

    def test_psychology_domain_accepts_safety_bounded_output(self) -> None:
        text = (
            SINGLE_CASE_OK
            + "\nAI 心理效果评价需要看危机识别、隐私、伦理、人工转介、信效度、量表和长期效果。"
            + "\n边界：不输出医疗级结论，不把陪伴等同于专业心理治疗。"
        )
        result = self.validator.validate_text(text, mode="single", domains=["psychology"])
        self.assertEqual([], result.errors)

    def test_github_domain_rejects_star_only_analysis(self) -> None:
        text = SINGLE_CASE_OK + "\n这个 repo 值得看，因为 star 很高。"
        result = self.validator.validate_text(text, mode="single", domains=["github"])
        self.assertTrue(any("GitHub" in error for error in result.errors))

    def test_github_domain_accepts_workflow_productization_analysis(self) -> None:
        text = (
            SINGLE_CASE_OK
            + "\nGitHub repo 分析：star 增速、fork 增速、commit 活跃、release 节奏、issue / PR、README、demo、docs 都需要检查。"
            + "\n真正要判断的是开发者工作流痛点、产品化潜力、基础设施入口和控制点。"
        )
        result = self.validator.validate_text(text, mode="single", domains=["github"])
        self.assertEqual([], result.errors)

    def test_daily_mode_accepts_case_selection_and_three_assets(self) -> None:
        result = self.validator.validate_text(DAILY_OK, mode="daily")
        self.assertEqual([], result.errors)

    def test_daily_mode_rejects_too_few_candidates(self) -> None:
        broken = "\n".join(line for line in DAILY_OK.splitlines() if not line.startswith("| H |"))
        result = self.validator.validate_text(broken, mode="daily")
        self.assertTrue(any("8-13" in error for error in result.errors))

    def test_daily_mode_rejects_missing_required_source_channel(self) -> None:
        broken = DAILY_OK.replace("| AI HOT | 已使用 | 发现 AI 产品与论文信号 | 仅作信号，已回溯原始来源 |", "")
        result = self.validator.validate_text(broken, mode="daily")
        self.assertTrue(any("source channel" in error or "AI HOT" in error for error in result.errors))

    def test_daily_mode_rejects_missing_score_thresholds(self) -> None:
        start = DAILY_OK.index("### Case Selection Score 阈值说明")
        end = DAILY_OK.index("【今日深度 case 选择理由】")
        broken = DAILY_OK[:start] + DAILY_OK[end:]
        result = self.validator.validate_text(broken, mode="daily")
        self.assertTrue(any("threshold" in error or "阈值" in error for error in result.errors))

    def test_daily_mode_rejects_unstructured_asset_watchlist(self) -> None:
        broken = DAILY_OK.replace("Watchlist 状态：持续跟踪。", "", 1)
        result = self.validator.validate_text(broken, mode="daily")
        self.assertTrue(any("Watchlist" in error for error in result.errors))

    def test_daily_mode_rejects_missing_quality_review_rubric(self) -> None:
        broken = DAILY_OK[: DAILY_OK.index("### Quality Review Rubric")]
        result = self.validator.validate_text(broken, mode="daily")
        self.assertTrue(any("Quality Review Rubric" in error for error in result.errors))

    def test_daily_mode_rejects_low_rubric_score_without_follow_up(self) -> None:
        broken = DAILY_OK.replace(
            "| 趋势推演可信度 | 3 | 长期信号仍少 | 下周复查 release 与客户案例 |",
            "| 趋势推演可信度 | 3 | 长期信号仍少 | |",
        )
        result = self.validator.validate_text(broken, mode="daily")
        self.assertTrue(any("补强" in error or "Rubric" in error for error in result.errors))

    def test_daily_mode_caps_asset_score_when_rubric_itself_is_invalid(self) -> None:
        broken = DAILY_OK.replace(
            "| 趋势推演可信度 | 3 | 长期信号仍少 | 下周复查 release 与客户案例 |",
            "| 趋势推演可信度 | 3 | 长期信号仍少 | |",
        )
        result = self.validator.validate_text(broken, mode="daily")
        self.assertTrue(any("Case Asset Card 可复用度" in error and "3" in error for error in result.errors))

    def test_daily_mode_rejects_one_full_case_and_two_summary_cards(self) -> None:
        broken = DAILY_OK.replace(DAILY_DEEP_CASES, DAILY_CASE_A + SUMMARY_CASES_B_C)
        result = self.validator.validate_text(broken, mode="daily")
        self.assertTrue(any("3 complete deep cases" in error or "deep case" in error for error in result.errors))

    def test_daily_mode_rejects_simplified_deep_case_phrase(self) -> None:
        broken = DAILY_OK.replace("【Case Asset Card】", "【Case Asset Card】\nCase Asset Card 简版", 1)
        result = self.validator.validate_text(broken, mode="daily")
        self.assertTrue(any("simplified" in error or "简版" in error for error in result.errors))

    def test_daily_mode_rejects_repeated_boilerplate_across_deep_cases(self) -> None:
        repeated = "它把最终结论进一步压实为可验证的行动取舍。"
        broken = DAILY_OK.replace("【底层矛盾与因果机制】", f"{repeated}\n【底层矛盾与因果机制】")
        result = self.validator.validate_text(broken, mode="daily")
        self.assertTrue(any("boilerplate" in error or "模板" in error for error in result.errors))

    def test_daily_mode_rejects_high_insight_score_with_thin_reasoning(self) -> None:
        high_score_b = self._inflate_insight_audit_to_perfect_score(DAILY_CASE_B)
        broken = DAILY_OK.replace(DAILY_CASE_B, high_score_b)
        result = self.validator.validate_text(broken, mode="daily")
        self.assertTrue(any("high Insight score" in error or "8-question depth" in error for error in result.errors))

    def test_daily_mode_rejects_incomplete_case_with_high_quality_scores(self) -> None:
        broken_case_b = DAILY_CASE_B.replace("【系统】", "【系统分析】", 1)
        broken = DAILY_OK.replace(DAILY_CASE_B, broken_case_b)
        result = self.validator.validate_text(broken, mode="daily")
        self.assertTrue(any("Deep case 2" in error for error in result.errors))
        self.assertTrue(any("Quality Review" in error or "at most 3" in error for error in result.errors))

    def test_daily_mode_rejects_c_level_fact_as_final_support_with_high_reliability_score(self) -> None:
        broken_case_a = DAILY_CASE_A.replace(
            "| 支持场景编辑 | 官方文档 | A | 是 | 否 |",
            "| 支持场景编辑 | AI HOT 摘要 | C | 是 | 是 |",
            1,
        )
        broken = DAILY_OK.replace(DAILY_CASE_A, broken_case_a)
        result = self.validator.validate_text(broken, mode="daily")
        self.assertTrue(any("C-level" in error or "事实可靠性" in error for error in result.errors))

    def test_daily_mode_rejects_high_asset_score_when_card_field_is_missing(self) -> None:
        broken = DAILY_OK.replace("Watchlist 状态：持续跟踪。", "", 1)
        result = self.validator.validate_text(broken, mode="daily")
        self.assertTrue(any("Case Asset Card 可复用度" in error and "3" in error for error in result.errors))

    def test_daily_mode_requires_rubric_to_name_paraphrased_heading_issue(self) -> None:
        broken = DAILY_OK.replace("今日雷达简报", "今日雷达案例", 1)
        result = self.validator.validate_text(broken, mode="daily")
        self.assertTrue(any("structural issue" in error or "结构问题" in error for error in result.errors))

    def test_single_case_rejects_asset_without_quality_grade(self) -> None:
        broken = SINGLE_CASE_OK.replace("资产等级：A。", "")
        result = self.validator.validate_text(broken, mode="single", domains=["3d"])
        self.assertTrue(any("资产等级" in error for error in result.errors))

    def test_diagnosis_mode_accepts_p6_p7_p7plus_sections(self) -> None:
        result = self.validator.validate_text(DIAGNOSIS_OK, mode="diagnosis")
        self.assertEqual([], result.errors)

    def test_cli_returns_nonzero_for_invalid_output(self) -> None:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as fh:
            fh.write("【应该做什么】\n直接做方案。")
            path = Path(fh.name)
        try:
            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = self.validator.main(["--mode", "single", str(path)])
            self.assertEqual(1, exit_code)
            self.assertIn("FAIL", stderr.getvalue())
        finally:
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
