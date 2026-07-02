"""Static import-only contract tests for state constants."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import states


def test_mvp_state_catalog_is_exact():
    expected_states = (
        "SCHEDULED_OR_STARTED",
        "CONFIG_BLOCKED",
        "RETRIEVING",
        "GENERATING",
        "RENDERING",
        "VALIDATING",
        "EVALUATING",
        "AUDITING",
        "PUBLISH_ALLOWED",
        "REVIEW_BLOCKED",
        "SYSTEM_FAILED",
        "ADAPTER_FAILED",
        "NOOP_COMPLETED",
        "BADCASE_CREATED",
    )

    assert states.MVP_STATES == expected_states
    assert len(states.MVP_STATES) == 14
    assert states.PASS_PUBLISHED_EXTERNAL_LABEL == "PASS_PUBLISHED"
    assert states.PASS_PUBLISHED_EXTERNAL_LABEL not in states.MVP_STATES


def test_state_category_partition_matches_catalog():
    expected_categories = {
        "initial": frozenset(("SCHEDULED_OR_STARTED",)),
        "active": frozenset(
            (
                "RETRIEVING",
                "GENERATING",
                "RENDERING",
                "VALIDATING",
                "EVALUATING",
                "AUDITING",
            )
        ),
        "intermediate_eligibility": frozenset(("PUBLISH_ALLOWED",)),
        "runtime_terminal_outcomes": frozenset(
            (
                "CONFIG_BLOCKED",
                "REVIEW_BLOCKED",
                "SYSTEM_FAILED",
                "ADAPTER_FAILED",
                "NOOP_COMPLETED",
            )
        ),
        "governance_follow_on": frozenset(("BADCASE_CREATED",)),
    }

    assert states.STATE_CATEGORIES == expected_categories

    partitioned_states = frozenset().union(*states.STATE_CATEGORIES.values())
    partitioned_count = sum(len(category) for category in states.STATE_CATEGORIES.values())

    assert partitioned_states == frozenset(states.MVP_STATES)
    assert partitioned_count == len(states.MVP_STATES)
    assert states.PUBLISH_ALLOWED not in states.RUNTIME_TERMINAL_STATES
    assert states.BADCASE_CREATED not in states.RUNTIME_TERMINAL_STATES


def test_failure_source_sets_match_contract():
    assert states.RUNTIME_FAILURE_SOURCE_STATES == frozenset(
        (
            "SCHEDULED_OR_STARTED",
            "RETRIEVING",
            "GENERATING",
            "RENDERING",
            "VALIDATING",
            "EVALUATING",
            "AUDITING",
            "PUBLISH_ALLOWED",
        )
    )
    assert states.ADAPTER_FAILURE_SOURCE_STATES == frozenset(
        (
            "RETRIEVING",
            "GENERATING",
            "RENDERING",
            "VALIDATING",
            "EVALUATING",
            "AUDITING",
            "PUBLISH_ALLOWED",
        )
    )
    assert "SCHEDULED_OR_STARTED" not in states.ADAPTER_FAILURE_SOURCE_STATES


def test_required_allowed_transitions_are_declared():
    allowed_edges = {
        (transition["from_state"], transition["to_state"], transition["condition"])
        for transition in states.ALLOWED_TRANSITIONS
    }

    required_base_edges = {
        (
            "SCHEDULED_OR_STARTED",
            "CONFIG_BLOCKED",
            "configuration_or_adapter_preflight_blocked",
        ),
        ("SCHEDULED_OR_STARTED", "RETRIEVING", "adapter_preflight_pass"),
        ("RETRIEVING", "GENERATING", "required_retrieval_contract_completed"),
        ("GENERATING", "RENDERING", "required_generation_contract_completed"),
        ("RENDERING", "VALIDATING", "required_rendering_contract_completed"),
        ("VALIDATING", "EVALUATING", "required_validation_contract_completed"),
        ("EVALUATING", "AUDITING", "rubric_pass"),
        ("EVALUATING", "REVIEW_BLOCKED", "rubric_blocked_or_invalid"),
        ("AUDITING", "REVIEW_BLOCKED", "audit_or_daily_publish_gate_blocked"),
        ("AUDITING", "PUBLISH_ALLOWED", "daily_publish_gate_pass"),
        ("PUBLISH_ALLOWED", "NOOP_COMPLETED", "noop_contract_completed"),
        ("CONFIG_BLOCKED", "BADCASE_CREATED", "persistent_or_user_reported"),
        ("REVIEW_BLOCKED", "BADCASE_CREATED", "badcase_required_for_terminal_outcome"),
        ("SYSTEM_FAILED", "BADCASE_CREATED", "badcase_required_for_terminal_outcome"),
        ("ADAPTER_FAILED", "BADCASE_CREATED", "badcase_required_for_terminal_outcome"),
    }
    required_runtime_failure_edges = {
        (source_state, "SYSTEM_FAILED", "runtime_failure_classified")
        for source_state in states.RUNTIME_FAILURE_SOURCE_STATES
    }
    required_adapter_failure_edges = {
        (source_state, "ADAPTER_FAILED", "adapter_preflight_passed_then_execution_failed")
        for source_state in states.ADAPTER_FAILURE_SOURCE_STATES
    }

    assert required_base_edges <= allowed_edges
    assert required_runtime_failure_edges <= allowed_edges
    assert required_adapter_failure_edges <= allowed_edges


def test_required_forbidden_transitions_are_declared():
    forbidden_edges = {
        (transition["from_state"], transition["to_state"])
        for transition in states.FORBIDDEN_TRANSITIONS
    }
    required_forbidden_edges = {
        ("SCHEDULED_OR_STARTED", "PUBLISH_ALLOWED"),
        ("SCHEDULED_OR_STARTED", "NOOP_COMPLETED"),
        ("CONFIG_BLOCKED", "RETRIEVING"),
        ("REVIEW_BLOCKED", "PUBLISH_ALLOWED"),
        ("SYSTEM_FAILED", "NOOP_COMPLETED"),
        ("ADAPTER_FAILED", "NOOP_COMPLETED"),
        ("PUBLISH_ALLOWED", "PASS_PUBLISHED"),
        ("NOOP_COMPLETED", "PASS_PUBLISHED"),
        ("runtime_terminal_outcome", "initial_active_or_intermediate_state"),
        ("any_state", "public_url_claim"),
    }

    assert required_forbidden_edges <= forbidden_edges


def test_transition_record_fields_are_declared():
    assert states.TRANSITION_RECORD_FIELDS == (
        "from_state",
        "to_state",
        "reason_code",
        "evidence_refs",
        "condition",
        "is_allowed",
        "source_of_truth",
        "notes",
    )

    for transition in states.ALLOWED_TRANSITIONS + states.FORBIDDEN_TRANSITIONS:
        assert tuple(transition.keys()) == states.TRANSITION_RECORD_FIELDS


def test_state_invariants_capture_mvp_boundaries():
    assert states.STATE_INVARIANTS == (
        "PASS_PUBLISHED excluded from MVP state enum",
        "NOOP_COMPLETED != PASS_PUBLISHED",
        "PUBLISH_ALLOWED is eligibility-only and non-terminal",
        "terminal-to-active same-run transitions forbidden",
        "blocked/failed states cannot claim success",
        "public URL creation/reservation/faking/implying is forbidden",
    )
