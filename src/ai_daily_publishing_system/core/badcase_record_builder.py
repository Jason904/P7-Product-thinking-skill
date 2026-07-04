"""Pure Badcase Record builder for caller-supplied badcase fields."""

from typing import Final

from ai_daily_publishing_system.core import gates, states


BADCASE_RECORD_BUILDABLE: Final[str] = "BADCASE_RECORD_BUILDABLE"
RUN_ID_MISSING: Final[str] = "RUN_ID_MISSING"
BADCASE_ID_MISSING: Final[str] = "BADCASE_ID_MISSING"
SOURCE_STATE_MISSING: Final[str] = "SOURCE_STATE_MISSING"
SOURCE_STATE_UNKNOWN: Final[str] = "SOURCE_STATE_UNKNOWN"
SOURCE_STATE_NOT_BADCASE_ELIGIBLE: Final[str] = (
    "SOURCE_STATE_NOT_BADCASE_ELIGIBLE"
)
BADCASE_KIND_MISSING: Final[str] = "BADCASE_KIND_MISSING"
BADCASE_REASON_CODE_MISSING: Final[str] = (
    "BADCASE_REASON_CODE_MISSING"
)
BADCASE_SUMMARY_MISSING: Final[str] = "BADCASE_SUMMARY_MISSING"
SEVERITY_MISSING: Final[str] = "SEVERITY_MISSING"
FAILURE_PACKAGE_REF_MISSING: Final[str] = (
    "FAILURE_PACKAGE_REF_MISSING"
)
RUN_LEDGER_ENTRY_REF_MISSING: Final[str] = (
    "RUN_LEDGER_ENTRY_REF_MISSING"
)
GATE_DECISION_ENVELOPE_REFS_MISSING: Final[str] = (
    "GATE_DECISION_ENVELOPE_REFS_MISSING"
)
ARTIFACT_REFS_MISSING: Final[str] = "ARTIFACT_REFS_MISSING"
EVIDENCE_REFS_MISSING: Final[str] = "EVIDENCE_REFS_MISSING"
CREATED_AT_MISSING: Final[str] = "CREATED_AT_MISSING"
TIMESTAMP_POLICY_MISSING: Final[str] = "TIMESTAMP_POLICY_MISSING"
SOURCE_OF_TRUTH_MISSING: Final[str] = "SOURCE_OF_TRUTH_MISSING"
PUBLIC_URL_CREATED_TRUE: Final[str] = "PUBLIC_URL_CREATED_TRUE"
PUBLIC_URL_NON_NULL: Final[str] = "PUBLIC_URL_NON_NULL"
ISSUE_REF_WITHOUT_ISSUE_CANDIDATE: Final[str] = (
    "ISSUE_REF_WITHOUT_ISSUE_CANDIDATE"
)

BADCASE_RECORD_BUILD_REASON_CODES: Final[tuple[str, ...]] = (
    RUN_ID_MISSING,
    BADCASE_ID_MISSING,
    SOURCE_STATE_MISSING,
    SOURCE_STATE_UNKNOWN,
    SOURCE_STATE_NOT_BADCASE_ELIGIBLE,
    BADCASE_KIND_MISSING,
    BADCASE_REASON_CODE_MISSING,
    BADCASE_SUMMARY_MISSING,
    SEVERITY_MISSING,
    FAILURE_PACKAGE_REF_MISSING,
    RUN_LEDGER_ENTRY_REF_MISSING,
    GATE_DECISION_ENVELOPE_REFS_MISSING,
    ARTIFACT_REFS_MISSING,
    EVIDENCE_REFS_MISSING,
    CREATED_AT_MISSING,
    TIMESTAMP_POLICY_MISSING,
    SOURCE_OF_TRUTH_MISSING,
    PUBLIC_URL_CREATED_TRUE,
    PUBLIC_URL_NON_NULL,
    ISSUE_REF_WITHOUT_ISSUE_CANDIDATE,
    BADCASE_RECORD_BUILDABLE,
)

_SOURCE: Final[str] = (
    "badcase_record_builder.explain_badcase_record_build"
)
_BADCASE_SOURCE_ELIGIBLE_STATES: Final[tuple[str, ...]] = (
    states.CONFIG_BLOCKED,
    states.REVIEW_BLOCKED,
    states.SYSTEM_FAILED,
    states.ADAPTER_FAILED,
)
_GATE_ENVELOPE_REQUIRED_SOURCE_STATES: Final[tuple[str, ...]] = (
    states.CONFIG_BLOCKED,
    states.REVIEW_BLOCKED,
    states.ADAPTER_FAILED,
)
_LOCAL_INVARIANTS: Final[tuple[str, ...]] = (
    "badcase_record_builder_only",
    "builder_not_badcase_record_writer",
    "builder_not_issue_creator",
    "builder_not_failure_package_writer",
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
    "no_badcase_record_write",
    "no_issue_creation",
    "no_failure_package_write",
    "no_public_url_behavior",
    "no_gate_decision_envelope_builder_call",
    "no_run_ledger_entry_builder_call",
    "no_failure_package_builder_call",
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
        BADCASE_ID_MISSING,
        "A non-empty caller-supplied badcase_id is required.",
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
        SOURCE_STATE_NOT_BADCASE_ELIGIBLE,
        "The caller-supplied source_state is not an eligible original "
        "badcase source.",
    ),
    (
        BADCASE_KIND_MISSING,
        "A non-empty caller-supplied badcase_kind is required.",
    ),
    (
        BADCASE_REASON_CODE_MISSING,
        "A non-empty caller-supplied badcase_reason_code is required.",
    ),
    (
        BADCASE_SUMMARY_MISSING,
        "A non-empty caller-supplied badcase_summary is required.",
    ),
    (
        SEVERITY_MISSING,
        "A non-empty caller-supplied severity marker is required.",
    ),
    (
        FAILURE_PACKAGE_REF_MISSING,
        "A non-empty caller-supplied failure package ref is required.",
    ),
    (
        RUN_LEDGER_ENTRY_REF_MISSING,
        "A non-empty caller-supplied run ledger entry ref is required.",
    ),
    (
        GATE_DECISION_ENVELOPE_REFS_MISSING,
        "This source_state requires at least one caller-supplied gate "
        "decision envelope ref.",
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
        "MVP badcase records require public_url_created to remain false.",
    ),
    (
        PUBLIC_URL_NON_NULL,
        "MVP badcase records require the caller-supplied public URL null "
        "marker to remain true.",
    ),
    (
        ISSUE_REF_WITHOUT_ISSUE_CANDIDATE,
        "issue_ref requires issue_candidate to be true.",
    ),
    (
        BADCASE_RECORD_BUILDABLE,
        "The caller-supplied fields can build the Badcase Record shape. "
        "This does not write badcase-record.yaml, create a GitHub or Ops "
        "issue, write failure-package.yaml, write a run ledger, execute a "
        "gate, map or execute a transition, calculate a hash, publish, "
        "send notification, create or return a public URL, read runtime "
        "context, configuration, credentials, adapter outputs, artifacts, "
        "reviews, hashes or ledgers, call existing policy or builder "
        "modules, or call an external service.",
    ),
)
_VIOLATION_FIELD_ENTRIES: Final[
    tuple[tuple[str, tuple[str, ...]], ...]
] = (
    (RUN_ID_MISSING, ("run_id",)),
    (BADCASE_ID_MISSING, ("badcase_id",)),
    (SOURCE_STATE_MISSING, ("source_state",)),
    (SOURCE_STATE_UNKNOWN, ("source_state",)),
    (
        SOURCE_STATE_NOT_BADCASE_ELIGIBLE,
        ("source_state",),
    ),
    (BADCASE_KIND_MISSING, ("badcase_kind",)),
    (
        BADCASE_REASON_CODE_MISSING,
        ("badcase_reason_code",),
    ),
    (BADCASE_SUMMARY_MISSING, ("badcase_summary",)),
    (SEVERITY_MISSING, ("severity",)),
    (FAILURE_PACKAGE_REF_MISSING, ("failure_package_ref",)),
    (RUN_LEDGER_ENTRY_REF_MISSING, ("run_ledger_entry_ref",)),
    (
        GATE_DECISION_ENVELOPE_REFS_MISSING,
        ("gate_decision_envelope_refs",),
    ),
    (ARTIFACT_REFS_MISSING, ("artifact_refs",)),
    (EVIDENCE_REFS_MISSING, ("evidence_refs",)),
    (CREATED_AT_MISSING, ("created_at",)),
    (TIMESTAMP_POLICY_MISSING, ("timestamp_policy",)),
    (SOURCE_OF_TRUTH_MISSING, ("source_of_truth",)),
    (PUBLIC_URL_CREATED_TRUE, ("public_url_created",)),
    (PUBLIC_URL_NON_NULL, ("public_url",)),
    (
        ISSUE_REF_WITHOUT_ISSUE_CANDIDATE,
        ("issue_ref",),
    ),
)


def _reason_text(reason_code: str) -> str:
    for code, text in _REASON_TEXT_ENTRIES:
        if code == reason_code:
            return text
    return "Unknown Badcase Record build result."


def _ordered_unique(values: tuple[str, ...]) -> tuple[str, ...]:
    ordered_values = ()
    for value in values:
        if value not in ordered_values:
            ordered_values = ordered_values + (value,)
    return ordered_values


def _missing_or_invalid_fields(
    record_violations: tuple[str, ...],
) -> tuple[str, ...]:
    field_names = ()
    for violation in record_violations:
        for reason_code, invalid_fields in _VIOLATION_FIELD_ENTRIES:
            if violation == reason_code:
                field_names = field_names + invalid_fields
    return _ordered_unique(field_names)


def _record(
    *,
    run_id: str,
    badcase_id: str,
    source_state: str,
    badcase_kind: str,
    badcase_reason_code: str,
    badcase_summary: str,
    severity: str,
    failure_package_ref: str,
    run_ledger_entry_ref: str,
    gate_decision_envelope_refs: tuple[str, ...],
    artifact_refs: tuple[str, ...],
    evidence_refs: tuple[str, ...],
    reproduction_refs: tuple[str, ...],
    artifact_hash_refs: tuple[str, ...],
    issue_candidate: bool,
    issue_ref: str,
    public_url_created: bool,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    return {
        "run_id": run_id,
        "badcase_id": badcase_id,
        "source_state": source_state,
        "badcase_kind": badcase_kind,
        "badcase_reason_code": badcase_reason_code,
        "badcase_summary": badcase_summary,
        "severity": severity,
        "failure_package_ref": failure_package_ref,
        "run_ledger_entry_ref": run_ledger_entry_ref,
        "gate_decision_envelope_refs": gate_decision_envelope_refs,
        "artifact_refs": artifact_refs,
        "evidence_refs": evidence_refs,
        "reproduction_refs": reproduction_refs,
        "artifact_hash_refs": artifact_hash_refs,
        "issue_candidate": issue_candidate,
        "issue_ref": issue_ref,
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
    record,
    record_violations: tuple[str, ...],
    missing_or_invalid_fields: tuple[str, ...],
) -> dict[str, object]:
    return {
        "buildable": buildable,
        "reason_code": reason_code,
        "reason": _reason_text(reason_code),
        "source": _SOURCE,
        "record": record,
        "record_violations": record_violations,
        "missing_or_invalid_fields": missing_or_invalid_fields,
        "invariant_refs": _INVARIANTS,
    }


def explain_badcase_record_build(
    *,
    run_id: str,
    badcase_id: str,
    source_state: str,
    badcase_kind: str,
    badcase_reason_code: str,
    badcase_summary: str,
    severity: str,
    failure_package_ref: str,
    run_ledger_entry_ref: str,
    gate_decision_envelope_refs: tuple[str, ...],
    artifact_refs: tuple[str, ...],
    evidence_refs: tuple[str, ...],
    reproduction_refs: tuple[str, ...],
    artifact_hash_refs: tuple[str, ...],
    issue_candidate: bool,
    issue_ref: str,
    public_url_created: bool,
    public_url_is_null: bool,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    """Explain whether caller-supplied fields can build the record."""
    source_state_missing = source_state.strip() == ""
    source_state_unknown = (
        source_state_missing is False
        and source_state not in states.MVP_STATES
    )
    source_state_not_eligible = (
        source_state_missing is False
        and source_state_unknown is False
        and source_state not in _BADCASE_SOURCE_ELIGIBLE_STATES
    )
    gate_envelope_refs_required = (
        source_state in _GATE_ENVELOPE_REQUIRED_SOURCE_STATES
    )
    issue_ref_present = issue_ref.strip() != ""
    prioritized_violations = (
        (run_id.strip() == "", RUN_ID_MISSING),
        (badcase_id.strip() == "", BADCASE_ID_MISSING),
        (source_state_missing, SOURCE_STATE_MISSING),
        (source_state_unknown, SOURCE_STATE_UNKNOWN),
        (
            source_state_not_eligible,
            SOURCE_STATE_NOT_BADCASE_ELIGIBLE,
        ),
        (badcase_kind.strip() == "", BADCASE_KIND_MISSING),
        (
            badcase_reason_code.strip() == "",
            BADCASE_REASON_CODE_MISSING,
        ),
        (badcase_summary.strip() == "", BADCASE_SUMMARY_MISSING),
        (severity.strip() == "", SEVERITY_MISSING),
        (
            failure_package_ref.strip() == "",
            FAILURE_PACKAGE_REF_MISSING,
        ),
        (
            run_ledger_entry_ref.strip() == "",
            RUN_LEDGER_ENTRY_REF_MISSING,
        ),
        (
            gate_envelope_refs_required
            and gate_decision_envelope_refs == (),
            GATE_DECISION_ENVELOPE_REFS_MISSING,
        ),
        (artifact_refs == (), ARTIFACT_REFS_MISSING),
        (evidence_refs == (), EVIDENCE_REFS_MISSING),
        (created_at.strip() == "", CREATED_AT_MISSING),
        (timestamp_policy.strip() == "", TIMESTAMP_POLICY_MISSING),
        (source_of_truth == (), SOURCE_OF_TRUTH_MISSING),
        (public_url_created is True, PUBLIC_URL_CREATED_TRUE),
        (public_url_is_null is False, PUBLIC_URL_NON_NULL),
        (
            issue_candidate is False and issue_ref_present,
            ISSUE_REF_WITHOUT_ISSUE_CANDIDATE,
        ),
    )
    record_violations = tuple(
        reason_code
        for condition, reason_code in prioritized_violations
        if condition
    )
    buildable = record_violations == ()
    reason_code = (
        BADCASE_RECORD_BUILDABLE
        if buildable
        else record_violations[0]
    )

    return _result(
        buildable=buildable,
        reason_code=reason_code,
        record=_record(
            run_id=run_id,
            badcase_id=badcase_id,
            source_state=source_state,
            badcase_kind=badcase_kind,
            badcase_reason_code=badcase_reason_code,
            badcase_summary=badcase_summary,
            severity=severity,
            failure_package_ref=failure_package_ref,
            run_ledger_entry_ref=run_ledger_entry_ref,
            gate_decision_envelope_refs=gate_decision_envelope_refs,
            artifact_refs=artifact_refs,
            evidence_refs=evidence_refs,
            reproduction_refs=reproduction_refs,
            artifact_hash_refs=artifact_hash_refs,
            issue_candidate=issue_candidate,
            issue_ref=issue_ref,
            public_url_created=public_url_created,
            created_at=created_at,
            timestamp_policy=timestamp_policy,
            source_of_truth=source_of_truth,
            notes=notes,
        ),
        record_violations=record_violations,
        missing_or_invalid_fields=(
            _missing_or_invalid_fields(record_violations)
        ),
    )


def is_badcase_record_buildable(
    *,
    run_id: str,
    badcase_id: str,
    source_state: str,
    badcase_kind: str,
    badcase_reason_code: str,
    badcase_summary: str,
    severity: str,
    failure_package_ref: str,
    run_ledger_entry_ref: str,
    gate_decision_envelope_refs: tuple[str, ...],
    artifact_refs: tuple[str, ...],
    evidence_refs: tuple[str, ...],
    reproduction_refs: tuple[str, ...],
    artifact_hash_refs: tuple[str, ...],
    issue_candidate: bool,
    issue_ref: str,
    public_url_created: bool,
    public_url_is_null: bool,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> bool:
    """Return only the boolean result from the build explanation."""
    return bool(
        explain_badcase_record_build(
            run_id=run_id,
            badcase_id=badcase_id,
            source_state=source_state,
            badcase_kind=badcase_kind,
            badcase_reason_code=badcase_reason_code,
            badcase_summary=badcase_summary,
            severity=severity,
            failure_package_ref=failure_package_ref,
            run_ledger_entry_ref=run_ledger_entry_ref,
            gate_decision_envelope_refs=gate_decision_envelope_refs,
            artifact_refs=artifact_refs,
            evidence_refs=evidence_refs,
            reproduction_refs=reproduction_refs,
            artifact_hash_refs=artifact_hash_refs,
            issue_candidate=issue_candidate,
            issue_ref=issue_ref,
            public_url_created=public_url_created,
            public_url_is_null=public_url_is_null,
            created_at=created_at,
            timestamp_policy=timestamp_policy,
            source_of_truth=source_of_truth,
            notes=notes,
        )["buildable"]
    )
