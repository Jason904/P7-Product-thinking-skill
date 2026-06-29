#!/usr/bin/env python3
"""P2C-4 no-op publish executor tests."""

from __future__ import annotations

import shutil
import subprocess
import sys
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RUBRIC_DIR = ROOT / "docs" / "quality" / "rubric-v2.1"
SCRIPT_PATH = ROOT / "scripts" / "run_noop_publish_executor.py"
POLICY_PATH = RUBRIC_DIR / "p2c4-noop-publish-executor-policy.yaml"
RUNTIME_ROOT = RUBRIC_DIR / "shadow-runs" / "p2c4-noop-publish-executor-test"
SOURCE_PACKAGE_DIR = RUNTIME_ROOT / "source-manual-publish-review-package"
OUTPUT_DIR = RUNTIME_ROOT / "output"
DECISION_PATH = OUTPUT_DIR / "noop-publish-execution-decision.yaml"
REPORT_PATH = OUTPUT_DIR / "noop-publish-execution-report.md"
PLAN_PATH = OUTPUT_DIR / "noop-publish-execution-plan.yaml"


def read_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class P2C4NoopPublishExecutorTests(unittest.TestCase):
    def setUp(self) -> None:
        shutil.rmtree(RUNTIME_ROOT, ignore_errors=True)
        SOURCE_PACKAGE_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        shutil.rmtree(RUNTIME_ROOT, ignore_errors=True)

    def write_manual_publish_review_package(
        self,
        *,
        manual_publish_review_ready: bool = True,
        decision_blocked: bool = False,
        formal_publish_allowed: bool = False,
        public_site_updated: bool = False,
        user_notification_sent: bool = False,
        live_llm_review: bool = False,
        automatic_publishing: bool = False,
    ) -> Path:
        release_manifest = {
            "stage": "P2C-2",
            "package_type": "release_candidate_decision_package",
            "release_candidate_created": True,
            "release_candidate_is_not_publish": True,
            "formal_publish_allowed": formal_publish_allowed,
            "public_site_updated": public_site_updated,
            "user_notification_sent": user_notification_sent,
            "live_llm_review": live_llm_review,
            "automatic_publishing": automatic_publishing,
        }
        human_decision = {
            "stage": "P2C-2",
            "gate_type": "human_confirmation_gate",
            "release_candidate_created": True,
            "release_candidate_is_not_publish": True,
            "formal_publish_allowed": formal_publish_allowed,
            "public_site_updated": public_site_updated,
            "user_notification_sent": user_notification_sent,
            "live_llm_review": live_llm_review,
            "automatic_publishing": automatic_publishing,
            "blocked": False,
            "blocked_reasons": [],
        }
        manual_decision = {
            "stage": "P2C-3",
            "gate_type": "manual_publish_review_dry_run",
            "not_formal_publish": True,
            "manual_publish_review_ready": manual_publish_review_ready,
            "manual_publish_review_ready_is_not_publish": True,
            "formal_publish_allowed": formal_publish_allowed,
            "public_site_updated": public_site_updated,
            "user_notification_sent": user_notification_sent,
            "live_llm_review": live_llm_review,
            "automatic_publishing": automatic_publishing,
            "requires_final_human_publish_confirmation": True,
            "blocked": decision_blocked,
            "blocked_reasons": ["MANUAL_REVIEW_BLOCKED"] if decision_blocked else [],
        }
        self.write_yaml(
            SOURCE_PACKAGE_DIR / "source-release-candidate-manifest.yaml",
            release_manifest,
        )
        self.write_yaml(
            SOURCE_PACKAGE_DIR / "source-human-confirmation-decision.yaml",
            human_decision,
        )
        self.write_yaml(
            SOURCE_PACKAGE_DIR / "manual-publish-review-decision.yaml",
            manual_decision,
        )
        (SOURCE_PACKAGE_DIR / "final-human-publish-checklist.md").write_text(
            "\n".join(
                [
                    "# Final Human Publish Checklist",
                    "",
                    "- Confirm no-op executor did not publish.",
                    "- Confirm public site update is not executed.",
                    "- Confirm user notification is not executed.",
                    "- Confirm explicit final publish command is still required.",
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

    def run_executor(self, *, package_dir: Path) -> dict:
        command = [
            sys.executable,
            str(SCRIPT_PATH),
            "--project-root",
            str(ROOT),
            "--policy",
            str(POLICY_PATH),
            "--manual-publish-review-package",
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
        self.assertTrue(PLAN_PATH.is_file())
        return yaml.safe_load(result.stdout)

    def assert_noop_contract(self, decision: dict) -> None:
        self.assertEqual("P2C-4", decision["stage"])
        self.assertEqual("noop_publish_executor", decision["executor_type"])
        self.assertTrue(decision["dry_run"])
        self.assertTrue(decision["noop"])
        self.assertFalse(decision["publish_executed"])
        self.assertFalse(decision["formal_publish_allowed"])
        self.assertFalse(decision["public_site_updated"])
        self.assertFalse(decision["user_notification_sent"])
        self.assertFalse(decision["live_llm_review"])
        self.assertFalse(decision["automatic_publishing"])
        self.assertTrue(decision["requires_explicit_final_publish_command"])
        self.assertTrue(decision["requires_final_human_publish_confirmation"])

    def test_p2c4_valid_manual_publish_review_package_generates_noop_plan(self) -> None:
        decision = self.run_executor(
            package_dir=self.write_manual_publish_review_package(),
        )
        plan = read_yaml(PLAN_PATH)

        self.assertFalse(decision["blocked"])
        self.assertTrue(decision["safe_to_run_real_publish_later"])
        self.assertEqual([], decision["blocked_reasons"])
        self.assert_noop_contract(decision)
        self.assertEqual(decision["planned_actions"], plan["planned_actions"])
        self.assertEqual(
            ["render_final_reader", "update_public_site", "send_user_notification"],
            [action["action"] for action in decision["planned_actions"]],
        )

    def test_p2c4_noop_executor_does_not_publish(self) -> None:
        decision = self.run_executor(
            package_dir=self.write_manual_publish_review_package(),
        )

        self.assertFalse(decision["publish_executed"])
        self.assertFalse(decision["formal_publish_allowed"])
        self.assertFalse(decision["public_site_updated"])
        self.assertFalse(decision["user_notification_sent"])
        self.assertTrue(decision["dry_run"])
        self.assertTrue(decision["noop"])
        side_effect_actions = [
            action for action in decision["planned_actions"] if action["side_effect"]
        ]
        self.assertTrue(side_effect_actions)
        for action in side_effect_actions:
            self.assertFalse(action["executed"], action)

    def test_p2c4_missing_final_human_publish_checklist_blocks(self) -> None:
        package_dir = self.write_manual_publish_review_package()
        (package_dir / "final-human-publish-checklist.md").unlink()

        decision = self.run_executor(package_dir=package_dir)

        self.assertTrue(decision["blocked"])
        self.assertFalse(decision["safe_to_run_real_publish_later"])
        self.assertIn("FINAL_HUMAN_PUBLISH_CHECKLIST_MISSING", decision["blocked_reasons"])
        self.assert_noop_contract(decision)

    def test_p2c4_manual_publish_review_not_ready_blocks(self) -> None:
        decision = self.run_executor(
            package_dir=self.write_manual_publish_review_package(
                manual_publish_review_ready=False,
                decision_blocked=True,
            ),
        )

        self.assertTrue(decision["blocked"])
        self.assertFalse(decision["safe_to_run_real_publish_later"])
        self.assertIn("MANUAL_PUBLISH_REVIEW_NOT_READY", decision["blocked_reasons"])
        self.assert_noop_contract(decision)

    def test_p2c4_formal_publish_allowed_violation_blocks(self) -> None:
        decision = self.run_executor(
            package_dir=self.write_manual_publish_review_package(formal_publish_allowed=True),
        )

        self.assertTrue(decision["blocked"])
        self.assertIn("FORMAL_PUBLISH_ALREADY_ALLOWED", decision["blocked_reasons"])
        self.assertFalse(decision["formal_publish_allowed"])

    def test_p2c4_public_site_update_violation_blocks(self) -> None:
        decision = self.run_executor(
            package_dir=self.write_manual_publish_review_package(public_site_updated=True),
        )

        self.assertTrue(decision["blocked"])
        self.assertIn("PUBLIC_SITE_ALREADY_UPDATED", decision["blocked_reasons"])
        self.assertFalse(decision["public_site_updated"])

    def test_p2c4_user_notification_violation_blocks(self) -> None:
        decision = self.run_executor(
            package_dir=self.write_manual_publish_review_package(user_notification_sent=True),
        )

        self.assertTrue(decision["blocked"])
        self.assertIn("USER_NOTIFICATION_ALREADY_SENT", decision["blocked_reasons"])
        self.assertFalse(decision["user_notification_sent"])

    def test_p2c4_live_llm_review_violation_blocks(self) -> None:
        decision = self.run_executor(
            package_dir=self.write_manual_publish_review_package(live_llm_review=True),
        )

        self.assertTrue(decision["blocked"])
        self.assertIn("LIVE_LLM_REVIEW_USED", decision["blocked_reasons"])
        self.assertFalse(decision["live_llm_review"])

    def test_p2c4_automatic_publishing_violation_blocks(self) -> None:
        decision = self.run_executor(
            package_dir=self.write_manual_publish_review_package(automatic_publishing=True),
        )

        self.assertTrue(decision["blocked"])
        self.assertIn("AUTOMATIC_PUBLISHING_ENABLED", decision["blocked_reasons"])
        self.assertFalse(decision["automatic_publishing"])

    def test_p2c4_runtime_artifacts_are_ignored_by_git(self) -> None:
        self.run_executor(package_dir=self.write_manual_publish_review_package())
        for path in (DECISION_PATH, REPORT_PATH, PLAN_PATH):
            result = subprocess.run(
                ["git", "check-ignore", "-q", str(path.relative_to(ROOT))],
                cwd=ROOT,
            )
            self.assertEqual(0, result.returncode, str(path))


if __name__ == "__main__":
    unittest.main()
