#!/usr/bin/env python3
"""P2B-0 evidence-derived local semantic reviewer tests."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RUBRIC_DIR = ROOT / "docs" / "quality" / "rubric-v2.1"
LIVE_ROOT = RUBRIC_DIR / "generated-replay"
SCRIPT_PATH = ROOT / "scripts" / "run_live_reviewer_generation.py"


def load_reviewer_module():
    spec = importlib.util.spec_from_file_location("run_live_reviewer_generation", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class P2B0LocalReviewerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_reviewer_module()
        standard = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--project-root",
                str(ROOT),
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if standard.returncode != 0:
            raise AssertionError(standard.stdout)
        no_audit = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--project-root",
                str(ROOT),
                "--sample-id",
                "v7_failure",
                "--no-audit",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if no_audit.returncode != 0:
            raise AssertionError(no_audit.stdout)

    def test_live_decision_should_be_derived_not_config_driven(self) -> None:
        config = copy.deepcopy(self.module.SAMPLE_CONFIGS["v3_target"])
        self.assertNotIn("decision", config)
        self.assertNotIn("publish_allowed", config)
        config["expected_decision"] = "FAIL_DAILY"
        config["expected_publish_allowed"] = False
        sources = self.module.read_sources(ROOT, config["sources"])
        anchors = read_yaml(RUBRIC_DIR / "rubric-score-anchors.yaml")["items"]
        raw = self.module.build_raw_response("v3_target", config, sources, no_audit=False)
        payload = self.module.build_reviewer_output("v3_target", config, raw, anchors)
        self.assertEqual("PASS", payload["daily_decision"])
        self.assertTrue(payload["publish_allowed"])
        self.assertEqual("evidence_derived_semantic_sections", raw["release_decision"]["basis"])

    def test_live_validator_result_sample_id_should_not_be_null(self) -> None:
        paths = [
            LIVE_ROOT / "v3_target_live" / "live-validator-result.yaml",
            LIVE_ROOT / "v6_target_live" / "live-validator-result.yaml",
            LIVE_ROOT / "v7_failure_live" / "live-validator-result.yaml",
            LIVE_ROOT / "v7_failure_no_audit_live" / "live-validator-result.yaml",
        ]
        for path in paths:
            with self.subTest(path=path):
                result = read_yaml(path)
                self.assertIsNotNone(result["sample_id"])
                self.assertIn(result["sample_id"], {"v3_target", "v6_target", "v7_failure"})

    def test_live_v3_pass_requires_minimum_semantic_sections(self) -> None:
        raw = read_json(LIVE_ROOT / "v3_target_live" / "raw-reviewer-response.json")
        self.assertTrue(raw["daily_semantic_evidence"]["source_candidate_pool_present"])
        self.assertEqual(3, len(raw["case_semantic_evidence"]))
        for case in raw["case_semantic_evidence"]:
            self.assertEqual(8, case["eightq"]["valid_question_count"])
            self.assertTrue(all(case["required_sections"].values()))

        markdown = (
            ROOT / "outputs/daily-training/2026-06-25/training-v3.md"
        ).read_text(encoding="utf-8")
        damaged = markdown.replace("【PREP 表达版本】", "【PREP 已删除】", 1)
        damaged = damaged.replace("【SCQA 表达版本】", "【SCQA 已删除】", 1)
        analysis = self.module.analyze_training_markdown(damaged)
        case_a = analysis["cases"][0]
        self.assertFalse(case_a["required_sections"]["prep_or_scqa_complete"])
        decision = self.module.derive_case_decision(
            "v3_target",
            "case_a",
            {"case_semantic_evidence": analysis["cases"], "semantic_findings": []},
            read_yaml(RUBRIC_DIR / "rubric-score-anchors.yaml")["items"],
        )
        self.assertNotEqual("PASS", decision)

    def test_live_v6_pass_requires_minimum_semantic_sections(self) -> None:
        raw = read_json(LIVE_ROOT / "v6_target_live" / "raw-reviewer-response.json")
        self.assertTrue(raw["daily_semantic_evidence"]["source_candidate_pool_present"])
        self.assertTrue(raw["daily_semantic_evidence"]["reader_html_complete"])
        self.assertEqual(24, raw["daily_semantic_evidence"]["reader_valid_question_card_count"])
        for case in raw["case_semantic_evidence"]:
            self.assertEqual(8, case["eightq"]["valid_question_count"])
            self.assertTrue(all(case["required_sections"].values()))

        markdown = (
            ROOT / "outputs/daily-training/2026-06-25/training-v6-raw.md"
        ).read_text(encoding="utf-8")
        damaged = markdown.replace("【Case Asset Card】", "【资产卡已删除】", 1)
        analysis = self.module.analyze_training_markdown(damaged)
        case_a = analysis["cases"][0]
        self.assertFalse(case_a["required_sections"]["case_asset_card"])
        decision = self.module.derive_case_decision(
            "v6_target",
            "case_a",
            {"case_semantic_evidence": analysis["cases"], "semantic_findings": []},
            read_yaml(RUBRIC_DIR / "rubric-score-anchors.yaml")["items"],
        )
        self.assertNotEqual("PASS", decision)

    def test_live_v7_no_audit_should_not_pass(self) -> None:
        output = LIVE_ROOT / "v7_failure_no_audit_live"
        payload = read_json(output / "live-reviewer-output.json")
        result = read_yaml(output / "live-validator-result.yaml")
        log = read_yaml(output / "live-generation-log.yaml")
        self.assertNotEqual("PASS", payload["daily_decision"])
        self.assertFalse(payload["publish_allowed"])
        self.assertTrue(result["publish_blocked"])
        self.assertTrue(log["no_audit"])
        self.assertNotIn(
            "outputs/daily-training/2026-06-26/v6-v7-regression-audit.md",
            {item["path"] for item in log["input_files"]},
        )

    def test_live_v7_no_audit_should_report_uncertainty_if_evidence_insufficient(self) -> None:
        output = LIVE_ROOT / "v7_failure_no_audit_live"
        raw = read_json(output / "raw-reviewer-response.json")
        result = read_yaml(output / "live-validator-result.yaml")
        self.assertFalse(raw["audit_used"])
        self.assertTrue(raw["uncertainty_boundary"]["present"])
        self.assertGreater(len(raw["uncertainty_boundary"]["limitations"]), 0)
        self.assertTrue(
            {
                "BOILERPLATE_REASONING",
                "CASE_DEPTH_IMBALANCE",
                "REVIEW_EVIDENCE_INVALID",
            }
            & set(result["failure_types"])
        )

    def test_p1_and_p2a_baselines_still_pass(self) -> None:
        command = [
            sys.executable,
            "-m",
            "unittest",
            "tests.test_rubric_v21_governance",
            "tests.test_rubric_v21_adversarial",
            "tests.test_rubric_v21_anchor_quality",
            "tests.test_rubric_v21_calibration_replay",
            "tests.test_rubric_v21_reviewer_generator",
            "tests.test_rubric_v21_live_reviewer_v7",
            "tests.test_rubric_v21_live_reviewer_samples",
        ]
        result = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertIn("Ran 101 tests", result.stdout)
        self.assertIn("OK", result.stdout)


if __name__ == "__main__":
    unittest.main()
