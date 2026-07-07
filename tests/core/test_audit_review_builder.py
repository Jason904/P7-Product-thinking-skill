"""Tests for the pure audit review artifact buildability builder."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import audit_review_builder as builder


RESULT_KEYS = (
    "buildable",
    "reason_code",
    "reason",
    "source",
    "audit_review",
    "audit_violations",
    "missing_or_invalid_fields",
    "audit_check_violations",
    "invariant_refs",
)

SOURCE_KEYS = (
    "artifact_refs",
    "source_of_truth",
)

AUDIT_REVIEW_KEYS = (
    "run_id",
    "audit_review_id",
    "review_kind",
    "artifact_refs",
    "audit_checks",
    "required_audit_check_ids",
    "missing_audit_check_ids",
    "blocking_audit_check_ids",
    "audit_outcome",
    "created_at",
    "timestamp_policy",
    "source_of_truth",
    "notes",
)

AUDIT_CHECK_KEYS = (
    "audit_check_id",
    "audit_check_role",
    "target_artifact_ref",
    "target_artifact_kind",
    "audit_status",
    "severity",
    "finding",
    "evidence_refs",
    "notes",
)

AUDIT_CHECK_VIOLATION_KEYS = (
    "audit_check_index",
    "audit_check_id",
    "reason_code",
    "field",
)

REASON_CODES = (
    "AUDIT_REVIEW_BUILDABLE",
    "RUN_ID_MISSING",
    "AUDIT_REVIEW_ID_MISSING",
    "REVIEW_KIND_MISSING",
    "ARTIFACT_REFS_MISSING",
    "AUDIT_CHECKS_MISSING",
    "REQUIRED_AUDIT_CHECK_IDS_MISSING",
    "MISSING_AUDIT_CHECK_IDS_DECLARED",
    "BLOCKING_AUDIT_CHECK_ID_UNKNOWN",
    "AUDIT_OUTCOME_MISSING",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "AUDIT_CHECK_NOT_DICT",
    "AUDIT_CHECK_KEYS_INVALID",
    "AUDIT_CHECK_ID_MISSING",
    "AUDIT_CHECK_ROLE_MISSING",
    "AUDIT_CHECK_TARGET_ARTIFACT_REF_MISSING",
    "AUDIT_CHECK_TARGET_ARTIFACT_KIND_MISSING",
    "AUDIT_CHECK_STATUS_MISSING",
    "AUDIT_CHECK_SEVERITY_MISSING",
    "AUDIT_CHECK_FINDING_MISSING",
    "AUDIT_CHECK_EVIDENCE_REFS_MISSING",
    "AUDIT_CHECK_ID_DUPLICATE",
    "AUDIT_CHECK_ID_NOT_REQUIRED",
    "REQUIRED_AUDIT_CHECK_MISSING",
    "AUDIT_CHECK_FORBIDDEN_RAW_FIELD_PRESENT",
)

REASON_PRIORITY = (
    "RUN_ID_MISSING",
    "AUDIT_REVIEW_ID_MISSING",
    "REVIEW_KIND_MISSING",
    "ARTIFACT_REFS_MISSING",
    "AUDIT_CHECKS_MISSING",
    "REQUIRED_AUDIT_CHECK_IDS_MISSING",
    "MISSING_AUDIT_CHECK_IDS_DECLARED",
    "BLOCKING_AUDIT_CHECK_ID_UNKNOWN",
    "AUDIT_OUTCOME_MISSING",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "AUDIT_CHECK_NOT_DICT",
    "AUDIT_CHECK_KEYS_INVALID",
    "AUDIT_CHECK_ID_MISSING",
    "AUDIT_CHECK_ROLE_MISSING",
    "AUDIT_CHECK_TARGET_ARTIFACT_REF_MISSING",
    "AUDIT_CHECK_TARGET_ARTIFACT_KIND_MISSING",
    "AUDIT_CHECK_STATUS_MISSING",
    "AUDIT_CHECK_SEVERITY_MISSING",
    "AUDIT_CHECK_FINDING_MISSING",
    "AUDIT_CHECK_EVIDENCE_REFS_MISSING",
    "AUDIT_CHECK_ID_DUPLICATE",
    "AUDIT_CHECK_ID_NOT_REQUIRED",
    "REQUIRED_AUDIT_CHECK_MISSING",
    "AUDIT_CHECK_FORBIDDEN_RAW_FIELD_PRESENT",
    "AUDIT_REVIEW_BUILDABLE",
)

FORBIDDEN_AUDIT_CHECK_FIELDS = (
    "raw_audit_output",
    "raw_review_output",
    "review_output",
    "audit_output",
    "raw_judge_output",
    "judge_output",
    "llm_judge_output",
    "llm_audit_output",
    "human_audit_output",
    "human_review_output",
    "audit_execution_result",
    "audit_result",
    "policy_execution_result",
    "policy_result",
    "policy_decision",
    "policy_pass",
    "quality_pass",
    "rubric_pass",
    "validator_pass",
    "eval_pass",
    "audit_pass",
    "gate_pass",
    "publish_allowed",
    "rendered_html",
    "html",
    "raw_html",
    "reader_html",
    "reader_html_content",
    "rendered_markdown",
    "markdown",
    "raw_markdown",
    "report_markdown",
    "training_report",
    "training_report_content",
    "training_report_markdown",
    "validator_result",
    "validator_result_content",
    "rubric_review",
    "rubric_review_content",
    "reader_artifact",
    "reader_artifact_content",
    "source_manifest",
    "source_manifest_content",
    "source_notes",
    "source_notes_content",
    "raw_content",
    "content",
    "source_content",
    "artifact_contents",
    "fetched_content",
    "generated_summary",
    "llm_summary",
    "inferred_fact",
    "model_output",
    "raw_model_output",
    "prompt",
    "raw_prompt",
    "source_url",
    "raw_url",
    "url",
    "public_url",
    "publish_url",
    "deployment_url",
    "hosting_target",
    "file_path",
    "path",
    "local_path",
    "reader_path",
    "training_report_path",
    "validator_result_path",
    "rubric_review_path",
    "source_manifest_path",
    "source_notes_path",
    "credentials",
    "raw_credentials",
    "env_vars",
    "raw_env_vars",
    "config",
    "raw_config",
    "adapter_outputs",
    "driver_object",
    "source_fetch_result",
    "source_reader_result",
    "retriever_result",
    "rss_fetch_result",
    "artifact_reader_result",
    "validator_execution_result",
    "rubric_execution_result",
    "judge_execution_result",
    "eval_result",
    "gate_result",
    "publish_result",
    "should_fetch",
    "should_read_reader",
    "should_read_training_report",
    "should_read_validator_result",
    "should_read_rubric_review",
    "should_read_source_manifest",
    "should_read_source_notes",
    "should_read_source",
    "should_read_file",
    "should_call_web",
    "should_call_github",
    "should_call_rss",
    "should_call_notion",
    "should_call_llm",
    "should_judge",
    "should_audit",
    "should_run_audit",
    "should_run_policy",
    "should_validate",
    "should_run_validator",
    "should_eval",
    "should_gate",
    "should_publish",
    "should_create_public_url",
    "reader_read",
    "training_report_read",
    "validator_result_read",
    "rubric_review_read",
    "source_manifest_read",
    "source_notes_read",
    "source_content_read",
    "file_read_executed",
    "fetch_executed",
    "web_called",
    "github_called",
    "rss_called",
    "notion_called",
    "llm_called",
    "judge_executed",
    "audit_executed",
    "policy_executed",
    "validator_executed",
    "eval_executed",
    "gate_executed",
    "published",
    "public_url_created",
)

ALLOWED_AUDIT_FIELD_NAMES = (
    "audit_review_id",
    "audit_review",
    "review_kind",
    "audit_checks",
    "required_audit_check_ids",
    "missing_audit_check_ids",
    "blocking_audit_check_ids",
    "audit_outcome",
    "audit_check_id",
    "audit_check_role",
    "audit_status",
    "target_artifact_ref",
    "target_artifact_kind",
    "artifact_refs",
    "evidence_refs",
)

FORBIDDEN_PSEUDO_REASON_CODES = (
    "READER_READ_FORBIDDEN",
    "TRAINING_REPORT_READ_FORBIDDEN",
    "VALIDATOR_RESULT_READ_FORBIDDEN",
    "RUBRIC_REVIEW_READ_FORBIDDEN",
    "SOURCE_MANIFEST_READ_FORBIDDEN",
    "SOURCE_NOTES_READ_FORBIDDEN",
    "SOURCE_CONTENT_READ_FORBIDDEN",
    "FILE_READ_FORBIDDEN",
    "WEB_FETCH_FORBIDDEN",
    "GITHUB_FETCH_FORBIDDEN",
    "RSS_FETCH_FORBIDDEN",
    "NOTION_FETCH_FORBIDDEN",
    "LLM_JUDGE_FORBIDDEN",
    "HUMAN_AUDIT_FORBIDDEN",
    "AUDIT_EXECUTION_FORBIDDEN",
    "POLICY_EXECUTION_FORBIDDEN",
    "VALIDATOR_EXECUTION_FORBIDDEN",
    "EVAL_EXECUTION_FORBIDDEN",
    "GATE_EXECUTION_FORBIDDEN",
    "PUBLISH_FORBIDDEN",
    "PUBLIC_URL_CREATION_FORBIDDEN",
)

FORBIDDEN_MODULE_NAMES = (
    "states",
    "gates",
    "artifacts",
    "rubric_review_builder",
    "validator_result_builder",
    "reader_artifact_builder",
    "training_report_builder",
    "source_manifest_builder",
    "source_notes_builder",
    "runtime_context_snapshot_builder",
    "runtime_profile_snapshot_builder",
    "config_snapshot_builder",
    "adapter_preflight_result_builder",
    "adapter_gate_evidence_policy",
    "adapter_gate_decision_policy",
    "daily_gate_evidence_policy",
    "daily_gate_decision_policy",
    "gate_decision_mapper",
    "transition_guard",
    "noop_completion_policy",
    "artifact_inventory_policy",
    "build_audit_review",
    "run_audit_review",
    "run_audit",
    "run_policy_engine",
    "compute_audit_result",
    "compute_risk_result",
    "judge_audit",
    "call_llm_judge",
    "call_human_auditor",
    "validate_artifact",
    "validate_reader",
    "validate_schema",
    "validate_html",
    "execute_validator",
    "build_gate_decision",
)

REQUIRED_INVARIANT_REFS = (
    "audit_review_builder_only",
    "builder_not_reader_reader",
    "builder_not_training_report_reader",
    "builder_not_validator_result_reader",
    "builder_not_rubric_review_reader",
    "builder_not_source_manifest_reader",
    "builder_not_source_notes_reader",
    "builder_not_source_reader",
    "builder_not_file_reader",
    "builder_not_web_fetcher",
    "builder_not_github_fetcher",
    "builder_not_rss_fetcher",
    "builder_not_notion_fetcher",
    "builder_not_llm_judge",
    "builder_not_human_auditor",
    "builder_not_audit_executor",
    "builder_not_policy_executor",
    "builder_not_validator_executor",
    "builder_not_eval_executor",
    "builder_not_gate_executor",
    "builder_not_publisher",
    "audit_checks_are_caller_supplied",
    "audit_findings_are_caller_supplied",
    "audit_outcome_is_caller_supplied",
    "artifact_refs_opaque",
    "target_artifact_refs_opaque",
    "evidence_refs_opaque",
    "audit_review_governance_evidence",
    "audit_review_not_public_candidate",
    "audit_outcome_not_quality_pass",
    "audit_outcome_not_gate_pass",
    "audit_outcome_not_publish_allowed",
    "buildable_not_audit_pass",
    "buildable_not_quality_pass",
    "buildable_not_eval_pass",
    "buildable_not_gate_pass",
    "buildable_not_publish_allowed",
    "buildable_not_public_url_created",
    "blocking_audit_check_ids_are_gate_evidence_only",
    "blocking_audit_check_ids_do_not_execute_gate",
    "no_reader_read",
    "no_training_report_read",
    "no_validator_result_read",
    "no_rubric_review_read",
    "no_source_manifest_read",
    "no_source_notes_read",
    "no_source_content_read",
    "no_url_fetch",
    "no_rss_fetch",
    "no_file_read",
    "no_raw_content",
    "no_raw_url",
    "no_generated_audit",
    "no_llm_summary",
    "no_llm_judge",
    "no_human_audit_workflow",
    "no_audit_execution",
    "no_policy_execution",
    "no_inferred_fact_generation",
    "no_hash_calculation",
    "no_existing_builder_or_policy_call",
    "no_validator_execution",
    "no_eval_execution",
    "no_gate_execution",
    "no_transition_execution",
    "no_runtime_execution",
    "no_adapter_execution",
    "no_publish",
    "no_notification",
    "no_public_url_behavior",
    "no_quality_pass_no_public_url",
    "noop_completed_not_pass_published",
)

MISSING_AUDIT_CHECK_KEY_EXPECTATIONS = (
    ("audit_check_id", "AUDIT_CHECK_ID_MISSING"),
    ("audit_check_role", "AUDIT_CHECK_ROLE_MISSING"),
    ("target_artifact_ref", "AUDIT_CHECK_TARGET_ARTIFACT_REF_MISSING"),
    ("target_artifact_kind", "AUDIT_CHECK_TARGET_ARTIFACT_KIND_MISSING"),
    ("audit_status", "AUDIT_CHECK_STATUS_MISSING"),
    ("severity", "AUDIT_CHECK_SEVERITY_MISSING"),
    ("finding", "AUDIT_CHECK_FINDING_MISSING"),
    ("evidence_refs", "AUDIT_CHECK_EVIDENCE_REFS_MISSING"),
    ("notes", "AUDIT_CHECK_KEYS_INVALID"),
)


def _audit_check(**overrides):
    values = {
        "audit_check_id": "audit-check-001",
        "audit_check_role": "audit_boundary",
        "target_artifact_ref": "rubric-review-001",
        "target_artifact_kind": "rubric_review",
        "audit_status": "pass",
        "severity": "info",
        "finding": "Caller supplied audit finding.",
        "evidence_refs": ("rubric-review-001#criterion-001",),
        "notes": ("audit-check-only",),
    }
    values.update(overrides)
    return values


def _valid_values():
    return {
        "run_id": "run-001",
        "audit_review_id": "audit-review-001",
        "review_kind": "final",
        "artifact_refs": (
            "reader-artifact-001",
            "validator-result-001",
            "rubric-review-001",
        ),
        "audit_checks": (_audit_check(),),
        "required_audit_check_ids": ("audit-check-001",),
        "missing_audit_check_ids": (),
        "blocking_audit_check_ids": (),
        "audit_outcome": "passed",
        "created_at": "caller-supplied-created-at",
        "timestamp_policy": "caller_supplied_no_time_parsing",
        "source_of_truth": ("p2d-30",),
        "notes": ("structured-only",),
    }


def _explain(**overrides):
    values = _valid_values()
    values.update(overrides)
    return builder.explain_audit_review_build(**values)


def _payload_keys(value):
    keys = ()
    if isinstance(value, dict):
        for key, nested in value.items():
            keys = keys + (key,)
            if key != "invariant_refs":
                keys = keys + _payload_keys(nested)
    if isinstance(value, tuple):
        for item in value:
            keys = keys + _payload_keys(item)
    return keys


def test_reason_code_constants_are_exact_and_stably_prioritized():
    assert builder.REASON_CODES == REASON_CODES
    assert builder.AUDIT_REVIEW_BUILD_REASON_CODES == REASON_CODES
    assert builder.REASON_PRIORITY == REASON_PRIORITY


def test_valid_audit_review_is_buildable_with_exact_result_shapes():
    result = _explain()

    assert result["buildable"] is True
    assert result["reason_code"] == "AUDIT_REVIEW_BUILDABLE"
    assert result["audit_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()
    assert result["audit_check_violations"] == ()
    assert tuple(result.keys()) == RESULT_KEYS
    assert tuple(result["source"].keys()) == SOURCE_KEYS
    assert tuple(result["audit_review"].keys()) == AUDIT_REVIEW_KEYS
    assert tuple(result["audit_review"]["audit_checks"][0].keys()) == (
        AUDIT_CHECK_KEYS
    )
    assert result["source"]["artifact_refs"] == (
        "reader-artifact-001",
        "validator-result-001",
        "rubric-review-001",
    )
    assert result["audit_review"]["audit_checks"][0]["finding"] == (
        "Caller supplied audit finding."
    )


def test_public_api_is_keyword_only_and_bool_wrapper_matches_explain():
    expected_kwonly = len(AUDIT_REVIEW_KEYS)

    assert builder.explain_audit_review_build.__code__.co_argcount == 0
    assert builder.explain_audit_review_build.__code__.co_kwonlyargcount == (
        expected_kwonly
    )
    assert builder.is_audit_review_buildable.__code__.co_argcount == 0
    assert builder.is_audit_review_buildable.__code__.co_kwonlyargcount == (
        expected_kwonly
    )
    assert builder.is_audit_review_buildable(**_valid_values()) is True

    invalid_values = _valid_values()
    invalid_values["run_id"] = ""
    assert builder.is_audit_review_buildable(**invalid_values) is False
    assert _explain(run_id="")["buildable"] is False


def test_stub_and_final_review_kinds_are_buildable():
    stub = _explain(review_kind="stub")
    final = _explain(review_kind="final")

    assert stub["buildable"] is True
    assert stub["audit_review"]["review_kind"] == "stub"
    assert final["buildable"] is True
    assert final["audit_review"]["review_kind"] == "final"


def test_failed_outcome_and_known_blocking_ids_still_buildable():
    failed = _explain(audit_outcome="failed")
    blocked = _explain(
        blocking_audit_check_ids=("audit-check-001",),
        audit_outcome="failed",
    )

    assert failed["buildable"] is True
    assert blocked["buildable"] is True
    assert blocked["audit_review"]["blocking_audit_check_ids"] == (
        "audit-check-001",
    )


def test_unknown_blocking_audit_check_ids_block_buildability():
    cases = (
        ("unknown-audit-check",),
        ("",),
        (object(),),
        ["audit-check-001"],
    )

    for blocking_audit_check_ids in cases:
        result = _explain(blocking_audit_check_ids=blocking_audit_check_ids)

        assert result["buildable"] is False
        assert result["reason_code"] == "BLOCKING_AUDIT_CHECK_ID_UNKNOWN"
        assert "BLOCKING_AUDIT_CHECK_ID_UNKNOWN" in (
            result["audit_violations"]
        )
        assert "blocking_audit_check_ids" in (
            result["missing_or_invalid_fields"]
        )


def test_required_top_level_field_violations_are_collected():
    cases = (
        ({"run_id": ""}, "RUN_ID_MISSING", "run_id"),
        (
            {"audit_review_id": ""},
            "AUDIT_REVIEW_ID_MISSING",
            "audit_review_id",
        ),
        ({"review_kind": ""}, "REVIEW_KIND_MISSING", "review_kind"),
        ({"artifact_refs": ()}, "ARTIFACT_REFS_MISSING", "artifact_refs"),
        ({"artifact_refs": ("",)}, "ARTIFACT_REFS_MISSING", "artifact_refs"),
        (
            {"artifact_refs": ["reader-artifact-001"]},
            "ARTIFACT_REFS_MISSING",
            "artifact_refs",
        ),
        (
            {"audit_checks": ()},
            "AUDIT_CHECKS_MISSING",
            "audit_checks",
        ),
        (
            {"audit_checks": [_audit_check()]},
            "AUDIT_CHECKS_MISSING",
            "audit_checks",
        ),
        (
            {"required_audit_check_ids": ()},
            "REQUIRED_AUDIT_CHECK_IDS_MISSING",
            "required_audit_check_ids",
        ),
        (
            {"required_audit_check_ids": ("",)},
            "REQUIRED_AUDIT_CHECK_IDS_MISSING",
            "required_audit_check_ids",
        ),
        (
            {"required_audit_check_ids": ["audit-check-001"]},
            "REQUIRED_AUDIT_CHECK_IDS_MISSING",
            "required_audit_check_ids",
        ),
        (
            {"missing_audit_check_ids": ("audit-check-002",)},
            "MISSING_AUDIT_CHECK_IDS_DECLARED",
            "missing_audit_check_ids",
        ),
        (
            {"missing_audit_check_ids": ["audit-check-002"]},
            "MISSING_AUDIT_CHECK_IDS_DECLARED",
            "missing_audit_check_ids",
        ),
        (
            {"audit_outcome": ""},
            "AUDIT_OUTCOME_MISSING",
            "audit_outcome",
        ),
        ({"created_at": ""}, "CREATED_AT_MISSING", "created_at"),
        (
            {"timestamp_policy": ""},
            "TIMESTAMP_POLICY_MISSING",
            "timestamp_policy",
        ),
        (
            {"source_of_truth": ()},
            "SOURCE_OF_TRUTH_MISSING",
            "source_of_truth",
        ),
        (
            {"source_of_truth": ("",)},
            "SOURCE_OF_TRUTH_MISSING",
            "source_of_truth",
        ),
    )

    for overrides, reason_code, field in cases:
        result = _explain(**overrides)

        assert result["buildable"] is False
        assert reason_code in result["audit_violations"]
        assert field in result["missing_or_invalid_fields"]
        assert result["reason_code"] == result["audit_violations"][0]


def test_artifact_refs_and_evidence_refs_are_required_opaque_tuples():
    opaque_result = _explain(
        artifact_refs=("opaque-reader-ref", "opaque-rubric-ref"),
        audit_checks=(
            _audit_check(
                target_artifact_ref="opaque-rubric-ref",
                evidence_refs=("opaque-evidence-ref",),
            ),
        ),
    )
    empty_evidence = _explain(audit_checks=(_audit_check(evidence_refs=()),))
    list_evidence = _explain(
        audit_checks=(_audit_check(evidence_refs=["evidence"]),)
    )

    assert opaque_result["buildable"] is True
    assert empty_evidence["reason_code"] == (
        "AUDIT_CHECK_EVIDENCE_REFS_MISSING"
    )
    assert "AUDIT_CHECK_EVIDENCE_REFS_MISSING" in (
        list_evidence["audit_violations"]
    )
    assert "audit_checks[0].evidence_refs" in (
        list_evidence["missing_or_invalid_fields"]
    )


def test_allowed_audit_marker_names_are_not_falsely_banned():
    result = _explain()

    for field_name in ALLOWED_AUDIT_FIELD_NAMES:
        assert field_name not in FORBIDDEN_AUDIT_CHECK_FIELDS

    assert result["buildable"] is True
    assert result["audit_review"]["audit_outcome"] == "passed"
    assert result["audit_review"]["audit_checks"][0]["audit_status"] == "pass"


def test_audit_check_id_uniqueness_required_boundary_and_required_presence():
    duplicate = _explain(audit_checks=(_audit_check(), _audit_check()))
    not_required = _explain(
        audit_checks=(_audit_check(audit_check_id="audit-check-002"),),
        required_audit_check_ids=("audit-check-001",),
    )
    required_missing = _explain(
        required_audit_check_ids=("audit-check-001", "audit-check-002")
    )

    assert "AUDIT_CHECK_ID_DUPLICATE" in duplicate["audit_violations"]
    assert "AUDIT_CHECK_ID_NOT_REQUIRED" in not_required["audit_violations"]
    assert "REQUIRED_AUDIT_CHECK_MISSING" in not_required["audit_violations"]
    assert "REQUIRED_AUDIT_CHECK_MISSING" in (
        required_missing["audit_violations"]
    )
    assert "required_audit_check_ids.audit-check-002" in (
        required_missing["missing_or_invalid_fields"]
    )


def test_audit_check_fields_must_be_non_empty_and_missing_keys_reported():
    field_cases = (
        ("audit_check_id", "", "AUDIT_CHECK_ID_MISSING"),
        ("audit_check_role", "", "AUDIT_CHECK_ROLE_MISSING"),
        (
            "target_artifact_ref",
            "",
            "AUDIT_CHECK_TARGET_ARTIFACT_REF_MISSING",
        ),
        (
            "target_artifact_kind",
            "",
            "AUDIT_CHECK_TARGET_ARTIFACT_KIND_MISSING",
        ),
        ("audit_status", "", "AUDIT_CHECK_STATUS_MISSING"),
        ("severity", "", "AUDIT_CHECK_SEVERITY_MISSING"),
        ("finding", "", "AUDIT_CHECK_FINDING_MISSING"),
        ("evidence_refs", (), "AUDIT_CHECK_EVIDENCE_REFS_MISSING"),
    )

    for field, value, reason_code in field_cases:
        result = _explain(audit_checks=(_audit_check(**{field: value}),))

        assert reason_code in result["audit_violations"]
        assert f"audit_checks[0].{field}" in (
            result["missing_or_invalid_fields"]
        )
        assert tuple(result["audit_check_violations"][0].keys()) == (
            AUDIT_CHECK_VIOLATION_KEYS
        )

    for missing_key, expected_reason_code in (
        MISSING_AUDIT_CHECK_KEY_EXPECTATIONS
    ):
        audit_check = _audit_check()
        del audit_check[missing_key]
        result = _explain(audit_checks=(audit_check,))

        assert "AUDIT_CHECK_KEYS_INVALID" in result["audit_violations"]
        assert expected_reason_code in result["audit_violations"]
        assert f"audit_checks[0].{missing_key}" in (
            result["missing_or_invalid_fields"]
        ) or (
            missing_key == "notes"
            and "audit_checks[0].keys" in (
                result["missing_or_invalid_fields"]
            )
        )


def test_non_dict_audit_check_records_audit_check_violation_shape():
    result = _explain(audit_checks=("not-an-audit-check",))

    assert result["buildable"] is False
    assert result["reason_code"] == "AUDIT_CHECK_NOT_DICT"
    assert result["audit_violations"] == (
        "AUDIT_CHECK_NOT_DICT",
        "REQUIRED_AUDIT_CHECK_MISSING",
    )
    assert tuple(result["audit_check_violations"][0].keys()) == (
        AUDIT_CHECK_VIOLATION_KEYS
    )
    assert result["audit_review"]["audit_checks"][0] == {
        "audit_check_id": "",
        "audit_check_role": "",
        "target_artifact_ref": "",
        "target_artifact_kind": "",
        "audit_status": "",
        "severity": "",
        "finding": "",
        "evidence_refs": (),
        "notes": (),
    }


def test_forbidden_raw_read_fetch_judge_audit_gate_publish_fields_suppressed():
    for field in FORBIDDEN_AUDIT_CHECK_FIELDS:
        result = _explain(audit_checks=(_audit_check(**{field: "forbidden"}),))
        payload_keys = _payload_keys(result)

        assert "AUDIT_CHECK_FORBIDDEN_RAW_FIELD_PRESENT" in (
            result["audit_violations"]
        )
        assert "AUDIT_CHECK_KEYS_INVALID" in result["audit_violations"]
        assert field not in payload_keys
        assert tuple(result["audit_check_violations"][0].keys()) == (
            AUDIT_CHECK_VIOLATION_KEYS
        )


def test_reason_catalog_priority_and_forbidden_pseudo_reason_codes():
    assert builder.REASON_CODES == REASON_CODES
    assert builder.AUDIT_REVIEW_BUILD_REASON_CODES == REASON_CODES
    assert builder.REASON_PRIORITY == REASON_PRIORITY

    for reason_code in FORBIDDEN_PSEUDO_REASON_CODES:
        assert reason_code not in builder.REASON_CODES
        assert reason_code not in builder.REASON_PRIORITY


def test_forbidden_module_namespace_and_io_names_are_absent():
    for module_name in FORBIDDEN_MODULE_NAMES:
        assert not hasattr(builder, module_name)

    for io_name in (
        "hashlib",
        "requests",
        "subprocess",
        "urllib",
        "feedparser",
        "jinja2",
        "open",
        "datetime",
        "os",
        "pathlib",
        "logging",
    ):
        assert not hasattr(builder, io_name)


def test_all_violations_are_priority_ordered_and_detail_collections_present():
    first_audit_check = _audit_check(
        audit_check_id="",
        audit_check_role="",
        target_artifact_ref="",
        target_artifact_kind="",
        audit_status="",
        severity="",
        finding="",
        evidence_refs=(),
        raw_audit_output="raw",
    )
    second_audit_check = _audit_check(audit_check_id="extra-audit-check")
    result = _explain(
        run_id="",
        audit_review_id="",
        review_kind="",
        artifact_refs=(),
        audit_checks=(first_audit_check, second_audit_check),
        required_audit_check_ids=("audit-check-001", "audit-check-002"),
        missing_audit_check_ids=("audit-check-002",),
        blocking_audit_check_ids=("missing-block",),
        audit_outcome="",
        created_at="",
        timestamp_policy="",
        source_of_truth=(),
    )
    expected_order = tuple(
        reason_code
        for reason_code in REASON_PRIORITY
        if reason_code != "AUDIT_REVIEW_BUILDABLE"
        and reason_code in result["audit_violations"]
    )

    assert result["audit_violations"] == expected_order
    assert result["reason_code"] == result["audit_violations"][0]
    assert "audit_checks[0].raw_audit_output" in (
        result["missing_or_invalid_fields"]
    )
    assert "audit_checks[1].audit_check_id" in (
        result["missing_or_invalid_fields"]
    )
    assert "required_audit_check_ids.audit-check-002" in (
        result["missing_or_invalid_fields"]
    )
    assert result["audit_check_violations"] != ()
    for audit_check_violation in result["audit_check_violations"]:
        assert tuple(audit_check_violation.keys()) == (
            AUDIT_CHECK_VIOLATION_KEYS
        )


def test_invariant_refs_capture_governance_and_no_execution_boundaries():
    result = _explain()

    assert result["invariant_refs"] == REQUIRED_INVARIANT_REFS


def test_payload_key_traversal_skips_invariants_instead_of_blanket_scans():
    result = _explain()
    payload_keys = _payload_keys(result)

    assert "no_raw_url" in result["invariant_refs"]
    assert "no_public_url_behavior" in result["invariant_refs"]
    assert "no_raw_url" not in payload_keys
    assert "no_public_url_behavior" not in payload_keys
