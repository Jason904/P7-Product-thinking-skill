"""Tests for the pure local noop runner result candidate assembler."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import (  # noqa: E402
    local_noop_runner_result_assembler as assembler,
)


RESULT_KEYS = (
    "assembled",
    "reason_code",
    "reason",
    "source",
    "local_noop_runner_result_candidate",
    "assembly_violations",
    "missing_or_invalid_fields",
    "result_candidate_evidence_item_violations",
    "invariant_refs",
)

SOURCE_KEYS = (
    "mode",
    "runner_terminal_status",
    "local_noop_runner_readiness_ref",
    "local_noop_runner_readiness_id",
    "local_noop_runner_readiness_buildable_marker",
    "public_url",
    "public_url_created",
    "source_of_truth",
)

LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_KEYS = (
    "run_id",
    "local_noop_runner_result_candidate_id",
    "candidate_kind",
    "mode",
    "runner_terminal_status",
    "local_noop_runner_readiness_ref",
    "local_noop_runner_readiness_id",
    "local_noop_runner_readiness_buildable_marker",
    "public_url",
    "public_url_created",
    "result_candidate_evidence_items",
    "required_result_candidate_evidence_ids",
    "missing_result_candidate_evidence_ids",
    "blocking_result_candidate_evidence_ids",
    "created_at",
    "timestamp_policy",
    "source_of_truth",
    "notes",
)

RESULT_CANDIDATE_EVIDENCE_ITEM_KEYS = (
    "result_candidate_evidence_id",
    "result_candidate_evidence_role",
    "artifact_ref",
    "artifact_kind",
    "evidence_status",
    "producer_ref",
    "evidence_refs",
    "notes",
)

RESULT_CANDIDATE_EVIDENCE_ITEM_VIOLATION_KEYS = (
    "result_candidate_evidence_item_index",
    "result_candidate_evidence_id",
    "reason_code",
    "field",
)

REASON_CODES = (
    "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_ASSEMBLED",
    "RUN_ID_MISSING",
    "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_ID_MISSING",
    "CANDIDATE_KIND_NOT_LOCAL_NOOP_RUNNER_RESULT_CANDIDATE",
    "MODE_NOT_NOOP",
    "PASS_PUBLISHED_FORBIDDEN",
    "RUNNER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
    "LOCAL_NOOP_RUNNER_READINESS_REF_MISSING",
    "LOCAL_NOOP_RUNNER_READINESS_ID_MISSING",
    "LOCAL_NOOP_RUNNER_READINESS_BUILDABLE_MARKER_NOT_TRUE",
    "PUBLIC_URL_IS_NULL_NOT_TRUE",
    "PUBLIC_URL_CREATED_NOT_FALSE",
    "RESULT_CANDIDATE_EVIDENCE_ITEMS_MISSING",
    "REQUIRED_RESULT_CANDIDATE_EVIDENCE_IDS_MISSING",
    "MISSING_RESULT_CANDIDATE_EVIDENCE_IDS_DECLARED",
    "BLOCKING_RESULT_CANDIDATE_EVIDENCE_ID_UNKNOWN",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_ITEM_NOT_DICT",
    "RESULT_CANDIDATE_EVIDENCE_ITEM_KEYS_INVALID",
    "RESULT_CANDIDATE_EVIDENCE_ID_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_ROLE_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_ARTIFACT_REF_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_ARTIFACT_KIND_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_STATUS_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_PRODUCER_REF_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_REFS_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_ID_DUPLICATE",
    "RESULT_CANDIDATE_EVIDENCE_ID_NOT_REQUIRED",
    "REQUIRED_RESULT_CANDIDATE_EVIDENCE_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT",
)

REASON_PRIORITY = (
    "RUN_ID_MISSING",
    "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_ID_MISSING",
    "CANDIDATE_KIND_NOT_LOCAL_NOOP_RUNNER_RESULT_CANDIDATE",
    "MODE_NOT_NOOP",
    "PASS_PUBLISHED_FORBIDDEN",
    "RUNNER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
    "LOCAL_NOOP_RUNNER_READINESS_REF_MISSING",
    "LOCAL_NOOP_RUNNER_READINESS_ID_MISSING",
    "LOCAL_NOOP_RUNNER_READINESS_BUILDABLE_MARKER_NOT_TRUE",
    "PUBLIC_URL_IS_NULL_NOT_TRUE",
    "PUBLIC_URL_CREATED_NOT_FALSE",
    "RESULT_CANDIDATE_EVIDENCE_ITEMS_MISSING",
    "REQUIRED_RESULT_CANDIDATE_EVIDENCE_IDS_MISSING",
    "MISSING_RESULT_CANDIDATE_EVIDENCE_IDS_DECLARED",
    "BLOCKING_RESULT_CANDIDATE_EVIDENCE_ID_UNKNOWN",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_ITEM_NOT_DICT",
    "RESULT_CANDIDATE_EVIDENCE_ITEM_KEYS_INVALID",
    "RESULT_CANDIDATE_EVIDENCE_ID_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_ROLE_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_ARTIFACT_REF_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_ARTIFACT_KIND_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_STATUS_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_PRODUCER_REF_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_REFS_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_ID_DUPLICATE",
    "RESULT_CANDIDATE_EVIDENCE_ID_NOT_REQUIRED",
    "REQUIRED_RESULT_CANDIDATE_EVIDENCE_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT",
    "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_ASSEMBLED",
)

FORBIDDEN_RESULT_CANDIDATE_EVIDENCE_ITEM_FIELDS = (
    "completed",
    "consumed",
    "runner_result_created",
    "execution_ready",
    "runnable",
    "executable",
    "invocation_ready",
    "runner_executed",
    "execution_performed",
    "runner_execution_result",
    "runtime_execution_result",
    "cli_execution_result",
    "command_execution_result",
    "subprocess_execution_result",
    "dry_run_execution_result",
    "e2e_execution_result",
    "noop_completion_result",
    "transition_result",
    "gate_execution_result",
    "policy_execution_result",
    "audit_execution_result",
    "validator_execution_result",
    "eval_result",
    "publish_result",
    "notification_result",
    "ledger_write_result",
    "local_noop_runner_result_candidate_content",
    "local_noop_runner_result_candidate_path",
    "local_noop_runner_readiness_content",
    "local_noop_runner_readiness_path",
    "local_noop_runner_readiness_read",
    "full_local_noop_runner_readiness",
    "local_noop_runner_readiness_payload",
    "raw_local_noop_runner_readiness_payload",
    "local_noop_runner_envelope_content",
    "local_noop_runner_envelope_path",
    "local_noop_runner_envelope_read",
    "full_local_noop_runner_envelope",
    "local_noop_runner_envelope_payload",
    "raw_local_noop_runner_envelope_payload",
    "runner_payload",
    "runner_result_payload",
    "runner_result",
    "final_runner_result",
    "dry_run_payload",
    "e2e_payload",
    "completion_payload",
    "runtime_result",
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
    "should_execute_runner",
    "should_consume_runner",
    "should_execute_runtime",
    "should_execute_cli",
    "should_execute_command",
    "should_run_command",
    "should_parse_args",
    "should_call_subprocess",
    "should_call_local_noop_runner_readiness_builder",
    "should_call_local_noop_runner_result_builder",
    "should_call_local_noop_runner_envelope_builder",
    "should_call_run_ledger_draft_builder",
    "should_call_noop_completion_policy",
    "should_call_transition_guard",
    "should_call_gate_decision_mapper",
    "runner_created",
    "runner_ready",
    "runner_consumed",
    "runtime_created",
    "cli_created",
    "command_executed",
    "subprocess_executed",
    "argparse_executed",
    "click_executed",
    "typer_executed",
    "manual_execution_result",
    "manual_command_result",
    "human_confirmation_result",
    "human_approval_result",
    "operator_action_result",
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
    "public_url_value",
    "publish_url",
    "deployment_url",
    "real_url",
    "live_url",
    "public_url_created_executed",
    "raw_artifact_content",
    "raw_evidence_content",
    "raw_content",
    "content",
    "source_content",
    "artifact_contents",
    "fetched_content",
    "generated_summary",
    "llm_summary",
    "model_output",
    "prompt",
    "quality_pass",
    "validator_pass",
    "rubric_pass",
    "audit_pass",
    "eval_pass",
    "gate_pass",
    "publish_allowed",
    "pass_published",
    "file_path",
    "local_path",
    "reader_path",
    "credentials",
    "env_vars",
    "config",
    "adapter_outputs",
    "source_fetch_result",
    "artifact_reader_result",
    "should_fetch",
    "should_call_web",
    "should_call_llm",
    "should_run_policy",
    "should_gate",
    "should_publish",
    "should_create_public_url",
    "should_write_ledger",
    "should_notify",
    "should_transition",
    "should_complete_noop",
    "reader_read",
    "source_read",
    "gate_input_read",
    "public_url_behavior",
)

FORBIDDEN_SUCCESS_NAMES = (
    "completed",
    "consumed",
    "runner_result_created",
    "execution_ready",
    "runnable",
    "executable",
    "invocation_ready",
    "runner_executed",
    "execution_performed",
)

FORBIDDEN_PSEUDO_REASON_CODES = (
    "COMPLETED",
    "CONSUMED",
    "RUNNER_RESULT_CREATED",
    "EXECUTION_READY",
    "RUNNABLE",
    "EXECUTABLE",
    "INVOCATION_READY",
    "RUNNER_EXECUTED",
    "EXECUTION_PERFORMED",
    "PASS_PUBLISHED",
    "QUALITY_PASS",
    "EVAL_PASS",
    "AUDIT_PASS",
    "GATE_PASS",
    "PUBLISH_ALLOWED",
    "REVIEW_BLOCKED",
    "PUBLIC_URL_CREATED",
    "RUNNER_EXECUTION_FORBIDDEN",
    "RUNNER_CONSUMER_FORBIDDEN",
    "RUNTIME_EXECUTION_FORBIDDEN",
    "CLI_EXECUTION_FORBIDDEN",
    "COMMAND_EXECUTION_FORBIDDEN",
    "SUBPROCESS_EXECUTION_FORBIDDEN",
    "P2D40_READINESS_READ_FORBIDDEN",
    "P2D39_ENVELOPE_READ_FORBIDDEN",
    "PREVIOUS_BUILDER_CALL_FORBIDDEN",
    "LEDGER_WRITE_FORBIDDEN",
)

FORBIDDEN_MODULE_NAMES = (
    "argparse",
    "click",
    "typer",
    "subprocess",
    "os",
    "pathlib",
    "datetime",
    "hashlib",
    "logging",
    "requests",
    "httpx",
    "urllib",
    "feedparser",
    "jinja2",
    "local_noop_runner_readiness_builder",
    "local_noop_runner_result_builder",
    "local_noop_runner_envelope_builder",
    "run_ledger_draft_builder",
    "run_ledger_entry_builder",
    "noop_completion_policy",
    "transition_guard",
    "gate_decision_mapper",
)

REQUIRED_INVARIANT_REFS = (
    "local_noop_runner_result_assembler_only",
    "assembler_not_runner_executor",
    "assembler_not_runner_consumer",
    "assembler_not_runtime_executor",
    "assembler_not_cli_executor",
    "assembler_not_manual_executor",
    "assembler_not_argparse_parser",
    "assembler_not_click_app",
    "assembler_not_typer_app",
    "assembler_not_console_script",
    "assembler_not_subprocess_runner",
    "assembler_not_command_runner",
    "assembler_not_run_ledger_writer",
    "assembler_not_run_ledger_entry_builder",
    "assembler_not_run_ledger_draft_builder",
    "assembler_not_local_noop_runner_result_builder",
    "assembler_not_local_noop_runner_readiness_builder",
    "assembler_not_local_noop_runner_envelope_builder",
    "assembler_not_noop_completion_policy",
    "assembler_not_transition_guard",
    "assembler_not_gate_decision_mapper",
    "assembler_not_file_reader",
    "assembler_not_artifact_reader",
    "assembler_not_p2d40_readiness_reader",
    "assembler_not_p2d39_envelope_reader",
    "assembler_not_web_fetcher",
    "assembler_not_github_fetcher",
    "assembler_not_rss_fetcher",
    "assembler_not_notion_fetcher",
    "assembler_not_llm_judge",
    "assembler_not_audit_executor",
    "assembler_not_policy_executor",
    "assembler_not_validator_executor",
    "assembler_not_eval_executor",
    "assembler_not_gate_executor",
    "assembler_not_transition_executor",
    "assembler_not_noop_completion_executor",
    "assembler_not_dry_run_executor",
    "assembler_not_e2e_executor",
    "assembler_not_publisher",
    "assembler_not_ledger_writer",
    "assembler_not_notifier",
    "result_candidate_evidence_items_are_caller_supplied",
    "result_candidate_evidence_status_is_caller_supplied",
    "local_noop_runner_readiness_ref_is_caller_supplied",
    "local_noop_runner_readiness_id_is_caller_supplied",
    "local_noop_runner_readiness_marker_is_caller_supplied",
    "local_noop_runner_readiness_ref_opaque",
    "artifact_refs_opaque",
    "evidence_refs_opaque",
    "local_noop_runner_result_candidate_governance_evidence_bundle",
    "local_noop_runner_result_candidate_not_runner_execution",
    "local_noop_runner_result_candidate_not_runner_consumer",
    "local_noop_runner_result_candidate_not_runtime_execution",
    "local_noop_runner_result_candidate_not_cli_execution",
    "local_noop_runner_result_candidate_not_manual_execution",
    "local_noop_runner_result_candidate_not_argument_parsing",
    "local_noop_runner_result_candidate_not_console_script",
    "local_noop_runner_result_candidate_not_command_execution",
    "local_noop_runner_result_candidate_not_subprocess_execution",
    "local_noop_runner_result_candidate_not_ledger_write",
    "local_noop_runner_result_candidate_not_run_ledger_yaml",
    "local_noop_runner_result_candidate_not_state_transition",
    "local_noop_runner_result_candidate_not_gate_decision",
    "local_noop_runner_result_candidate_not_publish_artifact",
    "local_noop_runner_result_candidate_not_public_candidate",
    "mode_noop_required",
    "public_url_must_be_null",
    "public_url_created_must_be_false",
    "runner_terminal_status_must_be_noop_completed",
    "noop_completed_not_pass_published",
    "pass_published_forbidden",
    "mode_noop_not_publish",
    "assembled_not_completed",
    "assembled_not_consumed",
    "assembled_not_runner_result_created",
    "assembled_not_execution_ready",
    "assembled_not_runnable",
    "assembled_not_executable",
    "assembled_not_invocation_ready",
    "assembled_not_runner_executed",
    "assembled_not_execution_performed",
    "readiness_buildable_marker_not_quality_pass",
    "readiness_buildable_marker_not_gate_pass",
    "readiness_buildable_marker_not_publish_allowed",
    "result_candidate_evidence_status_not_quality_pass",
    "result_candidate_evidence_status_not_gate_pass",
    "result_candidate_evidence_status_not_publish_allowed",
    "assembled_not_runtime_executed",
    "assembled_not_cli_executed",
    "assembled_not_manual_executed",
    "assembled_not_command_executed",
    "assembled_not_argparse_executed",
    "assembled_not_subprocess_executed",
    "assembled_not_ledger_written",
    "assembled_not_state_transition_executed",
    "assembled_not_quality_pass",
    "assembled_not_eval_pass",
    "assembled_not_audit_pass",
    "assembled_not_gate_pass",
    "assembled_not_publish_allowed",
    "assembled_not_review_blocked",
    "assembled_not_pass_published",
    "assembled_not_public_url_created",
    "assembled_not_notification_sent",
    "blocking_result_candidate_evidence_ids_are_evidence_only",
    "blocking_result_candidate_evidence_ids_do_not_execute_gate",
    "blocking_result_candidate_evidence_ids_do_not_execute_noop_completion",
    "blocking_result_candidate_evidence_ids_do_not_execute_dry_run",
    "blocking_result_candidate_evidence_ids_do_not_execute_e2e",
    "blocking_result_candidate_evidence_ids_do_not_execute_runner",
    "blocking_result_candidate_evidence_ids_do_not_write_ledger",
    "no_p2d40_readiness_read",
    "no_p2d39_envelope_read",
    "no_artifact_content_read",
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
    "no_runner_consumer",
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
    "no_run_ledger_yaml_read",
    "no_run_ledger_yaml_write",
    "no_public_url_behavior",
    "no_quality_pass_no_public_url",
)

MISSING_RESULT_CANDIDATE_EVIDENCE_ITEM_KEY_EXPECTATIONS = (
    ("result_candidate_evidence_id", "RESULT_CANDIDATE_EVIDENCE_ID_MISSING"),
    ("result_candidate_evidence_role", "RESULT_CANDIDATE_EVIDENCE_ROLE_MISSING"),
    ("artifact_ref", "RESULT_CANDIDATE_EVIDENCE_ARTIFACT_REF_MISSING"),
    ("artifact_kind", "RESULT_CANDIDATE_EVIDENCE_ARTIFACT_KIND_MISSING"),
    ("evidence_status", "RESULT_CANDIDATE_EVIDENCE_STATUS_MISSING"),
    ("producer_ref", "RESULT_CANDIDATE_EVIDENCE_PRODUCER_REF_MISSING"),
    ("evidence_refs", "RESULT_CANDIDATE_EVIDENCE_REFS_MISSING"),
)


def _result_candidate_evidence_item(**overrides):
    values = {
        "result_candidate_evidence_id": "result-candidate-evidence-001",
        "result_candidate_evidence_role": "local_noop_runner_readiness",
        "artifact_ref": "local-noop-runner-readiness-001",
        "artifact_kind": "local_noop_runner_readiness",
        "evidence_status": "passed",
        "producer_ref": "caller-supplied-result-candidate",
        "evidence_refs": ("local-noop-runner-readiness-001#noop-terminal",),
        "notes": ("caller-supplied-evidence-only",),
    }
    values.update(overrides)
    return values


def _valid_values():
    return {
        "run_id": "run-001",
        "local_noop_runner_result_candidate_id": (
            "local-noop-runner-result-candidate-001"
        ),
        "candidate_kind": "local_noop_runner_result_candidate",
        "mode": "noop",
        "runner_terminal_status": "NOOP_COMPLETED",
        "local_noop_runner_readiness_ref": "local-noop-runner-readiness-001",
        "local_noop_runner_readiness_id": (
            "local-noop-runner-readiness-id-001"
        ),
        "local_noop_runner_readiness_buildable_marker": True,
        "public_url_created": False,
        "public_url_is_null": True,
        "result_candidate_evidence_items": (
            _result_candidate_evidence_item(),
        ),
        "required_result_candidate_evidence_ids": (
            "result-candidate-evidence-001",
        ),
        "missing_result_candidate_evidence_ids": (),
        "blocking_result_candidate_evidence_ids": (),
        "created_at": "caller-supplied-created-at",
        "timestamp_policy": "caller_supplied_no_datetime_parsing",
        "source_of_truth": ("p2d-41",),
        "notes": ("structured-only",),
    }


def _assemble(**overrides):
    values = _valid_values()
    values.update(overrides)
    return assembler.assemble_local_noop_runner_result_candidate(**values)


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
    assert assembler.REASON_CODES == REASON_CODES
    assert (
        assembler.LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_ASSEMBLY_REASON_CODES
        == REASON_CODES
    )
    assert assembler.REASON_PRIORITY == REASON_PRIORITY


def test_valid_result_candidate_assembled_with_exact_shapes():
    result = _assemble()

    assert result["assembled"] is True
    assert result["reason_code"] == (
        "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_ASSEMBLED"
    )
    assert result["assembly_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()
    assert result["result_candidate_evidence_item_violations"] == ()
    assert tuple(result.keys()) == RESULT_KEYS
    assert tuple(result["source"].keys()) == SOURCE_KEYS
    assert tuple(
        result["local_noop_runner_result_candidate"].keys()
    ) == LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_KEYS
    assert tuple(
        result["local_noop_runner_result_candidate"][
            "result_candidate_evidence_items"
        ][0].keys()
    ) == RESULT_CANDIDATE_EVIDENCE_ITEM_KEYS
    assert result["source"]["public_url"] is None
    assert result["local_noop_runner_result_candidate"]["public_url"] is None
    assert result["source"]["public_url_created"] is False
    assert (
        result["local_noop_runner_result_candidate"]["public_url_created"]
        is False
    )
    assert "public_url_is_null" not in result
    assert "public_url_is_null" not in result["source"]
    assert (
        "public_url_is_null"
        not in result["local_noop_runner_result_candidate"]
    )


def test_public_api_is_keyword_only_and_bool_wrapper_matches_assembler():
    expected_kwonly = len(_valid_values())

    assert (
        assembler.assemble_local_noop_runner_result_candidate.__code__
        .co_argcount
        == 0
    )
    assert (
        assembler.assemble_local_noop_runner_result_candidate.__code__
        .co_kwonlyargcount
        == expected_kwonly
    )
    assert (
        assembler.is_local_noop_runner_result_candidate_assembled.__code__
        .co_argcount
        == 0
    )
    assert (
        assembler.is_local_noop_runner_result_candidate_assembled.__code__
        .co_kwonlyargcount
        == expected_kwonly
    )

    cases = (
        _valid_values(),
        {**_valid_values(), "run_id": ""},
        {**_valid_values(), "runner_terminal_status": "PASS_PUBLISHED"},
        {**_valid_values(), "public_url_is_null": False},
    )
    for values in cases:
        result = assembler.assemble_local_noop_runner_result_candidate(**values)
        assert (
            assembler.is_local_noop_runner_result_candidate_assembled(**values)
            is result["assembled"]
        )


def test_required_lockin_markers_block_when_invalid():
    cases = (
        (
            {"candidate_kind": "local_noop_runner_result"},
            "CANDIDATE_KIND_NOT_LOCAL_NOOP_RUNNER_RESULT_CANDIDATE",
            "candidate_kind",
        ),
        ({"mode": "real"}, "MODE_NOT_NOOP", "mode"),
        (
            {"runner_terminal_status": "DONE"},
            "RUNNER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
            "runner_terminal_status",
        ),
        (
            {"runner_terminal_status": "PASS_PUBLISHED"},
            "PASS_PUBLISHED_FORBIDDEN",
            "runner_terminal_status",
        ),
        (
            {"local_noop_runner_readiness_ref": ""},
            "LOCAL_NOOP_RUNNER_READINESS_REF_MISSING",
            "local_noop_runner_readiness_ref",
        ),
        (
            {"local_noop_runner_readiness_id": ""},
            "LOCAL_NOOP_RUNNER_READINESS_ID_MISSING",
            "local_noop_runner_readiness_id",
        ),
        (
            {"local_noop_runner_readiness_buildable_marker": False},
            "LOCAL_NOOP_RUNNER_READINESS_BUILDABLE_MARKER_NOT_TRUE",
            "local_noop_runner_readiness_buildable_marker",
        ),
        (
            {"local_noop_runner_readiness_buildable_marker": 1},
            "LOCAL_NOOP_RUNNER_READINESS_BUILDABLE_MARKER_NOT_TRUE",
            "local_noop_runner_readiness_buildable_marker",
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
        result = _assemble(**overrides)

        assert result["assembled"] is False
        assert reason_code in result["assembly_violations"]
        assert field in result["missing_or_invalid_fields"]


def test_pass_published_status_is_blocked_and_suppressed_from_payload():
    result = _assemble(runner_terminal_status="PASS_PUBLISHED")

    assert result["reason_code"] == "PASS_PUBLISHED_FORBIDDEN"
    assert "RUNNER_TERMINAL_STATUS_NOT_NOOP_COMPLETED" in (
        result["assembly_violations"]
    )
    assert result["source"]["runner_terminal_status"] == ""
    assert (
        result["local_noop_runner_result_candidate"][
            "runner_terminal_status"
        ]
        == ""
    )


def test_public_url_boundaries_are_forced_to_null_and_false():
    null_blocked = _assemble(public_url_is_null=False)
    created_blocked = _assemble(public_url_created=True)

    assert null_blocked["assembled"] is False
    assert "PUBLIC_URL_IS_NULL_NOT_TRUE" in (
        null_blocked["assembly_violations"]
    )
    assert created_blocked["assembled"] is False
    assert "PUBLIC_URL_CREATED_NOT_FALSE" in (
        created_blocked["assembly_violations"]
    )
    assert created_blocked["source"]["public_url_created"] is False
    assert (
        created_blocked["local_noop_runner_result_candidate"][
            "public_url_created"
        ]
        is False
    )
    assert null_blocked["source"]["public_url"] is None
    assert (
        null_blocked["local_noop_runner_result_candidate"]["public_url"]
        is None
    )


def test_failed_evidence_status_and_known_blocking_ids_still_assemble():
    failed = _assemble(
        result_candidate_evidence_items=(
            _result_candidate_evidence_item(evidence_status="failed"),
        )
    )
    blocked_known = _assemble(
        blocking_result_candidate_evidence_ids=(
            "result-candidate-evidence-001",
        ),
        result_candidate_evidence_items=(
            _result_candidate_evidence_item(evidence_status="failed"),
        ),
    )

    assert failed["assembled"] is True
    assert blocked_known["assembled"] is True
    assert blocked_known["local_noop_runner_result_candidate"][
        "blocking_result_candidate_evidence_ids"
    ] == ("result-candidate-evidence-001",)


def test_unknown_blank_or_non_tuple_blocking_ids_block_assembly():
    cases = (
        ("missing-result-candidate-evidence",),
        ("",),
        ["result-candidate-evidence-001"],
    )

    for blocking_result_candidate_evidence_ids in cases:
        result = _assemble(
            blocking_result_candidate_evidence_ids=(
                blocking_result_candidate_evidence_ids
            )
        )

        assert result["assembled"] is False
        assert "BLOCKING_RESULT_CANDIDATE_EVIDENCE_ID_UNKNOWN" in (
            result["assembly_violations"]
        )
        assert "blocking_result_candidate_evidence_ids" in (
            result["missing_or_invalid_fields"]
        )


def test_required_top_level_field_violations_are_collected():
    cases = (
        ("run_id", "", "RUN_ID_MISSING"),
        (
            "local_noop_runner_result_candidate_id",
            "",
            "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_ID_MISSING",
        ),
        (
            "result_candidate_evidence_items",
            (),
            "RESULT_CANDIDATE_EVIDENCE_ITEMS_MISSING",
        ),
        (
            "result_candidate_evidence_items",
            [],
            "RESULT_CANDIDATE_EVIDENCE_ITEMS_MISSING",
        ),
        (
            "required_result_candidate_evidence_ids",
            (),
            "REQUIRED_RESULT_CANDIDATE_EVIDENCE_IDS_MISSING",
        ),
        (
            "required_result_candidate_evidence_ids",
            ("",),
            "REQUIRED_RESULT_CANDIDATE_EVIDENCE_IDS_MISSING",
        ),
        (
            "required_result_candidate_evidence_ids",
            ["result-candidate-evidence-001"],
            "REQUIRED_RESULT_CANDIDATE_EVIDENCE_IDS_MISSING",
        ),
        (
            "missing_result_candidate_evidence_ids",
            ("result-candidate-evidence-002",),
            "MISSING_RESULT_CANDIDATE_EVIDENCE_IDS_DECLARED",
        ),
        (
            "missing_result_candidate_evidence_ids",
            [],
            "MISSING_RESULT_CANDIDATE_EVIDENCE_IDS_DECLARED",
        ),
        ("created_at", "", "CREATED_AT_MISSING"),
        ("timestamp_policy", "", "TIMESTAMP_POLICY_MISSING"),
        ("source_of_truth", (), "SOURCE_OF_TRUTH_MISSING"),
        ("source_of_truth", ("",), "SOURCE_OF_TRUTH_MISSING"),
        ("source_of_truth", ["p2d-41"], "SOURCE_OF_TRUTH_MISSING"),
    )

    for field, value, reason_code in cases:
        result = _assemble(**{field: value})

        assert result["assembled"] is False
        assert reason_code in result["assembly_violations"]
        assert field in result["missing_or_invalid_fields"]


def test_result_candidate_evidence_id_uniqueness_required_and_presence():
    duplicate = _assemble(
        result_candidate_evidence_items=(
            _result_candidate_evidence_item(),
            _result_candidate_evidence_item(),
        )
    )
    not_required = _assemble(
        result_candidate_evidence_items=(
            _result_candidate_evidence_item(
                result_candidate_evidence_id="result-candidate-evidence-002"
            ),
        )
    )
    required_missing = _assemble(
        required_result_candidate_evidence_ids=(
            "result-candidate-evidence-001",
            "result-candidate-evidence-002",
        )
    )

    assert "RESULT_CANDIDATE_EVIDENCE_ID_DUPLICATE" in (
        duplicate["assembly_violations"]
    )
    assert "RESULT_CANDIDATE_EVIDENCE_ID_NOT_REQUIRED" in (
        not_required["assembly_violations"]
    )
    assert "REQUIRED_RESULT_CANDIDATE_EVIDENCE_MISSING" in (
        required_missing["assembly_violations"]
    )


def test_result_candidate_evidence_item_fields_and_missing_keys_reported():
    cases = (
        (
            "result_candidate_evidence_id",
            "",
            "RESULT_CANDIDATE_EVIDENCE_ID_MISSING",
        ),
        (
            "result_candidate_evidence_role",
            "",
            "RESULT_CANDIDATE_EVIDENCE_ROLE_MISSING",
        ),
        (
            "artifact_ref",
            "",
            "RESULT_CANDIDATE_EVIDENCE_ARTIFACT_REF_MISSING",
        ),
        (
            "artifact_kind",
            "",
            "RESULT_CANDIDATE_EVIDENCE_ARTIFACT_KIND_MISSING",
        ),
        (
            "evidence_status",
            "",
            "RESULT_CANDIDATE_EVIDENCE_STATUS_MISSING",
        ),
        (
            "producer_ref",
            "",
            "RESULT_CANDIDATE_EVIDENCE_PRODUCER_REF_MISSING",
        ),
        ("evidence_refs", (), "RESULT_CANDIDATE_EVIDENCE_REFS_MISSING"),
        ("evidence_refs", ("",), "RESULT_CANDIDATE_EVIDENCE_REFS_MISSING"),
        ("evidence_refs", ["ref"], "RESULT_CANDIDATE_EVIDENCE_REFS_MISSING"),
    )
    for field, value, reason_code in cases:
        result = _assemble(
            result_candidate_evidence_items=(
                _result_candidate_evidence_item(**{field: value}),
            )
        )

        assert result["assembled"] is False
        assert reason_code in result["assembly_violations"]
        assert f"result_candidate_evidence_items[0].{field}" in (
            result["missing_or_invalid_fields"]
        )
        assert tuple(
            result["result_candidate_evidence_item_violations"][0].keys()
        ) == RESULT_CANDIDATE_EVIDENCE_ITEM_VIOLATION_KEYS

    for missing_key, reason_code in (
        MISSING_RESULT_CANDIDATE_EVIDENCE_ITEM_KEY_EXPECTATIONS
    ):
        item = _result_candidate_evidence_item()
        del item[missing_key]
        result = _assemble(result_candidate_evidence_items=(item,))

        assert result["assembled"] is False
        assert "RESULT_CANDIDATE_EVIDENCE_ITEM_KEYS_INVALID" in (
            result["assembly_violations"]
        )
        assert reason_code in result["assembly_violations"]
        assert f"result_candidate_evidence_items[0].{missing_key}" in (
            result["missing_or_invalid_fields"]
        )
        assert "result_candidate_evidence_items[0].keys" in (
            result["missing_or_invalid_fields"]
        )


def test_non_dict_result_candidate_evidence_item_records_violation_shape():
    result = _assemble(result_candidate_evidence_items=("not-evidence",))

    assert result["assembled"] is False
    assert "RESULT_CANDIDATE_EVIDENCE_ITEM_NOT_DICT" in (
        result["assembly_violations"]
    )
    assert tuple(
        result["result_candidate_evidence_item_violations"][0].keys()
    ) == RESULT_CANDIDATE_EVIDENCE_ITEM_VIOLATION_KEYS
    assert result["local_noop_runner_result_candidate"][
        "result_candidate_evidence_items"
    ] == (
        {
            "result_candidate_evidence_id": "",
            "result_candidate_evidence_role": "",
            "artifact_ref": "",
            "artifact_kind": "",
            "evidence_status": "",
            "producer_ref": "",
            "evidence_refs": (),
            "notes": (),
        },
    )


def test_forbidden_raw_execution_cli_url_and_publication_fields_suppressed():
    for field in FORBIDDEN_RESULT_CANDIDATE_EVIDENCE_ITEM_FIELDS:
        result = _assemble(
            result_candidate_evidence_items=(
                _result_candidate_evidence_item(**{field: "forbidden"}),
            )
        )

        assert result["assembled"] is False
        assert "RESULT_CANDIDATE_EVIDENCE_ITEM_KEYS_INVALID" in (
            result["assembly_violations"]
        )
        assert "RESULT_CANDIDATE_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT" in (
            result["assembly_violations"]
        )
        assert f"result_candidate_evidence_items[0].{field}" in (
            result["missing_or_invalid_fields"]
        )
        assert field not in (
            result["local_noop_runner_result_candidate"][
                "result_candidate_evidence_items"
            ][0]
        )
        assert tuple(
            result["result_candidate_evidence_item_violations"][0].keys()
        ) == RESULT_CANDIDATE_EVIDENCE_ITEM_VIOLATION_KEYS


def test_output_does_not_expose_public_url_is_null_or_extra_url_values():
    result = _assemble()
    forbidden_url = _assemble(
        result_candidate_evidence_items=(
            _result_candidate_evidence_item(
                public_url_value="https://example.test"
            ),
        )
    )
    payload_keys = _payload_keys(result)
    forbidden_payload_keys = _payload_keys(forbidden_url)

    assert "public_url_is_null" not in payload_keys
    assert result["source"]["public_url"] is None
    assert result["local_noop_runner_result_candidate"]["public_url"] is None
    assert "public_url_value" not in forbidden_payload_keys
    assert forbidden_url["source"]["public_url"] is None
    assert (
        forbidden_url["local_noop_runner_result_candidate"]["public_url"]
        is None
    )


def test_no_completed_consumed_runnable_executable_or_execution_success_names():
    result = _assemble()
    payload_keys = _payload_keys(result)

    assert "assembled" in payload_keys
    for success_name in FORBIDDEN_SUCCESS_NAMES:
        assert success_name not in payload_keys


def test_reason_catalog_priority_and_forbidden_pseudo_reason_codes():
    assert assembler.REASON_CODES == REASON_CODES
    assert (
        assembler.LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_ASSEMBLY_REASON_CODES
        == REASON_CODES
    )
    assert assembler.REASON_PRIORITY == REASON_PRIORITY

    for reason_code in FORBIDDEN_PSEUDO_REASON_CODES:
        assert reason_code not in assembler.REASON_CODES
        assert reason_code not in assembler.REASON_PRIORITY


def test_forbidden_module_namespace_and_io_names_are_absent():
    for module_name in FORBIDDEN_MODULE_NAMES:
        assert not hasattr(assembler, module_name)


def test_all_violations_are_priority_ordered_and_details_present():
    first_item = _result_candidate_evidence_item(
        result_candidate_evidence_id="",
        result_candidate_evidence_role="",
        artifact_ref="",
        artifact_kind="",
        evidence_status="",
        producer_ref="",
        evidence_refs=(),
        raw_artifact_content="raw",
    )
    second_item = _result_candidate_evidence_item(
        result_candidate_evidence_id="extra-evidence"
    )
    result = _assemble(
        run_id="",
        local_noop_runner_result_candidate_id="",
        candidate_kind="wrong",
        mode="real",
        runner_terminal_status="PASS_PUBLISHED",
        local_noop_runner_readiness_ref="",
        local_noop_runner_readiness_id="",
        local_noop_runner_readiness_buildable_marker=False,
        public_url_is_null=False,
        public_url_created=True,
        result_candidate_evidence_items=(first_item, second_item),
        required_result_candidate_evidence_ids=(
            "result-candidate-evidence-001",
            "result-candidate-evidence-002",
        ),
        missing_result_candidate_evidence_ids=(
            "result-candidate-evidence-002",
        ),
        blocking_result_candidate_evidence_ids=("missing-block",),
        created_at="",
        timestamp_policy="",
        source_of_truth=(),
    )
    expected_order = tuple(
        reason_code
        for reason_code in REASON_PRIORITY
        if reason_code != "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_ASSEMBLED"
        and reason_code in result["assembly_violations"]
    )

    assert result["assembly_violations"] == expected_order
    assert result["reason_code"] == result["assembly_violations"][0]
    assert "result_candidate_evidence_items[0].raw_artifact_content" in (
        result["missing_or_invalid_fields"]
    )
    assert (
        "result_candidate_evidence_items[1].result_candidate_evidence_id"
        in result["missing_or_invalid_fields"]
    )
    assert (
        "required_result_candidate_evidence_ids.result-candidate-evidence-002"
        in result["missing_or_invalid_fields"]
    )
    assert result["result_candidate_evidence_item_violations"] != ()
    for violation in result["result_candidate_evidence_item_violations"]:
        assert tuple(violation.keys()) == (
            RESULT_CANDIDATE_EVIDENCE_ITEM_VIOLATION_KEYS
        )


def test_invariant_refs_capture_governance_and_no_execution_boundaries():
    result = _assemble()

    assert result["invariant_refs"] == REQUIRED_INVARIANT_REFS


def test_payload_key_traversal_skips_invariants_instead_of_blanket_scans():
    result = _assemble()
    payload_keys = _payload_keys(result)

    assert "no_p2d40_readiness_read" in result["invariant_refs"]
    assert "no_p2d39_envelope_read" in result["invariant_refs"]
    assert "no_public_url_behavior" in result["invariant_refs"]
    assert "assembled_not_completed" in result["invariant_refs"]
    assert "assembled_not_consumed" in result["invariant_refs"]
    assert "assembled_not_runner_result_created" in result["invariant_refs"]
    assert "assembled_not_execution_ready" in result["invariant_refs"]
    assert "assembled_not_runnable" in result["invariant_refs"]
    assert "assembled_not_executable" in result["invariant_refs"]
    assert "local_noop_runner_result_candidate_not_runner_execution" in (
        result["invariant_refs"]
    )
    assert "local_noop_runner_result_candidate_not_runner_consumer" in (
        result["invariant_refs"]
    )
    assert "local_noop_runner_result_candidate_not_runtime_execution" in (
        result["invariant_refs"]
    )
    assert "local_noop_runner_result_candidate_not_cli_execution" in (
        result["invariant_refs"]
    )
    assert "local_noop_runner_result_candidate_not_command_execution" in (
        result["invariant_refs"]
    )
    assert "local_noop_runner_result_candidate_not_subprocess_execution" in (
        result["invariant_refs"]
    )
    assert "local_noop_runner_result_candidate_not_ledger_write" in (
        result["invariant_refs"]
    )
    assert "no_runner_execution" in result["invariant_refs"]
    assert "no_runner_consumer" in result["invariant_refs"]
    assert "no_runtime_execution" in result["invariant_refs"]
    assert "no_cli_execution" in result["invariant_refs"]
    assert "no_command_execution" in result["invariant_refs"]
    assert "no_subprocess_execution" in result["invariant_refs"]
    assert "no_run_ledger_yaml_read" in result["invariant_refs"]
    assert "no_run_ledger_yaml_write" in result["invariant_refs"]
    assert "public_url" in payload_keys
    assert result["source"]["public_url"] is None
    assert result["local_noop_runner_result_candidate"]["public_url"] is None
    assert "no_raw_url" not in payload_keys
    assert "no_public_url_behavior" not in payload_keys
    assert "assembled_not_completed" not in payload_keys
    assert "assembled_not_runnable" not in payload_keys
