#!/usr/bin/env python3
"""Contract tests for the Rubric v2.1 executable governance package."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]
RUBRIC_DIR = ROOT / "docs" / "quality" / "rubric-v2.1"


EXPECTED_FILES = (
    "rubric-v2.1.md",
    "rubric-enums.yaml",
    "rubric-score-anchors.yaml",
    "reviewer-output.schema.json",
    "claim-evidence-map.schema.json",
    "failure-object.schema.json",
    "calibration-tests.yaml",
    "repair-rerun-map.yaml",
    "validator-check-map.yaml",
)


def read_yaml(name: str):
    return yaml.safe_load((RUBRIC_DIR / name).read_text(encoding="utf-8"))


def read_json(name: str):
    return json.loads((RUBRIC_DIR / name).read_text(encoding="utf-8"))


class RubricV21GovernanceTests(unittest.TestCase):
    def test_expected_files_exist(self) -> None:
        for filename in EXPECTED_FILES:
            with self.subTest(filename=filename):
                self.assertTrue((RUBRIC_DIR / filename).is_file())

    def test_enums_are_the_single_source_of_truth(self) -> None:
        enums = read_yaml("rubric-enums.yaml")
        for key in (
            "item_ids",
            "failure_types",
            "decision_states",
            "content_repair_targets",
            "system_repair_targets",
            "gate_ids",
            "check_types",
        ):
            with self.subTest(enum=key):
                self.assertIn(key, enums)
                self.assertIsInstance(enums[key], list)
                self.assertEqual(len(enums[key]), len(set(enums[key])))

        required_item_ids = {
            "thinking.eightq_reasoning_validity",
            "thinking.causal_mechanism",
            "thinking.final_tradeoff_validation",
            "content.fact_support_core_claim",
            "expression.prep_scqa_quality",
        }
        self.assertTrue(required_item_ids.issubset(set(enums["item_ids"])))
        forbidden_aliases = {
            "eightq_validity",
            "8q_reasoning",
            "core_claim_fact_support",
        }
        self.assertTrue(forbidden_aliases.isdisjoint(set(enums["item_ids"])))

    def test_score_anchors_cover_every_item_id_with_full_score_ranges(self) -> None:
        enums = read_yaml("rubric-enums.yaml")
        anchors = read_yaml("rubric-score-anchors.yaml")
        item_ids = set(enums["item_ids"])
        anchored_item_ids = set(anchors["items"])
        self.assertEqual(item_ids, anchored_item_ids)

        account_totals = {"thinking_depth": 0, "content_quality": 0, "expression_quality": 0}
        for item_id, item in anchors["items"].items():
            with self.subTest(item_id=item_id):
                max_score = item["max_score"]
                objective_checks = item["objective_checks"]
                score_anchors = item["score_anchors"]
                self.assertGreaterEqual(len(objective_checks), max_score)
                self.assertEqual(set(range(max_score + 1)), set(score_anchors))
                previous_required_count = -1
                for score in range(max_score + 1):
                    anchor = score_anchors[score]
                    self.assertEqual(f"{score}分", anchor["label"])
                    self.assertIn("observable_rule", anchor)
                    self.assertIsInstance(anchor["required_checks"], list)
                    self.assertTrue(set(anchor["required_checks"]).issubset(objective_checks))
                    self.assertGreaterEqual(
                        len(anchor["required_checks"]),
                        previous_required_count,
                    )
                    previous_required_count = len(anchor["required_checks"])
                self.assertEqual([], score_anchors[0]["required_checks"])
                self.assertIn("failure_if", score_anchors[0])
                self.assertEqual(set(objective_checks), set(score_anchors[max_score]["required_checks"]))
                self.assertGreaterEqual(len(item["bad_patterns"]), 2)
                self.assertGreaterEqual(len(item["full_score_requires"]), 2)
                self.assertGreaterEqual(len(item["cannot_score_above"]), 1)
                account_totals[item["primary_account"]] += max_score

        self.assertEqual(
            {"thinking_depth": 45, "content_quality": 30, "expression_quality": 25},
            account_totals,
        )

    def test_reviewer_schema_captures_score_lifecycle_and_formula_checks(self) -> None:
        schema = read_json("reviewer-output.schema.json")
        jsonschema.Draft202012Validator.check_schema(schema)

        item_props = schema["$defs"]["item_review"]["properties"]
        for field in (
            "raw_score",
            "caps_applied",
            "capped_score",
            "deductions_applied",
            "adjusted_score",
            "final_score",
            "required_evidence_points",
            "item_evidence_sufficiency",
        ):
            with self.subTest(field=field):
                self.assertIn(field, item_props)

        account_props = schema["$defs"]["account_score"]["properties"]
        for field in (
            "account_raw_score",
            "account_cap_applied",
            "account_final_score",
        ):
            with self.subTest(field=field):
                self.assertIn(field, account_props)

        case_props = schema["$defs"]["case_review"]["properties"]
        for field in (
            "case_raw_total",
            "case_global_cap_applied",
            "case_final_total",
            "case_decision",
            "publish_allowed",
        ):
            with self.subTest(field=field):
                self.assertIn(field, case_props)

        formula_checks = set(schema["x_formula_checks"])
        self.assertIn("capped_score <= raw_score", formula_checks)
        self.assertIn("adjusted_score <= capped_score", formula_checks)
        self.assertIn("final_score == adjusted_score", formula_checks)
        self.assertIn(
            "account_raw_score == sum(item.final_score for account items)",
            formula_checks,
        )
        self.assertIn(
            "case_raw_total == sum(account.account_final_score)",
            formula_checks,
        )

    def test_claim_evidence_map_requires_traceable_source_objects(self) -> None:
        schema = read_json("claim-evidence-map.schema.json")
        jsonschema.Draft202012Validator.check_schema(schema)
        fact_props = schema["$defs"]["supporting_fact"]["properties"]
        source = fact_props["source"]
        self.assertEqual(
            {
                "title",
                "url",
                "source_type",
                "published_at",
                "accessed_at",
                "fact_confidence",
            },
            set(source["required"]),
        )
        self.assertEqual(
            ["official_doc", "github_repo", "paper", "media", "ai_hot", "community"],
            source["properties"]["source_type"]["enum"],
        )
        self.assertEqual(["A", "B", "C", "D"], source["properties"]["fact_confidence"]["enum"])
        self.assertIn(
            "C/D facts cannot support core_claim",
            schema["x_governance_rules"],
        )

    def test_failure_schema_separates_decision_publish_and_repair(self) -> None:
        schema = read_json("failure-object.schema.json")
        jsonschema.Draft202012Validator.check_schema(schema)
        props = schema["properties"]
        for field in (
            "decision_state",
            "publish_allowed",
            "repair_action",
            "retry_budget",
            "content_changed",
            "html_stale",
            "must_rerender_html",
            "must_rerun_gates",
        ):
            with self.subTest(field=field):
                self.assertIn(field, props)

        retry_props = props["retry_budget"]["properties"]
        self.assertEqual(2, retry_props["max_retries_per_gate"]["const"])
        self.assertIn(
            "content_changed implies html_stale and must_rerender_html",
            schema["x_formula_checks"],
        )

    def test_calibration_tests_distinguish_fixture_classes(self) -> None:
        calibration = read_yaml("calibration-tests.yaml")
        self.assertEqual(
            {
                "hard_fail",
                "soft_repair",
                "good_pass",
                "human_preference",
            },
            set(calibration["fixture_classes"]),
        )
        fixtures = calibration["fixtures"]
        for name in (
            "v7_failure_sample",
            "empty_8q_shell_sample",
            "news_summary_sample",
            "v3_target_sample",
            "v6_target_sample",
            "human_preference_sample",
        ):
            with self.subTest(fixture=name):
                self.assertIn(name, fixtures)
                self.assertIn("expected_decision", fixtures[name])

        self.assertIn("PUBLISH_BLOCK", fixtures["v7_failure_sample"]["expected_decision"])
        self.assertEqual("PASS", fixtures["v3_target_sample"]["expected_decision"])
        self.assertIn("publish_block", fixtures["v3_target_sample"]["forbidden"])

    def test_repair_rerun_map_marks_html_stale_after_content_changes(self) -> None:
        rerun_map = read_yaml("repair-rerun-map.yaml")
        self.assertTrue(rerun_map["content_change_rule"]["html_stale"])
        self.assertTrue(rerun_map["content_change_rule"]["must_rerender_html"])
        self.assertEqual(["G6", "G7", "G8"], rerun_map["content_change_rule"]["must_rerun_gates"])
        self.assertEqual(
            ["G3", "G5", "rubric_scoring", "G6", "G7", "G8"],
            rerun_map["repair_targets"]["rewrite_8q_reasoning"]["must_rerun_gates"],
        )

    def test_validator_check_map_separates_machine_and_judgment_work(self) -> None:
        check_map = read_yaml("validator-check-map.yaml")
        required_types = {"machine_check", "heuristic_check", "llm_review", "human_review"}
        self.assertEqual(required_types, set(check_map["check_types"]))
        checks = check_map["checks"]
        self.assertEqual("machine_check", checks["eightq_question_count"]["check_type"])
        self.assertEqual("llm_review", checks["method_generates_insight"]["check_type"])
        self.assertEqual("human_review", checks["career_asset_preference"]["check_type"])

    def test_rubric_document_contains_final_locking_rules(self) -> None:
        content = (RUBRIC_DIR / "rubric-v2.1.md").read_text(encoding="utf-8")
        required_terms = (
            "Case-level / Daily-level 聚合协议",
            "禁止跨 Case 补偿",
            "分数生命周期",
            "Claim Evidence Map",
            "rubric-score-anchors.yaml",
            "Decision FSM",
            "Second review is not an override mechanism",
            "任何 Markdown 内容修复都会使已有 HTML 失效",
            "生成者自评不得作为放行依据",
        )
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, content)


if __name__ == "__main__":
    unittest.main()
