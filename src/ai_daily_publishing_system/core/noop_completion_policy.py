"""Pure noop completion policy guard for the AI Daily Publishing System."""

from typing import Final

from ai_daily_publishing_system.core import states
from ai_daily_publishing_system.core import transition_guard


NOOP_COMPLETION_ALLOWED: Final[str] = "NOOP_COMPLETION_ALLOWED"
INVALID_FROM_STATE: Final[str] = "INVALID_FROM_STATE"
TRANSITION_GUARD_BLOCKED: Final[str] = "TRANSITION_GUARD_BLOCKED"
NON_NOOP_PUBLISH_MODE: Final[str] = "NON_NOOP_PUBLISH_MODE"
PUBLIC_URL_NON_NULL: Final[str] = "PUBLIC_URL_NON_NULL"
PUBLIC_URL_CREATED_TRUE: Final[str] = "PUBLIC_URL_CREATED_TRUE"

_POLICY_SOURCE: Final[str] = (
    "noop_completion_policy.explain_noop_completion_policy"
)
_TRANSITION_GUARD_SOURCE: Final[str] = "transition_guard.explain_transition"
_NOOP_PUBLISH_MODE: Final[str] = "noop"
_NOOP_COMPLETION_INVARIANTS: Final[tuple[str, ...]] = (
    states.STATE_INVARIANTS
)


def _decision(
    from_state: str,
    allowed: bool,
    reason_code: str,
    reason: str,
    source: str,
    publish_mode: str,
    public_url: object,
    public_url_created: bool,
    transition_guard_result: dict[str, object],
) -> dict[str, object]:
    return {
        "from_state": from_state,
        "to_state": states.NOOP_COMPLETED,
        "allowed": allowed,
        "reason_code": reason_code,
        "reason": reason,
        "source": source,
        "publish_mode": publish_mode,
        "public_url": public_url,
        "public_url_created": public_url_created,
        "transition_guard_result": transition_guard_result,
        "invariant_refs": _NOOP_COMPLETION_INVARIANTS,
    }


def explain_noop_completion_policy(
    from_state: str,
    publish_mode: str,
    public_url: object,
    public_url_created: bool,
) -> dict[str, object]:
    """Return a static noop completion decision without side effects."""
    transition_guard_result = transition_guard.explain_transition(
        from_state,
        states.NOOP_COMPLETED,
    )

    if from_state != states.PUBLISH_ALLOWED:
        return _decision(
            from_state=from_state,
            allowed=False,
            reason_code=INVALID_FROM_STATE,
            reason=(
                "Only PUBLISH_ALLOWED can be considered for noop "
                "completion."
            ),
            source=_POLICY_SOURCE,
            publish_mode=publish_mode,
            public_url=public_url,
            public_url_created=public_url_created,
            transition_guard_result=transition_guard_result,
        )

    if not transition_guard_result["allowed"]:
        return _decision(
            from_state=from_state,
            allowed=False,
            reason_code=TRANSITION_GUARD_BLOCKED,
            reason=(
                "transition_guard.explain_transition blocked the "
                "candidate noop completion transition."
            ),
            source=_TRANSITION_GUARD_SOURCE,
            publish_mode=publish_mode,
            public_url=public_url,
            public_url_created=public_url_created,
            transition_guard_result=transition_guard_result,
        )

    if publish_mode != _NOOP_PUBLISH_MODE:
        return _decision(
            from_state=from_state,
            allowed=False,
            reason_code=NON_NOOP_PUBLISH_MODE,
            reason=(
                "Only noop publish_mode can complete the noop policy "
                "path; real publish is not implied."
            ),
            source=_POLICY_SOURCE,
            publish_mode=publish_mode,
            public_url=public_url,
            public_url_created=public_url_created,
            transition_guard_result=transition_guard_result,
        )

    if public_url is not None:
        return _decision(
            from_state=from_state,
            allowed=False,
            reason_code=PUBLIC_URL_NON_NULL,
            reason=(
                "Noop completion requires caller-supplied public_url "
                "to be None."
            ),
            source=_POLICY_SOURCE,
            publish_mode=publish_mode,
            public_url=public_url,
            public_url_created=public_url_created,
            transition_guard_result=transition_guard_result,
        )

    if public_url_created is True:
        return _decision(
            from_state=from_state,
            allowed=False,
            reason_code=PUBLIC_URL_CREATED_TRUE,
            reason=(
                "Noop completion requires caller-supplied "
                "public_url_created to be False."
            ),
            source=_POLICY_SOURCE,
            publish_mode=publish_mode,
            public_url=public_url,
            public_url_created=public_url_created,
            transition_guard_result=transition_guard_result,
        )

    return _decision(
        from_state=from_state,
        allowed=True,
        reason_code=NOOP_COMPLETION_ALLOWED,
        reason=(
            "Caller-supplied noop policy fields allow the static noop "
            "completion result; no transition, publish, notification, "
            "ledger, or URL action is executed."
        ),
        source=_POLICY_SOURCE,
        publish_mode=publish_mode,
        public_url=public_url,
        public_url_created=public_url_created,
        transition_guard_result=transition_guard_result,
    )


def is_noop_completion_allowed(
    from_state: str,
    publish_mode: str,
    public_url: object,
    public_url_created: bool,
) -> bool:
    """Return only the boolean result from the noop policy explanation."""
    return bool(
        explain_noop_completion_policy(
            from_state,
            publish_mode,
            public_url,
            public_url_created,
        )["allowed"]
    )
