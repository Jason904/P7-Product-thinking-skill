"""Pure Shared Gate Decision Envelope builder for gate decision records."""

from typing import Final

from ai_daily_publishing_system.core import gates


GATE_DECISION_ENVELOPE_BUILDABLE: Final[str] = (
    "GATE_DECISION_ENVELOPE_BUILDABLE"
)
RUN_ID_MISSING: Final[str] = "RUN_ID_MISSING"
GATE_NAME_MISSING: Final[str] = "GATE_NAME_MISSING"
GATE_NAME_UNKNOWN: Final[str] = "GATE_NAME_UNKNOWN"
DECISION_MISSING: Final[str] = "DECISION_MISSING"
DECISION_UNKNOWN: Final[str] = "DECISION_UNKNOWN"
FROM_STATE_MISSING: Final[str] = "FROM_STATE_MISSING"
TO_STATE_MISSING: Final[str] = "TO_STATE_MISSING"
REASON_CODES_MISSING: Final[str] = "REASON_CODES_MISSING"
SOURCE_OF_TRUTH_MISSING: Final[str] = "SOURCE_OF_TRUTH_MISSING"
CHECKED_AT_MISSING: Final[str] = "CHECKED_AT_MISSING"
TIMESTAMP_POLICY_MISSING: Final[str] = "TIMESTAMP_POLICY_MISSING"
REDACTION_STATUS_MISSING: Final[str] = "REDACTION_STATUS_MISSING"
REQUIRED_INPUTS_PRESENT_WITH_MISSING_INPUTS: Final[str] = (
    "REQUIRED_INPUTS_PRESENT_WITH_MISSING_INPUTS"
)
REQUIRED_INPUTS_MISSING_WITHOUT_MISSING_INPUTS: Final[str] = (
    "REQUIRED_INPUTS_MISSING_WITHOUT_MISSING_INPUTS"
)
PASS_WITH_BLOCKING_REASONS: Final[str] = "PASS_WITH_BLOCKING_REASONS"
BLOCKED_WITHOUT_BLOCKING_REASONS: Final[str] = (
    "BLOCKED_WITHOUT_BLOCKING_REASONS"
)
PUBLIC_URL_CREATED_TRUE: Final[str] = "PUBLIC_URL_CREATED_TRUE"
PUBLIC_URL_NON_NULL: Final[str] = "PUBLIC_URL_NON_NULL"

GATE_DECISION_ENVELOPE_BUILD_REASON_CODES: Final[tuple[str, ...]] = (
    RUN_ID_MISSING,
    GATE_NAME_MISSING,
    GATE_NAME_UNKNOWN,
    DECISION_MISSING,
    DECISION_UNKNOWN,
    FROM_STATE_MISSING,
    TO_STATE_MISSING,
    REASON_CODES_MISSING,
    SOURCE_OF_TRUTH_MISSING,
    CHECKED_AT_MISSING,
    TIMESTAMP_POLICY_MISSING,
    REDACTION_STATUS_MISSING,
    REQUIRED_INPUTS_PRESENT_WITH_MISSING_INPUTS,
    REQUIRED_INPUTS_MISSING_WITHOUT_MISSING_INPUTS,
    PASS_WITH_BLOCKING_REASONS,
    BLOCKED_WITHOUT_BLOCKING_REASONS,
    PUBLIC_URL_CREATED_TRUE,
    PUBLIC_URL_NON_NULL,
    GATE_DECISION_ENVELOPE_BUILDABLE,
)

_SOURCE: Final[str] = (
    "gate_decision_envelope_builder."
    "explain_gate_decision_envelope_build"
)
_LOCAL_INVARIANTS: Final[tuple[str, ...]] = (
    "gate_decision_envelope_builder_only",
    "builder_not_gate_execution",
    "builder_not_transition_mapping",
    "builder_not_transition_execution",
    "buildable_not_ledger_write",
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
        GATE_NAME_MISSING,
        "A non-empty caller-supplied gate_name is required.",
    ),
    (
        GATE_NAME_UNKNOWN,
        "The caller-supplied gate_name is not declared in gates.GATE_NAMES.",
    ),
    (
        DECISION_MISSING,
        "A non-empty caller-supplied decision is required.",
    ),
    (
        DECISION_UNKNOWN,
        "The caller-supplied decision is not PASS or BLOCKED.",
    ),
    (
        FROM_STATE_MISSING,
        "A non-empty caller-supplied from_state is required.",
    ),
    (
        TO_STATE_MISSING,
        "A non-empty caller-supplied to_state is required.",
    ),
    (
        REASON_CODES_MISSING,
        "At least one caller-supplied reason code is required.",
    ),
    (
        SOURCE_OF_TRUTH_MISSING,
        "At least one caller-supplied source_of_truth reference is required.",
    ),
    (
        CHECKED_AT_MISSING,
        "A non-empty caller-supplied checked_at value is required.",
    ),
    (
        TIMESTAMP_POLICY_MISSING,
        "A non-empty caller-supplied timestamp_policy is required.",
    ),
    (
        REDACTION_STATUS_MISSING,
        "A non-empty caller-supplied redaction_status is required.",
    ),
    (
        REQUIRED_INPUTS_PRESENT_WITH_MISSING_INPUTS,
        "required_inputs_present cannot be true when missing_inputs is "
        "non-empty.",
    ),
    (
        REQUIRED_INPUTS_MISSING_WITHOUT_MISSING_INPUTS,
        "required_inputs_present cannot be false without caller-supplied "
        "missing_inputs.",
    ),
    (
        PASS_WITH_BLOCKING_REASONS,
        "PASS envelopes cannot include blocking_reasons.",
    ),
    (
        BLOCKED_WITHOUT_BLOCKING_REASONS,
        "BLOCKED envelopes require at least one blocking reason.",
    ),
    (
        PUBLIC_URL_CREATED_TRUE,
        "MVP noop envelopes require public_url_created to remain false.",
    ),
    (
        PUBLIC_URL_NON_NULL,
        "MVP noop envelopes require the caller-supplied public URL null "
        "marker to remain true.",
    ),
    (
        GATE_DECISION_ENVELOPE_BUILDABLE,
        "The caller-supplied fields can build the Shared Gate Decision "
        "Envelope shape. This does not execute a gate, map or execute a "
        "transition, write a ledger, publish, send notification, create "
        "or return a public URL, read runtime context, configuration, "
        "credentials, adapter outputs, artifacts, reviews, hashes or "
        "ledgers, call existing policy modules, or call an external "
        "service.",
    ),
)
_VIOLATION_FIELD_ENTRIES: Final[tuple[tuple[str, tuple[str, ...]], ...]] = (
    (RUN_ID_MISSING, ("run_id",)),
    (GATE_NAME_MISSING, ("gate_name",)),
    (GATE_NAME_UNKNOWN, ("gate_name",)),
    (DECISION_MISSING, ("decision",)),
    (DECISION_UNKNOWN, ("decision",)),
    (FROM_STATE_MISSING, ("from_state",)),
    (TO_STATE_MISSING, ("to_state",)),
    (REASON_CODES_MISSING, ("reason_codes",)),
    (SOURCE_OF_TRUTH_MISSING, ("source_of_truth",)),
    (CHECKED_AT_MISSING, ("checked_at",)),
    (TIMESTAMP_POLICY_MISSING, ("timestamp_policy",)),
    (REDACTION_STATUS_MISSING, ("redaction_status",)),
    (
        REQUIRED_INPUTS_PRESENT_WITH_MISSING_INPUTS,
        ("required_inputs_present", "missing_inputs"),
    ),
    (
        REQUIRED_INPUTS_MISSING_WITHOUT_MISSING_INPUTS,
        ("required_inputs_present", "missing_inputs"),
    ),
    (PASS_WITH_BLOCKING_REASONS, ("blocking_reasons",)),
    (BLOCKED_WITHOUT_BLOCKING_REASONS, ("blocking_reasons",)),
    (PUBLIC_URL_CREATED_TRUE, ("public_url_created",)),
    (PUBLIC_URL_NON_NULL, ("public_url",)),
)


def _reason_text(reason_code: str) -> str:
    for code, text in _REASON_TEXT_ENTRIES:
        if code == reason_code:
            return text
    return "Unknown Gate Decision Envelope build result."


def _ordered_unique(values: tuple[str, ...]) -> tuple[str, ...]:
    ordered_values = ()
    for value in values:
        if value not in ordered_values:
            ordered_values = ordered_values + (value,)
    return ordered_values


def _missing_or_invalid_fields(
    envelope_violations: tuple[str, ...],
) -> tuple[str, ...]:
    field_names = ()
    for violation in envelope_violations:
        for reason_code, invalid_fields in _VIOLATION_FIELD_ENTRIES:
            if violation == reason_code:
                field_names = field_names + invalid_fields
    return _ordered_unique(field_names)


def _envelope(
    *,
    run_id: str,
    gate_name: str,
    decision: str,
    from_state: str,
    to_state: str,
    reason_codes: tuple[str, ...],
    blocking_reasons: tuple[str, ...],
    evidence_refs: tuple[str, ...],
    input_evidence_refs: tuple[str, ...],
    required_inputs_present: bool,
    missing_inputs: tuple[str, ...],
    redaction_status: str,
    public_url_created: bool,
    checked_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    return {
        "run_id": run_id,
        "gate_name": gate_name,
        "decision": decision,
        "from_state": from_state,
        "to_state": to_state,
        "reason_codes": reason_codes,
        "blocking_reasons": blocking_reasons,
        "evidence_refs": evidence_refs,
        "input_evidence_refs": input_evidence_refs,
        "required_inputs_present": required_inputs_present,
        "missing_inputs": missing_inputs,
        "redaction_status": redaction_status,
        "public_url_created": public_url_created,
        "public_url": None,
        "checked_at": checked_at,
        "timestamp_policy": timestamp_policy,
        "source_of_truth": source_of_truth,
        "notes": notes,
    }


def _result(
    *,
    buildable: bool,
    reason_code: str,
    envelope,
    envelope_violations: tuple[str, ...],
    missing_or_invalid_fields: tuple[str, ...],
) -> dict[str, object]:
    return {
        "buildable": buildable,
        "reason_code": reason_code,
        "reason": _reason_text(reason_code),
        "source": _SOURCE,
        "envelope": envelope,
        "envelope_violations": envelope_violations,
        "missing_or_invalid_fields": missing_or_invalid_fields,
        "invariant_refs": _INVARIANTS,
    }


def explain_gate_decision_envelope_build(
    *,
    run_id: str,
    gate_name: str,
    decision: str,
    from_state: str,
    to_state: str,
    reason_codes: tuple[str, ...],
    blocking_reasons: tuple[str, ...],
    evidence_refs: tuple[str, ...],
    input_evidence_refs: tuple[str, ...],
    required_inputs_present: bool,
    missing_inputs: tuple[str, ...],
    redaction_status: str,
    public_url_created: bool,
    public_url_is_null: bool,
    checked_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    """Explain whether caller-supplied fields can build the envelope."""
    gate_name_missing = gate_name.strip() == ""
    gate_name_unknown = (
        gate_name_missing is False and gate_name not in gates.GATE_NAMES
    )
    decision_missing = decision.strip() == ""
    decision_unknown = (
        decision_missing is False
        and decision not in (gates.PASS, gates.BLOCKED)
    )
    prioritized_violations = (
        (run_id.strip() == "", RUN_ID_MISSING),
        (gate_name_missing, GATE_NAME_MISSING),
        (gate_name_unknown, GATE_NAME_UNKNOWN),
        (decision_missing, DECISION_MISSING),
        (decision_unknown, DECISION_UNKNOWN),
        (from_state.strip() == "", FROM_STATE_MISSING),
        (to_state.strip() == "", TO_STATE_MISSING),
        (reason_codes == (), REASON_CODES_MISSING),
        (source_of_truth == (), SOURCE_OF_TRUTH_MISSING),
        (checked_at.strip() == "", CHECKED_AT_MISSING),
        (timestamp_policy.strip() == "", TIMESTAMP_POLICY_MISSING),
        (redaction_status.strip() == "", REDACTION_STATUS_MISSING),
        (
            required_inputs_present is True and missing_inputs != (),
            REQUIRED_INPUTS_PRESENT_WITH_MISSING_INPUTS,
        ),
        (
            required_inputs_present is False and missing_inputs == (),
            REQUIRED_INPUTS_MISSING_WITHOUT_MISSING_INPUTS,
        ),
        (
            decision == gates.PASS and blocking_reasons != (),
            PASS_WITH_BLOCKING_REASONS,
        ),
        (
            decision == gates.BLOCKED and blocking_reasons == (),
            BLOCKED_WITHOUT_BLOCKING_REASONS,
        ),
        (public_url_created is True, PUBLIC_URL_CREATED_TRUE),
        (public_url_is_null is False, PUBLIC_URL_NON_NULL),
    )
    envelope_violations = tuple(
        reason_code
        for condition, reason_code in prioritized_violations
        if condition
    )
    buildable = envelope_violations == ()
    reason_code = (
        GATE_DECISION_ENVELOPE_BUILDABLE
        if buildable
        else envelope_violations[0]
    )

    return _result(
        buildable=buildable,
        reason_code=reason_code,
        envelope=_envelope(
            run_id=run_id,
            gate_name=gate_name,
            decision=decision,
            from_state=from_state,
            to_state=to_state,
            reason_codes=reason_codes,
            blocking_reasons=blocking_reasons,
            evidence_refs=evidence_refs,
            input_evidence_refs=input_evidence_refs,
            required_inputs_present=required_inputs_present,
            missing_inputs=missing_inputs,
            redaction_status=redaction_status,
            public_url_created=public_url_created,
            checked_at=checked_at,
            timestamp_policy=timestamp_policy,
            source_of_truth=source_of_truth,
            notes=notes,
        ),
        envelope_violations=envelope_violations,
        missing_or_invalid_fields=(
            _missing_or_invalid_fields(envelope_violations)
        ),
    )


def is_gate_decision_envelope_buildable(
    *,
    run_id: str,
    gate_name: str,
    decision: str,
    from_state: str,
    to_state: str,
    reason_codes: tuple[str, ...],
    blocking_reasons: tuple[str, ...],
    evidence_refs: tuple[str, ...],
    input_evidence_refs: tuple[str, ...],
    required_inputs_present: bool,
    missing_inputs: tuple[str, ...],
    redaction_status: str,
    public_url_created: bool,
    public_url_is_null: bool,
    checked_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> bool:
    """Return only the boolean result from the build explanation."""
    return bool(
        explain_gate_decision_envelope_build(
            run_id=run_id,
            gate_name=gate_name,
            decision=decision,
            from_state=from_state,
            to_state=to_state,
            reason_codes=reason_codes,
            blocking_reasons=blocking_reasons,
            evidence_refs=evidence_refs,
            input_evidence_refs=input_evidence_refs,
            required_inputs_present=required_inputs_present,
            missing_inputs=missing_inputs,
            redaction_status=redaction_status,
            public_url_created=public_url_created,
            public_url_is_null=public_url_is_null,
            checked_at=checked_at,
            timestamp_policy=timestamp_policy,
            source_of_truth=source_of_truth,
            notes=notes,
        )["buildable"]
    )
