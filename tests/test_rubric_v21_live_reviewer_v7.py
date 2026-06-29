#!/usr/bin/env python3
"""P2B-0 evidence-derived local semantic reviewer tests for V7."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RUBRIC_DIR = ROOT / "docs" / "quality" / "rubric-v2.1"
LIVE_DIR = RUBRIC_DIR / "generated-replay" / "v7_failure_live"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class LiveReviewerV7Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cmd = [
            sys.executable,
            "scripts/run_live_reviewer_generation_v7.py",
            "--project-root",
            str(ROOT),
        ]
        cls.process = subprocess.run(
            cmd,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if cls.process.returncode != 0:
            raise AssertionError(cls.process.stdout)

    def test_live_outputs_exist_and_keep_raw_response(self) -> None:
        expected = [
            "live-reviewer-output.json",
            "live-claim-evidence-map.json",
            "live-failure-objects.json",
            "live-generation-log.yaml",
            "live-validator-result.yaml",
            "live-vs-recorded-diff.yaml",
            "live-reviewer-generation-report.md",
            "raw-reviewer-response.json",
        ]
        for name in expected:
            with self.subTest(name=name):
                self.assertTrue((LIVE_DIR / name).is_file(), name)

    def test_live_generation_reads_real_v7_sources_not_recorded_payload(self) -> None:
        log = read_yaml(LIVE_DIR / "live-generation-log.yaml")
        self.assertEqual("v7_failure", log["sample_id"])
        self.assertEqual("local_semantic_reviewer", log["generation_method"])
        self.assertTrue(log["live_semantic_review"])
        self.assertFalse(log["recorded_generation"])
        self.assertFalse(log["replay_p1_fixture_payload"])
        self.assertTrue(log["not_stability_claim"])
        source_paths = {source["path"] for source in log["input_files"]}
        self.assertEqual(
            {
                "outputs/daily-training/2026-06-26/training-v7-raw.md",
                "outputs/daily-training/2026-06-26/training-v7-reader.html",
                "outputs/daily-training/2026-06-26/source-notes-v7.md",
                "outputs/daily-training/2026-06-26/v6-v7-regression-audit.md",
            },
            source_paths,
        )
        for source in log["input_files"]:
            self.assertGreater(source["bytes"], 0)
            self.assertRegex(source["sha256"], r"^[0-9a-f]{64}$")

    def test_live_v7_must_not_pass(self) -> None:
        payload = read_json(LIVE_DIR / "live-reviewer-output.json")
        result = read_yaml(LIVE_DIR / "live-validator-result.yaml")
        self.assertIn(payload["daily_decision"], {"FAIL_DAILY", "PUBLISH_BLOCK", "REVIEW"})
        self.assertFalse(payload["publish_allowed"])
        self.assertNotEqual("PASS", payload["daily_decision"])
        self.assertFalse(result["publish_allowed"])
        self.assertIn(result["governance_decision"], {"FAIL_DAILY", "PUBLISH_BLOCK", "REVIEW"})

    def test_live_payload_runs_existing_governance_validator(self) -> None:
        result = read_yaml(LIVE_DIR / "live-validator-result.yaml")
        self.assertEqual("PASS", result["schema_and_governance_payload_status"])
        self.assertEqual([], result["reviewer_errors"])
        self.assertEqual([], result["claim_evidence_map_errors"])
        self.assertEqual([], result["failure_object_errors"])
        self.assertTrue(result["publish_blocked"])

    def test_live_reviewer_identifies_content_quality_problem(self) -> None:
        result = read_yaml(LIVE_DIR / "live-validator-result.yaml")
        self.assertTrue(result["failure_categories"]["content_quality_failure"])
        self.assertTrue(
            {
                "EMPTY_8Q_REASONING",
                "DISCONNECTED_8Q_CHAIN",
                "BOILERPLATE_REASONING",
                "CASE_DEPTH_IMBALANCE",
                "REVIEW_EVIDENCE_INVALID",
            }
            & set(result["failure_types"])
        )

    def test_live_reviewer_distinguishes_failure_categories(self) -> None:
        result = read_yaml(LIVE_DIR / "live-validator-result.yaml")
        self.assertEqual(
            {
                "content_quality_failure",
                "html_rendering_integrity_failure",
                "source_evidence_failure",
                "self_review_inflation",
            },
            set(result["failure_categories"]),
        )
        self.assertIsInstance(result["failure_categories"]["html_rendering_integrity_failure"], bool)
        self.assertIsInstance(result["failure_categories"]["source_evidence_failure"], bool)

    def test_raw_response_contains_source_based_reasoning(self) -> None:
        raw = read_json(LIVE_DIR / "raw-reviewer-response.json")
        self.assertIn("reviewer_prompt", raw)
        self.assertIn("source_evidence", raw)
        self.assertIn("semantic_findings", raw)
        evidence_text = json.dumps(raw["source_evidence"], ensure_ascii=False)
        self.assertIn("V7 cannot be honestly called", evidence_text)
        self.assertIn("Case 2 8-question section", evidence_text)
        self.assertIn("self-scores 97/100", evidence_text)

    def test_live_vs_recorded_diff_explains_differences(self) -> None:
        diff = read_yaml(LIVE_DIR / "live-vs-recorded-diff.yaml")
        self.assertEqual("v7_failure", diff["sample_id"])
        self.assertTrue(diff["compared_to_recorded_fixture"])
        self.assertFalse(diff["used_recorded_payload_for_generation"])
        self.assertTrue(diff["daily_decision_match"])
        self.assertTrue(diff["publish_allowed_match"])
        self.assertTrue(
            {
                "EMPTY_8Q_REASONING",
                "DISCONNECTED_8Q_CHAIN",
                "BOILERPLATE_REASONING",
                "CASE_DEPTH_IMBALANCE",
                "REVIEW_EVIDENCE_INVALID",
            }
            & set(diff["failure_type_overlap"])
        )
        self.assertGreaterEqual(len(diff["explanations"]), 1)

    def test_p1_and_recorded_81_tests_must_still_pass(self) -> None:
        cmd = [
            sys.executable,
            "-m",
            "unittest",
            "tests.test_rubric_v21_governance",
            "tests.test_rubric_v21_adversarial",
            "tests.test_rubric_v21_anchor_quality",
            "tests.test_rubric_v21_calibration_replay",
            "tests.test_rubric_v21_reviewer_generator",
        ]
        result = subprocess.run(
            cmd,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertIn("Ran 81 tests", result.stdout)
        self.assertIn("OK", result.stdout)


if __name__ == "__main__":
    unittest.main()
