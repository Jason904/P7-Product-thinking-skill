#!/usr/bin/env python3
"""P2B-3 third-date real sample set tests."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RUBRIC_DIR = ROOT / "docs" / "quality" / "rubric-v2.1"
P2B3_ROOT = RUBRIC_DIR / "generated-replay" / "p2b3-samples"
SCRIPT_PATH = ROOT / "scripts" / "run_live_reviewer_p2b3_samples.py"

SAMPLES = (
    "2026_06_28_training_v8_pass",
    "2026_06_28_training_v8_review_boilerplate",
    "2026_06_28_training_v8_review_method_overlap",
)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def sample_dir(sample_id: str) -> Path:
    return P2B3_ROOT / sample_id


class P2B3ThirdDateSampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        result = subprocess.run(
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
        if result.returncode != 0:
            raise AssertionError(result.stdout)

    def test_each_p2b3_sample_has_required_outputs(self) -> None:
        expected = {
            "raw-reviewer-response.json",
            "live-reviewer-output.json",
            "live-claim-evidence-map.json",
            "live-failure-objects.json",
            "live-generation-log.yaml",
            "live-validator-result.yaml",
            "live-vs-expected-diff.yaml",
            "source-manifest.yaml",
        }
        for sample_id in SAMPLES:
            with self.subTest(sample_id=sample_id):
                existing = {path.name for path in sample_dir(sample_id).iterdir() if path.is_file()}
                self.assertTrue(expected.issubset(existing), expected - existing)

    def test_new_samples_are_real_third_date_not_synthetic_or_p2c(self) -> None:
        dates = set()
        for sample_id in SAMPLES:
            with self.subTest(sample_id=sample_id):
                manifest = read_yaml(sample_dir(sample_id) / "source-manifest.yaml")
                dates.add(manifest["date"])
                self.assertTrue(manifest["real_sample"])
                self.assertFalse(manifest["synthetic_fixture"])
                self.assertTrue(manifest["governance_generated_real_output"])
                self.assertTrue(manifest["local_semantic_reviewer"])
                self.assertFalse(manifest["live_llm_review"])
                self.assertTrue(manifest["not_daily_production_pipeline"])
                self.assertTrue(manifest["not_p2c"])
                self.assertTrue(manifest["sources"]["training_markdown"]["exists"])
                self.assertTrue((ROOT / manifest["sources"]["training_markdown"]["path"]).is_file())
        self.assertEqual({"2026-06-28"}, dates)

    def test_p2b3_adds_third_real_date_when_combined_with_p2b2(self) -> None:
        cross_root = RUBRIC_DIR / "generated-replay" / "cross-samples"
        cross_dates = {
            read_yaml(path)["date"]
            for path in sorted(cross_root.glob("*/source-manifest.yaml"))
            if read_yaml(path)["real_sample"]
        }
        p2b3_dates = {
            read_yaml(sample_dir(sample_id) / "source-manifest.yaml")["date"]
            for sample_id in SAMPLES
        }
        self.assertGreaterEqual(len(cross_dates | p2b3_dates), 3)
        self.assertEqual({"2026-06-25", "2026-06-26", "2026-06-28"}, cross_dates | p2b3_dates)

    def test_pass_sample_is_not_hard_failed(self) -> None:
        payload = read_json(sample_dir("2026_06_28_training_v8_pass") / "live-reviewer-output.json")
        diff = read_yaml(sample_dir("2026_06_28_training_v8_pass") / "live-vs-expected-diff.yaml")
        self.assertEqual("PASS", diff["expected_class"])
        self.assertNotIn(payload["daily_decision"], {"FAIL_DAILY", "PUBLISH_BLOCK", "REPLACE_CASE"})
        self.assertEqual("MATCH", diff["status"])

    def test_two_review_borderline_samples_are_held_not_published(self) -> None:
        review_samples = [
            "2026_06_28_training_v8_review_boilerplate",
            "2026_06_28_training_v8_review_method_overlap",
        ]
        for sample_id in review_samples:
            with self.subTest(sample_id=sample_id):
                manifest = read_yaml(sample_dir(sample_id) / "source-manifest.yaml")
                payload = read_json(sample_dir(sample_id) / "live-reviewer-output.json")
                diff = read_yaml(sample_dir(sample_id) / "live-vs-expected-diff.yaml")
                validator = read_yaml(sample_dir(sample_id) / "live-validator-result.yaml")
                self.assertEqual("REVIEW", manifest["expected_class"])
                self.assertTrue(manifest["why_review_or_borderline"])
                self.assertEqual("REVIEW", payload["daily_decision"])
                self.assertFalse(payload["publish_allowed"])
                self.assertEqual("MATCH", diff["status"])
                self.assertIn("BOILERPLATE_REASONING", validator["failure_types"])
                self.assertIn("REVIEW_EVIDENCE_INVALID", validator["failure_types"])

    def test_boundaries_and_authority_are_explicit(self) -> None:
        report = (RUBRIC_DIR / "live-reviewer-p2b3-sample-report.md").read_text(encoding="utf-8")
        self.assertIn("P2B-3 third-date real sample set", report)
        self.assertIn("local semantic reviewer", report)
        self.assertIn("Not a live LLM reviewer", report)
        self.assertIn("Does not enter P2C", report)
        self.assertIn("Self-review tables and historical audit reports are evidence inputs only", report)
        for sample_id in SAMPLES:
            self.assertIn(sample_id, report)

        for sample_id in SAMPLES:
            with self.subTest(sample_id=sample_id):
                log = read_yaml(sample_dir(sample_id) / "live-generation-log.yaml")
                diff = read_yaml(sample_dir(sample_id) / "live-vs-expected-diff.yaml")
                self.assertFalse(log["live_llm_review"])
                self.assertTrue(log["local_semantic_reviewer"])
                self.assertTrue(log["not_daily_production_pipeline"])
                self.assertTrue(log["not_p2c"])
                self.assertFalse(log["expected_class_used_for_decision"])
                self.assertFalse(log["self_review_used_as_release_authority"])
                self.assertFalse(log["historical_audit_used_as_release_authority"])
                self.assertFalse(diff["self_review_used_as_release_authority"])
                self.assertFalse(diff["historical_audit_used_as_release_authority"])


if __name__ == "__main__":
    unittest.main()
