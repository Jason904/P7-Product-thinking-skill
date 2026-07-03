"""Pure Adapter Gate decision policy guard for the publishing system."""

from typing import Final

from ai_daily_publishing_system.core import gates


ADAPTER_GATE_DECISION_ALLOWED: Final[str] = (
    "ADAPTER_GATE_DECISION_ALLOWED"
)
ADAPTER_GATE_DECISION_MISSING: Final[str] = (
    "ADAPTER_GATE_DECISION_MISSING"
)
ADAPTER_GATE_DECISION_UNKNOWN: Final[str] = (
    "ADAPTER_GATE_DECISION_UNKNOWN"
)
PASS_WITH_ADAPTER_EVIDENCE_POLICY_BLOCKED: Final[str] = (
    "PASS_WITH_ADAPTER_EVIDENCE_POLICY_BLOCKED"
)
PASS_WITH_BLOCKING_ADAPTER_MARKERS_PRESENT: Final[str] = (
    "PASS_WITH_BLOCKING_ADAPTER_MARKERS_PRESENT"
)
EVIDENCE_ALLOWED_WITH_BLOCKING_ADAPTER_MARKERS: Final[str] = (
    "EVIDENCE_ALLOWED_WITH_BLOCKING_ADAPTER_MARKERS"
)
BLOCKED_WITH_ADAPTER_EVIDENCE_ALLOWED_WITHOUT_BLOCKING_MARKERS: Final[str] = (
    "BLOCKED_WITH_ADAPTER_EVIDENCE_ALLOWED_WITHOUT_BLOCKING_MARKERS"
)

ADAPTER_GATE_DECISION_POLICY_REASON_CODES: Final[tuple[str, ...]] = (
    ADAPTER_GATE_DECISION_MISSING,
    ADAPTER_GATE_DECISION_UNKNOWN,
    PASS_WITH_ADAPTER_EVIDENCE_POLICY_BLOCKED,
    PASS_WITH_BLOCKING_ADAPTER_MARKERS_PRESENT,
    EVIDENCE_ALLOWED_WITH_BLOCKING_ADAPTER_MARKERS,
    BLOCKED_WITH_ADAPTER_EVIDENCE_ALLOWED_WITHOUT_BLOCKING_MARKERS,
    ADAPTER_GATE_DECISION_ALLOWED,
)

_POLICY_SOURCE: Final[str] = (
    "adapter_gate_decision_policy.explain_adapter_gate_decision_policy"
)
_LOCAL_POLICY_INVARIANTS: Final[tuple[str, ...]] = (
    "adapter_gate_decision_policy_only",
    "decision_policy_not_adapter_gate_execution",
    "decision_policy_not_transition_mapping",
    "allowed_pass_not_retrieving",
    "allowed_blocked_not_config_blocked",
    "blocked_decision_not_failure_package",
    "blocked_decision_not_badcase_created",
    "no_runtime_context_config_or_credential_read",
    "no_adapter_preflight",
    "no_external_adapter_call",
    "no_raw_credentials",
    "no_quality_pass_no_public_url",
    "no_artifact_or_review_io",
    "no_hash_calculation",
    "no_ledger_write",
    "no_publish_or_notification",
    "no_public_url_behavior",
)
_POLICY_INVARIANTS: Final[tuple[str, ...]] = (
    gates.GATE_INVARIANTS + _LOCAL_POLICY_INVARIANTS
)
_REASON_TEXT_ENTRIES: Final[tuple[tuple[str, str], ...]] = (
    (
        ADAPTER_GATE_DECISION_MISSING,
        "A non-empty caller-supplied Adapter Gate decision is required.",
    ),
    (
        ADAPTER_GATE_DECISION_UNKNOWN,
        "The caller-supplied decision is not a canonical Adapter Gate "
        "decision label.",
    ),
    (
        PASS_WITH_ADAPTER_EVIDENCE_POLICY_BLOCKED,
        "PASS is inconsistent when the caller-supplied Adapter evidence "
        "policy marker is blocked.",
    ),
    (
        PASS_WITH_BLOCKING_ADAPTER_MARKERS_PRESENT,
        "PASS is inconsistent when caller-supplied blocking Adapter "
        "markers are present.",
    ),
    (
        EVIDENCE_ALLOWED_WITH_BLOCKING_ADAPTER_MARKERS,
        "The caller-supplied evidence policy allowed marker conflicts "
        "with caller-supplied blocking Adapter markers.",
    ),
    (
        BLOCKED_WITH_ADAPTER_EVIDENCE_ALLOWED_WITHOUT_BLOCKING_MARKERS,
        "BLOCKED is inconsistent when evidence policy is allowed and no "
        "blocking Adapter markers are present.",
    ),
    (
        ADAPTER_GATE_DECISION_ALLOWED,
        "The caller-supplied Adapter Gate decision is consistent with "
        "the evidence policy and blocking Adapter markers. This static "
        "result does not execute a gate, map or execute a transition, "
        "produce a state, create a failure package or badcase, read "
        "runtime, configuration, credentials, Adapter output, artifacts, "
        "reviews or ledgers, run Adapter preflight, calculate a hash, "
        "call an external service, publish, notify, or create a public "
        "URL.",
    ),
)


def _reason_text(reason_code: str) -> str:
    for code, text in _REASON_TEXT_ENTRIES:
        if code == reason_code:
            return text
    return "Unknown Adapter Gate decision policy result."


def _decision(
    *,
    decision: str,
    evidence_policy_allowed: bool,
    blocking_adapter_markers_present: bool,
    allowed: bool,
    reason_code: str,
    decision_violations: tuple[str, ...],
) -> dict[str, object]:
    return {
        "allowed": allowed,
        "reason_code": reason_code,
        "reason": _reason_text(reason_code),
        "source": _POLICY_SOURCE,
        "decision": decision,
        "evidence_policy_allowed": evidence_policy_allowed,
        "blocking_adapter_markers_present": (
            blocking_adapter_markers_present
        ),
        "decision_violations": decision_violations,
        "invariant_refs": _POLICY_INVARIANTS,
    }


def explain_adapter_gate_decision_policy(
    *,
    decision: str,
    evidence_policy_allowed: bool,
    blocking_adapter_markers_present: bool,
) -> dict[str, object]:
    """Explain caller-supplied Adapter Gate decision consistency."""
    decision_missing = decision.strip() == ""
    decision_unknown = (
        decision_missing is False
        and decision not in (gates.PASS, gates.BLOCKED)
    )
    prioritized_violations = (
        (decision_missing, ADAPTER_GATE_DECISION_MISSING),
        (decision_unknown, ADAPTER_GATE_DECISION_UNKNOWN),
        (
            decision == gates.PASS
            and evidence_policy_allowed is False,
            PASS_WITH_ADAPTER_EVIDENCE_POLICY_BLOCKED,
        ),
        (
            decision == gates.PASS
            and blocking_adapter_markers_present is True,
            PASS_WITH_BLOCKING_ADAPTER_MARKERS_PRESENT,
        ),
        (
            evidence_policy_allowed is True
            and blocking_adapter_markers_present is True,
            EVIDENCE_ALLOWED_WITH_BLOCKING_ADAPTER_MARKERS,
        ),
        (
            decision == gates.BLOCKED
            and evidence_policy_allowed is True
            and blocking_adapter_markers_present is False,
            (
                BLOCKED_WITH_ADAPTER_EVIDENCE_ALLOWED_WITHOUT_BLOCKING_MARKERS
            ),
        ),
    )
    decision_violations = tuple(
        reason_code
        for condition, reason_code in prioritized_violations
        if condition
    )
    allowed = len(decision_violations) == 0
    reason_code = (
        ADAPTER_GATE_DECISION_ALLOWED
        if allowed
        else decision_violations[0]
    )

    return _decision(
        decision=decision,
        evidence_policy_allowed=evidence_policy_allowed,
        blocking_adapter_markers_present=(
            blocking_adapter_markers_present
        ),
        allowed=allowed,
        reason_code=reason_code,
        decision_violations=decision_violations,
    )


def is_adapter_gate_decision_allowed(
    *,
    decision: str,
    evidence_policy_allowed: bool,
    blocking_adapter_markers_present: bool,
) -> bool:
    """Return only the boolean result from the decision explanation."""
    return bool(
        explain_adapter_gate_decision_policy(
            decision=decision,
            evidence_policy_allowed=evidence_policy_allowed,
            blocking_adapter_markers_present=(
                blocking_adapter_markers_present
            ),
        )["allowed"]
    )
