#!/usr/bin/env python3
"""P2B-4 pre-production shadow review tests."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RUBRIC_DIR = ROOT / "docs" / "quality" / "rubric-v2.1"
SHADOW_DIR = RUBRIC_DIR / "shadow-runs" / "2026-06-28"
SCRIPT_PATH = ROOT / "scripts" / "run_daily_shadow_review.py"
HTML_VALIDATOR_PATH = ROOT / "skill" / "scripts" / "validate_training_reader_html.py"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class P2B4ShadowReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--project-root",
                str(ROOT),
                "--date",
                "2026-06-28",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if result.returncode != 0:
            raise AssertionError(result.stdout)

    def test_shadow_run_retains_all_intermediate_artifacts(self) -> None:
        expected = {
            "training.md",
            "reader.html",
            "source-notes.md",
            "raw-reviewer-response.json",
            "reviewer-output.json",
            "claim-evidence-map.json",
            "failure-objects.json",
            "shadow-generation-log.yaml",
            "shadow-review-result.yaml",
            "source-manifest.yaml",
        }
        existing = {path.name for path in SHADOW_DIR.iterdir() if path.is_file()}
        self.assertTrue(expected.issubset(existing), expected - existing)

    def test_reader_html_is_rendered_and_complete(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(HTML_VALIDATOR_PATH),
                str(SHADOW_DIR / "reader.html"),
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.assertEqual(0, result.returncode, result.stdout)

    def test_shadow_boundaries_prevent_publication(self) -> None:
        shadow = read_yaml(SHADOW_DIR / "shadow-review-result.yaml")
        log = read_yaml(SHADOW_DIR / "shadow-generation-log.yaml")
        manifest = read_yaml(SHADOW_DIR / "source-manifest.yaml")
        reviewer = read_json(SHADOW_DIR / "reviewer-output.json")

        self.assertTrue(shadow["local_semantic_reviewer"])
        self.assertFalse(shadow["live_llm_review"])
        self.assertTrue(shadow["not_p2c"])
        self.assertTrue(shadow["not_daily_production_pipeline"])
        self.assertFalse(shadow["website_updated"])
        self.assertFalse(shadow["user_notification_sent"])
        self.assertFalse(shadow["shadow_pass_is_formal_pass"])
        self.assertFalse(shadow["shadow_publish_allowed"])
        self.assertFalse(shadow["formal_publish_allowed"])
        self.assertTrue(shadow["manual_confirmation_required_before_p2c"])

        self.assertFalse(log["live_llm_review"])
        self.assertFalse(log["shadow_publish_allowed"])
        self.assertFalse(log["formal_publish_allowed"])
        self.assertFalse(manifest["live_llm_review"])
        self.assertTrue(manifest["not_p2c"])
        self.assertFalse(manifest["website_updated"])
        self.assertFalse(manifest["user_notification_sent"])

        self.assertEqual("REVIEW", reviewer["daily_decision"])
        self.assertFalse(reviewer["publish_allowed"])

    def test_review_or_fail_generates_reflowable_failure_package(self) -> None:
        shadow = read_yaml(SHADOW_DIR / "shadow-review-result.yaml")
        package_dir = ROOT / shadow["failure_package_path"]
        self.assertTrue(shadow["failure_package_required"])
        self.assertTrue(shadow["failure_package_created"])
        self.assertTrue(package_dir.is_dir())

        expected = {
            "package-manifest.yaml",
            "failure-objects.json",
            "reviewer-output.json",
            "claim-evidence-map.json",
            "shadow-review-result.yaml",
            "source-manifest.yaml",
            "repair-actions.yaml",
        }
        existing = {path.name for path in package_dir.iterdir() if path.is_file()}
        self.assertTrue(expected.issubset(existing), expected - existing)

        failure_objects = read_json(package_dir / "failure-objects.json")
        repair = read_yaml(package_dir / "repair-actions.yaml")
        package_manifest = read_yaml(package_dir / "package-manifest.yaml")
        self.assertGreaterEqual(len(failure_objects), 1)
        self.assertIn("rewrite_8q_reasoning", repair["repair_targets"])
        self.assertIn("G6", repair["must_rerun_gates"])
        self.assertEqual("shadow_failure_package", package_manifest["package_type"])
        self.assertFalse(package_manifest["shadow_pass_is_formal_pass"])

    def test_shadow_report_states_status_and_authority_limits(self) -> None:
        report = (RUBRIC_DIR / "shadow-run-report.md").read_text(encoding="utf-8")
        self.assertIn("P2B-4 Pre-production Shadow Run Report", report)
        self.assertIn("local semantic reviewer", report)
        self.assertIn("Not a live LLM reviewer", report)
        self.assertIn("Does not enter P2C", report)
        self.assertIn("Does not publish or update website content", report)
        self.assertIn("Shadow PASS is not formal PASS", report)
        self.assertIn("Failure package path", report)

    def test_governance_validator_passes_payload_but_shadow_still_blocks_publish(self) -> None:
        shadow = read_yaml(SHADOW_DIR / "shadow-review-result.yaml")
        self.assertEqual("PASS", shadow["governance_validator_status"])
        self.assertEqual("REVIEW", shadow["governance_decision"])
        self.assertTrue(shadow["publish_blocked"])
        self.assertFalse(shadow["shadow_publish_allowed"])
        self.assertIn("BOILERPLATE_REASONING", shadow["failure_types"])
        self.assertIn("REVIEW_EVIDENCE_INVALID", shadow["failure_types"])


if __name__ == "__main__":
    unittest.main()
