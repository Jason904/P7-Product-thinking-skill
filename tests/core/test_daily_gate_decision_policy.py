"""Focused contract tests for the pure Daily Gate decision policy guard."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import daily_gate_decision_policy as policy
from ai_daily_publishing_system.core import gates


REQUIRED_DECISION_FIELDS = {
    "allowed",
    "reason_code",
    "reason",
    "source",
    "decision",
    "evidence_policy_allowed",
    "conservative_block_requested",
    "conservative_block_reason_present",
    "decision_violations",
    "invariant_refs",
}

FORBIDDEN_RESULT_KEYS = {
    "gate_name",
    "from_state",
    "to_state",
    "state",
    "transition",
    "decision_result",
    "gate_passed",
    "PUBLISH_ALLOWED",
    "REVIEW_BLOCKED",
    "BADCASE_CREATED",
    "badcase_created",
    "failure_package",
    "public_url",
    "public_url_created",
    "published",
    "notification_sent",
    "artifact_path",
    "review_content",
    "hash_value",
    "ledger_written",
    "artifact_read",
    "artifact_written",
    "review_read",
    "file_stat",
    "hash_calculated",
    "ledger_read",
    "gate_executed",
    "transition_executed",
    "publisher",
    "notifier",
    "external_api_called",
}


def _explain(**overrides):
    markers = {
        "decision": gates.PASS,
        "evidence_policy_allowed": True,
        "conservative_block_requested": False,
        "conservative_block_reason_present": False,
    }
    markers.update(overrides)
    return policy.explain_daily_gate_decision_policy(**markers)


def test_pass_with_allowed_evidence_and_no_conservative_block_is_allowed():
    result = _explain()

    assert result["allowed"] is True
    assert result["reason_code"] == "DAILY_GATE_DECISION_ALLOWED"
    assert result["decision"] == gates.PASS
    assert result["decision_violations"] == ()


def test_blocked_with_evidence_failure_is_allowed():
    result = _explain(
        decision=gates.BLOCKED,
        evidence_policy_allowed=False,
    )

    assert result["allowed"] is True
    assert result["reason_code"] == "DAILY_GATE_DECISION_ALLOWED"
    assert result["decision"] == gates.BLOCKED
    assert result["decision_violations"] == ()


def test_blocked_with_evidence_allowed_and_conservative_reason_is_allowed():
    result = _explain(
        decision=gates.BLOCKED,
        conservative_block_requested=True,
        conservative_block_reason_present=True,
    )

    assert result["allowed"] is True
    assert result["reason_code"] == "DAILY_GATE_DECISION_ALLOWED"
    assert result["conservative_block_requested"] is True
    assert result["conservative_block_reason_present"] is True
    assert result["decision_violations"] == ()


def test_missing_decision_is_blocked():
    result = _explain(decision="")

    assert result["allowed"] is False
    assert result["reason_code"] == "DAILY_GATE_DECISION_MISSING"
    assert result["decision_violations"] == (
        "DAILY_GATE_DECISION_MISSING",
    )


def test_whitespace_decision_is_blocked():
    result = _explain(decision="   ")

    assert result["allowed"] is False
    assert result["reason_code"] == "DAILY_GATE_DECISION_MISSING"
    assert result["decision_violations"] == (
        "DAILY_GATE_DECISION_MISSING",
    )


def test_unknown_decision_is_blocked():
    result = _explain(decision="pass")

    assert result["allowed"] is False
    assert result["reason_code"] == "DAILY_GATE_DECISION_UNKNOWN"
    assert result["decision_violations"] == (
        "DAILY_GATE_DECISION_UNKNOWN",
    )


def test_pass_with_evidence_policy_blocked_is_blocked():
    result = _explain(evidence_policy_allowed=False)

    assert result["allowed"] is False
    assert result["reason_code"] == "PASS_WITH_EVIDENCE_POLICY_BLOCKED"
    assert result["decision_violations"] == (
        "PASS_WITH_EVIDENCE_POLICY_BLOCKED",
    )


def test_pass_with_conservative_block_requested_is_blocked():
    result = _explain(
        conservative_block_requested=True,
        conservative_block_reason_present=True,
    )

    assert result["allowed"] is False
    assert result["reason_code"] == "PASS_WITH_CONSERVATIVE_BLOCK_REQUESTED"
    assert result["decision_violations"] == (
        "PASS_WITH_CONSERVATIVE_BLOCK_REQUESTED",
    )


def test_blocked_with_evidence_allowed_without_conservative_block_is_blocked():
    result = _explain(decision=gates.BLOCKED)

    assert result["allowed"] is False
    assert (
        result["reason_code"]
        == "BLOCKED_WITH_EVIDENCE_POLICY_ALLOWED_WITHOUT_CONSERVATIVE_BLOCK"
    )
    assert result["decision_violations"] == (
        "BLOCKED_WITH_EVIDENCE_POLICY_ALLOWED_WITHOUT_CONSERVATIVE_BLOCK",
    )


def test_blocked_with_conservative_request_but_missing_reason_is_blocked():
    cases = (
        True,
        False,
    )

    for evidence_policy_allowed in cases:
        result = _explain(
            decision=gates.BLOCKED,
            evidence_policy_allowed=evidence_policy_allowed,
            conservative_block_requested=True,
            conservative_block_reason_present=False,
        )

        assert result["allowed"] is False
        assert (
            result["reason_code"]
            == "BLOCKED_WITH_CONSERVATIVE_BLOCK_REASON_MISSING"
        )
        assert result["decision_violations"] == (
            "BLOCKED_WITH_CONSERVATIVE_BLOCK_REASON_MISSING",
        )


def test_conservative_reason_without_request_is_blocked():
    result = _explain(conservative_block_reason_present=True)

    assert result["allowed"] is False
    assert (
        result["reason_code"]
        == "CONSERVATIVE_BLOCK_REASON_WITHOUT_REQUEST"
    )
    assert result["decision_violations"] == (
        "CONSERVATIVE_BLOCK_REASON_WITHOUT_REQUEST",
    )


def test_multi_violation_priority_and_collections_are_stable():
    unknown_result = _explain(
        decision="UNKNOWN",
        conservative_block_reason_present=True,
    )
    pass_result = _explain(
        evidence_policy_allowed=False,
        conservative_block_requested=True,
    )
    blocked_result = _explain(
        decision=gates.BLOCKED,
        conservative_block_reason_present=True,
    )

    assert unknown_result["reason_code"] == "DAILY_GATE_DECISION_UNKNOWN"
    assert unknown_result["decision_violations"] == (
        "DAILY_GATE_DECISION_UNKNOWN",
        "CONSERVATIVE_BLOCK_REASON_WITHOUT_REQUEST",
    )
    assert pass_result["reason_code"] == (
        "PASS_WITH_EVIDENCE_POLICY_BLOCKED"
    )
    assert pass_result["decision_violations"] == (
        "PASS_WITH_EVIDENCE_POLICY_BLOCKED",
        "PASS_WITH_CONSERVATIVE_BLOCK_REQUESTED",
    )
    assert blocked_result["reason_code"] == (
        "CONSERVATIVE_BLOCK_REASON_WITHOUT_REQUEST"
    )
    assert blocked_result["decision_violations"] == (
        "CONSERVATIVE_BLOCK_REASON_WITHOUT_REQUEST",
        "BLOCKED_WITH_EVIDENCE_POLICY_ALLOWED_WITHOUT_CONSERVATIVE_BLOCK",
    )


def test_bool_wrapper_matches_explanation():
    cases = (
        {
            "decision": gates.PASS,
            "evidence_policy_allowed": True,
            "conservative_block_requested": False,
            "conservative_block_reason_present": False,
        },
        {
            "decision": gates.BLOCKED,
            "evidence_policy_allowed": False,
            "conservative_block_requested": False,
            "conservative_block_reason_present": False,
        },
        {
            "decision": gates.BLOCKED,
            "evidence_policy_allowed": True,
            "conservative_block_requested": False,
            "conservative_block_reason_present": False,
        },
    )

    for markers in cases:
        explanation = policy.explain_daily_gate_decision_policy(**markers)
        assert (
            policy.is_daily_gate_decision_allowed(**markers)
            is explanation["allowed"]
        )


def test_result_shape_is_stable():
    result = _explain()

    assert set(result) == REQUIRED_DECISION_FIELDS


def test_result_does_not_include_state_transition_url_or_execution_fields():
    pass_result = _explain()
    blocked_result = _explain(
        decision=gates.BLOCKED,
        evidence_policy_allowed=False,
    )

    assert FORBIDDEN_RESULT_KEYS.isdisjoint(pass_result)
    assert FORBIDDEN_RESULT_KEYS.isdisjoint(blocked_result)


def test_allowed_pass_does_not_publish_or_create_publish_allowed():
    result = _explain()

    assert result["allowed"] is True
    assert "decision_policy_not_gate_execution" in result["invariant_refs"]
    assert "allowed_pass_not_publish_allowed" in result["invariant_refs"]
    assert "PUBLISH_ALLOWED" not in result.values()


def test_allowed_blocked_does_not_create_review_blocked_badcase_or_failure_package():
    result = _explain(
        decision=gates.BLOCKED,
        evidence_policy_allowed=False,
    )

    assert result["allowed"] is True
    assert "allowed_blocked_not_review_blocked" in result["invariant_refs"]
    assert "allowed_blocked_not_badcase_created" in result["invariant_refs"]
    assert "REVIEW_BLOCKED" not in result.values()
    assert "BADCASE_CREATED" not in result.values()


def test_reason_catalog_contains_only_executable_reason_codes():
    assert policy.DAILY_GATE_DECISION_POLICY_REASON_CODES == (
        "DAILY_GATE_DECISION_MISSING",
        "DAILY_GATE_DECISION_UNKNOWN",
        "CONSERVATIVE_BLOCK_REASON_WITHOUT_REQUEST",
        "PASS_WITH_EVIDENCE_POLICY_BLOCKED",
        "PASS_WITH_CONSERVATIVE_BLOCK_REQUESTED",
        "BLOCKED_WITH_EVIDENCE_POLICY_ALLOWED_WITHOUT_CONSERVATIVE_BLOCK",
        "BLOCKED_WITH_CONSERVATIVE_BLOCK_REASON_MISSING",
        "DAILY_GATE_DECISION_ALLOWED",
    )
    assert "DAILY_GATE_EXECUTION_FORBIDDEN" not in (
        policy.DAILY_GATE_DECISION_POLICY_REASON_CODES
    )
    assert "PUBLISH_OR_URL_BEHAVIOR_FORBIDDEN" not in (
        policy.DAILY_GATE_DECISION_POLICY_REASON_CODES
    )


def test_invariant_refs_capture_decision_policy_boundaries():
    result = _explain()
    required_policy_invariants = {
        "daily_gate_decision_policy_only",
        "decision_policy_not_gate_execution",
        "decision_policy_not_transition_mapping",
        "allowed_pass_not_publish_allowed",
        "allowed_blocked_not_review_blocked",
        "allowed_blocked_not_badcase_created",
        "no_quality_pass_no_public_url",
        "no_artifact_or_review_io",
        "no_hash_calculation",
        "no_ledger_write",
        "no_publish_or_notification",
        "no_public_url_behavior",
    }

    assert required_policy_invariants <= set(result["invariant_refs"])
    assert set(gates.GATE_INVARIANTS) <= set(result["invariant_refs"])


def test_policy_guard_does_not_mutate_gate_contracts():
    gate_decisions_before = gates.GATE_DECISIONS
    gate_invariants_before = gates.GATE_INVARIANTS
    gate_mappings_before = tuple(gates.GATE_TO_STATE_MAPPINGS.items())

    _explain()
    _explain(evidence_policy_allowed=False)
    _explain(
        decision=gates.BLOCKED,
        conservative_block_requested=True,
        conservative_block_reason_present=True,
    )
    policy.is_daily_gate_decision_allowed(
        decision=gates.PASS,
        evidence_policy_allowed=True,
        conservative_block_requested=False,
        conservative_block_reason_present=False,
    )

    assert gates.GATE_DECISIONS == gate_decisions_before
    assert gates.GATE_INVARIANTS == gate_invariants_before
    assert tuple(gates.GATE_TO_STATE_MAPPINGS.items()) == gate_mappings_before


def test_module_namespace_does_not_import_forbidden_behavior_modules_or_io_libraries():
    forbidden_names = {
        "gate_decision_mapper",
        "transition_guard",
        "daily_gate_evidence_policy",
        "artifact_inventory_policy",
        "pathlib",
        "os",
        "datetime",
        "hashlib",
        "logging",
        "subprocess",
        "requests",
    }

    assert forbidden_names.isdisjoint(policy.__dict__)


def test_no_artifact_review_hash_ledger_publish_notification_or_public_url_behavior_is_implied():
    results = (
        _explain(),
        _explain(
            decision=gates.BLOCKED,
            evidence_policy_allowed=False,
        ),
    )

    for result in results:
        assert FORBIDDEN_RESULT_KEYS.isdisjoint(result)
        assert result["source"] == (
            "daily_gate_decision_policy."
            "explain_daily_gate_decision_policy"
        )
