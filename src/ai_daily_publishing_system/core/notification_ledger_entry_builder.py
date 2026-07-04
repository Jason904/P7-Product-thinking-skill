"""Pure Notification Ledger Entry builder for caller-supplied noop fields."""

from typing import Final

from ai_daily_publishing_system.core import states


NOTIFICATION_LEDGER_ENTRY_BUILDABLE: Final[str] = (
    "NOTIFICATION_LEDGER_ENTRY_BUILDABLE"
)
RUN_ID_MISSING: Final[str] = "RUN_ID_MISSING"
NOTIFICATION_ID_MISSING: Final[str] = "NOTIFICATION_ID_MISSING"
NOTIFICATION_MODE_MISSING: Final[str] = "NOTIFICATION_MODE_MISSING"
NOTIFICATION_MODE_NOT_NOOP: Final[str] = "NOTIFICATION_MODE_NOT_NOOP"
NOTIFICATION_OUTCOME_MISSING: Final[str] = (
    "NOTIFICATION_OUTCOME_MISSING"
)
NOTIFICATION_OUTCOME_NOT_NOOP_SKIPPED: Final[str] = (
    "NOTIFICATION_OUTCOME_NOT_NOOP_SKIPPED"
)
RUN_STATE_MISSING: Final[str] = "RUN_STATE_MISSING"
RUN_STATE_UNKNOWN: Final[str] = "RUN_STATE_UNKNOWN"
RUN_STATE_NOT_NOOP_COMPLETED: Final[str] = (
    "RUN_STATE_NOT_NOOP_COMPLETED"
)
PUBLISH_LEDGER_ENTRY_REFS_MISSING: Final[str] = (
    "PUBLISH_LEDGER_ENTRY_REFS_MISSING"
)
GATE_DECISION_ENVELOPE_REFS_MISSING: Final[str] = (
    "GATE_DECISION_ENVELOPE_REFS_MISSING"
)
ARTIFACT_HASH_MANIFEST_REFS_MISSING: Final[str] = (
    "ARTIFACT_HASH_MANIFEST_REFS_MISSING"
)
ARTIFACT_REFS_MISSING: Final[str] = "ARTIFACT_REFS_MISSING"
REDACTION_STATUS_MISSING: Final[str] = "REDACTION_STATUS_MISSING"
NOTIFICATION_SENT_TRUE: Final[str] = "NOTIFICATION_SENT_TRUE"
EXTERNAL_NOTIFICATION_CREATED_TRUE: Final[str] = (
    "EXTERNAL_NOTIFICATION_CREATED_TRUE"
)
CREATED_AT_MISSING: Final[str] = "CREATED_AT_MISSING"
TIMESTAMP_POLICY_MISSING: Final[str] = "TIMESTAMP_POLICY_MISSING"
SOURCE_OF_TRUTH_MISSING: Final[str] = "SOURCE_OF_TRUTH_MISSING"
PUBLIC_URL_CREATED_TRUE: Final[str] = "PUBLIC_URL_CREATED_TRUE"
PUBLIC_URL_NON_NULL: Final[str] = "PUBLIC_URL_NON_NULL"

NOTIFICATION_LEDGER_ENTRY_BUILD_REASON_CODES: Final[
    tuple[str, ...]
] = (
    RUN_ID_MISSING,
    NOTIFICATION_ID_MISSING,
    NOTIFICATION_MODE_MISSING,
    NOTIFICATION_MODE_NOT_NOOP,
    NOTIFICATION_OUTCOME_MISSING,
    NOTIFICATION_OUTCOME_NOT_NOOP_SKIPPED,
    RUN_STATE_MISSING,
    RUN_STATE_UNKNOWN,
    RUN_STATE_NOT_NOOP_COMPLETED,
    PUBLISH_LEDGER_ENTRY_REFS_MISSING,
    GATE_DECISION_ENVELOPE_REFS_MISSING,
    ARTIFACT_HASH_MANIFEST_REFS_MISSING,
    ARTIFACT_REFS_MISSING,
    REDACTION_STATUS_MISSING,
    NOTIFICATION_SENT_TRUE,
    EXTERNAL_NOTIFICATION_CREATED_TRUE,
    CREATED_AT_MISSING,
    TIMESTAMP_POLICY_MISSING,
    SOURCE_OF_TRUTH_MISSING,
    PUBLIC_URL_CREATED_TRUE,
    PUBLIC_URL_NON_NULL,
    NOTIFICATION_LEDGER_ENTRY_BUILDABLE,
)

_SOURCE: Final[str] = (
    "notification_ledger_entry_builder."
    "explain_notification_ledger_entry_build"
)
_NOOP_NOTIFICATION_MODE: Final[str] = "noop"
_NOOP_NOTIFICATION_OUTCOME: Final[str] = "NOOP_NOTIFICATION_SKIPPED"
_PASS_PUBLISHED_LABEL: Final[str] = "PASS_PUBLISHED"
_LOCAL_INVARIANTS: Final[tuple[str, ...]] = (
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
        NOTIFICATION_ID_MISSING,
        "A non-empty caller-supplied notification_id is required.",
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
        NOTIFICATION_OUTCOME_MISSING,
        "A non-empty caller-supplied notification_outcome is required.",
    ),
    (
        NOTIFICATION_OUTCOME_NOT_NOOP_SKIPPED,
        "The caller-supplied notification_outcome must be "
        f"{_NOOP_NOTIFICATION_OUTCOME}; "
        f"{_PASS_PUBLISHED_LABEL} remains forbidden.",
    ),
    (
        RUN_STATE_MISSING,
        "A non-empty caller-supplied run_state is required.",
    ),
    (
        RUN_STATE_UNKNOWN,
        "The caller-supplied run_state is not declared in "
        "states.MVP_STATES.",
    ),
    (
        RUN_STATE_NOT_NOOP_COMPLETED,
        "The caller-supplied run_state must be NOOP_COMPLETED.",
    ),
    (
        PUBLISH_LEDGER_ENTRY_REFS_MISSING,
        "At least one caller-supplied publish ledger entry ref is "
        "required.",
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
        NOTIFICATION_SENT_TRUE,
        "MVP noop notification ledger entries require "
        "notification_sent to remain false.",
    ),
    (
        EXTERNAL_NOTIFICATION_CREATED_TRUE,
        "MVP noop notification ledger entries require "
        "external_notification_created to remain false.",
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
        "MVP noop notification ledger entries require "
        "public_url_created to remain false.",
    ),
    (
        PUBLIC_URL_NON_NULL,
        "MVP noop notification ledger entries require the "
        "caller-supplied public URL null marker to remain true.",
    ),
    (
        NOTIFICATION_LEDGER_ENTRY_BUILDABLE,
        "The caller-supplied fields can build the Notification "
        "Ledger Entry shape. This does not write "
        "notification-ledger.yaml, send a notification, create or "
        "return a public URL, read publish-ledger.yaml, read "
        "artifact-hash.yaml, write a ledger, execute a gate, map or "
        "execute a transition, persist NOOP_COMPLETED, read runtime "
        "context, configuration, credentials, contacts, notification "
        "targets, adapter outputs, artifacts, reviews or ledgers, "
        "call existing policy or builder modules, publish, or call an "
        "external service.",
    ),
)
_VIOLATION_FIELD_ENTRIES: Final[
    tuple[tuple[str, tuple[str, ...]], ...]
] = (
    (RUN_ID_MISSING, ("run_id",)),
    (NOTIFICATION_ID_MISSING, ("notification_id",)),
    (NOTIFICATION_MODE_MISSING, ("notification_mode",)),
    (NOTIFICATION_MODE_NOT_NOOP, ("notification_mode",)),
    (NOTIFICATION_OUTCOME_MISSING, ("notification_outcome",)),
    (
        NOTIFICATION_OUTCOME_NOT_NOOP_SKIPPED,
        ("notification_outcome",),
    ),
    (RUN_STATE_MISSING, ("run_state",)),
    (RUN_STATE_UNKNOWN, ("run_state",)),
    (RUN_STATE_NOT_NOOP_COMPLETED, ("run_state",)),
    (
        PUBLISH_LEDGER_ENTRY_REFS_MISSING,
        ("publish_ledger_entry_refs",),
    ),
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
    (NOTIFICATION_SENT_TRUE, ("notification_sent",)),
    (
        EXTERNAL_NOTIFICATION_CREATED_TRUE,
        ("external_notification_created",),
    ),
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
    return "Unknown Notification Ledger Entry build result."


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
    notification_id: str,
    notification_mode: str,
    notification_outcome: str,
    run_state: str,
    publish_ledger_entry_refs: tuple[str, ...],
    gate_decision_envelope_refs: tuple[str, ...],
    artifact_hash_manifest_refs: tuple[str, ...],
    artifact_refs: tuple[str, ...],
    redaction_status: str,
    notification_sent: bool,
    external_notification_created: bool,
    public_url_created: bool,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    return {
        "run_id": run_id,
        "notification_id": notification_id,
        "notification_mode": notification_mode,
        "notification_outcome": notification_outcome,
        "run_state": run_state,
        "publish_ledger_entry_refs": publish_ledger_entry_refs,
        "gate_decision_envelope_refs": gate_decision_envelope_refs,
        "artifact_hash_manifest_refs": artifact_hash_manifest_refs,
        "artifact_refs": artifact_refs,
        "redaction_status": redaction_status,
        "notification_sent": notification_sent,
        "external_notification_created": external_notification_created,
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


def explain_notification_ledger_entry_build(
    *,
    run_id: str,
    notification_id: str,
    notification_mode: str,
    notification_outcome: str,
    run_state: str,
    publish_ledger_entry_refs: tuple[str, ...],
    gate_decision_envelope_refs: tuple[str, ...],
    artifact_hash_manifest_refs: tuple[str, ...],
    artifact_refs: tuple[str, ...],
    redaction_status: str,
    notification_sent: bool,
    external_notification_created: bool,
    public_url_created: bool,
    public_url_is_null: bool,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    """Explain whether caller-supplied fields can build the entry."""
    notification_mode_missing = notification_mode.strip() == ""
    notification_outcome_missing = notification_outcome.strip() == ""
    run_state_missing = run_state.strip() == ""
    run_state_unknown = (
        run_state_missing is False
        and run_state not in states.MVP_STATES
    )
    run_state_not_noop_completed = (
        run_state_missing is False
        and run_state_unknown is False
        and run_state != states.NOOP_COMPLETED
    )
    prioritized_violations = (
        (run_id.strip() == "", RUN_ID_MISSING),
        (notification_id.strip() == "", NOTIFICATION_ID_MISSING),
        (notification_mode_missing, NOTIFICATION_MODE_MISSING),
        (
            notification_mode_missing is False
            and notification_mode != _NOOP_NOTIFICATION_MODE,
            NOTIFICATION_MODE_NOT_NOOP,
        ),
        (notification_outcome_missing, NOTIFICATION_OUTCOME_MISSING),
        (
            notification_outcome_missing is False
            and notification_outcome != _NOOP_NOTIFICATION_OUTCOME,
            NOTIFICATION_OUTCOME_NOT_NOOP_SKIPPED,
        ),
        (run_state_missing, RUN_STATE_MISSING),
        (run_state_unknown, RUN_STATE_UNKNOWN),
        (
            run_state_not_noop_completed,
            RUN_STATE_NOT_NOOP_COMPLETED,
        ),
        (
            publish_ledger_entry_refs == (),
            PUBLISH_LEDGER_ENTRY_REFS_MISSING,
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
        (notification_sent is True, NOTIFICATION_SENT_TRUE),
        (
            external_notification_created is True,
            EXTERNAL_NOTIFICATION_CREATED_TRUE,
        ),
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
        NOTIFICATION_LEDGER_ENTRY_BUILDABLE
        if buildable
        else entry_violations[0]
    )

    return _result(
        buildable=buildable,
        reason_code=reason_code,
        entry=_entry(
            run_id=run_id,
            notification_id=notification_id,
            notification_mode=notification_mode,
            notification_outcome=notification_outcome,
            run_state=run_state,
            publish_ledger_entry_refs=publish_ledger_entry_refs,
            gate_decision_envelope_refs=gate_decision_envelope_refs,
            artifact_hash_manifest_refs=artifact_hash_manifest_refs,
            artifact_refs=artifact_refs,
            redaction_status=redaction_status,
            notification_sent=notification_sent,
            external_notification_created=external_notification_created,
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


def is_notification_ledger_entry_buildable(
    *,
    run_id: str,
    notification_id: str,
    notification_mode: str,
    notification_outcome: str,
    run_state: str,
    publish_ledger_entry_refs: tuple[str, ...],
    gate_decision_envelope_refs: tuple[str, ...],
    artifact_hash_manifest_refs: tuple[str, ...],
    artifact_refs: tuple[str, ...],
    redaction_status: str,
    notification_sent: bool,
    external_notification_created: bool,
    public_url_created: bool,
    public_url_is_null: bool,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> bool:
    """Return only the boolean result from the build explanation."""
    return bool(
        explain_notification_ledger_entry_build(
            run_id=run_id,
            notification_id=notification_id,
            notification_mode=notification_mode,
            notification_outcome=notification_outcome,
            run_state=run_state,
            publish_ledger_entry_refs=publish_ledger_entry_refs,
            gate_decision_envelope_refs=gate_decision_envelope_refs,
            artifact_hash_manifest_refs=artifact_hash_manifest_refs,
            artifact_refs=artifact_refs,
            redaction_status=redaction_status,
            notification_sent=notification_sent,
            external_notification_created=external_notification_created,
            public_url_created=public_url_created,
            public_url_is_null=public_url_is_null,
            created_at=created_at,
            timestamp_policy=timestamp_policy,
            source_of_truth=source_of_truth,
            notes=notes,
        )["buildable"]
    )
