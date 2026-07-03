"""Pure Daily Gate decision policy guard for the publishing system."""

from typing import Final

from ai_daily_publishing_system.core import gates


DAILY_GATE_DECISION_ALLOWED: Final[str] = "DAILY_GATE_DECISION_ALLOWED"
DAILY_GATE_DECISION_MISSING: Final[str] = "DAILY_GATE_DECISION_MISSING"
DAILY_GATE_DECISION_UNKNOWN: Final[str] = "DAILY_GATE_DECISION_UNKNOWN"
PASS_WITH_EVIDENCE_POLICY_BLOCKED: Final[str] = (
    "PASS_WITH_EVIDENCE_POLICY_BLOCKED"
)
PASS_WITH_CONSERVATIVE_BLOCK_REQUESTED: Final[str] = (
    "PASS_WITH_CONSERVATIVE_BLOCK_REQUESTED"
)
BLOCKED_WITH_EVIDENCE_POLICY_ALLOWED_WITHOUT_CONSERVATIVE_BLOCK: Final[str] = (
    "BLOCKED_WITH_EVIDENCE_POLICY_ALLOWED_WITHOUT_CONSERVATIVE_BLOCK"
)
BLOCKED_WITH_CONSERVATIVE_BLOCK_REASON_MISSING: Final[str] = (
    "BLOCKED_WITH_CONSERVATIVE_BLOCK_REASON_MISSING"
)
CONSERVATIVE_BLOCK_REASON_WITHOUT_REQUEST: Final[str] = (
    "CONSERVATIVE_BLOCK_REASON_WITHOUT_REQUEST"
)

DAILY_GATE_DECISION_POLICY_REASON_CODES: Final[tuple[str, ...]] = (
    DAILY_GATE_DECISION_MISSING,
    DAILY_GATE_DECISION_UNKNOWN,
    CONSERVATIVE_BLOCK_REASON_WITHOUT_REQUEST,
    PASS_WITH_EVIDENCE_POLICY_BLOCKED,
    PASS_WITH_CONSERVATIVE_BLOCK_REQUESTED,
    BLOCKED_WITH_EVIDENCE_POLICY_ALLOWED_WITHOUT_CONSERVATIVE_BLOCK,
    BLOCKED_WITH_CONSERVATIVE_BLOCK_REASON_MISSING,
    DAILY_GATE_DECISION_ALLOWED,
)

_POLICY_SOURCE: Final[str] = (
    "daily_gate_decision_policy.explain_daily_gate_decision_policy"
)
_LOCAL_POLICY_INVARIANTS: Final[tuple[str, ...]] = (
    "daily_gate_decision_policy_only",
    "decision_policy_not_gate_execution",
    "decision_policy_not_transition_mapping",
    "allowed_pass_not_publish_allowed",
    "allowed_blocked_not_review_blocked",
    "allowed_blocked_not_badcase_created",
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
        DAILY_GATE_DECISION_MISSING,
        "A non-empty caller-supplied Daily Gate decision is required.",
    ),
    (
        DAILY_GATE_DECISION_UNKNOWN,
        "The caller-supplied decision is not a canonical Daily Gate "
        "decision label.",
    ),
    (
        CONSERVATIVE_BLOCK_REASON_WITHOUT_REQUEST,
        "A conservative block reason marker cannot be present without a "
        "conservative block request.",
    ),
    (
        PASS_WITH_EVIDENCE_POLICY_BLOCKED,
        "PASS is inconsistent when the caller-supplied evidence policy "
        "marker is blocked.",
    ),
    (
        PASS_WITH_CONSERVATIVE_BLOCK_REQUESTED,
        "PASS is inconsistent when a caller-supplied conservative block "
        "is requested.",
    ),
    (
        BLOCKED_WITH_EVIDENCE_POLICY_ALLOWED_WITHOUT_CONSERVATIVE_BLOCK,
        "BLOCKED requires a conservative block request when the "
        "caller-supplied evidence policy marker is allowed.",
    ),
    (
        BLOCKED_WITH_CONSERVATIVE_BLOCK_REASON_MISSING,
        "A requested conservative BLOCKED decision requires a "
        "caller-supplied conservative reason marker.",
    ),
    (
        DAILY_GATE_DECISION_ALLOWED,
        "The caller-supplied Daily Gate decision is consistent with the "
        "evidence policy and conservative block markers. This static "
        "result does not execute a gate, map or execute a transition, "
        "produce a state, create a badcase or failure package, read or "
        "write evidence, calculate a hash, write a ledger, publish, "
        "notify, or create a public URL.",
    ),
)


def _reason_text(reason_code: str) -> str:
    for code, text in _REASON_TEXT_ENTRIES:
        if code == reason_code:
            return text
    return "Unknown Daily Gate decision policy result."


def _decision(
    *,
    decision: str,
    evidence_policy_allowed: bool,
    conservative_block_requested: bool,
    conservative_block_reason_present: bool,
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
        "conservative_block_requested": conservative_block_requested,
        "conservative_block_reason_present": (
            conservative_block_reason_present
        ),
        "decision_violations": decision_violations,
        "invariant_refs": _POLICY_INVARIANTS,
    }


def explain_daily_gate_decision_policy(
    *,
    decision: str,
    evidence_policy_allowed: bool,
    conservative_block_requested: bool,
    conservative_block_reason_present: bool,
) -> dict[str, object]:
    """Explain caller-supplied Daily Gate decision consistency."""
    decision_missing = decision.strip() == ""
    decision_unknown = (
        decision_missing is False
        and decision not in (gates.PASS, gates.BLOCKED)
    )
    prioritized_violations = (
        (decision_missing, DAILY_GATE_DECISION_MISSING),
        (decision_unknown, DAILY_GATE_DECISION_UNKNOWN),
        (
            conservative_block_reason_present is True
            and conservative_block_requested is False,
            CONSERVATIVE_BLOCK_REASON_WITHOUT_REQUEST,
        ),
        (
            decision == gates.PASS
            and evidence_policy_allowed is False,
            PASS_WITH_EVIDENCE_POLICY_BLOCKED,
        ),
        (
            decision == gates.PASS
            and conservative_block_requested is True,
            PASS_WITH_CONSERVATIVE_BLOCK_REQUESTED,
        ),
        (
            decision == gates.BLOCKED
            and evidence_policy_allowed is True
            and conservative_block_requested is False,
            (
                BLOCKED_WITH_EVIDENCE_POLICY_ALLOWED_WITHOUT_CONSERVATIVE_BLOCK
            ),
        ),
        (
            decision == gates.BLOCKED
            and conservative_block_requested is True
            and conservative_block_reason_present is False,
            BLOCKED_WITH_CONSERVATIVE_BLOCK_REASON_MISSING,
        ),
    )
    decision_violations = tuple(
        reason_code
        for condition, reason_code in prioritized_violations
        if condition
    )
    allowed = len(decision_violations) == 0
    reason_code = (
        DAILY_GATE_DECISION_ALLOWED
        if allowed
        else decision_violations[0]
    )

    return _decision(
        decision=decision,
        evidence_policy_allowed=evidence_policy_allowed,
        conservative_block_requested=conservative_block_requested,
        conservative_block_reason_present=(
            conservative_block_reason_present
        ),
        allowed=allowed,
        reason_code=reason_code,
        decision_violations=decision_violations,
    )


def is_daily_gate_decision_allowed(
    *,
    decision: str,
    evidence_policy_allowed: bool,
    conservative_block_requested: bool,
    conservative_block_reason_present: bool,
) -> bool:
    """Return only the boolean result from the decision explanation."""
    return bool(
        explain_daily_gate_decision_policy(
            decision=decision,
            evidence_policy_allowed=evidence_policy_allowed,
            conservative_block_requested=conservative_block_requested,
            conservative_block_reason_present=(
                conservative_block_reason_present
            ),
        )["allowed"]
    )
