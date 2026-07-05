"""Focused contract tests for the pure Runtime Profile Snapshot builder."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import runtime_profile_snapshot_builder as builder
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
    "runtime_profile_snapshot_id",
    "runtime_profile_name",
    "runtime_profile_mode",
    "runtime_trigger_mode",
    "runtime_location_mode",
    "publish_mode",
    "notification_mode",
    "eval_mode",
    "scheduler_enabled",
    "external_adapters_enabled",
    "live_llm_enabled",
    "external_api_enabled",
    "public_url_creation_enabled",
    "credential_value_access_enabled",
    "driver_bypass_allowed",
    "runtime_profile_capability_markers",
    "disabled_runtime_capability_markers",
    "noop_policy_markers",
    "driver_boundary_markers",
    "redaction_status",
    "created_at",
    "timestamp_policy",
    "source_of_truth",
    "notes",
)

FORBIDDEN_RESULT_KEYS = {
    "run_state",
    "runtime_profile_snapshot_ref",
    "config_snapshot_ref",
    "runtime_context_ref",
    "public_url",
    "public_url_created",
    "public_url_is_null",
    "raw_public_url",
    "credential_values",
    "raw_credentials",
    "env_vars",
    "raw_env_vars",
    "environment",
    "environment_object",
    "config",
    "raw_config",
    "config_snapshot",
    "config_contents",
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
    "config_path",
    "artifact_path",
    "should_write_runtime_profile",
    "should_run_runtime",
    "should_execute_adapter",
    "should_evaluate_gate",
    "should_transition",
    "should_write_ledger",
    "runtime_executed",
    "scheduler_executed",
    "adapter_preflight_executed",
    "adapter_executed",
    "gate_executed",
    "transition_executed",
    "ledger_written",
    "runtime_profile_written",
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
    _pseudo_reason("RUNTIME", "PROFILE", "WRITE", "FORBIDDEN"),
    _pseudo_reason("CONFIG", "READ", "FORBIDDEN"),
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
        "runtime_profile_snapshot_id": "runtime-profile-snapshot-001",
        "runtime_profile_name": "local-noop",
        "runtime_profile_mode": "manual_local_noop",
        "runtime_trigger_mode": "manual",
        "runtime_location_mode": "local",
        "publish_mode": "noop",
        "notification_mode": "noop",
        "eval_mode": "stub",
        "scheduler_enabled": False,
        "external_adapters_enabled": False,
        "live_llm_enabled": False,
        "external_api_enabled": False,
        "public_url_creation_enabled": False,
        "credential_value_access_enabled": False,
        "driver_bypass_allowed": False,
        "runtime_profile_capability_markers": (
            "manual_local_noop_profile",
        ),
        "disabled_runtime_capability_markers": (
            "scheduler_disabled",
            "external_adapters_disabled",
            "live_llm_disabled",
            "external_api_disabled",
            "public_url_creation_disabled",
            "credential_value_access_disabled",
        ),
        "noop_policy_markers": ("noop_publish", "noop_notification"),
        "driver_boundary_markers": (
            "Codex",
            "Hermes",
            "Claude Code",
            "OpenClaw",
            "FutureAgent",
            "drivers_cannot_bypass_gates",
        ),
        "redaction_status": "pass",
        "created_at": "caller-supplied-created-at",
        "timestamp_policy": "caller_supplied_no_datetime_parsing",
        "source_of_truth": ("p2d-20", "p2d-21"),
        "notes": ("shape-only",),
    }


def _explain(**overrides: object) -> dict[str, object]:
    values = _valid_values()
    values.update(overrides)
    return builder.explain_runtime_profile_snapshot_build(**values)


def test_valid_manual_local_noop_runtime_profile_snapshot_is_buildable():
    result = _explain()

    assert result["buildable"] is True
    assert result["reason_code"] == "RUNTIME_PROFILE_SNAPSHOT_BUILDABLE"
    assert result["snapshot"]["runtime_profile_snapshot_id"] == (
        "runtime-profile-snapshot-001"
    )
    assert result["snapshot"]["runtime_profile_mode"] == "manual_local_noop"
    assert result["snapshot"]["runtime_trigger_mode"] == "manual"
    assert result["snapshot"]["runtime_location_mode"] == "local"
    assert result["snapshot"]["publish_mode"] == "noop"
    assert result["snapshot"]["notification_mode"] == "noop"
    assert result["snapshot"]["eval_mode"] == "stub"
    assert result["snapshot"]["scheduler_enabled"] is False
    assert result["snapshot"]["driver_bypass_allowed"] is False
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
            "runtime_profile_snapshot_id",
            "",
            "RUNTIME_PROFILE_SNAPSHOT_ID_MISSING",
            ("runtime_profile_snapshot_id",),
        ),
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
        (
            "runtime_trigger_mode",
            "",
            "RUNTIME_TRIGGER_MODE_MISSING",
            ("runtime_trigger_mode",),
        ),
        (
            "runtime_location_mode",
            "",
            "RUNTIME_LOCATION_MODE_MISSING",
            ("runtime_location_mode",),
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
            "runtime_profile_capability_markers",
            (),
            "RUNTIME_PROFILE_CAPABILITY_MARKERS_MISSING",
            ("runtime_profile_capability_markers",),
        ),
        (
            "disabled_runtime_capability_markers",
            (),
            "DISABLED_RUNTIME_CAPABILITY_MARKERS_MISSING",
            ("disabled_runtime_capability_markers",),
        ),
        (
            "noop_policy_markers",
            (),
            "NOOP_POLICY_MARKERS_MISSING",
            ("noop_policy_markers",),
        ),
        (
            "driver_boundary_markers",
            (),
            "DRIVER_BOUNDARY_MARKERS_MISSING",
            ("driver_boundary_markers",),
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
            "runtime_profile_snapshot_id",
            "\n",
            "RUNTIME_PROFILE_SNAPSHOT_ID_MISSING",
        ),
        (
            "runtime_profile_name",
            "\t",
            "RUNTIME_PROFILE_NAME_MISSING",
        ),
        (
            "runtime_profile_mode",
            "   ",
            "RUNTIME_PROFILE_MODE_MISSING",
        ),
        (
            "runtime_trigger_mode",
            "\n",
            "RUNTIME_TRIGGER_MODE_MISSING",
        ),
        (
            "runtime_location_mode",
            "\t",
            "RUNTIME_LOCATION_MODE_MISSING",
        ),
        ("publish_mode", "\t", "PUBLISH_MODE_MISSING"),
        ("notification_mode", "   ", "NOTIFICATION_MODE_MISSING"),
        ("eval_mode", "\n", "EVAL_MODE_MISSING"),
        ("redaction_status", "   ", "REDACTION_STATUS_MISSING"),
        ("created_at", "\n", "CREATED_AT_MISSING"),
        ("timestamp_policy", "   ", "TIMESTAMP_POLICY_MISSING"),
    )

    for field_name, value, reason_code in cases:
        result = _explain(**{field_name: value})

        assert result["buildable"] is False
        assert result["reason_code"] == reason_code


def test_runtime_profile_mode_must_be_manual_local_noop():
    for runtime_profile_mode in ("local", "manual", "noop", "NOOP"):
        result = _explain(runtime_profile_mode=runtime_profile_mode)

        assert result["buildable"] is False
        assert (
            result["reason_code"]
            == "RUNTIME_PROFILE_MODE_NOT_MANUAL_LOCAL_NOOP"
        )
        assert result["missing_or_invalid_fields"] == (
            "runtime_profile_mode",
        )


def test_runtime_trigger_and_location_modes_are_exact():
    trigger_result = _explain(runtime_trigger_mode="scheduled")
    location_result = _explain(runtime_location_mode="remote")

    assert trigger_result["buildable"] is False
    assert trigger_result["reason_code"] == "RUNTIME_TRIGGER_MODE_NOT_MANUAL"
    assert trigger_result["missing_or_invalid_fields"] == (
        "runtime_trigger_mode",
    )
    assert location_result["buildable"] is False
    assert (
        location_result["reason_code"] == "RUNTIME_LOCATION_MODE_NOT_LOCAL"
    )
    assert location_result["missing_or_invalid_fields"] == (
        "runtime_location_mode",
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


def test_disabled_runtime_capability_flags_must_remain_false():
    cases = (
        ("scheduler_enabled", True, "SCHEDULER_ENABLED_TRUE"),
        (
            "external_adapters_enabled",
            True,
            "EXTERNAL_ADAPTERS_ENABLED_TRUE",
        ),
        ("live_llm_enabled", True, "LIVE_LLM_ENABLED_TRUE"),
        ("external_api_enabled", True, "EXTERNAL_API_ENABLED_TRUE"),
        (
            "public_url_creation_enabled",
            True,
            "PUBLIC_URL_CREATION_ENABLED_TRUE",
        ),
        (
            "credential_value_access_enabled",
            True,
            "CREDENTIAL_VALUE_ACCESS_ENABLED_TRUE",
        ),
        ("driver_bypass_allowed", True, "DRIVER_BYPASS_ALLOWED_TRUE"),
    )

    for field_name, value, reason_code in cases:
        result = _explain(**{field_name: value})

        assert result["buildable"] is False
        assert result["reason_code"] == reason_code
        assert result["missing_or_invalid_fields"] == (field_name,)


def test_driver_boundary_markers_accept_ordinary_opaque_strings():
    for driver_marker in (
        "Codex",
        "Hermes",
        "Claude Code",
        "OpenClaw",
        "FutureAgent",
    ):
        result = _explain(driver_boundary_markers=(driver_marker,))

        assert result["buildable"] is True
        assert result["snapshot"]["driver_boundary_markers"] == (
            driver_marker,
        )


def test_no_run_state_refs_public_url_or_driver_identity_fields_exist():
    result = _explain()

    for field_name in (
        "run_state",
        "runtime_profile_snapshot_ref",
        "config_snapshot_ref",
        "runtime_context_ref",
        "public_url",
        "public_url_created",
        "public_url_is_null",
        "driver_name",
        "driver_request_ref",
    ):
        assert field_name not in result
        assert field_name not in result["snapshot"]


def test_result_does_not_include_raw_or_execution_fields():
    result = _explain()
    blocked = _explain(run_id="")

    assert FORBIDDEN_RESULT_KEYS.isdisjoint(result)
    assert FORBIDDEN_RESULT_KEYS.isdisjoint(result["snapshot"])
    assert FORBIDDEN_RESULT_KEYS.isdisjoint(blocked)
    assert FORBIDDEN_RESULT_KEYS.isdisjoint(blocked["snapshot"])
    assert "https://" not in repr(result)
    assert "secret" not in repr(result).lower()


def test_reason_priority_and_all_violations_are_collected():
    result = _explain(
        run_id="",
        runtime_profile_snapshot_id="",
        runtime_profile_name="",
        runtime_profile_mode="real",
        runtime_trigger_mode="scheduled",
        runtime_location_mode="remote",
        publish_mode="real",
        notification_mode="real",
        eval_mode="",
        scheduler_enabled=True,
        external_adapters_enabled=True,
        live_llm_enabled=True,
        external_api_enabled=True,
        public_url_creation_enabled=True,
        credential_value_access_enabled=True,
        driver_bypass_allowed=True,
        runtime_profile_capability_markers=(),
        disabled_runtime_capability_markers=(),
        noop_policy_markers=(),
        driver_boundary_markers=(),
        redaction_status="",
        created_at="",
        timestamp_policy="",
        source_of_truth=(),
    )

    expected_violations = (
        "RUN_ID_MISSING",
        "RUNTIME_PROFILE_SNAPSHOT_ID_MISSING",
        "RUNTIME_PROFILE_NAME_MISSING",
        "RUNTIME_PROFILE_MODE_NOT_MANUAL_LOCAL_NOOP",
        "RUNTIME_TRIGGER_MODE_NOT_MANUAL",
        "RUNTIME_LOCATION_MODE_NOT_LOCAL",
        "PUBLISH_MODE_NOT_NOOP",
        "NOTIFICATION_MODE_NOT_NOOP",
        "EVAL_MODE_MISSING",
        "SCHEDULER_ENABLED_TRUE",
        "EXTERNAL_ADAPTERS_ENABLED_TRUE",
        "LIVE_LLM_ENABLED_TRUE",
        "EXTERNAL_API_ENABLED_TRUE",
        "PUBLIC_URL_CREATION_ENABLED_TRUE",
        "CREDENTIAL_VALUE_ACCESS_ENABLED_TRUE",
        "DRIVER_BYPASS_ALLOWED_TRUE",
        "RUNTIME_PROFILE_CAPABILITY_MARKERS_MISSING",
        "DISABLED_RUNTIME_CAPABILITY_MARKERS_MISSING",
        "NOOP_POLICY_MARKERS_MISSING",
        "DRIVER_BOUNDARY_MARKERS_MISSING",
        "REDACTION_STATUS_MISSING",
        "CREATED_AT_MISSING",
        "TIMESTAMP_POLICY_MISSING",
        "SOURCE_OF_TRUTH_MISSING",
    )

    assert result["buildable"] is False
    assert result["reason_code"] == expected_violations[0]
    assert result["snapshot_violations"] == expected_violations
    assert result["missing_or_invalid_fields"] == (
        "run_id",
        "runtime_profile_snapshot_id",
        "runtime_profile_name",
        "runtime_profile_mode",
        "runtime_trigger_mode",
        "runtime_location_mode",
        "publish_mode",
        "notification_mode",
        "eval_mode",
        "scheduler_enabled",
        "external_adapters_enabled",
        "live_llm_enabled",
        "external_api_enabled",
        "public_url_creation_enabled",
        "credential_value_access_enabled",
        "driver_bypass_allowed",
        "runtime_profile_capability_markers",
        "disabled_runtime_capability_markers",
        "noop_policy_markers",
        "driver_boundary_markers",
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
            "runtime_profile_mode": "real",
        },
        {
            **_valid_values(),
            "scheduler_enabled": True,
        },
    )

    for values in cases:
        explanation = builder.explain_runtime_profile_snapshot_build(**values)
        assert (
            builder.is_runtime_profile_snapshot_buildable(**values)
            is explanation["buildable"]
        )


def test_reason_catalog_contains_only_executable_reason_codes():
    assert builder.RUNTIME_PROFILE_SNAPSHOT_BUILD_REASON_CODES == (
        "RUN_ID_MISSING",
        "RUNTIME_PROFILE_SNAPSHOT_ID_MISSING",
        "RUNTIME_PROFILE_NAME_MISSING",
        "RUNTIME_PROFILE_MODE_MISSING",
        "RUNTIME_PROFILE_MODE_NOT_MANUAL_LOCAL_NOOP",
        "RUNTIME_TRIGGER_MODE_MISSING",
        "RUNTIME_TRIGGER_MODE_NOT_MANUAL",
        "RUNTIME_LOCATION_MODE_MISSING",
        "RUNTIME_LOCATION_MODE_NOT_LOCAL",
        "PUBLISH_MODE_MISSING",
        "PUBLISH_MODE_NOT_NOOP",
        "NOTIFICATION_MODE_MISSING",
        "NOTIFICATION_MODE_NOT_NOOP",
        "EVAL_MODE_MISSING",
        "SCHEDULER_ENABLED_TRUE",
        "EXTERNAL_ADAPTERS_ENABLED_TRUE",
        "LIVE_LLM_ENABLED_TRUE",
        "EXTERNAL_API_ENABLED_TRUE",
        "PUBLIC_URL_CREATION_ENABLED_TRUE",
        "CREDENTIAL_VALUE_ACCESS_ENABLED_TRUE",
        "DRIVER_BYPASS_ALLOWED_TRUE",
        "RUNTIME_PROFILE_CAPABILITY_MARKERS_MISSING",
        "DISABLED_RUNTIME_CAPABILITY_MARKERS_MISSING",
        "NOOP_POLICY_MARKERS_MISSING",
        "DRIVER_BOUNDARY_MARKERS_MISSING",
        "REDACTION_STATUS_MISSING",
        "CREATED_AT_MISSING",
        "TIMESTAMP_POLICY_MISSING",
        "SOURCE_OF_TRUTH_MISSING",
        "RUNTIME_PROFILE_SNAPSHOT_BUILDABLE",
    )
    assert set(FORBIDDEN_PSEUDO_REASON_CODES).isdisjoint(
        builder.RUNTIME_PROFILE_SNAPSHOT_BUILD_REASON_CODES
    )


def test_states_constants_are_not_mutated():
    state_invariants_before = states.STATE_INVARIANTS

    _explain()
    _explain(run_id="", publish_mode="real")
    builder.is_runtime_profile_snapshot_buildable(**_valid_values())

    assert states.STATE_INVARIANTS == state_invariants_before


def test_module_namespace_does_not_import_forbidden_modules_or_io_libraries():
    assert set(FORBIDDEN_MODULE_NAMES).isdisjoint(builder.__dict__)
    assert "states" in builder.__dict__


def test_invariant_refs_capture_runtime_profile_snapshot_boundaries():
    result = _explain()
    required_invariants = {
        "runtime_profile_snapshot_builder_only",
        "builder_not_runtime_runner",
        "builder_not_scheduler",
        "builder_not_adapter_preflight_runner",
        "builder_not_adapter_executor",
        "builder_not_driver_invoker",
        "builder_not_live_llm_invoker",
        "builder_not_external_api_client",
        "builder_not_gate_execution",
        "builder_not_transition_mapping",
        "builder_not_transition_execution",
        "builder_not_runtime_profile_writer",
        "builder_not_runtime_context_writer",
        "builder_not_ledger_writer",
        "buildable_not_runtime_profile_write",
        "buildable_not_runtime_context_write",
        "buildable_not_runtime_execution",
        "buildable_not_scheduler_execution",
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
        "no_environment_or_env_var_read",
        "no_runtime_profile_or_runtime_context_read",
        "no_config_read",
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
        "no_runtime_profile_write",
        "no_runtime_context_write",
        "no_runtime_context_snapshot_builder_call",
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
        "manual_local_noop_runtime_profile_mode_only",
        "manual_runtime_trigger_mode_only",
        "local_runtime_location_mode_only",
        "noop_publish_mode_only",
        "noop_notification_mode_only",
        "eval_mode_declared_only",
        "scheduler_disabled",
        "external_adapters_disabled",
        "live_llm_disabled",
        "external_api_disabled",
        "public_url_creation_disabled",
        "credential_value_access_disabled",
        "driver_bypass_disallowed",
        "driver_boundary_markers_are_opaque",
        "drivers_cannot_bypass_gates",
        "no_quality_pass_no_public_url",
    }

    assert required_invariants <= set(result["invariant_refs"])
    assert set(states.STATE_INVARIANTS) <= set(result["invariant_refs"])
