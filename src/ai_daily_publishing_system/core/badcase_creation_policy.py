"""Pure badcase creation policy guard for the AI Daily Publishing System."""

from typing import Final

from ai_daily_publishing_system.core import states
from ai_daily_publishing_system.core import transition_guard


BADCASE_CREATION_ALLOWED: Final[str] = "BADCASE_CREATION_ALLOWED"
INVALID_FROM_STATE: Final[str] = "INVALID_FROM_STATE"
TRANSITION_GUARD_BLOCKED: Final[str] = "TRANSITION_GUARD_BLOCKED"
UNKNOWN_TRIGGER: Final[str] = "UNKNOWN_TRIGGER"
MISSING_TRIGGER: Final[str] = "MISSING_TRIGGER"
MISSING_EVIDENCE_MARKER: Final[str] = "MISSING_EVIDENCE_MARKER"
CONFIG_BLOCKER_CONDITION_NOT_MET: Final[str] = (
    "CONFIG_BLOCKER_CONDITION_NOT_MET"
)
PASS_PUBLISHED_FORBIDDEN: Final[str] = "PASS_PUBLISHED_FORBIDDEN"
SUCCESS_STATE_FORBIDDEN: Final[str] = "SUCCESS_STATE_FORBIDDEN"
ACTIVE_STATE_FORBIDDEN: Final[str] = "ACTIVE_STATE_FORBIDDEN"
BADCASE_ALREADY_CREATED: Final[str] = "BADCASE_ALREADY_CREATED"

PERSISTENT_CONFIG_BLOCKER: Final[str] = "persistent_config_blocker"
USER_REPORTED_CONFIG_BLOCKER: Final[str] = "user_reported_config_blocker"
REVIEW_BLOCKED_TRIGGER: Final[str] = "review_blocked"
SYSTEM_FAILED_TRIGGER: Final[str] = "system_failed"
ADAPTER_FAILED_TRIGGER: Final[str] = "adapter_failed"

_POLICY_SOURCE: Final[str] = (
    "badcase_creation_policy.explain_badcase_creation_policy"
)
_TRANSITION_GUARD_SOURCE: Final[str] = "transition_guard.explain_transition"
_BADCASE_CREATION_TRIGGERS: Final[frozenset[str]] = frozenset(
    (
        PERSISTENT_CONFIG_BLOCKER,
        USER_REPORTED_CONFIG_BLOCKER,
        REVIEW_BLOCKED_TRIGGER,
        SYSTEM_FAILED_TRIGGER,
        ADAPTER_FAILED_TRIGGER,
    )
)
_BADCASE_CREATION_SOURCE_STATES: Final[frozenset[str]] = frozenset(
    (
        states.CONFIG_BLOCKED,
        states.REVIEW_BLOCKED,
        states.SYSTEM_FAILED,
        states.ADAPTER_FAILED,
    )
)
_SUCCESS_OR_ELIGIBILITY_STATES: Final[frozenset[str]] = frozenset(
    (
        states.PUBLISH_ALLOWED,
        states.NOOP_COMPLETED,
    )
)
_BADCASE_CREATION_INVARIANTS: Final[tuple[str, ...]] = (
    states.STATE_INVARIANTS
    + (
        "BADCASE_CREATED is governance follow-on, not runtime success",
        "NOOP_COMPLETED != BADCASE_CREATED",
        (
            "Badcase creation policy does not create issues, records, "
            "artifacts, ledgers, hashes, URLs, publish output, or "
            "notification output"
        ),
    )
)


def _decision(
    from_state: str,
    allowed: bool,
    reason_code: str,
    reason: str,
    source: str,
    trigger: str,
    evidence_marker_present: bool,
    config_blocker_persistent_or_user_reported: bool,
    transition_guard_result: dict[str, object],
) -> dict[str, object]:
    return {
        "from_state": from_state,
        "to_state": states.BADCASE_CREATED,
        "allowed": allowed,
        "reason_code": reason_code,
        "reason": reason,
        "source": source,
        "trigger": trigger,
        "evidence_marker_present": evidence_marker_present,
        "config_blocker_persistent_or_user_reported": (
            config_blocker_persistent_or_user_reported
        ),
        "transition_guard_result": transition_guard_result,
        "invariant_refs": _BADCASE_CREATION_INVARIANTS,
    }


def _is_pass_published_label(from_state: str) -> bool:
    normalized_state = from_state.strip().upper().replace("-", "_")
    normalized_state = normalized_state.replace(" ", "_")
    return normalized_state == states.PASS_PUBLISHED_EXTERNAL_LABEL


def explain_badcase_creation_policy(
    from_state: str,
    trigger: str,
    evidence_marker_present: bool,
    config_blocker_persistent_or_user_reported: bool,
) -> dict[str, object]:
    """Return a static badcase creation decision without side effects."""
    transition_guard_result = transition_guard.explain_transition(
        from_state,
        states.BADCASE_CREATED,
    )

    if _is_pass_published_label(from_state):
        return _decision(
            from_state=from_state,
            allowed=False,
            reason_code=PASS_PUBLISHED_FORBIDDEN,
            reason="PASS_PUBLISHED is excluded and cannot create badcases.",
            source=_POLICY_SOURCE,
            trigger=trigger,
            evidence_marker_present=evidence_marker_present,
            config_blocker_persistent_or_user_reported=(
                config_blocker_persistent_or_user_reported
            ),
            transition_guard_result=transition_guard_result,
        )

    if from_state in states.ACTIVE_STATES:
        return _decision(
            from_state=from_state,
            allowed=False,
            reason_code=ACTIVE_STATE_FORBIDDEN,
            reason=(
                "Active states must first reach a blocked or failed state "
                "before badcase creation can be considered."
            ),
            source=_POLICY_SOURCE,
            trigger=trigger,
            evidence_marker_present=evidence_marker_present,
            config_blocker_persistent_or_user_reported=(
                config_blocker_persistent_or_user_reported
            ),
            transition_guard_result=transition_guard_result,
        )

    if from_state in _SUCCESS_OR_ELIGIBILITY_STATES:
        return _decision(
            from_state=from_state,
            allowed=False,
            reason_code=SUCCESS_STATE_FORBIDDEN,
            reason=(
                "Eligibility or noop success states cannot create "
                "badcases."
            ),
            source=_POLICY_SOURCE,
            trigger=trigger,
            evidence_marker_present=evidence_marker_present,
            config_blocker_persistent_or_user_reported=(
                config_blocker_persistent_or_user_reported
            ),
            transition_guard_result=transition_guard_result,
        )

    if from_state == states.BADCASE_CREATED:
        return _decision(
            from_state=from_state,
            allowed=False,
            reason_code=BADCASE_ALREADY_CREATED,
            reason="BADCASE_CREATED cannot create another badcase.",
            source=_POLICY_SOURCE,
            trigger=trigger,
            evidence_marker_present=evidence_marker_present,
            config_blocker_persistent_or_user_reported=(
                config_blocker_persistent_or_user_reported
            ),
            transition_guard_result=transition_guard_result,
        )

    if from_state not in states.MVP_STATES:
        return _decision(
            from_state=from_state,
            allowed=False,
            reason_code=INVALID_FROM_STATE,
            reason="from_state must be declared in states.MVP_STATES.",
            source=_POLICY_SOURCE,
            trigger=trigger,
            evidence_marker_present=evidence_marker_present,
            config_blocker_persistent_or_user_reported=(
                config_blocker_persistent_or_user_reported
            ),
            transition_guard_result=transition_guard_result,
        )

    if trigger.strip() == "":
        return _decision(
            from_state=from_state,
            allowed=False,
            reason_code=MISSING_TRIGGER,
            reason="A non-empty badcase creation trigger is required.",
            source=_POLICY_SOURCE,
            trigger=trigger,
            evidence_marker_present=evidence_marker_present,
            config_blocker_persistent_or_user_reported=(
                config_blocker_persistent_or_user_reported
            ),
            transition_guard_result=transition_guard_result,
        )

    if trigger not in _BADCASE_CREATION_TRIGGERS:
        return _decision(
            from_state=from_state,
            allowed=False,
            reason_code=UNKNOWN_TRIGGER,
            reason="The badcase creation trigger is not recognized.",
            source=_POLICY_SOURCE,
            trigger=trigger,
            evidence_marker_present=evidence_marker_present,
            config_blocker_persistent_or_user_reported=(
                config_blocker_persistent_or_user_reported
            ),
            transition_guard_result=transition_guard_result,
        )

    if evidence_marker_present is False:
        return _decision(
            from_state=from_state,
            allowed=False,
            reason_code=MISSING_EVIDENCE_MARKER,
            reason=(
                "Caller-supplied evidence marker must be present before "
                "badcase creation can be considered."
            ),
            source=_POLICY_SOURCE,
            trigger=trigger,
            evidence_marker_present=evidence_marker_present,
            config_blocker_persistent_or_user_reported=(
                config_blocker_persistent_or_user_reported
            ),
            transition_guard_result=transition_guard_result,
        )

    if (
        from_state == states.CONFIG_BLOCKED
        and config_blocker_persistent_or_user_reported is False
    ):
        return _decision(
            from_state=from_state,
            allowed=False,
            reason_code=CONFIG_BLOCKER_CONDITION_NOT_MET,
            reason=(
                "CONFIG_BLOCKED requires a persistent or user-reported "
                "marker before badcase creation can be considered."
            ),
            source=_POLICY_SOURCE,
            trigger=trigger,
            evidence_marker_present=evidence_marker_present,
            config_blocker_persistent_or_user_reported=(
                config_blocker_persistent_or_user_reported
            ),
            transition_guard_result=transition_guard_result,
        )

    if not transition_guard_result["allowed"]:
        return _decision(
            from_state=from_state,
            allowed=False,
            reason_code=TRANSITION_GUARD_BLOCKED,
            reason=(
                "transition_guard.explain_transition blocked the candidate "
                "badcase creation transition."
            ),
            source=_TRANSITION_GUARD_SOURCE,
            trigger=trigger,
            evidence_marker_present=evidence_marker_present,
            config_blocker_persistent_or_user_reported=(
                config_blocker_persistent_or_user_reported
            ),
            transition_guard_result=transition_guard_result,
        )

    return _decision(
        from_state=from_state,
        allowed=True,
        reason_code=BADCASE_CREATION_ALLOWED,
        reason=(
            "Caller-supplied badcase policy fields allow the static "
            "BADCASE_CREATED result; no transition, issue, record, "
            "artifact, ledger, hash, URL, publish, or notification action "
            "is executed."
        ),
        source=_POLICY_SOURCE,
        trigger=trigger,
        evidence_marker_present=evidence_marker_present,
        config_blocker_persistent_or_user_reported=(
            config_blocker_persistent_or_user_reported
        ),
        transition_guard_result=transition_guard_result,
    )


def is_badcase_creation_allowed(
    from_state: str,
    trigger: str,
    evidence_marker_present: bool,
    config_blocker_persistent_or_user_reported: bool,
) -> bool:
    """Return only the boolean result from the badcase policy explanation."""
    return bool(
        explain_badcase_creation_policy(
            from_state,
            trigger,
            evidence_marker_present,
            config_blocker_persistent_or_user_reported,
        )["allowed"]
    )
