#!/usr/bin/env python3
"""P2A tests for recorded reviewer payload generation from real samples."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RUBRIC_DIR = ROOT / "docs" / "quality" / "rubric-v2.1"
GENERATED_DIR = RUBRIC_DIR / "generated-replay"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class ReviewerPayloadGeneratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cmd = [
            sys.executable,
            "scripts/run_reviewer_generation_replay.py",
            "--project-root",
            str(ROOT),
        ]
        cls.replay = subprocess.run(
            cmd,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if cls.replay.returncode != 0:
            raise AssertionError(cls.replay.stdout)

    def sample_dir(self, sample_id: str) -> Path:
        return GENERATED_DIR / sample_id

    def reviewer(self, sample_id: str) -> dict:
        return read_json(self.sample_dir(sample_id) / "reviewer-output.json")

    def validator_result(self, sample_id: str) -> dict:
        return read_yaml(self.sample_dir(sample_id) / "validator-result.yaml")

    def generation_log(self, sample_id: str) -> dict:
        return read_yaml(self.sample_dir(sample_id) / "generation-log.yaml")

    def test_generator_reads_real_source_files(self) -> None:
        for sample_id in ("v3_target", "v6_target", "v7_failure"):
            with self.subTest(sample_id=sample_id):
                log = self.generation_log(sample_id)
                self.assertTrue(log["recorded_generation"])
                self.assertTrue(log["not_live_llm_review"])
                self.assertGreaterEqual(len(log["input_files"]), 1)
                for source in log["input_files"]:
                    source_path = ROOT / source["path"]
                    self.assertTrue(source_path.is_file(), source)
                    self.assertGreater(source["bytes"], 0, source)
                    self.assertRegex(source["sha256"], r"^[0-9a-f]{64}$")
                    self.assertEqual(source_path.stat().st_size, source["bytes"])

    def test_v3_generated_payload_should_pass_validator(self) -> None:
        reviewer = self.reviewer("v3_target")
        result = self.validator_result("v3_target")
        self.assertEqual("PASS", reviewer["daily_decision"])
        self.assertTrue(reviewer["publish_allowed"])
        self.assertEqual("PASS", result["validator_status"])
        self.assertEqual([], result["reviewer_errors"])
        self.assertEqual([], result["claim_evidence_map_errors"])
        self.assertEqual([], result["failure_object_errors"])

    def test_v6_generated_payload_should_pass_validator(self) -> None:
        reviewer = self.reviewer("v6_target")
        result = self.validator_result("v6_target")
        self.assertEqual("PASS", reviewer["daily_decision"])
        self.assertTrue(reviewer["publish_allowed"])
        self.assertEqual("PASS", result["validator_status"])
        self.assertEqual([], result["reviewer_errors"])
        self.assertEqual([], result["claim_evidence_map_errors"])
        self.assertEqual([], result["failure_object_errors"])

    def test_v7_generated_payload_should_not_pass(self) -> None:
        reviewer = self.reviewer("v7_failure")
        result = self.validator_result("v7_failure")
        self.assertIn(reviewer["daily_decision"], {"FAIL_DAILY", "PUBLISH_BLOCK", "REVIEW"})
        self.assertFalse(reviewer["publish_allowed"])
        self.assertNotEqual("PASS", result["golden_comparison"]["daily_decision"])
        self.assertIn("EMPTY_8Q_REASONING", result["failure_types"])

    def test_generated_payload_should_include_claim_evidence_map(self) -> None:
        for sample_id in ("v3_target", "v6_target", "v7_failure"):
            with self.subTest(sample_id=sample_id):
                sample_dir = self.sample_dir(sample_id)
                claim_map = read_json(sample_dir / "claim-evidence-map.json")
                reviewer = self.reviewer(sample_id)
                self.assertEqual({"case_a", "case_b", "case_c"}, set(claim_map.keys()))
                for case_review in reviewer["case_reviews"]:
                    self.assertGreaterEqual(len(case_review["claim_evidence_map"]), 1)

    def test_generated_failure_objects_should_match_expected_failure_types(self) -> None:
        failures = read_json(self.sample_dir("v7_failure") / "failure-objects.json")
        failure_types = {failure["failure_type"] for failure in failures}
        self.assertTrue(
            {
                "EMPTY_8Q_REASONING",
                "DISCONNECTED_8Q_CHAIN",
                "BOILERPLATE_REASONING",
            }.issubset(failure_types)
        )

    def test_generated_payload_should_ignore_self_review_scores(self) -> None:
        for sample_id in ("v3_target", "v6_target", "v7_failure"):
            with self.subTest(sample_id=sample_id):
                log = self.generation_log(sample_id)
                self.assertTrue(log["self_review_policy"]["ignored_as_release_evidence"])
                self.assertEqual(
                    "self_review_is_subject_not_authority",
                    log["self_review_policy"]["rule_id"],
                )

    def test_generated_payload_should_record_generation_log(self) -> None:
        for sample_id in ("v3_target", "v6_target", "v7_failure"):
            with self.subTest(sample_id=sample_id):
                log = self.generation_log(sample_id)
                self.assertEqual(sample_id, log["sample_id"])
                self.assertEqual("p2a-recorded-generator-v1", log["prompt_version"])
                self.assertEqual("recorded_fixture_replay", log["generation_method"])
                for key in (
                    "reviewer_output_path",
                    "claim_evidence_map_path",
                    "failure_objects_path",
                    "validator_result_path",
                ):
                    self.assertTrue((ROOT / log["output_paths"][key]).is_file())

    def test_p1_72_tests_must_still_pass(self) -> None:
        cmd = [
            sys.executable,
            "-m",
            "unittest",
            "tests.test_rubric_v21_governance",
            "tests.test_rubric_v21_adversarial",
            "tests.test_rubric_v21_anchor_quality",
            "tests.test_rubric_v21_calibration_replay",
        ]
        result = subprocess.run(
            cmd,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertIn("Ran 72 tests", result.stdout)
        self.assertIn("OK", result.stdout)


if __name__ == "__main__":
    unittest.main()
