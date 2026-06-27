#!/usr/bin/env python3
"""Tests for the Hermes failure feedback loop assets."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "skill" / "scripts" / "validate_failure_feedback.py"
FEEDBACK_GUIDE_PATH = ROOT / "skill" / "references" / "failure-feedback.md"
FAILURE_CASES_PATH = ROOT / "skill" / "references" / "failure-cases.md"


def load_feedback_validator():
    spec = importlib.util.spec_from_file_location("validate_failure_feedback", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Cannot import validator at {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FailureFeedbackLoopTests(unittest.TestCase):
    def test_failure_feedback_reference_and_v7_case_exist(self) -> None:
        self.assertTrue(FEEDBACK_GUIDE_PATH.exists(), "failure feedback workflow reference is missing")
        self.assertTrue(FAILURE_CASES_PATH.exists(), "failure case registry is missing")

        guide = FEEDBACK_GUIDE_PATH.read_text(encoding="utf-8")
        cases = FAILURE_CASES_PATH.read_text(encoding="utf-8")

        for term in (
            "失败登记",
            "失败归因",
            "规则回流",
            "测试回流",
            "复测回归",
            "失败处理",
        ):
            self.assertIn(term, guide)

        for term in (
            "V7 内容退坡与网页空壳回流样本",
            "8 问推理为空壳",
            "模板套话重复",
            "高分但内容浅",
            "回流动作",
            "复测证据",
        ):
            self.assertIn(term, cases)

    def test_failure_case_registry_passes_validator(self) -> None:
        validator = load_feedback_validator()
        result = validator.validate_text(FAILURE_CASES_PATH.read_text(encoding="utf-8"))
        self.assertEqual([], result.errors)

    def test_failure_case_validator_rejects_missing_regression_test(self) -> None:
        validator = load_feedback_validator()
        broken = FAILURE_CASES_PATH.read_text(encoding="utf-8").replace("【测试回流】", "【测试遗漏】", 1)
        result = validator.validate_text(broken)
        self.assertTrue(any("测试回流" in error for error in result.errors))

    def test_failure_case_validator_cli_fails_for_incomplete_record(self) -> None:
        validator = load_feedback_validator()
        with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8", delete=False) as fh:
            fh.write("## V7 内容退坡与网页空壳回流样本\n【问题现象】\n只有现象，没有闭环。\n")
            path = Path(fh.name)
        try:
            self.assertEqual(1, validator.main([str(path)]))
        finally:
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
