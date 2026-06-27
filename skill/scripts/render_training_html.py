#!/usr/bin/env python3
"""Render Hermes daily training Markdown into a readable standalone HTML page."""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path


SECTION_TITLES = (
    "来源通道使用情况",
    "今日候选 case 池",
    "今日深度 case 选择理由",
    "今日雷达简报",
    "今日 3 个深度 case",
    "今日自主训练题",
    "旧 case 复现",
    "今日训练复盘",
)

SECTION_ANCHORS = {title: f"section-{index}" for index, title in enumerate(SECTION_TITLES, start=1)}


def default_output_path(markdown_path: Path) -> Path:
    return markdown_path.with_suffix(".html")


def _slug(text: str, fallback: str) -> str:
    ascii_slug = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return ascii_slug or fallback


def _section_anchor(text: str, fallback: str) -> str:
    for known, anchor in SECTION_ANCHORS.items():
        if known in text:
            return anchor
    return _slug(text, fallback)


def _linkify_escaped(text: str) -> str:
    pattern = re.compile(r"(https?://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+)")

    def replace(match: re.Match[str]) -> str:
        url = match.group(1).rstrip(".,，。)")
        suffix = match.group(1)[len(url) :]
        return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{url}</a>{suffix}'

    return pattern.sub(replace, text)


def _inline(text: str) -> str:
    return _linkify_escaped(html.escape(text, quote=False))


def _extract_title(markdown: str, source_name: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return source_name or "Hermes P7+ Daily Training"


def _extract_case_names(markdown: str) -> list[str]:
    names = re.findall(r"^Case 名称：\s*(.+)$", markdown, flags=re.M)
    if names:
        return [name.strip() for name in names[:3]]
    return [f"Case {index}" for index in range(1, markdown.count("【Case】") + 1)]


def _extract_totals(markdown: str) -> list[str]:
    return re.findall(r"^总分：\s*(\d+\s*/\s*100)", markdown, flags=re.M)


def _source_channel_status(markdown: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    lines = markdown.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != "| 来源通道 | 状态 | 用途 | 限制与降级处理 |":
            continue
        for row in lines[index + 2 :]:
            if not row.strip().startswith("|"):
                break
            cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
            if len(cells) >= 2:
                rows.append((cells[0], cells[1]))
        break
    return rows


def _build_nav(markdown: str, case_names: list[str]) -> str:
    section_links = []
    for title in SECTION_TITLES:
        if title in markdown:
            section_links.append(f'<a href="#{SECTION_ANCHORS[title]}">{html.escape(title)}</a>')

    case_links = [
        f'<a href="#case-{index}">Case {index}: {html.escape(name)}</a>'
        for index, name in enumerate(case_names, start=1)
    ]
    return "\n".join(
        [
            '<nav class="side-nav" aria-label="阅读导航">',
            "<strong>阅读导航</strong>",
            *section_links,
            '<span class="nav-label">深度 case</span>',
            *case_links,
            "</nav>",
        ]
    )


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


def _render_markdown_body(markdown: str, case_names: list[str]) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    case_index = 0
    open_case = False

    def flush_paragraph() -> None:
        if paragraph:
            out.append("<p>" + "<br>".join(_inline(line) for line in paragraph) + "</p>")
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
            level = min(len(hashes), 4)
            title_text = text.strip()
            anchor = _section_anchor(title_text, f"section-{index}")
            out.append(f'<h{level} id="{anchor}">{_inline(title_text)}</h{level}>')
            index += 1
            continue

        if stripped == "【Case】":
            flush_paragraph()
            if open_case:
                out.append("</div></details>")
            case_index += 1
            name = case_names[case_index - 1] if case_index - 1 < len(case_names) else f"Case {case_index}"
            out.append(
                f'<details class="case-panel" id="case-{case_index}" open>'
                f'<summary><span>Case {case_index}</span><strong>{html.escape(name)}</strong></summary><div class="case-body">'
            )
            open_case = True
            index += 1
            continue

        if stripped.startswith("【") and stripped.endswith("】"):
            flush_paragraph()
            out.append(f'<h3 class="bracket-heading">{_inline(stripped)}</h3>')
            index += 1
            continue

        if stripped.startswith("- "):
            flush_paragraph()
            items = []
            while index < len(lines) and lines[index].strip().startswith("- "):
                items.append(lines[index].strip()[2:])
                index += 1
            out.append("<ul>" + "".join(f"<li>{_inline(item)}</li>" for item in items) + "</ul>")
            continue

        if re.match(r"^\d+\.\s+", stripped):
            flush_paragraph()
            out.append(f'<p class="numbered">{_inline(stripped)}</p>')
            index += 1
            continue

        paragraph.append(line)
        index += 1

    flush_paragraph()
    if open_case:
        out.append("</div></details>")
    return "\n".join(out)


def _styles() -> str:
    return """
    :root {
      --bg: #f6f8fb;
      --panel: #ffffff;
      --ink: #172033;
      --muted: #5b667a;
      --line: #d9e0ea;
      --blue: #2364d8;
      --green: #0f766e;
      --amber: #b7791f;
      --red: #b42318;
      --violet: #6d5bd0;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      color: var(--ink);
      background: var(--bg);
      font: 16px/1.72 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    a { color: var(--blue); text-decoration-thickness: 1px; text-underline-offset: 3px; }
    .layout { display: grid; grid-template-columns: minmax(220px, 280px) minmax(0, 1fr); gap: 28px; max-width: 1440px; margin: 0 auto; padding: 28px; }
    .side-nav {
      position: sticky; top: 20px; align-self: start; max-height: calc(100vh - 40px); overflow: auto;
      background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 16px;
    }
    .side-nav strong { display: block; margin-bottom: 10px; font-size: 14px; }
    .side-nav a, .nav-label { display: block; padding: 7px 8px; border-radius: 6px; color: var(--ink); text-decoration: none; font-size: 14px; }
    .side-nav a:hover { background: #eef4ff; color: var(--blue); }
    .nav-label { margin-top: 10px; color: var(--muted); font-weight: 700; }
    main { min-width: 0; }
    .hero {
      background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 24px;
      margin-bottom: 18px;
    }
    .hero h1 { margin: 0 0 10px; font-size: 30px; line-height: 1.2; letter-spacing: 0; }
    .hero p { margin: 0; color: var(--muted); }
    .stat-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin-top: 18px; }
    .stat { border: 1px solid var(--line); border-radius: 8px; padding: 12px; background: #fbfcff; }
    .stat small { display: block; color: var(--muted); }
    .stat strong { font-size: 20px; }
    .source-badges { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
    .badge { border: 1px solid var(--line); border-radius: 999px; padding: 5px 10px; background: #fff; font-size: 13px; color: var(--muted); }
    .badge.ok { color: var(--green); border-color: #9dd7cd; }
    .content {
      background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 26px;
    }
    h1, h2, h3, h4 { line-height: 1.3; letter-spacing: 0; }
    h1 { font-size: 28px; }
    h2 { margin-top: 42px; border-top: 1px solid var(--line); padding-top: 24px; font-size: 24px; }
    h3 { margin-top: 28px; font-size: 19px; }
    .bracket-heading { color: var(--blue); }
    p { margin: 12px 0; }
    ul { margin: 10px 0 14px 22px; padding: 0; }
    li { margin: 5px 0; }
    .numbered { font-weight: 700; color: var(--ink); }
    .table-wrap { overflow: auto; margin: 16px 0; border: 1px solid var(--line); border-radius: 8px; }
    table { width: 100%; border-collapse: collapse; min-width: 720px; background: #fff; }
    th, td { border-bottom: 1px solid var(--line); padding: 9px 10px; vertical-align: top; text-align: left; }
    th { background: #eef2f7; font-size: 13px; color: #29344a; }
    tr:last-child td { border-bottom: 0; }
    .case-panel {
      margin: 24px 0; border: 1px solid var(--line); border-radius: 8px; background: #fcfdff;
    }
    .case-panel summary {
      cursor: pointer; display: flex; gap: 12px; align-items: center; padding: 14px 16px; border-bottom: 1px solid var(--line);
    }
    .case-panel summary span {
      color: #fff; background: var(--blue); border-radius: 999px; padding: 3px 9px; font-size: 13px; font-weight: 700;
    }
    .case-panel summary strong { font-size: 17px; }
    .case-body { padding: 4px 18px 18px; }
    @media (max-width: 900px) {
      .layout { display: block; padding: 14px; }
      .side-nav { position: static; margin-bottom: 14px; max-height: none; }
      .stat-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .content, .hero { padding: 18px; }
      .hero h1 { font-size: 24px; }
    }
    """


def render_html(markdown: str, source_name: str = "") -> str:
    title = _extract_title(markdown, source_name)
    case_names = _extract_case_names(markdown)
    totals = _extract_totals(markdown)
    source_rows = _source_channel_status(markdown)
    nav = _build_nav(markdown, case_names)
    body = _render_markdown_body(markdown, case_names)
    case_count = len(case_names)
    average_score = "-"
    if totals:
        numeric = [int(total.split("/")[0].strip()) for total in totals]
        average_score = f"{round(sum(numeric) / len(numeric), 1)}/100"
    source_badges = "\n".join(
        f'<span class="badge {"ok" if status == "已使用" else ""}">{html.escape(channel)}：{html.escape(status)}</span>'
        for channel, status in source_rows
    )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,">
  <title>{html.escape(title)}</title>
  <style>{_styles()}</style>
</head>
<body>
  <div class="layout">
    {nav}
    <main>
      <header class="hero">
        <h1>{html.escape(title)}</h1>
        <p>从 Markdown 渲染的 Hermes P7+ 阅读页。内容层保持完整，交互层负责降低阅读负担。</p>
        <div class="stat-grid">
          <div class="stat"><small>来源文件</small><strong>{html.escape(source_name or "-")}</strong></div>
          <div class="stat"><small>深度 case</small><strong>{case_count}</strong></div>
          <div class="stat"><small>Insight 均分</small><strong>{average_score}</strong></div>
          <div class="stat"><small>阅读方式</small><strong>先总览再展开</strong></div>
        </div>
        <div class="source-badges">{source_badges}</div>
      </header>
      <article class="content">
        {body}
      </article>
    </main>
  </div>
</body>
</html>
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render Hermes daily training Markdown to HTML.")
    parser.add_argument("markdown", type=Path, help="Path to the daily training Markdown file.")
    parser.add_argument("-o", "--output", type=Path, help="Output HTML path. Defaults to the Markdown path with .html suffix.")
    args = parser.parse_args(argv)

    markdown_path = args.markdown
    output_path = args.output or default_output_path(markdown_path)
    markdown = markdown_path.read_text(encoding="utf-8")
    html_text = render_html(markdown, source_name=markdown_path.name)
    output_path.write_text(html_text, encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
