#!/usr/bin/env python3
"""Render Hermes daily training Markdown into a reader-first responsive HTML page."""

from __future__ import annotations

import argparse
import html
import re
import sys
from dataclasses import dataclass
from pathlib import Path


SECTION_TITLES = (
    "今日阅读导读",
    "来源与候选",
    "Case A",
    "Case B",
    "Case C",
    "表达演练",
    "资产卡",
    "复习",
)


@dataclass
class SourceStatus:
    channel: str
    status: str


@dataclass
class CandidateInfo:
    title: str
    case_type: str
    source: str
    fact_grade: str
    relevance: str
    signal_strength: str
    training_value: str
    verifiability: str
    asset_value: str
    total: str
    handling: str
    description: str = ""
    links: str = ""
    score_reason: str = ""
    radar_conclusion: str = ""
    radar_value: str = ""
    next_action: str = ""


@dataclass
class SelectionReason:
    label: str
    reason: str
    training_goal: str
    tradeoff: str


@dataclass
class CaseInfo:
    index: int
    label: str
    title: str
    anchor: str
    content: str
    insight: str
    judgment: str
    do: str
    dont: str
    validate: str
    total_score: str
    thinking_score: str
    content_score: str
    expression_score: str
    weak_point: str
    improvement: str
    asset_grade: str
    watchlist_status: str


def default_output_path(markdown_path: Path) -> Path:
    name = markdown_path.name
    if name.endswith("-raw.md"):
        return markdown_path.with_name(name.replace("-raw.md", "-reader.html"))
    return markdown_path.with_suffix(".reader.html")


def _slug(text: str, fallback: str) -> str:
    ascii_slug = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return ascii_slug or fallback


def _linkify_escaped(text: str) -> str:
    pattern = re.compile(r"(https?://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+)")

    def replace(match: re.Match[str]) -> str:
        url = match.group(1).rstrip(".,，。)")
        suffix = match.group(1)[len(url) :]
        return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{url}</a>{suffix}'

    return pattern.sub(replace, text)


def _clean_reader_copy(text: str) -> str:
    text = re.sub(r"\bV\d+\.\d+\s+", "", text)
    text = re.sub(r"\bHermes skill\b", "训练系统", text)
    text = re.sub(r"\bHermes\b", "本训练体系", text)
    text = re.sub(r"\bV\d+(?:/V\d+)+\b", "多轮样本", text)
    text = re.sub(r"\bV\d+\b", "样本版本", text)
    text = text.replace("盲测", "连续样本验证")
    text = text.replace("HTML Pro Max", "阅读体验优化")
    text = text.replace("Markdown 输出", "训练稿输出")
    text = text.replace("validator", "结构校验器")
    text = text.replace("差距报告", "质量对比报告")
    text = text.replace("本训练体系 ", "本训练体系")
    text = text.replace(" 本训练体系", "本训练体系")
    text = text.replace("对 训练系统 的", "对本训练体系的")
    text = text.replace("训练系统 合并", "训练系统合并")
    text = text.replace("本训练体系GitHub", "本训练体系的 GitHub")
    text = text.replace("多轮样本 已", "多轮样本已")
    text = text.replace("多轮样本 输出", "多轮样本输出")
    text = text.replace("样本版本 继续", "后续版本继续")
    text = text.replace("连续连续样本验证", "连续样本验证")
    text = text.replace("做 / 不做 / 先验证", "建议推进 / 暂不推进 / 优先验证")
    text = text.replace("做 / 不做 / 优先验证", "建议推进 / 暂不推进 / 优先验证")
    text = text.replace("不做：", "暂不推进：")
    text = re.sub(r"(?<!不)做：", "建议推进：", text)
    text = text.replace("不建议推进：", "暂不推进：")
    text = re.sub(r"(?<!优)先验证：", "优先验证：", text)
    text = text.replace("优优先验证", "优先验证")
    return text


INLINE_LABEL_BLOCKLIST = {
    "它有价值的地方是：",
}


SEMANTIC_ROLE_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "risk",
        (
            "暂不推进",
            "不做",
            "主要风险",
            "最大风险",
            "风险",
            "待验证假设",
            "关键假设",
            "扣分点",
            "为什么不够",
            "阻力",
        ),
    ),
    (
        "next",
        (
            "如何影响下一步",
            "后续关注",
            "后续动作",
            "下一步",
            "迁移方式",
            "可迁移",
        ),
    ),
    (
        "practice",
        (
            "优先验证",
            "先验证",
            "验证",
            "表达",
            "演练",
            "PREP",
            "SCQA",
            "面试",
            "汇报",
            "2 分钟",
        ),
    ),
    (
        "action",
        (
            "建议推进",
            "行动取舍",
            "可复用 Pattern",
            "Watchlist 状态",
            "未来 Watchlist",
            "关注对象",
            "关注指标",
            "复习优先级",
            "做：",
            "做:",
        ),
    ),
    (
        "insight",
        (
            "核心 Insight",
            "一句话 Insight",
            "最重要 Insight",
            "核心判断",
            "一句话本质",
            "本质上",
            "本质判断",
            "本质",
        ),
    ),
    (
        "conclusion",
        (
            "结论先行",
            "阶段结论",
            "最终判断",
            "所以我的最终判断",
            "机会判断",
            "最大机会",
            "长期形态",
            "长期趋势",
            "结论",
            "机会",
        ),
    ),
    (
        "evidence",
        (
            "已确认事实",
            "行业观点",
            "信息来源",
            "来源",
            "事实",
            "背景事实",
            "发生了什么",
            "当前信号",
            "事实等级",
            "现象",
        ),
    ),
    (
        "process",
        (
            "目的",
            "分析方法",
            "为什么用这个方法",
            "推导过程",
            "原因",
            "系统",
            "趋势",
            "谁",
            "在哪",
            "损失什么",
            "想得到什么",
            "为什么卡住",
            "谁共同作用",
            "未来怎么变",
            "价值流向哪里",
        ),
    ),
)


def _extract_inline_label(stripped: str) -> tuple[str, str] | None:
    if stripped.startswith(("http://", "https://")):
        return None
    label_match = re.match(r"^([^：:]{1,18}[：:])\s*(.*)$", stripped)
    if not label_match:
        return None
    label, rest = label_match.groups()
    if (
        label in INLINE_LABEL_BLOCKLIST
        or "://" in label
        or "“" in label
        or "”" in label
    ):
        return None
    return label, rest


def _semantic_role(label: str, text: str = "") -> str:
    label_clean = label.strip().rstrip("：:")
    if label_clean in {"建议推进", "做"}:
        return "action"
    if label_clean in {"暂不推进", "不做", "主要风险", "最大风险"}:
        return "risk"
    if label_clean in {"优先验证", "先验证"}:
        return "practice"
    if label_clean in {"Pattern", "可复用 Pattern"}:
        return "action"
    if label_clean.startswith("迁移到"):
        return "next"
    if label_clean == "P7+ 要问":
        return "conclusion"
    if (
        "建议推进 / 暂不推进 / 优先验证" in label_clean
        or "做 / 不做 / 先验证" in label_clean
        or "做 / 不做 / 优先验证" in label_clean
        or "行动取舍" in label_clean
    ):
        return "action"
    haystack = f"{label} {text}".lower()
    exact_keywords = {"谁", "在哪"}
    for role, keywords in SEMANTIC_ROLE_KEYWORDS:
        for keyword in keywords:
            keyword_lower = keyword.lower()
            if keyword in exact_keywords:
                if label_clean == keyword:
                    return role
                continue
            if keyword_lower in haystack:
                return role
    return "neutral"


def _semantic_classes(label: str, text: str = "", base_class: str = "semantic-item") -> str:
    role = _semantic_role(label, text)
    classes = [base_class]
    if role != "neutral":
        classes.extend(("semantic-item", f"semantic-{role}", f"{base_class}-{role}"))
    return " ".join(dict.fromkeys(classes))


def _semantic_label_class(label: str, text: str = "") -> str:
    role = _semantic_role(label, text)
    if role == "neutral":
        return ""
    return f" semantic-label semantic-label-{role}"


def _display_title(title: str) -> str:
    clean = title.replace("Hermes ", "")
    clean = re.sub(r"\s+V\d+\s+Raw\b", "", clean, flags=re.I)
    clean = re.sub(r"\s+Raw\b", "", clean, flags=re.I)
    return clean.strip()


def _inline(text: str, *, clean: bool = True) -> str:
    if clean:
        text = _clean_reader_copy(text)
    placeholders: list[str] = []

    def stash(value: str) -> str:
        token = f"@@HERMES_PLACEHOLDER_{len(placeholders)}@@"
        placeholders.append(value)
        return token

    def markdown_link(match: re.Match[str]) -> str:
        label = html.escape(match.group(1), quote=False)
        url = html.escape(match.group(2), quote=True)
        return stash(f'<a href="{url}" target="_blank" rel="noopener noreferrer">{label}</a>')

    def inline_code(match: re.Match[str]) -> str:
        code = html.escape(match.group(1), quote=False)
        return stash(f"<code>{code}</code>")

    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", markdown_link, text)
    text = re.sub(r"`([^`]+)`", inline_code, text)
    escaped = html.escape(text, quote=False)
    escaped = _linkify_escaped(escaped)
    for index, value in enumerate(placeholders):
        escaped = escaped.replace(f"@@HERMES_PLACEHOLDER_{index}@@", value)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def _extract_title(markdown: str, source_name: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return source_name or "Hermes P7+ Daily Training"


def _extract_date_version(title: str, source_name: str) -> tuple[str, str]:
    date_match = re.search(r"(20\d{2}-\d{2}-\d{2})", title)
    version_match = re.search(r"\b(V\d+)\b", title, flags=re.I)
    if not version_match:
        version_match = re.search(r"training-(v\d+)", source_name, flags=re.I)
    date = date_match.group(1) if date_match else "-"
    version = version_match.group(1).upper() if version_match else "-"
    return date, version


def _source_channel_status(markdown: str) -> list[SourceStatus]:
    rows: list[SourceStatus] = []
    lines = markdown.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != "| 来源通道 | 状态 | 用途 | 限制与降级处理 |":
            continue
        for row in lines[index + 2 :]:
            if not row.strip().startswith("|"):
                break
            cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
            if len(cells) >= 2:
                rows.append(SourceStatus(cells[0], cells[1]))
        break
    return rows


def _heading_level(heading: str) -> int:
    return len(heading) - len(heading.lstrip("#"))


def _extract_heading_section(markdown: str, heading: str) -> str:
    lines = markdown.splitlines()
    level = _heading_level(heading)
    start = None
    for index, line in enumerate(lines):
        if line.strip() == heading:
            start = index + 1
            break
    if start is None:
        return ""
    end = len(lines)
    for index in range(start, len(lines)):
        stripped = lines[index].strip()
        if not stripped.startswith("#"):
            continue
        match = re.match(r"^(#{1,6})\s+", stripped)
        if match and len(match.group(1)) <= level:
            end = index
            break
    return "\n".join(lines[start:end]).strip()


def _parse_markdown_table(section: str, header_prefix: str) -> list[list[str]]:
    lines = section.splitlines()
    for index, line in enumerate(lines):
        if not line.strip().startswith(header_prefix):
            continue
        rows: list[list[str]] = []
        for row in lines[index + 2 :]:
            if not row.strip().startswith("|"):
                break
            cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
            if cells and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
                continue
            rows.append(cells)
        return rows
    return []


def _candidate_key(title: str) -> str:
    return re.sub(r"[\s\W_]+", "", title, flags=re.UNICODE).lower()


def _parse_candidate_quick_cards(markdown: str) -> list[dict[str, str]]:
    section = _extract_heading_section(markdown, "### 候选 case 快速认知卡片")
    cards: list[dict[str, str]] = []
    for raw_line in section.splitlines():
        line = raw_line.strip()
        if not re.match(r"^\d+\.\s+", line):
            continue
        try:
            item = re.sub(r"^\d+\.\s+", "", line)
            title, rest = item.split("：一句话描述是，", 1)
            description, rest = rest.split("。溯源链接：", 1)
            links, rest = rest.split("。为什么是", 1)
            _score_text, rest = rest.split("分：", 1)
            score_reason, handling = rest.rsplit("。处理方式：", 1)
        except ValueError:
            continue
        cards.append({
            "title": title.strip(),
            "key": _candidate_key(title),
            "description": description.strip(),
            "links": links.strip(),
            "score_reason": score_reason.strip(),
            "handling": handling.strip().rstrip("。"),
        })
    return cards


def _text_tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+|[\u4e00-\u9fff]+", text.lower()))


def _similarity(left: str, right: str) -> float:
    left_key = _candidate_key(left)
    right_key = _candidate_key(right)
    if left_key and right_key and (left_key.startswith(right_key) or right_key.startswith(left_key)):
        return 1.0
    left_tokens = _text_tokens(left)
    right_tokens = _text_tokens(right)
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / min(len(left_tokens), len(right_tokens))


def _find_quick_card(title: str, quick_cards: list[dict[str, str]], index: int) -> dict[str, str]:
    title_key = _candidate_key(title)
    best: dict[str, str] = {}
    best_score = 0.0
    for card in quick_cards:
        key = card.get("key", "")
        if title_key.startswith(key) or key.startswith(title_key):
            return card
        score = _similarity(title, card.get("title", ""))
        if score > best_score:
            best_score = score
            best = card
    if best_score >= 0.55:
        return best
    if index < len(quick_cards):
        return quick_cards[index]
    return {}


def _parse_radar_infos(markdown: str) -> list[dict[str, str]]:
    section = _extract_heading_section(markdown, "## 三、今日雷达简报")
    infos: list[dict[str, str]] = []
    for row in _parse_markdown_table(section, "| 标题 |"):
        if len(row) < 6:
            continue
        infos.append(
            {
                "title": row[0],
                "type": row[1],
                "conclusion": row[2],
                "value": row[3],
                "link": row[4],
                "action": row[5],
            }
        )
    return infos


def _find_radar_info(title: str, radar_infos: list[dict[str, str]]) -> dict[str, str]:
    best: dict[str, str] = {}
    best_score = 0.0
    for info in radar_infos:
        score = _similarity(title, info.get("title", ""))
        if score > best_score:
            best_score = score
            best = info
    if best_score >= 0.45:
        return best
    return {}


def _parse_candidate_infos(markdown: str) -> list[CandidateInfo]:
    section = _extract_heading_section(markdown, "## 一、今日候选 case 池 + Case Selection Score")
    quick_cards = _parse_candidate_quick_cards(markdown)
    radar_infos = _parse_radar_infos(markdown)
    candidates: list[CandidateInfo] = []
    for index, row in enumerate(_parse_markdown_table(section, "| Case |")):
        if len(row) < 11:
            continue
        quick = _find_quick_card(row[0], quick_cards, index)
        radar = _find_radar_info(row[0], radar_infos)
        candidates.append(
            CandidateInfo(
                title=row[0],
                case_type=row[1],
                source=row[2],
                fact_grade=row[3],
                relevance=row[4],
                signal_strength=row[5],
                training_value=row[6],
                verifiability=row[7],
                asset_value=row[8],
                total=row[9],
                handling=quick.get("handling") or row[10],
                description=quick.get("description") or radar.get("conclusion", ""),
                links=quick.get("links") or radar.get("link") or row[2],
                score_reason=quick.get("score_reason") or radar.get("value", ""),
                radar_conclusion=radar.get("conclusion", ""),
                radar_value=radar.get("value", ""),
                next_action=radar.get("action", ""),
            )
        )
    return candidates


def _parse_selection_reasons(markdown: str) -> list[SelectionReason]:
    section = _extract_heading_section(markdown, "## 二、今日深度 case 选择理由")
    reasons: list[SelectionReason] = []
    matches = list(re.finditer(r"^Case ([ABC])：$", section, flags=re.M))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(section)
        block = section[match.end() : end]
        reasons.append(
            SelectionReason(
                label=f"Case {match.group(1)}",
                reason=_line_value(block, "选择原因："),
                training_goal=_line_value(block, "训练目标："),
                tradeoff=_line_value(block, "没有选择更热 case 的原因："),
            )
        )
    return reasons


def _line_value(block: str, label: str) -> str:
    for line in block.splitlines():
        stripped = line.strip()
        if stripped.startswith(label):
            return stripped[len(label) :].strip()
    return ""


def _field_after_label(block: str, label: str) -> str:
    lines = block.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != label:
            continue
        values: list[str] = []
        for candidate in lines[index + 1 :]:
            stripped = candidate.strip()
            if not stripped:
                if values:
                    break
                continue
            if stripped.startswith("【") and stripped.endswith("】"):
                break
            if re.fullmatch(r"[\u4e00-\u9fffA-Za-z0-9 /+：:（）()]+：", stripped) and values:
                break
            values.append(stripped)
        return " ".join(values).strip()
    return ""


def _section_between(block: str, start_label: str, end_labels: tuple[str, ...]) -> str:
    lines = block.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == start_label:
            start = index + 1
            break
    if start is None:
        return ""
    end = len(lines)
    for index in range(start, len(lines)):
        stripped = lines[index].strip()
        if stripped in end_labels:
            end = index
            break
    return "\n".join(lines[start:end]).strip()


def _extract_actions(block: str) -> tuple[str, str, str]:
    section = _section_between(block, "行动取舍：", ("【异常信号】", "【V3.1 分析方法工作台】"))
    do = dont = validate = ""
    for line in section.splitlines():
        stripped = line.strip().lstrip("-").strip()
        if stripped.startswith("做："):
            do = stripped[2:].strip()
        elif stripped.startswith("不做："):
            dont = stripped[3:].strip()
        elif stripped.startswith("先验证："):
            validate = stripped[4:].strip()
    return do, dont, validate


def _first_bullet_after(block: str, label: str) -> str:
    section = _field_after_label(block, label)
    section = section.replace("- ", "").strip()
    return section


def _score_after(block: str, label: str) -> str:
    match = re.search(rf"^{re.escape(label)}\s*(.+)$", block, flags=re.M)
    return match.group(1).strip() if match else ""


def _split_cases(markdown: str) -> list[CaseInfo]:
    matches = list(re.finditer(r"^### Case ([ABC])：(.+)$", markdown, flags=re.M))
    cases: list[CaseInfo] = []
    for index, match in enumerate(matches, start=1):
        end = matches[index].start() if index < len(matches) else len(markdown)
        next_daily = re.search(r"^## 五、", markdown[match.end() : end], flags=re.M)
        if next_daily:
            end = match.end() + next_daily.start()
        content = markdown[match.end() : end].strip()
        insight = _field_after_label(content, "一句话 Insight：")
        judgment = _field_after_label(content, "核心判断：")
        do, dont, validate = _extract_actions(content)
        total = _score_after(content, "总分：")
        thinking = _score_after(content, "思考深度小计：")
        content_score = _score_after(content, "内容质量小计：")
        expression = _score_after(content, "表达质量小计：")
        weak = _first_bullet_after(content, "主要扣分点：")
        improvement = _first_bullet_after(content, "下一步补强：")
        asset_grade = _field_after_label(content, "资产等级：").lstrip("-").strip()
        watchlist = _field_after_label(content, "Watchlist 状态：").lstrip("-").strip()
        label = f"Case {match.group(1)}"
        title = match.group(2).strip()
        cases.append(
            CaseInfo(
                index=index,
                label=label,
                title=title,
                anchor=f"case-{index}",
                content=content,
                insight=insight,
                judgment=judgment,
                do=do,
                dont=dont,
                validate=validate,
                total_score=total,
                thinking_score=thinking,
                content_score=content_score,
                expression_score=expression,
                weak_point=weak,
                improvement=improvement,
                asset_grade=asset_grade,
                watchlist_status=watchlist,
            )
        )
    return cases


def _prelude(markdown: str) -> str:
    match = re.search(r"^### Case [ABC]：", markdown, flags=re.M)
    return markdown[: match.start()].strip() if match else markdown


def _postlude(markdown: str) -> str:
    match = re.search(r"^## 五、", markdown, flags=re.M)
    return markdown[match.start() :].strip() if match else ""


def _average_score(cases: list[CaseInfo]) -> str:
    values: list[int] = []
    for case in cases:
        match = re.match(r"(\d+)\s*/\s*100", case.total_score)
        if match:
            values.append(int(match.group(1)))
    if not values:
        return "-"
    return f"{round(sum(values) / len(values), 1)}/100"


def _strongest_case(cases: list[CaseInfo]) -> CaseInfo | None:
    def value(case: CaseInfo) -> int:
        match = re.match(r"(\d+)\s*/\s*100", case.total_score)
        return int(match.group(1)) if match else 0

    return max(cases, key=value) if cases else None


def _render_table(lines: list[str], start: int) -> tuple[str, int]:
    table_lines: list[str] = []
    index = start
    while index < len(lines) and lines[index].strip().startswith("|"):
        table_lines.append(lines[index])
        index += 1

    rows = []
    for row in table_lines:
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        rows.append(cells)

    if not rows:
        return "", index

    header = rows[0]
    body = rows[1:]
    html_lines = ['<div class="table-wrap"><table>']
    html_lines.append("<thead><tr>" + "".join(f"<th>{_inline(cell)}</th>" for cell in header) + "</tr></thead>")
    if body:
        html_lines.append("<tbody>")
        for row in body:
            html_lines.append("<tr>" + "".join(f"<td>{_inline(cell)}</td>" for cell in row) + "</tr>")
        html_lines.append("</tbody>")
    html_lines.append("</table></div>")
    return "\n".join(html_lines), index


def _render_markdown_fragment(markdown: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    paragraph: list[str] = []

    def render_line(line: str) -> str:
        stripped = line.strip()
        label_match = _extract_inline_label(stripped)
        if label_match:
            label, rest = label_match
            rest_html = _inline(rest) if rest else ""
            label_class = _semantic_label_class(label, rest)
            return f'<span class="inline-label{label_class}">{_inline(label)}</span>{rest_html}'
        return _inline(line)

    def flush_paragraph() -> None:
        if paragraph:
            class_attr = ""
            label_match = _extract_inline_label(paragraph[0].strip())
            if label_match:
                class_attr = f' class="{_semantic_classes(label_match[0], label_match[1], "semantic-paragraph")}"'
            out.append(f"<p{class_attr}>" + "<br>".join(render_line(line) for line in paragraph) + "</p>")
            paragraph.clear()

    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            index += 1
            continue
        if stripped.startswith("|"):
            flush_paragraph()
            table_html, index = _render_table(lines, index)
            if table_html:
                out.append(table_html)
            continue
        heading_match = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading_match:
            flush_paragraph()
            hashes, text = heading_match.groups()
            level = min(len(hashes) + 1, 5)
            anchor = _slug(text, f"section-{index}")
            out.append(f'<h{level} id="{anchor}">{_inline(text)}</h{level}>')
            index += 1
            continue
        if stripped.startswith("- "):
            flush_paragraph()
            items: list[str] = []
            while index < len(lines) and lines[index].strip().startswith("- "):
                items.append(lines[index].strip()[2:])
                index += 1
            out.append("<ul>" + "".join(f"<li>{_inline(item)}</li>" for item in items) + "</ul>")
            continue
        if re.match(r"^\d+\.\s+", stripped):
            flush_paragraph()
            items = []
            while index < len(lines) and re.match(r"^\d+\.\s+", lines[index].strip()):
                items.append(re.sub(r"^\d+\.\s+", "", lines[index].strip()))
                index += 1
            out.append("<ol>" + "".join(f"<li>{_inline(item)}</li>" for item in items) + "</ol>")
            continue
        paragraph.append(line)
        index += 1

    flush_paragraph()
    return "\n".join(out)


EIGHT_QUESTION_FIELDS = (
    "目的",
    "分析方法",
    "为什么用这个方法",
    "推导过程",
    "阶段结论",
    "如何影响下一步",
)

EIGHT_QUESTION_DIMENSIONS = {
    "谁": "对象与利益相关者",
    "在哪": "场景与使用位置",
    "损失什么": "成本与损失",
    "想得到什么": "收益与 JTBD",
    "为什么卡住": "底层矛盾",
    "谁共同作用": "系统变量",
    "未来怎么变": "趋势推演",
    "价值流向哪里": "价值迁移",
}

PHASE_LABELS = ("现在", "阶段 1", "阶段 2", "长期形态")
SIX_LAYER_TITLES = ("现象", "原因", "本质", "系统", "趋势", "机会")
SPEECH_MARKER = "如果我在面试或汇报中表达，我会这样说："


def _eight_question_key(question: str) -> str:
    return re.sub(r"[\s？?。.:：、]+", "", question)


def _parse_eight_questions(markdown: str) -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    current_field = ""

    def flush_current() -> None:
        nonlocal current
        if current:
            items.append(current)
        current = None

    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        question_match = re.match(r"^(\d+)[.、]\s*(.+?)\s*$", line)
        if question_match:
            flush_current()
            current = {
                "raw_number": question_match.group(1),
                "question": question_match.group(2).strip(),
                "fields": {},
            }
            current_field = ""
            continue
        field_match = re.match(rf"^({'|'.join(re.escape(field) for field in EIGHT_QUESTION_FIELDS)})[：:]\s*(.*)$", line)
        if field_match and current is not None:
            current_field = field_match.group(1)
            inline_value = field_match.group(2).strip()
            fields = current["fields"]  # type: ignore[index]
            fields.setdefault(current_field, "")  # type: ignore[attr-defined]
            if inline_value:
                existing = fields.get(current_field, "")  # type: ignore[attr-defined]
                fields[current_field] = f"{existing}\n{inline_value}".strip() if existing else inline_value  # type: ignore[index]
            continue
        if current is not None and current_field:
            fields = current["fields"]  # type: ignore[index]
            existing = fields.get(current_field, "")  # type: ignore[attr-defined]
            fields[current_field] = f"{existing}\n{line}".strip() if existing else line  # type: ignore[index]

    flush_current()
    return items


def _parse_labeled_segments(text: str, labels: tuple[str, ...]) -> list[tuple[str, str]]:
    pattern = re.compile("(" + "|".join(re.escape(label) for label in labels) + r")[：:]")
    matches = list(pattern.finditer(text))
    if len(matches) < 2:
        return []
    segments: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        value = text[start:end].strip()
        if value:
            segments.append((match.group(1), value))
    return segments


def _render_phase_sequence(text: str) -> str:
    segments = _parse_labeled_segments(text, PHASE_LABELS)
    if not segments:
        return ""
    items = []
    for label, value in segments:
        items.append(
            f"""
            <div class="{_semantic_classes(label, value, "phase-step")}">
              <dt>{_inline(label)}</dt>
              <dd>{_render_markdown_fragment(value)}</dd>
            </div>
            """
        )
    return f'<dl class="phase-sequence">{"".join(items)}</dl>'


def _render_reasoning_field(field: str, value: str) -> str:
    if field == "推导过程":
        phase_html = _render_phase_sequence(value)
        if phase_html:
            return phase_html
    return _render_markdown_fragment(value)


def _render_eight_question_workbench(markdown: str, case_anchor: str) -> str:
    items = _parse_eight_questions(markdown)
    if not items:
        return _render_markdown_fragment(markdown)

    route_items = []
    cards = []
    for index, item in enumerate(items, start=1):
        question = str(item.get("question", "")).strip()
        key = _eight_question_key(question)
        dimension = EIGHT_QUESTION_DIMENSIONS.get(key, "分析维度")
        anchor = f"{case_anchor}-eight-q{index}"
        route_items.append(
            f"""
            <a href="#{anchor}">
              <strong>{index:02d}</strong>
              <span>{_inline(question)}</span>
            </a>
            """
        )

        fields = item.get("fields", {})
        process_blocks = []
        for field in ("目的", "分析方法", "为什么用这个方法", "推导过程"):
            value = str(fields.get(field, "")).strip() if isinstance(fields, dict) else ""
            if not value:
                continue
            field_classes = _semantic_classes(field, value, "eight-question-field")
            process_blocks.append(
                f"""
                <div class="{field_classes}">
                  <dt>{_inline(field)}</dt>
                  <dd>{_render_reasoning_field(field, value)}</dd>
                </div>
                """
            )

        emphasis_blocks = []
        for field in ("阶段结论", "如何影响下一步"):
            value = str(fields.get(field, "")).strip() if isinstance(fields, dict) else ""
            if not value:
                continue
            field_classes = f'{_semantic_classes(field, value, "eight-question-field")} focus'
            emphasis_blocks.append(
                f"""
                <div class="{field_classes}">
                  <dt>{_inline(field)}</dt>
                  <dd>{_render_markdown_fragment(value)}</dd>
                </div>
                """
            )

        cards.append(
            f"""
            <article class="eight-question-card" id="{anchor}">
              <header class="eight-question-card-header">
                <span class="eight-question-number">{index:02d}</span>
                <div>
                  <h5>{_inline(question)}</h5>
                  <p>{_inline(dimension)}</p>
                </div>
              </header>
              <dl class="eight-question-fields">
                {"".join(process_blocks)}
              </dl>
              <dl class="eight-question-focus-grid">
                {"".join(emphasis_blocks)}
              </dl>
            </article>
            """
        )

    return f"""
    <section class="eight-question-workbench">
      <header class="eight-question-workbench-header">
        <span>8 问推理链</span>
        <h4>把一个 case 拆成 8 个连续判断</h4>
        <p>先拆对象、场景、成本、收益和矛盾，再看系统、趋势和价值流向。重点看每一步的阶段结论，以及它如何推动下一步推理。</p>
      </header>
      <nav class="eight-question-route" aria-label="8 问推理路线">
        {"".join(route_items)}
      </nav>
      <div class="eight-question-list">
        {"".join(cards)}
      </div>
    </section>
    """


def _render_six_layer_body(title: str, body: str) -> str:
    if title == "趋势":
        phase_html = _render_phase_sequence(body)
        if phase_html:
            prefix = re.split(r"(?:现在|阶段 1|阶段 2|长期形态)[：:]", body, maxsplit=1)[0].strip()
            prefix_html = _render_markdown_fragment(prefix) if prefix else ""
            return prefix_html + phase_html
    return _render_markdown_fragment(body)


def _render_six_layer_workbench(sections: list[tuple[str, str]], case_anchor: str) -> str:
    cards = []
    for index, (title, body) in enumerate(sections, start=1):
        cards.append(
            f"""
            <article class="{_semantic_classes(title, body, "six-layer-card")}" id="{case_anchor}-six-layer-{index}">
              <header>
                <span>{index:02d}</span>
                <h5>{_inline(title)}</h5>
              </header>
              <div class="six-layer-card-body">{_render_six_layer_body(title, body)}</div>
            </article>
            """
        )
    return f"""
    <section class="six-layer-workbench">
      <header class="six-layer-workbench-header">
        <span>六层判断链</span>
        <h4>现象、原因、本质、系统、趋势、机会</h4>
        <p>把推理结果压缩成可汇报的判断链：先说明看见了什么，再解释为什么发生，最后落到系统关系、趋势推演和机会判断。</p>
      </header>
      <div class="six-layer-grid">
        {"".join(cards)}
      </div>
    </section>
    """


def _render_six_layer_speech(markdown: str) -> str:
    text = markdown.replace(SPEECH_MARKER, "").strip().strip("“").strip("”")
    lines = [line.strip().strip("“").strip("”") for line in text.splitlines() if line.strip()]
    step_labels = ("第一", "第二", "第三", "第四", "第五", "第六")
    steps = []
    closing_lines = []
    for line in lines:
        if any(line.startswith(label + "，") for label in step_labels):
            match = re.match(r"^(第一|第二|第三|第四|第五|第六)，([^，]+)，(.+)$", line)
            if match:
                order, layer, content = match.groups()
                steps.append((order, layer, content.rstrip("。")))
            else:
                steps.append(("", "", line.rstrip("。")))
        else:
            closing_lines.append(line)

    step_html = []
    for index, (order, layer, content) in enumerate(steps, start=1):
        step_html.append(
            f"""
            <div class="{_semantic_classes(layer or order, content, "speech-step")}">
              <span>{index:02d}</span>
              <div>
                <strong>{_inline(layer or order or f"第 {index} 层")}</strong>
                <p>{_inline(content)}</p>
              </div>
            </div>
            """
        )
    closing_html = _render_markdown_fragment("\n".join(closing_lines)) if closing_lines else ""
    return f"""
    <section class="speech-module">
      <header class="speech-module-header">
        <span>六层表达</span>
        <h4>如果我在面试或汇报中表达，我会这样说</h4>
      </header>
      <div class="speech-step-list">
        {"".join(step_html)}
      </div>
      <div class="speech-closing semantic-item semantic-conclusion">
        {closing_html}
      </div>
    </section>
    """


def _split_bracket_sections(markdown: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    matches = list(re.finditer(r"^【([^】]+)】$", markdown, flags=re.M))
    if not matches:
        return [("完整内容", markdown)]
    if matches[0].start() > 0:
        prefix = markdown[: matches[0].start()].strip()
        if prefix:
            sections.append(("开篇", prefix))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        title = match.group(1).strip()
        body = markdown[match.end() : end].strip()
        sections.append((title, body))
    return sections


def _prepare_case_sections(markdown: str) -> list[tuple[str, str]]:
    prepared: list[tuple[str, str]] = []
    sections = _split_bracket_sections(markdown)
    pending_source = ""
    index = 0
    while index < len(sections):
        title, body = sections[index]
        if title == "信息来源":
            pending_source = body.strip()
            index += 1
            continue
        if title == "本次训练目标" and pending_source:
            body = f"{body.strip()}\n\n来源链接：\n{pending_source}"
            pending_source = ""
        if title == "P6+ 第一反应":
            correct = ""
            insufficient = ""
            if index + 1 < len(sections) and sections[index + 1][0] == "这个思路对在哪里":
                correct = sections[index + 1][1].strip()
                index += 1
            if index + 1 < len(sections) and sections[index + 1][0] == "这个思路为什么不够":
                insufficient = sections[index + 1][1].strip()
                index += 1
            body = body.strip()
            if correct:
                body += f"\n\n这个思路对在哪里：\n{correct}"
            if insufficient:
                body += f"\n\n这个思路为什么不够：\n{insufficient}"
        if title == "最大风险" and SPEECH_MARKER in body:
            risk_body, speech_body = body.split(SPEECH_MARKER, 1)
            if risk_body.strip():
                prepared.append((title, risk_body.strip()))
            prepared.append(("六层表达版本", f"{SPEECH_MARKER}\n{speech_body.strip()}"))
            index += 1
            continue
        prepared.append((title, body))
        index += 1
    if pending_source:
        prepared.append(("信息来源", pending_source))
    return prepared


def _section_kind(title: str) -> str:
    if "Fact" in title or "信息来源" in title or "背景" in title:
        return "evidence"
    if title in {"六层判断与表达", "六层表达版本"} or "表达" in title or "PREP" in title or "SCQA" in title or "被追问" in title:
        return "speak"
    if "分析方法" in title or "8 问" in title or "追问" in title or "系统关系" in title or "底层矛盾" in title or "反面论证" in title:
        return "reason"
    if "Asset" in title or "复盘" in title:
        return "asset"
    return "read"


def _section_label(title: str) -> str:
    mapping = {
        "Fact Confidence Table": "事实证据",
        "V3.1 分析方法工作台": "分析方法工作台",
        "P7+ 追问深答": "P7+ 追问深答",
        "8 问显性推理": "8 问推理",
        "分析方法总表": "分析方法总表",
        "P7+ 面试 / 汇报表达版本": "表达演练",
        "六层判断与表达": "六层判断链",
        "六层表达版本": "六层表达版本",
        "应该做什么": "建议推进什么",
        "不应该做什么": "暂不推进什么",
        "先验证什么": "优先验证什么",
        "Case Asset Card": "资产卡",
    }
    return mapping.get(title, title)


@dataclass(frozen=True)
class SectionGroup:
    anchor: str
    label: str
    title: str
    description: str
    auto_open: str = "first"


GROUP_BACKGROUND = SectionGroup(
    "context",
    "背景",
    "背景与事实",
    "先确认 case 是什么、事实从哪里来，以及 P6+ 第一反应为什么需要刹车。",
)
GROUP_REASON = SectionGroup(
    "reason",
    "推理",
    "推理工作台",
    "集中阅读分析方法、8 问、因果机制、系统关系、趋势和机会判断。",
)
GROUP_DECISION = SectionGroup(
    "decision",
    "判断",
    "取舍与验证",
    "把洞察落到推进方向、暂缓边界、优先验证项，以及风险和边界条件。",
)
GROUP_SPEAK = SectionGroup(
    "speak",
    "表达",
    "表达演练",
    "用于面试、汇报或讨论，直接练 PREP、SCQA 和被追问时的回答。",
    "all",
)
GROUP_ASSET = SectionGroup(
    "asset",
    "资产",
    "复盘与资产卡",
    "沉淀训练能力、可复用 Pattern、迁移方式和 Case Asset Card。",
    "first",
)


def _section_group(title: str) -> SectionGroup:
    if title in {"六层判断与表达", "六层表达版本", "PREP 表达版本", "SCQA 表达版本", "被追问时的回答"} or "表达" in title:
        return GROUP_SPEAK
    if title in {
        "Insight Quality Audit",
        "训练能力",
        "P6+ 易犯错误",
        "P7+ 正确思路",
        "可复用 Pattern",
        "迁移方式",
        "Case Asset Card",
    }:
        return GROUP_ASSET
    if title in {
        "核心判断",
        "应该做什么",
        "不应该做什么",
        "先验证什么",
        "关键假设",
        "验证指标",
        "最小可行方案",
        "长期机会",
        "最大风险",
    }:
        return GROUP_DECISION
    if title in SIX_LAYER_TITLES:
        return GROUP_SPEAK
    if _section_kind(title) == "reason" or title in {"V3.1 Insight 总览", "异常信号"}:
        return GROUP_REASON
    return GROUP_BACKGROUND


def _render_case_sections(case: CaseInfo) -> str:
    group_order = [GROUP_BACKGROUND, GROUP_REASON, GROUP_DECISION, GROUP_SPEAK, GROUP_ASSET]
    group_lines: dict[str, list[str]] = {group.anchor: [] for group in group_order}
    group_counts: dict[str, int] = {group.anchor: 0 for group in group_order}

    def append_section(title: str, body_html: str, kind: str, open_attr: str) -> None:
        group = _section_group(title)
        group_counts[group.anchor] = group_counts.get(group.anchor, 0) + 1
        detail_id = f"{case.anchor}-{group.anchor}-{group_counts[group.anchor]}"
        group_lines.setdefault(group.anchor, []).append(
            f'<details class="reader-section {kind}" data-mode="{kind}"{open_attr}>'
            f'<summary id="{detail_id}"><span>{_inline(_section_label(title))}</span><small>{_inline(kind)}</small></summary>'
            f'<div class="reader-section-body">{body_html}</div>'
            "</details>"
        )

    sections = _prepare_case_sections(case.content)
    index = 0
    while index < len(sections):
        title, body = sections[index]
        if title in {"Case", "类型"}:
            index += 1
            continue
        if title in SIX_LAYER_TITLES:
            six_sections: list[tuple[str, str]] = []
            while index < len(sections) and sections[index][0] in SIX_LAYER_TITLES:
                six_sections.append(sections[index])
                index += 1
            append_section(
                "六层判断与表达",
                _render_six_layer_workbench(six_sections, case.anchor),
                _section_kind("六层判断与表达"),
                " open",
            )
            continue
        kind = _section_kind(title)
        open_attr = "" if title == "Insight Quality Audit" else " open"
        if title == "8 问显性推理":
            body_html = _render_eight_question_workbench(body, case.anchor)
        elif title == "六层表达版本":
            body_html = _render_six_layer_speech(body)
        else:
            body_html = _render_markdown_fragment(body)
        append_section(title, body_html, kind, open_attr)
        index += 1

    output: list[str] = []
    for group in group_order:
        lines = group_lines.get(group.anchor, [])
        if not lines:
            continue
        output.append(
            f"""
            <section class="section-group {group.anchor}" id="{case.anchor}-{group.anchor}" data-auto-open="{group.auto_open}">
              <header class="section-group-header">
                <span class="section-group-label">{_inline(group.label)}</span>
                <div>
                  <h3>{_inline(group.title)}</h3>
                  <p>{_inline(group.description)}</p>
                </div>
                <span class="section-group-count">{len(lines)} 节</span>
              </header>
              <div class="section-group-body">
                {"".join(lines)}
              </div>
            </section>
            """
        )
    return "\n".join(output)


def _case_mode_strip(case: CaseInfo) -> str:
    items = (
        (f"{case.anchor}-insight", "总览", "核心 Insight"),
        (f"{case.anchor}-reason", "推理", "方法工作台"),
        (f"{case.anchor}-speak", "表达", "PREP / SCQA"),
        (f"{case.anchor}-asset", "资产", "复用卡片"),
    )
    return "\n".join(
        f'<a href="#{anchor}"><strong>{label}</strong><span>{sub}</span></a>' for anchor, label, sub in items
    )


def _render_source_badges(sources: list[SourceStatus]) -> str:
    if not sources:
        return '<span class="chip neutral">来源状态未记录</span>'
    badges = []
    for source in sources:
        ok = "ok" if source.status == "已使用" else "warn"
        badges.append(f'<span class="chip {ok}">{_inline(source.channel)} · {_inline(source.status)}</span>')
    return "\n".join(badges)


def _render_case_cards(cases: list[CaseInfo], selection_reasons: list[SelectionReason]) -> str:
    cards: list[str] = []
    reason_map = {reason.label.strip(): reason for reason in selection_reasons}
    for case in cases:
        reason = reason_map.get(case.label)
        reason_html = ""
        if reason:
            reason_html = f"""
              <div class="case-card-reason">
                <span>最终入选理由</span>
                <p>{_inline(reason.reason or "-")}</p>
                <p><strong>训练目标：</strong>{_inline(reason.training_goal or "-")}</p>
              </div>
            """
        cards.append(
            f"""
            <article class="case-card">
              <div class="case-card-top">
                <span>{_inline(case.label)}</span>
                <strong>{_inline(case.total_score or "-")}</strong>
              </div>
              <h3><a href="#{case.anchor}-insight">{_inline(case.title)}</a></h3>
              <p class="case-card-insight">{_inline(case.insight or case.judgment or "Insight 待抽取")}</p>
              <p class="case-card-weak">扣分点：{_inline(case.weak_point or "暂无明显扣分")}</p>
              {reason_html}
              <div class="case-card-actions">
                <a href="#{case.anchor}-insight">进入阅读</a>
                <a href="#{case.anchor}-speak">表达演练</a>
                <a href="#{case.anchor}-asset">资产卡片</a>
              </div>
            </article>
            """
        )
    return "\n".join(cards)


SCORE_DIMENSION_LABELS = {
    "relevance": "相关性",
    "signal_strength": "信号强度",
    "training_value": "训练价值",
    "verifiability": "可验证性",
    "asset_value": "资产化价值",
}


SCORE_DESCRIPTIONS = {
    "相关性": {
        "5": "高度贴合当天 P7+ 训练目标，能直接服务判断力、表达力或职业壁垒。",
        "4": "与训练目标相关，但不是当天最核心的训练主线。",
        "3": "有观察价值，但需要更强连接才能进入深度分析。",
    },
    "信号强度": {
        "5": "来自官方、AI HOT 精选、行业讨论或开发者社区的强信号叠加。",
        "4": "信号明确，但传播、采用或后续影响还需要继续观察。",
        "3": "已有苗头，但不足以独立支撑深度判断。",
    },
    "训练价值": {
        "5": "能训练关键 P7+ 能力，例如本质抽象、系统判断、机会取舍或反面论证。",
        "4": "能训练某个重要子能力，但洞察迁移面稍窄。",
        "3": "适合轻量观察，不足以撑起完整深度 case。",
    },
    "可验证性": {
        "5": "有官方公告、论文、GitHub、产品页或一手资料支撑。",
        "4": "核心事实可验证，但部分数据、采用或影响仍需后续补证。",
        "3": "有公开线索，但事实链还不够稳。",
        "2": "主要来自信号源或二手摘要，只能进入 Watchlist。",
    },
    "资产化价值": {
        "5": "可直接沉淀为面试素材、项目方法论或长期复用 Pattern。",
        "4": "有资产潜力，但需要补事实、补数据或补后续案例。",
        "3": "更适合作为观察记录，暂不作为关键判断资产。",
    },
}


def _score_description(dimension: str, value: str) -> str:
    return SCORE_DESCRIPTIONS.get(dimension, {}).get(value, "需要结合今日训练目标和事实链进一步解释。")


def _case_type_explanation(case_type: str) -> str:
    if "Case A" in case_type:
        return "Case A 代表外部变化类训练，重点看行业、基础设施或竞争格局变化如何影响产品判断。"
    if "Case B" in case_type:
        return "Case B 代表产品 / 商业趋势类训练，重点看产品机制、商业化入口和企业采用逻辑。"
    if "Case C" in case_type:
        return "Case C 代表个人壁垒类训练，重点看方法论、表达能力和可迁移判断力。"
    return "这是候选池中的观察方向，是否进入深度分析取决于事实强度、训练价值和当天三案平衡。"


def _handling_class(handling: str) -> str:
    if "深度" in handling:
        return "deep"
    if "雷达" in handling:
        return "radar"
    if "Watchlist" in handling:
        return "watchlist"
    return "observe"


def _ensure_sentence(text: str) -> str:
    text = text.strip()
    if not text:
        return ""
    if text.endswith(("。", ".", "！", "？", "!", "?")):
        return text
    return text + "。"


def _score_band(total: str) -> str:
    try:
        value = int(re.match(r"\d+", total or "").group(0))  # type: ignore[union-attr]
    except AttributeError:
        return "评分规则待核验"
    if value >= 21:
        return "21-25：深度分析候选分段"
    if value >= 17:
        return "17-20：雷达简报 / Watchlist 分段"
    if value >= 13:
        return "13-16：轻量观察分段"
    return "12 以下：暂不处理分段"


def _score_decision_hint(candidate: CandidateInfo) -> str:
    handling = candidate.handling or "待判断"
    band = _score_band(candidate.total)
    if "深度" in handling:
        return f"{band}，今天进入深度 case。"
    if "雷达" in handling:
        return f"{band}，今天先作为雷达信号跟踪。"
    if "Watchlist" in handling:
        return f"{band}，有价值但仍需后续验证。"
    return f"{band}，处理方式为 {handling}。"


def _render_source_links(raw_links: str) -> str:
    if not raw_links:
        return ""
    links: list[str] = []
    pattern = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
    for match in pattern.finditer(raw_links):
        label = html.escape(match.group(1), quote=False)
        url = html.escape(match.group(2), quote=True)
        links.append(f'<a class="source-link" href="{url}" target="_blank" rel="noopener noreferrer">打开原文：{label}</a>')
    if not links:
        for url in re.findall(r"https?://[^\s，。、)]+", raw_links):
            escaped_url = html.escape(url, quote=True)
            label = html.escape(re.sub(r"^https?://", "", url).split("/")[0], quote=False)
            links.append(f'<a class="source-link" href="{escaped_url}" target="_blank" rel="noopener noreferrer">打开原文：{label}</a>')
    if not links:
        return f'<span class="source-text">{_inline(raw_links)}</span>'
    return "\n".join(links)


def _candidate_context_items(candidate: CandidateInfo) -> list[tuple[str, str]]:
    items: list[tuple[str, str]] = []
    description = candidate.description.strip()
    if description and "待补充" not in description:
        items.append(("发生了什么", _ensure_sentence(candidate.description)))
    if candidate.radar_value and candidate.radar_value not in candidate.score_reason:
        items.append(("为什么值得看", _ensure_sentence(candidate.radar_value)))
    if candidate.next_action:
        items.append(("后续关注", _ensure_sentence(candidate.next_action)))
    if not items and candidate.score_reason:
        items.append(("判断意义", _ensure_sentence(candidate.score_reason)))
    if not items and candidate.source:
        items.append(("当前信号", f"来自{_ensure_sentence(candidate.source)}"))
    return items or [("判断提示", "需要结合原文来源、评分拆解和后续信号继续判断。")]


def _render_context_items(items: list[tuple[str, str]], class_name: str = "context-list") -> str:
    rows = []
    for label, text in items:
        rows.append(
            f"""
            <div class="{_semantic_classes(label, text, "context-item")}">
              <dt>{_inline(label)}</dt>
              <dd>{_inline(text)}</dd>
            </div>
            """
        )
    return f'<dl class="{class_name}">{"".join(rows)}</dl>'


def _render_score_breakdown(candidate: CandidateInfo) -> str:
    rows = []
    values = {
        "relevance": candidate.relevance,
        "signal_strength": candidate.signal_strength,
        "training_value": candidate.training_value,
        "verifiability": candidate.verifiability,
        "asset_value": candidate.asset_value,
    }
    for key, value in values.items():
        label = SCORE_DIMENSION_LABELS[key]
        rows.append(
            f"""
            <div class="score-row">
              <span>{_inline(label)}</span>
              <strong>{_inline(value)}</strong>
              <p>{_inline(_score_description(label, value))}</p>
            </div>
            """
        )
    return "\n".join(rows)


def _render_candidate_overview(markdown: str, cases: list[CaseInfo]) -> str:
    candidates = _parse_candidate_infos(markdown)
    radar_infos = _parse_radar_infos(markdown)

    if not candidates and not radar_infos:
        return ""

    candidate_cards = []
    for index, candidate in enumerate(candidates, start=1):
        handling_class = _handling_class(candidate.handling)
        score_reason = _ensure_sentence(candidate.score_reason or "分项评分需要结合事实链、训练价值和资产化潜力理解")
        score_hint = _score_decision_hint(candidate)
        candidate_cards.append(
            f"""
            <article class="candidate-item {handling_class}">
              <div class="candidate-score-panel">
                <div class="score-heading">
                  <span class="score-label">选择评分</span>
                  <button type="button" class="score-help" data-toast="{html.escape(score_hint, quote=True)}">规则</button>
                </div>
                <div class="candidate-score">
                  <strong>{_inline(candidate.total or "-")}</strong>
                  <span>/25</span>
                </div>
                <p class="score-reason"><strong>为什么是 {_inline(candidate.total or "-")} 分：</strong>{_inline(score_reason)}</p>
              </div>
              <div class="candidate-main">
                <div class="candidate-meta">
                  <span><b>处理</b>{_inline(candidate.handling or "待判断")}</span>
                  <span><b>事实等级</b>{ _inline(candidate.fact_grade or "-") }</span>
                  <span><b>排序</b>#{index}</span>
                </div>
                <h3>{_inline(candidate.title)}</h3>
                {_render_context_items(_candidate_context_items(candidate), "context-list candidate-context-list")}
                <div class="candidate-links">
                  <span>溯源链接</span>
                  {_render_source_links(candidate.links or candidate.source)}
                </div>
                <details class="candidate-breakdown">
                  <summary><span>展开评分拆解、训练角色和来源</span></summary>
                  <p><strong>训练角色：</strong>{_inline(_case_type_explanation(candidate.case_type))}</p>
                  <p><strong>原始类型：</strong>{_inline(candidate.case_type)}</p>
                  <p><strong>来源：</strong>{_inline(candidate.source)}</p>
                  <div class="score-breakdown">
                    {_render_score_breakdown(candidate)}
                  </div>
                </details>
              </div>
            </article>
            """
        )

    radar_cards = []
    for candidate in candidates:
        if "深度" in candidate.handling:
            continue
        radar_cards.append(
            f"""
            <article class="radar-card">
              <div>
                <span>{_inline(candidate.handling or "Watchlist")}</span>
                <strong>{_inline(candidate.total or "-")}/25</strong>
              </div>
              <h3>{_inline(candidate.title)}</h3>
              {_render_context_items(_candidate_context_items(candidate), "context-list radar-context-list")}
              <div class="radar-link-row">{_render_source_links(candidate.links or candidate.source)}</div>
            </article>
            """
        )
    for info in radar_infos:
        if any(_similarity(info.get("title", ""), candidate.title) >= 0.45 for candidate in candidates):
            continue
        context_items = [
            (label, text)
            for label, text in (
                ("发生了什么", _ensure_sentence(info.get("conclusion", ""))) if info.get("conclusion") else ("", ""),
                ("为什么值得看", _ensure_sentence(info.get("value", ""))) if info.get("value") else ("", ""),
                ("后续关注", _ensure_sentence(info.get("action", ""))) if info.get("action") else ("", ""),
            )
            if label and text
        ]
        radar_cards.append(
            f"""
            <article class="radar-card">
              <div>
                <span>{_inline(info.get("type", "") or "雷达")}</span>
                <strong>雷达</strong>
              </div>
              <h3>{_inline(info.get("title", ""))}</h3>
              {_render_context_items(context_items or [("判断提示", "需要结合原文来源和后续信号继续观察。")], "context-list radar-context-list")}
              <div class="radar-link-row">{_render_source_links(info.get("link", ""))}</div>
            </article>
            """
        )

    radar_panel = ""
    if radar_cards:
        radar_panel = f"""
        <section class="radar-panel" id="radar">
          <header class="content-block-header compact">
            <span>雷达重点</span>
            <h2>今天值得继续跟踪的信号</h2>
            <p>这些没有进入 3 个深度 case，但对后续趋势判断、开源观察和产品机会仍然重要。</p>
          </header>
          <div class="radar-grid">
            {"".join(radar_cards)}
          </div>
        </section>
        """

    return f"""
    <section class="candidate-overview">
      <header class="content-block-header">
        <span>今日判断</span>
        <h2>先看雷达，再看候选选择</h2>
        <p>雷达信号帮助你建立今天的行业感，候选池负责解释每个 case 为什么深挖、暂缓或继续观察。</p>
      </header>
      {radar_panel}
      <section class="candidate-pool-panel" id="candidates">
        <header class="content-block-header compact">
          <span>候选池</span>
          <h2>今日候选 case 与选择判断</h2>
          <p>这里把快速认知、选择评分、分数原因和溯源链接合在同一张卡里。分项评分和训练角色默认折叠，需要复核时再展开。</p>
        </header>
      <div class="candidate-list">
        {"".join(candidate_cards)}
      </div>
      </section>
    </section>
    """


def _render_reference_panel(markdown: str) -> str:
    source_section = _extract_heading_section(markdown, "## 零、来源通道使用情况")
    threshold_section = _extract_heading_section(markdown, "### Case Selection Score 阈值说明")
    reference_blocks = []
    if source_section:
        reference_blocks.append(
            f"""
            <details class="reference-disclosure" id="source-evidence">
              <summary>来源佐证</summary>
              <div>{_render_markdown_fragment(source_section)}</div>
            </details>
            """
        )
    if threshold_section:
        reference_blocks.append(
            f"""
            <details class="reference-disclosure" id="scoring-rule">
              <summary>Case Selection Score 阈值规则</summary>
              <div>{_render_markdown_fragment(threshold_section)}</div>
            </details>
            """
        )
    if not reference_blocks:
        return ""
    return f"""
    <section class="reference-panel" id="references">
      <header class="content-block-header compact">
        <span>证据层附录</span>
        <h2>需要复核时再看</h2>
      </header>
      {"".join(reference_blocks)}
    </section>
    """


def _render_action_grid(case: CaseInfo) -> str:
    items = (
        ("建议推进", case.do),
        ("暂不推进", case.dont),
        ("优先验证", case.validate),
        ("主要风险", case.weak_point),
    )
    return "\n".join(
        f'<div class="{_semantic_classes(label, value or "", "action-cell")}"><span>{label}</span><p>{_inline(value or "-")}</p></div>'
        for label, value in items
    )


def _render_case(case: CaseInfo) -> str:
    return f"""
    <article class="case-article" id="{case.anchor}">
      <header class="case-header">
        <div class="case-kicker">{_inline(case.label)} · 深度阅读</div>
        <h2>{_inline(case.title)}</h2>
        <div class="meta-row">
          <span>总分 { _inline(case.total_score or "-") }</span>
          <span>思考 { _inline(case.thinking_score or "-") }</span>
          <span>内容 { _inline(case.content_score or "-") }</span>
          <span>表达 { _inline(case.expression_score or "-") }</span>
          <span>资产 { _inline(case.asset_grade or "-") }</span>
        </div>
      </header>

      <section class="insight-callout semantic-item semantic-insight" id="{case.anchor}-insight">
        <span class="section-eyebrow">核心 Insight</span>
        <p>{_inline(case.insight or case.judgment or "暂未抽取到一句话 Insight。")}</p>
      </section>

      <section class="judgment-block semantic-item semantic-conclusion">
        <h3>结论先行</h3>
        <p>{_inline(case.judgment or "暂未抽取到核心判断。")}</p>
        <div class="action-grid">{_render_action_grid(case)}</div>
      </section>

      <nav class="mode-strip" aria-label="{html.escape(case.title)} 阅读模式">
        {_case_mode_strip(case)}
      </nav>

      <div class="section-stack">
        {_render_case_sections(case)}
      </div>
    </article>
    """


def _render_nav(cases: list[CaseInfo]) -> str:
    case_links = "\n".join(
        f'<a class="toc-case" href="#{case.anchor}"><span>{_inline(case.label)}</span><em>{_inline(case.title)}</em></a>'
        for case in cases
    )
    return f"""
    <nav class="reader-toc" aria-label="阅读目录">
      <strong>阅读目录</strong>
      <div class="nav-group">
        <span class="nav-group-title">今日</span>
        <a href="#guide">今日导读</a>
        <a href="#radar">雷达重点</a>
        <a href="#candidates">候选与选择</a>
      </div>
      <div class="nav-group">
        <span class="nav-group-title">深度 Case</span>
        {case_links}
      </div>
      <div class="nav-group">
        <span class="nav-group-title">练习</span>
        <a href="#review">练习与复盘</a>
        <a href="#references">证据层</a>
      </div>
    </nav>
    """


def _render_mobile_toc(cases: list[CaseInfo]) -> str:
    case_links = "\n".join(
        f'<a class="toc-case-mobile" href="#{case.anchor}"><span>{_inline(case.label)}</span><em>{_inline(case.title)}</em></a>'
        for case in cases
    )
    return f"""
    <div class="mobile-toc-panel">
      <details>
        <summary>阅读目录</summary>
        <nav class="mobile-toc-links" aria-label="移动端阅读目录">
          <a href="#guide">今日导读</a>
          <a href="#radar">雷达重点</a>
          <a href="#candidates">候选与选择</a>
          {case_links}
          <a href="#review">练习与复盘</a>
          <a href="#references">证据层</a>
        </nav>
      </details>
    </div>
    """


def _render_mobile_bottom_nav(cases: list[CaseInfo]) -> str:
    links = ['<a href="#guide">总览</a>']
    for case in cases[:3]:
        label = case.label.replace("Case ", "")
        links.append(f'<a href="#{case.anchor}">{_inline(label)}</a>')
    while len(links) < 4:
        links.append('<a href="#review">复盘</a>')
    return f"""
  <nav class="mobile-bottom-nav" aria-label="移动端快速跳转">
    {"".join(links[:4])}
  </nav>
    """


def _styles() -> str:
    return """
    :root {
      --bg: #eef2f5;
      --paper: #fffefa;
      --surface: #ffffff;
      --surface-muted: #edf1f5;
      --ink: #101827;
      --muted: #5f6a7d;
      --line: #d2d9e3;
      --blue: #2458c8;
      --blue-soft: #e9f0ff;
      --teal: #0f756b;
      --teal-soft: #e4f4f1;
      --amber: #9b640f;
      --amber-soft: #fff4d9;
      --red: #a93328;
      --shadow: 0 24px 80px rgba(28, 39, 58, 0.09);
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: auto; overflow-x: hidden; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font: 16px/1.82 -apple-system, BlinkMacSystemFont, "SF Pro Text", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Segoe UI", sans-serif;
      letter-spacing: 0;
      text-rendering: optimizeLegibility;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
    }
    a { color: var(--blue); text-decoration-thickness: 1px; text-underline-offset: 3px; }
    code { background: var(--surface-muted); border: 1px solid var(--line); border-radius: 5px; padding: 1px 5px; font-size: .92em; }
    .progress {
      position: fixed; left: 0; top: 0; z-index: 50; height: 3px; width: 100%;
      background: linear-gradient(90deg, var(--blue), var(--teal));
      transform: none; transform-origin: left center;
    }
    @supports (animation-timeline: scroll()) {
      @media (prefers-reduced-motion: no-preference) {
        .progress {
          transform: scaleX(0);
          animation: reader-progress linear both;
          animation-timeline: scroll(root);
        }
      }
    }
    @keyframes reader-progress {
      from { transform: scaleX(0); }
      to { transform: scaleX(1); }
    }
    .topbar {
      position: sticky; top: 0; z-index: 40;
      backdrop-filter: blur(14px);
      background: rgba(244,246,248,.92);
      border-bottom: 1px solid rgba(217,222,229,.86);
    }
    .topbar-inner {
      max-width: 1480px; margin: 0 auto; padding: 14px 28px;
      display: flex; align-items: center; justify-content: space-between; gap: 18px;
    }
    .brand { min-width: 0; }
    .brand strong { display: block; font-size: 15px; line-height: 1.2; }
    .brand span { display: block; color: var(--muted); font-size: 13px; margin-top: 3px; }
    .source-chips { display: flex; flex-wrap: wrap; gap: 8px; justify-content: flex-end; }
    .chip {
      display: inline-flex; align-items: center; min-height: 28px;
      padding: 4px 9px; border-radius: 999px; border: 1px solid var(--line);
      background: var(--surface); color: var(--muted); font-size: 12px; white-space: nowrap;
      font-variant-numeric: tabular-nums;
    }
    .chip.ok { color: var(--teal); background: var(--teal-soft); border-color: #b7ddd6; }
    .chip.warn { color: var(--amber); background: var(--amber-soft); border-color: #efd39a; }
    .chip.neutral { color: var(--muted); }
    .mobile-toc-panel { display: none; }
    .layout {
      display: grid; grid-template-columns: 260px minmax(0, 1040px);
      gap: 56px; max-width: 1480px; margin: 0 auto; padding: 28px 28px 104px;
    }
    .reader-toc {
      position: sticky; top: 78px; align-self: start; max-height: calc(100vh - 96px); overflow: auto;
      padding: 10px 8px 20px; font-size: 13px;
    }
    .reader-toc strong { display: block; color: #27354f; margin: 0 0 12px; font-size: 13px; font-weight: 800; }
    .nav-group { margin: 0 0 14px; }
    .nav-group-title {
      display: block; color: var(--muted); font-size: 11px; font-weight: 700;
      margin: 10px 0 5px; letter-spacing: 0;
    }
    .reader-toc a {
      display: flex; align-items: center; min-height: 38px;
      padding: 8px 10px; border: 1px solid transparent;
      color: #4c566b; text-decoration: none; border-radius: 8px;
      line-height: 1.45; margin: 2px 0;
    }
    .reader-toc a:hover {
      background: rgba(36,88,200,.07); color: var(--blue); border-color: #c9d7f3;
    }
    .reader-toc a:active,
    .mobile-toc-links a:active,
    .mode-strip a:active,
    .case-card-actions a:active,
    .candidate-links a:active,
    .case-card:active {
      transform: translateY(1px);
    }
    .reader-toc a:focus-visible,
    .mobile-toc-links a:focus-visible,
    .mobile-bottom-nav a:focus-visible,
    .case-card-actions a:focus-visible,
    .candidate-links a:focus-visible,
    .mode-strip a:focus-visible {
      outline: 2px solid rgba(36,88,200,.45);
      outline-offset: 2px;
    }
    .reader-toc a[aria-current="true"] {
      background: var(--blue-soft); color: #173f9a; border-color: #adc1ef; font-weight: 700;
    }
    .toc-case {
      display: grid !important; grid-template-columns: 52px minmax(0, 1fr); gap: 8px; align-items: start !important;
      min-height: 48px !important;
    }
    .toc-case span {
      color: var(--blue); font-size: 12px; font-weight: 800; white-space: nowrap;
    }
    .toc-case em {
      font-style: normal; color: inherit; font-size: 12.5px;
    }
    main.reader {
      min-width: 0; background: var(--paper); border: 1px solid rgba(217,222,229,.9);
      border-radius: 12px; box-shadow: var(--shadow);
    }
    .reader-inner { max-width: 940px; margin: 0 auto; padding: 50px 58px 88px; }
    .reader-hero { margin-bottom: 34px; }
    .reader-hero .eyebrow, .section-eyebrow {
      display: inline-flex; margin-bottom: 12px; color: var(--blue); font-size: 13px; font-weight: 700;
    }
    h1, h2, h3, h4 { letter-spacing: 0; line-height: 1.32; color: #141c2f; }
    h1 { margin: 0 0 16px; font-size: 31px; }
    h2 {
      margin: 56px 0 18px; font-size: 26px;
      padding-bottom: 12px; border-bottom: 1px solid var(--line);
    }
    h3 {
      margin: 34px 0 14px; font-size: 19px;
      padding-left: 12px; border-left: 3px solid var(--blue);
    }
    h4 {
      margin: 26px 0 10px; font-size: 16px; color: #26344e;
      padding: 7px 10px; background: #f5f2eb; border-radius: 6px;
    }
    p { margin: 13px 0; color: #26344e; }
    ul, ol { margin: 10px 0 16px 22px; padding: 0; }
    li { margin: 5px 0; }
    .guide-card {
      border: 1px solid var(--line); border-radius: 10px; background: #fff9ed;
      padding: 20px; margin: 22px 0 26px;
    }
    .guide-card h2 { margin: 0 0 10px; font-size: 22px; }
    .guide-path {
      display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px;
    }
    .guide-path span {
      border: 1px solid #ead8ad; background: #fff; border-radius: 999px; padding: 5px 10px; color: #705213; font-size: 13px;
    }
    .case-card-list {
      display: grid; grid-template-columns: 1fr; gap: 12px; margin: 20px 0 8px;
    }
    .case-card {
      display: grid; grid-template-columns: 78px minmax(0, 1fr); column-gap: 18px; align-items: start;
      color: var(--ink);
      border: 1px solid #cbd5e2; background: var(--surface); border-radius: 10px;
      padding: 18px 20px; min-height: 0; transition: border-color .18s ease, transform .18s ease, box-shadow .18s ease;
    }
    .case-card:hover { border-color: #9eb4df; transform: translateY(-1px); box-shadow: 0 14px 34px rgba(36,88,200,.10); }
    .case-card-top {
      display: flex; flex-direction: column; gap: 5px; color: var(--muted); font-size: 12px;
      font-variant-numeric: tabular-nums;
    }
    .case-card-top strong { color: var(--teal); font-size: 13px; }
    .case-card h3 { grid-column: 2; margin: 0 0 6px; font-size: 17px; line-height: 1.38; }
    .case-card h3 a { color: var(--ink); text-decoration: none; }
    .case-card h3 a:hover { color: var(--blue); text-decoration: underline; text-decoration-thickness: 1px; }
    .case-card-insight { grid-column: 2; color: var(--ink); font-size: 14px; line-height: 1.62; margin: 0 0 5px; }
    .case-card-weak { grid-column: 2; color: var(--muted); font-size: 12px; line-height: 1.5; margin: 0; }
    .case-card-reason {
      grid-column: 2; margin-top: 10px; padding: 10px 12px;
      border-left: 3px solid #9eb4df; background: #f7f9ff; border-radius: 0 8px 8px 0;
    }
    .case-card-reason span {
      display: inline-flex; color: var(--blue); font-size: 12px; font-weight: 800; margin-bottom: 4px;
    }
    .case-card-reason p { margin: 3px 0; font-size: 13px; line-height: 1.58; color: #26344e; }
    .case-card-actions {
      grid-column: 2; align-self: start; margin-top: 12px;
      display: flex; gap: 8px; flex-wrap: wrap; justify-content: flex-start;
    }
    .case-card-actions a {
      display: inline-flex; align-items: center; justify-content: center;
      min-height: 34px; padding: 6px 12px; border-radius: 8px;
      color: #173f9a; background: #ffffff; border: 1px solid #adc1ef;
      font-size: 12px; font-weight: 760;
      text-decoration: none; transition: background .16s ease, border-color .16s ease, transform .16s ease;
    }
    .case-card-actions a:hover { background: var(--blue-soft); border-color: #7f9edb; }
    .details-note {
      border-top: 1px solid var(--line); border-bottom: 1px solid var(--line);
      padding: 13px 0; color: var(--muted); font-size: 14px; margin: 24px 0;
    }
    .content-block-header {
      margin: 54px 0 18px; padding-top: 22px; border-top: 1px solid #d5dce5;
    }
    .content-block-header.compact { margin-top: 40px; }
    .content-block-header span {
      display: inline-flex; color: var(--blue); background: var(--blue-soft);
      padding: 4px 9px; border-radius: 7px; font-size: 13px; font-weight: 800;
      margin-bottom: 10px;
    }
    .content-block-header h2 {
      margin: 0 0 8px; padding: 0; border: 0; font-size: 24px;
    }
    .content-block-header p {
      margin: 0; color: var(--muted); max-width: 66ch; font-size: 14px; line-height: 1.7;
    }
    .candidate-list { display: grid; gap: 14px; }
    .candidate-item {
      display: grid; grid-template-columns: minmax(180px, 230px) minmax(0, 1fr); gap: 18px;
      border: 1px solid #c8d4e2; border-radius: 12px; background: #fff;
      padding: 18px; scroll-margin-top: 96px;
    }
    .candidate-item.deep { border-color: #99b4e4; background: linear-gradient(180deg, #f7faff, #fff); }
    .candidate-score-panel {
      border: 1px solid #d8e1ed; border-radius: 10px; background: #f8fafc;
      padding: 14px; min-width: 0;
    }
    .score-heading {
      display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-bottom: 6px;
    }
    .score-label {
      display: block; color: var(--muted); font-size: 12px; font-weight: 760;
    }
    .score-help {
      display: inline-flex; align-items: center; justify-content: center;
      min-height: 24px; padding: 2px 7px; border-radius: 999px;
      border: 1px solid #c7d5ef; background: #fff; color: var(--blue);
      font: inherit; font-size: 11px; font-weight: 760; cursor: pointer;
    }
    .score-help:hover { background: var(--blue-soft); }
    .score-help:focus-visible {
      outline: 2px solid rgba(36,88,200,.45); outline-offset: 2px;
    }
    .candidate-score {
      display: flex; align-items: baseline; gap: 4px;
      color: var(--teal); font-variant-numeric: tabular-nums;
    }
    .candidate-score strong { font-size: 34px; line-height: 1; letter-spacing: 0; }
    .candidate-score span { color: var(--muted); font-size: 13px; margin-top: 3px; }
    .candidate-score-panel p {
      margin: 8px 0 0; color: #3a465a; font-size: 13px; line-height: 1.55;
    }
    .candidate-score-panel .score-reason {
      margin-top: 10px; padding-top: 10px; border-top: 1px solid #dde5ee;
    }
    .candidate-score-panel .score-reason strong { color: #172033; }
    .candidate-main { min-width: 0; }
    .candidate-meta { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 10px; }
    .candidate-meta span {
      display: inline-flex; align-items: center; gap: 6px; min-height: 26px; padding: 3px 8px;
      border: 1px solid var(--line); border-radius: 7px; color: #3e4a5e;
      background: #fff; font-size: 12px; line-height: 1.2;
    }
    .candidate-meta b {
      color: var(--muted); font-weight: 650;
    }
    .candidate-item.deep .candidate-meta span:first-child {
      color: var(--blue); background: var(--blue-soft); border-color: #b9c8eb; font-weight: 700;
    }
    .candidate-item.radar .candidate-meta span:first-child,
    .candidate-item.watchlist .candidate-meta span:first-child {
      color: var(--amber); background: var(--amber-soft); border-color: #efd39a; font-weight: 700;
    }
    .candidate-main h3 {
      margin: 0 0 9px; padding: 0; border-left: 0; font-size: 20px; line-height: 1.35;
    }
    .candidate-main p { margin: 8px 0; font-size: 14.5px; line-height: 1.68; }
    .context-list {
      margin: 10px 0 12px; display: grid; gap: 8px;
    }
    .context-list div {
      display: grid; grid-template-columns: 86px minmax(0, 1fr); gap: 10px; align-items: start;
    }
    .context-list dt {
      margin: 0; color: var(--blue); font-size: 12px; font-weight: 820;
      white-space: nowrap;
    }
    .context-list dd {
      margin: 0; color: #26344e; font-size: 14px; line-height: 1.62;
    }
    .candidate-context-list {
      background: #f7f9fb; border-left: 3px solid #9eb4df;
      padding: 11px 13px; border-radius: 0 8px 8px 0;
    }
    .candidate-links {
      display: flex; flex-wrap: wrap; align-items: center; gap: 8px; margin: 12px 0 8px; font-size: 13px;
    }
    .candidate-links > span {
      color: var(--muted); font-size: 12px; font-weight: 760;
    }
    .source-link {
      display: inline-flex; align-items: baseline; gap: 0;
      color: var(--blue); background: transparent; border: 0; padding: 0;
      border-radius: 0; text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 4px;
      font-weight: 720; white-space: nowrap;
    }
    .source-text { color: var(--muted); }
    .radar-link-row { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px; }
    .candidate-breakdown {
      margin-top: 12px; border-top: 1px solid #e4e9ef; padding-top: 12px;
    }
    .candidate-breakdown summary {
      cursor: pointer; list-style: none; color: var(--blue); font-size: 13px; font-weight: 760;
      display: inline-flex; align-items: center; min-height: 34px; padding: 5px 10px;
      border: 1px solid #b9c8eb; border-radius: 8px; background: #fff;
    }
    .candidate-breakdown summary::-webkit-details-marker { display: none; }
    .candidate-breakdown summary::before {
      content: "+";
      display: inline-flex; align-items: center; justify-content: center;
      width: 16px; height: 16px; margin-right: 7px; border-radius: 4px;
      background: var(--blue-soft); color: var(--blue);
    }
    .candidate-breakdown[open] summary::before { content: "-"; }
    .candidate-breakdown summary:hover { background: var(--blue-soft); }
    .score-breakdown {
      display: grid; gap: 8px; margin-top: 12px;
    }
    .score-row {
      display: grid; grid-template-columns: 74px 28px minmax(0, 1fr); gap: 10px;
      align-items: start; border: 1px solid #e4e9ef; border-radius: 8px; padding: 9px 10px;
      background: #fffdf9;
    }
    .score-row span { color: var(--muted); font-size: 13px; }
    .score-row strong { color: var(--ink); font-variant-numeric: tabular-nums; }
    .score-row p { margin: 0; font-size: 13px; line-height: 1.55; }
    .selection-grid { display: grid; grid-template-columns: 1fr; gap: 10px; }
    .selection-card {
      border: 1px solid var(--line); border-radius: 10px; padding: 16px 18px; background: #fffaf0;
    }
    .selection-card > span { color: var(--blue); font-size: 13px; font-weight: 800; }
    .selection-card h3 {
      margin: 6px 0 8px; padding: 0; border-left: 0; font-size: 18px;
    }
    .selection-card h4 {
      margin: 14px 0 5px; padding: 0; background: none; color: var(--muted); font-size: 13px;
    }
    .selection-card p { margin: 0; font-size: 14.5px; line-height: 1.68; }
    .radar-grid {
      display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px;
    }
    .radar-card {
      border: 1px solid #d6dde8; border-radius: 10px; background: #fff; padding: 15px 16px;
    }
    .radar-card > div:first-child {
      display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-bottom: 8px;
    }
    .radar-card span {
      color: var(--amber); background: var(--amber-soft); border: 1px solid #efd39a;
      border-radius: 7px; padding: 3px 7px; font-size: 12px; font-weight: 760;
    }
    .radar-card strong {
      color: var(--teal); font-size: 13px; font-variant-numeric: tabular-nums;
    }
    .radar-card h3 {
      margin: 0 0 8px; padding: 0; border-left: 0; font-size: 17px; line-height: 1.35;
    }
    .radar-context-list { margin: 8px 0 12px; }
    .radar-context-list div { grid-template-columns: 82px minmax(0, 1fr); }
    .radar-context-list dd { font-size: 13.5px; }
    .candidate-pool-panel .content-block-header,
    .radar-panel .content-block-header {
      padding-top: 18px;
    }
    .candidate-pool-panel,
    .radar-panel {
      scroll-margin-top: 96px;
    }
    .reference-panel { margin-bottom: 34px; }
    .reference-disclosure {
      border: 1px solid var(--line); border-radius: 10px; background: #fff;
      margin: 10px 0; overflow: hidden;
    }
    .reference-disclosure summary {
      cursor: pointer; min-height: 48px; padding: 12px 16px;
      display: flex; align-items: center; font-weight: 760; color: #26344e;
      background: #f7f9fb;
    }
    .reference-disclosure > div { padding: 0 16px 16px; }
    .case-article {
      margin: 62px 0 28px; padding-top: 20px;
      border-top: 2px solid #d4dbe5;
      scroll-margin-top: 82px;
    }
    .section-group,
    .insight-callout {
      scroll-margin-top: 96px;
    }
    .case-kicker { color: var(--blue); font-size: 13px; font-weight: 700; margin-bottom: 8px; }
    .case-header h2 { margin-top: 0; }
    .case-header {
      padding: 0 0 8px;
    }
    .meta-row { display: flex; flex-wrap: wrap; gap: 8px; margin: 12px 0 18px; }
    .meta-row span {
      border: 1px solid var(--line); background: var(--surface); border-radius: 999px;
      padding: 4px 9px; color: var(--muted); font-size: 12px;
      font-variant-numeric: tabular-nums;
    }
    .insight-callout {
      margin: 22px 0; padding: 20px 22px; border-left: 4px solid var(--blue);
      border-radius: 0 8px 8px 0; background: #f4f7ff;
    }
    .insight-callout p { margin: 0; font-size: 18px; line-height: 1.75; color: #13213e; }
    .judgment-block {
      margin: 24px 0; padding: 18px 20px; border: 1px solid var(--line); border-radius: 8px;
      background: #fffaf0;
    }
    .judgment-block h3 { margin-top: 0; border-left-color: var(--amber); }
    .action-grid {
      display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; margin-top: 16px;
    }
    .action-cell {
      border: 1px solid var(--line); border-radius: 8px; background: #fff; padding: 12px;
    }
    .action-cell span { display: block; color: var(--muted); font-size: 12px; margin-bottom: 4px; }
    .action-cell p { margin: 0; font-size: 14px; line-height: 1.55; }
    .mode-strip {
      position: sticky; top: 58px; z-index: 20;
      display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 8px;
      padding: 10px 0; margin: 22px 0 26px;
      background: linear-gradient(180deg, rgba(255,253,249,.96), rgba(255,253,249,.9));
      backdrop-filter: blur(12px);
      border-bottom: 1px solid rgba(217,222,229,.72);
    }
    .mode-strip a {
      color: #30405c; text-decoration: none; border: 1px solid #cfdaea; background: #fff; border-radius: 10px;
      padding: 9px 10px; font-size: 13px; min-height: 50px;
      display: flex; flex-direction: column; justify-content: center; gap: 2px;
      transition: transform .16s ease, border-color .16s ease, background .16s ease;
    }
    .mode-strip a strong { color: #162238; font-size: 14px; line-height: 1.2; }
    .mode-strip a span { color: var(--muted); font-size: 11px; line-height: 1.2; }
    .mode-strip a:hover,
    .mode-strip a[aria-current="true"] {
      background: var(--blue-soft); border-color: #aebfe0;
    }
    .mode-strip a[aria-current="true"] strong { color: var(--blue); }
    .section-stack { margin-top: 8px; }
    .section-group {
      scroll-margin-top: 124px;
      margin: 30px 0 36px;
    }
    .section-group-header {
      display: grid; grid-template-columns: 64px minmax(0, 1fr) auto;
      gap: 16px; align-items: start;
      padding: 20px 0 14px;
      border-top: 1px solid #cfd6e0;
      border-bottom: 1px solid #e7ebef;
    }
    .section-group-label {
      display: inline-flex; align-items: center; justify-content: center;
      min-height: 32px; border-radius: 8px;
      color: var(--blue); background: var(--blue-soft);
      font-size: 13px; font-weight: 800;
    }
    .section-group-header h3 {
      margin: 0 0 5px; padding: 0; border-left: 0;
      font-size: 21px; line-height: 1.28; color: #121b2d;
    }
    .section-group-header p {
      margin: 0; color: var(--muted); font-size: 14px; line-height: 1.6;
      max-width: 58ch;
    }
    .section-group-count {
      color: var(--muted); border: 1px solid var(--line); border-radius: 999px;
      padding: 3px 9px; font-size: 12px; white-space: nowrap; font-variant-numeric: tabular-nums;
    }
    .section-group.speak .section-group-label { color: #8b4b09; background: var(--amber-soft); }
    .section-group.asset .section-group-label { color: var(--teal); background: var(--teal-soft); }
    .section-group.decision .section-group-label { color: #4d5570; background: #f0f2f6; }
    .section-group-body { margin-top: 12px; }
    .section-group.speak .reader-section,
    .section-group.asset .reader-section {
      background: #fff;
      border-color: #d7dee8;
    }
    .reader-section {
      margin: 10px 0;
      border: 1px solid var(--line);
      border-radius: 10px;
      background: #fffdf9;
      overflow: hidden;
      scroll-margin-top: 110px;
    }
    .reader-section summary {
      cursor: pointer; display: flex; align-items: center; justify-content: flex-start; gap: 10px;
      padding: 16px 17px; list-style: none;
      background: linear-gradient(180deg, #fff, #fafbfc);
    }
    .reader-section summary::-webkit-details-marker { display: none; }
    .reader-section summary::before {
      content: "";
      width: 8px; height: 8px; flex: 0 0 auto;
      border-right: 2px solid var(--blue);
      border-bottom: 2px solid var(--blue);
      transform: rotate(-45deg);
      transition: transform .16s ease;
      margin-left: 2px;
    }
    .reader-section[open] summary::before { transform: rotate(45deg); }
    .reader-section summary span { font-weight: 760; color: var(--ink); text-wrap: pretty; }
    .reader-section summary small {
      color: var(--muted); border: 1px solid var(--line); border-radius: 999px; padding: 2px 8px; font-size: 11px;
    }
    .reader-section-body {
      padding: 8px 20px 24px 38px;
      border-top: 1px solid rgba(217,222,229,.82);
      background: #fffdf8;
    }
    .reader-section-body > p:first-child { margin-top: 10px; }
    .reader-section-body p {
      max-width: 68ch;
    }
    .inline-label {
      display: inline-flex; align-items: center; min-height: 25px;
      margin: 0 6px 4px 0; padding: 2px 8px;
      color: #173f9a; background: var(--blue-soft); border: 1px solid #c7d5ef;
      border-radius: 7px; font-weight: 820; line-height: 1.25;
    }
    .eight-question-workbench {
      margin: 8px 0 2px;
    }
    .eight-question-workbench-header {
      border: 1px solid #cbd8ec; border-radius: 12px 12px 0 0;
      background: linear-gradient(180deg, #f7f9ff, #fffdf8);
      padding: 18px 18px 16px;
    }
    .eight-question-workbench-header span {
      display: inline-flex; color: var(--blue); background: var(--blue-soft);
      border: 1px solid #c7d5ef; border-radius: 7px; padding: 3px 8px;
      font-size: 12px; font-weight: 820; margin-bottom: 10px;
    }
    .eight-question-workbench-header h4 {
      margin: 0 0 7px; padding: 0; background: none; color: var(--ink);
      font-size: 20px; line-height: 1.28;
    }
    .eight-question-workbench-header p {
      margin: 0; max-width: 68ch; color: var(--muted); font-size: 14px; line-height: 1.7;
    }
    .eight-question-route {
      display: grid; grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 1px; padding: 1px; background: #cbd8ec; border-left: 1px solid #cbd8ec; border-right: 1px solid #cbd8ec;
    }
    .eight-question-route a {
      min-width: 0; min-height: 52px; display: grid; grid-template-columns: 34px minmax(0, 1fr);
      align-items: center; gap: 8px; padding: 8px 10px; background: #fff;
      color: #26344e; text-decoration: none; transition: background .16s ease, color .16s ease;
    }
    .eight-question-route a:hover {
      background: var(--blue-soft); color: #173f9a;
    }
    .eight-question-route strong {
      color: var(--blue); font-size: 12px; font-variant-numeric: tabular-nums;
    }
    .eight-question-route span {
      overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 13px; font-weight: 760;
    }
    .eight-question-list {
      display: grid; gap: 12px; padding: 14px; border: 1px solid #cbd8ec; border-top: 0;
      border-radius: 0 0 12px 12px; background: #f8fafc;
    }
    .eight-question-card {
      scroll-margin-top: 124px; border: 1px solid #d5deea; border-radius: 10px;
      background: #fff; padding: 16px;
    }
    .eight-question-card-header {
      display: grid; grid-template-columns: 48px minmax(0, 1fr); gap: 12px; align-items: start;
      padding-bottom: 12px; border-bottom: 1px solid #e5ebf2; margin-bottom: 12px;
    }
    .eight-question-number {
      display: inline-flex; align-items: center; justify-content: center;
      width: 40px; height: 40px; border-radius: 9px; color: #173f9a;
      background: var(--blue-soft); border: 1px solid #adc1ef; font-weight: 860;
      font-variant-numeric: tabular-nums;
    }
    .eight-question-card-header h5 {
      margin: 0 0 4px; color: var(--ink); font-size: 18px; line-height: 1.32;
    }
    .eight-question-card-header p {
      margin: 0; color: var(--muted); font-size: 13px; line-height: 1.45;
    }
    .eight-question-fields {
      display: grid; gap: 9px; margin: 0;
    }
    .eight-question-field {
      display: grid; grid-template-columns: 116px minmax(0, 1fr); gap: 14px; align-items: start;
      margin: 0; padding: 10px 0; border-bottom: 1px solid #edf1f6;
    }
    .eight-question-field:last-child { border-bottom: 0; }
    .eight-question-field dt {
      color: #173f9a; font-size: 12px; font-weight: 820; line-height: 1.45;
    }
    .eight-question-field dd {
      margin: 0; color: #26344e; font-size: 14.5px; line-height: 1.68;
    }
    .eight-question-field dd p {
      margin: 0; max-width: 68ch;
    }
    .eight-question-focus-grid {
      display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px;
      margin: 12px 0 0;
    }
    .eight-question-field.focus {
      display: block; padding: 12px 13px; border: 1px solid #d4e0f3; border-left: 4px solid var(--blue);
      border-radius: 9px; background: #f7f9ff;
    }
    .eight-question-field.focus dt {
      display: block; color: #173f9a; margin-bottom: 6px; font-size: 12px; font-weight: 860;
    }
    .eight-question-field.focus dd {
      color: #18243a; font-weight: 560;
    }
    .phase-sequence {
      margin: 0; display: grid; gap: 8px;
    }
    .phase-step {
      display: grid; grid-template-columns: 82px minmax(0, 1fr); gap: 10px;
      align-items: start; margin: 0; padding: 9px 10px;
      border: 1px solid #e1e8f2; border-radius: 8px; background: #f8fafc;
    }
    .phase-step dt {
      color: #173f9a; font-size: 12px; font-weight: 860; line-height: 1.35;
      font-variant-numeric: tabular-nums;
    }
    .phase-step dd { margin: 0; color: #26344e; font-size: 14px; line-height: 1.62; }
    .phase-step dd p { margin: 0; }
    .six-layer-workbench,
    .speech-module {
      border: 1px solid #cbd8ec; border-radius: 12px; background: #f8fafc; overflow: hidden;
    }
    .six-layer-workbench-header,
    .speech-module-header {
      padding: 18px 18px 15px; background: linear-gradient(180deg, #f7f9ff, #fffdf8);
      border-bottom: 1px solid #dbe4f1;
    }
    .six-layer-workbench-header span,
    .speech-module-header span {
      display: inline-flex; color: var(--blue); background: var(--blue-soft);
      border: 1px solid #c7d5ef; border-radius: 7px; padding: 3px 8px;
      font-size: 12px; font-weight: 820; margin-bottom: 10px;
    }
    .six-layer-workbench-header h4,
    .speech-module-header h4 {
      margin: 0 0 7px; padding: 0; background: none; color: var(--ink);
      font-size: 20px; line-height: 1.28;
    }
    .six-layer-workbench-header p {
      margin: 0; max-width: 70ch; color: var(--muted); font-size: 14px; line-height: 1.7;
    }
    .six-layer-grid {
      display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1px;
      background: #dbe4f1;
    }
    .six-layer-card {
      min-width: 0; background: #fff; padding: 15px 16px;
    }
    .six-layer-card header {
      display: flex; align-items: center; gap: 9px; margin-bottom: 10px;
    }
    .six-layer-card header span,
    .speech-step > span {
      display: inline-flex; align-items: center; justify-content: center;
      width: 30px; height: 30px; border-radius: 8px; color: #173f9a;
      background: var(--blue-soft); border: 1px solid #adc1ef; font-size: 12px; font-weight: 860;
      font-variant-numeric: tabular-nums;
    }
    .six-layer-card h5 {
      margin: 0; color: var(--ink); font-size: 17px; line-height: 1.32;
    }
    .six-layer-card-body p {
      margin: 8px 0; color: #26344e; font-size: 14.5px; line-height: 1.66;
    }
    .speech-step-list {
      display: grid; gap: 1px; background: #dbe4f1;
    }
    .speech-step {
      display: grid; grid-template-columns: 42px minmax(0, 1fr); gap: 12px;
      background: #fff; padding: 14px 16px;
    }
    .speech-step strong {
      display: block; color: #173f9a; font-size: 13px; margin-bottom: 4px;
    }
    .speech-step p {
      margin: 0; color: #26344e; font-size: 14.5px; line-height: 1.66;
    }
    .speech-closing {
      border-top: 1px solid #dbe4f1; background: #fffdf8; padding: 16px 18px;
    }
    .speech-closing p {
      margin: 8px 0; color: #18243a; font-size: 15px; line-height: 1.72; font-weight: 560;
    }
    .reader-section-body h3 {
      margin-top: 28px;
    }
    .reader-section-body ul,
    .reader-section-body ol {
      max-width: 68ch;
    }
    .reader-section.reason summary small { color: var(--blue); }
    .reader-section.evidence summary small { color: var(--teal); }
    .reader-section.speak summary small { color: var(--amber); }
    .reader-section.asset summary small { color: var(--teal); }
    .table-wrap {
      overflow-x: auto; margin: 16px 0 22px; border: 1px solid var(--line); border-radius: 8px; background: #fff;
      -webkit-overflow-scrolling: touch; max-width: 100%; min-width: 0; overscroll-behavior-inline: contain;
    }
    table { width: 100%; min-width: 760px; border-collapse: collapse; }
    th, td { border-bottom: 1px solid var(--line); padding: 10px 11px; vertical-align: top; text-align: left; }
    th { background: #f0ece3; color: #394255; font-size: 13px; }
    td { font-size: 14px; line-height: 1.6; }
    tr:last-child td { border-bottom: 0; }
    .postlude {
      margin-top: 54px; padding-top: 24px; border-top: 2px solid #e6dfd1;
      scroll-margin-top: 82px;
    }
    .mobile-bottom-nav { display: none; }
    .reader-toast {
      position: fixed; left: 50%; bottom: 24px; z-index: 80; max-width: min(520px, calc(100vw - 32px));
      transform: translate(-50%, 10px); opacity: 0; pointer-events: none;
      padding: 12px 14px; border-radius: 10px; border: 1px solid #b9c8eb;
      background: rgba(255,255,255,.98); box-shadow: 0 18px 48px rgba(29,42,65,.18);
      color: #172033; font-size: 13px; line-height: 1.55;
      transition: opacity .18s ease, transform .18s ease;
    }
    .reader-toast.show { opacity: 1; transform: translate(-50%, 0); }
    @media (min-width: 1500px) {
      .topbar-inner,
      .layout { max-width: 1540px; }
      .layout { grid-template-columns: 270px minmax(0, 1100px); gap: 60px; }
      .reader-inner { max-width: 980px; }
    }
    @media (max-width: 980px) {
      .layout { display: block; padding: 20px 18px 96px; }
      .reader-toc {
        position: sticky; top: 58px; z-index: 30; max-height: none; overflow-x: auto;
        display: flex; gap: 8px; padding: 10px 0; margin: 0 0 16px;
        background: rgba(247,245,239,.94); border-bottom: 1px solid var(--line);
      }
      .reader-toc strong, .nav-group-title { display: none; }
      .nav-group { display: flex; gap: 8px; margin: 0; }
      .reader-toc a {
        flex: 0 0 auto; border: 1px solid var(--line); border-radius: 999px; padding: 6px 10px; background: var(--surface);
        min-height: 34px;
      }
      .toc-case {
        display: flex !important; grid-template-columns: none; min-height: 34px !important;
      }
      .toc-case span { font-size: 12px; }
      .toc-case em {
        max-width: 160px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 12px;
      }
      main.reader { border-radius: 8px; }
      .reader-inner { padding: 34px 30px 70px; }
      .case-card { grid-template-columns: 70px minmax(0, 1fr); }
      .case-card-actions { grid-column: 2; grid-row: auto; justify-content: flex-start; margin-top: 10px; }
      .candidate-item { grid-template-columns: minmax(170px, 210px) minmax(0, 1fr); }
      .radar-grid { grid-template-columns: 1fr; }
      .score-row { grid-template-columns: 72px 28px minmax(0, 1fr); }
      .section-group-header { grid-template-columns: 56px minmax(0, 1fr); }
      .section-group-count { display: none; }
    }
    @media (max-width: 680px) {
      body { font-size: 16px; line-height: 1.82; background: var(--paper); }
      .topbar { position: static; }
      .topbar-inner { display: block; padding: 12px 14px; }
      .source-chips { justify-content: flex-start; margin-top: 8px; overflow-x: auto; flex-wrap: nowrap; padding-bottom: 2px; }
      .mobile-toc-panel {
        display: block; position: sticky; top: 0; z-index: 45;
        background: rgba(255,254,251,.97); border-bottom: 1px solid var(--line); backdrop-filter: blur(10px);
      }
      .mobile-toc-panel summary {
        list-style: none; min-height: 48px; padding: 0 18px;
        display: flex; align-items: center; justify-content: space-between;
        cursor: pointer; font-weight: 800; color: #202b41;
      }
      .mobile-toc-panel summary::-webkit-details-marker { display: none; }
      .mobile-toc-panel summary::after {
        content: ""; width: 9px; height: 9px; border-right: 2px solid var(--blue); border-bottom: 2px solid var(--blue);
        transform: rotate(45deg); transition: transform .16s ease;
      }
      .mobile-toc-panel details[open] summary::after { transform: rotate(225deg); }
      .mobile-toc-links {
        display: grid; gap: 8px; max-height: 48vh; overflow: auto;
        padding: 0 18px 16px; -webkit-overflow-scrolling: touch;
      }
      .mobile-toc-links a {
        display: block; min-height: 44px; padding: 10px 12px; border: 1px solid var(--line); border-radius: 8px;
        background: #fff; color: #2b3650; text-decoration: none; line-height: 1.45;
      }
      .mobile-toc-links a[aria-current="true"] {
        border-color: #adc1ef; background: var(--blue-soft); color: #173f9a; font-weight: 750;
      }
      .toc-case-mobile {
        display: grid !important; grid-template-columns: 56px minmax(0, 1fr); gap: 8px; align-items: start;
      }
      .toc-case-mobile span { color: var(--blue); font-weight: 800; white-space: nowrap; }
      .toc-case-mobile em { font-style: normal; color: inherit; }
      .layout { padding: 0 0 84px; }
      .reader-toc { display: none; }
      main.reader { border: 0; border-radius: 0; box-shadow: none; }
      .reader-inner { padding: 26px 18px 68px; max-width: none; }
      h1 { font-size: 25px; }
      h2 { font-size: 23px; margin-top: 42px; }
      .guide-card { padding: 16px; }
      .case-card {
        display: block; padding: 15px 16px;
      }
      .case-card h3 { margin: 9px 0 7px; }
      .case-card-insight { margin: 0 0 7px; }
      .case-card-reason { margin-top: 10px; }
      .case-card-actions { justify-content: flex-start; margin-top: 10px; }
      .content-block-header { margin-top: 38px; padding: 18px 0 0; }
      .content-block-header h2 { font-size: 22px; }
      .candidate-item {
        display: block; padding: 15px 15px 16px;
      }
      .candidate-score-panel { margin-bottom: 14px; padding: 13px; }
      .candidate-score strong { font-size: 30px; }
      .candidate-meta { gap: 5px; }
      .candidate-meta span { width: 100%; justify-content: space-between; }
      .candidate-main h3 { font-size: 17px; }
      .candidate-links { display: grid; gap: 7px; align-items: start; }
      .source-link { width: fit-content; }
      .context-list div { grid-template-columns: 1fr; gap: 2px; }
      .context-list dt { white-space: normal; }
      .radar-context-list dd,
      .context-list dd { font-size: 14px; }
      .score-row {
        display: block; padding: 10px 11px;
      }
      .score-row span,
      .score-row strong { display: inline-flex; margin-right: 8px; }
      .selection-card { padding: 15px 16px; }
      .insight-callout { padding: 16px 17px; }
      .insight-callout p { font-size: 17px; }
      .action-grid { grid-template-columns: 1fr; }
      .mode-strip {
        top: 48px; grid-template-columns: repeat(4, minmax(72px, 1fr)); gap: 6px;
        overflow-x: auto; padding: 8px 0; margin: 18px 0 22px;
      }
      .mode-strip a { min-height: 46px; padding: 8px 8px; }
      .mode-strip a strong { font-size: 13px; }
      .mode-strip a span { font-size: 10.5px; }
      .section-group {
        scroll-margin-top: 112px;
        margin: 26px 0 30px;
      }
      .section-group-header {
        grid-template-columns: 1fr; gap: 10px; padding: 18px 0 12px;
      }
      .section-group-label {
        justify-content: flex-start; width: fit-content; min-height: 30px;
        padding: 0 10px;
      }
      .section-group-header h3 { font-size: 20px; }
      .section-group-header p { font-size: 14px; line-height: 1.65; }
      .reader-section summary { padding: 17px 14px; min-height: 56px; }
      .reader-section summary small { display: none; }
      .reader-section-body { padding: 8px 16px 22px 28px; }
      .eight-question-workbench-header { padding: 15px 15px 14px; }
      .eight-question-workbench-header h4 { font-size: 18px; }
      .eight-question-route { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .eight-question-route a {
        min-height: 48px; grid-template-columns: 30px minmax(0, 1fr); padding: 7px 9px;
      }
      .eight-question-list { padding: 10px; gap: 10px; }
      .eight-question-card { padding: 14px; }
      .eight-question-card-header {
        grid-template-columns: 40px minmax(0, 1fr); gap: 10px;
      }
      .eight-question-number {
        width: 34px; height: 34px; border-radius: 8px; font-size: 13px;
      }
      .eight-question-card-header h5 { font-size: 17px; }
      .eight-question-field {
        grid-template-columns: 1fr; gap: 4px; padding: 9px 0;
      }
      .eight-question-focus-grid {
        grid-template-columns: 1fr; gap: 8px;
      }
      .phase-step {
        grid-template-columns: 1fr; gap: 4px; padding: 9px 0;
      }
      .six-layer-workbench-header,
      .speech-module-header {
        padding: 15px 15px 14px;
      }
      .six-layer-workbench-header h4,
      .speech-module-header h4 {
        font-size: 18px;
      }
      .six-layer-grid {
        grid-template-columns: 1fr;
      }
      .six-layer-card {
        padding: 14px;
      }
      .speech-step {
        grid-template-columns: 34px minmax(0, 1fr); gap: 10px; padding: 13px 14px;
      }
      .speech-step > span {
        width: 30px; height: 30px;
      }
      .speech-closing {
        padding: 14px;
      }
      table { min-width: 680px; }
      .mobile-bottom-nav {
        position: fixed; left: 0; right: 0; bottom: 0; z-index: 60; display: grid; grid-template-columns: repeat(4, 1fr);
        background: rgba(255,253,248,.96); border-top: 1px solid var(--line); backdrop-filter: blur(12px);
      }
      .mobile-bottom-nav a {
        display: block; text-align: center; padding: 10px 4px 12px; color: var(--muted); text-decoration: none; font-size: 13px;
      }
      .mobile-bottom-nav a:hover,
      .mobile-bottom-nav a[aria-current="true"] { color: var(--blue); font-weight: 800; }
    }
    :root {
      --bg: #edf1f3;
      --paper: #fffdfa;
      --surface: #ffffff;
      --surface-muted: #f4f6f8;
      --surface-tint: #f8fafc;
      --ink: #111827;
      --text: #263348;
      --muted: #667085;
      --faint: #8792a4;
      --line: #dfe5ec;
      --line-strong: #c8d1dc;
      --blue: #2254b8;
      --blue-soft: #edf3ff;
      --blue-wash: #f7faff;
      --teal: #19736b;
      --teal-soft: #eaf5f3;
      --amber: #8b5a15;
      --amber-soft: #fff6df;
      --red: #a93328;
      --semantic-insight: #1f56b5;
      --semantic-insight-soft: #f3f7ff;
      --semantic-insight-line: #9db8e8;
      --semantic-conclusion: #254d99;
      --semantic-conclusion-soft: #f6f9ff;
      --semantic-conclusion-line: #b7c8eb;
      --semantic-next: #19736b;
      --semantic-next-soft: #eff8f6;
      --semantic-next-line: #9ccfc7;
      --semantic-action: #19736b;
      --semantic-action-soft: #edf8f4;
      --semantic-action-line: #a4d0c4;
      --semantic-practice: #8b5a15;
      --semantic-practice-soft: #fff8e8;
      --semantic-practice-line: #e3c17b;
      --semantic-risk: #9c3d35;
      --semantic-risk-soft: #fff5f3;
      --semantic-risk-line: #dfaaa4;
      --semantic-evidence: #596679;
      --semantic-evidence-soft: #f6f8fa;
      --semantic-evidence-line: #d5dde7;
      --semantic-process: #415f93;
      --semantic-process-soft: #f5f8fc;
      --semantic-process-line: #c8d7eb;
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 14px;
      --radius-xl: 18px;
      --radius-pill: 999px;
      --font-body: "SF Pro Text", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Segoe UI", system-ui, sans-serif;
      --font-display: "SF Pro Display", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Segoe UI", system-ui, sans-serif;
      --font-mono: "SFMono-Regular", "Cascadia Mono", "Menlo", "Consolas", ui-monospace, monospace;
      --shadow: 0 26px 80px rgba(28, 39, 58, 0.075);
      --shadow-soft: 0 14px 44px rgba(36, 54, 78, 0.07);
      --ease: cubic-bezier(.2,.8,.2,1);
    }
    body {
      background:
        radial-gradient(circle at 12% -8%, rgba(34,84,184,.08), transparent 34%),
        linear-gradient(180deg, #f3f6f7 0%, var(--bg) 36%, #e9eef2 100%);
      color: var(--ink);
      font: 16px/1.74 var(--font-body);
      -webkit-font-smoothing: antialiased;
      text-rendering: optimizeLegibility;
    }
    body::before {
      content: "";
      position: fixed; inset: 0; z-index: -1; pointer-events: none;
      background-image:
        linear-gradient(rgba(17,24,39,.018) 1px, transparent 1px),
        linear-gradient(90deg, rgba(17,24,39,.014) 1px, transparent 1px);
      background-size: 28px 28px;
      mask-image: linear-gradient(180deg, rgba(0,0,0,.8), transparent 70%);
    }
    a {
      color: var(--blue);
      text-decoration-thickness: 1px;
      text-underline-offset: 4px;
    }
    code {
      font-family: var(--font-mono);
      background: #f5f7fa;
      border-color: #d9e1ea;
      border-radius: var(--radius-sm);
    }
    .progress {
      height: 2px;
      background: linear-gradient(90deg, #1d4fae, #5b7fd2);
    }
    .topbar {
      background: rgba(244,247,248,.88);
      border-bottom: 1px solid rgba(207,216,226,.78);
      box-shadow: 0 8px 30px rgba(31,42,59,.04);
    }
    .topbar-inner {
      padding: 15px 28px;
    }
    .brand strong {
      font-family: var(--font-display);
      font-size: 15px;
      font-weight: 660;
      letter-spacing: 0;
    }
    .brand span {
      color: var(--muted);
      font-size: 12.5px;
    }
    .chip {
      min-height: 30px;
      padding: 5px 10px;
      border-radius: var(--radius-pill);
      border-color: #cfd9e5;
      background: rgba(255,255,255,.72);
      color: #536073;
      font-size: 12px;
      font-weight: 560;
      box-shadow: inset 0 1px 0 rgba(255,255,255,.72);
    }
    .chip.ok {
      color: #166b63;
      background: rgba(234,245,243,.78);
      border-color: #c8e2de;
    }
    .chip.warn {
      color: #80530f;
      background: rgba(255,246,223,.78);
      border-color: #eed9a8;
    }
    .layout {
      grid-template-columns: 252px minmax(0, 1040px);
      gap: 50px;
      padding-top: 30px;
    }
    .reader-toc {
      padding: 12px 6px 24px;
      color: var(--muted);
    }
    .reader-toc strong {
      color: #1f2a3d;
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 650;
      margin-bottom: 16px;
    }
    .nav-group {
      margin-bottom: 18px;
    }
    .nav-group-title {
      color: #7a8595;
      font-size: 11px;
      font-weight: 600;
      margin: 14px 0 6px;
    }
    .reader-toc a {
      min-height: 36px;
      padding: 7px 11px;
      border-radius: var(--radius-md);
      color: #515e70;
      transition: background .18s var(--ease), border-color .18s var(--ease), color .18s var(--ease), transform .18s var(--ease);
    }
    .reader-toc a:hover {
      background: rgba(255,255,255,.68);
      color: var(--blue);
      border-color: rgba(172,190,219,.7);
    }
    .reader-toc a[aria-current="true"] {
      background: rgba(237,243,255,.86);
      color: #1e4da8;
      border-color: #b9c9e7;
      font-weight: 650;
      box-shadow: inset 3px 0 0 var(--blue);
    }
    .toc-case {
      grid-template-columns: 52px minmax(0, 1fr);
    }
    .toc-case span {
      color: #1e4da8;
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 650;
    }
    .toc-case em {
      color: #4d596a;
      font-size: 12.5px;
      line-height: 1.45;
    }
    main.reader {
      background: linear-gradient(180deg, rgba(255,255,255,.96), var(--paper));
      border-color: rgba(204,213,224,.92);
      border-radius: var(--radius-xl);
      box-shadow: var(--shadow);
    }
    .reader-inner {
      max-width: 900px;
      padding: 56px 64px 96px;
    }
    .reader-hero {
      margin-bottom: 38px;
    }
    .reader-hero .eyebrow,
    .section-eyebrow {
      color: #1f56b5;
      font-size: 12.5px;
      font-weight: 620;
      margin-bottom: 14px;
    }
    h1, h2, h3, h4 {
      font-family: var(--font-display);
      color: var(--ink);
      line-height: 1.24;
      text-wrap: pretty;
    }
    h1 {
      margin-bottom: 18px;
      font-size: 32px;
      font-weight: 640;
      letter-spacing: 0;
    }
    h2 {
      margin: 62px 0 20px;
      padding-bottom: 14px;
      border-bottom-color: #dbe2ea;
      font-size: 25px;
      font-weight: 650;
    }
    h3 {
      margin: 38px 0 16px;
      padding-left: 13px;
      border-left: 3px solid var(--blue);
      font-size: 19px;
      font-weight: 650;
    }
    h4 {
      margin: 28px 0 12px;
      padding: 0;
      background: none;
      border-radius: 0;
      color: #263348;
      font-size: 16px;
      font-weight: 600;
    }
    p, li {
      color: var(--text);
    }
    p {
      margin: 12px 0;
    }
    li {
      margin: 6px 0;
    }
    .guide-card {
      border-color: #e1d4b7;
      border-radius: var(--radius-lg);
      background: linear-gradient(180deg, #fffaf0, #fffdf8);
      padding: 24px;
      box-shadow: inset 0 1px 0 rgba(255,255,255,.8);
    }
    .guide-card h2 {
      font-size: 23px;
      font-weight: 650;
    }
    .guide-path span {
      border-radius: var(--radius-pill);
      background: rgba(255,255,255,.76);
      color: #745315;
      font-weight: 620;
    }
    .case-card-list {
      gap: 14px;
      margin-top: 22px;
    }
    .case-card {
      grid-template-columns: 82px minmax(0, 1fr);
      border-color: #d9e1eb;
      border-radius: var(--radius-lg);
      background: rgba(255,255,255,.92);
      padding: 20px 22px;
      box-shadow: 0 1px 0 rgba(255,255,255,.8);
      transition: border-color .18s var(--ease), transform .18s var(--ease), box-shadow .18s var(--ease), background .18s var(--ease);
    }
    .case-card:hover {
      border-color: #b8c8e2;
      background: #fff;
      transform: translateY(-1px);
      box-shadow: var(--shadow-soft);
    }
    .case-card-top {
      font-family: var(--font-mono);
      color: var(--faint);
      font-size: 11.5px;
      line-height: 1.5;
    }
    .case-card-top strong {
      color: #166b63;
      font-size: 13px;
      font-weight: 650;
    }
    .case-card h3 {
      font-size: 18px;
      font-weight: 650;
    }
    .case-card-insight {
      color: #1f2937;
      font-size: 14.5px;
      line-height: 1.72;
    }
    .case-card-weak {
      color: #788497;
      font-size: 12.5px;
    }
    .case-card-reason {
      padding: 12px 14px;
      border-left-color: #b9c9e7;
      background: #f8faff;
      border-radius: 0 var(--radius-md) var(--radius-md) 0;
    }
    .case-card-reason span {
      color: #1f56b5;
      font-size: 12px;
      font-weight: 650;
    }
    .case-card-actions a,
    .candidate-breakdown summary,
    .score-help {
      border-radius: var(--radius-pill);
      font-weight: 620;
    }
    .case-card-actions a {
      min-height: 34px;
      padding: 6px 13px;
      background: #fff;
      border-color: #b9c9e7;
      color: #1f56b5;
    }
    .case-card-actions a:hover {
      background: var(--blue-soft);
      border-color: #92a9d6;
    }
    .content-block-header {
      margin-top: 58px;
      border-top-color: #dbe2ea;
    }
    .content-block-header span {
      background: transparent;
      color: #1f56b5;
      padding: 0;
      border-radius: 0;
      font-size: 12.5px;
      font-weight: 650;
    }
    .content-block-header h2 {
      font-size: 24px;
      font-weight: 650;
    }
    .content-block-header p {
      color: var(--muted);
      line-height: 1.72;
    }
    .candidate-item,
    .selection-card,
    .radar-card,
    .reference-disclosure,
    .judgment-block,
    .action-cell {
      border-color: #dce3eb;
      border-radius: var(--radius-lg);
      background: rgba(255,255,255,.94);
      box-shadow: 0 1px 0 rgba(255,255,255,.74);
    }
    .candidate-item.deep {
      border-color: #b9c9e7;
      background: linear-gradient(180deg, #fbfdff, #fffefa);
    }
    .candidate-score-panel {
      border-color: #dce4ee;
      border-radius: var(--radius-md);
      background: #f8fafc;
    }
    .candidate-score strong {
      font-family: var(--font-mono);
      font-size: 32px;
      font-weight: 650;
    }
    .candidate-meta span {
      border-radius: var(--radius-pill);
      background: #f9fbfd;
      color: #4e5a6c;
    }
    .candidate-main h3 {
      font-size: 19px;
      font-weight: 650;
    }
    .radar-card h3 {
      font-size: 17px;
      font-weight: 650;
      letter-spacing: 0;
    }
    .context-list dt,
    .eight-question-field dt,
    .phase-step dt {
      color: #1f56b5;
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 650;
    }
    .candidate-context-list {
      background: #f8fafc;
      border-left-color: #b9c9e7;
      border-radius: 0 var(--radius-md) var(--radius-md) 0;
    }
    .candidate-links {
      gap: 9px;
    }
    .candidate-links > span {
      color: var(--faint);
      font-size: 12px;
    }
    .source-link {
      color: #1f56b5;
      font-weight: 650;
      text-decoration-thickness: 1.5px;
    }
    .source-link:hover {
      color: #153c85;
    }
    .score-row {
      border-color: #e5ebf1;
      border-radius: var(--radius-md);
      background: #fff;
    }
    .case-article {
      margin-top: 70px;
      border-top-color: #cfd8e3;
    }
    .case-kicker {
      color: #1f56b5;
      font-size: 12.5px;
      font-weight: 650;
    }
    .case-header h2 {
      font-weight: 650;
      letter-spacing: 0;
    }
    .meta-row span {
      border-radius: var(--radius-pill);
      background: #fbfcfd;
      color: #667085;
      font-family: var(--font-mono);
      font-size: 11.5px;
    }
    .insight-callout {
      border-left-color: var(--blue);
      border-radius: 0 var(--radius-lg) var(--radius-lg) 0;
      background: #f6f9ff;
      padding: 22px 24px;
    }
    .insight-callout p {
      color: #162238;
      font-size: 18px;
      line-height: 1.78;
    }
    .insight-callout.semantic-insight {
      border-left-color: var(--semantic-insight-line);
      background: linear-gradient(180deg, #f6f9ff, #fbfdff);
    }
    .judgment-block.semantic-conclusion {
      border-color: var(--semantic-conclusion-line);
      background: linear-gradient(180deg, #fffefa, var(--semantic-conclusion-soft));
    }
    .action-cell.semantic-action,
    .action-cell.semantic-next {
      border-left: 3px solid var(--semantic-action-line);
      background: var(--semantic-action-soft);
    }
    .action-cell.semantic-practice {
      border-left: 3px solid var(--semantic-practice-line);
      background: var(--semantic-practice-soft);
    }
    .action-cell.semantic-risk {
      border-left: 3px solid var(--semantic-risk-line);
      background: var(--semantic-risk-soft);
    }
    .action-cell.semantic-action span,
    .action-cell.semantic-next span { color: var(--semantic-action); }
    .action-cell.semantic-practice span { color: var(--semantic-practice); }
    .action-cell.semantic-risk span { color: var(--semantic-risk); }
    .mode-strip {
      top: 60px;
      gap: 9px;
      padding: 11px 0;
      margin: 24px 0 30px;
      background: linear-gradient(180deg, rgba(255,253,250,.96), rgba(255,253,250,.9));
      border-bottom-color: rgba(217,226,236,.82);
    }
    .mode-strip a {
      min-height: 52px;
      border-color: #d5deea;
      border-radius: var(--radius-md);
      background: rgba(255,255,255,.88);
      color: #344054;
      transition: border-color .18s var(--ease), background .18s var(--ease), transform .18s var(--ease), box-shadow .18s var(--ease);
    }
    .mode-strip a strong {
      color: #182230;
      font-size: 14px;
      font-weight: 650;
    }
    .mode-strip a span {
      color: #7a8595;
      font-size: 11px;
    }
    .mode-strip a:hover,
    .mode-strip a[aria-current="true"] {
      background: #f3f7ff;
      border-color: #aebfe0;
      box-shadow: inset 0 0 0 1px rgba(34,84,184,.05);
    }
    .section-group {
      margin: 38px 0 46px;
    }
    .section-group-header {
      grid-template-columns: 58px minmax(0, 1fr) auto;
      gap: 18px;
      padding: 22px 0 16px;
      border-top-color: #d6dee8;
      border-bottom-color: #e9eef3;
    }
    .section-group-label {
      min-height: 30px;
      border-radius: var(--radius-sm);
      background: transparent;
      color: #1f56b5;
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 650;
      border: 1px solid #c6d5ef;
    }
    .section-group.speak .section-group-label,
    .section-group.asset .section-group-label,
    .section-group.decision .section-group-label {
      background: transparent;
    }
    .section-group.speak .section-group-label {
      color: #80530f;
      border-color: #ead7a9;
    }
    .section-group.asset .section-group-label {
      color: #166b63;
      border-color: #c8e2de;
    }
    .section-group.decision .section-group-label {
      color: #526074;
      border-color: #d4dce6;
    }
    .section-group-header h3 {
      font-size: 22px;
      font-weight: 650;
    }
    .section-group-header p {
      color: #667085;
      line-height: 1.68;
      max-width: 62ch;
    }
    .section-group-count {
      border-radius: var(--radius-pill);
      border-color: #d7e0eb;
      color: #7a8595;
      font-family: var(--font-mono);
      font-size: 11.5px;
    }
    .reader-section {
      margin: 12px 0;
      border-color: #dfe6ee;
      border-radius: var(--radius-lg);
      background: #ffffff;
      box-shadow: 0 1px 0 rgba(255,255,255,.8);
    }
    .reader-section summary {
      min-height: 58px;
      padding: 16px 18px;
      background: #fff;
      scroll-margin-top: 124px;
    }
    .reader-section summary::before {
      border-color: #2d5ab4;
      opacity: .9;
    }
    .reader-section summary span {
      font-size: 16px;
      font-weight: 650;
      color: #141c2f;
    }
    .reader-section summary small {
      display: none;
    }
    .reader-section-body {
      padding: 18px 24px 28px 42px;
      background: #fffefa;
      border-top-color: #edf1f5;
    }
    .reader-section-body p {
      max-width: 66ch;
      color: var(--text);
      line-height: 1.78;
    }
    .reader-section-body ul,
    .reader-section-body ol {
      max-width: 66ch;
    }
    .inline-label {
      display: inline;
      min-height: 0;
      margin: 0 4px 0 0;
      padding: 0;
      border: 0;
      border-radius: 0;
      background: transparent;
      color: #1f56b5;
      font-weight: 600;
      line-height: inherit;
    }
    .reader-section-body p > .inline-label:first-child,
    .six-layer-card-body p > .inline-label:first-child,
    .speech-closing p > .inline-label:first-child,
    .action-cell p > .inline-label:first-child,
    .candidate-main p > .inline-label:first-child {
      display: block;
      margin: 0 0 5px;
      color: #1f56b5;
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 650;
      line-height: 1.45;
    }
    .inline-label.semantic-label-insight { color: var(--semantic-insight); }
    .inline-label.semantic-label-conclusion { color: var(--semantic-conclusion); }
    .inline-label.semantic-label-next,
    .inline-label.semantic-label-action { color: var(--semantic-action); }
    .inline-label.semantic-label-practice { color: var(--semantic-practice); }
    .inline-label.semantic-label-risk { color: var(--semantic-risk); }
    .inline-label.semantic-label-evidence { color: var(--semantic-evidence); }
    .inline-label.semantic-label-process { color: var(--semantic-process); }
    .semantic-paragraph.semantic-insight,
    .semantic-paragraph.semantic-conclusion,
    .semantic-paragraph.semantic-next,
    .semantic-paragraph.semantic-action,
    .semantic-paragraph.semantic-practice,
    .semantic-paragraph.semantic-risk {
      margin: 13px 0;
      padding: 11px 13px 11px 14px;
      border-left: 3px solid var(--semantic-conclusion-line);
      border-radius: 0 var(--radius-md) var(--radius-md) 0;
      background: var(--semantic-conclusion-soft);
    }
    .semantic-paragraph.semantic-insight {
      border-left-color: var(--semantic-insight-line);
      background: var(--semantic-insight-soft);
    }
    .semantic-paragraph.semantic-next,
    .semantic-paragraph.semantic-action {
      border-left-color: var(--semantic-action-line);
      background: var(--semantic-action-soft);
    }
    .semantic-paragraph.semantic-practice {
      border-left-color: var(--semantic-practice-line);
      background: var(--semantic-practice-soft);
    }
    .semantic-paragraph.semantic-risk {
      border-left-color: var(--semantic-risk-line);
      background: var(--semantic-risk-soft);
    }
    .context-item.semantic-insight,
    .context-item.semantic-conclusion,
    .context-item.semantic-next,
    .context-item.semantic-action,
    .context-item.semantic-practice,
    .context-item.semantic-risk {
      padding: 8px 10px;
      border-left: 2px solid var(--semantic-conclusion-line);
      border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
      background: var(--semantic-conclusion-soft);
    }
    .context-item.semantic-next,
    .context-item.semantic-action {
      border-left-color: var(--semantic-action-line);
      background: var(--semantic-action-soft);
    }
    .context-item.semantic-practice {
      border-left-color: var(--semantic-practice-line);
      background: var(--semantic-practice-soft);
    }
    .context-item.semantic-risk {
      border-left-color: var(--semantic-risk-line);
      background: var(--semantic-risk-soft);
    }
    .context-item.semantic-evidence dt { color: var(--semantic-evidence); }
    .context-item.semantic-process dt { color: var(--semantic-process); }
    .eight-question-workbench-header,
    .six-layer-workbench-header,
    .speech-module-header {
      border-color: #d6e0ed;
      background: linear-gradient(180deg, #fbfdff, #fffefa);
      padding: 20px 20px 17px;
    }
    .eight-question-workbench-header span,
    .six-layer-workbench-header span,
    .speech-module-header span {
      display: block;
      width: fit-content;
      margin-bottom: 11px;
      padding: 0;
      border: 0;
      border-radius: 0;
      background: transparent;
      color: #1f56b5;
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 650;
    }
    .eight-question-workbench-header h4,
    .six-layer-workbench-header h4,
    .speech-module-header h4 {
      font-size: 21px;
      font-weight: 650;
    }
    .eight-question-workbench-header p,
    .six-layer-workbench-header p {
      line-height: 1.72;
      color: #667085;
    }
    .eight-question-route {
      background: #dbe4ef;
      border-color: #d6e0ed;
    }
    .eight-question-route a {
      background: #fff;
      color: #344054;
    }
    .eight-question-route strong,
    .eight-question-number,
    .six-layer-card header span,
    .speech-step > span {
      font-family: var(--font-mono);
    }
    .eight-question-list {
      gap: 14px;
      padding: 16px;
      border-color: #d6e0ed;
      background: #f6f8fb;
    }
    .eight-question-card {
      border-color: #dde6ef;
      border-radius: var(--radius-lg);
      padding: 18px;
      background: #fff;
    }
    .eight-question-number {
      border-radius: var(--radius-md);
      color: #1f56b5;
      background: #edf3ff;
      border-color: #bdccea;
    }
    .eight-question-card-header h5 {
      font-size: 19px;
      font-weight: 650;
    }
    .eight-question-card-header p {
      color: #7a8595;
    }
    .eight-question-field {
      border-bottom-color: #eef2f6;
    }
    .eight-question-field dd {
      color: var(--text);
      line-height: 1.72;
    }
    .eight-question-field.focus {
      border-color: #cddcf3;
      border-left-color: var(--blue);
      border-radius: var(--radius-md);
      background: #f7faff;
    }
    .eight-question-field.focus.semantic-conclusion {
      border-left-color: var(--semantic-conclusion-line);
      background: var(--semantic-conclusion-soft);
    }
    .eight-question-field.focus.semantic-next {
      border-left-color: var(--semantic-next-line);
      background: var(--semantic-next-soft);
    }
    .eight-question-field.focus dt {
      font-family: var(--font-mono);
      color: #1f56b5;
    }
    .eight-question-field.focus.semantic-conclusion dt { color: var(--semantic-conclusion); }
    .eight-question-field.focus.semantic-next dt { color: var(--semantic-next); }
    .eight-question-field.semantic-process dt { color: var(--semantic-process); }
    .eight-question-field.semantic-evidence dt { color: var(--semantic-evidence); }
    .phase-step {
      border-color: #e1e8f1;
      border-radius: var(--radius-md);
      background: #f8fafc;
    }
    .phase-step.semantic-conclusion,
    .phase-step.semantic-next {
      border-left: 3px solid var(--semantic-conclusion-line);
      background: var(--semantic-conclusion-soft);
    }
    .phase-step.semantic-next {
      border-left-color: var(--semantic-next-line);
      background: var(--semantic-next-soft);
    }
    .phase-step dd {
      color: var(--text);
      line-height: 1.66;
    }
    .six-layer-workbench,
    .speech-module {
      border-color: #d6e0ed;
      border-radius: var(--radius-lg);
      background: #f7f9fb;
    }
    .six-layer-grid,
    .speech-step-list {
      background: #dfe7f0;
    }
    .six-layer-card {
      background: #fff;
      padding: 18px;
    }
    .six-layer-card.semantic-insight,
    .six-layer-card.semantic-conclusion,
    .six-layer-card.semantic-next,
    .six-layer-card.semantic-action {
      box-shadow: inset 3px 0 0 var(--semantic-conclusion-line);
      background: linear-gradient(180deg, #fff, var(--semantic-conclusion-soft));
    }
    .six-layer-card.semantic-insight {
      box-shadow: inset 3px 0 0 var(--semantic-insight-line);
      background: linear-gradient(180deg, #fff, var(--semantic-insight-soft));
    }
    .six-layer-card.semantic-next,
    .six-layer-card.semantic-action {
      box-shadow: inset 3px 0 0 var(--semantic-action-line);
      background: linear-gradient(180deg, #fff, var(--semantic-action-soft));
    }
    .six-layer-card h5 {
      font-size: 17px;
      font-weight: 650;
    }
    .six-layer-card-body p {
      color: var(--text);
      line-height: 1.74;
    }
    .speech-step {
      background: #fff;
      padding: 16px 18px;
    }
    .speech-step.semantic-insight,
    .speech-step.semantic-conclusion,
    .speech-step.semantic-next,
    .speech-step.semantic-action {
      box-shadow: inset 3px 0 0 var(--semantic-conclusion-line);
      background: linear-gradient(180deg, #fff, var(--semantic-conclusion-soft));
    }
    .speech-step.semantic-insight {
      box-shadow: inset 3px 0 0 var(--semantic-insight-line);
      background: linear-gradient(180deg, #fff, var(--semantic-insight-soft));
    }
    .speech-step.semantic-next,
    .speech-step.semantic-action {
      box-shadow: inset 3px 0 0 var(--semantic-action-line);
      background: linear-gradient(180deg, #fff, var(--semantic-action-soft));
    }
    .speech-step strong {
      color: #1f56b5;
      font-family: var(--font-mono);
      font-size: 12.5px;
      font-weight: 650;
    }
    .speech-step p {
      color: var(--text);
      font-size: 15px;
      line-height: 1.72;
    }
    .speech-closing {
      background: #fffefa;
      padding: 18px 20px;
    }
    .speech-closing.semantic-conclusion {
      border-left: 3px solid var(--semantic-conclusion-line);
      background: var(--semantic-conclusion-soft);
    }
    .speech-closing p {
      color: #1f2937;
      line-height: 1.78;
    }
    .table-wrap {
      border-color: #dce4ec;
      border-radius: var(--radius-lg);
    }
    th {
      background: #f5f7fa;
      color: #465366;
      font-size: 12.5px;
      font-weight: 650;
    }
    td {
      color: #263348;
      font-size: 14px;
      line-height: 1.66;
    }
    .mobile-bottom-nav {
      background: rgba(255,253,250,.96);
      border-top-color: #d9e1ea;
    }
    .mobile-bottom-nav a {
      color: #6b7687;
      font-weight: 620;
    }
    .mobile-bottom-nav a[aria-current="true"] {
      color: #1f56b5;
      font-weight: 650;
    }
    @media (min-width: 1500px) {
      .reader-inner { max-width: 920px; }
    }
    @media (max-width: 980px) {
      .layout {
        padding: 18px 18px 96px;
      }
      .reader-toc {
        background: rgba(244,247,248,.94);
      }
      main.reader {
        border-radius: var(--radius-lg);
      }
      .reader-inner {
        padding: 38px 34px 78px;
      }
    }
    @media (max-width: 680px) {
      body {
        background: var(--paper);
        font-size: 16px;
        line-height: 1.76;
      }
      .topbar-inner {
        padding: 13px 16px;
      }
      .mobile-toc-panel {
        background: rgba(255,253,250,.98);
      }
      .mobile-toc-panel summary {
        color: #182230;
        font-size: 15px;
        font-weight: 650;
      }
      .layout {
        padding-bottom: 84px;
      }
      .reader-inner {
        padding: 28px 18px 72px;
      }
      h1 {
        font-size: 26px;
        line-height: 1.28;
      }
      h2 {
        font-size: 23px;
      }
      .guide-card {
        padding: 18px;
      }
      .case-card {
        padding: 17px 18px;
      }
      .mode-strip {
        margin: 18px 0 24px;
        padding: 8px 0;
      }
      .mode-strip a {
        min-height: 48px;
        border-radius: var(--radius-md);
      }
      .section-group {
        margin: 30px 0 38px;
      }
      .section-group-header {
        padding: 20px 0 14px;
      }
      .section-group-header h3 {
        font-size: 21px;
      }
      .reader-section {
        margin: 12px 0;
        border-radius: var(--radius-lg);
        scroll-margin-top: 148px;
      }
      .reader-section summary {
        padding: 16px 15px;
        scroll-margin-top: 150px;
      }
      .reader-section-body {
        padding: 15px 12px 23px;
      }
      .reader-section-body p {
        line-height: 1.78;
      }
      .inline-label {
        font-size: inherit;
      }
      .eight-question-workbench-header,
      .six-layer-workbench-header,
      .speech-module-header {
        padding: 17px 16px 15px;
      }
      .eight-question-workbench-header h4,
      .six-layer-workbench-header h4,
      .speech-module-header h4 {
        font-size: 19px;
      }
      .eight-question-list {
        padding: 9px;
      }
      .eight-question-card {
        padding: 14px 12px;
        scroll-margin-top: 148px;
      }
      .phase-step {
        padding: 11px 12px;
      }
      .six-layer-card,
      .speech-step {
        padding: 16px;
      }
      .speech-step {
        grid-template-columns: 1fr;
        gap: 8px;
        padding: 15px 14px;
      }
      .speech-step > span {
        width: 32px;
        height: 32px;
      }
      .speech-step p {
        font-size: 15px;
      }
      .six-layer-workbench,
      .speech-module,
      .eight-question-workbench-header,
      .eight-question-list {
        margin-left: 0;
        margin-right: 0;
      }
      table {
        min-width: 680px;
      }
    }
    @media (prefers-reduced-motion: reduce) {
      html { scroll-behavior: auto; }
      .case-card,
      .mode-strip a,
      .reader-toc a,
      .case-card-actions a {
        transition: none;
      }
    }
    """


def _script() -> str:
    return """
    const majorLinks = Array.from(document.querySelectorAll('.reader-toc a[href^="#"], .mobile-toc-panel a[href^="#"], .mobile-bottom-nav a[href^="#"]'));
    const modeLinks = Array.from(document.querySelectorAll('.mode-strip a[href^="#"]'));
    const allLinks = Array.from(document.querySelectorAll('a[href^="#"]'));

    function linkTarget(link) {
      return decodeURIComponent(link.getAttribute('href').slice(1));
    }

    function parentCaseId(id) {
      const match = id.match(/^(case-\\d+)/);
      return match ? match[1] : id;
    }

    function setCurrentOn(links, id, normalizer) {
      const activeId = normalizer(id);
      links.forEach((link) => {
        if (normalizer(linkTarget(link)) === activeId) {
          link.setAttribute('aria-current', 'true');
        } else {
          link.removeAttribute('aria-current');
        }
      });
    }

    function openTarget(id) {
      const target = document.getElementById(id);
      if (!target) return;
      if (target.tagName === 'SUMMARY') {
        const details = target.closest('details');
        if (details) details.open = true;
        return;
      }
      const owningDetails = target.closest('details');
      if (owningDetails) owningDetails.open = true;
      if (target.classList.contains('section-group')) {
        const details = Array.from(target.querySelectorAll('details'));
        if (target.dataset.autoOpen === 'all') {
          details.forEach((detail) => detail.open = true);
        } else if (details[0]) {
          details[0].open = true;
        }
      }
    }

    function scrollToTarget(id) {
      const target = document.getElementById(id);
      if (!target) return;
      requestAnimationFrame(() => {
        target.scrollIntoView({ block: 'start', inline: 'nearest', behavior: 'auto' });
      });
    }

    function setCurrent(id, options = {}) {
      setCurrentOn(majorLinks, parentCaseId(id), (value) => parentCaseId(value));
      setCurrentOn(modeLinks, id, (value) => value);
      openTarget(id);
      if (options.scroll) scrollToTarget(id);
    }

    function activeTargetId(targets) {
      if (!targets.length) return null;
      const activationY = Math.min(180, window.innerHeight * 0.28);
      let active = targets[0].id;
      targets.forEach((target) => {
        if (target.getBoundingClientRect().top <= activationY) {
          active = target.id;
        }
      });
      return active;
    }

    allLinks.forEach((link) => {
      link.addEventListener('click', (event) => {
        event.preventDefault();
        const targetId = linkTarget(link);
        history.pushState(null, '', '#' + encodeURIComponent(targetId));
        setCurrent(targetId, { scroll: true });
        const mobilePanel = link.closest('.mobile-toc-panel details');
        if (mobilePanel) mobilePanel.open = false;
      });
    });

    if ('IntersectionObserver' in window) {
      const majorIds = Array.from(new Set(majorLinks.map(linkTarget)));
      const majorTargets = majorIds.map((id) => document.getElementById(id)).filter(Boolean);
      const majorObserver = new IntersectionObserver(() => {
        const activeId = activeTargetId(majorTargets);
        if (activeId) setCurrentOn(majorLinks, activeId, (value) => parentCaseId(value));
      }, { rootMargin: '-18% 0px -72% 0px', threshold: [0, 0.2, 1] });
      majorTargets.forEach((target) => majorObserver.observe(target));

      const modeIds = Array.from(new Set(modeLinks.map(linkTarget)));
      const modeTargets = modeIds.map((id) => document.getElementById(id)).filter(Boolean);
      const modeObserver = new IntersectionObserver(() => {
        const activeId = activeTargetId(modeTargets);
        if (activeId) setCurrentOn(modeLinks, activeId, (value) => value);
      }, { rootMargin: '-16% 0px -76% 0px', threshold: [0, 0.2, 1] });
      modeTargets.forEach((target) => modeObserver.observe(target));
    }

    function currentHashId() {
      return location.hash ? decodeURIComponent(location.hash.slice(1)) : 'guide';
    }

    window.addEventListener('hashchange', () => setCurrent(currentHashId(), { scroll: true }));
    window.addEventListener('popstate', () => setCurrent(currentHashId(), { scroll: true }));
    const toast = document.createElement('div');
    toast.className = 'reader-toast';
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');
    document.body.appendChild(toast);
    let toastTimer;
    document.querySelectorAll('[data-toast]').forEach((button) => {
      button.addEventListener('click', () => {
        toast.textContent = button.dataset.toast || '';
        toast.classList.add('show');
        clearTimeout(toastTimer);
        toastTimer = setTimeout(() => toast.classList.remove('show'), 2600);
      });
    });
    setCurrent(currentHashId(), { scroll: !!location.hash });
    """


def render_reader_html(markdown: str, source_name: str = "") -> str:
    title = _extract_title(markdown, source_name)
    display_title = _display_title(title)
    date, version = _extract_date_version(title, source_name)
    cases = _split_cases(markdown)
    sources = _source_channel_status(markdown)
    strongest = _strongest_case(cases)
    prelude = _prelude(markdown)
    postlude = _postlude(markdown)
    selection_reasons = _parse_selection_reasons(prelude)
    average = _average_score(cases)
    strongest_text = strongest.insight if strongest else "今日核心 Insight 待抽取。"
    reader_title = "P7+ 产品思维每日训练"

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <link rel="icon" href="data:,">
  <title>{html.escape(display_title)}</title>
  <style>{_styles()}</style>
</head>
<body>
  <div class="progress" aria-hidden="true"></div>
  <header class="topbar">
    <div class="topbar-inner">
      <div class="brand">
        <strong>{reader_title}</strong>
        <span>{html.escape(date)} · 深度阅读版 · Avg {html.escape(average)}</span>
      </div>
      <div class="source-chips" aria-label="来源状态">
        {_render_source_badges(sources)}
      </div>
    </div>
  </header>

  {_render_mobile_toc(cases)}

  <div class="layout">
    {_render_nav(cases)}
    <main class="reader">
      <div class="reader-inner">
        <section class="reader-hero" id="guide">
          <span class="eyebrow">今日阅读导读</span>
          <h1>{_inline(display_title)}</h1>
          <div class="guide-card">
            <h2>先读总览，再进入深读</h2>
            <p>建议先看三个深度 case 的核心 Insight，再进入候选选择面板理解为什么选它们，最后按需要展开证据、表达演练和资产卡。</p>
            <p><strong>今日最重要 Insight：</strong>{_inline(strongest_text)}</p>
            <div class="guide-path" aria-label="推荐阅读路径">
              <span>1. 今日导读</span>
              <span>2. 核心 Insight</span>
              <span>3. 结论先行</span>
              <span>4. 论证链路</span>
              <span>5. 表达 / 资产</span>
            </div>
          </div>
          <div class="case-card-list">
            {_render_case_cards(cases, selection_reasons)}
          </div>
        </section>

        {_render_candidate_overview(prelude, cases)}

        {"".join(_render_case(case) for case in cases)}

        <section class="postlude" id="review">
          {_render_markdown_fragment(postlude)}
        </section>

        {_render_reference_panel(prelude)}
      </div>
    </main>
  </div>

  {_render_mobile_bottom_nav(cases)}

  <script>{_script()}</script>
</body>
</html>
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render Hermes daily training Markdown to reader-first HTML.")
    parser.add_argument("markdown", type=Path, help="Path to the daily training Markdown file.")
    parser.add_argument("-o", "--output", type=Path, help="Output HTML path. Defaults to *-reader.html.")
    args = parser.parse_args(argv)

    markdown_path = args.markdown
    output_path = args.output or default_output_path(markdown_path)
    markdown = markdown_path.read_text(encoding="utf-8")
    html_text = render_reader_html(markdown, source_name=markdown_path.name)
    output_path.write_text(html_text, encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
