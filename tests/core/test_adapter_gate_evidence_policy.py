"""Focused contract tests for the pure Adapter Gate evidence policy guard."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import adapter_gate_evidence_policy as policy
from ai_daily_publishing_system.core import gates


REQUIRED_DECISION_FIELDS = {
    "allowed",
    "reason_code",
    "reason",
    "source",
    "runtime_context_present",
    "runtime_profile_snapshot_ref_present",
    "runtime_profile_mode_is_manual_local_noop",
    "config_snapshot_ref_present",
    "adapter_configuration_declared",
    "required_credential_markers_present",
    "credential_redaction_passed",
    "publish_mode_is_noop",
    "notification_mode_is_noop",
    "eval_mode_declared",
    "adapter_capability_markers_present",
    "noop_policy_markers_present",
    "disabled_external_adapters_declared",
    "environment_safety_marker_present",
    "blocking_adapter_markers_present",
    "missing_evidence_markers",
    "failed_policy_markers",
    "mode_policy_violations",
    "adapter_policy_violations",
    "invariant_refs",
}

FORBIDDEN_RESULT_KEYS = {
    "gate_name",
    "decision",
    "gate_passed",
    "from_state",
    "to_state",
    "state",
    "transition",
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
    "gate_executed",
    "transition_executed",
    "publisher",
    "notifier",
}


def _valid_markers() -> dict[str, bool]:
    return {
        "runtime_context_present": True,
        "runtime_profile_snapshot_ref_present": True,
        "runtime_profile_mode_is_manual_local_noop": True,
        "config_snapshot_ref_present": True,
        "adapter_configuration_declared": True,
        "required_credential_markers_present": True,
        "credential_redaction_passed": True,
        "publish_mode_is_noop": True,
        "notification_mode_is_noop": True,
        "eval_mode_declared": True,
        "adapter_capability_markers_present": True,
        "noop_policy_markers_present": True,
        "disabled_external_adapters_declared": True,
        "environment_safety_marker_present": True,
        "blocking_adapter_markers_present": False,
    }


def _explain(**overrides: bool) -> dict[str, object]:
    markers = _valid_markers()
    markers.update(overrides)
    return policy.explain_adapter_gate_evidence_policy(**markers)


def test_valid_adapter_gate_evidence_markers_are_allowed():
    result = _explain()

    assert result["allowed"] is True
    assert result["reason_code"] == "ADAPTER_GATE_EVIDENCE_ALLOWED"
    assert result["missing_evidence_markers"] == ()
    assert result["failed_policy_markers"] == ()
    assert result["mode_policy_violations"] == ()
    assert result["adapter_policy_violations"] == ()


def test_runtime_context_missing_is_blocked():
    result = _explain(runtime_context_present=False)

    assert result["allowed"] is False
    assert result["reason_code"] == "RUNTIME_CONTEXT_MISSING"
    assert result["missing_evidence_markers"] == (
        "runtime_context_present",
    )


def test_runtime_profile_snapshot_ref_missing_is_blocked():
    result = _explain(runtime_profile_snapshot_ref_present=False)

    assert result["allowed"] is False
    assert (
        result["reason_code"]
        == "RUNTIME_PROFILE_SNAPSHOT_REF_MISSING"
    )
    assert result["missing_evidence_markers"] == (
        "runtime_profile_snapshot_ref_present",
    )


def test_runtime_profile_mode_not_manual_local_noop_is_blocked():
    result = _explain(
        runtime_profile_mode_is_manual_local_noop=False,
    )

    assert result["allowed"] is False
    assert (
        result["reason_code"]
        == "RUNTIME_PROFILE_MODE_NOT_MANUAL_LOCAL_NOOP"
    )
    assert result["failed_policy_markers"] == (
        "runtime_profile_mode_is_manual_local_noop",
    )
    assert result["mode_policy_violations"] == (
        "runtime_profile_mode_is_manual_local_noop",
    )


def test_config_snapshot_ref_missing_is_blocked():
    result = _explain(config_snapshot_ref_present=False)

    assert result["allowed"] is False
    assert result["reason_code"] == "CONFIG_SNAPSHOT_REF_MISSING"
    assert result["missing_evidence_markers"] == (
        "config_snapshot_ref_present",
    )


def test_adapter_configuration_not_declared_is_blocked():
    result = _explain(adapter_configuration_declared=False)

    assert result["allowed"] is False
    assert result["reason_code"] == "ADAPTER_CONFIGURATION_NOT_DECLARED"
    assert result["missing_evidence_markers"] == (
        "adapter_configuration_declared",
    )
    assert result["adapter_policy_violations"] == (
        "adapter_configuration_declared",
    )


def test_required_credential_markers_missing_is_blocked():
    result = _explain(required_credential_markers_present=False)

    assert result["allowed"] is False
    assert result["reason_code"] == "REQUIRED_CREDENTIAL_MARKERS_MISSING"
    assert result["missing_evidence_markers"] == (
        "required_credential_markers_present",
    )


def test_credential_redaction_not_passed_is_blocked():
    result = _explain(credential_redaction_passed=False)

    assert result["allowed"] is False
    assert result["reason_code"] == "CREDENTIAL_REDACTION_NOT_PASSED"
    assert result["failed_policy_markers"] == (
        "credential_redaction_passed",
    )


def test_publish_mode_not_noop_is_blocked():
    result = _explain(publish_mode_is_noop=False)

    assert result["allowed"] is False
    assert result["reason_code"] == "PUBLISH_MODE_NOT_NOOP"
    assert result["failed_policy_markers"] == (
        "publish_mode_is_noop",
    )
    assert result["mode_policy_violations"] == (
        "publish_mode_is_noop",
    )


def test_notification_mode_not_noop_is_blocked():
    result = _explain(notification_mode_is_noop=False)

    assert result["allowed"] is False
    assert result["reason_code"] == "NOTIFICATION_MODE_NOT_NOOP"
    assert result["failed_policy_markers"] == (
        "notification_mode_is_noop",
    )
    assert result["mode_policy_violations"] == (
        "notification_mode_is_noop",
    )


def test_eval_mode_not_declared_is_blocked():
    result = _explain(eval_mode_declared=False)

    assert result["allowed"] is False
    assert result["reason_code"] == "EVAL_MODE_NOT_DECLARED"
    assert result["missing_evidence_markers"] == (
        "eval_mode_declared",
    )


def test_adapter_capability_markers_missing_is_blocked():
    result = _explain(adapter_capability_markers_present=False)

    assert result["allowed"] is False
    assert result["reason_code"] == "ADAPTER_CAPABILITY_MARKERS_MISSING"
    assert result["missing_evidence_markers"] == (
        "adapter_capability_markers_present",
    )
    assert result["adapter_policy_violations"] == (
        "adapter_capability_markers_present",
    )


def test_noop_policy_markers_missing_is_blocked():
    result = _explain(noop_policy_markers_present=False)

    assert result["allowed"] is False
    assert result["reason_code"] == "NOOP_POLICY_MARKERS_MISSING"
    assert result["missing_evidence_markers"] == (
        "noop_policy_markers_present",
    )


def test_disabled_external_adapters_not_declared_is_blocked():
    result = _explain(disabled_external_adapters_declared=False)

    assert result["allowed"] is False
    assert (
        result["reason_code"]
        == "DISABLED_EXTERNAL_ADAPTERS_NOT_DECLARED"
    )
    assert result["missing_evidence_markers"] == (
        "disabled_external_adapters_declared",
    )
    assert result["adapter_policy_violations"] == (
        "disabled_external_adapters_declared",
    )


def test_environment_safety_marker_missing_is_blocked():
    result = _explain(environment_safety_marker_present=False)

    assert result["allowed"] is False
    assert result["reason_code"] == "ENVIRONMENT_SAFETY_MARKER_MISSING"
    assert result["missing_evidence_markers"] == (
        "environment_safety_marker_present",
    )


def test_blocking_adapter_markers_present_is_blocked():
    result = _explain(blocking_adapter_markers_present=True)

    assert result["allowed"] is False
    assert result["reason_code"] == "BLOCKING_ADAPTER_MARKERS_PRESENT"
    assert result["failed_policy_markers"] == (
        "blocking_adapter_markers_present",
    )
    assert result["adapter_policy_violations"] == (
        "blocking_adapter_markers_present",
    )


def test_multi_failure_priority_and_collections_are_stable():
    result = policy.explain_adapter_gate_evidence_policy(
        runtime_context_present=False,
        runtime_profile_snapshot_ref_present=False,
        runtime_profile_mode_is_manual_local_noop=False,
        config_snapshot_ref_present=False,
        adapter_configuration_declared=False,
        required_credential_markers_present=False,
        credential_redaction_passed=False,
        publish_mode_is_noop=False,
        notification_mode_is_noop=False,
        eval_mode_declared=False,
        adapter_capability_markers_present=False,
        noop_policy_markers_present=False,
        disabled_external_adapters_declared=False,
        environment_safety_marker_present=False,
        blocking_adapter_markers_present=True,
    )

    assert result["allowed"] is False
    assert result["reason_code"] == "RUNTIME_CONTEXT_MISSING"
    assert result["missing_evidence_markers"] == (
        "runtime_context_present",
        "runtime_profile_snapshot_ref_present",
        "config_snapshot_ref_present",
        "adapter_configuration_declared",
        "required_credential_markers_present",
        "eval_mode_declared",
        "adapter_capability_markers_present",
        "noop_policy_markers_present",
        "disabled_external_adapters_declared",
        "environment_safety_marker_present",
    )
    assert result["failed_policy_markers"] == (
        "runtime_profile_mode_is_manual_local_noop",
        "credential_redaction_passed",
        "publish_mode_is_noop",
        "notification_mode_is_noop",
        "blocking_adapter_markers_present",
    )
    assert result["mode_policy_violations"] == (
        "runtime_profile_mode_is_manual_local_noop",
        "publish_mode_is_noop",
        "notification_mode_is_noop",
    )
    assert result["adapter_policy_violations"] == (
        "adapter_configuration_declared",
        "adapter_capability_markers_present",
        "disabled_external_adapters_declared",
        "blocking_adapter_markers_present",
    )


def test_bool_wrapper_matches_explanation():
    cases = (
        _valid_markers(),
        {
            **_valid_markers(),
            "runtime_context_present": False,
        },
        {
            **_valid_markers(),
            "publish_mode_is_noop": False,
        },
        {
            **_valid_markers(),
            "blocking_adapter_markers_present": True,
        },
    )

    for markers in cases:
        explanation = policy.explain_adapter_gate_evidence_policy(**markers)
        assert (
            policy.is_adapter_gate_evidence_allowed(**markers)
            is explanation["allowed"]
        )


def test_result_shape_is_stable():
    result = _explain()

    assert set(result) == REQUIRED_DECISION_FIELDS


def test_result_does_not_include_gate_state_credential_adapter_url_or_execution_fields():
    allowed_result = _explain()
    blocked_result = _explain(runtime_context_present=False)

    assert FORBIDDEN_RESULT_KEYS.isdisjoint(allowed_result)
    assert FORBIDDEN_RESULT_KEYS.isdisjoint(blocked_result)


def test_allowed_result_is_not_adapter_gate_pass_or_retrieving():
    result = _explain()

    assert result["allowed"] is True
    assert "allowed_not_adapter_gate_pass" in result["invariant_refs"]
    assert "allowed_not_retrieving" in result["invariant_refs"]
    assert gates.PASS not in result.values()
    assert "RETRIEVING" not in result.values()


def test_blocked_result_is_not_config_blocked():
    result = _explain(runtime_context_present=False)

    assert result["allowed"] is False
    assert "blocked_not_config_blocked" in result["invariant_refs"]
    assert gates.BLOCKED not in result.values()
    assert "CONFIG_BLOCKED" not in result.values()


def test_reason_catalog_contains_only_executable_reason_codes():
    assert policy.ADAPTER_GATE_EVIDENCE_POLICY_REASON_CODES == (
        "RUNTIME_CONTEXT_MISSING",
        "RUNTIME_PROFILE_SNAPSHOT_REF_MISSING",
        "RUNTIME_PROFILE_MODE_NOT_MANUAL_LOCAL_NOOP",
        "CONFIG_SNAPSHOT_REF_MISSING",
        "ADAPTER_CONFIGURATION_NOT_DECLARED",
        "REQUIRED_CREDENTIAL_MARKERS_MISSING",
        "CREDENTIAL_REDACTION_NOT_PASSED",
        "PUBLISH_MODE_NOT_NOOP",
        "NOTIFICATION_MODE_NOT_NOOP",
        "EVAL_MODE_NOT_DECLARED",
        "ADAPTER_CAPABILITY_MARKERS_MISSING",
        "NOOP_POLICY_MARKERS_MISSING",
        "DISABLED_EXTERNAL_ADAPTERS_NOT_DECLARED",
        "ENVIRONMENT_SAFETY_MARKER_MISSING",
        "BLOCKING_ADAPTER_MARKERS_PRESENT",
        "ADAPTER_GATE_EVIDENCE_ALLOWED",
    )
    assert "ADAPTER_GATE_EXECUTION_FORBIDDEN" not in (
        policy.ADAPTER_GATE_EVIDENCE_POLICY_REASON_CODES
    )
    assert "EXTERNAL_ADAPTER_CALL_FORBIDDEN" not in (
        policy.ADAPTER_GATE_EVIDENCE_POLICY_REASON_CODES
    )
    assert "CREDENTIAL_READ_FORBIDDEN" not in (
        policy.ADAPTER_GATE_EVIDENCE_POLICY_REASON_CODES
    )


def test_invariant_refs_capture_adapter_gate_policy_boundaries():
    result = _explain()
    required_policy_invariants = {
        "adapter_gate_evidence_policy_only",
        "evidence_policy_not_adapter_gate_execution",
        "allowed_not_adapter_gate_pass",
        "allowed_not_retrieving",
        "blocked_not_config_blocked",
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
        "external_agents_cannot_bypass_later_gates",
    }

    assert required_policy_invariants <= set(result["invariant_refs"])
    assert set(gates.GATE_INVARIANTS) <= set(result["invariant_refs"])


def test_policy_guard_does_not_mutate_gate_contracts():
    gate_inputs_before = gates.ADAPTER_CONFIGURATION_GATE_INPUT_FIELDS
    gate_reason_codes_before = gates.ADAPTER_CONFIGURATION_GATE_REASON_CODES
    gate_invariants_before = gates.GATE_INVARIANTS
    gate_mappings_before = tuple(gates.GATE_TO_STATE_MAPPINGS.items())

    _explain()
    _explain(
        adapter_configuration_declared=False,
        blocking_adapter_markers_present=True,
    )
    policy.is_adapter_gate_evidence_allowed(**_valid_markers())

    assert gates.ADAPTER_CONFIGURATION_GATE_INPUT_FIELDS == gate_inputs_before
    assert (
        gates.ADAPTER_CONFIGURATION_GATE_REASON_CODES
        == gate_reason_codes_before
    )
    assert gates.GATE_INVARIANTS == gate_invariants_before
    assert tuple(gates.GATE_TO_STATE_MAPPINGS.items()) == gate_mappings_before


def test_module_namespace_does_not_import_forbidden_behavior_modules_or_io_libraries():
    forbidden_names = {
        "gate_decision_mapper",
        "transition_guard",
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


def test_no_runtime_config_credential_adapter_artifact_hash_ledger_publish_notification_or_public_url_behavior_is_implied():
    results = (
        _explain(),
        _explain(blocking_adapter_markers_present=True),
    )

    for result in results:
        assert FORBIDDEN_RESULT_KEYS.isdisjoint(result)
        assert result["source"] == (
            "adapter_gate_evidence_policy."
            "explain_adapter_gate_evidence_policy"
        )
