#!/usr/bin/env python3
"""P2C-0 shadow-only daily integration tests."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RUBRIC_DIR = ROOT / "docs" / "quality" / "rubric-v2.1"
SHADOW_ROOT = RUBRIC_DIR / "shadow-runs" / "2026-06-28"
PASS_DIR = SHADOW_ROOT / "p2c0-pass"
REVIEW_DIR = SHADOW_ROOT / "p2c0-review"
SCRIPT_PATH = ROOT / "scripts" / "run_daily_shadow_integration.py"
SOURCE_NOTES = ROOT / "outputs" / "daily-training" / "2026-06-28" / "source-notes-p2b3.md"
PASS_TRAINING = ROOT / "outputs" / "daily-training" / "2026-06-28" / "training-v8-pass.md"
REVIEW_TRAINING = ROOT / "outputs" / "daily-training" / "2026-06-28" / "training-v8-review-boilerplate.md"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class P2C0ShadowIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        for path in (PASS_DIR, REVIEW_DIR):
            shutil.rmtree(path, ignore_errors=True)

        cls.pass_result = cls.run_scenario(
            scenario="pass",
            training=PASS_TRAINING,
        )
        cls.review_result = cls.run_scenario(
            scenario="review",
            training=REVIEW_TRAINING,
        )

    @classmethod
    def run_scenario(cls, *, scenario: str, training: Path) -> dict:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--project-root",
                str(ROOT),
                "--date",
                "2026-06-28",
                "--scenario",
                scenario,
                "--training-md",
                str(training),
                "--source-notes",
                str(SOURCE_NOTES),
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if result.returncode != 0:
            raise AssertionError(result.stdout)
        return yaml.safe_load(result.stdout)

    def assert_shadow_only_contract(self, result: dict) -> None:
        self.assertEqual("P2C-0", result["stage"])
        self.assertTrue(result["shadow_only"])
        self.assertTrue(result["not_formal_p2c"])
        self.assertTrue(result["local_semantic_reviewer"])
        self.assertFalse(result["live_llm_review"])
        self.assertFalse(result["public_site_updated"])
        self.assertFalse(result["user_notification_sent"])
        self.assertFalse(result["formal_publish_allowed"])
        self.assertTrue(result["human_confirmation_required"])

    def test_p2c0_shadow_pass_never_formally_publishes(self) -> None:
        result = read_yaml(PASS_DIR / "shadow-review-result.yaml")
        reviewer = read_json(PASS_DIR / "reviewer-output.json")

        self.assertEqual("PASS", reviewer["daily_decision"])
        self.assertEqual("PASS", result["reviewer_decision"])
        self.assertTrue(result["shadow_publish_allowed"])
        self.assertFalse(result["formal_publish_allowed"])
        self.assertTrue(result["human_confirmation_required"])
        self.assertFalse(result["failure_package_required"])
        self.assertFalse(result["failure_package_created"])
        self.assert_shadow_only_contract(result)

    def test_p2c0_review_creates_failure_package(self) -> None:
        result = read_yaml(REVIEW_DIR / "shadow-review-result.yaml")
        reviewer = read_json(REVIEW_DIR / "reviewer-output.json")

        self.assertEqual("REVIEW", reviewer["daily_decision"])
        self.assertEqual("REVIEW", result["reviewer_decision"])
        self.assertFalse(result["shadow_publish_allowed"])
        self.assertFalse(result["formal_publish_allowed"])
        self.assertTrue(result["failure_package_required"])
        self.assertTrue(result["failure_package_created"])

        package_dir = REVIEW_DIR / "shadow-failure-package"
        expected = {
            "source-manifest.yaml",
            "reviewer-output.json",
            "claim-evidence-map.json",
            "failure-objects.json",
            "shadow-review-result.yaml",
            "repair-actions.yaml",
            "package-manifest.yaml",
        }
        existing = {path.name for path in package_dir.iterdir() if path.is_file()}
        self.assertTrue(expected.issubset(existing), expected - existing)

    def test_p2c0_shadow_outputs_required_files(self) -> None:
        expected = {
            "training.md",
            "reader.html",
            "source-notes.md",
            "reviewer-output.json",
            "claim-evidence-map.json",
            "failure-objects.json",
            "shadow-review-result.yaml",
            "shadow-generation-log.yaml",
            "shadow-run-report.md",
        }
        for shadow_dir in (PASS_DIR, REVIEW_DIR):
            existing = {path.name for path in shadow_dir.iterdir() if path.is_file()}
            self.assertTrue(expected.issubset(existing), (shadow_dir, expected - existing))

    def test_p2c0_result_declares_shadow_only_not_formal_p2c(self) -> None:
        self.assert_shadow_only_contract(read_yaml(PASS_DIR / "shadow-review-result.yaml"))
        self.assert_shadow_only_contract(read_yaml(REVIEW_DIR / "shadow-review-result.yaml"))

    def test_p2c0_does_not_touch_public_site(self) -> None:
        for path in (PASS_DIR, REVIEW_DIR):
            result = read_yaml(path / "shadow-review-result.yaml")
            log = read_yaml(path / "shadow-generation-log.yaml")
            manifest = read_yaml(path / "source-manifest.yaml")
            self.assertFalse(result["public_site_updated"])
            self.assertFalse(log["public_site_updated"])
            self.assertFalse(manifest["public_site_updated"])

    def test_p2c0_does_not_send_notifications(self) -> None:
        for path in (PASS_DIR, REVIEW_DIR):
            result = read_yaml(path / "shadow-review-result.yaml")
            log = read_yaml(path / "shadow-generation-log.yaml")
            manifest = read_yaml(path / "source-manifest.yaml")
            self.assertFalse(result["user_notification_sent"])
            self.assertFalse(log["user_notification_sent"])
            self.assertFalse(manifest["user_notification_sent"])

    def test_p2c0_uses_local_semantic_reviewer_not_live_llm(self) -> None:
        for path in (PASS_DIR, REVIEW_DIR):
            result = read_yaml(path / "shadow-review-result.yaml")
            log = read_yaml(path / "shadow-generation-log.yaml")
            manifest = read_yaml(path / "source-manifest.yaml")
            self.assertTrue(result["local_semantic_reviewer"])
            self.assertFalse(result["live_llm_review"])
            self.assertTrue(log["local_semantic_reviewer"])
            self.assertFalse(log["live_llm_review"])
            self.assertTrue(manifest["local_semantic_reviewer"])
            self.assertFalse(manifest["live_llm_review"])

    def test_p2c0_runtime_artifacts_are_ignored_by_git(self) -> None:
        for path in (PASS_DIR / "training.md", REVIEW_DIR / "shadow-failure-package" / "package-manifest.yaml"):
            result = subprocess.run(
                ["git", "check-ignore", "-q", str(path.relative_to(ROOT))],
                cwd=ROOT,
            )
            self.assertEqual(0, result.returncode, str(path))

    def test_p2c0_human_confirmation_required_for_pass_and_review(self) -> None:
        for path in (PASS_DIR, REVIEW_DIR):
            result = read_yaml(path / "shadow-review-result.yaml")
            self.assertTrue(result["human_confirmation_required"])
            self.assertFalse(result["formal_publish_allowed"])


if __name__ == "__main__":
    unittest.main()
