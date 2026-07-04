"""Focused contract tests for the pure Notification Ledger Entry builder."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import (
    notification_ledger_entry_builder as builder,
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
    "notification_id",
    "notification_mode",
    "notification_outcome",
    "run_state",
    "publish_ledger_entry_refs",
    "gate_decision_envelope_refs",
    "artifact_hash_manifest_refs",
    "artifact_refs",
    "redaction_status",
    "notification_sent",
    "external_notification_created",
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
    "recipient_refs",
    "notification_target_refs",
    "email_address",
    "webhook_url",
    "im_target",
    "contact_id",
    "runtime_context",
    "config_snapshot",
    "adapter_outputs",
    "adapter_preflight_result",
    "publish_ledger_content",
    "review_content",
    "artifact_contents",
    "artifact_hash_manifest_content",
    "artifact_hash_values",
    "ledger_path",
    "notification_ledger_path",
    "publish_ledger_path",
    "artifact_hash_path",
    "run_ledger_path",
    "gate_decision_envelope",
    "publish_ledger_entry",
    "artifact_hash_manifest",
    "run_ledger_entry",
    "should_write_notification_ledger",
    "should_notify",
    "should_send_email",
    "should_call_webhook",
    "should_create_public_url",
    "should_transition",
    "should_write_ledger",
    "notification_executed",
    "email_sent",
    "webhook_called",
    "im_sent",
    "url_created",
    "gate_executed",
    "transition_executed",
    "ledger_written",
    "notification_ledger_written",
    "public_url_reserved",
    "public_url_faked",
    "runtime_context_read",
    "config_read",
    "credential_read",
    "contact_read",
    "email_account_read",
    "webhook_url_read",
    "im_target_read",
    "adapter_preflight_executed",
    "adapter_executed",
    "external_api_called",
    "artifact_read",
    "artifact_hash_read",
    "publish_ledger_read",
    "review_read",
    "file_stat",
    "file_exists_check",
    "hash_calculated",
    "ledger_read",
    "published",
    "notified",
    "public_url_generated",
    "generated_state",
    "generated_transition",
    "gate_execution_result",
    "transition_execution_result",
    "notification_execution_result",
    "noop_completed_persisted",
}

PASS_PUBLISHED_LABEL = "PASS_PUBLISHED"


def _valid_values():
    return {
        "run_id": "run-001",
        "notification_id": "notification-001",
        "notification_mode": "noop",
        "notification_outcome": "NOOP_NOTIFICATION_SKIPPED",
        "run_state": states.NOOP_COMPLETED,
        "publish_ledger_entry_refs": (
            "publish-ledger.yaml#publish-001",
        ),
        "gate_decision_envelope_refs": (
            "daily-gate-decision-envelope.yaml",
        ),
        "artifact_hash_manifest_refs": ("artifact-hash.yaml",),
        "artifact_refs": ("reader.html",),
        "redaction_status": "pass",
        "notification_sent": False,
        "external_notification_created": False,
        "public_url_created": False,
        "public_url_is_null": True,
        "created_at": "caller-supplied-created-at",
        "timestamp_policy": "caller_supplied_no_datetime_parsing",
        "source_of_truth": ("p2d-2g", "p2d-19"),
        "notes": ("shape-only",),
    }


def _explain(**overrides):
    values = _valid_values()
    values.update(overrides)
    return builder.explain_notification_ledger_entry_build(**values)


def test_valid_noop_notification_ledger_entry_is_buildable():
    result = _explain()

    assert result["buildable"] is True
    assert result["reason_code"] == "NOTIFICATION_LEDGER_ENTRY_BUILDABLE"
    assert result["entry"]["notification_mode"] == "noop"
    assert (
        result["entry"]["notification_outcome"]
        == "NOOP_NOTIFICATION_SKIPPED"
    )
    assert result["entry"]["run_state"] == states.NOOP_COMPLETED
    assert result["entry"]["notification_sent"] is False
    assert result["entry"]["external_notification_created"] is False
    assert result["entry"]["public_url_created"] is False
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
        (
            "notification_id",
            "",
            "NOTIFICATION_ID_MISSING",
            ("notification_id",),
        ),
        (
            "notification_mode",
            "",
            "NOTIFICATION_MODE_MISSING",
            ("notification_mode",),
        ),
        (
            "notification_outcome",
            "",
            "NOTIFICATION_OUTCOME_MISSING",
            ("notification_outcome",),
        ),
        (
            "run_state",
            "",
            "RUN_STATE_MISSING",
            ("run_state",),
        ),
        (
            "publish_ledger_entry_refs",
            (),
            "PUBLISH_LEDGER_ENTRY_REFS_MISSING",
            ("publish_ledger_entry_refs",),
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
        ("notification_id", "\t", "NOTIFICATION_ID_MISSING"),
        ("notification_mode", "\n", "NOTIFICATION_MODE_MISSING"),
        (
            "notification_outcome",
            " ",
            "NOTIFICATION_OUTCOME_MISSING",
        ),
        ("run_state", "\t", "RUN_STATE_MISSING"),
        ("redaction_status", "\n", "REDACTION_STATUS_MISSING"),
        ("created_at", " ", "CREATED_AT_MISSING"),
        ("timestamp_policy", "\t", "TIMESTAMP_POLICY_MISSING"),
    )

    for field_name, value, reason_code in cases:
        result = _explain(**{field_name: value})

        assert result["reason_code"] == reason_code


def test_notification_mode_must_be_exactly_noop():
    for notification_mode in ("none", "real", "NOOP", "noop "):
        result = _explain(notification_mode=notification_mode)

        assert result["buildable"] is False
        assert result["reason_code"] == "NOTIFICATION_MODE_NOT_NOOP"
        assert result["missing_or_invalid_fields"] == (
            "notification_mode",
        )


def test_notification_outcome_must_be_noop_notification_skipped():
    for notification_outcome in (
        states.NOOP_COMPLETED,
        "NOTIFICATION_SENT",
        "noop_notification_skipped",
    ):
        result = _explain(notification_outcome=notification_outcome)

        assert result["buildable"] is False
        assert (
            result["reason_code"]
            == "NOTIFICATION_OUTCOME_NOT_NOOP_SKIPPED"
        )
        assert result["missing_or_invalid_fields"] == (
            "notification_outcome",
        )


def test_run_state_unknown_and_known_wrong_are_distinct():
    unknown = _explain(run_state="UNKNOWN_STATE")
    known_wrong = _explain(run_state=states.PUBLISH_ALLOWED)

    assert unknown["reason_code"] == "RUN_STATE_UNKNOWN"
    assert known_wrong["reason_code"] == (
        "RUN_STATE_NOT_NOOP_COMPLETED"
    )


def test_pass_published_is_rejected_without_states_dependency():
    outcome = _explain(notification_outcome=PASS_PUBLISHED_LABEL)
    run_state = _explain(run_state=PASS_PUBLISHED_LABEL)

    assert (
        outcome["reason_code"]
        == "NOTIFICATION_OUTCOME_NOT_NOOP_SKIPPED"
    )
    assert run_state["reason_code"] == (
        "RUN_STATE_UNKNOWN"
        if PASS_PUBLISHED_LABEL not in states.MVP_STATES
        else "RUN_STATE_NOT_NOOP_COMPLETED"
    )
    assert builder._PASS_PUBLISHED_LABEL == PASS_PUBLISHED_LABEL
    assert PASS_PUBLISHED_LABEL not in states.MVP_STATES


def test_notification_sent_true_blocks():
    result = _explain(notification_sent=True)

    assert result["reason_code"] == "NOTIFICATION_SENT_TRUE"
    assert result["missing_or_invalid_fields"] == ("notification_sent",)


def test_external_notification_created_true_blocks():
    result = _explain(external_notification_created=True)

    assert result["reason_code"] == "EXTERNAL_NOTIFICATION_CREATED_TRUE"
    assert result["missing_or_invalid_fields"] == (
        "external_notification_created",
    )


def test_public_url_created_true_and_non_null_marker_block():
    created = _explain(public_url_created=True)
    non_null = _explain(public_url_is_null=False)

    assert created["reason_code"] == "PUBLIC_URL_CREATED_TRUE"
    assert created["missing_or_invalid_fields"] == (
        "public_url_created",
    )
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


def test_no_raw_url_credentials_or_notification_targets_appear():
    results = (
        _explain(),
        _explain(public_url_is_null=False),
        _explain(notification_sent=True),
    )
    forbidden_values = (
        "https://public.example.invalid/daily",
        "secret-token",
        "raw-credential-value",
        "person@example.invalid",
        "https://hooks.example.invalid/secret",
        "im-target-001",
        "contact-001",
    )

    for result in results:
        rendered_result = repr(result)
        for forbidden_value in forbidden_values:
            assert forbidden_value not in rendered_result


def test_reason_priority_and_all_violations_are_collected():
    result = _explain(
        run_id="",
        notification_id="",
        notification_mode="",
        notification_outcome="",
        run_state="",
        publish_ledger_entry_refs=(),
        gate_decision_envelope_refs=(),
        artifact_hash_manifest_refs=(),
        artifact_refs=(),
        redaction_status="",
        notification_sent=True,
        external_notification_created=True,
        created_at="",
        timestamp_policy="",
        source_of_truth=(),
        public_url_created=True,
        public_url_is_null=False,
    )

    assert result["buildable"] is False
    assert result["reason_code"] == "RUN_ID_MISSING"
    assert result["reason_code"] == result["entry_violations"][0]
    assert result["entry_violations"] == (
        "RUN_ID_MISSING",
        "NOTIFICATION_ID_MISSING",
        "NOTIFICATION_MODE_MISSING",
        "NOTIFICATION_OUTCOME_MISSING",
        "RUN_STATE_MISSING",
        "PUBLISH_LEDGER_ENTRY_REFS_MISSING",
        "GATE_DECISION_ENVELOPE_REFS_MISSING",
        "ARTIFACT_HASH_MANIFEST_REFS_MISSING",
        "ARTIFACT_REFS_MISSING",
        "REDACTION_STATUS_MISSING",
        "NOTIFICATION_SENT_TRUE",
        "EXTERNAL_NOTIFICATION_CREATED_TRUE",
        "CREATED_AT_MISSING",
        "TIMESTAMP_POLICY_MISSING",
        "SOURCE_OF_TRUTH_MISSING",
        "PUBLIC_URL_CREATED_TRUE",
        "PUBLIC_URL_NON_NULL",
    )
    assert result["missing_or_invalid_fields"] == (
        "run_id",
        "notification_id",
        "notification_mode",
        "notification_outcome",
        "run_state",
        "publish_ledger_entry_refs",
        "gate_decision_envelope_refs",
        "artifact_hash_manifest_refs",
        "artifact_refs",
        "redaction_status",
        "notification_sent",
        "external_notification_created",
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
        dict(_valid_values(), notification_mode="real"),
        dict(_valid_values(), run_state=states.PUBLISH_ALLOWED),
        dict(_valid_values(), notification_sent=True),
        dict(_valid_values(), public_url_is_null=False),
    )

    for values in cases:
        explanation = builder.explain_notification_ledger_entry_build(
            **values
        )

        assert (
            builder.is_notification_ledger_entry_buildable(**values)
            is explanation["buildable"]
        )


def test_reason_catalog_contains_only_executable_reason_codes():
    assert builder.NOTIFICATION_LEDGER_ENTRY_BUILD_REASON_CODES == (
        "RUN_ID_MISSING",
        "NOTIFICATION_ID_MISSING",
        "NOTIFICATION_MODE_MISSING",
        "NOTIFICATION_MODE_NOT_NOOP",
        "NOTIFICATION_OUTCOME_MISSING",
        "NOTIFICATION_OUTCOME_NOT_NOOP_SKIPPED",
        "RUN_STATE_MISSING",
        "RUN_STATE_UNKNOWN",
        "RUN_STATE_NOT_NOOP_COMPLETED",
        "PUBLISH_LEDGER_ENTRY_REFS_MISSING",
        "GATE_DECISION_ENVELOPE_REFS_MISSING",
        "ARTIFACT_HASH_MANIFEST_REFS_MISSING",
        "ARTIFACT_REFS_MISSING",
        "REDACTION_STATUS_MISSING",
        "NOTIFICATION_SENT_TRUE",
        "EXTERNAL_NOTIFICATION_CREATED_TRUE",
        "CREATED_AT_MISSING",
        "TIMESTAMP_POLICY_MISSING",
        "SOURCE_OF_TRUTH_MISSING",
        "PUBLIC_URL_CREATED_TRUE",
        "PUBLIC_URL_NON_NULL",
        "NOTIFICATION_LEDGER_ENTRY_BUILDABLE",
    )
    forbidden_codes = {
        "NOTIFICATION_LEDGER_WRITE_" + "FORBIDDEN",
        "NOTIFICATION_" + "FORBIDDEN",
        "EMAIL_SEND_" + "FORBIDDEN",
        "WEBHOOK_CALL_" + "FORBIDDEN",
        "IM_SEND_" + "FORBIDDEN",
        "PUBLIC_URL_CREATION_" + "FORBIDDEN",
        "LEDGER_WRITE_" + "FORBIDDEN",
        "GATE_EXECUTION_" + "FORBIDDEN",
        "TRANSITION_EXECUTION_" + "FORBIDDEN",
    }

    assert forbidden_codes.isdisjoint(
        builder.NOTIFICATION_LEDGER_ENTRY_BUILD_REASON_CODES
    )


def test_states_constants_are_not_mutated():
    mvp_states_before = states.MVP_STATES
    state_invariants_before = states.STATE_INVARIANTS

    _explain()
    _explain(run_state=PASS_PUBLISHED_LABEL)
    builder.is_notification_ledger_entry_buildable(**_valid_values())

    assert states.MVP_STATES == mvp_states_before
    assert states.STATE_INVARIANTS == state_invariants_before
    assert states.NOOP_COMPLETED != PASS_PUBLISHED_LABEL


def test_module_namespace_does_not_import_forbidden_modules_or_io_libraries():
    forbidden_names = {
        "gates",
        "artifacts",
        "gate_decision_mapper",
        "transition_guard",
        "noop_completion_policy",
        "publish_ledger_entry_builder",
        "artifact_hash_manifest_builder",
        "adapter_gate_evidence_policy",
        "adapter_gate_decision_policy",
        "daily_gate_evidence_policy",
        "daily_gate_decision_policy",
        "gate_decision_envelope_builder",
        "run_ledger_entry_builder",
        "failure_package_builder",
        "badcase_record_builder",
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
        _explain(notification_outcome=PASS_PUBLISHED_LABEL),
    )

    for result in results:
        assert FORBIDDEN_RESULT_KEYS.isdisjoint(result)
        assert FORBIDDEN_RESULT_KEYS.isdisjoint(result["entry"])


def test_invariant_refs_capture_builder_and_safety_boundaries():
    result = _explain()
    required_invariants = {
        "notification_ledger_entry_builder_only",
        "builder_not_notifier",
        "builder_not_email_sender",
        "builder_not_webhook_sender",
        "builder_not_im_sender",
        "builder_not_public_url_creator",
        "builder_not_notification_ledger_writer",
        "builder_not_publish_ledger_reader",
        "builder_not_ledger_writer",
        "builder_not_gate_execution",
        "builder_not_transition_mapping",
        "builder_not_transition_execution",
        "builder_not_noop_completion_executor",
        "buildable_not_notification_ledger_write",
        "buildable_not_notification_execution",
        "buildable_not_public_url_creation",
        "buildable_not_gate_execution",
        "buildable_not_transition_execution",
        "buildable_not_run_ledger_persistence",
        "no_runtime_context_config_or_credential_read",
        "no_contact_or_recipient_read",
        "no_email_account_or_webhook_or_im_target_read",
        "no_adapter_preflight",
        "no_external_adapter_call",
        "no_raw_credentials",
        "no_raw_public_url",
        "no_raw_recipient_email_webhook_im_target",
        "no_quality_pass_no_public_url",
        "noop_only_notification_mode",
        "noop_notification_skipped_outcome_only",
        "noop_completed_not_pass_published",
        "daily_gate_pass_not_direct_publish",
        "notification_post_completion_marker_only",
        "no_artifact_hash_publish_ledger_or_review_io",
        "no_hashlib",
        "no_hash_calculation",
        "no_ledger_write",
        "no_notification_ledger_write",
        "no_public_url_behavior",
        "no_noop_completion_policy_call",
        "no_gate_decision_mapper_call",
        "no_transition_guard_call",
        "no_artifact_inventory_policy_call",
        "no_gate_decision_envelope_builder_call",
        "no_run_ledger_entry_builder_call",
        "no_artifact_hash_manifest_builder_call",
        "no_publish_ledger_entry_builder_call",
    }

    assert required_invariants <= set(result["invariant_refs"])
    assert set(states.STATE_INVARIANTS) <= set(result["invariant_refs"])
