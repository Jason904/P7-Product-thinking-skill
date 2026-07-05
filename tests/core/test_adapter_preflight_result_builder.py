"""Focused contract tests for the pure Adapter Preflight Result builder."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import adapter_preflight_result_builder as builder
from ai_daily_publishing_system.core import states


REQUIRED_RESULT_FIELDS = (
    "buildable",
    "reason_code",
    "reason",
    "source",
    "preflight_result",
    "preflight_result_violations",
    "missing_or_invalid_fields",
    "invariant_refs",
)

REQUIRED_PREFLIGHT_RESULT_FIELDS = (
    "run_id",
    "adapter_preflight_result_id",
    "runtime_context_ref",
    "runtime_profile_snapshot_ref",
    "config_snapshot_ref",
    "adapter_name",
    "adapter_mode",
    "adapter_configuration_declared",
    "required_credentials_presence_markers",
    "credential_values_present",
    "credential_value_accessed",
    "redaction_status",
    "publish_mode",
    "notification_mode",
    "eval_mode",
    "adapter_capability_markers",
    "noop_policy_markers",
    "disabled_external_adapters_declared",
    "environment_safety_marker",
    "preflight_outcome",
    "external_adapter_called",
    "live_llm_called",
    "external_api_called",
    "created_at",
    "timestamp_policy",
    "source_of_truth",
    "notes",
)

FORBIDDEN_RESULT_KEYS = {
    "run_state",
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
    "raw_adapter_outputs",
    "adapter_outputs",
    "adapter_preflight_output",
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
    "config_snapshot_path",
    "artifact_contents",
    "artifact_hash_manifest_content",
    "review_content",
    "ledger_content",
    "ledger_path",
    "artifact_path",
    "should_write_adapter_preflight_result",
    "should_run_adapter_preflight",
    "should_execute_adapter",
    "should_evaluate_gate",
    "should_transition",
    "should_write_ledger",
    "adapter_preflight_result_written",
    "config_read",
    "config_written",
    "credential_read",
    "environment_read",
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
    _name("config", "snapshot", "builder"),
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
    _pseudo_reason("ENV", "READ", "FORBIDDEN"),
    _pseudo_reason("CONFIG", "READ", "FORBIDDEN"),
    _pseudo_reason("CREDENTIAL", "READ", "FORBIDDEN"),
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
        "adapter_preflight_result_id": "adapter-preflight-result-001",
        "runtime_context_ref": "runtime-context-001",
        "runtime_profile_snapshot_ref": "runtime-profile-snapshot-001",
        "config_snapshot_ref": "config-snapshot-001",
        "adapter_name": "local-noop-adapter",
        "adapter_mode": "noop",
        "adapter_configuration_declared": True,
        "required_credentials_presence_markers": (
            "credentials_not_required_for_noop",
        ),
        "credential_values_present": False,
        "credential_value_accessed": False,
        "redaction_status": "pass",
        "publish_mode": "noop",
        "notification_mode": "noop",
        "eval_mode": "stub",
        "adapter_capability_markers": ("noop_adapter_declared",),
        "noop_policy_markers": ("noop_publish", "noop_notification"),
        "disabled_external_adapters_declared": True,
        "environment_safety_marker": "manual_local_noop_environment",
        "preflight_outcome": "NOOP_PREFLIGHT_DECLARED",
        "external_adapter_called": False,
        "live_llm_called": False,
        "external_api_called": False,
        "created_at": "caller-supplied-created-at",
        "timestamp_policy": "caller_supplied_no_datetime_parsing",
        "source_of_truth": ("p2d-22", "p2d-23"),
        "notes": ("shape-only",),
    }


def _explain(**overrides: object) -> dict[str, object]:
    values = _valid_values()
    values.update(overrides)
    return builder.explain_adapter_preflight_result_build(**values)


def test_valid_noop_preflight_result_is_buildable():
    result = _explain()

    assert result["buildable"] is True
    assert result["reason_code"] == "ADAPTER_PREFLIGHT_RESULT_BUILDABLE"
    assert result["source"] == (
        "adapter_preflight_result_builder."
        "explain_adapter_preflight_result_build"
    )
    assert result["preflight_result"]["adapter_mode"] == "noop"
    assert result["preflight_result"]["preflight_outcome"] == (
        "NOOP_PREFLIGHT_DECLARED"
    )
    assert result["preflight_result"]["credential_values_present"] is False
    assert result["preflight_result"]["credential_value_accessed"] is False
    assert result["preflight_result"]["external_adapter_called"] is False
    assert result["preflight_result"]["live_llm_called"] is False
    assert result["preflight_result"]["external_api_called"] is False
    assert result["preflight_result_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()


def test_public_api_is_keyword_only():
    values = tuple(_valid_values().values())

    try:
        builder.explain_adapter_preflight_result_build(*values)
    except TypeError as exc:
        assert "positional" in str(exc)
    else:
        assert False

    try:
        builder.is_adapter_preflight_result_buildable(*values)
    except TypeError as exc:
        assert "positional" in str(exc)
    else:
        assert False


def test_result_and_preflight_result_shapes_are_exact():
    result = _explain()

    assert tuple(result.keys()) == REQUIRED_RESULT_FIELDS
    assert set(result) == set(REQUIRED_RESULT_FIELDS)
    assert (
        tuple(result["preflight_result"].keys())
        == REQUIRED_PREFLIGHT_RESULT_FIELDS
    )
    assert set(result["preflight_result"]) == set(
        REQUIRED_PREFLIGHT_RESULT_FIELDS
    )


def test_missing_required_fields_block_with_dedicated_reasons():
    cases = (
        ("run_id", "", "RUN_ID_MISSING", ("run_id",)),
        (
            "adapter_preflight_result_id",
            "",
            "ADAPTER_PREFLIGHT_RESULT_ID_MISSING",
            ("adapter_preflight_result_id",),
        ),
        (
            "runtime_context_ref",
            "",
            "RUNTIME_CONTEXT_REF_MISSING",
            ("runtime_context_ref",),
        ),
        (
            "runtime_profile_snapshot_ref",
            "",
            "RUNTIME_PROFILE_SNAPSHOT_REF_MISSING",
            ("runtime_profile_snapshot_ref",),
        ),
        (
            "config_snapshot_ref",
            "",
            "CONFIG_SNAPSHOT_REF_MISSING",
            ("config_snapshot_ref",),
        ),
        ("adapter_name", "", "ADAPTER_NAME_MISSING", ("adapter_name",)),
        ("adapter_mode", "", "ADAPTER_MODE_MISSING", ("adapter_mode",)),
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
            "credential_values_present",
            True,
            "CREDENTIAL_VALUES_PRESENT_TRUE",
            ("credential_values_present",),
        ),
        (
            "credential_value_accessed",
            True,
            "CREDENTIAL_VALUE_ACCESSED_TRUE",
            ("credential_value_accessed",),
        ),
        ("redaction_status", "", "REDACTION_STATUS_MISSING", (
            "redaction_status",
        )),
        ("publish_mode", "", "PUBLISH_MODE_MISSING", ("publish_mode",)),
        (
            "notification_mode",
            "",
            "NOTIFICATION_MODE_MISSING",
            ("notification_mode",),
        ),
        ("eval_mode", "", "EVAL_MODE_MISSING", ("eval_mode",)),
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
            "preflight_outcome",
            "",
            "PREFLIGHT_OUTCOME_MISSING",
            ("preflight_outcome",),
        ),
        (
            "external_adapter_called",
            True,
            "EXTERNAL_ADAPTER_CALLED_TRUE",
            ("external_adapter_called",),
        ),
        (
            "live_llm_called",
            True,
            "LIVE_LLM_CALLED_TRUE",
            ("live_llm_called",),
        ),
        (
            "external_api_called",
            True,
            "EXTERNAL_API_CALLED_TRUE",
            ("external_api_called",),
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
        assert result["preflight_result_violations"] == (reason_code,)
        assert result["missing_or_invalid_fields"] == invalid_fields


def test_whitespace_required_strings_are_missing():
    cases = (
        ("run_id", "   ", "RUN_ID_MISSING"),
        (
            "adapter_preflight_result_id",
            "\n",
            "ADAPTER_PREFLIGHT_RESULT_ID_MISSING",
        ),
        ("runtime_context_ref", "\t", "RUNTIME_CONTEXT_REF_MISSING"),
        (
            "runtime_profile_snapshot_ref",
            "   ",
            "RUNTIME_PROFILE_SNAPSHOT_REF_MISSING",
        ),
        ("config_snapshot_ref", "\n", "CONFIG_SNAPSHOT_REF_MISSING"),
        ("adapter_name", "\t", "ADAPTER_NAME_MISSING"),
        ("adapter_mode", "   ", "ADAPTER_MODE_MISSING"),
        ("redaction_status", "   ", "REDACTION_STATUS_MISSING"),
        ("publish_mode", "\t", "PUBLISH_MODE_MISSING"),
        ("notification_mode", "   ", "NOTIFICATION_MODE_MISSING"),
        ("eval_mode", "\n", "EVAL_MODE_MISSING"),
        (
            "environment_safety_marker",
            "   ",
            "ENVIRONMENT_SAFETY_MARKER_MISSING",
        ),
        ("preflight_outcome", "\n", "PREFLIGHT_OUTCOME_MISSING"),
        ("created_at", "\n", "CREATED_AT_MISSING"),
        ("timestamp_policy", "   ", "TIMESTAMP_POLICY_MISSING"),
    )

    for field_name, value, reason_code in cases:
        result = _explain(**{field_name: value})

        assert result["buildable"] is False
        assert result["reason_code"] == reason_code


def test_adapter_mode_must_be_noop():
    for adapter_mode in ("real", "manual", "NOOP", "noop "):
        result = _explain(adapter_mode=adapter_mode)

        assert result["buildable"] is False
        assert result["reason_code"] == "ADAPTER_MODE_NOT_NOOP"
        assert result["missing_or_invalid_fields"] == ("adapter_mode",)


def test_preflight_outcome_must_be_noop_preflight_declared():
    for preflight_outcome in ("PASS", "noop", "NOOP", "NOOP_PREFLIGHT"):
        result = _explain(preflight_outcome=preflight_outcome)

        assert result["buildable"] is False
        assert result["reason_code"] == "PREFLIGHT_OUTCOME_NOT_NOOP_DECLARED"
        assert result["missing_or_invalid_fields"] == ("preflight_outcome",)


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
        assert result["preflight_result"]["eval_mode"] == eval_mode

    blocked = _explain(eval_mode="")
    assert blocked["buildable"] is False
    assert blocked["reason_code"] == "EVAL_MODE_MISSING"
    assert "EVAL_MODE_NOT_" not in repr(builder.__dict__)


def test_noop_preflight_marker_booleans_are_required():
    cases = (
        (
            "adapter_configuration_declared",
            False,
            "ADAPTER_CONFIGURATION_NOT_DECLARED",
        ),
        (
            "credential_values_present",
            True,
            "CREDENTIAL_VALUES_PRESENT_TRUE",
        ),
        (
            "credential_value_accessed",
            True,
            "CREDENTIAL_VALUE_ACCESSED_TRUE",
        ),
        (
            "disabled_external_adapters_declared",
            False,
            "DISABLED_EXTERNAL_ADAPTERS_NOT_DECLARED",
        ),
        (
            "external_adapter_called",
            True,
            "EXTERNAL_ADAPTER_CALLED_TRUE",
        ),
        ("live_llm_called", True, "LIVE_LLM_CALLED_TRUE"),
        ("external_api_called", True, "EXTERNAL_API_CALLED_TRUE"),
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


def test_environment_safety_marker_is_required():
    result = _explain(environment_safety_marker="")

    assert result["buildable"] is False
    assert result["reason_code"] == "ENVIRONMENT_SAFETY_MARKER_MISSING"
    assert result["missing_or_invalid_fields"] == (
        "environment_safety_marker",
    )


def test_no_forbidden_reference_or_public_url_fields_exist():
    result = _explain()

    for field_name in (
        "run_state",
        "adapter_preflight_result_ref",
        "public_url",
        "public_url_created",
        "public_url_is_null",
        "raw_public_url",
    ):
        assert field_name not in result
        assert field_name not in result["preflight_result"]


def test_result_does_not_include_raw_credentials_or_execution_fields():
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
    assert FORBIDDEN_RESULT_KEYS.isdisjoint(result["preflight_result"])
    assert FORBIDDEN_RESULT_KEYS.isdisjoint(blocked)
    assert FORBIDDEN_RESULT_KEYS.isdisjoint(blocked["preflight_result"])
    assert allowed_raw_boundary_invariants <= set(result["invariant_refs"])
    assert "https://" not in result_contract_repr
    assert "http://" not in result_contract_repr
    assert "secret" not in result_contract_repr.lower()
    assert "token" not in result_contract_repr.lower()
    assert "raw_config" not in result_contract_repr
    assert "raw_credentials" not in result_contract_repr
    assert "credential_values':" not in result_contract_repr
    assert "raw_env" not in result_contract_repr
    assert "raw_adapter_outputs" not in result_contract_repr
    assert "driver_object" not in result_contract_repr


def test_no_runtime_config_adapter_artifact_or_ledger_path_leakage():
    result = _explain()
    result_without_invariants = {
        key: value for key, value in result.items() if key != "invariant_refs"
    }

    forbidden_fragments = (
        "runtime_context_path",
        "runtime_profile_path",
        "config_path",
        "config_snapshot_path",
        "config_contents",
        "runtime_profile_contents",
        "runtime_context_contents",
        "adapter_preflight_result_ref",
        "adapter_preflight_result_path",
        "adapter_outputs",
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
        adapter_preflight_result_id="",
        runtime_context_ref="",
        runtime_profile_snapshot_ref="",
        config_snapshot_ref="",
        adapter_name="",
        adapter_mode="real",
        adapter_configuration_declared=False,
        required_credentials_presence_markers=(),
        credential_values_present=True,
        credential_value_accessed=True,
        redaction_status="",
        publish_mode="real",
        notification_mode="real",
        eval_mode="",
        adapter_capability_markers=(),
        noop_policy_markers=(),
        disabled_external_adapters_declared=False,
        environment_safety_marker="",
        preflight_outcome="PASS",
        external_adapter_called=True,
        live_llm_called=True,
        external_api_called=True,
        created_at="",
        timestamp_policy="",
        source_of_truth=(),
    )

    expected_violations = (
        "RUN_ID_MISSING",
        "ADAPTER_PREFLIGHT_RESULT_ID_MISSING",
        "RUNTIME_CONTEXT_REF_MISSING",
        "RUNTIME_PROFILE_SNAPSHOT_REF_MISSING",
        "CONFIG_SNAPSHOT_REF_MISSING",
        "ADAPTER_NAME_MISSING",
        "ADAPTER_MODE_NOT_NOOP",
        "ADAPTER_CONFIGURATION_NOT_DECLARED",
        "REQUIRED_CREDENTIALS_PRESENCE_MARKERS_MISSING",
        "CREDENTIAL_VALUES_PRESENT_TRUE",
        "CREDENTIAL_VALUE_ACCESSED_TRUE",
        "REDACTION_STATUS_MISSING",
        "PUBLISH_MODE_NOT_NOOP",
        "NOTIFICATION_MODE_NOT_NOOP",
        "EVAL_MODE_MISSING",
        "ADAPTER_CAPABILITY_MARKERS_MISSING",
        "NOOP_POLICY_MARKERS_MISSING",
        "DISABLED_EXTERNAL_ADAPTERS_NOT_DECLARED",
        "ENVIRONMENT_SAFETY_MARKER_MISSING",
        "PREFLIGHT_OUTCOME_NOT_NOOP_DECLARED",
        "EXTERNAL_ADAPTER_CALLED_TRUE",
        "LIVE_LLM_CALLED_TRUE",
        "EXTERNAL_API_CALLED_TRUE",
        "CREATED_AT_MISSING",
        "TIMESTAMP_POLICY_MISSING",
        "SOURCE_OF_TRUTH_MISSING",
    )

    assert result["buildable"] is False
    assert result["reason_code"] == expected_violations[0]
    assert result["reason_code"] == result["preflight_result_violations"][0]
    assert result["preflight_result_violations"] == expected_violations
    assert result["missing_or_invalid_fields"] == (
        "run_id",
        "adapter_preflight_result_id",
        "runtime_context_ref",
        "runtime_profile_snapshot_ref",
        "config_snapshot_ref",
        "adapter_name",
        "adapter_mode",
        "adapter_configuration_declared",
        "required_credentials_presence_markers",
        "credential_values_present",
        "credential_value_accessed",
        "redaction_status",
        "publish_mode",
        "notification_mode",
        "eval_mode",
        "adapter_capability_markers",
        "noop_policy_markers",
        "disabled_external_adapters_declared",
        "environment_safety_marker",
        "preflight_outcome",
        "external_adapter_called",
        "live_llm_called",
        "external_api_called",
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
            "adapter_mode": "real",
        },
        {
            **_valid_values(),
            "external_adapter_called": True,
        },
    )

    for values in cases:
        explanation = builder.explain_adapter_preflight_result_build(**values)
        assert (
            builder.is_adapter_preflight_result_buildable(**values)
            is explanation["buildable"]
        )


def test_reason_catalog_contains_only_executable_reason_codes():
    assert builder.ADAPTER_PREFLIGHT_RESULT_BUILD_REASON_CODES == (
        "RUN_ID_MISSING",
        "ADAPTER_PREFLIGHT_RESULT_ID_MISSING",
        "RUNTIME_CONTEXT_REF_MISSING",
        "RUNTIME_PROFILE_SNAPSHOT_REF_MISSING",
        "CONFIG_SNAPSHOT_REF_MISSING",
        "ADAPTER_NAME_MISSING",
        "ADAPTER_MODE_MISSING",
        "ADAPTER_MODE_NOT_NOOP",
        "ADAPTER_CONFIGURATION_NOT_DECLARED",
        "REQUIRED_CREDENTIALS_PRESENCE_MARKERS_MISSING",
        "CREDENTIAL_VALUES_PRESENT_TRUE",
        "CREDENTIAL_VALUE_ACCESSED_TRUE",
        "REDACTION_STATUS_MISSING",
        "PUBLISH_MODE_MISSING",
        "PUBLISH_MODE_NOT_NOOP",
        "NOTIFICATION_MODE_MISSING",
        "NOTIFICATION_MODE_NOT_NOOP",
        "EVAL_MODE_MISSING",
        "ADAPTER_CAPABILITY_MARKERS_MISSING",
        "NOOP_POLICY_MARKERS_MISSING",
        "DISABLED_EXTERNAL_ADAPTERS_NOT_DECLARED",
        "ENVIRONMENT_SAFETY_MARKER_MISSING",
        "PREFLIGHT_OUTCOME_MISSING",
        "PREFLIGHT_OUTCOME_NOT_NOOP_DECLARED",
        "EXTERNAL_ADAPTER_CALLED_TRUE",
        "LIVE_LLM_CALLED_TRUE",
        "EXTERNAL_API_CALLED_TRUE",
        "CREATED_AT_MISSING",
        "TIMESTAMP_POLICY_MISSING",
        "SOURCE_OF_TRUTH_MISSING",
        "ADAPTER_PREFLIGHT_RESULT_BUILDABLE",
    )
    assert set(FORBIDDEN_PSEUDO_REASON_CODES).isdisjoint(
        builder.ADAPTER_PREFLIGHT_RESULT_BUILD_REASON_CODES
    )


def test_states_constants_are_not_mutated():
    state_invariants_before = states.STATE_INVARIANTS

    _explain()
    _explain(run_id="", publish_mode="real")
    builder.is_adapter_preflight_result_buildable(**_valid_values())

    assert states.STATE_INVARIANTS == state_invariants_before


def test_module_namespace_does_not_import_forbidden_modules_or_io_libraries():
    assert set(FORBIDDEN_MODULE_NAMES).isdisjoint(builder.__dict__)
    assert "states" in builder.__dict__


def test_invariant_refs_capture_adapter_preflight_result_boundaries():
    result = _explain()
    required_invariants = {
        "adapter_preflight_result_builder_only",
        "builder_not_adapter_preflight_runner",
        "builder_not_adapter_executor",
        "builder_not_driver_invoker",
        "builder_not_live_llm_invoker",
        "builder_not_external_api_client",
        "builder_not_config_reader",
        "builder_not_credential_checker",
        "builder_not_environment_reader",
        "builder_not_runtime_runner",
        "builder_not_scheduler",
        "builder_not_gate_execution",
        "builder_not_transition_mapping",
        "builder_not_transition_execution",
        "builder_not_adapter_preflight_result_writer",
        "builder_not_runtime_context_writer",
        "builder_not_ledger_writer",
        "buildable_not_adapter_preflight_result_write",
        "buildable_not_runtime_execution",
        "buildable_not_adapter_preflight",
        "buildable_not_adapter_execution",
        "buildable_not_config_read",
        "buildable_not_credential_check",
        "buildable_not_environment_read",
        "buildable_not_gate_execution",
        "buildable_not_transition_execution",
        "buildable_not_public_url_creation",
        "buildable_not_publish",
        "buildable_not_notification",
        "no_file_read",
        "no_file_write",
        "no_file_exists_check",
        "no_file_stat",
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
        "no_adapter_preflight_result_write",
        "no_runtime_context_snapshot_builder_call",
        "no_runtime_profile_snapshot_builder_call",
        "no_config_snapshot_builder_call",
        "no_adapter_gate_evidence_policy_call",
        "no_adapter_gate_decision_policy_call",
        "no_daily_gate_evidence_policy_call",
        "no_daily_gate_decision_policy_call",
        "noop_adapter_mode_only",
        "noop_publish_mode_only",
        "noop_notification_mode_only",
        "eval_mode_declared_only",
        "noop_preflight_outcome_declared_only",
        "adapter_configuration_declared_only",
        "credential_values_absent",
        "credential_value_access_disabled",
        "disabled_external_adapters_declared",
        "external_adapter_call_disabled",
        "live_llm_call_disabled",
        "external_api_call_disabled",
        "no_quality_pass_no_public_url",
    }

    assert required_invariants <= set(result["invariant_refs"])
    assert set(states.STATE_INVARIANTS) <= set(result["invariant_refs"])
