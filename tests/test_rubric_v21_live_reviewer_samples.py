#!/usr/bin/env python3
"""P2B-0 evidence-derived local semantic reviewer tests for V3/V6/V7."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RUBRIC_DIR = ROOT / "docs" / "quality" / "rubric-v2.1"
LIVE_ROOT = RUBRIC_DIR / "generated-replay"
SAMPLES = ("v3_target", "v6_target", "v7_failure")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def live_dir(sample_id: str) -> Path:
    return LIVE_ROOT / f"{sample_id}_live"


class LiveReviewerSamplesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cmd = [
            sys.executable,
            "scripts/run_live_reviewer_generation.py",
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

    def test_live_reviewer_reads_v3_v6_v7_sources(self) -> None:
        expected_sources = {
            "v3_target": {
                "outputs/daily-training/2026-06-25/training-v3.md",
            },
            "v6_target": {
                "outputs/daily-training/2026-06-25/training-v6-raw.md",
                "outputs/daily-training/2026-06-25/training-v6-reader.html",
                "outputs/daily-training/2026-06-25/source-notes-v6.md",
                "outputs/daily-training/2026-06-25/training-v6-quality-report.md",
            },
            "v7_failure": {
                "outputs/daily-training/2026-06-26/training-v7-raw.md",
                "outputs/daily-training/2026-06-26/training-v7-reader.html",
                "outputs/daily-training/2026-06-26/source-notes-v7.md",
                "outputs/daily-training/2026-06-26/v6-v7-regression-audit.md",
            },
        }
        for sample_id in SAMPLES:
            with self.subTest(sample_id=sample_id):
                log = read_yaml(live_dir(sample_id) / "live-generation-log.yaml")
                self.assertEqual(sample_id, log["sample_id"])
                self.assertEqual("local_semantic_reviewer", log["generation_method"])
                self.assertTrue(log["live_semantic_review"])
                self.assertFalse(log["live_llm_review"])
                self.assertFalse(log["recorded_generation"])
                self.assertFalse(log["replay_p1_fixture_payload"])
                self.assertEqual(expected_sources[sample_id], {item["path"] for item in log["input_files"]})

    def test_live_v3_should_pass(self) -> None:
        payload = read_json(live_dir("v3_target") / "live-reviewer-output.json")
        result = read_yaml(live_dir("v3_target") / "live-validator-result.yaml")
        self.assertEqual("PASS", payload["daily_decision"])
        self.assertTrue(payload["publish_allowed"])
        self.assertEqual("PASS", result["schema_and_governance_payload_status"])
        self.assertFalse(result["publish_blocked"])
        self.assertEqual([], result["failure_types"])

    def test_live_v6_should_pass(self) -> None:
        payload = read_json(live_dir("v6_target") / "live-reviewer-output.json")
        result = read_yaml(live_dir("v6_target") / "live-validator-result.yaml")
        self.assertEqual("PASS", payload["daily_decision"])
        self.assertTrue(payload["publish_allowed"])
        self.assertEqual("PASS", result["schema_and_governance_payload_status"])
        self.assertFalse(result["publish_blocked"])
        self.assertEqual([], result["failure_types"])

    def test_live_v7_should_not_pass(self) -> None:
        payload = read_json(live_dir("v7_failure") / "live-reviewer-output.json")
        result = read_yaml(live_dir("v7_failure") / "live-validator-result.yaml")
        self.assertNotEqual("PASS", payload["daily_decision"])
        self.assertFalse(payload["publish_allowed"])
        self.assertTrue(result["publish_blocked"])
        self.assertEqual("FAIL_DAILY", result["governance_decision"])

    def test_live_outputs_preserve_raw_response(self) -> None:
        expected_files = {
            "live-reviewer-output.json",
            "live-claim-evidence-map.json",
            "live-failure-objects.json",
            "live-generation-log.yaml",
            "live-validator-result.yaml",
            "live-vs-recorded-diff.yaml",
            "raw-reviewer-response.json",
        }
        for sample_id in SAMPLES:
            with self.subTest(sample_id=sample_id):
                existing = {path.name for path in live_dir(sample_id).iterdir() if path.is_file()}
                self.assertTrue(expected_files.issubset(existing))
                raw = read_json(live_dir(sample_id) / "raw-reviewer-response.json")
                self.assertEqual(sample_id, raw["sample_id"])
                self.assertIn("reviewer_prompt", raw)
                self.assertIn("semantic_findings", raw)
                self.assertIn("source_files", raw)

    def test_live_generation_logs_include_hashes(self) -> None:
        for sample_id in SAMPLES:
            with self.subTest(sample_id=sample_id):
                log = read_yaml(live_dir(sample_id) / "live-generation-log.yaml")
                self.assertGreaterEqual(len(log["input_files"]), 1)
                for source in log["input_files"]:
                    self.assertGreater(source["bytes"], 0)
                    self.assertRegex(source["sha256"], r"^[0-9a-f]{64}$")
                    self.assertEqual((ROOT / source["path"]).stat().st_size, source["bytes"])

    def test_live_good_samples_do_not_depend_on_self_review_scores(self) -> None:
        for sample_id in ("v3_target", "v6_target"):
            with self.subTest(sample_id=sample_id):
                raw = read_json(live_dir(sample_id) / "raw-reviewer-response.json")
                log = read_yaml(live_dir(sample_id) / "live-generation-log.yaml")
                self.assertEqual(
                    "self_review_is_subject_not_authority",
                    raw["self_review_policy"]["rule_id"],
                )
                self.assertTrue(raw["self_review_policy"]["ignored_as_release_evidence"])
                self.assertTrue(log["self_review_policy"]["ignored_as_release_evidence"])
                self.assertEqual("evidence_derived_semantic_sections", raw["release_decision"]["basis"])

    def test_live_v7_failure_types_overlap_recorded(self) -> None:
        result = read_yaml(live_dir("v7_failure") / "live-validator-result.yaml")
        diff = read_yaml(live_dir("v7_failure") / "live-vs-recorded-diff.yaml")
        required = {
            "DISCONNECTED_8Q_CHAIN",
            "BOILERPLATE_REASONING",
            "CASE_DEPTH_IMBALANCE",
            "REVIEW_EVIDENCE_INVALID",
        }
        self.assertGreaterEqual(len(required & set(result["failure_types"])), 2)
        self.assertTrue(required & set(diff["failure_type_overlap"]))
        self.assertTrue(result["failure_categories"]["content_quality_failure"])

    def test_live_vs_recorded_diff_for_each_sample(self) -> None:
        for sample_id in SAMPLES:
            with self.subTest(sample_id=sample_id):
                diff = read_yaml(live_dir(sample_id) / "live-vs-recorded-diff.yaml")
                self.assertEqual(sample_id, diff["sample_id"])
                self.assertTrue(diff["compared_to_recorded_fixture"])
                self.assertFalse(diff["used_recorded_payload_for_generation"])
                self.assertIn("daily_decision_match", diff)
                self.assertIn("publish_allowed_match", diff)
                self.assertEqual({"case_id", "live", "recorded", "matches"}, set(diff["case_decision_diff"][0]))
                self.assertIn("failure_type_overlap", diff)
                self.assertIn("caps_applied_match", diff)

    def test_report_states_boundaries(self) -> None:
        report = (RUBRIC_DIR / "live-reviewer-samples-report.md").read_text(encoding="utf-8")
        self.assertIn("local semantic reviewer", report)
        self.assertIn("not a live LLM reviewer", report)
        self.assertIn("does not prove cross-date generalization", report)
        self.assertIn("P2B", report)

    def test_p1_and_p2a_baselines_still_pass(self) -> None:
        cmd = [
            sys.executable,
            "-m",
            "unittest",
            "tests.test_rubric_v21_governance",
            "tests.test_rubric_v21_adversarial",
            "tests.test_rubric_v21_anchor_quality",
            "tests.test_rubric_v21_calibration_replay",
            "tests.test_rubric_v21_reviewer_generator",
            "tests.test_rubric_v21_live_reviewer_v7",
        ]
        result = subprocess.run(
            cmd,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertIn("Ran 90 tests", result.stdout)
        self.assertIn("OK", result.stdout)


if __name__ == "__main__":
    unittest.main()
