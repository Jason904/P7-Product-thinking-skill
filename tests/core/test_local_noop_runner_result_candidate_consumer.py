"""Tests for the pure in-memory local noop result candidate consumer."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import (  # noqa: E402
    local_noop_runner_result_candidate_consumer as consumer,
)


RESULT_KEYS = (
    "consumed",
    "reason_code",
    "reason",
    "source",
    "normalized_local_noop_runner_result_candidate",
    "local_noop_runner_consumption_receipt",
    "consumption_violations",
    "missing_or_invalid_fields",
    "result_candidate_evidence_item_violations",
    "invariant_refs",
)

OUTPUT_SOURCE_KEYS = (
    "p2d41_assembled",
    "p2d41_reason_code",
    "local_noop_runner_result_candidate_id",
    "candidate_kind",
    "mode",
    "public_url",
    "public_url_created",
    "source_of_truth",
)

ROOT_KEYS = (
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

CANDIDATE_KEYS = (
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

EVIDENCE_ITEM_KEYS = (
    "result_candidate_evidence_id",
    "result_candidate_evidence_role",
    "artifact_ref",
    "artifact_kind",
    "evidence_status",
    "producer_ref",
    "evidence_refs",
    "notes",
)

RECEIPT_KEYS = (
    "receipt_kind",
    "consumption_scope",
    "run_id",
    "local_noop_runner_result_candidate_id",
    "candidate_kind",
    "mode",
    "public_url",
    "public_url_created",
)

EVIDENCE_VIOLATION_KEYS = (
    "result_candidate_evidence_item_index",
    "result_candidate_evidence_id",
    "reason_code",
    "field",
)

REASON_CODES = (
    "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_CONSUMED_IN_MEMORY",
    "CANDIDATE_ASSEMBLY_NOT_DICT",
    "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
    "CANDIDATE_ASSEMBLY_KEYS_INVALID",
    "P2D41_ASSEMBLED_MARKER_NOT_TRUE",
    "P2D41_ASSEMBLY_REASON_CODE_INVALID",
    "P2D41_ASSEMBLY_REASON_MISSING",
    "P2D41_ASSEMBLY_VIOLATIONS_NOT_EMPTY",
    "P2D41_MISSING_OR_INVALID_FIELDS_NOT_EMPTY",
    "P2D41_EVIDENCE_ITEM_VIOLATIONS_NOT_EMPTY",
    "P2D41_INVARIANT_REFS_INVALID",
    "P2D41_REQUIRED_INVARIANT_REF_MISSING",
    "P2D41_SOURCE_NOT_DICT",
    "P2D41_SOURCE_KEYS_INVALID",
    "P2D41_RESULT_CANDIDATE_NOT_DICT",
    "P2D41_RESULT_CANDIDATE_KEYS_INVALID",
    "RUN_ID_MISSING",
    "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_ID_MISSING",
    "CANDIDATE_KIND_NOT_LOCAL_NOOP_RUNNER_RESULT_CANDIDATE",
    "MODE_NOT_NOOP",
    "PASS_PUBLISHED_FORBIDDEN",
    "RUNNER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
    "LOCAL_NOOP_RUNNER_READINESS_REF_MISSING",
    "LOCAL_NOOP_RUNNER_READINESS_ID_MISSING",
    "LOCAL_NOOP_RUNNER_READINESS_BUILDABLE_MARKER_NOT_TRUE",
    "PUBLIC_URL_NOT_NULL",
    "PUBLIC_URL_CREATED_NOT_FALSE",
    "P2D41_SOURCE_CANDIDATE_MISMATCH",
    "RESULT_CANDIDATE_EVIDENCE_ITEMS_MISSING",
    "REQUIRED_RESULT_CANDIDATE_EVIDENCE_IDS_MISSING",
    "MISSING_RESULT_CANDIDATE_EVIDENCE_IDS_DECLARED",
    "BLOCKING_RESULT_CANDIDATE_EVIDENCE_ID_UNKNOWN",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "NOTES_INVALID",
    "RESULT_CANDIDATE_EVIDENCE_ITEM_NOT_DICT",
    "RESULT_CANDIDATE_EVIDENCE_ITEM_KEYS_INVALID",
    "RESULT_CANDIDATE_EVIDENCE_ID_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_ROLE_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_ARTIFACT_REF_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_ARTIFACT_KIND_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_STATUS_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_PRODUCER_REF_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_REFS_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_NOTES_INVALID",
    "RESULT_CANDIDATE_EVIDENCE_ID_DUPLICATE",
    "RESULT_CANDIDATE_EVIDENCE_ID_NOT_REQUIRED",
    "REQUIRED_RESULT_CANDIDATE_EVIDENCE_MISSING",
)

REASON_PRIORITY = (
    "CANDIDATE_ASSEMBLY_NOT_DICT",
    "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
    "CANDIDATE_ASSEMBLY_KEYS_INVALID",
    "P2D41_ASSEMBLED_MARKER_NOT_TRUE",
    "P2D41_ASSEMBLY_REASON_CODE_INVALID",
    "P2D41_ASSEMBLY_REASON_MISSING",
    "P2D41_ASSEMBLY_VIOLATIONS_NOT_EMPTY",
    "P2D41_MISSING_OR_INVALID_FIELDS_NOT_EMPTY",
    "P2D41_EVIDENCE_ITEM_VIOLATIONS_NOT_EMPTY",
    "P2D41_INVARIANT_REFS_INVALID",
    "P2D41_REQUIRED_INVARIANT_REF_MISSING",
    "P2D41_SOURCE_NOT_DICT",
    "P2D41_SOURCE_KEYS_INVALID",
    "P2D41_RESULT_CANDIDATE_NOT_DICT",
    "P2D41_RESULT_CANDIDATE_KEYS_INVALID",
    "RUN_ID_MISSING",
    "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_ID_MISSING",
    "CANDIDATE_KIND_NOT_LOCAL_NOOP_RUNNER_RESULT_CANDIDATE",
    "MODE_NOT_NOOP",
    "PASS_PUBLISHED_FORBIDDEN",
    "RUNNER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
    "LOCAL_NOOP_RUNNER_READINESS_REF_MISSING",
    "LOCAL_NOOP_RUNNER_READINESS_ID_MISSING",
    "LOCAL_NOOP_RUNNER_READINESS_BUILDABLE_MARKER_NOT_TRUE",
    "PUBLIC_URL_NOT_NULL",
    "PUBLIC_URL_CREATED_NOT_FALSE",
    "P2D41_SOURCE_CANDIDATE_MISMATCH",
    "RESULT_CANDIDATE_EVIDENCE_ITEMS_MISSING",
    "REQUIRED_RESULT_CANDIDATE_EVIDENCE_IDS_MISSING",
    "MISSING_RESULT_CANDIDATE_EVIDENCE_IDS_DECLARED",
    "BLOCKING_RESULT_CANDIDATE_EVIDENCE_ID_UNKNOWN",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "NOTES_INVALID",
    "RESULT_CANDIDATE_EVIDENCE_ITEM_NOT_DICT",
    "RESULT_CANDIDATE_EVIDENCE_ITEM_KEYS_INVALID",
    "RESULT_CANDIDATE_EVIDENCE_ID_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_ROLE_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_ARTIFACT_REF_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_ARTIFACT_KIND_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_STATUS_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_PRODUCER_REF_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_REFS_MISSING",
    "RESULT_CANDIDATE_EVIDENCE_NOTES_INVALID",
    "RESULT_CANDIDATE_EVIDENCE_ID_DUPLICATE",
    "RESULT_CANDIDATE_EVIDENCE_ID_NOT_REQUIRED",
    "REQUIRED_RESULT_CANDIDATE_EVIDENCE_MISSING",
    "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_CONSUMED_IN_MEMORY",
)

REQUIRED_P2D41_INVARIANT_REFS = (
    "local_noop_runner_result_assembler_only",
    "assembled_not_consumed",
    "local_noop_runner_result_candidate_governance_evidence_bundle",
    "result_candidate_evidence_status_is_caller_supplied",
    "mode_noop_required",
    "public_url_must_be_null",
    "public_url_created_must_be_false",
    "runner_terminal_status_must_be_noop_completed",
    "noop_completed_not_pass_published",
    "pass_published_forbidden",
    "no_existing_builder_or_policy_call",
    "no_runner_execution",
    "no_runtime_execution",
    "no_ledger_write",
    "no_quality_pass_no_public_url",
)

INVARIANT_REFS = (
    "local_noop_runner_result_candidate_consumer_only",
    "consumer_pure_in_memory_only",
    "consumer_accepts_full_p2d41_assembly",
    "consumer_rejects_nested_candidate_bypass",
    "full_p2d41_wrapper_requires_assembled_true",
    "full_p2d41_wrapper_requires_empty_violations",
    "consume_means_validate_and_normalize_only",
    "consumed_true_means_accepted_and_normalized_in_memory_only",
    "caller_input_not_mutated",
    "source_candidate_lockins_must_match",
    "unknown_keys_block_and_are_suppressed",
    "forbidden_fields_block_and_are_suppressed",
    "recursive_key_scan_does_not_scan_string_values",
    "normalized_candidate_returned_only_when_consumed",
    "consumption_receipt_returned_only_when_consumed",
    "consumption_receipt_not_runner_result",
    "consumed_not_runner_execution",
    "consumed_not_runtime_execution",
    "consumed_not_adapter_execution",
    "consumed_not_scheduler_execution",
    "consumed_not_cli_execution",
    "consumed_not_manual_execution",
    "consumed_not_argument_parsing",
    "consumed_not_command_execution",
    "consumed_not_subprocess_execution",
    "consumed_not_dry_run_execution",
    "consumed_not_e2e_execution",
    "consumed_not_noop_completion_execution",
    "consumed_not_state_transition",
    "consumed_not_gate_decision",
    "consumed_not_policy_execution",
    "consumed_not_runner_result_created",
    "consumed_not_noop_completed_achievement",
    "consumed_not_quality_pass",
    "consumed_not_eval_pass",
    "consumed_not_audit_pass",
    "consumed_not_gate_pass",
    "consumed_not_publish_allowed",
    "consumed_not_pass_published",
    "consumed_not_public_url_created",
    "consumed_not_ledger_written",
    "consumed_not_notification_sent",
    "no_sibling_module_import",
    "no_prior_builder_or_policy_call",
    "no_file_read",
    "no_artifact_read",
    "no_config_env_credentials_read",
    "no_web_github_rss_notion_access",
    "no_llm_summary_or_judge",
    "no_run_ledger_yaml_read",
    "no_run_ledger_yaml_write",
    "no_publish",
    "no_notification",
    "mode_noop_required",
    "public_url_must_be_null",
    "public_url_created_must_be_false",
    "normalized_runner_terminal_status_must_be_noop_completed",
    "noop_completed_is_declarative_input_only",
    "noop_completed_not_pass_published",
    "pass_published_forbidden",
    "evidence_status_opaque_except_pass_published",
    "failed_evidence_status_may_be_consumed",
    "known_blocking_evidence_ids_are_evidence_only",
    "unknown_blocking_evidence_ids_block_consumption",
    "no_quality_pass_no_public_url",
)

BLOCKED_SOURCE = {
    "p2d41_assembled": False,
    "p2d41_reason_code": "",
    "local_noop_runner_result_candidate_id": "",
    "candidate_kind": "",
    "mode": "",
    "public_url": None,
    "public_url_created": False,
    "source_of_truth": (),
}

FORBIDDEN_POSITIVE_FIELDS = (
    "accepted",
    "normalized",
    "executed",
    "completed",
    "noop_completed",
    "runner_result_created",
    "runtime_started",
    "runner_executed",
    "execution_performed",
    "execution_ready",
    "runnable",
    "executable",
    "invocation_ready",
    "quality_pass",
    "validator_pass",
    "rubric_pass",
    "audit_pass",
    "eval_pass",
    "gate_pass",
    "publish_allowed",
    "pass_published",
    "published",
    "notified",
    "ledger_written",
)

FORBIDDEN_EXACT_INPUT_KEYS = (
    "accepted",
    "consumed",
    "normalized",
    "executed",
    "completed",
    "noop_completed",
    "runner_result_created",
    "runtime_started",
    "runner_executed",
    "execution_performed",
    "execution_ready",
    "runnable",
    "executable",
    "invocation_ready",
    "quality_pass",
    "validator_pass",
    "rubric_pass",
    "audit_pass",
    "eval_pass",
    "gate_pass",
    "publish_allowed",
    "pass_published",
    "published",
    "notified",
    "ledger_written",
    "public_url_value",
    "publish_url",
    "deployment_url",
    "real_url",
    "live_url",
    "public_url_behavior",
    "command",
    "raw_command",
    "shell_command",
    "argv",
    "args",
    "parsed_args",
    "stdout",
    "stderr",
    "exit_code",
    "argparse_namespace",
    "click_context",
    "typer_app",
    "console_script",
    "entrypoint",
    "entry_point",
    "process_result",
    "human_confirmation_result",
    "human_approval_result",
    "operator_action_result",
    "content",
    "path",
    "file_path",
    "local_path",
    "credentials",
    "env_vars",
    "config",
    "prompt",
    "generated_summary",
)

FORBIDDEN_INPUT_PREFIXES = (
    "should_",
    "raw_",
    "full_",
    "runner_execution_",
    "runtime_",
    "adapter_",
    "scheduler_",
    "cli_",
    "command_",
    "subprocess_",
    "dry_run_",
    "e2e_",
    "noop_completion_",
    "transition_",
    "gate_execution_",
    "policy_execution_",
    "validator_execution_",
    "audit_execution_",
    "eval_",
    "publish_",
    "notification_",
    "ledger_",
    "run_ledger_",
    "web_",
    "github_",
    "rss_",
    "notion_",
    "llm_",
    "model_",
    "artifact_reader_",
    "source_fetch_",
)

FORBIDDEN_INPUT_SUFFIXES = (
    "_content",
    "_path",
    "_payload",
    "_command",
    "_output",
    "_result",
    "_read",
    "_write",
    "_written",
    "_executed",
    "_execution_result",
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
    "local_noop_runner_result_assembler",
    "local_noop_runner_result_builder",
    "local_noop_runner_readiness_builder",
    "local_noop_runner_envelope_builder",
    "noop_completion_policy",
    "transition_guard",
    "gate_decision_mapper",
)

_DEFAULT_ASSEMBLY = object()


def _evidence_item(**overrides):
    values = {
        "result_candidate_evidence_id": "result-candidate-evidence-001",
        "result_candidate_evidence_role": "local_noop_runner_readiness",
        "artifact_ref": "local-noop-runner-readiness-001",
        "artifact_kind": "local_noop_runner_readiness",
        "evidence_status": "passed",
        "producer_ref": "caller-supplied-result-candidate",
        "evidence_refs": ("local-noop-runner-readiness-001#noop",),
        "notes": ("caller-supplied-evidence-only",),
    }
    values.update(overrides)
    return values


def _candidate(**overrides):
    values = {
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
        "public_url": None,
        "public_url_created": False,
        "result_candidate_evidence_items": (_evidence_item(),),
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
    values.update(overrides)
    return values


def _source(candidate):
    return {
        "mode": candidate["mode"],
        "runner_terminal_status": candidate["runner_terminal_status"],
        "local_noop_runner_readiness_ref": candidate[
            "local_noop_runner_readiness_ref"
        ],
        "local_noop_runner_readiness_id": candidate[
            "local_noop_runner_readiness_id"
        ],
        "local_noop_runner_readiness_buildable_marker": candidate[
            "local_noop_runner_readiness_buildable_marker"
        ],
        "public_url": candidate["public_url"],
        "public_url_created": candidate["public_url_created"],
        "source_of_truth": candidate["source_of_truth"],
    }


def _valid_assembly():
    candidate = _candidate()
    return {
        "assembled": True,
        "reason_code": "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_ASSEMBLED",
        "reason": "Caller-supplied P2D-41 assembly succeeded.",
        "source": _source(candidate),
        "local_noop_runner_result_candidate": candidate,
        "assembly_violations": (),
        "missing_or_invalid_fields": (),
        "result_candidate_evidence_item_violations": (),
        "invariant_refs": REQUIRED_P2D41_INVARIANT_REFS,
    }


def _consume(assembly=_DEFAULT_ASSEMBLY):
    if assembly is _DEFAULT_ASSEMBLY:
        assembly = _valid_assembly()
    return consumer.consume_local_noop_runner_result_candidate(
        local_noop_runner_result_candidate_assembly=assembly,
    )


def _assert_blocked_safe(result):
    assert result["consumed"] is False
    assert tuple(result.keys()) == RESULT_KEYS
    assert isinstance(result["reason"], str)
    assert result["reason"].strip() != ""
    assert result["consumption_violations"] != ()
    assert result["source"] == BLOCKED_SOURCE
    assert result["normalized_local_noop_runner_result_candidate"] == {}
    assert result["local_noop_runner_consumption_receipt"] == {}
    assert result["invariant_refs"] == INVARIANT_REFS


def _assert_evidence_violation(
    result,
    *,
    reason_code,
    index,
    evidence_id,
    field,
):
    violations = result["result_candidate_evidence_item_violations"]
    assert violations != ()
    assert {
        "result_candidate_evidence_item_index": index,
        "result_candidate_evidence_id": evidence_id,
        "reason_code": reason_code,
        "field": field,
    } in violations
    for violation in violations:
        assert tuple(violation.keys()) == EVIDENCE_VIOLATION_KEYS


def _payload_keys(value, skip_invariants=True):
    keys = ()
    if isinstance(value, dict):
        for key, nested in value.items():
            keys = keys + (key,)
            if not (skip_invariants and key == "invariant_refs"):
                keys = keys + _payload_keys(nested, skip_invariants)
    elif isinstance(value, tuple) or isinstance(value, list):
        for nested in value:
            keys = keys + _payload_keys(nested, skip_invariants)
    return keys


def _all_scalar_strings(value, skip_invariants=True):
    strings = ()
    if isinstance(value, dict):
        for key, nested in value.items():
            if skip_invariants and key == "invariant_refs":
                continue
            strings = strings + _all_scalar_strings(nested, skip_invariants)
    elif isinstance(value, tuple) or isinstance(value, list):
        for nested in value:
            strings = strings + _all_scalar_strings(nested, skip_invariants)
    elif isinstance(value, str):
        strings = strings + (value,)
    return strings


def test_reason_code_constants_are_exact_and_stably_prioritized():
    assert consumer.REASON_CODES == REASON_CODES
    assert (
        consumer.LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_CONSUMPTION_REASON_CODES
        == REASON_CODES
    )
    assert consumer.REASON_PRIORITY == REASON_PRIORITY


def test_valid_full_wrapper_consumes_with_exact_shapes():
    assembly = _valid_assembly()
    result = _consume(assembly)
    candidate = result["normalized_local_noop_runner_result_candidate"]
    receipt = result["local_noop_runner_consumption_receipt"]

    assert result["consumed"] is True
    assert result["reason_code"] == (
        "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_CONSUMED_IN_MEMORY"
    )
    assert result["consumption_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()
    assert result["result_candidate_evidence_item_violations"] == ()
    assert tuple(result.keys()) == RESULT_KEYS
    assert tuple(result["source"].keys()) == OUTPUT_SOURCE_KEYS
    assert tuple(candidate.keys()) == CANDIDATE_KEYS
    assert tuple(candidate["result_candidate_evidence_items"][0].keys()) == (
        EVIDENCE_ITEM_KEYS
    )
    assert tuple(receipt.keys()) == RECEIPT_KEYS
    assert candidate == assembly["local_noop_runner_result_candidate"]
    assert candidate is not assembly["local_noop_runner_result_candidate"]
    assert receipt == {
        "receipt_kind": (
            "local_noop_runner_result_candidate_consumption_receipt"
        ),
        "consumption_scope": (
            "pure_in_memory_validation_and_normalization_only"
        ),
        "run_id": "run-001",
        "local_noop_runner_result_candidate_id": (
            "local-noop-runner-result-candidate-001"
        ),
        "candidate_kind": "local_noop_runner_result_candidate",
        "mode": "noop",
        "public_url": None,
        "public_url_created": False,
    }


def test_success_source_and_receipt_have_only_approved_meaning():
    result = _consume()
    source = result["source"]
    receipt = result["local_noop_runner_consumption_receipt"]

    assert source == {
        "p2d41_assembled": True,
        "p2d41_reason_code": (
            "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_ASSEMBLED"
        ),
        "local_noop_runner_result_candidate_id": (
            "local-noop-runner-result-candidate-001"
        ),
        "candidate_kind": "local_noop_runner_result_candidate",
        "mode": "noop",
        "public_url": None,
        "public_url_created": False,
        "source_of_truth": ("p2d-41",),
    }
    assert receipt["receipt_kind"] == (
        "local_noop_runner_result_candidate_consumption_receipt"
    )
    assert receipt["consumption_scope"] == (
        "pure_in_memory_validation_and_normalization_only"
    )
    for forbidden_key in (
        "runner_terminal_status",
        "completed",
        "executed",
        "runner_result",
        "result_kind",
        "local_noop_runner_result_id",
        "created_at",
        "ledger_written",
        "published",
        "notified",
    ):
        assert forbidden_key not in receipt


def test_input_is_not_mutated_and_output_dicts_are_fresh():
    assembly = _valid_assembly()
    expected = _valid_assembly()
    candidate = assembly["local_noop_runner_result_candidate"]
    evidence_item = candidate["result_candidate_evidence_items"][0]

    result = _consume(assembly)
    normalized = result["normalized_local_noop_runner_result_candidate"]

    assert assembly == expected
    assert normalized is not candidate
    assert normalized["result_candidate_evidence_items"][0] is not evidence_item
    assert result["source"] is not assembly["source"]


def test_public_api_is_keyword_only_and_bool_wrapper_matches():
    public_functions = tuple(
        name
        for name, value in consumer.__dict__.items()
        if not name.startswith("_")
        and callable(value)
        and getattr(value, "__module__", None) == consumer.__name__
    )
    assert public_functions == (
        "consume_local_noop_runner_result_candidate",
        "is_local_noop_runner_result_candidate_consumed",
    )
    assert (
        consumer.consume_local_noop_runner_result_candidate.__code__.co_argcount
        == 0
    )
    assert (
        consumer.consume_local_noop_runner_result_candidate.__code__
        .co_kwonlyargcount
        == 1
    )
    assert (
        consumer.is_local_noop_runner_result_candidate_consumed.__code__
        .co_argcount
        == 0
    )
    assert (
        consumer.is_local_noop_runner_result_candidate_consumed.__code__
        .co_kwonlyargcount
        == 1
    )
    for assembly in (
        _valid_assembly(),
        {**_valid_assembly(), "assembled": False},
        {**_valid_assembly(), "reason_code": "wrong"},
    ):
        result = _consume(assembly)
        assert (
            consumer.is_local_noop_runner_result_candidate_consumed(
                local_noop_runner_result_candidate_assembly=assembly,
            )
            is result["consumed"]
        )


def test_input_mapping_order_is_irrelevant_and_output_order_is_fixed():
    assembly = _valid_assembly()
    candidate = assembly["local_noop_runner_result_candidate"]
    evidence_item = candidate["result_candidate_evidence_items"][0]
    assembly["source"] = {
        key: assembly["source"][key] for key in reversed(SOURCE_KEYS)
    }
    candidate["result_candidate_evidence_items"] = (
        {key: evidence_item[key] for key in reversed(EVIDENCE_ITEM_KEYS)},
    )
    assembly["local_noop_runner_result_candidate"] = {
        key: candidate[key] for key in reversed(CANDIDATE_KEYS)
    }
    assembly = {key: assembly[key] for key in reversed(ROOT_KEYS)}

    result = _consume(assembly)

    assert result["consumed"] is True
    assert tuple(result.keys()) == RESULT_KEYS
    assert tuple(result["source"].keys()) == OUTPUT_SOURCE_KEYS
    assert tuple(
        result["normalized_local_noop_runner_result_candidate"].keys()
    ) == CANDIDATE_KEYS


def test_non_dict_input_blocks_with_fixed_safe_projection():
    for value in (None, (), [], "assembly"):
        result = _consume(value)
        _assert_blocked_safe(result)
        assert result["reason_code"] == "CANDIDATE_ASSEMBLY_NOT_DICT"


def test_nested_candidate_only_blocks_as_invalid_assembly_keys():
    result = _consume(_candidate())

    _assert_blocked_safe(result)
    assert result["reason_code"] == "CANDIDATE_ASSEMBLY_KEYS_INVALID"
    assert "CANDIDATE_ASSEMBLY_KEYS_INVALID" in result[
        "consumption_violations"
    ]


def test_unknown_keys_block_at_every_declared_mapping_level():
    assemblies = []

    root = _valid_assembly()
    root["unknown_root"] = "not-echoed"
    assemblies.append((root, "CANDIDATE_ASSEMBLY_KEYS_INVALID"))

    source = _valid_assembly()
    source["source"]["unknown_source"] = "not-echoed"
    assemblies.append((source, "P2D41_SOURCE_KEYS_INVALID"))

    candidate = _valid_assembly()
    candidate["local_noop_runner_result_candidate"][
        "unknown_candidate"
    ] = "not-echoed"
    assemblies.append((candidate, "P2D41_RESULT_CANDIDATE_KEYS_INVALID"))

    evidence = _valid_assembly()
    evidence["local_noop_runner_result_candidate"][
        "result_candidate_evidence_items"
    ][0]["unknown_evidence"] = "not-echoed"
    assemblies.append(
        (evidence, "RESULT_CANDIDATE_EVIDENCE_ITEM_KEYS_INVALID")
    )

    for assembly, expected_reason in assemblies:
        result = _consume(assembly)
        _assert_blocked_safe(result)
        assert expected_reason in result["consumption_violations"]


def test_recursive_forbidden_keys_and_normalized_variants_block():
    forbidden_keys = (
        "runtime_result",
        "Runtime-Result",
        " should publish ",
        "raw-content",
        "ledger_write",
        "cli_command",
        "model_output",
    )
    for forbidden_key in forbidden_keys:
        assembly = _valid_assembly()
        assembly["extra_container"] = (
            [{forbidden_key: "caller-value"}],
        )
        result = _consume(assembly)
        _assert_blocked_safe(result)
        assert "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT" in result[
            "consumption_violations"
        ]


def test_every_minimum_forbidden_exact_prefix_and_suffix_blocks():
    forbidden_keys = FORBIDDEN_EXACT_INPUT_KEYS + tuple(
        prefix + "caller_claim" for prefix in FORBIDDEN_INPUT_PREFIXES
    ) + tuple(
        "caller_claim" + suffix for suffix in FORBIDDEN_INPUT_SUFFIXES
    )
    for forbidden_key in forbidden_keys:
        assembly = _valid_assembly()
        assembly[forbidden_key] = "caller-value"
        result = _consume(assembly)
        _assert_blocked_safe(result)
        assert result["reason_code"] == (
            "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"
        )


def test_raw_forbidden_key_is_suppressed_by_fixed_safe_diagnostics():
    assembly = _valid_assembly()
    assembly["Raw Evil-Key"] = "caller-value"

    result = _consume(assembly)

    _assert_blocked_safe(result)
    assert result["reason_code"] == (
        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"
    )
    assert "CANDIDATE_ASSEMBLY_KEYS_INVALID" in result[
        "consumption_violations"
    ]
    assert result["missing_or_invalid_fields"].count(
        "candidate_assembly.forbidden_field_or_namespace"
    ) == 1
    assert "candidate_assembly.keys" in result["missing_or_invalid_fields"]
    for output_string in _all_scalar_strings(result):
        assert "Raw Evil-Key" not in output_string
        assert "raw_evil_key" not in output_string


def test_unknown_parent_and_nested_forbidden_keys_are_suppressed():
    nested_values = (
        {"raw-command": "caller-value"},
        [{"raw-command": "caller-value"}],
        ({"raw-command": "caller-value"},),
    )
    caller_tokens = (
        "Unknown Parent",
        "unknown_parent",
        "raw-command",
        "raw_command",
    )

    for nested_value in nested_values:
        assembly = _valid_assembly()
        assembly["Unknown Parent"] = nested_value

        result = _consume(assembly)

        _assert_blocked_safe(result)
        assert "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT" in result[
            "consumption_violations"
        ]
        assert "CANDIDATE_ASSEMBLY_KEYS_INVALID" in result[
            "consumption_violations"
        ]
        assert result["missing_or_invalid_fields"].count(
            "candidate_assembly.forbidden_field_or_namespace"
        ) == 1
        assert "candidate_assembly.keys" in result[
            "missing_or_invalid_fields"
        ]
        for output_string in _all_scalar_strings(result):
            for caller_token in caller_tokens:
                assert caller_token not in output_string


def test_declared_schema_key_at_wrong_path_blocks():
    wrong_path_items = (
        {"public_url": None},
        {"assembled": True},
        {"runner_terminal_status": "NOOP_COMPLETED"},
        {"artifact_ref": "opaque-ref"},
    )
    for wrong_path_item in wrong_path_items:
        assembly = _valid_assembly()
        assembly["local_noop_runner_result_candidate"]["notes"] = (
            wrong_path_item,
        )
        result = _consume(assembly)
        _assert_blocked_safe(result)
        assert "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT" in result[
            "consumption_violations"
        ]
        assert "NOTES_INVALID" in result["consumption_violations"]


def test_legitimate_schema_paths_do_not_false_positive():
    result = _consume()

    assert result["consumed"] is True
    assert "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT" not in result[
        "consumption_violations"
    ]


def test_scalar_string_contents_are_not_scanned_for_fields_or_statuses():
    assembly = _valid_assembly()
    candidate = assembly["local_noop_runner_result_candidate"]
    evidence_item = candidate["result_candidate_evidence_items"][0]
    opaque = (
        "PASS_PUBLISHED runtime_result should_publish public_url live_url"
    )
    assembly["reason"] = opaque
    candidate["notes"] = (opaque,)
    candidate["source_of_truth"] = (opaque,)
    assembly["source"]["source_of_truth"] = (opaque,)
    evidence_item["notes"] = (opaque,)
    evidence_item["evidence_refs"] = (opaque,)
    assembly["invariant_refs"] = REQUIRED_P2D41_INVARIANT_REFS + (opaque,)

    result = _consume(assembly)

    assert result["consumed"] is True
    assert result["consumption_violations"] == ()


def test_wrapper_success_markers_and_empty_details_are_required():
    cases = (
        ("assembled", False, "P2D41_ASSEMBLED_MARKER_NOT_TRUE"),
        ("assembled", 1, "P2D41_ASSEMBLED_MARKER_NOT_TRUE"),
        ("reason_code", "wrong", "P2D41_ASSEMBLY_REASON_CODE_INVALID"),
        ("reason_code", 1, "P2D41_ASSEMBLY_REASON_CODE_INVALID"),
        ("reason", " ", "P2D41_ASSEMBLY_REASON_MISSING"),
        ("reason", 1, "P2D41_ASSEMBLY_REASON_MISSING"),
        (
            "assembly_violations",
            ("old",),
            "P2D41_ASSEMBLY_VIOLATIONS_NOT_EMPTY",
        ),
        (
            "assembly_violations",
            [],
            "P2D41_ASSEMBLY_VIOLATIONS_NOT_EMPTY",
        ),
        (
            "missing_or_invalid_fields",
            ("old",),
            "P2D41_MISSING_OR_INVALID_FIELDS_NOT_EMPTY",
        ),
        (
            "missing_or_invalid_fields",
            [],
            "P2D41_MISSING_OR_INVALID_FIELDS_NOT_EMPTY",
        ),
        (
            "result_candidate_evidence_item_violations",
            ({"old": True},),
            "P2D41_EVIDENCE_ITEM_VIOLATIONS_NOT_EMPTY",
        ),
        (
            "result_candidate_evidence_item_violations",
            [],
            "P2D41_EVIDENCE_ITEM_VIOLATIONS_NOT_EMPTY",
        ),
    )
    for field, value, reason_code in cases:
        assembly = _valid_assembly()
        assembly[field] = value
        result = _consume(assembly)
        _assert_blocked_safe(result)
        assert reason_code in result["consumption_violations"]


def test_upstream_invariant_tuple_and_every_required_ref_are_validated():
    for invalid in (None, (), [], ("",), (" ",), (1,)):
        assembly = _valid_assembly()
        assembly["invariant_refs"] = invalid
        result = _consume(assembly)
        _assert_blocked_safe(result)
        assert "P2D41_INVARIANT_REFS_INVALID" in result[
            "consumption_violations"
        ]

    for required_ref in REQUIRED_P2D41_INVARIANT_REFS:
        assembly = _valid_assembly()
        assembly["invariant_refs"] = tuple(
            value
            for value in REQUIRED_P2D41_INVARIANT_REFS
            if value != required_ref
        )
        result = _consume(assembly)
        _assert_blocked_safe(result)
        assert "P2D41_REQUIRED_INVARIANT_REF_MISSING" in result[
            "consumption_violations"
        ]


def test_source_and_candidate_must_be_exact_dict_shapes():
    source_not_dict = _valid_assembly()
    source_not_dict["source"] = ()
    result = _consume(source_not_dict)
    _assert_blocked_safe(result)
    assert "P2D41_SOURCE_NOT_DICT" in result["consumption_violations"]

    for missing_key in SOURCE_KEYS:
        source_keys = _valid_assembly()
        del source_keys["source"][missing_key]
        result = _consume(source_keys)
        _assert_blocked_safe(result)
        assert "P2D41_SOURCE_KEYS_INVALID" in result[
            "consumption_violations"
        ]

    candidate_not_dict = _valid_assembly()
    candidate_not_dict["local_noop_runner_result_candidate"] = ()
    result = _consume(candidate_not_dict)
    _assert_blocked_safe(result)
    assert "P2D41_RESULT_CANDIDATE_NOT_DICT" in result[
        "consumption_violations"
    ]

    for missing_key in CANDIDATE_KEYS:
        candidate_keys = _valid_assembly()
        del candidate_keys["local_noop_runner_result_candidate"][missing_key]
        result = _consume(candidate_keys)
        _assert_blocked_safe(result)
        assert "P2D41_RESULT_CANDIDATE_KEYS_INVALID" in result[
            "consumption_violations"
        ]


def test_every_missing_root_and_evidence_key_blocks_exact_shape():
    for missing_key in ROOT_KEYS:
        assembly = _valid_assembly()
        del assembly[missing_key]
        result = _consume(assembly)
        _assert_blocked_safe(result)
        assert "CANDIDATE_ASSEMBLY_KEYS_INVALID" in result[
            "consumption_violations"
        ]

    for missing_key in EVIDENCE_ITEM_KEYS:
        assembly = _valid_assembly()
        del assembly["local_noop_runner_result_candidate"][
            "result_candidate_evidence_items"
        ][0][missing_key]
        result = _consume(assembly)
        _assert_blocked_safe(result)
        assert "RESULT_CANDIDATE_EVIDENCE_ITEM_KEYS_INVALID" in result[
            "consumption_violations"
        ]


def test_candidate_required_string_fields_and_kind_are_validated():
    cases = (
        ("run_id", "", "RUN_ID_MISSING"),
        (
            "local_noop_runner_result_candidate_id",
            1,
            "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_ID_MISSING",
        ),
        (
            "candidate_kind",
            "wrong",
            "CANDIDATE_KIND_NOT_LOCAL_NOOP_RUNNER_RESULT_CANDIDATE",
        ),
        (
            "local_noop_runner_readiness_ref",
            " ",
            "LOCAL_NOOP_RUNNER_READINESS_REF_MISSING",
        ),
        (
            "local_noop_runner_readiness_id",
            None,
            "LOCAL_NOOP_RUNNER_READINESS_ID_MISSING",
        ),
        ("created_at", "", "CREATED_AT_MISSING"),
        ("timestamp_policy", 1, "TIMESTAMP_POLICY_MISSING"),
    )
    for field, value, reason_code in cases:
        assembly = _valid_assembly()
        assembly["local_noop_runner_result_candidate"][field] = value
        result = _consume(assembly)
        _assert_blocked_safe(result)
        assert reason_code in result["consumption_violations"]


def test_noop_terminal_readiness_and_public_url_lockins_are_exact():
    cases = (
        ("mode", "real", "MODE_NOT_NOOP"),
        (
            "runner_terminal_status",
            "OTHER",
            "RUNNER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
        ),
        (
            "local_noop_runner_readiness_buildable_marker",
            1,
            "LOCAL_NOOP_RUNNER_READINESS_BUILDABLE_MARKER_NOT_TRUE",
        ),
        ("public_url", "https://example.invalid", "PUBLIC_URL_NOT_NULL"),
        ("public_url_created", 0, "PUBLIC_URL_CREATED_NOT_FALSE"),
        ("source_of_truth", (), "SOURCE_OF_TRUTH_MISSING"),
        ("source_of_truth", [], "SOURCE_OF_TRUTH_MISSING"),
        ("source_of_truth", ("",), "SOURCE_OF_TRUTH_MISSING"),
        ("source_of_truth", (1,), "SOURCE_OF_TRUTH_MISSING"),
        ("notes", (1,), "NOTES_INVALID"),
        ("notes", [], "NOTES_INVALID"),
    )
    for field, value, reason_code in cases:
        assembly = _valid_assembly()
        assembly["local_noop_runner_result_candidate"][field] = value
        result = _consume(assembly)
        _assert_blocked_safe(result)
        assert reason_code in result["consumption_violations"]


def test_empty_candidate_and_evidence_notes_are_allowed():
    assembly = _valid_assembly()
    candidate = assembly["local_noop_runner_result_candidate"]
    candidate["notes"] = ()
    candidate["result_candidate_evidence_items"][0]["notes"] = ()

    result = _consume(assembly)

    assert result["consumed"] is True
    normalized = result["normalized_local_noop_runner_result_candidate"]
    assert normalized["notes"] == ()
    assert normalized["result_candidate_evidence_items"][0]["notes"] == ()


def test_source_and_candidate_lockins_must_match():
    replacement_values = {
        "mode": "real",
        "runner_terminal_status": "OTHER",
        "local_noop_runner_readiness_ref": "other-ref",
        "local_noop_runner_readiness_id": "other-id",
        "local_noop_runner_readiness_buildable_marker": False,
        "public_url": "https://example.invalid",
        "public_url_created": True,
        "source_of_truth": ("other-source",),
    }
    for field in SOURCE_KEYS:
        if field not in replacement_values:
            continue
        assembly = _valid_assembly()
        assembly["source"][field] = replacement_values[field]
        result = _consume(assembly)
        _assert_blocked_safe(result)
        assert "P2D41_SOURCE_CANDIDATE_MISMATCH" in result[
            "consumption_violations"
        ]


def test_readiness_marker_coherence_uses_exact_boolean_types():
    expected_violations = (
        "LOCAL_NOOP_RUNNER_READINESS_BUILDABLE_MARKER_NOT_TRUE",
        "P2D41_SOURCE_CANDIDATE_MISMATCH",
    )
    for source_value, candidate_value in ((True, 1), (1, True)):
        assembly = _valid_assembly()
        assembly["source"][
            "local_noop_runner_readiness_buildable_marker"
        ] = source_value
        assembly["local_noop_runner_result_candidate"][
            "local_noop_runner_readiness_buildable_marker"
        ] = candidate_value

        result = _consume(assembly)

        _assert_blocked_safe(result)
        assert result["consumption_violations"] == expected_violations


def test_public_url_created_coherence_uses_exact_boolean_types():
    expected_violations = (
        "PUBLIC_URL_CREATED_NOT_FALSE",
        "P2D41_SOURCE_CANDIDATE_MISMATCH",
    )
    for source_value, candidate_value in ((False, 0), (0, False)):
        assembly = _valid_assembly()
        assembly["source"]["public_url_created"] = source_value
        assembly["local_noop_runner_result_candidate"][
            "public_url_created"
        ] = candidate_value

        result = _consume(assembly)

        _assert_blocked_safe(result)
        assert result["consumption_violations"] == expected_violations


def test_exact_matching_boolean_lockins_do_not_add_mismatch():
    assembly = _valid_assembly()
    source = assembly["source"]
    candidate = assembly["local_noop_runner_result_candidate"]

    assert source["local_noop_runner_readiness_buildable_marker"] is True
    assert candidate["local_noop_runner_readiness_buildable_marker"] is True
    assert source["public_url_created"] is False
    assert candidate["public_url_created"] is False

    result = _consume(assembly)

    assert result["consumed"] is True
    assert "P2D41_SOURCE_CANDIDATE_MISMATCH" not in result[
        "consumption_violations"
    ]


def test_pass_published_runner_status_blocks_and_is_not_echoed():
    assembly = _valid_assembly()
    assembly["source"]["runner_terminal_status"] = "PASS_PUBLISHED"
    assembly["local_noop_runner_result_candidate"][
        "runner_terminal_status"
    ] = "PASS_PUBLISHED"

    result = _consume(assembly)

    _assert_blocked_safe(result)
    assert result["reason_code"] == "PASS_PUBLISHED_FORBIDDEN"
    assert "runner_terminal_status" not in result["source"]


def test_pass_published_evidence_status_blocks_and_is_not_echoed():
    assembly = _valid_assembly()
    assembly["local_noop_runner_result_candidate"][
        "result_candidate_evidence_items"
    ][0]["evidence_status"] = "PASS_PUBLISHED"

    result = _consume(assembly)

    _assert_blocked_safe(result)
    assert "PASS_PUBLISHED_FORBIDDEN" in result["consumption_violations"]
    assert "evidence_status" not in result["source"]
    _assert_evidence_violation(
        result,
        reason_code="PASS_PUBLISHED_FORBIDDEN",
        index=0,
        evidence_id="result-candidate-evidence-001",
        field=(
            "local_noop_runner_result_candidate."
            "result_candidate_evidence_items[0].evidence_status"
        ),
    )


def test_evidence_items_and_exact_keys_are_required():
    for invalid in (None, (), []):
        assembly = _valid_assembly()
        assembly["local_noop_runner_result_candidate"][
            "result_candidate_evidence_items"
        ] = invalid
        result = _consume(assembly)
        _assert_blocked_safe(result)
        assert "RESULT_CANDIDATE_EVIDENCE_ITEMS_MISSING" in result[
            "consumption_violations"
        ]

    assembly = _valid_assembly()
    assembly["local_noop_runner_result_candidate"][
        "result_candidate_evidence_items"
    ] = ("not-a-dict",)
    result = _consume(assembly)
    _assert_blocked_safe(result)
    assert "RESULT_CANDIDATE_EVIDENCE_ITEM_NOT_DICT" in result[
        "consumption_violations"
    ]
    _assert_evidence_violation(
        result,
        reason_code="RESULT_CANDIDATE_EVIDENCE_ITEM_NOT_DICT",
        index=0,
        evidence_id="",
        field=(
            "local_noop_runner_result_candidate."
            "result_candidate_evidence_items[0]"
        ),
    )

    assembly = _valid_assembly()
    del assembly["local_noop_runner_result_candidate"][
        "result_candidate_evidence_items"
    ][0]["artifact_ref"]
    result = _consume(assembly)
    _assert_blocked_safe(result)
    assert "RESULT_CANDIDATE_EVIDENCE_ITEM_KEYS_INVALID" in result[
        "consumption_violations"
    ]
    _assert_evidence_violation(
        result,
        reason_code="RESULT_CANDIDATE_EVIDENCE_ITEM_KEYS_INVALID",
        index=0,
        evidence_id="result-candidate-evidence-001",
        field=(
            "local_noop_runner_result_candidate."
            "result_candidate_evidence_items[0]"
        ),
    )


def test_evidence_scalar_refs_and_notes_validation():
    scalar_cases = (
        ("result_candidate_evidence_id", "", "RESULT_CANDIDATE_EVIDENCE_ID_MISSING"),
        (
            "result_candidate_evidence_role",
            None,
            "RESULT_CANDIDATE_EVIDENCE_ROLE_MISSING",
        ),
        (
            "artifact_ref",
            " ",
            "RESULT_CANDIDATE_EVIDENCE_ARTIFACT_REF_MISSING",
        ),
        (
            "artifact_kind",
            1,
            "RESULT_CANDIDATE_EVIDENCE_ARTIFACT_KIND_MISSING",
        ),
        (
            "evidence_status",
            "",
            "RESULT_CANDIDATE_EVIDENCE_STATUS_MISSING",
        ),
        (
            "producer_ref",
            None,
            "RESULT_CANDIDATE_EVIDENCE_PRODUCER_REF_MISSING",
        ),
    )
    for field, value, reason_code in scalar_cases:
        assembly = _valid_assembly()
        assembly["local_noop_runner_result_candidate"][
            "result_candidate_evidence_items"
        ][0][field] = value
        result = _consume(assembly)
        _assert_blocked_safe(result)
        assert reason_code in result["consumption_violations"]
        safe_evidence_id = (
            value
            if field == "result_candidate_evidence_id"
            and isinstance(value, str)
            else "result-candidate-evidence-001"
        )
        if field == "result_candidate_evidence_id" and not isinstance(
            value,
            str,
        ):
            safe_evidence_id = ""
        _assert_evidence_violation(
            result,
            reason_code=reason_code,
            index=0,
            evidence_id=safe_evidence_id,
            field=(
                "local_noop_runner_result_candidate."
                f"result_candidate_evidence_items[0].{field}"
            ),
        )

    for field, value, reason_code in (
        ("evidence_refs", (), "RESULT_CANDIDATE_EVIDENCE_REFS_MISSING"),
        ("evidence_refs", [], "RESULT_CANDIDATE_EVIDENCE_REFS_MISSING"),
        (
            "evidence_refs",
            ("",),
            "RESULT_CANDIDATE_EVIDENCE_REFS_MISSING",
        ),
        (
            "evidence_refs",
            (1,),
            "RESULT_CANDIDATE_EVIDENCE_REFS_MISSING",
        ),
        ("notes", (1,), "RESULT_CANDIDATE_EVIDENCE_NOTES_INVALID"),
        ("notes", [], "RESULT_CANDIDATE_EVIDENCE_NOTES_INVALID"),
    ):
        assembly = _valid_assembly()
        assembly["local_noop_runner_result_candidate"][
            "result_candidate_evidence_items"
        ][0][field] = value
        result = _consume(assembly)
        _assert_blocked_safe(result)
        assert reason_code in result["consumption_violations"]


def test_evidence_id_relationships_are_enforced():
    duplicate = _valid_assembly()
    duplicate["local_noop_runner_result_candidate"][
        "result_candidate_evidence_items"
    ] = (_evidence_item(), _evidence_item())
    result = _consume(duplicate)
    _assert_blocked_safe(result)
    assert "RESULT_CANDIDATE_EVIDENCE_ID_DUPLICATE" in result[
        "consumption_violations"
    ]

    not_required = _valid_assembly()
    not_required["local_noop_runner_result_candidate"][
        "result_candidate_evidence_items"
    ] = (
        _evidence_item(result_candidate_evidence_id="extra-evidence"),
    )
    result = _consume(not_required)
    _assert_blocked_safe(result)
    assert "RESULT_CANDIDATE_EVIDENCE_ID_NOT_REQUIRED" in result[
        "consumption_violations"
    ]
    assert "REQUIRED_RESULT_CANDIDATE_EVIDENCE_MISSING" in result[
        "consumption_violations"
    ]

    for invalid_required_ids in ((), [], ("",), (1,)):
        invalid_required = _valid_assembly()
        invalid_required["local_noop_runner_result_candidate"][
            "required_result_candidate_evidence_ids"
        ] = invalid_required_ids
        result = _consume(invalid_required)
        _assert_blocked_safe(result)
        assert "REQUIRED_RESULT_CANDIDATE_EVIDENCE_IDS_MISSING" in result[
            "consumption_violations"
        ]

    for invalid_missing_ids in (("missing-evidence",), [], None):
        missing_declared = _valid_assembly()
        missing_declared["local_noop_runner_result_candidate"][
            "missing_result_candidate_evidence_ids"
        ] = invalid_missing_ids
        result = _consume(missing_declared)
        _assert_blocked_safe(result)
        assert "MISSING_RESULT_CANDIDATE_EVIDENCE_IDS_DECLARED" in result[
            "consumption_violations"
        ]


def test_failed_evidence_and_known_blocking_ids_still_consume():
    assembly = _valid_assembly()
    candidate = assembly["local_noop_runner_result_candidate"]
    candidate["result_candidate_evidence_items"][0][
        "evidence_status"
    ] = "failed"
    candidate["blocking_result_candidate_evidence_ids"] = (
        "result-candidate-evidence-001",
    )

    result = _consume(assembly)

    assert result["consumed"] is True
    normalized = result["normalized_local_noop_runner_result_candidate"]
    assert normalized["result_candidate_evidence_items"][0][
        "evidence_status"
    ] == "failed"
    assert normalized["blocking_result_candidate_evidence_ids"] == (
        "result-candidate-evidence-001",
    )


def test_unknown_blank_and_non_tuple_blocking_ids_block():
    for blocking_ids in (
        ("unknown",),
        ("",),
        (1,),
        ["result-candidate-evidence-001"],
        None,
    ):
        assembly = _valid_assembly()
        assembly["local_noop_runner_result_candidate"][
            "blocking_result_candidate_evidence_ids"
        ] = blocking_ids
        result = _consume(assembly)
        _assert_blocked_safe(result)
        assert "BLOCKING_RESULT_CANDIDATE_EVIDENCE_ID_UNKNOWN" in result[
            "consumption_violations"
        ]


def test_blocked_source_never_echoes_malformed_caller_values():
    assembly = _valid_assembly()
    assembly["reason"] = "caller-secret-reason"
    assembly["source"]["mode"] = "caller-secret-mode"
    candidate = assembly["local_noop_runner_result_candidate"]
    candidate["local_noop_runner_result_candidate_id"] = "caller-secret-id"
    candidate["candidate_kind"] = "caller-secret-kind"
    candidate["public_url"] = "https://caller-secret.invalid"

    result = _consume(assembly)

    _assert_blocked_safe(result)
    assert result["reason"] != assembly["reason"]
    assert result["source"] == BLOCKED_SOURCE


def test_consumed_is_only_approved_positive_success_field():
    result = _consume()
    payload_keys = _payload_keys(result)

    assert result["consumed"] is True
    assert "consumed" in payload_keys
    for forbidden_field in FORBIDDEN_POSITIVE_FIELDS:
        assert forbidden_field not in payload_keys


def test_all_violations_are_collected_and_priority_ordered():
    assembly = _valid_assembly()
    assembly["assembled"] = False
    assembly["reason_code"] = "wrong"
    assembly["reason"] = ""
    assembly["assembly_violations"] = ("old",)
    assembly["source"]["mode"] = "real"
    candidate = assembly["local_noop_runner_result_candidate"]
    candidate["run_id"] = ""
    candidate["mode"] = "real"
    candidate["runner_terminal_status"] = "PASS_PUBLISHED"
    assembly["source"]["runner_terminal_status"] = "PASS_PUBLISHED"
    candidate["public_url"] = "https://example.invalid"
    assembly["source"]["public_url"] = "https://example.invalid"
    evidence_item = candidate["result_candidate_evidence_items"][0]
    evidence_item["artifact_ref"] = ""
    evidence_item["evidence_refs"] = ()

    result = _consume(assembly)
    expected = (
        "P2D41_ASSEMBLED_MARKER_NOT_TRUE",
        "P2D41_ASSEMBLY_REASON_CODE_INVALID",
        "P2D41_ASSEMBLY_REASON_MISSING",
        "P2D41_ASSEMBLY_VIOLATIONS_NOT_EMPTY",
        "RUN_ID_MISSING",
        "MODE_NOT_NOOP",
        "PASS_PUBLISHED_FORBIDDEN",
        "RUNNER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
        "PUBLIC_URL_NOT_NULL",
        "RESULT_CANDIDATE_EVIDENCE_ARTIFACT_REF_MISSING",
        "RESULT_CANDIDATE_EVIDENCE_REFS_MISSING",
    )

    _assert_blocked_safe(result)
    assert result["consumption_violations"] == expected
    assert len(result["consumption_violations"]) == len(
        set(result["consumption_violations"])
    )
    assert result["reason_code"] == result["consumption_violations"][0]


def test_reason_is_deterministic_and_never_echoes_caller_reason():
    first = _valid_assembly()
    first["reason"] = "caller-secret-one"
    first["assembled"] = False
    second = _valid_assembly()
    second["reason"] = "caller-secret-two"
    second["assembled"] = False

    first_result = _consume(first)
    second_result = _consume(second)

    assert first_result["reason"] == second_result["reason"]
    assert first_result["reason"] != first["reason"]
    assert second_result["reason"] != second["reason"]


def test_output_invariant_refs_are_exact():
    result = _consume()

    assert result["invariant_refs"] == INVARIANT_REFS


def test_forbidden_module_namespaces_and_dependencies_are_absent():
    for module_name in FORBIDDEN_MODULE_NAMES:
        assert not hasattr(consumer, module_name)


def test_recursive_output_key_scan_skips_invariant_text_and_not_values():
    result = _consume()
    payload_keys = _payload_keys(result)

    assert "consumed_not_runner_execution" in result["invariant_refs"]
    assert "consumed_not_runner_execution" not in payload_keys
    assert "public_url" in payload_keys
    assert "runner_terminal_status" in payload_keys
    assert "no_publish" not in payload_keys
