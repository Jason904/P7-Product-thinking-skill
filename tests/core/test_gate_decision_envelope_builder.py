"""Focused contract tests for the pure Gate Decision Envelope builder."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import gate_decision_envelope_builder as builder
from ai_daily_publishing_system.core import gates


REQUIRED_RESULT_FIELDS = {
    "buildable",
    "reason_code",
    "reason",
    "source",
    "envelope",
    "envelope_violations",
    "missing_or_invalid_fields",
    "invariant_refs",
}

FORBIDDEN_RESULT_KEYS = {
    "public_url_is_null",
    "raw_public_url",
    "credential_values",
    "raw_credentials",
    "adapter_outputs",
    "adapter_preflight_result",
    "review_content",
    "artifact_hash",
    "ledger_path",
    "should_write_ledger",
    "should_transition",
    "should_publish",
    "should_notify",
    "gate_executed",
    "transition_executed",
    "ledger_written",
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
    "publisher",
    "notifier",
    "public_url_generated",
}


def _valid_values():
    return {
        "run_id": "run-001",
        "gate_name": gates.DAILY_PUBLISH_GATE,
        "decision": gates.PASS,
        "from_state": "AUDITING",
        "to_state": "PUBLISH_ALLOWED",
        "reason_codes": ("DAILY_GATE_DECISION_ALLOWED",),
        "blocking_reasons": (),
        "evidence_refs": ("validator-result.yaml", "rubric-review.json"),
        "input_evidence_refs": ("training-report.md",),
        "required_inputs_present": True,
        "missing_inputs": (),
        "redaction_status": "pass",
        "public_url_created": False,
        "public_url_is_null": True,
        "checked_at": "caller-supplied-timestamp",
        "timestamp_policy": "caller_supplied_no_datetime_parsing",
        "source_of_truth": ("p2d-2h", "p2d-13"),
        "notes": ("shape-only",),
    }


def _explain(**overrides):
    values = _valid_values()
    values.update(overrides)
    return builder.explain_gate_decision_envelope_build(**values)


def _all_result_values(result):
    return tuple(result.values()) + tuple(result["envelope"].values())


def test_valid_adapter_gate_pass_like_envelope_is_buildable():
    result = _explain(
        gate_name=gates.ADAPTER_CONFIGURATION_GATE,
        decision=gates.PASS,
        from_state="SCHEDULED_OR_STARTED",
        to_state="RETRIEVING",
        reason_codes=("ADAPTER_GATE_DECISION_ALLOWED",),
        evidence_refs=("adapter-preflight-result.yaml",),
        input_evidence_refs=("runtime-context.yaml",),
    )

    assert result["buildable"] is True
    assert result["reason_code"] == "GATE_DECISION_ENVELOPE_BUILDABLE"
    assert result["envelope"]["gate_name"] == gates.ADAPTER_CONFIGURATION_GATE
    assert result["envelope"]["decision"] == gates.PASS
    assert result["envelope_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()


def test_valid_adapter_gate_blocked_like_envelope_is_buildable():
    result = _explain(
        gate_name=gates.ADAPTER_CONFIGURATION_GATE,
        decision=gates.BLOCKED,
        from_state="SCHEDULED_OR_STARTED",
        to_state="CONFIG_BLOCKED",
        reason_codes=("ADAPTER_GATE_DECISION_ALLOWED",),
        blocking_reasons=("blocking adapter marker present",),
        evidence_refs=("adapter-preflight-result.yaml",),
        input_evidence_refs=("runtime-context.yaml",),
    )

    assert result["buildable"] is True
    assert result["reason_code"] == "GATE_DECISION_ENVELOPE_BUILDABLE"
    assert result["envelope"]["decision"] == gates.BLOCKED
    assert result["envelope"]["blocking_reasons"] == (
        "blocking adapter marker present",
    )


def test_valid_daily_gate_pass_like_envelope_is_buildable():
    result = _explain()

    assert result["buildable"] is True
    assert result["reason_code"] == "GATE_DECISION_ENVELOPE_BUILDABLE"
    assert result["envelope"]["gate_name"] == gates.DAILY_PUBLISH_GATE
    assert result["envelope"]["decision"] == gates.PASS
    assert result["envelope"]["to_state"] == "PUBLISH_ALLOWED"


def test_valid_daily_gate_blocked_like_envelope_is_buildable():
    result = _explain(
        decision=gates.BLOCKED,
        to_state="REVIEW_BLOCKED",
        reason_codes=("DAILY_GATE_DECISION_ALLOWED",),
        blocking_reasons=("audit review blocked",),
    )

    assert result["buildable"] is True
    assert result["reason_code"] == "GATE_DECISION_ENVELOPE_BUILDABLE"
    assert result["envelope"]["decision"] == gates.BLOCKED
    assert result["envelope"]["blocking_reasons"] == (
        "audit review blocked",
    )


def test_envelope_keys_exactly_match_shared_gate_decision_envelope_fields():
    result = _explain()

    assert tuple(result["envelope"].keys()) == (
        gates.SHARED_GATE_DECISION_ENVELOPE_FIELDS
    )
    assert set(result["envelope"]) == set(
        gates.SHARED_GATE_DECISION_ENVELOPE_FIELDS
    )


def test_result_shape_is_stable():
    result = _explain()

    assert set(result) == REQUIRED_RESULT_FIELDS


def test_missing_required_fields_block_with_dedicated_reasons():
    cases = (
        ("run_id", "", "RUN_ID_MISSING", ("run_id",)),
        ("gate_name", "", "GATE_NAME_MISSING", ("gate_name",)),
        ("decision", "", "DECISION_MISSING", ("decision",)),
        ("from_state", "", "FROM_STATE_MISSING", ("from_state",)),
        ("to_state", "", "TO_STATE_MISSING", ("to_state",)),
        ("reason_codes", (), "REASON_CODES_MISSING", ("reason_codes",)),
        (
            "source_of_truth",
            (),
            "SOURCE_OF_TRUTH_MISSING",
            ("source_of_truth",),
        ),
        ("checked_at", "", "CHECKED_AT_MISSING", ("checked_at",)),
        (
            "timestamp_policy",
            "",
            "TIMESTAMP_POLICY_MISSING",
            ("timestamp_policy",),
        ),
        (
            "redaction_status",
            "",
            "REDACTION_STATUS_MISSING",
            ("redaction_status",),
        ),
    )

    for field_name, value, reason_code, invalid_fields in cases:
        result = _explain(**{field_name: value})

        assert result["buildable"] is False
        assert result["reason_code"] == reason_code
        assert result["envelope_violations"] == (reason_code,)
        assert result["missing_or_invalid_fields"] == invalid_fields


def test_whitespace_required_strings_are_missing():
    cases = (
        ("run_id", "   ", "RUN_ID_MISSING"),
        ("gate_name", "   ", "GATE_NAME_MISSING"),
        ("decision", "   ", "DECISION_MISSING"),
        ("from_state", "   ", "FROM_STATE_MISSING"),
        ("to_state", "   ", "TO_STATE_MISSING"),
        ("checked_at", "   ", "CHECKED_AT_MISSING"),
        ("timestamp_policy", "   ", "TIMESTAMP_POLICY_MISSING"),
        ("redaction_status", "   ", "REDACTION_STATUS_MISSING"),
    )

    for field_name, value, reason_code in cases:
        result = _explain(**{field_name: value})

        assert result["buildable"] is False
        assert result["reason_code"] == reason_code


def test_unknown_gate_name_is_blocked():
    result = _explain(gate_name="Unknown Gate")

    assert result["buildable"] is False
    assert result["reason_code"] == "GATE_NAME_UNKNOWN"
    assert result["envelope_violations"] == ("GATE_NAME_UNKNOWN",)
    assert result["missing_or_invalid_fields"] == ("gate_name",)


def test_unknown_and_non_canonical_decisions_are_blocked():
    for decision in ("UNKNOWN", "pass", "blocked", " PASS ", " BLOCKED "):
        result = _explain(decision=decision)

        assert result["buildable"] is False
        assert result["reason_code"] == "DECISION_UNKNOWN"
        assert result["envelope_violations"] == ("DECISION_UNKNOWN",)
        assert result["missing_or_invalid_fields"] == ("decision",)


def test_pass_with_blocking_reasons_is_blocked():
    result = _explain(blocking_reasons=("blocking reason",))

    assert result["buildable"] is False
    assert result["reason_code"] == "PASS_WITH_BLOCKING_REASONS"
    assert result["envelope_violations"] == (
        "PASS_WITH_BLOCKING_REASONS",
    )
    assert result["missing_or_invalid_fields"] == ("blocking_reasons",)


def test_blocked_without_blocking_reasons_is_blocked():
    result = _explain(decision=gates.BLOCKED)

    assert result["buildable"] is False
    assert result["reason_code"] == "BLOCKED_WITHOUT_BLOCKING_REASONS"
    assert result["envelope_violations"] == (
        "BLOCKED_WITHOUT_BLOCKING_REASONS",
    )
    assert result["missing_or_invalid_fields"] == ("blocking_reasons",)


def test_required_inputs_present_with_missing_inputs_is_blocked():
    result = _explain(missing_inputs=("validator-result.yaml",))

    assert result["buildable"] is False
    assert (
        result["reason_code"]
        == "REQUIRED_INPUTS_PRESENT_WITH_MISSING_INPUTS"
    )
    assert result["missing_or_invalid_fields"] == (
        "required_inputs_present",
        "missing_inputs",
    )


def test_required_inputs_missing_without_missing_inputs_is_blocked():
    result = _explain(required_inputs_present=False)

    assert result["buildable"] is False
    assert (
        result["reason_code"]
        == "REQUIRED_INPUTS_MISSING_WITHOUT_MISSING_INPUTS"
    )
    assert result["missing_or_invalid_fields"] == (
        "required_inputs_present",
        "missing_inputs",
    )


def test_public_url_created_true_is_blocked():
    result = _explain(public_url_created=True)

    assert result["buildable"] is False
    assert result["reason_code"] == "PUBLIC_URL_CREATED_TRUE"
    assert result["missing_or_invalid_fields"] == ("public_url_created",)
    assert result["envelope"]["public_url_created"] is True
    assert result["envelope"]["public_url"] is None


def test_public_url_is_null_false_is_blocked_without_echoing_url():
    result = _explain(public_url_is_null=False)

    assert result["buildable"] is False
    assert result["reason_code"] == "PUBLIC_URL_NON_NULL"
    assert result["missing_or_invalid_fields"] == ("public_url",)
    assert result["envelope"]["public_url"] is None
    assert "public_url_is_null" not in result
    assert "public_url_is_null" not in result["envelope"]


def test_envelope_always_returns_public_url_none():
    results = (
        _explain(),
        _explain(public_url_created=True),
        _explain(public_url_is_null=False),
    )

    for result in results:
        assert result["envelope"]["public_url"] is None


def test_no_raw_url_string_appears_in_result():
    result = _explain()

    assert "https://" not in repr(result)
    assert "raw_public_url" not in result
    assert "raw_public_url" not in result["envelope"]


def test_reason_priority_and_all_violations_are_collected():
    result = _explain(
        run_id="",
        gate_name="Unknown Gate",
        from_state="",
        to_state="",
        reason_codes=(),
        source_of_truth=(),
        checked_at="",
        timestamp_policy="",
        redaction_status="",
        missing_inputs=("validator-result.yaml",),
        blocking_reasons=("blocking reason",),
        public_url_created=True,
        public_url_is_null=False,
    )

    assert result["buildable"] is False
    assert result["reason_code"] == "RUN_ID_MISSING"
    assert result["envelope_violations"] == (
        "RUN_ID_MISSING",
        "GATE_NAME_UNKNOWN",
        "FROM_STATE_MISSING",
        "TO_STATE_MISSING",
        "REASON_CODES_MISSING",
        "SOURCE_OF_TRUTH_MISSING",
        "CHECKED_AT_MISSING",
        "TIMESTAMP_POLICY_MISSING",
        "REDACTION_STATUS_MISSING",
        "REQUIRED_INPUTS_PRESENT_WITH_MISSING_INPUTS",
        "PASS_WITH_BLOCKING_REASONS",
        "PUBLIC_URL_CREATED_TRUE",
        "PUBLIC_URL_NON_NULL",
    )
    assert result["missing_or_invalid_fields"] == (
        "run_id",
        "gate_name",
        "from_state",
        "to_state",
        "reason_codes",
        "source_of_truth",
        "checked_at",
        "timestamp_policy",
        "redaction_status",
        "required_inputs_present",
        "missing_inputs",
        "blocking_reasons",
        "public_url_created",
        "public_url",
    )


def test_buildable_result_has_empty_violation_and_field_collections():
    result = _explain()

    assert result["buildable"] is True
    assert result["envelope_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()


def test_bool_wrapper_matches_explanation():
    cases = (
        _valid_values(),
        {
            **_valid_values(),
            "decision": gates.BLOCKED,
            "to_state": "REVIEW_BLOCKED",
            "blocking_reasons": ("audit review blocked",),
        },
        {
            **_valid_values(),
            "run_id": "",
        },
        {
            **_valid_values(),
            "public_url_is_null": False,
        },
    )

    for values in cases:
        explanation = builder.explain_gate_decision_envelope_build(**values)
        assert (
            builder.is_gate_decision_envelope_buildable(**values)
            is explanation["buildable"]
        )


def test_no_raw_credential_adapter_review_hash_or_ledger_values_appear():
    result = _explain()
    forbidden_values = (
        "secret-token",
        "provider-secret-value",
        "adapter-output-body",
        "review-content-body",
        "artifact-hash-value",
        "ledger/path/value",
    )
    rendered_result = repr(result)

    for forbidden_value in forbidden_values:
        assert forbidden_value not in rendered_result


def test_buildable_result_does_not_include_execution_behavior_fields():
    result = _explain()

    assert result["buildable"] is True
    assert FORBIDDEN_RESULT_KEYS.isdisjoint(result)
    assert FORBIDDEN_RESULT_KEYS.isdisjoint(result["envelope"])
    assert "builder_not_gate_execution" in result["invariant_refs"]
    assert "builder_not_transition_execution" in result["invariant_refs"]
    assert "buildable_not_ledger_write" in result["invariant_refs"]
    assert "buildable_not_publish" in result["invariant_refs"]
    assert "buildable_not_notification" in result["invariant_refs"]
    assert "buildable_not_public_url" in result["invariant_refs"]


def test_gate_constants_are_not_mutated():
    gate_names_before = gates.GATE_NAMES
    gate_fields_before = gates.SHARED_GATE_DECISION_ENVELOPE_FIELDS
    gate_invariants_before = gates.GATE_INVARIANTS
    gate_mappings_before = tuple(gates.GATE_TO_STATE_MAPPINGS.items())

    _explain()
    _explain(public_url_created=True)
    builder.is_gate_decision_envelope_buildable(**_valid_values())

    assert gates.GATE_NAMES == gate_names_before
    assert gates.SHARED_GATE_DECISION_ENVELOPE_FIELDS == gate_fields_before
    assert gates.GATE_INVARIANTS == gate_invariants_before
    assert tuple(gates.GATE_TO_STATE_MAPPINGS.items()) == gate_mappings_before


def test_module_namespace_does_not_import_forbidden_modules_or_io_libraries():
    forbidden_names = {
        "states",
        "artifacts",
        "gate_decision_mapper",
        "transition_guard",
        "adapter_gate_evidence_policy",
        "adapter_gate_decision_policy",
        "daily_gate_evidence_policy",
        "daily_gate_decision_policy",
        "artifact_inventory_policy",
        "noop_completion_policy",
        "badcase_creation_policy",
        "pathlib",
        "os",
        "datetime",
        "hashlib",
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
        "runtime_context",
        "config",
        "artifact_path",
        "hash_value",
        "gate_passed",
        "state",
        "transition",
        "decision_result",
    }

    for result in results:
        assert forbidden_keys.isdisjoint(result)
        assert forbidden_keys.isdisjoint(result["envelope"])
        assert "no_runtime_context_config_or_credential_read" in (
            result["invariant_refs"]
        )
        assert "no_artifact_or_review_io" in result["invariant_refs"]
        assert "no_hash_calculation" in result["invariant_refs"]
        assert "no_ledger_write" in result["invariant_refs"]
        assert "no_public_url_behavior" in result["invariant_refs"]


def test_reason_catalog_contains_only_executable_reason_codes():
    assert builder.GATE_DECISION_ENVELOPE_BUILD_REASON_CODES == (
        "RUN_ID_MISSING",
        "GATE_NAME_MISSING",
        "GATE_NAME_UNKNOWN",
        "DECISION_MISSING",
        "DECISION_UNKNOWN",
        "FROM_STATE_MISSING",
        "TO_STATE_MISSING",
        "REASON_CODES_MISSING",
        "SOURCE_OF_TRUTH_MISSING",
        "CHECKED_AT_MISSING",
        "TIMESTAMP_POLICY_MISSING",
        "REDACTION_STATUS_MISSING",
        "REQUIRED_INPUTS_PRESENT_WITH_MISSING_INPUTS",
        "REQUIRED_INPUTS_MISSING_WITHOUT_MISSING_INPUTS",
        "PASS_WITH_BLOCKING_REASONS",
        "BLOCKED_WITHOUT_BLOCKING_REASONS",
        "PUBLIC_URL_CREATED_TRUE",
        "PUBLIC_URL_NON_NULL",
        "GATE_DECISION_ENVELOPE_BUILDABLE",
    )
    forbidden_codes = {
        "GATE_EXECUTION_FORBIDDEN",
        "TRANSITION_EXECUTION_FORBIDDEN",
        "LEDGER_WRITE_FORBIDDEN",
        "PUBLISH_FORBIDDEN",
        "NOTIFICATION_FORBIDDEN",
        "PUBLIC_URL_CREATION_FORBIDDEN",
    }

    assert forbidden_codes.isdisjoint(
        builder.GATE_DECISION_ENVELOPE_BUILD_REASON_CODES
    )


def test_invariant_refs_capture_builder_boundaries():
    result = _explain()
    required_invariants = {
        "gate_decision_envelope_builder_only",
        "builder_not_gate_execution",
        "builder_not_transition_mapping",
        "builder_not_transition_execution",
        "buildable_not_ledger_write",
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
        "no_public_url_behavior",
    }

    assert required_invariants <= set(result["invariant_refs"])
    assert set(gates.GATE_INVARIANTS) <= set(result["invariant_refs"])


def test_no_forbidden_payload_or_control_inputs_are_in_result():
    result = _explain()
    forbidden_names = (
        "payload",
        "adapter_payload",
        "daily_payload",
        "runtime_context",
        "config_snapshot",
        "credential_values",
        "raw_credentials",
        "adapter_outputs",
        "review_content",
        "artifact_hash",
        "ledger_path",
        "should_write_ledger",
        "should_transition",
        "should_publish",
        "should_notify",
    )

    for forbidden_name in forbidden_names:
        assert forbidden_name not in result
        assert forbidden_name not in result["envelope"]
