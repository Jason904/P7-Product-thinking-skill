"""Focused contract tests for the pure Config Snapshot builder."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import config_snapshot_builder as builder
from ai_daily_publishing_system.core import states


REQUIRED_RESULT_FIELDS = {
    "buildable",
    "reason_code",
    "reason",
    "source",
    "snapshot",
    "snapshot_violations",
    "missing_or_invalid_fields",
    "invariant_refs",
}

REQUIRED_SNAPSHOT_FIELDS = (
    "run_id",
    "config_snapshot_id",
    "config_name",
    "config_mode",
    "config_source_mode",
    "runtime_profile_snapshot_ref",
    "publish_mode",
    "notification_mode",
    "eval_mode",
    "adapter_configuration_declared",
    "required_credentials_presence_markers",
    "credential_value_access_enabled",
    "adapter_capability_markers",
    "noop_policy_markers",
    "disabled_external_adapters_declared",
    "environment_safety_marker",
    "redaction_status",
    "created_at",
    "timestamp_policy",
    "source_of_truth",
    "notes",
)

FORBIDDEN_RESULT_KEYS = {
    "run_state",
    "config_snapshot_ref",
    "runtime_context_ref",
    "adapter_preflight_result_ref",
    "public_url",
    "public_url_created",
    "public_url_is_null",
    "raw_public_url",
    "raw_config",
    "config_contents",
    "config_path",
    "credential_values",
    "raw_credentials",
    "env_vars",
    "raw_env_vars",
    "environment",
    "environment_object",
    "adapter_outputs",
    "adapter_preflight_result",
    "driver",
    "driver_name",
    "driver_request_ref",
    "driver_object",
    "driver_credentials",
    "driver_token",
    "runtime_context",
    "runtime_profile",
    "runtime_profile_path",
    "runtime_context_path",
    "artifact_contents",
    "artifact_hash_manifest_content",
    "review_content",
    "ledger_content",
    "ledger_path",
    "artifact_path",
    "should_write_config",
    "should_run_runtime",
    "should_execute_adapter",
    "should_evaluate_gate",
    "should_transition",
    "should_write_ledger",
    "config_read",
    "config_written",
    "runtime_executed",
    "scheduler_executed",
    "adapter_preflight_executed",
    "adapter_executed",
    "gate_executed",
    "transition_executed",
    "ledger_written",
    "runtime_context_written",
    "public_url_reserved",
    "public_url_faked",
    "published",
    "notified",
    "notification_sent",
    "external_api_called",
    "live_llm_called",
    "hash_calculated",
    "file_stat",
    "file_exists_check",
    "artifact_read",
    "artifact_hash_read",
    "publish_ledger_read",
    "notification_ledger_read",
    "run_ledger_read",
    "review_read",
}


def _name(*parts: str) -> str:
    return "_".join(parts)


FORBIDDEN_MODULE_NAMES = (
    "gates",
    "artifacts",
    _name("runtime", "context", "snapshot", "builder"),
    _name("runtime", "profile", "snapshot", "builder"),
    _name("gate", "decision", "mapper"),
    _name("transition", "guard"),
    _name("noop", "completion", "policy"),
    _name("adapter", "gate", "evidence", "policy"),
    _name("adapter", "gate", "decision", "policy"),
    _name("daily", "gate", "evidence", "policy"),
    _name("daily", "gate", "decision", "policy"),
    _name("gate", "decision", "envelope", "builder"),
    _name("run", "ledger", "entry", "builder"),
    _name("failure", "package", "builder"),
    _name("badcase", "record", "builder"),
    _name("artifact", "hash", "manifest", "builder"),
    _name("publish", "ledger", "entry", "builder"),
    _name("notification", "ledger", "entry", "builder"),
    _name("artifact", "inventory", "policy"),
    _name("badcase", "creation", "policy"),
    "pathlib",
    "os",
    "date" + "time",
    "hash" + "lib",
    "logging",
    "sub" + "process",
    "request" + "s",
)


def _pseudo_reason(*parts: str) -> str:
    return "_".join(parts)


FORBIDDEN_PSEUDO_REASON_CODES = (
    _pseudo_reason("CONFIG", "READ", "FORBIDDEN"),
    _pseudo_reason("CONFIG", "WRITE", "FORBIDDEN"),
    _pseudo_reason("CREDENTIAL", "READ", "FORBIDDEN"),
    _pseudo_reason("ENV", "READ", "FORBIDDEN"),
    _pseudo_reason("ADAPTER", "PREFLIGHT", "FORBIDDEN"),
    _pseudo_reason("ADAPTER", "EXECUTION", "FORBIDDEN"),
    _pseudo_reason("DRIVER", "INVOCATION", "FORBIDDEN"),
    _pseudo_reason("GATE", "EXECUTION", "FORBIDDEN"),
    _pseudo_reason("TRANSITION", "EXECUTION", "FORBIDDEN"),
    _pseudo_reason("PUBLIC", "URL", "CREATION", "FORBIDDEN"),
    _pseudo_reason("LEDGER", "WRITE", "FORBIDDEN"),
)


def _valid_values() -> dict[str, object]:
    return {
        "run_id": "run-001",
        "config_snapshot_id": "config-snapshot-001",
        "config_name": "local-noop-config",
        "config_mode": "manual_local_noop",
        "config_source_mode": "caller_supplied",
        "runtime_profile_snapshot_ref": "runtime-profile-snapshot-001",
        "publish_mode": "noop",
        "notification_mode": "noop",
        "eval_mode": "stub",
        "adapter_configuration_declared": True,
        "required_credentials_presence_markers": (
            "credentials_not_required_for_noop",
        ),
        "credential_value_access_enabled": False,
        "adapter_capability_markers": ("noop_adapter_declared",),
        "noop_policy_markers": ("noop_publish", "noop_notification"),
        "disabled_external_adapters_declared": True,
        "environment_safety_marker": "manual_local_noop_environment",
        "redaction_status": "pass",
        "created_at": "caller-supplied-created-at",
        "timestamp_policy": "caller_supplied_no_datetime_parsing",
        "source_of_truth": ("p2d-20", "p2d-22"),
        "notes": ("shape-only",),
    }


def _explain(**overrides: object) -> dict[str, object]:
    values = _valid_values()
    values.update(overrides)
    return builder.explain_config_snapshot_build(**values)


def test_valid_manual_local_noop_config_snapshot_is_buildable():
    result = _explain()

    assert result["buildable"] is True
    assert result["reason_code"] == "CONFIG_SNAPSHOT_BUILDABLE"
    assert result["snapshot"]["config_snapshot_id"] == "config-snapshot-001"
    assert result["snapshot"]["config_mode"] == "manual_local_noop"
    assert result["snapshot"]["config_source_mode"] == "caller_supplied"
    assert result["snapshot"]["publish_mode"] == "noop"
    assert result["snapshot"]["notification_mode"] == "noop"
    assert result["snapshot"]["eval_mode"] == "stub"
    assert result["snapshot"]["credential_value_access_enabled"] is False
    assert result["snapshot_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()


def test_result_and_snapshot_shapes_are_exact():
    result = _explain()

    assert set(result) == REQUIRED_RESULT_FIELDS
    assert tuple(result["snapshot"].keys()) == REQUIRED_SNAPSHOT_FIELDS
    assert set(result["snapshot"]) == set(REQUIRED_SNAPSHOT_FIELDS)


def test_missing_required_fields_block_with_dedicated_reasons():
    cases = (
        ("run_id", "", "RUN_ID_MISSING", ("run_id",)),
        (
            "config_snapshot_id",
            "",
            "CONFIG_SNAPSHOT_ID_MISSING",
            ("config_snapshot_id",),
        ),
        ("config_name", "", "CONFIG_NAME_MISSING", ("config_name",)),
        ("config_mode", "", "CONFIG_MODE_MISSING", ("config_mode",)),
        (
            "config_source_mode",
            "",
            "CONFIG_SOURCE_MODE_MISSING",
            ("config_source_mode",),
        ),
        (
            "runtime_profile_snapshot_ref",
            "",
            "RUNTIME_PROFILE_SNAPSHOT_REF_MISSING",
            ("runtime_profile_snapshot_ref",),
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
            "adapter_configuration_declared",
            False,
            "ADAPTER_CONFIGURATION_NOT_DECLARED",
            ("adapter_configuration_declared",),
        ),
        (
            "required_credentials_presence_markers",
            (),
            "REQUIRED_CREDENTIALS_PRESENCE_MARKERS_MISSING",
            ("required_credentials_presence_markers",),
        ),
        (
            "credential_value_access_enabled",
            True,
            "CREDENTIAL_VALUE_ACCESS_ENABLED_TRUE",
            ("credential_value_access_enabled",),
        ),
        (
            "adapter_capability_markers",
            (),
            "ADAPTER_CAPABILITY_MARKERS_MISSING",
            ("adapter_capability_markers",),
        ),
        (
            "noop_policy_markers",
            (),
            "NOOP_POLICY_MARKERS_MISSING",
            ("noop_policy_markers",),
        ),
        (
            "disabled_external_adapters_declared",
            False,
            "DISABLED_EXTERNAL_ADAPTERS_NOT_DECLARED",
            ("disabled_external_adapters_declared",),
        ),
        (
            "environment_safety_marker",
            "",
            "ENVIRONMENT_SAFETY_MARKER_MISSING",
            ("environment_safety_marker",),
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
        assert result["snapshot_violations"] == (reason_code,)
        assert result["missing_or_invalid_fields"] == invalid_fields


def test_whitespace_required_strings_are_missing():
    cases = (
        ("run_id", "   ", "RUN_ID_MISSING"),
        (
            "config_snapshot_id",
            "\n",
            "CONFIG_SNAPSHOT_ID_MISSING",
        ),
        ("config_name", "\t", "CONFIG_NAME_MISSING"),
        ("config_mode", "   ", "CONFIG_MODE_MISSING"),
        ("config_source_mode", "\n", "CONFIG_SOURCE_MODE_MISSING"),
        (
            "runtime_profile_snapshot_ref",
            "   ",
            "RUNTIME_PROFILE_SNAPSHOT_REF_MISSING",
        ),
        ("publish_mode", "\t", "PUBLISH_MODE_MISSING"),
        ("notification_mode", "   ", "NOTIFICATION_MODE_MISSING"),
        ("eval_mode", "\n", "EVAL_MODE_MISSING"),
        (
            "environment_safety_marker",
            "   ",
            "ENVIRONMENT_SAFETY_MARKER_MISSING",
        ),
        ("redaction_status", "   ", "REDACTION_STATUS_MISSING"),
        ("created_at", "\n", "CREATED_AT_MISSING"),
        ("timestamp_policy", "   ", "TIMESTAMP_POLICY_MISSING"),
    )

    for field_name, value, reason_code in cases:
        result = _explain(**{field_name: value})

        assert result["buildable"] is False
        assert result["reason_code"] == reason_code


def test_config_mode_must_be_manual_local_noop():
    for config_mode in ("local", "manual", "noop", "NOOP"):
        result = _explain(config_mode=config_mode)

        assert result["buildable"] is False
        assert result["reason_code"] == "CONFIG_MODE_NOT_MANUAL_LOCAL_NOOP"
        assert result["missing_or_invalid_fields"] == ("config_mode",)


def test_config_source_mode_must_be_caller_supplied():
    for config_source_mode in ("file", "env", "runtime", "CALLER_SUPPLIED"):
        result = _explain(config_source_mode=config_source_mode)

        assert result["buildable"] is False
        assert (
            result["reason_code"]
            == "CONFIG_SOURCE_MODE_NOT_CALLER_SUPPLIED"
        )
        assert result["missing_or_invalid_fields"] == (
            "config_source_mode",
        )


def test_publish_and_notification_modes_must_be_noop():
    publish_result = _explain(publish_mode="real")
    notification_result = _explain(notification_mode="none")

    assert publish_result["buildable"] is False
    assert publish_result["reason_code"] == "PUBLISH_MODE_NOT_NOOP"
    assert publish_result["missing_or_invalid_fields"] == ("publish_mode",)
    assert notification_result["buildable"] is False
    assert (
        notification_result["reason_code"] == "NOTIFICATION_MODE_NOT_NOOP"
    )
    assert notification_result["missing_or_invalid_fields"] == (
        "notification_mode",
    )


def test_eval_mode_only_requires_non_empty_declaration():
    for eval_mode in ("stub", "noop", "manual_review_stub"):
        result = _explain(eval_mode=eval_mode)

        assert result["buildable"] is True
        assert result["snapshot"]["eval_mode"] == eval_mode

    blocked = _explain(eval_mode="")
    assert blocked["buildable"] is False
    assert blocked["reason_code"] == "EVAL_MODE_MISSING"
    assert "EVAL_MODE_NOT_" not in repr(builder.__dict__)


def test_manual_local_noop_marker_booleans_are_required():
    cases = (
        (
            "adapter_configuration_declared",
            False,
            "ADAPTER_CONFIGURATION_NOT_DECLARED",
        ),
        (
            "credential_value_access_enabled",
            True,
            "CREDENTIAL_VALUE_ACCESS_ENABLED_TRUE",
        ),
        (
            "disabled_external_adapters_declared",
            False,
            "DISABLED_EXTERNAL_ADAPTERS_NOT_DECLARED",
        ),
    )

    for field_name, value, reason_code in cases:
        result = _explain(**{field_name: value})

        assert result["buildable"] is False
        assert result["reason_code"] == reason_code
        assert result["missing_or_invalid_fields"] == (field_name,)


def test_marker_tuples_are_required():
    cases = (
        (
            "required_credentials_presence_markers",
            (),
            "REQUIRED_CREDENTIALS_PRESENCE_MARKERS_MISSING",
        ),
        (
            "adapter_capability_markers",
            (),
            "ADAPTER_CAPABILITY_MARKERS_MISSING",
        ),
        (
            "noop_policy_markers",
            (),
            "NOOP_POLICY_MARKERS_MISSING",
        ),
    )

    for field_name, value, reason_code in cases:
        result = _explain(**{field_name: value})

        assert result["buildable"] is False
        assert result["reason_code"] == reason_code
        assert result["missing_or_invalid_fields"] == (field_name,)


def test_no_forbidden_reference_or_public_url_fields_exist():
    result = _explain()

    for field_name in (
        "run_state",
        "config_snapshot_ref",
        "runtime_context_ref",
        "adapter_preflight_result_ref",
        "public_url",
        "public_url_created",
        "public_url_is_null",
        "raw_public_url",
    ):
        assert field_name not in result
        assert field_name not in result["snapshot"]


def test_result_does_not_include_raw_or_execution_fields():
    result = _explain()
    blocked = _explain(run_id="", publish_mode="real")
    allowed_raw_boundary_invariants = {
        "no_raw_config",
        "no_raw_credentials",
        "no_raw_env_vars",
        "no_raw_adapter_outputs",
        "no_raw_driver_object",
        "no_raw_public_url",
    }
    result_without_invariants = {
        key: value for key, value in result.items() if key != "invariant_refs"
    }
    result_contract_repr = repr(result_without_invariants)

    assert FORBIDDEN_RESULT_KEYS.isdisjoint(result)
    assert FORBIDDEN_RESULT_KEYS.isdisjoint(result["snapshot"])
    assert FORBIDDEN_RESULT_KEYS.isdisjoint(blocked)
    assert FORBIDDEN_RESULT_KEYS.isdisjoint(blocked["snapshot"])
    assert allowed_raw_boundary_invariants <= set(result["invariant_refs"])
    assert "https://" not in result_contract_repr
    assert "http://" not in result_contract_repr
    assert "secret" not in result_contract_repr.lower()
    assert "token" not in result_contract_repr.lower()
    assert "raw_config" not in result_contract_repr
    assert "raw_env" not in result_contract_repr
    assert "adapter_outputs" not in result_contract_repr
    assert "driver_object" not in result_contract_repr


def test_no_runtime_profile_context_config_adapter_artifact_or_ledger_leakage():
    result = _explain()
    result_without_invariants = {
        key: value for key, value in result.items() if key != "invariant_refs"
    }

    forbidden_fragments = (
        "runtime_context_path",
        "runtime_profile_path",
        "config_path",
        "adapter_preflight_result",
        "artifact_contents",
        "artifact_hash_manifest_content",
        "review_content",
        "ledger_content",
        "ledger_path",
        "should_write",
        "should_run",
        "should_execute",
        "should_evaluate",
        "should_transition",
    )
    result_contract_repr = repr(result_without_invariants)

    for fragment in forbidden_fragments:
        assert fragment not in result_contract_repr


def test_reason_priority_and_all_violations_are_collected():
    result = _explain(
        run_id="",
        config_snapshot_id="",
        config_name="",
        config_mode="real",
        config_source_mode="file",
        runtime_profile_snapshot_ref="",
        publish_mode="real",
        notification_mode="real",
        eval_mode="",
        adapter_configuration_declared=False,
        required_credentials_presence_markers=(),
        credential_value_access_enabled=True,
        adapter_capability_markers=(),
        noop_policy_markers=(),
        disabled_external_adapters_declared=False,
        environment_safety_marker="",
        redaction_status="",
        created_at="",
        timestamp_policy="",
        source_of_truth=(),
    )

    expected_violations = (
        "RUN_ID_MISSING",
        "CONFIG_SNAPSHOT_ID_MISSING",
        "CONFIG_NAME_MISSING",
        "CONFIG_MODE_NOT_MANUAL_LOCAL_NOOP",
        "CONFIG_SOURCE_MODE_NOT_CALLER_SUPPLIED",
        "RUNTIME_PROFILE_SNAPSHOT_REF_MISSING",
        "PUBLISH_MODE_NOT_NOOP",
        "NOTIFICATION_MODE_NOT_NOOP",
        "EVAL_MODE_MISSING",
        "ADAPTER_CONFIGURATION_NOT_DECLARED",
        "REQUIRED_CREDENTIALS_PRESENCE_MARKERS_MISSING",
        "CREDENTIAL_VALUE_ACCESS_ENABLED_TRUE",
        "ADAPTER_CAPABILITY_MARKERS_MISSING",
        "NOOP_POLICY_MARKERS_MISSING",
        "DISABLED_EXTERNAL_ADAPTERS_NOT_DECLARED",
        "ENVIRONMENT_SAFETY_MARKER_MISSING",
        "REDACTION_STATUS_MISSING",
        "CREATED_AT_MISSING",
        "TIMESTAMP_POLICY_MISSING",
        "SOURCE_OF_TRUTH_MISSING",
    )

    assert result["buildable"] is False
    assert result["reason_code"] == expected_violations[0]
    assert result["reason_code"] == result["snapshot_violations"][0]
    assert result["snapshot_violations"] == expected_violations
    assert result["missing_or_invalid_fields"] == (
        "run_id",
        "config_snapshot_id",
        "config_name",
        "config_mode",
        "config_source_mode",
        "runtime_profile_snapshot_ref",
        "publish_mode",
        "notification_mode",
        "eval_mode",
        "adapter_configuration_declared",
        "required_credentials_presence_markers",
        "credential_value_access_enabled",
        "adapter_capability_markers",
        "noop_policy_markers",
        "disabled_external_adapters_declared",
        "environment_safety_marker",
        "redaction_status",
        "created_at",
        "timestamp_policy",
        "source_of_truth",
    )


def test_bool_wrapper_matches_explanation():
    cases = (
        _valid_values(),
        {
            **_valid_values(),
            "run_id": "",
        },
        {
            **_valid_values(),
            "config_mode": "real",
        },
        {
            **_valid_values(),
            "credential_value_access_enabled": True,
        },
    )

    for values in cases:
        explanation = builder.explain_config_snapshot_build(**values)
        assert (
            builder.is_config_snapshot_buildable(**values)
            is explanation["buildable"]
        )


def test_reason_catalog_contains_only_executable_reason_codes():
    assert builder.CONFIG_SNAPSHOT_BUILD_REASON_CODES == (
        "RUN_ID_MISSING",
        "CONFIG_SNAPSHOT_ID_MISSING",
        "CONFIG_NAME_MISSING",
        "CONFIG_MODE_MISSING",
        "CONFIG_MODE_NOT_MANUAL_LOCAL_NOOP",
        "CONFIG_SOURCE_MODE_MISSING",
        "CONFIG_SOURCE_MODE_NOT_CALLER_SUPPLIED",
        "RUNTIME_PROFILE_SNAPSHOT_REF_MISSING",
        "PUBLISH_MODE_MISSING",
        "PUBLISH_MODE_NOT_NOOP",
        "NOTIFICATION_MODE_MISSING",
        "NOTIFICATION_MODE_NOT_NOOP",
        "EVAL_MODE_MISSING",
        "ADAPTER_CONFIGURATION_NOT_DECLARED",
        "REQUIRED_CREDENTIALS_PRESENCE_MARKERS_MISSING",
        "CREDENTIAL_VALUE_ACCESS_ENABLED_TRUE",
        "ADAPTER_CAPABILITY_MARKERS_MISSING",
        "NOOP_POLICY_MARKERS_MISSING",
        "DISABLED_EXTERNAL_ADAPTERS_NOT_DECLARED",
        "ENVIRONMENT_SAFETY_MARKER_MISSING",
        "REDACTION_STATUS_MISSING",
        "CREATED_AT_MISSING",
        "TIMESTAMP_POLICY_MISSING",
        "SOURCE_OF_TRUTH_MISSING",
        "CONFIG_SNAPSHOT_BUILDABLE",
    )
    assert set(FORBIDDEN_PSEUDO_REASON_CODES).isdisjoint(
        builder.CONFIG_SNAPSHOT_BUILD_REASON_CODES
    )


def test_states_constants_are_not_mutated():
    state_invariants_before = states.STATE_INVARIANTS

    _explain()
    _explain(run_id="", publish_mode="real")
    builder.is_config_snapshot_buildable(**_valid_values())

    assert states.STATE_INVARIANTS == state_invariants_before


def test_module_namespace_does_not_import_forbidden_modules_or_io_libraries():
    assert set(FORBIDDEN_MODULE_NAMES).isdisjoint(builder.__dict__)
    assert "states" in builder.__dict__


def test_invariant_refs_capture_config_snapshot_boundaries():
    result = _explain()
    required_invariants = {
        "config_snapshot_builder_only",
        "builder_not_config_reader",
        "builder_not_credential_checker",
        "builder_not_environment_reader",
        "builder_not_adapter_preflight_runner",
        "builder_not_adapter_executor",
        "builder_not_runtime_runner",
        "builder_not_scheduler",
        "builder_not_driver_invoker",
        "builder_not_gate_execution",
        "builder_not_transition_mapping",
        "builder_not_transition_execution",
        "builder_not_config_writer",
        "builder_not_runtime_context_writer",
        "builder_not_ledger_writer",
        "buildable_not_config_write",
        "buildable_not_runtime_context_write",
        "buildable_not_runtime_execution",
        "buildable_not_adapter_preflight",
        "buildable_not_adapter_execution",
        "buildable_not_credential_check",
        "buildable_not_environment_read",
        "buildable_not_config_read",
        "buildable_not_gate_execution",
        "buildable_not_transition_execution",
        "buildable_not_public_url_creation",
        "buildable_not_publish",
        "buildable_not_notification",
        "no_config_read",
        "no_environment_or_env_var_read",
        "no_credential_read",
        "no_raw_credentials",
        "no_raw_env_vars",
        "no_raw_config",
        "no_raw_adapter_outputs",
        "no_raw_driver_object",
        "no_public_url_behavior",
        "no_raw_public_url",
        "no_hashlib",
        "no_hash_calculation",
        "no_ledger_write",
        "no_config_write",
        "no_runtime_context_write",
        "no_runtime_context_snapshot_builder_call",
        "no_runtime_profile_snapshot_builder_call",
        "no_adapter_gate_evidence_policy_call",
        "no_adapter_gate_decision_policy_call",
        "no_daily_gate_evidence_policy_call",
        "no_daily_gate_decision_policy_call",
        "no_noop_completion_policy_call",
        "no_gate_decision_mapper_call",
        "no_transition_guard_call",
        "no_artifact_inventory_policy_call",
        "no_gate_decision_envelope_builder_call",
        "no_run_ledger_entry_builder_call",
        "no_artifact_hash_manifest_builder_call",
        "no_publish_ledger_entry_builder_call",
        "no_notification_ledger_entry_builder_call",
        "manual_local_noop_config_mode_only",
        "caller_supplied_config_source_mode_only",
        "noop_publish_mode_only",
        "noop_notification_mode_only",
        "eval_mode_declared_only",
        "adapter_configuration_declared_only",
        "credential_value_access_disabled",
        "disabled_external_adapters_declared",
        "no_quality_pass_no_public_url",
    }

    assert required_invariants <= set(result["invariant_refs"])
    assert set(states.STATE_INVARIANTS) <= set(result["invariant_refs"])
