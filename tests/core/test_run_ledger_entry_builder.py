"""Focused contract tests for the pure Run Ledger Entry builder."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import gates
from ai_daily_publishing_system.core import run_ledger_entry_builder as builder
from ai_daily_publishing_system.core import states


REQUIRED_RESULT_FIELDS = {
    "buildable",
    "reason_code",
    "reason",
    "source",
    "entry",
    "entry_violations",
    "missing_or_invalid_fields",
    "invariant_refs",
}

REQUIRED_ENTRY_FIELDS = (
    "run_id",
    "run_state",
    "run_outcome",
    "runtime_profile_name",
    "runtime_profile_mode",
    "publish_mode",
    "notification_mode",
    "eval_mode",
    "gate_decision_envelope_refs",
    "artifact_refs",
    "artifact_hash_refs",
    "failure_package_ref",
    "badcase_record_ref",
    "public_url_created",
    "public_url",
    "started_at",
    "completed_at",
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
    "run_ledger_path",
    "publish_ledger_path",
    "notification_ledger_path",
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
    "run_ledger_written",
    "publisher",
    "notifier",
    "public_url_generated",
}


def _valid_values():
    return {
        "run_id": "run-001",
        "run_state": states.NOOP_COMPLETED,
        "run_outcome": "noop_completed",
        "runtime_profile_name": "manual-local-noop",
        "runtime_profile_mode": "manual_local_noop",
        "publish_mode": "noop",
        "notification_mode": "noop",
        "eval_mode": "stubbed",
        "gate_decision_envelope_refs": (
            "adapter-gate-decision-envelope.yaml",
            "daily-gate-decision-envelope.yaml",
        ),
        "artifact_refs": (
            "reader.html",
            "validator-result.yaml",
            "run-ledger.yaml",
        ),
        "artifact_hash_refs": ("artifact-hash.yaml#final",),
        "failure_package_ref": "",
        "badcase_record_ref": "",
        "public_url_created": False,
        "public_url_is_null": True,
        "started_at": "caller-supplied-started-at",
        "completed_at": "caller-supplied-completed-at",
        "timestamp_policy": "caller_supplied_no_datetime_parsing",
        "source_of_truth": ("p2d-2g", "p2d-14"),
        "notes": ("shape-only",),
    }


def _explain(**overrides):
    values = _valid_values()
    values.update(overrides)
    return builder.explain_run_ledger_entry_build(**values)


def test_valid_noop_completed_like_entry_is_buildable():
    result = _explain()

    assert result["buildable"] is True
    assert result["reason_code"] == "RUN_LEDGER_ENTRY_BUILDABLE"
    assert result["entry"]["run_state"] == states.NOOP_COMPLETED
    assert result["entry"]["failure_package_ref"] == ""
    assert result["entry"]["badcase_record_ref"] == ""
    assert result["entry_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()


def test_valid_review_blocked_like_entry_is_buildable():
    result = _explain(
        run_state=states.REVIEW_BLOCKED,
        run_outcome="review_blocked",
        failure_package_ref="failure-package.yaml",
    )

    assert result["buildable"] is True
    assert result["reason_code"] == "RUN_LEDGER_ENTRY_BUILDABLE"
    assert result["entry"]["run_state"] == states.REVIEW_BLOCKED
    assert result["entry"]["failure_package_ref"] == "failure-package.yaml"
    assert result["entry"]["badcase_record_ref"] == ""


def test_valid_config_blocked_like_entry_is_buildable():
    result = _explain(
        run_state=states.CONFIG_BLOCKED,
        run_outcome="config_blocked",
        failure_package_ref="failure-package.yaml",
    )

    assert result["buildable"] is True
    assert result["reason_code"] == "RUN_LEDGER_ENTRY_BUILDABLE"
    assert result["entry"]["run_state"] == states.CONFIG_BLOCKED


def test_valid_system_failed_like_entry_is_buildable():
    result = _explain(
        run_state=states.SYSTEM_FAILED,
        run_outcome="system_failed",
        failure_package_ref="failure-package.yaml",
    )

    assert result["buildable"] is True
    assert result["reason_code"] == "RUN_LEDGER_ENTRY_BUILDABLE"
    assert result["entry"]["run_state"] == states.SYSTEM_FAILED


def test_valid_adapter_failed_like_entry_is_buildable():
    result = _explain(
        run_state=states.ADAPTER_FAILED,
        run_outcome="adapter_failed",
        failure_package_ref="failure-package.yaml",
    )

    assert result["buildable"] is True
    assert result["reason_code"] == "RUN_LEDGER_ENTRY_BUILDABLE"
    assert result["entry"]["run_state"] == states.ADAPTER_FAILED


def test_valid_badcase_created_like_entry_is_buildable():
    result = _explain(
        run_state=states.BADCASE_CREATED,
        run_outcome="badcase_created",
        failure_package_ref="failure-package.yaml",
        badcase_record_ref="badcase-record.yaml",
    )

    assert result["buildable"] is True
    assert result["reason_code"] == "RUN_LEDGER_ENTRY_BUILDABLE"
    assert result["entry"]["run_state"] == states.BADCASE_CREATED
    assert result["entry"]["badcase_record_ref"] == "badcase-record.yaml"


def test_entry_keys_exactly_match_run_ledger_entry_fields():
    result = _explain()

    assert tuple(result["entry"].keys()) == REQUIRED_ENTRY_FIELDS
    assert set(result["entry"]) == set(REQUIRED_ENTRY_FIELDS)


def test_result_shape_is_stable():
    result = _explain()

    assert set(result) == REQUIRED_RESULT_FIELDS


def test_missing_required_fields_block_with_dedicated_reasons():
    cases = (
        ("run_id", "", "RUN_ID_MISSING", ("run_id",)),
        ("run_state", "", "RUN_STATE_MISSING", ("run_state",)),
        ("run_outcome", "", "RUN_OUTCOME_MISSING", ("run_outcome",)),
        (
            "runtime_profile_name",
            "",
            "RUNTIME_PROFILE_NAME_MISSING",
            ("runtime_profile_name",),
        ),
        (
            "runtime_profile_mode",
            "",
            "RUNTIME_PROFILE_MODE_MISSING",
            ("runtime_profile_mode",),
        ),
        ("publish_mode", "", "PUBLISH_MODE_MISSING", ("publish_mode",)),
        (
            "notification_mode",
            "",
            "NOTIFICATION_MODE_MISSING",
            ("notification_mode",),
        ),
        ("eval_mode", "", "EVAL_MODE_MISSING", ("eval_mode",)),
        (
            "gate_decision_envelope_refs",
            (),
            "GATE_DECISION_ENVELOPE_REFS_MISSING",
            ("gate_decision_envelope_refs",),
        ),
        ("artifact_refs", (), "ARTIFACT_REFS_MISSING", ("artifact_refs",)),
        (
            "artifact_hash_refs",
            (),
            "ARTIFACT_HASH_REFS_MISSING",
            ("artifact_hash_refs",),
        ),
        ("started_at", "", "STARTED_AT_MISSING", ("started_at",)),
        ("completed_at", "", "COMPLETED_AT_MISSING", ("completed_at",)),
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
        assert result["entry_violations"] == (reason_code,)
        assert result["missing_or_invalid_fields"] == invalid_fields


def test_whitespace_required_strings_are_missing():
    cases = (
        ("run_id", "   ", "RUN_ID_MISSING"),
        ("run_state", "   ", "RUN_STATE_MISSING"),
        ("run_outcome", "   ", "RUN_OUTCOME_MISSING"),
        ("runtime_profile_name", "   ", "RUNTIME_PROFILE_NAME_MISSING"),
        ("runtime_profile_mode", "   ", "RUNTIME_PROFILE_MODE_MISSING"),
        ("publish_mode", "   ", "PUBLISH_MODE_MISSING"),
        ("notification_mode", "   ", "NOTIFICATION_MODE_MISSING"),
        ("eval_mode", "   ", "EVAL_MODE_MISSING"),
        ("started_at", "   ", "STARTED_AT_MISSING"),
        ("completed_at", "   ", "COMPLETED_AT_MISSING"),
        ("timestamp_policy", "   ", "TIMESTAMP_POLICY_MISSING"),
    )

    for field_name, value, reason_code in cases:
        result = _explain(**{field_name: value})

        assert result["buildable"] is False
        assert result["reason_code"] == reason_code


def test_unknown_run_state_is_blocked():
    result = _explain(run_state="UNKNOWN_STATE")

    assert result["buildable"] is False
    assert result["reason_code"] == "RUN_STATE_UNKNOWN"
    assert result["entry_violations"] == ("RUN_STATE_UNKNOWN",)
    assert result["missing_or_invalid_fields"] == ("run_state",)


def test_public_url_created_true_is_blocked():
    result = _explain(public_url_created=True)

    assert result["buildable"] is False
    assert result["reason_code"] == "PUBLIC_URL_CREATED_TRUE"
    assert result["missing_or_invalid_fields"] == ("public_url_created",)
    assert result["entry"]["public_url_created"] is True
    assert result["entry"]["public_url"] is None


def test_public_url_is_null_false_is_blocked_without_echoing_url():
    result = _explain(public_url_is_null=False)

    assert result["buildable"] is False
    assert result["reason_code"] == "PUBLIC_URL_NON_NULL"
    assert result["missing_or_invalid_fields"] == ("public_url",)
    assert result["entry"]["public_url"] is None
    assert "public_url_is_null" not in result
    assert "public_url_is_null" not in result["entry"]


def test_entry_always_returns_public_url_none():
    results = (
        _explain(),
        _explain(public_url_created=True),
        _explain(public_url_is_null=False),
    )

    for result in results:
        assert result["entry"]["public_url"] is None


def test_no_raw_url_string_appears_in_result():
    result = _explain()

    assert "https://" not in repr(result)
    assert "raw_public_url" not in result
    assert "raw_public_url" not in result["entry"]


def test_failure_package_ref_is_required_for_failure_states():
    for run_state in (
        states.CONFIG_BLOCKED,
        states.REVIEW_BLOCKED,
        states.SYSTEM_FAILED,
        states.ADAPTER_FAILED,
        states.BADCASE_CREATED,
    ):
        result = _explain(run_state=run_state, run_outcome=run_state.lower())

        assert result["buildable"] is False
        assert "FAILURE_OUTCOME_WITHOUT_FAILURE_REF" in (
            result["entry_violations"]
        )
        assert "failure_package_ref" in result["missing_or_invalid_fields"]


def test_failure_package_ref_is_forbidden_for_non_failure_states():
    result = _explain(failure_package_ref="failure-package.yaml")

    assert result["buildable"] is False
    assert result["reason_code"] == "FAILURE_REF_WITH_NON_FAILURE_OUTCOME"
    assert result["missing_or_invalid_fields"] == ("failure_package_ref",)


def test_badcase_record_ref_is_required_only_for_badcase_created():
    missing = _explain(
        run_state=states.BADCASE_CREATED,
        run_outcome="badcase_created",
        failure_package_ref="failure-package.yaml",
    )
    allowed = _explain(
        run_state=states.BADCASE_CREATED,
        run_outcome="badcase_created",
        failure_package_ref="failure-package.yaml",
        badcase_record_ref="badcase-record.yaml",
    )

    assert missing["buildable"] is False
    assert missing["reason_code"] == "GOVERNANCE_OUTCOME_WITHOUT_BADCASE_REF"
    assert missing["missing_or_invalid_fields"] == ("badcase_record_ref",)
    assert allowed["buildable"] is True


def test_badcase_record_ref_is_forbidden_for_non_governance_states():
    for run_state in (
        states.NOOP_COMPLETED,
        states.CONFIG_BLOCKED,
        states.REVIEW_BLOCKED,
        states.SYSTEM_FAILED,
        states.ADAPTER_FAILED,
    ):
        result = _explain(
            run_state=run_state,
            run_outcome=run_state.lower(),
            failure_package_ref=(
                "" if run_state == states.NOOP_COMPLETED else "failure-package.yaml"
            ),
            badcase_record_ref="badcase-record.yaml",
        )

        assert result["buildable"] is False
        assert "BADCASE_REF_WITH_NON_GOVERNANCE_OUTCOME" in (
            result["entry_violations"]
        )
        assert "badcase_record_ref" in result["missing_or_invalid_fields"]


def test_reason_priority_and_all_violations_are_collected():
    result = _explain(
        run_id="",
        run_state=states.BADCASE_CREATED,
        run_outcome="",
        runtime_profile_name="",
        runtime_profile_mode="",
        publish_mode="",
        notification_mode="",
        eval_mode="",
        gate_decision_envelope_refs=(),
        artifact_refs=(),
        artifact_hash_refs=(),
        started_at="",
        completed_at="",
        timestamp_policy="",
        source_of_truth=(),
        public_url_created=True,
        public_url_is_null=False,
    )

    assert result["buildable"] is False
    assert result["reason_code"] == "RUN_ID_MISSING"
    assert result["entry_violations"] == (
        "RUN_ID_MISSING",
        "RUN_OUTCOME_MISSING",
        "RUNTIME_PROFILE_NAME_MISSING",
        "RUNTIME_PROFILE_MODE_MISSING",
        "PUBLISH_MODE_MISSING",
        "NOTIFICATION_MODE_MISSING",
        "EVAL_MODE_MISSING",
        "GATE_DECISION_ENVELOPE_REFS_MISSING",
        "ARTIFACT_REFS_MISSING",
        "ARTIFACT_HASH_REFS_MISSING",
        "STARTED_AT_MISSING",
        "COMPLETED_AT_MISSING",
        "TIMESTAMP_POLICY_MISSING",
        "SOURCE_OF_TRUTH_MISSING",
        "PUBLIC_URL_CREATED_TRUE",
        "PUBLIC_URL_NON_NULL",
        "FAILURE_OUTCOME_WITHOUT_FAILURE_REF",
        "GOVERNANCE_OUTCOME_WITHOUT_BADCASE_REF",
    )
    assert result["missing_or_invalid_fields"] == (
        "run_id",
        "run_outcome",
        "runtime_profile_name",
        "runtime_profile_mode",
        "publish_mode",
        "notification_mode",
        "eval_mode",
        "gate_decision_envelope_refs",
        "artifact_refs",
        "artifact_hash_refs",
        "started_at",
        "completed_at",
        "timestamp_policy",
        "source_of_truth",
        "public_url_created",
        "public_url",
        "failure_package_ref",
        "badcase_record_ref",
    )


def test_buildable_result_has_empty_violation_and_field_collections():
    result = _explain()

    assert result["buildable"] is True
    assert result["entry_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()


def test_bool_wrapper_matches_explanation():
    cases = (
        _valid_values(),
        {
            **_valid_values(),
            "run_state": states.REVIEW_BLOCKED,
            "run_outcome": "review_blocked",
            "failure_package_ref": "failure-package.yaml",
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
        explanation = builder.explain_run_ledger_entry_build(**values)
        assert (
            builder.is_run_ledger_entry_buildable(**values)
            is explanation["buildable"]
        )


def test_no_raw_credential_adapter_review_hash_or_ledger_values_appear():
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


def test_buildable_result_does_not_include_execution_behavior_fields():
    result = _explain()

    assert result["buildable"] is True
    assert FORBIDDEN_RESULT_KEYS.isdisjoint(result)
    assert FORBIDDEN_RESULT_KEYS.isdisjoint(result["entry"])
    assert "builder_not_run_ledger_writer" in result["invariant_refs"]
    assert "builder_not_gate_execution" in result["invariant_refs"]
    assert "builder_not_transition_execution" in result["invariant_refs"]
    assert "buildable_not_hash_calculation" in result["invariant_refs"]
    assert "buildable_not_publish" in result["invariant_refs"]
    assert "buildable_not_notification" in result["invariant_refs"]
    assert "buildable_not_public_url" in result["invariant_refs"]


def test_states_and_gates_constants_are_not_mutated():
    mvp_states_before = states.MVP_STATES
    state_categories_before = tuple(states.STATE_CATEGORIES.items())
    gate_invariants_before = gates.GATE_INVARIANTS
    gate_names_before = gates.GATE_NAMES

    _explain()
    _explain(public_url_created=True)
    builder.is_run_ledger_entry_buildable(**_valid_values())

    assert states.MVP_STATES == mvp_states_before
    assert tuple(states.STATE_CATEGORIES.items()) == state_categories_before
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
        "runtime_context",
        "config",
        "artifact_path",
        "hash_value",
        "gate_passed",
        "generated_state",
        "generated_transition",
        "decision_result",
        "transition",
    }

    for result in results:
        assert forbidden_keys.isdisjoint(result)
        assert forbidden_keys.isdisjoint(result["entry"])
        assert "no_runtime_context_config_or_credential_read" in (
            result["invariant_refs"]
        )
        assert "no_adapter_preflight" in result["invariant_refs"]
        assert "no_external_adapter_call" in result["invariant_refs"]
        assert "no_artifact_or_review_io" in result["invariant_refs"]
        assert "no_hash_calculation" in result["invariant_refs"]
        assert "no_ledger_write" in result["invariant_refs"]
        assert "no_public_url_behavior" in result["invariant_refs"]
        assert "no_gate_decision_envelope_builder_call" in (
            result["invariant_refs"]
        )


def test_reason_catalog_contains_only_executable_reason_codes():
    assert builder.RUN_LEDGER_ENTRY_BUILD_REASON_CODES == (
        "RUN_ID_MISSING",
        "RUN_STATE_MISSING",
        "RUN_STATE_UNKNOWN",
        "RUN_OUTCOME_MISSING",
        "RUNTIME_PROFILE_NAME_MISSING",
        "RUNTIME_PROFILE_MODE_MISSING",
        "PUBLISH_MODE_MISSING",
        "NOTIFICATION_MODE_MISSING",
        "EVAL_MODE_MISSING",
        "GATE_DECISION_ENVELOPE_REFS_MISSING",
        "ARTIFACT_REFS_MISSING",
        "ARTIFACT_HASH_REFS_MISSING",
        "STARTED_AT_MISSING",
        "COMPLETED_AT_MISSING",
        "TIMESTAMP_POLICY_MISSING",
        "SOURCE_OF_TRUTH_MISSING",
        "PUBLIC_URL_CREATED_TRUE",
        "PUBLIC_URL_NON_NULL",
        "FAILURE_REF_WITH_NON_FAILURE_OUTCOME",
        "FAILURE_OUTCOME_WITHOUT_FAILURE_REF",
        "BADCASE_REF_WITH_NON_GOVERNANCE_OUTCOME",
        "GOVERNANCE_OUTCOME_WITHOUT_BADCASE_REF",
        "RUN_LEDGER_ENTRY_BUILDABLE",
    )
    forbidden_codes = {
        "RUN_LEDGER_WRITE_FORBIDDEN",
        "GATE_EXECUTION_FORBIDDEN",
        "TRANSITION_EXECUTION_FORBIDDEN",
        "HASH_CALCULATION_FORBIDDEN",
        "PUBLISH_FORBIDDEN",
        "NOTIFICATION_FORBIDDEN",
        "PUBLIC_URL_CREATION_FORBIDDEN",
    }

    assert forbidden_codes.isdisjoint(
        builder.RUN_LEDGER_ENTRY_BUILD_REASON_CODES
    )


def test_invariant_refs_capture_run_ledger_entry_builder_boundaries():
    result = _explain()
    required_invariants = {
        "run_ledger_entry_builder_only",
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
        "no_public_url_behavior",
        "no_gate_decision_envelope_builder_call",
    }

    assert required_invariants <= set(result["invariant_refs"])
    assert set(gates.GATE_INVARIANTS) <= set(result["invariant_refs"])


def test_no_forbidden_payload_or_control_inputs_are_in_result():
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
        "run_ledger_path",
        "publish_ledger_path",
        "notification_ledger_path",
        "failure_package",
        "badcase_record",
        "gate_decision_envelope",
        "should_write_ledger",
        "should_transition",
        "should_publish",
        "should_notify",
    )

    for forbidden_name in forbidden_names:
        assert forbidden_name not in result
        assert forbidden_name not in result["entry"]
