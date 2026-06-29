#!/usr/bin/env python3
"""Adversarial tests for the Rubric v2.1 executable governance validator."""

from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RUBRIC_DIR = ROOT / "docs" / "quality" / "rubric-v2.1"


def load_validator():
    path = RUBRIC_DIR / "rubric_governance_validator.py"
    spec = importlib.util.spec_from_file_location("rubric_governance_validator", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def read_yaml(name: str):
    return yaml.safe_load((RUBRIC_DIR / name).read_text(encoding="utf-8"))


def valid_source(confidence: str = "A") -> dict:
    return {
        "title": "Official product release",
        "url": "https://example.invalid/release",
        "source_type": "official_doc",
        "published_at": "2026-06-27",
        "accessed_at": "2026-06-28",
        "fact_confidence": confidence,
    }


def valid_claim_map(case_id: str = "case_a", claim_count: int = 1) -> dict:
    claims = []
    for idx in range(claim_count):
        claims.append(
            {
                "claim_id": f"{case_id}_core_claim_{idx + 1}",
                "claim_text": "核心判断由 A 级事实支撑。",
                "claim_type": "core_judgment",
                "supporting_facts": [
                    {
                        "fact": "官方发布记录了相关产品变化。",
                        "source": valid_source("A"),
                        "supports_claim_how": "该事实证明判断中的产品变化真实存在。",
                    }
                ],
                "support_level": "SUFFICIENT",
                "unsupported_parts": [],
                "decision_impact": "supports core_judgment",
            }
        )
    return {"case_id": case_id, "claims": claims}


def valid_item_review(item_id: str, anchor: dict) -> dict:
    max_score = anchor["max_score"]
    return {
        "item_id": item_id,
        "level": anchor["level"],
        "primary_account": anchor["primary_account"],
        "max_score": max_score,
        "raw_score": max_score,
        "caps_applied": [],
        "capped_score": max_score,
        "deductions_applied": [],
        "adjusted_score": max_score,
        "final_score": max_score,
        "anchor_matched": f"{max_score}分",
        "required_evidence_points": [
            {"point": "核心证据点", "support_level": "SUFFICIENT"}
        ],
        "item_evidence_sufficiency": "SUFFICIENT",
        "positive_evidence": [
            {
                "quote": "原文证据句",
                "location": "Case / section",
                "supports_what": "支撑该观察项",
                "evidence_sufficiency": "SUFFICIENT",
            }
        ],
        "missing_evidence": [],
        "deduction_reason": "",
        "why_not_higher": "",
        "repair_action": "",
        "decision": "PASS",
    }


def account_scores_from_items(items: list[dict]) -> list[dict]:
    minimums = {
        "thinking_depth": 38,
        "content_quality": 25,
        "expression_quality": 21,
    }
    accounts = []
    for account_id in ("thinking_depth", "content_quality", "expression_quality"):
        total = sum(
            item["final_score"]
            for item in items
            if item["primary_account"] == account_id
        )
        accounts.append(
            {
                "account_id": account_id,
                "account_raw_score": total,
                "account_cap_applied": None,
                "account_final_score": total,
                "min_pass_score": minimums[account_id],
            }
        )
    return accounts


def valid_case_review(case_id: str) -> dict:
    anchors = read_yaml("rubric-score-anchors.yaml")["items"]
    items = [
        valid_item_review(item_id, anchor)
        for item_id, anchor in anchors.items()
    ]
    accounts = account_scores_from_items(items)
    return {
        "case_id": case_id,
        "case_title": f"{case_id} title",
        "claim_evidence_map": [valid_claim_map(case_id)],
        "item_reviews": items,
        "account_scores": accounts,
        "case_raw_total": sum(account["account_final_score"] for account in accounts),
        "case_global_cap_applied": None,
        "case_final_total": sum(account["account_final_score"] for account in accounts),
        "case_decision": "PASS",
        "publish_allowed": True,
    }


def valid_reviewer_output() -> dict:
    return {
        "reviewer_output_valid": True,
        "reviewer_id": "independent-reviewer",
        "reviewed_at": "2026-06-28T00:00:00+08:00",
        "rubric_version": "2.1",
        "case_score_policy": "each_deep_case_scored_independently_100",
        "daily_score_policy": "no_cross_case_compensation",
        "daily_decision_rule": "all_cases_must_pass",
        "daily_decision": "PASS",
        "publish_allowed": True,
        "gate_statuses": {"G6": "PASS", "G7": "PASS", "G8": "PASS"},
        "case_reviews": [
            valid_case_review("case_a"),
            valid_case_review("case_b"),
            valid_case_review("case_c"),
        ],
    }


def valid_failure_object() -> dict:
    return {
        "failure_type": "NO_FINAL_TRADEOFF",
        "decision_state": "FAIL_DAILY",
        "publish_allowed": False,
        "repair_action": "rewrite_tradeoff_validation",
        "retry_budget": {
            "max_retries_per_gate": 2,
            "current_retry_count": 1,
            "retry_allowed": True,
        },
        "content_repair_required": True,
        "content_repair_target": "rewrite_tradeoff_validation",
        "system_repair_required": True,
        "system_repair_target": ["reviewer_prompt"],
        "regression_sample_required": True,
        "content_changed": True,
        "html_stale": True,
        "must_rerender_html": True,
        "must_rerun_gates": ["G5", "G6", "G7", "G8"],
    }


class RubricV21AdversarialTests(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = load_validator()

    def assert_errors_include(self, errors: list[str], *needles: str) -> None:
        joined = "\n".join(errors)
        self.assertTrue(errors, "expected validation errors")
        for needle in needles:
            self.assertIn(needle, joined)

    def validate_reviewer(self, payload: dict) -> list[str]:
        return self.validator.validate_reviewer_output(payload, RUBRIC_DIR)

    def validate_claims(self, payload: dict) -> list[str]:
        return self.validator.validate_claim_evidence_map(payload, RUBRIC_DIR)

    def validate_failure(self, payload: dict) -> list[str]:
        return self.validator.validate_failure_object(payload, RUBRIC_DIR)

    def test_case_a_case_b_case_c_should_pass(self) -> None:
        self.assertEqual([], self.validate_reviewer(valid_reviewer_output()))

    def test_duplicate_case_a_should_fail(self) -> None:
        payload = valid_reviewer_output()
        payload["case_reviews"][1] = copy.deepcopy(payload["case_reviews"][0])
        self.assert_errors_include(self.validate_reviewer(payload), "case_reviews", "duplicate")

    def test_missing_case_c_should_fail(self) -> None:
        payload = valid_reviewer_output()
        payload["case_reviews"] = payload["case_reviews"][:2]
        self.assert_errors_include(self.validate_reviewer(payload), "case_reviews", "case_c")

    def test_all_registered_items_should_pass(self) -> None:
        self.assertEqual([], self.validate_reviewer(valid_reviewer_output()))

    def test_bad_item_id_should_fail(self) -> None:
        payload = valid_reviewer_output()
        payload["case_reviews"][0]["item_reviews"][0]["item_id"] = "thinking.fake_item"
        self.assert_errors_include(self.validate_reviewer(payload), "item_reviews[0].item_id")

    def test_duplicate_item_id_should_fail(self) -> None:
        payload = valid_reviewer_output()
        payload["case_reviews"][0]["item_reviews"][1]["item_id"] = payload["case_reviews"][0]["item_reviews"][0]["item_id"]
        self.assert_errors_include(self.validate_reviewer(payload), "item_reviews", "duplicate")

    def test_missing_item_id_should_fail(self) -> None:
        payload = valid_reviewer_output()
        payload["case_reviews"][0]["item_reviews"].pop()
        self.assert_errors_include(self.validate_reviewer(payload), "item_reviews", "missing")

    def test_three_accounts_should_pass(self) -> None:
        self.assertEqual([], self.validate_reviewer(valid_reviewer_output()))

    def test_duplicate_thinking_depth_account_should_fail(self) -> None:
        payload = valid_reviewer_output()
        payload["case_reviews"][0]["account_scores"][1]["account_id"] = "thinking_depth"
        self.assert_errors_include(self.validate_reviewer(payload), "account_scores", "duplicate")

    def test_missing_expression_quality_should_fail(self) -> None:
        payload = valid_reviewer_output()
        payload["case_reviews"][0]["account_scores"].pop()
        self.assert_errors_include(self.validate_reviewer(payload), "account_scores", "expression_quality")

    def test_final_score_greater_than_max_should_fail(self) -> None:
        payload = valid_reviewer_output()
        item = payload["case_reviews"][0]["item_reviews"][0]
        item["final_score"] = item["max_score"] + 1
        item["adjusted_score"] = item["final_score"]
        self.assert_errors_include(self.validate_reviewer(payload), "item_reviews[0].final_score")

    def test_capped_score_greater_than_raw_should_fail(self) -> None:
        payload = valid_reviewer_output()
        payload["case_reviews"][0]["item_reviews"][0]["capped_score"] += 1
        self.assert_errors_include(self.validate_reviewer(payload), "item_reviews[0].capped_score")

    def test_adjusted_score_greater_than_capped_should_fail(self) -> None:
        payload = valid_reviewer_output()
        payload["case_reviews"][0]["item_reviews"][0]["adjusted_score"] += 1
        self.assert_errors_include(self.validate_reviewer(payload), "item_reviews[0].adjusted_score")

    def test_final_score_not_equal_adjusted_should_fail(self) -> None:
        payload = valid_reviewer_output()
        payload["case_reviews"][0]["item_reviews"][0]["final_score"] -= 1
        self.assert_errors_include(self.validate_reviewer(payload), "item_reviews[0].final_score")

    def test_account_total_mismatch_should_fail(self) -> None:
        payload = valid_reviewer_output()
        payload["case_reviews"][0]["account_scores"][0]["account_raw_score"] += 1
        self.assert_errors_include(self.validate_reviewer(payload), "account_scores[0].account_raw_score")

    def test_case_total_mismatch_should_fail(self) -> None:
        payload = valid_reviewer_output()
        payload["case_reviews"][0]["case_raw_total"] -= 1
        self.assert_errors_include(self.validate_reviewer(payload), "case_reviews[0].case_raw_total")

    def test_global_cap_not_applied_should_fail(self) -> None:
        payload = valid_reviewer_output()
        payload["case_reviews"][0]["case_global_cap_applied"] = {
            "cap_type": "global_cap",
            "reason": "NEWS_SUMMARY_ONLY",
            "max_allowed_score": 70,
        }
        self.assert_errors_include(self.validate_reviewer(payload), "case_reviews[0].case_final_total", "global cap")

    def test_wrong_item_max_score_should_fail(self) -> None:
        payload = valid_reviewer_output()
        payload["case_reviews"][0]["item_reviews"][0]["max_score"] += 1
        self.assert_errors_include(self.validate_reviewer(payload), "item_reviews[0].max_score")

    def test_wrong_primary_account_should_fail(self) -> None:
        payload = valid_reviewer_output()
        payload["case_reviews"][0]["item_reviews"][0]["primary_account"] = "content_quality"
        self.assert_errors_include(self.validate_reviewer(payload), "item_reviews[0].primary_account")

    def test_high_score_empty_evidence_should_fail(self) -> None:
        payload = valid_reviewer_output()
        payload["case_reviews"][0]["item_reviews"][0]["positive_evidence"] = []
        self.assert_errors_include(self.validate_reviewer(payload), "item_reviews[0].positive_evidence")

    def test_partial_sufficiency_without_cap_should_fail(self) -> None:
        payload = valid_reviewer_output()
        item = payload["case_reviews"][0]["item_reviews"][0]
        item["item_evidence_sufficiency"] = "PARTIAL"
        self.assert_errors_include(self.validate_reviewer(payload), "item_reviews[0].caps_applied")

    def test_partial_sufficiency_exceeds_floor_cap_should_fail(self) -> None:
        payload = valid_reviewer_output()
        item = payload["case_reviews"][0]["item_reviews"][0]
        item["item_evidence_sufficiency"] = "PARTIAL"
        item["caps_applied"] = [{"cap_type": "item_cap", "reason": "partial evidence", "max_allowed_score": 1}]
        self.assert_errors_include(self.validate_reviewer(payload), "item_reviews[0].final_score")

    def test_insufficient_sufficiency_score_above_2_should_fail(self) -> None:
        payload = valid_reviewer_output()
        item = payload["case_reviews"][0]["item_reviews"][0]
        item["item_evidence_sufficiency"] = "INSUFFICIENT"
        item["caps_applied"] = [{"cap_type": "item_cap", "reason": "insufficient evidence", "max_allowed_score": 2}]
        self.assert_errors_include(self.validate_reviewer(payload), "item_reviews[0].final_score")

    def test_missing_sufficiency_nonzero_score_should_fail(self) -> None:
        payload = valid_reviewer_output()
        item = payload["case_reviews"][0]["item_reviews"][0]
        item["item_evidence_sufficiency"] = "MISSING"
        item["caps_applied"] = [{"cap_type": "item_cap", "reason": "missing evidence", "max_allowed_score": 0}]
        self.assert_errors_include(self.validate_reviewer(payload), "item_reviews[0].final_score")

    def test_non_full_score_missing_why_not_higher_should_fail(self) -> None:
        payload = valid_reviewer_output()
        item = payload["case_reviews"][0]["item_reviews"][0]
        item["final_score"] -= 1
        item["adjusted_score"] = item["final_score"]
        item["capped_score"] = item["final_score"]
        item["raw_score"] = item["final_score"]
        item["missing_evidence"] = ["缺少证据"]
        item["why_not_higher"] = ""
        self.assert_errors_include(self.validate_reviewer(payload), "item_reviews[0].why_not_higher")

    def test_review_without_repair_action_should_fail(self) -> None:
        payload = valid_reviewer_output()
        item = payload["case_reviews"][0]["item_reviews"][0]
        item["decision"] = "REVIEW"
        item["repair_action"] = ""
        self.assert_errors_include(self.validate_reviewer(payload), "item_reviews[0].repair_action")

    def test_cd_fact_supports_core_claim_should_fail(self) -> None:
        payload = valid_claim_map()
        payload["claims"][0]["supporting_facts"][0]["source"]["fact_confidence"] = "C"
        self.assert_errors_include(self.validate_claims(payload), "claims[0].supporting_facts[0].source.fact_confidence")

    def test_sufficient_without_ab_fact_should_fail(self) -> None:
        payload = valid_claim_map()
        payload["claims"][0]["supporting_facts"][0]["source"]["fact_confidence"] = "D"
        payload["claims"][0]["support_level"] = "SUFFICIENT"
        self.assert_errors_include(self.validate_claims(payload), "claims[0].support_level", "A/B")

    def test_missing_source_url_should_fail(self) -> None:
        payload = valid_claim_map()
        payload["claims"][0]["supporting_facts"][0]["source"]["url"] = ""
        self.assert_errors_include(self.validate_claims(payload), "source.url")

    def test_missing_supports_claim_how_should_fail(self) -> None:
        payload = valid_claim_map()
        payload["claims"][0]["supporting_facts"][0]["supports_claim_how"] = ""
        self.assert_errors_include(self.validate_claims(payload), "supports_claim_how")

    def test_insufficient_claim_supports_final_tradeoff_should_fail(self) -> None:
        payload = valid_claim_map()
        payload["claims"][0]["support_level"] = "INSUFFICIENT"
        payload["claims"][0]["decision_impact"] = "supports final_tradeoff"
        self.assert_errors_include(self.validate_claims(payload), "claims[0].decision_impact")

    def test_one_to_three_core_claims_should_pass(self) -> None:
        self.assertEqual([], self.validate_claims(valid_claim_map(claim_count=3)))

    def test_zero_claims_should_fail(self) -> None:
        payload = valid_claim_map()
        payload["claims"] = []
        self.assert_errors_include(self.validate_claims(payload), "claims")

    def test_more_than_three_claims_should_fail(self) -> None:
        payload = valid_claim_map(claim_count=4)
        self.assert_errors_include(self.validate_claims(payload), "claims")

    def test_daily_pass_with_case_review_should_fail(self) -> None:
        payload = valid_reviewer_output()
        payload["case_reviews"][0]["case_decision"] = "REVIEW"
        self.assert_errors_include(self.validate_reviewer(payload), "daily_decision")

    def test_daily_pass_with_case_fail_should_fail(self) -> None:
        payload = valid_reviewer_output()
        payload["case_reviews"][0]["case_decision"] = "FAIL_DAILY"
        payload["case_reviews"][0]["publish_allowed"] = False
        self.assert_errors_include(self.validate_reviewer(payload), "daily_decision", "publish_allowed")

    def test_publish_true_with_reviewer_invalid_should_fail(self) -> None:
        payload = valid_reviewer_output()
        payload["reviewer_output_valid"] = False
        self.assert_errors_include(self.validate_reviewer(payload), "reviewer_output_valid", "publish_allowed")

    def test_publish_true_without_g6_g7_g8_should_fail_when_gate_statuses_present(self) -> None:
        payload = valid_reviewer_output()
        payload["gate_statuses"] = {"G6": "PASS"}
        self.assert_errors_include(self.validate_reviewer(payload), "gate_statuses", "G7")

    def test_cross_case_compensation_policy_change_should_fail(self) -> None:
        payload = valid_reviewer_output()
        payload["daily_score_policy"] = "average_score"
        self.assert_errors_include(self.validate_reviewer(payload), "daily_score_policy")

    def test_unknown_failure_type_should_fail(self) -> None:
        payload = valid_failure_object()
        payload["failure_type"] = "UNKNOWN_FAILURE"
        self.assert_errors_include(self.validate_failure(payload), "failure_type")

    def test_unknown_repair_target_should_fail(self) -> None:
        payload = valid_failure_object()
        payload["repair_action"] = "unknown_repair"
        self.assert_errors_include(self.validate_failure(payload), "repair_action")

    def test_unknown_system_repair_target_should_fail(self) -> None:
        payload = valid_failure_object()
        payload["system_repair_target"] = ["unknown_system_target"]
        self.assert_errors_include(self.validate_failure(payload), "system_repair_target[0]")

    def test_unknown_gate_id_should_fail(self) -> None:
        payload = valid_failure_object()
        payload["must_rerun_gates"] = ["G6", "G9"]
        self.assert_errors_include(self.validate_failure(payload), "must_rerun_gates[1]")

    def test_html_content_loss_not_publish_block_should_fail(self) -> None:
        payload = valid_failure_object()
        payload["failure_type"] = "HTML_CONTENT_LOSS"
        payload["decision_state"] = "FAIL_DAILY"
        self.assert_errors_include(self.validate_failure(payload), "decision_state", "PUBLISH_BLOCK")

    def test_content_changed_without_html_stale_should_fail(self) -> None:
        payload = valid_failure_object()
        payload["html_stale"] = False
        self.assert_errors_include(self.validate_failure(payload), "html_stale")

    def test_content_changed_without_rerender_should_fail(self) -> None:
        payload = valid_failure_object()
        payload["must_rerender_html"] = False
        self.assert_errors_include(self.validate_failure(payload), "must_rerender_html")

    def test_content_changed_missing_g6_g7_g8_should_fail(self) -> None:
        payload = valid_failure_object()
        payload["must_rerun_gates"] = ["G5", "G6"]
        self.assert_errors_include(self.validate_failure(payload), "must_rerun_gates", "G7")


if __name__ == "__main__":
    unittest.main()
