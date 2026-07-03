"""Focused contract tests for the pure Daily Gate evidence policy guard."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import daily_gate_evidence_policy
from ai_daily_publishing_system.core import gates


REQUIRED_DECISION_FIELDS = {
    "allowed",
    "reason_code",
    "reason",
    "source",
    "required_daily_gate_inputs_present",
    "validator_result_present",
    "rubric_review_present",
    "audit_review_present",
    "artifact_inventory_policy_allowed",
    "pre_gate_hash_evidence_present",
    "public_private_leak_check_present",
    "credential_redaction_marker_present",
    "evidence_completeness_marker_present",
    "blocking_risk_flags_present",
    "noop_publish_mode_declared",
    "noop_public_url_is_null",
    "noop_public_url_created_is_false",
    "missing_evidence_markers",
    "failed_policy_markers",
    "noop_policy_violations",
    "invariant_refs",
}

FORBIDDEN_RESULT_KEYS = {
    "decision",
    "gate_passed",
    "from_state",
    "to_state",
    "PUBLISH_ALLOWED",
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


def _valid_markers() -> dict[str, bool]:
    return {
        "required_daily_gate_inputs_present": True,
        "validator_result_present": True,
        "rubric_review_present": True,
        "audit_review_present": True,
        "artifact_inventory_policy_allowed": True,
        "pre_gate_hash_evidence_present": True,
        "public_private_leak_check_present": True,
        "credential_redaction_marker_present": True,
        "evidence_completeness_marker_present": True,
        "blocking_risk_flags_present": False,
        "noop_publish_mode_declared": True,
        "noop_public_url_is_null": True,
        "noop_public_url_created_is_false": True,
    }


def _explain(**overrides: bool) -> dict[str, object]:
    markers = _valid_markers()
    markers.update(overrides)
    return daily_gate_evidence_policy.explain_daily_gate_evidence_policy(
        **markers
    )


def test_valid_daily_gate_evidence_markers_are_allowed():
    result = _explain()

    assert result["allowed"] is True
    assert result["reason_code"] == "DAILY_GATE_EVIDENCE_ALLOWED"
    assert result["missing_evidence_markers"] == ()
    assert result["failed_policy_markers"] == ()
    assert result["noop_policy_violations"] == ()


def test_required_daily_gate_inputs_missing_is_blocked():
    result = _explain(required_daily_gate_inputs_present=False)

    assert result["allowed"] is False
    assert result["reason_code"] == "REQUIRED_DAILY_GATE_INPUTS_MISSING"
    assert result["missing_evidence_markers"] == (
        "required_daily_gate_inputs_present",
    )


def test_validator_result_missing_is_blocked():
    result = _explain(validator_result_present=False)

    assert result["allowed"] is False
    assert result["reason_code"] == "VALIDATOR_RESULT_MISSING"
    assert result["missing_evidence_markers"] == (
        "validator_result_present",
    )


def test_rubric_review_missing_is_blocked():
    result = _explain(rubric_review_present=False)

    assert result["allowed"] is False
    assert result["reason_code"] == "RUBRIC_REVIEW_MISSING"
    assert result["missing_evidence_markers"] == (
        "rubric_review_present",
    )


def test_audit_review_missing_is_blocked():
    result = _explain(audit_review_present=False)

    assert result["allowed"] is False
    assert result["reason_code"] == "AUDIT_REVIEW_MISSING"
    assert result["missing_evidence_markers"] == (
        "audit_review_present",
    )


def test_artifact_inventory_policy_blocked_is_blocked():
    result = _explain(artifact_inventory_policy_allowed=False)

    assert result["allowed"] is False
    assert result["reason_code"] == "ARTIFACT_INVENTORY_POLICY_BLOCKED"
    assert result["failed_policy_markers"] == (
        "artifact_inventory_policy_allowed",
    )


def test_pre_gate_hash_missing_is_blocked():
    result = _explain(pre_gate_hash_evidence_present=False)

    assert result["allowed"] is False
    assert result["reason_code"] == "PREGATE_HASH_MISSING"
    assert result["missing_evidence_markers"] == (
        "pre_gate_hash_evidence_present",
    )


def test_public_private_leak_check_missing_is_blocked():
    result = _explain(public_private_leak_check_present=False)

    assert result["allowed"] is False
    assert result["reason_code"] == "MISSING_PUBLIC_PRIVATE_LEAK_CHECK"
    assert result["missing_evidence_markers"] == (
        "public_private_leak_check_present",
    )


def test_credential_redaction_marker_missing_is_blocked():
    result = _explain(credential_redaction_marker_present=False)

    assert result["allowed"] is False
    assert result["reason_code"] == "MISSING_CREDENTIAL_REDACTION_MARKER"
    assert result["missing_evidence_markers"] == (
        "credential_redaction_marker_present",
    )


def test_evidence_completeness_marker_missing_is_blocked():
    result = _explain(evidence_completeness_marker_present=False)

    assert result["allowed"] is False
    assert result["reason_code"] == "MISSING_EVIDENCE_COMPLETENESS_MARKER"
    assert result["missing_evidence_markers"] == (
        "evidence_completeness_marker_present",
    )


def test_blocking_risk_present_is_blocked():
    result = _explain(blocking_risk_flags_present=True)

    assert result["allowed"] is False
    assert result["reason_code"] == "BLOCKING_RISK_PRESENT"
    assert result["failed_policy_markers"] == (
        "blocking_risk_flags_present",
    )


def test_noop_publish_mode_not_declared_is_blocked():
    result = _explain(noop_publish_mode_declared=False)

    assert result["allowed"] is False
    assert result["reason_code"] == "NOOP_PUBLISH_MODE_NOT_DECLARED"
    assert result["noop_policy_violations"] == (
        "noop_publish_mode_declared",
    )


def test_noop_public_url_non_null_is_blocked():
    result = _explain(noop_public_url_is_null=False)

    assert result["allowed"] is False
    assert result["reason_code"] == "NOOP_PUBLIC_URL_NON_NULL"
    assert result["noop_policy_violations"] == (
        "noop_public_url_is_null",
    )


def test_noop_public_url_created_true_is_blocked():
    result = _explain(noop_public_url_created_is_false=False)

    assert result["allowed"] is False
    assert result["reason_code"] == "NOOP_PUBLIC_URL_CREATED_TRUE"
    assert result["noop_policy_violations"] == (
        "noop_public_url_created_is_false",
    )


def test_multi_failure_reason_priority_and_violation_collections_are_stable():
    result = _explain(
        required_daily_gate_inputs_present=False,
        validator_result_present=False,
        rubric_review_present=False,
        audit_review_present=False,
        artifact_inventory_policy_allowed=False,
        pre_gate_hash_evidence_present=False,
        public_private_leak_check_present=False,
        credential_redaction_marker_present=False,
        evidence_completeness_marker_present=False,
        blocking_risk_flags_present=True,
        noop_publish_mode_declared=False,
        noop_public_url_is_null=False,
        noop_public_url_created_is_false=False,
    )

    assert result["allowed"] is False
    assert result["reason_code"] == "REQUIRED_DAILY_GATE_INPUTS_MISSING"
    assert result["missing_evidence_markers"] == (
        "required_daily_gate_inputs_present",
        "validator_result_present",
        "rubric_review_present",
        "audit_review_present",
        "pre_gate_hash_evidence_present",
        "public_private_leak_check_present",
        "credential_redaction_marker_present",
        "evidence_completeness_marker_present",
    )
    assert result["failed_policy_markers"] == (
        "artifact_inventory_policy_allowed",
        "blocking_risk_flags_present",
    )
    assert result["noop_policy_violations"] == (
        "noop_publish_mode_declared",
        "noop_public_url_is_null",
        "noop_public_url_created_is_false",
    )


def test_allowed_result_does_not_include_gate_state_url_or_execution_fields():
    result = _explain()

    assert FORBIDDEN_RESULT_KEYS.isdisjoint(result)


def test_allowed_result_is_not_daily_gate_pass_or_publish_allowed():
    result = _explain()

    assert result["allowed"] is True
    assert "allowed_not_daily_gate_pass" in result["invariant_refs"]
    assert "allowed_not_publish_allowed" in result["invariant_refs"]
    assert gates.PASS not in result.values()
    assert "PUBLISH_ALLOWED" not in result.values()


def test_is_daily_gate_evidence_allowed_matches_explanation():
    cases = (
        _valid_markers(),
        {
            **_valid_markers(),
            "validator_result_present": False,
        },
        {
            **_valid_markers(),
            "blocking_risk_flags_present": True,
        },
        {
            **_valid_markers(),
            "noop_public_url_created_is_false": False,
        },
    )

    for markers in cases:
        explanation = (
            daily_gate_evidence_policy.explain_daily_gate_evidence_policy(
                **markers
            )
        )
        assert (
            daily_gate_evidence_policy.is_daily_gate_evidence_allowed(
                **markers
            )
            is explanation["allowed"]
        )


def test_result_shape_is_stable():
    result = _explain()

    assert set(result) == REQUIRED_DECISION_FIELDS


def test_invariant_refs_capture_policy_boundaries():
    result = _explain()
    required_policy_invariants = {
        "daily_gate_evidence_policy_only",
        "evidence_policy_not_gate_execution",
        "allowed_not_daily_gate_pass",
        "allowed_not_publish_allowed",
        "no_quality_pass_no_public_url",
        "noop_public_url_must_remain_null",
        "noop_public_url_created_must_remain_false",
        "no_artifact_or_review_io",
        "no_hash_calculation",
        "no_ledger_write",
        "no_publish_or_notification",
    }

    assert required_policy_invariants <= set(result["invariant_refs"])
    assert set(gates.GATE_INVARIANTS) <= set(result["invariant_refs"])


def test_policy_guard_does_not_mutate_gate_contracts():
    gate_invariants_before = gates.GATE_INVARIANTS
    gate_reason_codes_before = gates.DAILY_PUBLISH_GATE_REASON_CODES
    gate_mappings_before = tuple(gates.GATE_TO_STATE_MAPPINGS.items())

    _explain()
    _explain(
        artifact_inventory_policy_allowed=False,
        blocking_risk_flags_present=True,
        noop_public_url_is_null=False,
    )
    daily_gate_evidence_policy.is_daily_gate_evidence_allowed(
        **_valid_markers()
    )

    assert gates.GATE_INVARIANTS == gate_invariants_before
    assert gates.DAILY_PUBLISH_GATE_REASON_CODES == gate_reason_codes_before
    assert tuple(gates.GATE_TO_STATE_MAPPINGS.items()) == gate_mappings_before


def test_reason_codes_align_with_gate_catalog_when_present():
    overlapping_reason_codes = {
        daily_gate_evidence_policy.VALIDATOR_RESULT_MISSING,
        daily_gate_evidence_policy.RUBRIC_REVIEW_MISSING,
        daily_gate_evidence_policy.AUDIT_REVIEW_MISSING,
        daily_gate_evidence_policy.PREGATE_HASH_MISSING,
        daily_gate_evidence_policy.BLOCKING_RISK_PRESENT,
        daily_gate_evidence_policy.NOOP_PUBLIC_URL_NON_NULL,
        daily_gate_evidence_policy.NOOP_PUBLIC_URL_CREATED_TRUE,
    }

    if hasattr(gates, "DAILY_PUBLISH_GATE_REASON_CODES"):
        assert overlapping_reason_codes <= set(
            gates.DAILY_PUBLISH_GATE_REASON_CODES
        )


def test_no_artifact_review_hash_ledger_publish_notification_or_public_url_behavior_is_implied():
    result = _explain()

    assert FORBIDDEN_RESULT_KEYS.isdisjoint(result)
    assert result["source"] == (
        "daily_gate_evidence_policy."
        "explain_daily_gate_evidence_policy"
    )
