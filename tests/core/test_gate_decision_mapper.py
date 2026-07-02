"""Focused contract tests for the pure gate decision mapper."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import gate_decision_mapper
from ai_daily_publishing_system.core import gates
from ai_daily_publishing_system.core import states
from ai_daily_publishing_system.core import transition_guard


REQUIRED_DECISION_FIELDS = {
    "gate_name",
    "decision",
    "from_state",
    "to_state",
    "allowed",
    "reason_code",
    "reason",
    "source",
    "mapping_ref",
    "transition_guard_result",
    "invariant_refs",
}

CANONICAL_CASES = (
    (
        gates.ADAPTER_CONFIGURATION_GATE,
        gates.PASS,
        states.SCHEDULED_OR_STARTED,
        states.RETRIEVING,
    ),
    (
        gates.ADAPTER_CONFIGURATION_GATE,
        gates.BLOCKED,
        states.SCHEDULED_OR_STARTED,
        states.CONFIG_BLOCKED,
    ),
    (
        gates.DAILY_PUBLISH_GATE,
        gates.PASS,
        states.AUDITING,
        states.PUBLISH_ALLOWED,
    ),
    (
        gates.DAILY_PUBLISH_GATE,
        gates.BLOCKED,
        states.AUDITING,
        states.REVIEW_BLOCKED,
    ),
)


def _snapshot_mapping(mapping):
    return tuple(mapping.items())


def _snapshot_catalog(catalog):
    return tuple(tuple(record.items()) for record in catalog)


def test_canonical_gate_decision_mappings_are_allowed():
    for gate_name, decision, from_state, to_state in CANONICAL_CASES:
        result = gate_decision_mapper.explain_gate_decision_transition(
            gate_name,
            decision,
            from_state,
        )

        assert set(result) == REQUIRED_DECISION_FIELDS
        assert result["gate_name"] == gate_name
        assert result["decision"] == decision
        assert result["from_state"] == from_state
        assert result["to_state"] == to_state
        assert result["allowed"] is True
        assert (
            result["reason_code"]
            == "GATE_DECISION_TRANSITION_ALLOWED"
        )
        assert result["mapping_ref"] == (gate_name, decision)


def test_nested_transition_guard_result_matches_direct_explanation():
    for gate_name, decision, from_state, to_state in CANONICAL_CASES:
        result = gate_decision_mapper.explain_gate_decision_transition(
            gate_name,
            decision,
            from_state,
        )

        assert result["transition_guard_result"] == (
            transition_guard.explain_transition(from_state, to_state)
        )


def test_transition_guard_result_is_present_for_every_declared_candidate_mapping():
    for gate_name, decision in gates.GATE_TO_STATE_MAPPINGS:
        result = gate_decision_mapper.explain_gate_decision_transition(
            gate_name,
            decision,
            states.SCHEDULED_OR_STARTED,
        )

        assert result["to_state"] is not None
        assert result["transition_guard_result"] is not None


def test_wrong_from_state_is_blocked_by_transition_guard():
    result = gate_decision_mapper.explain_gate_decision_transition(
        gates.DAILY_PUBLISH_GATE,
        gates.PASS,
        states.SCHEDULED_OR_STARTED,
    )

    assert result["to_state"] == states.PUBLISH_ALLOWED
    assert result["allowed"] is False
    assert result["reason_code"] == "TRANSITION_GUARD_BLOCKED"
    assert result["transition_guard_result"]["allowed"] is False


def test_unknown_gate_is_blocked_before_mapping():
    result = gate_decision_mapper.explain_gate_decision_transition(
        "Unknown Gate",
        gates.PASS,
        states.SCHEDULED_OR_STARTED,
    )

    assert result["allowed"] is False
    assert result["to_state"] is None
    assert result["reason_code"] == "UNKNOWN_GATE"
    assert result["mapping_ref"] is None
    assert result["transition_guard_result"] is None


def test_unknown_decision_is_blocked_before_mapping():
    result = gate_decision_mapper.explain_gate_decision_transition(
        gates.ADAPTER_CONFIGURATION_GATE,
        "UNKNOWN_DECISION_VALUE",
        states.SCHEDULED_OR_STARTED,
    )

    assert result["allowed"] is False
    assert result["to_state"] is None
    assert result["reason_code"] == "UNKNOWN_DECISION"
    assert result["mapping_ref"] is None
    assert result["transition_guard_result"] is None


def test_all_known_gate_decision_pairs_have_declared_mappings():
    known_pairs = {
        (gate_name, decision)
        for gate_name in gates.GATE_NAMES
        for decision in gates.GATE_DECISIONS
    }

    assert set(gates.GATE_TO_STATE_MAPPINGS) == known_pairs
    assert (
        gate_decision_mapper.GATE_MAPPING_NOT_DECLARED
        == "GATE_MAPPING_NOT_DECLARED"
    )


def test_boolean_wrapper_matches_explanation():
    cases = CANONICAL_CASES + (
        (
            gates.DAILY_PUBLISH_GATE,
            gates.PASS,
            states.SCHEDULED_OR_STARTED,
            states.PUBLISH_ALLOWED,
        ),
    )

    for gate_name, decision, from_state, _to_state in cases:
        explanation = (
            gate_decision_mapper.explain_gate_decision_transition(
                gate_name,
                decision,
                from_state,
            )
        )
        assert (
            gate_decision_mapper.is_allowed_gate_decision_transition(
                gate_name,
                decision,
                from_state,
            )
            is explanation["allowed"]
        )


def test_daily_pass_only_maps_to_publish_allowed():
    result = gate_decision_mapper.explain_gate_decision_transition(
        gates.DAILY_PUBLISH_GATE,
        gates.PASS,
        states.AUDITING,
    )

    assert result["to_state"] == states.PUBLISH_ALLOWED
    assert result["to_state"] != states.NOOP_COMPLETED
    assert result["to_state"] != states.PASS_PUBLISHED_EXTERNAL_LABEL


def test_canonical_mappings_are_disjoint_from_forbidden_mappings():
    forbidden_triples = {
        (
            mapping["gate_name"],
            mapping["decision"],
            mapping["forbidden_result"],
        )
        for mapping in gates.FORBIDDEN_GATE_MAPPINGS
        if mapping["gate_name"] != "any gate"
    }
    global_forbidden_targets = {
        mapping["forbidden_result"]
        for mapping in gates.FORBIDDEN_GATE_MAPPINGS
        if mapping["gate_name"] == "any gate"
    }

    for (gate_name, decision), to_state in (
        gates.GATE_TO_STATE_MAPPINGS.items()
    ):
        assert (gate_name, decision, to_state) not in forbidden_triples
        assert to_state not in global_forbidden_targets


def test_transition_guard_blocks_forbidden_daily_pass_targets():
    forbidden_targets = (
        states.NOOP_COMPLETED,
        states.PASS_PUBLISHED_EXTERNAL_LABEL,
        "public_url_creation",
    )

    for to_state in forbidden_targets:
        result = transition_guard.explain_transition(
            states.AUDITING,
            to_state,
        )

        assert result["allowed"] is False


def test_mapper_does_not_mutate_static_contracts():
    mappings_before = _snapshot_mapping(gates.GATE_TO_STATE_MAPPINGS)
    forbidden_mappings_before = _snapshot_catalog(
        gates.FORBIDDEN_GATE_MAPPINGS
    )
    gate_invariants_before = gates.GATE_INVARIANTS
    allowed_transitions_before = _snapshot_catalog(
        states.ALLOWED_TRANSITIONS
    )
    forbidden_transitions_before = _snapshot_catalog(
        states.FORBIDDEN_TRANSITIONS
    )

    for gate_name, decision, from_state, _to_state in CANONICAL_CASES:
        gate_decision_mapper.explain_gate_decision_transition(
            gate_name,
            decision,
            from_state,
        )
        gate_decision_mapper.is_allowed_gate_decision_transition(
            gate_name,
            decision,
            from_state,
        )

    gate_decision_mapper.explain_gate_decision_transition(
        "Unknown Gate",
        "Unknown Decision",
        "Unknown State",
    )

    assert _snapshot_mapping(
        gates.GATE_TO_STATE_MAPPINGS
    ) == mappings_before
    assert _snapshot_catalog(
        gates.FORBIDDEN_GATE_MAPPINGS
    ) == forbidden_mappings_before
    assert gates.GATE_INVARIANTS == gate_invariants_before
    assert _snapshot_catalog(
        states.ALLOWED_TRANSITIONS
    ) == allowed_transitions_before
    assert _snapshot_catalog(
        states.FORBIDDEN_TRANSITIONS
    ) == forbidden_transitions_before
