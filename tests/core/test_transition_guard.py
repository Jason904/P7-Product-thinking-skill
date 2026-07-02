"""Focused contract tests for the pure transition guard."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import states
from ai_daily_publishing_system.core.transition_guard import (
    explain_transition,
    is_allowed_transition,
)


REQUIRED_DECISION_FIELDS = {
    "from_state",
    "to_state",
    "allowed",
    "reason_code",
    "reason",
    "source",
    "invariant_refs",
}


def _snapshot_catalog(catalog):
    return tuple(tuple(transition.items()) for transition in catalog)


def test_allowed_catalog_transitions_are_allowed():
    for transition in states.ALLOWED_TRANSITIONS:
        result = explain_transition(
            transition["from_state"],
            transition["to_state"],
        )

        assert result["allowed"] is True
        assert result["reason_code"] == "ALLOWED_TRANSITION"
        assert result["source"] == "states.ALLOWED_TRANSITIONS"


def test_forbidden_catalog_transitions_are_blocked():
    for transition in states.FORBIDDEN_TRANSITIONS:
        result = explain_transition(
            transition["from_state"],
            transition["to_state"],
        )

        assert result["allowed"] is False
        assert result["reason_code"] == "FORBIDDEN_TRANSITION"
        assert result["source"] == "states.FORBIDDEN_TRANSITIONS"

    terminal_family_result = explain_transition(
        states.NOOP_COMPLETED,
        states.RETRIEVING,
    )
    assert terminal_family_result["allowed"] is False
    assert terminal_family_result["reason_code"] == "FORBIDDEN_TRANSITION"
    assert terminal_family_result["source"] == "states.FORBIDDEN_TRANSITIONS"


def test_unknown_states_are_blocked():
    unknown_from = explain_transition("UNKNOWN_FROM_STATE", states.RETRIEVING)
    unknown_to = explain_transition(states.RETRIEVING, "UNKNOWN_TO_STATE")

    assert unknown_from["allowed"] is False
    assert unknown_from["reason_code"] == "UNKNOWN_STATE"
    assert unknown_to["allowed"] is False
    assert unknown_to["reason_code"] == "UNKNOWN_STATE"


def test_pass_published_is_blocked():
    pass_published = states.PASS_PUBLISHED_EXTERNAL_LABEL

    unknown_source_result = explain_transition(
        pass_published,
        states.SCHEDULED_OR_STARTED,
    )
    unknown_destination_result = explain_transition(
        states.SCHEDULED_OR_STARTED,
        pass_published,
    )
    publish_allowed_result = explain_transition(
        states.PUBLISH_ALLOWED,
        pass_published,
    )
    noop_completed_result = explain_transition(
        states.NOOP_COMPLETED,
        pass_published,
    )

    assert unknown_source_result["allowed"] is False
    assert unknown_source_result["reason_code"] == "PASS_PUBLISHED_EXCLUDED"
    assert unknown_destination_result["allowed"] is False
    assert unknown_destination_result["reason_code"] == "PASS_PUBLISHED_EXCLUDED"
    assert publish_allowed_result["allowed"] is False
    assert noop_completed_result["allowed"] is False
    assert "PASS_PUBLISHED excluded from MVP state enum" in (
        unknown_destination_result["invariant_refs"]
    )
    assert "NOOP_COMPLETED != PASS_PUBLISHED" in (
        unknown_destination_result["invariant_refs"]
    )


def test_blocked_failed_success_claims_are_blocked():
    blocked_failed_claims = (
        (states.CONFIG_BLOCKED, states.NOOP_COMPLETED),
        (states.REVIEW_BLOCKED, states.NOOP_COMPLETED),
        (states.SYSTEM_FAILED, states.PUBLISH_ALLOWED),
        (states.ADAPTER_FAILED, states.PUBLISH_ALLOWED),
    )

    for from_state, to_state in blocked_failed_claims:
        result = explain_transition(from_state, to_state)

        assert result["allowed"] is False
        assert (
            result["reason_code"]
            == "BLOCKED_FAILED_SUCCESS_CLAIM_FORBIDDEN"
        )


def test_public_url_claims_are_blocked():
    destination_claim = explain_transition(
        states.SCHEDULED_OR_STARTED,
        "public_url_claim_requested",
    )
    source_claim = explain_transition(
        "PUBLIC_URL_CREATED",
        states.SCHEDULED_OR_STARTED,
    )

    assert destination_claim["allowed"] is False
    assert destination_claim["reason_code"] == "PUBLIC_URL_CLAIM_FORBIDDEN"
    assert source_claim["allowed"] is False
    assert source_claim["reason_code"] == "PUBLIC_URL_CLAIM_FORBIDDEN"


def test_result_shape_is_stable():
    result = explain_transition(
        states.SCHEDULED_OR_STARTED,
        states.RETRIEVING,
    )

    assert set(result) == REQUIRED_DECISION_FIELDS
    assert result["from_state"] == states.SCHEDULED_OR_STARTED
    assert result["to_state"] == states.RETRIEVING


def test_is_allowed_transition_matches_explain_transition():
    transitions = (
        (states.SCHEDULED_OR_STARTED, states.RETRIEVING),
        (states.SCHEDULED_OR_STARTED, states.NOOP_COMPLETED),
        (states.RETRIEVING, states.VALIDATING),
    )

    for from_state, to_state in transitions:
        assert is_allowed_transition(from_state, to_state) == (
            explain_transition(from_state, to_state)["allowed"]
        )


def test_transition_guard_does_not_mutate_static_contracts():
    allowed_before = _snapshot_catalog(states.ALLOWED_TRANSITIONS)
    forbidden_before = _snapshot_catalog(states.FORBIDDEN_TRANSITIONS)
    mvp_states_before = states.MVP_STATES
    invariants_before = states.STATE_INVARIANTS

    explain_transition(states.SCHEDULED_OR_STARTED, states.RETRIEVING)
    explain_transition(
        states.NOOP_COMPLETED,
        states.PASS_PUBLISHED_EXTERNAL_LABEL,
    )
    is_allowed_transition(states.RETRIEVING, "UNKNOWN_TO_STATE")

    assert _snapshot_catalog(states.ALLOWED_TRANSITIONS) == allowed_before
    assert _snapshot_catalog(states.FORBIDDEN_TRANSITIONS) == forbidden_before
    assert states.MVP_STATES == mvp_states_before
    assert states.STATE_INVARIANTS == invariants_before
