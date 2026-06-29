#!/usr/bin/env python3
"""P2C-3 manual publish review dry-run gate tests."""

from __future__ import annotations

import shutil
import subprocess
import sys
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RUBRIC_DIR = ROOT / "docs" / "quality" / "rubric-v2.1"
SCRIPT_PATH = ROOT / "scripts" / "run_manual_publish_review_gate.py"
POLICY_PATH = RUBRIC_DIR / "p2c3-manual-publish-review-policy.yaml"
RUNTIME_ROOT = RUBRIC_DIR / "shadow-runs" / "p2c3-manual-publish-review-test"
SOURCE_PACKAGE_DIR = RUNTIME_ROOT / "source-release-candidate-package"
OUTPUT_DIR = RUNTIME_ROOT / "output"
DECISION_PATH = OUTPUT_DIR / "manual-publish-review-decision.yaml"
REPORT_PATH = OUTPUT_DIR / "manual-publish-review-report.md"
OUTPUT_PACKAGE_DIR = OUTPUT_DIR / "manual-publish-review-package"


def read_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class P2C3ManualPublishReviewGateTests(unittest.TestCase):
    def setUp(self) -> None:
        shutil.rmtree(RUNTIME_ROOT, ignore_errors=True)
        SOURCE_PACKAGE_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        shutil.rmtree(RUNTIME_ROOT, ignore_errors=True)

    def write_release_candidate_package(
        self,
        *,
        release_candidate_created: bool = True,
        decision_blocked: bool = False,
        formal_publish_allowed: bool = False,
        public_site_updated: bool = False,
        user_notification_sent: bool = False,
        live_llm_review: bool = False,
        automatic_publishing: bool = False,
    ) -> Path:
        manifest = {
            "stage": "P2C-2",
            "package_type": "release_candidate_decision_package",
            "release_candidate_created": release_candidate_created,
            "release_candidate_is_not_publish": True,
            "manual_publish_review_required_after_release_candidate": True,
            "formal_publish_allowed": formal_publish_allowed,
            "public_site_updated": public_site_updated,
            "user_notification_sent": user_notification_sent,
            "live_llm_review": live_llm_review,
            "automatic_publishing": automatic_publishing,
            "requires_manual_publish_step": True,
            "source_observation_ledger": "source-observation-ledger.yaml",
            "decision": "human-confirmation-decision.yaml",
            "manual_publish_review_checklist": "manual-publish-review-checklist.md",
        }
        decision = {
            "stage": "P2C-2",
            "gate_type": "human_confirmation_gate",
            "shadow_only_source": True,
            "not_formal_publish": True,
            "release_candidate_created": release_candidate_created,
            "human_confirmed": True,
            "formal_publish_allowed": formal_publish_allowed,
            "public_site_updated": public_site_updated,
            "user_notification_sent": user_notification_sent,
            "live_llm_review": live_llm_review,
            "automatic_publishing": automatic_publishing,
            "requires_manual_publish_step": True,
            "eligible_for_manual_publish_review": release_candidate_created and not decision_blocked,
            "blocked": decision_blocked,
            "blocked_reasons": ["OBSERVATION_BLOCKED"] if decision_blocked else [],
            "source_observation_status": "OBSERVATION_READY",
            "release_candidate_is_not_publish": True,
        }
        ledger = {
            "stage": "P2C-1",
            "observation_status": "OBSERVATION_READY",
            "formal_publish_allowed": False,
            "public_site_updated": False,
            "user_notification_sent": False,
            "live_llm_review": False,
        }
        self.write_yaml(SOURCE_PACKAGE_DIR / "release-candidate-manifest.yaml", manifest)
        self.write_yaml(SOURCE_PACKAGE_DIR / "source-observation-ledger.yaml", ledger)
        self.write_yaml(SOURCE_PACKAGE_DIR / "human-confirmation-decision.yaml", decision)
        (SOURCE_PACKAGE_DIR / "manual-publish-review-checklist.md").write_text(
            "\n".join(
                [
                    "# Manual Publish Review Checklist",
                    "",
                    "- Confirm release candidate is not formal publish.",
                    "- Confirm no public site update happened.",
                    "- Confirm no user notification was sent.",
                    "- Confirm final human publish confirmation is still required.",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        return SOURCE_PACKAGE_DIR

    def write_yaml(self, path: Path, data: dict) -> None:
        path.write_text(
            yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )

    def run_gate(self, *, package_dir: Path) -> dict:
        command = [
            sys.executable,
            str(SCRIPT_PATH),
            "--project-root",
            str(ROOT),
            "--policy",
            str(POLICY_PATH),
            "--release-candidate-package",
            str(package_dir),
            "--output-dir",
            str(OUTPUT_DIR),
        ]
        result = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if result.returncode != 0:
            raise AssertionError(result.stdout)
        self.assertTrue(DECISION_PATH.is_file())
        self.assertTrue(REPORT_PATH.is_file())
        return yaml.safe_load(result.stdout)

    def assert_decision_contract(self, decision: dict) -> None:
        self.assertEqual("P2C-3", decision["stage"])
        self.assertEqual("manual_publish_review_dry_run", decision["gate_type"])
        self.assertTrue(decision["not_formal_publish"])
        self.assertFalse(decision["formal_publish_allowed"])
        self.assertFalse(decision["public_site_updated"])
        self.assertFalse(decision["user_notification_sent"])
        self.assertFalse(decision["live_llm_review"])
        self.assertFalse(decision["automatic_publishing"])
        self.assertTrue(decision["requires_final_human_publish_confirmation"])

    def test_p2c3_valid_release_candidate_enters_manual_publish_review(self) -> None:
        decision = self.run_gate(
            package_dir=self.write_release_candidate_package(),
        )

        self.assertTrue(decision["manual_publish_review_ready"])
        self.assertFalse(decision["blocked"])
        self.assertEqual([], decision["blocked_reasons"])
        self.assert_decision_contract(decision)

        expected = {
            "source-release-candidate-manifest.yaml",
            "source-human-confirmation-decision.yaml",
            "manual-publish-review-decision.yaml",
            "final-human-publish-checklist.md",
        }
        existing = {path.name for path in OUTPUT_PACKAGE_DIR.iterdir() if path.is_file()}
        self.assertTrue(expected.issubset(existing), expected - existing)

    def test_p2c3_manual_publish_review_ready_is_not_formal_publish(self) -> None:
        decision = self.run_gate(
            package_dir=self.write_release_candidate_package(),
        )
        manifest = read_yaml(OUTPUT_PACKAGE_DIR / "source-release-candidate-manifest.yaml")

        self.assertTrue(decision["manual_publish_review_ready"])
        self.assertFalse(decision["formal_publish_allowed"])
        self.assertFalse(decision["public_site_updated"])
        self.assertFalse(decision["user_notification_sent"])
        self.assertFalse(decision["automatic_publishing"])
        self.assertTrue(decision["manual_publish_review_ready_is_not_publish"])
        self.assertTrue(decision["requires_final_human_publish_confirmation"])
        self.assertTrue(manifest["release_candidate_is_not_publish"])

    def test_p2c3_missing_manifest_blocks(self) -> None:
        package_dir = self.write_release_candidate_package()
        (package_dir / "release-candidate-manifest.yaml").unlink()

        decision = self.run_gate(package_dir=package_dir)

        self.assertFalse(decision["manual_publish_review_ready"])
        self.assertTrue(decision["blocked"])
        self.assertIn("RELEASE_CANDIDATE_MANIFEST_MISSING", decision["blocked_reasons"])
        self.assert_decision_contract(decision)

    def test_p2c3_missing_manual_publish_checklist_blocks(self) -> None:
        package_dir = self.write_release_candidate_package()
        (package_dir / "manual-publish-review-checklist.md").unlink()

        decision = self.run_gate(package_dir=package_dir)

        self.assertFalse(decision["manual_publish_review_ready"])
        self.assertTrue(decision["blocked"])
        self.assertIn("MANUAL_PUBLISH_CHECKLIST_MISSING", decision["blocked_reasons"])

    def test_p2c3_blocked_human_confirmation_decision_blocks(self) -> None:
        decision = self.run_gate(
            package_dir=self.write_release_candidate_package(decision_blocked=True),
        )

        self.assertFalse(decision["manual_publish_review_ready"])
        self.assertTrue(decision["blocked"])
        self.assertIn("RELEASE_CANDIDATE_BLOCKED", decision["blocked_reasons"])

    def test_p2c3_release_candidate_not_created_blocks(self) -> None:
        decision = self.run_gate(
            package_dir=self.write_release_candidate_package(release_candidate_created=False),
        )

        self.assertFalse(decision["manual_publish_review_ready"])
        self.assertTrue(decision["blocked"])
        self.assertIn("RELEASE_CANDIDATE_NOT_CREATED", decision["blocked_reasons"])

    def test_p2c3_formal_publish_allowed_violation_blocks(self) -> None:
        decision = self.run_gate(
            package_dir=self.write_release_candidate_package(formal_publish_allowed=True),
        )

        self.assertFalse(decision["manual_publish_review_ready"])
        self.assertTrue(decision["blocked"])
        self.assertIn("FORMAL_PUBLISH_ALREADY_ALLOWED", decision["blocked_reasons"])
        self.assertFalse(decision["formal_publish_allowed"])

    def test_p2c3_public_site_update_violation_blocks(self) -> None:
        decision = self.run_gate(
            package_dir=self.write_release_candidate_package(public_site_updated=True),
        )

        self.assertFalse(decision["manual_publish_review_ready"])
        self.assertTrue(decision["blocked"])
        self.assertIn("PUBLIC_SITE_ALREADY_UPDATED", decision["blocked_reasons"])
        self.assertFalse(decision["public_site_updated"])

    def test_p2c3_user_notification_violation_blocks(self) -> None:
        decision = self.run_gate(
            package_dir=self.write_release_candidate_package(user_notification_sent=True),
        )

        self.assertFalse(decision["manual_publish_review_ready"])
        self.assertTrue(decision["blocked"])
        self.assertIn("USER_NOTIFICATION_ALREADY_SENT", decision["blocked_reasons"])
        self.assertFalse(decision["user_notification_sent"])

    def test_p2c3_live_llm_review_violation_blocks(self) -> None:
        decision = self.run_gate(
            package_dir=self.write_release_candidate_package(live_llm_review=True),
        )

        self.assertFalse(decision["manual_publish_review_ready"])
        self.assertTrue(decision["blocked"])
        self.assertIn("LIVE_LLM_REVIEW_USED", decision["blocked_reasons"])
        self.assertFalse(decision["live_llm_review"])

    def test_p2c3_automatic_publishing_violation_blocks(self) -> None:
        decision = self.run_gate(
            package_dir=self.write_release_candidate_package(automatic_publishing=True),
        )

        self.assertFalse(decision["manual_publish_review_ready"])
        self.assertTrue(decision["blocked"])
        self.assertIn("AUTOMATIC_PUBLISHING_ENABLED", decision["blocked_reasons"])
        self.assertFalse(decision["automatic_publishing"])

    def test_p2c3_runtime_artifacts_are_ignored_by_git(self) -> None:
        self.run_gate(package_dir=self.write_release_candidate_package())
        for path in (
            DECISION_PATH,
            REPORT_PATH,
            OUTPUT_PACKAGE_DIR / "manual-publish-review-decision.yaml",
            OUTPUT_PACKAGE_DIR / "final-human-publish-checklist.md",
        ):
            result = subprocess.run(
                ["git", "check-ignore", "-q", str(path.relative_to(ROOT))],
                cwd=ROOT,
            )
            self.assertEqual(0, result.returncode, str(path))


if __name__ == "__main__":
    unittest.main()
