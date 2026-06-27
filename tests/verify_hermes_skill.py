#!/usr/bin/env python3
"""Verify the Hermes P7+ product-thinking skill artifact."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.exists(), f"Missing required file: {path}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: verify_hermes_skill.py <skill-dir>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).expanduser()
    require(root.exists(), f"Skill directory does not exist: {root}")
    require(root.is_dir(), f"Skill path is not a directory: {root}")

    skill_md = read(root / "SKILL.md")
    framework = read(root / "references" / "framework.md")
    templates = read(root / "references" / "templates.md")
    domain_addons = read(root / "references" / "domain-addons.md")
    failure_feedback = read(root / "references" / "failure-feedback.md")
    failure_cases = read(root / "references" / "failure-cases.md")
    output_validator = read(root / "scripts" / "validate_hermes_output.py")
    failure_validator = read(root / "scripts" / "validate_failure_feedback.py")
    openai_yaml = read(root / "agents" / "openai.yaml")

    all_text = "\n".join([skill_md, framework, templates, domain_addons, failure_feedback, failure_cases, output_validator, failure_validator])

    require(skill_md.startswith("---\n"), "SKILL.md must start with YAML frontmatter")
    frontmatter_match = re.match(r"---\n(.*?)\n---\n", skill_md, re.S)
    require(frontmatter_match is not None, "SKILL.md frontmatter is malformed")
    frontmatter = frontmatter_match.group(1)
    require("name: hermes-p7-product-thinking" in frontmatter, "Skill name is incorrect")
    description_match = re.search(r"^description:\s*(.+)$", frontmatter, re.M)
    require(description_match is not None, "Description is missing")
    description = description_match.group(1).strip().strip('"')
    require(description.startswith("Use when"), "Description must start with 'Use when'")
    require(len(frontmatter) <= 1024, "Frontmatter exceeds 1024 characters")

    require(len(skill_md.splitlines()) <= 220, "SKILL.md should stay concise")
    require("V3.1 Insight" in skill_md, "SKILL.md must identify the V3.1 Insight contract")
    require("TODO" not in all_text, "Skill contains unresolved TODO text")

    required_terms = [
        "先问谁，再问场景",
        "8 问",
        "Fact Confidence",
        "Case Selection Score",
        "今日雷达简报",
        "Case Asset Card",
        "遗忘曲线",
        "P6+",
        "P7",
        "P7+",
        "3D AI",
        "心理",
        "GitHub",
        "AI HOT",
        "做 / 不做 / 先验证",
        "现象 → 原因 → 本质 → 系统 → 趋势 → 机会",
        "每日训练模式",
        "单 case 训练模式",
        "用户答案诊断模式",
        "validate_hermes_output.py",
        "Mandatory Source Usage",
        "Source Access Fallback Policy",
        "Case Selection Score Threshold",
        "Quality Review Rubric",
        "AI HOT REST API Access Notes",
        "Fact Upgrade Rule",
        "Daily Deep Case Completeness Rule",
        "Exact Template Compliance Rule",
        "Quality Review Guardrail",
        "Watchlist 状态",
        "资产等级",
        "复习优先级",
        "Daily HTML Artifact Workflow",
        "Daily HTML Reader Redesign Mode",
        "HTML Reader Redesign Contract",
        "render_training_reader_html.py",
        "validate_training_reader_html.py",
        "validate_failure_feedback.py",
        "Failure Feedback Loop",
        "失败登记",
        "失败归因",
        "规则回流",
        "测试回流",
        "复测回归",
        "失败处理",
        "V7 内容退坡与网页空壳回流样本",
        "render_training_html.py",
        "chat reply should contain only the HTML link",
        "YYYY-MM-DD",
    ]
    missing_terms = [term for term in required_terms if term not in all_text]
    require(not missing_terms, f"Missing required Hermes concepts: {missing_terms}")

    require(
        "| Case | 类型 | 来源 | 事实等级 | 相关性 | 信号强度 | 训练价值 | 可验证性 | 资产化价值 | 总分 | 处理方式 |"
        in templates,
        "Candidate case scoring table template is missing",
    )
    require(
        "| 事实 | 来源 | 事实等级 | 是否可用于最终判断 | 是否需要继续核验 |" in templates,
        "Fact confidence table template is missing",
    )
    require(
        all(channel in skill_md for channel in ("Search API / Web Search", "AI HOT", "GitHub Trending")),
        "Daily mode must require Search, AI HOT, and GitHub source channels",
    )
    require(
        all(threshold in framework for threshold in ("21-25", "17-20", "13-16", "12 以下")),
        "Case Selection Score thresholds are incomplete",
    )
    aihot_routes = (
        "GET /api/public/items?mode=selected&since=<语义窗>",
        "GET /api/public/daily",
        "/daily/{date}",
        "GET /api/public/items?mode=all",
        "GET /api/public/items?mode=selected&category=...",
        "GET /api/public/items?mode=selected&since=ISO-8601",
        "GET /api/public/items?q=<keyword>",
        "GET /api/public/dailies?take=N",
    )
    require(all(route in framework for route in aihot_routes), "AI HOT endpoint routing notes are incomplete")
    require(
        all(category in framework for category in ("AI 模型", "产品", "论文", "技巧")),
        "AI HOT confirmed category examples are incomplete",
    )
    forbidden_category = "category=" + "行业"
    require(forbidden_category not in all_text, f"Skill must not invent the unconfirmed {forbidden_category} value")
    require(
        all(term in framework for term in ("official Skill", "OpenAPI", "actual request", "url` field")),
        "AI HOT endpoint and original-source verification rules are incomplete",
    )
    require(
        "User-Agent" in framework and "403" in framework,
        "AI HOT API access notes must cover the current User-Agent requirement",
    )
    require(
        "AI HOT 摘要默认为 C 级" in framework and "升级为 A / B 级" in framework,
        "AI HOT Fact Confidence mapping is incomplete",
    )
    require(
        all(term in framework for term in (
            "Original-source verification does not automatically upgrade a claim to A level",
            "user experience report",
            "official rollout scope",
            "unofficial roadmap",
            "C-level facts can guide candidate selection",
            "D-level facts cannot support final judgment",
        )),
        "Fact Upgrade Rule is incomplete",
    )
    require(
        all(term in framework for term in (
            "Daily mode always requires 3 complete deep cases",
            "Case A：外部变化类",
            "Case B：产品 / 商业 / 开源趋势类",
            "Case C：个人壁垒类",
            "Do not output a simplified version for Case B or Case C",
            "Case Asset Card 简版",
        )),
        "Daily Deep Case Completeness Rule is incomplete",
    )
    require(
        all(term in framework for term in (
            "must follow `references/templates.md` exactly",
            "今日候选 case 池",
            "今日 3 个深度 case",
            "旧 case 复现",
            "一句话结论",
        )),
        "Exact Template Compliance Rule is incomplete",
    )
    require(
        all(term in framework for term in (
            "If the generated daily output fails the validator",
            "Case Asset Card 可复用度",
            "本质抽象深度",
            "系统关系清晰度",
            "事实可靠性",
            "structural issue",
        )),
        "Quality Review Guardrail is incomplete",
    )
    require(
        all(term in framework for term in ("If AI HOT is unavailable", "AI HOT 今日精选显示", "AI HOT 日报提到", "AI HOT-derived signals are absent")),
        "AI HOT-specific fallback policy is incomplete",
    )
    require(
        all(term in templates for term in ("实际调用 / 查询词", "是否回原文核验", "仍待核验的信号")),
        "Daily source usage template is not auditable enough",
    )
    require(
        "| 来源通道 | 状态 | 用途 | 限制与降级处理 |" in templates,
        "Daily source table header must remain validator-compatible",
    )
    require("/api/public/" not in output_validator, "Validator must not hard-code AI HOT endpoints")
    require(
        all(field in templates for field in ("关注对象：", "关注指标：", "Watchlist 状态：", "资产等级：", "复习优先级：")),
        "Case Asset Card V5.1 fields are incomplete",
    )
    require(
        "不做临床诊断" in domain_addons and "人工转介" in domain_addons,
        "AI psychology safety constraints are incomplete",
    )
    require(
        "可编辑、可复用、可交付" in domain_addons,
        "3D AI workflow constraints are incomplete",
    )
    require(
        "scripts/validate_hermes_output.py" in skill_md,
        "SKILL.md must tell agents how to run the output conformance validator",
    )
    require(
        "scripts/render_training_reader_html.py" in skill_md,
        "SKILL.md must make the reader HTML renderer the daily default",
    )
    require(
        "scripts/validate_training_reader_html.py" in skill_md and "validate_training_reader_html.py" in templates,
        "Daily workflow must require the reader HTML completeness validator",
    )
    require(
        "validate_html_text" in (root / "scripts" / "validate_training_reader_html.py").read_text(encoding="utf-8"),
        "Reader HTML completeness validator implementation is missing",
    )
    require(
        all(term in skill_md for term in ("references/failure-feedback.md", "references/failure-cases.md", "validate_failure_feedback.py")),
        "SKILL.md must wire severe failures into the failure feedback loop",
    )
    require(
        all(term in failure_feedback for term in ("失败登记", "失败归因", "规则回流", "测试回流", "复测回归", "失败处理")),
        "Failure feedback workflow reference is incomplete",
    )
    require(
        all(term in failure_cases for term in ("V7 内容退坡与网页空壳回流样本", "高分但内容浅", "模板套话重复", "8 问推理为空壳", "复测证据")),
        "V7 failure feedback sample is incomplete",
    )
    require(
        "validate_text" in failure_validator and "REQUIRED_RECORD_MARKERS" in failure_validator,
        "Failure feedback validator implementation is missing",
    )
    require(
        all(term in all_text for term in (
            "redesign-existing-projects",
            "design-taste-frontend",
            "Audit first",
            "no horizontal overflow",
            "navigation",
            "typography",
            "mobile",
            "window.addEventListener('scroll')",
        )),
        "Daily HTML reader redesign workflow is incomplete",
    )
    require(
        "daily" in output_validator and "single" in output_validator and "diagnosis" in output_validator,
        "Output validator must support daily, single, and diagnosis modes",
    )
    require(
        "psychology" in output_validator and "github" in output_validator and "3d" in output_validator,
        "Output validator must support psychology, GitHub, and 3D domain checks",
    )

    require("display_name:" in openai_yaml, "openai.yaml missing display_name")
    require("short_description:" in openai_yaml, "openai.yaml missing short_description")
    require(
        "$hermes-p7-product-thinking" in openai_yaml,
        "openai.yaml default_prompt must mention $hermes-p7-product-thinking",
    )

    print(f"PASS: Hermes skill verified at {root}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
