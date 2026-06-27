#!/usr/bin/env python3
"""Validate Hermes daily reader HTML content completeness.

This checker guards the reader surface after Markdown rendering. The Markdown
validator proves structure; this script proves that required reasoning fields
actually survived into the HTML artifact.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


EXPECTED_EIGHT_QUESTION_FIELDS = (
    "目的",
    "分析方法",
    "为什么用这个方法",
    "推导过程",
    "阶段结论",
    "如何影响下一步",
)


@dataclass
class HtmlValidationResult:
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def _plain_text(fragment: str) -> str:
    without_tags = re.sub(r"<[^>]+>", "", fragment)
    return html.unescape(without_tags).strip()


def validate_html_text(text: str, *, min_cases: int = 3) -> HtmlValidationResult:
    result = HtmlValidationResult()

    case_ids = sorted({int(match) for match in re.findall(r'id="case-(\d+)-eight-q\d+"', text)})
    if len(case_ids) < min_cases:
        result.errors.append(f"Reader HTML requires at least {min_cases} deep cases with 8-question cards; found {len(case_ids)}")

    for case_id in case_ids[:min_cases]:
        cards = re.findall(
            rf'<article class="eight-question-card" id="case-{case_id}-eight-q(\d+)">(.*?)</article>',
            text,
            flags=re.S,
        )
        if len(cards) != 8:
            result.errors.append(f"case-{case_id} requires 8 rendered 8-question cards; found {len(cards)}")

        for question_number, card_html in cards:
            for field_name in EXPECTED_EIGHT_QUESTION_FIELDS:
                field_match = re.search(rf"<dt>{re.escape(field_name)}</dt>\s*<dd>(.*?)</dd>", card_html, flags=re.S)
                if field_match is None:
                    result.errors.append(f"case-{case_id} q{question_number} missing 8-question field: {field_name}")
                    continue
                if not _plain_text(field_match.group(1)):
                    result.errors.append(f"case-{case_id} q{question_number} empty 8-question field: {field_name}")

    if re.search(r'<dl class="eight-question-fields">\s*</dl>', text, flags=re.S):
        result.errors.append("Reader HTML contains an empty 8-question field list")

    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate Hermes reader HTML completeness.")
    parser.add_argument("file", type=Path, help="Reader HTML file to validate")
    parser.add_argument("--min-cases", type=int, default=3, help="Minimum deep cases expected in the reader")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    result = validate_html_text(args.file.read_text(encoding="utf-8"), min_cases=args.min_cases)

    if result.ok:
        print("PASS: Hermes reader HTML contains complete rendered reasoning fields.")
        return 0

    print("FAIL: Hermes reader HTML is incomplete:", file=sys.stderr)
    for error in result.errors:
        print(f"- {error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
