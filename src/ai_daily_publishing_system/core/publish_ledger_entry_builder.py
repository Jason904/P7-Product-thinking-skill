"""Pure Publish Ledger Entry builder for caller-supplied noop fields."""

from typing import Final

from ai_daily_publishing_system.core import states


PUBLISH_LEDGER_ENTRY_BUILDABLE: Final[str] = (
    "PUBLISH_LEDGER_ENTRY_BUILDABLE"
)
RUN_ID_MISSING: Final[str] = "RUN_ID_MISSING"
PUBLISH_ID_MISSING: Final[str] = "PUBLISH_ID_MISSING"
PUBLISH_MODE_MISSING: Final[str] = "PUBLISH_MODE_MISSING"
PUBLISH_MODE_NOT_NOOP: Final[str] = "PUBLISH_MODE_NOT_NOOP"
PUBLISH_OUTCOME_MISSING: Final[str] = "PUBLISH_OUTCOME_MISSING"
PUBLISH_OUTCOME_NOT_NOOP_COMPLETED: Final[str] = (
    "PUBLISH_OUTCOME_NOT_NOOP_COMPLETED"
)
SOURCE_STATE_MISSING: Final[str] = "SOURCE_STATE_MISSING"
SOURCE_STATE_UNKNOWN: Final[str] = "SOURCE_STATE_UNKNOWN"
SOURCE_STATE_NOT_PUBLISH_ALLOWED: Final[str] = (
    "SOURCE_STATE_NOT_PUBLISH_ALLOWED"
)
TARGET_STATE_MISSING: Final[str] = "TARGET_STATE_MISSING"
TARGET_STATE_UNKNOWN: Final[str] = "TARGET_STATE_UNKNOWN"
TARGET_STATE_NOT_NOOP_COMPLETED: Final[str] = (
    "TARGET_STATE_NOT_NOOP_COMPLETED"
)
PUBLIC_CANDIDATE_REF_MISSING: Final[str] = (
    "PUBLIC_CANDIDATE_REF_MISSING"
)
GATE_DECISION_ENVELOPE_REFS_MISSING: Final[str] = (
    "GATE_DECISION_ENVELOPE_REFS_MISSING"
)
ARTIFACT_HASH_MANIFEST_REFS_MISSING: Final[str] = (
    "ARTIFACT_HASH_MANIFEST_REFS_MISSING"
)
ARTIFACT_REFS_MISSING: Final[str] = "ARTIFACT_REFS_MISSING"
REDACTION_STATUS_MISSING: Final[str] = "REDACTION_STATUS_MISSING"
CREATED_AT_MISSING: Final[str] = "CREATED_AT_MISSING"
TIMESTAMP_POLICY_MISSING: Final[str] = "TIMESTAMP_POLICY_MISSING"
SOURCE_OF_TRUTH_MISSING: Final[str] = "SOURCE_OF_TRUTH_MISSING"
PUBLIC_URL_CREATED_TRUE: Final[str] = "PUBLIC_URL_CREATED_TRUE"
PUBLIC_URL_NON_NULL: Final[str] = "PUBLIC_URL_NON_NULL"

PUBLISH_LEDGER_ENTRY_BUILD_REASON_CODES: Final[tuple[str, ...]] = (
    RUN_ID_MISSING,
    PUBLISH_ID_MISSING,
    PUBLISH_MODE_MISSING,
    PUBLISH_MODE_NOT_NOOP,
    PUBLISH_OUTCOME_MISSING,
    PUBLISH_OUTCOME_NOT_NOOP_COMPLETED,
    SOURCE_STATE_MISSING,
    SOURCE_STATE_UNKNOWN,
    SOURCE_STATE_NOT_PUBLISH_ALLOWED,
    TARGET_STATE_MISSING,
    TARGET_STATE_UNKNOWN,
    TARGET_STATE_NOT_NOOP_COMPLETED,
    PUBLIC_CANDIDATE_REF_MISSING,
    GATE_DECISION_ENVELOPE_REFS_MISSING,
    ARTIFACT_HASH_MANIFEST_REFS_MISSING,
    ARTIFACT_REFS_MISSING,
    REDACTION_STATUS_MISSING,
    CREATED_AT_MISSING,
    TIMESTAMP_POLICY_MISSING,
    SOURCE_OF_TRUTH_MISSING,
    PUBLIC_URL_CREATED_TRUE,
    PUBLIC_URL_NON_NULL,
    PUBLISH_LEDGER_ENTRY_BUILDABLE,
)

_SOURCE: Final[str] = (
    "publish_ledger_entry_builder.explain_publish_ledger_entry_build"
)
_NOOP_PUBLISH_MODE: Final[str] = "noop"
_PASS_PUBLISHED_LABEL: Final[str] = "PASS_PUBLISHED"
_LOCAL_INVARIANTS: Final[tuple[str, ...]] = (
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
        PUBLISH_ID_MISSING,
        "A non-empty caller-supplied publish_id is required.",
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
        PUBLISH_OUTCOME_MISSING,
        "A non-empty caller-supplied publish_outcome is required.",
    ),
    (
        PUBLISH_OUTCOME_NOT_NOOP_COMPLETED,
        "The caller-supplied publish_outcome must be NOOP_COMPLETED; "
        f"{_PASS_PUBLISHED_LABEL} remains forbidden.",
    ),
    (
        SOURCE_STATE_MISSING,
        "A non-empty caller-supplied source_state is required.",
    ),
    (
        SOURCE_STATE_UNKNOWN,
        "The caller-supplied source_state is not declared in "
        "states.MVP_STATES.",
    ),
    (
        SOURCE_STATE_NOT_PUBLISH_ALLOWED,
        "The caller-supplied source_state must be PUBLISH_ALLOWED.",
    ),
    (
        TARGET_STATE_MISSING,
        "A non-empty caller-supplied target_state is required.",
    ),
    (
        TARGET_STATE_UNKNOWN,
        "The caller-supplied target_state is not declared in "
        "states.MVP_STATES.",
    ),
    (
        TARGET_STATE_NOT_NOOP_COMPLETED,
        "The caller-supplied target_state must be NOOP_COMPLETED.",
    ),
    (
        PUBLIC_CANDIDATE_REF_MISSING,
        "A non-empty caller-supplied public_candidate_ref is required.",
    ),
    (
        GATE_DECISION_ENVELOPE_REFS_MISSING,
        "At least one caller-supplied gate decision envelope ref is "
        "required.",
    ),
    (
        ARTIFACT_HASH_MANIFEST_REFS_MISSING,
        "At least one caller-supplied artifact hash manifest ref is "
        "required.",
    ),
    (
        ARTIFACT_REFS_MISSING,
        "At least one caller-supplied artifact ref is required.",
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
        PUBLIC_URL_CREATED_TRUE,
        "MVP noop publish ledger entries require public_url_created to "
        "remain false.",
    ),
    (
        PUBLIC_URL_NON_NULL,
        "MVP noop publish ledger entries require the caller-supplied "
        "public URL null marker to remain true.",
    ),
    (
        PUBLISH_LEDGER_ENTRY_BUILDABLE,
        "The caller-supplied fields can build the Publish Ledger Entry "
        "shape. This does not write publish-ledger.yaml, publish an "
        "artifact, create or return a public URL, send notification, "
        "write a ledger, execute a gate, map or execute a transition, "
        "persist NOOP_COMPLETED, read runtime context, configuration, "
        "credentials, adapter outputs, artifacts, artifact hashes, "
        "reviews or ledgers, call existing policy or builder modules, "
        "or call an external service.",
    ),
)
_VIOLATION_FIELD_ENTRIES: Final[
    tuple[tuple[str, tuple[str, ...]], ...]
] = (
    (RUN_ID_MISSING, ("run_id",)),
    (PUBLISH_ID_MISSING, ("publish_id",)),
    (PUBLISH_MODE_MISSING, ("publish_mode",)),
    (PUBLISH_MODE_NOT_NOOP, ("publish_mode",)),
    (PUBLISH_OUTCOME_MISSING, ("publish_outcome",)),
    (
        PUBLISH_OUTCOME_NOT_NOOP_COMPLETED,
        ("publish_outcome",),
    ),
    (SOURCE_STATE_MISSING, ("source_state",)),
    (SOURCE_STATE_UNKNOWN, ("source_state",)),
    (SOURCE_STATE_NOT_PUBLISH_ALLOWED, ("source_state",)),
    (TARGET_STATE_MISSING, ("target_state",)),
    (TARGET_STATE_UNKNOWN, ("target_state",)),
    (TARGET_STATE_NOT_NOOP_COMPLETED, ("target_state",)),
    (PUBLIC_CANDIDATE_REF_MISSING, ("public_candidate_ref",)),
    (
        GATE_DECISION_ENVELOPE_REFS_MISSING,
        ("gate_decision_envelope_refs",),
    ),
    (
        ARTIFACT_HASH_MANIFEST_REFS_MISSING,
        ("artifact_hash_manifest_refs",),
    ),
    (ARTIFACT_REFS_MISSING, ("artifact_refs",)),
    (REDACTION_STATUS_MISSING, ("redaction_status",)),
    (CREATED_AT_MISSING, ("created_at",)),
    (TIMESTAMP_POLICY_MISSING, ("timestamp_policy",)),
    (SOURCE_OF_TRUTH_MISSING, ("source_of_truth",)),
    (PUBLIC_URL_CREATED_TRUE, ("public_url_created",)),
    (PUBLIC_URL_NON_NULL, ("public_url",)),
)


def _reason_text(reason_code: str) -> str:
    for code, text in _REASON_TEXT_ENTRIES:
        if code == reason_code:
            return text
    return "Unknown Publish Ledger Entry build result."


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
    publish_id: str,
    publish_mode: str,
    publish_outcome: str,
    source_state: str,
    target_state: str,
    public_candidate_ref: str,
    gate_decision_envelope_refs: tuple[str, ...],
    artifact_hash_manifest_refs: tuple[str, ...],
    artifact_refs: tuple[str, ...],
    redaction_status: str,
    public_url_created: bool,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    return {
        "run_id": run_id,
        "publish_id": publish_id,
        "publish_mode": publish_mode,
        "publish_outcome": publish_outcome,
        "source_state": source_state,
        "target_state": target_state,
        "public_candidate_ref": public_candidate_ref,
        "gate_decision_envelope_refs": gate_decision_envelope_refs,
        "artifact_hash_manifest_refs": artifact_hash_manifest_refs,
        "artifact_refs": artifact_refs,
        "redaction_status": redaction_status,
        "public_url_created": public_url_created,
        "public_url": None,
        "created_at": created_at,
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


def explain_publish_ledger_entry_build(
    *,
    run_id: str,
    publish_id: str,
    publish_mode: str,
    publish_outcome: str,
    source_state: str,
    target_state: str,
    public_candidate_ref: str,
    gate_decision_envelope_refs: tuple[str, ...],
    artifact_hash_manifest_refs: tuple[str, ...],
    artifact_refs: tuple[str, ...],
    redaction_status: str,
    public_url_created: bool,
    public_url_is_null: bool,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    """Explain whether caller-supplied fields can build the entry."""
    publish_mode_missing = publish_mode.strip() == ""
    publish_outcome_missing = publish_outcome.strip() == ""
    source_state_missing = source_state.strip() == ""
    source_state_unknown = (
        source_state_missing is False
        and source_state not in states.MVP_STATES
    )
    source_state_not_publish_allowed = (
        source_state_missing is False
        and source_state_unknown is False
        and source_state != states.PUBLISH_ALLOWED
    )
    target_state_missing = target_state.strip() == ""
    target_state_unknown = (
        target_state_missing is False
        and target_state not in states.MVP_STATES
    )
    target_state_not_noop_completed = (
        target_state_missing is False
        and target_state_unknown is False
        and target_state != states.NOOP_COMPLETED
    )
    prioritized_violations = (
        (run_id.strip() == "", RUN_ID_MISSING),
        (publish_id.strip() == "", PUBLISH_ID_MISSING),
        (publish_mode_missing, PUBLISH_MODE_MISSING),
        (
            publish_mode_missing is False
            and publish_mode != _NOOP_PUBLISH_MODE,
            PUBLISH_MODE_NOT_NOOP,
        ),
        (publish_outcome_missing, PUBLISH_OUTCOME_MISSING),
        (
            publish_outcome_missing is False
            and publish_outcome != states.NOOP_COMPLETED,
            PUBLISH_OUTCOME_NOT_NOOP_COMPLETED,
        ),
        (source_state_missing, SOURCE_STATE_MISSING),
        (source_state_unknown, SOURCE_STATE_UNKNOWN),
        (
            source_state_not_publish_allowed,
            SOURCE_STATE_NOT_PUBLISH_ALLOWED,
        ),
        (target_state_missing, TARGET_STATE_MISSING),
        (target_state_unknown, TARGET_STATE_UNKNOWN),
        (
            target_state_not_noop_completed,
            TARGET_STATE_NOT_NOOP_COMPLETED,
        ),
        (
            public_candidate_ref.strip() == "",
            PUBLIC_CANDIDATE_REF_MISSING,
        ),
        (
            gate_decision_envelope_refs == (),
            GATE_DECISION_ENVELOPE_REFS_MISSING,
        ),
        (
            artifact_hash_manifest_refs == (),
            ARTIFACT_HASH_MANIFEST_REFS_MISSING,
        ),
        (artifact_refs == (), ARTIFACT_REFS_MISSING),
        (redaction_status.strip() == "", REDACTION_STATUS_MISSING),
        (created_at.strip() == "", CREATED_AT_MISSING),
        (timestamp_policy.strip() == "", TIMESTAMP_POLICY_MISSING),
        (source_of_truth == (), SOURCE_OF_TRUTH_MISSING),
        (public_url_created is True, PUBLIC_URL_CREATED_TRUE),
        (public_url_is_null is False, PUBLIC_URL_NON_NULL),
    )
    entry_violations = tuple(
        reason_code
        for condition, reason_code in prioritized_violations
        if condition
    )
    buildable = entry_violations == ()
    reason_code = (
        PUBLISH_LEDGER_ENTRY_BUILDABLE
        if buildable
        else entry_violations[0]
    )

    return _result(
        buildable=buildable,
        reason_code=reason_code,
        entry=_entry(
            run_id=run_id,
            publish_id=publish_id,
            publish_mode=publish_mode,
            publish_outcome=publish_outcome,
            source_state=source_state,
            target_state=target_state,
            public_candidate_ref=public_candidate_ref,
            gate_decision_envelope_refs=gate_decision_envelope_refs,
            artifact_hash_manifest_refs=artifact_hash_manifest_refs,
            artifact_refs=artifact_refs,
            redaction_status=redaction_status,
            public_url_created=public_url_created,
            created_at=created_at,
            timestamp_policy=timestamp_policy,
            source_of_truth=source_of_truth,
            notes=notes,
        ),
        entry_violations=entry_violations,
        missing_or_invalid_fields=(
            _missing_or_invalid_fields(entry_violations)
        ),
    )


def is_publish_ledger_entry_buildable(
    *,
    run_id: str,
    publish_id: str,
    publish_mode: str,
    publish_outcome: str,
    source_state: str,
    target_state: str,
    public_candidate_ref: str,
    gate_decision_envelope_refs: tuple[str, ...],
    artifact_hash_manifest_refs: tuple[str, ...],
    artifact_refs: tuple[str, ...],
    redaction_status: str,
    public_url_created: bool,
    public_url_is_null: bool,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> bool:
    """Return only the boolean result from the build explanation."""
    return bool(
        explain_publish_ledger_entry_build(
            run_id=run_id,
            publish_id=publish_id,
            publish_mode=publish_mode,
            publish_outcome=publish_outcome,
            source_state=source_state,
            target_state=target_state,
            public_candidate_ref=public_candidate_ref,
            gate_decision_envelope_refs=gate_decision_envelope_refs,
            artifact_hash_manifest_refs=artifact_hash_manifest_refs,
            artifact_refs=artifact_refs,
            redaction_status=redaction_status,
            public_url_created=public_url_created,
            public_url_is_null=public_url_is_null,
            created_at=created_at,
            timestamp_policy=timestamp_policy,
            source_of_truth=source_of_truth,
            notes=notes,
        )["buildable"]
    )
