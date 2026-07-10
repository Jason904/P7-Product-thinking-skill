"""Create a pure declarative local noop terminal-result assembly decision."""

from typing import Final


REASON_CODES: Final[tuple[str, ...]] = (
    "LOCAL_NOOP_TERMINAL_RESULT_ASSEMBLY_DECISION_CREATED",
    "P2D42_CONSUMER_RESULT_NOT_DICT",
    "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
    "P2D42_CONSUMER_RESULT_KEYS_INVALID",
    "P2D42_CONSUMED_MARKER_NOT_TRUE",
    "P2D42_CONSUMPTION_REASON_CODE_INVALID",
    "P2D42_CONSUMPTION_REASON_MISSING",
    "P2D42_CONSUMPTION_VIOLATIONS_NOT_EMPTY",
    "P2D42_MISSING_OR_INVALID_FIELDS_NOT_EMPTY",
    "P2D42_EVIDENCE_ITEM_VIOLATIONS_NOT_EMPTY",
    "P2D42_INVARIANT_REFS_INVALID",
    "P2D42_REQUIRED_INVARIANT_REF_MISSING",
    "P2D42_SOURCE_NOT_DICT",
    "P2D42_SOURCE_KEYS_INVALID",
    "P2D42_SOURCE_FIELD_INVALID",
    "P2D42_NORMALIZED_CANDIDATE_NOT_DICT",
    "P2D42_NORMALIZED_CANDIDATE_KEYS_INVALID",
    "P2D42_NORMALIZED_CANDIDATE_FIELD_INVALID",
    "PASS_PUBLISHED_FORBIDDEN",
    "MODE_NOT_NOOP",
    "RUNNER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
    "PUBLIC_URL_NOT_NULL",
    "PUBLIC_URL_CREATED_NOT_FALSE",
    "P2D42_EVIDENCE_ITEM_NOT_DICT",
    "P2D42_EVIDENCE_ITEM_KEYS_INVALID",
    "P2D42_EVIDENCE_ITEM_FIELD_INVALID",
    "P2D42_EVIDENCE_RELATIONSHIP_INVALID",
    "P2D42_RECEIPT_NOT_DICT",
    "P2D42_RECEIPT_KEYS_INVALID",
    "P2D42_RECEIPT_KIND_INVALID",
    "P2D42_RECEIPT_SCOPE_INVALID",
    "P2D42_RECEIPT_FIELD_INVALID",
    "P2D42_SOURCE_CANDIDATE_RECEIPT_MISMATCH",
)

LOCAL_NOOP_TERMINAL_RESULT_ASSEMBLY_DECISION_REASON_CODES: Final[
    tuple[str, ...]
] = REASON_CODES

REASON_PRIORITY: Final[tuple[str, ...]] = (
    "P2D42_CONSUMER_RESULT_NOT_DICT",
    "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
    "P2D42_CONSUMER_RESULT_KEYS_INVALID",
    "P2D42_CONSUMED_MARKER_NOT_TRUE",
    "P2D42_CONSUMPTION_REASON_CODE_INVALID",
    "P2D42_CONSUMPTION_REASON_MISSING",
    "P2D42_CONSUMPTION_VIOLATIONS_NOT_EMPTY",
    "P2D42_MISSING_OR_INVALID_FIELDS_NOT_EMPTY",
    "P2D42_EVIDENCE_ITEM_VIOLATIONS_NOT_EMPTY",
    "P2D42_INVARIANT_REFS_INVALID",
    "P2D42_REQUIRED_INVARIANT_REF_MISSING",
    "P2D42_SOURCE_NOT_DICT",
    "P2D42_SOURCE_KEYS_INVALID",
    "P2D42_NORMALIZED_CANDIDATE_NOT_DICT",
    "P2D42_NORMALIZED_CANDIDATE_KEYS_INVALID",
    "P2D42_RECEIPT_NOT_DICT",
    "P2D42_RECEIPT_KEYS_INVALID",
    "PASS_PUBLISHED_FORBIDDEN",
    "MODE_NOT_NOOP",
    "RUNNER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
    "PUBLIC_URL_NOT_NULL",
    "PUBLIC_URL_CREATED_NOT_FALSE",
    "P2D42_SOURCE_FIELD_INVALID",
    "P2D42_NORMALIZED_CANDIDATE_FIELD_INVALID",
    "P2D42_EVIDENCE_ITEM_NOT_DICT",
    "P2D42_EVIDENCE_ITEM_KEYS_INVALID",
    "P2D42_EVIDENCE_ITEM_FIELD_INVALID",
    "P2D42_EVIDENCE_RELATIONSHIP_INVALID",
    "P2D42_RECEIPT_KIND_INVALID",
    "P2D42_RECEIPT_SCOPE_INVALID",
    "P2D42_RECEIPT_FIELD_INVALID",
    "P2D42_SOURCE_CANDIDATE_RECEIPT_MISMATCH",
    "LOCAL_NOOP_TERMINAL_RESULT_ASSEMBLY_DECISION_CREATED",
)

_ROOT_KEYS: Final[tuple[str, ...]] = (
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

_SOURCE_KEYS: Final[tuple[str, ...]] = (
    "p2d41_assembled",
    "p2d41_reason_code",
    "local_noop_runner_result_candidate_id",
    "candidate_kind",
    "mode",
    "public_url",
    "public_url_created",
    "source_of_truth",
)

_CANDIDATE_KEYS: Final[tuple[str, ...]] = (
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

_RECEIPT_KEYS: Final[tuple[str, ...]] = (
    "receipt_kind",
    "consumption_scope",
    "run_id",
    "local_noop_runner_result_candidate_id",
    "candidate_kind",
    "mode",
    "public_url",
    "public_url_created",
)

_EVIDENCE_ITEM_KEYS: Final[tuple[str, ...]] = (
    "result_candidate_evidence_id",
    "result_candidate_evidence_role",
    "artifact_ref",
    "artifact_kind",
    "evidence_status",
    "producer_ref",
    "evidence_refs",
    "notes",
)

_EVIDENCE_STRING_FIELDS: Final[tuple[str, ...]] = (
    "result_candidate_evidence_id",
    "result_candidate_evidence_role",
    "artifact_ref",
    "artifact_kind",
    "evidence_status",
    "producer_ref",
)

_SOURCE_CANDIDATE_COHERENCE_FIELDS: Final[tuple[str, ...]] = (
    "local_noop_runner_result_candidate_id",
    "candidate_kind",
    "mode",
    "public_url",
    "public_url_created",
    "source_of_truth",
)

_CANDIDATE_RECEIPT_COHERENCE_FIELDS: Final[tuple[str, ...]] = (
    "run_id",
    "local_noop_runner_result_candidate_id",
    "candidate_kind",
    "mode",
    "public_url",
    "public_url_created",
)

_SOURCE_RECEIPT_COHERENCE_FIELDS: Final[tuple[str, ...]] = (
    "local_noop_runner_result_candidate_id",
    "candidate_kind",
    "mode",
    "public_url",
    "public_url_created",
)

_REQUIRED_P2D42_INVARIANT_REFS: Final[tuple[str, ...]] = (
    "local_noop_runner_result_candidate_consumer_only",
    "consumer_pure_in_memory_only",
    "consumer_accepts_full_p2d41_assembly",
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
    "consumption_receipt_not_runner_result",
    "consumed_not_noop_completion_execution",
    "consumed_not_state_transition",
    "consumed_not_runner_result_created",
    "consumed_not_noop_completed_achievement",
    "no_sibling_module_import",
    "no_prior_builder_or_policy_call",
    "no_file_read",
    "no_artifact_read",
    "no_run_ledger_yaml_read",
    "no_run_ledger_yaml_write",
    "no_publish",
    "no_notification",
    "mode_noop_required",
    "public_url_must_be_null",
    "public_url_created_must_be_false",
    "normalized_runner_terminal_status_must_be_noop_completed",
    "noop_completed_is_declarative_input_only",
    "pass_published_forbidden",
    "evidence_status_opaque_except_pass_published",
    "failed_evidence_status_may_be_consumed",
    "known_blocking_evidence_ids_are_evidence_only",
    "unknown_blocking_evidence_ids_block_consumption",
    "no_quality_pass_no_public_url",
)

_FORBIDDEN_EXACT_KEYS: Final[tuple[str, ...]] = (
    "accepted",
    "normalized",
    "eligible",
    "terminal_realization_eligible",
    "terminal_result_assembly_eligible",
    "executed",
    "completed",
    "realized",
    "terminal_realized",
    "terminal_reached",
    "noop_completed",
    "achieved_noop_completed",
    "achieved_terminal_status",
    "completion_achieved",
    "state_transitioned",
    "transitioned",
    "runner_result_created",
    "result_assembled",
    "final_result_created",
    "final_runner_result",
    "decision_created",
    "decision_authorized",
    "execution_authorized",
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

_FORBIDDEN_PREFIXES: Final[tuple[str, ...]] = (
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

_FORBIDDEN_SUFFIXES: Final[tuple[str, ...]] = (
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

_INVARIANT_REFS: Final[tuple[str, ...]] = (
    "local_noop_terminal_result_assembly_decision_only",
    "decision_pure_in_memory_only",
    "decision_accepts_full_p2d42_consumer_result",
    "decision_rejects_normalized_candidate_bypass",
    "full_p2d42_wrapper_requires_consumed_true",
    "full_p2d42_wrapper_requires_exact_success_reason",
    "full_p2d42_wrapper_requires_empty_violations",
    "normalized_candidate_revalidated_not_trusted",
    "consumption_receipt_revalidated_not_trusted",
    "source_candidate_receipt_coherence_required",
    "exact_type_aware_coherence",
    "caller_input_not_mutated",
    "output_contains_refs_and_decision_only",
    "normalized_candidate_not_returned",
    "consumption_receipt_not_returned",
    "decision_created_means_declarative_decision_only",
    "decision_value_means_future_separately_authorized_assembly_only",
    "eligibility_not_execution_authorization",
    "candidate_runner_terminal_status_is_metadata_only",
    "noop_completed_not_top_level_outcome",
    "decision_not_runner_result",
    "decision_not_runner_execution",
    "decision_not_runtime_execution",
    "decision_not_adapter_execution",
    "decision_not_scheduler_execution",
    "decision_not_cli_or_manual_execution",
    "decision_not_argument_parsing",
    "decision_not_command_or_subprocess_execution",
    "decision_not_dry_run_or_e2e_execution",
    "decision_not_noop_completion_execution",
    "decision_not_state_transition",
    "decision_not_runner_result_created",
    "decision_not_noop_completed_achievement",
    "decision_not_ledger_write_authorization",
    "decision_not_quality_pass",
    "decision_not_gate_pass",
    "decision_not_publish_allowed",
    "decision_not_pass_published",
    "decision_not_public_url_created",
    "decision_not_notification_sent",
    "evidence_status_opaque_except_pass_published",
    "failed_evidence_status_may_be_assembly_eligible",
    "known_blocking_evidence_ids_are_evidence_only",
    "unknown_blocking_evidence_ids_block_decision",
    "unknown_keys_block_and_are_suppressed",
    "forbidden_fields_block_and_are_suppressed",
    "recursive_key_scan_does_not_scan_string_values",
    "no_sibling_module_import",
    "no_prior_builder_or_policy_call",
    "no_file_or_artifact_io",
    "no_config_env_credentials_read",
    "no_web_github_rss_notion_access",
    "no_llm_summary_or_judge",
    "no_run_ledger_yaml_read_or_write",
    "no_publish_or_notification",
    "mode_noop_required",
    "public_url_must_be_null",
    "public_url_created_must_be_false",
    "pass_published_forbidden",
    "no_quality_pass_no_public_url",
)

_REASON_TEXT_ENTRIES: Final[tuple[tuple[str, str], ...]] = (
    (
        "LOCAL_NOOP_TERMINAL_RESULT_ASSEMBLY_DECISION_CREATED",
        "The complete P2D-42 consumer result was validated and a pure "
        "declarative terminal-result assembly decision was created in memory.",
    ),
    (
        "P2D42_CONSUMER_RESULT_NOT_DICT",
        "The P2D-42 consumer result must be a dict.",
    ),
    (
        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
        "The caller payload contains a forbidden field or namespace.",
    ),
    (
        "P2D42_CONSUMER_RESULT_KEYS_INVALID",
        "The P2D-42 consumer result must contain the exact approved root keys.",
    ),
    (
        "P2D42_CONSUMED_MARKER_NOT_TRUE",
        "The P2D-42 consumed marker must be exactly true.",
    ),
    (
        "P2D42_CONSUMPTION_REASON_CODE_INVALID",
        "The P2D-42 reason code must declare in-memory consumption.",
    ),
    (
        "P2D42_CONSUMPTION_REASON_MISSING",
        "The P2D-42 consumer result requires a nonblank reason.",
    ),
    (
        "P2D42_CONSUMPTION_VIOLATIONS_NOT_EMPTY",
        "The P2D-42 consumption violations must be empty.",
    ),
    (
        "P2D42_MISSING_OR_INVALID_FIELDS_NOT_EMPTY",
        "The P2D-42 missing-or-invalid fields must be empty.",
    ),
    (
        "P2D42_EVIDENCE_ITEM_VIOLATIONS_NOT_EMPTY",
        "The P2D-42 evidence item violations must be empty.",
    ),
    (
        "P2D42_INVARIANT_REFS_INVALID",
        "The P2D-42 invariant refs must be nonempty nonblank strings.",
    ),
    (
        "P2D42_REQUIRED_INVARIANT_REF_MISSING",
        "A required P2D-42 invariant reference is missing.",
    ),
    ("P2D42_SOURCE_NOT_DICT", "The P2D-42 source must be a dict."),
    (
        "P2D42_SOURCE_KEYS_INVALID",
        "The P2D-42 source must contain the exact approved keys.",
    ),
    (
        "P2D42_SOURCE_FIELD_INVALID",
        "A required P2D-42 source field is invalid.",
    ),
    (
        "P2D42_NORMALIZED_CANDIDATE_NOT_DICT",
        "The normalized P2D-42 candidate must be a dict.",
    ),
    (
        "P2D42_NORMALIZED_CANDIDATE_KEYS_INVALID",
        "The normalized P2D-42 candidate must contain the exact approved keys.",
    ),
    (
        "P2D42_NORMALIZED_CANDIDATE_FIELD_INVALID",
        "A required normalized candidate field is invalid.",
    ),
    (
        "PASS_PUBLISHED_FORBIDDEN",
        "PASS_PUBLISHED is forbidden at this noop decision boundary.",
    ),
    ("MODE_NOT_NOOP", "mode must be noop."),
    (
        "RUNNER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
        "The candidate runner terminal status must be declarative NOOP_COMPLETED.",
    ),
    ("PUBLIC_URL_NOT_NULL", "public_url must remain null."),
    (
        "PUBLIC_URL_CREATED_NOT_FALSE",
        "public_url_created must remain exactly false.",
    ),
    (
        "P2D42_EVIDENCE_ITEM_NOT_DICT",
        "Every normalized candidate evidence item must be a dict.",
    ),
    (
        "P2D42_EVIDENCE_ITEM_KEYS_INVALID",
        "Every normalized candidate evidence item must use the exact keys.",
    ),
    (
        "P2D42_EVIDENCE_ITEM_FIELD_INVALID",
        "A normalized candidate evidence item field is invalid.",
    ),
    (
        "P2D42_EVIDENCE_RELATIONSHIP_INVALID",
        "The normalized candidate evidence ID relationships are invalid.",
    ),
    ("P2D42_RECEIPT_NOT_DICT", "The P2D-42 receipt must be a dict."),
    (
        "P2D42_RECEIPT_KEYS_INVALID",
        "The P2D-42 receipt must contain the exact approved keys.",
    ),
    (
        "P2D42_RECEIPT_KIND_INVALID",
        "The P2D-42 receipt kind is invalid.",
    ),
    (
        "P2D42_RECEIPT_SCOPE_INVALID",
        "The P2D-42 receipt scope is invalid.",
    ),
    (
        "P2D42_RECEIPT_FIELD_INVALID",
        "A required P2D-42 receipt field is invalid.",
    ),
    (
        "P2D42_SOURCE_CANDIDATE_RECEIPT_MISMATCH",
        "The P2D-42 source, normalized candidate, and receipt are incoherent.",
    ),
)

_P2D42_SUCCESS_REASON: Final[str] = (
    "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_CONSUMED_IN_MEMORY"
)
_P2D41_SUCCESS_REASON: Final[str] = (
    "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_ASSEMBLED"
)
_SUCCESS_REASON: Final[str] = (
    "LOCAL_NOOP_TERMINAL_RESULT_ASSEMBLY_DECISION_CREATED"
)
_CANDIDATE_KIND: Final[str] = "local_noop_runner_result_candidate"
_RECEIPT_KIND: Final[str] = (
    "local_noop_runner_result_candidate_consumption_receipt"
)
_CONSUMPTION_SCOPE: Final[str] = (
    "pure_in_memory_validation_and_normalization_only"
)
_DECISION_KIND: Final[str] = (
    "local_noop_terminal_result_assembly_decision"
)
_DECISION_VALUE: Final[str] = (
    "NOOP_TERMINAL_RESULT_ASSEMBLY_ELIGIBLE"
)
_DECISION_SCOPE: Final[str] = (
    "future_separately_authorized_pure_terminal_result_assembly_only"
)
_NOOP_MODE: Final[str] = "noop"
_NOOP_COMPLETED: Final[str] = "NOOP_COMPLETED"
_PASS_PUBLISHED: Final[str] = "PASS_PUBLISHED"
_FORBIDDEN_FIELD_SENTINEL: Final[str] = (
    "p2d42_consumer_result.forbidden_field_or_namespace"
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
    if not isinstance(value, tuple) or value == ():
        return False
    for item in value:
        if not _is_nonblank_string(item):
            return False
    return True


def _values_match_exactly(left: object, right: object) -> bool:
    return type(left) is type(right) and left == right


def _copy_string_tuple(value: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(item for item in value)


def _safe_string_tuple(value: object) -> tuple[str, ...]:
    if not isinstance(value, tuple):
        return ()
    return tuple(item for item in value if isinstance(item, str))


def _has_exact_keys(value: dict[str, object], keys: tuple[str, ...]) -> bool:
    if len(value) != len(keys):
        return False
    for key in keys:
        if key not in value:
            return False
    return True


def _reason_text(reason_code: str) -> str:
    for candidate_reason_code, reason in _REASON_TEXT_ENTRIES:
        if candidate_reason_code == reason_code:
            return reason
    return "The local noop terminal-result assembly decision was not created."


def _add_reason(reason_codes: list[str], reason_code: str) -> None:
    if reason_code not in reason_codes:
        reason_codes.append(reason_code)


def _add_field(
    field_entries: list[tuple[str, str]],
    *,
    reason_code: str,
    field: str,
) -> None:
    entry = (reason_code, field)
    if entry not in field_entries:
        field_entries.append(entry)


def _add_violation(
    reason_codes: list[str],
    field_entries: list[tuple[str, str]],
    *,
    reason_code: str,
    field: str,
) -> None:
    _add_reason(reason_codes, reason_code)
    _add_field(field_entries, reason_code=reason_code, field=field)


def _ordered_reason_codes(reason_codes: tuple[str, ...]) -> tuple[str, ...]:
    ordered = ()
    for reason_code in REASON_PRIORITY:
        if reason_code != _SUCCESS_REASON and reason_code in reason_codes:
            ordered = ordered + (reason_code,)
    return ordered


def _ordered_field_entries(
    field_entries: tuple[tuple[str, str], ...],
) -> tuple[tuple[str, str], ...]:
    ordered = ()
    for reason_code in REASON_PRIORITY:
        if reason_code == _SUCCESS_REASON:
            continue
        for entry_reason_code, field in field_entries:
            entry = (entry_reason_code, field)
            if entry_reason_code == reason_code and entry not in ordered:
                ordered = ordered + (entry,)
    return ordered


def _ordered_fields(
    field_entries: tuple[tuple[str, str], ...],
) -> tuple[str, ...]:
    ordered = ()
    for _, field in _ordered_field_entries(field_entries):
        if field not in ordered:
            ordered = ordered + (field,)
    return ordered


def _validation_violation_records(
    field_entries: tuple[tuple[str, str], ...],
) -> tuple[dict[str, object], ...]:
    records = ()
    for reason_code, field in _ordered_field_entries(field_entries):
        records = records + (
            {
                "reason_code": reason_code,
                "field": field,
            },
        )
    return records


def _normalized_key(key: object) -> str:
    if not isinstance(key, str):
        return ""
    return key.strip().casefold().replace("-", "_").replace(" ", "_")


def _is_evidence_item_path(path: tuple[object, ...]) -> bool:
    return (
        len(path) == 3
        and path[0] == "normalized_local_noop_runner_result_candidate"
        and path[1] == "result_candidate_evidence_items"
        and isinstance(path[2], int)
    )


def _approved_keys_for_path(path: tuple[object, ...]) -> tuple[str, ...]:
    if path == ():
        return _ROOT_KEYS
    if path == ("source",):
        return _SOURCE_KEYS
    if path == ("normalized_local_noop_runner_result_candidate",):
        return _CANDIDATE_KEYS
    if path == ("local_noop_runner_consumption_receipt",):
        return _RECEIPT_KEYS
    if _is_evidence_item_path(path):
        return _EVIDENCE_ITEM_KEYS
    return ()


def _is_declared_schema_key(key: str) -> bool:
    return (
        key in _ROOT_KEYS
        or key in _SOURCE_KEYS
        or key in _CANDIDATE_KEYS
        or key in _RECEIPT_KEYS
        or key in _EVIDENCE_ITEM_KEYS
    )


def _matches_forbidden_catalog(key: str) -> bool:
    if key in _FORBIDDEN_EXACT_KEYS:
        return True
    for prefix in _FORBIDDEN_PREFIXES:
        if key.startswith(prefix):
            return True
    for suffix in _FORBIDDEN_SUFFIXES:
        if key.endswith(suffix):
            return True
    return False


def _scan_forbidden_keys(
    value: object,
    *,
    path: tuple[object, ...],
    reason_codes: list[str],
    field_entries: list[tuple[str, str]],
) -> None:
    stack = [(value, path)]
    visited_container_ids: set[int] = set()

    while stack:
        current, current_path = stack.pop()
        if not isinstance(current, (dict, list, tuple)):
            continue

        current_id = id(current)
        if current_id in visited_container_ids:
            continue
        visited_container_ids.add(current_id)

        children = []
        if isinstance(current, dict):
            approved_keys = _approved_keys_for_path(current_path)
            for key, nested_value in current.items():
                normalized_key = _normalized_key(key)
                key_is_approved = (
                    isinstance(key, str)
                    and key == normalized_key
                    and key in approved_keys
                )
                key_is_declared_elsewhere = _is_declared_schema_key(
                    normalized_key
                )
                if not key_is_approved and (
                    key_is_declared_elsewhere
                    or _matches_forbidden_catalog(normalized_key)
                ):
                    _add_violation(
                        reason_codes,
                        field_entries,
                        reason_code=(
                            "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"
                        ),
                        field=_FORBIDDEN_FIELD_SENTINEL,
                    )
                child_component = (
                    key if isinstance(key, str) else "<key>"
                )
                children.append(
                    (
                        nested_value,
                        current_path + (child_component,),
                    )
                )
        else:
            for index, nested_value in enumerate(current):
                children.append(
                    (nested_value, current_path + (index,))
                )

        for child in reversed(children):
            stack.append(child)


def _validate_mode_and_public_url(
    value: dict[str, object],
    *,
    prefix: str,
    reason_codes: list[str],
    field_entries: list[tuple[str, str]],
) -> None:
    if value.get("mode") != _NOOP_MODE:
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="MODE_NOT_NOOP",
            field=f"{prefix}.mode",
        )
    if value.get("public_url") is not None:
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="PUBLIC_URL_NOT_NULL",
            field=f"{prefix}.public_url",
        )
    if value.get("public_url_created") is not False:
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="PUBLIC_URL_CREATED_NOT_FALSE",
            field=f"{prefix}.public_url_created",
        )


def _validate_source(
    source: dict[str, object],
    *,
    reason_codes: list[str],
    field_entries: list[tuple[str, str]],
) -> None:
    prefix = "p2d42_consumer_result.source"
    if source.get("p2d41_assembled") is not True:
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="P2D42_SOURCE_FIELD_INVALID",
            field=f"{prefix}.p2d41_assembled",
        )
    if source.get("p2d41_reason_code") != _P2D41_SUCCESS_REASON:
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="P2D42_SOURCE_FIELD_INVALID",
            field=f"{prefix}.p2d41_reason_code",
        )
    if not _is_nonblank_string(
        source.get("local_noop_runner_result_candidate_id")
    ):
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="P2D42_SOURCE_FIELD_INVALID",
            field=f"{prefix}.local_noop_runner_result_candidate_id",
        )
    if source.get("candidate_kind") != _CANDIDATE_KIND:
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="P2D42_SOURCE_FIELD_INVALID",
            field=f"{prefix}.candidate_kind",
        )
    if not _is_nonempty_string_tuple(source.get("source_of_truth")):
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="P2D42_SOURCE_FIELD_INVALID",
            field=f"{prefix}.source_of_truth",
        )
    _validate_mode_and_public_url(
        source,
        prefix=prefix,
        reason_codes=reason_codes,
        field_entries=field_entries,
    )


def _validate_evidence(
    candidate: dict[str, object],
    *,
    reason_codes: list[str],
    field_entries: list[tuple[str, str]],
) -> None:
    prefix = "p2d42_consumer_result.normalized_candidate"
    evidence_path = f"{prefix}.evidence_items"
    evidence_items_value = candidate.get("result_candidate_evidence_items")
    if not isinstance(evidence_items_value, tuple) or evidence_items_value == ():
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="P2D42_NORMALIZED_CANDIDATE_FIELD_INVALID",
            field=evidence_path,
        )
        evidence_items = ()
    else:
        evidence_items = evidence_items_value

    required_ids_value = candidate.get(
        "required_result_candidate_evidence_ids"
    )
    required_ids_valid = _is_nonempty_string_tuple(required_ids_value)
    if not required_ids_valid:
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="P2D42_EVIDENCE_RELATIONSHIP_INVALID",
            field=f"{prefix}.required_result_candidate_evidence_ids",
        )
    required_ids = _safe_string_tuple(required_ids_value)
    if len(required_ids) != len(tuple(dict.fromkeys(required_ids))):
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="P2D42_EVIDENCE_RELATIONSHIP_INVALID",
            field=f"{prefix}.required_result_candidate_evidence_ids",
        )

    if candidate.get("missing_result_candidate_evidence_ids") != ():
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="P2D42_EVIDENCE_RELATIONSHIP_INVALID",
            field=f"{prefix}.missing_result_candidate_evidence_ids",
        )

    known_ids = ()
    seen_ids = ()
    for index, evidence_item in enumerate(evidence_items):
        item_prefix = f"{evidence_path}[{index}]"
        if not isinstance(evidence_item, dict):
            _add_violation(
                reason_codes,
                field_entries,
                reason_code="P2D42_EVIDENCE_ITEM_NOT_DICT",
                field=item_prefix,
            )
            continue
        if not _has_exact_keys(evidence_item, _EVIDENCE_ITEM_KEYS):
            _add_violation(
                reason_codes,
                field_entries,
                reason_code="P2D42_EVIDENCE_ITEM_KEYS_INVALID",
                field=f"{item_prefix}.keys",
            )
        for field in _EVIDENCE_STRING_FIELDS:
            if not _is_nonblank_string(evidence_item.get(field)):
                _add_violation(
                    reason_codes,
                    field_entries,
                    reason_code="P2D42_EVIDENCE_ITEM_FIELD_INVALID",
                    field=f"{item_prefix}.{field}",
                )
        if evidence_item.get("evidence_status") == _PASS_PUBLISHED:
            _add_violation(
                reason_codes,
                field_entries,
                reason_code="PASS_PUBLISHED_FORBIDDEN",
                field=f"{item_prefix}.evidence_status",
            )
        if not _is_nonempty_string_tuple(evidence_item.get("evidence_refs")):
            _add_violation(
                reason_codes,
                field_entries,
                reason_code="P2D42_EVIDENCE_ITEM_FIELD_INVALID",
                field=f"{item_prefix}.evidence_refs",
            )
        if not _is_string_tuple(evidence_item.get("notes")):
            _add_violation(
                reason_codes,
                field_entries,
                reason_code="P2D42_EVIDENCE_ITEM_FIELD_INVALID",
                field=f"{item_prefix}.notes",
            )

        evidence_id = evidence_item.get("result_candidate_evidence_id")
        if _is_nonblank_string(evidence_id):
            known_ids = known_ids + (evidence_id,)
            if evidence_id in seen_ids:
                _add_violation(
                    reason_codes,
                    field_entries,
                    reason_code="P2D42_EVIDENCE_RELATIONSHIP_INVALID",
                    field=f"{item_prefix}.result_candidate_evidence_id",
                )
            else:
                seen_ids = seen_ids + (evidence_id,)
            if required_ids_valid and evidence_id not in required_ids:
                _add_violation(
                    reason_codes,
                    field_entries,
                    reason_code="P2D42_EVIDENCE_RELATIONSHIP_INVALID",
                    field=f"{item_prefix}.result_candidate_evidence_id",
                )

    if required_ids_valid:
        for required_id in required_ids:
            if required_id not in known_ids:
                _add_violation(
                    reason_codes,
                    field_entries,
                    reason_code="P2D42_EVIDENCE_RELATIONSHIP_INVALID",
                    field=f"{prefix}.required_result_candidate_evidence_ids",
                )

    blocking_ids = candidate.get("blocking_result_candidate_evidence_ids")
    if not isinstance(blocking_ids, tuple):
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="P2D42_EVIDENCE_RELATIONSHIP_INVALID",
            field=f"{prefix}.blocking_result_candidate_evidence_ids",
        )
    else:
        for blocking_id in blocking_ids:
            if not _is_nonblank_string(blocking_id) or blocking_id not in known_ids:
                _add_violation(
                    reason_codes,
                    field_entries,
                    reason_code="P2D42_EVIDENCE_RELATIONSHIP_INVALID",
                    field=f"{prefix}.blocking_result_candidate_evidence_ids",
                )


def _validate_candidate(
    candidate: dict[str, object],
    *,
    reason_codes: list[str],
    field_entries: list[tuple[str, str]],
) -> None:
    prefix = "p2d42_consumer_result.normalized_candidate"
    for field in (
        "run_id",
        "local_noop_runner_result_candidate_id",
        "local_noop_runner_readiness_ref",
        "local_noop_runner_readiness_id",
        "created_at",
        "timestamp_policy",
    ):
        if not _is_nonblank_string(candidate.get(field)):
            _add_violation(
                reason_codes,
                field_entries,
                reason_code="P2D42_NORMALIZED_CANDIDATE_FIELD_INVALID",
                field=f"{prefix}.{field}",
            )
    if candidate.get("candidate_kind") != _CANDIDATE_KIND:
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="P2D42_NORMALIZED_CANDIDATE_FIELD_INVALID",
            field=f"{prefix}.candidate_kind",
        )
    if candidate.get("local_noop_runner_readiness_buildable_marker") is not True:
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="P2D42_NORMALIZED_CANDIDATE_FIELD_INVALID",
            field=f"{prefix}.local_noop_runner_readiness_buildable_marker",
        )
    runner_terminal_status = candidate.get("runner_terminal_status")
    if runner_terminal_status == _PASS_PUBLISHED:
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="PASS_PUBLISHED_FORBIDDEN",
            field=f"{prefix}.runner_terminal_status",
        )
    if runner_terminal_status != _NOOP_COMPLETED:
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="RUNNER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
            field=f"{prefix}.runner_terminal_status",
        )
    if not _is_nonempty_string_tuple(candidate.get("source_of_truth")):
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="P2D42_NORMALIZED_CANDIDATE_FIELD_INVALID",
            field=f"{prefix}.source_of_truth",
        )
    if not _is_string_tuple(candidate.get("notes")):
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="P2D42_NORMALIZED_CANDIDATE_FIELD_INVALID",
            field=f"{prefix}.notes",
        )
    _validate_mode_and_public_url(
        candidate,
        prefix=prefix,
        reason_codes=reason_codes,
        field_entries=field_entries,
    )
    _validate_evidence(
        candidate,
        reason_codes=reason_codes,
        field_entries=field_entries,
    )


def _validate_receipt(
    receipt: dict[str, object],
    *,
    reason_codes: list[str],
    field_entries: list[tuple[str, str]],
) -> None:
    prefix = "p2d42_consumer_result.receipt"
    if receipt.get("receipt_kind") != _RECEIPT_KIND:
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="P2D42_RECEIPT_KIND_INVALID",
            field=f"{prefix}.receipt_kind",
        )
    if receipt.get("consumption_scope") != _CONSUMPTION_SCOPE:
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="P2D42_RECEIPT_SCOPE_INVALID",
            field=f"{prefix}.consumption_scope",
        )
    for field in ("run_id", "local_noop_runner_result_candidate_id"):
        if not _is_nonblank_string(receipt.get(field)):
            _add_violation(
                reason_codes,
                field_entries,
                reason_code="P2D42_RECEIPT_FIELD_INVALID",
                field=f"{prefix}.{field}",
            )
    if receipt.get("candidate_kind") != _CANDIDATE_KIND:
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="P2D42_RECEIPT_FIELD_INVALID",
            field=f"{prefix}.candidate_kind",
        )
    _validate_mode_and_public_url(
        receipt,
        prefix=prefix,
        reason_codes=reason_codes,
        field_entries=field_entries,
    )


def _validate_coherence(
    source: dict[str, object],
    candidate: dict[str, object],
    receipt: dict[str, object],
    *,
    reason_codes: list[str],
    field_entries: list[tuple[str, str]],
) -> None:
    reason_code = "P2D42_SOURCE_CANDIDATE_RECEIPT_MISMATCH"
    for field in _SOURCE_CANDIDATE_COHERENCE_FIELDS:
        if not _values_match_exactly(source.get(field), candidate.get(field)):
            _add_violation(
                reason_codes,
                field_entries,
                reason_code=reason_code,
                field=f"p2d42_consumer_result.source.{field}",
            )
    for field in _CANDIDATE_RECEIPT_COHERENCE_FIELDS:
        if not _values_match_exactly(candidate.get(field), receipt.get(field)):
            _add_violation(
                reason_codes,
                field_entries,
                reason_code=reason_code,
                field=f"p2d42_consumer_result.receipt.{field}",
            )
    for field in _SOURCE_RECEIPT_COHERENCE_FIELDS:
        if not _values_match_exactly(source.get(field), receipt.get(field)):
            _add_violation(
                reason_codes,
                field_entries,
                reason_code=reason_code,
                field=f"p2d42_consumer_result.receipt.{field}",
            )


def _blocked_source() -> dict[str, object]:
    return {
        "p2d42_consumed": False,
        "p2d42_reason_code": "",
        "local_noop_runner_result_candidate_id": "",
        "local_noop_runner_consumption_receipt_kind": "",
        "mode": "",
        "candidate_runner_terminal_status": "",
        "public_url": None,
        "public_url_created": False,
        "source_of_truth": (),
    }


def _successful_source(candidate: dict[str, object]) -> dict[str, object]:
    source_of_truth = candidate["source_of_truth"]
    return {
        "p2d42_consumed": True,
        "p2d42_reason_code": _P2D42_SUCCESS_REASON,
        "local_noop_runner_result_candidate_id": candidate[
            "local_noop_runner_result_candidate_id"
        ],
        "local_noop_runner_consumption_receipt_kind": _RECEIPT_KIND,
        "mode": _NOOP_MODE,
        "candidate_runner_terminal_status": _NOOP_COMPLETED,
        "public_url": None,
        "public_url_created": False,
        "source_of_truth": _copy_string_tuple(source_of_truth),
    }


def _successful_decision(candidate: dict[str, object]) -> dict[str, object]:
    return {
        "decision_kind": _DECISION_KIND,
        "decision_value": _DECISION_VALUE,
        "decision_scope": _DECISION_SCOPE,
        "run_id": candidate["run_id"],
        "local_noop_runner_result_candidate_id": candidate[
            "local_noop_runner_result_candidate_id"
        ],
        "local_noop_runner_consumption_receipt_kind": _RECEIPT_KIND,
        "mode": _NOOP_MODE,
        "public_url": None,
        "public_url_created": False,
    }


def decide_local_noop_terminal_result_assembly(
    *,
    local_noop_runner_result_candidate_consumption: dict[str, object],
) -> dict[str, object]:
    """Create one pure declarative terminal-result assembly decision."""

    reason_codes = []
    field_entries = []

    scan_path = ()
    if (
        isinstance(local_noop_runner_result_candidate_consumption, dict)
        and _has_exact_keys(
            local_noop_runner_result_candidate_consumption,
            _CANDIDATE_KEYS,
        )
    ):
        scan_path = ("normalized_local_noop_runner_result_candidate",)

    _scan_forbidden_keys(
        local_noop_runner_result_candidate_consumption,
        path=scan_path,
        reason_codes=reason_codes,
        field_entries=field_entries,
    )

    if not isinstance(local_noop_runner_result_candidate_consumption, dict):
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="P2D42_CONSUMER_RESULT_NOT_DICT",
            field="<root>",
        )
        consumer_result = {}
    else:
        consumer_result = local_noop_runner_result_candidate_consumption
        if not _has_exact_keys(consumer_result, _ROOT_KEYS):
            _add_violation(
                reason_codes,
                field_entries,
                reason_code="P2D42_CONSUMER_RESULT_KEYS_INVALID",
                field="p2d42_consumer_result.keys",
            )
        if consumer_result.get("consumed") is not True:
            _add_violation(
                reason_codes,
                field_entries,
                reason_code="P2D42_CONSUMED_MARKER_NOT_TRUE",
                field="p2d42_consumer_result.consumed",
            )
        if consumer_result.get("reason_code") != _P2D42_SUCCESS_REASON:
            _add_violation(
                reason_codes,
                field_entries,
                reason_code="P2D42_CONSUMPTION_REASON_CODE_INVALID",
                field="p2d42_consumer_result.reason_code",
            )
        if not _is_nonblank_string(consumer_result.get("reason")):
            _add_violation(
                reason_codes,
                field_entries,
                reason_code="P2D42_CONSUMPTION_REASON_MISSING",
                field="p2d42_consumer_result.reason",
            )
        if consumer_result.get("consumption_violations") != ():
            _add_violation(
                reason_codes,
                field_entries,
                reason_code="P2D42_CONSUMPTION_VIOLATIONS_NOT_EMPTY",
                field="p2d42_consumer_result.consumption_violations",
            )
        if consumer_result.get("missing_or_invalid_fields") != ():
            _add_violation(
                reason_codes,
                field_entries,
                reason_code="P2D42_MISSING_OR_INVALID_FIELDS_NOT_EMPTY",
                field="p2d42_consumer_result.missing_or_invalid_fields",
            )
        if consumer_result.get("result_candidate_evidence_item_violations") != ():
            _add_violation(
                reason_codes,
                field_entries,
                reason_code="P2D42_EVIDENCE_ITEM_VIOLATIONS_NOT_EMPTY",
                field=(
                    "p2d42_consumer_result."
                    "result_candidate_evidence_item_violations"
                ),
            )

        invariant_refs = consumer_result.get("invariant_refs")
        if not _is_nonempty_string_tuple(invariant_refs):
            _add_violation(
                reason_codes,
                field_entries,
                reason_code="P2D42_INVARIANT_REFS_INVALID",
                field="p2d42_consumer_result.invariant_refs",
            )
        safe_invariant_refs = _safe_string_tuple(invariant_refs)
        for required_ref in _REQUIRED_P2D42_INVARIANT_REFS:
            if required_ref not in safe_invariant_refs:
                _add_violation(
                    reason_codes,
                    field_entries,
                    reason_code="P2D42_REQUIRED_INVARIANT_REF_MISSING",
                    field="p2d42_consumer_result.invariant_refs",
                )

    source_value = consumer_result.get("source")
    if not isinstance(source_value, dict):
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="P2D42_SOURCE_NOT_DICT",
            field="p2d42_consumer_result.source",
        )
        source = {}
    else:
        source = source_value
        if not _has_exact_keys(source, _SOURCE_KEYS):
            _add_violation(
                reason_codes,
                field_entries,
                reason_code="P2D42_SOURCE_KEYS_INVALID",
                field="p2d42_consumer_result.source.keys",
            )
        _validate_source(
            source,
            reason_codes=reason_codes,
            field_entries=field_entries,
        )

    candidate_value = consumer_result.get(
        "normalized_local_noop_runner_result_candidate"
    )
    if not isinstance(candidate_value, dict):
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="P2D42_NORMALIZED_CANDIDATE_NOT_DICT",
            field="p2d42_consumer_result.normalized_candidate",
        )
        candidate = {}
    else:
        candidate = candidate_value
        if not _has_exact_keys(candidate, _CANDIDATE_KEYS):
            _add_violation(
                reason_codes,
                field_entries,
                reason_code="P2D42_NORMALIZED_CANDIDATE_KEYS_INVALID",
                field="p2d42_consumer_result.normalized_candidate.keys",
            )
        _validate_candidate(
            candidate,
            reason_codes=reason_codes,
            field_entries=field_entries,
        )

    receipt_value = consumer_result.get("local_noop_runner_consumption_receipt")
    if not isinstance(receipt_value, dict):
        _add_violation(
            reason_codes,
            field_entries,
            reason_code="P2D42_RECEIPT_NOT_DICT",
            field="p2d42_consumer_result.receipt",
        )
        receipt = {}
    else:
        receipt = receipt_value
        if not _has_exact_keys(receipt, _RECEIPT_KEYS):
            _add_violation(
                reason_codes,
                field_entries,
                reason_code="P2D42_RECEIPT_KEYS_INVALID",
                field="p2d42_consumer_result.receipt.keys",
            )
        _validate_receipt(
            receipt,
            reason_codes=reason_codes,
            field_entries=field_entries,
        )

    if (
        isinstance(source_value, dict)
        and isinstance(candidate_value, dict)
        and isinstance(receipt_value, dict)
    ):
        _validate_coherence(
            source,
            candidate,
            receipt,
            reason_codes=reason_codes,
            field_entries=field_entries,
        )

    decision_violations = _ordered_reason_codes(tuple(reason_codes))
    decision_created = decision_violations == ()
    reason_code = _SUCCESS_REASON if decision_created else decision_violations[0]

    if decision_created:
        source_output = _successful_source(candidate)
        decision_output = _successful_decision(candidate)
    else:
        source_output = _blocked_source()
        decision_output = {}

    return {
        "decision_created": decision_created,
        "reason_code": reason_code,
        "reason": _reason_text(reason_code),
        "source": source_output,
        "local_noop_terminal_result_assembly_decision": decision_output,
        "decision_violations": decision_violations,
        "missing_or_invalid_fields": _ordered_fields(tuple(field_entries)),
        "decision_validation_violations": _validation_violation_records(
            tuple(field_entries)
        ),
        "invariant_refs": _INVARIANT_REFS,
    }


def is_local_noop_terminal_result_assembly_decision_created(
    *,
    local_noop_runner_result_candidate_consumption: dict[str, object],
) -> bool:
    """Return whether the pure declarative decision was created."""

    return decide_local_noop_terminal_result_assembly(
        local_noop_runner_result_candidate_consumption=(
            local_noop_runner_result_candidate_consumption
        ),
    )["decision_created"]
