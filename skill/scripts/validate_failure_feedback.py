#!/usr/bin/env python3
"""Validate Hermes failure feedback loop records."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_RECORD_MARKERS = (
    "【失败编号】",
    "【问题现象】",
    "【用户影响】",
    "【根因归类】",
    "【根因判断】",
    "【回流动作】",
    "【规则回流】",
    "【测试回流】",
    "【门禁处理】",
    "【失败处理策略】",
    "【复测证据】",
    "【验收状态】",
    "【下次遇到同类问题】",
)

REQUIRED_V7_TERMS = (
    "V7 内容退坡与网页空壳回流样本",
    "高分但内容浅",
    "模板套话重复",
    "8 问推理为空壳",
    "validate_hermes_output.py",
    "validate_training_reader_html.py",
    "test_hermes_output_validator.py",
    "test_render_training_reader_html.py",
    "test_failure_feedback_loop.py",
)


class FeedbackValidationResult:
    def __init__(self) -> None:
        self.errors: list[str] = []

    @property
    def ok(self) -> bool:
        return not self.errors


def _record_blocks(text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"^##\s+(.+)$", text, flags=re.M))
    blocks: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks.append((match.group(1).strip(), text[start:end].strip()))
    return blocks


def validate_text(text: str) -> FeedbackValidationResult:
    result = FeedbackValidationResult()
    blocks = _record_blocks(text)
    if not blocks:
        result.errors.append("Failure feedback registry requires at least one ## record")
        return result

    for title, block in blocks:
        missing = [marker for marker in REQUIRED_RECORD_MARKERS if marker not in block]
        for marker in missing:
            result.errors.append(f"{title} missing required marker: {marker.strip('【】')}")

        unresolved_marker = "TO" + "DO"
        if "待补" in block or unresolved_marker in block:
            result.errors.append(f"{title} contains unresolved placeholder text")

        if "PASS" not in block:
            result.errors.append(f"{title} must record PASS/FAIL verification status")

    if "V7 内容退坡与网页空壳回流样本" not in text:
        result.errors.append("Failure feedback registry must include the V7 regression sample")
    else:
        for term in REQUIRED_V7_TERMS:
            if term not in text:
                result.errors.append(f"V7 regression sample missing required evidence: {term}")

    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate Hermes failure feedback registry.")
    parser.add_argument("file", type=Path, help="Failure feedback Markdown registry")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    result = validate_text(args.file.read_text(encoding="utf-8"))
    if result.ok:
        print("PASS: Hermes failure feedback registry is complete.")
        return 0

    print("FAIL: Hermes failure feedback registry is incomplete:", file=sys.stderr)
    for error in result.errors:
        print(f"- {error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
