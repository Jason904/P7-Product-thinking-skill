#!/usr/bin/env python3
"""P2C-1 shadow-only observation ledger tests."""

from __future__ import annotations

import shutil
import subprocess
import sys
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RUBRIC_DIR = ROOT / "docs" / "quality" / "rubric-v2.1"
SCRIPT_PATH = ROOT / "scripts" / "run_shadow_observation_ledger.py"
POLICY_PATH = RUBRIC_DIR / "p2c1-shadow-observation-policy.yaml"
RUNTIME_ROOT = RUBRIC_DIR / "shadow-runs" / "p2c1-observation-test"
LEDGER_PATH = RUNTIME_ROOT / "shadow-observation-ledger.yaml"
REPORT_PATH = RUNTIME_ROOT / "shadow-observation-report.md"


def read_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class P2C1ShadowObservationTests(unittest.TestCase):
    def setUp(self) -> None:
        shutil.rmtree(RUNTIME_ROOT, ignore_errors=True)
        RUNTIME_ROOT.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        shutil.rmtree(RUNTIME_ROOT, ignore_errors=True)

    def create_shadow_run(
        self,
        date: str,
        *,
        reviewer_decision: str = "PASS",
        shadow_publish_allowed: bool = True,
        formal_publish_allowed: bool = False,
        failure_package_created: bool = False,
        human_confirmed: bool = False,
        public_site_updated: bool = False,
        user_notification_sent: bool = False,
        live_llm_review: bool = False,
        omit_result: bool = False,
        omit_reader: bool = False,
        omit_source_notes: bool = False,
        omit_reviewer_output: bool = False,
    ) -> Path:
        shadow_dir = RUNTIME_ROOT / f"fixture-{date}"
        shadow_dir.mkdir(parents=True, exist_ok=True)
        if not omit_reader:
            (shadow_dir / "reader.html").write_text("<html>reader</html>\n", encoding="utf-8")
        if not omit_source_notes:
            (shadow_dir / "source-notes.md").write_text("# source notes\n", encoding="utf-8")
        if not omit_reviewer_output:
            (shadow_dir / "reviewer-output.json").write_text("{}\n", encoding="utf-8")
        if not omit_result:
            (shadow_dir / "shadow-review-result.yaml").write_text(
                yaml.safe_dump(
                    {
                        "stage": "P2C-0",
                        "date": date,
                        "reviewer_decision": reviewer_decision,
                        "shadow_publish_allowed": shadow_publish_allowed,
                        "formal_publish_allowed": formal_publish_allowed,
                        "failure_package_created": failure_package_created,
                        "human_confirmed": human_confirmed,
                        "shadow_only": True,
                        "not_formal_p2c": True,
                        "public_site_updated": public_site_updated,
                        "user_notification_sent": user_notification_sent,
                        "live_llm_review": live_llm_review,
                        "human_confirmation_required": True,
                    },
                    allow_unicode=True,
                    sort_keys=False,
                ),
                encoding="utf-8",
            )
        return shadow_dir

    def run_ledger(self, shadow_dirs: list[Path]) -> dict:
        command = [
            sys.executable,
            str(SCRIPT_PATH),
            "--project-root",
            str(ROOT),
            "--policy",
            str(POLICY_PATH),
            "--output-dir",
            str(RUNTIME_ROOT),
        ]
        for path in shadow_dirs:
            command.extend(["--shadow-run", str(path)])
        result = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if result.returncode != 0:
            raise AssertionError(result.stdout)
        self.assertTrue(LEDGER_PATH.is_file())
        self.assertTrue(REPORT_PATH.is_file())
        return yaml.safe_load(result.stdout)

    def assert_shadow_only_contract(self, ledger: dict) -> None:
        self.assertEqual("P2C-1", ledger["stage"])
        self.assertTrue(ledger["shadow_only"])
        self.assertTrue(ledger["not_formal_p2c"])
        self.assertFalse(ledger["formal_publish_allowed"])
        self.assertFalse(ledger["public_site_updated"])
        self.assertFalse(ledger["user_notification_sent"])
        self.assertFalse(ledger["live_llm_review"])
        self.assertTrue(ledger["human_confirmation_required"])
        self.assertFalse(ledger["promotion_gate"]["eligible_for_p2c2"])

    def test_p2c1_three_day_pass_window_still_does_not_formally_publish(self) -> None:
        ledger = self.run_ledger(
            [
                self.create_shadow_run("2026-06-26"),
                self.create_shadow_run("2026-06-27"),
                self.create_shadow_run("2026-06-28"),
            ]
        )

        self.assertEqual("OBSERVATION_READY", ledger["observation_status"])
        self.assertEqual(3, ledger["observation_window"]["observed_days"])
        self.assertFalse(ledger["formal_publish_allowed"])
        self.assertFalse(ledger["promotion_gate"]["eligible_for_p2c2"])
        self.assertIn("Human confirmation", ledger["promotion_gate"]["reason"])
        self.assert_shadow_only_contract(ledger)
        self.assertTrue(all(day["reviewer_decision"] == "PASS" for day in ledger["observation_window"]["dates"]))
        self.assertTrue(all(day["formal_publish_allowed"] is False for day in ledger["observation_window"]["dates"]))

    def test_p2c1_review_day_blocks_p2c2(self) -> None:
        ledger = self.run_ledger(
            [
                self.create_shadow_run("2026-06-26"),
                self.create_shadow_run(
                    "2026-06-27",
                    reviewer_decision="REVIEW",
                    shadow_publish_allowed=False,
                    failure_package_created=True,
                ),
                self.create_shadow_run("2026-06-28"),
            ]
        )

        self.assertEqual("OBSERVATION_BLOCKED", ledger["observation_status"])
        self.assertFalse(ledger["promotion_gate"]["eligible_for_p2c2"])
        self.assertIn("REVIEW", " ".join(ledger["blocked_reasons"]))

    def test_p2c1_incomplete_window_is_not_ready(self) -> None:
        ledger = self.run_ledger(
            [
                self.create_shadow_run("2026-06-27"),
                self.create_shadow_run("2026-06-28"),
            ]
        )

        self.assertEqual("OBSERVATION_INCOMPLETE", ledger["observation_status"])
        self.assertEqual(2, ledger["observation_window"]["observed_days"])
        self.assertFalse(ledger["promotion_gate"]["eligible_for_p2c2"])

    def test_p2c1_missing_shadow_result_blocks(self) -> None:
        ledger = self.run_ledger(
            [
                self.create_shadow_run("2026-06-26"),
                self.create_shadow_run("2026-06-27", omit_result=True),
                self.create_shadow_run("2026-06-28"),
            ]
        )

        self.assertEqual("OBSERVATION_BLOCKED", ledger["observation_status"])
        self.assertFalse(ledger["promotion_gate"]["eligible_for_p2c2"])
        self.assertIn("missing shadow-review-result.yaml", " ".join(ledger["blocked_reasons"]))

    def test_p2c1_public_site_update_is_forbidden(self) -> None:
        ledger = self.run_ledger(
            [
                self.create_shadow_run("2026-06-26"),
                self.create_shadow_run("2026-06-27", public_site_updated=True),
                self.create_shadow_run("2026-06-28"),
            ]
        )

        self.assertEqual("OBSERVATION_BLOCKED", ledger["observation_status"])
        self.assertFalse(ledger["public_site_updated"])
        self.assertIn("public_site_updated", " ".join(ledger["blocked_reasons"]))

    def test_p2c1_user_notification_is_forbidden(self) -> None:
        ledger = self.run_ledger(
            [
                self.create_shadow_run("2026-06-26"),
                self.create_shadow_run("2026-06-27", user_notification_sent=True),
                self.create_shadow_run("2026-06-28"),
            ]
        )

        self.assertEqual("OBSERVATION_BLOCKED", ledger["observation_status"])
        self.assertFalse(ledger["user_notification_sent"])
        self.assertIn("user_notification_sent", " ".join(ledger["blocked_reasons"]))

    def test_p2c1_live_llm_review_is_forbidden(self) -> None:
        ledger = self.run_ledger(
            [
                self.create_shadow_run("2026-06-26"),
                self.create_shadow_run("2026-06-27", live_llm_review=True),
                self.create_shadow_run("2026-06-28"),
            ]
        )

        self.assertEqual("OBSERVATION_BLOCKED", ledger["observation_status"])
        self.assertFalse(ledger["live_llm_review"])
        self.assertIn("live_llm_review", " ".join(ledger["blocked_reasons"]))

    def test_p2c1_human_confirmation_required(self) -> None:
        ledger = self.run_ledger(
            [
                self.create_shadow_run("2026-06-26", human_confirmed=True),
                self.create_shadow_run("2026-06-27", human_confirmed=True),
                self.create_shadow_run("2026-06-28", human_confirmed=True),
            ]
        )

        self.assertTrue(ledger["human_confirmation_required"])
        self.assertFalse(ledger["promotion_gate"]["eligible_for_p2c2"])
        self.assertIn("not formal PASS", ledger["promotion_gate"]["reason"])

    def test_p2c1_runtime_ledger_is_ignored_by_git(self) -> None:
        self.run_ledger(
            [
                self.create_shadow_run("2026-06-26"),
                self.create_shadow_run("2026-06-27"),
                self.create_shadow_run("2026-06-28"),
            ]
        )
        for path in (LEDGER_PATH, REPORT_PATH):
            result = subprocess.run(
                ["git", "check-ignore", "-q", str(path.relative_to(ROOT))],
                cwd=ROOT,
            )
            self.assertEqual(0, result.returncode, str(path))


if __name__ == "__main__":
    unittest.main()
