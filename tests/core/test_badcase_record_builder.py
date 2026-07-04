"""Focused contract tests for the pure Badcase Record builder."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import badcase_record_builder as builder
from ai_daily_publishing_system.core import gates
from ai_daily_publishing_system.core import states


REQUIRED_RESULT_FIELDS = {
    "buildable",
    "reason_code",
    "reason",
    "source",
    "record",
    "record_violations",
    "missing_or_invalid_fields",
    "invariant_refs",
}

REQUIRED_RECORD_FIELDS = (
    "run_id",
    "badcase_id",
    "source_state",
    "badcase_kind",
    "badcase_reason_code",
    "badcase_summary",
    "severity",
    "failure_package_ref",
    "run_ledger_entry_ref",
    "gate_decision_envelope_refs",
    "artifact_refs",
    "evidence_refs",
    "reproduction_refs",
    "artifact_hash_refs",
    "issue_candidate",
    "issue_ref",
    "public_url_created",
    "public_url",
    "created_at",
    "timestamp_policy",
    "source_of_truth",
    "notes",
)

FORBIDDEN_RESULT_KEYS = {
    "public_url_is_null",
    "raw_public_url",
    "credential_values",
    "raw_credentials",
    "runtime_context",
    "config_snapshot",
    "adapter_outputs",
    "adapter_preflight_result",
    "review_content",
    "artifact_contents",
    "artifact_hash_values",
    "ledger_path",
    "badcase_record_path",
    "failure_package_path",
    "run_ledger_path",
    "issue_path",
    "should_write_badcase_record",
    "should_create_issue",
    "should_write_ledger",
    "should_transition",
    "should_publish",
    "should_notify",
    "gate_executed",
    "transition_executed",
    "ledger_written",
    "badcase_record_written",
    "failure_package_written",
    "issue_created",
    "badcase_created",
    "published",
    "notification_sent",
    "public_url_reserved",
    "public_url_faked",
    "runtime_context_read",
    "config_read",
    "credential_read",
    "adapter_preflight_executed",
    "adapter_executed",
    "external_api_called",
    "artifact_read",
    "artifact_written",
    "review_read",
    "file_stat",
    "hash_calculated",
    "ledger_read",
    "publisher",
    "notifier",
    "public_url_generated",
    "generated_state",
    "generated_transition",
    "gate_execution_result",
    "transition_execution_result",
}


def _valid_values():
    return {
        "run_id": "run-001",
        "badcase_id": "badcase-001",
        "source_state": states.REVIEW_BLOCKED,
        "badcase_kind": "review_blocked",
        "badcase_reason_code": "DAILY_GATE_BLOCKED",
        "badcase_summary": "Caller-supplied summary of the badcase.",
        "severity": "medium",
        "failure_package_ref": "failure-package.yaml#failure-001",
        "run_ledger_entry_ref": "run-ledger.yaml#run-001",
        "gate_decision_envelope_refs": (
            "daily-gate-decision-envelope.yaml",
        ),
        "artifact_refs": (
            "validator-result.yaml",
            "rubric-review.json",
        ),
        "evidence_refs": ("rubric-review.json#summary",),
        "reproduction_refs": (),
        "artifact_hash_refs": (),
        "issue_candidate": True,
        "issue_ref": "",
        "public_url_created": False,
        "public_url_is_null": True,
        "created_at": "caller-supplied-created-at",
        "timestamp_policy": "caller_supplied_no_datetime_parsing",
        "source_of_truth": ("p2d-2g", "p2d-16"),
        "notes": ("shape-only",),
    }


def _explain(**overrides):
    values = _valid_values()
    values.update(overrides)
    return builder.explain_badcase_record_build(**values)


def test_valid_config_blocked_badcase_record_is_buildable():
    result = _explain(
        source_state=states.CONFIG_BLOCKED,
        badcase_kind="config_blocked",
        badcase_reason_code="ADAPTER_CONFIGURATION_BLOCKED",
        gate_decision_envelope_refs=(
            "adapter-gate-decision-envelope.yaml",
        ),
    )

    assert result["buildable"] is True
    assert result["reason_code"] == "BADCASE_RECORD_BUILDABLE"
    assert result["record"]["source_state"] == states.CONFIG_BLOCKED


def test_valid_review_blocked_badcase_record_is_buildable():
    result = _explain()

    assert result["buildable"] is True
    assert result["reason_code"] == "BADCASE_RECORD_BUILDABLE"
    assert result["record"]["source_state"] == states.REVIEW_BLOCKED
    assert result["record_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()


def test_valid_system_failed_badcase_record_is_buildable():
    result = _explain(
        source_state=states.SYSTEM_FAILED,
        badcase_kind="system_failed",
        badcase_reason_code="RUNTIME_FAILURE_CLASSIFIED",
        gate_decision_envelope_refs=(),
    )

    assert result["buildable"] is True
    assert result["reason_code"] == "BADCASE_RECORD_BUILDABLE"
    assert result["record"]["source_state"] == states.SYSTEM_FAILED


def test_valid_adapter_failed_badcase_record_is_buildable():
    result = _explain(
        source_state=states.ADAPTER_FAILED,
        badcase_kind="adapter_failed",
        badcase_reason_code="ADAPTER_EXECUTION_FAILED",
        gate_decision_envelope_refs=(
            "adapter-gate-decision-envelope.yaml",
        ),
    )

    assert result["buildable"] is True
    assert result["reason_code"] == "BADCASE_RECORD_BUILDABLE"
    assert result["record"]["source_state"] == states.ADAPTER_FAILED


def test_system_failed_allows_empty_gate_decision_envelope_refs():
    result = _explain(
        source_state=states.SYSTEM_FAILED,
        gate_decision_envelope_refs=(),
    )

    assert result["buildable"] is True
    assert result["record"]["gate_decision_envelope_refs"] == ()
    assert "GATE_DECISION_ENVELOPE_REFS_MISSING" not in (
        result["record_violations"]
    )


def test_system_failed_allows_empty_reproduction_refs():
    result = _explain(
        source_state=states.SYSTEM_FAILED,
        gate_decision_envelope_refs=(),
        reproduction_refs=(),
    )

    assert result["buildable"] is True
    assert result["record"]["reproduction_refs"] == ()


def test_system_failed_allows_empty_artifact_hash_refs():
    result = _explain(
        source_state=states.SYSTEM_FAILED,
        gate_decision_envelope_refs=(),
        artifact_hash_refs=(),
    )

    assert result["buildable"] is True
    assert result["record"]["artifact_hash_refs"] == ()


def test_gate_related_source_states_require_gate_envelope_refs():
    for source_state in (
        states.CONFIG_BLOCKED,
        states.REVIEW_BLOCKED,
        states.ADAPTER_FAILED,
    ):
        result = _explain(
            source_state=source_state,
            gate_decision_envelope_refs=(),
        )

        assert result["buildable"] is False
        assert (
            result["reason_code"]
            == "GATE_DECISION_ENVELOPE_REFS_MISSING"
        )
        assert result["record_violations"] == (
            "GATE_DECISION_ENVELOPE_REFS_MISSING",
        )
        assert result["missing_or_invalid_fields"] == (
            "gate_decision_envelope_refs",
        )


def test_badcase_created_is_not_badcase_record_source_eligible():
    result = _explain(source_state=states.BADCASE_CREATED)

    assert result["buildable"] is False
    assert (
        result["reason_code"]
        == "SOURCE_STATE_NOT_BADCASE_ELIGIBLE"
    )
    assert result["missing_or_invalid_fields"] == ("source_state",)


def test_noop_completed_is_not_badcase_record_source_eligible():
    result = _explain(source_state=states.NOOP_COMPLETED)

    assert result["buildable"] is False
    assert (
        result["reason_code"]
        == "SOURCE_STATE_NOT_BADCASE_ELIGIBLE"
    )
    assert result["missing_or_invalid_fields"] == ("source_state",)


def test_publish_allowed_is_not_badcase_record_source_eligible():
    result = _explain(source_state=states.PUBLISH_ALLOWED)

    assert result["buildable"] is False
    assert (
        result["reason_code"]
        == "SOURCE_STATE_NOT_BADCASE_ELIGIBLE"
    )
    assert result["missing_or_invalid_fields"] == ("source_state",)


def test_unknown_source_state_is_blocked():
    result = _explain(source_state="UNKNOWN_STATE")

    assert result["buildable"] is False
    assert result["reason_code"] == "SOURCE_STATE_UNKNOWN"
    assert result["record_violations"] == ("SOURCE_STATE_UNKNOWN",)
    assert result["missing_or_invalid_fields"] == ("source_state",)


def test_record_keys_exactly_match_badcase_record_fields():
    result = _explain()

    assert tuple(result["record"].keys()) == REQUIRED_RECORD_FIELDS
    assert set(result["record"]) == set(REQUIRED_RECORD_FIELDS)


def test_result_shape_is_stable():
    result = _explain()

    assert set(result) == REQUIRED_RESULT_FIELDS


def test_missing_required_fields_block_with_dedicated_reasons():
    cases = (
        ("run_id", "", "RUN_ID_MISSING", ("run_id",)),
        ("badcase_id", "", "BADCASE_ID_MISSING", ("badcase_id",)),
        (
            "source_state",
            "",
            "SOURCE_STATE_MISSING",
            ("source_state",),
        ),
        (
            "badcase_kind",
            "",
            "BADCASE_KIND_MISSING",
            ("badcase_kind",),
        ),
        (
            "badcase_reason_code",
            "",
            "BADCASE_REASON_CODE_MISSING",
            ("badcase_reason_code",),
        ),
        (
            "badcase_summary",
            "",
            "BADCASE_SUMMARY_MISSING",
            ("badcase_summary",),
        ),
        ("severity", "", "SEVERITY_MISSING", ("severity",)),
        (
            "failure_package_ref",
            "",
            "FAILURE_PACKAGE_REF_MISSING",
            ("failure_package_ref",),
        ),
        (
            "run_ledger_entry_ref",
            "",
            "RUN_LEDGER_ENTRY_REF_MISSING",
            ("run_ledger_entry_ref",),
        ),
        ("artifact_refs", (), "ARTIFACT_REFS_MISSING", ("artifact_refs",)),
        ("evidence_refs", (), "EVIDENCE_REFS_MISSING", ("evidence_refs",)),
        (
            "created_at",
            "",
            "CREATED_AT_MISSING",
            ("created_at",),
        ),
        (
            "timestamp_policy",
            "",
            "TIMESTAMP_POLICY_MISSING",
            ("timestamp_policy",),
        ),
        (
            "source_of_truth",
            (),
            "SOURCE_OF_TRUTH_MISSING",
            ("source_of_truth",),
        ),
    )

    for field_name, value, reason_code, invalid_fields in cases:
        result = _explain(**{field_name: value})

        assert result["buildable"] is False
        assert result["reason_code"] == reason_code
        assert result["record_violations"] == (reason_code,)
        assert result["missing_or_invalid_fields"] == invalid_fields


def test_whitespace_required_strings_are_missing():
    cases = (
        ("run_id", "   ", "RUN_ID_MISSING"),
        ("badcase_id", "   ", "BADCASE_ID_MISSING"),
        ("source_state", "   ", "SOURCE_STATE_MISSING"),
        ("badcase_kind", "   ", "BADCASE_KIND_MISSING"),
        (
            "badcase_reason_code",
            "   ",
            "BADCASE_REASON_CODE_MISSING",
        ),
        ("badcase_summary", "   ", "BADCASE_SUMMARY_MISSING"),
        ("severity", "   ", "SEVERITY_MISSING"),
        (
            "failure_package_ref",
            "   ",
            "FAILURE_PACKAGE_REF_MISSING",
        ),
        (
            "run_ledger_entry_ref",
            "   ",
            "RUN_LEDGER_ENTRY_REF_MISSING",
        ),
        ("created_at", "   ", "CREATED_AT_MISSING"),
        ("timestamp_policy", "   ", "TIMESTAMP_POLICY_MISSING"),
    )

    for field_name, value, reason_code in cases:
        result = _explain(**{field_name: value})

        assert result["buildable"] is False
        assert result["reason_code"] == reason_code


def test_public_url_created_true_is_blocked():
    result = _explain(public_url_created=True)

    assert result["buildable"] is False
    assert result["reason_code"] == "PUBLIC_URL_CREATED_TRUE"
    assert result["missing_or_invalid_fields"] == ("public_url_created",)
    assert result["record"]["public_url_created"] is True
    assert result["record"]["public_url"] is None


def test_public_url_is_null_false_is_blocked_without_echoing_url():
    result = _explain(public_url_is_null=False)

    assert result["buildable"] is False
    assert result["reason_code"] == "PUBLIC_URL_NON_NULL"
    assert result["missing_or_invalid_fields"] == ("public_url",)
    assert result["record"]["public_url"] is None
    assert "public_url_is_null" not in result
    assert "public_url_is_null" not in result["record"]


def test_record_always_returns_public_url_none():
    results = (
        _explain(),
        _explain(public_url_created=True),
        _explain(public_url_is_null=False),
    )

    for result in results:
        assert result["record"]["public_url"] is None


def test_no_raw_url_string_appears_in_result():
    result = _explain()

    assert "https://" not in repr(result)
    assert "raw_public_url" not in result
    assert "raw_public_url" not in result["record"]


def test_issue_candidate_allows_empty_or_existing_ref():
    without_ref = _explain(
        issue_candidate=True,
        issue_ref="",
    )
    with_ref = _explain(
        issue_candidate=True,
        issue_ref="ops-issue#badcase-001",
    )

    assert without_ref["buildable"] is True
    assert with_ref["buildable"] is True
    assert with_ref["record"]["issue_ref"] == "ops-issue#badcase-001"


def test_issue_ref_without_issue_candidate_is_blocked():
    result = _explain(
        issue_candidate=False,
        issue_ref="ops-issue#badcase-001",
    )

    assert result["buildable"] is False
    assert (
        result["reason_code"]
        == "ISSUE_REF_WITHOUT_ISSUE_CANDIDATE"
    )
    assert result["missing_or_invalid_fields"] == ("issue_ref",)


def test_reproduction_refs_are_optional_caller_supplied_refs():
    without_refs = _explain(reproduction_refs=())
    with_refs = _explain(
        reproduction_refs=("manual-repro#step-1",),
    )

    assert without_refs["buildable"] is True
    assert with_refs["buildable"] is True
    assert without_refs["record"]["reproduction_refs"] == ()
    assert with_refs["record"]["reproduction_refs"] == (
        "manual-repro#step-1",
    )


def test_artifact_hash_refs_are_optional_caller_supplied_refs():
    without_refs = _explain(artifact_hash_refs=())
    with_refs = _explain(
        artifact_hash_refs=("artifact-hash.yaml#pre-gate",),
    )

    assert without_refs["buildable"] is True
    assert with_refs["buildable"] is True
    assert without_refs["record"]["artifact_hash_refs"] == ()
    assert with_refs["record"]["artifact_hash_refs"] == (
        "artifact-hash.yaml#pre-gate",
    )


def test_optional_ref_missing_reasons_are_not_declared():
    reproduction_missing = "REPRODUCTION_" + "REFS_MISSING"
    artifact_hash_missing = "ARTIFACT_" + "HASH_REFS_MISSING"

    assert reproduction_missing not in builder.BADCASE_RECORD_BUILD_REASON_CODES
    assert reproduction_missing not in builder.__dict__
    assert artifact_hash_missing not in builder.BADCASE_RECORD_BUILD_REASON_CODES
    assert artifact_hash_missing not in builder.__dict__


def test_reason_priority_and_all_violations_are_collected():
    result = _explain(
        run_id="",
        badcase_id="",
        source_state=states.REVIEW_BLOCKED,
        badcase_kind="",
        badcase_reason_code="",
        badcase_summary="",
        severity="",
        failure_package_ref="",
        run_ledger_entry_ref="",
        gate_decision_envelope_refs=(),
        artifact_refs=(),
        evidence_refs=(),
        public_url_created=True,
        public_url_is_null=False,
        issue_candidate=False,
        issue_ref="ops-issue#badcase-001",
        created_at="",
        timestamp_policy="",
        source_of_truth=(),
    )

    assert result["buildable"] is False
    assert result["reason_code"] == "RUN_ID_MISSING"
    assert result["record_violations"] == (
        "RUN_ID_MISSING",
        "BADCASE_ID_MISSING",
        "BADCASE_KIND_MISSING",
        "BADCASE_REASON_CODE_MISSING",
        "BADCASE_SUMMARY_MISSING",
        "SEVERITY_MISSING",
        "FAILURE_PACKAGE_REF_MISSING",
        "RUN_LEDGER_ENTRY_REF_MISSING",
        "GATE_DECISION_ENVELOPE_REFS_MISSING",
        "ARTIFACT_REFS_MISSING",
        "EVIDENCE_REFS_MISSING",
        "CREATED_AT_MISSING",
        "TIMESTAMP_POLICY_MISSING",
        "SOURCE_OF_TRUTH_MISSING",
        "PUBLIC_URL_CREATED_TRUE",
        "PUBLIC_URL_NON_NULL",
        "ISSUE_REF_WITHOUT_ISSUE_CANDIDATE",
    )
    assert result["missing_or_invalid_fields"] == (
        "run_id",
        "badcase_id",
        "badcase_kind",
        "badcase_reason_code",
        "badcase_summary",
        "severity",
        "failure_package_ref",
        "run_ledger_entry_ref",
        "gate_decision_envelope_refs",
        "artifact_refs",
        "evidence_refs",
        "created_at",
        "timestamp_policy",
        "source_of_truth",
        "public_url_created",
        "public_url",
        "issue_ref",
    )


def test_buildable_result_has_empty_violation_and_field_collections():
    result = _explain()

    assert result["buildable"] is True
    assert result["record_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()


def test_bool_wrapper_matches_explanation():
    cases = (
        _valid_values(),
        dict(_valid_values(), run_id=""),
        dict(
            _valid_values(),
            source_state=states.SYSTEM_FAILED,
            gate_decision_envelope_refs=(),
        ),
        dict(
            _valid_values(),
            issue_candidate=False,
            issue_ref="ops-issue#badcase-001",
        ),
    )

    for values in cases:
        explanation = builder.explain_badcase_record_build(**values)

        assert (
            builder.is_badcase_record_buildable(**values)
            is explanation["buildable"]
        )


def test_no_raw_credential_adapter_review_artifact_hash_ledger_or_issue_values_appear():
    result = _explain()
    forbidden_values = (
        "secret-token",
        "provider-secret-value",
        "adapter-output-body",
        "review-content-body",
        "artifact-body-content",
        "artifact-hash-value",
        "ledger/path/value",
        "issue/path/value",
    )
    rendered_result = repr(result)

    for forbidden_value in forbidden_values:
        assert forbidden_value not in rendered_result


def test_buildable_result_does_not_imply_execution_writes_or_issue_creation():
    result = _explain()

    assert result["buildable"] is True
    assert FORBIDDEN_RESULT_KEYS.isdisjoint(result)
    assert FORBIDDEN_RESULT_KEYS.isdisjoint(result["record"])
    assert "builder_not_badcase_record_writer" in result["invariant_refs"]
    assert "builder_not_issue_creator" in result["invariant_refs"]
    assert "builder_not_failure_package_writer" in result["invariant_refs"]
    assert "builder_not_run_ledger_writer" in result["invariant_refs"]
    assert "builder_not_gate_execution" in result["invariant_refs"]
    assert "builder_not_transition_execution" in result["invariant_refs"]
    assert "buildable_not_hash_calculation" in result["invariant_refs"]
    assert "buildable_not_publish" in result["invariant_refs"]
    assert "buildable_not_notification" in result["invariant_refs"]
    assert "buildable_not_public_url" in result["invariant_refs"]


def test_states_and_gates_constants_are_not_mutated():
    mvp_states_before = states.MVP_STATES
    state_invariants_before = states.STATE_INVARIANTS
    gate_invariants_before = gates.GATE_INVARIANTS
    gate_names_before = gates.GATE_NAMES

    _explain()
    _explain(public_url_created=True)
    builder.is_badcase_record_buildable(**_valid_values())

    assert states.MVP_STATES == mvp_states_before
    assert states.STATE_INVARIANTS == state_invariants_before
    assert gates.GATE_INVARIANTS == gate_invariants_before
    assert gates.GATE_NAMES == gate_names_before


def test_module_namespace_does_not_import_forbidden_modules_or_io_libraries():
    forbidden_names = {
        "artifacts",
        "gate_decision_mapper",
        "transition_guard",
        "adapter_gate_evidence_policy",
        "adapter_gate_decision_policy",
        "daily_gate_evidence_policy",
        "daily_gate_decision_policy",
        "gate_decision_envelope_builder",
        "run_ledger_entry_builder",
        "failure_package_builder",
        "artifact_inventory_policy",
        "noop_completion_policy",
        "badcase_creation_policy",
        "pathlib",
        "os",
        "datetime",
        "hashlib",
        "logging",
        "subprocess",
        "requests",
    }

    assert forbidden_names.isdisjoint(builder.__dict__)


def test_result_does_not_imply_runtime_or_io_behavior():
    results = (
        _explain(),
        _explain(public_url_is_null=False),
    )
    forbidden_keys = FORBIDDEN_RESULT_KEYS | {
        "config",
        "artifact_path",
        "hash_value",
        "gate_passed",
        "transition",
        "decision_result",
        states.CONFIG_BLOCKED,
        states.REVIEW_BLOCKED,
        states.SYSTEM_FAILED,
        states.ADAPTER_FAILED,
        states.BADCASE_CREATED,
    }

    for result in results:
        assert forbidden_keys.isdisjoint(result)
        assert forbidden_keys.isdisjoint(result["record"])
        assert "no_runtime_context_config_or_credential_read" in (
            result["invariant_refs"]
        )
        assert "no_adapter_preflight" in result["invariant_refs"]
        assert "no_external_adapter_call" in result["invariant_refs"]
        assert "no_artifact_or_review_io" in result["invariant_refs"]
        assert "no_hash_calculation" in result["invariant_refs"]
        assert "no_ledger_write" in result["invariant_refs"]
        assert "no_badcase_record_write" in result["invariant_refs"]
        assert "no_issue_creation" in result["invariant_refs"]
        assert "no_failure_package_write" in result["invariant_refs"]
        assert "no_public_url_behavior" in result["invariant_refs"]


def test_reason_catalog_contains_only_executable_reason_codes():
    assert builder.BADCASE_RECORD_BUILD_REASON_CODES == (
        "RUN_ID_MISSING",
        "BADCASE_ID_MISSING",
        "SOURCE_STATE_MISSING",
        "SOURCE_STATE_UNKNOWN",
        "SOURCE_STATE_NOT_BADCASE_ELIGIBLE",
        "BADCASE_KIND_MISSING",
        "BADCASE_REASON_CODE_MISSING",
        "BADCASE_SUMMARY_MISSING",
        "SEVERITY_MISSING",
        "FAILURE_PACKAGE_REF_MISSING",
        "RUN_LEDGER_ENTRY_REF_MISSING",
        "GATE_DECISION_ENVELOPE_REFS_MISSING",
        "ARTIFACT_REFS_MISSING",
        "EVIDENCE_REFS_MISSING",
        "CREATED_AT_MISSING",
        "TIMESTAMP_POLICY_MISSING",
        "SOURCE_OF_TRUTH_MISSING",
        "PUBLIC_URL_CREATED_TRUE",
        "PUBLIC_URL_NON_NULL",
        "ISSUE_REF_WITHOUT_ISSUE_CANDIDATE",
        "BADCASE_RECORD_BUILDABLE",
    )
    forbidden_codes = {
        "BADCASE_RECORD_WRITE_FORBIDDEN",
        "ISSUE_CREATION_FORBIDDEN",
        "FAILURE_PACKAGE_WRITE_FORBIDDEN",
        "RUN_LEDGER_WRITE_FORBIDDEN",
        "GATE_EXECUTION_FORBIDDEN",
        "TRANSITION_EXECUTION_FORBIDDEN",
        "HASH_CALCULATION_FORBIDDEN",
        "PUBLISH_FORBIDDEN",
        "NOTIFICATION_FORBIDDEN",
        "PUBLIC_URL_CREATION_FORBIDDEN",
    }

    assert forbidden_codes.isdisjoint(
        builder.BADCASE_RECORD_BUILD_REASON_CODES
    )


def test_invariant_refs_capture_badcase_record_builder_boundaries():
    result = _explain()
    required_invariants = {
        "badcase_record_builder_only",
        "builder_not_badcase_record_writer",
        "builder_not_issue_creator",
        "builder_not_failure_package_writer",
        "builder_not_run_ledger_writer",
        "builder_not_gate_execution",
        "builder_not_transition_mapping",
        "builder_not_transition_execution",
        "buildable_not_hash_calculation",
        "buildable_not_publish",
        "buildable_not_notification",
        "buildable_not_public_url",
        "no_runtime_context_config_or_credential_read",
        "no_adapter_preflight",
        "no_external_adapter_call",
        "no_raw_credentials",
        "no_raw_public_url",
        "no_quality_pass_no_public_url",
        "no_artifact_or_review_io",
        "no_hash_calculation",
        "no_ledger_write",
        "no_badcase_record_write",
        "no_issue_creation",
        "no_failure_package_write",
        "no_public_url_behavior",
        "no_gate_decision_envelope_builder_call",
        "no_run_ledger_entry_builder_call",
        "no_failure_package_builder_call",
        "no_badcase_creation_policy_call",
    }

    assert required_invariants <= set(result["invariant_refs"])
    assert set(states.STATE_INVARIANTS) <= set(result["invariant_refs"])
    assert set(gates.GATE_INVARIANTS) <= set(result["invariant_refs"])


def test_no_forbidden_payload_object_path_or_control_inputs_are_in_result():
    result = _explain()
    forbidden_names = (
        "runtime_context",
        "config_snapshot",
        "credential_values",
        "raw_credentials",
        "raw_public_url",
        "adapter_outputs",
        "review_content",
        "artifact_contents",
        "artifact_hash_values",
        "ledger_path",
        "badcase_record_path",
        "failure_package_path",
        "run_ledger_path",
        "issue_path",
        "badcase_record",
        "failure_package",
        "gate_decision_envelope",
        "run_ledger_entry",
        "should_write_badcase_record",
        "should_create_issue",
        "should_write_ledger",
        "should_transition",
        "should_publish",
        "should_notify",
    )

    for forbidden_name in forbidden_names:
        assert forbidden_name not in result
        assert forbidden_name not in result["record"]
