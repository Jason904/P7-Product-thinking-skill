"""Focused contract tests for the pure badcase creation policy guard."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import badcase_creation_policy
from ai_daily_publishing_system.core import states
from ai_daily_publishing_system.core import transition_guard


REQUIRED_DECISION_FIELDS = {
    "from_state",
    "to_state",
    "allowed",
    "reason_code",
    "reason",
    "source",
    "trigger",
    "evidence_marker_present",
    "config_blocker_persistent_or_user_reported",
    "transition_guard_result",
    "invariant_refs",
}


def _snapshot_catalog(catalog):
    return tuple(tuple(transition.items()) for transition in catalog)


def test_config_blocked_badcase_creation_is_allowed_with_required_marker():
    triggers = (
        "persistent_config_blocker",
        "user_reported_config_blocker",
    )

    for trigger in triggers:
        result = badcase_creation_policy.explain_badcase_creation_policy(
            states.CONFIG_BLOCKED,
            trigger,
            True,
            True,
        )

        assert result["allowed"] is True
        assert result["reason_code"] == "BADCASE_CREATION_ALLOWED"
        assert result["from_state"] == states.CONFIG_BLOCKED
        assert result["to_state"] == states.BADCASE_CREATED
        assert result["trigger"] == trigger
        assert result["evidence_marker_present"] is True
        assert (
            result["config_blocker_persistent_or_user_reported"] is True
        )


def test_review_blocked_badcase_creation_is_allowed():
    result = badcase_creation_policy.explain_badcase_creation_policy(
        states.REVIEW_BLOCKED,
        "review_blocked",
        True,
        False,
    )

    assert result["allowed"] is True
    assert result["reason_code"] == "BADCASE_CREATION_ALLOWED"
    assert result["from_state"] == states.REVIEW_BLOCKED
    assert result["to_state"] == states.BADCASE_CREATED


def test_system_failed_badcase_creation_is_allowed():
    result = badcase_creation_policy.explain_badcase_creation_policy(
        states.SYSTEM_FAILED,
        "system_failed",
        True,
        False,
    )

    assert result["allowed"] is True
    assert result["reason_code"] == "BADCASE_CREATION_ALLOWED"
    assert result["from_state"] == states.SYSTEM_FAILED
    assert result["to_state"] == states.BADCASE_CREATED


def test_adapter_failed_badcase_creation_is_allowed():
    result = badcase_creation_policy.explain_badcase_creation_policy(
        states.ADAPTER_FAILED,
        "adapter_failed",
        True,
        False,
    )

    assert result["allowed"] is True
    assert result["reason_code"] == "BADCASE_CREATION_ALLOWED"
    assert result["from_state"] == states.ADAPTER_FAILED
    assert result["to_state"] == states.BADCASE_CREATED


def test_transition_guard_result_matches_direct_guard_call():
    cases = (
        (states.CONFIG_BLOCKED, "persistent_config_blocker", True),
        (states.REVIEW_BLOCKED, "review_blocked", False),
        (states.SYSTEM_FAILED, "system_failed", False),
        (states.ADAPTER_FAILED, "adapter_failed", False),
        (states.SCHEDULED_OR_STARTED, "system_failed", False),
    )

    for from_state, trigger, config_marker in cases:
        result = badcase_creation_policy.explain_badcase_creation_policy(
            from_state,
            trigger,
            True,
            config_marker,
        )

        assert result["transition_guard_result"] == (
            transition_guard.explain_transition(
                from_state,
                states.BADCASE_CREATED,
            )
        )


def test_active_states_are_blocked():
    for from_state in states.ACTIVE_STATES:
        result = badcase_creation_policy.explain_badcase_creation_policy(
            from_state,
            "system_failed",
            True,
            False,
        )

        assert result["allowed"] is False
        assert result["reason_code"] == "ACTIVE_STATE_FORBIDDEN"
        assert result["to_state"] == states.BADCASE_CREATED


def test_publish_allowed_and_noop_completed_are_success_forbidden():
    cases = (
        states.PUBLISH_ALLOWED,
        states.NOOP_COMPLETED,
    )

    for from_state in cases:
        result = badcase_creation_policy.explain_badcase_creation_policy(
            from_state,
            "system_failed",
            True,
            False,
        )

        assert result["allowed"] is False
        assert result["reason_code"] == "SUCCESS_STATE_FORBIDDEN"
        assert result["to_state"] == states.BADCASE_CREATED


def test_badcase_created_is_already_created():
    result = badcase_creation_policy.explain_badcase_creation_policy(
        states.BADCASE_CREATED,
        "system_failed",
        True,
        False,
    )

    assert result["allowed"] is False
    assert result["reason_code"] == "BADCASE_ALREADY_CREATED"
    assert result["to_state"] == states.BADCASE_CREATED


def test_unknown_state_is_invalid():
    result = badcase_creation_policy.explain_badcase_creation_policy(
        "UNKNOWN_FROM_STATE",
        "system_failed",
        True,
        False,
    )

    assert result["allowed"] is False
    assert result["reason_code"] == "INVALID_FROM_STATE"
    assert result["to_state"] == states.BADCASE_CREATED


def test_config_blocked_requires_persistent_or_user_reported_marker():
    result = badcase_creation_policy.explain_badcase_creation_policy(
        states.CONFIG_BLOCKED,
        "persistent_config_blocker",
        True,
        False,
    )

    assert result["allowed"] is False
    assert result["reason_code"] == "CONFIG_BLOCKER_CONDITION_NOT_MET"
    assert result["to_state"] == states.BADCASE_CREATED


def test_missing_trigger_is_blocked():
    for trigger in ("", "   "):
        result = badcase_creation_policy.explain_badcase_creation_policy(
            states.REVIEW_BLOCKED,
            trigger,
            True,
            False,
        )

        assert result["allowed"] is False
        assert result["reason_code"] == "MISSING_TRIGGER"
        assert result["to_state"] == states.BADCASE_CREATED


def test_unknown_trigger_is_blocked():
    result = badcase_creation_policy.explain_badcase_creation_policy(
        states.REVIEW_BLOCKED,
        "manual_badcase",
        True,
        False,
    )

    assert result["allowed"] is False
    assert result["reason_code"] == "UNKNOWN_TRIGGER"
    assert result["to_state"] == states.BADCASE_CREATED


def test_missing_evidence_marker_is_blocked():
    result = badcase_creation_policy.explain_badcase_creation_policy(
        states.REVIEW_BLOCKED,
        "review_blocked",
        False,
        False,
    )

    assert result["allowed"] is False
    assert result["reason_code"] == "MISSING_EVIDENCE_MARKER"
    assert result["to_state"] == states.BADCASE_CREATED


def test_transition_guard_blocked_source_is_blocked():
    result = badcase_creation_policy.explain_badcase_creation_policy(
        states.SCHEDULED_OR_STARTED,
        "system_failed",
        True,
        False,
    )

    assert result["allowed"] is False
    assert result["reason_code"] == "TRANSITION_GUARD_BLOCKED"
    assert result["transition_guard_result"]["allowed"] is False
    assert result["to_state"] == states.BADCASE_CREATED


def test_pass_published_is_forbidden_and_never_produced():
    cases = (
        states.PASS_PUBLISHED_EXTERNAL_LABEL,
        "pass-published",
        "pass published",
        states.REVIEW_BLOCKED,
    )

    for from_state in cases:
        result = badcase_creation_policy.explain_badcase_creation_policy(
            from_state,
            "review_blocked",
            True,
            False,
        )

        assert result["to_state"] == states.BADCASE_CREATED
        assert result["to_state"] != states.PASS_PUBLISHED_EXTERNAL_LABEL

    pass_published_result = (
        badcase_creation_policy.explain_badcase_creation_policy(
            states.PASS_PUBLISHED_EXTERNAL_LABEL,
            "review_blocked",
            True,
            False,
        )
    )

    assert pass_published_result["allowed"] is False
    assert (
        pass_published_result["reason_code"]
        == "PASS_PUBLISHED_FORBIDDEN"
    )


def test_no_issue_record_artifact_hash_ledger_or_public_url_behavior_is_implied():
    result = badcase_creation_policy.explain_badcase_creation_policy(
        states.REVIEW_BLOCKED,
        "review_blocked",
        True,
        False,
    )

    forbidden_behavior_keys = {
        "issue_created",
        "issue_url",
        "badcase_record_written",
        "artifact_read",
        "artifact_written",
        "ledger_read",
        "ledger_written",
        "hash_calculated",
        "published",
        "publisher",
        "notified",
        "notification_sent",
        "public_url",
        "public_url_created",
        "public_url_reserved",
        "public_url_generated",
    }

    assert forbidden_behavior_keys.isdisjoint(result)
    assert result["to_state"] == states.BADCASE_CREATED


def test_is_badcase_creation_allowed_matches_explanation():
    cases = (
        (states.CONFIG_BLOCKED, "persistent_config_blocker", True, True),
        (states.REVIEW_BLOCKED, "review_blocked", True, False),
        (states.SYSTEM_FAILED, "system_failed", True, False),
        (states.ADAPTER_FAILED, "adapter_failed", True, False),
        (states.REVIEW_BLOCKED, "", True, False),
        (states.REVIEW_BLOCKED, "unknown", True, False),
        (states.REVIEW_BLOCKED, "review_blocked", False, False),
        (states.CONFIG_BLOCKED, "persistent_config_blocker", True, False),
        (states.PUBLISH_ALLOWED, "system_failed", True, False),
    )

    for (
        from_state,
        trigger,
        evidence_marker_present,
        config_marker,
    ) in cases:
        explanation = (
            badcase_creation_policy.explain_badcase_creation_policy(
                from_state,
                trigger,
                evidence_marker_present,
                config_marker,
            )
        )
        assert (
            badcase_creation_policy.is_badcase_creation_allowed(
                from_state,
                trigger,
                evidence_marker_present,
                config_marker,
            )
            is explanation["allowed"]
        )


def test_result_shape_is_stable():
    result = badcase_creation_policy.explain_badcase_creation_policy(
        states.REVIEW_BLOCKED,
        "review_blocked",
        True,
        False,
    )

    assert set(result) == REQUIRED_DECISION_FIELDS
    assert result["from_state"] == states.REVIEW_BLOCKED
    assert result["to_state"] == states.BADCASE_CREATED


def test_policy_guard_does_not_mutate_static_contracts():
    mvp_states_before = states.MVP_STATES
    allowed_before = _snapshot_catalog(states.ALLOWED_TRANSITIONS)
    forbidden_before = _snapshot_catalog(states.FORBIDDEN_TRANSITIONS)

    badcase_creation_policy.explain_badcase_creation_policy(
        states.CONFIG_BLOCKED,
        "persistent_config_blocker",
        True,
        True,
    )
    badcase_creation_policy.explain_badcase_creation_policy(
        states.REVIEW_BLOCKED,
        "review_blocked",
        True,
        False,
    )
    badcase_creation_policy.explain_badcase_creation_policy(
        states.PUBLISH_ALLOWED,
        "system_failed",
        True,
        False,
    )
    badcase_creation_policy.is_badcase_creation_allowed(
        states.SYSTEM_FAILED,
        "system_failed",
        True,
        False,
    )

    assert states.MVP_STATES == mvp_states_before
    assert _snapshot_catalog(states.ALLOWED_TRANSITIONS) == allowed_before
    assert _snapshot_catalog(states.FORBIDDEN_TRANSITIONS) == forbidden_before
