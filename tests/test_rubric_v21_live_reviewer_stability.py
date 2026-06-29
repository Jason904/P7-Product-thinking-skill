#!/usr/bin/env python3
"""P2B-1 stability / no-audit stress tests for the local semantic reviewer."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RUBRIC_DIR = ROOT / "docs" / "quality" / "rubric-v2.1"
STABILITY_ROOT = RUBRIC_DIR / "generated-replay" / "stability"
SCRIPT_PATH = ROOT / "scripts" / "run_live_reviewer_stability.py"

SCENARIOS = (
    "v7_failure_no_audit_should_not_pass",
    "v7_failure_without_self_review_should_not_pass",
    "v7_failure_without_reader_html_should_not_pass_or_review",
    "v7_failure_without_source_notes_should_not_pass_or_review",
    "v3_without_self_review_should_still_pass_or_review_not_fail",
    "v6_without_quality_report_should_still_pass_or_review_not_fail",
    "case_order_changed_should_not_change_daily_decision",
    "repeated_run_same_input_should_be_deterministic",
)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def scenario_dir(scenario_id: str) -> Path:
    return STABILITY_ROOT / scenario_id


class P2B1StabilityTests(unittest.TestCase):
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

    def test_each_stability_fixture_outputs_required_files(self) -> None:
        expected = {
            "raw-reviewer-response.json",
            "live-reviewer-output.json",
            "live-claim-evidence-map.json",
            "live-failure-objects.json",
            "live-generation-log.yaml",
            "live-validator-result.yaml",
            "perturbation-manifest.yaml",
        }
        for scenario_id in SCENARIOS:
            with self.subTest(scenario_id=scenario_id):
                existing = {path.name for path in scenario_dir(scenario_id).iterdir()}
                self.assertTrue(expected.issubset(existing), expected - existing)

    def test_all_stability_fixtures_are_local_not_p1_recorded_or_p2c(self) -> None:
        for scenario_id in SCENARIOS:
            with self.subTest(scenario_id=scenario_id):
                manifest = read_yaml(scenario_dir(scenario_id) / "perturbation-manifest.yaml")
                log = read_yaml(scenario_dir(scenario_id) / "live-generation-log.yaml")
                self.assertFalse(manifest["p1_recorded_payload_used_as_generation"])
                self.assertFalse(manifest["live_llm_review"])
                self.assertTrue(manifest["local_semantic_reviewer"])
                self.assertTrue(manifest["not_p2c"])
                self.assertFalse(log["recorded_generation"])
                self.assertFalse(log["replay_p1_fixture_payload"])
                self.assertFalse(log["live_llm_review"])
                self.assertTrue(log["local_semantic_reviewer"])
                self.assertTrue(log["not_daily_production_pipeline"])
                self.assertTrue(log["not_p2c"])

    def test_every_perturbation_manifest_records_input_changes(self) -> None:
        for scenario_id in SCENARIOS:
            with self.subTest(scenario_id=scenario_id):
                manifest = read_yaml(scenario_dir(scenario_id) / "perturbation-manifest.yaml")
                self.assertGreaterEqual(len(manifest["perturbations"]), 1)
                if "without_reader_html" in scenario_id:
                    self.assertIn("reader_html", manifest["removed_source_roles"])
                if "without_source_notes" in scenario_id:
                    self.assertIn("source_notes", manifest["removed_source_roles"])
                if "no_audit" in scenario_id:
                    self.assertIn("regression_audit", manifest["removed_source_roles"])

    def test_v7_failure_no_audit_should_not_pass(self) -> None:
        self.assert_v7_non_pass("v7_failure_no_audit_should_not_pass")

    def test_v7_failure_without_self_review_should_not_pass(self) -> None:
        self.assert_v7_non_pass("v7_failure_without_self_review_should_not_pass")

    def test_v7_failure_without_reader_html_should_not_pass_or_review(self) -> None:
        self.assert_v7_non_pass("v7_failure_without_reader_html_should_not_pass_or_review")
        result = read_yaml(scenario_dir("v7_failure_without_reader_html_should_not_pass_or_review") / "live-validator-result.yaml")
        self.assertTrue(result["failure_origin"]["input_missing"])

    def test_v7_failure_without_source_notes_should_not_pass_or_review(self) -> None:
        self.assert_v7_non_pass("v7_failure_without_source_notes_should_not_pass_or_review")
        result = read_yaml(scenario_dir("v7_failure_without_source_notes_should_not_pass_or_review") / "live-validator-result.yaml")
        self.assertTrue(result["failure_origin"]["input_missing"])

    def test_v3_without_self_review_should_still_pass_or_review_not_fail(self) -> None:
        payload = read_json(scenario_dir("v3_without_self_review_should_still_pass_or_review_not_fail") / "live-reviewer-output.json")
        self.assertIn(payload["daily_decision"], {"PASS", "REVIEW"})
        self.assertNotIn(payload["daily_decision"], {"FAIL_DAILY", "PUBLISH_BLOCK", "REPLACE_CASE"})

    def test_v6_without_quality_report_should_still_pass_or_review_not_fail(self) -> None:
        payload = read_json(scenario_dir("v6_without_quality_report_should_still_pass_or_review_not_fail") / "live-reviewer-output.json")
        self.assertIn(payload["daily_decision"], {"PASS", "REVIEW"})
        self.assertNotIn(payload["daily_decision"], {"FAIL_DAILY", "PUBLISH_BLOCK", "REPLACE_CASE"})

    def test_case_order_changed_should_not_change_daily_decision(self) -> None:
        baseline = read_json(RUBRIC_DIR / "generated-replay" / "v6_target_live" / "live-reviewer-output.json")
        changed = read_json(scenario_dir("case_order_changed_should_not_change_daily_decision") / "live-reviewer-output.json")
        self.assertEqual(baseline["daily_decision"], changed["daily_decision"])
        self.assertEqual(baseline["publish_allowed"], changed["publish_allowed"])

    def test_repeated_run_same_input_should_be_deterministic(self) -> None:
        result = read_yaml(scenario_dir("repeated_run_same_input_should_be_deterministic") / "live-validator-result.yaml")
        manifest = read_yaml(scenario_dir("repeated_run_same_input_should_be_deterministic") / "perturbation-manifest.yaml")
        self.assertTrue(result["determinism_check"]["canonical_hashes_match"])
        self.assertTrue(manifest["determinism_check"]["canonical_hashes_match"])

    def test_report_states_boundaries_and_failure_origins(self) -> None:
        report = (RUBRIC_DIR / "live-reviewer-stability-report.md").read_text(encoding="utf-8")
        self.assertIn("P2B-1 stability / no-audit stress", report)
        self.assertIn("local semantic reviewer", report)
        self.assertIn("Not a live LLM reviewer", report)
        self.assertIn("does not enter P2C", report)
        self.assertIn("content-quality failures", report)
        self.assertIn("missing-input risk", report)

    def assert_v7_non_pass(self, scenario_id: str) -> None:
        payload = read_json(scenario_dir(scenario_id) / "live-reviewer-output.json")
        result = read_yaml(scenario_dir(scenario_id) / "live-validator-result.yaml")
        self.assertNotEqual("PASS", payload["daily_decision"])
        self.assertFalse(payload["publish_allowed"])
        self.assertNotEqual("PASS", result["governance_decision"])
        self.assertTrue(result["failure_origin"]["content_quality"] or result["failure_origin"]["input_missing"])


if __name__ == "__main__":
    unittest.main()
