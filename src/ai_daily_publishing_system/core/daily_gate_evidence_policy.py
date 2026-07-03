"""Pure Daily Gate evidence policy guard for the AI Daily Publishing System."""

from typing import Final

from ai_daily_publishing_system.core import gates


DAILY_GATE_EVIDENCE_ALLOWED: Final[str] = "DAILY_GATE_EVIDENCE_ALLOWED"
REQUIRED_DAILY_GATE_INPUTS_MISSING: Final[str] = (
    "REQUIRED_DAILY_GATE_INPUTS_MISSING"
)
VALIDATOR_RESULT_MISSING: Final[str] = "VALIDATOR_RESULT_MISSING"
RUBRIC_REVIEW_MISSING: Final[str] = "RUBRIC_REVIEW_MISSING"
AUDIT_REVIEW_MISSING: Final[str] = "AUDIT_REVIEW_MISSING"
ARTIFACT_INVENTORY_POLICY_BLOCKED: Final[str] = (
    "ARTIFACT_INVENTORY_POLICY_BLOCKED"
)
PREGATE_HASH_MISSING: Final[str] = "PREGATE_HASH_MISSING"
MISSING_PUBLIC_PRIVATE_LEAK_CHECK: Final[str] = (
    "MISSING_PUBLIC_PRIVATE_LEAK_CHECK"
)
MISSING_CREDENTIAL_REDACTION_MARKER: Final[str] = (
    "MISSING_CREDENTIAL_REDACTION_MARKER"
)
MISSING_EVIDENCE_COMPLETENESS_MARKER: Final[str] = (
    "MISSING_EVIDENCE_COMPLETENESS_MARKER"
)
BLOCKING_RISK_PRESENT: Final[str] = "BLOCKING_RISK_PRESENT"
NOOP_PUBLISH_MODE_NOT_DECLARED: Final[str] = (
    "NOOP_PUBLISH_MODE_NOT_DECLARED"
)
NOOP_PUBLIC_URL_NON_NULL: Final[str] = "NOOP_PUBLIC_URL_NON_NULL"
NOOP_PUBLIC_URL_CREATED_TRUE: Final[str] = (
    "NOOP_PUBLIC_URL_CREATED_TRUE"
)

DAILY_GATE_EVIDENCE_POLICY_REASON_CODES: Final[tuple[str, ...]] = (
    REQUIRED_DAILY_GATE_INPUTS_MISSING,
    VALIDATOR_RESULT_MISSING,
    RUBRIC_REVIEW_MISSING,
    AUDIT_REVIEW_MISSING,
    ARTIFACT_INVENTORY_POLICY_BLOCKED,
    PREGATE_HASH_MISSING,
    MISSING_PUBLIC_PRIVATE_LEAK_CHECK,
    MISSING_CREDENTIAL_REDACTION_MARKER,
    MISSING_EVIDENCE_COMPLETENESS_MARKER,
    BLOCKING_RISK_PRESENT,
    NOOP_PUBLISH_MODE_NOT_DECLARED,
    NOOP_PUBLIC_URL_NON_NULL,
    NOOP_PUBLIC_URL_CREATED_TRUE,
    DAILY_GATE_EVIDENCE_ALLOWED,
)

_POLICY_SOURCE: Final[str] = (
    "daily_gate_evidence_policy.explain_daily_gate_evidence_policy"
)
_LOCAL_POLICY_INVARIANTS: Final[tuple[str, ...]] = (
    "daily_gate_evidence_policy_only",
    "evidence_policy_not_gate_execution",
    "allowed_not_daily_gate_pass",
    "allowed_not_publish_allowed",
    "no_quality_pass_no_public_url",
    "noop_public_url_must_remain_null",
    "noop_public_url_created_must_remain_false",
    "generated_post_gate_ledgers_are_not_daily_gate_inputs",
    "no_artifact_or_review_io",
    "no_hash_calculation",
    "no_ledger_write",
    "no_publish_or_notification",
)
_POLICY_INVARIANTS: Final[tuple[str, ...]] = (
    gates.GATE_INVARIANTS + _LOCAL_POLICY_INVARIANTS
)
_REASON_TEXT_ENTRIES: Final[tuple[tuple[str, str], ...]] = (
    (
        REQUIRED_DAILY_GATE_INPUTS_MISSING,
        "Caller-supplied required Daily Gate input evidence marker is "
        "missing.",
    ),
    (
        VALIDATOR_RESULT_MISSING,
        "Caller-supplied validator result presence marker is missing; "
        "the policy does not read or evaluate validator content.",
    ),
    (
        RUBRIC_REVIEW_MISSING,
        "Caller-supplied rubric review presence marker is missing; the "
        "policy does not read or score review content.",
    ),
    (
        AUDIT_REVIEW_MISSING,
        "Caller-supplied audit review presence marker is missing; the "
        "policy does not read or audit review content.",
    ),
    (
        ARTIFACT_INVENTORY_POLICY_BLOCKED,
        "Caller-supplied artifact inventory policy marker is blocked; "
        "this policy does not call or repeat the inventory policy.",
    ),
    (
        PREGATE_HASH_MISSING,
        "Caller-supplied pre-gate hash evidence marker is missing; this "
        "policy does not read artifacts or calculate hashes.",
    ),
    (
        MISSING_PUBLIC_PRIVATE_LEAK_CHECK,
        "Caller-supplied public/private leak check presence marker is "
        "missing; this policy does not execute a leak scan.",
    ),
    (
        MISSING_CREDENTIAL_REDACTION_MARKER,
        "Caller-supplied credential redaction marker is missing; this "
        "policy does not read credential values.",
    ),
    (
        MISSING_EVIDENCE_COMPLETENESS_MARKER,
        "Caller-supplied evidence completeness marker is missing; this "
        "policy does not read evidence content.",
    ),
    (
        BLOCKING_RISK_PRESENT,
        "Caller-supplied blocking risk marker indicates that blocking "
        "risk flags are present.",
    ),
    (
        NOOP_PUBLISH_MODE_NOT_DECLARED,
        "Caller-supplied MVP noop publish mode marker is not declared.",
    ),
    (
        NOOP_PUBLIC_URL_NON_NULL,
        "Caller-supplied noop marker does not confirm that the public "
        "URL remains null.",
    ),
    (
        NOOP_PUBLIC_URL_CREATED_TRUE,
        "Caller-supplied noop marker does not confirm that public URL "
        "creation remains false.",
    ),
    (
        DAILY_GATE_EVIDENCE_ALLOWED,
        "Caller-supplied evidence markers satisfy the static Daily Gate "
        "evidence policy. This does not mean Daily Gate PASS, does not "
        "produce PUBLISH_ALLOWED, and executes no gate, transition, "
        "artifact or review IO, hash calculation, ledger write, publish "
        "action, notification action, or public URL behavior.",
    ),
)


def _reason_text(reason_code: str) -> str:
    for code, text in _REASON_TEXT_ENTRIES:
        if code == reason_code:
            return text
    return "Unknown Daily Gate evidence policy result."


def _decision(
    *,
    markers: dict[str, bool],
    allowed: bool,
    reason_code: str,
    missing_evidence_markers: tuple[str, ...],
    failed_policy_markers: tuple[str, ...],
    noop_policy_violations: tuple[str, ...],
) -> dict[str, object]:
    return {
        "allowed": allowed,
        "reason_code": reason_code,
        "reason": _reason_text(reason_code),
        "source": _POLICY_SOURCE,
        **markers,
        "missing_evidence_markers": missing_evidence_markers,
        "failed_policy_markers": failed_policy_markers,
        "noop_policy_violations": noop_policy_violations,
        "invariant_refs": _POLICY_INVARIANTS,
    }


def explain_daily_gate_evidence_policy(
    *,
    required_daily_gate_inputs_present: bool,
    validator_result_present: bool,
    rubric_review_present: bool,
    audit_review_present: bool,
    artifact_inventory_policy_allowed: bool,
    pre_gate_hash_evidence_present: bool,
    public_private_leak_check_present: bool,
    credential_redaction_marker_present: bool,
    evidence_completeness_marker_present: bool,
    blocking_risk_flags_present: bool,
    noop_publish_mode_declared: bool,
    noop_public_url_is_null: bool,
    noop_public_url_created_is_false: bool,
) -> dict[str, object]:
    """Explain caller-supplied evidence marker policy without side effects."""
    markers = {
        "required_daily_gate_inputs_present": (
            required_daily_gate_inputs_present
        ),
        "validator_result_present": validator_result_present,
        "rubric_review_present": rubric_review_present,
        "audit_review_present": audit_review_present,
        "artifact_inventory_policy_allowed": (
            artifact_inventory_policy_allowed
        ),
        "pre_gate_hash_evidence_present": pre_gate_hash_evidence_present,
        "public_private_leak_check_present": (
            public_private_leak_check_present
        ),
        "credential_redaction_marker_present": (
            credential_redaction_marker_present
        ),
        "evidence_completeness_marker_present": (
            evidence_completeness_marker_present
        ),
        "blocking_risk_flags_present": blocking_risk_flags_present,
        "noop_publish_mode_declared": noop_publish_mode_declared,
        "noop_public_url_is_null": noop_public_url_is_null,
        "noop_public_url_created_is_false": (
            noop_public_url_created_is_false
        ),
    }
    missing_evidence_markers = tuple(
        marker_name
        for marker_name, marker_present in (
            (
                "required_daily_gate_inputs_present",
                required_daily_gate_inputs_present,
            ),
            ("validator_result_present", validator_result_present),
            ("rubric_review_present", rubric_review_present),
            ("audit_review_present", audit_review_present),
            (
                "pre_gate_hash_evidence_present",
                pre_gate_hash_evidence_present,
            ),
            (
                "public_private_leak_check_present",
                public_private_leak_check_present,
            ),
            (
                "credential_redaction_marker_present",
                credential_redaction_marker_present,
            ),
            (
                "evidence_completeness_marker_present",
                evidence_completeness_marker_present,
            ),
        )
        if marker_present is False
    )
    failed_policy_markers = tuple(
        marker_name
        for marker_name, marker_failed in (
            (
                "artifact_inventory_policy_allowed",
                artifact_inventory_policy_allowed is False,
            ),
            (
                "blocking_risk_flags_present",
                blocking_risk_flags_present is True,
            ),
        )
        if marker_failed
    )
    noop_policy_violations = tuple(
        marker_name
        for marker_name, marker_violated in (
            (
                "noop_publish_mode_declared",
                noop_publish_mode_declared is False,
            ),
            (
                "noop_public_url_is_null",
                noop_public_url_is_null is False,
            ),
            (
                "noop_public_url_created_is_false",
                noop_public_url_created_is_false is False,
            ),
        )
        if marker_violated
    )
    prioritized_failures = (
        (
            required_daily_gate_inputs_present is False,
            REQUIRED_DAILY_GATE_INPUTS_MISSING,
        ),
        (validator_result_present is False, VALIDATOR_RESULT_MISSING),
        (rubric_review_present is False, RUBRIC_REVIEW_MISSING),
        (audit_review_present is False, AUDIT_REVIEW_MISSING),
        (
            artifact_inventory_policy_allowed is False,
            ARTIFACT_INVENTORY_POLICY_BLOCKED,
        ),
        (pre_gate_hash_evidence_present is False, PREGATE_HASH_MISSING),
        (
            public_private_leak_check_present is False,
            MISSING_PUBLIC_PRIVATE_LEAK_CHECK,
        ),
        (
            credential_redaction_marker_present is False,
            MISSING_CREDENTIAL_REDACTION_MARKER,
        ),
        (
            evidence_completeness_marker_present is False,
            MISSING_EVIDENCE_COMPLETENESS_MARKER,
        ),
        (blocking_risk_flags_present is True, BLOCKING_RISK_PRESENT),
        (
            noop_publish_mode_declared is False,
            NOOP_PUBLISH_MODE_NOT_DECLARED,
        ),
        (noop_public_url_is_null is False, NOOP_PUBLIC_URL_NON_NULL),
        (
            noop_public_url_created_is_false is False,
            NOOP_PUBLIC_URL_CREATED_TRUE,
        ),
    )

    for is_blocked, reason_code in prioritized_failures:
        if is_blocked:
            return _decision(
                markers=markers,
                allowed=False,
                reason_code=reason_code,
                missing_evidence_markers=missing_evidence_markers,
                failed_policy_markers=failed_policy_markers,
                noop_policy_violations=noop_policy_violations,
            )

    return _decision(
        markers=markers,
        allowed=True,
        reason_code=DAILY_GATE_EVIDENCE_ALLOWED,
        missing_evidence_markers=missing_evidence_markers,
        failed_policy_markers=failed_policy_markers,
        noop_policy_violations=noop_policy_violations,
    )


def is_daily_gate_evidence_allowed(
    *,
    required_daily_gate_inputs_present: bool,
    validator_result_present: bool,
    rubric_review_present: bool,
    audit_review_present: bool,
    artifact_inventory_policy_allowed: bool,
    pre_gate_hash_evidence_present: bool,
    public_private_leak_check_present: bool,
    credential_redaction_marker_present: bool,
    evidence_completeness_marker_present: bool,
    blocking_risk_flags_present: bool,
    noop_publish_mode_declared: bool,
    noop_public_url_is_null: bool,
    noop_public_url_created_is_false: bool,
) -> bool:
    """Return only the boolean result from the evidence explanation."""
    return bool(
        explain_daily_gate_evidence_policy(
            required_daily_gate_inputs_present=(
                required_daily_gate_inputs_present
            ),
            validator_result_present=validator_result_present,
            rubric_review_present=rubric_review_present,
            audit_review_present=audit_review_present,
            artifact_inventory_policy_allowed=(
                artifact_inventory_policy_allowed
            ),
            pre_gate_hash_evidence_present=pre_gate_hash_evidence_present,
            public_private_leak_check_present=(
                public_private_leak_check_present
            ),
            credential_redaction_marker_present=(
                credential_redaction_marker_present
            ),
            evidence_completeness_marker_present=(
                evidence_completeness_marker_present
            ),
            blocking_risk_flags_present=blocking_risk_flags_present,
            noop_publish_mode_declared=noop_publish_mode_declared,
            noop_public_url_is_null=noop_public_url_is_null,
            noop_public_url_created_is_false=(
                noop_public_url_created_is_false
            ),
        )["allowed"]
    )
