"""Focused contract tests for the pure Failure Package builder."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import failure_package_builder as builder
from ai_daily_publishing_system.core import gates
from ai_daily_publishing_system.core import states


REQUIRED_RESULT_FIELDS = {
    "buildable",
    "reason_code",
    "reason",
    "source",
    "package",
    "package_violations",
    "missing_or_invalid_fields",
    "invariant_refs",
}

REQUIRED_PACKAGE_FIELDS = (
    "run_id",
    "failure_id",
    "failed_state",
    "failure_kind",
    "failure_reason_code",
    "failure_summary",
    "blocking_reasons",
    "missing_inputs",
    "gate_decision_envelope_refs",
    "run_ledger_entry_ref",
    "artifact_refs",
    "evidence_refs",
    "artifact_hash_refs",
    "redaction_status",
    "public_url_created",
    "public_url",
    "badcase_candidate",
    "badcase_record_ref",
    "created_at",
    "timestamp_policy",
    "source_of_truth",
    "notes",
)

FORBIDDEN_RESULT_KEYS = {
    "public_url_is_null",
    "raw_public_url",
    "credential_values",
    "raw_credentials",
    "runtime_context",
    "config_snapshot",
    "adapter_outputs",
    "adapter_preflight_result",
    "review_content",
    "artifact_contents",
    "artifact_hash_values",
    "ledger_path",
    "failure_package_path",
    "run_ledger_path",
    "badcase_record_path",
    "should_write_failure_package",
    "should_create_badcase",
    "should_write_ledger",
    "should_transition",
    "should_publish",
    "should_notify",
    "gate_executed",
    "transition_executed",
    "ledger_written",
    "failure_package_written",
    "badcase_record_written",
    "badcase_created",
    "published",
    "notification_sent",
    "public_url_reserved",
    "public_url_faked",
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
    "ledger_written",
    "publisher",
    "notifier",
    "public_url_generated",
    "generated_state",
    "generated_transition",
    "gate_execution_result",
    "transition_execution_result",
}


def _valid_values():
    return {
        "run_id": "run-001",
        "failure_id": "failure-001",
        "failed_state": states.REVIEW_BLOCKED,
        "failure_kind": "review_blocked",
        "failure_reason_code": "DAILY_GATE_BLOCKED",
        "failure_summary": (
            "Caller-supplied summary of why the run is blocked."
        ),
        "blocking_reasons": ("daily gate blocked",),
        "missing_inputs": (),
        "gate_decision_envelope_refs": (
            "daily-gate-decision-envelope.yaml",
        ),
        "run_ledger_entry_ref": "run-ledger.yaml#run-001",
        "artifact_refs": (
            "validator-result.yaml",
            "rubric-review.json",
        ),
        "evidence_refs": ("rubric-review.json#summary",),
        "artifact_hash_refs": (),
        "redaction_status": "pass",
        "public_url_created": False,
        "public_url_is_null": True,
        "badcase_candidate": True,
        "badcase_record_ref": "",
        "created_at": "caller-supplied-created-at",
        "timestamp_policy": "caller_supplied_no_datetime_parsing",
        "source_of_truth": ("p2d-2g", "p2d-15"),
        "notes": ("shape-only",),
    }


def _explain(**overrides):
    values = _valid_values()
    values.update(overrides)
    return builder.explain_failure_package_build(**values)


def test_valid_config_blocked_failure_package_is_buildable():
    result = _explain(
        failed_state=states.CONFIG_BLOCKED,
        failure_kind="config_blocked",
        failure_reason_code="ADAPTER_CONFIGURATION_BLOCKED",
        gate_decision_envelope_refs=(
            "adapter-gate-decision-envelope.yaml",
        ),
    )

    assert result["buildable"] is True
    assert result["reason_code"] == "FAILURE_PACKAGE_BUILDABLE"
    assert result["package"]["failed_state"] == states.CONFIG_BLOCKED


def test_valid_review_blocked_failure_package_is_buildable():
    result = _explain()

    assert result["buildable"] is True
    assert result["reason_code"] == "FAILURE_PACKAGE_BUILDABLE"
    assert result["package"]["failed_state"] == states.REVIEW_BLOCKED
    assert result["package_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()


def test_valid_system_failed_failure_package_is_buildable():
    result = _explain(
        failed_state=states.SYSTEM_FAILED,
        failure_kind="system_failed",
        failure_reason_code="RUNTIME_FAILURE_CLASSIFIED",
        gate_decision_envelope_refs=(),
    )

    assert result["buildable"] is True
    assert result["reason_code"] == "FAILURE_PACKAGE_BUILDABLE"
    assert result["package"]["failed_state"] == states.SYSTEM_FAILED


def test_valid_adapter_failed_failure_package_is_buildable():
    result = _explain(
        failed_state=states.ADAPTER_FAILED,
        failure_kind="adapter_failed",
        failure_reason_code="ADAPTER_EXECUTION_FAILED",
        gate_decision_envelope_refs=(
            "adapter-gate-decision-envelope.yaml",
        ),
    )

    assert result["buildable"] is True
    assert result["reason_code"] == "FAILURE_PACKAGE_BUILDABLE"
    assert result["package"]["failed_state"] == states.ADAPTER_FAILED


def test_system_failed_allows_empty_gate_decision_envelope_refs():
    result = _explain(
        failed_state=states.SYSTEM_FAILED,
        gate_decision_envelope_refs=(),
    )

    assert result["buildable"] is True
    assert result["package"]["gate_decision_envelope_refs"] == ()
    assert "GATE_DECISION_ENVELOPE_REFS_MISSING" not in (
        result["package_violations"]
    )


def test_system_failed_allows_empty_artifact_hash_refs():
    result = _explain(
        failed_state=states.SYSTEM_FAILED,
        gate_decision_envelope_refs=(),
        artifact_hash_refs=(),
    )

    assert result["buildable"] is True
    assert result["package"]["artifact_hash_refs"] == ()


def test_gate_related_failure_states_require_gate_envelope_refs():
    for failed_state in (
        states.CONFIG_BLOCKED,
        states.REVIEW_BLOCKED,
        states.ADAPTER_FAILED,
    ):
        result = _explain(
            failed_state=failed_state,
            gate_decision_envelope_refs=(),
        )

        assert result["buildable"] is False
        assert (
            result["reason_code"]
            == "GATE_DECISION_ENVELOPE_REFS_MISSING"
        )
        assert result["package_violations"] == (
            "GATE_DECISION_ENVELOPE_REFS_MISSING",
        )
        assert result["missing_or_invalid_fields"] == (
            "gate_decision_envelope_refs",
        )


def test_badcase_created_is_not_failure_package_eligible():
    result = _explain(failed_state=states.BADCASE_CREATED)

    assert result["buildable"] is False
    assert (
        result["reason_code"]
        == "FAILED_STATE_NOT_FAILURE_PACKAGE_ELIGIBLE"
    )
    assert result["missing_or_invalid_fields"] == ("failed_state",)


def test_noop_completed_is_not_failure_package_eligible():
    result = _explain(failed_state=states.NOOP_COMPLETED)

    assert result["buildable"] is False
    assert (
        result["reason_code"]
        == "FAILED_STATE_NOT_FAILURE_PACKAGE_ELIGIBLE"
    )
    assert result["missing_or_invalid_fields"] == ("failed_state",)


def test_unknown_failed_state_is_blocked():
    result = _explain(failed_state="UNKNOWN_STATE")

    assert result["buildable"] is False
    assert result["reason_code"] == "FAILED_STATE_UNKNOWN"
    assert result["package_violations"] == ("FAILED_STATE_UNKNOWN",)
    assert result["missing_or_invalid_fields"] == ("failed_state",)


def test_package_keys_exactly_match_failure_package_fields():
    result = _explain()

    assert tuple(result["package"].keys()) == REQUIRED_PACKAGE_FIELDS
    assert set(result["package"]) == set(REQUIRED_PACKAGE_FIELDS)


def test_result_shape_is_stable():
    result = _explain()

    assert set(result) == REQUIRED_RESULT_FIELDS


def test_missing_required_fields_block_with_dedicated_reasons():
    cases = (
        ("run_id", "", "RUN_ID_MISSING", ("run_id",)),
        ("failure_id", "", "FAILURE_ID_MISSING", ("failure_id",)),
        (
            "failed_state",
            "",
            "FAILED_STATE_MISSING",
            ("failed_state",),
        ),
        (
            "failure_kind",
            "",
            "FAILURE_KIND_MISSING",
            ("failure_kind",),
        ),
        (
            "failure_reason_code",
            "",
            "FAILURE_REASON_CODE_MISSING",
            ("failure_reason_code",),
        ),
        (
            "failure_summary",
            "",
            "FAILURE_SUMMARY_MISSING",
            ("failure_summary",),
        ),
        (
            "blocking_reasons",
            (),
            "BLOCKING_REASONS_MISSING",
            ("blocking_reasons",),
        ),
        (
            "run_ledger_entry_ref",
            "",
            "RUN_LEDGER_ENTRY_REF_MISSING",
            ("run_ledger_entry_ref",),
        ),
        (
            "artifact_refs",
            (),
            "ARTIFACT_REFS_MISSING",
            ("artifact_refs",),
        ),
        (
            "evidence_refs",
            (),
            "EVIDENCE_REFS_MISSING",
            ("evidence_refs",),
        ),
        (
            "redaction_status",
            "",
            "REDACTION_STATUS_MISSING",
            ("redaction_status",),
        ),
        (
            "created_at",
            "",
            "CREATED_AT_MISSING",
            ("created_at",),
        ),
        (
            "timestamp_policy",
            "",
            "TIMESTAMP_POLICY_MISSING",
            ("timestamp_policy",),
        ),
        (
            "source_of_truth",
            (),
            "SOURCE_OF_TRUTH_MISSING",
            ("source_of_truth",),
        ),
    )

    for field_name, value, reason_code, invalid_fields in cases:
        result = _explain(**{field_name: value})

        assert result["buildable"] is False
        assert result["reason_code"] == reason_code
        assert result["package_violations"] == (reason_code,)
        assert result["missing_or_invalid_fields"] == invalid_fields


def test_whitespace_required_strings_are_missing():
    cases = (
        ("run_id", "   ", "RUN_ID_MISSING"),
        ("failure_id", "   ", "FAILURE_ID_MISSING"),
        ("failed_state", "   ", "FAILED_STATE_MISSING"),
        ("failure_kind", "   ", "FAILURE_KIND_MISSING"),
        (
            "failure_reason_code",
            "   ",
            "FAILURE_REASON_CODE_MISSING",
        ),
        ("failure_summary", "   ", "FAILURE_SUMMARY_MISSING"),
        (
            "run_ledger_entry_ref",
            "   ",
            "RUN_LEDGER_ENTRY_REF_MISSING",
        ),
        ("redaction_status", "   ", "REDACTION_STATUS_MISSING"),
        ("created_at", "   ", "CREATED_AT_MISSING"),
        ("timestamp_policy", "   ", "TIMESTAMP_POLICY_MISSING"),
    )

    for field_name, value, reason_code in cases:
        result = _explain(**{field_name: value})

        assert result["buildable"] is False
        assert result["reason_code"] == reason_code


def test_public_url_created_true_is_blocked():
    result = _explain(public_url_created=True)

    assert result["buildable"] is False
    assert result["reason_code"] == "PUBLIC_URL_CREATED_TRUE"
    assert result["missing_or_invalid_fields"] == ("public_url_created",)
    assert result["package"]["public_url_created"] is True
    assert result["package"]["public_url"] is None


def test_public_url_is_null_false_is_blocked_without_echoing_url():
    result = _explain(public_url_is_null=False)

    assert result["buildable"] is False
    assert result["reason_code"] == "PUBLIC_URL_NON_NULL"
    assert result["missing_or_invalid_fields"] == ("public_url",)
    assert result["package"]["public_url"] is None
    assert "public_url_is_null" not in result
    assert "public_url_is_null" not in result["package"]


def test_package_always_returns_public_url_none():
    results = (
        _explain(),
        _explain(public_url_created=True),
        _explain(public_url_is_null=False),
    )

    for result in results:
        assert result["package"]["public_url"] is None


def test_no_raw_url_string_appears_in_result():
    result = _explain()

    assert "https://" not in repr(result)
    assert "raw_public_url" not in result
    assert "raw_public_url" not in result["package"]


def test_badcase_candidate_allows_empty_or_existing_ref():
    without_ref = _explain(
        badcase_candidate=True,
        badcase_record_ref="",
    )
    with_ref = _explain(
        badcase_candidate=True,
        badcase_record_ref="badcase-record.yaml#badcase-001",
    )

    assert without_ref["buildable"] is True
    assert with_ref["buildable"] is True
    assert (
        with_ref["package"]["badcase_record_ref"]
        == "badcase-record.yaml#badcase-001"
    )


def test_badcase_ref_without_candidate_is_blocked():
    result = _explain(
        badcase_candidate=False,
        badcase_record_ref="badcase-record.yaml#badcase-001",
    )

    assert result["buildable"] is False
    assert (
        result["reason_code"]
        == "BADCASE_REF_WITHOUT_BADCASE_CANDIDATE"
    )
    assert result["missing_or_invalid_fields"] == ("badcase_record_ref",)


def test_artifact_hash_refs_are_optional_caller_supplied_refs():
    without_refs = _explain(artifact_hash_refs=())
    with_refs = _explain(
        artifact_hash_refs=("artifact-hash.yaml#pre-gate",),
    )

    assert without_refs["buildable"] is True
    assert with_refs["buildable"] is True
    assert without_refs["package"]["artifact_hash_refs"] == ()
    assert with_refs["package"]["artifact_hash_refs"] == (
        "artifact-hash.yaml#pre-gate",
    )


def test_artifact_hash_refs_missing_reason_is_not_declared():
    excluded_reason = "ARTIFACT_" + "HASH_REFS_MISSING"

    assert excluded_reason not in builder.FAILURE_PACKAGE_BUILD_REASON_CODES
    assert excluded_reason not in builder.__dict__


def test_reason_priority_and_all_violations_are_collected():
    result = _explain(
        run_id="",
        failure_id="",
        failed_state=states.REVIEW_BLOCKED,
        failure_kind="",
        failure_reason_code="",
        failure_summary="",
        blocking_reasons=(),
        gate_decision_envelope_refs=(),
        run_ledger_entry_ref="",
        artifact_refs=(),
        evidence_refs=(),
        redaction_status="",
        public_url_created=True,
        public_url_is_null=False,
        badcase_candidate=False,
        badcase_record_ref="badcase-record.yaml#badcase-001",
        created_at="",
        timestamp_policy="",
        source_of_truth=(),
    )

    assert result["buildable"] is False
    assert result["reason_code"] == "RUN_ID_MISSING"
    assert result["package_violations"] == (
        "RUN_ID_MISSING",
        "FAILURE_ID_MISSING",
        "FAILURE_KIND_MISSING",
        "FAILURE_REASON_CODE_MISSING",
        "FAILURE_SUMMARY_MISSING",
        "BLOCKING_REASONS_MISSING",
        "GATE_DECISION_ENVELOPE_REFS_MISSING",
        "RUN_LEDGER_ENTRY_REF_MISSING",
        "ARTIFACT_REFS_MISSING",
        "EVIDENCE_REFS_MISSING",
        "REDACTION_STATUS_MISSING",
        "CREATED_AT_MISSING",
        "TIMESTAMP_POLICY_MISSING",
        "SOURCE_OF_TRUTH_MISSING",
        "PUBLIC_URL_CREATED_TRUE",
        "PUBLIC_URL_NON_NULL",
        "BADCASE_REF_WITHOUT_BADCASE_CANDIDATE",
    )
    assert result["missing_or_invalid_fields"] == (
        "run_id",
        "failure_id",
        "failure_kind",
        "failure_reason_code",
        "failure_summary",
        "blocking_reasons",
        "gate_decision_envelope_refs",
        "run_ledger_entry_ref",
        "artifact_refs",
        "evidence_refs",
        "redaction_status",
        "created_at",
        "timestamp_policy",
        "source_of_truth",
        "public_url_created",
        "public_url",
        "badcase_record_ref",
    )


def test_buildable_result_has_empty_violation_and_field_collections():
    result = _explain()

    assert result["buildable"] is True
    assert result["package_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()


def test_bool_wrapper_matches_explanation():
    cases = (
        _valid_values(),
        dict(_valid_values(), run_id=""),
        dict(
            _valid_values(),
            failed_state=states.SYSTEM_FAILED,
            gate_decision_envelope_refs=(),
        ),
        dict(
            _valid_values(),
            badcase_candidate=False,
            badcase_record_ref="badcase-record.yaml#badcase-001",
        ),
    )

    for values in cases:
        explanation = builder.explain_failure_package_build(**values)

        assert (
            builder.is_failure_package_buildable(**values)
            is explanation["buildable"]
        )


def test_no_raw_credential_adapter_review_artifact_hash_or_ledger_values_appear():
    result = _explain()
    forbidden_values = (
        "secret-token",
        "provider-secret-value",
        "adapter-output-body",
        "review-content-body",
        "artifact-body-content",
        "artifact-hash-value",
        "ledger/path/value",
    )
    rendered_result = repr(result)

    for forbidden_value in forbidden_values:
        assert forbidden_value not in rendered_result


def test_buildable_result_does_not_imply_execution_or_writes():
    result = _explain()

    assert result["buildable"] is True
    assert FORBIDDEN_RESULT_KEYS.isdisjoint(result)
    assert FORBIDDEN_RESULT_KEYS.isdisjoint(result["package"])
    assert "builder_not_failure_package_writer" in result["invariant_refs"]
    assert "builder_not_badcase_record_writer" in result["invariant_refs"]
    assert "builder_not_run_ledger_writer" in result["invariant_refs"]
    assert "builder_not_gate_execution" in result["invariant_refs"]
    assert "builder_not_transition_execution" in result["invariant_refs"]
    assert "buildable_not_hash_calculation" in result["invariant_refs"]
    assert "buildable_not_publish" in result["invariant_refs"]
    assert "buildable_not_notification" in result["invariant_refs"]
    assert "buildable_not_public_url" in result["invariant_refs"]


def test_states_and_gates_constants_are_not_mutated():
    mvp_states_before = states.MVP_STATES
    state_invariants_before = states.STATE_INVARIANTS
    gate_invariants_before = gates.GATE_INVARIANTS
    gate_names_before = gates.GATE_NAMES

    _explain()
    _explain(public_url_created=True)
    builder.is_failure_package_buildable(**_valid_values())

    assert states.MVP_STATES == mvp_states_before
    assert states.STATE_INVARIANTS == state_invariants_before
    assert gates.GATE_INVARIANTS == gate_invariants_before
    assert gates.GATE_NAMES == gate_names_before


def test_module_namespace_does_not_import_forbidden_modules_or_io_libraries():
    forbidden_names = {
        "artifacts",
        "gate_decision_mapper",
        "transition_guard",
        "adapter_gate_evidence_policy",
        "adapter_gate_decision_policy",
        "daily_gate_evidence_policy",
        "daily_gate_decision_policy",
        "gate_decision_envelope_builder",
        "run_ledger_entry_builder",
        "artifact_inventory_policy",
        "noop_completion_policy",
        "badcase_creation_policy",
        "pathlib",
        "os",
        "datetime",
        "hashlib",
        "logging",
        "subprocess",
        "requests",
    }

    assert forbidden_names.isdisjoint(builder.__dict__)


def test_result_does_not_imply_runtime_or_io_behavior():
    results = (
        _explain(),
        _explain(public_url_is_null=False),
    )
    forbidden_keys = FORBIDDEN_RESULT_KEYS | {
        "config",
        "artifact_path",
        "hash_value",
        "gate_passed",
        "transition",
        "decision_result",
        states.CONFIG_BLOCKED,
        states.REVIEW_BLOCKED,
        states.SYSTEM_FAILED,
        states.ADAPTER_FAILED,
        states.BADCASE_CREATED,
    }

    for result in results:
        assert forbidden_keys.isdisjoint(result)
        assert forbidden_keys.isdisjoint(result["package"])
        assert "no_runtime_context_config_or_credential_read" in (
            result["invariant_refs"]
        )
        assert "no_adapter_preflight" in result["invariant_refs"]
        assert "no_external_adapter_call" in result["invariant_refs"]
        assert "no_artifact_or_review_io" in result["invariant_refs"]
        assert "no_hash_calculation" in result["invariant_refs"]
        assert "no_ledger_write" in result["invariant_refs"]
        assert "no_failure_package_write" in result["invariant_refs"]
        assert "no_badcase_record_write" in result["invariant_refs"]
        assert "no_public_url_behavior" in result["invariant_refs"]


def test_reason_catalog_contains_only_executable_reason_codes():
    assert builder.FAILURE_PACKAGE_BUILD_REASON_CODES == (
        "RUN_ID_MISSING",
        "FAILURE_ID_MISSING",
        "FAILED_STATE_MISSING",
        "FAILED_STATE_UNKNOWN",
        "FAILED_STATE_NOT_FAILURE_PACKAGE_ELIGIBLE",
        "FAILURE_KIND_MISSING",
        "FAILURE_REASON_CODE_MISSING",
        "FAILURE_SUMMARY_MISSING",
        "BLOCKING_REASONS_MISSING",
        "GATE_DECISION_ENVELOPE_REFS_MISSING",
        "RUN_LEDGER_ENTRY_REF_MISSING",
        "ARTIFACT_REFS_MISSING",
        "EVIDENCE_REFS_MISSING",
        "REDACTION_STATUS_MISSING",
        "CREATED_AT_MISSING",
        "TIMESTAMP_POLICY_MISSING",
        "SOURCE_OF_TRUTH_MISSING",
        "PUBLIC_URL_CREATED_TRUE",
        "PUBLIC_URL_NON_NULL",
        "BADCASE_REF_WITHOUT_BADCASE_CANDIDATE",
        "FAILURE_PACKAGE_BUILDABLE",
    )
    forbidden_codes = {
        "FAILURE_PACKAGE_WRITE_FORBIDDEN",
        "BADCASE_CREATION_FORBIDDEN",
        "RUN_LEDGER_WRITE_FORBIDDEN",
        "GATE_EXECUTION_FORBIDDEN",
        "TRANSITION_EXECUTION_FORBIDDEN",
        "HASH_CALCULATION_FORBIDDEN",
        "PUBLISH_FORBIDDEN",
        "NOTIFICATION_FORBIDDEN",
        "PUBLIC_URL_CREATION_FORBIDDEN",
    }

    assert forbidden_codes.isdisjoint(
        builder.FAILURE_PACKAGE_BUILD_REASON_CODES
    )


def test_invariant_refs_capture_failure_package_builder_boundaries():
    result = _explain()
    required_invariants = {
        "failure_package_builder_only",
        "builder_not_failure_package_writer",
        "builder_not_badcase_record_writer",
        "builder_not_run_ledger_writer",
        "builder_not_gate_execution",
        "builder_not_transition_mapping",
        "builder_not_transition_execution",
        "buildable_not_hash_calculation",
        "buildable_not_publish",
        "buildable_not_notification",
        "buildable_not_public_url",
        "no_runtime_context_config_or_credential_read",
        "no_adapter_preflight",
        "no_external_adapter_call",
        "no_raw_credentials",
        "no_raw_public_url",
        "no_quality_pass_no_public_url",
        "no_artifact_or_review_io",
        "no_hash_calculation",
        "no_ledger_write",
        "no_failure_package_write",
        "no_badcase_record_write",
        "no_public_url_behavior",
        "no_gate_decision_envelope_builder_call",
        "no_run_ledger_entry_builder_call",
        "no_badcase_creation_policy_call",
    }

    assert required_invariants <= set(result["invariant_refs"])
    assert set(states.STATE_INVARIANTS) <= set(result["invariant_refs"])
    assert set(gates.GATE_INVARIANTS) <= set(result["invariant_refs"])


def test_no_forbidden_payload_object_path_or_control_inputs_are_in_result():
    result = _explain()
    forbidden_names = (
        "runtime_context",
        "config_snapshot",
        "credential_values",
        "raw_credentials",
        "raw_public_url",
        "adapter_outputs",
        "review_content",
        "artifact_contents",
        "artifact_hash_values",
        "ledger_path",
        "failure_package_path",
        "run_ledger_path",
        "badcase_record_path",
        "failure_package",
        "badcase_record",
        "gate_decision_envelope",
        "run_ledger_entry",
        "should_write_failure_package",
        "should_create_badcase",
        "should_write_ledger",
        "should_transition",
        "should_publish",
        "should_notify",
    )

    for forbidden_name in forbidden_names:
        assert forbidden_name not in result
        assert forbidden_name not in result["package"]
