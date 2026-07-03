"""Pure Run Ledger Entry builder for caller-supplied run fields."""

from typing import Final

from ai_daily_publishing_system.core import gates, states


RUN_LEDGER_ENTRY_BUILDABLE: Final[str] = "RUN_LEDGER_ENTRY_BUILDABLE"
RUN_ID_MISSING: Final[str] = "RUN_ID_MISSING"
RUN_STATE_MISSING: Final[str] = "RUN_STATE_MISSING"
RUN_STATE_UNKNOWN: Final[str] = "RUN_STATE_UNKNOWN"
RUN_OUTCOME_MISSING: Final[str] = "RUN_OUTCOME_MISSING"
RUNTIME_PROFILE_NAME_MISSING: Final[str] = (
    "RUNTIME_PROFILE_NAME_MISSING"
)
RUNTIME_PROFILE_MODE_MISSING: Final[str] = (
    "RUNTIME_PROFILE_MODE_MISSING"
)
PUBLISH_MODE_MISSING: Final[str] = "PUBLISH_MODE_MISSING"
NOTIFICATION_MODE_MISSING: Final[str] = "NOTIFICATION_MODE_MISSING"
EVAL_MODE_MISSING: Final[str] = "EVAL_MODE_MISSING"
GATE_DECISION_ENVELOPE_REFS_MISSING: Final[str] = (
    "GATE_DECISION_ENVELOPE_REFS_MISSING"
)
ARTIFACT_REFS_MISSING: Final[str] = "ARTIFACT_REFS_MISSING"
ARTIFACT_HASH_REFS_MISSING: Final[str] = (
    "ARTIFACT_HASH_REFS_MISSING"
)
STARTED_AT_MISSING: Final[str] = "STARTED_AT_MISSING"
COMPLETED_AT_MISSING: Final[str] = "COMPLETED_AT_MISSING"
TIMESTAMP_POLICY_MISSING: Final[str] = "TIMESTAMP_POLICY_MISSING"
SOURCE_OF_TRUTH_MISSING: Final[str] = "SOURCE_OF_TRUTH_MISSING"
PUBLIC_URL_CREATED_TRUE: Final[str] = "PUBLIC_URL_CREATED_TRUE"
PUBLIC_URL_NON_NULL: Final[str] = "PUBLIC_URL_NON_NULL"
FAILURE_REF_WITH_NON_FAILURE_OUTCOME: Final[str] = (
    "FAILURE_REF_WITH_NON_FAILURE_OUTCOME"
)
FAILURE_OUTCOME_WITHOUT_FAILURE_REF: Final[str] = (
    "FAILURE_OUTCOME_WITHOUT_FAILURE_REF"
)
BADCASE_REF_WITH_NON_GOVERNANCE_OUTCOME: Final[str] = (
    "BADCASE_REF_WITH_NON_GOVERNANCE_OUTCOME"
)
GOVERNANCE_OUTCOME_WITHOUT_BADCASE_REF: Final[str] = (
    "GOVERNANCE_OUTCOME_WITHOUT_BADCASE_REF"
)

RUN_LEDGER_ENTRY_BUILD_REASON_CODES: Final[tuple[str, ...]] = (
    RUN_ID_MISSING,
    RUN_STATE_MISSING,
    RUN_STATE_UNKNOWN,
    RUN_OUTCOME_MISSING,
    RUNTIME_PROFILE_NAME_MISSING,
    RUNTIME_PROFILE_MODE_MISSING,
    PUBLISH_MODE_MISSING,
    NOTIFICATION_MODE_MISSING,
    EVAL_MODE_MISSING,
    GATE_DECISION_ENVELOPE_REFS_MISSING,
    ARTIFACT_REFS_MISSING,
    ARTIFACT_HASH_REFS_MISSING,
    STARTED_AT_MISSING,
    COMPLETED_AT_MISSING,
    TIMESTAMP_POLICY_MISSING,
    SOURCE_OF_TRUTH_MISSING,
    PUBLIC_URL_CREATED_TRUE,
    PUBLIC_URL_NON_NULL,
    FAILURE_REF_WITH_NON_FAILURE_OUTCOME,
    FAILURE_OUTCOME_WITHOUT_FAILURE_REF,
    BADCASE_REF_WITH_NON_GOVERNANCE_OUTCOME,
    GOVERNANCE_OUTCOME_WITHOUT_BADCASE_REF,
    RUN_LEDGER_ENTRY_BUILDABLE,
)

_SOURCE: Final[str] = (
    "run_ledger_entry_builder.explain_run_ledger_entry_build"
)
_FAILURE_STATES: Final[tuple[str, ...]] = (
    states.CONFIG_BLOCKED,
    states.REVIEW_BLOCKED,
    states.SYSTEM_FAILED,
    states.ADAPTER_FAILED,
    states.BADCASE_CREATED,
)
_GOVERNANCE_STATES: Final[tuple[str, ...]] = (
    states.BADCASE_CREATED,
)
_LOCAL_INVARIANTS: Final[tuple[str, ...]] = (
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
)
_INVARIANTS: Final[tuple[str, ...]] = (
    gates.GATE_INVARIANTS + _LOCAL_INVARIANTS
)
_REASON_TEXT_ENTRIES: Final[tuple[tuple[str, str], ...]] = (
    (
        RUN_ID_MISSING,
        "A non-empty caller-supplied run_id is required.",
    ),
    (
        RUN_STATE_MISSING,
        "A non-empty caller-supplied run_state is required.",
    ),
    (
        RUN_STATE_UNKNOWN,
        "The caller-supplied run_state is not declared in states.MVP_STATES.",
    ),
    (
        RUN_OUTCOME_MISSING,
        "A non-empty caller-supplied run_outcome is required.",
    ),
    (
        RUNTIME_PROFILE_NAME_MISSING,
        "A non-empty caller-supplied runtime_profile_name is required.",
    ),
    (
        RUNTIME_PROFILE_MODE_MISSING,
        "A non-empty caller-supplied runtime_profile_mode is required.",
    ),
    (
        PUBLISH_MODE_MISSING,
        "A non-empty caller-supplied publish_mode is required.",
    ),
    (
        NOTIFICATION_MODE_MISSING,
        "A non-empty caller-supplied notification_mode is required.",
    ),
    (
        EVAL_MODE_MISSING,
        "A non-empty caller-supplied eval_mode is required.",
    ),
    (
        GATE_DECISION_ENVELOPE_REFS_MISSING,
        "At least one caller-supplied gate decision envelope ref is "
        "required.",
    ),
    (
        ARTIFACT_REFS_MISSING,
        "At least one caller-supplied artifact ref is required.",
    ),
    (
        ARTIFACT_HASH_REFS_MISSING,
        "At least one caller-supplied artifact hash ref is required.",
    ),
    (
        STARTED_AT_MISSING,
        "A non-empty caller-supplied started_at value is required.",
    ),
    (
        COMPLETED_AT_MISSING,
        "A non-empty caller-supplied completed_at value is required.",
    ),
    (
        TIMESTAMP_POLICY_MISSING,
        "A non-empty caller-supplied timestamp_policy is required.",
    ),
    (
        SOURCE_OF_TRUTH_MISSING,
        "At least one caller-supplied source_of_truth reference is required.",
    ),
    (
        PUBLIC_URL_CREATED_TRUE,
        "MVP noop run ledger entries require public_url_created to remain "
        "false.",
    ),
    (
        PUBLIC_URL_NON_NULL,
        "MVP noop run ledger entries require the caller-supplied public URL "
        "null marker to remain true.",
    ),
    (
        FAILURE_REF_WITH_NON_FAILURE_OUTCOME,
        "failure_package_ref is only allowed for failure or governance "
        "run_state values.",
    ),
    (
        FAILURE_OUTCOME_WITHOUT_FAILURE_REF,
        "failure or governance run_state values require a caller-supplied "
        "failure_package_ref.",
    ),
    (
        BADCASE_REF_WITH_NON_GOVERNANCE_OUTCOME,
        "badcase_record_ref is only allowed for governance run_state values.",
    ),
    (
        GOVERNANCE_OUTCOME_WITHOUT_BADCASE_REF,
        "governance run_state values require a caller-supplied "
        "badcase_record_ref.",
    ),
    (
        RUN_LEDGER_ENTRY_BUILDABLE,
        "The caller-supplied fields can build the Run Ledger Entry shape. "
        "This does not write run-ledger.yaml, execute a gate, map or execute "
        "a transition, calculate a hash, publish, send notification, create "
        "or return a public URL, read runtime context, configuration, "
        "credentials, adapter outputs, artifact refs, review refs, hash refs "
        "or ledgers, call existing policy modules, call the gate decision "
        "envelope builder, or call an external service.",
    ),
)
_VIOLATION_FIELD_ENTRIES: Final[tuple[tuple[str, tuple[str, ...]], ...]] = (
    (RUN_ID_MISSING, ("run_id",)),
    (RUN_STATE_MISSING, ("run_state",)),
    (RUN_STATE_UNKNOWN, ("run_state",)),
    (RUN_OUTCOME_MISSING, ("run_outcome",)),
    (RUNTIME_PROFILE_NAME_MISSING, ("runtime_profile_name",)),
    (RUNTIME_PROFILE_MODE_MISSING, ("runtime_profile_mode",)),
    (PUBLISH_MODE_MISSING, ("publish_mode",)),
    (NOTIFICATION_MODE_MISSING, ("notification_mode",)),
    (EVAL_MODE_MISSING, ("eval_mode",)),
    (
        GATE_DECISION_ENVELOPE_REFS_MISSING,
        ("gate_decision_envelope_refs",),
    ),
    (ARTIFACT_REFS_MISSING, ("artifact_refs",)),
    (ARTIFACT_HASH_REFS_MISSING, ("artifact_hash_refs",)),
    (STARTED_AT_MISSING, ("started_at",)),
    (COMPLETED_AT_MISSING, ("completed_at",)),
    (TIMESTAMP_POLICY_MISSING, ("timestamp_policy",)),
    (SOURCE_OF_TRUTH_MISSING, ("source_of_truth",)),
    (PUBLIC_URL_CREATED_TRUE, ("public_url_created",)),
    (PUBLIC_URL_NON_NULL, ("public_url",)),
    (FAILURE_REF_WITH_NON_FAILURE_OUTCOME, ("failure_package_ref",)),
    (FAILURE_OUTCOME_WITHOUT_FAILURE_REF, ("failure_package_ref",)),
    (BADCASE_REF_WITH_NON_GOVERNANCE_OUTCOME, ("badcase_record_ref",)),
    (GOVERNANCE_OUTCOME_WITHOUT_BADCASE_REF, ("badcase_record_ref",)),
)


def _reason_text(reason_code: str) -> str:
    for code, text in _REASON_TEXT_ENTRIES:
        if code == reason_code:
            return text
    return "Unknown Run Ledger Entry build result."


def _ordered_unique(values: tuple[str, ...]) -> tuple[str, ...]:
    ordered_values = ()
    for value in values:
        if value not in ordered_values:
            ordered_values = ordered_values + (value,)
    return ordered_values


def _missing_or_invalid_fields(
    entry_violations: tuple[str, ...],
) -> tuple[str, ...]:
    field_names = ()
    for violation in entry_violations:
        for reason_code, invalid_fields in _VIOLATION_FIELD_ENTRIES:
            if violation == reason_code:
                field_names = field_names + invalid_fields
    return _ordered_unique(field_names)


def _entry(
    *,
    run_id: str,
    run_state: str,
    run_outcome: str,
    runtime_profile_name: str,
    runtime_profile_mode: str,
    publish_mode: str,
    notification_mode: str,
    eval_mode: str,
    gate_decision_envelope_refs: tuple[str, ...],
    artifact_refs: tuple[str, ...],
    artifact_hash_refs: tuple[str, ...],
    failure_package_ref: str,
    badcase_record_ref: str,
    public_url_created: bool,
    started_at: str,
    completed_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    return {
        "run_id": run_id,
        "run_state": run_state,
        "run_outcome": run_outcome,
        "runtime_profile_name": runtime_profile_name,
        "runtime_profile_mode": runtime_profile_mode,
        "publish_mode": publish_mode,
        "notification_mode": notification_mode,
        "eval_mode": eval_mode,
        "gate_decision_envelope_refs": gate_decision_envelope_refs,
        "artifact_refs": artifact_refs,
        "artifact_hash_refs": artifact_hash_refs,
        "failure_package_ref": failure_package_ref,
        "badcase_record_ref": badcase_record_ref,
        "public_url_created": public_url_created,
        "public_url": None,
        "started_at": started_at,
        "completed_at": completed_at,
        "timestamp_policy": timestamp_policy,
        "source_of_truth": source_of_truth,
        "notes": notes,
    }


def _result(
    *,
    buildable: bool,
    reason_code: str,
    entry,
    entry_violations: tuple[str, ...],
    missing_or_invalid_fields: tuple[str, ...],
) -> dict[str, object]:
    return {
        "buildable": buildable,
        "reason_code": reason_code,
        "reason": _reason_text(reason_code),
        "source": _SOURCE,
        "entry": entry,
        "entry_violations": entry_violations,
        "missing_or_invalid_fields": missing_or_invalid_fields,
        "invariant_refs": _INVARIANTS,
    }


def explain_run_ledger_entry_build(
    *,
    run_id: str,
    run_state: str,
    run_outcome: str,
    runtime_profile_name: str,
    runtime_profile_mode: str,
    publish_mode: str,
    notification_mode: str,
    eval_mode: str,
    gate_decision_envelope_refs: tuple[str, ...],
    artifact_refs: tuple[str, ...],
    artifact_hash_refs: tuple[str, ...],
    failure_package_ref: str,
    badcase_record_ref: str,
    public_url_created: bool,
    public_url_is_null: bool,
    started_at: str,
    completed_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    """Explain whether caller-supplied fields can build the entry."""
    run_state_missing = run_state.strip() == ""
    run_state_unknown = (
        run_state_missing is False and run_state not in states.MVP_STATES
    )
    run_state_is_failure = run_state in _FAILURE_STATES
    run_state_is_governance = run_state in _GOVERNANCE_STATES
    failure_package_ref_present = failure_package_ref.strip() != ""
    badcase_record_ref_present = badcase_record_ref.strip() != ""
    prioritized_violations = (
        (run_id.strip() == "", RUN_ID_MISSING),
        (run_state_missing, RUN_STATE_MISSING),
        (run_state_unknown, RUN_STATE_UNKNOWN),
        (run_outcome.strip() == "", RUN_OUTCOME_MISSING),
        (
            runtime_profile_name.strip() == "",
            RUNTIME_PROFILE_NAME_MISSING,
        ),
        (
            runtime_profile_mode.strip() == "",
            RUNTIME_PROFILE_MODE_MISSING,
        ),
        (publish_mode.strip() == "", PUBLISH_MODE_MISSING),
        (notification_mode.strip() == "", NOTIFICATION_MODE_MISSING),
        (eval_mode.strip() == "", EVAL_MODE_MISSING),
        (
            gate_decision_envelope_refs == (),
            GATE_DECISION_ENVELOPE_REFS_MISSING,
        ),
        (artifact_refs == (), ARTIFACT_REFS_MISSING),
        (artifact_hash_refs == (), ARTIFACT_HASH_REFS_MISSING),
        (started_at.strip() == "", STARTED_AT_MISSING),
        (completed_at.strip() == "", COMPLETED_AT_MISSING),
        (timestamp_policy.strip() == "", TIMESTAMP_POLICY_MISSING),
        (source_of_truth == (), SOURCE_OF_TRUTH_MISSING),
        (public_url_created is True, PUBLIC_URL_CREATED_TRUE),
        (public_url_is_null is False, PUBLIC_URL_NON_NULL),
        (
            run_state_is_failure is False and failure_package_ref_present,
            FAILURE_REF_WITH_NON_FAILURE_OUTCOME,
        ),
        (
            run_state_is_failure is True
            and failure_package_ref_present is False,
            FAILURE_OUTCOME_WITHOUT_FAILURE_REF,
        ),
        (
            run_state_is_governance is False and badcase_record_ref_present,
            BADCASE_REF_WITH_NON_GOVERNANCE_OUTCOME,
        ),
        (
            run_state_is_governance is True
            and badcase_record_ref_present is False,
            GOVERNANCE_OUTCOME_WITHOUT_BADCASE_REF,
        ),
    )
    entry_violations = tuple(
        reason_code
        for condition, reason_code in prioritized_violations
        if condition
    )
    buildable = entry_violations == ()
    reason_code = (
        RUN_LEDGER_ENTRY_BUILDABLE if buildable else entry_violations[0]
    )

    return _result(
        buildable=buildable,
        reason_code=reason_code,
        entry=_entry(
            run_id=run_id,
            run_state=run_state,
            run_outcome=run_outcome,
            runtime_profile_name=runtime_profile_name,
            runtime_profile_mode=runtime_profile_mode,
            publish_mode=publish_mode,
            notification_mode=notification_mode,
            eval_mode=eval_mode,
            gate_decision_envelope_refs=gate_decision_envelope_refs,
            artifact_refs=artifact_refs,
            artifact_hash_refs=artifact_hash_refs,
            failure_package_ref=failure_package_ref,
            badcase_record_ref=badcase_record_ref,
            public_url_created=public_url_created,
            started_at=started_at,
            completed_at=completed_at,
            timestamp_policy=timestamp_policy,
            source_of_truth=source_of_truth,
            notes=notes,
        ),
        entry_violations=entry_violations,
        missing_or_invalid_fields=(
            _missing_or_invalid_fields(entry_violations)
        ),
    )


def is_run_ledger_entry_buildable(
    *,
    run_id: str,
    run_state: str,
    run_outcome: str,
    runtime_profile_name: str,
    runtime_profile_mode: str,
    publish_mode: str,
    notification_mode: str,
    eval_mode: str,
    gate_decision_envelope_refs: tuple[str, ...],
    artifact_refs: tuple[str, ...],
    artifact_hash_refs: tuple[str, ...],
    failure_package_ref: str,
    badcase_record_ref: str,
    public_url_created: bool,
    public_url_is_null: bool,
    started_at: str,
    completed_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> bool:
    """Return only the boolean result from the build explanation."""
    return bool(
        explain_run_ledger_entry_build(
            run_id=run_id,
            run_state=run_state,
            run_outcome=run_outcome,
            runtime_profile_name=runtime_profile_name,
            runtime_profile_mode=runtime_profile_mode,
            publish_mode=publish_mode,
            notification_mode=notification_mode,
            eval_mode=eval_mode,
            gate_decision_envelope_refs=gate_decision_envelope_refs,
            artifact_refs=artifact_refs,
            artifact_hash_refs=artifact_hash_refs,
            failure_package_ref=failure_package_ref,
            badcase_record_ref=badcase_record_ref,
            public_url_created=public_url_created,
            public_url_is_null=public_url_is_null,
            started_at=started_at,
            completed_at=completed_at,
            timestamp_policy=timestamp_policy,
            source_of_truth=source_of_truth,
            notes=notes,
        )["buildable"]
    )
