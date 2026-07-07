"""Tests for the pure gate input assembly buildability builder."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import gate_input_assembly_builder as builder


RESULT_KEYS = (
    "buildable",
    "reason_code",
    "reason",
    "source",
    "gate_input",
    "assembly_violations",
    "missing_or_invalid_fields",
    "evidence_item_violations",
    "invariant_refs",
)

SOURCE_KEYS = (
    "candidate_artifact_ref",
    "candidate_artifact_kind",
    "gate_policy_refs",
    "source_of_truth",
)

GATE_INPUT_KEYS = (
    "run_id",
    "gate_input_id",
    "assembly_kind",
    "candidate_artifact_ref",
    "candidate_artifact_kind",
    "evidence_items",
    "required_evidence_ids",
    "missing_evidence_ids",
    "blocking_evidence_ids",
    "gate_policy_refs",
    "created_at",
    "timestamp_policy",
    "source_of_truth",
    "notes",
)

EVIDENCE_ITEM_KEYS = (
    "evidence_id",
    "evidence_role",
    "artifact_ref",
    "artifact_kind",
    "evidence_status",
    "producer_ref",
    "evidence_refs",
    "notes",
)

EVIDENCE_ITEM_VIOLATION_KEYS = (
    "evidence_item_index",
    "evidence_id",
    "reason_code",
    "field",
)

REASON_CODES = (
    "GATE_INPUT_ASSEMBLY_BUILDABLE",
    "RUN_ID_MISSING",
    "GATE_INPUT_ID_MISSING",
    "ASSEMBLY_KIND_MISSING",
    "CANDIDATE_ARTIFACT_REF_MISSING",
    "CANDIDATE_ARTIFACT_KIND_MISSING",
    "EVIDENCE_ITEMS_MISSING",
    "REQUIRED_EVIDENCE_IDS_MISSING",
    "MISSING_EVIDENCE_IDS_DECLARED",
    "BLOCKING_EVIDENCE_ID_UNKNOWN",
    "GATE_POLICY_REFS_MISSING",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "EVIDENCE_ITEM_NOT_DICT",
    "EVIDENCE_ITEM_KEYS_INVALID",
    "EVIDENCE_ID_MISSING",
    "EVIDENCE_ROLE_MISSING",
    "EVIDENCE_ARTIFACT_REF_MISSING",
    "EVIDENCE_ARTIFACT_KIND_MISSING",
    "EVIDENCE_STATUS_MISSING",
    "EVIDENCE_PRODUCER_REF_MISSING",
    "EVIDENCE_REFS_MISSING",
    "EVIDENCE_ID_DUPLICATE",
    "EVIDENCE_ID_NOT_REQUIRED",
    "REQUIRED_EVIDENCE_MISSING",
    "EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT",
)

REASON_PRIORITY = (
    "RUN_ID_MISSING",
    "GATE_INPUT_ID_MISSING",
    "ASSEMBLY_KIND_MISSING",
    "CANDIDATE_ARTIFACT_REF_MISSING",
    "CANDIDATE_ARTIFACT_KIND_MISSING",
    "EVIDENCE_ITEMS_MISSING",
    "REQUIRED_EVIDENCE_IDS_MISSING",
    "MISSING_EVIDENCE_IDS_DECLARED",
    "BLOCKING_EVIDENCE_ID_UNKNOWN",
    "GATE_POLICY_REFS_MISSING",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "EVIDENCE_ITEM_NOT_DICT",
    "EVIDENCE_ITEM_KEYS_INVALID",
    "EVIDENCE_ID_MISSING",
    "EVIDENCE_ROLE_MISSING",
    "EVIDENCE_ARTIFACT_REF_MISSING",
    "EVIDENCE_ARTIFACT_KIND_MISSING",
    "EVIDENCE_STATUS_MISSING",
    "EVIDENCE_PRODUCER_REF_MISSING",
    "EVIDENCE_REFS_MISSING",
    "EVIDENCE_ID_DUPLICATE",
    "EVIDENCE_ID_NOT_REQUIRED",
    "REQUIRED_EVIDENCE_MISSING",
    "EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT",
    "GATE_INPUT_ASSEMBLY_BUILDABLE",
)

FORBIDDEN_EVIDENCE_ITEM_FIELDS = (
    "raw_artifact_content",
    "raw_evidence_content",
    "raw_reader_html",
    "reader_html_content",
    "rendered_html",
    "html",
    "raw_html",
    "rendered_markdown",
    "markdown",
    "raw_markdown",
    "training_report_content",
    "validator_result_content",
    "rubric_review_content",
    "audit_review_content",
    "source_manifest_content",
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
    "evidence_payload",
    "raw_evidence_payload",
    "gate_input_payload",
    "raw_gate_input_payload",
    "gate_execution_result",
    "gate_result",
    "gate_decision",
    "policy_execution_result",
    "policy_result",
    "policy_decision",
    "policy_pass",
    "quality_pass",
    "validator_pass",
    "rubric_pass",
    "audit_pass",
    "eval_pass",
    "gate_pass",
    "publish_allowed",
    "review_blocked",
    "publish_blocked",
    "noop_completed",
    "pass_published",
    "public_url",
    "publish_url",
    "deployment_url",
    "hosting_target",
    "public_url_created",
    "file_path",
    "path",
    "local_path",
    "reader_path",
    "training_report_path",
    "validator_result_path",
    "rubric_review_path",
    "audit_review_path",
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
    "audit_execution_result",
    "judge_execution_result",
    "eval_result",
    "publish_result",
    "notification_result",
    "ledger_write_result",
    "transition_result",
    "runtime_result",
    "adapter_result",
    "should_fetch",
    "should_read_reader",
    "should_read_training_report",
    "should_read_validator_result",
    "should_read_rubric_review",
    "should_read_audit_review",
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
    "should_write_ledger",
    "should_notify",
    "reader_read",
    "training_report_read",
    "validator_result_read",
    "rubric_review_read",
    "audit_review_read",
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
    "notified",
    "ledger_written",
)

FORBIDDEN_PSEUDO_REASON_CODES = (
    "READER_READ_FORBIDDEN",
    "TRAINING_REPORT_READ_FORBIDDEN",
    "VALIDATOR_RESULT_READ_FORBIDDEN",
    "RUBRIC_REVIEW_READ_FORBIDDEN",
    "AUDIT_REVIEW_READ_FORBIDDEN",
    "SOURCE_MANIFEST_READ_FORBIDDEN",
    "SOURCE_NOTES_READ_FORBIDDEN",
    "SOURCE_CONTENT_READ_FORBIDDEN",
    "FILE_READ_FORBIDDEN",
    "WEB_FETCH_FORBIDDEN",
    "GITHUB_FETCH_FORBIDDEN",
    "RSS_FETCH_FORBIDDEN",
    "NOTION_FETCH_FORBIDDEN",
    "LLM_JUDGE_FORBIDDEN",
    "AUDIT_EXECUTION_FORBIDDEN",
    "POLICY_EXECUTION_FORBIDDEN",
    "VALIDATOR_EXECUTION_FORBIDDEN",
    "EVAL_EXECUTION_FORBIDDEN",
    "GATE_EXECUTION_FORBIDDEN",
    "PUBLISH_FORBIDDEN",
    "LEDGER_WRITE_FORBIDDEN",
    "NOTIFICATION_FORBIDDEN",
    "PUBLIC_URL_CREATION_FORBIDDEN",
)

FORBIDDEN_MODULE_NAMES = (
    "states",
    "gates",
    "artifacts",
    "audit_review_builder",
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
    "build_gate_input",
    "run_gate_input_assembly",
    "run_gate",
    "run_policy_engine",
    "compute_gate_decision",
    "compute_publish_allowed",
    "compute_quality_pass",
    "compute_noop_completion",
    "judge_gate",
    "validate_artifact",
    "execute_validator",
    "execute_audit",
    "execute_eval",
    "publish",
    "create_public_url",
    "write_ledger",
    "send_notification",
)

REQUIRED_INVARIANT_REFS = (
    "gate_input_assembly_builder_only",
    "builder_not_reader_reader",
    "builder_not_training_report_reader",
    "builder_not_validator_result_reader",
    "builder_not_rubric_review_reader",
    "builder_not_audit_review_reader",
    "builder_not_source_manifest_reader",
    "builder_not_source_notes_reader",
    "builder_not_source_reader",
    "builder_not_file_reader",
    "builder_not_web_fetcher",
    "builder_not_github_fetcher",
    "builder_not_rss_fetcher",
    "builder_not_notion_fetcher",
    "builder_not_llm_judge",
    "builder_not_audit_executor",
    "builder_not_policy_executor",
    "builder_not_validator_executor",
    "builder_not_eval_executor",
    "builder_not_gate_executor",
    "builder_not_publisher",
    "builder_not_ledger_writer",
    "builder_not_notifier",
    "evidence_items_are_caller_supplied",
    "evidence_status_is_caller_supplied",
    "gate_policy_refs_are_caller_supplied",
    "candidate_artifact_ref_opaque",
    "artifact_refs_opaque",
    "evidence_refs_opaque",
    "gate_input_governance_evidence_bundle",
    "gate_input_not_gate_decision",
    "gate_input_not_public_candidate",
    "gate_input_not_publish_artifact",
    "candidate_artifact_not_public_url",
    "evidence_status_not_quality_pass",
    "evidence_status_not_gate_pass",
    "evidence_status_not_publish_allowed",
    "gate_policy_refs_not_policy_execution",
    "buildable_not_quality_pass",
    "buildable_not_eval_pass",
    "buildable_not_audit_pass",
    "buildable_not_gate_pass",
    "buildable_not_publish_allowed",
    "buildable_not_review_blocked",
    "buildable_not_noop_completed",
    "buildable_not_pass_published",
    "buildable_not_public_url_created",
    "blocking_evidence_ids_are_gate_evidence_only",
    "blocking_evidence_ids_do_not_execute_gate",
    "no_reader_read",
    "no_training_report_read",
    "no_validator_result_read",
    "no_rubric_review_read",
    "no_audit_review_read",
    "no_source_manifest_read",
    "no_source_notes_read",
    "no_source_content_read",
    "no_url_fetch",
    "no_rss_fetch",
    "no_file_read",
    "no_raw_content",
    "no_raw_url",
    "no_generated_gate_decision",
    "no_llm_summary",
    "no_llm_judge",
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
    "no_ledger_write",
    "no_public_url_behavior",
    "no_quality_pass_no_public_url",
    "noop_completed_not_pass_published",
)

ALLOWED_GATE_INPUT_FIELD_NAMES = (
    "gate_input_id",
    "gate_input",
    "assembly_kind",
    "candidate_artifact_ref",
    "candidate_artifact_kind",
    "evidence_items",
    "required_evidence_ids",
    "missing_evidence_ids",
    "blocking_evidence_ids",
    "gate_policy_refs",
    "evidence_id",
    "evidence_role",
    "artifact_ref",
    "artifact_kind",
    "evidence_status",
    "producer_ref",
    "evidence_refs",
    "source_of_truth",
    "notes",
)

MISSING_EVIDENCE_ITEM_KEY_EXPECTATIONS = (
    ("evidence_id", "EVIDENCE_ID_MISSING"),
    ("evidence_role", "EVIDENCE_ROLE_MISSING"),
    ("artifact_ref", "EVIDENCE_ARTIFACT_REF_MISSING"),
    ("artifact_kind", "EVIDENCE_ARTIFACT_KIND_MISSING"),
    ("evidence_status", "EVIDENCE_STATUS_MISSING"),
    ("producer_ref", "EVIDENCE_PRODUCER_REF_MISSING"),
    ("evidence_refs", "EVIDENCE_REFS_MISSING"),
    ("notes", "EVIDENCE_ITEM_KEYS_INVALID"),
)


def _evidence_item(**overrides):
    values = {
        "evidence_id": "evidence-001",
        "evidence_role": "validator_result",
        "artifact_ref": "validator-result-001",
        "artifact_kind": "validator_result",
        "evidence_status": "passed",
        "producer_ref": "validator-result-builder",
        "evidence_refs": ("validator-result-001#summary",),
        "notes": ("caller-supplied-evidence-only",),
    }
    values.update(overrides)
    return values


def _valid_values():
    return {
        "run_id": "run-001",
        "gate_input_id": "gate-input-001",
        "assembly_kind": "pre_publish",
        "candidate_artifact_ref": "reader-artifact-001",
        "candidate_artifact_kind": "reader_html",
        "evidence_items": (_evidence_item(),),
        "required_evidence_ids": ("evidence-001",),
        "missing_evidence_ids": (),
        "blocking_evidence_ids": (),
        "gate_policy_refs": ("daily-gate-policy-v1",),
        "created_at": "caller-supplied-created-at",
        "timestamp_policy": "caller_supplied_no_datetime_parsing",
        "source_of_truth": ("p2d-31",),
        "notes": ("structured-only",),
    }


def _explain(**overrides):
    values = _valid_values()
    values.update(overrides)
    return builder.explain_gate_input_assembly_build(**values)


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
    assert builder.GATE_INPUT_ASSEMBLY_BUILD_REASON_CODES == REASON_CODES
    assert builder.REASON_PRIORITY == REASON_PRIORITY


def test_valid_gate_input_bundle_is_buildable_with_exact_result_shapes():
    result = _explain()

    assert result["buildable"] is True
    assert result["reason_code"] == "GATE_INPUT_ASSEMBLY_BUILDABLE"
    assert result["assembly_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()
    assert result["evidence_item_violations"] == ()
    assert tuple(result.keys()) == RESULT_KEYS
    assert tuple(result["source"].keys()) == SOURCE_KEYS
    assert tuple(result["gate_input"].keys()) == GATE_INPUT_KEYS
    assert tuple(result["gate_input"]["evidence_items"][0].keys()) == (
        EVIDENCE_ITEM_KEYS
    )
    assert result["source"]["candidate_artifact_ref"] == "reader-artifact-001"
    assert result["source"]["gate_policy_refs"] == ("daily-gate-policy-v1",)


def test_public_api_is_keyword_only_and_bool_wrapper_matches_explain():
    expected_kwonly = len(GATE_INPUT_KEYS)

    assert builder.explain_gate_input_assembly_build.__code__.co_argcount == 0
    assert builder.explain_gate_input_assembly_build.__code__.co_kwonlyargcount == (
        expected_kwonly
    )
    assert builder.is_gate_input_assembly_buildable.__code__.co_argcount == 0
    assert builder.is_gate_input_assembly_buildable.__code__.co_kwonlyargcount == (
        expected_kwonly
    )
    assert builder.is_gate_input_assembly_buildable(**_valid_values()) is True

    invalid_values = _valid_values()
    invalid_values["run_id"] = ""
    assert builder.is_gate_input_assembly_buildable(**invalid_values) is False
    assert _explain(run_id="")["buildable"] is False


def test_noop_and_pre_publish_assembly_kinds_are_buildable_opaque_markers():
    noop = _explain(assembly_kind="noop")
    pre_publish = _explain(assembly_kind="pre_publish")

    assert noop["buildable"] is True
    assert noop["gate_input"]["assembly_kind"] == "noop"
    assert pre_publish["buildable"] is True
    assert pre_publish["gate_input"]["assembly_kind"] == "pre_publish"


def test_failed_evidence_status_and_known_blocking_ids_still_buildable():
    failed = _explain(evidence_items=(_evidence_item(evidence_status="failed"),))
    blocked = _explain(
        blocking_evidence_ids=("evidence-001",),
        evidence_items=(_evidence_item(evidence_status="failed"),),
    )

    assert failed["buildable"] is True
    assert failed["gate_input"]["evidence_items"][0]["evidence_status"] == (
        "failed"
    )
    assert blocked["buildable"] is True
    assert blocked["gate_input"]["blocking_evidence_ids"] == ("evidence-001",)


def test_unknown_blocking_evidence_ids_block_buildability():
    cases = (
        ("unknown-evidence",),
        ("",),
        (object(),),
        ["evidence-001"],
    )

    for blocking_evidence_ids in cases:
        result = _explain(blocking_evidence_ids=blocking_evidence_ids)

        assert result["buildable"] is False
        assert result["reason_code"] == "BLOCKING_EVIDENCE_ID_UNKNOWN"
        assert "BLOCKING_EVIDENCE_ID_UNKNOWN" in result["assembly_violations"]
        assert "blocking_evidence_ids" in result["missing_or_invalid_fields"]


def test_required_top_level_field_violations_are_collected():
    cases = (
        ({"run_id": ""}, "RUN_ID_MISSING", "run_id"),
        ({"run_id": "   "}, "RUN_ID_MISSING", "run_id"),
        ({"gate_input_id": ""}, "GATE_INPUT_ID_MISSING", "gate_input_id"),
        ({"assembly_kind": ""}, "ASSEMBLY_KIND_MISSING", "assembly_kind"),
        (
            {"candidate_artifact_ref": ""},
            "CANDIDATE_ARTIFACT_REF_MISSING",
            "candidate_artifact_ref",
        ),
        (
            {"candidate_artifact_kind": ""},
            "CANDIDATE_ARTIFACT_KIND_MISSING",
            "candidate_artifact_kind",
        ),
        ({"evidence_items": ()}, "EVIDENCE_ITEMS_MISSING", "evidence_items"),
        ({"evidence_items": []}, "EVIDENCE_ITEMS_MISSING", "evidence_items"),
        (
            {"required_evidence_ids": ()},
            "REQUIRED_EVIDENCE_IDS_MISSING",
            "required_evidence_ids",
        ),
        (
            {"required_evidence_ids": ("",)},
            "REQUIRED_EVIDENCE_IDS_MISSING",
            "required_evidence_ids",
        ),
        (
            {"required_evidence_ids": ["evidence-001"]},
            "REQUIRED_EVIDENCE_IDS_MISSING",
            "required_evidence_ids",
        ),
        (
            {"missing_evidence_ids": ("evidence-002",)},
            "MISSING_EVIDENCE_IDS_DECLARED",
            "missing_evidence_ids",
        ),
        (
            {"missing_evidence_ids": ["evidence-002"]},
            "MISSING_EVIDENCE_IDS_DECLARED",
            "missing_evidence_ids",
        ),
        (
            {"gate_policy_refs": ()},
            "GATE_POLICY_REFS_MISSING",
            "gate_policy_refs",
        ),
        (
            {"gate_policy_refs": ("",)},
            "GATE_POLICY_REFS_MISSING",
            "gate_policy_refs",
        ),
        (
            {"gate_policy_refs": ["daily-gate-policy-v1"]},
            "GATE_POLICY_REFS_MISSING",
            "gate_policy_refs",
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
        assert reason_code in result["assembly_violations"]
        assert field in result["missing_or_invalid_fields"]
        assert result["reason_code"] == result["assembly_violations"][0]


def test_candidate_artifact_gate_policy_and_evidence_refs_are_opaque():
    opaque_result = _explain(
        candidate_artifact_ref="opaque-reader-candidate-ref",
        candidate_artifact_kind="opaque-reader-candidate-kind",
        gate_policy_refs=("opaque-policy-ref",),
        evidence_items=(
            _evidence_item(
                artifact_ref="opaque-validator-ref",
                artifact_kind="opaque-validator-kind",
                evidence_refs=("opaque-evidence-ref",),
            ),
        ),
    )
    empty_evidence_refs = _explain(
        evidence_items=(_evidence_item(evidence_refs=()),)
    )
    list_evidence_refs = _explain(
        evidence_items=(_evidence_item(evidence_refs=["evidence"]),)
    )

    assert opaque_result["buildable"] is True
    assert opaque_result["source"]["candidate_artifact_ref"] == (
        "opaque-reader-candidate-ref"
    )
    assert opaque_result["source"]["gate_policy_refs"] == ("opaque-policy-ref",)
    assert empty_evidence_refs["reason_code"] == "EVIDENCE_REFS_MISSING"
    assert "EVIDENCE_REFS_MISSING" in (
        list_evidence_refs["assembly_violations"]
    )
    assert "evidence_items[0].evidence_refs" in (
        list_evidence_refs["missing_or_invalid_fields"]
    )


def test_allowed_gate_input_marker_names_are_not_falsely_banned():
    result = _explain()

    for field_name in ALLOWED_GATE_INPUT_FIELD_NAMES:
        assert field_name not in FORBIDDEN_EVIDENCE_ITEM_FIELDS

    assert result["buildable"] is True
    assert result["gate_input"]["gate_input_id"] == "gate-input-001"
    assert result["gate_input"]["evidence_items"][0]["evidence_status"] == (
        "passed"
    )


def test_evidence_id_uniqueness_required_boundary_and_required_presence():
    duplicate = _explain(evidence_items=(_evidence_item(), _evidence_item()))
    not_required = _explain(
        evidence_items=(_evidence_item(evidence_id="evidence-002"),),
        required_evidence_ids=("evidence-001",),
    )
    required_missing = _explain(
        required_evidence_ids=("evidence-001", "evidence-002")
    )

    assert "EVIDENCE_ID_DUPLICATE" in duplicate["assembly_violations"]
    assert "EVIDENCE_ID_NOT_REQUIRED" in not_required["assembly_violations"]
    assert "REQUIRED_EVIDENCE_MISSING" in not_required["assembly_violations"]
    assert "REQUIRED_EVIDENCE_MISSING" in (
        required_missing["assembly_violations"]
    )
    assert "required_evidence_ids.evidence-002" in (
        required_missing["missing_or_invalid_fields"]
    )


def test_evidence_item_fields_must_be_non_empty_and_missing_keys_reported():
    field_cases = (
        ("evidence_id", "", "EVIDENCE_ID_MISSING"),
        ("evidence_role", "", "EVIDENCE_ROLE_MISSING"),
        ("artifact_ref", "", "EVIDENCE_ARTIFACT_REF_MISSING"),
        ("artifact_kind", "", "EVIDENCE_ARTIFACT_KIND_MISSING"),
        ("evidence_status", "", "EVIDENCE_STATUS_MISSING"),
        ("producer_ref", "", "EVIDENCE_PRODUCER_REF_MISSING"),
        ("evidence_refs", (), "EVIDENCE_REFS_MISSING"),
    )

    for field, value, reason_code in field_cases:
        result = _explain(evidence_items=(_evidence_item(**{field: value}),))

        assert reason_code in result["assembly_violations"]
        assert f"evidence_items[0].{field}" in (
            result["missing_or_invalid_fields"]
        )
        assert tuple(result["evidence_item_violations"][0].keys()) == (
            EVIDENCE_ITEM_VIOLATION_KEYS
        )

    for missing_key, expected_reason_code in (
        MISSING_EVIDENCE_ITEM_KEY_EXPECTATIONS
    ):
        evidence_item = _evidence_item()
        del evidence_item[missing_key]
        result = _explain(evidence_items=(evidence_item,))

        assert "EVIDENCE_ITEM_KEYS_INVALID" in result["assembly_violations"]
        assert expected_reason_code in result["assembly_violations"]
        assert f"evidence_items[0].{missing_key}" in (
            result["missing_or_invalid_fields"]
        ) or (
            missing_key == "notes"
            and "evidence_items[0].keys" in (
                result["missing_or_invalid_fields"]
            )
        )


def test_non_dict_evidence_item_records_violation_shape():
    result = _explain(evidence_items=("not-an-evidence-item",))

    assert result["buildable"] is False
    assert result["reason_code"] == "EVIDENCE_ITEM_NOT_DICT"
    assert result["assembly_violations"] == (
        "EVIDENCE_ITEM_NOT_DICT",
        "REQUIRED_EVIDENCE_MISSING",
    )
    assert tuple(result["evidence_item_violations"][0].keys()) == (
        EVIDENCE_ITEM_VIOLATION_KEYS
    )
    assert result["gate_input"]["evidence_items"][0] == {
        "evidence_id": "",
        "evidence_role": "",
        "artifact_ref": "",
        "artifact_kind": "",
        "evidence_status": "",
        "producer_ref": "",
        "evidence_refs": (),
        "notes": (),
    }


def test_forbidden_raw_read_execution_gate_publish_fields_are_suppressed():
    for field in FORBIDDEN_EVIDENCE_ITEM_FIELDS:
        result = _explain(
            evidence_items=(_evidence_item(**{field: "forbidden"}),)
        )
        payload_keys = _payload_keys(result)

        assert "EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT" in (
            result["assembly_violations"]
        )
        assert "EVIDENCE_ITEM_KEYS_INVALID" in result["assembly_violations"]
        assert field not in payload_keys
        assert tuple(result["evidence_item_violations"][0].keys()) == (
            EVIDENCE_ITEM_VIOLATION_KEYS
        )


def test_reason_catalog_priority_and_forbidden_pseudo_reason_codes():
    assert builder.REASON_CODES == REASON_CODES
    assert builder.GATE_INPUT_ASSEMBLY_BUILD_REASON_CODES == REASON_CODES
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
        "httpx",
        "open",
        "datetime",
        "os",
        "pathlib",
        "logging",
    ):
        assert not hasattr(builder, io_name)


def test_all_violations_are_priority_ordered_and_details_present():
    first_evidence_item = _evidence_item(
        evidence_id="",
        evidence_role="",
        artifact_ref="",
        artifact_kind="",
        evidence_status="",
        producer_ref="",
        evidence_refs=(),
        raw_artifact_content="raw",
    )
    second_evidence_item = _evidence_item(evidence_id="extra-evidence")
    result = _explain(
        run_id="",
        gate_input_id="",
        assembly_kind="",
        candidate_artifact_ref="",
        candidate_artifact_kind="",
        evidence_items=(first_evidence_item, second_evidence_item),
        required_evidence_ids=("evidence-001", "evidence-002"),
        missing_evidence_ids=("evidence-002",),
        blocking_evidence_ids=("missing-block",),
        gate_policy_refs=(),
        created_at="",
        timestamp_policy="",
        source_of_truth=(),
    )
    expected_order = tuple(
        reason_code
        for reason_code in REASON_PRIORITY
        if reason_code != "GATE_INPUT_ASSEMBLY_BUILDABLE"
        and reason_code in result["assembly_violations"]
    )

    assert result["assembly_violations"] == expected_order
    assert result["reason_code"] == result["assembly_violations"][0]
    assert "evidence_items[0].raw_artifact_content" in (
        result["missing_or_invalid_fields"]
    )
    assert "evidence_items[1].evidence_id" in (
        result["missing_or_invalid_fields"]
    )
    assert "required_evidence_ids.evidence-002" in (
        result["missing_or_invalid_fields"]
    )
    assert result["evidence_item_violations"] != ()
    for evidence_item_violation in result["evidence_item_violations"]:
        assert tuple(evidence_item_violation.keys()) == (
            EVIDENCE_ITEM_VIOLATION_KEYS
        )


def test_invariant_refs_capture_governance_and_no_execution_boundaries():
    result = _explain()

    assert result["invariant_refs"] == REQUIRED_INVARIANT_REFS


def test_payload_key_traversal_skips_invariants_instead_of_blanket_scans():
    result = _explain()
    payload_keys = _payload_keys(result)

    assert "no_raw_url" in result["invariant_refs"]
    assert "no_public_url_behavior" in result["invariant_refs"]
    assert "buildable_not_publish_allowed" in result["invariant_refs"]
    assert "no_raw_url" not in payload_keys
    assert "no_public_url_behavior" not in payload_keys
    assert "buildable_not_publish_allowed" not in payload_keys
