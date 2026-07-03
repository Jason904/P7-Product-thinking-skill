"""Focused contract tests for the pure Adapter Gate decision policy guard."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import adapter_gate_decision_policy as policy
from ai_daily_publishing_system.core import gates


REQUIRED_DECISION_FIELDS = {
    "allowed",
    "reason_code",
    "reason",
    "source",
    "decision",
    "evidence_policy_allowed",
    "blocking_adapter_markers_present",
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
    "RETRIEVING",
    "CONFIG_BLOCKED",
    "raw_credentials",
    "credential_values",
    "credential_names",
    "runtime_context",
    "config",
    "adapter_names",
    "adapter_outputs",
    "adapter_preflight_result",
    "adapter_failure_reason",
    "environment_name",
    "current_env",
    "public_url",
    "public_url_created",
    "published",
    "notification_sent",
    "artifact_path",
    "review_content",
    "hash_value",
    "ledger_written",
    "runtime_context_read",
    "config_read",
    "credential_read",
    "adapter_preflight_executed",
    "adapter_executed",
    "external_api_called",
    "artifact_read",
    "artifact_written",
    "review_read",
    "file_stat",
    "hash_calculated",
    "ledger_read",
    "failure_package",
    "badcase_created",
    "gate_executed",
    "transition_executed",
    "publisher",
    "notifier",
}


def _explain(**overrides):
    markers = {
        "decision": gates.PASS,
        "evidence_policy_allowed": True,
        "blocking_adapter_markers_present": False,
    }
    markers.update(overrides)
    return policy.explain_adapter_gate_decision_policy(**markers)


def test_valid_adapter_gate_pass_decision_is_allowed():
    result = _explain()

    assert result["allowed"] is True
    assert result["reason_code"] == "ADAPTER_GATE_DECISION_ALLOWED"
    assert result["decision"] == gates.PASS
    assert result["decision_violations"] == ()


def test_blocked_from_evidence_failure_is_allowed():
    result = _explain(
        decision=gates.BLOCKED,
        evidence_policy_allowed=False,
    )

    assert result["allowed"] is True
    assert result["reason_code"] == "ADAPTER_GATE_DECISION_ALLOWED"
    assert result["decision"] == gates.BLOCKED
    assert result["decision_violations"] == ()


def test_blocked_from_evidence_failure_with_blocking_marker_is_allowed():
    result = _explain(
        decision=gates.BLOCKED,
        evidence_policy_allowed=False,
        blocking_adapter_markers_present=True,
    )

    assert result["allowed"] is True
    assert result["reason_code"] == "ADAPTER_GATE_DECISION_ALLOWED"
    assert result["decision_violations"] == ()


def test_missing_decision_is_blocked():
    result = _explain(decision="")

    assert result["allowed"] is False
    assert result["reason_code"] == "ADAPTER_GATE_DECISION_MISSING"
    assert result["decision_violations"] == (
        "ADAPTER_GATE_DECISION_MISSING",
    )


def test_whitespace_decision_is_blocked():
    result = _explain(decision="   ")

    assert result["allowed"] is False
    assert result["reason_code"] == "ADAPTER_GATE_DECISION_MISSING"
    assert result["decision_violations"] == (
        "ADAPTER_GATE_DECISION_MISSING",
    )


def test_unknown_decisions_are_blocked():
    for decision in ("pass", "blocked", " PASS ", " BLOCKED ", "APPROVED"):
        result = _explain(decision=decision)

        assert result["allowed"] is False
        assert result["reason_code"] == "ADAPTER_GATE_DECISION_UNKNOWN"
        assert result["decision_violations"] == (
            "ADAPTER_GATE_DECISION_UNKNOWN",
        )


def test_pass_with_adapter_evidence_policy_blocked_is_blocked():
    result = _explain(evidence_policy_allowed=False)

    assert result["allowed"] is False
    assert (
        result["reason_code"]
        == "PASS_WITH_ADAPTER_EVIDENCE_POLICY_BLOCKED"
    )
    assert result["decision_violations"] == (
        "PASS_WITH_ADAPTER_EVIDENCE_POLICY_BLOCKED",
    )


def test_pass_with_blocking_adapter_markers_present_is_blocked():
    result = _explain(blocking_adapter_markers_present=True)

    assert result["allowed"] is False
    assert (
        result["reason_code"]
        == "PASS_WITH_BLOCKING_ADAPTER_MARKERS_PRESENT"
    )


def test_pass_with_evidence_failure_and_blocking_marker_collects_priority_violations():
    result = _explain(
        evidence_policy_allowed=False,
        blocking_adapter_markers_present=True,
    )

    assert result["allowed"] is False
    assert (
        result["reason_code"]
        == "PASS_WITH_ADAPTER_EVIDENCE_POLICY_BLOCKED"
    )
    assert result["decision_violations"] == (
        "PASS_WITH_ADAPTER_EVIDENCE_POLICY_BLOCKED",
        "PASS_WITH_BLOCKING_ADAPTER_MARKERS_PRESENT",
    )


def test_pass_with_evidence_allowed_and_blocking_marker_collects_marker_inconsistency():
    result = _explain(blocking_adapter_markers_present=True)

    assert result["reason_code"] == (
        "PASS_WITH_BLOCKING_ADAPTER_MARKERS_PRESENT"
    )
    assert result["decision_violations"] == (
        "PASS_WITH_BLOCKING_ADAPTER_MARKERS_PRESENT",
        "EVIDENCE_ALLOWED_WITH_BLOCKING_ADAPTER_MARKERS",
    )


def test_blocked_with_evidence_allowed_without_blocking_marker_is_blocked():
    result = _explain(decision=gates.BLOCKED)

    assert result["allowed"] is False
    assert result["reason_code"] == (
        "BLOCKED_WITH_ADAPTER_EVIDENCE_ALLOWED_WITHOUT_BLOCKING_MARKERS"
    )
    assert result["decision_violations"] == (
        "BLOCKED_WITH_ADAPTER_EVIDENCE_ALLOWED_WITHOUT_BLOCKING_MARKERS",
    )


def test_blocked_with_evidence_allowed_and_blocking_marker_is_marker_inconsistency():
    result = _explain(
        decision=gates.BLOCKED,
        blocking_adapter_markers_present=True,
    )

    assert result["allowed"] is False
    assert (
        result["reason_code"]
        == "EVIDENCE_ALLOWED_WITH_BLOCKING_ADAPTER_MARKERS"
    )
    assert result["decision_violations"] == (
        "EVIDENCE_ALLOWED_WITH_BLOCKING_ADAPTER_MARKERS",
    )


def test_unknown_decision_keeps_unknown_priority_over_marker_inconsistency():
    result = _explain(
        decision="UNKNOWN",
        blocking_adapter_markers_present=True,
    )

    assert result["allowed"] is False
    assert result["reason_code"] == "ADAPTER_GATE_DECISION_UNKNOWN"
    assert result["decision_violations"] == (
        "ADAPTER_GATE_DECISION_UNKNOWN",
        "EVIDENCE_ALLOWED_WITH_BLOCKING_ADAPTER_MARKERS",
    )


def test_allowed_result_has_empty_decision_violations():
    results = (
        _explain(),
        _explain(
            decision=gates.BLOCKED,
            evidence_policy_allowed=False,
        ),
        _explain(
            decision=gates.BLOCKED,
            evidence_policy_allowed=False,
            blocking_adapter_markers_present=True,
        ),
    )

    for result in results:
        assert result["allowed"] is True
        assert result["decision_violations"] == ()


def test_bool_wrapper_matches_explanation():
    cases = (
        {
            "decision": gates.PASS,
            "evidence_policy_allowed": True,
            "blocking_adapter_markers_present": False,
        },
        {
            "decision": gates.BLOCKED,
            "evidence_policy_allowed": False,
            "blocking_adapter_markers_present": True,
        },
        {
            "decision": gates.BLOCKED,
            "evidence_policy_allowed": True,
            "blocking_adapter_markers_present": False,
        },
    )

    for markers in cases:
        explanation = policy.explain_adapter_gate_decision_policy(**markers)
        assert (
            policy.is_adapter_gate_decision_allowed(**markers)
            is explanation["allowed"]
        )


def test_result_shape_is_stable():
    result = _explain()

    assert set(result) == REQUIRED_DECISION_FIELDS


def test_result_does_not_include_gate_state_credential_adapter_url_or_execution_fields():
    results = (
        _explain(),
        _explain(
            decision=gates.BLOCKED,
            evidence_policy_allowed=False,
        ),
    )

    for result in results:
        assert FORBIDDEN_RESULT_KEYS.isdisjoint(result)


def test_allowed_pass_is_not_adapter_gate_execution_or_retrieving():
    result = _explain()

    assert result["allowed"] is True
    assert (
        "decision_policy_not_adapter_gate_execution"
        in result["invariant_refs"]
    )
    assert "allowed_pass_not_retrieving" in result["invariant_refs"]
    assert "RETRIEVING" not in result.values()


def test_allowed_blocked_is_not_config_blocked():
    result = _explain(
        decision=gates.BLOCKED,
        evidence_policy_allowed=False,
    )

    assert result["allowed"] is True
    assert "allowed_blocked_not_config_blocked" in result["invariant_refs"]
    assert "CONFIG_BLOCKED" not in result.values()


def test_blocked_decision_does_not_create_failure_package_or_badcase():
    result = _explain(decision=gates.BLOCKED)

    assert result["allowed"] is False
    assert "blocked_decision_not_failure_package" in result["invariant_refs"]
    assert (
        "blocked_decision_not_badcase_created"
        in result["invariant_refs"]
    )
    assert "failure_package" not in result
    assert "badcase_created" not in result


def test_reason_catalog_contains_only_executable_reason_codes():
    assert policy.ADAPTER_GATE_DECISION_POLICY_REASON_CODES == (
        "ADAPTER_GATE_DECISION_MISSING",
        "ADAPTER_GATE_DECISION_UNKNOWN",
        "PASS_WITH_ADAPTER_EVIDENCE_POLICY_BLOCKED",
        "PASS_WITH_BLOCKING_ADAPTER_MARKERS_PRESENT",
        "EVIDENCE_ALLOWED_WITH_BLOCKING_ADAPTER_MARKERS",
        "BLOCKED_WITH_ADAPTER_EVIDENCE_ALLOWED_WITHOUT_BLOCKING_MARKERS",
        "ADAPTER_GATE_DECISION_ALLOWED",
    )
    forbidden_codes = {
        "ADAPTER_GATE_EXECUTION_FORBIDDEN",
        "RETRIEVING_GENERATION_FORBIDDEN",
        "CONFIG_BLOCKED_GENERATION_FORBIDDEN",
        "EXTERNAL_ADAPTER_CALL_FORBIDDEN",
        "CREDENTIAL_READ_FORBIDDEN",
    }
    assert forbidden_codes.isdisjoint(
        policy.ADAPTER_GATE_DECISION_POLICY_REASON_CODES
    )


def test_invariant_refs_capture_adapter_gate_decision_policy_boundaries():
    result = _explain()
    required_policy_invariants = {
        "adapter_gate_decision_policy_only",
        "decision_policy_not_adapter_gate_execution",
        "decision_policy_not_transition_mapping",
        "allowed_pass_not_retrieving",
        "allowed_blocked_not_config_blocked",
        "blocked_decision_not_failure_package",
        "blocked_decision_not_badcase_created",
        "no_runtime_context_config_or_credential_read",
        "no_adapter_preflight",
        "no_external_adapter_call",
        "no_raw_credentials",
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
    _explain(
        decision=gates.BLOCKED,
        evidence_policy_allowed=False,
        blocking_adapter_markers_present=True,
    )
    policy.is_adapter_gate_decision_allowed(
        decision=gates.PASS,
        evidence_policy_allowed=True,
        blocking_adapter_markers_present=False,
    )

    assert gates.GATE_DECISIONS == gate_decisions_before
    assert gates.GATE_INVARIANTS == gate_invariants_before
    assert tuple(gates.GATE_TO_STATE_MAPPINGS.items()) == gate_mappings_before


def test_module_namespace_does_not_import_forbidden_behavior_modules_or_io_libraries():
    forbidden_names = {
        "gate_decision_mapper",
        "transition_guard",
        "adapter_gate_evidence_policy",
        "daily_gate_evidence_policy",
        "daily_gate_decision_policy",
        "artifact_inventory_policy",
        "noop_completion_policy",
        "badcase_creation_policy",
        "artifacts",
        "states",
        "pathlib",
        "os",
        "datetime",
        "hashlib",
        "logging",
        "subprocess",
        "requests",
    }

    assert forbidden_names.isdisjoint(policy.__dict__)


def test_no_runtime_config_credential_adapter_artifact_hash_ledger_public_url_behavior_is_implied():
    results = (
        _explain(),
        _explain(decision=gates.BLOCKED),
    )

    for result in results:
        assert FORBIDDEN_RESULT_KEYS.isdisjoint(result)
        assert result["source"] == (
            "adapter_gate_decision_policy."
            "explain_adapter_gate_decision_policy"
        )
