#!/usr/bin/env python3
"""Executable governance checks for Rubric v2.1.

JSON Schema validates shape. This module validates the governance rules that
require cross-field, cross-file, and score-lifecycle reasoning.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import jsonschema
import yaml


EXPECTED_CASE_IDS = ("case_a", "case_b", "case_c")
EXPECTED_ACCOUNT_IDS = ("thinking_depth", "content_quality", "expression_quality")
FINAL_GATE_IDS = ("G6", "G7", "G8")
NON_PASS_DECISIONS = {
    "REVIEW",
    "REWRITE_MODULE",
    "REWRITE_CASE",
    "REPLACE_CASE",
    "FAIL_DAILY",
    "PUBLISH_BLOCK",
    "USER_REVIEW_REQUIRED",
}
BLOCKING_DECISIONS = {"FAIL_DAILY", "PUBLISH_BLOCK"}
EVIDENCE_CAPS = {
    "PARTIAL": "partial",
    "INSUFFICIENT": "insufficient",
    "MISSING": "missing",
}


def validate_reviewer_output(payload: dict, rubric_dir: Path) -> list[str]:
    """Validate reviewer output against schema and governance rules."""

    ctx = _RubricContext(rubric_dir)
    errors = _schema_errors(payload, ctx.json("reviewer-output.schema.json"))

    if payload.get("case_score_policy") != "each_deep_case_scored_independently_100":
        errors.append("case_score_policy must equal each_deep_case_scored_independently_100")
    if payload.get("daily_score_policy") != "no_cross_case_compensation":
        errors.append("daily_score_policy must equal no_cross_case_compensation")

    if payload.get("reviewer_output_valid") is False and payload.get("publish_allowed") is True:
        errors.append("reviewer_output_valid=false requires publish_allowed=false")

    case_reviews = payload.get("case_reviews", [])
    _check_exact_set(
        errors,
        "case_reviews",
        [case.get("case_id") for case in case_reviews if isinstance(case, dict)],
        set(EXPECTED_CASE_IDS),
    )

    if len(case_reviews) != 3:
        errors.append(f"case_reviews.length must be 3, got {len(case_reviews)}")

    for case_index, case_review in enumerate(case_reviews):
        if not isinstance(case_review, dict):
            errors.append(f"case_reviews[{case_index}] must be object")
            continue
        _validate_case_review(case_review, case_index, ctx, errors)

    if payload.get("daily_decision") == "PASS":
        for index, case_review in enumerate(case_reviews):
            decision = case_review.get("case_decision") if isinstance(case_review, dict) else None
            publish_allowed = case_review.get("publish_allowed") if isinstance(case_review, dict) else None
            if decision != "PASS":
                errors.append(
                    f"daily_decision cannot be PASS when case_reviews[{index}].case_decision={decision}"
                )
            if publish_allowed is not True:
                errors.append(
                    f"daily_decision PASS requires case_reviews[{index}].publish_allowed=true"
                )

    for index, case_review in enumerate(case_reviews):
        if not isinstance(case_review, dict):
            continue
        if case_review.get("case_decision") in BLOCKING_DECISIONS and payload.get("publish_allowed") is True:
            errors.append(
                f"publish_allowed must be false when case_reviews[{index}].case_decision={case_review.get('case_decision')}"
            )

    gate_statuses = payload.get("gate_statuses")
    if gate_statuses is not None:
        for gate_id in FINAL_GATE_IDS:
            if gate_statuses.get(gate_id) != "PASS":
                errors.append(f"gate_statuses.{gate_id} must be PASS for daily PASS")
        if payload.get("daily_decision") == "PASS" and any(
            gate_statuses.get(gate_id) != "PASS" for gate_id in FINAL_GATE_IDS
        ):
            errors.append("daily_decision PASS requires G6/G7/G8 PASS")

    if payload.get("daily_decision") == "PASS" and payload.get("reviewer_output_valid") is not True:
        errors.append("daily_decision PASS requires reviewer_output_valid=true")
    if payload.get("publish_allowed") is True and payload.get("reviewer_output_valid") is not True:
        errors.append("publish_allowed=true requires reviewer_output_valid=true")

    return errors


def validate_failure_object(payload: dict, rubric_dir: Path) -> list[str]:
    """Validate a failure package object against enum and repair semantics."""

    ctx = _RubricContext(rubric_dir)
    errors = _schema_errors(payload, ctx.json("failure-object.schema.json"))
    enums = ctx.enums

    failure_type = payload.get("failure_type")
    if failure_type not in enums["failure_types"]:
        errors.append(f"failure_type must be registered enum, got {failure_type!r}")

    decision_state = payload.get("decision_state")
    if decision_state not in enums["decision_states"]:
        errors.append(f"decision_state must be registered enum, got {decision_state!r}")

    repair_action = payload.get("repair_action")
    if repair_action not in enums["content_repair_targets"]:
        errors.append(f"repair_action must be registered content_repair_target, got {repair_action!r}")

    content_repair_target = payload.get("content_repair_target")
    if content_repair_target not in enums["content_repair_targets"]:
        errors.append(
            f"content_repair_target must be registered content_repair_target, got {content_repair_target!r}"
        )

    for index, target in enumerate(payload.get("system_repair_target", [])):
        if target not in enums["system_repair_targets"]:
            errors.append(f"system_repair_target[{index}] must be registered enum, got {target!r}")

    for index, gate_id in enumerate(payload.get("must_rerun_gates", [])):
        if gate_id not in enums["gate_ids"]:
            errors.append(f"must_rerun_gates[{index}] must be registered gate_id, got {gate_id!r}")

    if failure_type == "HTML_CONTENT_LOSS":
        if decision_state != "PUBLISH_BLOCK":
            errors.append("decision_state must be PUBLISH_BLOCK when failure_type=HTML_CONTENT_LOSS")
        if payload.get("publish_allowed") is not False:
            errors.append("publish_allowed must be false when failure_type=HTML_CONTENT_LOSS")

    if payload.get("reviewer_output_valid") is False and payload.get("publish_allowed") is True:
        errors.append("reviewer_output_valid=false requires publish_allowed=false")

    if payload.get("content_changed") is True:
        if payload.get("html_stale") is not True:
            errors.append("html_stale must be true when content_changed=true")
        if payload.get("must_rerender_html") is not True:
            errors.append("must_rerender_html must be true when content_changed=true")
        gates = set(payload.get("must_rerun_gates", []))
        missing_gates = [gate_id for gate_id in FINAL_GATE_IDS if gate_id not in gates]
        if missing_gates:
            errors.append(
                f"must_rerun_gates must include G6/G7/G8 when content_changed=true; missing {missing_gates}"
            )

    return errors


def validate_claim_evidence_map(payload: dict, rubric_dir: Path) -> list[str]:
    """Validate Claim Evidence Map governance rules."""

    ctx = _RubricContext(rubric_dir)
    errors = _schema_errors(payload, ctx.json("claim-evidence-map.schema.json"))
    claims = payload.get("claims", [])

    if not 1 <= len(claims) <= 3:
        errors.append(f"claims must contain 1-3 core claims, got {len(claims)}")

    for claim_index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            errors.append(f"claims[{claim_index}] must be object")
            continue

        facts = claim.get("supporting_facts", [])
        if not facts:
            errors.append(f"claims[{claim_index}].supporting_facts must not be empty")

        ab_fact_count = 0
        claim_type = claim.get("claim_type")
        support_level = claim.get("support_level")
        for fact_index, fact in enumerate(facts):
            source = fact.get("source", {}) if isinstance(fact, dict) else {}
            source_path = f"claims[{claim_index}].supporting_facts[{fact_index}].source"
            for field in ("title", "url", "accessed_at", "fact_confidence"):
                if not _present(source.get(field)):
                    errors.append(f"{source_path}.{field} must be non-empty")
            if not _present(fact.get("supports_claim_how") if isinstance(fact, dict) else None):
                errors.append(
                    f"claims[{claim_index}].supporting_facts[{fact_index}].supports_claim_how must be non-empty"
                )

            fact_confidence = source.get("fact_confidence")
            if fact_confidence in {"A", "B"}:
                ab_fact_count += 1
            if claim_type == "core_judgment" and fact_confidence in {"C", "D"}:
                errors.append(
                    f"{source_path}.fact_confidence C/D facts cannot support core_claim"
                )

        if support_level == "SUFFICIENT" and ab_fact_count == 0:
            errors.append(f"claims[{claim_index}].support_level=SUFFICIENT requires at least one A/B fact")

        if support_level in {"INSUFFICIENT", "MISSING"} and "final_tradeoff" in str(
            claim.get("decision_impact", "")
        ):
            errors.append(
                f"claims[{claim_index}].decision_impact cannot support final_tradeoff when support_level={support_level}"
            )

    return errors


def validate_anchor_quality(rubric_dir: Path) -> list[str]:
    """Validate anchor-quality hardening beyond the contract tests."""

    ctx = _RubricContext(rubric_dir)
    errors: list[str] = []
    anchors = ctx.anchors["items"]
    check_map = ctx.yaml("validator-check-map.yaml")
    registered_checks = check_map.get("objective_checks", {})
    allowed_types = set(check_map.get("check_types", []))
    forbidden_exact = {
        "cause_variables_named",
        "result_variables_named",
        "mediator_variables_named",
        "pattern_named",
        "stakeholder_roles_named",
        "alternative_judgment_named",
        "stakeholder_count_ge_4",
        "source_count_ge_3",
        "ai_hot_marked_signal_only",
        "answer_handles_followup",
        "conclusion_names_not_x_but_y",
    }
    forbidden_suffixes = ("_named", "_present")

    for item_id, anchor in anchors.items():
        checks = anchor.get("objective_checks", [])
        for check in checks:
            path = f"items.{item_id}.objective_checks.{check}"
            if check in forbidden_exact or check.endswith(forbidden_suffixes):
                errors.append(f"{path} is too easy to satisfy by point-name compliance")
            if check not in registered_checks:
                errors.append(f"{path} missing from validator-check-map.yaml objective_checks")
            elif registered_checks[check].get("check_type") not in allowed_types:
                errors.append(f"{path} has invalid check_type={registered_checks[check].get('check_type')}")

        max_score = anchor.get("max_score")
        if max_score in anchor.get("score_anchors", {}):
            required = set(anchor["score_anchors"][max_score].get("required_checks", []))
            missing = set(checks) - required
            if missing:
                errors.append(f"items.{item_id}.score_anchors[{max_score}].required_checks missing {sorted(missing)}")

    prep = set(anchors["expression.prep_scqa_quality"]["objective_checks"])
    followup = set(anchors["expression.interview_followup_resilience"]["objective_checks"])
    overlap = prep & followup
    if overlap:
        errors.append(f"expression.prep_scqa_quality overlaps followup scoring checks: {sorted(overlap)}")

    return errors


def _validate_case_review(case_review: dict, case_index: int, ctx: "_RubricContext", errors: list[str]) -> None:
    path = f"case_reviews[{case_index}]"
    item_reviews = case_review.get("item_reviews", [])
    _check_exact_set(
        errors,
        f"{path}.item_reviews",
        [item.get("item_id") for item in item_reviews if isinstance(item, dict)],
        set(ctx.enums["item_ids"]),
    )

    account_scores = case_review.get("account_scores", [])
    _check_exact_set(
        errors,
        f"{path}.account_scores",
        [account.get("account_id") for account in account_scores if isinstance(account, dict)],
        set(EXPECTED_ACCOUNT_IDS),
    )

    item_final_by_account = {account_id: 0 for account_id in EXPECTED_ACCOUNT_IDS}
    for item_index, item in enumerate(item_reviews):
        if not isinstance(item, dict):
            errors.append(f"{path}.item_reviews[{item_index}] must be object")
            continue
        _validate_item_review(item, item_index, ctx, path, errors)
        account_id = item.get("primary_account")
        if account_id in item_final_by_account:
            item_final_by_account[account_id] += _num(item.get("final_score"))

    account_final_sum = 0
    for account_index, account in enumerate(account_scores):
        if not isinstance(account, dict):
            errors.append(f"{path}.account_scores[{account_index}] must be object")
            continue
        account_id = account.get("account_id")
        account_path = f"{path}.account_scores[{account_index}]"
        expected_raw = item_final_by_account.get(account_id)
        if expected_raw is not None and account.get("account_raw_score") != expected_raw:
            errors.append(
                f"{account_path}.account_raw_score must equal sum(item.final_score)={expected_raw}"
            )
        if _num(account.get("account_final_score")) > _num(account.get("account_raw_score")):
            errors.append(f"{account_path}.account_final_score must be <= account_raw_score")
        account_final_sum += _num(account.get("account_final_score"))

    if case_review.get("case_raw_total") != account_final_sum:
        errors.append(f"{path}.case_raw_total must equal sum(account.account_final_score)={account_final_sum}")
    if _num(case_review.get("case_final_total")) > _num(case_review.get("case_raw_total")):
        errors.append(f"{path}.case_final_total must be <= case_raw_total")

    global_cap = case_review.get("case_global_cap_applied")
    if isinstance(global_cap, dict):
        cap_value = _num(global_cap.get("max_allowed_score"))
        if _num(case_review.get("case_final_total")) > cap_value:
            errors.append(f"{path}.case_final_total exceeds active global cap {cap_value}")

    for claim_index, claim_map in enumerate(case_review.get("claim_evidence_map", [])):
        claim_errors = validate_claim_evidence_map(claim_map, ctx.rubric_dir)
        errors.extend(f"{path}.claim_evidence_map[{claim_index}].{error}" for error in claim_errors)


def _validate_item_review(item: dict, item_index: int, ctx: "_RubricContext", case_path: str, errors: list[str]) -> None:
    path = f"{case_path}.item_reviews[{item_index}]"
    item_id = item.get("item_id")
    anchor = ctx.anchors["items"].get(item_id)
    if anchor is None:
        errors.append(f"{path}.item_id {item_id!r} is not registered")
        return

    max_score = _num(item.get("max_score"))
    if max_score != anchor.get("max_score"):
        errors.append(f"{path}.max_score must equal rubric anchor max_score={anchor.get('max_score')}")
    if item.get("primary_account") != anchor.get("primary_account"):
        errors.append(f"{path}.primary_account must equal rubric anchor primary_account={anchor.get('primary_account')}")

    raw_score = _num(item.get("raw_score"))
    capped_score = _num(item.get("capped_score"))
    adjusted_score = _num(item.get("adjusted_score"))
    final_score = _num(item.get("final_score"))

    if not 0 <= raw_score <= max_score:
        errors.append(f"{path}.raw_score must be between 0 and max_score")
    if not 0 <= capped_score <= raw_score:
        errors.append(f"{path}.capped_score must be between 0 and raw_score")
    if not 0 <= adjusted_score <= capped_score:
        errors.append(f"{path}.adjusted_score must be between 0 and capped_score")
    if final_score != adjusted_score:
        errors.append(f"{path}.final_score must equal adjusted_score")
    if final_score > max_score:
        errors.append(f"{path}.final_score must be <= max_score")

    item_caps = [
        cap for cap in item.get("caps_applied", [])
        if isinstance(cap, dict) and cap.get("cap_type") == "item_cap"
    ]
    if item_caps:
        active_cap = min(_num(cap.get("max_allowed_score")) for cap in item_caps)
        if final_score > active_cap:
            errors.append(f"{path}.final_score exceeds active item cap {active_cap}")

    if final_score >= 2 and not item.get("positive_evidence"):
        errors.append(f"{path}.positive_evidence must not be empty when final_score>=2")
    if final_score < max_score and not item.get("missing_evidence"):
        errors.append(f"{path}.missing_evidence must not be empty when final_score<max_score")
    if final_score < max_score and not _present(item.get("why_not_higher")):
        errors.append(f"{path}.why_not_higher must not be empty when final_score<max_score")
    if item.get("decision") != "PASS" and not _present(item.get("repair_action")):
        errors.append(f"{path}.repair_action must not be empty when decision!=PASS")

    sufficiency = item.get("item_evidence_sufficiency")
    if sufficiency in EVIDENCE_CAPS and not item_caps:
        errors.append(f"{path}.caps_applied must include item_cap when item_evidence_sufficiency={sufficiency}")

    cap_limit = _sufficiency_limit(sufficiency, max_score)
    if cap_limit is not None and final_score > cap_limit:
        errors.append(f"{path}.final_score exceeds {sufficiency} evidence cap {cap_limit}")
    if sufficiency == "MISSING" and final_score != 0:
        errors.append(f"{path}.final_score must be 0 when item_evidence_sufficiency=MISSING")


def _schema_errors(payload: dict, schema: dict) -> list[str]:
    validator = jsonschema.Draft202012Validator(schema)
    errors = []
    for error in sorted(validator.iter_errors(payload), key=lambda err: list(err.path)):
        path = _path(list(error.path))
        errors.append(f"{path}: {error.message}" if path else error.message)
    return errors


def _check_exact_set(errors: list[str], path: str, values: list[Any], expected: set[str]) -> None:
    value_set = set(values)
    if len(values) != len(value_set):
        errors.append(f"{path} contains duplicate values")
    missing = sorted(expected - value_set)
    extra = sorted(value_set - expected)
    if missing:
        errors.append(f"{path} missing {missing}")
    if extra:
        errors.append(f"{path} contains unregistered {extra}")


def _sufficiency_limit(sufficiency: Any, max_score: int) -> int | None:
    if sufficiency == "PARTIAL":
        return math.floor(max_score * 0.7)
    if sufficiency == "INSUFFICIENT":
        return min(2, max_score)
    if sufficiency == "MISSING":
        return 0
    return None


def _path(parts: list[Any]) -> str:
    if not parts:
        return ""
    output = ""
    for part in parts:
        if isinstance(part, int):
            output += f"[{part}]"
        else:
            output += ("" if not output else ".") + str(part)
    return output


def _present(value: Any) -> bool:
    return value is not None and str(value).strip() != ""


def _num(value: Any) -> int:
    return int(value) if isinstance(value, int) else 0


class _RubricContext:
    def __init__(self, rubric_dir: Path) -> None:
        self.rubric_dir = Path(rubric_dir)
        self.enums = self.yaml("rubric-enums.yaml")
        self.anchors = self.yaml("rubric-score-anchors.yaml")

    def yaml(self, name: str) -> dict:
        return yaml.safe_load((self.rubric_dir / name).read_text(encoding="utf-8"))

    def json(self, name: str) -> dict:
        return json.loads((self.rubric_dir / name).read_text(encoding="utf-8"))


__all__ = [
    "validate_reviewer_output",
    "validate_failure_object",
    "validate_claim_evidence_map",
    "validate_anchor_quality",
]
