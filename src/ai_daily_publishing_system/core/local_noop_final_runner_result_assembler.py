"""Assemble one pure final local noop runner-result object in memory."""

from typing import Final

from .local_noop_runner_result_builder import (
    explain_local_noop_runner_result_build,
)


REASON_CODES: Final[tuple[str, ...]] = (
    "LOCAL_NOOP_FINAL_RUNNER_RESULT_OBJECT_ASSEMBLED",
    "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
    "P2D43_DECISION_RESULT_INVALID",
    "P2D42_CONSUMPTION_RESULT_INVALID",
    "P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID",
    "FINAL_RUNNER_RESULT_ID_INVALID",
    "FINAL_RUNNER_RESULT_ID_NOT_DISTINCT",
    "CROSS_LAYER_COHERENCE_MISMATCH",
    "PASS_PUBLISHED_FORBIDDEN",
    "EVIDENCE_PROJECTION_INVALID",
    "P2D35_BUILD_RESULT_REJECTED",
    "P2D35_BUILD_RESULT_INVALID",
    "P2D35_OUTPUT_COHERENCE_MISMATCH",
)

LOCAL_NOOP_FINAL_RUNNER_RESULT_ASSEMBLER_REASON_CODES: Final[
    tuple[str, ...]
] = REASON_CODES

REASON_PRIORITY: Final[tuple[str, ...]] = (
    "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
    "P2D43_DECISION_RESULT_INVALID",
    "P2D42_CONSUMPTION_RESULT_INVALID",
    "P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID",
    "FINAL_RUNNER_RESULT_ID_INVALID",
    "FINAL_RUNNER_RESULT_ID_NOT_DISTINCT",
    "PASS_PUBLISHED_FORBIDDEN",
    "CROSS_LAYER_COHERENCE_MISMATCH",
    "EVIDENCE_PROJECTION_INVALID",
    "P2D35_BUILD_RESULT_REJECTED",
    "P2D35_BUILD_RESULT_INVALID",
    "P2D35_OUTPUT_COHERENCE_MISMATCH",
    "LOCAL_NOOP_FINAL_RUNNER_RESULT_OBJECT_ASSEMBLED",
)

INVARIANT_REFS: Final[tuple[str, ...]] = (
    "local_noop_final_runner_result_assembler_only",
    "assembler_pure_in_memory_only",
    "assembler_accepts_complete_p2d43_p2d42_p2d33_results",
    "nested_decision_candidate_contract_bypass_rejected",
    "explicit_final_runner_result_id_required",
    "final_runner_result_id_is_opaque_caller_identity",
    "final_runner_result_id_not_generated_or_derived",
    "final_runner_result_id_distinct_from_candidate_and_e2e_ids",
    "p2d33_supplies_e2e_contract_provenance",
    "readiness_reference_not_used_as_e2e_contract_reference",
    "p2d35_is_only_allowed_sibling_dependency",
    "p2d35_called_only_after_complete_validation",
    "p2d35_called_exactly_once_on_valid_input",
    "p2d35_not_called_on_upstream_failure",
    "p2d35_bool_wrapper_not_called",
    "p2d35_output_revalidated",
    "p2d35_blocked_output_not_returned_as_final_result",
    "p2d35_output_returned_as_fresh_projection",
    "candidate_evidence_projected_without_value_change",
    "candidate_evidence_identity_preserved",
    "candidate_evidence_role_preserved",
    "source_of_truth_combines_p2d33_then_p2d42",
    "source_of_truth_order_and_duplicates_preserved",
    "caller_input_not_mutated",
    "final_result_output_not_aliased",
    "final_result_object_assembled_means_in_memory_object_only",
    "noop_completed_is_nested_declarative_metadata_only",
    "final_result_not_runner_execution",
    "final_result_not_e2e_execution",
    "final_result_not_runtime_execution",
    "final_result_not_noop_completion_execution",
    "final_result_not_state_transition",
    "final_result_not_external_noop_completed_achievement",
    "final_result_not_ledger_write_authorization",
    "final_result_not_ledger_persistence",
    "final_result_not_cli_or_manual_invocation",
    "final_result_not_quality_pass",
    "final_result_not_gate_pass",
    "final_result_not_publish_allowed",
    "final_result_not_pass_published",
    "final_result_not_public_url_created",
    "final_result_not_notification_sent",
    "failed_evidence_may_be_assembled",
    "known_blocking_evidence_ids_are_evidence_only",
    "unknown_blocking_evidence_ids_block_assembly",
    "unknown_keys_block_and_are_suppressed",
    "forbidden_fields_block_and_are_suppressed",
    "recursive_key_scan_is_cycle_and_depth_safe",
    "recursive_key_scan_does_not_scan_scalar_strings",
    "mode_noop_required",
    "public_url_must_be_null",
    "public_url_created_must_be_false",
    "pass_published_forbidden",
    "no_file_or_artifact_io",
    "no_config_env_credentials_read",
    "no_run_ledger_yaml_read_or_write",
    "no_runtime_cli_command_or_subprocess",
    "no_completion_transition_gate_eval_audit_execution",
    "no_publish_or_notification",
    "no_quality_pass_no_public_url",
)

_P2D43_ROOT_KEYS: Final[tuple[str, ...]] = (
    "decision_created", "reason_code", "reason", "source",
    "local_noop_terminal_result_assembly_decision", "decision_violations",
    "missing_or_invalid_fields", "decision_validation_violations",
    "invariant_refs",
)
_P2D43_SOURCE_KEYS: Final[tuple[str, ...]] = (
    "p2d42_consumed", "p2d42_reason_code",
    "local_noop_runner_result_candidate_id",
    "local_noop_runner_consumption_receipt_kind", "mode",
    "candidate_runner_terminal_status", "public_url", "public_url_created",
    "source_of_truth",
)
_P2D43_DECISION_KEYS: Final[tuple[str, ...]] = (
    "decision_kind", "decision_value", "decision_scope", "run_id",
    "local_noop_runner_result_candidate_id",
    "local_noop_runner_consumption_receipt_kind", "mode", "public_url",
    "public_url_created",
)
_P2D42_ROOT_KEYS: Final[tuple[str, ...]] = (
    "consumed", "reason_code", "reason", "source",
    "normalized_local_noop_runner_result_candidate",
    "local_noop_runner_consumption_receipt", "consumption_violations",
    "missing_or_invalid_fields", "result_candidate_evidence_item_violations",
    "invariant_refs",
)
_P2D42_SOURCE_KEYS: Final[tuple[str, ...]] = (
    "p2d41_assembled", "p2d41_reason_code",
    "local_noop_runner_result_candidate_id", "candidate_kind", "mode",
    "public_url", "public_url_created", "source_of_truth",
)
_P2D42_CANDIDATE_KEYS: Final[tuple[str, ...]] = (
    "run_id", "local_noop_runner_result_candidate_id", "candidate_kind",
    "mode", "runner_terminal_status", "local_noop_runner_readiness_ref",
    "local_noop_runner_readiness_id",
    "local_noop_runner_readiness_buildable_marker", "public_url",
    "public_url_created", "result_candidate_evidence_items",
    "required_result_candidate_evidence_ids",
    "missing_result_candidate_evidence_ids",
    "blocking_result_candidate_evidence_ids", "created_at", "timestamp_policy",
    "source_of_truth", "notes",
)
_P2D42_RECEIPT_KEYS: Final[tuple[str, ...]] = (
    "receipt_kind", "consumption_scope", "run_id",
    "local_noop_runner_result_candidate_id", "candidate_kind", "mode",
    "public_url", "public_url_created",
)
_P2D42_EVIDENCE_KEYS: Final[tuple[str, ...]] = (
    "result_candidate_evidence_id", "result_candidate_evidence_role",
    "artifact_ref", "artifact_kind", "evidence_status", "producer_ref",
    "evidence_refs", "notes",
)
_P2D33_ROOT_KEYS: Final[tuple[str, ...]] = (
    "buildable", "reason_code", "reason", "source", "local_noop_e2e_contract",
    "contract_violations", "missing_or_invalid_fields",
    "dry_run_evidence_item_violations", "invariant_refs",
)
_P2D33_SOURCE_KEYS: Final[tuple[str, ...]] = (
    "gate_input_ref", "gate_input_buildable_marker",
    "local_noop_run_assembly_ref", "local_noop_run_buildable_marker",
    "mode", "e2e_terminal_status", "public_url", "public_url_created",
    "source_of_truth",
)
_P2D33_CONTRACT_KEYS: Final[tuple[str, ...]] = (
    "run_id", "local_noop_e2e_contract_id", "contract_kind", "mode",
    "e2e_terminal_status", "gate_input_ref", "gate_input_buildable_marker",
    "local_noop_run_assembly_ref", "local_noop_run_buildable_marker",
    "public_url", "public_url_created", "dry_run_evidence_items",
    "required_dry_run_evidence_ids", "missing_dry_run_evidence_ids",
    "blocking_dry_run_evidence_ids", "created_at", "timestamp_policy",
    "source_of_truth", "notes",
)
_P2D33_EVIDENCE_KEYS: Final[tuple[str, ...]] = (
    "dry_run_evidence_id", "dry_run_evidence_role", "artifact_ref",
    "artifact_kind", "evidence_status", "producer_ref", "evidence_refs",
    "notes",
)
_P2D35_ROOT_KEYS: Final[tuple[str, ...]] = (
    "buildable", "reason_code", "reason", "source", "local_noop_runner_result",
    "result_violations", "missing_or_invalid_fields",
    "runner_evidence_item_violations", "invariant_refs",
)
_P2D35_SOURCE_KEYS: Final[tuple[str, ...]] = (
    "local_noop_e2e_contract_ref", "local_noop_e2e_contract_buildable_marker",
    "mode", "runner_terminal_status", "public_url", "public_url_created",
    "source_of_truth",
)
_FINAL_RESULT_KEYS: Final[tuple[str, ...]] = (
    "run_id", "local_noop_runner_result_id", "result_kind", "mode",
    "runner_terminal_status", "local_noop_e2e_contract_ref",
    "local_noop_e2e_contract_buildable_marker", "public_url",
    "public_url_created", "runner_evidence_items", "required_runner_evidence_ids",
    "missing_runner_evidence_ids", "blocking_runner_evidence_ids", "created_at",
    "timestamp_policy", "source_of_truth", "notes",
)
_RUNNER_EVIDENCE_KEYS: Final[tuple[str, ...]] = (
    "runner_evidence_id", "runner_evidence_role", "artifact_ref", "artifact_kind",
    "evidence_status", "producer_ref", "evidence_refs", "notes",
)
_OUTPUT_KEYS: Final[tuple[str, ...]] = (
    "final_result_object_assembled", "reason_code", "reason", "source",
    "local_noop_runner_result", "assembly_violations",
    "missing_or_invalid_fields", "result_validation_violations", "invariant_refs",
)
_OUTPUT_SOURCE_KEYS: Final[tuple[str, ...]] = (
    "p2d43_decision_created", "p2d43_reason_code", "p2d42_consumed",
    "p2d42_reason_code", "p2d33_buildable", "p2d33_reason_code",
    "p2d35_buildable", "p2d35_reason_code", "run_id",
    "local_noop_runner_result_id", "local_noop_runner_result_candidate_id",
    "local_noop_e2e_contract_ref", "mode", "runner_terminal_status",
    "public_url", "public_url_created", "source_of_truth",
)

_P2D43_REQUIRED_INVARIANTS: Final[tuple[str, ...]] = (
    "local_noop_terminal_result_assembly_decision_only",
    "decision_pure_in_memory_only", "decision_accepts_full_p2d42_consumer_result",
    "decision_rejects_normalized_candidate_bypass",
    "full_p2d42_wrapper_requires_consumed_true",
    "full_p2d42_wrapper_requires_exact_success_reason",
    "full_p2d42_wrapper_requires_empty_violations",
    "normalized_candidate_revalidated_not_trusted",
    "consumption_receipt_revalidated_not_trusted",
    "source_candidate_receipt_coherence_required", "exact_type_aware_coherence",
    "caller_input_not_mutated", "output_contains_refs_and_decision_only",
    "normalized_candidate_not_returned", "consumption_receipt_not_returned",
    "decision_created_means_declarative_decision_only",
    "decision_not_runner_execution", "decision_not_e2e_execution",
    "decision_not_state_transition", "decision_not_noop_completed_achievement",
    "decision_not_ledger_write_authorization", "decision_not_publish_allowed",
    "unknown_keys_block_and_are_suppressed",
    "forbidden_fields_block_and_are_suppressed", "mode_noop_required",
    "public_url_must_be_null", "public_url_created_must_be_false",
    "pass_published_forbidden", "no_quality_pass_no_public_url",
)
_P2D42_REQUIRED_INVARIANTS: Final[tuple[str, ...]] = (
    "local_noop_runner_result_candidate_consumer_only",
    "consumer_pure_in_memory_only", "consumer_accepts_full_p2d41_assembly",
    "consumer_rejects_nested_candidate_bypass",
    "full_p2d41_wrapper_requires_assembled_true",
    "full_p2d41_wrapper_requires_empty_violations",
    "consume_means_validate_and_normalize_only",
    "consumed_true_means_accepted_and_normalized_in_memory_only",
    "source_candidate_lockins_must_match",
    "unknown_keys_block_and_are_suppressed",
    "forbidden_fields_block_and_are_suppressed",
    "normalized_candidate_returned_only_when_consumed",
    "consumption_receipt_returned_only_when_consumed",
    "consumption_receipt_not_runner_result", "consumed_not_noop_completion_execution",
    "consumed_not_state_transition", "consumed_not_runner_result_created",
    "consumed_not_noop_completed_achievement", "no_sibling_module_import",
    "no_prior_builder_or_policy_call", "no_file_read", "no_artifact_read",
    "no_run_ledger_yaml_read", "no_run_ledger_yaml_write", "no_publish",
    "no_notification", "mode_noop_required", "public_url_must_be_null",
    "public_url_created_must_be_false",
    "normalized_runner_terminal_status_must_be_noop_completed",
    "noop_completed_is_declarative_input_only", "pass_published_forbidden",
    "evidence_status_opaque_except_pass_published",
    "failed_evidence_status_may_be_consumed",
    "known_blocking_evidence_ids_are_evidence_only",
    "unknown_blocking_evidence_ids_block_consumption",
    "no_quality_pass_no_public_url",
)
_P2D33_REQUIRED_INVARIANTS: Final[tuple[str, ...]] = (
    "local_noop_e2e_contract_builder_only", "builder_not_e2e_executor",
    "builder_not_noop_completion_executor", "dry_run_evidence_items_are_caller_supplied",
    "local_noop_e2e_contract_not_runtime_execution",
    "local_noop_e2e_contract_not_state_transition",
    "local_noop_e2e_contract_not_public_candidate", "mode_noop_required",
    "public_url_must_be_null", "public_url_created_must_be_false",
    "e2e_terminal_status_must_be_noop_completed", "pass_published_forbidden",
    "buildable_not_runtime_executed", "buildable_not_state_transition_executed",
    "buildable_not_quality_pass", "buildable_not_gate_pass",
    "buildable_not_publish_allowed", "buildable_not_pass_published",
    "buildable_not_public_url_created", "no_existing_builder_or_policy_call",
    "no_e2e_execution", "no_publish", "no_notification", "no_ledger_write",
    "no_quality_pass_no_public_url",
)
_P2D35_REQUIRED_INVARIANTS: Final[tuple[str, ...]] = (
    "local_noop_runner_result_builder_only", "builder_not_runner_executor",
    "local_noop_e2e_contract_ref_is_caller_supplied",
    "local_noop_e2e_contract_buildable_marker_is_caller_supplied",
    "local_noop_e2e_contract_ref_opaque", "mode_noop_required",
    "public_url_must_be_null", "public_url_created_must_be_false",
    "runner_terminal_status_must_be_noop_completed", "pass_published_forbidden",
    "buildable_not_runner_executed", "buildable_not_runtime_executed",
    "buildable_not_state_transition_executed", "buildable_not_quality_pass",
    "buildable_not_gate_pass", "buildable_not_publish_allowed",
    "buildable_not_pass_published", "buildable_not_public_url_created",
    "no_existing_builder_or_policy_call", "no_runner_execution", "no_e2e_execution",
    "no_publish", "no_notification", "no_ledger_write",
    "no_quality_pass_no_public_url",
)

_FORBIDDEN_EXACT_KEYS: Final[tuple[str, ...]] = (
    "accepted", "normalized", "eligible", "terminal_realization_eligible",
    "terminal_result_assembly_eligible", "executed", "completed", "realized",
    "terminal_realized", "terminal_reached", "noop_completed",
    "achieved_noop_completed", "achieved_terminal_status", "completion_achieved",
    "state_transitioned", "transitioned", "runner_result_created",
    "result_assembled", "final_result_created", "final_runner_result",
    "decision_created", "decision_authorized", "execution_authorized",
    "runtime_started", "runner_executed", "execution_performed",
    "execution_ready", "runnable", "executable", "invocation_ready",
    "quality_pass", "validator_pass", "rubric_pass", "audit_pass", "eval_pass",
    "gate_pass", "publish_allowed", "pass_published", "published", "notified",
    "ledger_written", "public_url_value", "publish_url", "deployment_url",
    "real_url", "live_url", "public_url_behavior", "command", "raw_command",
    "shell_command", "argv", "args", "parsed_args", "stdout", "stderr",
    "exit_code", "argparse_namespace", "click_context", "typer_app",
    "console_script", "entrypoint", "entry_point", "process_result",
    "human_confirmation_result", "human_approval_result", "operator_action_result",
    "content", "path", "file_path", "local_path", "credentials", "env_vars",
    "config", "prompt", "generated_summary", "final_result_object_assembled",
    "local_noop_runner_result", "p2d35_buildable", "p2d35_reason_code",
)
_FORBIDDEN_PREFIXES: Final[tuple[str, ...]] = (
    "should_", "raw_", "full_", "runner_execution_", "runtime_", "adapter_",
    "scheduler_", "cli_", "command_", "subprocess_", "dry_run_", "e2e_",
    "noop_completion_", "transition_", "gate_execution_", "policy_execution_",
    "validator_execution_", "audit_execution_", "eval_", "publish_",
    "notification_", "ledger_", "run_ledger_", "web_", "github_", "rss_",
    "notion_", "llm_", "model_", "artifact_reader_", "source_fetch_",
)
_FORBIDDEN_SUFFIXES: Final[tuple[str, ...]] = (
    "_content", "_path", "_payload", "_command", "_output", "_result",
    "_read", "_write", "_written", "_executed", "_execution_result",
)

_REASON_TEXT_ENTRIES: Final[tuple[tuple[str, str], ...]] = (
    ("LOCAL_NOOP_FINAL_RUNNER_RESULT_OBJECT_ASSEMBLED", "A final local noop runner-result object was assembled in memory."),
    ("FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT", "A forbidden field or namespace was supplied."),
    ("P2D43_DECISION_RESULT_INVALID", "The complete P2D-43 decision result is invalid."),
    ("P2D42_CONSUMPTION_RESULT_INVALID", "The complete P2D-42 consumption result is invalid."),
    ("P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID", "The complete P2D-33 E2E contract build result is invalid."),
    ("FINAL_RUNNER_RESULT_ID_INVALID", "A nonblank caller-supplied final runner-result ID is required."),
    ("FINAL_RUNNER_RESULT_ID_NOT_DISTINCT", "The final runner-result ID must be distinct from upstream identities."),
    ("CROSS_LAYER_COHERENCE_MISMATCH", "The validated upstream results are not coherent."),
    ("PASS_PUBLISHED_FORBIDDEN", "PASS_PUBLISHED is forbidden at this noop boundary."),
    ("EVIDENCE_PROJECTION_INVALID", "The candidate evidence cannot be projected safely."),
    ("P2D35_BUILD_RESULT_REJECTED", "The P2D-35 result builder rejected the validated input."),
    ("P2D35_BUILD_RESULT_INVALID", "The P2D-35 result builder returned an invalid result."),
    ("P2D35_OUTPUT_COHERENCE_MISMATCH", "The P2D-35 result is not coherent with validated inputs."),
)


def _is_nonblank_string(value: object) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _is_string_tuple(value: object) -> bool:
    if not isinstance(value, tuple):
        return False
    for item in value:
        if not isinstance(item, str):
            return False
    return True


def _is_nonempty_string_tuple(value: object) -> bool:
    return _is_string_tuple(value) and value != () and all(
        item.strip() != "" for item in value
    )


def _fresh_string_tuple(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(value for value in values)


def _values_match_exactly(left: object, right: object) -> bool:
    return type(left) is type(right) and left == right


def _has_exact_keys(value: dict[str, object], keys: tuple[str, ...]) -> bool:
    return tuple(value.keys()) == keys


def _add_issue(
    reason_codes: list[str], field_entries: list[tuple[str, str]],
    reason_code: str, field: str,
) -> None:
    if reason_code not in reason_codes:
        reason_codes.append(reason_code)
    entry = (reason_code, field)
    if entry not in field_entries:
        field_entries.append(entry)


def _ordered_reason_codes(reason_codes: list[str]) -> tuple[str, ...]:
    return tuple(code for code in REASON_PRIORITY if code in reason_codes)


def _ordered_fields(field_entries: list[tuple[str, str]]) -> tuple[str, ...]:
    result = []
    for reason_code in REASON_PRIORITY:
        for entry_reason, field in field_entries:
            if entry_reason == reason_code and field not in result:
                result.append(field)
    return tuple(result)


def _violation_records(field_entries: list[tuple[str, str]]) -> tuple[dict[str, str], ...]:
    records = []
    for reason_code in REASON_PRIORITY:
        for entry_reason, field in field_entries:
            if entry_reason == reason_code:
                record = {"reason_code": reason_code, "field": field}
                if record not in records:
                    records.append(record)
    return tuple(records)


def _reason_text(reason_code: str) -> str:
    for known_code, text in _REASON_TEXT_ENTRIES:
        if known_code == reason_code:
            return text
    return "The final local noop runner-result object was not assembled."


def _normalized_key(key: object) -> str:
    if not isinstance(key, str):
        return ""
    return key.strip().casefold().replace("-", "_").replace(" ", "_")


def _approved_keys_for_path(path: tuple[object, ...]) -> tuple[str, ...]:
    if path == ("p2d43",):
        return _P2D43_ROOT_KEYS
    if path == ("p2d43", "source"):
        return _P2D43_SOURCE_KEYS
    if path == ("p2d43", "decision"):
        return _P2D43_DECISION_KEYS
    if path == ("p2d42",):
        return _P2D42_ROOT_KEYS
    if path == ("p2d42", "source"):
        return _P2D42_SOURCE_KEYS
    if path == ("p2d42", "candidate"):
        return _P2D42_CANDIDATE_KEYS
    if path == ("p2d42", "receipt"):
        return _P2D42_RECEIPT_KEYS
    if len(path) == 4 and path[:3] == ("p2d42", "candidate", "evidence"):
        return _P2D42_EVIDENCE_KEYS
    if path == ("p2d33",):
        return _P2D33_ROOT_KEYS
    if path == ("p2d33", "source"):
        return _P2D33_SOURCE_KEYS
    if path == ("p2d33", "contract"):
        return _P2D33_CONTRACT_KEYS
    if len(path) == 4 and path[:3] == ("p2d33", "contract", "evidence"):
        return _P2D33_EVIDENCE_KEYS
    return ()


def _is_declared_schema_key(key: str) -> bool:
    known = (
        _P2D43_ROOT_KEYS + _P2D43_SOURCE_KEYS + _P2D43_DECISION_KEYS
        + _P2D42_ROOT_KEYS + _P2D42_SOURCE_KEYS + _P2D42_CANDIDATE_KEYS
        + _P2D42_RECEIPT_KEYS + _P2D42_EVIDENCE_KEYS + _P2D33_ROOT_KEYS
        + _P2D33_SOURCE_KEYS + _P2D33_CONTRACT_KEYS + _P2D33_EVIDENCE_KEYS
    )
    return key in known


def _matches_forbidden_catalog(key: str) -> bool:
    return (
        key in _FORBIDDEN_EXACT_KEYS
        or any(key.startswith(prefix) for prefix in _FORBIDDEN_PREFIXES)
        or any(key.endswith(suffix) for suffix in _FORBIDDEN_SUFFIXES)
    )


def _child_path(path: tuple[object, ...], key: object) -> tuple[object, ...]:
    if path == ("p2d43",) and key == "source":
        return path + ("source",)
    if path == ("p2d43",) and key == "local_noop_terminal_result_assembly_decision":
        return path + ("decision",)
    if path == ("p2d42",) and key == "source":
        return path + ("source",)
    if path == ("p2d42",) and key == "normalized_local_noop_runner_result_candidate":
        return path + ("candidate",)
    if path == ("p2d42",) and key == "local_noop_runner_consumption_receipt":
        return path + ("receipt",)
    if path == ("p2d42", "candidate") and key == "result_candidate_evidence_items":
        return path + ("evidence",)
    if path == ("p2d33",) and key == "source":
        return path + ("source",)
    if path == ("p2d33",) and key == "local_noop_e2e_contract":
        return path + ("contract",)
    if path == ("p2d33", "contract") and key == "dry_run_evidence_items":
        return path + ("evidence",)
    return path + (key,)


def _scan_forbidden_keys(
    value: object, path: tuple[object, ...], reason_codes: list[str],
    field_entries: list[tuple[str, str]],
) -> None:
    stack = [(value, path)]
    visited = set()
    while stack:
        current, current_path = stack.pop()
        if not isinstance(current, (dict, list, tuple)):
            continue
        current_id = id(current)
        if current_id in visited:
            continue
        visited.add(current_id)
        if isinstance(current, dict):
            approved = _approved_keys_for_path(current_path)
            for key, nested in current.items():
                normalized = _normalized_key(key)
                if normalized not in approved and (
                    _matches_forbidden_catalog(normalized)
                    or _is_declared_schema_key(normalized)
                ):
                    _add_issue(
                        reason_codes, field_entries,
                        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
                        "p2d44.forbidden_field_or_namespace",
                    )
                stack.append((nested, _child_path(current_path, key)))
        else:
            for index, nested in enumerate(current):
                stack.append((nested, current_path + (index,)))


def _check_required_invariants(
    value: object, required: tuple[str, ...], reason_codes: list[str],
    fields: list[tuple[str, str]], reason_code: str, field: str,
) -> None:
    if not _is_nonempty_string_tuple(value):
        _add_issue(reason_codes, fields, reason_code, field)
        return
    for required_item in required:
        if required_item not in value:
            _add_issue(reason_codes, fields, reason_code, field)
            return


def _validate_p2d43(
    value: object, reason_codes: list[str], fields: list[tuple[str, str]],
) -> dict[str, object]:
    if not isinstance(value, dict):
        _add_issue(reason_codes, fields, "P2D43_DECISION_RESULT_INVALID", "p2d44.p2d43_result")
        return {}
    if not _has_exact_keys(value, _P2D43_ROOT_KEYS):
        _add_issue(reason_codes, fields, "P2D43_DECISION_RESULT_INVALID", "p2d44.p2d43_result.keys")
    if value.get("decision_created") is not True or value.get("reason_code") != "LOCAL_NOOP_TERMINAL_RESULT_ASSEMBLY_DECISION_CREATED":
        _add_issue(reason_codes, fields, "P2D43_DECISION_RESULT_INVALID", "p2d44.p2d43_result")
    if not _is_nonblank_string(value.get("reason")) or value.get("decision_violations") != () or value.get("missing_or_invalid_fields") != () or value.get("decision_validation_violations") != ():
        _add_issue(reason_codes, fields, "P2D43_DECISION_RESULT_INVALID", "p2d44.p2d43_result")
    _check_required_invariants(value.get("invariant_refs"), _P2D43_REQUIRED_INVARIANTS, reason_codes, fields, "P2D43_DECISION_RESULT_INVALID", "p2d44.p2d43_result")
    source = value.get("source")
    decision = value.get("local_noop_terminal_result_assembly_decision")
    if not isinstance(source, dict):
        _add_issue(reason_codes, fields, "P2D43_DECISION_RESULT_INVALID", "p2d44.p2d43_result.source.keys")
        source = {}
    elif not _has_exact_keys(source, _P2D43_SOURCE_KEYS):
        _add_issue(reason_codes, fields, "P2D43_DECISION_RESULT_INVALID", "p2d44.p2d43_result.source.keys")
    if not isinstance(decision, dict):
        _add_issue(reason_codes, fields, "P2D43_DECISION_RESULT_INVALID", "p2d44.p2d43_result.decision.keys")
        decision = {}
    elif not _has_exact_keys(decision, _P2D43_DECISION_KEYS):
        _add_issue(reason_codes, fields, "P2D43_DECISION_RESULT_INVALID", "p2d44.p2d43_result.decision.keys")
    source_expected = (
        source.get("p2d42_consumed") is True
        and source.get("p2d42_reason_code") == "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_CONSUMED_IN_MEMORY"
        and _is_nonblank_string(source.get("local_noop_runner_result_candidate_id"))
        and source.get("local_noop_runner_consumption_receipt_kind") == "local_noop_runner_result_candidate_consumption_receipt"
        and source.get("mode") == "noop"
        and source.get("candidate_runner_terminal_status") == "NOOP_COMPLETED"
        and source.get("public_url") is None
        and source.get("public_url_created") is False
        and _is_nonempty_string_tuple(source.get("source_of_truth"))
    )
    decision_expected = (
        decision.get("decision_kind") == "local_noop_terminal_result_assembly_decision"
        and decision.get("decision_value") == "NOOP_TERMINAL_RESULT_ASSEMBLY_ELIGIBLE"
        and decision.get("decision_scope") == "future_separately_authorized_pure_terminal_result_assembly_only"
        and _is_nonblank_string(decision.get("run_id"))
        and _is_nonblank_string(decision.get("local_noop_runner_result_candidate_id"))
        and decision.get("local_noop_runner_consumption_receipt_kind") == "local_noop_runner_result_candidate_consumption_receipt"
        and decision.get("mode") == "noop"
        and decision.get("public_url") is None
        and decision.get("public_url_created") is False
    )
    if not source_expected or not decision_expected:
        _add_issue(reason_codes, fields, "P2D43_DECISION_RESULT_INVALID", "p2d44.p2d43_result")
    return {"source": source, "decision": decision}


def _validate_p2d42_evidence(
    evidence_items: object, required_ids: object, missing_ids: object,
    blocking_ids: object, reason_codes: list[str], fields: list[tuple[str, str]],
) -> None:
    if not isinstance(evidence_items, tuple) or evidence_items == ():
        _add_issue(reason_codes, fields, "EVIDENCE_PROJECTION_INVALID", "p2d44.p2d42_result.candidate.evidence_items.keys")
        return
    known_ids = []
    for index, item in enumerate(evidence_items):
        path = "p2d44.p2d42_result.candidate.evidence_items.keys"
        if not isinstance(item, dict) or not _has_exact_keys(item, _P2D42_EVIDENCE_KEYS):
            _add_issue(reason_codes, fields, "EVIDENCE_PROJECTION_INVALID", path)
            continue
        for field_name in _P2D42_EVIDENCE_KEYS[:6]:
            if not _is_nonblank_string(item.get(field_name)):
                _add_issue(reason_codes, fields, "EVIDENCE_PROJECTION_INVALID", path)
        if not _is_nonempty_string_tuple(item.get("evidence_refs")) or not _is_string_tuple(item.get("notes")):
            _add_issue(reason_codes, fields, "EVIDENCE_PROJECTION_INVALID", path)
        evidence_id = item.get("result_candidate_evidence_id")
        if _is_nonblank_string(evidence_id):
            if evidence_id in known_ids:
                _add_issue(reason_codes, fields, "EVIDENCE_PROJECTION_INVALID", path)
            known_ids.append(evidence_id)
        if item.get("evidence_status") == "PASS_PUBLISHED":
            _add_issue(reason_codes, fields, "PASS_PUBLISHED_FORBIDDEN", "p2d44.p2d42_result.candidate.evidence_items.keys")
    if not _is_nonempty_string_tuple(required_ids) or tuple(known_ids) != required_ids:
        _add_issue(reason_codes, fields, "EVIDENCE_PROJECTION_INVALID", "p2d44.p2d42_result.candidate.evidence_items.keys")
    if missing_ids != ():
        _add_issue(reason_codes, fields, "EVIDENCE_PROJECTION_INVALID", "p2d44.p2d42_result.candidate.evidence_items.keys")
    if not isinstance(blocking_ids, tuple):
        _add_issue(reason_codes, fields, "EVIDENCE_PROJECTION_INVALID", "p2d44.p2d42_result.candidate.evidence_items.keys")
    else:
        for evidence_id in blocking_ids:
            if not _is_nonblank_string(evidence_id) or evidence_id not in known_ids:
                _add_issue(reason_codes, fields, "EVIDENCE_PROJECTION_INVALID", "p2d44.p2d42_result.candidate.evidence_items.keys")


def _validate_p2d42(
    value: object, reason_codes: list[str], fields: list[tuple[str, str]],
) -> dict[str, object]:
    if not isinstance(value, dict):
        _add_issue(reason_codes, fields, "P2D42_CONSUMPTION_RESULT_INVALID", "p2d44.p2d42_result")
        return {}
    if not _has_exact_keys(value, _P2D42_ROOT_KEYS):
        _add_issue(reason_codes, fields, "P2D42_CONSUMPTION_RESULT_INVALID", "p2d44.p2d42_result.keys")
    if value.get("consumed") is not True or value.get("reason_code") != "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_CONSUMED_IN_MEMORY" or not _is_nonblank_string(value.get("reason")):
        _add_issue(reason_codes, fields, "P2D42_CONSUMPTION_RESULT_INVALID", "p2d44.p2d42_result")
    if value.get("consumption_violations") != () or value.get("missing_or_invalid_fields") != () or value.get("result_candidate_evidence_item_violations") != ():
        _add_issue(reason_codes, fields, "P2D42_CONSUMPTION_RESULT_INVALID", "p2d44.p2d42_result")
    _check_required_invariants(value.get("invariant_refs"), _P2D42_REQUIRED_INVARIANTS, reason_codes, fields, "P2D42_CONSUMPTION_RESULT_INVALID", "p2d44.p2d42_result")
    source = value.get("source")
    candidate = value.get("normalized_local_noop_runner_result_candidate")
    receipt = value.get("local_noop_runner_consumption_receipt")
    if not isinstance(source, dict):
        _add_issue(reason_codes, fields, "P2D42_CONSUMPTION_RESULT_INVALID", "p2d44.p2d42_result.source.keys")
        source = {}
    elif not _has_exact_keys(source, _P2D42_SOURCE_KEYS):
        _add_issue(reason_codes, fields, "P2D42_CONSUMPTION_RESULT_INVALID", "p2d44.p2d42_result.source.keys")
    if not isinstance(candidate, dict):
        _add_issue(reason_codes, fields, "P2D42_CONSUMPTION_RESULT_INVALID", "p2d44.p2d42_result.candidate.keys")
        candidate = {}
    elif not _has_exact_keys(candidate, _P2D42_CANDIDATE_KEYS):
        _add_issue(reason_codes, fields, "P2D42_CONSUMPTION_RESULT_INVALID", "p2d44.p2d42_result.candidate.keys")
    if not isinstance(receipt, dict):
        _add_issue(reason_codes, fields, "P2D42_CONSUMPTION_RESULT_INVALID", "p2d44.p2d42_result.receipt.keys")
        receipt = {}
    elif not _has_exact_keys(receipt, _P2D42_RECEIPT_KEYS):
        _add_issue(reason_codes, fields, "P2D42_CONSUMPTION_RESULT_INVALID", "p2d44.p2d42_result.receipt.keys")
    candidate_expected = (
        _is_nonblank_string(candidate.get("run_id"))
        and _is_nonblank_string(candidate.get("local_noop_runner_result_candidate_id"))
        and candidate.get("candidate_kind") == "local_noop_runner_result_candidate"
        and candidate.get("mode") == "noop"
        and candidate.get("runner_terminal_status") == "NOOP_COMPLETED"
        and _is_nonblank_string(candidate.get("local_noop_runner_readiness_ref"))
        and _is_nonblank_string(candidate.get("local_noop_runner_readiness_id"))
        and candidate.get("local_noop_runner_readiness_buildable_marker") is True
        and candidate.get("public_url") is None
        and candidate.get("public_url_created") is False
        and _is_nonblank_string(candidate.get("created_at"))
        and _is_nonblank_string(candidate.get("timestamp_policy"))
        and _is_nonempty_string_tuple(candidate.get("source_of_truth"))
        and _is_string_tuple(candidate.get("notes"))
    )
    source_expected = (
        source.get("p2d41_assembled") is True
        and source.get("p2d41_reason_code") == "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_ASSEMBLED"
        and source.get("candidate_kind") == "local_noop_runner_result_candidate"
        and source.get("mode") == "noop" and source.get("public_url") is None
        and source.get("public_url_created") is False
        and _is_nonblank_string(source.get("local_noop_runner_result_candidate_id"))
        and _is_nonempty_string_tuple(source.get("source_of_truth"))
    )
    receipt_expected = (
        receipt.get("receipt_kind") == "local_noop_runner_result_candidate_consumption_receipt"
        and receipt.get("consumption_scope") == "pure_in_memory_validation_and_normalization_only"
        and _is_nonblank_string(receipt.get("run_id"))
        and receipt.get("candidate_kind") == "local_noop_runner_result_candidate"
        and receipt.get("mode") == "noop" and receipt.get("public_url") is None
        and receipt.get("public_url_created") is False
        and _is_nonblank_string(receipt.get("local_noop_runner_result_candidate_id"))
    )
    if not candidate_expected or not source_expected or not receipt_expected:
        _add_issue(reason_codes, fields, "P2D42_CONSUMPTION_RESULT_INVALID", "p2d44.p2d42_result")
    _validate_p2d42_evidence(candidate.get("result_candidate_evidence_items"), candidate.get("required_result_candidate_evidence_ids"), candidate.get("missing_result_candidate_evidence_ids"), candidate.get("blocking_result_candidate_evidence_ids"), reason_codes, fields)
    for left, right in (
        (source.get("local_noop_runner_result_candidate_id"), candidate.get("local_noop_runner_result_candidate_id")),
        (source.get("candidate_kind"), candidate.get("candidate_kind")),
        (source.get("mode"), candidate.get("mode")),
        (source.get("public_url"), candidate.get("public_url")),
        (source.get("public_url_created"), candidate.get("public_url_created")),
        (source.get("source_of_truth"), candidate.get("source_of_truth")),
        (receipt.get("run_id"), candidate.get("run_id")),
        (receipt.get("local_noop_runner_result_candidate_id"), candidate.get("local_noop_runner_result_candidate_id")),
        (receipt.get("candidate_kind"), candidate.get("candidate_kind")),
        (receipt.get("mode"), candidate.get("mode")),
        (receipt.get("public_url"), candidate.get("public_url")),
        (receipt.get("public_url_created"), candidate.get("public_url_created")),
    ):
        if not _values_match_exactly(left, right):
            _add_issue(reason_codes, fields, "P2D42_CONSUMPTION_RESULT_INVALID", "p2d44.p2d42_result")
    if candidate.get("runner_terminal_status") == "PASS_PUBLISHED":
        _add_issue(reason_codes, fields, "PASS_PUBLISHED_FORBIDDEN", "p2d44.p2d42_result.candidate.keys")
    return {"source": source, "candidate": candidate, "receipt": receipt}


def _validate_p2d33_evidence(
    evidence_items: object, required_ids: object, missing_ids: object,
    blocking_ids: object, reason_codes: list[str], fields: list[tuple[str, str]],
) -> None:
    if not isinstance(evidence_items, tuple) or evidence_items == ():
        _add_issue(reason_codes, fields, "P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID", "p2d44.p2d33_result.contract.keys")
        return
    known_ids = []
    for item in evidence_items:
        if not isinstance(item, dict) or not _has_exact_keys(item, _P2D33_EVIDENCE_KEYS):
            _add_issue(reason_codes, fields, "P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID", "p2d44.p2d33_result.contract.keys")
            continue
        for field_name in _P2D33_EVIDENCE_KEYS[:6]:
            if not _is_nonblank_string(item.get(field_name)):
                _add_issue(reason_codes, fields, "P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID", "p2d44.p2d33_result.contract.keys")
        if not _is_nonempty_string_tuple(item.get("evidence_refs")) or not _is_string_tuple(item.get("notes")):
            _add_issue(reason_codes, fields, "P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID", "p2d44.p2d33_result.contract.keys")
        evidence_id = item.get("dry_run_evidence_id")
        if _is_nonblank_string(evidence_id):
            if evidence_id in known_ids:
                _add_issue(reason_codes, fields, "P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID", "p2d44.p2d33_result.contract.keys")
            known_ids.append(evidence_id)
        if item.get("evidence_status") == "PASS_PUBLISHED":
            _add_issue(reason_codes, fields, "PASS_PUBLISHED_FORBIDDEN", "p2d44.p2d33_result.contract.keys")
    if not _is_nonempty_string_tuple(required_ids) or tuple(known_ids) != required_ids or missing_ids != ():
        _add_issue(reason_codes, fields, "P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID", "p2d44.p2d33_result.contract.keys")
    if not isinstance(blocking_ids, tuple):
        _add_issue(reason_codes, fields, "P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID", "p2d44.p2d33_result.contract.keys")
    else:
        for evidence_id in blocking_ids:
            if not _is_nonblank_string(evidence_id) or evidence_id not in known_ids:
                _add_issue(reason_codes, fields, "P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID", "p2d44.p2d33_result.contract.keys")


def _validate_p2d33(
    value: object, reason_codes: list[str], fields: list[tuple[str, str]],
) -> dict[str, object]:
    if not isinstance(value, dict):
        _add_issue(reason_codes, fields, "P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID", "p2d44.p2d33_result")
        return {}
    if not _has_exact_keys(value, _P2D33_ROOT_KEYS):
        _add_issue(reason_codes, fields, "P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID", "p2d44.p2d33_result.keys")
    if value.get("buildable") is not True or value.get("reason_code") != "LOCAL_NOOP_E2E_CONTRACT_BUILDABLE" or not _is_nonblank_string(value.get("reason")):
        _add_issue(reason_codes, fields, "P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID", "p2d44.p2d33_result")
    if value.get("contract_violations") != () or value.get("missing_or_invalid_fields") != () or value.get("dry_run_evidence_item_violations") != ():
        _add_issue(reason_codes, fields, "P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID", "p2d44.p2d33_result")
    _check_required_invariants(value.get("invariant_refs"), _P2D33_REQUIRED_INVARIANTS, reason_codes, fields, "P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID", "p2d44.p2d33_result")
    source = value.get("source")
    contract = value.get("local_noop_e2e_contract")
    if not isinstance(source, dict):
        _add_issue(reason_codes, fields, "P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID", "p2d44.p2d33_result.source.keys")
        source = {}
    elif not _has_exact_keys(source, _P2D33_SOURCE_KEYS):
        _add_issue(reason_codes, fields, "P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID", "p2d44.p2d33_result.source.keys")
    if not isinstance(contract, dict):
        _add_issue(reason_codes, fields, "P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID", "p2d44.p2d33_result.contract.keys")
        contract = {}
    elif not _has_exact_keys(contract, _P2D33_CONTRACT_KEYS):
        _add_issue(reason_codes, fields, "P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID", "p2d44.p2d33_result.contract.keys")
    contract_expected = (
        _is_nonblank_string(contract.get("run_id"))
        and _is_nonblank_string(contract.get("local_noop_e2e_contract_id"))
        and contract.get("contract_kind") == "local_noop_e2e_dry_run_contract"
        and contract.get("mode") == "noop"
        and contract.get("e2e_terminal_status") == "NOOP_COMPLETED"
        and _is_nonblank_string(contract.get("gate_input_ref"))
        and contract.get("gate_input_buildable_marker") is True
        and _is_nonblank_string(contract.get("local_noop_run_assembly_ref"))
        and contract.get("local_noop_run_buildable_marker") is True
        and contract.get("public_url") is None and contract.get("public_url_created") is False
        and _is_nonblank_string(contract.get("created_at"))
        and _is_nonblank_string(contract.get("timestamp_policy"))
        and _is_nonempty_string_tuple(contract.get("source_of_truth"))
        and _is_string_tuple(contract.get("notes"))
    )
    source_expected = (
        _is_nonblank_string(source.get("gate_input_ref"))
        and source.get("gate_input_buildable_marker") is True
        and _is_nonblank_string(source.get("local_noop_run_assembly_ref"))
        and source.get("local_noop_run_buildable_marker") is True
        and source.get("mode") == "noop"
        and source.get("e2e_terminal_status") == "NOOP_COMPLETED"
        and source.get("public_url") is None and source.get("public_url_created") is False
        and _is_nonempty_string_tuple(source.get("source_of_truth"))
    )
    if not contract_expected or not source_expected:
        _add_issue(reason_codes, fields, "P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID", "p2d44.p2d33_result")
    _validate_p2d33_evidence(contract.get("dry_run_evidence_items"), contract.get("required_dry_run_evidence_ids"), contract.get("missing_dry_run_evidence_ids"), contract.get("blocking_dry_run_evidence_ids"), reason_codes, fields)
    for key in _P2D33_SOURCE_KEYS:
        if key in contract and not _values_match_exactly(source.get(key), contract.get(key)):
            _add_issue(reason_codes, fields, "P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID", "p2d44.p2d33_result")
    if contract.get("e2e_terminal_status") == "PASS_PUBLISHED":
        _add_issue(reason_codes, fields, "PASS_PUBLISHED_FORBIDDEN", "p2d44.p2d33_result.contract.keys")
    return {"source": source, "contract": contract}


def _validate_cross_layer(
    p2d43: dict[str, object], p2d42: dict[str, object], p2d33: dict[str, object],
    reason_codes: list[str], fields: list[tuple[str, str]],
) -> None:
    decision = p2d43.get("decision", {})
    decision_source = p2d43.get("source", {})
    candidate = p2d42.get("candidate", {})
    candidate_source = p2d42.get("source", {})
    receipt = p2d42.get("receipt", {})
    contract = p2d33.get("contract", {})
    if not all(isinstance(item, dict) for item in (decision, decision_source, candidate, candidate_source, receipt, contract)):
        return
    pairs = (
        (decision.get("run_id"), candidate.get("run_id")),
        (decision.get("local_noop_runner_result_candidate_id"), candidate.get("local_noop_runner_result_candidate_id")),
        (decision_source.get("local_noop_runner_result_candidate_id"), candidate.get("local_noop_runner_result_candidate_id")),
        (candidate_source.get("local_noop_runner_result_candidate_id"), candidate.get("local_noop_runner_result_candidate_id")),
        (receipt.get("local_noop_runner_result_candidate_id"), candidate.get("local_noop_runner_result_candidate_id")),
        (decision.get("mode"), candidate.get("mode")),
        (decision_source.get("mode"), candidate.get("mode")),
        (candidate_source.get("mode"), candidate.get("mode")),
        (receipt.get("mode"), candidate.get("mode")),
        (decision_source.get("candidate_runner_terminal_status"), candidate.get("runner_terminal_status")),
        (decision.get("public_url"), candidate.get("public_url")),
        (decision_source.get("public_url"), candidate.get("public_url")),
        (candidate_source.get("public_url"), candidate.get("public_url")),
        (receipt.get("public_url"), candidate.get("public_url")),
        (decision.get("public_url_created"), candidate.get("public_url_created")),
        (decision_source.get("public_url_created"), candidate.get("public_url_created")),
        (candidate_source.get("public_url_created"), candidate.get("public_url_created")),
        (receipt.get("public_url_created"), candidate.get("public_url_created")),
        (decision_source.get("source_of_truth"), candidate.get("source_of_truth")),
        (candidate_source.get("source_of_truth"), candidate.get("source_of_truth")),
        (contract.get("run_id"), candidate.get("run_id")),
        (contract.get("mode"), candidate.get("mode")),
        (contract.get("e2e_terminal_status"), candidate.get("runner_terminal_status")),
        (contract.get("public_url"), candidate.get("public_url")),
        (contract.get("public_url_created"), candidate.get("public_url_created")),
        (contract.get("run_id"), decision.get("run_id")),
        (contract.get("mode"), decision.get("mode")),
        (contract.get("e2e_terminal_status"), decision_source.get("candidate_runner_terminal_status")),
        (contract.get("public_url"), decision.get("public_url")),
        (contract.get("public_url"), decision_source.get("public_url")),
        (contract.get("public_url_created"), decision.get("public_url_created")),
        (contract.get("public_url_created"), decision_source.get("public_url_created")),
    )
    for left, right in pairs:
        if not _values_match_exactly(left, right):
            _add_issue(reason_codes, fields, "CROSS_LAYER_COHERENCE_MISMATCH", "p2d44.cross_layer_coherence")
            return


def _project_runner_evidence(candidate: dict[str, object]) -> tuple[dict[str, object], ...]:
    projected = []
    for item in candidate["result_candidate_evidence_items"]:
        projected.append({
            "runner_evidence_id": item["result_candidate_evidence_id"],
            "runner_evidence_role": item["result_candidate_evidence_role"],
            "artifact_ref": item["artifact_ref"],
            "artifact_kind": item["artifact_kind"],
            "evidence_status": item["evidence_status"],
            "producer_ref": item["producer_ref"],
            "evidence_refs": _fresh_string_tuple(item["evidence_refs"]),
            "notes": _fresh_string_tuple(item["notes"]),
        })
    return tuple(item for item in projected)


def _copy_final_result(value: dict[str, object]) -> dict[str, object]:
    evidence = []
    for item in value["runner_evidence_items"]:
        evidence.append({
            "runner_evidence_id": item["runner_evidence_id"],
            "runner_evidence_role": item["runner_evidence_role"],
            "artifact_ref": item["artifact_ref"],
            "artifact_kind": item["artifact_kind"],
            "evidence_status": item["evidence_status"],
            "producer_ref": item["producer_ref"],
            "evidence_refs": _fresh_string_tuple(item["evidence_refs"]),
            "notes": _fresh_string_tuple(item["notes"]),
        })
    return {
        "run_id": value["run_id"],
        "local_noop_runner_result_id": value["local_noop_runner_result_id"],
        "result_kind": value["result_kind"], "mode": value["mode"],
        "runner_terminal_status": value["runner_terminal_status"],
        "local_noop_e2e_contract_ref": value["local_noop_e2e_contract_ref"],
        "local_noop_e2e_contract_buildable_marker": value["local_noop_e2e_contract_buildable_marker"],
        "public_url": None, "public_url_created": value["public_url_created"],
        "runner_evidence_items": tuple(item for item in evidence),
        "required_runner_evidence_ids": _fresh_string_tuple(value["required_runner_evidence_ids"]),
        "missing_runner_evidence_ids": (),
        "blocking_runner_evidence_ids": _fresh_string_tuple(value["blocking_runner_evidence_ids"]),
        "created_at": value["created_at"], "timestamp_policy": value["timestamp_policy"],
        "source_of_truth": _fresh_string_tuple(value["source_of_truth"]),
        "notes": _fresh_string_tuple(value["notes"]),
    }


def _blocked_source() -> dict[str, object]:
    return {
        "p2d43_decision_created": False, "p2d43_reason_code": "",
        "p2d42_consumed": False, "p2d42_reason_code": "",
        "p2d33_buildable": False, "p2d33_reason_code": "",
        "p2d35_buildable": False, "p2d35_reason_code": "", "run_id": "",
        "local_noop_runner_result_id": "",
        "local_noop_runner_result_candidate_id": "",
        "local_noop_e2e_contract_ref": "", "mode": "",
        "runner_terminal_status": "", "public_url": None,
        "public_url_created": False, "source_of_truth": (),
    }


def _blocked_result(reason_codes: list[str], fields: list[tuple[str, str]]) -> dict[str, object]:
    violations = _ordered_reason_codes(reason_codes)
    reason_code = violations[0] if violations else "P2D35_BUILD_RESULT_INVALID"
    return {
        "final_result_object_assembled": False, "reason_code": reason_code,
        "reason": _reason_text(reason_code), "source": _blocked_source(),
        "local_noop_runner_result": {}, "assembly_violations": violations,
        "missing_or_invalid_fields": _ordered_fields(fields),
        "result_validation_violations": _violation_records(fields),
        "invariant_refs": INVARIANT_REFS,
    }


def _validate_p2d35_output(
    output: object, expected: dict[str, object], reason_codes: list[str],
    fields: list[tuple[str, str]],
) -> dict[str, object]:
    if not isinstance(output, dict):
        _add_issue(reason_codes, fields, "P2D35_BUILD_RESULT_INVALID", "p2d44.p2d35_result")
        return {}
    if not _has_exact_keys(output, _P2D35_ROOT_KEYS):
        _add_issue(reason_codes, fields, "P2D35_BUILD_RESULT_INVALID", "p2d44.p2d35_result.keys")
    if output.get("buildable") is not True or output.get("reason_code") != "LOCAL_NOOP_RUNNER_RESULT_BUILDABLE" or not _is_nonblank_string(output.get("reason")):
        _add_issue(reason_codes, fields, "P2D35_BUILD_RESULT_REJECTED", "p2d44.p2d35_result")
    if output.get("result_violations") != () or output.get("missing_or_invalid_fields") != () or output.get("runner_evidence_item_violations") != ():
        _add_issue(reason_codes, fields, "P2D35_BUILD_RESULT_REJECTED", "p2d44.p2d35_result")
    _check_required_invariants(
        output.get("invariant_refs"), _P2D35_REQUIRED_INVARIANTS,
        reason_codes, fields, "P2D35_BUILD_RESULT_INVALID", "p2d44.p2d35_result",
    )
    source = output.get("source")
    result = output.get("local_noop_runner_result")
    if not isinstance(source, dict) or not _has_exact_keys(source, _P2D35_SOURCE_KEYS):
        _add_issue(reason_codes, fields, "P2D35_BUILD_RESULT_INVALID", "p2d44.p2d35_result.source.keys")
        source = {}
    if not isinstance(result, dict) or not _has_exact_keys(result, _FINAL_RESULT_KEYS):
        _add_issue(reason_codes, fields, "P2D35_BUILD_RESULT_INVALID", "p2d44.p2d35_result.local_noop_runner_result.keys")
        return {}
    evidence_items = result.get("runner_evidence_items")
    if not isinstance(evidence_items, tuple):
        _add_issue(reason_codes, fields, "P2D35_BUILD_RESULT_INVALID", "p2d44.p2d35_result.local_noop_runner_result.keys")
    else:
        for item in evidence_items:
            if not isinstance(item, dict) or not _has_exact_keys(item, _RUNNER_EVIDENCE_KEYS):
                _add_issue(reason_codes, fields, "P2D35_BUILD_RESULT_INVALID", "p2d44.p2d35_result.local_noop_runner_result.keys")
    for field_name, expected_value in expected.items():
        if not _values_match_exactly(result.get(field_name), expected_value):
            _add_issue(reason_codes, fields, "P2D35_OUTPUT_COHERENCE_MISMATCH", "p2d44.p2d35_result")
            break
    for field_name in _P2D35_SOURCE_KEYS:
        if field_name in expected and not _values_match_exactly(source.get(field_name), expected[field_name]):
            _add_issue(reason_codes, fields, "P2D35_OUTPUT_COHERENCE_MISMATCH", "p2d44.p2d35_result.source.keys")
            break
    if result.get("runner_terminal_status") == "PASS_PUBLISHED":
        _add_issue(reason_codes, fields, "PASS_PUBLISHED_FORBIDDEN", "p2d44.p2d35_result")
    if isinstance(evidence_items, tuple):
        for item in evidence_items:
            if isinstance(item, dict) and item.get("evidence_status") == "PASS_PUBLISHED":
                _add_issue(reason_codes, fields, "PASS_PUBLISHED_FORBIDDEN", "p2d44.p2d35_result")
    return result


def assemble_local_noop_final_runner_result(
    *,
    local_noop_terminal_result_assembly_decision_result: dict[str, object],
    local_noop_runner_result_candidate_consumption: dict[str, object],
    local_noop_e2e_contract_build_result: dict[str, object],
    local_noop_runner_result_id: str,
) -> dict[str, object]:
    """Assemble a validated final local noop runner-result object in memory."""

    reason_codes = []
    fields = []
    _scan_forbidden_keys(local_noop_terminal_result_assembly_decision_result, ("p2d43",), reason_codes, fields)
    _scan_forbidden_keys(local_noop_runner_result_candidate_consumption, ("p2d42",), reason_codes, fields)
    _scan_forbidden_keys(local_noop_e2e_contract_build_result, ("p2d33",), reason_codes, fields)
    p2d43 = _validate_p2d43(local_noop_terminal_result_assembly_decision_result, reason_codes, fields)
    p2d42 = _validate_p2d42(local_noop_runner_result_candidate_consumption, reason_codes, fields)
    p2d33 = _validate_p2d33(local_noop_e2e_contract_build_result, reason_codes, fields)
    if type(local_noop_runner_result_id) is not str or local_noop_runner_result_id.strip() == "":
        _add_issue(reason_codes, fields, "FINAL_RUNNER_RESULT_ID_INVALID", "p2d44.local_noop_runner_result_id")
    _validate_cross_layer(p2d43, p2d42, p2d33, reason_codes, fields)
    candidate = p2d42.get("candidate", {})
    contract = p2d33.get("contract", {})
    if isinstance(candidate, dict) and isinstance(contract, dict) and type(local_noop_runner_result_id) is str:
        if local_noop_runner_result_id in (
            candidate.get("local_noop_runner_result_candidate_id"),
            contract.get("local_noop_e2e_contract_id"),
        ):
            _add_issue(reason_codes, fields, "FINAL_RUNNER_RESULT_ID_NOT_DISTINCT", "p2d44.local_noop_runner_result_id")
    if reason_codes:
        return _blocked_result(reason_codes, fields)
    projected_evidence = _project_runner_evidence(candidate)
    required_ids = _fresh_string_tuple(candidate["required_result_candidate_evidence_ids"])
    missing_ids = ()
    blocking_ids = _fresh_string_tuple(candidate["blocking_result_candidate_evidence_ids"])
    source_of_truth = (
        _fresh_string_tuple(contract["source_of_truth"])
        + _fresh_string_tuple(candidate["source_of_truth"])
    )
    notes = _fresh_string_tuple(candidate["notes"])
    expected = {
        "run_id": candidate["run_id"],
        "local_noop_runner_result_id": local_noop_runner_result_id,
        "result_kind": "local_noop_runner_result", "mode": "noop",
        "runner_terminal_status": "NOOP_COMPLETED",
        "local_noop_e2e_contract_ref": contract["local_noop_e2e_contract_id"],
        "local_noop_e2e_contract_buildable_marker": True,
        "public_url": None, "public_url_created": False,
        "runner_evidence_items": projected_evidence,
        "required_runner_evidence_ids": required_ids,
        "missing_runner_evidence_ids": missing_ids,
        "blocking_runner_evidence_ids": blocking_ids,
        "created_at": candidate["created_at"],
        "timestamp_policy": candidate["timestamp_policy"],
        "source_of_truth": source_of_truth, "notes": notes,
    }
    try:
        p2d35_output = explain_local_noop_runner_result_build(
            run_id=expected["run_id"],
            local_noop_runner_result_id=expected["local_noop_runner_result_id"],
            result_kind=expected["result_kind"], mode=expected["mode"],
            runner_terminal_status=expected["runner_terminal_status"],
            local_noop_e2e_contract_ref=expected["local_noop_e2e_contract_ref"],
            local_noop_e2e_contract_buildable_marker=True,
            public_url_created=False, public_url_is_null=True,
            runner_evidence_items=projected_evidence,
            required_runner_evidence_ids=required_ids,
            missing_runner_evidence_ids=missing_ids,
            blocking_runner_evidence_ids=blocking_ids,
            created_at=expected["created_at"],
            timestamp_policy=expected["timestamp_policy"],
            source_of_truth=source_of_truth, notes=notes,
        )
    except Exception:
        _add_issue(reason_codes, fields, "P2D35_BUILD_RESULT_INVALID", "p2d44.p2d35_result")
        return _blocked_result(reason_codes, fields)
    final_result = _validate_p2d35_output(p2d35_output, expected, reason_codes, fields)
    if reason_codes:
        return _blocked_result(reason_codes, fields)
    decision = p2d43["decision"]
    return {
        "final_result_object_assembled": True,
        "reason_code": "LOCAL_NOOP_FINAL_RUNNER_RESULT_OBJECT_ASSEMBLED",
        "reason": _reason_text("LOCAL_NOOP_FINAL_RUNNER_RESULT_OBJECT_ASSEMBLED"),
        "source": {
            "p2d43_decision_created": True,
            "p2d43_reason_code": "LOCAL_NOOP_TERMINAL_RESULT_ASSEMBLY_DECISION_CREATED",
            "p2d42_consumed": True,
            "p2d42_reason_code": "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_CONSUMED_IN_MEMORY",
            "p2d33_buildable": True,
            "p2d33_reason_code": "LOCAL_NOOP_E2E_CONTRACT_BUILDABLE",
            "p2d35_buildable": True,
            "p2d35_reason_code": "LOCAL_NOOP_RUNNER_RESULT_BUILDABLE",
            "run_id": candidate["run_id"],
            "local_noop_runner_result_id": local_noop_runner_result_id,
            "local_noop_runner_result_candidate_id": candidate["local_noop_runner_result_candidate_id"],
            "local_noop_e2e_contract_ref": contract["local_noop_e2e_contract_id"],
            "mode": "noop", "runner_terminal_status": "NOOP_COMPLETED",
            "public_url": None, "public_url_created": False,
            "source_of_truth": _fresh_string_tuple(source_of_truth),
        },
        "local_noop_runner_result": _copy_final_result(final_result),
        "assembly_violations": (), "missing_or_invalid_fields": (),
        "result_validation_violations": (), "invariant_refs": INVARIANT_REFS,
    }


def is_local_noop_final_runner_result_object_assembled(
    *,
    local_noop_terminal_result_assembly_decision_result: dict[str, object],
    local_noop_runner_result_candidate_consumption: dict[str, object],
    local_noop_e2e_contract_build_result: dict[str, object],
    local_noop_runner_result_id: str,
) -> bool:
    """Return only whether a final in-memory result object was assembled."""

    return assemble_local_noop_final_runner_result(
        local_noop_terminal_result_assembly_decision_result=(
            local_noop_terminal_result_assembly_decision_result
        ),
        local_noop_runner_result_candidate_consumption=(
            local_noop_runner_result_candidate_consumption
        ),
        local_noop_e2e_contract_build_result=local_noop_e2e_contract_build_result,
        local_noop_runner_result_id=local_noop_runner_result_id,
    )["final_result_object_assembled"]
