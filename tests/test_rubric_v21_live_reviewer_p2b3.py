#!/usr/bin/env python3
"""P2B-3 readiness guard tests.

These tests verify that the original P2B-2 corpus is not reclassified by
itself, while the explicit 2026-06-28 P2B-3 supplement can satisfy the combined
third-date and REVIEW/borderline coverage.
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RUBRIC_DIR = ROOT / "docs" / "quality" / "rubric-v2.1"
CROSS_ROOT = RUBRIC_DIR / "generated-replay" / "cross-samples"
P2B3_ROOT = RUBRIC_DIR / "generated-replay" / "p2b3-samples"
SCRIPT_PATH = ROOT / "scripts" / "run_live_reviewer_cross_samples.py"
P2B3_SCRIPT_PATH = ROOT / "scripts" / "run_live_reviewer_p2b3_samples.py"


def read_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class P2B3ReadinessGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        p2b3_result = subprocess.run(
            [
                sys.executable,
                str(P2B3_SCRIPT_PATH),
                "--project-root",
                str(ROOT),
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if p2b3_result.returncode != 0:
            raise AssertionError(p2b3_result.stdout)
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

    def test_p2b2_corpus_remains_insufficient_by_itself(self) -> None:
        cross_manifests = [
            read_yaml(path)
            for path in sorted(CROSS_ROOT.glob("*/source-manifest.yaml"))
        ]
        cross_dates = {item["date"] for item in cross_manifests if item["real_sample"]}
        self.assertEqual({"2026-06-25", "2026-06-26"}, cross_dates)
        self.assertLess(len(cross_dates), 3)

        report = (RUBRIC_DIR / "live-reviewer-cross-sample-report.md").read_text(encoding="utf-8")
        self.assertIn("P2B-2 corpus date count: 2 / required >= 3 for P2B-3", report)
        self.assertIn("P2B-2 original 6-sample corpus remains insufficient by itself", report)

    def test_p2b3_supplement_adds_third_date_and_two_review_samples(self) -> None:
        cross_manifests = [
            read_yaml(path)
            for path in sorted(CROSS_ROOT.glob("*/source-manifest.yaml"))
        ]
        p2b3_manifests = [
            read_yaml(path)
            for path in sorted(P2B3_ROOT.glob("*/source-manifest.yaml"))
        ]
        combined_dates = {
            item["date"]
            for item in [*cross_manifests, *p2b3_manifests]
            if item["real_sample"] and not item["synthetic_fixture"]
        }
        review_samples = [
            item for item in p2b3_manifests
            if item["real_sample"] and item["expected_class"] == "REVIEW"
        ]
        self.assertEqual({"2026-06-25", "2026-06-26", "2026-06-28"}, combined_dates)
        self.assertGreaterEqual(len(review_samples), 2)

        report = (RUBRIC_DIR / "live-reviewer-cross-sample-report.md").read_text(encoding="utf-8")
        self.assertIn("P2B-3 status: `READY_WITH_2026_06_28_SUPPLEMENT`", report)
        self.assertIn("Combined real date count: 3 / required >= 3", report)
        self.assertIn("Combined REVIEW / borderline expected sample count: 2 / required >= 2", report)

    def test_no_synthetic_fixture_counts_toward_p2b3(self) -> None:
        for path in [*sorted(CROSS_ROOT.glob("*/source-manifest.yaml")), *sorted(P2B3_ROOT.glob("*/source-manifest.yaml"))]:
            with self.subTest(path=path):
                manifest = read_yaml(path)
                self.assertTrue(manifest["real_sample"])
                self.assertFalse(manifest["synthetic_fixture"])

        report = (RUBRIC_DIR / "live-reviewer-cross-sample-report.md").read_text(encoding="utf-8")
        self.assertIn("No synthetic fixture is used to pretend third-date coverage", report)
        self.assertIn("Synthetic fixtures are not allowed to satisfy these counts", report)

    def test_boundaries_remain_local_non_llm_non_p2c(self) -> None:
        report = (RUBRIC_DIR / "live-reviewer-cross-sample-report.md").read_text(encoding="utf-8")
        self.assertIn("Reviewer: local semantic reviewer", report)
        self.assertIn("Not a live LLM reviewer", report)
        self.assertIn("Does not enter P2C", report)
        self.assertIn("Self-review tables and historical audit reports are evidence inputs only", report)


if __name__ == "__main__":
    unittest.main()
