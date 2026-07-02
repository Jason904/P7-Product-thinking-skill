"""Pure gate-decision-to-transition mapping and explanation."""

from typing import Final, Optional

from ai_daily_publishing_system.core import gates
from ai_daily_publishing_system.core import transition_guard


GATE_DECISION_TRANSITION_ALLOWED: Final[str] = (
    "GATE_DECISION_TRANSITION_ALLOWED"
)
UNKNOWN_GATE: Final[str] = "UNKNOWN_GATE"
UNKNOWN_DECISION: Final[str] = "UNKNOWN_DECISION"
GATE_MAPPING_NOT_DECLARED: Final[str] = "GATE_MAPPING_NOT_DECLARED"
FORBIDDEN_GATE_MAPPING: Final[str] = "FORBIDDEN_GATE_MAPPING"
TRANSITION_GUARD_BLOCKED: Final[str] = "TRANSITION_GUARD_BLOCKED"

_GATE_NAMES_SOURCE: Final[str] = "gates.GATE_NAMES"
_GATE_DECISIONS_SOURCE: Final[str] = "gates.GATE_DECISIONS"
_GATE_MAPPINGS_SOURCE: Final[str] = "gates.GATE_TO_STATE_MAPPINGS"
_FORBIDDEN_MAPPINGS_SOURCE: Final[str] = "gates.FORBIDDEN_GATE_MAPPINGS"
_TRANSITION_GUARD_SOURCE: Final[str] = "transition_guard.explain_transition"


def _decision(
    gate_name: str,
    decision: str,
    from_state: str,
    to_state: Optional[str],
    allowed: bool,
    reason_code: str,
    reason: str,
    source: str,
    mapping_ref: Optional[tuple[str, str]],
    transition_guard_result: Optional[dict[str, object]],
    invariant_refs: tuple[str, ...],
) -> dict[str, object]:
    return {
        "gate_name": gate_name,
        "decision": decision,
        "from_state": from_state,
        "to_state": to_state,
        "allowed": allowed,
        "reason_code": reason_code,
        "reason": reason,
        "source": source,
        "mapping_ref": mapping_ref,
        "transition_guard_result": transition_guard_result,
        "invariant_refs": invariant_refs,
    }


def _find_forbidden_mapping(
    gate_name: str,
    decision: str,
    to_state: str,
):
    for mapping in gates.FORBIDDEN_GATE_MAPPINGS:
        gate_matches = mapping["gate_name"] in (gate_name, "any gate")
        decision_matches = mapping["decision"] in (decision, "any")
        target_matches = mapping["forbidden_result"] == to_state
        if gate_matches and decision_matches and target_matches:
            return mapping
    return None


def explain_gate_decision_transition(
    gate_name: str,
    decision: str,
    from_state: str,
) -> dict[str, object]:
    """Map an existing gate decision and explain transition eligibility."""
    if gate_name not in gates.GATE_NAMES:
        return _decision(
            gate_name=gate_name,
            decision=decision,
            from_state=from_state,
            to_state=None,
            allowed=False,
            reason_code=UNKNOWN_GATE,
            reason="The gate name is not declared in gates.GATE_NAMES.",
            source=_GATE_NAMES_SOURCE,
            mapping_ref=None,
            transition_guard_result=None,
            invariant_refs=(),
        )

    if decision not in gates.GATE_DECISIONS:
        return _decision(
            gate_name=gate_name,
            decision=decision,
            from_state=from_state,
            to_state=None,
            allowed=False,
            reason_code=UNKNOWN_DECISION,
            reason="The decision is not declared in gates.GATE_DECISIONS.",
            source=_GATE_DECISIONS_SOURCE,
            mapping_ref=None,
            transition_guard_result=None,
            invariant_refs=(),
        )

    mapping_ref = (gate_name, decision)
    to_state = gates.GATE_TO_STATE_MAPPINGS.get(mapping_ref)
    if to_state is None:
        return _decision(
            gate_name=gate_name,
            decision=decision,
            from_state=from_state,
            to_state=None,
            allowed=False,
            reason_code=GATE_MAPPING_NOT_DECLARED,
            reason=(
                "The gate and decision pair has no declared target state."
            ),
            source=_GATE_MAPPINGS_SOURCE,
            mapping_ref=mapping_ref,
            transition_guard_result=None,
            invariant_refs=gates.GATE_INVARIANTS,
        )

    transition_guard_result = transition_guard.explain_transition(
        from_state,
        to_state,
    )
    forbidden_mapping = _find_forbidden_mapping(
        gate_name,
        decision,
        to_state,
    )
    if forbidden_mapping is not None:
        return _decision(
            gate_name=gate_name,
            decision=decision,
            from_state=from_state,
            to_state=to_state,
            allowed=False,
            reason_code=FORBIDDEN_GATE_MAPPING,
            reason=forbidden_mapping["reason"],
            source=_FORBIDDEN_MAPPINGS_SOURCE,
            mapping_ref=mapping_ref,
            transition_guard_result=transition_guard_result,
            invariant_refs=gates.GATE_INVARIANTS,
        )

    if not transition_guard_result["allowed"]:
        return _decision(
            gate_name=gate_name,
            decision=decision,
            from_state=from_state,
            to_state=to_state,
            allowed=False,
            reason_code=TRANSITION_GUARD_BLOCKED,
            reason=(
                "The mapped transition was blocked by "
                "transition_guard.explain_transition."
            ),
            source=_TRANSITION_GUARD_SOURCE,
            mapping_ref=mapping_ref,
            transition_guard_result=transition_guard_result,
            invariant_refs=gates.GATE_INVARIANTS,
        )

    return _decision(
        gate_name=gate_name,
        decision=decision,
        from_state=from_state,
        to_state=to_state,
        allowed=True,
        reason_code=GATE_DECISION_TRANSITION_ALLOWED,
        reason=(
            "The gate decision mapping is declared and the transition "
            "guard allows the candidate transition."
        ),
        source=_GATE_MAPPINGS_SOURCE,
        mapping_ref=mapping_ref,
        transition_guard_result=transition_guard_result,
        invariant_refs=gates.GATE_INVARIANTS,
    )


def is_allowed_gate_decision_transition(
    gate_name: str,
    decision: str,
    from_state: str,
) -> bool:
    """Return only the boolean result from the gate decision explanation."""
    return bool(
        explain_gate_decision_transition(
            gate_name,
            decision,
            from_state,
        )["allowed"]
    )
