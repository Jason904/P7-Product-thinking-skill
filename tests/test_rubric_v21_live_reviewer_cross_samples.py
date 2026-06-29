#!/usr/bin/env python3
"""P2B-2 cross-date / cross-topic real sample replay tests."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RUBRIC_DIR = ROOT / "docs" / "quality" / "rubric-v2.1"
CROSS_ROOT = RUBRIC_DIR / "generated-replay" / "cross-samples"
SCRIPT_PATH = ROOT / "scripts" / "run_live_reviewer_cross_samples.py"

SAMPLES = (
    "2026_06_25_training_v2",
    "2026_06_25_training_v3",
    "2026_06_25_training_v4_raw",
    "2026_06_25_training_v5_raw",
    "2026_06_25_training_v6_raw",
    "2026_06_26_training_v7_raw",
)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def sample_dir(sample_id: str) -> Path:
    return CROSS_ROOT / sample_id


class P2B2CrossSampleTests(unittest.TestCase):
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

    def test_each_cross_sample_has_required_outputs(self) -> None:
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
        self.assertGreaterEqual(len(SAMPLES), 5)
        self.assertLessEqual(len(SAMPLES), 10)
        for sample_id in SAMPLES:
            with self.subTest(sample_id=sample_id):
                existing = {path.name for path in sample_dir(sample_id).iterdir() if path.is_file()}
                self.assertTrue(expected.issubset(existing), expected - existing)

    def test_source_manifests_are_real_samples_and_trace_sources(self) -> None:
        dates = set()
        for sample_id in SAMPLES:
            with self.subTest(sample_id=sample_id):
                manifest = read_yaml(sample_dir(sample_id) / "source-manifest.yaml")
                dates.add(manifest["date"])
                self.assertTrue(manifest["real_sample"])
                self.assertFalse(manifest["synthetic_fixture"])
                self.assertIn(manifest["expected_class"], {"PASS", "REVIEW", "FAIL"})
                self.assertTrue(manifest["why_selected"])
                self.assertTrue(manifest["sources"]["training_markdown"]["exists"])
                self.assertTrue((ROOT / manifest["sources"]["training_markdown"]["path"]).is_file())
                self.assertFalse(manifest["live_llm_review"])
                self.assertTrue(manifest["local_semantic_reviewer"])
                self.assertTrue(manifest["not_p2c"])
        self.assertEqual({"2026-06-25", "2026-06-26"}, dates)

    def test_date_coverage_shortfall_is_explicit_not_faked(self) -> None:
        report = (RUBRIC_DIR / "live-reviewer-cross-sample-report.md").read_text(encoding="utf-8")
        self.assertIn("Real sample count: 6", report)
        self.assertIn("Date coverage status: INSUFFICIENT_REAL_HISTORY", report)
        self.assertIn("No synthetic fixture is used to pretend third-date coverage", report)
        self.assertIn("Third-date coverage requires additional real historical daily-training output", report)

    def test_bad_samples_must_not_pass(self) -> None:
        for sample_id in ("2026_06_25_training_v2", "2026_06_26_training_v7_raw"):
            with self.subTest(sample_id=sample_id):
                manifest = read_yaml(sample_dir(sample_id) / "source-manifest.yaml")
                payload = read_json(sample_dir(sample_id) / "live-reviewer-output.json")
                diff = read_yaml(sample_dir(sample_id) / "live-vs-expected-diff.yaml")
                self.assertEqual("FAIL", manifest["expected_class"])
                self.assertNotEqual("PASS", payload["daily_decision"])
                self.assertFalse(payload["publish_allowed"])
                self.assertEqual("MATCH", diff["status"])

    def test_good_samples_must_not_hard_fail(self) -> None:
        for sample_id in (
            "2026_06_25_training_v3",
            "2026_06_25_training_v4_raw",
            "2026_06_25_training_v5_raw",
            "2026_06_25_training_v6_raw",
        ):
            with self.subTest(sample_id=sample_id):
                manifest = read_yaml(sample_dir(sample_id) / "source-manifest.yaml")
                payload = read_json(sample_dir(sample_id) / "live-reviewer-output.json")
                diff = read_yaml(sample_dir(sample_id) / "live-vs-expected-diff.yaml")
                self.assertEqual("PASS", manifest["expected_class"])
                self.assertNotIn(payload["daily_decision"], {"FAIL_DAILY", "PUBLISH_BLOCK", "REPLACE_CASE"})
                self.assertEqual("MATCH", diff["status"])

    def test_review_samples_are_reported_even_when_none_present(self) -> None:
        report = (RUBRIC_DIR / "live-reviewer-cross-sample-report.md").read_text(encoding="utf-8")
        self.assertIn("## REVIEW / REWRITE Hold Samples", report)
        for sample_id in SAMPLES:
            diff = read_yaml(sample_dir(sample_id) / "live-vs-expected-diff.yaml")
            if diff["expected_class"] == "REVIEW":
                self.assertFalse(diff["actual_publish_allowed"])
                self.assertNotEqual("PASS", diff["actual_daily_decision"])

    def test_failure_origin_distinguishes_content_quality_and_input_missing(self) -> None:
        v2 = read_yaml(sample_dir("2026_06_25_training_v2") / "live-validator-result.yaml")
        self.assertTrue(v2["cross_sample"]["failure_origin"]["content_quality"])
        self.assertFalse(v2["cross_sample"]["failure_origin"]["input_missing"])

        v7 = read_yaml(sample_dir("2026_06_26_training_v7_raw") / "live-validator-result.yaml")
        self.assertTrue(v7["cross_sample"]["failure_origin"]["content_quality"])
        self.assertTrue(v7["cross_sample"]["failure_origin"]["self_review_inflation"])

    def test_raw_html_is_not_misused_as_reader_html(self) -> None:
        for sample_id in ("2026_06_25_training_v4_raw", "2026_06_25_training_v5_raw"):
            with self.subTest(sample_id=sample_id):
                manifest = read_yaml(sample_dir(sample_id) / "source-manifest.yaml")
                self.assertFalse(manifest["sources"]["reader_html"]["exists"])
                self.assertTrue(manifest["available_but_not_used"]["raw_html_not_reader"]["exists"])
                self.assertIn("not the structured reader HTML", manifest["available_but_not_used"]["raw_html_not_reader"]["reason_not_used"])

    def test_no_release_depends_on_self_review_or_historical_audit_authority(self) -> None:
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

    def test_report_lists_pass_review_fail_and_boundaries(self) -> None:
        report = (RUBRIC_DIR / "live-reviewer-cross-sample-report.md").read_text(encoding="utf-8")
        self.assertIn("## PASS Samples", report)
        self.assertIn("## REVIEW / REWRITE Hold Samples", report)
        self.assertIn("## FAIL Samples", report)
        self.assertIn("local semantic reviewer", report)
        self.assertIn("Not a live LLM reviewer", report)
        self.assertIn("Does not enter P2C", report)
        self.assertIn("Self-review tables and historical audit reports are evidence inputs only", report)


if __name__ == "__main__":
    unittest.main()
