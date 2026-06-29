#!/usr/bin/env python3
"""Anchor-quality tests that prevent point-name compliance and double scoring."""

from __future__ import annotations

import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RUBRIC_DIR = ROOT / "docs" / "quality" / "rubric-v2.1"


def read_yaml(name: str):
    return yaml.safe_load((RUBRIC_DIR / name).read_text(encoding="utf-8"))


class RubricV21AnchorQualityTests(unittest.TestCase):
    def objective_checks(self) -> dict[str, list[str]]:
        anchors = read_yaml("rubric-score-anchors.yaml")
        return {
            item_id: item["objective_checks"]
            for item_id, item in anchors["items"].items()
        }

    def test_anchors_named_checks_are_case_specific(self) -> None:
        forbidden_suffixes = ("_named", "_present")
        forbidden_exact = {
            "cause_variables_named",
            "result_variables_named",
            "mediator_variables_named",
            "pattern_named",
            "stakeholder_roles_named",
            "alternative_judgment_named",
        }
        for item_id, checks in self.objective_checks().items():
            for check in checks:
                with self.subTest(item_id=item_id, check=check):
                    self.assertNotIn(check, forbidden_exact)
                    self.assertFalse(check.endswith(forbidden_suffixes))

    def test_stakeholder_padding_should_not_pass_system_relation(self) -> None:
        checks = self.objective_checks()["thinking.system_relation_value_flow"]
        self.assertNotIn("stakeholder_count_ge_4", checks)
        self.assertIn("relevant_stakeholders_complete", checks)
        self.assertIn("irrelevant_stakeholder_padding_absent", checks)

    def test_source_coverage_does_not_reward_low_quality_source_padding(self) -> None:
        checks = self.objective_checks()["content.information_density"]
        self.assertNotIn("source_count_ge_3", checks)
        self.assertIn("source_coverage_sufficient", checks)
        self.assertIn("source_quality_not_padded", checks)

    def test_no_ai_hot_required_when_not_used(self) -> None:
        checks = self.objective_checks()["content.source_traceability"]
        self.assertNotIn("ai_hot_marked_signal_only", checks)
        self.assertIn("ai_hot_if_used_marked_signal_only", checks)

    def test_no_duplicate_scoring_between_prep_and_followup(self) -> None:
        prep_checks = self.objective_checks()["expression.prep_scqa_quality"]
        followup_checks = self.objective_checks()["expression.interview_followup_resilience"]
        self.assertNotIn("answer_handles_followup", prep_checks)
        self.assertTrue({"counterargument_followup_addressed", "validation_followup_addressed"}.issubset(set(followup_checks)))
        self.assertTrue(set(prep_checks).isdisjoint(set(followup_checks)))

    def test_contrastive_judgment_not_locked_to_single_phrase(self) -> None:
        checks = self.objective_checks()["expression.conclusion_first"]
        self.assertNotIn("conclusion_names_not_x_but_y", checks)
        self.assertIn("contrastive_judgment_case_specific", checks)

    def test_asset_card_does_not_duplicate_thinking_depth_scoring(self) -> None:
        checks = self.objective_checks()["expression.case_asset_card_transfer"]
        forbidden = {
            "core_conflict_present",
            "system_relation_present",
            "value_flow_present",
            "do_dont_validate_present",
        }
        self.assertTrue(forbidden.isdisjoint(set(checks)))
        self.assertIn("asset_card_inherits_core_judgment", checks)
        self.assertIn("reusable_pattern_with_transfer_boundary", checks)

    def test_all_objective_checks_have_check_type_should_pass(self) -> None:
        check_map = read_yaml("validator-check-map.yaml")
        registry = check_map.get("objective_checks", {})
        allowed_types = set(check_map["check_types"])
        missing = []
        invalid_types = []
        for item_id, checks in self.objective_checks().items():
            for check in checks:
                if check not in registry:
                    missing.append(f"{item_id}.{check}")
                elif registry[check]["check_type"] not in allowed_types:
                    invalid_types.append(f"{item_id}.{check}")
        self.assertEqual([], missing)
        self.assertEqual([], invalid_types)


if __name__ == "__main__":
    unittest.main()
