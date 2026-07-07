"""Tests for the pure rubric review artifact buildability builder."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import rubric_review_builder as builder


RESULT_KEYS = (
    "buildable",
    "reason_code",
    "reason",
    "source",
    "rubric_review",
    "rubric_violations",
    "missing_or_invalid_fields",
    "criterion_violations",
    "invariant_refs",
)

SOURCE_KEYS = (
    "artifact_refs",
    "source_of_truth",
)

RUBRIC_REVIEW_KEYS = (
    "run_id",
    "rubric_review_id",
    "review_kind",
    "artifact_refs",
    "rubric_criteria",
    "required_criterion_ids",
    "missing_criterion_ids",
    "blocking_criterion_ids",
    "rubric_outcome",
    "score_total",
    "score_threshold",
    "created_at",
    "timestamp_policy",
    "source_of_truth",
    "notes",
)

CRITERION_KEYS = (
    "criterion_id",
    "criterion_role",
    "target_artifact_ref",
    "target_artifact_kind",
    "criterion_status",
    "severity",
    "score",
    "max_score",
    "finding",
    "evidence_refs",
    "notes",
)

CRITERION_VIOLATION_KEYS = (
    "criterion_index",
    "criterion_id",
    "reason_code",
    "field",
)

REASON_CODES = (
    "RUBRIC_REVIEW_BUILDABLE",
    "RUN_ID_MISSING",
    "RUBRIC_REVIEW_ID_MISSING",
    "REVIEW_KIND_MISSING",
    "ARTIFACT_REFS_MISSING",
    "RUBRIC_CRITERIA_MISSING",
    "REQUIRED_CRITERION_IDS_MISSING",
    "MISSING_CRITERION_IDS_DECLARED",
    "BLOCKING_CRITERION_ID_UNKNOWN",
    "RUBRIC_OUTCOME_MISSING",
    "SCORE_TOTAL_MISSING",
    "SCORE_THRESHOLD_MISSING",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "CRITERION_NOT_DICT",
    "CRITERION_KEYS_INVALID",
    "CRITERION_ID_MISSING",
    "CRITERION_ROLE_MISSING",
    "CRITERION_TARGET_ARTIFACT_REF_MISSING",
    "CRITERION_TARGET_ARTIFACT_KIND_MISSING",
    "CRITERION_STATUS_MISSING",
    "CRITERION_SEVERITY_MISSING",
    "CRITERION_SCORE_MISSING",
    "CRITERION_MAX_SCORE_MISSING",
    "CRITERION_FINDING_MISSING",
    "CRITERION_EVIDENCE_REFS_MISSING",
    "CRITERION_ID_DUPLICATE",
    "CRITERION_ID_NOT_REQUIRED",
    "REQUIRED_CRITERION_MISSING",
    "CRITERION_FORBIDDEN_RAW_FIELD_PRESENT",
)

REASON_PRIORITY = (
    "RUN_ID_MISSING",
    "RUBRIC_REVIEW_ID_MISSING",
    "REVIEW_KIND_MISSING",
    "ARTIFACT_REFS_MISSING",
    "RUBRIC_CRITERIA_MISSING",
    "REQUIRED_CRITERION_IDS_MISSING",
    "MISSING_CRITERION_IDS_DECLARED",
    "BLOCKING_CRITERION_ID_UNKNOWN",
    "RUBRIC_OUTCOME_MISSING",
    "SCORE_TOTAL_MISSING",
    "SCORE_THRESHOLD_MISSING",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "CRITERION_NOT_DICT",
    "CRITERION_KEYS_INVALID",
    "CRITERION_ID_MISSING",
    "CRITERION_ROLE_MISSING",
    "CRITERION_TARGET_ARTIFACT_REF_MISSING",
    "CRITERION_TARGET_ARTIFACT_KIND_MISSING",
    "CRITERION_STATUS_MISSING",
    "CRITERION_SEVERITY_MISSING",
    "CRITERION_SCORE_MISSING",
    "CRITERION_MAX_SCORE_MISSING",
    "CRITERION_FINDING_MISSING",
    "CRITERION_EVIDENCE_REFS_MISSING",
    "CRITERION_ID_DUPLICATE",
    "CRITERION_ID_NOT_REQUIRED",
    "REQUIRED_CRITERION_MISSING",
    "CRITERION_FORBIDDEN_RAW_FIELD_PRESENT",
    "RUBRIC_REVIEW_BUILDABLE",
)

FORBIDDEN_CRITERION_FIELDS = (
    "raw_rubric_output",
    "raw_review_output",
    "review_output",
    "rubric_output",
    "raw_judge_output",
    "judge_output",
    "llm_judge_output",
    "llm_output",
    "raw_llm_output",
    "human_review_output",
    "human_review_result",
    "score_computation",
    "computed_score",
    "computed_total",
    "computed_threshold",
    "score_explanation",
    "raw_score_explanation",
    "quality_pass",
    "rubric_pass",
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
    "audit_result",
    "gate_result",
    "publish_result",
    "should_fetch",
    "should_read_reader",
    "should_read_training_report",
    "should_read_validator_result",
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
    "should_score",
    "should_validate",
    "should_run_validator",
    "should_eval",
    "should_audit",
    "should_gate",
    "should_publish",
    "should_create_public_url",
    "reader_read",
    "training_report_read",
    "validator_result_read",
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
    "rubric_executed",
    "validator_executed",
    "eval_executed",
    "audit_executed",
    "gate_executed",
    "published",
    "public_url_created",
)

ALLOWED_RUBRIC_FIELD_NAMES = (
    "rubric_review_id",
    "rubric_review",
    "review_kind",
    "rubric_criteria",
    "required_criterion_ids",
    "missing_criterion_ids",
    "blocking_criterion_ids",
    "rubric_outcome",
    "score_total",
    "score_threshold",
    "criterion_status",
    "target_artifact_ref",
    "target_artifact_kind",
    "artifact_refs",
    "evidence_refs",
    "score",
    "max_score",
)

FORBIDDEN_PSEUDO_REASON_CODES = (
    "READER_READ_FORBIDDEN",
    "TRAINING_REPORT_READ_FORBIDDEN",
    "VALIDATOR_RESULT_READ_FORBIDDEN",
    "SOURCE_MANIFEST_READ_FORBIDDEN",
    "SOURCE_NOTES_READ_FORBIDDEN",
    "SOURCE_CONTENT_READ_FORBIDDEN",
    "FILE_READ_FORBIDDEN",
    "WEB_FETCH_FORBIDDEN",
    "GITHUB_FETCH_FORBIDDEN",
    "RSS_FETCH_FORBIDDEN",
    "NOTION_FETCH_FORBIDDEN",
    "LLM_JUDGE_FORBIDDEN",
    "HUMAN_REVIEW_FORBIDDEN",
    "RUBRIC_EXECUTION_FORBIDDEN",
    "SCORE_COMPUTATION_FORBIDDEN",
    "VALIDATOR_EXECUTION_FORBIDDEN",
    "EVAL_EXECUTION_FORBIDDEN",
    "AUDIT_EXECUTION_FORBIDDEN",
    "GATE_EXECUTION_FORBIDDEN",
    "PUBLISH_FORBIDDEN",
    "PUBLIC_URL_CREATION_FORBIDDEN",
)

FORBIDDEN_MODULE_NAMES = (
    "states",
    "gates",
    "artifacts",
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
    "build_rubric_review",
    "run_rubric_review",
    "run_rubric_scoring",
    "compute_score",
    "judge_rubric",
    "call_llm_judge",
    "validate_artifact",
    "validate_reader",
    "validate_schema",
    "validate_html",
    "execute_validator",
    "build_gate_decision",
)

REQUIRED_INVARIANT_REFS = (
    "rubric_review_builder_only",
    "builder_not_reader_reader",
    "builder_not_training_report_reader",
    "builder_not_validator_result_reader",
    "builder_not_source_manifest_reader",
    "builder_not_source_notes_reader",
    "builder_not_source_reader",
    "builder_not_file_reader",
    "builder_not_web_fetcher",
    "builder_not_github_fetcher",
    "builder_not_rss_fetcher",
    "builder_not_notion_fetcher",
    "builder_not_llm_judge",
    "builder_not_human_reviewer",
    "builder_not_rubric_executor",
    "builder_not_score_computer",
    "builder_not_validator_executor",
    "builder_not_eval_executor",
    "builder_not_audit_executor",
    "builder_not_gate_executor",
    "builder_not_publisher",
    "rubric_criteria_are_caller_supplied",
    "criterion_findings_are_caller_supplied",
    "criterion_scores_are_caller_supplied",
    "artifact_refs_opaque",
    "target_artifact_refs_opaque",
    "evidence_refs_opaque",
    "rubric_review_governance_evidence",
    "rubric_review_not_public_candidate",
    "rubric_outcome_not_quality_pass",
    "rubric_outcome_not_publish_allowed",
    "score_total_not_quality_pass",
    "score_threshold_not_publish_gate",
    "buildable_not_rubric_pass",
    "buildable_not_quality_pass",
    "buildable_not_eval_pass",
    "buildable_not_audit_pass",
    "buildable_not_publish_allowed",
    "buildable_not_public_url_created",
    "blocking_criterion_ids_are_gate_evidence_only",
    "blocking_criterion_ids_do_not_execute_gate",
    "no_reader_read",
    "no_training_report_read",
    "no_validator_result_read",
    "no_source_manifest_read",
    "no_source_notes_read",
    "no_source_content_read",
    "no_url_fetch",
    "no_rss_fetch",
    "no_file_read",
    "no_raw_content",
    "no_raw_url",
    "no_generated_review",
    "no_llm_summary",
    "no_llm_judge",
    "no_human_review_workflow",
    "no_score_computation",
    "no_inferred_fact_generation",
    "no_hash_calculation",
    "no_existing_builder_or_policy_call",
    "no_rubric_execution",
    "no_validator_execution",
    "no_eval_execution",
    "no_audit_execution",
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

MISSING_CRITERION_KEY_EXPECTATIONS = (
    ("criterion_id", "CRITERION_ID_MISSING"),
    ("criterion_role", "CRITERION_ROLE_MISSING"),
    ("target_artifact_ref", "CRITERION_TARGET_ARTIFACT_REF_MISSING"),
    ("target_artifact_kind", "CRITERION_TARGET_ARTIFACT_KIND_MISSING"),
    ("criterion_status", "CRITERION_STATUS_MISSING"),
    ("severity", "CRITERION_SEVERITY_MISSING"),
    ("score", "CRITERION_SCORE_MISSING"),
    ("max_score", "CRITERION_MAX_SCORE_MISSING"),
    ("finding", "CRITERION_FINDING_MISSING"),
    ("evidence_refs", "CRITERION_EVIDENCE_REFS_MISSING"),
    ("notes", "CRITERION_KEYS_INVALID"),
)


def _criterion(**overrides):
    values = {
        "criterion_id": "criterion-001",
        "criterion_role": "thinking_depth",
        "target_artifact_ref": "reader-artifact-001",
        "target_artifact_kind": "reader_artifact",
        "criterion_status": "pass",
        "severity": "info",
        "score": "8",
        "max_score": "10",
        "finding": "Caller supplied rubric finding.",
        "evidence_refs": ("reader-artifact-001#block-001",),
        "notes": ("rubric-criterion-only",),
    }
    values.update(overrides)
    return values


def _valid_values():
    return {
        "run_id": "run-001",
        "rubric_review_id": "rubric-review-001",
        "review_kind": "final",
        "artifact_refs": ("reader-artifact-001", "validator-result-001"),
        "rubric_criteria": (_criterion(),),
        "required_criterion_ids": ("criterion-001",),
        "missing_criterion_ids": (),
        "blocking_criterion_ids": (),
        "rubric_outcome": "passed",
        "score_total": "85",
        "score_threshold": "80",
        "created_at": "caller-supplied-created-at",
        "timestamp_policy": "caller_supplied_no_time_parsing",
        "source_of_truth": ("p2d-29",),
        "notes": ("structured-only",),
    }


def _explain(**overrides):
    values = _valid_values()
    values.update(overrides)
    return builder.explain_rubric_review_build(**values)


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
    assert builder.RUBRIC_REVIEW_BUILD_REASON_CODES == REASON_CODES
    assert builder.REASON_PRIORITY == REASON_PRIORITY


def test_valid_rubric_review_is_buildable_with_exact_result_shapes():
    result = _explain()

    assert result["buildable"] is True
    assert result["reason_code"] == "RUBRIC_REVIEW_BUILDABLE"
    assert result["rubric_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()
    assert result["criterion_violations"] == ()
    assert tuple(result.keys()) == RESULT_KEYS
    assert tuple(result["source"].keys()) == SOURCE_KEYS
    assert tuple(result["rubric_review"].keys()) == RUBRIC_REVIEW_KEYS
    assert tuple(result["rubric_review"]["rubric_criteria"][0].keys()) == (
        CRITERION_KEYS
    )
    assert result["source"]["artifact_refs"] == (
        "reader-artifact-001",
        "validator-result-001",
    )
    assert result["rubric_review"]["rubric_criteria"][0]["finding"] == (
        "Caller supplied rubric finding."
    )
    assert result["rubric_review"]["rubric_criteria"][0]["score"] == "8"
    assert result["rubric_review"]["rubric_criteria"][0]["max_score"] == "10"


def test_public_api_is_keyword_only_and_bool_wrapper_matches_explain():
    expected_kwonly = len(RUBRIC_REVIEW_KEYS)

    assert builder.explain_rubric_review_build.__code__.co_argcount == 0
    assert builder.explain_rubric_review_build.__code__.co_kwonlyargcount == (
        expected_kwonly
    )
    assert builder.is_rubric_review_buildable.__code__.co_argcount == 0
    assert builder.is_rubric_review_buildable.__code__.co_kwonlyargcount == (
        expected_kwonly
    )
    assert builder.is_rubric_review_buildable(**_valid_values()) is True

    invalid_values = _valid_values()
    invalid_values["run_id"] = ""
    assert builder.is_rubric_review_buildable(**invalid_values) is False
    assert _explain(run_id="")["buildable"] is False


def test_stub_and_final_review_kinds_are_buildable():
    stub = _explain(review_kind="stub")
    final = _explain(review_kind="final")

    assert stub["buildable"] is True
    assert stub["rubric_review"]["review_kind"] == "stub"
    assert final["buildable"] is True
    assert final["rubric_review"]["review_kind"] == "final"


def test_failed_outcome_low_score_and_known_blocking_ids_still_buildable():
    failed = _explain(rubric_outcome="failed")
    low_score = _explain(score_total="20", score_threshold="80")
    blocking = _explain(
        blocking_criterion_ids=("criterion-001",),
        rubric_outcome="failed",
        score_total="20",
        score_threshold="80",
    )

    assert failed["buildable"] is True
    assert low_score["buildable"] is True
    assert blocking["buildable"] is True
    assert blocking["rubric_review"]["blocking_criterion_ids"] == (
        "criterion-001",
    )


def test_unknown_blocking_criterion_ids_block_buildability():
    cases = (
        ("unknown-criterion",),
        ("",),
        (object(),),
        ["criterion-001"],
    )

    for blocking_criterion_ids in cases:
        result = _explain(blocking_criterion_ids=blocking_criterion_ids)

        assert result["buildable"] is False
        assert result["reason_code"] == "BLOCKING_CRITERION_ID_UNKNOWN"
        assert "BLOCKING_CRITERION_ID_UNKNOWN" in result["rubric_violations"]
        assert "blocking_criterion_ids" in result["missing_or_invalid_fields"]


def test_required_top_level_field_violations_are_collected():
    cases = (
        ({"run_id": ""}, "RUN_ID_MISSING", "run_id"),
        (
            {"rubric_review_id": ""},
            "RUBRIC_REVIEW_ID_MISSING",
            "rubric_review_id",
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
            {"rubric_criteria": ()},
            "RUBRIC_CRITERIA_MISSING",
            "rubric_criteria",
        ),
        (
            {"rubric_criteria": [_criterion()]},
            "RUBRIC_CRITERIA_MISSING",
            "rubric_criteria",
        ),
        (
            {"required_criterion_ids": ()},
            "REQUIRED_CRITERION_IDS_MISSING",
            "required_criterion_ids",
        ),
        (
            {"required_criterion_ids": ("",)},
            "REQUIRED_CRITERION_IDS_MISSING",
            "required_criterion_ids",
        ),
        (
            {"required_criterion_ids": ["criterion-001"]},
            "REQUIRED_CRITERION_IDS_MISSING",
            "required_criterion_ids",
        ),
        (
            {"missing_criterion_ids": ("criterion-002",)},
            "MISSING_CRITERION_IDS_DECLARED",
            "missing_criterion_ids",
        ),
        (
            {"missing_criterion_ids": ["criterion-002"]},
            "MISSING_CRITERION_IDS_DECLARED",
            "missing_criterion_ids",
        ),
        (
            {"rubric_outcome": ""},
            "RUBRIC_OUTCOME_MISSING",
            "rubric_outcome",
        ),
        ({"score_total": ""}, "SCORE_TOTAL_MISSING", "score_total"),
        (
            {"score_threshold": ""},
            "SCORE_THRESHOLD_MISSING",
            "score_threshold",
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
        assert reason_code in result["rubric_violations"]
        assert field in result["missing_or_invalid_fields"]
        assert result["reason_code"] == result["rubric_violations"][0]


def test_artifact_refs_and_evidence_refs_are_required_opaque_tuples():
    opaque_result = _explain(
        artifact_refs=("opaque-reader-ref", "opaque-validator-ref"),
        rubric_criteria=(
            _criterion(
                target_artifact_ref="opaque-reader-ref",
                evidence_refs=("opaque-evidence-ref",),
            ),
        ),
    )
    empty_evidence = _explain(rubric_criteria=(_criterion(evidence_refs=()),))
    list_evidence = _explain(
        rubric_criteria=(_criterion(evidence_refs=["evidence"]),)
    )

    assert opaque_result["buildable"] is True
    assert empty_evidence["reason_code"] == "CRITERION_EVIDENCE_REFS_MISSING"
    assert "CRITERION_EVIDENCE_REFS_MISSING" in (
        list_evidence["rubric_violations"]
    )
    assert "rubric_criteria[0].evidence_refs" in (
        list_evidence["missing_or_invalid_fields"]
    )


def test_allowed_rubric_and_score_marker_names_are_not_falsely_banned():
    result = _explain()

    for field_name in ALLOWED_RUBRIC_FIELD_NAMES:
        assert field_name not in FORBIDDEN_CRITERION_FIELDS

    assert result["buildable"] is True
    assert result["rubric_review"]["score_total"] == "85"
    assert result["rubric_review"]["score_threshold"] == "80"
    assert result["rubric_review"]["rubric_criteria"][0]["score"] == "8"
    assert result["rubric_review"]["rubric_criteria"][0]["max_score"] == "10"


def test_criterion_id_uniqueness_required_boundary_and_required_presence():
    duplicate = _explain(rubric_criteria=(_criterion(), _criterion()))
    not_required = _explain(
        rubric_criteria=(_criterion(criterion_id="criterion-002"),),
        required_criterion_ids=("criterion-001",),
    )
    required_missing = _explain(
        required_criterion_ids=("criterion-001", "criterion-002")
    )

    assert "CRITERION_ID_DUPLICATE" in duplicate["rubric_violations"]
    assert "CRITERION_ID_NOT_REQUIRED" in not_required["rubric_violations"]
    assert "REQUIRED_CRITERION_MISSING" in not_required["rubric_violations"]
    assert "REQUIRED_CRITERION_MISSING" in required_missing["rubric_violations"]
    assert "required_criterion_ids.criterion-002" in (
        required_missing["missing_or_invalid_fields"]
    )


def test_criterion_fields_must_be_non_empty_and_missing_keys_are_reported():
    field_cases = (
        ("criterion_id", "", "CRITERION_ID_MISSING"),
        ("criterion_role", "", "CRITERION_ROLE_MISSING"),
        (
            "target_artifact_ref",
            "",
            "CRITERION_TARGET_ARTIFACT_REF_MISSING",
        ),
        (
            "target_artifact_kind",
            "",
            "CRITERION_TARGET_ARTIFACT_KIND_MISSING",
        ),
        ("criterion_status", "", "CRITERION_STATUS_MISSING"),
        ("severity", "", "CRITERION_SEVERITY_MISSING"),
        ("score", "", "CRITERION_SCORE_MISSING"),
        ("max_score", "", "CRITERION_MAX_SCORE_MISSING"),
        ("finding", "", "CRITERION_FINDING_MISSING"),
        ("evidence_refs", (), "CRITERION_EVIDENCE_REFS_MISSING"),
    )

    for field, value, reason_code in field_cases:
        result = _explain(rubric_criteria=(_criterion(**{field: value}),))

        assert reason_code in result["rubric_violations"]
        assert f"rubric_criteria[0].{field}" in (
            result["missing_or_invalid_fields"]
        )
        assert tuple(result["criterion_violations"][0].keys()) == (
            CRITERION_VIOLATION_KEYS
        )

    for missing_key, expected_reason_code in MISSING_CRITERION_KEY_EXPECTATIONS:
        criterion = _criterion()
        del criterion[missing_key]
        result = _explain(rubric_criteria=(criterion,))

        assert "CRITERION_KEYS_INVALID" in result["rubric_violations"]
        assert expected_reason_code in result["rubric_violations"]
        assert f"rubric_criteria[0].{missing_key}" in (
            result["missing_or_invalid_fields"]
        ) or (
            missing_key == "notes"
            and "rubric_criteria[0].keys" in (
                result["missing_or_invalid_fields"]
            )
        )


def test_non_dict_criterion_records_criterion_violation_shape():
    result = _explain(rubric_criteria=("not-a-criterion",))

    assert result["buildable"] is False
    assert result["reason_code"] == "CRITERION_NOT_DICT"
    assert result["rubric_violations"] == (
        "CRITERION_NOT_DICT",
        "REQUIRED_CRITERION_MISSING",
    )
    assert tuple(result["criterion_violations"][0].keys()) == (
        CRITERION_VIOLATION_KEYS
    )
    assert result["rubric_review"]["rubric_criteria"][0] == {
        "criterion_id": "",
        "criterion_role": "",
        "target_artifact_ref": "",
        "target_artifact_kind": "",
        "criterion_status": "",
        "severity": "",
        "score": "",
        "max_score": "",
        "finding": "",
        "evidence_refs": (),
        "notes": (),
    }


def test_forbidden_raw_read_fetch_judge_score_gate_publish_fields_are_suppressed():
    for field in FORBIDDEN_CRITERION_FIELDS:
        result = _explain(rubric_criteria=(_criterion(**{field: "forbidden"}),))
        payload_keys = _payload_keys(result)

        assert "CRITERION_FORBIDDEN_RAW_FIELD_PRESENT" in (
            result["rubric_violations"]
        )
        assert "CRITERION_KEYS_INVALID" in result["rubric_violations"]
        assert field not in payload_keys
        assert tuple(result["criterion_violations"][0].keys()) == (
            CRITERION_VIOLATION_KEYS
        )


def test_reason_catalog_priority_and_forbidden_pseudo_reason_codes():
    assert builder.REASON_CODES == REASON_CODES
    assert builder.RUBRIC_REVIEW_BUILD_REASON_CODES == REASON_CODES
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


def test_all_violations_are_priority_ordered_and_detail_collections_are_present():
    first_criterion = _criterion(
        criterion_id="",
        criterion_role="",
        target_artifact_ref="",
        target_artifact_kind="",
        criterion_status="",
        severity="",
        score="",
        max_score="",
        finding="",
        evidence_refs=(),
        raw_rubric_output="raw",
    )
    second_criterion = _criterion(criterion_id="extra-criterion")
    result = _explain(
        run_id="",
        rubric_review_id="",
        review_kind="",
        artifact_refs=(),
        rubric_criteria=(first_criterion, second_criterion),
        required_criterion_ids=("criterion-001", "criterion-002"),
        missing_criterion_ids=("criterion-002",),
        blocking_criterion_ids=("missing-block",),
        rubric_outcome="",
        score_total="",
        score_threshold="",
        created_at="",
        timestamp_policy="",
        source_of_truth=(),
    )
    expected_order = tuple(
        reason_code
        for reason_code in REASON_PRIORITY
        if reason_code != "RUBRIC_REVIEW_BUILDABLE"
        and reason_code in result["rubric_violations"]
    )

    assert result["rubric_violations"] == expected_order
    assert result["reason_code"] == result["rubric_violations"][0]
    assert "rubric_criteria[0].raw_rubric_output" in (
        result["missing_or_invalid_fields"]
    )
    assert "rubric_criteria[1].criterion_id" in (
        result["missing_or_invalid_fields"]
    )
    assert "required_criterion_ids.criterion-002" in (
        result["missing_or_invalid_fields"]
    )
    assert result["criterion_violations"] != ()
    for criterion_violation in result["criterion_violations"]:
        assert tuple(criterion_violation.keys()) == CRITERION_VIOLATION_KEYS


def test_invariant_refs_capture_governance_and_no_execution_boundaries():
    result = _explain()

    for invariant_ref in REQUIRED_INVARIANT_REFS:
        assert invariant_ref in result["invariant_refs"]


def test_payload_key_traversal_skips_invariants_instead_of_blanket_result_scans():
    result = _explain()
    payload_keys = _payload_keys(result)

    assert "no_raw_url" in result["invariant_refs"]
    assert "no_public_url_behavior" in result["invariant_refs"]
    assert "no_raw_url" not in payload_keys
    assert "no_public_url_behavior" not in payload_keys
