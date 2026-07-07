"""Tests for the pure local noop E2E dry-run contract builder."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import (  # noqa: E402
    local_noop_e2e_contract_builder as builder,
)


RESULT_KEYS = (
    "buildable",
    "reason_code",
    "reason",
    "source",
    "local_noop_e2e_contract",
    "contract_violations",
    "missing_or_invalid_fields",
    "dry_run_evidence_item_violations",
    "invariant_refs",
)

SOURCE_KEYS = (
    "gate_input_ref",
    "gate_input_buildable_marker",
    "local_noop_run_assembly_ref",
    "local_noop_run_buildable_marker",
    "mode",
    "e2e_terminal_status",
    "public_url",
    "public_url_created",
    "source_of_truth",
)

LOCAL_NOOP_E2E_CONTRACT_KEYS = (
    "run_id",
    "local_noop_e2e_contract_id",
    "contract_kind",
    "mode",
    "e2e_terminal_status",
    "gate_input_ref",
    "gate_input_buildable_marker",
    "local_noop_run_assembly_ref",
    "local_noop_run_buildable_marker",
    "public_url",
    "public_url_created",
    "dry_run_evidence_items",
    "required_dry_run_evidence_ids",
    "missing_dry_run_evidence_ids",
    "blocking_dry_run_evidence_ids",
    "created_at",
    "timestamp_policy",
    "source_of_truth",
    "notes",
)

DRY_RUN_EVIDENCE_ITEM_KEYS = (
    "dry_run_evidence_id",
    "dry_run_evidence_role",
    "artifact_ref",
    "artifact_kind",
    "evidence_status",
    "producer_ref",
    "evidence_refs",
    "notes",
)

DRY_RUN_EVIDENCE_ITEM_VIOLATION_KEYS = (
    "dry_run_evidence_item_index",
    "dry_run_evidence_id",
    "reason_code",
    "field",
)

REASON_CODES = (
    "LOCAL_NOOP_E2E_CONTRACT_BUILDABLE",
    "RUN_ID_MISSING",
    "LOCAL_NOOP_E2E_CONTRACT_ID_MISSING",
    "CONTRACT_KIND_NOT_LOCAL_NOOP_E2E_DRY_RUN_CONTRACT",
    "MODE_NOT_NOOP",
    "PASS_PUBLISHED_FORBIDDEN",
    "E2E_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
    "GATE_INPUT_REF_MISSING",
    "GATE_INPUT_BUILDABLE_MARKER_NOT_TRUE",
    "LOCAL_NOOP_RUN_ASSEMBLY_REF_MISSING",
    "LOCAL_NOOP_RUN_BUILDABLE_MARKER_NOT_TRUE",
    "PUBLIC_URL_IS_NULL_NOT_TRUE",
    "PUBLIC_URL_CREATED_NOT_FALSE",
    "DRY_RUN_EVIDENCE_ITEMS_MISSING",
    "REQUIRED_DRY_RUN_EVIDENCE_IDS_MISSING",
    "MISSING_DRY_RUN_EVIDENCE_IDS_DECLARED",
    "BLOCKING_DRY_RUN_EVIDENCE_ID_UNKNOWN",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "DRY_RUN_EVIDENCE_ITEM_NOT_DICT",
    "DRY_RUN_EVIDENCE_ITEM_KEYS_INVALID",
    "DRY_RUN_EVIDENCE_ID_MISSING",
    "DRY_RUN_EVIDENCE_ROLE_MISSING",
    "DRY_RUN_EVIDENCE_ARTIFACT_REF_MISSING",
    "DRY_RUN_EVIDENCE_ARTIFACT_KIND_MISSING",
    "DRY_RUN_EVIDENCE_STATUS_MISSING",
    "DRY_RUN_EVIDENCE_PRODUCER_REF_MISSING",
    "DRY_RUN_EVIDENCE_REFS_MISSING",
    "DRY_RUN_EVIDENCE_ID_DUPLICATE",
    "DRY_RUN_EVIDENCE_ID_NOT_REQUIRED",
    "REQUIRED_DRY_RUN_EVIDENCE_MISSING",
    "DRY_RUN_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT",
)

REASON_PRIORITY = (
    "RUN_ID_MISSING",
    "LOCAL_NOOP_E2E_CONTRACT_ID_MISSING",
    "CONTRACT_KIND_NOT_LOCAL_NOOP_E2E_DRY_RUN_CONTRACT",
    "MODE_NOT_NOOP",
    "PASS_PUBLISHED_FORBIDDEN",
    "E2E_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
    "GATE_INPUT_REF_MISSING",
    "GATE_INPUT_BUILDABLE_MARKER_NOT_TRUE",
    "LOCAL_NOOP_RUN_ASSEMBLY_REF_MISSING",
    "LOCAL_NOOP_RUN_BUILDABLE_MARKER_NOT_TRUE",
    "PUBLIC_URL_IS_NULL_NOT_TRUE",
    "PUBLIC_URL_CREATED_NOT_FALSE",
    "DRY_RUN_EVIDENCE_ITEMS_MISSING",
    "REQUIRED_DRY_RUN_EVIDENCE_IDS_MISSING",
    "MISSING_DRY_RUN_EVIDENCE_IDS_DECLARED",
    "BLOCKING_DRY_RUN_EVIDENCE_ID_UNKNOWN",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "DRY_RUN_EVIDENCE_ITEM_NOT_DICT",
    "DRY_RUN_EVIDENCE_ITEM_KEYS_INVALID",
    "DRY_RUN_EVIDENCE_ID_MISSING",
    "DRY_RUN_EVIDENCE_ROLE_MISSING",
    "DRY_RUN_EVIDENCE_ARTIFACT_REF_MISSING",
    "DRY_RUN_EVIDENCE_ARTIFACT_KIND_MISSING",
    "DRY_RUN_EVIDENCE_STATUS_MISSING",
    "DRY_RUN_EVIDENCE_PRODUCER_REF_MISSING",
    "DRY_RUN_EVIDENCE_REFS_MISSING",
    "DRY_RUN_EVIDENCE_ID_DUPLICATE",
    "DRY_RUN_EVIDENCE_ID_NOT_REQUIRED",
    "REQUIRED_DRY_RUN_EVIDENCE_MISSING",
    "DRY_RUN_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT",
    "LOCAL_NOOP_E2E_CONTRACT_BUILDABLE",
)

FORBIDDEN_DRY_RUN_EVIDENCE_ITEM_FIELDS = (
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
    "should_fetch",
    "should_read_reader",
    "should_read_training_report",
    "should_read_validator_result",
    "should_read_rubric_review",
    "should_read_audit_review",
    "should_read_gate_input",
    "should_read_local_noop_run",
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
    "reader_read",
    "training_report_read",
    "validator_result_read",
    "rubric_review_read",
    "audit_review_read",
    "gate_input_read",
    "local_noop_run_read",
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
    "published",
    "notified",
    "ledger_written",
    "public_url_created_executed",
)

FORBIDDEN_PSEUDO_REASON_CODES = (
    "READER_READ_FORBIDDEN",
    "TRAINING_REPORT_READ_FORBIDDEN",
    "VALIDATOR_RESULT_READ_FORBIDDEN",
    "RUBRIC_REVIEW_READ_FORBIDDEN",
    "AUDIT_REVIEW_READ_FORBIDDEN",
    "GATE_INPUT_READ_FORBIDDEN",
    "LOCAL_NOOP_RUN_READ_FORBIDDEN",
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
    "PUBLISH_FORBIDDEN",
    "LEDGER_WRITE_FORBIDDEN",
    "NOTIFICATION_FORBIDDEN",
    "PUBLIC_URL_CREATION_FORBIDDEN",
)

FORBIDDEN_MODULE_NAMES = (
    "states",
    "gates",
    "artifacts",
    "gate_input_assembly_builder",
    "local_noop_run_assembly_builder",
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
    "build_local_noop_e2e_contract",
    "run_local_noop_e2e_contract",
    "execute_dry_run",
    "execute_e2e",
    "complete_noop",
    "run_noop_completion",
    "run_transition",
    "run_gate",
    "run_policy_engine",
    "compute_publish_allowed",
    "compute_quality_pass",
    "compute_gate_decision",
    "publish",
    "create_public_url",
    "write_ledger",
    "send_notification",
)

REQUIRED_INVARIANT_REFS = (
    "local_noop_e2e_contract_builder_only",
    "builder_not_reader_reader",
    "builder_not_training_report_reader",
    "builder_not_validator_result_reader",
    "builder_not_rubric_review_reader",
    "builder_not_audit_review_reader",
    "builder_not_gate_input_reader",
    "builder_not_local_noop_run_reader",
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
    "builder_not_publisher",
    "builder_not_ledger_writer",
    "builder_not_notifier",
    "dry_run_evidence_items_are_caller_supplied",
    "dry_run_evidence_status_is_caller_supplied",
    "gate_input_ref_is_caller_supplied",
    "gate_input_buildable_marker_is_caller_supplied",
    "local_noop_run_assembly_ref_is_caller_supplied",
    "local_noop_run_buildable_marker_is_caller_supplied",
    "gate_input_ref_opaque",
    "local_noop_run_assembly_ref_opaque",
    "artifact_refs_opaque",
    "evidence_refs_opaque",
    "local_noop_e2e_contract_governance_evidence_bundle",
    "local_noop_e2e_contract_not_runtime_execution",
    "local_noop_e2e_contract_not_state_transition",
    "local_noop_e2e_contract_not_gate_decision",
    "local_noop_e2e_contract_not_publish_artifact",
    "local_noop_e2e_contract_not_public_candidate",
    "mode_noop_required",
    "public_url_must_be_null",
    "public_url_created_must_be_false",
    "e2e_terminal_status_must_be_noop_completed",
    "noop_completed_not_pass_published",
    "pass_published_forbidden",
    "mode_noop_not_publish",
    "gate_input_buildable_marker_not_quality_pass",
    "gate_input_buildable_marker_not_gate_pass",
    "gate_input_buildable_marker_not_publish_allowed",
    "local_noop_run_buildable_marker_not_publish_allowed",
    "dry_run_evidence_status_not_quality_pass",
    "dry_run_evidence_status_not_gate_pass",
    "dry_run_evidence_status_not_publish_allowed",
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
    "blocking_dry_run_evidence_ids_are_evidence_only",
    "blocking_dry_run_evidence_ids_do_not_execute_gate",
    "blocking_dry_run_evidence_ids_do_not_execute_noop_completion",
    "blocking_dry_run_evidence_ids_do_not_execute_dry_run",
    "no_reader_read",
    "no_training_report_read",
    "no_validator_result_read",
    "no_rubric_review_read",
    "no_audit_review_read",
    "no_gate_input_read",
    "no_local_noop_run_read",
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
    "no_runtime_execution",
    "no_adapter_execution",
    "no_publish",
    "no_notification",
    "no_ledger_write",
    "no_public_url_behavior",
    "no_quality_pass_no_public_url",
)

MISSING_DRY_RUN_EVIDENCE_ITEM_KEY_EXPECTATIONS = (
    ("dry_run_evidence_id", "DRY_RUN_EVIDENCE_ID_MISSING"),
    ("dry_run_evidence_role", "DRY_RUN_EVIDENCE_ROLE_MISSING"),
    ("artifact_ref", "DRY_RUN_EVIDENCE_ARTIFACT_REF_MISSING"),
    ("artifact_kind", "DRY_RUN_EVIDENCE_ARTIFACT_KIND_MISSING"),
    ("evidence_status", "DRY_RUN_EVIDENCE_STATUS_MISSING"),
    ("producer_ref", "DRY_RUN_EVIDENCE_PRODUCER_REF_MISSING"),
    ("evidence_refs", "DRY_RUN_EVIDENCE_REFS_MISSING"),
    ("notes", "DRY_RUN_EVIDENCE_ITEM_KEYS_INVALID"),
)


def _dry_run_evidence_item(**overrides):
    values = {
        "dry_run_evidence_id": "dry-run-evidence-001",
        "dry_run_evidence_role": "local_noop_e2e_contract",
        "artifact_ref": "local-noop-run-assembly-001",
        "artifact_kind": "local_noop_run_assembly",
        "evidence_status": "passed",
        "producer_ref": "caller-supplied-local-noop-e2e-contract",
        "evidence_refs": ("local-noop-run-assembly-001#noop-contract",),
        "notes": ("caller-supplied-evidence-only",),
    }
    values.update(overrides)
    return values


def _valid_values():
    return {
        "run_id": "run-001",
        "local_noop_e2e_contract_id": "local-noop-e2e-contract-001",
        "contract_kind": "local_noop_e2e_dry_run_contract",
        "mode": "noop",
        "e2e_terminal_status": "NOOP_COMPLETED",
        "gate_input_ref": "gate-input-001",
        "gate_input_buildable_marker": True,
        "local_noop_run_assembly_ref": "local-noop-run-assembly-001",
        "local_noop_run_buildable_marker": True,
        "public_url_created": False,
        "public_url_is_null": True,
        "dry_run_evidence_items": (_dry_run_evidence_item(),),
        "required_dry_run_evidence_ids": ("dry-run-evidence-001",),
        "missing_dry_run_evidence_ids": (),
        "blocking_dry_run_evidence_ids": (),
        "created_at": "caller-supplied-created-at",
        "timestamp_policy": "caller_supplied_timestamp_marker",
        "source_of_truth": ("p2d-33",),
        "notes": ("structured-only",),
    }


def _explain(**overrides):
    values = _valid_values()
    values.update(overrides)
    return builder.explain_local_noop_e2e_contract_build(**values)


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
    assert builder.LOCAL_NOOP_E2E_CONTRACT_BUILD_REASON_CODES == (
        REASON_CODES
    )
    assert builder.REASON_PRIORITY == REASON_PRIORITY


def test_valid_local_noop_e2e_contract_is_buildable_with_exact_shapes():
    result = _explain()

    assert result["buildable"] is True
    assert result["reason_code"] == "LOCAL_NOOP_E2E_CONTRACT_BUILDABLE"
    assert result["contract_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()
    assert result["dry_run_evidence_item_violations"] == ()
    assert tuple(result.keys()) == RESULT_KEYS
    assert tuple(result["source"].keys()) == SOURCE_KEYS
    assert tuple(result["local_noop_e2e_contract"].keys()) == (
        LOCAL_NOOP_E2E_CONTRACT_KEYS
    )
    assert tuple(
        result["local_noop_e2e_contract"]["dry_run_evidence_items"][0].keys()
    ) == DRY_RUN_EVIDENCE_ITEM_KEYS
    assert result["source"]["public_url"] is None
    assert result["local_noop_e2e_contract"]["public_url"] is None


def test_public_api_is_keyword_only_and_bool_wrapper_matches_explain():
    expected_kwonly = len(LOCAL_NOOP_E2E_CONTRACT_KEYS)

    assert builder.explain_local_noop_e2e_contract_build.__code__.co_argcount == 0
    assert (
        builder.explain_local_noop_e2e_contract_build.__code__
        .co_kwonlyargcount
        == expected_kwonly
    )
    assert builder.is_local_noop_e2e_contract_buildable.__code__.co_argcount == 0
    assert (
        builder.is_local_noop_e2e_contract_buildable.__code__.co_kwonlyargcount
        == expected_kwonly
    )

    cases = (
        _valid_values(),
        {**_valid_values(), "run_id": ""},
        {**_valid_values(), "e2e_terminal_status": "PASS_PUBLISHED"},
        {**_valid_values(), "public_url_is_null": False},
    )
    for values in cases:
        explanation = builder.explain_local_noop_e2e_contract_build(**values)
        assert (
            builder.is_local_noop_e2e_contract_buildable(**values)
            is explanation["buildable"]
        )


def test_required_lockin_markers_block_when_invalid():
    cases = (
        (
            {"contract_kind": "dry_run_contract"},
            "CONTRACT_KIND_NOT_LOCAL_NOOP_E2E_DRY_RUN_CONTRACT",
            "contract_kind",
        ),
        ({"mode": "real"}, "MODE_NOT_NOOP", "mode"),
        (
            {"e2e_terminal_status": "DONE"},
            "E2E_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
            "e2e_terminal_status",
        ),
        (
            {"e2e_terminal_status": "PASS_PUBLISHED"},
            "PASS_PUBLISHED_FORBIDDEN",
            "e2e_terminal_status",
        ),
        (
            {"gate_input_buildable_marker": False},
            "GATE_INPUT_BUILDABLE_MARKER_NOT_TRUE",
            "gate_input_buildable_marker",
        ),
        (
            {"gate_input_buildable_marker": 1},
            "GATE_INPUT_BUILDABLE_MARKER_NOT_TRUE",
            "gate_input_buildable_marker",
        ),
        (
            {"local_noop_run_buildable_marker": False},
            "LOCAL_NOOP_RUN_BUILDABLE_MARKER_NOT_TRUE",
            "local_noop_run_buildable_marker",
        ),
        (
            {"local_noop_run_buildable_marker": 1},
            "LOCAL_NOOP_RUN_BUILDABLE_MARKER_NOT_TRUE",
            "local_noop_run_buildable_marker",
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
        assert reason_code in result["contract_violations"]
        assert field in result["missing_or_invalid_fields"]


def test_pass_published_status_is_blocked_and_suppressed_from_payload():
    result = _explain(e2e_terminal_status="PASS_PUBLISHED")

    assert result["reason_code"] == "PASS_PUBLISHED_FORBIDDEN"
    assert "E2E_TERMINAL_STATUS_NOT_NOOP_COMPLETED" in (
        result["contract_violations"]
    )
    assert result["source"]["e2e_terminal_status"] == ""
    assert result["local_noop_e2e_contract"]["e2e_terminal_status"] == ""


def test_refs_markers_status_and_evidence_refs_are_opaque():
    result = _explain(
        gate_input_ref="opaque-gate-input-ref",
        local_noop_run_assembly_ref="opaque-local-noop-run-ref",
        dry_run_evidence_items=(
            _dry_run_evidence_item(
                artifact_ref="opaque-artifact-ref",
                artifact_kind="opaque-artifact-kind",
                evidence_status="failed",
                evidence_refs=("opaque-evidence-ref",),
            ),
        ),
    )
    empty_refs = _explain(
        dry_run_evidence_items=(
            _dry_run_evidence_item(evidence_refs=()),
        ),
    )
    list_refs = _explain(
        dry_run_evidence_items=(
            _dry_run_evidence_item(evidence_refs=["evidence"]),
        ),
    )

    assert result["buildable"] is True
    assert result["source"]["gate_input_ref"] == "opaque-gate-input-ref"
    assert result["source"]["local_noop_run_assembly_ref"] == (
        "opaque-local-noop-run-ref"
    )
    assert (
        result["local_noop_e2e_contract"]["dry_run_evidence_items"][0][
            "evidence_status"
        ]
        == "failed"
    )
    assert empty_refs["reason_code"] == "DRY_RUN_EVIDENCE_REFS_MISSING"
    assert "DRY_RUN_EVIDENCE_REFS_MISSING" in (
        list_refs["contract_violations"]
    )


def test_known_blocking_dry_run_evidence_ids_still_buildable():
    result = _explain(
        blocking_dry_run_evidence_ids=("dry-run-evidence-001",),
        dry_run_evidence_items=(
            _dry_run_evidence_item(evidence_status="failed"),
        ),
    )

    assert result["buildable"] is True
    assert result["local_noop_e2e_contract"][
        "blocking_dry_run_evidence_ids"
    ] == ("dry-run-evidence-001",)


def test_unknown_blank_or_non_tuple_blocking_ids_block_buildability():
    cases = (
        ("unknown-evidence",),
        ("",),
        (object(),),
        ["dry-run-evidence-001"],
    )

    for blocking_dry_run_evidence_ids in cases:
        result = _explain(
            blocking_dry_run_evidence_ids=blocking_dry_run_evidence_ids
        )

        assert result["buildable"] is False
        assert result["reason_code"] == (
            "BLOCKING_DRY_RUN_EVIDENCE_ID_UNKNOWN"
        )
        assert "blocking_dry_run_evidence_ids" in (
            result["missing_or_invalid_fields"]
        )


def test_required_top_level_field_violations_are_collected():
    cases = (
        ({"run_id": ""}, "RUN_ID_MISSING", "run_id"),
        (
            {"local_noop_e2e_contract_id": ""},
            "LOCAL_NOOP_E2E_CONTRACT_ID_MISSING",
            "local_noop_e2e_contract_id",
        ),
        ({"gate_input_ref": ""}, "GATE_INPUT_REF_MISSING", "gate_input_ref"),
        (
            {"local_noop_run_assembly_ref": ""},
            "LOCAL_NOOP_RUN_ASSEMBLY_REF_MISSING",
            "local_noop_run_assembly_ref",
        ),
        (
            {"dry_run_evidence_items": ()},
            "DRY_RUN_EVIDENCE_ITEMS_MISSING",
            "dry_run_evidence_items",
        ),
        (
            {"dry_run_evidence_items": []},
            "DRY_RUN_EVIDENCE_ITEMS_MISSING",
            "dry_run_evidence_items",
        ),
        (
            {"required_dry_run_evidence_ids": ()},
            "REQUIRED_DRY_RUN_EVIDENCE_IDS_MISSING",
            "required_dry_run_evidence_ids",
        ),
        (
            {"required_dry_run_evidence_ids": ("",)},
            "REQUIRED_DRY_RUN_EVIDENCE_IDS_MISSING",
            "required_dry_run_evidence_ids",
        ),
        (
            {"required_dry_run_evidence_ids": ["dry-run-evidence-001"]},
            "REQUIRED_DRY_RUN_EVIDENCE_IDS_MISSING",
            "required_dry_run_evidence_ids",
        ),
        (
            {"missing_dry_run_evidence_ids": ("dry-run-evidence-002",)},
            "MISSING_DRY_RUN_EVIDENCE_IDS_DECLARED",
            "missing_dry_run_evidence_ids",
        ),
        (
            {"missing_dry_run_evidence_ids": ["dry-run-evidence-002"]},
            "MISSING_DRY_RUN_EVIDENCE_IDS_DECLARED",
            "missing_dry_run_evidence_ids",
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
        (
            {"source_of_truth": ["p2d-33"]},
            "SOURCE_OF_TRUTH_MISSING",
            "source_of_truth",
        ),
    )

    for overrides, reason_code, field in cases:
        result = _explain(**overrides)

        assert result["buildable"] is False
        assert reason_code in result["contract_violations"]
        assert field in result["missing_or_invalid_fields"]
        assert result["reason_code"] == result["contract_violations"][0]


def test_dry_run_evidence_id_uniqueness_required_boundary_and_presence():
    duplicate = _explain(
        dry_run_evidence_items=(
            _dry_run_evidence_item(),
            _dry_run_evidence_item(),
        ),
    )
    not_required = _explain(
        dry_run_evidence_items=(
            _dry_run_evidence_item(
                dry_run_evidence_id="dry-run-evidence-002"
            ),
        ),
        required_dry_run_evidence_ids=("dry-run-evidence-001",),
    )
    required_missing = _explain(
        required_dry_run_evidence_ids=(
            "dry-run-evidence-001",
            "dry-run-evidence-002",
        ),
    )

    assert "DRY_RUN_EVIDENCE_ID_DUPLICATE" in (
        duplicate["contract_violations"]
    )
    assert "DRY_RUN_EVIDENCE_ID_NOT_REQUIRED" in (
        not_required["contract_violations"]
    )
    assert "REQUIRED_DRY_RUN_EVIDENCE_MISSING" in (
        not_required["contract_violations"]
    )
    assert "REQUIRED_DRY_RUN_EVIDENCE_MISSING" in (
        required_missing["contract_violations"]
    )
    assert "required_dry_run_evidence_ids.dry-run-evidence-002" in (
        required_missing["missing_or_invalid_fields"]
    )


def test_dry_run_evidence_item_fields_and_missing_keys_reported():
    field_cases = (
        ("dry_run_evidence_id", "", "DRY_RUN_EVIDENCE_ID_MISSING"),
        ("dry_run_evidence_role", "", "DRY_RUN_EVIDENCE_ROLE_MISSING"),
        ("artifact_ref", "", "DRY_RUN_EVIDENCE_ARTIFACT_REF_MISSING"),
        ("artifact_kind", "", "DRY_RUN_EVIDENCE_ARTIFACT_KIND_MISSING"),
        ("evidence_status", "", "DRY_RUN_EVIDENCE_STATUS_MISSING"),
        ("producer_ref", "", "DRY_RUN_EVIDENCE_PRODUCER_REF_MISSING"),
        ("evidence_refs", (), "DRY_RUN_EVIDENCE_REFS_MISSING"),
    )

    for field, value, reason_code in field_cases:
        result = _explain(
            dry_run_evidence_items=(
                _dry_run_evidence_item(**{field: value}),
            ),
        )

        assert reason_code in result["contract_violations"]
        assert f"dry_run_evidence_items[0].{field}" in (
            result["missing_or_invalid_fields"]
        )
        assert tuple(
            result["dry_run_evidence_item_violations"][0].keys()
        ) == DRY_RUN_EVIDENCE_ITEM_VIOLATION_KEYS

    for missing_key, expected_reason_code in (
        MISSING_DRY_RUN_EVIDENCE_ITEM_KEY_EXPECTATIONS
    ):
        dry_run_evidence_item = _dry_run_evidence_item()
        del dry_run_evidence_item[missing_key]
        result = _explain(
            dry_run_evidence_items=(dry_run_evidence_item,)
        )

        assert "DRY_RUN_EVIDENCE_ITEM_KEYS_INVALID" in (
            result["contract_violations"]
        )
        assert expected_reason_code in result["contract_violations"]
        assert (
            f"dry_run_evidence_items[0].{missing_key}"
            in result["missing_or_invalid_fields"]
        ) or (
            missing_key == "notes"
            and "dry_run_evidence_items[0].keys"
            in result["missing_or_invalid_fields"]
        )


def test_non_dict_dry_run_evidence_item_records_violation_shape():
    result = _explain(dry_run_evidence_items=("not-an-evidence-item",))

    assert result["buildable"] is False
    assert result["reason_code"] == "DRY_RUN_EVIDENCE_ITEM_NOT_DICT"
    assert result["contract_violations"] == (
        "DRY_RUN_EVIDENCE_ITEM_NOT_DICT",
        "REQUIRED_DRY_RUN_EVIDENCE_MISSING",
    )
    assert tuple(result["dry_run_evidence_item_violations"][0].keys()) == (
        DRY_RUN_EVIDENCE_ITEM_VIOLATION_KEYS
    )
    assert result["local_noop_e2e_contract"]["dry_run_evidence_items"][0] == {
        "dry_run_evidence_id": "",
        "dry_run_evidence_role": "",
        "artifact_ref": "",
        "artifact_kind": "",
        "evidence_status": "",
        "producer_ref": "",
        "evidence_refs": (),
        "notes": (),
    }


def test_forbidden_raw_execution_url_and_publication_fields_are_suppressed():
    for field in FORBIDDEN_DRY_RUN_EVIDENCE_ITEM_FIELDS:
        result = _explain(
            dry_run_evidence_items=(
                _dry_run_evidence_item(**{field: "forbidden"}),
            ),
        )
        payload_keys = _payload_keys(result)

        assert "DRY_RUN_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT" in (
            result["contract_violations"]
        )
        assert "DRY_RUN_EVIDENCE_ITEM_KEYS_INVALID" in (
            result["contract_violations"]
        )
        assert field not in payload_keys
        assert tuple(
            result["dry_run_evidence_item_violations"][0].keys()
        ) == DRY_RUN_EVIDENCE_ITEM_VIOLATION_KEYS


def test_output_does_not_expose_public_url_is_null_or_extra_url_values():
    result = _explain()
    forbidden_url = _explain(
        dry_run_evidence_items=(
            _dry_run_evidence_item(public_url_value="https://example.test"),
        ),
    )
    payload_keys = _payload_keys(result)
    forbidden_payload_keys = _payload_keys(forbidden_url)

    assert "public_url_is_null" not in payload_keys
    assert result["source"]["public_url"] is None
    assert result["local_noop_e2e_contract"]["public_url"] is None
    assert "public_url_value" not in forbidden_payload_keys
    assert forbidden_url["source"]["public_url"] is None
    assert forbidden_url["local_noop_e2e_contract"]["public_url"] is None


def test_reason_catalog_priority_and_forbidden_pseudo_reason_codes():
    assert builder.REASON_CODES == REASON_CODES
    assert builder.LOCAL_NOOP_E2E_CONTRACT_BUILD_REASON_CODES == (
        REASON_CODES
    )
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
    first_item = _dry_run_evidence_item(
        dry_run_evidence_id="",
        dry_run_evidence_role="",
        artifact_ref="",
        artifact_kind="",
        evidence_status="",
        producer_ref="",
        evidence_refs=(),
        raw_artifact_content="raw",
    )
    second_item = _dry_run_evidence_item(
        dry_run_evidence_id="extra-evidence"
    )
    result = _explain(
        run_id="",
        local_noop_e2e_contract_id="",
        contract_kind="wrong",
        mode="real",
        e2e_terminal_status="PASS_PUBLISHED",
        gate_input_ref="",
        gate_input_buildable_marker=False,
        local_noop_run_assembly_ref="",
        local_noop_run_buildable_marker=False,
        public_url_is_null=False,
        public_url_created=True,
        dry_run_evidence_items=(first_item, second_item),
        required_dry_run_evidence_ids=(
            "dry-run-evidence-001",
            "dry-run-evidence-002",
        ),
        missing_dry_run_evidence_ids=("dry-run-evidence-002",),
        blocking_dry_run_evidence_ids=("missing-block",),
        created_at="",
        timestamp_policy="",
        source_of_truth=(),
    )
    expected_order = tuple(
        reason_code
        for reason_code in REASON_PRIORITY
        if reason_code != "LOCAL_NOOP_E2E_CONTRACT_BUILDABLE"
        and reason_code in result["contract_violations"]
    )

    assert result["contract_violations"] == expected_order
    assert result["reason_code"] == result["contract_violations"][0]
    assert "dry_run_evidence_items[0].raw_artifact_content" in (
        result["missing_or_invalid_fields"]
    )
    assert "dry_run_evidence_items[1].dry_run_evidence_id" in (
        result["missing_or_invalid_fields"]
    )
    assert "required_dry_run_evidence_ids.dry-run-evidence-002" in (
        result["missing_or_invalid_fields"]
    )
    assert result["dry_run_evidence_item_violations"] != ()
    for violation in result["dry_run_evidence_item_violations"]:
        assert tuple(violation.keys()) == (
            DRY_RUN_EVIDENCE_ITEM_VIOLATION_KEYS
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
    assert "public_url" in payload_keys
    assert result["source"]["public_url"] is None
    assert result["local_noop_e2e_contract"]["public_url"] is None
    assert "no_raw_url" not in payload_keys
    assert "no_public_url_behavior" not in payload_keys
    assert "buildable_not_publish_allowed" not in payload_keys
