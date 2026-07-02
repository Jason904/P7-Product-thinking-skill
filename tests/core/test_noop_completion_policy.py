"""Focused contract tests for the pure noop completion policy guard."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import noop_completion_policy
from ai_daily_publishing_system.core import states
from ai_daily_publishing_system.core import transition_guard


REQUIRED_DECISION_FIELDS = {
    "from_state",
    "to_state",
    "allowed",
    "reason_code",
    "reason",
    "source",
    "publish_mode",
    "public_url",
    "public_url_created",
    "transition_guard_result",
    "invariant_refs",
}


def _snapshot_catalog(catalog):
    return tuple(tuple(transition.items()) for transition in catalog)


def test_valid_noop_completion_policy_is_allowed():
    result = noop_completion_policy.explain_noop_completion_policy(
        states.PUBLISH_ALLOWED,
        "noop",
        None,
        False,
    )

    assert result["allowed"] is True
    assert result["reason_code"] == "NOOP_COMPLETION_ALLOWED"
    assert result["from_state"] == states.PUBLISH_ALLOWED
    assert result["to_state"] == states.NOOP_COMPLETED
    assert result["publish_mode"] == "noop"
    assert result["public_url"] is None
    assert result["public_url_created"] is False


def test_transition_guard_result_matches_direct_guard_call():
    result = noop_completion_policy.explain_noop_completion_policy(
        states.PUBLISH_ALLOWED,
        "noop",
        None,
        False,
    )

    assert result["transition_guard_result"] == (
        transition_guard.explain_transition(
            states.PUBLISH_ALLOWED,
            states.NOOP_COMPLETED,
        )
    )


def test_invalid_from_state_is_blocked():
    result = noop_completion_policy.explain_noop_completion_policy(
        states.SCHEDULED_OR_STARTED,
        "noop",
        None,
        False,
    )

    assert result["allowed"] is False
    assert result["reason_code"] == "INVALID_FROM_STATE"
    assert result["to_state"] == states.NOOP_COMPLETED
    assert result["transition_guard_result"] is not None
    assert result["transition_guard_result"]["allowed"] is False


def test_transition_guard_blocked_case_uses_documented_priority():
    result = noop_completion_policy.explain_noop_completion_policy(
        states.AUDITING,
        "noop",
        None,
        False,
    )

    assert result["transition_guard_result"] == (
        transition_guard.explain_transition(
            states.AUDITING,
            states.NOOP_COMPLETED,
        )
    )
    assert result["transition_guard_result"]["allowed"] is False
    assert result["reason_code"] == "INVALID_FROM_STATE"
    assert result["reason_code"] != "TRANSITION_GUARD_BLOCKED"


def test_non_noop_publish_mode_is_blocked():
    result = noop_completion_policy.explain_noop_completion_policy(
        states.PUBLISH_ALLOWED,
        "real",
        None,
        False,
    )

    assert result["allowed"] is False
    assert result["reason_code"] == "NON_NOOP_PUBLISH_MODE"
    assert result["to_state"] == states.NOOP_COMPLETED


def test_public_url_non_null_is_blocked():
    public_url_marker = "caller-supplied-public-url-marker"

    result = noop_completion_policy.explain_noop_completion_policy(
        states.PUBLISH_ALLOWED,
        "noop",
        public_url_marker,
        False,
    )

    assert result["allowed"] is False
    assert result["reason_code"] == "PUBLIC_URL_NON_NULL"
    assert result["public_url"] == public_url_marker


def test_public_url_created_true_is_blocked():
    result = noop_completion_policy.explain_noop_completion_policy(
        states.PUBLISH_ALLOWED,
        "noop",
        None,
        True,
    )

    assert result["allowed"] is False
    assert result["reason_code"] == "PUBLIC_URL_CREATED_TRUE"
    assert result["public_url"] is None
    assert result["public_url_created"] is True


def test_pass_published_is_never_produced():
    cases = (
        (states.PUBLISH_ALLOWED, "noop", None, False),
        (states.SCHEDULED_OR_STARTED, "noop", None, False),
        (states.PUBLISH_ALLOWED, "real", None, False),
        (states.PUBLISH_ALLOWED, "noop", "non-null-marker", False),
        (states.PUBLISH_ALLOWED, "noop", None, True),
    )

    for from_state, publish_mode, public_url, public_url_created in cases:
        result = noop_completion_policy.explain_noop_completion_policy(
            from_state,
            publish_mode,
            public_url,
            public_url_created,
        )

        assert result["to_state"] == states.NOOP_COMPLETED
        assert result["to_state"] != states.PASS_PUBLISHED_EXTERNAL_LABEL


def test_no_publish_notification_or_public_url_behavior_is_implied():
    result = noop_completion_policy.explain_noop_completion_policy(
        states.PUBLISH_ALLOWED,
        "noop",
        None,
        False,
    )

    forbidden_behavior_keys = {
        "published",
        "publisher",
        "notified",
        "notification_sent",
        "public_url_reserved",
        "public_url_generated",
    }

    assert forbidden_behavior_keys.isdisjoint(result)
    assert result["public_url"] is None
    assert result["public_url_created"] is False


def test_is_noop_completion_allowed_matches_explanation():
    cases = (
        (states.PUBLISH_ALLOWED, "noop", None, False),
        (states.SCHEDULED_OR_STARTED, "noop", None, False),
        (states.PUBLISH_ALLOWED, "real", None, False),
        (states.PUBLISH_ALLOWED, "noop", "non-null-marker", False),
        (states.PUBLISH_ALLOWED, "noop", None, True),
    )

    for from_state, publish_mode, public_url, public_url_created in cases:
        explanation = noop_completion_policy.explain_noop_completion_policy(
            from_state,
            publish_mode,
            public_url,
            public_url_created,
        )
        assert (
            noop_completion_policy.is_noop_completion_allowed(
                from_state,
                publish_mode,
                public_url,
                public_url_created,
            )
            is explanation["allowed"]
        )


def test_result_shape_is_stable():
    result = noop_completion_policy.explain_noop_completion_policy(
        states.PUBLISH_ALLOWED,
        "noop",
        None,
        False,
    )

    assert set(result) == REQUIRED_DECISION_FIELDS


def test_policy_guard_does_not_mutate_static_contracts():
    mvp_states_before = states.MVP_STATES
    allowed_before = _snapshot_catalog(states.ALLOWED_TRANSITIONS)
    forbidden_before = _snapshot_catalog(states.FORBIDDEN_TRANSITIONS)

    noop_completion_policy.explain_noop_completion_policy(
        states.PUBLISH_ALLOWED,
        "noop",
        None,
        False,
    )
    noop_completion_policy.explain_noop_completion_policy(
        states.SCHEDULED_OR_STARTED,
        "noop",
        None,
        False,
    )
    noop_completion_policy.is_noop_completion_allowed(
        states.PUBLISH_ALLOWED,
        "noop",
        "non-null-marker",
        True,
    )

    assert states.MVP_STATES == mvp_states_before
    assert _snapshot_catalog(states.ALLOWED_TRANSITIONS) == allowed_before
    assert _snapshot_catalog(states.FORBIDDEN_TRANSITIONS) == forbidden_before
