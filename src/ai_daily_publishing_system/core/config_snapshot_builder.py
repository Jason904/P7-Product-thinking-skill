"""Pure Config Snapshot builder for caller-supplied markers."""

from typing import Final

from ai_daily_publishing_system.core import states


CONFIG_SNAPSHOT_BUILDABLE: Final[str] = "CONFIG_SNAPSHOT_BUILDABLE"
RUN_ID_MISSING: Final[str] = "RUN_ID_MISSING"
CONFIG_SNAPSHOT_ID_MISSING: Final[str] = "CONFIG_SNAPSHOT_ID_MISSING"
CONFIG_NAME_MISSING: Final[str] = "CONFIG_NAME_MISSING"
CONFIG_MODE_MISSING: Final[str] = "CONFIG_MODE_MISSING"
CONFIG_MODE_NOT_MANUAL_LOCAL_NOOP: Final[str] = (
    "CONFIG_MODE_NOT_MANUAL_LOCAL_NOOP"
)
CONFIG_SOURCE_MODE_MISSING: Final[str] = "CONFIG_SOURCE_MODE_MISSING"
CONFIG_SOURCE_MODE_NOT_CALLER_SUPPLIED: Final[str] = (
    "CONFIG_SOURCE_MODE_NOT_CALLER_SUPPLIED"
)
RUNTIME_PROFILE_SNAPSHOT_REF_MISSING: Final[str] = (
    "RUNTIME_PROFILE_SNAPSHOT_REF_MISSING"
)
PUBLISH_MODE_MISSING: Final[str] = "PUBLISH_MODE_MISSING"
PUBLISH_MODE_NOT_NOOP: Final[str] = "PUBLISH_MODE_NOT_NOOP"
NOTIFICATION_MODE_MISSING: Final[str] = "NOTIFICATION_MODE_MISSING"
NOTIFICATION_MODE_NOT_NOOP: Final[str] = "NOTIFICATION_MODE_NOT_NOOP"
EVAL_MODE_MISSING: Final[str] = "EVAL_MODE_MISSING"
ADAPTER_CONFIGURATION_NOT_DECLARED: Final[str] = (
    "ADAPTER_CONFIGURATION_NOT_DECLARED"
)
REQUIRED_CREDENTIALS_PRESENCE_MARKERS_MISSING: Final[str] = (
    "REQUIRED_CREDENTIALS_PRESENCE_MARKERS_MISSING"
)
CREDENTIAL_VALUE_ACCESS_ENABLED_TRUE: Final[str] = (
    "CREDENTIAL_VALUE_ACCESS_ENABLED_TRUE"
)
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
REDACTION_STATUS_MISSING: Final[str] = "REDACTION_STATUS_MISSING"
CREATED_AT_MISSING: Final[str] = "CREATED_AT_MISSING"
TIMESTAMP_POLICY_MISSING: Final[str] = "TIMESTAMP_POLICY_MISSING"
SOURCE_OF_TRUTH_MISSING: Final[str] = "SOURCE_OF_TRUTH_MISSING"

CONFIG_SNAPSHOT_BUILD_REASON_CODES: Final[tuple[str, ...]] = (
    RUN_ID_MISSING,
    CONFIG_SNAPSHOT_ID_MISSING,
    CONFIG_NAME_MISSING,
    CONFIG_MODE_MISSING,
    CONFIG_MODE_NOT_MANUAL_LOCAL_NOOP,
    CONFIG_SOURCE_MODE_MISSING,
    CONFIG_SOURCE_MODE_NOT_CALLER_SUPPLIED,
    RUNTIME_PROFILE_SNAPSHOT_REF_MISSING,
    PUBLISH_MODE_MISSING,
    PUBLISH_MODE_NOT_NOOP,
    NOTIFICATION_MODE_MISSING,
    NOTIFICATION_MODE_NOT_NOOP,
    EVAL_MODE_MISSING,
    ADAPTER_CONFIGURATION_NOT_DECLARED,
    REQUIRED_CREDENTIALS_PRESENCE_MARKERS_MISSING,
    CREDENTIAL_VALUE_ACCESS_ENABLED_TRUE,
    ADAPTER_CAPABILITY_MARKERS_MISSING,
    NOOP_POLICY_MARKERS_MISSING,
    DISABLED_EXTERNAL_ADAPTERS_NOT_DECLARED,
    ENVIRONMENT_SAFETY_MARKER_MISSING,
    REDACTION_STATUS_MISSING,
    CREATED_AT_MISSING,
    TIMESTAMP_POLICY_MISSING,
    SOURCE_OF_TRUTH_MISSING,
    CONFIG_SNAPSHOT_BUILDABLE,
)

_SOURCE: Final[str] = (
    "config_snapshot_builder.explain_config_snapshot_build"
)
_MANUAL_LOCAL_NOOP_CONFIG_MODE: Final[str] = "manual_local_noop"
_CALLER_SUPPLIED_CONFIG_SOURCE_MODE: Final[str] = "caller_supplied"
_NOOP_PUBLISH_MODE: Final[str] = "noop"
_NOOP_NOTIFICATION_MODE: Final[str] = "noop"
_LOCAL_INVARIANTS: Final[tuple[str, ...]] = (
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
        CONFIG_SNAPSHOT_ID_MISSING,
        "A non-empty caller-supplied config_snapshot_id is required.",
    ),
    (
        CONFIG_NAME_MISSING,
        "A non-empty caller-supplied config_name is required.",
    ),
    (
        CONFIG_MODE_MISSING,
        "A non-empty caller-supplied config_mode is required.",
    ),
    (
        CONFIG_MODE_NOT_MANUAL_LOCAL_NOOP,
        "The caller-supplied config_mode must be exactly "
        "manual_local_noop.",
    ),
    (
        CONFIG_SOURCE_MODE_MISSING,
        "A non-empty caller-supplied config_source_mode is required.",
    ),
    (
        CONFIG_SOURCE_MODE_NOT_CALLER_SUPPLIED,
        "The caller-supplied config_source_mode must be exactly "
        "caller_supplied.",
    ),
    (
        RUNTIME_PROFILE_SNAPSHOT_REF_MISSING,
        "A non-empty caller-supplied runtime_profile_snapshot_ref is "
        "required; the builder does not read profile snapshots.",
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
        CREDENTIAL_VALUE_ACCESS_ENABLED_TRUE,
        "MVP config snapshots require credential_value_access_enabled "
        "to remain false.",
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
        REDACTION_STATUS_MISSING,
        "A non-empty caller-supplied redaction_status is required.",
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
        CONFIG_SNAPSHOT_BUILDABLE,
        "The caller-supplied fields can build the Config Snapshot "
        "shape. This does not write config-snapshot.yaml, write "
        "runtime-context.yaml, start runtime execution, run a scheduler, "
        "read environment, configuration or credentials, check "
        "credential availability, execute adapter preflight, call "
        "adapters, invoke drivers, execute gates, map or execute "
        "transitions, read artifacts, reviews, hashes or ledgers, "
        "calculate hashes, write ledgers, publish, notify, create or "
        "return a public URL, or call existing policy or builder "
        "modules.",
    ),
)
_VIOLATION_FIELD_ENTRIES: Final[tuple[tuple[str, tuple[str, ...]], ...]] = (
    (RUN_ID_MISSING, ("run_id",)),
    (CONFIG_SNAPSHOT_ID_MISSING, ("config_snapshot_id",)),
    (CONFIG_NAME_MISSING, ("config_name",)),
    (CONFIG_MODE_MISSING, ("config_mode",)),
    (CONFIG_MODE_NOT_MANUAL_LOCAL_NOOP, ("config_mode",)),
    (CONFIG_SOURCE_MODE_MISSING, ("config_source_mode",)),
    (
        CONFIG_SOURCE_MODE_NOT_CALLER_SUPPLIED,
        ("config_source_mode",),
    ),
    (
        RUNTIME_PROFILE_SNAPSHOT_REF_MISSING,
        ("runtime_profile_snapshot_ref",),
    ),
    (PUBLISH_MODE_MISSING, ("publish_mode",)),
    (PUBLISH_MODE_NOT_NOOP, ("publish_mode",)),
    (NOTIFICATION_MODE_MISSING, ("notification_mode",)),
    (NOTIFICATION_MODE_NOT_NOOP, ("notification_mode",)),
    (EVAL_MODE_MISSING, ("eval_mode",)),
    (
        ADAPTER_CONFIGURATION_NOT_DECLARED,
        ("adapter_configuration_declared",),
    ),
    (
        REQUIRED_CREDENTIALS_PRESENCE_MARKERS_MISSING,
        ("required_credentials_presence_markers",),
    ),
    (
        CREDENTIAL_VALUE_ACCESS_ENABLED_TRUE,
        ("credential_value_access_enabled",),
    ),
    (ADAPTER_CAPABILITY_MARKERS_MISSING, ("adapter_capability_markers",)),
    (NOOP_POLICY_MARKERS_MISSING, ("noop_policy_markers",)),
    (
        DISABLED_EXTERNAL_ADAPTERS_NOT_DECLARED,
        ("disabled_external_adapters_declared",),
    ),
    (ENVIRONMENT_SAFETY_MARKER_MISSING, ("environment_safety_marker",)),
    (REDACTION_STATUS_MISSING, ("redaction_status",)),
    (CREATED_AT_MISSING, ("created_at",)),
    (TIMESTAMP_POLICY_MISSING, ("timestamp_policy",)),
    (SOURCE_OF_TRUTH_MISSING, ("source_of_truth",)),
)


def _reason_text(reason_code: str) -> str:
    for code, text in _REASON_TEXT_ENTRIES:
        if code == reason_code:
            return text
    return "Unknown Config Snapshot build result."


def _ordered_unique(values: tuple[str, ...]) -> tuple[str, ...]:
    ordered_values = ()
    for value in values:
        if value not in ordered_values:
            ordered_values = ordered_values + (value,)
    return ordered_values


def _missing_or_invalid_fields(
    snapshot_violations: tuple[str, ...],
) -> tuple[str, ...]:
    field_names = ()
    for violation in snapshot_violations:
        for reason_code, invalid_fields in _VIOLATION_FIELD_ENTRIES:
            if reason_code == violation:
                field_names = field_names + invalid_fields
    return _ordered_unique(field_names)


def _snapshot(
    *,
    run_id: str,
    config_snapshot_id: str,
    config_name: str,
    config_mode: str,
    config_source_mode: str,
    runtime_profile_snapshot_ref: str,
    publish_mode: str,
    notification_mode: str,
    eval_mode: str,
    adapter_configuration_declared: bool,
    required_credentials_presence_markers: tuple[str, ...],
    credential_value_access_enabled: bool,
    adapter_capability_markers: tuple[str, ...],
    noop_policy_markers: tuple[str, ...],
    disabled_external_adapters_declared: bool,
    environment_safety_marker: str,
    redaction_status: str,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    return {
        "run_id": run_id,
        "config_snapshot_id": config_snapshot_id,
        "config_name": config_name,
        "config_mode": config_mode,
        "config_source_mode": config_source_mode,
        "runtime_profile_snapshot_ref": runtime_profile_snapshot_ref,
        "publish_mode": publish_mode,
        "notification_mode": notification_mode,
        "eval_mode": eval_mode,
        "adapter_configuration_declared": adapter_configuration_declared,
        "required_credentials_presence_markers": (
            required_credentials_presence_markers
        ),
        "credential_value_access_enabled": credential_value_access_enabled,
        "adapter_capability_markers": adapter_capability_markers,
        "noop_policy_markers": noop_policy_markers,
        "disabled_external_adapters_declared": (
            disabled_external_adapters_declared
        ),
        "environment_safety_marker": environment_safety_marker,
        "redaction_status": redaction_status,
        "created_at": created_at,
        "timestamp_policy": timestamp_policy,
        "source_of_truth": source_of_truth,
        "notes": notes,
    }


def _result(
    *,
    buildable: bool,
    reason_code: str,
    snapshot: object,
    snapshot_violations: tuple[str, ...],
    missing_or_invalid_fields: tuple[str, ...],
) -> dict[str, object]:
    return {
        "buildable": buildable,
        "reason_code": reason_code,
        "reason": _reason_text(reason_code),
        "source": _SOURCE,
        "snapshot": snapshot,
        "snapshot_violations": snapshot_violations,
        "missing_or_invalid_fields": missing_or_invalid_fields,
        "invariant_refs": _INVARIANTS,
    }


def explain_config_snapshot_build(
    *,
    run_id: str,
    config_snapshot_id: str,
    config_name: str,
    config_mode: str,
    config_source_mode: str,
    runtime_profile_snapshot_ref: str,
    publish_mode: str,
    notification_mode: str,
    eval_mode: str,
    adapter_configuration_declared: bool,
    required_credentials_presence_markers: tuple[str, ...],
    credential_value_access_enabled: bool,
    adapter_capability_markers: tuple[str, ...],
    noop_policy_markers: tuple[str, ...],
    disabled_external_adapters_declared: bool,
    environment_safety_marker: str,
    redaction_status: str,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    """Explain whether caller-supplied fields can build a snapshot."""
    snapshot = _snapshot(
        run_id=run_id,
        config_snapshot_id=config_snapshot_id,
        config_name=config_name,
        config_mode=config_mode,
        config_source_mode=config_source_mode,
        runtime_profile_snapshot_ref=runtime_profile_snapshot_ref,
        publish_mode=publish_mode,
        notification_mode=notification_mode,
        eval_mode=eval_mode,
        adapter_configuration_declared=adapter_configuration_declared,
        required_credentials_presence_markers=(
            required_credentials_presence_markers
        ),
        credential_value_access_enabled=credential_value_access_enabled,
        adapter_capability_markers=adapter_capability_markers,
        noop_policy_markers=noop_policy_markers,
        disabled_external_adapters_declared=(
            disabled_external_adapters_declared
        ),
        environment_safety_marker=environment_safety_marker,
        redaction_status=redaction_status,
        created_at=created_at,
        timestamp_policy=timestamp_policy,
        source_of_truth=source_of_truth,
        notes=notes,
    )
    prioritized_failures = (
        (run_id.strip() == "", RUN_ID_MISSING),
        (config_snapshot_id.strip() == "", CONFIG_SNAPSHOT_ID_MISSING),
        (config_name.strip() == "", CONFIG_NAME_MISSING),
        (config_mode.strip() == "", CONFIG_MODE_MISSING),
        (
            config_mode.strip() != ""
            and config_mode != _MANUAL_LOCAL_NOOP_CONFIG_MODE,
            CONFIG_MODE_NOT_MANUAL_LOCAL_NOOP,
        ),
        (config_source_mode.strip() == "", CONFIG_SOURCE_MODE_MISSING),
        (
            config_source_mode.strip() != ""
            and config_source_mode != _CALLER_SUPPLIED_CONFIG_SOURCE_MODE,
            CONFIG_SOURCE_MODE_NOT_CALLER_SUPPLIED,
        ),
        (
            runtime_profile_snapshot_ref.strip() == "",
            RUNTIME_PROFILE_SNAPSHOT_REF_MISSING,
        ),
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
            adapter_configuration_declared is not True,
            ADAPTER_CONFIGURATION_NOT_DECLARED,
        ),
        (
            required_credentials_presence_markers == (),
            REQUIRED_CREDENTIALS_PRESENCE_MARKERS_MISSING,
        ),
        (
            credential_value_access_enabled is True,
            CREDENTIAL_VALUE_ACCESS_ENABLED_TRUE,
        ),
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
        (redaction_status.strip() == "", REDACTION_STATUS_MISSING),
        (created_at.strip() == "", CREATED_AT_MISSING),
        (timestamp_policy.strip() == "", TIMESTAMP_POLICY_MISSING),
        (source_of_truth == (), SOURCE_OF_TRUTH_MISSING),
    )
    snapshot_violations = ()
    for is_violated, reason_code in prioritized_failures:
        if is_violated:
            snapshot_violations = snapshot_violations + (reason_code,)

    if snapshot_violations:
        return _result(
            buildable=False,
            reason_code=snapshot_violations[0],
            snapshot=snapshot,
            snapshot_violations=snapshot_violations,
            missing_or_invalid_fields=_missing_or_invalid_fields(
                snapshot_violations
            ),
        )

    return _result(
        buildable=True,
        reason_code=CONFIG_SNAPSHOT_BUILDABLE,
        snapshot=snapshot,
        snapshot_violations=(),
        missing_or_invalid_fields=(),
    )


def is_config_snapshot_buildable(
    *,
    run_id: str,
    config_snapshot_id: str,
    config_name: str,
    config_mode: str,
    config_source_mode: str,
    runtime_profile_snapshot_ref: str,
    publish_mode: str,
    notification_mode: str,
    eval_mode: str,
    adapter_configuration_declared: bool,
    required_credentials_presence_markers: tuple[str, ...],
    credential_value_access_enabled: bool,
    adapter_capability_markers: tuple[str, ...],
    noop_policy_markers: tuple[str, ...],
    disabled_external_adapters_declared: bool,
    environment_safety_marker: str,
    redaction_status: str,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> bool:
    """Return only the boolean result from the snapshot explanation."""
    return bool(
        explain_config_snapshot_build(
            run_id=run_id,
            config_snapshot_id=config_snapshot_id,
            config_name=config_name,
            config_mode=config_mode,
            config_source_mode=config_source_mode,
            runtime_profile_snapshot_ref=runtime_profile_snapshot_ref,
            publish_mode=publish_mode,
            notification_mode=notification_mode,
            eval_mode=eval_mode,
            adapter_configuration_declared=adapter_configuration_declared,
            required_credentials_presence_markers=(
                required_credentials_presence_markers
            ),
            credential_value_access_enabled=credential_value_access_enabled,
            adapter_capability_markers=adapter_capability_markers,
            noop_policy_markers=noop_policy_markers,
            disabled_external_adapters_declared=(
                disabled_external_adapters_declared
            ),
            environment_safety_marker=environment_safety_marker,
            redaction_status=redaction_status,
            created_at=created_at,
            timestamp_policy=timestamp_policy,
            source_of_truth=source_of_truth,
            notes=notes,
        )["buildable"]
    )
