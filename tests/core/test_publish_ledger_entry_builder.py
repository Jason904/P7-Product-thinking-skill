"""Focused contract tests for the pure Publish Ledger Entry builder."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import (
    publish_ledger_entry_builder as builder,
)
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
    "publish_id",
    "publish_mode",
    "publish_outcome",
    "source_state",
    "target_state",
    "public_candidate_ref",
    "gate_decision_envelope_refs",
    "artifact_hash_manifest_refs",
    "artifact_refs",
    "redaction_status",
    "public_url_created",
    "public_url",
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
    "artifact_hash_manifest_content",
    "artifact_hash_values",
    "ledger_path",
    "publish_ledger_path",
    "notification_ledger_path",
    "artifact_hash_path",
    "run_ledger_path",
    "gate_decision_envelope",
    "artifact_hash_manifest",
    "run_ledger_entry",
    "should_write_publish_ledger",
    "should_publish",
    "should_create_public_url",
    "should_notify",
    "should_transition",
    "should_write_ledger",
    "publish_executed",
    "url_created",
    "notification_sent",
    "gate_executed",
    "transition_executed",
    "ledger_written",
    "publish_ledger_written",
    "public_url_reserved",
    "public_url_faked",
    "runtime_context_read",
    "config_read",
    "credential_read",
    "adapter_preflight_executed",
    "adapter_executed",
    "external_api_called",
    "artifact_read",
    "artifact_hash_read",
    "review_read",
    "file_stat",
    "file_exists_check",
    "hash_calculated",
    "ledger_read",
    "notification_ledger_written",
    "published",
    "public_url_generated",
    "generated_state",
    "generated_transition",
    "gate_execution_result",
    "transition_execution_result",
    "publish_execution_result",
    "noop_completed_persisted",
}

PASS_PUBLISHED_LABEL = "PASS_PUBLISHED"


def _valid_values():
    return {
        "run_id": "run-001",
        "publish_id": "publish-001",
        "publish_mode": "noop",
        "publish_outcome": states.NOOP_COMPLETED,
        "source_state": states.PUBLISH_ALLOWED,
        "target_state": states.NOOP_COMPLETED,
        "public_candidate_ref": "reader.html",
        "gate_decision_envelope_refs": (
            "daily-gate-decision-envelope.yaml",
        ),
        "artifact_hash_manifest_refs": ("artifact-hash.yaml",),
        "artifact_refs": ("reader.html",),
        "redaction_status": "pass",
        "public_url_created": False,
        "public_url_is_null": True,
        "created_at": "caller-supplied-created-at",
        "timestamp_policy": "caller_supplied_no_datetime_parsing",
        "source_of_truth": ("p2d-2g", "p2d-18"),
        "notes": ("shape-only",),
    }


def _explain(**overrides):
    values = _valid_values()
    values.update(overrides)
    return builder.explain_publish_ledger_entry_build(**values)


def test_valid_noop_publish_ledger_entry_is_buildable():
    result = _explain()

    assert result["buildable"] is True
    assert result["reason_code"] == "PUBLISH_LEDGER_ENTRY_BUILDABLE"
    assert result["entry"]["publish_mode"] == "noop"
    assert result["entry"]["publish_outcome"] == states.NOOP_COMPLETED
    assert result["entry"]["source_state"] == states.PUBLISH_ALLOWED
    assert result["entry"]["target_state"] == states.NOOP_COMPLETED
    assert result["entry"]["public_url"] is None
    assert result["entry_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()


def test_result_and_entry_shapes_are_exact():
    result = _explain()

    assert set(result) == REQUIRED_RESULT_FIELDS
    assert tuple(result["entry"].keys()) == REQUIRED_ENTRY_FIELDS
    assert set(result["entry"]) == set(REQUIRED_ENTRY_FIELDS)


def test_missing_required_fields_block_with_dedicated_reasons():
    cases = (
        ("run_id", "", "RUN_ID_MISSING", ("run_id",)),
        ("publish_id", "", "PUBLISH_ID_MISSING", ("publish_id",)),
        (
            "publish_mode",
            "",
            "PUBLISH_MODE_MISSING",
            ("publish_mode",),
        ),
        (
            "publish_outcome",
            "",
            "PUBLISH_OUTCOME_MISSING",
            ("publish_outcome",),
        ),
        (
            "source_state",
            "",
            "SOURCE_STATE_MISSING",
            ("source_state",),
        ),
        (
            "target_state",
            "",
            "TARGET_STATE_MISSING",
            ("target_state",),
        ),
        (
            "public_candidate_ref",
            "",
            "PUBLIC_CANDIDATE_REF_MISSING",
            ("public_candidate_ref",),
        ),
        (
            "gate_decision_envelope_refs",
            (),
            "GATE_DECISION_ENVELOPE_REFS_MISSING",
            ("gate_decision_envelope_refs",),
        ),
        (
            "artifact_hash_manifest_refs",
            (),
            "ARTIFACT_HASH_MANIFEST_REFS_MISSING",
            ("artifact_hash_manifest_refs",),
        ),
        (
            "artifact_refs",
            (),
            "ARTIFACT_REFS_MISSING",
            ("artifact_refs",),
        ),
        (
            "redaction_status",
            "",
            "REDACTION_STATUS_MISSING",
            ("redaction_status",),
        ),
        ("created_at", "", "CREATED_AT_MISSING", ("created_at",)),
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
        ("run_id", " ", "RUN_ID_MISSING"),
        ("publish_id", "\t", "PUBLISH_ID_MISSING"),
        ("publish_mode", "\n", "PUBLISH_MODE_MISSING"),
        ("publish_outcome", " ", "PUBLISH_OUTCOME_MISSING"),
        ("source_state", " ", "SOURCE_STATE_MISSING"),
        ("target_state", "\t", "TARGET_STATE_MISSING"),
        (
            "public_candidate_ref",
            "\n",
            "PUBLIC_CANDIDATE_REF_MISSING",
        ),
        ("redaction_status", " ", "REDACTION_STATUS_MISSING"),
        ("created_at", "\t", "CREATED_AT_MISSING"),
        ("timestamp_policy", "\n", "TIMESTAMP_POLICY_MISSING"),
    )

    for field_name, value, reason_code in cases:
        result = _explain(**{field_name: value})

        assert result["reason_code"] == reason_code


def test_publish_mode_must_be_exactly_noop():
    for publish_mode in ("real", "NOOP", "noop "):
        result = _explain(publish_mode=publish_mode)

        assert result["buildable"] is False
        assert result["reason_code"] == "PUBLISH_MODE_NOT_NOOP"
        assert result["missing_or_invalid_fields"] == ("publish_mode",)


def test_publish_outcome_must_be_noop_completed():
    for publish_outcome in (
        states.PUBLISH_ALLOWED,
        states.REVIEW_BLOCKED,
        "noop_completed",
    ):
        result = _explain(publish_outcome=publish_outcome)

        assert result["buildable"] is False
        assert (
            result["reason_code"]
            == "PUBLISH_OUTCOME_NOT_NOOP_COMPLETED"
        )
        assert result["missing_or_invalid_fields"] == ("publish_outcome",)


def test_source_state_unknown_and_known_wrong_are_distinct():
    unknown = _explain(source_state="UNKNOWN_STATE")
    known_wrong = _explain(source_state=states.AUDITING)

    assert unknown["reason_code"] == "SOURCE_STATE_UNKNOWN"
    assert known_wrong["reason_code"] == "SOURCE_STATE_NOT_PUBLISH_ALLOWED"


def test_target_state_unknown_and_known_wrong_are_distinct():
    unknown = _explain(target_state="UNKNOWN_STATE")
    known_wrong = _explain(target_state=states.PUBLISH_ALLOWED)

    assert unknown["reason_code"] == "TARGET_STATE_UNKNOWN"
    assert known_wrong["reason_code"] == "TARGET_STATE_NOT_NOOP_COMPLETED"


def test_pass_published_external_label_is_rejected_without_states_dependency():
    outcome = _explain(publish_outcome=PASS_PUBLISHED_LABEL)
    source = _explain(source_state=PASS_PUBLISHED_LABEL)
    target = _explain(target_state=PASS_PUBLISHED_LABEL)

    assert (
        outcome["reason_code"]
        == "PUBLISH_OUTCOME_NOT_NOOP_COMPLETED"
    )
    assert source["reason_code"] == (
        "SOURCE_STATE_UNKNOWN"
        if PASS_PUBLISHED_LABEL not in states.MVP_STATES
        else "SOURCE_STATE_NOT_PUBLISH_ALLOWED"
    )
    assert target["reason_code"] == (
        "TARGET_STATE_UNKNOWN"
        if PASS_PUBLISHED_LABEL not in states.MVP_STATES
        else "TARGET_STATE_NOT_NOOP_COMPLETED"
    )
    assert builder._PASS_PUBLISHED_LABEL == PASS_PUBLISHED_LABEL


def test_public_url_created_true_and_non_null_marker_block():
    created = _explain(public_url_created=True)
    non_null = _explain(public_url_is_null=False)

    assert created["reason_code"] == "PUBLIC_URL_CREATED_TRUE"
    assert created["missing_or_invalid_fields"] == ("public_url_created",)
    assert non_null["reason_code"] == "PUBLIC_URL_NON_NULL"
    assert non_null["missing_or_invalid_fields"] == ("public_url",)


def test_entry_public_url_is_always_none():
    results = (
        _explain(),
        _explain(public_url_created=True),
        _explain(public_url_is_null=False),
    )

    for result in results:
        assert result["entry"]["public_url"] is None
        assert "public_url_is_null" not in result
        assert "public_url_is_null" not in result["entry"]


def test_no_raw_url_or_credentials_appear_in_results():
    results = (_explain(), _explain(public_url_is_null=False))
    forbidden_values = (
        "https://public.example.invalid/daily",
        "secret-token",
        "provider-secret-value",
        "raw-credential-value",
    )

    for result in results:
        rendered_result = repr(result)
        for forbidden_value in forbidden_values:
            assert forbidden_value not in rendered_result


def test_reason_priority_and_all_violations_are_collected():
    result = _explain(
        run_id="",
        publish_id="",
        publish_mode="",
        publish_outcome="",
        source_state="",
        target_state="",
        public_candidate_ref="",
        gate_decision_envelope_refs=(),
        artifact_hash_manifest_refs=(),
        artifact_refs=(),
        redaction_status="",
        public_url_created=True,
        public_url_is_null=False,
        created_at="",
        timestamp_policy="",
        source_of_truth=(),
    )

    assert result["buildable"] is False
    assert result["reason_code"] == "RUN_ID_MISSING"
    assert result["reason_code"] == result["entry_violations"][0]
    assert result["entry_violations"] == (
        "RUN_ID_MISSING",
        "PUBLISH_ID_MISSING",
        "PUBLISH_MODE_MISSING",
        "PUBLISH_OUTCOME_MISSING",
        "SOURCE_STATE_MISSING",
        "TARGET_STATE_MISSING",
        "PUBLIC_CANDIDATE_REF_MISSING",
        "GATE_DECISION_ENVELOPE_REFS_MISSING",
        "ARTIFACT_HASH_MANIFEST_REFS_MISSING",
        "ARTIFACT_REFS_MISSING",
        "REDACTION_STATUS_MISSING",
        "CREATED_AT_MISSING",
        "TIMESTAMP_POLICY_MISSING",
        "SOURCE_OF_TRUTH_MISSING",
        "PUBLIC_URL_CREATED_TRUE",
        "PUBLIC_URL_NON_NULL",
    )
    assert result["missing_or_invalid_fields"] == (
        "run_id",
        "publish_id",
        "publish_mode",
        "publish_outcome",
        "source_state",
        "target_state",
        "public_candidate_ref",
        "gate_decision_envelope_refs",
        "artifact_hash_manifest_refs",
        "artifact_refs",
        "redaction_status",
        "created_at",
        "timestamp_policy",
        "source_of_truth",
        "public_url_created",
        "public_url",
    )


def test_bool_wrapper_matches_explanation():
    cases = (
        _valid_values(),
        dict(_valid_values(), run_id=""),
        dict(_valid_values(), publish_mode="real"),
        dict(_valid_values(), source_state=states.AUDITING),
        dict(_valid_values(), public_url_is_null=False),
    )

    for values in cases:
        explanation = builder.explain_publish_ledger_entry_build(**values)

        assert (
            builder.is_publish_ledger_entry_buildable(**values)
            is explanation["buildable"]
        )


def test_reason_catalog_contains_only_executable_reason_codes():
    assert builder.PUBLISH_LEDGER_ENTRY_BUILD_REASON_CODES == (
        "RUN_ID_MISSING",
        "PUBLISH_ID_MISSING",
        "PUBLISH_MODE_MISSING",
        "PUBLISH_MODE_NOT_NOOP",
        "PUBLISH_OUTCOME_MISSING",
        "PUBLISH_OUTCOME_NOT_NOOP_COMPLETED",
        "SOURCE_STATE_MISSING",
        "SOURCE_STATE_UNKNOWN",
        "SOURCE_STATE_NOT_PUBLISH_ALLOWED",
        "TARGET_STATE_MISSING",
        "TARGET_STATE_UNKNOWN",
        "TARGET_STATE_NOT_NOOP_COMPLETED",
        "PUBLIC_CANDIDATE_REF_MISSING",
        "GATE_DECISION_ENVELOPE_REFS_MISSING",
        "ARTIFACT_HASH_MANIFEST_REFS_MISSING",
        "ARTIFACT_REFS_MISSING",
        "REDACTION_STATUS_MISSING",
        "CREATED_AT_MISSING",
        "TIMESTAMP_POLICY_MISSING",
        "SOURCE_OF_TRUTH_MISSING",
        "PUBLIC_URL_CREATED_TRUE",
        "PUBLIC_URL_NON_NULL",
        "PUBLISH_LEDGER_ENTRY_BUILDABLE",
    )
    forbidden_codes = {
        "PUBLISH_LEDGER_WRITE_" + "FORBIDDEN",
        "PUBLISH_" + "FORBIDDEN",
        "PUBLIC_URL_CREATION_" + "FORBIDDEN",
        "NOTIFICATION_" + "FORBIDDEN",
        "LEDGER_WRITE_" + "FORBIDDEN",
        "GATE_EXECUTION_" + "FORBIDDEN",
        "TRANSITION_EXECUTION_" + "FORBIDDEN",
    }

    assert forbidden_codes.isdisjoint(
        builder.PUBLISH_LEDGER_ENTRY_BUILD_REASON_CODES
    )


def test_states_constants_are_not_mutated():
    mvp_states_before = states.MVP_STATES
    state_invariants_before = states.STATE_INVARIANTS

    _explain()
    _explain(source_state=PASS_PUBLISHED_LABEL)
    builder.is_publish_ledger_entry_buildable(**_valid_values())

    assert states.MVP_STATES == mvp_states_before
    assert states.STATE_INVARIANTS == state_invariants_before


def test_module_namespace_does_not_import_forbidden_modules_or_io_libraries():
    forbidden_names = {
        "gates",
        "artifacts",
        "gate_decision_mapper",
        "transition_guard",
        "noop_completion_policy",
        "adapter_gate_evidence_policy",
        "adapter_gate_decision_policy",
        "daily_gate_evidence_policy",
        "daily_gate_decision_policy",
        "gate_decision_envelope_builder",
        "run_ledger_entry_builder",
        "failure_package_builder",
        "badcase_record_builder",
        "artifact_hash_manifest_builder",
        "artifact_inventory_policy",
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


def test_result_does_not_expose_payload_paths_controls_or_execution_fields():
    results = (
        _explain(),
        _explain(public_url_is_null=False),
        _explain(publish_outcome=PASS_PUBLISHED_LABEL),
    )

    for result in results:
        assert FORBIDDEN_RESULT_KEYS.isdisjoint(result)
        assert FORBIDDEN_RESULT_KEYS.isdisjoint(result["entry"])


def test_invariant_refs_capture_builder_and_safety_boundaries():
    result = _explain()
    required_invariants = {
        "publish_ledger_entry_builder_only",
        "builder_not_publisher",
        "builder_not_notifier",
        "builder_not_public_url_creator",
        "builder_not_publish_ledger_writer",
        "builder_not_notification_ledger_writer",
        "builder_not_ledger_writer",
        "builder_not_gate_execution",
        "builder_not_transition_mapping",
        "builder_not_transition_execution",
        "builder_not_noop_completion_executor",
        "buildable_not_publish_ledger_write",
        "buildable_not_publish_execution",
        "buildable_not_public_url_creation",
        "buildable_not_notification",
        "buildable_not_gate_execution",
        "buildable_not_transition_execution",
        "buildable_not_run_ledger_persistence",
        "no_runtime_context_config_or_credential_read",
        "no_adapter_preflight",
        "no_external_adapter_call",
        "no_raw_credentials",
        "no_raw_public_url",
        "no_quality_pass_no_public_url",
        "noop_only_publish_mode",
        "noop_completed_not_pass_published",
        "daily_gate_pass_not_direct_publish",
        "publish_allowed_to_noop_completed_marker_only",
        "no_artifact_hash_or_review_io",
        "no_hashlib",
        "no_hash_calculation",
        "no_ledger_write",
        "no_publish_ledger_write",
        "no_public_url_behavior",
        "no_noop_completion_policy_call",
        "no_gate_decision_mapper_call",
        "no_transition_guard_call",
        "no_artifact_inventory_policy_call",
        "no_gate_decision_envelope_builder_call",
        "no_run_ledger_entry_builder_call",
        "no_artifact_hash_manifest_builder_call",
    }

    assert required_invariants <= set(result["invariant_refs"])
    assert set(states.STATE_INVARIANTS) <= set(result["invariant_refs"])
