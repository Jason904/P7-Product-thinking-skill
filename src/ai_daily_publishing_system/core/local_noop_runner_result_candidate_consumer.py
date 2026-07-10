"""Consume a validated local noop runner result candidate in memory only."""

from typing import Final


REASON_CODES: Final[tuple[str, ...]] = (
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

LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_CONSUMPTION_REASON_CODES: Final[
    tuple[str, ...]
] = REASON_CODES

REASON_PRIORITY: Final[tuple[str, ...]] = (
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

_ROOT_KEYS: Final[tuple[str, ...]] = (
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

_SOURCE_KEYS: Final[tuple[str, ...]] = (
    "mode",
    "runner_terminal_status",
    "local_noop_runner_readiness_ref",
    "local_noop_runner_readiness_id",
    "local_noop_runner_readiness_buildable_marker",
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

_EVIDENCE_STRING_FIELDS: Final[tuple[tuple[str, str], ...]] = (
    ("result_candidate_evidence_id", "RESULT_CANDIDATE_EVIDENCE_ID_MISSING"),
    (
        "result_candidate_evidence_role",
        "RESULT_CANDIDATE_EVIDENCE_ROLE_MISSING",
    ),
    (
        "artifact_ref",
        "RESULT_CANDIDATE_EVIDENCE_ARTIFACT_REF_MISSING",
    ),
    (
        "artifact_kind",
        "RESULT_CANDIDATE_EVIDENCE_ARTIFACT_KIND_MISSING",
    ),
    ("evidence_status", "RESULT_CANDIDATE_EVIDENCE_STATUS_MISSING"),
    (
        "producer_ref",
        "RESULT_CANDIDATE_EVIDENCE_PRODUCER_REF_MISSING",
    ),
)

_COHERENCE_FIELDS: Final[tuple[str, ...]] = (
    "mode",
    "runner_terminal_status",
    "local_noop_runner_readiness_ref",
    "local_noop_runner_readiness_id",
    "local_noop_runner_readiness_buildable_marker",
    "public_url",
    "public_url_created",
    "source_of_truth",
)

_REQUIRED_P2D41_INVARIANT_REFS: Final[tuple[str, ...]] = (
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

_FORBIDDEN_EXACT_KEYS: Final[tuple[str, ...]] = (
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

_REASON_TEXT_ENTRIES: Final[tuple[tuple[str, str], ...]] = (
    (
        "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_CONSUMED_IN_MEMORY",
        "The complete P2D-41 result candidate assembly was accepted and "
        "normalized in memory only; no execution, completion, ledger, "
        "publish, public URL, or notification behavior occurred.",
    ),
    ("CANDIDATE_ASSEMBLY_NOT_DICT", "The P2D-41 assembly must be a dict."),
    (
        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
        "The caller payload contains a forbidden field or namespace.",
    ),
    (
        "CANDIDATE_ASSEMBLY_KEYS_INVALID",
        "The P2D-41 assembly must contain the exact approved root keys.",
    ),
    (
        "P2D41_ASSEMBLED_MARKER_NOT_TRUE",
        "The P2D-41 assembled marker must be exactly true.",
    ),
    (
        "P2D41_ASSEMBLY_REASON_CODE_INVALID",
        "The P2D-41 reason code must declare successful assembly.",
    ),
    (
        "P2D41_ASSEMBLY_REASON_MISSING",
        "The P2D-41 assembly requires a nonblank reason.",
    ),
    (
        "P2D41_ASSEMBLY_VIOLATIONS_NOT_EMPTY",
        "The P2D-41 assembly violations must be empty.",
    ),
    (
        "P2D41_MISSING_OR_INVALID_FIELDS_NOT_EMPTY",
        "The P2D-41 missing-or-invalid fields must be empty.",
    ),
    (
        "P2D41_EVIDENCE_ITEM_VIOLATIONS_NOT_EMPTY",
        "The P2D-41 evidence item violations must be empty.",
    ),
    (
        "P2D41_INVARIANT_REFS_INVALID",
        "The P2D-41 invariant refs must be nonempty nonblank strings.",
    ),
    (
        "P2D41_REQUIRED_INVARIANT_REF_MISSING",
        "A required P2D-41 invariant reference is missing.",
    ),
    ("P2D41_SOURCE_NOT_DICT", "The P2D-41 source must be a dict."),
    (
        "P2D41_SOURCE_KEYS_INVALID",
        "The P2D-41 source must contain the exact approved keys.",
    ),
    (
        "P2D41_RESULT_CANDIDATE_NOT_DICT",
        "The P2D-41 result candidate must be a dict.",
    ),
    (
        "P2D41_RESULT_CANDIDATE_KEYS_INVALID",
        "The P2D-41 result candidate must contain the exact approved keys.",
    ),
    ("RUN_ID_MISSING", "A nonblank caller-supplied run_id is required."),
    (
        "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_ID_MISSING",
        "A nonblank caller-supplied result candidate id is required.",
    ),
    (
        "CANDIDATE_KIND_NOT_LOCAL_NOOP_RUNNER_RESULT_CANDIDATE",
        "candidate_kind must be local_noop_runner_result_candidate.",
    ),
    ("MODE_NOT_NOOP", "mode must be noop."),
    (
        "PASS_PUBLISHED_FORBIDDEN",
        "PASS_PUBLISHED is forbidden at the noop consumer boundary.",
    ),
    (
        "RUNNER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
        "runner_terminal_status must be declarative NOOP_COMPLETED.",
    ),
    (
        "LOCAL_NOOP_RUNNER_READINESS_REF_MISSING",
        "A nonblank caller-supplied readiness ref is required.",
    ),
    (
        "LOCAL_NOOP_RUNNER_READINESS_ID_MISSING",
        "A nonblank caller-supplied readiness id is required.",
    ),
    (
        "LOCAL_NOOP_RUNNER_READINESS_BUILDABLE_MARKER_NOT_TRUE",
        "The readiness buildable marker must be exactly true.",
    ),
    ("PUBLIC_URL_NOT_NULL", "public_url must remain null."),
    (
        "PUBLIC_URL_CREATED_NOT_FALSE",
        "public_url_created must remain exactly false.",
    ),
    (
        "P2D41_SOURCE_CANDIDATE_MISMATCH",
        "The P2D-41 source and candidate lock-ins must match.",
    ),
    (
        "RESULT_CANDIDATE_EVIDENCE_ITEMS_MISSING",
        "At least one result candidate evidence item is required.",
    ),
    (
        "REQUIRED_RESULT_CANDIDATE_EVIDENCE_IDS_MISSING",
        "At least one required nonblank evidence id is required.",
    ),
    (
        "MISSING_RESULT_CANDIDATE_EVIDENCE_IDS_DECLARED",
        "Missing result candidate evidence ids must be empty.",
    ),
    (
        "BLOCKING_RESULT_CANDIDATE_EVIDENCE_ID_UNKNOWN",
        "Blocking evidence ids must be known nonblank ids in a tuple.",
    ),
    ("CREATED_AT_MISSING", "A nonblank caller-supplied created_at is required."),
    (
        "TIMESTAMP_POLICY_MISSING",
        "A nonblank caller-supplied timestamp_policy is required.",
    ),
    (
        "SOURCE_OF_TRUTH_MISSING",
        "At least one nonblank source-of-truth reference is required.",
    ),
    ("NOTES_INVALID", "Candidate notes must be a tuple of strings."),
    (
        "RESULT_CANDIDATE_EVIDENCE_ITEM_NOT_DICT",
        "Every result candidate evidence item must be a dict.",
    ),
    (
        "RESULT_CANDIDATE_EVIDENCE_ITEM_KEYS_INVALID",
        "Every evidence item must contain the exact approved keys.",
    ),
    (
        "RESULT_CANDIDATE_EVIDENCE_ID_MISSING",
        "Every evidence item requires a nonblank id.",
    ),
    (
        "RESULT_CANDIDATE_EVIDENCE_ROLE_MISSING",
        "Every evidence item requires a nonblank role.",
    ),
    (
        "RESULT_CANDIDATE_EVIDENCE_ARTIFACT_REF_MISSING",
        "Every evidence item requires a nonblank artifact_ref.",
    ),
    (
        "RESULT_CANDIDATE_EVIDENCE_ARTIFACT_KIND_MISSING",
        "Every evidence item requires a nonblank artifact_kind.",
    ),
    (
        "RESULT_CANDIDATE_EVIDENCE_STATUS_MISSING",
        "Every evidence item requires a nonblank evidence_status.",
    ),
    (
        "RESULT_CANDIDATE_EVIDENCE_PRODUCER_REF_MISSING",
        "Every evidence item requires a nonblank producer_ref.",
    ),
    (
        "RESULT_CANDIDATE_EVIDENCE_REFS_MISSING",
        "Every evidence item requires nonblank evidence_refs.",
    ),
    (
        "RESULT_CANDIDATE_EVIDENCE_NOTES_INVALID",
        "Evidence notes must be a tuple of strings.",
    ),
    (
        "RESULT_CANDIDATE_EVIDENCE_ID_DUPLICATE",
        "Result candidate evidence ids must be unique.",
    ),
    (
        "RESULT_CANDIDATE_EVIDENCE_ID_NOT_REQUIRED",
        "Every evidence id must be declared as required.",
    ),
    (
        "REQUIRED_RESULT_CANDIDATE_EVIDENCE_MISSING",
        "Every required evidence id must have one evidence item.",
    ),
)

_CANDIDATE_KIND: Final[str] = "local_noop_runner_result_candidate"
_P2D41_SUCCESS_REASON: Final[str] = (
    "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_ASSEMBLED"
)
_SUCCESS_REASON: Final[str] = (
    "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_CONSUMED_IN_MEMORY"
)
_NOOP_MODE: Final[str] = "noop"
_NOOP_COMPLETED: Final[str] = "NOOP_COMPLETED"
_PASS_PUBLISHED: Final[str] = "PASS_PUBLISHED"
_FORBIDDEN_FIELD_SENTINEL: Final[str] = (
    "candidate_assembly.forbidden_field_or_namespace"
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


def _safe_string(value: object) -> str:
    if isinstance(value, str):
        return value
    return ""


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
    return "The local noop runner result candidate was not consumed."


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


def _add_evidence_violation(
    violations: list[dict[str, object]],
    *,
    index: int,
    evidence_id: object,
    reason_code: str,
    field: str,
) -> None:
    violation = {
        "result_candidate_evidence_item_index": index,
        "result_candidate_evidence_id": _safe_string(evidence_id),
        "reason_code": reason_code,
        "field": field,
    }
    if violation not in violations:
        violations.append(violation)


def _ordered_reason_codes(reason_codes: tuple[str, ...]) -> tuple[str, ...]:
    ordered = ()
    for reason_code in REASON_PRIORITY:
        if reason_code != _SUCCESS_REASON and reason_code in reason_codes:
            ordered = ordered + (reason_code,)
    return ordered


def _ordered_fields(
    field_entries: tuple[tuple[str, str], ...],
) -> tuple[str, ...]:
    ordered = ()
    for reason_code in REASON_PRIORITY:
        if reason_code == _SUCCESS_REASON:
            continue
        for entry_reason_code, field in field_entries:
            if entry_reason_code == reason_code and field not in ordered:
                ordered = ordered + (field,)
    return ordered


def _ordered_evidence_violations(
    violations: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    ordered = ()
    for reason_code in REASON_PRIORITY:
        if reason_code == _SUCCESS_REASON:
            continue
        for violation in violations:
            if violation["reason_code"] == reason_code:
                ordered = ordered + (violation,)
    return ordered


def _normalized_key(key: object) -> str:
    if not isinstance(key, str):
        return ""
    return (
        key.strip()
        .casefold()
        .replace("-", "_")
        .replace(" ", "_")
    )


def _is_evidence_item_path(path: tuple[object, ...]) -> bool:
    return (
        len(path) == 3
        and path[0] == "local_noop_runner_result_candidate"
        and path[1] == "result_candidate_evidence_items"
        and isinstance(path[2], int)
    )


def _approved_keys_for_path(path: tuple[object, ...]) -> tuple[str, ...]:
    if path == ():
        return _ROOT_KEYS
    if path == ("source",):
        return _SOURCE_KEYS
    if path == ("local_noop_runner_result_candidate",):
        return _CANDIDATE_KEYS
    if _is_evidence_item_path(path):
        return _EVIDENCE_ITEM_KEYS
    return ()


def _is_declared_schema_key(key: str) -> bool:
    return (
        key in _ROOT_KEYS
        or key in _SOURCE_KEYS
        or key in _CANDIDATE_KEYS
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


def _path_text(path: tuple[object, ...]) -> str:
    text = ""
    for component in path:
        if isinstance(component, int):
            text = text + f"[{component}]"
        elif text == "":
            text = component if isinstance(component, str) else "<non_string_key>"
        else:
            label = component if isinstance(component, str) else "<non_string_key>"
            text = text + "." + label
    return text or "<root>"


def _scan_forbidden_keys(
    value: object,
    *,
    path: tuple[object, ...],
    reason_codes: list[str],
    field_entries: list[tuple[str, str]],
) -> None:
    if isinstance(value, dict):
        approved_keys = _approved_keys_for_path(path)
        for key, nested_value in value.items():
            normalized_key = _normalized_key(key)
            key_is_approved = (
                isinstance(key, str)
                and key == normalized_key
                and key in approved_keys
            )
            key_is_declared_elsewhere = _is_declared_schema_key(normalized_key)
            if not key_is_approved and (
                key_is_declared_elsewhere
                or _matches_forbidden_catalog(normalized_key)
            ):
                _add_reason(
                    reason_codes,
                    "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
                )
                _add_field(
                    field_entries,
                    reason_code="FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
                    field=_FORBIDDEN_FIELD_SENTINEL,
                )
            child_component = key if isinstance(key, str) else "<non_string_key>"
            _scan_forbidden_keys(
                nested_value,
                path=path + (child_component,),
                reason_codes=reason_codes,
                field_entries=field_entries,
            )
    elif isinstance(value, tuple) or isinstance(value, list):
        for index, nested_value in enumerate(value):
            _scan_forbidden_keys(
                nested_value,
                path=path + (index,),
                reason_codes=reason_codes,
                field_entries=field_entries,
            )


def _validate_noop_fields(
    value: dict[str, object],
    *,
    prefix: str,
    reason_codes: list[str],
    field_entries: list[tuple[str, str]],
) -> None:
    if value.get("mode") != _NOOP_MODE:
        _add_reason(reason_codes, "MODE_NOT_NOOP")
        _add_field(
            field_entries,
            reason_code="MODE_NOT_NOOP",
            field=f"{prefix}.mode",
        )

    runner_terminal_status = value.get("runner_terminal_status")
    if runner_terminal_status == _PASS_PUBLISHED:
        _add_reason(reason_codes, "PASS_PUBLISHED_FORBIDDEN")
        _add_field(
            field_entries,
            reason_code="PASS_PUBLISHED_FORBIDDEN",
            field=f"{prefix}.runner_terminal_status",
        )
    if runner_terminal_status != _NOOP_COMPLETED:
        _add_reason(
            reason_codes,
            "RUNNER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
        )
        _add_field(
            field_entries,
            reason_code="RUNNER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
            field=f"{prefix}.runner_terminal_status",
        )

    if not _is_nonblank_string(value.get("local_noop_runner_readiness_ref")):
        _add_reason(reason_codes, "LOCAL_NOOP_RUNNER_READINESS_REF_MISSING")
        _add_field(
            field_entries,
            reason_code="LOCAL_NOOP_RUNNER_READINESS_REF_MISSING",
            field=f"{prefix}.local_noop_runner_readiness_ref",
        )

    if not _is_nonblank_string(value.get("local_noop_runner_readiness_id")):
        _add_reason(reason_codes, "LOCAL_NOOP_RUNNER_READINESS_ID_MISSING")
        _add_field(
            field_entries,
            reason_code="LOCAL_NOOP_RUNNER_READINESS_ID_MISSING",
            field=f"{prefix}.local_noop_runner_readiness_id",
        )

    if value.get("local_noop_runner_readiness_buildable_marker") is not True:
        _add_reason(
            reason_codes,
            "LOCAL_NOOP_RUNNER_READINESS_BUILDABLE_MARKER_NOT_TRUE",
        )
        _add_field(
            field_entries,
            reason_code=(
                "LOCAL_NOOP_RUNNER_READINESS_BUILDABLE_MARKER_NOT_TRUE"
            ),
            field=f"{prefix}.local_noop_runner_readiness_buildable_marker",
        )

    if value.get("public_url") is not None:
        _add_reason(reason_codes, "PUBLIC_URL_NOT_NULL")
        _add_field(
            field_entries,
            reason_code="PUBLIC_URL_NOT_NULL",
            field=f"{prefix}.public_url",
        )

    if value.get("public_url_created") is not False:
        _add_reason(reason_codes, "PUBLIC_URL_CREATED_NOT_FALSE")
        _add_field(
            field_entries,
            reason_code="PUBLIC_URL_CREATED_NOT_FALSE",
            field=f"{prefix}.public_url_created",
        )

    if not _is_nonempty_string_tuple(value.get("source_of_truth")):
        _add_reason(reason_codes, "SOURCE_OF_TRUTH_MISSING")
        _add_field(
            field_entries,
            reason_code="SOURCE_OF_TRUTH_MISSING",
            field=f"{prefix}.source_of_truth",
        )


def _blocked_source() -> dict[str, object]:
    return {
        "p2d41_assembled": False,
        "p2d41_reason_code": "",
        "local_noop_runner_result_candidate_id": "",
        "candidate_kind": "",
        "mode": "",
        "public_url": None,
        "public_url_created": False,
        "source_of_truth": (),
    }


def _successful_source(candidate: dict[str, object]) -> dict[str, object]:
    source_of_truth = candidate["source_of_truth"]
    return {
        "p2d41_assembled": True,
        "p2d41_reason_code": _P2D41_SUCCESS_REASON,
        "local_noop_runner_result_candidate_id": candidate[
            "local_noop_runner_result_candidate_id"
        ],
        "candidate_kind": _CANDIDATE_KIND,
        "mode": _NOOP_MODE,
        "public_url": None,
        "public_url_created": False,
        "source_of_truth": _copy_string_tuple(source_of_truth),
    }


def _normalized_evidence_item(
    evidence_item: dict[str, object],
) -> dict[str, object]:
    evidence_refs = evidence_item["evidence_refs"]
    notes = evidence_item["notes"]
    return {
        "result_candidate_evidence_id": evidence_item[
            "result_candidate_evidence_id"
        ],
        "result_candidate_evidence_role": evidence_item[
            "result_candidate_evidence_role"
        ],
        "artifact_ref": evidence_item["artifact_ref"],
        "artifact_kind": evidence_item["artifact_kind"],
        "evidence_status": evidence_item["evidence_status"],
        "producer_ref": evidence_item["producer_ref"],
        "evidence_refs": _copy_string_tuple(evidence_refs),
        "notes": _copy_string_tuple(notes),
    }


def _normalized_candidate(candidate: dict[str, object]) -> dict[str, object]:
    evidence_items = candidate["result_candidate_evidence_items"]
    normalized_evidence_items = tuple(
        _normalized_evidence_item(evidence_item)
        for evidence_item in evidence_items
    )
    return {
        "run_id": candidate["run_id"],
        "local_noop_runner_result_candidate_id": candidate[
            "local_noop_runner_result_candidate_id"
        ],
        "candidate_kind": _CANDIDATE_KIND,
        "mode": _NOOP_MODE,
        "runner_terminal_status": _NOOP_COMPLETED,
        "local_noop_runner_readiness_ref": candidate[
            "local_noop_runner_readiness_ref"
        ],
        "local_noop_runner_readiness_id": candidate[
            "local_noop_runner_readiness_id"
        ],
        "local_noop_runner_readiness_buildable_marker": True,
        "public_url": None,
        "public_url_created": False,
        "result_candidate_evidence_items": normalized_evidence_items,
        "required_result_candidate_evidence_ids": _copy_string_tuple(
            candidate["required_result_candidate_evidence_ids"]
        ),
        "missing_result_candidate_evidence_ids": (),
        "blocking_result_candidate_evidence_ids": _copy_string_tuple(
            candidate["blocking_result_candidate_evidence_ids"]
        ),
        "created_at": candidate["created_at"],
        "timestamp_policy": candidate["timestamp_policy"],
        "source_of_truth": _copy_string_tuple(candidate["source_of_truth"]),
        "notes": _copy_string_tuple(candidate["notes"]),
    }


def _consumption_receipt(candidate: dict[str, object]) -> dict[str, object]:
    return {
        "receipt_kind": (
            "local_noop_runner_result_candidate_consumption_receipt"
        ),
        "consumption_scope": (
            "pure_in_memory_validation_and_normalization_only"
        ),
        "run_id": candidate["run_id"],
        "local_noop_runner_result_candidate_id": candidate[
            "local_noop_runner_result_candidate_id"
        ],
        "candidate_kind": _CANDIDATE_KIND,
        "mode": _NOOP_MODE,
        "public_url": None,
        "public_url_created": False,
    }


def consume_local_noop_runner_result_candidate(
    *,
    local_noop_runner_result_candidate_assembly: dict[str, object],
) -> dict[str, object]:
    """Validate and normalize one complete P2D-41 assembly in memory."""

    reason_codes = []
    field_entries = []
    evidence_violations = []

    scan_path = ()
    if (
        isinstance(local_noop_runner_result_candidate_assembly, dict)
        and _has_exact_keys(
            local_noop_runner_result_candidate_assembly,
            _CANDIDATE_KEYS,
        )
    ):
        scan_path = ("local_noop_runner_result_candidate",)

    _scan_forbidden_keys(
        local_noop_runner_result_candidate_assembly,
        path=scan_path,
        reason_codes=reason_codes,
        field_entries=field_entries,
    )

    if not isinstance(local_noop_runner_result_candidate_assembly, dict):
        _add_reason(reason_codes, "CANDIDATE_ASSEMBLY_NOT_DICT")
        _add_field(
            field_entries,
            reason_code="CANDIDATE_ASSEMBLY_NOT_DICT",
            field="<root>",
        )
        assembly = {}
    else:
        assembly = local_noop_runner_result_candidate_assembly
        if not _has_exact_keys(assembly, _ROOT_KEYS):
            _add_reason(reason_codes, "CANDIDATE_ASSEMBLY_KEYS_INVALID")
            _add_field(
                field_entries,
                reason_code="CANDIDATE_ASSEMBLY_KEYS_INVALID",
                field="candidate_assembly.keys",
            )

        if assembly.get("assembled") is not True:
            _add_reason(reason_codes, "P2D41_ASSEMBLED_MARKER_NOT_TRUE")
            _add_field(
                field_entries,
                reason_code="P2D41_ASSEMBLED_MARKER_NOT_TRUE",
                field="assembled",
            )

        if assembly.get("reason_code") != _P2D41_SUCCESS_REASON:
            _add_reason(reason_codes, "P2D41_ASSEMBLY_REASON_CODE_INVALID")
            _add_field(
                field_entries,
                reason_code="P2D41_ASSEMBLY_REASON_CODE_INVALID",
                field="reason_code",
            )

        if not _is_nonblank_string(assembly.get("reason")):
            _add_reason(reason_codes, "P2D41_ASSEMBLY_REASON_MISSING")
            _add_field(
                field_entries,
                reason_code="P2D41_ASSEMBLY_REASON_MISSING",
                field="reason",
            )

        if assembly.get("assembly_violations") != ():
            _add_reason(reason_codes, "P2D41_ASSEMBLY_VIOLATIONS_NOT_EMPTY")
            _add_field(
                field_entries,
                reason_code="P2D41_ASSEMBLY_VIOLATIONS_NOT_EMPTY",
                field="assembly_violations",
            )

        if assembly.get("missing_or_invalid_fields") != ():
            _add_reason(
                reason_codes,
                "P2D41_MISSING_OR_INVALID_FIELDS_NOT_EMPTY",
            )
            _add_field(
                field_entries,
                reason_code="P2D41_MISSING_OR_INVALID_FIELDS_NOT_EMPTY",
                field="missing_or_invalid_fields",
            )

        if assembly.get("result_candidate_evidence_item_violations") != ():
            _add_reason(
                reason_codes,
                "P2D41_EVIDENCE_ITEM_VIOLATIONS_NOT_EMPTY",
            )
            _add_field(
                field_entries,
                reason_code="P2D41_EVIDENCE_ITEM_VIOLATIONS_NOT_EMPTY",
                field="result_candidate_evidence_item_violations",
            )

        invariant_refs = assembly.get("invariant_refs")
        if not _is_nonempty_string_tuple(invariant_refs):
            _add_reason(reason_codes, "P2D41_INVARIANT_REFS_INVALID")
            _add_field(
                field_entries,
                reason_code="P2D41_INVARIANT_REFS_INVALID",
                field="invariant_refs",
            )
        safe_invariant_refs = _safe_string_tuple(invariant_refs)
        for required_invariant_ref in _REQUIRED_P2D41_INVARIANT_REFS:
            if required_invariant_ref not in safe_invariant_refs:
                _add_reason(
                    reason_codes,
                    "P2D41_REQUIRED_INVARIANT_REF_MISSING",
                )
                _add_field(
                    field_entries,
                    reason_code="P2D41_REQUIRED_INVARIANT_REF_MISSING",
                    field=f"invariant_refs.{required_invariant_ref}",
                )

    source_value = assembly.get("source") if isinstance(assembly, dict) else None
    if not isinstance(source_value, dict):
        _add_reason(reason_codes, "P2D41_SOURCE_NOT_DICT")
        _add_field(
            field_entries,
            reason_code="P2D41_SOURCE_NOT_DICT",
            field="source",
        )
        source = {}
    else:
        source = source_value
        if not _has_exact_keys(source, _SOURCE_KEYS):
            _add_reason(reason_codes, "P2D41_SOURCE_KEYS_INVALID")
            _add_field(
                field_entries,
                reason_code="P2D41_SOURCE_KEYS_INVALID",
                field="candidate_assembly.source.keys",
            )
        _validate_noop_fields(
            source,
            prefix="source",
            reason_codes=reason_codes,
            field_entries=field_entries,
        )

    candidate_value = (
        assembly.get("local_noop_runner_result_candidate")
        if isinstance(assembly, dict)
        else None
    )
    if not isinstance(candidate_value, dict):
        _add_reason(reason_codes, "P2D41_RESULT_CANDIDATE_NOT_DICT")
        _add_field(
            field_entries,
            reason_code="P2D41_RESULT_CANDIDATE_NOT_DICT",
            field="local_noop_runner_result_candidate",
        )
        candidate = {}
    else:
        candidate = candidate_value
        if not _has_exact_keys(candidate, _CANDIDATE_KEYS):
            _add_reason(reason_codes, "P2D41_RESULT_CANDIDATE_KEYS_INVALID")
            _add_field(
                field_entries,
                reason_code="P2D41_RESULT_CANDIDATE_KEYS_INVALID",
                field=(
                    "candidate_assembly."
                    "local_noop_runner_result_candidate.keys"
                ),
            )

        if not _is_nonblank_string(candidate.get("run_id")):
            _add_reason(reason_codes, "RUN_ID_MISSING")
            _add_field(
                field_entries,
                reason_code="RUN_ID_MISSING",
                field="local_noop_runner_result_candidate.run_id",
            )

        if not _is_nonblank_string(
            candidate.get("local_noop_runner_result_candidate_id")
        ):
            _add_reason(
                reason_codes,
                "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_ID_MISSING",
            )
            _add_field(
                field_entries,
                reason_code="LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_ID_MISSING",
                field=(
                    "local_noop_runner_result_candidate."
                    "local_noop_runner_result_candidate_id"
                ),
            )

        if candidate.get("candidate_kind") != _CANDIDATE_KIND:
            _add_reason(
                reason_codes,
                "CANDIDATE_KIND_NOT_LOCAL_NOOP_RUNNER_RESULT_CANDIDATE",
            )
            _add_field(
                field_entries,
                reason_code=(
                    "CANDIDATE_KIND_NOT_LOCAL_NOOP_RUNNER_RESULT_CANDIDATE"
                ),
                field="local_noop_runner_result_candidate.candidate_kind",
            )

        _validate_noop_fields(
            candidate,
            prefix="local_noop_runner_result_candidate",
            reason_codes=reason_codes,
            field_entries=field_entries,
        )

        if not _is_nonblank_string(candidate.get("created_at")):
            _add_reason(reason_codes, "CREATED_AT_MISSING")
            _add_field(
                field_entries,
                reason_code="CREATED_AT_MISSING",
                field="local_noop_runner_result_candidate.created_at",
            )

        if not _is_nonblank_string(candidate.get("timestamp_policy")):
            _add_reason(reason_codes, "TIMESTAMP_POLICY_MISSING")
            _add_field(
                field_entries,
                reason_code="TIMESTAMP_POLICY_MISSING",
                field="local_noop_runner_result_candidate.timestamp_policy",
            )

        if not _is_string_tuple(candidate.get("notes")):
            _add_reason(reason_codes, "NOTES_INVALID")
            _add_field(
                field_entries,
                reason_code="NOTES_INVALID",
                field="local_noop_runner_result_candidate.notes",
            )

    if isinstance(source_value, dict) and isinstance(candidate_value, dict):
        for field in _COHERENCE_FIELDS:
            if not _values_match_exactly(
                source.get(field),
                candidate.get(field),
            ):
                _add_reason(reason_codes, "P2D41_SOURCE_CANDIDATE_MISMATCH")
                _add_field(
                    field_entries,
                    reason_code="P2D41_SOURCE_CANDIDATE_MISMATCH",
                    field=f"source.{field}",
                )

    evidence_items = candidate.get("result_candidate_evidence_items")
    if not isinstance(evidence_items, tuple) or evidence_items == ():
        _add_reason(reason_codes, "RESULT_CANDIDATE_EVIDENCE_ITEMS_MISSING")
        _add_field(
            field_entries,
            reason_code="RESULT_CANDIDATE_EVIDENCE_ITEMS_MISSING",
            field=(
                "local_noop_runner_result_candidate."
                "result_candidate_evidence_items"
            ),
        )
        safe_evidence_items = ()
    else:
        safe_evidence_items = evidence_items

    required_ids_value = candidate.get("required_result_candidate_evidence_ids")
    if not _is_nonempty_string_tuple(required_ids_value):
        _add_reason(
            reason_codes,
            "REQUIRED_RESULT_CANDIDATE_EVIDENCE_IDS_MISSING",
        )
        _add_field(
            field_entries,
            reason_code="REQUIRED_RESULT_CANDIDATE_EVIDENCE_IDS_MISSING",
            field=(
                "local_noop_runner_result_candidate."
                "required_result_candidate_evidence_ids"
            ),
        )
    required_ids = _safe_string_tuple(required_ids_value)

    if candidate.get("missing_result_candidate_evidence_ids") != ():
        _add_reason(
            reason_codes,
            "MISSING_RESULT_CANDIDATE_EVIDENCE_IDS_DECLARED",
        )
        _add_field(
            field_entries,
            reason_code="MISSING_RESULT_CANDIDATE_EVIDENCE_IDS_DECLARED",
            field=(
                "local_noop_runner_result_candidate."
                "missing_result_candidate_evidence_ids"
            ),
        )

    known_ids = ()
    seen_ids = ()
    for index, evidence_item in enumerate(safe_evidence_items):
        item_prefix = (
            "local_noop_runner_result_candidate."
            f"result_candidate_evidence_items[{index}]"
        )
        if not isinstance(evidence_item, dict):
            _add_reason(reason_codes, "RESULT_CANDIDATE_EVIDENCE_ITEM_NOT_DICT")
            _add_field(
                field_entries,
                reason_code="RESULT_CANDIDATE_EVIDENCE_ITEM_NOT_DICT",
                field=item_prefix,
            )
            _add_evidence_violation(
                evidence_violations,
                index=index,
                evidence_id="",
                reason_code="RESULT_CANDIDATE_EVIDENCE_ITEM_NOT_DICT",
                field=item_prefix,
            )
            continue

        evidence_id = evidence_item.get("result_candidate_evidence_id")
        if not _has_exact_keys(evidence_item, _EVIDENCE_ITEM_KEYS):
            _add_reason(
                reason_codes,
                "RESULT_CANDIDATE_EVIDENCE_ITEM_KEYS_INVALID",
            )
            _add_field(
                field_entries,
                reason_code="RESULT_CANDIDATE_EVIDENCE_ITEM_KEYS_INVALID",
                field=f"candidate_assembly.{item_prefix}.keys",
            )
            _add_evidence_violation(
                evidence_violations,
                index=index,
                evidence_id=evidence_id,
                reason_code="RESULT_CANDIDATE_EVIDENCE_ITEM_KEYS_INVALID",
                field=item_prefix,
            )

        for field, missing_reason in _EVIDENCE_STRING_FIELDS:
            if not _is_nonblank_string(evidence_item.get(field)):
                field_path = f"{item_prefix}.{field}"
                _add_reason(reason_codes, missing_reason)
                _add_field(
                    field_entries,
                    reason_code=missing_reason,
                    field=field_path,
                )
                _add_evidence_violation(
                    evidence_violations,
                    index=index,
                    evidence_id=evidence_id,
                    reason_code=missing_reason,
                    field=field_path,
                )

        if evidence_item.get("evidence_status") == _PASS_PUBLISHED:
            field_path = f"{item_prefix}.evidence_status"
            _add_reason(reason_codes, "PASS_PUBLISHED_FORBIDDEN")
            _add_field(
                field_entries,
                reason_code="PASS_PUBLISHED_FORBIDDEN",
                field=field_path,
            )
            _add_evidence_violation(
                evidence_violations,
                index=index,
                evidence_id=evidence_id,
                reason_code="PASS_PUBLISHED_FORBIDDEN",
                field=field_path,
            )

        if not _is_nonempty_string_tuple(evidence_item.get("evidence_refs")):
            field_path = f"{item_prefix}.evidence_refs"
            _add_reason(
                reason_codes,
                "RESULT_CANDIDATE_EVIDENCE_REFS_MISSING",
            )
            _add_field(
                field_entries,
                reason_code="RESULT_CANDIDATE_EVIDENCE_REFS_MISSING",
                field=field_path,
            )
            _add_evidence_violation(
                evidence_violations,
                index=index,
                evidence_id=evidence_id,
                reason_code="RESULT_CANDIDATE_EVIDENCE_REFS_MISSING",
                field=field_path,
            )

        if not _is_string_tuple(evidence_item.get("notes")):
            field_path = f"{item_prefix}.notes"
            _add_reason(
                reason_codes,
                "RESULT_CANDIDATE_EVIDENCE_NOTES_INVALID",
            )
            _add_field(
                field_entries,
                reason_code="RESULT_CANDIDATE_EVIDENCE_NOTES_INVALID",
                field=field_path,
            )
            _add_evidence_violation(
                evidence_violations,
                index=index,
                evidence_id=evidence_id,
                reason_code="RESULT_CANDIDATE_EVIDENCE_NOTES_INVALID",
                field=field_path,
            )

        if _is_nonblank_string(evidence_id):
            known_ids = known_ids + (evidence_id,)
            if evidence_id in seen_ids:
                field_path = f"{item_prefix}.result_candidate_evidence_id"
                _add_reason(
                    reason_codes,
                    "RESULT_CANDIDATE_EVIDENCE_ID_DUPLICATE",
                )
                _add_field(
                    field_entries,
                    reason_code="RESULT_CANDIDATE_EVIDENCE_ID_DUPLICATE",
                    field=field_path,
                )
                _add_evidence_violation(
                    evidence_violations,
                    index=index,
                    evidence_id=evidence_id,
                    reason_code="RESULT_CANDIDATE_EVIDENCE_ID_DUPLICATE",
                    field=field_path,
                )
            else:
                seen_ids = seen_ids + (evidence_id,)

            if evidence_id not in required_ids:
                field_path = f"{item_prefix}.result_candidate_evidence_id"
                _add_reason(
                    reason_codes,
                    "RESULT_CANDIDATE_EVIDENCE_ID_NOT_REQUIRED",
                )
                _add_field(
                    field_entries,
                    reason_code="RESULT_CANDIDATE_EVIDENCE_ID_NOT_REQUIRED",
                    field=field_path,
                )
                _add_evidence_violation(
                    evidence_violations,
                    index=index,
                    evidence_id=evidence_id,
                    reason_code="RESULT_CANDIDATE_EVIDENCE_ID_NOT_REQUIRED",
                    field=field_path,
                )

    for required_id in required_ids:
        if _is_nonblank_string(required_id) and required_id not in known_ids:
            _add_reason(
                reason_codes,
                "REQUIRED_RESULT_CANDIDATE_EVIDENCE_MISSING",
            )
            _add_field(
                field_entries,
                reason_code="REQUIRED_RESULT_CANDIDATE_EVIDENCE_MISSING",
                field=(
                    "local_noop_runner_result_candidate."
                    "required_result_candidate_evidence_ids."
                    f"{required_id}"
                ),
            )

    blocking_ids = candidate.get("blocking_result_candidate_evidence_ids")
    blocking_ids_valid = isinstance(blocking_ids, tuple)
    if blocking_ids_valid:
        for blocking_id in blocking_ids:
            if (
                not _is_nonblank_string(blocking_id)
                or blocking_id not in known_ids
            ):
                blocking_ids_valid = False
                break
    if not blocking_ids_valid:
        _add_reason(
            reason_codes,
            "BLOCKING_RESULT_CANDIDATE_EVIDENCE_ID_UNKNOWN",
        )
        _add_field(
            field_entries,
            reason_code="BLOCKING_RESULT_CANDIDATE_EVIDENCE_ID_UNKNOWN",
            field=(
                "local_noop_runner_result_candidate."
                "blocking_result_candidate_evidence_ids"
            ),
        )

    consumption_violations = _ordered_reason_codes(tuple(reason_codes))
    consumed = consumption_violations == ()
    reason_code = _SUCCESS_REASON if consumed else consumption_violations[0]

    if consumed:
        source_output = _successful_source(candidate)
        normalized_candidate = _normalized_candidate(candidate)
        receipt = _consumption_receipt(candidate)
    else:
        source_output = _blocked_source()
        normalized_candidate = {}
        receipt = {}

    return {
        "consumed": consumed,
        "reason_code": reason_code,
        "reason": _reason_text(reason_code),
        "source": source_output,
        "normalized_local_noop_runner_result_candidate": normalized_candidate,
        "local_noop_runner_consumption_receipt": receipt,
        "consumption_violations": consumption_violations,
        "missing_or_invalid_fields": _ordered_fields(tuple(field_entries)),
        "result_candidate_evidence_item_violations": (
            _ordered_evidence_violations(tuple(evidence_violations))
        ),
        "invariant_refs": _INVARIANT_REFS,
    }


def is_local_noop_runner_result_candidate_consumed(
    *,
    local_noop_runner_result_candidate_assembly: dict[str, object],
) -> bool:
    """Return whether the complete P2D-41 assembly was consumed in memory."""

    return consume_local_noop_runner_result_candidate(
        local_noop_runner_result_candidate_assembly=(
            local_noop_runner_result_candidate_assembly
        ),
    )["consumed"]
