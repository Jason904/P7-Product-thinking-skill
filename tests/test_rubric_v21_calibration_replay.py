#!/usr/bin/env python3
"""Calibration replay tests for Rubric v2.1 governance fixtures."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RUBRIC_DIR = ROOT / "docs" / "quality" / "rubric-v2.1"
FIXTURE_DIR = RUBRIC_DIR / "fixtures" / "calibration"


def load_validator():
    path = RUBRIC_DIR / "rubric_governance_validator.py"
    spec = importlib.util.spec_from_file_location("rubric_governance_validator", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class RubricV21CalibrationReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()

    def fixture(self, sample_id: str) -> dict:
        sample_dir = FIXTURE_DIR / sample_id
        manifest = read_yaml(sample_dir / "source-manifest.yaml")
        reviewer = read_json(sample_dir / "reviewer-output.json")
        claim_map = read_json(sample_dir / "claim-evidence-map.json")
        failure_file = sample_dir / "failure-objects.json"
        failures = read_json(failure_file) if failure_file.exists() else []
        reviewer_errors = self.validator.validate_reviewer_output(reviewer, RUBRIC_DIR)
        claim_errors = self.validator.validate_claim_evidence_map(claim_map, RUBRIC_DIR)
        failure_errors = []
        for index, failure in enumerate(failures):
            failure_errors.extend(
                f"failure_objects[{index}].{error}"
                for error in self.validator.validate_failure_object(failure, RUBRIC_DIR)
            )
        return {
            "dir": sample_dir,
            "manifest": manifest,
            "reviewer": reviewer,
            "claim_map": claim_map,
            "failures": failures,
            "reviewer_errors": reviewer_errors,
            "claim_errors": claim_errors,
            "failure_errors": failure_errors,
        }

    def assert_real_sources_exist(self, fixture: dict) -> None:
        manifest = fixture["manifest"]
        self.assertEqual("real", manifest["sample_type"])
        self.assertFalse(manifest["synthetic_fixture"])
        markdown = manifest.get("source_markdown")
        self.assertTrue(markdown)
        self.assertTrue((ROOT / markdown).is_file(), markdown)
        html = manifest.get("source_html")
        if html:
            self.assertTrue((ROOT / html).is_file(), html)
        for source_record in manifest.get("source_records") or []:
            self.assertTrue((ROOT / source_record).is_file(), source_record)

    def assert_synthetic_marked(self, fixture: dict) -> None:
        manifest = fixture["manifest"]
        self.assertEqual("synthetic", manifest["sample_type"])
        self.assertTrue(manifest["synthetic_fixture"])
        self.assertTrue(manifest["not_real_sample_replay"])

    def failure_types(self, fixture: dict) -> set[str]:
        return {failure["failure_type"] for failure in fixture["failures"]}

    def test_v3_target_replay_should_pass(self) -> None:
        fx = self.fixture("v3_target")
        self.assert_real_sources_exist(fx)
        self.assertEqual([], fx["reviewer_errors"])
        self.assertEqual([], fx["claim_errors"])
        self.assertEqual([], fx["failure_errors"])
        self.assertEqual("PASS", fx["reviewer"]["daily_decision"])
        self.assertTrue(fx["reviewer"]["publish_allowed"])

    def test_v6_target_replay_should_pass(self) -> None:
        fx = self.fixture("v6_target")
        self.assert_real_sources_exist(fx)
        self.assertEqual([], fx["reviewer_errors"])
        self.assertEqual([], fx["claim_errors"])
        self.assertEqual([], fx["failure_errors"])
        self.assertEqual("PASS", fx["reviewer"]["daily_decision"])
        self.assertTrue(fx["reviewer"]["publish_allowed"])
        self.assertEqual({"G6": "PASS", "G7": "PASS", "G8": "PASS"}, fx["reviewer"]["gate_statuses"])

    def test_v7_failure_replay_should_fail(self) -> None:
        fx = self.fixture("v7_failure")
        self.assert_real_sources_exist(fx)
        self.assertIn(fx["reviewer"]["daily_decision"], {"FAIL_DAILY", "PUBLISH_BLOCK"})
        self.assertFalse(fx["reviewer"]["publish_allowed"])
        self.assertTrue(fx["reviewer_errors"], "V7 must expose validator-visible errors")
        self.assertEqual([], fx["claim_errors"])
        self.assertEqual([], fx["failure_errors"])
        self.assertTrue(
            {
                "EMPTY_8Q_REASONING",
                "DISCONNECTED_8Q_CHAIN",
                "BOILERPLATE_REASONING",
                "CASE_DEPTH_IMBALANCE",
                "REVIEW_EVIDENCE_INVALID",
            }.issubset(self.failure_types(fx))
        )

    def test_empty_8q_replay_should_fail(self) -> None:
        fx = self.fixture("empty_8q")
        self.assert_synthetic_marked(fx)
        self.assertIn(fx["reviewer"]["daily_decision"], {"FAIL_DAILY", "PUBLISH_BLOCK"})
        self.assertFalse(fx["reviewer"]["publish_allowed"])
        self.assertEqual([], fx["claim_errors"])
        self.assertEqual([], fx["failure_errors"])
        self.assertTrue({"EMPTY_8Q_REASONING", "INCOMPLETE_8Q_FIELDS"}.issubset(self.failure_types(fx)))
        case_a = fx["reviewer"]["case_reviews"][0]
        eightq = next(item for item in case_a["item_reviews"] if item["item_id"] == "thinking.eightq_reasoning_validity")
        self.assertEqual(0, eightq["final_score"])
        self.assertEqual("MISSING", eightq["item_evidence_sufficiency"])

    def test_news_summary_replay_should_apply_global_cap_70(self) -> None:
        fx = self.fixture("news_summary")
        self.assert_synthetic_marked(fx)
        self.assertNotEqual("PASS", fx["reviewer"]["daily_decision"])
        self.assertFalse(fx["reviewer"]["publish_allowed"])
        self.assertEqual([], fx["claim_errors"])
        self.assertEqual([], fx["failure_errors"])
        self.assertIn("NEWS_SUMMARY_ONLY", self.failure_types(fx))
        capped_case = fx["reviewer"]["case_reviews"][0]
        self.assertEqual(70, capped_case["case_global_cap_applied"]["max_allowed_score"])
        self.assertLessEqual(capped_case["case_final_total"], 70)

    def test_inflated_self_review_replay_should_fail_or_review(self) -> None:
        fx = self.fixture("inflated_self_review")
        self.assert_synthetic_marked(fx)
        self.assertIn(fx["reviewer"]["daily_decision"], {"FAIL_DAILY", "PUBLISH_BLOCK", "REVIEW"})
        self.assertFalse(fx["reviewer"]["publish_allowed"])
        self.assertFalse(fx["reviewer"]["reviewer_output_valid"])
        self.assertEqual([], fx["claim_errors"])
        self.assertEqual([], fx["failure_errors"])
        self.assertTrue({"SELF_REVIEW_INFLATION", "REVIEW_EVIDENCE_INVALID"}.issubset(self.failure_types(fx)))

    def test_human_preference_replay_should_require_user_review(self) -> None:
        fx = self.fixture("human_preference")
        self.assert_synthetic_marked(fx)
        self.assertEqual([], fx["reviewer_errors"])
        self.assertEqual([], fx["claim_errors"])
        self.assertEqual([], fx["failure_errors"])
        self.assertEqual("USER_REVIEW_REQUIRED", fx["reviewer"]["daily_decision"])
        self.assertFalse(fx["reviewer"]["publish_allowed"])


if __name__ == "__main__":
    unittest.main()
