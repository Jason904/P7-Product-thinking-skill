#!/usr/bin/env python3
"""P2C-2 human confirmation gate tests."""

from __future__ import annotations

import shutil
import subprocess
import sys
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RUBRIC_DIR = ROOT / "docs" / "quality" / "rubric-v2.1"
SCRIPT_PATH = ROOT / "scripts" / "run_human_confirmation_gate.py"
POLICY_PATH = RUBRIC_DIR / "p2c2-human-confirmation-policy.yaml"
RUNTIME_ROOT = RUBRIC_DIR / "shadow-runs" / "p2c2-human-confirmation-test"
LEDGER_PATH = RUNTIME_ROOT / "source-shadow-observation-ledger.yaml"
DECISION_PATH = RUNTIME_ROOT / "human-confirmation-decision.yaml"
REPORT_PATH = RUNTIME_ROOT / "human-confirmation-report.md"
PACKAGE_DIR = RUNTIME_ROOT / "release-candidate-package"


def read_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class P2C2HumanConfirmationGateTests(unittest.TestCase):
    def setUp(self) -> None:
        shutil.rmtree(RUNTIME_ROOT, ignore_errors=True)
        RUNTIME_ROOT.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        shutil.rmtree(RUNTIME_ROOT, ignore_errors=True)

    def write_ledger(
        self,
        *,
        observation_status: str = "OBSERVATION_READY",
        formal_publish_allowed: bool = False,
        public_site_updated: bool = False,
        user_notification_sent: bool = False,
        live_llm_review: bool = False,
    ) -> Path:
        ledger = {
            "stage": "P2C-1",
            "shadow_only": True,
            "not_formal_p2c": True,
            "formal_publish_allowed": formal_publish_allowed,
            "public_site_updated": public_site_updated,
            "user_notification_sent": user_notification_sent,
            "live_llm_review": live_llm_review,
            "human_confirmation_required": True,
            "observation_status": observation_status,
            "observation_window": {
                "required_days": 3,
                "observed_days": 3 if observation_status != "OBSERVATION_INCOMPLETE" else 2,
                "dates": [
                    {
                        "date": "2026-06-26",
                        "reviewer_decision": "PASS",
                        "shadow_publish_allowed": True,
                        "formal_publish_allowed": False,
                        "failure_package_created": False,
                        "human_confirmed": False,
                        "required_artifacts_present": True,
                        "missing_artifacts": [],
                    },
                    {
                        "date": "2026-06-27",
                        "reviewer_decision": "PASS" if observation_status != "OBSERVATION_BLOCKED" else "REVIEW",
                        "shadow_publish_allowed": observation_status != "OBSERVATION_BLOCKED",
                        "formal_publish_allowed": False,
                        "failure_package_created": observation_status == "OBSERVATION_BLOCKED",
                        "human_confirmed": False,
                        "required_artifacts_present": True,
                        "missing_artifacts": [],
                    },
                    {
                        "date": "2026-06-28",
                        "reviewer_decision": "PASS",
                        "shadow_publish_allowed": True,
                        "formal_publish_allowed": False,
                        "failure_package_created": False,
                        "human_confirmed": False,
                        "required_artifacts_present": True,
                        "missing_artifacts": [],
                    },
                ],
            },
            "blocked_reasons": [] if observation_status == "OBSERVATION_READY" else [observation_status],
            "promotion_gate": {
                "eligible_for_p2c2": False,
                "reason": "Human confirmation is still required. Shadow PASS is not formal PASS.",
            },
        }
        LEDGER_PATH.write_text(
            yaml.safe_dump(ledger, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        return LEDGER_PATH

    def run_gate(self, *, ledger: Path, human_confirmed: bool) -> dict:
        command = [
            sys.executable,
            str(SCRIPT_PATH),
            "--project-root",
            str(ROOT),
            "--policy",
            str(POLICY_PATH),
            "--ledger",
            str(ledger),
            "--output-dir",
            str(RUNTIME_ROOT),
        ]
        if human_confirmed:
            command.append("--human-confirmed")
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
        self.assertEqual("P2C-2", decision["stage"])
        self.assertEqual("human_confirmation_gate", decision["gate_type"])
        self.assertTrue(decision["shadow_only_source"])
        self.assertTrue(decision["not_formal_publish"])
        self.assertFalse(decision["formal_publish_allowed"])
        self.assertFalse(decision["public_site_updated"])
        self.assertFalse(decision["user_notification_sent"])
        self.assertFalse(decision["live_llm_review"])
        self.assertTrue(decision["requires_manual_publish_step"])

    def test_p2c2_ready_without_human_confirmation_blocks(self) -> None:
        decision = self.run_gate(
            ledger=self.write_ledger(observation_status="OBSERVATION_READY"),
            human_confirmed=False,
        )

        self.assertFalse(decision["release_candidate_created"])
        self.assertFalse(decision["eligible_for_manual_publish_review"])
        self.assertTrue(decision["blocked"])
        self.assertIn("HUMAN_CONFIRMATION_MISSING", decision["blocked_reasons"])
        self.assert_decision_contract(decision)
        self.assertFalse(PACKAGE_DIR.exists())

    def test_p2c2_ready_with_human_confirmation_creates_release_candidate(self) -> None:
        decision = self.run_gate(
            ledger=self.write_ledger(observation_status="OBSERVATION_READY"),
            human_confirmed=True,
        )

        self.assertTrue(decision["release_candidate_created"])
        self.assertTrue(decision["eligible_for_manual_publish_review"])
        self.assertFalse(decision["blocked"])
        self.assertEqual([], decision["blocked_reasons"])
        self.assert_decision_contract(decision)

        expected = {
            "release-candidate-manifest.yaml",
            "source-observation-ledger.yaml",
            "human-confirmation-decision.yaml",
            "manual-publish-review-checklist.md",
        }
        existing = {path.name for path in PACKAGE_DIR.iterdir() if path.is_file()}
        self.assertTrue(expected.issubset(existing), expected - existing)

    def test_p2c2_release_candidate_is_not_formal_publish(self) -> None:
        decision = self.run_gate(
            ledger=self.write_ledger(observation_status="OBSERVATION_READY"),
            human_confirmed=True,
        )
        manifest = read_yaml(PACKAGE_DIR / "release-candidate-manifest.yaml")

        self.assertTrue(decision["release_candidate_created"])
        self.assertFalse(decision["formal_publish_allowed"])
        self.assertFalse(decision["public_site_updated"])
        self.assertFalse(decision["user_notification_sent"])
        self.assertTrue(decision["requires_manual_publish_step"])
        self.assertTrue(manifest["release_candidate_is_not_publish"])
        self.assertFalse(manifest["formal_publish_allowed"])

    def test_p2c2_blocked_observation_cannot_be_overridden_by_human_confirmation(self) -> None:
        decision = self.run_gate(
            ledger=self.write_ledger(observation_status="OBSERVATION_BLOCKED"),
            human_confirmed=True,
        )

        self.assertFalse(decision["release_candidate_created"])
        self.assertFalse(decision["eligible_for_manual_publish_review"])
        self.assertTrue(decision["blocked"])
        self.assertIn("OBSERVATION_BLOCKED", decision["blocked_reasons"])
        self.assert_decision_contract(decision)

    def test_p2c2_incomplete_observation_cannot_be_overridden_by_human_confirmation(self) -> None:
        decision = self.run_gate(
            ledger=self.write_ledger(observation_status="OBSERVATION_INCOMPLETE"),
            human_confirmed=True,
        )

        self.assertFalse(decision["release_candidate_created"])
        self.assertFalse(decision["eligible_for_manual_publish_review"])
        self.assertTrue(decision["blocked"])
        self.assertIn("OBSERVATION_INCOMPLETE", decision["blocked_reasons"])

    def test_p2c2_public_site_update_violation_blocks(self) -> None:
        decision = self.run_gate(
            ledger=self.write_ledger(public_site_updated=True),
            human_confirmed=True,
        )

        self.assertTrue(decision["blocked"])
        self.assertFalse(decision["release_candidate_created"])
        self.assertIn("PUBLIC_SITE_ALREADY_UPDATED", decision["blocked_reasons"])
        self.assertFalse(decision["public_site_updated"])

    def test_p2c2_user_notification_violation_blocks(self) -> None:
        decision = self.run_gate(
            ledger=self.write_ledger(user_notification_sent=True),
            human_confirmed=True,
        )

        self.assertTrue(decision["blocked"])
        self.assertFalse(decision["release_candidate_created"])
        self.assertIn("USER_NOTIFICATION_ALREADY_SENT", decision["blocked_reasons"])
        self.assertFalse(decision["user_notification_sent"])

    def test_p2c2_live_llm_review_violation_blocks(self) -> None:
        decision = self.run_gate(
            ledger=self.write_ledger(live_llm_review=True),
            human_confirmed=True,
        )

        self.assertTrue(decision["blocked"])
        self.assertFalse(decision["release_candidate_created"])
        self.assertIn("LIVE_LLM_REVIEW_USED", decision["blocked_reasons"])
        self.assertFalse(decision["live_llm_review"])

    def test_p2c2_formal_publish_allowed_violation_blocks(self) -> None:
        decision = self.run_gate(
            ledger=self.write_ledger(formal_publish_allowed=True),
            human_confirmed=True,
        )

        self.assertTrue(decision["blocked"])
        self.assertFalse(decision["release_candidate_created"])
        self.assertIn("FORMAL_PUBLISH_ALREADY_ALLOWED", decision["blocked_reasons"])
        self.assertFalse(decision["formal_publish_allowed"])

    def test_p2c2_runtime_artifacts_are_ignored_by_git(self) -> None:
        self.run_gate(
            ledger=self.write_ledger(observation_status="OBSERVATION_READY"),
            human_confirmed=True,
        )
        for path in (
            DECISION_PATH,
            REPORT_PATH,
            PACKAGE_DIR / "release-candidate-manifest.yaml",
        ):
            result = subprocess.run(
                ["git", "check-ignore", "-q", str(path.relative_to(ROOT))],
                cwd=ROOT,
            )
            self.assertEqual(0, result.returncode, str(path))


if __name__ == "__main__":
    unittest.main()
