#!/usr/bin/env python3
"""Validate Hermes P7+ product-thinking Markdown outputs.

This is a deterministic guardrail for generated Hermes answers. It checks the
output contract; it does not judge whether the strategic conclusion is true.
"""

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def _has(text: str, needle: str) -> bool:
    return needle in text


def _add_missing(errors: list[str], text: str, needle: str, label: Optional[str] = None) -> None:
    if not _has(text, needle):
        errors.append(f"Missing required section/content: {label or needle}")


def _first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def _candidate_row_count(text: str) -> int:
    header = "| Case | 类型 | 来源 | 事实等级 | 相关性 | 信号强度 | 训练价值 | 可验证性 | 资产化价值 | 总分 | 处理方式 |"
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() == header:
            count = 0
            for row in lines[index + 1 :]:
                stripped = row.strip()
                if not stripped:
                    if count:
                        break
                    continue
                if not stripped.startswith("|"):
                    if count:
                        break
                    continue
                if "---" in stripped or "Case | 类型" in stripped:
                    continue
                if stripped.count("|") >= 10:
                    count += 1
            return count
    return 0


def _table_rows(text: str, header: str) -> list[list[str]]:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != header:
            continue
        rows: list[list[str]] = []
        for row in lines[index + 1 :]:
            stripped = row.strip()
            if not stripped:
                if rows:
                    break
                continue
            if not stripped.startswith("|"):
                if rows:
                    break
                continue
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            if cells and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
                continue
            rows.append(cells)
        return rows
    return []


def _asset_card_blocks(text: str) -> list[str]:
    return [block for block in text.split("【Case Asset Card】")[1:] if block.strip()]


ASSET_CARD_V51_FIELDS = (
    "关注对象：",
    "关注指标：",
    "Watchlist 状态：",
    "资产等级：",
    "资产等级说明：",
    "复习优先级：",
)

ASSET_CARD_REQUIRED_FIELDS = (
    "Case 名称：",
    "所属方向：",
    "一句话现象：",
    "一句话本质：",
    "核心矛盾：",
    "关键系统关系：",
    "价值流向：",
    "做 / 不做 / 先验证：",
    "可复用 Pattern：",
    "可迁移到我的哪个项目：",
    "可迁移到哪类面试题：",
    "2 分钟表达版本：",
    "未来 Watchlist：",
    *ASSET_CARD_V51_FIELDS,
)

FACT_CONFIDENCE_HEADER = "| 事实 | 来源 | 事实等级 | 是否可用于最终判断 | 是否需要继续核验 |"
INSIGHT_AUDIT_HEADER = "| 一级维度 | 子项 | 分值 | 得分 | 证据 | 扣分原因 | 补强动作 |"

INSIGHT_AUDIT_REQUIRED_SUBITEMS = (
    "问题重构",
    "底层矛盾",
    "因果机制",
    "系统关系",
    "反面论证 / 边界条件",
    "取舍判断",
    "事实可靠性",
    "背景解释",
    "信息颗粒度",
    "方法使用质量",
    "趋势与机会信息",
    "结论先行",
    "结构清晰",
    "推导可读",
    "口头表达",
    "记忆点",
)

FORBIDDEN_DAILY_DEEP_PHRASES = (
    "精简版",
    "简版",
    "核心判断版",
    "Case Asset Card 简版",
    "因篇幅控制，聚焦核心",
    "以下为简要分析",
)

FORBIDDEN_BOILERPLATE_PHRASES = (
    "它把最终结论进一步压实为可验证的行动取舍",
)

HIGH_SCORE_MIN_8Q_CHARS = 1800
HIGH_SCORE_MIN_INSIGHT_CHARS = 340


def _validate_asset_card_v51(block: str, errors: list[str], label: str) -> None:
    for field_name in ASSET_CARD_V51_FIELDS:
        if field_name not in block:
            errors.append(f"{label} missing V5.1 field: {field_name}")


def _validate_insight_quality_audit(text: str, errors: list[str]) -> None:
    _add_missing(errors, text, "【Insight Quality Audit】", "Insight Quality Audit")
    _add_missing(errors, text, INSIGHT_AUDIT_HEADER, "Insight Quality Audit table")

    for marker in (
        "核心 Insight：",
        "思考深度小计：",
        "内容质量小计：",
        "表达质量小计：",
        "总分：",
        "Insight 等级：",
        "是否达到 training-v3 标准：",
        "主要扣分点：",
        "下一步补强：",
    ):
        _add_missing(errors, text, marker, f"Insight Quality Audit marker {marker}")

    rows = _table_rows(text, INSIGHT_AUDIT_HEADER)
    if len(rows) < len(INSIGHT_AUDIT_REQUIRED_SUBITEMS):
        errors.append(f"Insight Quality Audit requires at least {len(INSIGHT_AUDIT_REQUIRED_SUBITEMS)} rows; found {len(rows)}")

    by_subitem = {row[1]: row for row in rows if len(row) >= 7}
    expected_max_scores = {
        "问题重构": 8,
        "底层矛盾": 8,
        "因果机制": 8,
        "系统关系": 7,
        "反面论证 / 边界条件": 7,
        "取舍判断": 7,
        "事实可靠性": 7,
        "背景解释": 5,
        "信息颗粒度": 6,
        "方法使用质量": 6,
        "趋势与机会信息": 6,
        "结论先行": 5,
        "结构清晰": 5,
        "推导可读": 5,
        "口头表达": 5,
        "记忆点": 5,
    }
    expected_dimension = {
        "问题重构": "思考深度",
        "底层矛盾": "思考深度",
        "因果机制": "思考深度",
        "系统关系": "思考深度",
        "反面论证 / 边界条件": "思考深度",
        "取舍判断": "思考深度",
        "事实可靠性": "内容质量",
        "背景解释": "内容质量",
        "信息颗粒度": "内容质量",
        "方法使用质量": "内容质量",
        "趋势与机会信息": "内容质量",
        "结论先行": "表达质量",
        "结构清晰": "表达质量",
        "推导可读": "表达质量",
        "口头表达": "表达质量",
        "记忆点": "表达质量",
    }

    for subitem in INSIGHT_AUDIT_REQUIRED_SUBITEMS:
        row = by_subitem.get(subitem)
        if row is None:
            errors.append(f"Insight Quality Audit missing subitem: {subitem}")
            continue
        if row[0] != expected_dimension[subitem]:
            errors.append(f"Insight Quality Audit subitem {subitem} has wrong dimension: {row[0]}")
        try:
            max_score = int(row[2])
            score = int(row[3])
        except ValueError:
            errors.append(f"Insight Quality Audit subitem {subitem} has non-numeric score")
            continue
        if max_score != expected_max_scores[subitem]:
            errors.append(f"Insight Quality Audit subitem {subitem} has wrong max score: {max_score}")
        if score < 0 or score > max_score:
            errors.append(f"Insight Quality Audit subitem {subitem} score outside 0-{max_score}")
        for cell_index, label in ((4, "证据"), (5, "扣分原因"), (6, "补强动作")):
            if not row[cell_index].strip():
                errors.append(f"Insight Quality Audit subitem {subitem} missing {label}")

    dimension_totals = {"思考深度": 0, "内容质量": 0, "表达质量": 0}
    for subitem, row in by_subitem.items():
        if subitem not in expected_dimension or len(row) < 4:
            continue
        try:
            dimension_totals[expected_dimension[subitem]] += int(row[3])
        except ValueError:
            continue

    expected_subtotals = {
        "思考深度": (45, "思考深度小计"),
        "内容质量": (30, "内容质量小计"),
        "表达质量": (25, "表达质量小计"),
    }
    for dimension, (max_score, label) in expected_subtotals.items():
        match = re.search(rf"{label}：\s*(\d+)\s*/\s*{max_score}", text)
        if not match:
            errors.append(f"Insight Quality Audit missing numeric subtotal for {label}")
            continue
        declared = int(match.group(1))
        if declared != dimension_totals[dimension]:
            errors.append(f"Insight Quality Audit subtotal mismatch for {label}: declared {declared}, calculated {dimension_totals[dimension]}")

    total_match = re.search(r"总分：\s*(\d+)\s*/\s*100", text)
    if not total_match:
        errors.append("Insight Quality Audit missing numeric total score")
    else:
        declared_total = int(total_match.group(1))
        calculated_total = sum(dimension_totals.values())
        if declared_total != calculated_total:
            errors.append(f"Insight Quality Audit total mismatch: declared {declared_total}, calculated {calculated_total}")

    standard_match = re.search(r"是否达到 training-v3 标准：\s*\n-\s*(是|否)", text)
    if standard_match and standard_match.group(1) == "是":
        total = sum(dimension_totals.values())
        if total < 85 or dimension_totals["思考深度"] < 38 or dimension_totals["内容质量"] < 25 or dimension_totals["表达质量"] < 21:
            errors.append("Insight Quality Audit marks training-v3 standard as yes without meeting thresholds")


def _daily_deep_section(text: str) -> str:
    start = text.find("今日 3 个深度 case")
    if start < 0:
        return ""
    end = text.find("【今日自主训练题】", start)
    return text[start:] if end < 0 else text[start:end]


def _daily_deep_case_blocks(text: str) -> list[str]:
    section = _daily_deep_section(text)
    return [f"【Case】{part}" for part in section.split("【Case】")[1:] if part.strip()]


def _bracket_section(text: str, marker: str, stop_markers: tuple[str, ...]) -> str:
    start = text.find(marker)
    if start < 0:
        return ""
    content_start = start + len(marker)
    stops = [text.find(stop, content_start) for stop in stop_markers]
    positive_stops = [stop for stop in stops if stop >= 0]
    end = min(positive_stops) if positive_stops else len(text)
    return text[content_start:end].strip()


def _insight_total_score(text: str) -> Optional[int]:
    match = re.search(r"总分：\s*(\d+)\s*/\s*100", text)
    return int(match.group(1)) if match else None


def _validate_high_score_depth(case: str, errors: list[str], label: str) -> None:
    total_score = _insight_total_score(case)
    if total_score is None or total_score < 95:
        return

    eight_question = _bracket_section(
        case,
        "【8 问显性推理】",
        ("【分析方法总表】", "【Insight Quality Audit】", "【现象】", "| 环节 |"),
    )
    insight_overview = _bracket_section(case, "【V3.1 Insight 总览】", ("【异常信号】",))

    if len(eight_question) < HIGH_SCORE_MIN_8Q_CHARS:
        errors.append(
            f"{label}: high Insight score {total_score}/100 requires 8-question depth >= "
            f"{HIGH_SCORE_MIN_8Q_CHARS} chars; found {len(eight_question)}"
        )
    if len(insight_overview) < HIGH_SCORE_MIN_INSIGHT_CHARS:
        errors.append(
            f"{label}: high Insight score {total_score}/100 requires Insight overview >= "
            f"{HIGH_SCORE_MIN_INSIGHT_CHARS} chars; found {len(insight_overview)}"
        )


def _require_any(errors: list[str], text: str, options: list[str], label: str) -> None:
    if not any(option in text for option in options):
        errors.append(f"Missing required content: {label}")


def _validate_no_solution_first(text: str, errors: list[str]) -> None:
    first = _first_nonempty_line(text)
    solution_first_markers = (
        "【应该做什么】",
        "【核心判断】",
        "方案",
        "建议",
        "做：",
        "先做",
    )
    if first.startswith(solution_first_markers):
        errors.append("Output is solution-first; missing P6+ brake before recommendations")


def _validate_fact_separation(text: str, errors: list[str]) -> None:
    for label in ("已确认事实", "行业观点", "个人推断", "待验证假设"):
        _add_missing(errors, text, label, f"fact separation label {label}")


def _validate_single(text: str, errors: list[str]) -> None:
    _validate_no_solution_first(text, errors)
    _validate_fact_separation(text, errors)

    for label in (
        "【Case】",
        "【类型】",
        "【背景事实】",
        "【信息来源】",
        "【为什么值得分析】",
        "【本次训练目标】",
    ):
        _add_missing(errors, text, label)

    _add_missing(
        errors,
        text,
        FACT_CONFIDENCE_HEADER,
        "Fact Confidence Table",
    )

    for label in (
        "【P6+ 第一反应】",
        "【这个思路对在哪里】",
        "【这个思路为什么不够】",
        "【P7+ 刹车动作】",
    ):
        _add_missing(errors, text, label, "P6+ brake")

    _add_missing(errors, text, "【8 问显性推理】", "8-question loop heading")

    for question in (
        "1. 谁？",
        "2. 在哪？",
        "3. 损失什么？",
        "4. 想得到什么？",
        "5. 为什么卡住？",
        "6. 谁共同作用？",
        "7. 未来怎么变？",
        "8. 价值流向哪里？",
    ):
        _add_missing(errors, text, question, f"8-question loop item {question}")

    for marker in ("目的：", "分析方法：", "为什么用这个方法：", "推导过程：", "阶段结论：", "如何影响下一步："):
        count = text.count(marker)
        if count < 8:
            errors.append(f"8-question loop requires at least 8 occurrences of {marker}; found {count}")

    _add_missing(
        errors,
        text,
        "| 环节 | 分析方法 | 为什么使用 | 得到什么结论 | 对后续判断的价值 |",
        "analysis method table",
    )

    for label in (
        "【V3.1 Insight 总览】",
        "【异常信号】",
        "【V3.1 分析方法工作台】",
        "【P7+ 追问深答】",
        "【底层矛盾与因果机制】",
        "【系统关系与价值迁移】",
        "【反面论证与边界条件】",
    ):
        _add_missing(errors, text, label, "V3.1 insight layer")

    for marker in ("一句话 Insight：", "核心判断：", "行动取舍：", "深度回答：", "可能反驳：", "回应反驳："):
        if marker not in text:
            errors.append(f"V3.1 insight layer missing marker: {marker}")

    _validate_insight_quality_audit(text, errors)

    for label in ("【现象】", "【原因】", "【本质】", "【系统】", "【趋势】", "【机会】"):
        _add_missing(errors, text, label, "6-layer summary")

    for label in (
        "【核心判断】",
        "【应该做什么】",
        "【不应该做什么】",
        "【先验证什么】",
        "【关键假设】",
        "【验证指标】",
        "【最小可行方案】",
        "【长期机会】",
        "【最大风险】",
    ):
        _add_missing(errors, text, label, "final judgment and tradeoff")

    for label in (
        "如果我在面试或汇报中表达",
        "【PREP 表达版本】",
        "Point 观点：",
        "Reason 理由：",
        "Example 例证：",
        "Point 回收：",
        "【SCQA 表达版本】",
        "Situation：",
        "Complication：",
        "Question：",
        "Answer：",
        "【训练能力】",
        "【P6+ 易犯错误】",
        "【P7+ 正确思路】",
        "【可复用 Pattern】",
        "【迁移方式】",
        "【Case Asset Card】",
    ):
        _add_missing(errors, text, label)

    for field_name in ASSET_CARD_REQUIRED_FIELDS:
        _add_missing(errors, text, field_name, f"Case Asset Card field {field_name}")

    if "这不是" not in text or "而是" not in text:
        errors.append("Missing P7+ essence sentence using '这不是 X，而是 Y'")
    if "最大机会不在" not in text or "而在" not in text:
        errors.append("Missing opportunity tradeoff sentence using '最大机会不在 A，而在 B'")


def _validate_daily(text: str, errors: list[str]) -> None:
    required_daily_labels = (
        "今日候选 case 池",
        "Case Selection Score",
        "【今日深度 case 选择理由】",
        "Case A：",
        "Case B：",
        "Case C：",
        "今日雷达简报",
        "今日 3 个深度 case",
        "【今日自主训练题】",
        "旧 case 复现",
        "遗忘曲线",
        "今日训练复盘",
        "Quality Review Rubric",
    )
    missing_exact_labels = [label for label in required_daily_labels if label not in text]
    for label in required_daily_labels:
        _add_missing(errors, text, label)

    source_header = "| 来源通道 | 状态 | 用途 | 限制与降级处理 |"
    _add_missing(errors, text, "来源通道使用情况", "daily source channel usage record")
    _add_missing(errors, text, source_header, "daily source channel table")
    source_rows = _table_rows(text, source_header)
    source_channels = {
        row[0]: row for row in source_rows if len(row) >= 4 and row[0] in {
            "Search API / Web Search",
            "AI HOT",
            "GitHub / Open-source",
        }
    }
    for channel in ("Search API / Web Search", "AI HOT", "GitHub / Open-source"):
        if channel not in source_channels:
            errors.append(f"Daily mode missing required source channel: {channel}")
            continue
        row = source_channels[channel]
        if row[1] not in {"已使用", "不可用"}:
            errors.append(f"Daily source channel {channel} has invalid status: {row[1]}")
        if row[1] == "不可用":
            fallback = " ".join(row[2:])
            if not any(marker in fallback for marker in ("待核验", "待验证假设")):
                errors.append(f"Unavailable source channel {channel} must downgrade affected claims")
            if "最终判断" not in fallback:
                errors.append(f"Unavailable source channel {channel} must state final-judgment impact")

    _add_missing(
        errors,
        text,
        "| Case | 类型 | 来源 | 事实等级 | 相关性 | 信号强度 | 训练价值 | 可验证性 | 资产化价值 | 总分 | 处理方式 |",
        "candidate Case Selection Score table",
    )
    _add_missing(
        errors,
        text,
        "| 标题 | 类型 | 一句话结论 | 为什么值得看 | 链接 | 后续动作 |",
        "radar brief table",
    )
    required_table_headers = (
        source_header,
        "| Case | 类型 | 来源 | 事实等级 | 相关性 | 信号强度 | 训练价值 | 可验证性 | 资产化价值 | 总分 | 处理方式 |",
        "| 标题 | 类型 | 一句话结论 | 为什么值得看 | 链接 | 后续动作 |",
        "| 维度 | 分数 1-5 | 简评 | 下一步如何补强 |",
    )
    missing_exact_headers = [header for header in required_table_headers if header not in text]

    row_count = _candidate_row_count(text)
    if not 8 <= row_count <= 13:
        errors.append(f"Daily mode requires 8-13 candidate cases; found {row_count}")

    deep_section = _daily_deep_section(text)
    forbidden_found = [phrase for phrase in FORBIDDEN_DAILY_DEEP_PHRASES if phrase in deep_section]
    for phrase in forbidden_found:
        errors.append(f"Daily deep cases use forbidden simplified phrase: {phrase}")
    for phrase in FORBIDDEN_BOILERPLATE_PHRASES:
        count = deep_section.count(phrase)
        if count >= 3:
            errors.append(f"Daily deep cases repeat boilerplate/template phrase {count} times: {phrase}")

    deep_cases = _daily_deep_case_blocks(text)
    if len(deep_cases) != 3:
        errors.append(f"Daily mode requires 3 complete deep cases; found {len(deep_cases)}")

    incomplete_case_indexes: list[int] = []
    c_level_final_support = False
    for index, case in enumerate(deep_cases[:3], start=1):
        case_errors: list[str] = []
        _validate_single(case, case_errors)
        if case_errors:
            incomplete_case_indexes.append(index)
            errors.extend(f"Deep case {index}: {error}" for error in case_errors)
        _validate_high_score_depth(case, errors, f"Deep case {index}")
        for row in _table_rows(case, FACT_CONFIDENCE_HEADER):
            if len(row) >= 5 and row[2].strip().upper() == "C" and row[3].strip().lower() in {"是", "yes", "可以"}:
                c_level_final_support = True
                errors.append(f"Deep case {index}: C-level fact cannot independently support final judgment")

    missing_deep_flow = len(deep_cases) != 3 or bool(incomplete_case_indexes)
    case_b_or_c_incomplete = len(deep_cases) < 3 or any(index in {2, 3} for index in incomplete_case_indexes) or bool(forbidden_found)

    cards = _asset_card_blocks(text)
    if len(cards) < 3:
        errors.append("Daily mode requires at least 3 Case Asset Cards")
    for index, card in enumerate(cards[:3], start=1):
        _validate_asset_card_v51(card, errors, f"Daily Case Asset Card {index}")
    card_missing = len(cards) < 3 or any(
        any(field not in card for field in ASSET_CARD_REQUIRED_FIELDS)
        for card in cards[:3]
    )

    for threshold in ("21-25", "17-20", "13-16", "12 以下"):
        if threshold not in text:
            errors.append(f"Missing Case Selection Score threshold: {threshold}")

    score_header = "| Case | 类型 | 来源 | 事实等级 | 相关性 | 信号强度 | 训练价值 | 可验证性 | 资产化价值 | 总分 | 处理方式 |"
    for row in _table_rows(text, score_header):
        if len(row) < 11:
            continue
        try:
            dimensions = [int(value) for value in row[4:9]]
            total = int(row[9])
        except ValueError:
            errors.append(f"Case Selection Score row for {row[0]} contains non-numeric scores")
            continue
        if any(value < 1 or value > 5 for value in dimensions):
            errors.append(f"Case Selection Score row for {row[0]} has a dimension outside 1-5")
        if sum(dimensions) != total:
            errors.append(f"Case Selection Score total mismatch for {row[0]}")

    rubric_header = "| 维度 | 分数 1-5 | 简评 | 下一步如何补强 |"
    rubric_rows = _table_rows(text, rubric_header)
    required_dimensions = (
        "事实可靠性",
        "本质抽象深度",
        "系统关系清晰度",
        "趋势推演可信度",
        "机会判断质量",
        "取舍明确度",
        "验证方案可执行性",
        "Case Asset Card 可复用度",
    )
    rubric_by_dimension = {row[0]: row for row in rubric_rows if len(row) >= 4}
    rubric_scores: dict[str, int] = {}
    for dimension in required_dimensions:
        row = rubric_by_dimension.get(dimension)
        if row is None:
            errors.append(f"Quality Review Rubric missing dimension: {dimension}")
            continue
        try:
            score = int(row[1])
        except ValueError:
            errors.append(f"Quality Review Rubric has invalid score for {dimension}")
            continue
        rubric_scores[dimension] = score
        if not 1 <= score <= 5:
            errors.append(f"Quality Review Rubric score outside 1-5 for {dimension}")
        if not row[2]:
            errors.append(f"Quality Review Rubric missing review for {dimension}")
        if score < 4 and not row[3]:
            errors.append(f"Quality Review Rubric score below 4 requires 下一步如何补强 for {dimension}")

    asset_score = rubric_scores.get("Case Asset Card 可复用度")
    if errors and asset_score is not None and asset_score > 3:
        errors.append("Quality Review Guardrail: Case Asset Card 可复用度 must be at most 3 when validation fails")

    rubric_text = " ".join(" ".join(row[2:4]) for row in rubric_rows if len(row) >= 4)
    if missing_deep_flow and not (
        any(term in rubric_text for term in ("补全", "完整流程"))
        and any(term in rubric_text for term in ("deep case", "case", "流程"))
    ):
        errors.append("Quality Review Guardrail: missing deep-case full flow must be stated in 下一步如何补强")

    if case_b_or_c_incomplete:
        for dimension in ("本质抽象深度", "系统关系清晰度", "Case Asset Card 可复用度"):
            if rubric_scores.get(dimension, 0) > 3:
                errors.append(f"Quality Review Guardrail: {dimension} must be at most 3 when Case B or Case C is incomplete")

    if c_level_final_support and rubric_scores.get("事实可靠性", 0) > 3:
        errors.append("Quality Review Guardrail: 事实可靠性 must be at most 3 when C-level facts support final judgment")

    if card_missing and asset_score is not None and asset_score > 3:
        errors.append("Quality Review Guardrail: Case Asset Card 可复用度 must be at most 3 when required card fields are missing")

    if (missing_exact_labels or missing_exact_headers) and "结构" not in rubric_text:
        errors.append("Quality Review Guardrail: rubric must name the structural issue caused by paraphrased headings or table headers")

    for phrase in ("没有选择更热 case 的原因", "请你先回答 8 问", "做 / 不做 / 先验证"):
        _add_missing(errors, text, phrase)


def _validate_diagnosis(text: str, errors: list[str]) -> None:
    for label in (
        "【你的答案当前更像】",
        "P6+",
        "P7",
        "P7+",
        "【做得好的地方】",
        "【主要短板】",
        "【如果升级到 P7，应该补什么】",
        "【如果升级到 P7+，应该补什么】",
        "【改写后的 P7+ 版本】",
    ):
        _add_missing(errors, text, label, "diagnosis output")


def _validate_3d(text: str, errors: list[str]) -> None:
    _require_any(errors, text, ["3D", "空间"], "3D/spatial context")
    for term in ("可编辑", "可复用", "可交付"):
        _add_missing(errors, text, term, "3D deliverability")
    _add_missing(errors, text, "工作流", "3D workflow")
    _require_any(errors, text, ["3D Eval", "验收"], "3D evaluation/acceptance")


def _validate_psychology(text: str, errors: list[str]) -> None:
    clinical_patterns = (
        r"诊断为",
        r"确诊",
        r"治疗方案",
        r"处方",
        r"用药",
    )
    for pattern in clinical_patterns:
        if re.search(pattern, text):
            errors.append("AI psychology output crosses clinical/诊断 safety boundary")
            break

    for term in ("危机", "隐私", "伦理", "转介"):
        _add_missing(errors, text, term, "AI psychology safety boundary")
    _require_any(errors, text, ["效果评价", "信效度", "量表", "长期效果"], "AI psychology effect evidence")


def _validate_github(text: str, errors: list[str]) -> None:
    terms = {
        "star": ["star", "Star"],
        "fork": ["fork", "Fork"],
        "commit": ["commit", "Commit"],
        "release": ["release", "Release"],
        "issue_or_pr": ["issue", "Issue", "PR", "pull request"],
        "readme": ["README", "文档"],
        "demo_or_docs": ["demo", "Demo", "docs", "Docs", "示例"],
        "workflow_or_productization": ["工作流", "workflow", "产品化", "基础设施", "控制点"],
    }
    missing = [name for name, options in terms.items() if not any(option in text for option in options)]
    if missing:
        errors.append(f"GitHub/open-source analysis is incomplete; missing {', '.join(missing)}")


def validate_text(text: str, mode: str, domains: Optional[list[str]] = None) -> ValidationResult:
    result = ValidationResult()
    normalized_domains = {domain.lower() for domain in (domains or [])}

    if mode == "single":
        _validate_single(text, result.errors)
    elif mode == "daily":
        _validate_daily(text, result.errors)
    elif mode == "diagnosis":
        _validate_diagnosis(text, result.errors)
    else:
        result.errors.append(f"Unknown mode: {mode}")

    if "3d" in normalized_domains or "spatial" in normalized_domains:
        _validate_3d(text, result.errors)
    if "psychology" in normalized_domains or "心理" in normalized_domains:
        _validate_psychology(text, result.errors)
    if "github" in normalized_domains or "open-source" in normalized_domains:
        _validate_github(text, result.errors)

    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate Hermes P7+ Markdown output.")
    parser.add_argument("file", type=Path, help="Markdown output file to validate")
    parser.add_argument("--mode", choices=("daily", "single", "diagnosis"), required=True)
    parser.add_argument(
        "--domain",
        action="append",
        default=[],
        choices=("3d", "spatial", "psychology", "心理", "github", "open-source"),
        help="Optional domain-specific checks; repeatable",
    )
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    text = args.file.read_text(encoding="utf-8")
    result = validate_text(text, mode=args.mode, domains=args.domain)

    if result.ok:
        print("PASS: Hermes output conforms to the requested contract.")
        return 0

    print("FAIL: Hermes output does not conform:", file=sys.stderr)
    for error in result.errors:
        print(f"- {error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
