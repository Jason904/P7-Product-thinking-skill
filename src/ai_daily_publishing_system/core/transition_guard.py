"""Pure transition decisions for the AI Daily Publishing System state contract."""

from typing import Final

from ai_daily_publishing_system.core import states


ALLOWED_TRANSITION: Final[str] = "ALLOWED_TRANSITION"
FORBIDDEN_TRANSITION: Final[str] = "FORBIDDEN_TRANSITION"
UNKNOWN_STATE: Final[str] = "UNKNOWN_STATE"
PASS_PUBLISHED_EXCLUDED: Final[str] = "PASS_PUBLISHED_EXCLUDED"
UNDECLARED_TRANSITION: Final[str] = "UNDECLARED_TRANSITION"
BLOCKED_FAILED_SUCCESS_CLAIM_FORBIDDEN: Final[str] = (
    "BLOCKED_FAILED_SUCCESS_CLAIM_FORBIDDEN"
)
PUBLIC_URL_CLAIM_FORBIDDEN: Final[str] = "PUBLIC_URL_CLAIM_FORBIDDEN"

_ALLOWED_SOURCE: Final[str] = "states.ALLOWED_TRANSITIONS"
_FORBIDDEN_SOURCE: Final[str] = "states.FORBIDDEN_TRANSITIONS"
_MVP_STATES_SOURCE: Final[str] = "states.MVP_STATES"
_INVARIANTS_SOURCE: Final[str] = "states.STATE_INVARIANTS"

_BLOCKED_FAILED_STATES: Final[frozenset[str]] = frozenset(
    (
        states.CONFIG_BLOCKED,
        states.REVIEW_BLOCKED,
        states.SYSTEM_FAILED,
        states.ADAPTER_FAILED,
    )
)
_SUCCESS_CLAIM_STATES: Final[frozenset[str]] = frozenset(
    (
        states.PUBLISH_ALLOWED,
        states.NOOP_COMPLETED,
    )
)
_PASS_PUBLISHED_INVARIANTS: Final[tuple[str, ...]] = tuple(
    invariant
    for invariant in states.STATE_INVARIANTS
    if "PASS_PUBLISHED" in invariant
)
_PUBLIC_URL_INVARIANTS: Final[tuple[str, ...]] = tuple(
    invariant
    for invariant in states.STATE_INVARIANTS
    if "public URL" in invariant
)
_BLOCKED_FAILED_INVARIANTS: Final[tuple[str, ...]] = tuple(
    invariant
    for invariant in states.STATE_INVARIANTS
    if "blocked/failed" in invariant
)
_TERMINAL_TO_ACTIVE_INVARIANTS: Final[tuple[str, ...]] = tuple(
    invariant
    for invariant in states.STATE_INVARIANTS
    if "terminal-to-active" in invariant
)


def _find_exact_transition(catalog, from_state: str, to_state: str):
    for transition in catalog:
        if (
            transition["from_state"] == from_state
            and transition["to_state"] == to_state
        ):
            return transition
    return None


def _catalog_reason(transition) -> str:
    return f'{transition["reason_code"]}: {transition["notes"]}'


def _decision(
    from_state: str,
    to_state: str,
    allowed: bool,
    reason_code: str,
    reason: str,
    source: str,
    invariant_refs: tuple[str, ...],
) -> dict[str, object]:
    return {
        "from_state": from_state,
        "to_state": to_state,
        "allowed": allowed,
        "reason_code": reason_code,
        "reason": reason,
        "source": source,
        "invariant_refs": invariant_refs,
    }


def _is_public_url_claim_label(state_label: str) -> bool:
    normalized_label = state_label.lower().replace("-", "_").replace(" ", "_")
    return "public_url" in normalized_label


def explain_transition(from_state: str, to_state: str) -> dict[str, object]:
    """Return a static decision without executing or mutating a transition."""
    allowed_transition = _find_exact_transition(
        states.ALLOWED_TRANSITIONS,
        from_state,
        to_state,
    )
    if allowed_transition is not None:
        return _decision(
            from_state=from_state,
            to_state=to_state,
            allowed=True,
            reason_code=ALLOWED_TRANSITION,
            reason=_catalog_reason(allowed_transition),
            source=_ALLOWED_SOURCE,
            invariant_refs=(),
        )

    forbidden_transition = _find_exact_transition(
        states.FORBIDDEN_TRANSITIONS,
        from_state,
        to_state,
    )
    if forbidden_transition is not None:
        return _decision(
            from_state=from_state,
            to_state=to_state,
            allowed=False,
            reason_code=FORBIDDEN_TRANSITION,
            reason=_catalog_reason(forbidden_transition),
            source=_FORBIDDEN_SOURCE,
            invariant_refs=states.STATE_INVARIANTS,
        )

    if (
        from_state == states.PASS_PUBLISHED_EXTERNAL_LABEL
        or to_state == states.PASS_PUBLISHED_EXTERNAL_LABEL
    ):
        return _decision(
            from_state=from_state,
            to_state=to_state,
            allowed=False,
            reason_code=PASS_PUBLISHED_EXCLUDED,
            reason="PASS_PUBLISHED is excluded from the MVP state catalog.",
            source=_INVARIANTS_SOURCE,
            invariant_refs=_PASS_PUBLISHED_INVARIANTS,
        )

    if _is_public_url_claim_label(from_state) or _is_public_url_claim_label(
        to_state
    ):
        return _decision(
            from_state=from_state,
            to_state=to_state,
            allowed=False,
            reason_code=PUBLIC_URL_CLAIM_FORBIDDEN,
            reason="Public URL semantic claims are forbidden in the MVP.",
            source=_FORBIDDEN_SOURCE,
            invariant_refs=_PUBLIC_URL_INVARIANTS,
        )

    if from_state not in states.MVP_STATES or to_state not in states.MVP_STATES:
        return _decision(
            from_state=from_state,
            to_state=to_state,
            allowed=False,
            reason_code=UNKNOWN_STATE,
            reason="Both transition endpoints must be declared MVP states.",
            source=_MVP_STATES_SOURCE,
            invariant_refs=(),
        )

    if (
        from_state in _BLOCKED_FAILED_STATES
        and to_state in _SUCCESS_CLAIM_STATES
    ):
        return _decision(
            from_state=from_state,
            to_state=to_state,
            allowed=False,
            reason_code=BLOCKED_FAILED_SUCCESS_CLAIM_FORBIDDEN,
            reason="Blocked or failed states cannot claim success.",
            source=_INVARIANTS_SOURCE,
            invariant_refs=_BLOCKED_FAILED_INVARIANTS,
        )

    if (
        from_state in states.SAME_RUN_TERMINAL_TO_ACTIVE_SOURCE_STATES
        and to_state in states.SAME_RUN_TERMINAL_TO_ACTIVE_DESTINATION_STATES
    ):
        return _decision(
            from_state=from_state,
            to_state=to_state,
            allowed=False,
            reason_code=FORBIDDEN_TRANSITION,
            reason="Same-run terminal-to-active transitions are forbidden.",
            source=_FORBIDDEN_SOURCE,
            invariant_refs=_TERMINAL_TO_ACTIVE_INVARIANTS,
        )

    return _decision(
        from_state=from_state,
        to_state=to_state,
        allowed=False,
        reason_code=UNDECLARED_TRANSITION,
        reason="The transition is not declared in states.ALLOWED_TRANSITIONS.",
        source=_ALLOWED_SOURCE,
        invariant_refs=(),
    )


def is_allowed_transition(from_state: str, to_state: str) -> bool:
    """Return only the boolean decision from explain_transition."""
    return bool(explain_transition(from_state, to_state)["allowed"])
