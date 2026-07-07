"""Tests for the pure validator result buildability builder."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import validator_result_builder as builder


RESULT_KEYS = (
    "buildable",
    "reason_code",
    "reason",
    "source",
    "validator_result",
    "validator_violations",
    "missing_or_invalid_fields",
    "check_violations",
    "invariant_refs",
)

SOURCE_KEYS = (
    "artifact_refs",
    "source_of_truth",
)

VALIDATOR_RESULT_KEYS = (
    "run_id",
    "validator_result_id",
    "artifact_refs",
    "validation_checks",
    "required_check_ids",
    "missing_check_ids",
    "blocking_check_ids",
    "validator_outcome",
    "created_at",
    "timestamp_policy",
    "source_of_truth",
    "notes",
)

CHECK_KEYS = (
    "check_id",
    "check_role",
    "target_artifact_ref",
    "target_artifact_kind",
    "check_status",
    "severity",
    "finding",
    "evidence_refs",
    "notes",
)

CHECK_VIOLATION_KEYS = (
    "check_index",
    "check_id",
    "reason_code",
    "field",
)

REASON_CODES = (
    "VALIDATOR_RESULT_BUILDABLE",
    "RUN_ID_MISSING",
    "VALIDATOR_RESULT_ID_MISSING",
    "ARTIFACT_REFS_MISSING",
    "VALIDATION_CHECKS_MISSING",
    "REQUIRED_CHECK_IDS_MISSING",
    "MISSING_CHECK_IDS_DECLARED",
    "BLOCKING_CHECK_ID_UNKNOWN",
    "VALIDATOR_OUTCOME_MISSING",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "CHECK_NOT_DICT",
    "CHECK_KEYS_INVALID",
    "CHECK_ID_MISSING",
    "CHECK_ROLE_MISSING",
    "CHECK_TARGET_ARTIFACT_REF_MISSING",
    "CHECK_TARGET_ARTIFACT_KIND_MISSING",
    "CHECK_STATUS_MISSING",
    "CHECK_SEVERITY_MISSING",
    "CHECK_FINDING_MISSING",
    "CHECK_EVIDENCE_REFS_MISSING",
    "CHECK_ID_DUPLICATE",
    "CHECK_ID_NOT_REQUIRED",
    "REQUIRED_CHECK_MISSING",
    "CHECK_FORBIDDEN_RAW_FIELD_PRESENT",
)

REASON_PRIORITY = (
    "RUN_ID_MISSING",
    "VALIDATOR_RESULT_ID_MISSING",
    "ARTIFACT_REFS_MISSING",
    "VALIDATION_CHECKS_MISSING",
    "REQUIRED_CHECK_IDS_MISSING",
    "MISSING_CHECK_IDS_DECLARED",
    "BLOCKING_CHECK_ID_UNKNOWN",
    "VALIDATOR_OUTCOME_MISSING",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "CHECK_NOT_DICT",
    "CHECK_KEYS_INVALID",
    "CHECK_ID_MISSING",
    "CHECK_ROLE_MISSING",
    "CHECK_TARGET_ARTIFACT_REF_MISSING",
    "CHECK_TARGET_ARTIFACT_KIND_MISSING",
    "CHECK_STATUS_MISSING",
    "CHECK_SEVERITY_MISSING",
    "CHECK_FINDING_MISSING",
    "CHECK_EVIDENCE_REFS_MISSING",
    "CHECK_ID_DUPLICATE",
    "CHECK_ID_NOT_REQUIRED",
    "REQUIRED_CHECK_MISSING",
    "CHECK_FORBIDDEN_RAW_FIELD_PRESENT",
    "VALIDATOR_RESULT_BUILDABLE",
)

FORBIDDEN_CHECK_FIELDS = (
    "raw_validation_output",
    "raw_validator_output",
    "validation_output",
    "validator_output",
    "schema_validation_result",
    "html_validation_result",
    "link_check_result",
    "content_quality_result",
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
    "gate_result",
    "publish_result",
    "should_fetch",
    "should_read_reader",
    "should_read_training_report",
    "should_read_source_manifest",
    "should_read_source_notes",
    "should_read_source",
    "should_read_file",
    "should_call_web",
    "should_call_github",
    "should_call_rss",
    "should_call_notion",
    "should_validate",
    "should_run_validator",
    "should_eval",
    "should_audit",
    "should_gate",
    "should_publish",
    "should_create_public_url",
    "reader_read",
    "training_report_read",
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
    "validator_executed",
    "eval_executed",
    "audit_executed",
    "gate_executed",
    "published",
    "public_url_created",
)

FORBIDDEN_PSEUDO_REASON_CODES = (
    "READER_READ_FORBIDDEN",
    "TRAINING_REPORT_READ_FORBIDDEN",
    "SOURCE_MANIFEST_READ_FORBIDDEN",
    "SOURCE_NOTES_READ_FORBIDDEN",
    "SOURCE_CONTENT_READ_FORBIDDEN",
    "FILE_READ_FORBIDDEN",
    "WEB_FETCH_FORBIDDEN",
    "GITHUB_FETCH_FORBIDDEN",
    "RSS_FETCH_FORBIDDEN",
    "NOTION_FETCH_FORBIDDEN",
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
    "build_validator_result",
    "run_validator",
    "validate_artifact",
    "validate_reader",
    "validate_schema",
    "validate_html",
    "execute_validator",
    "build_gate_decision",
)

REQUIRED_INVARIANT_REFS = (
    "validator_result_builder_only",
    "builder_not_reader_reader",
    "builder_not_training_report_reader",
    "builder_not_source_manifest_reader",
    "builder_not_source_notes_reader",
    "builder_not_source_reader",
    "builder_not_file_reader",
    "builder_not_web_fetcher",
    "builder_not_github_fetcher",
    "builder_not_rss_fetcher",
    "builder_not_notion_fetcher",
    "builder_not_llm_summarizer",
    "builder_not_validator_executor",
    "builder_not_eval_executor",
    "builder_not_audit_executor",
    "builder_not_gate_executor",
    "builder_not_publisher",
    "validation_checks_are_caller_supplied",
    "check_findings_are_caller_supplied",
    "artifact_refs_opaque",
    "target_artifact_refs_opaque",
    "evidence_refs_opaque",
    "validator_result_governance_evidence",
    "validator_result_not_public_candidate",
    "validator_outcome_not_quality_pass",
    "validator_outcome_not_publish_allowed",
    "buildable_not_validator_pass",
    "buildable_not_quality_pass",
    "buildable_not_eval_pass",
    "buildable_not_audit_pass",
    "buildable_not_publish_allowed",
    "buildable_not_public_url_created",
    "blocking_check_ids_are_gate_evidence_only",
    "blocking_check_ids_do_not_execute_gate",
    "no_reader_read",
    "no_training_report_read",
    "no_source_manifest_read",
    "no_source_notes_read",
    "no_source_content_read",
    "no_url_fetch",
    "no_rss_fetch",
    "no_file_read",
    "no_raw_content",
    "no_raw_url",
    "no_generated_validation",
    "no_llm_summary",
    "no_inferred_fact_generation",
    "no_hash_calculation",
    "no_existing_builder_or_policy_call",
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

MISSING_CHECK_KEY_EXPECTATIONS = (
    ("check_id", "CHECK_ID_MISSING"),
    ("check_role", "CHECK_ROLE_MISSING"),
    ("target_artifact_ref", "CHECK_TARGET_ARTIFACT_REF_MISSING"),
    ("target_artifact_kind", "CHECK_TARGET_ARTIFACT_KIND_MISSING"),
    ("check_status", "CHECK_STATUS_MISSING"),
    ("severity", "CHECK_SEVERITY_MISSING"),
    ("finding", "CHECK_FINDING_MISSING"),
    ("evidence_refs", "CHECK_EVIDENCE_REFS_MISSING"),
    ("notes", "CHECK_KEYS_INVALID"),
)


def _check(**overrides):
    values = {
        "check_id": "check-001",
        "check_role": "reader_artifact_shape",
        "target_artifact_ref": "reader-artifact-001",
        "target_artifact_kind": "reader_artifact",
        "check_status": "pass",
        "severity": "info",
        "finding": "Caller supplied validation finding.",
        "evidence_refs": ("reader-artifact-001#block-001",),
        "notes": ("shape-only",),
    }
    values.update(overrides)
    return values


def _valid_values():
    return {
        "run_id": "run-001",
        "validator_result_id": "validator-result-001",
        "artifact_refs": ("reader-artifact-001",),
        "validation_checks": (_check(),),
        "required_check_ids": ("check-001",),
        "missing_check_ids": (),
        "blocking_check_ids": (),
        "validator_outcome": "passed",
        "created_at": "caller-supplied-created-at",
        "timestamp_policy": "caller_supplied_no_time_parsing",
        "source_of_truth": ("p2d-28",),
        "notes": ("structured-only",),
    }


def _explain(**overrides):
    values = _valid_values()
    values.update(overrides)
    return builder.explain_validator_result_build(**values)


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


def test_valid_validator_result_is_buildable_and_shapes_are_exact():
    result = _explain()

    assert result["buildable"] is True
    assert result["reason_code"] == "VALIDATOR_RESULT_BUILDABLE"
    assert result["validator_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()
    assert result["check_violations"] == ()
    assert tuple(result.keys()) == RESULT_KEYS
    assert tuple(result["source"].keys()) == SOURCE_KEYS
    assert tuple(result["validator_result"].keys()) == VALIDATOR_RESULT_KEYS
    assert tuple(result["validator_result"]["validation_checks"][0].keys()) == CHECK_KEYS
    assert result["source"]["artifact_refs"] == ("reader-artifact-001",)
    assert result["validator_result"]["validation_checks"][0]["finding"] == (
        "Caller supplied validation finding."
    )


def test_public_api_is_keyword_only_and_bool_wrapper_matches_explain():
    expected_kwonly = len(VALIDATOR_RESULT_KEYS)

    assert builder.explain_validator_result_build.__code__.co_argcount == 0
    assert builder.explain_validator_result_build.__code__.co_kwonlyargcount == expected_kwonly
    assert builder.is_validator_result_buildable.__code__.co_argcount == 0
    assert builder.is_validator_result_buildable.__code__.co_kwonlyargcount == expected_kwonly
    assert builder.is_validator_result_buildable(**_valid_values()) is True

    invalid_values = _valid_values()
    invalid_values["run_id"] = ""
    assert builder.is_validator_result_buildable(**invalid_values) is False
    assert _explain(run_id="")["buildable"] is False


def test_failed_outcome_and_known_blocking_check_ids_are_still_buildable():
    failed = _explain(validator_outcome="failed")
    blocking = _explain(blocking_check_ids=("check-001",), validator_outcome="failed")

    assert failed["buildable"] is True
    assert blocking["buildable"] is True
    assert blocking["validator_result"]["blocking_check_ids"] == ("check-001",)


def test_unknown_blocking_check_ids_block_buildability():
    result = _explain(blocking_check_ids=("unknown-check",))

    assert result["buildable"] is False
    assert result["reason_code"] == "BLOCKING_CHECK_ID_UNKNOWN"
    assert result["validator_violations"] == ("BLOCKING_CHECK_ID_UNKNOWN",)
    assert "blocking_check_ids" in result["missing_or_invalid_fields"]


def test_required_top_level_field_violations_are_collected():
    cases = (
        ({"run_id": ""}, "RUN_ID_MISSING", "run_id"),
        ({"validator_result_id": ""}, "VALIDATOR_RESULT_ID_MISSING", "validator_result_id"),
        ({"artifact_refs": ()}, "ARTIFACT_REFS_MISSING", "artifact_refs"),
        ({"artifact_refs": ("",)}, "ARTIFACT_REFS_MISSING", "artifact_refs"),
        ({"artifact_refs": ["reader-artifact-001"]}, "ARTIFACT_REFS_MISSING", "artifact_refs"),
        ({"validation_checks": ()}, "VALIDATION_CHECKS_MISSING", "validation_checks"),
        ({"required_check_ids": ()}, "REQUIRED_CHECK_IDS_MISSING", "required_check_ids"),
        ({"required_check_ids": ("",)}, "REQUIRED_CHECK_IDS_MISSING", "required_check_ids"),
        ({"missing_check_ids": ("check-002",)}, "MISSING_CHECK_IDS_DECLARED", "missing_check_ids"),
        ({"validator_outcome": ""}, "VALIDATOR_OUTCOME_MISSING", "validator_outcome"),
        ({"created_at": ""}, "CREATED_AT_MISSING", "created_at"),
        ({"timestamp_policy": ""}, "TIMESTAMP_POLICY_MISSING", "timestamp_policy"),
        ({"source_of_truth": ()}, "SOURCE_OF_TRUTH_MISSING", "source_of_truth"),
        ({"source_of_truth": ("",)}, "SOURCE_OF_TRUTH_MISSING", "source_of_truth"),
    )

    for overrides, reason_code, field in cases:
        result = _explain(**overrides)

        assert result["buildable"] is False
        assert reason_code in result["validator_violations"]
        assert field in result["missing_or_invalid_fields"]
        assert result["reason_code"] == result["validator_violations"][0]


def test_artifact_refs_and_evidence_refs_are_required_opaque_tuples():
    opaque_result = _explain(
        artifact_refs=("opaque-reader-artifact-ref",),
        validation_checks=(
            _check(
                target_artifact_ref="opaque-reader-artifact-ref",
                evidence_refs=("opaque-evidence-ref",),
            ),
        ),
    )
    empty_evidence = _explain(validation_checks=(_check(evidence_refs=()),))
    list_evidence = _explain(validation_checks=(_check(evidence_refs=["evidence"]),))

    assert opaque_result["buildable"] is True
    assert empty_evidence["reason_code"] == "CHECK_EVIDENCE_REFS_MISSING"
    assert "CHECK_EVIDENCE_REFS_MISSING" in list_evidence["validator_violations"]
    assert "validation_checks[0].evidence_refs" in list_evidence["missing_or_invalid_fields"]


def test_check_id_uniqueness_required_boundary_and_required_check_presence():
    duplicate = _explain(validation_checks=(_check(), _check()))
    not_required = _explain(
        validation_checks=(_check(check_id="check-002"),),
        required_check_ids=("check-001",),
    )
    required_missing = _explain(required_check_ids=("check-001", "check-002"))

    assert "CHECK_ID_DUPLICATE" in duplicate["validator_violations"]
    assert "CHECK_ID_NOT_REQUIRED" in not_required["validator_violations"]
    assert "REQUIRED_CHECK_MISSING" in not_required["validator_violations"]
    assert "REQUIRED_CHECK_MISSING" in required_missing["validator_violations"]
    assert "required_check_ids.check-002" in required_missing["missing_or_invalid_fields"]


def test_check_fields_must_be_non_empty_and_missing_key_shapes_are_reported():
    field_cases = (
        ("check_id", "", "CHECK_ID_MISSING"),
        ("check_role", "", "CHECK_ROLE_MISSING"),
        ("target_artifact_ref", "", "CHECK_TARGET_ARTIFACT_REF_MISSING"),
        ("target_artifact_kind", "", "CHECK_TARGET_ARTIFACT_KIND_MISSING"),
        ("check_status", "", "CHECK_STATUS_MISSING"),
        ("severity", "", "CHECK_SEVERITY_MISSING"),
        ("finding", "", "CHECK_FINDING_MISSING"),
        ("evidence_refs", (), "CHECK_EVIDENCE_REFS_MISSING"),
    )

    for field, value, reason_code in field_cases:
        result = _explain(validation_checks=(_check(**{field: value}),))

        assert reason_code in result["validator_violations"]
        assert f"validation_checks[0].{field}" in result["missing_or_invalid_fields"]
        assert tuple(result["check_violations"][0].keys()) == CHECK_VIOLATION_KEYS

    for missing_key, expected_reason_code in MISSING_CHECK_KEY_EXPECTATIONS:
        check = _check()
        del check[missing_key]
        result = _explain(validation_checks=(check,))

        assert "CHECK_KEYS_INVALID" in result["validator_violations"]
        assert expected_reason_code in result["validator_violations"]
        assert f"validation_checks[0].{missing_key}" in result["missing_or_invalid_fields"] or (
            missing_key == "notes"
            and "validation_checks[0].keys" in result["missing_or_invalid_fields"]
        )


def test_non_dict_check_records_check_violation_shape():
    result = _explain(validation_checks=("not-a-check",))

    assert result["buildable"] is False
    assert result["reason_code"] == "CHECK_NOT_DICT"
    assert result["validator_violations"] == ("CHECK_NOT_DICT", "REQUIRED_CHECK_MISSING")
    assert tuple(result["check_violations"][0].keys()) == CHECK_VIOLATION_KEYS
    assert result["validator_result"]["validation_checks"][0] == {
        "check_id": "",
        "check_role": "",
        "target_artifact_ref": "",
        "target_artifact_kind": "",
        "check_status": "",
        "severity": "",
        "finding": "",
        "evidence_refs": (),
        "notes": (),
    }


def test_forbidden_raw_output_read_fetch_execution_gate_publish_fields_are_suppressed():
    for field in FORBIDDEN_CHECK_FIELDS:
        result = _explain(validation_checks=(_check(**{field: "forbidden"}),))
        payload_keys = _payload_keys(result)

        assert "CHECK_FORBIDDEN_RAW_FIELD_PRESENT" in result["validator_violations"]
        assert "CHECK_KEYS_INVALID" in result["validator_violations"]
        assert field not in payload_keys
        assert tuple(result["check_violations"][0].keys()) == CHECK_VIOLATION_KEYS


def test_reason_catalog_priority_and_forbidden_pseudo_reason_codes():
    assert builder.REASON_CODES == REASON_CODES
    assert builder.VALIDATOR_RESULT_BUILD_REASON_CODES == REASON_CODES
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
    ):
        assert not hasattr(builder, io_name)


def test_all_violations_are_priority_ordered_and_detail_collections_are_present():
    first_check = _check(
        check_id="",
        check_role="",
        target_artifact_ref="",
        target_artifact_kind="",
        check_status="",
        severity="",
        finding="",
        evidence_refs=(),
        raw_validation_output="raw",
    )
    second_check = _check(check_id="extra-check")
    result = _explain(
        run_id="",
        validator_result_id="",
        artifact_refs=(),
        validation_checks=(first_check, second_check),
        required_check_ids=("check-001", "check-002"),
        missing_check_ids=("check-002",),
        blocking_check_ids=("missing-block",),
        validator_outcome="",
        created_at="",
        timestamp_policy="",
        source_of_truth=(),
    )
    expected_order = tuple(
        reason_code
        for reason_code in REASON_PRIORITY
        if reason_code != "VALIDATOR_RESULT_BUILDABLE"
        and reason_code in result["validator_violations"]
    )

    assert result["validator_violations"] == expected_order
    assert result["reason_code"] == result["validator_violations"][0]
    assert "validation_checks[0].raw_validation_output" in result["missing_or_invalid_fields"]
    assert "validation_checks[1].check_id" in result["missing_or_invalid_fields"]
    assert "required_check_ids.check-002" in result["missing_or_invalid_fields"]
    assert result["check_violations"] != ()
    for check_violation in result["check_violations"]:
        assert tuple(check_violation.keys()) == CHECK_VIOLATION_KEYS


def test_invariant_refs_capture_governance_and_no_execution_boundaries():
    result = _explain()

    for invariant_ref in REQUIRED_INVARIANT_REFS:
        assert invariant_ref in result["invariant_refs"]


def test_payload_key_traversal_skips_invariants_instead_of_blanket_result_scans():
    result = _explain()
    payload_keys = _payload_keys(result)

    assert "no_raw_url" in result["invariant_refs"]
    assert "no_raw_url" not in payload_keys
