#!/usr/bin/env python3
"""Tests for rendering Hermes daily training Markdown into readable HTML."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


RENDERER_PATH = Path(__file__).resolve().parents[1] / "skill" / "scripts" / "render_training_html.py"


def load_renderer():
    spec = importlib.util.spec_from_file_location("render_training_html", RENDERER_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Cannot import renderer at {RENDERER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SAMPLE_DAILY = """# Hermes P7+ 每日训练 - 2026-06-25 V4 Raw

## 零、来源通道使用情况

| 来源通道 | 状态 | 用途 | 限制与降级处理 |
| --- | --- | --- | --- |
| Search API / Web Search | 已使用 | 核验官方公告 | 无 |
| AI HOT | 已使用 | 发现精选信号 | 仅作信号 |
| GitHub / Open-source | 已使用 | 核验 repo | 无 |

## 一、今日候选 case 池 + Case Selection Score

| Case | 类型 | 来源 | 事实等级 | 相关性 | 信号强度 | 训练价值 | 可验证性 | 资产化价值 | 总分 | 处理方式 |
| ---- | ---- | ---- | -------- | ------ | -------- | -------- | -------- | ---------- | ---- | -------- |
| Gemini computer use | 外部变化类 | https://blog.google/example | A | 5 | 5 | 5 | 5 | 4 | 24 | 深度分析 |

## 四、今日 3 个深度 case

【Case】

【类型】
Case A：外部变化类。

【V3.1 Insight 总览】

一句话 Insight：能力默认化以后，治理变稀缺。

核心判断：这不是 computer use 能力升级问题，而是企业执行授权系统问题。

【8 问显性推理】

1. 谁？

目的：识别授权者和风险承担者。

分析方法：利益相关者地图。

为什么用这个方法：多角色共同决定采用。

推导过程：使用者要效率，安全团队承担风险。

阶段结论：核心对象是组织，而不是单个用户。

如何影响下一步：进入权限和审计判断。

【Case Asset Card】

Case 名称：Gemini computer use

一句话本质：执行能力默认化，治理能力稀缺化。

## 七、今日训练复盘

### Quality Review Rubric

| 维度 | 分数 1-5 | 简评 | 下一步如何补强 |
| --- | ---: | --- | --- |
| 事实可靠性 | 5 | 来源可靠 | 保持 |
"""


class RenderTrainingHtmlTests(unittest.TestCase):
    def setUp(self) -> None:
        self.renderer = load_renderer()

    def test_render_html_has_reading_navigation_and_preserves_source_links(self) -> None:
        html = self.renderer.render_html(SAMPLE_DAILY, source_name="training-v4-raw.md")

        self.assertIn("<!doctype html>", html.lower())
        self.assertIn("Hermes P7+ 每日训练", html)
        self.assertIn("阅读导航", html)
        self.assertIn("Insight 总览", html)
        self.assertIn("Case Asset Card", html)
        self.assertIn("Gemini computer use", html)
        self.assertIn('<a href="https://blog.google/example"', html)
        self.assertIn("<details", html)
        self.assertIn("Quality Review Rubric", html)
        self.assertIn('rel="icon"', html)
        self.assertIn('href="#section-1"', html)
        self.assertIn('id="section-1"', html)

    def test_linkify_does_not_swallow_markdown_backticks_or_chinese_punctuation(self) -> None:
        html = self.renderer.render_html("来源：`https://example.com/api?x=1%2B2`，用于核验。")

        self.assertIn('href="https://example.com/api?x=1%2B2"', html)
        self.assertNotIn('href="https://example.com/api?x=1%2B2`，用于核验。"', html)

    def test_default_output_path_replaces_markdown_suffix_with_html(self) -> None:
        output = self.renderer.default_output_path(Path("/tmp/2026-06-25/training-v4-raw.md"))

        self.assertEqual(Path("/tmp/2026-06-25/training-v4-raw.html"), output)

    def test_cli_writes_html_next_to_markdown_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            markdown_path = Path(tmpdir) / "training-v4-raw.md"
            markdown_path.write_text(SAMPLE_DAILY, encoding="utf-8")

            exit_code = self.renderer.main([str(markdown_path)])

            html_path = markdown_path.with_suffix(".html")
            self.assertEqual(0, exit_code)
            self.assertTrue(html_path.exists())
            html = html_path.read_text(encoding="utf-8")
            self.assertIn("Hermes P7+ 每日训练", html)
            self.assertIn("training-v4-raw.md", html)


if __name__ == "__main__":
    unittest.main()
