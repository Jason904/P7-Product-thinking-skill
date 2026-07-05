"""Pure Adapter Preflight Result builder for caller-supplied markers."""

from typing import Final

from ai_daily_publishing_system.core import states


ADAPTER_PREFLIGHT_RESULT_BUILDABLE: Final[str] = (
    "ADAPTER_PREFLIGHT_RESULT_BUILDABLE"
)
RUN_ID_MISSING: Final[str] = "RUN_ID_MISSING"
ADAPTER_PREFLIGHT_RESULT_ID_MISSING: Final[str] = (
    "ADAPTER_PREFLIGHT_RESULT_ID_MISSING"
)
RUNTIME_CONTEXT_REF_MISSING: Final[str] = "RUNTIME_CONTEXT_REF_MISSING"
RUNTIME_PROFILE_SNAPSHOT_REF_MISSING: Final[str] = (
    "RUNTIME_PROFILE_SNAPSHOT_REF_MISSING"
)
CONFIG_SNAPSHOT_REF_MISSING: Final[str] = "CONFIG_SNAPSHOT_REF_MISSING"
ADAPTER_NAME_MISSING: Final[str] = "ADAPTER_NAME_MISSING"
ADAPTER_MODE_MISSING: Final[str] = "ADAPTER_MODE_MISSING"
ADAPTER_MODE_NOT_NOOP: Final[str] = "ADAPTER_MODE_NOT_NOOP"
ADAPTER_CONFIGURATION_NOT_DECLARED: Final[str] = (
    "ADAPTER_CONFIGURATION_NOT_DECLARED"
)
REQUIRED_CREDENTIALS_PRESENCE_MARKERS_MISSING: Final[str] = (
    "REQUIRED_CREDENTIALS_PRESENCE_MARKERS_MISSING"
)
CREDENTIAL_VALUES_PRESENT_TRUE: Final[str] = (
    "CREDENTIAL_VALUES_PRESENT_TRUE"
)
CREDENTIAL_VALUE_ACCESSED_TRUE: Final[str] = (
    "CREDENTIAL_VALUE_ACCESSED_TRUE"
)
REDACTION_STATUS_MISSING: Final[str] = "REDACTION_STATUS_MISSING"
PUBLISH_MODE_MISSING: Final[str] = "PUBLISH_MODE_MISSING"
PUBLISH_MODE_NOT_NOOP: Final[str] = "PUBLISH_MODE_NOT_NOOP"
NOTIFICATION_MODE_MISSING: Final[str] = "NOTIFICATION_MODE_MISSING"
NOTIFICATION_MODE_NOT_NOOP: Final[str] = "NOTIFICATION_MODE_NOT_NOOP"
EVAL_MODE_MISSING: Final[str] = "EVAL_MODE_MISSING"
ADAPTER_CAPABILITY_MARKERS_MISSING: Final[str] = (
    "ADAPTER_CAPABILITY_MARKERS_MISSING"
)
NOOP_POLICY_MARKERS_MISSING: Final[str] = "NOOP_POLICY_MARKERS_MISSING"
DISABLED_EXTERNAL_ADAPTERS_NOT_DECLARED: Final[str] = (
    "DISABLED_EXTERNAL_ADAPTERS_NOT_DECLARED"
)
ENVIRONMENT_SAFETY_MARKER_MISSING: Final[str] = (
    "ENVIRONMENT_SAFETY_MARKER_MISSING"
)
PREFLIGHT_OUTCOME_MISSING: Final[str] = "PREFLIGHT_OUTCOME_MISSING"
PREFLIGHT_OUTCOME_NOT_NOOP_DECLARED: Final[str] = (
    "PREFLIGHT_OUTCOME_NOT_NOOP_DECLARED"
)
EXTERNAL_ADAPTER_CALLED_TRUE: Final[str] = (
    "EXTERNAL_ADAPTER_CALLED_TRUE"
)
LIVE_LLM_CALLED_TRUE: Final[str] = "LIVE_LLM_CALLED_TRUE"
EXTERNAL_API_CALLED_TRUE: Final[str] = "EXTERNAL_API_CALLED_TRUE"
CREATED_AT_MISSING: Final[str] = "CREATED_AT_MISSING"
TIMESTAMP_POLICY_MISSING: Final[str] = "TIMESTAMP_POLICY_MISSING"
SOURCE_OF_TRUTH_MISSING: Final[str] = "SOURCE_OF_TRUTH_MISSING"

ADAPTER_PREFLIGHT_RESULT_BUILD_REASON_CODES: Final[tuple[str, ...]] = (
    RUN_ID_MISSING,
    ADAPTER_PREFLIGHT_RESULT_ID_MISSING,
    RUNTIME_CONTEXT_REF_MISSING,
    RUNTIME_PROFILE_SNAPSHOT_REF_MISSING,
    CONFIG_SNAPSHOT_REF_MISSING,
    ADAPTER_NAME_MISSING,
    ADAPTER_MODE_MISSING,
    ADAPTER_MODE_NOT_NOOP,
    ADAPTER_CONFIGURATION_NOT_DECLARED,
    REQUIRED_CREDENTIALS_PRESENCE_MARKERS_MISSING,
    CREDENTIAL_VALUES_PRESENT_TRUE,
    CREDENTIAL_VALUE_ACCESSED_TRUE,
    REDACTION_STATUS_MISSING,
    PUBLISH_MODE_MISSING,
    PUBLISH_MODE_NOT_NOOP,
    NOTIFICATION_MODE_MISSING,
    NOTIFICATION_MODE_NOT_NOOP,
    EVAL_MODE_MISSING,
    ADAPTER_CAPABILITY_MARKERS_MISSING,
    NOOP_POLICY_MARKERS_MISSING,
    DISABLED_EXTERNAL_ADAPTERS_NOT_DECLARED,
    ENVIRONMENT_SAFETY_MARKER_MISSING,
    PREFLIGHT_OUTCOME_MISSING,
    PREFLIGHT_OUTCOME_NOT_NOOP_DECLARED,
    EXTERNAL_ADAPTER_CALLED_TRUE,
    LIVE_LLM_CALLED_TRUE,
    EXTERNAL_API_CALLED_TRUE,
    CREATED_AT_MISSING,
    TIMESTAMP_POLICY_MISSING,
    SOURCE_OF_TRUTH_MISSING,
    ADAPTER_PREFLIGHT_RESULT_BUILDABLE,
)

_SOURCE: Final[str] = (
    "adapter_preflight_result_builder."
    "explain_adapter_preflight_result_build"
)
_NOOP_ADAPTER_MODE: Final[str] = "noop"
_NOOP_PUBLISH_MODE: Final[str] = "noop"
_NOOP_NOTIFICATION_MODE: Final[str] = "noop"
_NOOP_PREFLIGHT_OUTCOME: Final[str] = "NOOP_PREFLIGHT_DECLARED"
_LOCAL_INVARIANTS: Final[tuple[str, ...]] = (
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
)
_INVARIANTS: Final[tuple[str, ...]] = (
    states.STATE_INVARIANTS + _LOCAL_INVARIANTS
)
_REASON_TEXT_ENTRIES: Final[tuple[tuple[str, str], ...]] = (
    (
        RUN_ID_MISSING,
        "A non-empty caller-supplied run_id is required.",
    ),
    (
        ADAPTER_PREFLIGHT_RESULT_ID_MISSING,
        "A non-empty caller-supplied adapter_preflight_result_id is "
        "required.",
    ),
    (
        RUNTIME_CONTEXT_REF_MISSING,
        "A non-empty caller-supplied runtime_context_ref is required; "
        "the builder does not read runtime context files.",
    ),
    (
        RUNTIME_PROFILE_SNAPSHOT_REF_MISSING,
        "A non-empty caller-supplied runtime_profile_snapshot_ref is "
        "required; the builder does not read profile snapshots.",
    ),
    (
        CONFIG_SNAPSHOT_REF_MISSING,
        "A non-empty caller-supplied config_snapshot_ref is required; "
        "the builder does not read config snapshots.",
    ),
    (
        ADAPTER_NAME_MISSING,
        "A non-empty caller-supplied adapter_name is required.",
    ),
    (
        ADAPTER_MODE_MISSING,
        "A non-empty caller-supplied adapter_mode is required.",
    ),
    (
        ADAPTER_MODE_NOT_NOOP,
        "The caller-supplied adapter_mode must be exactly noop.",
    ),
    (
        ADAPTER_CONFIGURATION_NOT_DECLARED,
        "The caller-supplied adapter_configuration_declared marker must "
        "be true.",
    ),
    (
        REQUIRED_CREDENTIALS_PRESENCE_MARKERS_MISSING,
        "At least one caller-supplied credential presence marker is "
        "required; the builder does not read credential values.",
    ),
    (
        CREDENTIAL_VALUES_PRESENT_TRUE,
        "MVP adapter preflight results require credential_values_present "
        "to remain false.",
    ),
    (
        CREDENTIAL_VALUE_ACCESSED_TRUE,
        "MVP adapter preflight results require credential_value_accessed "
        "to remain false.",
    ),
    (
        REDACTION_STATUS_MISSING,
        "A non-empty caller-supplied redaction_status is required.",
    ),
    (
        PUBLISH_MODE_MISSING,
        "A non-empty caller-supplied publish_mode is required.",
    ),
    (
        PUBLISH_MODE_NOT_NOOP,
        "The caller-supplied publish_mode must be exactly noop.",
    ),
    (
        NOTIFICATION_MODE_MISSING,
        "A non-empty caller-supplied notification_mode is required.",
    ),
    (
        NOTIFICATION_MODE_NOT_NOOP,
        "The caller-supplied notification_mode must be exactly noop.",
    ),
    (
        EVAL_MODE_MISSING,
        "A non-empty caller-supplied eval_mode declaration is required; "
        "the builder does not execute evaluation.",
    ),
    (
        ADAPTER_CAPABILITY_MARKERS_MISSING,
        "At least one caller-supplied adapter capability marker is "
        "required; the builder does not probe adapters.",
    ),
    (
        NOOP_POLICY_MARKERS_MISSING,
        "At least one caller-supplied noop policy marker is required.",
    ),
    (
        DISABLED_EXTERNAL_ADAPTERS_NOT_DECLARED,
        "The caller-supplied disabled_external_adapters_declared marker "
        "must be true.",
    ),
    (
        ENVIRONMENT_SAFETY_MARKER_MISSING,
        "A non-empty caller-supplied environment_safety_marker is "
        "required; the builder does not read the environment.",
    ),
    (
        PREFLIGHT_OUTCOME_MISSING,
        "A non-empty caller-supplied preflight_outcome is required.",
    ),
    (
        PREFLIGHT_OUTCOME_NOT_NOOP_DECLARED,
        "The caller-supplied preflight_outcome must be exactly "
        "NOOP_PREFLIGHT_DECLARED.",
    ),
    (
        EXTERNAL_ADAPTER_CALLED_TRUE,
        "MVP adapter preflight results require external_adapter_called "
        "to remain false.",
    ),
    (
        LIVE_LLM_CALLED_TRUE,
        "MVP adapter preflight results require live_llm_called to remain "
        "false.",
    ),
    (
        EXTERNAL_API_CALLED_TRUE,
        "MVP adapter preflight results require external_api_called to "
        "remain false.",
    ),
    (
        CREATED_AT_MISSING,
        "A non-empty caller-supplied created_at value is required.",
    ),
    (
        TIMESTAMP_POLICY_MISSING,
        "A non-empty caller-supplied timestamp_policy is required.",
    ),
    (
        SOURCE_OF_TRUTH_MISSING,
        "At least one caller-supplied source_of_truth reference is "
        "required.",
    ),
    (
        ADAPTER_PREFLIGHT_RESULT_BUILDABLE,
        "The caller-supplied fields can build the Adapter Preflight "
        "Result shape. This does not write adapter-preflight-result.yaml, "
        "write runtime-context.yaml, read files, check file existence, "
        "stat files, calculate hashes, read environment, configuration "
        "or credentials, execute adapter preflight, call adapters, invoke "
        "drivers, call live LLMs or external APIs, execute gates, map or "
        "execute transitions, read artifacts, reviews, hashes or ledgers, "
        "write ledgers, publish, notify, create or return a public URL, "
        "or call existing policy or builder modules.",
    ),
)
_VIOLATION_FIELD_ENTRIES: Final[tuple[tuple[str, tuple[str, ...]], ...]] = (
    (RUN_ID_MISSING, ("run_id",)),
    (
        ADAPTER_PREFLIGHT_RESULT_ID_MISSING,
        ("adapter_preflight_result_id",),
    ),
    (RUNTIME_CONTEXT_REF_MISSING, ("runtime_context_ref",)),
    (
        RUNTIME_PROFILE_SNAPSHOT_REF_MISSING,
        ("runtime_profile_snapshot_ref",),
    ),
    (CONFIG_SNAPSHOT_REF_MISSING, ("config_snapshot_ref",)),
    (ADAPTER_NAME_MISSING, ("adapter_name",)),
    (ADAPTER_MODE_MISSING, ("adapter_mode",)),
    (ADAPTER_MODE_NOT_NOOP, ("adapter_mode",)),
    (
        ADAPTER_CONFIGURATION_NOT_DECLARED,
        ("adapter_configuration_declared",),
    ),
    (
        REQUIRED_CREDENTIALS_PRESENCE_MARKERS_MISSING,
        ("required_credentials_presence_markers",),
    ),
    (CREDENTIAL_VALUES_PRESENT_TRUE, ("credential_values_present",)),
    (CREDENTIAL_VALUE_ACCESSED_TRUE, ("credential_value_accessed",)),
    (REDACTION_STATUS_MISSING, ("redaction_status",)),
    (PUBLISH_MODE_MISSING, ("publish_mode",)),
    (PUBLISH_MODE_NOT_NOOP, ("publish_mode",)),
    (NOTIFICATION_MODE_MISSING, ("notification_mode",)),
    (NOTIFICATION_MODE_NOT_NOOP, ("notification_mode",)),
    (EVAL_MODE_MISSING, ("eval_mode",)),
    (ADAPTER_CAPABILITY_MARKERS_MISSING, ("adapter_capability_markers",)),
    (NOOP_POLICY_MARKERS_MISSING, ("noop_policy_markers",)),
    (
        DISABLED_EXTERNAL_ADAPTERS_NOT_DECLARED,
        ("disabled_external_adapters_declared",),
    ),
    (ENVIRONMENT_SAFETY_MARKER_MISSING, ("environment_safety_marker",)),
    (PREFLIGHT_OUTCOME_MISSING, ("preflight_outcome",)),
    (
        PREFLIGHT_OUTCOME_NOT_NOOP_DECLARED,
        ("preflight_outcome",),
    ),
    (EXTERNAL_ADAPTER_CALLED_TRUE, ("external_adapter_called",)),
    (LIVE_LLM_CALLED_TRUE, ("live_llm_called",)),
    (EXTERNAL_API_CALLED_TRUE, ("external_api_called",)),
    (CREATED_AT_MISSING, ("created_at",)),
    (TIMESTAMP_POLICY_MISSING, ("timestamp_policy",)),
    (SOURCE_OF_TRUTH_MISSING, ("source_of_truth",)),
)


def _reason_text(reason_code: str) -> str:
    for code, text in _REASON_TEXT_ENTRIES:
        if code == reason_code:
            return text
    return "Unknown Adapter Preflight Result build result."


def _ordered_unique(values: tuple[str, ...]) -> tuple[str, ...]:
    ordered_values = ()
    for value in values:
        if value not in ordered_values:
            ordered_values = ordered_values + (value,)
    return ordered_values


def _missing_or_invalid_fields(
    preflight_result_violations: tuple[str, ...],
) -> tuple[str, ...]:
    field_names = ()
    for violation in preflight_result_violations:
        for reason_code, invalid_fields in _VIOLATION_FIELD_ENTRIES:
            if reason_code == violation:
                field_names = field_names + invalid_fields
    return _ordered_unique(field_names)


def _preflight_result(
    *,
    run_id: str,
    adapter_preflight_result_id: str,
    runtime_context_ref: str,
    runtime_profile_snapshot_ref: str,
    config_snapshot_ref: str,
    adapter_name: str,
    adapter_mode: str,
    adapter_configuration_declared: bool,
    required_credentials_presence_markers: tuple[str, ...],
    credential_values_present: bool,
    credential_value_accessed: bool,
    redaction_status: str,
    publish_mode: str,
    notification_mode: str,
    eval_mode: str,
    adapter_capability_markers: tuple[str, ...],
    noop_policy_markers: tuple[str, ...],
    disabled_external_adapters_declared: bool,
    environment_safety_marker: str,
    preflight_outcome: str,
    external_adapter_called: bool,
    live_llm_called: bool,
    external_api_called: bool,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    return {
        "run_id": run_id,
        "adapter_preflight_result_id": adapter_preflight_result_id,
        "runtime_context_ref": runtime_context_ref,
        "runtime_profile_snapshot_ref": runtime_profile_snapshot_ref,
        "config_snapshot_ref": config_snapshot_ref,
        "adapter_name": adapter_name,
        "adapter_mode": adapter_mode,
        "adapter_configuration_declared": adapter_configuration_declared,
        "required_credentials_presence_markers": (
            required_credentials_presence_markers
        ),
        "credential_values_present": credential_values_present,
        "credential_value_accessed": credential_value_accessed,
        "redaction_status": redaction_status,
        "publish_mode": publish_mode,
        "notification_mode": notification_mode,
        "eval_mode": eval_mode,
        "adapter_capability_markers": adapter_capability_markers,
        "noop_policy_markers": noop_policy_markers,
        "disabled_external_adapters_declared": (
            disabled_external_adapters_declared
        ),
        "environment_safety_marker": environment_safety_marker,
        "preflight_outcome": preflight_outcome,
        "external_adapter_called": external_adapter_called,
        "live_llm_called": live_llm_called,
        "external_api_called": external_api_called,
        "created_at": created_at,
        "timestamp_policy": timestamp_policy,
        "source_of_truth": source_of_truth,
        "notes": notes,
    }


def _result(
    *,
    buildable: bool,
    reason_code: str,
    preflight_result: object,
    preflight_result_violations: tuple[str, ...],
    missing_or_invalid_fields: tuple[str, ...],
) -> dict[str, object]:
    return {
        "buildable": buildable,
        "reason_code": reason_code,
        "reason": _reason_text(reason_code),
        "source": _SOURCE,
        "preflight_result": preflight_result,
        "preflight_result_violations": preflight_result_violations,
        "missing_or_invalid_fields": missing_or_invalid_fields,
        "invariant_refs": _INVARIANTS,
    }


def explain_adapter_preflight_result_build(
    *,
    run_id: str,
    adapter_preflight_result_id: str,
    runtime_context_ref: str,
    runtime_profile_snapshot_ref: str,
    config_snapshot_ref: str,
    adapter_name: str,
    adapter_mode: str,
    adapter_configuration_declared: bool,
    required_credentials_presence_markers: tuple[str, ...],
    credential_values_present: bool,
    credential_value_accessed: bool,
    redaction_status: str,
    publish_mode: str,
    notification_mode: str,
    eval_mode: str,
    adapter_capability_markers: tuple[str, ...],
    noop_policy_markers: tuple[str, ...],
    disabled_external_adapters_declared: bool,
    environment_safety_marker: str,
    preflight_outcome: str,
    external_adapter_called: bool,
    live_llm_called: bool,
    external_api_called: bool,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    """Explain whether caller-supplied fields can build a result."""
    preflight_result = _preflight_result(
        run_id=run_id,
        adapter_preflight_result_id=adapter_preflight_result_id,
        runtime_context_ref=runtime_context_ref,
        runtime_profile_snapshot_ref=runtime_profile_snapshot_ref,
        config_snapshot_ref=config_snapshot_ref,
        adapter_name=adapter_name,
        adapter_mode=adapter_mode,
        adapter_configuration_declared=adapter_configuration_declared,
        required_credentials_presence_markers=(
            required_credentials_presence_markers
        ),
        credential_values_present=credential_values_present,
        credential_value_accessed=credential_value_accessed,
        redaction_status=redaction_status,
        publish_mode=publish_mode,
        notification_mode=notification_mode,
        eval_mode=eval_mode,
        adapter_capability_markers=adapter_capability_markers,
        noop_policy_markers=noop_policy_markers,
        disabled_external_adapters_declared=(
            disabled_external_adapters_declared
        ),
        environment_safety_marker=environment_safety_marker,
        preflight_outcome=preflight_outcome,
        external_adapter_called=external_adapter_called,
        live_llm_called=live_llm_called,
        external_api_called=external_api_called,
        created_at=created_at,
        timestamp_policy=timestamp_policy,
        source_of_truth=source_of_truth,
        notes=notes,
    )
    prioritized_failures = (
        (run_id.strip() == "", RUN_ID_MISSING),
        (
            adapter_preflight_result_id.strip() == "",
            ADAPTER_PREFLIGHT_RESULT_ID_MISSING,
        ),
        (runtime_context_ref.strip() == "", RUNTIME_CONTEXT_REF_MISSING),
        (
            runtime_profile_snapshot_ref.strip() == "",
            RUNTIME_PROFILE_SNAPSHOT_REF_MISSING,
        ),
        (config_snapshot_ref.strip() == "", CONFIG_SNAPSHOT_REF_MISSING),
        (adapter_name.strip() == "", ADAPTER_NAME_MISSING),
        (adapter_mode.strip() == "", ADAPTER_MODE_MISSING),
        (
            adapter_mode.strip() != ""
            and adapter_mode != _NOOP_ADAPTER_MODE,
            ADAPTER_MODE_NOT_NOOP,
        ),
        (
            adapter_configuration_declared is not True,
            ADAPTER_CONFIGURATION_NOT_DECLARED,
        ),
        (
            required_credentials_presence_markers == (),
            REQUIRED_CREDENTIALS_PRESENCE_MARKERS_MISSING,
        ),
        (
            credential_values_present is True,
            CREDENTIAL_VALUES_PRESENT_TRUE,
        ),
        (
            credential_value_accessed is True,
            CREDENTIAL_VALUE_ACCESSED_TRUE,
        ),
        (redaction_status.strip() == "", REDACTION_STATUS_MISSING),
        (publish_mode.strip() == "", PUBLISH_MODE_MISSING),
        (
            publish_mode.strip() != "" and publish_mode != _NOOP_PUBLISH_MODE,
            PUBLISH_MODE_NOT_NOOP,
        ),
        (notification_mode.strip() == "", NOTIFICATION_MODE_MISSING),
        (
            notification_mode.strip() != ""
            and notification_mode != _NOOP_NOTIFICATION_MODE,
            NOTIFICATION_MODE_NOT_NOOP,
        ),
        (eval_mode.strip() == "", EVAL_MODE_MISSING),
        (
            adapter_capability_markers == (),
            ADAPTER_CAPABILITY_MARKERS_MISSING,
        ),
        (noop_policy_markers == (), NOOP_POLICY_MARKERS_MISSING),
        (
            disabled_external_adapters_declared is not True,
            DISABLED_EXTERNAL_ADAPTERS_NOT_DECLARED,
        ),
        (
            environment_safety_marker.strip() == "",
            ENVIRONMENT_SAFETY_MARKER_MISSING,
        ),
        (preflight_outcome.strip() == "", PREFLIGHT_OUTCOME_MISSING),
        (
            preflight_outcome.strip() != ""
            and preflight_outcome != _NOOP_PREFLIGHT_OUTCOME,
            PREFLIGHT_OUTCOME_NOT_NOOP_DECLARED,
        ),
        (
            external_adapter_called is True,
            EXTERNAL_ADAPTER_CALLED_TRUE,
        ),
        (live_llm_called is True, LIVE_LLM_CALLED_TRUE),
        (external_api_called is True, EXTERNAL_API_CALLED_TRUE),
        (created_at.strip() == "", CREATED_AT_MISSING),
        (timestamp_policy.strip() == "", TIMESTAMP_POLICY_MISSING),
        (source_of_truth == (), SOURCE_OF_TRUTH_MISSING),
    )
    preflight_result_violations = ()
    for is_violated, reason_code in prioritized_failures:
        if is_violated:
            preflight_result_violations = (
                preflight_result_violations + (reason_code,)
            )

    if preflight_result_violations:
        return _result(
            buildable=False,
            reason_code=preflight_result_violations[0],
            preflight_result=preflight_result,
            preflight_result_violations=preflight_result_violations,
            missing_or_invalid_fields=_missing_or_invalid_fields(
                preflight_result_violations
            ),
        )

    return _result(
        buildable=True,
        reason_code=ADAPTER_PREFLIGHT_RESULT_BUILDABLE,
        preflight_result=preflight_result,
        preflight_result_violations=(),
        missing_or_invalid_fields=(),
    )


def is_adapter_preflight_result_buildable(
    *,
    run_id: str,
    adapter_preflight_result_id: str,
    runtime_context_ref: str,
    runtime_profile_snapshot_ref: str,
    config_snapshot_ref: str,
    adapter_name: str,
    adapter_mode: str,
    adapter_configuration_declared: bool,
    required_credentials_presence_markers: tuple[str, ...],
    credential_values_present: bool,
    credential_value_accessed: bool,
    redaction_status: str,
    publish_mode: str,
    notification_mode: str,
    eval_mode: str,
    adapter_capability_markers: tuple[str, ...],
    noop_policy_markers: tuple[str, ...],
    disabled_external_adapters_declared: bool,
    environment_safety_marker: str,
    preflight_outcome: str,
    external_adapter_called: bool,
    live_llm_called: bool,
    external_api_called: bool,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> bool:
    """Return only the boolean result from the result explanation."""
    return explain_adapter_preflight_result_build(
        run_id=run_id,
        adapter_preflight_result_id=adapter_preflight_result_id,
        runtime_context_ref=runtime_context_ref,
        runtime_profile_snapshot_ref=runtime_profile_snapshot_ref,
        config_snapshot_ref=config_snapshot_ref,
        adapter_name=adapter_name,
        adapter_mode=adapter_mode,
        adapter_configuration_declared=adapter_configuration_declared,
        required_credentials_presence_markers=(
            required_credentials_presence_markers
        ),
        credential_values_present=credential_values_present,
        credential_value_accessed=credential_value_accessed,
        redaction_status=redaction_status,
        publish_mode=publish_mode,
        notification_mode=notification_mode,
        eval_mode=eval_mode,
        adapter_capability_markers=adapter_capability_markers,
        noop_policy_markers=noop_policy_markers,
        disabled_external_adapters_declared=(
            disabled_external_adapters_declared
        ),
        environment_safety_marker=environment_safety_marker,
        preflight_outcome=preflight_outcome,
        external_adapter_called=external_adapter_called,
        live_llm_called=live_llm_called,
        external_api_called=external_api_called,
        created_at=created_at,
        timestamp_policy=timestamp_policy,
        source_of_truth=source_of_truth,
        notes=notes,
    )["buildable"]
