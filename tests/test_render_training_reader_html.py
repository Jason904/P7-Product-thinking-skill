#!/usr/bin/env python3
"""Tests for the reader-first Hermes HTML renderer."""

from __future__ import annotations

import importlib.util
import re
import sys
import tempfile
import unittest
from pathlib import Path


RENDERER_PATH = Path(__file__).resolve().parents[1] / "skill" / "scripts" / "render_training_reader_html.py"
HTML_VALIDATOR_PATH = Path(__file__).resolve().parents[1] / "skill" / "scripts" / "validate_training_reader_html.py"


def load_renderer():
    spec = importlib.util.spec_from_file_location("render_training_reader_html", RENDERER_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Cannot import renderer at {RENDERER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_html_validator():
    spec = importlib.util.spec_from_file_location("validate_training_reader_html", HTML_VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Cannot import HTML validator at {HTML_VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


SAMPLE_DAILY = """# Hermes P7+ 每日训练 - 2026-06-25 V6 Raw

## 零、来源通道使用情况

| 来源通道 | 状态 | 用途 | 限制与降级处理 |
| --- | --- | --- | --- |
| Search API / Web Search | 已使用 | 核验官方公告 | 无 |
| AI HOT | 已使用 | 发现精选信号 | 仅作信号 |
| GitHub / Open-source | 已使用 | 核验 repo | 无 |

## 一、今日候选 case 池 + Case Selection Score

| Case | 类型 | 来源 | 事实等级 | 相关性 | 信号强度 | 训练价值 | 可验证性 | 资产化价值 | 总分 | 处理方式 |
| ---- | ---- | ---- | -------- | ------ | -------- | -------- | -------- | ---------- | ---- | -------- |
| OpenAI + Broadcom Jalapeño 推理芯片 | Case A 外部变化类 / AI 基础设施 | OpenAI 官方公告；AI HOT | A | 5 | 5 | 5 | 5 | 4 | 24 | 深度分析 |
| Mistral Connectors 企业治理控制 | Case B 产品 / 商业趋势类 | Mistral 官方公告；AI HOT | A | 5 | 5 | 5 | 5 | 5 | 25 | 深度分析 |
| Google Thinking to Recall | Case C 个人壁垒类 / 推理训练方法 | Google Research；AI HOT | A | 5 | 4 | 5 | 5 | 5 | 24 | 深度分析 |

### Case Selection Score 阈值说明

| 总分 | 默认处理方式 | 说明 |
| ---: | --- | --- |
| 21-25 | 深度分析候选 | 优先进入 Case A / B / C 深度选择池 |

### 候选 case 快速认知卡片

1. OpenAI + Broadcom Jalapeño：一句话描述是，OpenAI 开始把推理成本、延迟、供给可靠性纳入自研芯片。溯源链接：[OpenAI](https://openai.com/)、[AI HOT](https://aihot.example/item)。为什么是 24 分：基础设施信号强、官方来源完整，但性能细节仍待技术报告。处理方式：深度分析。
2. Mistral Connectors：一句话描述是，Mistral 把 connectors 从能接工具升级到企业治理控制。溯源链接：[Mistral](https://mistral.ai/)、[AI HOT](https://aihot.example/item2)。为什么是 25 分：官方来源清楚，能沉淀为治理产品化 Pattern。处理方式：深度分析。
3. Google Thinking to Recall：一句话描述是，Google Research 研究 reasoning trace 如何帮助模型召回知识。溯源链接：[Google Research](https://research.google/)、[AI HOT](https://aihot.example/item3)。为什么是 24 分：直接关系到 Hermes 显性推理训练的理论基础。处理方式：深度分析。

## 二、今日深度 case 选择理由

Case A：
选择原因：外部基础设施变化能训练系统判断。
训练目标：训练如何从芯片变化看到产品体验边界。
没有选择更热 case 的原因：官方来源更稳。

Case B：
选择原因：企业 agent 治理是产品化关键。
训练目标：训练如何从 feature list 抽象购买理由。
没有选择更热 case 的原因：更适合作为商业趋势 deep case。

Case C：
选择原因：推理研究能训练个人壁垒。
训练目标：训练如何把研究结论迁移为表达能力。
没有选择更热 case 的原因：更贴近个人成长目标。

## 三、今日雷达简报

| 标题 | 类型 | 一句话结论 | 为什么值得看 | 链接 | 后续动作 |
| ---- | ---- | ---------- | ------------ | ---- | -------- |
| GitHub Copilot AGENTS.md support | Review Gate | Repo 级规则进入 AI review。 | 可迁移到治理。 | https://github.blog/ | 下周复查。 |

## 四、今日 3 个深度 case

### Case A：OpenAI + Broadcom Jalapeño 推理芯片

【Case】

【信息来源】

- OpenAI official announcement：https://openai.com/

【本次训练目标】

训练从基础设施变化判断产品体验边界。

【P6+ 第一反应】

一个执行型产品经理可能会直接想：
“OpenAI 做芯片了，说明要降低成本。”

【这个思路对在哪里】

它有价值的地方是：抓住了成本和供给。

【这个思路为什么不够】

它的问题是没有推到产品体验和商业指标。

【V3.1 Insight 总览】

一句话 Insight：
基础设施正在变成产品能力。

核心判断：
这不是芯片新闻，而是智能交付系统问题。

行动取舍：
- 做：关注成本、延迟、可靠性。
- 不做：不提前判断芯片战胜负。
- 先验证：部署规模和体验传导。

【8 问显性推理】

1. 谁？
目的：
识别影响对象。
分析方法：
利益相关者地图。
为什么用这个方法：
先知道谁受影响，才能继续判断场景。
推导过程：
OpenAI、开发者、企业客户和用户都被推理成本影响。
阶段结论：
这是多方共同参与的产品交付问题。
如何影响下一步：
下一步不能只看芯片参数，要看体验传导。

2. 在哪？
目的：
定位影响场景。
分析方法：
场景分层。
为什么用这个方法：
不同场景的性能约束不同。
推导过程：
现在：ChatGPT、Codex、API 和企业 agent 已经分别受到延迟、吞吐和可靠性的约束。阶段 1：先在 OpenAI 内部高频推理 workload 里验证成本和稳定性。阶段 2：改善传导到 ChatGPT、Codex、API 和企业 agent 的体验指标。长期形态：基础设施能力沉淀为产品可承诺的智能交付能力。
阶段结论：
价值发生在高频、长任务和强可靠场景。
如何影响下一步：
后续要看不同 workload 的体验改善。

【现象】

我观察到：
OpenAI 发布面向推理场景的芯片。

【原因】

它不是由单一因素导致，而是：
推理成本、延迟和供给稳定性正在成为 AI 产品体验的硬约束。

其中最核心的驱动是：
基础设施已经从后台成本项变成产品能力的一部分。

【本质】

表面上是：
OpenAI 发布一颗推理芯片。

本质上是：
OpenAI 试图控制智能交付的成本、延迟和可靠性。

一句话本质判断：
这不是芯片新闻，而是 AI 产品交付系统的控制权竞争。

【系统】

关键参与因素包括：
OpenAI、开发者、企业客户、终端用户和基础设施合作方。

核心系统关系是：
模型能力、推理系统、基础设施成本、网络延迟和产品体验共同作用。

推力：
用户需要更快、更稳定、更便宜的智能服务。

阻力：
芯片研发、部署规模、生态兼容和技术报告仍待验证。

瓶颈：
能否把性能改善稳定传导到产品体验。

放大器：
OpenAI 自有 workload、产品闭环、模型 roadmap 和产业伙伴。

【趋势】

我判断它会从：
现在 -> 阶段 1 -> 阶段 2 -> 长期形态

现在：官方发布与工程样品，性能细节仍待报告。阶段 1：在 OpenAI 内部特定推理 workload 中试部署。阶段 2：效率收益传导到 ChatGPT、Codex、API 和企业产品。长期形态：模型、芯片、网络、调度和产品体验共同设计，形成 AI full-stack flywheel。

长期趋势是：
AI 公司会越来越把基础设施当作产品能力的一部分。

【机会】

最大机会不在：
判断某颗芯片能否击败 GPU。

而在：
理解推理成本下降后，哪些 AI 产品形态会被打开。

因为：
长期竞争不只靠模型能力，还靠稳定、便宜、低延迟地交付给更多场景。

【P7+ 面试 / 汇报表达版本】

【最大风险】

最大风险是过早把它理解成芯片战，忽略产品体验和商业指标是否真的改善。

如果我在面试或汇报中表达，我会这样说：
“我会从六层来看这个问题。
第一，现象上，OpenAI 发布了面向 LLM inference 的芯片。
第二，原因上，ChatGPT、Codex、API 和 agent 产品都受到推理成本、延迟和供给稳定性的约束。
第三，本质上，这不是芯片新闻，而是 AI 产品交付系统的控制权竞争。
第四，系统上，模型、推理系统、芯片、网络、数据中心和产品体验共同作用。
第五，趋势上，AI 公司会从模型竞争进入 full-stack intelligence delivery 竞争。
第六，机会判断上，最大机会不是判断它能否替代 GPU，而是观察它能否降低单位智能交付成本，打开更长任务、更低延迟和更高可靠性的产品形态。

所以我的最终判断是，应该把推理基础设施当作产品变量持续跟踪。
不应该优先下结论说 OpenAI 已经赢了芯片战。
而应该先验证技术报告、部署规模和产品体验变化。”

【PREP 表达版本】

Point 观点：
基础设施是产品能力。

【Insight Quality Audit】

思考深度小计：42/45

内容质量小计：28/30

表达质量小计：23/25

总分：93/100

主要扣分点：
- 部署数据待验证。

下一步补强：
- 跟踪技术报告。

【Case Asset Card】

Case 名称：
OpenAI + Broadcom Jalapeño 推理芯片

Watchlist 状态：
- 持续跟踪

资产等级：
- A

### Case B：Mistral Connectors 企业治理控制

【Case】

【V3.1 Insight 总览】

一句话 Insight：
连接能力正在迁移到治理能力。

核心判断：
这不是连接器数量问题，而是企业 agent 治理问题。

行动取舍：
- 做：治理连接器。
- 不做：只堆 integration。
- 先验证：安全审批时间。

【Insight Quality Audit】

总分：96/100

【Case Asset Card】

Case 名称：
Mistral Connectors 企业治理控制

### Case C：Google Thinking to Recall

【Case】

【V3.1 Insight 总览】

一句话 Insight：
推理价值在可审计和可迁移。

核心判断：
这不是推理越长越好，而是过程可治理。

行动取舍：
- 做：事实分级。
- 不做：长文本崇拜。
- 先验证：用户复述。

【Insight Quality Audit】

总分：95/100

【Case Asset Card】

Case 名称：
Google Thinking to Recall

## 七、今日训练复盘

### Quality Review Rubric
"""


class RenderTrainingReaderHtmlTests(unittest.TestCase):
    def setUp(self) -> None:
        self.renderer = load_renderer()

    def test_render_reader_html_contains_reader_first_structure(self) -> None:
        html = self.renderer.render_reader_html(SAMPLE_DAILY, source_name="training-v6-raw.md")

        self.assertIn("今日阅读导读", html)
        self.assertIn("深度阅读版", html)
        self.assertIn("case-card-list", html)
        self.assertIn("candidate-overview", html)
        self.assertIn('<section class="candidate-overview">', html)
        self.assertNotIn('<section class="candidate-overview" id="candidates">', html)
        self.assertIn('<section class="candidate-pool-panel" id="candidates">', html)
        self.assertLess(html.find('id="radar"'), html.find('id="candidates"'))
        self.assertIn("先看雷达，再看候选选择", html)
        self.assertIn("今天值得继续跟踪的信号", html)
        self.assertIn("今日候选 case 与选择判断", html)
        self.assertIn("最终入选理由", html)
        self.assertIn("为什么是 24 分", html)
        self.assertIn("score-help", html)
        self.assertIn("reader-toast", html)
        self.assertIn("context-list radar-context-list", html)
        self.assertIn("打开原文：", html)
        self.assertIn("来源链接", html)
        self.assertIn("inline-label", html)
        self.assertIn("--semantic-insight", html)
        self.assertIn("--semantic-conclusion", html)
        self.assertIn("--semantic-risk", html)
        self.assertIn('insight-callout semantic-item semantic-insight', html)
        self.assertIn('judgment-block semantic-item semantic-conclusion', html)
        self.assertIn('action-cell semantic-item semantic-action action-cell-action', html)
        self.assertIn('action-cell semantic-item semantic-risk action-cell-risk', html)
        self.assertIn('action-cell semantic-item semantic-practice action-cell-practice', html)
        self.assertIn('semantic-paragraph semantic-item semantic-insight semantic-paragraph-insight', html)
        self.assertIn('semantic-paragraph semantic-item semantic-conclusion semantic-paragraph-conclusion', html)
        self.assertIn("eight-question-workbench", html)
        self.assertIn("eight-question-route", html)
        self.assertIn("eight-question-card", html)
        self.assertIn("eight-question-focus-grid", html)
        self.assertIn('eight-question-field semantic-item semantic-conclusion eight-question-field-conclusion focus', html)
        self.assertIn('eight-question-field semantic-item semantic-next eight-question-field-next focus', html)
        self.assertIn("把一个 case 拆成 8 个连续判断", html)
        self.assertIn("phase-sequence", html)
        self.assertIn(">01</span>", html)
        self.assertIn(">02</span>", html)
        self.assertIn("这是多方共同参与的产品交付问题", html)
        self.assertIn("下一步不能只看芯片参数", html)
        self.assertIn("six-layer-workbench", html)
        self.assertIn("six-layer-card", html)
        self.assertIn('six-layer-card semantic-item semantic-insight six-layer-card-insight', html)
        self.assertIn('speech-closing semantic-item semantic-conclusion', html)
        self.assertIn("六层判断链", html)
        self.assertIn("现象、原因、本质、系统、趋势、机会", html)
        self.assertIn("speech-module", html)
        self.assertIn("speech-step", html)
        self.assertIn("六层表达版本", html)
        self.assertIn("如果我在面试或汇报中表达，我会这样说", html)
        self.assertNotRegex(html, r"<summary[^>]*><span>现象</span>")
        self.assertNotRegex(html, r"<summary[^>]*><span>原因</span>")
        self.assertLess(html.find("六层判断链"), html.find("如果我在面试或汇报中表达，我会这样说"))
        self.assertIn("展开评分拆解、训练角色和来源", html)
        self.assertIn("打开原文", html)
        self.assertIn("建议推进", html)
        self.assertIn("暂不推进", html)
        self.assertIn("优先验证", html)
        self.assertIn('id="source-evidence"', html)
        self.assertIn('id="scoring-rule"', html)
        self.assertIn("核心 Insight", html)
        self.assertIn("结论先行", html)
        self.assertIn("nav-group-title", html)
        self.assertIn("mobile-toc-panel", html)
        self.assertIn("toc-case-mobile", html)
        self.assertIn("mobile-bottom-nav", html)
        self.assertNotIn("selection-panel", html)
        self.assertIn("function activeTargetId(targets)", html)
        self.assertIn("const activeId = activeTargetId(majorTargets)", html)
        self.assertNotIn("visible[0].target.id", html)
        self.assertNotIn("为什么最终选这 3 个深度 case", html)
        self.assertNotIn("<span>信息来源</span>", html)
        self.assertNotRegex(html, r"<summary[^>]*><span>类型</span>")
        self.assertNotIn("<span>这个思路对在哪里</span>", html)
        self.assertNotIn("<span>这个思路为什么不够</span>", html)
        self.assertNotIn('<span class="inline-label">它有价值的地方是：</span>', html)
        self.assertIn("它有价值的地方是：抓住了成本和供给。", html)
        self.assertIn('id="case-1-reason"', html)
        self.assertIn('id="case-1-speak"', html)
        self.assertIn('id="case-1-asset"', html)
        self.assertIn('href="#case-1-speak"', html)
        self.assertIn('href="#case-1-asset"', html)
        self.assertIn("section-group speak", html)
        self.assertIn('data-auto-open="all"', html)
        reader_sections = re.findall(r'<details class="reader-section [^"]+"[^>]*>', html)
        self.assertGreater(len(reader_sections), 0)
        self.assertIn('<details class="reader-section reason" data-mode="reason" open>', html)
        self.assertRegex(
            html,
            r'<details class="reader-section read" data-mode="read">\s*<summary[^>]*><span>Insight Quality Audit</span>',
        )
        ids = re.findall(r'id="([^"]+)"', html)
        self.assertEqual(len(ids), len(set(ids)))
        candidate_breakdowns = re.findall(r'<details class="candidate-breakdown"[^>]*>', html)
        self.assertGreater(len(candidate_breakdowns), 0)
        self.assertTrue(all(" open" not in section for section in candidate_breakdowns))
        self.assertNotIn("addEventListener('scroll'", html)
        self.assertNotIn("window.scrollY", html)
        self.assertNotIn("来源与候选池：", html)
        self.assertNotIn("Hermes", html)
        self.assertNotIn("V6 Raw", html)
        self.assertIn("基础设施正在变成产品能力", html)
        self.assertIn("Mistral Connectors 企业治理控制", html)
        self.assertIn("Google Thinking to Recall", html)
        self.assertIn("Avg 94.7/100", html)

    def test_default_output_path_uses_reader_suffix(self) -> None:
        output = self.renderer.default_output_path(Path("/tmp/training-v6-raw.md"))

        self.assertEqual(Path("/tmp/training-v6-reader.html"), output)

    def test_eight_question_parser_accepts_inline_field_values(self) -> None:
        markdown = """【8 问显性推理】
1. 谁？

目的：识别核心利益相关人。

分析方法：利益相关者地图。

为什么用这个方法：先知道谁受影响，才能判断价值。

推导过程：受影响者是 founder、brand team 和广告平台。

阶段结论：受影响的是整个营销实验系统。

如何影响下一步：后续看团队角色和采购人。
"""

        items = self.renderer._parse_eight_questions(markdown)

        self.assertEqual(1, len(items))
        fields = items[0]["fields"]
        self.assertEqual("识别核心利益相关人。", fields["目的"])
        self.assertEqual("利益相关者地图。", fields["分析方法"])
        self.assertIn("founder", fields["推导过程"])
        html = self.renderer._render_eight_question_workbench(markdown, "case-test")
        self.assertIn("识别核心利益相关人", html)
        self.assertIn("受影响者是 founder", html)
        self.assertIn("受影响的是整个营销实验系统", html)

    def test_reader_html_completeness_checker_rejects_empty_eight_question_fields(self) -> None:
        html = self.renderer.render_reader_html(SAMPLE_DAILY, source_name="training-v6-raw.md")
        broken = re.sub(
            r"(<dt>目的</dt>\s*<dd>).*?(</dd>)",
            r"\1\2",
            html,
            count=1,
            flags=re.S,
        )
        html_validator = load_html_validator()

        result = html_validator.validate_html_text(broken)

        self.assertFalse(result.ok)
        self.assertTrue(any("empty 8-question field" in error for error in result.errors))

    def test_cli_writes_reader_html(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            markdown_path = Path(tmpdir) / "training-v6-raw.md"
            markdown_path.write_text(SAMPLE_DAILY, encoding="utf-8")

            exit_code = self.renderer.main([str(markdown_path)])

            html_path = Path(tmpdir) / "training-v6-reader.html"
            self.assertEqual(0, exit_code)
            self.assertTrue(html_path.exists())
            html = html_path.read_text(encoding="utf-8")
            self.assertIn("今日阅读导读", html)


if __name__ == "__main__":
    unittest.main()
