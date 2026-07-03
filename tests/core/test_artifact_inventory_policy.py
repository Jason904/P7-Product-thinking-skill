"""Focused contract tests for the pure artifact inventory policy guard."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import artifact_inventory_policy
from ai_daily_publishing_system.core import artifacts


REQUIRED_DECISION_FIELDS = {
    "allowed",
    "reason_code",
    "reason",
    "source",
    "artifact_names",
    "public_candidate_names",
    "daily_gate_input_names",
    "pre_gate_hash_evidence_present",
    "unknown_artifact_names",
    "public_candidate_violations",
    "private_public_leak_candidates",
    "post_gate_daily_input_violations",
    "missing_inventory_artifacts",
    "invariant_refs",
}


def _minimal_inventory():
    return (
        artifacts.READER_HTML_ARTIFACT,
        artifacts.ARTIFACT_HASH_ARTIFACT,
    )


def _explain(
    artifact_names=_minimal_inventory(),
    public_candidate_names=(artifacts.READER_HTML_ARTIFACT,),
    daily_gate_input_names=_minimal_inventory(),
    pre_gate_hash_evidence_present=True,
):
    return artifact_inventory_policy.explain_artifact_inventory_policy(
        artifact_names,
        public_candidate_names,
        daily_gate_input_names,
        pre_gate_hash_evidence_present,
    )


def test_valid_minimal_inventory_is_allowed():
    result = _explain()

    assert result["allowed"] is True
    assert result["reason_code"] == "ARTIFACT_INVENTORY_ALLOWED"
    assert result["artifact_names"] == _minimal_inventory()
    assert result["public_candidate_names"] == (
        artifacts.READER_HTML_ARTIFACT,
    )
    assert result["daily_gate_input_names"] == _minimal_inventory()
    assert result["pre_gate_hash_evidence_present"] is True


def test_reader_html_is_allowed_as_sole_public_candidate():
    result = _explain(
        artifact_names=(artifacts.READER_HTML_ARTIFACT,),
        public_candidate_names=(artifacts.READER_HTML_ARTIFACT,),
        daily_gate_input_names=(),
    )

    assert result["allowed"] is True
    assert result["reason_code"] == "ARTIFACT_INVENTORY_ALLOWED"
    assert result["public_candidate_violations"] == ()


def test_empty_inventory_is_blocked():
    result = _explain(
        artifact_names=(),
        public_candidate_names=(),
        daily_gate_input_names=(),
    )

    assert result["allowed"] is False
    assert result["reason_code"] == "EMPTY_ARTIFACT_INVENTORY"


def test_unknown_artifact_in_inventory_is_blocked():
    result = _explain(
        artifact_names=("unknown-artifact.yaml",),
        public_candidate_names=(),
        daily_gate_input_names=(),
    )

    assert result["allowed"] is False
    assert result["reason_code"] == "UNKNOWN_ARTIFACT"
    assert result["unknown_artifact_names"] == ("unknown-artifact.yaml",)


def test_unknown_public_candidate_is_blocked():
    result = _explain(
        artifact_names=(artifacts.READER_HTML_ARTIFACT,),
        public_candidate_names=("unknown-public.html",),
        daily_gate_input_names=(),
    )

    assert result["allowed"] is False
    assert result["reason_code"] == "UNKNOWN_ARTIFACT"
    assert result["unknown_artifact_names"] == ("unknown-public.html",)


def test_unknown_daily_gate_input_is_blocked():
    result = _explain(
        artifact_names=(artifacts.READER_HTML_ARTIFACT,),
        public_candidate_names=(),
        daily_gate_input_names=("unknown-input.yaml",),
    )

    assert result["allowed"] is False
    assert result["reason_code"] == "UNKNOWN_ARTIFACT"
    assert result["unknown_artifact_names"] == ("unknown-input.yaml",)


def test_public_candidate_not_in_inventory_is_blocked():
    result = _explain(
        artifact_names=(artifacts.ARTIFACT_HASH_ARTIFACT,),
        public_candidate_names=(artifacts.READER_HTML_ARTIFACT,),
        daily_gate_input_names=(),
    )

    assert result["allowed"] is False
    assert result["reason_code"] == "PUBLIC_CANDIDATE_NOT_IN_INVENTORY"
    assert result["missing_inventory_artifacts"] == (
        artifacts.READER_HTML_ARTIFACT,
    )


def test_daily_gate_input_not_in_inventory_is_blocked():
    result = _explain(
        artifact_names=(artifacts.READER_HTML_ARTIFACT,),
        public_candidate_names=(artifacts.READER_HTML_ARTIFACT,),
        daily_gate_input_names=(artifacts.ARTIFACT_HASH_ARTIFACT,),
    )

    assert result["allowed"] is False
    assert result["reason_code"] == "DAILY_GATE_INPUT_NOT_IN_INVENTORY"
    assert result["missing_inventory_artifacts"] == (
        artifacts.ARTIFACT_HASH_ARTIFACT,
    )


def test_training_report_marked_public_is_blocked():
    result = _explain(
        artifact_names=(artifacts.TRAINING_REPORT_ARTIFACT,),
        public_candidate_names=(artifacts.TRAINING_REPORT_ARTIFACT,),
        daily_gate_input_names=(),
    )

    assert result["allowed"] is False
    assert result["reason_code"] == "TRAINING_REPORT_MARKED_PUBLIC"
    assert result["public_candidate_violations"] == (
        artifacts.TRAINING_REPORT_ARTIFACT,
    )


def test_private_evidence_marked_public_is_blocked():
    result = _explain(
        artifact_names=(artifacts.SOURCE_MANIFEST_ARTIFACT,),
        public_candidate_names=(artifacts.SOURCE_MANIFEST_ARTIFACT,),
        daily_gate_input_names=(),
    )

    assert result["allowed"] is False
    assert result["reason_code"] == "PRIVATE_EVIDENCE_MARKED_PUBLIC"
    assert result["private_public_leak_candidates"] == (
        artifacts.SOURCE_MANIFEST_ARTIFACT,
    )


def test_ledger_marked_public_is_blocked():
    result = _explain(
        artifact_names=(artifacts.RUNTIME_CONTEXT_ARTIFACT,),
        public_candidate_names=(artifacts.RUNTIME_CONTEXT_ARTIFACT,),
        daily_gate_input_names=(),
    )

    assert result["allowed"] is False
    assert result["reason_code"] == "LEDGER_MARKED_PUBLIC"
    assert result["public_candidate_violations"] == (
        artifacts.RUNTIME_CONTEXT_ARTIFACT,
    )


def test_failure_evidence_marked_public_is_blocked():
    result = _explain(
        artifact_names=(artifacts.FAILURE_PACKAGE_ARTIFACT,),
        public_candidate_names=(artifacts.FAILURE_PACKAGE_ARTIFACT,),
        daily_gate_input_names=(),
    )

    assert result["allowed"] is False
    assert result["reason_code"] == "FAILURE_EVIDENCE_MARKED_PUBLIC"
    assert result["public_candidate_violations"] == (
        artifacts.FAILURE_PACKAGE_ARTIFACT,
    )


def test_governance_evidence_marked_public_is_blocked():
    result = _explain(
        artifact_names=(artifacts.BADCASE_RECORD_ARTIFACT,),
        public_candidate_names=(artifacts.BADCASE_RECORD_ARTIFACT,),
        daily_gate_input_names=(),
    )

    assert result["allowed"] is False
    assert result["reason_code"] == "GOVERNANCE_EVIDENCE_MARKED_PUBLIC"
    assert result["public_candidate_violations"] == (
        artifacts.BADCASE_RECORD_ARTIFACT,
    )


def test_non_reader_public_candidate_is_forward_compatible_static_marker_under_current_closed_catalog():
    dedicated_non_reader_artifacts = (
        artifacts.PUBLIC_SAFE_RENDER_SOURCE_ARTIFACTS
        | artifacts.PRIVATE_EVIDENCE_ARTIFACTS
        | artifacts.LEDGER_ARTIFACTS
        | artifacts.FAILURE_EVIDENCE_ARTIFACTS
        | artifacts.GOVERNANCE_EVIDENCE_ARTIFACTS
    )

    assert (
        frozenset(artifacts.ARTIFACT_NAMES)
        - artifacts.PUBLIC_CANDIDATE_ARTIFACTS
    ) == dedicated_non_reader_artifacts
    assert (
        artifact_inventory_policy.NON_READER_PUBLIC_CANDIDATE
        == "NON_READER_PUBLIC_CANDIDATE"
    )

    representative_dedicated_cases = (
        (
            artifacts.TRAINING_REPORT_ARTIFACT,
            "TRAINING_REPORT_MARKED_PUBLIC",
        ),
        (
            artifacts.SOURCE_MANIFEST_ARTIFACT,
            "PRIVATE_EVIDENCE_MARKED_PUBLIC",
        ),
        (
            artifacts.PUBLISH_LEDGER_ARTIFACT,
            "LEDGER_MARKED_PUBLIC",
        ),
        (
            artifacts.FAILURE_PACKAGE_ARTIFACT,
            "FAILURE_EVIDENCE_MARKED_PUBLIC",
        ),
        (
            artifacts.BADCASE_RECORD_ARTIFACT,
            "GOVERNANCE_EVIDENCE_MARKED_PUBLIC",
        ),
    )

    for artifact_name, expected_reason_code in (
        representative_dedicated_cases
    ):
        result = _explain(
            artifact_names=(artifact_name,),
            public_candidate_names=(artifact_name,),
            daily_gate_input_names=(),
        )

        assert result["reason_code"] == expected_reason_code
        assert (
            result["reason_code"]
            != artifact_inventory_policy.NON_READER_PUBLIC_CANDIDATE
        )

    unknown_result = _explain(
        artifact_names=(artifacts.READER_HTML_ARTIFACT,),
        public_candidate_names=("future-unknown-public-candidate",),
        daily_gate_input_names=(),
    )

    assert unknown_result["reason_code"] == "UNKNOWN_ARTIFACT"
    assert (
        unknown_result["reason_code"]
        != artifact_inventory_policy.NON_READER_PUBLIC_CANDIDATE
    )


def test_post_gate_daily_gate_input_violation_takes_priority_over_missing_inventory():
    post_gate_artifacts = (
        artifacts.PUBLISH_LEDGER_ARTIFACT,
        artifacts.NOTIFICATION_LEDGER_ARTIFACT,
        artifacts.RUN_LEDGER_ARTIFACT,
    )

    for artifact_name in post_gate_artifacts:
        result = _explain(
            artifact_names=(
                artifacts.READER_HTML_ARTIFACT,
                artifacts.TRAINING_REPORT_ARTIFACT,
                artifacts.ARTIFACT_HASH_ARTIFACT,
            ),
            public_candidate_names=(artifacts.READER_HTML_ARTIFACT,),
            daily_gate_input_names=(artifact_name,),
        )

        assert result["allowed"] is False
        assert (
            result["reason_code"]
            == "POST_GATE_ARTIFACT_USED_AS_DAILY_GATE_INPUT"
        )
        assert result["post_gate_daily_input_violations"] == (
            artifact_name,
        )
        assert result["missing_inventory_artifacts"] == (artifact_name,)


def test_missing_pre_gate_hash_evidence_is_blocked():
    result = _explain(pre_gate_hash_evidence_present=False)

    assert result["allowed"] is False
    assert result["reason_code"] == "MISSING_PRE_GATE_HASH_EVIDENCE"


def test_is_artifact_inventory_allowed_matches_explanation():
    cases = (
        (_minimal_inventory(), (artifacts.READER_HTML_ARTIFACT,), True),
        ((artifacts.READER_HTML_ARTIFACT,), (), True),
        ((artifacts.READER_HTML_ARTIFACT,), (), False),
    )

    for artifact_names, public_candidate_names, marker in cases:
        explanation = _explain(
            artifact_names=artifact_names,
            public_candidate_names=public_candidate_names,
            daily_gate_input_names=artifact_names,
            pre_gate_hash_evidence_present=marker,
        )

        assert (
            artifact_inventory_policy.is_artifact_inventory_allowed(
                artifact_names,
                public_candidate_names,
                artifact_names,
                marker,
            )
            is explanation["allowed"]
        )


def test_result_shape_is_stable():
    result = _explain()

    assert set(result) == REQUIRED_DECISION_FIELDS


def test_policy_guard_does_not_mutate_artifact_contracts():
    artifact_names_before = artifacts.ARTIFACT_NAMES
    classification_before = tuple(
        artifacts.ARTIFACT_CLASSIFICATION_BY_NAME.items()
    )
    public_candidates_before = artifacts.PUBLIC_CANDIDATE_ARTIFACTS
    private_evidence_before = artifacts.PRIVATE_EVIDENCE_ARTIFACTS
    ledgers_before = artifacts.LEDGER_ARTIFACTS
    invariants_before = artifacts.ARTIFACT_INVARIANTS

    _explain()
    _explain(
        artifact_names=(artifacts.SOURCE_MANIFEST_ARTIFACT,),
        public_candidate_names=(artifacts.SOURCE_MANIFEST_ARTIFACT,),
        daily_gate_input_names=(),
    )
    artifact_inventory_policy.is_artifact_inventory_allowed(
        (artifacts.PUBLISH_LEDGER_ARTIFACT,),
        (),
        (artifacts.PUBLISH_LEDGER_ARTIFACT,),
        True,
    )

    assert artifacts.ARTIFACT_NAMES == artifact_names_before
    assert (
        tuple(artifacts.ARTIFACT_CLASSIFICATION_BY_NAME.items())
        == classification_before
    )
    assert artifacts.PUBLIC_CANDIDATE_ARTIFACTS == public_candidates_before
    assert artifacts.PRIVATE_EVIDENCE_ARTIFACTS == private_evidence_before
    assert artifacts.LEDGER_ARTIFACTS == ledgers_before
    assert artifacts.ARTIFACT_INVARIANTS == invariants_before


def test_no_artifact_io_hash_ledger_publish_notification_or_url_behavior_is_implied():
    result = _explain()

    forbidden_behavior_keys = {
        "artifact_read",
        "artifact_written",
        "file_stat",
        "hash_calculated",
        "ledger_read",
        "ledger_written",
        "published",
        "publisher",
        "notification_sent",
        "public_url",
        "public_url_created",
        "external_api_called",
    }

    assert forbidden_behavior_keys.isdisjoint(result)
