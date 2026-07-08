"""Tests for the pure run ledger draft buildability builder."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import (  # noqa: E402
    run_ledger_draft_builder as builder,
)


RESULT_KEYS = (
    "buildable",
    "reason_code",
    "reason",
    "source",
    "run_ledger_draft",
    "draft_violations",
    "missing_or_invalid_fields",
    "ledger_draft_evidence_item_violations",
    "invariant_refs",
)

SOURCE_KEYS = (
    "local_noop_runner_result_ref",
    "local_noop_runner_result_buildable_marker",
    "mode",
    "ledger_terminal_status",
    "public_url",
    "public_url_created",
    "source_of_truth",
)

RUN_LEDGER_DRAFT_KEYS = (
    "run_id",
    "run_ledger_draft_id",
    "draft_kind",
    "mode",
    "ledger_terminal_status",
    "local_noop_runner_result_ref",
    "local_noop_runner_result_buildable_marker",
    "public_url",
    "public_url_created",
    "ledger_draft_evidence_items",
    "required_ledger_draft_evidence_ids",
    "missing_ledger_draft_evidence_ids",
    "blocking_ledger_draft_evidence_ids",
    "created_at",
    "timestamp_policy",
    "source_of_truth",
    "notes",
)

LEDGER_DRAFT_EVIDENCE_ITEM_KEYS = (
    "ledger_draft_evidence_id",
    "ledger_draft_evidence_role",
    "artifact_ref",
    "artifact_kind",
    "evidence_status",
    "producer_ref",
    "evidence_refs",
    "notes",
)

LEDGER_DRAFT_EVIDENCE_ITEM_VIOLATION_KEYS = (
    "ledger_draft_evidence_item_index",
    "ledger_draft_evidence_id",
    "reason_code",
    "field",
)

REASON_CODES = (
    "RUN_LEDGER_DRAFT_BUILDABLE",
    "RUN_ID_MISSING",
    "RUN_LEDGER_DRAFT_ID_MISSING",
    "DRAFT_KIND_NOT_RUN_LEDGER_DRAFT",
    "MODE_NOT_NOOP",
    "PASS_PUBLISHED_FORBIDDEN",
    "LEDGER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
    "LOCAL_NOOP_RUNNER_RESULT_REF_MISSING",
    "LOCAL_NOOP_RUNNER_RESULT_BUILDABLE_MARKER_NOT_TRUE",
    "PUBLIC_URL_IS_NULL_NOT_TRUE",
    "PUBLIC_URL_CREATED_NOT_FALSE",
    "LEDGER_DRAFT_EVIDENCE_ITEMS_MISSING",
    "REQUIRED_LEDGER_DRAFT_EVIDENCE_IDS_MISSING",
    "MISSING_LEDGER_DRAFT_EVIDENCE_IDS_DECLARED",
    "BLOCKING_LEDGER_DRAFT_EVIDENCE_ID_UNKNOWN",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "LEDGER_DRAFT_EVIDENCE_ITEM_NOT_DICT",
    "LEDGER_DRAFT_EVIDENCE_ITEM_KEYS_INVALID",
    "LEDGER_DRAFT_EVIDENCE_ID_MISSING",
    "LEDGER_DRAFT_EVIDENCE_ROLE_MISSING",
    "LEDGER_DRAFT_EVIDENCE_ARTIFACT_REF_MISSING",
    "LEDGER_DRAFT_EVIDENCE_ARTIFACT_KIND_MISSING",
    "LEDGER_DRAFT_EVIDENCE_STATUS_MISSING",
    "LEDGER_DRAFT_EVIDENCE_PRODUCER_REF_MISSING",
    "LEDGER_DRAFT_EVIDENCE_REFS_MISSING",
    "LEDGER_DRAFT_EVIDENCE_ID_DUPLICATE",
    "LEDGER_DRAFT_EVIDENCE_ID_NOT_REQUIRED",
    "REQUIRED_LEDGER_DRAFT_EVIDENCE_MISSING",
    "LEDGER_DRAFT_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT",
)

REASON_PRIORITY = (
    "RUN_ID_MISSING",
    "RUN_LEDGER_DRAFT_ID_MISSING",
    "DRAFT_KIND_NOT_RUN_LEDGER_DRAFT",
    "MODE_NOT_NOOP",
    "PASS_PUBLISHED_FORBIDDEN",
    "LEDGER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
    "LOCAL_NOOP_RUNNER_RESULT_REF_MISSING",
    "LOCAL_NOOP_RUNNER_RESULT_BUILDABLE_MARKER_NOT_TRUE",
    "PUBLIC_URL_IS_NULL_NOT_TRUE",
    "PUBLIC_URL_CREATED_NOT_FALSE",
    "LEDGER_DRAFT_EVIDENCE_ITEMS_MISSING",
    "REQUIRED_LEDGER_DRAFT_EVIDENCE_IDS_MISSING",
    "MISSING_LEDGER_DRAFT_EVIDENCE_IDS_DECLARED",
    "BLOCKING_LEDGER_DRAFT_EVIDENCE_ID_UNKNOWN",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "LEDGER_DRAFT_EVIDENCE_ITEM_NOT_DICT",
    "LEDGER_DRAFT_EVIDENCE_ITEM_KEYS_INVALID",
    "LEDGER_DRAFT_EVIDENCE_ID_MISSING",
    "LEDGER_DRAFT_EVIDENCE_ROLE_MISSING",
    "LEDGER_DRAFT_EVIDENCE_ARTIFACT_REF_MISSING",
    "LEDGER_DRAFT_EVIDENCE_ARTIFACT_KIND_MISSING",
    "LEDGER_DRAFT_EVIDENCE_STATUS_MISSING",
    "LEDGER_DRAFT_EVIDENCE_PRODUCER_REF_MISSING",
    "LEDGER_DRAFT_EVIDENCE_REFS_MISSING",
    "LEDGER_DRAFT_EVIDENCE_ID_DUPLICATE",
    "LEDGER_DRAFT_EVIDENCE_ID_NOT_REQUIRED",
    "REQUIRED_LEDGER_DRAFT_EVIDENCE_MISSING",
    "LEDGER_DRAFT_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT",
    "RUN_LEDGER_DRAFT_BUILDABLE",
)

FORBIDDEN_LEDGER_DRAFT_EVIDENCE_ITEM_FIELDS = (
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
    "gate_input_content",
    "local_noop_run_content",
    "local_noop_e2e_contract_content",
    "local_noop_runner_result_content",
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
    "runner_payload",
    "raw_runner_payload",
    "runner_result_payload",
    "raw_runner_result_payload",
    "e2e_payload",
    "raw_e2e_payload",
    "dry_run_payload",
    "raw_dry_run_payload",
    "local_noop_e2e_payload",
    "raw_local_noop_e2e_payload",
    "completion_payload",
    "raw_completion_payload",
    "noop_run_payload",
    "raw_noop_run_payload",
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
    "pass_published",
    "public_url_value",
    "publish_url",
    "deployment_url",
    "hosting_target",
    "real_url",
    "live_url",
    "file_path",
    "path",
    "local_path",
    "reader_path",
    "training_report_path",
    "validator_result_path",
    "rubric_review_path",
    "audit_review_path",
    "gate_input_path",
    "local_noop_run_path",
    "local_noop_e2e_contract_path",
    "local_noop_runner_result_path",
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
    "noop_completion_result",
    "dry_run_execution_result",
    "e2e_execution_result",
    "runner_execution_result",
    "should_fetch",
    "should_read_reader",
    "should_read_training_report",
    "should_read_validator_result",
    "should_read_rubric_review",
    "should_read_audit_review",
    "should_read_gate_input",
    "should_read_local_noop_run",
    "should_read_local_noop_e2e_contract",
    "should_read_local_noop_runner_result",
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
    "should_transition",
    "should_complete_noop",
    "should_execute_dry_run",
    "should_execute_e2e",
    "should_execute_runner",
    "reader_read",
    "training_report_read",
    "validator_result_read",
    "rubric_review_read",
    "audit_review_read",
    "gate_input_read",
    "local_noop_run_read",
    "local_noop_e2e_contract_read",
    "local_noop_runner_result_read",
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
    "transition_executed",
    "noop_completed_executed",
    "dry_run_executed",
    "e2e_executed",
    "runner_executed",
    "published",
    "notified",
    "ledger_written",
    "public_url_created_executed",
    "run_ledger_yaml",
    "run_ledger_content",
    "run_ledger_entry",
    "run_ledger_entry_payload",
    "run_ledger_write_result",
    "ledger_file_path",
    "ledger_path",
    "ledger_content",
    "raw_ledger_content",
    "ledger_entry",
    "ledger_writer_result",
    "should_write_run_ledger",
    "should_append_run_ledger",
    "should_update_run_ledger",
    "run_ledger_written",
    "ledger_appended",
    "ledger_updated",
)

FORBIDDEN_PSEUDO_REASON_CODES = (
    "READER_READ_FORBIDDEN",
    "TRAINING_REPORT_READ_FORBIDDEN",
    "VALIDATOR_RESULT_READ_FORBIDDEN",
    "RUBRIC_REVIEW_READ_FORBIDDEN",
    "AUDIT_REVIEW_READ_FORBIDDEN",
    "GATE_INPUT_READ_FORBIDDEN",
    "LOCAL_NOOP_RUN_READ_FORBIDDEN",
    "LOCAL_NOOP_E2E_CONTRACT_READ_FORBIDDEN",
    "LOCAL_NOOP_RUNNER_RESULT_READ_FORBIDDEN",
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
    "TRANSITION_EXECUTION_FORBIDDEN",
    "NOOP_COMPLETION_EXECUTION_FORBIDDEN",
    "DRY_RUN_EXECUTION_FORBIDDEN",
    "E2E_EXECUTION_FORBIDDEN",
    "RUNNER_EXECUTION_FORBIDDEN",
    "PUBLISH_FORBIDDEN",
    "LEDGER_WRITE_FORBIDDEN",
    "NOTIFICATION_FORBIDDEN",
    "PUBLIC_URL_CREATION_FORBIDDEN",
)

FORBIDDEN_MODULE_NAMES = (
    "artifacts",
    "states",
    "gates",
    "run_ledger_entry_builder",
    "local_noop_runner_result_builder",
    "local_noop_e2e_contract_builder",
    "gate_input_assembly_builder",
    "local_noop_run_assembly_builder",
    "noop_completion_policy",
    "transition_guard",
    "gate_decision_mapper",
    "daily_gate_decision_policy",
    "daily_gate_evidence_policy",
    "adapter_gate_decision_policy",
    "adapter_gate_evidence_policy",
    "audit_review_builder",
    "rubric_review_builder",
    "validator_result_builder",
    "reader_artifact_builder",
    "training_report_builder",
    "source_manifest_builder",
    "source_notes_builder",
    "pathlib",
    "os",
    "datetime",
    "hashlib",
    "logging",
    "subprocess",
    "requests",
    "urllib",
    "httpx",
    "feedparser",
    "jinja2",
    "open",
)

REQUIRED_INVARIANT_REFS = (
    "run_ledger_draft_builder_only",
    "builder_not_run_ledger_writer",
    "builder_not_run_ledger_entry_builder",
    "builder_not_local_noop_runner_result_builder",
    "builder_not_reader_reader",
    "builder_not_training_report_reader",
    "builder_not_validator_result_reader",
    "builder_not_rubric_review_reader",
    "builder_not_audit_review_reader",
    "builder_not_gate_input_reader",
    "builder_not_local_noop_run_reader",
    "builder_not_local_noop_e2e_contract_reader",
    "builder_not_local_noop_runner_result_reader",
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
    "builder_not_transition_executor",
    "builder_not_noop_completion_executor",
    "builder_not_dry_run_executor",
    "builder_not_e2e_executor",
    "builder_not_runner_executor",
    "builder_not_publisher",
    "builder_not_ledger_writer",
    "builder_not_notifier",
    "ledger_draft_evidence_items_are_caller_supplied",
    "ledger_draft_evidence_status_is_caller_supplied",
    "local_noop_runner_result_ref_is_caller_supplied",
    "local_noop_runner_result_buildable_marker_is_caller_supplied",
    "local_noop_runner_result_ref_opaque",
    "artifact_refs_opaque",
    "evidence_refs_opaque",
    "run_ledger_draft_governance_evidence_bundle",
    "run_ledger_draft_not_ledger_write",
    "run_ledger_draft_not_run_ledger_yaml",
    "run_ledger_draft_not_runner_execution",
    "run_ledger_draft_not_runtime_execution",
    "run_ledger_draft_not_state_transition",
    "run_ledger_draft_not_gate_decision",
    "run_ledger_draft_not_publish_artifact",
    "run_ledger_draft_not_public_candidate",
    "mode_noop_required",
    "public_url_must_be_null",
    "public_url_created_must_be_false",
    "ledger_terminal_status_must_be_noop_completed",
    "noop_completed_not_pass_published",
    "pass_published_forbidden",
    "mode_noop_not_publish",
    "local_noop_runner_result_buildable_marker_not_quality_pass",
    "local_noop_runner_result_buildable_marker_not_gate_pass",
    "local_noop_runner_result_buildable_marker_not_publish_allowed",
    "ledger_draft_evidence_status_not_quality_pass",
    "ledger_draft_evidence_status_not_gate_pass",
    "ledger_draft_evidence_status_not_publish_allowed",
    "buildable_not_ledger_written",
    "buildable_not_runner_executed",
    "buildable_not_runtime_executed",
    "buildable_not_state_transition_executed",
    "buildable_not_quality_pass",
    "buildable_not_eval_pass",
    "buildable_not_audit_pass",
    "buildable_not_gate_pass",
    "buildable_not_publish_allowed",
    "buildable_not_review_blocked",
    "buildable_not_pass_published",
    "buildable_not_public_url_created",
    "buildable_not_notification_sent",
    "blocking_ledger_draft_evidence_ids_are_evidence_only",
    "blocking_ledger_draft_evidence_ids_do_not_execute_gate",
    "blocking_ledger_draft_evidence_ids_do_not_execute_noop_completion",
    "blocking_ledger_draft_evidence_ids_do_not_execute_dry_run",
    "blocking_ledger_draft_evidence_ids_do_not_execute_e2e",
    "blocking_ledger_draft_evidence_ids_do_not_execute_runner",
    "blocking_ledger_draft_evidence_ids_do_not_write_ledger",
    "no_reader_read",
    "no_training_report_read",
    "no_validator_result_read",
    "no_rubric_review_read",
    "no_audit_review_read",
    "no_gate_input_read",
    "no_local_noop_run_read",
    "no_local_noop_e2e_contract_read",
    "no_local_noop_runner_result_read",
    "no_source_manifest_read",
    "no_source_notes_read",
    "no_source_content_read",
    "no_url_fetch",
    "no_rss_fetch",
    "no_file_read",
    "no_raw_content",
    "no_raw_url",
    "no_generated_gate_decision",
    "no_generated_public_url",
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
    "no_noop_completion_execution",
    "no_dry_run_execution",
    "no_e2e_execution",
    "no_runner_execution",
    "no_runtime_execution",
    "no_adapter_execution",
    "no_publish",
    "no_notification",
    "no_ledger_write",
    "no_run_ledger_yaml_write",
    "no_public_url_behavior",
    "no_quality_pass_no_public_url",
)

MISSING_LEDGER_DRAFT_EVIDENCE_ITEM_KEY_EXPECTATIONS = (
    ("ledger_draft_evidence_id", "LEDGER_DRAFT_EVIDENCE_ID_MISSING"),
    ("ledger_draft_evidence_role", "LEDGER_DRAFT_EVIDENCE_ROLE_MISSING"),
    ("artifact_ref", "LEDGER_DRAFT_EVIDENCE_ARTIFACT_REF_MISSING"),
    ("artifact_kind", "LEDGER_DRAFT_EVIDENCE_ARTIFACT_KIND_MISSING"),
    ("evidence_status", "LEDGER_DRAFT_EVIDENCE_STATUS_MISSING"),
    ("producer_ref", "LEDGER_DRAFT_EVIDENCE_PRODUCER_REF_MISSING"),
    ("evidence_refs", "LEDGER_DRAFT_EVIDENCE_REFS_MISSING"),
)


def _ledger_draft_evidence_item(**overrides):
    values = {
        "ledger_draft_evidence_id": "ledger-draft-evidence-001",
        "ledger_draft_evidence_role": "run_ledger_draft",
        "artifact_ref": "local-noop-runner-result-001",
        "artifact_kind": "local_noop_runner_result",
        "evidence_status": "passed",
        "producer_ref": "caller-supplied-run-ledger-draft",
        "evidence_refs": ("local-noop-runner-result-001#noop-terminal",),
        "notes": ("caller-supplied-evidence-only",),
    }
    values.update(overrides)
    return values


def _valid_values():
    return {
        "run_id": "run-001",
        "run_ledger_draft_id": "run-ledger-draft-001",
        "draft_kind": "run_ledger_draft",
        "mode": "noop",
        "ledger_terminal_status": "NOOP_COMPLETED",
        "local_noop_runner_result_ref": "local-noop-runner-result-001",
        "local_noop_runner_result_buildable_marker": True,
        "public_url_created": False,
        "public_url_is_null": True,
        "ledger_draft_evidence_items": (_ledger_draft_evidence_item(),),
        "required_ledger_draft_evidence_ids": ("ledger-draft-evidence-001",),
        "missing_ledger_draft_evidence_ids": (),
        "blocking_ledger_draft_evidence_ids": (),
        "created_at": "caller-supplied-created-at",
        "timestamp_policy": "caller_supplied_no_datetime_parsing",
        "source_of_truth": ("p2d-36",),
        "notes": ("structured-only",),
    }


def _explain(**overrides):
    values = _valid_values()
    values.update(overrides)
    return builder.explain_run_ledger_draft_build(**values)


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
    assert builder.RUN_LEDGER_DRAFT_BUILD_REASON_CODES == (
        REASON_CODES
    )
    assert builder.REASON_PRIORITY == REASON_PRIORITY


def test_valid_run_ledger_draft_is_buildable_with_exact_shapes():
    result = _explain()

    assert result["buildable"] is True
    assert result["reason_code"] == "RUN_LEDGER_DRAFT_BUILDABLE"
    assert result["draft_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()
    assert result["ledger_draft_evidence_item_violations"] == ()
    assert tuple(result.keys()) == RESULT_KEYS
    assert tuple(result["source"].keys()) == SOURCE_KEYS
    assert tuple(result["run_ledger_draft"].keys()) == (
        RUN_LEDGER_DRAFT_KEYS
    )
    assert tuple(
        result["run_ledger_draft"]["ledger_draft_evidence_items"][0].keys()
    ) == LEDGER_DRAFT_EVIDENCE_ITEM_KEYS
    assert result["source"]["public_url"] is None
    assert result["run_ledger_draft"]["public_url"] is None
    assert "public_url_is_null" not in result
    assert "public_url_is_null" not in result["source"]
    assert "public_url_is_null" not in result["run_ledger_draft"]


def test_public_api_is_keyword_only_and_bool_wrapper_matches_explain():
    expected_kwonly = len(RUN_LEDGER_DRAFT_KEYS)

    assert (
        builder.explain_run_ledger_draft_build.__code__.co_argcount
        == 0
    )
    assert (
        builder.explain_run_ledger_draft_build.__code__
        .co_kwonlyargcount
        == expected_kwonly
    )
    assert (
        builder.is_run_ledger_draft_buildable.__code__.co_argcount
        == 0
    )
    assert (
        builder.is_run_ledger_draft_buildable.__code__
        .co_kwonlyargcount
        == expected_kwonly
    )

    cases = (
        _valid_values(),
        {**_valid_values(), "run_id": ""},
        {**_valid_values(), "ledger_terminal_status": "PASS_PUBLISHED"},
        {**_valid_values(), "public_url_is_null": False},
    )
    for values in cases:
        explanation = builder.explain_run_ledger_draft_build(**values)
        assert (
            builder.is_run_ledger_draft_buildable(**values)
            is explanation["buildable"]
        )


def test_required_lockin_markers_block_when_invalid():
    cases = (
        (
            {"draft_kind": "runner_result"},
            "DRAFT_KIND_NOT_RUN_LEDGER_DRAFT",
            "draft_kind",
        ),
        ({"mode": "real"}, "MODE_NOT_NOOP", "mode"),
        (
            {"ledger_terminal_status": "DONE"},
            "LEDGER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
            "ledger_terminal_status",
        ),
        (
            {"ledger_terminal_status": "PASS_PUBLISHED"},
            "PASS_PUBLISHED_FORBIDDEN",
            "ledger_terminal_status",
        ),
        (
            {"local_noop_runner_result_buildable_marker": False},
            "LOCAL_NOOP_RUNNER_RESULT_BUILDABLE_MARKER_NOT_TRUE",
            "local_noop_runner_result_buildable_marker",
        ),
        (
            {"local_noop_runner_result_buildable_marker": 1},
            "LOCAL_NOOP_RUNNER_RESULT_BUILDABLE_MARKER_NOT_TRUE",
            "local_noop_runner_result_buildable_marker",
        ),
        (
            {"public_url_is_null": False},
            "PUBLIC_URL_IS_NULL_NOT_TRUE",
            "public_url",
        ),
        (
            {"public_url_is_null": "true"},
            "PUBLIC_URL_IS_NULL_NOT_TRUE",
            "public_url",
        ),
        (
            {"public_url_created": True},
            "PUBLIC_URL_CREATED_NOT_FALSE",
            "public_url_created",
        ),
        (
            {"public_url_created": 0},
            "PUBLIC_URL_CREATED_NOT_FALSE",
            "public_url_created",
        ),
    )

    for overrides, reason_code, field in cases:
        result = _explain(**overrides)

        assert result["buildable"] is False
        assert reason_code in result["draft_violations"]
        assert field in result["missing_or_invalid_fields"]


def test_pass_published_status_is_blocked_and_suppressed_from_payload():
    result = _explain(ledger_terminal_status="PASS_PUBLISHED")

    assert result["reason_code"] == "PASS_PUBLISHED_FORBIDDEN"
    assert "LEDGER_TERMINAL_STATUS_NOT_NOOP_COMPLETED" in (
        result["draft_violations"]
    )
    assert result["source"]["ledger_terminal_status"] == ""
    assert result["run_ledger_draft"]["ledger_terminal_status"] == ""


def test_public_url_created_is_blocked_and_suppressed_from_payload():
    result = _explain(public_url_created=True)

    assert result["buildable"] is False
    assert "PUBLIC_URL_CREATED_NOT_FALSE" in result["draft_violations"]
    assert result["source"]["public_url_created"] is False
    assert result["run_ledger_draft"]["public_url_created"] is False


def test_refs_status_and_evidence_refs_are_opaque():
    result = _explain(
        local_noop_runner_result_ref="opaque-runner-result-ref",
        ledger_draft_evidence_items=(
            _ledger_draft_evidence_item(
                evidence_status="failed",
                evidence_refs=("opaque-evidence-ref",),
            ),
        ),
    )

    assert result["buildable"] is True
    assert (
        result["source"]["local_noop_runner_result_ref"]
        == "opaque-runner-result-ref"
    )
    assert (
        result["run_ledger_draft"]["ledger_draft_evidence_items"][0][
            "evidence_status"
        ]
        == "failed"
    )
    assert (
        result["run_ledger_draft"]["ledger_draft_evidence_items"][0][
            "evidence_refs"
        ]
        == ("opaque-evidence-ref",)
    )


def test_known_blocking_ledger_draft_evidence_ids_still_buildable():
    result = _explain(
        blocking_ledger_draft_evidence_ids=("ledger-draft-evidence-001",),
        ledger_draft_evidence_items=(
            _ledger_draft_evidence_item(evidence_status="failed"),
        ),
    )

    assert result["buildable"] is True
    assert result["run_ledger_draft"][
        "blocking_ledger_draft_evidence_ids"
    ] == ("ledger-draft-evidence-001",)


def test_unknown_blank_or_non_tuple_blocking_ids_block_buildability():
    cases = (
        ("missing-ledger-draft-evidence",),
        ("",),
        (1,),
        ["ledger-draft-evidence-001"],
    )

    for blocking_ledger_draft_evidence_ids in cases:
        result = _explain(
            blocking_ledger_draft_evidence_ids=blocking_ledger_draft_evidence_ids
        )

        assert result["buildable"] is False
        assert "BLOCKING_LEDGER_DRAFT_EVIDENCE_ID_UNKNOWN" in (
            result["draft_violations"]
        )
        assert "blocking_ledger_draft_evidence_ids" in (
            result["missing_or_invalid_fields"]
        )


def test_required_top_level_field_violations_are_collected():
    cases = (
        ({"run_id": ""}, "RUN_ID_MISSING", "run_id"),
        (
            {"run_ledger_draft_id": ""},
            "RUN_LEDGER_DRAFT_ID_MISSING",
            "run_ledger_draft_id",
        ),
        (
            {"local_noop_runner_result_ref": ""},
            "LOCAL_NOOP_RUNNER_RESULT_REF_MISSING",
            "local_noop_runner_result_ref",
        ),
        (
            {"ledger_draft_evidence_items": ()},
            "LEDGER_DRAFT_EVIDENCE_ITEMS_MISSING",
            "ledger_draft_evidence_items",
        ),
        (
            {"ledger_draft_evidence_items": []},
            "LEDGER_DRAFT_EVIDENCE_ITEMS_MISSING",
            "ledger_draft_evidence_items",
        ),
        (
            {"required_ledger_draft_evidence_ids": ()},
            "REQUIRED_LEDGER_DRAFT_EVIDENCE_IDS_MISSING",
            "required_ledger_draft_evidence_ids",
        ),
        (
            {"required_ledger_draft_evidence_ids": ("",)},
            "REQUIRED_LEDGER_DRAFT_EVIDENCE_IDS_MISSING",
            "required_ledger_draft_evidence_ids",
        ),
        (
            {"required_ledger_draft_evidence_ids": ["ledger-draft-evidence-001"]},
            "REQUIRED_LEDGER_DRAFT_EVIDENCE_IDS_MISSING",
            "required_ledger_draft_evidence_ids",
        ),
        (
            {"missing_ledger_draft_evidence_ids": ("ledger-draft-evidence-002",)},
            "MISSING_LEDGER_DRAFT_EVIDENCE_IDS_DECLARED",
            "missing_ledger_draft_evidence_ids",
        ),
        (
            {"missing_ledger_draft_evidence_ids": ["ledger-draft-evidence-002"]},
            "MISSING_LEDGER_DRAFT_EVIDENCE_IDS_DECLARED",
            "missing_ledger_draft_evidence_ids",
        ),
        ({"created_at": ""}, "CREATED_AT_MISSING", "created_at"),
        (
            {"timestamp_policy": ""},
            "TIMESTAMP_POLICY_MISSING",
            "timestamp_policy",
        ),
        ({"source_of_truth": ()}, "SOURCE_OF_TRUTH_MISSING", "source_of_truth"),
        (
            {"source_of_truth": ("",)},
            "SOURCE_OF_TRUTH_MISSING",
            "source_of_truth",
        ),
        (
            {"source_of_truth": ["p2d-36"]},
            "SOURCE_OF_TRUTH_MISSING",
            "source_of_truth",
        ),
    )

    for overrides, reason_code, field in cases:
        result = _explain(**overrides)

        assert result["buildable"] is False
        assert reason_code in result["draft_violations"]
        assert field in result["missing_or_invalid_fields"]


def test_ledger_draft_evidence_id_uniqueness_required_boundary_and_presence():
    duplicate = _explain(
        ledger_draft_evidence_items=(
            _ledger_draft_evidence_item(),
            _ledger_draft_evidence_item(),
        )
    )
    not_required = _explain(
        ledger_draft_evidence_items=(
            _ledger_draft_evidence_item(
                ledger_draft_evidence_id="ledger-draft-evidence-002"
            ),
        ),
        required_ledger_draft_evidence_ids=("ledger-draft-evidence-001",),
    )
    required_missing = _explain(
        required_ledger_draft_evidence_ids=(
            "ledger-draft-evidence-001",
            "ledger-draft-evidence-002",
        )
    )

    assert "LEDGER_DRAFT_EVIDENCE_ID_DUPLICATE" in duplicate["draft_violations"]
    assert "ledger_draft_evidence_items[1].ledger_draft_evidence_id" in (
        duplicate["missing_or_invalid_fields"]
    )
    assert "LEDGER_DRAFT_EVIDENCE_ID_NOT_REQUIRED" in (
        not_required["draft_violations"]
    )
    assert "ledger_draft_evidence_items[0].ledger_draft_evidence_id" in (
        not_required["missing_or_invalid_fields"]
    )
    assert "REQUIRED_LEDGER_DRAFT_EVIDENCE_MISSING" in (
        required_missing["draft_violations"]
    )
    assert "required_ledger_draft_evidence_ids.ledger-draft-evidence-002" in (
        required_missing["missing_or_invalid_fields"]
    )


def test_ledger_draft_evidence_item_fields_and_missing_keys_reported():
    string_field_cases = (
        ("ledger_draft_evidence_id", "", "LEDGER_DRAFT_EVIDENCE_ID_MISSING"),
        ("ledger_draft_evidence_role", "", "LEDGER_DRAFT_EVIDENCE_ROLE_MISSING"),
        ("artifact_ref", "", "LEDGER_DRAFT_EVIDENCE_ARTIFACT_REF_MISSING"),
        ("artifact_kind", "", "LEDGER_DRAFT_EVIDENCE_ARTIFACT_KIND_MISSING"),
        ("evidence_status", "", "LEDGER_DRAFT_EVIDENCE_STATUS_MISSING"),
        ("producer_ref", "", "LEDGER_DRAFT_EVIDENCE_PRODUCER_REF_MISSING"),
        ("evidence_refs", (), "LEDGER_DRAFT_EVIDENCE_REFS_MISSING"),
        ("evidence_refs", ("",), "LEDGER_DRAFT_EVIDENCE_REFS_MISSING"),
        ("evidence_refs", ["ref"], "LEDGER_DRAFT_EVIDENCE_REFS_MISSING"),
    )

    for field, value, reason_code in string_field_cases:
        result = _explain(
            ledger_draft_evidence_items=(
                _ledger_draft_evidence_item(**{field: value}),
            )
        )

        assert result["buildable"] is False
        assert reason_code in result["draft_violations"]
        assert f"ledger_draft_evidence_items[0].{field}" in (
            result["missing_or_invalid_fields"]
        )
        assert tuple(
            result["ledger_draft_evidence_item_violations"][0].keys()
        ) == LEDGER_DRAFT_EVIDENCE_ITEM_VIOLATION_KEYS

    for missing_key, reason_code in MISSING_LEDGER_DRAFT_EVIDENCE_ITEM_KEY_EXPECTATIONS:
        ledger_draft_evidence_item = _ledger_draft_evidence_item()
        del ledger_draft_evidence_item[missing_key]
        result = _explain(ledger_draft_evidence_items=(ledger_draft_evidence_item,))

        assert result["buildable"] is False
        assert "LEDGER_DRAFT_EVIDENCE_ITEM_KEYS_INVALID" in (
            result["draft_violations"]
        )
        assert reason_code in result["draft_violations"]
        assert f"ledger_draft_evidence_items[0].{missing_key}" in (
            result["missing_or_invalid_fields"]
        )
        assert "ledger_draft_evidence_items[0].keys" in (
            result["missing_or_invalid_fields"]
        )


def test_non_dict_ledger_draft_evidence_item_records_violation_shape():
    result = _explain(ledger_draft_evidence_items=("not-an-evidence-item",))

    assert result["buildable"] is False
    assert "LEDGER_DRAFT_EVIDENCE_ITEM_NOT_DICT" in result["draft_violations"]
    assert "ledger_draft_evidence_items[0]" in result["missing_or_invalid_fields"]
    assert tuple(result["ledger_draft_evidence_item_violations"][0].keys()) == (
        LEDGER_DRAFT_EVIDENCE_ITEM_VIOLATION_KEYS
    )
    assert result["run_ledger_draft"]["ledger_draft_evidence_items"][0] == {
        "ledger_draft_evidence_id": "",
        "ledger_draft_evidence_role": "",
        "artifact_ref": "",
        "artifact_kind": "",
        "evidence_status": "",
        "producer_ref": "",
        "evidence_refs": (),
        "notes": (),
    }


def test_forbidden_raw_execution_url_and_publication_fields_are_suppressed():
    for field in FORBIDDEN_LEDGER_DRAFT_EVIDENCE_ITEM_FIELDS:
        result = _explain(
            ledger_draft_evidence_items=(
                _ledger_draft_evidence_item(**{field: "forbidden"}),
            )
        )

        assert result["buildable"] is False
        assert "LEDGER_DRAFT_EVIDENCE_ITEM_KEYS_INVALID" in (
            result["draft_violations"]
        )
        assert "LEDGER_DRAFT_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT" in (
            result["draft_violations"]
        )
        assert f"ledger_draft_evidence_items[0].{field}" in (
            result["missing_or_invalid_fields"]
        )
        assert field not in (
            result["run_ledger_draft"]["ledger_draft_evidence_items"][0]
        )
        assert tuple(
            result["ledger_draft_evidence_item_violations"][0].keys()
        ) == LEDGER_DRAFT_EVIDENCE_ITEM_VIOLATION_KEYS


def test_output_does_not_expose_public_url_is_null_or_extra_url_values():
    result = _explain()
    forbidden_url = _explain(
        ledger_draft_evidence_items=(
            _ledger_draft_evidence_item(public_url_value="https://example.test"),
        )
    )
    payload_keys = _payload_keys(result)
    forbidden_payload_keys = _payload_keys(forbidden_url)

    assert "public_url_is_null" not in payload_keys
    assert result["source"]["public_url"] is None
    assert result["run_ledger_draft"]["public_url"] is None
    assert "public_url_value" not in forbidden_payload_keys
    assert forbidden_url["source"]["public_url"] is None
    assert forbidden_url["run_ledger_draft"]["public_url"] is None


def test_reason_catalog_priority_and_forbidden_pseudo_reason_codes():
    assert builder.REASON_CODES == REASON_CODES
    assert builder.RUN_LEDGER_DRAFT_BUILD_REASON_CODES == REASON_CODES
    assert builder.REASON_PRIORITY == REASON_PRIORITY

    for reason_code in FORBIDDEN_PSEUDO_REASON_CODES:
        assert reason_code not in builder.REASON_CODES
        assert reason_code not in builder.REASON_PRIORITY


def test_forbidden_module_namespace_and_io_names_are_absent():
    for module_name in FORBIDDEN_MODULE_NAMES:
        assert not hasattr(builder, module_name)


def test_all_violations_are_priority_ordered_and_details_present():
    first_item = _ledger_draft_evidence_item(
        ledger_draft_evidence_id="",
        ledger_draft_evidence_role="",
        artifact_ref="",
        artifact_kind="",
        evidence_status="",
        producer_ref="",
        evidence_refs=(),
        raw_artifact_content="raw",
    )
    second_item = _ledger_draft_evidence_item(
        ledger_draft_evidence_id="extra-evidence"
    )
    result = _explain(
        run_id="",
        run_ledger_draft_id="",
        draft_kind="wrong",
        mode="real",
        ledger_terminal_status="PASS_PUBLISHED",
        local_noop_runner_result_ref="",
        local_noop_runner_result_buildable_marker=False,
        public_url_is_null=False,
        public_url_created=True,
        ledger_draft_evidence_items=(first_item, second_item),
        required_ledger_draft_evidence_ids=(
            "ledger-draft-evidence-001",
            "ledger-draft-evidence-002",
        ),
        missing_ledger_draft_evidence_ids=("ledger-draft-evidence-002",),
        blocking_ledger_draft_evidence_ids=("missing-block",),
        created_at="",
        timestamp_policy="",
        source_of_truth=(),
    )
    expected_order = tuple(
        reason_code
        for reason_code in REASON_PRIORITY
        if reason_code != "RUN_LEDGER_DRAFT_BUILDABLE"
        and reason_code in result["draft_violations"]
    )

    assert result["draft_violations"] == expected_order
    assert result["reason_code"] == result["draft_violations"][0]
    assert "ledger_draft_evidence_items[0].raw_artifact_content" in (
        result["missing_or_invalid_fields"]
    )
    assert "ledger_draft_evidence_items[1].ledger_draft_evidence_id" in (
        result["missing_or_invalid_fields"]
    )
    assert "required_ledger_draft_evidence_ids.ledger-draft-evidence-002" in (
        result["missing_or_invalid_fields"]
    )
    assert result["ledger_draft_evidence_item_violations"] != ()
    for violation in result["ledger_draft_evidence_item_violations"]:
        assert tuple(violation.keys()) == (
            LEDGER_DRAFT_EVIDENCE_ITEM_VIOLATION_KEYS
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
    assert "run_ledger_draft_not_runner_execution" in (
        result["invariant_refs"]
    )
    assert "public_url" in payload_keys
    assert result["source"]["public_url"] is None
    assert result["run_ledger_draft"]["public_url"] is None
    assert "no_raw_url" not in payload_keys
    assert "no_public_url_behavior" not in payload_keys
