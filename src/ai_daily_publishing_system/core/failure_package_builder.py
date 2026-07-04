"""Pure Failure Package builder for caller-supplied failure fields."""

from typing import Final

from ai_daily_publishing_system.core import gates, states


FAILURE_PACKAGE_BUILDABLE: Final[str] = "FAILURE_PACKAGE_BUILDABLE"
RUN_ID_MISSING: Final[str] = "RUN_ID_MISSING"
FAILURE_ID_MISSING: Final[str] = "FAILURE_ID_MISSING"
FAILED_STATE_MISSING: Final[str] = "FAILED_STATE_MISSING"
FAILED_STATE_UNKNOWN: Final[str] = "FAILED_STATE_UNKNOWN"
FAILED_STATE_NOT_FAILURE_PACKAGE_ELIGIBLE: Final[str] = (
    "FAILED_STATE_NOT_FAILURE_PACKAGE_ELIGIBLE"
)
FAILURE_KIND_MISSING: Final[str] = "FAILURE_KIND_MISSING"
FAILURE_REASON_CODE_MISSING: Final[str] = "FAILURE_REASON_CODE_MISSING"
FAILURE_SUMMARY_MISSING: Final[str] = "FAILURE_SUMMARY_MISSING"
BLOCKING_REASONS_MISSING: Final[str] = "BLOCKING_REASONS_MISSING"
GATE_DECISION_ENVELOPE_REFS_MISSING: Final[str] = (
    "GATE_DECISION_ENVELOPE_REFS_MISSING"
)
RUN_LEDGER_ENTRY_REF_MISSING: Final[str] = (
    "RUN_LEDGER_ENTRY_REF_MISSING"
)
ARTIFACT_REFS_MISSING: Final[str] = "ARTIFACT_REFS_MISSING"
EVIDENCE_REFS_MISSING: Final[str] = "EVIDENCE_REFS_MISSING"
REDACTION_STATUS_MISSING: Final[str] = "REDACTION_STATUS_MISSING"
CREATED_AT_MISSING: Final[str] = "CREATED_AT_MISSING"
TIMESTAMP_POLICY_MISSING: Final[str] = "TIMESTAMP_POLICY_MISSING"
SOURCE_OF_TRUTH_MISSING: Final[str] = "SOURCE_OF_TRUTH_MISSING"
PUBLIC_URL_CREATED_TRUE: Final[str] = "PUBLIC_URL_CREATED_TRUE"
PUBLIC_URL_NON_NULL: Final[str] = "PUBLIC_URL_NON_NULL"
BADCASE_REF_WITHOUT_BADCASE_CANDIDATE: Final[str] = (
    "BADCASE_REF_WITHOUT_BADCASE_CANDIDATE"
)

FAILURE_PACKAGE_BUILD_REASON_CODES: Final[tuple[str, ...]] = (
    RUN_ID_MISSING,
    FAILURE_ID_MISSING,
    FAILED_STATE_MISSING,
    FAILED_STATE_UNKNOWN,
    FAILED_STATE_NOT_FAILURE_PACKAGE_ELIGIBLE,
    FAILURE_KIND_MISSING,
    FAILURE_REASON_CODE_MISSING,
    FAILURE_SUMMARY_MISSING,
    BLOCKING_REASONS_MISSING,
    GATE_DECISION_ENVELOPE_REFS_MISSING,
    RUN_LEDGER_ENTRY_REF_MISSING,
    ARTIFACT_REFS_MISSING,
    EVIDENCE_REFS_MISSING,
    REDACTION_STATUS_MISSING,
    CREATED_AT_MISSING,
    TIMESTAMP_POLICY_MISSING,
    SOURCE_OF_TRUTH_MISSING,
    PUBLIC_URL_CREATED_TRUE,
    PUBLIC_URL_NON_NULL,
    BADCASE_REF_WITHOUT_BADCASE_CANDIDATE,
    FAILURE_PACKAGE_BUILDABLE,
)

_SOURCE: Final[str] = (
    "failure_package_builder.explain_failure_package_build"
)
_FAILURE_PACKAGE_ELIGIBLE_STATES: Final[tuple[str, ...]] = (
    states.CONFIG_BLOCKED,
    states.REVIEW_BLOCKED,
    states.SYSTEM_FAILED,
    states.ADAPTER_FAILED,
)
_GATE_ENVELOPE_REQUIRED_FAILURE_STATES: Final[tuple[str, ...]] = (
    states.CONFIG_BLOCKED,
    states.REVIEW_BLOCKED,
    states.ADAPTER_FAILED,
)
_LOCAL_INVARIANTS: Final[tuple[str, ...]] = (
    "failure_package_builder_only",
    "builder_not_failure_package_writer",
    "builder_not_badcase_record_writer",
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
    "no_failure_package_write",
    "no_badcase_record_write",
    "no_public_url_behavior",
    "no_gate_decision_envelope_builder_call",
    "no_run_ledger_entry_builder_call",
    "no_badcase_creation_policy_call",
)
_INVARIANTS: Final[tuple[str, ...]] = (
    states.STATE_INVARIANTS
    + gates.GATE_INVARIANTS
    + _LOCAL_INVARIANTS
)
_REASON_TEXT_ENTRIES: Final[tuple[tuple[str, str], ...]] = (
    (
        RUN_ID_MISSING,
        "A non-empty caller-supplied run_id is required.",
    ),
    (
        FAILURE_ID_MISSING,
        "A non-empty caller-supplied failure_id is required.",
    ),
    (
        FAILED_STATE_MISSING,
        "A non-empty caller-supplied failed_state is required.",
    ),
    (
        FAILED_STATE_UNKNOWN,
        "The caller-supplied failed_state is not declared in "
        "states.MVP_STATES.",
    ),
    (
        FAILED_STATE_NOT_FAILURE_PACKAGE_ELIGIBLE,
        "The caller-supplied failed_state is not an eligible original "
        "failure source.",
    ),
    (
        FAILURE_KIND_MISSING,
        "A non-empty caller-supplied failure_kind is required.",
    ),
    (
        FAILURE_REASON_CODE_MISSING,
        "A non-empty caller-supplied failure_reason_code is required.",
    ),
    (
        FAILURE_SUMMARY_MISSING,
        "A non-empty caller-supplied failure_summary is required.",
    ),
    (
        BLOCKING_REASONS_MISSING,
        "At least one caller-supplied blocking reason is required.",
    ),
    (
        GATE_DECISION_ENVELOPE_REFS_MISSING,
        "This failed_state requires at least one caller-supplied gate "
        "decision envelope ref.",
    ),
    (
        RUN_LEDGER_ENTRY_REF_MISSING,
        "A non-empty caller-supplied run ledger entry ref is required.",
    ),
    (
        ARTIFACT_REFS_MISSING,
        "At least one caller-supplied artifact ref is required.",
    ),
    (
        EVIDENCE_REFS_MISSING,
        "At least one caller-supplied evidence ref is required.",
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
        "At least one caller-supplied source_of_truth reference is required.",
    ),
    (
        PUBLIC_URL_CREATED_TRUE,
        "MVP failure packages require public_url_created to remain false.",
    ),
    (
        PUBLIC_URL_NON_NULL,
        "MVP failure packages require the caller-supplied public URL null "
        "marker to remain true.",
    ),
    (
        BADCASE_REF_WITHOUT_BADCASE_CANDIDATE,
        "badcase_record_ref requires badcase_candidate to be true.",
    ),
    (
        FAILURE_PACKAGE_BUILDABLE,
        "The caller-supplied fields can build the Failure Package shape. "
        "This does not write failure-package.yaml, create or write a "
        "badcase record, write a run ledger, execute a gate, map or execute "
        "a transition, calculate a hash, publish, send notification, create "
        "or return a public URL, read runtime context, configuration, "
        "credentials, adapter outputs, artifacts, reviews, hashes or "
        "ledgers, call existing policy or builder modules, or call an "
        "external service.",
    ),
)
_VIOLATION_FIELD_ENTRIES: Final[
    tuple[tuple[str, tuple[str, ...]], ...]
] = (
    (RUN_ID_MISSING, ("run_id",)),
    (FAILURE_ID_MISSING, ("failure_id",)),
    (FAILED_STATE_MISSING, ("failed_state",)),
    (FAILED_STATE_UNKNOWN, ("failed_state",)),
    (
        FAILED_STATE_NOT_FAILURE_PACKAGE_ELIGIBLE,
        ("failed_state",),
    ),
    (FAILURE_KIND_MISSING, ("failure_kind",)),
    (FAILURE_REASON_CODE_MISSING, ("failure_reason_code",)),
    (FAILURE_SUMMARY_MISSING, ("failure_summary",)),
    (BLOCKING_REASONS_MISSING, ("blocking_reasons",)),
    (
        GATE_DECISION_ENVELOPE_REFS_MISSING,
        ("gate_decision_envelope_refs",),
    ),
    (RUN_LEDGER_ENTRY_REF_MISSING, ("run_ledger_entry_ref",)),
    (ARTIFACT_REFS_MISSING, ("artifact_refs",)),
    (EVIDENCE_REFS_MISSING, ("evidence_refs",)),
    (REDACTION_STATUS_MISSING, ("redaction_status",)),
    (CREATED_AT_MISSING, ("created_at",)),
    (TIMESTAMP_POLICY_MISSING, ("timestamp_policy",)),
    (SOURCE_OF_TRUTH_MISSING, ("source_of_truth",)),
    (PUBLIC_URL_CREATED_TRUE, ("public_url_created",)),
    (PUBLIC_URL_NON_NULL, ("public_url",)),
    (
        BADCASE_REF_WITHOUT_BADCASE_CANDIDATE,
        ("badcase_record_ref",),
    ),
)


def _reason_text(reason_code: str) -> str:
    for code, text in _REASON_TEXT_ENTRIES:
        if code == reason_code:
            return text
    return "Unknown Failure Package build result."


def _ordered_unique(values: tuple[str, ...]) -> tuple[str, ...]:
    ordered_values = ()
    for value in values:
        if value not in ordered_values:
            ordered_values = ordered_values + (value,)
    return ordered_values


def _missing_or_invalid_fields(
    package_violations: tuple[str, ...],
) -> tuple[str, ...]:
    field_names = ()
    for violation in package_violations:
        for reason_code, invalid_fields in _VIOLATION_FIELD_ENTRIES:
            if violation == reason_code:
                field_names = field_names + invalid_fields
    return _ordered_unique(field_names)


def _package(
    *,
    run_id: str,
    failure_id: str,
    failed_state: str,
    failure_kind: str,
    failure_reason_code: str,
    failure_summary: str,
    blocking_reasons: tuple[str, ...],
    missing_inputs: tuple[str, ...],
    gate_decision_envelope_refs: tuple[str, ...],
    run_ledger_entry_ref: str,
    artifact_refs: tuple[str, ...],
    evidence_refs: tuple[str, ...],
    artifact_hash_refs: tuple[str, ...],
    redaction_status: str,
    public_url_created: bool,
    badcase_candidate: bool,
    badcase_record_ref: str,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    return {
        "run_id": run_id,
        "failure_id": failure_id,
        "failed_state": failed_state,
        "failure_kind": failure_kind,
        "failure_reason_code": failure_reason_code,
        "failure_summary": failure_summary,
        "blocking_reasons": blocking_reasons,
        "missing_inputs": missing_inputs,
        "gate_decision_envelope_refs": gate_decision_envelope_refs,
        "run_ledger_entry_ref": run_ledger_entry_ref,
        "artifact_refs": artifact_refs,
        "evidence_refs": evidence_refs,
        "artifact_hash_refs": artifact_hash_refs,
        "redaction_status": redaction_status,
        "public_url_created": public_url_created,
        "public_url": None,
        "badcase_candidate": badcase_candidate,
        "badcase_record_ref": badcase_record_ref,
        "created_at": created_at,
        "timestamp_policy": timestamp_policy,
        "source_of_truth": source_of_truth,
        "notes": notes,
    }


def _result(
    *,
    buildable: bool,
    reason_code: str,
    package,
    package_violations: tuple[str, ...],
    missing_or_invalid_fields: tuple[str, ...],
) -> dict[str, object]:
    return {
        "buildable": buildable,
        "reason_code": reason_code,
        "reason": _reason_text(reason_code),
        "source": _SOURCE,
        "package": package,
        "package_violations": package_violations,
        "missing_or_invalid_fields": missing_or_invalid_fields,
        "invariant_refs": _INVARIANTS,
    }


def explain_failure_package_build(
    *,
    run_id: str,
    failure_id: str,
    failed_state: str,
    failure_kind: str,
    failure_reason_code: str,
    failure_summary: str,
    blocking_reasons: tuple[str, ...],
    missing_inputs: tuple[str, ...],
    gate_decision_envelope_refs: tuple[str, ...],
    run_ledger_entry_ref: str,
    artifact_refs: tuple[str, ...],
    evidence_refs: tuple[str, ...],
    artifact_hash_refs: tuple[str, ...],
    redaction_status: str,
    public_url_created: bool,
    public_url_is_null: bool,
    badcase_candidate: bool,
    badcase_record_ref: str,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    """Explain whether caller-supplied fields can build the package."""
    failed_state_missing = failed_state.strip() == ""
    failed_state_unknown = (
        failed_state_missing is False
        and failed_state not in states.MVP_STATES
    )
    failed_state_not_eligible = (
        failed_state_missing is False
        and failed_state_unknown is False
        and failed_state not in _FAILURE_PACKAGE_ELIGIBLE_STATES
    )
    gate_envelope_refs_required = (
        failed_state in _GATE_ENVELOPE_REQUIRED_FAILURE_STATES
    )
    badcase_record_ref_present = badcase_record_ref.strip() != ""
    prioritized_violations = (
        (run_id.strip() == "", RUN_ID_MISSING),
        (failure_id.strip() == "", FAILURE_ID_MISSING),
        (failed_state_missing, FAILED_STATE_MISSING),
        (failed_state_unknown, FAILED_STATE_UNKNOWN),
        (
            failed_state_not_eligible,
            FAILED_STATE_NOT_FAILURE_PACKAGE_ELIGIBLE,
        ),
        (failure_kind.strip() == "", FAILURE_KIND_MISSING),
        (
            failure_reason_code.strip() == "",
            FAILURE_REASON_CODE_MISSING,
        ),
        (failure_summary.strip() == "", FAILURE_SUMMARY_MISSING),
        (blocking_reasons == (), BLOCKING_REASONS_MISSING),
        (
            gate_envelope_refs_required
            and gate_decision_envelope_refs == (),
            GATE_DECISION_ENVELOPE_REFS_MISSING,
        ),
        (
            run_ledger_entry_ref.strip() == "",
            RUN_LEDGER_ENTRY_REF_MISSING,
        ),
        (artifact_refs == (), ARTIFACT_REFS_MISSING),
        (evidence_refs == (), EVIDENCE_REFS_MISSING),
        (redaction_status.strip() == "", REDACTION_STATUS_MISSING),
        (created_at.strip() == "", CREATED_AT_MISSING),
        (timestamp_policy.strip() == "", TIMESTAMP_POLICY_MISSING),
        (source_of_truth == (), SOURCE_OF_TRUTH_MISSING),
        (public_url_created is True, PUBLIC_URL_CREATED_TRUE),
        (public_url_is_null is False, PUBLIC_URL_NON_NULL),
        (
            badcase_candidate is False and badcase_record_ref_present,
            BADCASE_REF_WITHOUT_BADCASE_CANDIDATE,
        ),
    )
    package_violations = tuple(
        reason_code
        for condition, reason_code in prioritized_violations
        if condition
    )
    buildable = package_violations == ()
    reason_code = (
        FAILURE_PACKAGE_BUILDABLE
        if buildable
        else package_violations[0]
    )

    return _result(
        buildable=buildable,
        reason_code=reason_code,
        package=_package(
            run_id=run_id,
            failure_id=failure_id,
            failed_state=failed_state,
            failure_kind=failure_kind,
            failure_reason_code=failure_reason_code,
            failure_summary=failure_summary,
            blocking_reasons=blocking_reasons,
            missing_inputs=missing_inputs,
            gate_decision_envelope_refs=gate_decision_envelope_refs,
            run_ledger_entry_ref=run_ledger_entry_ref,
            artifact_refs=artifact_refs,
            evidence_refs=evidence_refs,
            artifact_hash_refs=artifact_hash_refs,
            redaction_status=redaction_status,
            public_url_created=public_url_created,
            badcase_candidate=badcase_candidate,
            badcase_record_ref=badcase_record_ref,
            created_at=created_at,
            timestamp_policy=timestamp_policy,
            source_of_truth=source_of_truth,
            notes=notes,
        ),
        package_violations=package_violations,
        missing_or_invalid_fields=(
            _missing_or_invalid_fields(package_violations)
        ),
    )


def is_failure_package_buildable(
    *,
    run_id: str,
    failure_id: str,
    failed_state: str,
    failure_kind: str,
    failure_reason_code: str,
    failure_summary: str,
    blocking_reasons: tuple[str, ...],
    missing_inputs: tuple[str, ...],
    gate_decision_envelope_refs: tuple[str, ...],
    run_ledger_entry_ref: str,
    artifact_refs: tuple[str, ...],
    evidence_refs: tuple[str, ...],
    artifact_hash_refs: tuple[str, ...],
    redaction_status: str,
    public_url_created: bool,
    public_url_is_null: bool,
    badcase_candidate: bool,
    badcase_record_ref: str,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> bool:
    """Return only the boolean result from the build explanation."""
    return bool(
        explain_failure_package_build(
            run_id=run_id,
            failure_id=failure_id,
            failed_state=failed_state,
            failure_kind=failure_kind,
            failure_reason_code=failure_reason_code,
            failure_summary=failure_summary,
            blocking_reasons=blocking_reasons,
            missing_inputs=missing_inputs,
            gate_decision_envelope_refs=gate_decision_envelope_refs,
            run_ledger_entry_ref=run_ledger_entry_ref,
            artifact_refs=artifact_refs,
            evidence_refs=evidence_refs,
            artifact_hash_refs=artifact_hash_refs,
            redaction_status=redaction_status,
            public_url_created=public_url_created,
            public_url_is_null=public_url_is_null,
            badcase_candidate=badcase_candidate,
            badcase_record_ref=badcase_record_ref,
            created_at=created_at,
            timestamp_policy=timestamp_policy,
            source_of_truth=source_of_truth,
            notes=notes,
        )["buildable"]
    )
