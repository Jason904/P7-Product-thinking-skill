"""Tests for the pure local noop runner readiness builder."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import (  # noqa: E402
    local_noop_runner_readiness_builder as builder,
)


RESULT_KEYS = (
    "buildable",
    "reason_code",
    "reason",
    "source",
    "local_noop_runner_readiness",
    "readiness_violations",
    "missing_or_invalid_fields",
    "readiness_evidence_item_violations",
    "invariant_refs",
)

SOURCE_KEYS = (
    "mode",
    "expected_terminal_status",
    "local_noop_runner_envelope_ref",
    "local_noop_runner_envelope_buildable_marker",
    "public_url",
    "public_url_created",
    "source_of_truth",
)

LOCAL_NOOP_RUNNER_READINESS_KEYS = (
    "run_id",
    "local_noop_runner_readiness_id",
    "readiness_kind",
    "mode",
    "expected_terminal_status",
    "local_noop_runner_envelope_ref",
    "local_noop_runner_envelope_buildable_marker",
    "public_url",
    "public_url_created",
    "readiness_evidence_items",
    "required_readiness_evidence_ids",
    "missing_readiness_evidence_ids",
    "blocking_readiness_evidence_ids",
    "created_at",
    "timestamp_policy",
    "source_of_truth",
    "notes",
)

READINESS_EVIDENCE_ITEM_KEYS = (
    "readiness_evidence_id",
    "readiness_evidence_role",
    "artifact_ref",
    "artifact_kind",
    "evidence_status",
    "producer_ref",
    "evidence_refs",
    "notes",
)

READINESS_EVIDENCE_ITEM_VIOLATION_KEYS = (
    "readiness_evidence_item_index",
    "readiness_evidence_id",
    "reason_code",
    "field",
)

REASON_CODES = (
    "LOCAL_NOOP_RUNNER_READINESS_BUILDABLE",
    "RUN_ID_MISSING",
    "LOCAL_NOOP_RUNNER_READINESS_ID_MISSING",
    "READINESS_KIND_NOT_LOCAL_NOOP_RUNNER_READINESS",
    "MODE_NOT_NOOP",
    "PASS_PUBLISHED_FORBIDDEN",
    "EXPECTED_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
    "LOCAL_NOOP_RUNNER_ENVELOPE_REF_MISSING",
    "LOCAL_NOOP_RUNNER_ENVELOPE_BUILDABLE_MARKER_NOT_TRUE",
    "PUBLIC_URL_IS_NULL_NOT_TRUE",
    "PUBLIC_URL_CREATED_NOT_FALSE",
    "READINESS_EVIDENCE_ITEMS_MISSING",
    "REQUIRED_READINESS_EVIDENCE_IDS_MISSING",
    "MISSING_READINESS_EVIDENCE_IDS_DECLARED",
    "BLOCKING_READINESS_EVIDENCE_ID_UNKNOWN",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "READINESS_EVIDENCE_ITEM_NOT_DICT",
    "READINESS_EVIDENCE_ITEM_KEYS_INVALID",
    "READINESS_EVIDENCE_ID_MISSING",
    "READINESS_EVIDENCE_ROLE_MISSING",
    "READINESS_EVIDENCE_ARTIFACT_REF_MISSING",
    "READINESS_EVIDENCE_ARTIFACT_KIND_MISSING",
    "READINESS_EVIDENCE_STATUS_MISSING",
    "READINESS_EVIDENCE_PRODUCER_REF_MISSING",
    "READINESS_EVIDENCE_REFS_MISSING",
    "READINESS_EVIDENCE_ID_DUPLICATE",
    "READINESS_EVIDENCE_ID_NOT_REQUIRED",
    "REQUIRED_READINESS_EVIDENCE_MISSING",
    "READINESS_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT",
)

REASON_PRIORITY = (
    "RUN_ID_MISSING",
    "LOCAL_NOOP_RUNNER_READINESS_ID_MISSING",
    "READINESS_KIND_NOT_LOCAL_NOOP_RUNNER_READINESS",
    "MODE_NOT_NOOP",
    "PASS_PUBLISHED_FORBIDDEN",
    "EXPECTED_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
    "LOCAL_NOOP_RUNNER_ENVELOPE_REF_MISSING",
    "LOCAL_NOOP_RUNNER_ENVELOPE_BUILDABLE_MARKER_NOT_TRUE",
    "PUBLIC_URL_IS_NULL_NOT_TRUE",
    "PUBLIC_URL_CREATED_NOT_FALSE",
    "READINESS_EVIDENCE_ITEMS_MISSING",
    "REQUIRED_READINESS_EVIDENCE_IDS_MISSING",
    "MISSING_READINESS_EVIDENCE_IDS_DECLARED",
    "BLOCKING_READINESS_EVIDENCE_ID_UNKNOWN",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "READINESS_EVIDENCE_ITEM_NOT_DICT",
    "READINESS_EVIDENCE_ITEM_KEYS_INVALID",
    "READINESS_EVIDENCE_ID_MISSING",
    "READINESS_EVIDENCE_ROLE_MISSING",
    "READINESS_EVIDENCE_ARTIFACT_REF_MISSING",
    "READINESS_EVIDENCE_ARTIFACT_KIND_MISSING",
    "READINESS_EVIDENCE_STATUS_MISSING",
    "READINESS_EVIDENCE_PRODUCER_REF_MISSING",
    "READINESS_EVIDENCE_REFS_MISSING",
    "READINESS_EVIDENCE_ID_DUPLICATE",
    "READINESS_EVIDENCE_ID_NOT_REQUIRED",
    "REQUIRED_READINESS_EVIDENCE_MISSING",
    "READINESS_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT",
    "LOCAL_NOOP_RUNNER_READINESS_BUILDABLE",
)

FORBIDDEN_READINESS_EVIDENCE_ITEM_FIELDS = (
    "ready",
    "execution_ready",
    "runnable",
    "executable",
    "invocation_ready",
    "assembled",
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
    "local_noop_runner_readiness_content",
    "local_noop_runner_readiness_path",
    "local_noop_runner_envelope_content",
    "local_noop_runner_envelope_path",
    "local_noop_runner_envelope_read",
    "full_local_noop_runner_envelope",
    "local_noop_runner_envelope_payload",
    "raw_local_noop_runner_envelope_payload",
    "runner_envelope_payload",
    "raw_runner_envelope_payload",
    "runner_payload",
    "runner_result_payload",
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
    "should_execute_runtime",
    "should_execute_cli",
    "should_execute_command",
    "should_run_command",
    "should_parse_args",
    "should_call_subprocess",
    "should_call_local_noop_runner_envelope_builder",
    "should_call_local_noop_runner_result_builder",
    "should_call_run_ledger_draft_builder",
    "should_call_noop_completion_policy",
    "should_call_transition_guard",
    "should_call_gate_decision_mapper",
    "runner_created",
    "runner_ready",
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
    "ready",
    "execution_ready",
    "runnable",
    "executable",
    "invocation_ready",
    "assembled",
    "runner_executed",
    "execution_performed",
)

FORBIDDEN_PSEUDO_REASON_CODES = (
    "READY",
    "RUNNER_READY",
    "RUNNER_EXECUTION_FORBIDDEN",
    "RUNTIME_EXECUTION_FORBIDDEN",
    "CLI_EXECUTION_FORBIDDEN",
    "COMMAND_EXECUTION_FORBIDDEN",
    "SUBPROCESS_EXECUTION_FORBIDDEN",
    "P2D39_ENVELOPE_READ_FORBIDDEN",
    "PREVIOUS_BUILDER_CALL_FORBIDDEN",
    "LEDGER_WRITE_FORBIDDEN",
    "PUBLIC_URL_CREATION_FORBIDDEN",
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
    "requests",
    "httpx",
    "urllib",
    "feedparser",
    "jinja2",
    "local_noop_runner_envelope_builder",
    "local_noop_runner_result_builder",
    "run_ledger_draft_builder",
    "run_ledger_entry_builder",
    "local_noop_cli_contract_builder",
    "local_noop_runner_skeleton_builder",
    "local_noop_e2e_contract_builder",
    "gate_input_assembly_builder",
    "local_noop_run_assembly_builder",
    "noop_completion_policy",
    "transition_guard",
    "gate_decision_mapper",
)

REQUIRED_INVARIANT_REFS = (
    "local_noop_runner_readiness_builder_only",
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
    "builder_not_local_noop_runner_envelope_builder",
    "builder_not_local_noop_cli_contract_builder",
    "builder_not_local_noop_runner_skeleton_builder",
    "builder_not_noop_completion_policy",
    "builder_not_transition_guard",
    "builder_not_gate_decision_mapper",
    "builder_not_file_reader",
    "builder_not_artifact_reader",
    "builder_not_p2d39_envelope_reader",
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
    "readiness_evidence_items_are_caller_supplied",
    "readiness_evidence_status_is_caller_supplied",
    "local_noop_runner_envelope_ref_is_caller_supplied",
    "local_noop_runner_envelope_marker_is_caller_supplied",
    "local_noop_runner_envelope_ref_opaque",
    "artifact_refs_opaque",
    "evidence_refs_opaque",
    "local_noop_runner_readiness_governance_evidence_bundle",
    "local_noop_runner_readiness_not_runner_execution",
    "local_noop_runner_readiness_not_runtime_execution",
    "local_noop_runner_readiness_not_cli_execution",
    "local_noop_runner_readiness_not_manual_execution",
    "local_noop_runner_readiness_not_argument_parsing",
    "local_noop_runner_readiness_not_console_script",
    "local_noop_runner_readiness_not_command_execution",
    "local_noop_runner_readiness_not_subprocess_execution",
    "local_noop_runner_readiness_not_ledger_write",
    "local_noop_runner_readiness_not_run_ledger_yaml",
    "local_noop_runner_readiness_not_state_transition",
    "local_noop_runner_readiness_not_gate_decision",
    "local_noop_runner_readiness_not_publish_artifact",
    "local_noop_runner_readiness_not_public_candidate",
    "mode_noop_required",
    "public_url_must_be_null",
    "public_url_created_must_be_false",
    "expected_terminal_status_must_be_noop_completed",
    "noop_completed_not_pass_published",
    "pass_published_forbidden",
    "mode_noop_not_publish",
    "buildable_not_ready",
    "buildable_not_execution_ready",
    "buildable_not_runnable",
    "buildable_not_executable",
    "buildable_not_invocation_ready",
    "buildable_not_assembled",
    "buildable_not_runner_executed",
    "buildable_not_execution_performed",
    "envelope_buildable_marker_not_quality_pass",
    "envelope_buildable_marker_not_gate_pass",
    "envelope_buildable_marker_not_publish_allowed",
    "readiness_evidence_status_not_quality_pass",
    "readiness_evidence_status_not_gate_pass",
    "readiness_evidence_status_not_publish_allowed",
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
    "blocking_readiness_evidence_ids_are_evidence_only",
    "blocking_readiness_evidence_ids_do_not_execute_gate",
    "blocking_readiness_evidence_ids_do_not_execute_noop_completion",
    "blocking_readiness_evidence_ids_do_not_execute_dry_run",
    "blocking_readiness_evidence_ids_do_not_execute_e2e",
    "blocking_readiness_evidence_ids_do_not_execute_runner",
    "blocking_readiness_evidence_ids_do_not_write_ledger",
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

MISSING_READINESS_EVIDENCE_ITEM_KEY_EXPECTATIONS = (
    ("readiness_evidence_id", "READINESS_EVIDENCE_ID_MISSING"),
    ("readiness_evidence_role", "READINESS_EVIDENCE_ROLE_MISSING"),
    ("artifact_ref", "READINESS_EVIDENCE_ARTIFACT_REF_MISSING"),
    ("artifact_kind", "READINESS_EVIDENCE_ARTIFACT_KIND_MISSING"),
    ("evidence_status", "READINESS_EVIDENCE_STATUS_MISSING"),
    ("producer_ref", "READINESS_EVIDENCE_PRODUCER_REF_MISSING"),
    ("evidence_refs", "READINESS_EVIDENCE_REFS_MISSING"),
)


def _readiness_evidence_item(**overrides):
    values = {
        "readiness_evidence_id": "readiness-evidence-001",
        "readiness_evidence_role": "local_noop_runner_envelope",
        "artifact_ref": "local-noop-runner-envelope-001",
        "artifact_kind": "local_noop_runner_envelope",
        "evidence_status": "passed",
        "producer_ref": "caller-supplied-readiness",
        "evidence_refs": ("local-noop-runner-envelope-001#noop-terminal",),
        "notes": ("caller-supplied-evidence-only",),
    }
    values.update(overrides)
    return values


def _valid_values():
    return {
        "run_id": "run-001",
        "local_noop_runner_readiness_id": "local-noop-runner-readiness-001",
        "readiness_kind": "local_noop_runner_readiness",
        "mode": "noop",
        "expected_terminal_status": "NOOP_COMPLETED",
        "local_noop_runner_envelope_ref": "local-noop-runner-envelope-001",
        "local_noop_runner_envelope_buildable_marker": True,
        "public_url_created": False,
        "public_url_is_null": True,
        "readiness_evidence_items": (_readiness_evidence_item(),),
        "required_readiness_evidence_ids": ("readiness-evidence-001",),
        "missing_readiness_evidence_ids": (),
        "blocking_readiness_evidence_ids": (),
        "created_at": "caller-supplied-created-at",
        "timestamp_policy": "caller_supplied_no_datetime_parsing",
        "source_of_truth": ("p2d-40",),
        "notes": ("structured-only",),
    }


def _explain(**overrides):
    values = _valid_values()
    values.update(overrides)
    return builder.explain_local_noop_runner_readiness_build(**values)


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
    assert builder.LOCAL_NOOP_RUNNER_READINESS_BUILD_REASON_CODES == (
        REASON_CODES
    )
    assert builder.REASON_PRIORITY == REASON_PRIORITY


def test_valid_readiness_is_buildable_with_exact_shapes():
    result = _explain()

    assert result["buildable"] is True
    assert result["reason_code"] == "LOCAL_NOOP_RUNNER_READINESS_BUILDABLE"
    assert result["readiness_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()
    assert result["readiness_evidence_item_violations"] == ()
    assert tuple(result.keys()) == RESULT_KEYS
    assert tuple(result["source"].keys()) == SOURCE_KEYS
    assert tuple(result["local_noop_runner_readiness"].keys()) == (
        LOCAL_NOOP_RUNNER_READINESS_KEYS
    )
    assert tuple(
        result["local_noop_runner_readiness"][
            "readiness_evidence_items"
        ][0].keys()
    ) == READINESS_EVIDENCE_ITEM_KEYS
    assert result["source"]["public_url"] is None
    assert result["local_noop_runner_readiness"]["public_url"] is None
    assert result["source"]["public_url_created"] is False
    assert result["local_noop_runner_readiness"]["public_url_created"] is False
    assert "public_url_is_null" not in result
    assert "public_url_is_null" not in result["source"]
    assert "public_url_is_null" not in result["local_noop_runner_readiness"]


def test_public_api_is_keyword_only_and_bool_wrapper_matches_explain():
    expected_kwonly = len(_valid_values())

    assert (
        builder.explain_local_noop_runner_readiness_build.__code__.co_argcount
        == 0
    )
    assert (
        builder.explain_local_noop_runner_readiness_build.__code__
        .co_kwonlyargcount
        == expected_kwonly
    )
    assert (
        builder.is_local_noop_runner_readiness_buildable.__code__.co_argcount
        == 0
    )
    assert (
        builder.is_local_noop_runner_readiness_buildable.__code__
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
        explanation = builder.explain_local_noop_runner_readiness_build(
            **values
        )
        assert (
            builder.is_local_noop_runner_readiness_buildable(**values)
            is explanation["buildable"]
        )


def test_required_lockin_markers_block_when_invalid():
    cases = (
        (
            {"readiness_kind": "local_noop_runner"},
            "READINESS_KIND_NOT_LOCAL_NOOP_RUNNER_READINESS",
            "readiness_kind",
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
            {"local_noop_runner_envelope_ref": ""},
            "LOCAL_NOOP_RUNNER_ENVELOPE_REF_MISSING",
            "local_noop_runner_envelope_ref",
        ),
        (
            {"local_noop_runner_envelope_buildable_marker": False},
            "LOCAL_NOOP_RUNNER_ENVELOPE_BUILDABLE_MARKER_NOT_TRUE",
            "local_noop_runner_envelope_buildable_marker",
        ),
        (
            {"local_noop_runner_envelope_buildable_marker": 1},
            "LOCAL_NOOP_RUNNER_ENVELOPE_BUILDABLE_MARKER_NOT_TRUE",
            "local_noop_runner_envelope_buildable_marker",
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
        assert reason_code in result["readiness_violations"]
        assert field in result["missing_or_invalid_fields"]


def test_pass_published_status_is_blocked_and_suppressed_from_payload():
    result = _explain(expected_terminal_status="PASS_PUBLISHED")

    assert result["reason_code"] == "PASS_PUBLISHED_FORBIDDEN"
    assert "EXPECTED_TERMINAL_STATUS_NOT_NOOP_COMPLETED" in (
        result["readiness_violations"]
    )
    assert result["source"]["expected_terminal_status"] == ""
    assert (
        result["local_noop_runner_readiness"]["expected_terminal_status"] == ""
    )


def test_public_url_created_is_blocked_and_suppressed_from_payload():
    result = _explain(public_url_created=True)

    assert result["buildable"] is False
    assert "PUBLIC_URL_CREATED_NOT_FALSE" in result["readiness_violations"]
    assert result["source"]["public_url_created"] is False
    assert result["local_noop_runner_readiness"]["public_url_created"] is False


def test_failed_evidence_status_and_known_blocking_ids_still_buildable():
    failed = _explain(
        readiness_evidence_items=(
            _readiness_evidence_item(evidence_status="failed"),
        )
    )
    blocked_known = _explain(
        blocking_readiness_evidence_ids=("readiness-evidence-001",),
        readiness_evidence_items=(
            _readiness_evidence_item(evidence_status="failed"),
        ),
    )

    assert failed["buildable"] is True
    assert blocked_known["buildable"] is True
    assert blocked_known["local_noop_runner_readiness"][
        "blocking_readiness_evidence_ids"
    ] == ("readiness-evidence-001",)


def test_unknown_blank_or_non_tuple_blocking_ids_block_buildability():
    cases = (
        ("missing-readiness-evidence",),
        ("",),
        ["readiness-evidence-001"],
    )

    for blocking_readiness_evidence_ids in cases:
        result = _explain(
            blocking_readiness_evidence_ids=blocking_readiness_evidence_ids
        )

        assert result["buildable"] is False
        assert "BLOCKING_READINESS_EVIDENCE_ID_UNKNOWN" in (
            result["readiness_violations"]
        )
        assert "blocking_readiness_evidence_ids" in (
            result["missing_or_invalid_fields"]
        )


def test_required_top_level_field_violations_are_collected():
    cases = (
        ("run_id", "", "RUN_ID_MISSING"),
        (
            "local_noop_runner_readiness_id",
            "",
            "LOCAL_NOOP_RUNNER_READINESS_ID_MISSING",
        ),
        (
            "readiness_evidence_items",
            (),
            "READINESS_EVIDENCE_ITEMS_MISSING",
        ),
        (
            "readiness_evidence_items",
            [],
            "READINESS_EVIDENCE_ITEMS_MISSING",
        ),
        (
            "required_readiness_evidence_ids",
            (),
            "REQUIRED_READINESS_EVIDENCE_IDS_MISSING",
        ),
        (
            "required_readiness_evidence_ids",
            ("",),
            "REQUIRED_READINESS_EVIDENCE_IDS_MISSING",
        ),
        (
            "required_readiness_evidence_ids",
            ["readiness-evidence-001"],
            "REQUIRED_READINESS_EVIDENCE_IDS_MISSING",
        ),
        (
            "missing_readiness_evidence_ids",
            ("readiness-evidence-002",),
            "MISSING_READINESS_EVIDENCE_IDS_DECLARED",
        ),
        (
            "missing_readiness_evidence_ids",
            [],
            "MISSING_READINESS_EVIDENCE_IDS_DECLARED",
        ),
        ("created_at", "", "CREATED_AT_MISSING"),
        ("timestamp_policy", "", "TIMESTAMP_POLICY_MISSING"),
        ("source_of_truth", (), "SOURCE_OF_TRUTH_MISSING"),
        ("source_of_truth", ("",), "SOURCE_OF_TRUTH_MISSING"),
        ("source_of_truth", ["p2d-40"], "SOURCE_OF_TRUTH_MISSING"),
    )

    for field, value, reason_code in cases:
        result = _explain(**{field: value})

        assert result["buildable"] is False
        assert reason_code in result["readiness_violations"]
        assert field in result["missing_or_invalid_fields"]


def test_readiness_evidence_id_uniqueness_required_boundary_and_presence():
    duplicate = _explain(
        readiness_evidence_items=(
            _readiness_evidence_item(),
            _readiness_evidence_item(),
        )
    )
    not_required = _explain(
        readiness_evidence_items=(
            _readiness_evidence_item(
                readiness_evidence_id="readiness-evidence-002"
            ),
        )
    )
    required_missing = _explain(
        required_readiness_evidence_ids=(
            "readiness-evidence-001",
            "readiness-evidence-002",
        )
    )

    assert "READINESS_EVIDENCE_ID_DUPLICATE" in duplicate[
        "readiness_violations"
    ]
    assert "READINESS_EVIDENCE_ID_NOT_REQUIRED" in (
        not_required["readiness_violations"]
    )
    assert "REQUIRED_READINESS_EVIDENCE_MISSING" in (
        required_missing["readiness_violations"]
    )


def test_readiness_evidence_item_fields_and_missing_keys_reported():
    cases = (
        ("readiness_evidence_id", "", "READINESS_EVIDENCE_ID_MISSING"),
        ("readiness_evidence_role", "", "READINESS_EVIDENCE_ROLE_MISSING"),
        ("artifact_ref", "", "READINESS_EVIDENCE_ARTIFACT_REF_MISSING"),
        ("artifact_kind", "", "READINESS_EVIDENCE_ARTIFACT_KIND_MISSING"),
        ("evidence_status", "", "READINESS_EVIDENCE_STATUS_MISSING"),
        ("producer_ref", "", "READINESS_EVIDENCE_PRODUCER_REF_MISSING"),
        ("evidence_refs", (), "READINESS_EVIDENCE_REFS_MISSING"),
        ("evidence_refs", ("",), "READINESS_EVIDENCE_REFS_MISSING"),
        ("evidence_refs", ["ref"], "READINESS_EVIDENCE_REFS_MISSING"),
    )
    for field, value, reason_code in cases:
        result = _explain(
            readiness_evidence_items=(
                _readiness_evidence_item(**{field: value}),
            )
        )

        assert result["buildable"] is False
        assert reason_code in result["readiness_violations"]
        assert f"readiness_evidence_items[0].{field}" in (
            result["missing_or_invalid_fields"]
        )
        assert tuple(
            result["readiness_evidence_item_violations"][0].keys()
        ) == READINESS_EVIDENCE_ITEM_VIOLATION_KEYS

    for missing_key, reason_code in MISSING_READINESS_EVIDENCE_ITEM_KEY_EXPECTATIONS:
        readiness_evidence_item = _readiness_evidence_item()
        del readiness_evidence_item[missing_key]
        result = _explain(readiness_evidence_items=(readiness_evidence_item,))

        assert result["buildable"] is False
        assert "READINESS_EVIDENCE_ITEM_KEYS_INVALID" in (
            result["readiness_violations"]
        )
        assert reason_code in result["readiness_violations"]
        assert f"readiness_evidence_items[0].{missing_key}" in (
            result["missing_or_invalid_fields"]
        )
        assert "readiness_evidence_items[0].keys" in (
            result["missing_or_invalid_fields"]
        )


def test_non_dict_readiness_evidence_item_records_violation_shape():
    result = _explain(readiness_evidence_items=("not-evidence",))

    assert result["buildable"] is False
    assert "READINESS_EVIDENCE_ITEM_NOT_DICT" in result["readiness_violations"]
    assert tuple(result["readiness_evidence_item_violations"][0].keys()) == (
        READINESS_EVIDENCE_ITEM_VIOLATION_KEYS
    )
    assert result["local_noop_runner_readiness"][
        "readiness_evidence_items"
    ] == (
        {
            "readiness_evidence_id": "",
            "readiness_evidence_role": "",
            "artifact_ref": "",
            "artifact_kind": "",
            "evidence_status": "",
            "producer_ref": "",
            "evidence_refs": (),
            "notes": (),
        },
    )


def test_forbidden_raw_execution_cli_url_and_publication_fields_are_suppressed():
    for field in FORBIDDEN_READINESS_EVIDENCE_ITEM_FIELDS:
        result = _explain(
            readiness_evidence_items=(
                _readiness_evidence_item(**{field: "forbidden"}),
            )
        )

        assert result["buildable"] is False
        assert "READINESS_EVIDENCE_ITEM_KEYS_INVALID" in (
            result["readiness_violations"]
        )
        assert "READINESS_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT" in (
            result["readiness_violations"]
        )
        assert f"readiness_evidence_items[0].{field}" in (
            result["missing_or_invalid_fields"]
        )
        assert field not in (
            result["local_noop_runner_readiness"][
                "readiness_evidence_items"
            ][0]
        )
        assert tuple(
            result["readiness_evidence_item_violations"][0].keys()
        ) == READINESS_EVIDENCE_ITEM_VIOLATION_KEYS


def test_output_does_not_expose_public_url_is_null_or_extra_url_values():
    result = _explain()
    forbidden_url = _explain(
        readiness_evidence_items=(
            _readiness_evidence_item(public_url_value="https://example.test"),
        )
    )
    payload_keys = _payload_keys(result)
    forbidden_payload_keys = _payload_keys(forbidden_url)

    assert "public_url_is_null" not in payload_keys
    assert result["source"]["public_url"] is None
    assert result["local_noop_runner_readiness"]["public_url"] is None
    assert "public_url_value" not in forbidden_payload_keys
    assert forbidden_url["source"]["public_url"] is None
    assert forbidden_url["local_noop_runner_readiness"]["public_url"] is None


def test_no_ready_runnable_executable_or_execution_success_names():
    result = _explain()
    payload_keys = _payload_keys(result)

    assert "buildable" in payload_keys
    for success_name in FORBIDDEN_SUCCESS_NAMES:
        assert success_name not in payload_keys


def test_reason_catalog_priority_and_forbidden_pseudo_reason_codes():
    assert builder.REASON_CODES == REASON_CODES
    assert builder.LOCAL_NOOP_RUNNER_READINESS_BUILD_REASON_CODES == (
        REASON_CODES
    )
    assert builder.REASON_PRIORITY == REASON_PRIORITY

    for reason_code in FORBIDDEN_PSEUDO_REASON_CODES:
        assert reason_code not in builder.REASON_CODES
        assert reason_code not in builder.REASON_PRIORITY


def test_forbidden_module_namespace_and_io_names_are_absent():
    for module_name in FORBIDDEN_MODULE_NAMES:
        assert not hasattr(builder, module_name)


def test_all_violations_are_priority_ordered_and_details_present():
    first_item = _readiness_evidence_item(
        readiness_evidence_id="",
        readiness_evidence_role="",
        artifact_ref="",
        artifact_kind="",
        evidence_status="",
        producer_ref="",
        evidence_refs=(),
        raw_artifact_content="raw",
    )
    second_item = _readiness_evidence_item(
        readiness_evidence_id="extra-evidence"
    )
    result = _explain(
        run_id="",
        local_noop_runner_readiness_id="",
        readiness_kind="wrong",
        mode="real",
        expected_terminal_status="PASS_PUBLISHED",
        local_noop_runner_envelope_ref="",
        local_noop_runner_envelope_buildable_marker=False,
        public_url_is_null=False,
        public_url_created=True,
        readiness_evidence_items=(first_item, second_item),
        required_readiness_evidence_ids=(
            "readiness-evidence-001",
            "readiness-evidence-002",
        ),
        missing_readiness_evidence_ids=("readiness-evidence-002",),
        blocking_readiness_evidence_ids=("missing-block",),
        created_at="",
        timestamp_policy="",
        source_of_truth=(),
    )
    expected_order = tuple(
        reason_code
        for reason_code in REASON_PRIORITY
        if reason_code != "LOCAL_NOOP_RUNNER_READINESS_BUILDABLE"
        and reason_code in result["readiness_violations"]
    )

    assert result["readiness_violations"] == expected_order
    assert result["reason_code"] == result["readiness_violations"][0]
    assert "readiness_evidence_items[0].raw_artifact_content" in (
        result["missing_or_invalid_fields"]
    )
    assert "readiness_evidence_items[1].readiness_evidence_id" in (
        result["missing_or_invalid_fields"]
    )
    assert (
        "required_readiness_evidence_ids.readiness-evidence-002"
        in result["missing_or_invalid_fields"]
    )
    assert result["readiness_evidence_item_violations"] != ()
    for violation in result["readiness_evidence_item_violations"]:
        assert tuple(violation.keys()) == (
            READINESS_EVIDENCE_ITEM_VIOLATION_KEYS
        )


def test_invariant_refs_capture_governance_and_no_execution_boundaries():
    result = _explain()

    assert result["invariant_refs"] == REQUIRED_INVARIANT_REFS


def test_payload_key_traversal_skips_invariants_instead_of_blanket_scans():
    result = _explain()
    payload_keys = _payload_keys(result)

    assert "no_p2d39_envelope_read" in result["invariant_refs"]
    assert "no_public_url_behavior" in result["invariant_refs"]
    assert "buildable_not_ready" in result["invariant_refs"]
    assert "buildable_not_execution_ready" in result["invariant_refs"]
    assert "buildable_not_runnable" in result["invariant_refs"]
    assert "buildable_not_executable" in result["invariant_refs"]
    assert "local_noop_runner_readiness_not_runner_execution" in (
        result["invariant_refs"]
    )
    assert "local_noop_runner_readiness_not_runtime_execution" in (
        result["invariant_refs"]
    )
    assert "local_noop_runner_readiness_not_command_execution" in (
        result["invariant_refs"]
    )
    assert "local_noop_runner_readiness_not_subprocess_execution" in (
        result["invariant_refs"]
    )
    assert "no_runner_execution" in result["invariant_refs"]
    assert "no_runtime_execution" in result["invariant_refs"]
    assert "no_command_execution" in result["invariant_refs"]
    assert "no_subprocess_execution" in result["invariant_refs"]
    assert "no_run_ledger_yaml_write" in result["invariant_refs"]
    assert "public_url" in payload_keys
    assert result["source"]["public_url"] is None
    assert result["local_noop_runner_readiness"]["public_url"] is None
    assert "no_raw_url" not in payload_keys
    assert "no_public_url_behavior" not in payload_keys
    assert "buildable_not_ready" not in payload_keys
    assert "buildable_not_runnable" not in payload_keys
