"""Tests for the pure local noop runner envelope builder."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import (  # noqa: E402
    local_noop_runner_envelope_builder as builder,
)


RESULT_KEYS = (
    "buildable",
    "reason_code",
    "reason",
    "source",
    "local_noop_runner_envelope",
    "runner_envelope_violations",
    "missing_or_invalid_fields",
    "runner_envelope_evidence_item_violations",
    "invariant_refs",
)

SOURCE_KEYS = (
    "mode",
    "expected_terminal_status",
    "gate_input_ref",
    "gate_input_buildable_marker",
    "local_noop_run_assembly_ref",
    "local_noop_run_assembly_buildable_marker",
    "local_noop_e2e_contract_ref",
    "local_noop_e2e_contract_buildable_marker",
    "local_noop_runner_result_ref",
    "local_noop_runner_result_buildable_marker",
    "run_ledger_draft_ref",
    "run_ledger_draft_buildable_marker",
    "local_noop_cli_contract_ref",
    "local_noop_cli_contract_buildable_marker",
    "local_noop_runner_skeleton_ref",
    "local_noop_runner_skeleton_buildable_marker",
    "public_url",
    "public_url_created",
    "source_of_truth",
)

LOCAL_NOOP_RUNNER_ENVELOPE_KEYS = (
    "run_id",
    "local_noop_runner_envelope_id",
    "envelope_kind",
    "mode",
    "expected_terminal_status",
    "gate_input_ref",
    "gate_input_buildable_marker",
    "local_noop_run_assembly_ref",
    "local_noop_run_assembly_buildable_marker",
    "local_noop_e2e_contract_ref",
    "local_noop_e2e_contract_buildable_marker",
    "local_noop_runner_result_ref",
    "local_noop_runner_result_buildable_marker",
    "run_ledger_draft_ref",
    "run_ledger_draft_buildable_marker",
    "local_noop_cli_contract_ref",
    "local_noop_cli_contract_buildable_marker",
    "local_noop_runner_skeleton_ref",
    "local_noop_runner_skeleton_buildable_marker",
    "public_url",
    "public_url_created",
    "runner_envelope_evidence_items",
    "required_runner_envelope_evidence_ids",
    "missing_runner_envelope_evidence_ids",
    "blocking_runner_envelope_evidence_ids",
    "created_at",
    "timestamp_policy",
    "source_of_truth",
    "notes",
)

RUNNER_ENVELOPE_EVIDENCE_ITEM_KEYS = (
    "runner_envelope_evidence_id",
    "runner_envelope_evidence_role",
    "artifact_ref",
    "artifact_kind",
    "evidence_status",
    "producer_ref",
    "evidence_refs",
    "notes",
)

RUNNER_ENVELOPE_EVIDENCE_ITEM_VIOLATION_KEYS = (
    "runner_envelope_evidence_item_index",
    "runner_envelope_evidence_id",
    "reason_code",
    "field",
)

REASON_CODES = (
    "LOCAL_NOOP_RUNNER_ENVELOPE_BUILDABLE",
    "RUN_ID_MISSING",
    "LOCAL_NOOP_RUNNER_ENVELOPE_ID_MISSING",
    "ENVELOPE_KIND_NOT_LOCAL_NOOP_RUNNER_ENVELOPE",
    "MODE_NOT_NOOP",
    "PASS_PUBLISHED_FORBIDDEN",
    "EXPECTED_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
    "GATE_INPUT_REF_MISSING",
    "GATE_INPUT_BUILDABLE_MARKER_NOT_TRUE",
    "LOCAL_NOOP_RUN_ASSEMBLY_REF_MISSING",
    "LOCAL_NOOP_RUN_ASSEMBLY_BUILDABLE_MARKER_NOT_TRUE",
    "LOCAL_NOOP_E2E_CONTRACT_REF_MISSING",
    "LOCAL_NOOP_E2E_CONTRACT_BUILDABLE_MARKER_NOT_TRUE",
    "LOCAL_NOOP_RUNNER_RESULT_REF_MISSING",
    "LOCAL_NOOP_RUNNER_RESULT_BUILDABLE_MARKER_NOT_TRUE",
    "RUN_LEDGER_DRAFT_REF_MISSING",
    "RUN_LEDGER_DRAFT_BUILDABLE_MARKER_NOT_TRUE",
    "LOCAL_NOOP_CLI_CONTRACT_REF_MISSING",
    "LOCAL_NOOP_CLI_CONTRACT_BUILDABLE_MARKER_NOT_TRUE",
    "LOCAL_NOOP_RUNNER_SKELETON_REF_MISSING",
    "LOCAL_NOOP_RUNNER_SKELETON_BUILDABLE_MARKER_NOT_TRUE",
    "PUBLIC_URL_IS_NULL_NOT_TRUE",
    "PUBLIC_URL_CREATED_NOT_FALSE",
    "RUNNER_ENVELOPE_EVIDENCE_ITEMS_MISSING",
    "REQUIRED_RUNNER_ENVELOPE_EVIDENCE_IDS_MISSING",
    "MISSING_RUNNER_ENVELOPE_EVIDENCE_IDS_DECLARED",
    "BLOCKING_RUNNER_ENVELOPE_EVIDENCE_ID_UNKNOWN",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "RUNNER_ENVELOPE_EVIDENCE_ITEM_NOT_DICT",
    "RUNNER_ENVELOPE_EVIDENCE_ITEM_KEYS_INVALID",
    "RUNNER_ENVELOPE_EVIDENCE_ID_MISSING",
    "RUNNER_ENVELOPE_EVIDENCE_ROLE_MISSING",
    "RUNNER_ENVELOPE_EVIDENCE_ARTIFACT_REF_MISSING",
    "RUNNER_ENVELOPE_EVIDENCE_ARTIFACT_KIND_MISSING",
    "RUNNER_ENVELOPE_EVIDENCE_STATUS_MISSING",
    "RUNNER_ENVELOPE_EVIDENCE_PRODUCER_REF_MISSING",
    "RUNNER_ENVELOPE_EVIDENCE_REFS_MISSING",
    "RUNNER_ENVELOPE_EVIDENCE_ID_DUPLICATE",
    "RUNNER_ENVELOPE_EVIDENCE_ID_NOT_REQUIRED",
    "REQUIRED_RUNNER_ENVELOPE_EVIDENCE_MISSING",
    "RUNNER_ENVELOPE_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT",
)

REASON_PRIORITY = (
    "RUN_ID_MISSING",
    "LOCAL_NOOP_RUNNER_ENVELOPE_ID_MISSING",
    "ENVELOPE_KIND_NOT_LOCAL_NOOP_RUNNER_ENVELOPE",
    "MODE_NOT_NOOP",
    "PASS_PUBLISHED_FORBIDDEN",
    "EXPECTED_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
    "GATE_INPUT_REF_MISSING",
    "GATE_INPUT_BUILDABLE_MARKER_NOT_TRUE",
    "LOCAL_NOOP_RUN_ASSEMBLY_REF_MISSING",
    "LOCAL_NOOP_RUN_ASSEMBLY_BUILDABLE_MARKER_NOT_TRUE",
    "LOCAL_NOOP_E2E_CONTRACT_REF_MISSING",
    "LOCAL_NOOP_E2E_CONTRACT_BUILDABLE_MARKER_NOT_TRUE",
    "LOCAL_NOOP_RUNNER_RESULT_REF_MISSING",
    "LOCAL_NOOP_RUNNER_RESULT_BUILDABLE_MARKER_NOT_TRUE",
    "RUN_LEDGER_DRAFT_REF_MISSING",
    "RUN_LEDGER_DRAFT_BUILDABLE_MARKER_NOT_TRUE",
    "LOCAL_NOOP_CLI_CONTRACT_REF_MISSING",
    "LOCAL_NOOP_CLI_CONTRACT_BUILDABLE_MARKER_NOT_TRUE",
    "LOCAL_NOOP_RUNNER_SKELETON_REF_MISSING",
    "LOCAL_NOOP_RUNNER_SKELETON_BUILDABLE_MARKER_NOT_TRUE",
    "PUBLIC_URL_IS_NULL_NOT_TRUE",
    "PUBLIC_URL_CREATED_NOT_FALSE",
    "RUNNER_ENVELOPE_EVIDENCE_ITEMS_MISSING",
    "REQUIRED_RUNNER_ENVELOPE_EVIDENCE_IDS_MISSING",
    "MISSING_RUNNER_ENVELOPE_EVIDENCE_IDS_DECLARED",
    "BLOCKING_RUNNER_ENVELOPE_EVIDENCE_ID_UNKNOWN",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "RUNNER_ENVELOPE_EVIDENCE_ITEM_NOT_DICT",
    "RUNNER_ENVELOPE_EVIDENCE_ITEM_KEYS_INVALID",
    "RUNNER_ENVELOPE_EVIDENCE_ID_MISSING",
    "RUNNER_ENVELOPE_EVIDENCE_ROLE_MISSING",
    "RUNNER_ENVELOPE_EVIDENCE_ARTIFACT_REF_MISSING",
    "RUNNER_ENVELOPE_EVIDENCE_ARTIFACT_KIND_MISSING",
    "RUNNER_ENVELOPE_EVIDENCE_STATUS_MISSING",
    "RUNNER_ENVELOPE_EVIDENCE_PRODUCER_REF_MISSING",
    "RUNNER_ENVELOPE_EVIDENCE_REFS_MISSING",
    "RUNNER_ENVELOPE_EVIDENCE_ID_DUPLICATE",
    "RUNNER_ENVELOPE_EVIDENCE_ID_NOT_REQUIRED",
    "REQUIRED_RUNNER_ENVELOPE_EVIDENCE_MISSING",
    "RUNNER_ENVELOPE_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT",
    "LOCAL_NOOP_RUNNER_ENVELOPE_BUILDABLE",
)

FORBIDDEN_RUNNER_ENVELOPE_EVIDENCE_ITEM_FIELDS = (
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
    "local_noop_cli_contract_content",
    "local_noop_runner_skeleton_content",
    "local_noop_runner_skeleton_read",
    "local_noop_runner_envelope_content",
    "run_ledger_draft_content",
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
    "runner_envelope_payload",
    "raw_runner_envelope_payload",
    "runner_payload",
    "raw_runner_payload",
    "runner_result_payload",
    "raw_runner_result_payload",
    "e2e_payload",
    "raw_e2e_payload",
    "dry_run_payload",
    "raw_dry_run_payload",
    "completion_payload",
    "raw_completion_payload",
    "gate_execution_result",
    "policy_execution_result",
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
    "local_noop_runner_envelope_path",
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
    "rss_fetch_result",
    "artifact_reader_result",
    "validator_execution_result",
    "audit_execution_result",
    "judge_execution_result",
    "eval_result",
    "publish_result",
    "notification_result",
    "ledger_write_result",
    "transition_result",
    "runtime_result",
    "runtime_execution_result",
    "noop_completion_result",
    "dry_run_execution_result",
    "e2e_execution_result",
    "runner_execution_result",
    "cli_execution_result",
    "command_execution_result",
    "subprocess_execution_result",
    "command",
    "raw_command",
    "shell_command",
    "cli_command",
    "argv",
    "args",
    "parsed_args",
    "argparse_namespace",
    "click_context",
    "typer_app",
    "console_script",
    "entrypoint",
    "entry_point",
    "package_entry_point",
    "subprocess_result",
    "process_result",
    "exit_code",
    "stdout",
    "stderr",
    "command_output",
    "command_result",
    "should_fetch",
    "should_read_reader",
    "should_call_web",
    "should_call_github",
    "should_call_rss",
    "should_call_notion",
    "should_call_llm",
    "should_run_policy",
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
    "should_execute_runtime",
    "should_execute_cli",
    "should_execute_command",
    "should_run_command",
    "should_parse_args",
    "should_call_subprocess",
    "reader_read",
    "gate_input_read",
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
    "runtime_executed",
    "cli_executed",
    "command_executed",
    "subprocess_executed",
    "argparse_executed",
    "click_executed",
    "typer_executed",
    "manual_execution_result",
    "manual_command_result",
    "published",
    "notified",
    "ledger_written",
    "public_url_created_executed",
    "run_ledger_yaml",
    "run_ledger_yaml_read",
    "run_ledger_yaml_write",
    "run_ledger_content",
    "run_ledger_entry",
    "run_ledger_write_result",
    "ledger_file_path",
    "ledger_path",
    "ledger_content",
    "raw_ledger_content",
    "ledger_writer_result",
    "should_write_run_ledger",
    "run_ledger_written",
    "ledger_appended",
    "ledger_updated",
    "runnable",
    "executable",
    "invocation_ready",
    "assembled",
)

FORBIDDEN_PSEUDO_REASON_CODES = (
    "RUNNER_EXECUTION_FORBIDDEN",
    "RUNTIME_EXECUTION_FORBIDDEN",
    "CLI_EXECUTION_FORBIDDEN",
    "MANUAL_EXECUTION_FORBIDDEN",
    "ARGUMENT_PARSING_FORBIDDEN",
    "COMMAND_EXECUTION_FORBIDDEN",
    "SUBPROCESS_EXECUTION_FORBIDDEN",
    "READER_READ_FORBIDDEN",
    "WEB_FETCH_FORBIDDEN",
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
    "artifacts",
    "states",
    "gates",
    "run_ledger_entry_builder",
    "run_ledger_draft_builder",
    "local_noop_runner_result_builder",
    "local_noop_cli_contract_builder",
    "local_noop_runner_skeleton_builder",
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
    "os",
    "pathlib",
    "datetime",
    "hashlib",
    "logging",
    "subprocess",
    "argparse",
    "click",
    "typer",
    "requests",
    "urllib",
    "httpx",
    "feedparser",
    "jinja2",
    "open",
)

FORBIDDEN_SUCCESS_NAMES = (
    "runnable",
    "executable",
    "invocation_ready",
    "assembled",
)

REQUIRED_INVARIANT_REFS = (
    "local_noop_runner_envelope_builder_only",
    "builder_not_runner_executor",
    "builder_not_runtime_executor",
    "builder_not_cli_executor",
    "builder_not_manual_executor",
    "builder_not_argparse_parser",
    "builder_not_click_app",
    "builder_not_typer_app",
    "builder_not_console_script",
    "builder_not_subprocess_runner",
    "builder_not_command_runner",
    "builder_not_run_ledger_writer",
    "builder_not_run_ledger_entry_builder",
    "builder_not_run_ledger_draft_builder",
    "builder_not_local_noop_runner_result_builder",
    "builder_not_local_noop_cli_contract_builder",
    "builder_not_local_noop_runner_skeleton_builder",
    "builder_not_local_noop_e2e_contract_builder",
    "builder_not_local_noop_run_assembly_builder",
    "builder_not_gate_input_assembly_builder",
    "builder_not_noop_completion_policy",
    "builder_not_transition_guard",
    "builder_not_gate_decision_mapper",
    "builder_not_reader_reader",
    "builder_not_training_report_reader",
    "builder_not_validator_result_reader",
    "builder_not_rubric_review_reader",
    "builder_not_audit_review_reader",
    "builder_not_gate_input_reader",
    "builder_not_local_noop_run_reader",
    "builder_not_local_noop_e2e_contract_reader",
    "builder_not_local_noop_runner_result_reader",
    "builder_not_local_noop_cli_contract_reader",
    "builder_not_local_noop_runner_skeleton_reader",
    "builder_not_run_ledger_draft_reader",
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
    "runner_envelope_evidence_items_are_caller_supplied",
    "runner_envelope_evidence_status_is_caller_supplied",
    "all_upstream_refs_are_caller_supplied",
    "all_upstream_markers_are_caller_supplied",
    "upstream_refs_opaque",
    "artifact_refs_opaque",
    "evidence_refs_opaque",
    "local_noop_runner_envelope_governance_evidence_bundle",
    "local_noop_runner_envelope_not_runner_execution",
    "local_noop_runner_envelope_not_runtime_execution",
    "local_noop_runner_envelope_not_cli_execution",
    "local_noop_runner_envelope_not_manual_execution",
    "local_noop_runner_envelope_not_argument_parsing",
    "local_noop_runner_envelope_not_console_script",
    "local_noop_runner_envelope_not_command_execution",
    "local_noop_runner_envelope_not_subprocess_execution",
    "local_noop_runner_envelope_not_ledger_write",
    "local_noop_runner_envelope_not_run_ledger_yaml",
    "local_noop_runner_envelope_not_state_transition",
    "local_noop_runner_envelope_not_gate_decision",
    "local_noop_runner_envelope_not_publish_artifact",
    "local_noop_runner_envelope_not_public_candidate",
    "mode_noop_required",
    "public_url_must_be_null",
    "public_url_created_must_be_false",
    "expected_terminal_status_must_be_noop_completed",
    "noop_completed_not_pass_published",
    "pass_published_forbidden",
    "mode_noop_not_publish",
    "buildable_not_runnable",
    "buildable_not_executable",
    "upstream_buildable_markers_not_quality_pass",
    "upstream_buildable_markers_not_gate_pass",
    "upstream_buildable_markers_not_publish_allowed",
    "runner_envelope_evidence_status_not_quality_pass",
    "runner_envelope_evidence_status_not_gate_pass",
    "runner_envelope_evidence_status_not_publish_allowed",
    "buildable_not_runner_executed",
    "buildable_not_runtime_executed",
    "buildable_not_cli_executed",
    "buildable_not_manual_executed",
    "buildable_not_command_executed",
    "buildable_not_argparse_executed",
    "buildable_not_subprocess_executed",
    "buildable_not_ledger_written",
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
    "blocking_runner_envelope_evidence_ids_are_evidence_only",
    "blocking_runner_envelope_evidence_ids_do_not_execute_gate",
    "blocking_runner_envelope_evidence_ids_do_not_execute_noop_completion",
    "blocking_runner_envelope_evidence_ids_do_not_execute_dry_run",
    "blocking_runner_envelope_evidence_ids_do_not_execute_e2e",
    "blocking_runner_envelope_evidence_ids_do_not_execute_runner",
    "blocking_runner_envelope_evidence_ids_do_not_write_ledger",
    "no_reader_read",
    "no_training_report_read",
    "no_validator_result_read",
    "no_rubric_review_read",
    "no_audit_review_read",
    "no_gate_input_read",
    "no_local_noop_run_read",
    "no_local_noop_e2e_contract_read",
    "no_local_noop_runner_result_read",
    "no_local_noop_cli_contract_read",
    "no_local_noop_runner_skeleton_read",
    "no_run_ledger_draft_read",
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
    "no_cli_execution",
    "no_manual_execution",
    "no_argument_parsing",
    "no_console_script",
    "no_command_execution",
    "no_subprocess_execution",
    "no_publish",
    "no_notification",
    "no_ledger_write",
    "no_run_ledger_yaml_write",
    "no_public_url_behavior",
    "no_quality_pass_no_public_url",
)

MISSING_RUNNER_ENVELOPE_EVIDENCE_ITEM_KEY_EXPECTATIONS = (
    ("runner_envelope_evidence_id", "RUNNER_ENVELOPE_EVIDENCE_ID_MISSING"),
    ("runner_envelope_evidence_role", "RUNNER_ENVELOPE_EVIDENCE_ROLE_MISSING"),
    ("artifact_ref", "RUNNER_ENVELOPE_EVIDENCE_ARTIFACT_REF_MISSING"),
    ("artifact_kind", "RUNNER_ENVELOPE_EVIDENCE_ARTIFACT_KIND_MISSING"),
    ("evidence_status", "RUNNER_ENVELOPE_EVIDENCE_STATUS_MISSING"),
    ("producer_ref", "RUNNER_ENVELOPE_EVIDENCE_PRODUCER_REF_MISSING"),
    ("evidence_refs", "RUNNER_ENVELOPE_EVIDENCE_REFS_MISSING"),
)


def _runner_envelope_evidence_item(**overrides):
    values = {
        "runner_envelope_evidence_id": "runner-envelope-evidence-001",
        "runner_envelope_evidence_role": "local_noop_runner_skeleton",
        "artifact_ref": "local-noop-runner-skeleton-001",
        "artifact_kind": "local_noop_runner_skeleton",
        "evidence_status": "passed",
        "producer_ref": "caller-supplied-runner-envelope",
        "evidence_refs": ("local-noop-runner-skeleton-001#noop-terminal",),
        "notes": ("caller-supplied-evidence-only",),
    }
    values.update(overrides)
    return values


def _valid_values():
    return {
        "run_id": "run-001",
        "local_noop_runner_envelope_id": "local-noop-runner-envelope-001",
        "envelope_kind": "local_noop_runner_envelope",
        "mode": "noop",
        "expected_terminal_status": "NOOP_COMPLETED",
        "gate_input_ref": "gate-input-001",
        "gate_input_buildable_marker": True,
        "local_noop_run_assembly_ref": "local-noop-run-assembly-001",
        "local_noop_run_assembly_buildable_marker": True,
        "local_noop_e2e_contract_ref": "local-noop-e2e-contract-001",
        "local_noop_e2e_contract_buildable_marker": True,
        "local_noop_runner_result_ref": "local-noop-runner-result-001",
        "local_noop_runner_result_buildable_marker": True,
        "run_ledger_draft_ref": "run-ledger-draft-001",
        "run_ledger_draft_buildable_marker": True,
        "local_noop_cli_contract_ref": "local-noop-cli-contract-001",
        "local_noop_cli_contract_buildable_marker": True,
        "local_noop_runner_skeleton_ref": "local-noop-runner-skeleton-001",
        "local_noop_runner_skeleton_buildable_marker": True,
        "public_url_created": False,
        "public_url_is_null": True,
        "runner_envelope_evidence_items": (_runner_envelope_evidence_item(),),
        "required_runner_envelope_evidence_ids": (
            "runner-envelope-evidence-001",
        ),
        "missing_runner_envelope_evidence_ids": (),
        "blocking_runner_envelope_evidence_ids": (),
        "created_at": "caller-supplied-created-at",
        "timestamp_policy": "caller_supplied_no_datetime_parsing",
        "source_of_truth": ("p2d-39",),
        "notes": ("structured-only",),
    }


def _explain(**overrides):
    values = _valid_values()
    values.update(overrides)
    return builder.explain_local_noop_runner_envelope_build(**values)


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
    assert builder.LOCAL_NOOP_RUNNER_ENVELOPE_BUILD_REASON_CODES == (
        REASON_CODES
    )
    assert builder.REASON_PRIORITY == REASON_PRIORITY


def test_valid_runner_envelope_is_buildable_with_exact_shapes():
    result = _explain()

    assert result["buildable"] is True
    assert result["reason_code"] == "LOCAL_NOOP_RUNNER_ENVELOPE_BUILDABLE"
    assert result["runner_envelope_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()
    assert result["runner_envelope_evidence_item_violations"] == ()
    assert tuple(result.keys()) == RESULT_KEYS
    assert tuple(result["source"].keys()) == SOURCE_KEYS
    assert tuple(result["local_noop_runner_envelope"].keys()) == (
        LOCAL_NOOP_RUNNER_ENVELOPE_KEYS
    )
    assert tuple(
        result["local_noop_runner_envelope"][
            "runner_envelope_evidence_items"
        ][0].keys()
    ) == RUNNER_ENVELOPE_EVIDENCE_ITEM_KEYS
    assert result["source"]["public_url"] is None
    assert result["local_noop_runner_envelope"]["public_url"] is None
    assert result["source"]["public_url_created"] is False
    assert result["local_noop_runner_envelope"]["public_url_created"] is False
    assert "public_url_is_null" not in result
    assert "public_url_is_null" not in result["source"]
    assert "public_url_is_null" not in result["local_noop_runner_envelope"]


def test_public_api_is_keyword_only_and_bool_wrapper_matches_explain():
    expected_kwonly = len(_valid_values())

    assert (
        builder.explain_local_noop_runner_envelope_build.__code__.co_argcount
        == 0
    )
    assert (
        builder.explain_local_noop_runner_envelope_build.__code__
        .co_kwonlyargcount
        == expected_kwonly
    )
    assert (
        builder.is_local_noop_runner_envelope_buildable.__code__.co_argcount
        == 0
    )
    assert (
        builder.is_local_noop_runner_envelope_buildable.__code__
        .co_kwonlyargcount
        == expected_kwonly
    )

    cases = (
        _valid_values(),
        {**_valid_values(), "run_id": ""},
        {**_valid_values(), "expected_terminal_status": "PASS_PUBLISHED"},
        {**_valid_values(), "public_url_is_null": False},
    )
    for values in cases:
        explanation = builder.explain_local_noop_runner_envelope_build(**values)
        assert (
            builder.is_local_noop_runner_envelope_buildable(**values)
            is explanation["buildable"]
        )


def test_required_lockin_markers_block_when_invalid():
    cases = (
        (
            {"envelope_kind": "local_noop_runner"},
            "ENVELOPE_KIND_NOT_LOCAL_NOOP_RUNNER_ENVELOPE",
            "envelope_kind",
        ),
        ({"mode": "real"}, "MODE_NOT_NOOP", "mode"),
        (
            {"expected_terminal_status": "DONE"},
            "EXPECTED_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
            "expected_terminal_status",
        ),
        (
            {"expected_terminal_status": "PASS_PUBLISHED"},
            "PASS_PUBLISHED_FORBIDDEN",
            "expected_terminal_status",
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
            {"local_noop_run_assembly_buildable_marker": False},
            "LOCAL_NOOP_RUN_ASSEMBLY_BUILDABLE_MARKER_NOT_TRUE",
            "local_noop_run_assembly_buildable_marker",
        ),
        (
            {"local_noop_e2e_contract_buildable_marker": False},
            "LOCAL_NOOP_E2E_CONTRACT_BUILDABLE_MARKER_NOT_TRUE",
            "local_noop_e2e_contract_buildable_marker",
        ),
        (
            {"local_noop_runner_result_buildable_marker": False},
            "LOCAL_NOOP_RUNNER_RESULT_BUILDABLE_MARKER_NOT_TRUE",
            "local_noop_runner_result_buildable_marker",
        ),
        (
            {"run_ledger_draft_buildable_marker": False},
            "RUN_LEDGER_DRAFT_BUILDABLE_MARKER_NOT_TRUE",
            "run_ledger_draft_buildable_marker",
        ),
        (
            {"local_noop_cli_contract_buildable_marker": False},
            "LOCAL_NOOP_CLI_CONTRACT_BUILDABLE_MARKER_NOT_TRUE",
            "local_noop_cli_contract_buildable_marker",
        ),
        (
            {"local_noop_runner_skeleton_buildable_marker": False},
            "LOCAL_NOOP_RUNNER_SKELETON_BUILDABLE_MARKER_NOT_TRUE",
            "local_noop_runner_skeleton_buildable_marker",
        ),
        (
            {"local_noop_runner_skeleton_buildable_marker": 1},
            "LOCAL_NOOP_RUNNER_SKELETON_BUILDABLE_MARKER_NOT_TRUE",
            "local_noop_runner_skeleton_buildable_marker",
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
        assert reason_code in result["runner_envelope_violations"]
        assert field in result["missing_or_invalid_fields"]


def test_pass_published_status_is_blocked_and_suppressed_from_payload():
    result = _explain(expected_terminal_status="PASS_PUBLISHED")

    assert result["reason_code"] == "PASS_PUBLISHED_FORBIDDEN"
    assert "EXPECTED_TERMINAL_STATUS_NOT_NOOP_COMPLETED" in (
        result["runner_envelope_violations"]
    )
    assert result["source"]["expected_terminal_status"] == ""
    assert result["local_noop_runner_envelope"]["expected_terminal_status"] == ""


def test_public_url_created_is_blocked_and_suppressed_from_payload():
    result = _explain(public_url_created=True)

    assert result["buildable"] is False
    assert "PUBLIC_URL_CREATED_NOT_FALSE" in (
        result["runner_envelope_violations"]
    )
    assert result["source"]["public_url_created"] is False
    assert result["local_noop_runner_envelope"]["public_url_created"] is False


def test_each_upstream_ref_is_required_and_opaque():
    cases = (
        ("gate_input_ref", "GATE_INPUT_REF_MISSING"),
        ("local_noop_run_assembly_ref", "LOCAL_NOOP_RUN_ASSEMBLY_REF_MISSING"),
        ("local_noop_e2e_contract_ref", "LOCAL_NOOP_E2E_CONTRACT_REF_MISSING"),
        ("local_noop_runner_result_ref", "LOCAL_NOOP_RUNNER_RESULT_REF_MISSING"),
        ("run_ledger_draft_ref", "RUN_LEDGER_DRAFT_REF_MISSING"),
        ("local_noop_cli_contract_ref", "LOCAL_NOOP_CLI_CONTRACT_REF_MISSING"),
        (
            "local_noop_runner_skeleton_ref",
            "LOCAL_NOOP_RUNNER_SKELETON_REF_MISSING",
        ),
    )

    for field, reason_code in cases:
        result = _explain(**{field: ""})

        assert result["buildable"] is False
        assert reason_code in result["runner_envelope_violations"]
        assert field in result["missing_or_invalid_fields"]

    opaque = _explain(
        gate_input_ref="opaque-gate-input",
        local_noop_run_assembly_ref="opaque-run-assembly",
        local_noop_e2e_contract_ref="opaque-e2e-contract",
        local_noop_runner_result_ref="opaque-runner-result",
        run_ledger_draft_ref="opaque-ledger-draft",
        local_noop_cli_contract_ref="opaque-cli-contract",
        local_noop_runner_skeleton_ref="opaque-runner-skeleton",
    )

    assert opaque["buildable"] is True
    assert opaque["source"]["gate_input_ref"] == "opaque-gate-input"
    assert opaque["source"]["local_noop_runner_skeleton_ref"] == (
        "opaque-runner-skeleton"
    )


def test_refs_status_and_evidence_refs_are_opaque():
    result = _explain(
        runner_envelope_evidence_items=(
            _runner_envelope_evidence_item(
                evidence_status="failed",
                evidence_refs=("opaque-evidence-ref",),
            ),
        ),
    )

    assert result["buildable"] is True
    assert (
        result["local_noop_runner_envelope"][
            "runner_envelope_evidence_items"
        ][0]["evidence_status"]
        == "failed"
    )
    assert (
        result["local_noop_runner_envelope"][
            "runner_envelope_evidence_items"
        ][0]["evidence_refs"]
        == ("opaque-evidence-ref",)
    )


def test_known_blocking_runner_envelope_evidence_ids_still_buildable():
    result = _explain(
        blocking_runner_envelope_evidence_ids=(
            "runner-envelope-evidence-001",
        ),
        runner_envelope_evidence_items=(
            _runner_envelope_evidence_item(evidence_status="failed"),
        ),
    )

    assert result["buildable"] is True
    assert result["local_noop_runner_envelope"][
        "blocking_runner_envelope_evidence_ids"
    ] == ("runner-envelope-evidence-001",)


def test_unknown_blank_or_non_tuple_blocking_ids_block_buildability():
    cases = (
        ("missing-runner-envelope-evidence",),
        ("",),
        (1,),
        ["runner-envelope-evidence-001"],
    )

    for blocking_runner_envelope_evidence_ids in cases:
        result = _explain(
            blocking_runner_envelope_evidence_ids=(
                blocking_runner_envelope_evidence_ids
            )
        )

        assert result["buildable"] is False
        assert "BLOCKING_RUNNER_ENVELOPE_EVIDENCE_ID_UNKNOWN" in (
            result["runner_envelope_violations"]
        )
        assert "blocking_runner_envelope_evidence_ids" in (
            result["missing_or_invalid_fields"]
        )


def test_required_top_level_field_violations_are_collected():
    cases = (
        ({"run_id": ""}, "RUN_ID_MISSING", "run_id"),
        (
            {"local_noop_runner_envelope_id": ""},
            "LOCAL_NOOP_RUNNER_ENVELOPE_ID_MISSING",
            "local_noop_runner_envelope_id",
        ),
        (
            {"runner_envelope_evidence_items": ()},
            "RUNNER_ENVELOPE_EVIDENCE_ITEMS_MISSING",
            "runner_envelope_evidence_items",
        ),
        (
            {"runner_envelope_evidence_items": []},
            "RUNNER_ENVELOPE_EVIDENCE_ITEMS_MISSING",
            "runner_envelope_evidence_items",
        ),
        (
            {"required_runner_envelope_evidence_ids": ()},
            "REQUIRED_RUNNER_ENVELOPE_EVIDENCE_IDS_MISSING",
            "required_runner_envelope_evidence_ids",
        ),
        (
            {"required_runner_envelope_evidence_ids": ("",)},
            "REQUIRED_RUNNER_ENVELOPE_EVIDENCE_IDS_MISSING",
            "required_runner_envelope_evidence_ids",
        ),
        (
            {"required_runner_envelope_evidence_ids": ["id"]},
            "REQUIRED_RUNNER_ENVELOPE_EVIDENCE_IDS_MISSING",
            "required_runner_envelope_evidence_ids",
        ),
        (
            {"missing_runner_envelope_evidence_ids": ("id-002",)},
            "MISSING_RUNNER_ENVELOPE_EVIDENCE_IDS_DECLARED",
            "missing_runner_envelope_evidence_ids",
        ),
        (
            {"missing_runner_envelope_evidence_ids": ["id-002"]},
            "MISSING_RUNNER_ENVELOPE_EVIDENCE_IDS_DECLARED",
            "missing_runner_envelope_evidence_ids",
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
            {"source_of_truth": ["p2d-39"]},
            "SOURCE_OF_TRUTH_MISSING",
            "source_of_truth",
        ),
    )

    for overrides, reason_code, field in cases:
        result = _explain(**overrides)

        assert result["buildable"] is False
        assert reason_code in result["runner_envelope_violations"]
        assert field in result["missing_or_invalid_fields"]


def test_runner_envelope_evidence_id_uniqueness_required_and_presence():
    duplicate = _explain(
        runner_envelope_evidence_items=(
            _runner_envelope_evidence_item(),
            _runner_envelope_evidence_item(),
        )
    )
    not_required = _explain(
        runner_envelope_evidence_items=(
            _runner_envelope_evidence_item(
                runner_envelope_evidence_id="runner-envelope-evidence-002"
            ),
        ),
        required_runner_envelope_evidence_ids=("runner-envelope-evidence-001",),
    )
    required_missing = _explain(
        required_runner_envelope_evidence_ids=(
            "runner-envelope-evidence-001",
            "runner-envelope-evidence-002",
        )
    )

    assert "RUNNER_ENVELOPE_EVIDENCE_ID_DUPLICATE" in (
        duplicate["runner_envelope_violations"]
    )
    assert "runner_envelope_evidence_items[1].runner_envelope_evidence_id" in (
        duplicate["missing_or_invalid_fields"]
    )
    assert "RUNNER_ENVELOPE_EVIDENCE_ID_NOT_REQUIRED" in (
        not_required["runner_envelope_violations"]
    )
    assert "runner_envelope_evidence_items[0].runner_envelope_evidence_id" in (
        not_required["missing_or_invalid_fields"]
    )
    assert "REQUIRED_RUNNER_ENVELOPE_EVIDENCE_MISSING" in (
        required_missing["runner_envelope_violations"]
    )
    assert "required_runner_envelope_evidence_ids.runner-envelope-evidence-002" in (
        required_missing["missing_or_invalid_fields"]
    )


def test_runner_envelope_evidence_item_fields_and_missing_keys_reported():
    string_field_cases = (
        (
            "runner_envelope_evidence_id",
            "",
            "RUNNER_ENVELOPE_EVIDENCE_ID_MISSING",
        ),
        (
            "runner_envelope_evidence_role",
            "",
            "RUNNER_ENVELOPE_EVIDENCE_ROLE_MISSING",
        ),
        ("artifact_ref", "", "RUNNER_ENVELOPE_EVIDENCE_ARTIFACT_REF_MISSING"),
        ("artifact_kind", "", "RUNNER_ENVELOPE_EVIDENCE_ARTIFACT_KIND_MISSING"),
        ("evidence_status", "", "RUNNER_ENVELOPE_EVIDENCE_STATUS_MISSING"),
        ("producer_ref", "", "RUNNER_ENVELOPE_EVIDENCE_PRODUCER_REF_MISSING"),
        ("evidence_refs", (), "RUNNER_ENVELOPE_EVIDENCE_REFS_MISSING"),
        ("evidence_refs", ("",), "RUNNER_ENVELOPE_EVIDENCE_REFS_MISSING"),
        ("evidence_refs", ["ref"], "RUNNER_ENVELOPE_EVIDENCE_REFS_MISSING"),
    )

    for field, value, reason_code in string_field_cases:
        result = _explain(
            runner_envelope_evidence_items=(
                _runner_envelope_evidence_item(**{field: value}),
            )
        )

        assert result["buildable"] is False
        assert reason_code in result["runner_envelope_violations"]
        assert f"runner_envelope_evidence_items[0].{field}" in (
            result["missing_or_invalid_fields"]
        )
        assert tuple(
            result["runner_envelope_evidence_item_violations"][0].keys()
        ) == RUNNER_ENVELOPE_EVIDENCE_ITEM_VIOLATION_KEYS

    for missing_key, reason_code in (
        MISSING_RUNNER_ENVELOPE_EVIDENCE_ITEM_KEY_EXPECTATIONS
    ):
        runner_envelope_evidence_item = _runner_envelope_evidence_item()
        del runner_envelope_evidence_item[missing_key]
        result = _explain(
            runner_envelope_evidence_items=(runner_envelope_evidence_item,)
        )

        assert result["buildable"] is False
        assert "RUNNER_ENVELOPE_EVIDENCE_ITEM_KEYS_INVALID" in (
            result["runner_envelope_violations"]
        )
        assert reason_code in result["runner_envelope_violations"]
        assert f"runner_envelope_evidence_items[0].{missing_key}" in (
            result["missing_or_invalid_fields"]
        )
        assert "runner_envelope_evidence_items[0].keys" in (
            result["missing_or_invalid_fields"]
        )


def test_non_dict_runner_envelope_evidence_item_records_violation_shape():
    result = _explain(runner_envelope_evidence_items=("not-evidence",))

    assert result["buildable"] is False
    assert "RUNNER_ENVELOPE_EVIDENCE_ITEM_NOT_DICT" in (
        result["runner_envelope_violations"]
    )
    assert "runner_envelope_evidence_items[0]" in (
        result["missing_or_invalid_fields"]
    )
    assert tuple(result["runner_envelope_evidence_item_violations"][0].keys()) == (
        RUNNER_ENVELOPE_EVIDENCE_ITEM_VIOLATION_KEYS
    )
    assert result["local_noop_runner_envelope"][
        "runner_envelope_evidence_items"
    ][0] == {
        "runner_envelope_evidence_id": "",
        "runner_envelope_evidence_role": "",
        "artifact_ref": "",
        "artifact_kind": "",
        "evidence_status": "",
        "producer_ref": "",
        "evidence_refs": (),
        "notes": (),
    }


def test_forbidden_raw_execution_cli_url_publication_fields_are_suppressed():
    for field in FORBIDDEN_RUNNER_ENVELOPE_EVIDENCE_ITEM_FIELDS:
        result = _explain(
            runner_envelope_evidence_items=(
                _runner_envelope_evidence_item(**{field: "forbidden"}),
            )
        )

        assert result["buildable"] is False
        assert "RUNNER_ENVELOPE_EVIDENCE_ITEM_KEYS_INVALID" in (
            result["runner_envelope_violations"]
        )
        assert "RUNNER_ENVELOPE_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT" in (
            result["runner_envelope_violations"]
        )
        assert f"runner_envelope_evidence_items[0].{field}" in (
            result["missing_or_invalid_fields"]
        )
        assert field not in (
            result["local_noop_runner_envelope"][
                "runner_envelope_evidence_items"
            ][0]
        )
        assert tuple(
            result["runner_envelope_evidence_item_violations"][0].keys()
        ) == RUNNER_ENVELOPE_EVIDENCE_ITEM_VIOLATION_KEYS


def test_output_does_not_expose_public_url_is_null_or_extra_url_values():
    result = _explain()
    forbidden_url = _explain(
        runner_envelope_evidence_items=(
            _runner_envelope_evidence_item(public_url_value="https://example.test"),
        )
    )
    payload_keys = _payload_keys(result)
    forbidden_payload_keys = _payload_keys(forbidden_url)

    assert "public_url_is_null" not in payload_keys
    assert result["source"]["public_url"] is None
    assert result["local_noop_runner_envelope"]["public_url"] is None
    assert "public_url_value" not in forbidden_payload_keys
    assert forbidden_url["source"]["public_url"] is None
    assert forbidden_url["local_noop_runner_envelope"]["public_url"] is None


def test_no_runnable_executable_invocation_ready_assembled_success_names():
    result = _explain()
    payload_keys = _payload_keys(result)

    assert "buildable" in payload_keys
    for success_name in FORBIDDEN_SUCCESS_NAMES:
        assert success_name not in payload_keys


def test_reason_catalog_priority_and_forbidden_pseudo_reason_codes():
    assert builder.REASON_CODES == REASON_CODES
    assert builder.LOCAL_NOOP_RUNNER_ENVELOPE_BUILD_REASON_CODES == REASON_CODES
    assert builder.REASON_PRIORITY == REASON_PRIORITY

    for reason_code in FORBIDDEN_PSEUDO_REASON_CODES:
        assert reason_code not in builder.REASON_CODES
        assert reason_code not in builder.REASON_PRIORITY


def test_forbidden_module_namespace_and_io_names_are_absent():
    for module_name in FORBIDDEN_MODULE_NAMES:
        assert not hasattr(builder, module_name)


def test_all_violations_are_priority_ordered_and_details_present():
    first_item = _runner_envelope_evidence_item(
        runner_envelope_evidence_id="",
        runner_envelope_evidence_role="",
        artifact_ref="",
        artifact_kind="",
        evidence_status="",
        producer_ref="",
        evidence_refs=(),
        raw_artifact_content="raw",
    )
    second_item = _runner_envelope_evidence_item(
        runner_envelope_evidence_id="extra-evidence"
    )
    result = _explain(
        run_id="",
        local_noop_runner_envelope_id="",
        envelope_kind="wrong",
        mode="real",
        expected_terminal_status="PASS_PUBLISHED",
        gate_input_ref="",
        gate_input_buildable_marker=False,
        local_noop_run_assembly_ref="",
        local_noop_run_assembly_buildable_marker=False,
        local_noop_e2e_contract_ref="",
        local_noop_e2e_contract_buildable_marker=False,
        local_noop_runner_result_ref="",
        local_noop_runner_result_buildable_marker=False,
        run_ledger_draft_ref="",
        run_ledger_draft_buildable_marker=False,
        local_noop_cli_contract_ref="",
        local_noop_cli_contract_buildable_marker=False,
        local_noop_runner_skeleton_ref="",
        local_noop_runner_skeleton_buildable_marker=False,
        public_url_is_null=False,
        public_url_created=True,
        runner_envelope_evidence_items=(first_item, second_item),
        required_runner_envelope_evidence_ids=(
            "runner-envelope-evidence-001",
            "runner-envelope-evidence-002",
        ),
        missing_runner_envelope_evidence_ids=("runner-envelope-evidence-002",),
        blocking_runner_envelope_evidence_ids=("missing-block",),
        created_at="",
        timestamp_policy="",
        source_of_truth=(),
    )
    expected_order = tuple(
        reason_code
        for reason_code in REASON_PRIORITY
        if reason_code != "LOCAL_NOOP_RUNNER_ENVELOPE_BUILDABLE"
        and reason_code in result["runner_envelope_violations"]
    )

    assert result["runner_envelope_violations"] == expected_order
    assert result["reason_code"] == result["runner_envelope_violations"][0]
    assert "runner_envelope_evidence_items[0].raw_artifact_content" in (
        result["missing_or_invalid_fields"]
    )
    assert "runner_envelope_evidence_items[1].runner_envelope_evidence_id" in (
        result["missing_or_invalid_fields"]
    )
    assert (
        "required_runner_envelope_evidence_ids.runner-envelope-evidence-002"
        in result["missing_or_invalid_fields"]
    )
    assert result["runner_envelope_evidence_item_violations"] != ()
    for violation in result["runner_envelope_evidence_item_violations"]:
        assert tuple(violation.keys()) == (
            RUNNER_ENVELOPE_EVIDENCE_ITEM_VIOLATION_KEYS
        )


def test_invariant_refs_capture_governance_and_no_execution_boundaries():
    result = _explain()

    assert result["invariant_refs"] == REQUIRED_INVARIANT_REFS


def test_payload_key_traversal_skips_invariants_instead_of_blanket_scans():
    result = _explain()
    payload_keys = _payload_keys(result)

    assert "no_raw_url" in result["invariant_refs"]
    assert "no_public_url_behavior" in result["invariant_refs"]
    assert "buildable_not_runnable" in result["invariant_refs"]
    assert "buildable_not_executable" in result["invariant_refs"]
    assert "local_noop_runner_envelope_not_runner_execution" in (
        result["invariant_refs"]
    )
    assert "local_noop_runner_envelope_not_runtime_execution" in (
        result["invariant_refs"]
    )
    assert "local_noop_runner_envelope_not_command_execution" in (
        result["invariant_refs"]
    )
    assert "local_noop_runner_envelope_not_subprocess_execution" in (
        result["invariant_refs"]
    )
    assert "no_runner_execution" in result["invariant_refs"]
    assert "no_runtime_execution" in result["invariant_refs"]
    assert "no_command_execution" in result["invariant_refs"]
    assert "no_subprocess_execution" in result["invariant_refs"]
    assert "no_run_ledger_yaml_write" in result["invariant_refs"]
    assert "public_url" in payload_keys
    assert result["source"]["public_url"] is None
    assert result["local_noop_runner_envelope"]["public_url"] is None
    assert "no_raw_url" not in payload_keys
    assert "no_public_url_behavior" not in payload_keys
    assert "buildable_not_runnable" not in payload_keys
    assert "buildable_not_executable" not in payload_keys
