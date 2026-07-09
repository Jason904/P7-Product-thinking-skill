"""Build pure local noop runner readiness buildability explanations."""

from typing import Final


REASON_CODES: Final[tuple[str, ...]] = (
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

LOCAL_NOOP_RUNNER_READINESS_BUILD_REASON_CODES: Final[tuple[str, ...]] = (
    REASON_CODES
)

REASON_PRIORITY: Final[tuple[str, ...]] = (
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

_READINESS_KIND: Final[str] = "local_noop_runner_readiness"
_NOOP_MODE: Final[str] = "noop"
_NOOP_COMPLETED: Final[str] = "NOOP_COMPLETED"
_PASS_PUBLISHED: Final[str] = "PASS_PUBLISHED"

_READINESS_EVIDENCE_ITEM_KEYS: Final[tuple[str, ...]] = (
    "readiness_evidence_id",
    "readiness_evidence_role",
    "artifact_ref",
    "artifact_kind",
    "evidence_status",
    "producer_ref",
    "evidence_refs",
    "notes",
)

_READINESS_EVIDENCE_ITEM_STRING_FIELDS: Final[tuple[tuple[str, str], ...]] = (
    ("readiness_evidence_id", "READINESS_EVIDENCE_ID_MISSING"),
    ("readiness_evidence_role", "READINESS_EVIDENCE_ROLE_MISSING"),
    ("artifact_ref", "READINESS_EVIDENCE_ARTIFACT_REF_MISSING"),
    ("artifact_kind", "READINESS_EVIDENCE_ARTIFACT_KIND_MISSING"),
    ("evidence_status", "READINESS_EVIDENCE_STATUS_MISSING"),
    ("producer_ref", "READINESS_EVIDENCE_PRODUCER_REF_MISSING"),
)

_FORBIDDEN_READINESS_EVIDENCE_ITEM_FIELDS: Final[tuple[str, ...]] = (
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

_INVARIANT_REFS: Final[tuple[str, ...]] = (
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

_REASON_TEXT_ENTRIES: Final[tuple[tuple[str, str], ...]] = (
    ("RUN_ID_MISSING", "A non-empty caller-supplied run_id is required."),
    (
        "LOCAL_NOOP_RUNNER_READINESS_ID_MISSING",
        "A non-empty caller-supplied local_noop_runner_readiness_id is required.",
    ),
    (
        "READINESS_KIND_NOT_LOCAL_NOOP_RUNNER_READINESS",
        "readiness_kind must be local_noop_runner_readiness.",
    ),
    ("MODE_NOT_NOOP", "mode must be noop."),
    (
        "PASS_PUBLISHED_FORBIDDEN",
        "PASS_PUBLISHED is forbidden for local noop runner readiness.",
    ),
    (
        "EXPECTED_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
        "expected_terminal_status must be NOOP_COMPLETED.",
    ),
    (
        "LOCAL_NOOP_RUNNER_ENVELOPE_REF_MISSING",
        "A caller-supplied local noop runner envelope ref is required.",
    ),
    (
        "LOCAL_NOOP_RUNNER_ENVELOPE_BUILDABLE_MARKER_NOT_TRUE",
        "The caller-supplied envelope buildable marker must be true.",
    ),
    (
        "PUBLIC_URL_IS_NULL_NOT_TRUE",
        "The caller-supplied public URL null marker must be true.",
    ),
    ("PUBLIC_URL_CREATED_NOT_FALSE", "public_url_created must remain false."),
    (
        "READINESS_EVIDENCE_ITEMS_MISSING",
        "At least one readiness evidence item is required.",
    ),
    (
        "REQUIRED_READINESS_EVIDENCE_IDS_MISSING",
        "At least one required readiness evidence id is required.",
    ),
    (
        "MISSING_READINESS_EVIDENCE_IDS_DECLARED",
        "missing_readiness_evidence_ids must be an empty tuple.",
    ),
    (
        "BLOCKING_READINESS_EVIDENCE_ID_UNKNOWN",
        "Blocking readiness evidence ids must be known non-empty ids.",
    ),
    ("CREATED_AT_MISSING", "A caller-supplied created_at value is required."),
    (
        "TIMESTAMP_POLICY_MISSING",
        "A caller-supplied timestamp_policy value is required.",
    ),
    (
        "SOURCE_OF_TRUTH_MISSING",
        "At least one caller-supplied source_of_truth reference is required.",
    ),
    (
        "READINESS_EVIDENCE_ITEM_NOT_DICT",
        "Every readiness evidence item must be a dict.",
    ),
    (
        "READINESS_EVIDENCE_ITEM_KEYS_INVALID",
        "Every readiness evidence item must contain exact expected keys.",
    ),
    (
        "READINESS_EVIDENCE_ID_MISSING",
        "Every readiness evidence item requires a non-empty id.",
    ),
    (
        "READINESS_EVIDENCE_ROLE_MISSING",
        "Every readiness evidence item requires a non-empty role.",
    ),
    (
        "READINESS_EVIDENCE_ARTIFACT_REF_MISSING",
        "Every readiness evidence item requires a non-empty artifact_ref.",
    ),
    (
        "READINESS_EVIDENCE_ARTIFACT_KIND_MISSING",
        "Every readiness evidence item requires a non-empty artifact_kind.",
    ),
    (
        "READINESS_EVIDENCE_STATUS_MISSING",
        "Every readiness evidence item requires a non-empty status.",
    ),
    (
        "READINESS_EVIDENCE_PRODUCER_REF_MISSING",
        "Every readiness evidence item requires a non-empty producer_ref.",
    ),
    (
        "READINESS_EVIDENCE_REFS_MISSING",
        "Every readiness evidence item requires non-empty evidence_refs.",
    ),
    (
        "READINESS_EVIDENCE_ID_DUPLICATE",
        "readiness_evidence_id values must be unique.",
    ),
    (
        "READINESS_EVIDENCE_ID_NOT_REQUIRED",
        "Every readiness_evidence_id must be declared as required.",
    ),
    (
        "REQUIRED_READINESS_EVIDENCE_MISSING",
        "Every required readiness evidence id must have one evidence item.",
    ),
    (
        "READINESS_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT",
        "Readiness evidence items must not contain raw, ready, execution, URL, "
        "IO, publish, ledger, notification, CLI, command, subprocess, policy, "
        "previous builder, or P2D-39 envelope payload fields.",
    ),
    (
        "LOCAL_NOOP_RUNNER_READINESS_BUILDABLE",
        "The caller-supplied fields can build the local noop runner readiness "
        "shape. This does not execute a runner, runtime, CLI, manual command, "
        "subprocess, dry-run, E2E, noop completion, transition, gate, policy, "
        "validator, eval, audit, publish, ledger write, notification, artifact "
        "read, previous builder call, run-ledger.yaml behavior, or public URL "
        "behavior.",
    ),
)


def _is_nonblank_string(value: object) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _is_nonempty_string_tuple(value: object) -> bool:
    if not isinstance(value, tuple) or value == ():
        return False
    for item in value:
        if not _is_nonblank_string(item):
            return False
    return True


def _safe_string(value: object) -> str:
    if isinstance(value, str):
        return value
    return ""


def _safe_expected_terminal_status(value: object) -> str:
    if value == _PASS_PUBLISHED:
        return ""
    return _safe_string(value)


def _safe_string_tuple(value: object) -> tuple[str, ...]:
    if not isinstance(value, tuple):
        return ()

    safe_values = ()
    for item in value:
        if isinstance(item, str):
            safe_values = safe_values + (item,)
    return safe_values


def _safe_readiness_evidence_item(
    readiness_evidence_item: object,
) -> dict[str, object]:
    if not isinstance(readiness_evidence_item, dict):
        return {
            "readiness_evidence_id": "",
            "readiness_evidence_role": "",
            "artifact_ref": "",
            "artifact_kind": "",
            "evidence_status": "",
            "producer_ref": "",
            "evidence_refs": (),
            "notes": (),
        }

    return {
        "readiness_evidence_id": _safe_string(
            readiness_evidence_item.get("readiness_evidence_id")
        ),
        "readiness_evidence_role": _safe_string(
            readiness_evidence_item.get("readiness_evidence_role")
        ),
        "artifact_ref": _safe_string(readiness_evidence_item.get("artifact_ref")),
        "artifact_kind": _safe_string(
            readiness_evidence_item.get("artifact_kind")
        ),
        "evidence_status": _safe_string(
            readiness_evidence_item.get("evidence_status")
        ),
        "producer_ref": _safe_string(
            readiness_evidence_item.get("producer_ref")
        ),
        "evidence_refs": _safe_string_tuple(
            readiness_evidence_item.get("evidence_refs")
        ),
        "notes": _safe_string_tuple(readiness_evidence_item.get("notes")),
    }


def _safe_readiness_evidence_items(
    value: object,
) -> tuple[dict[str, object], ...]:
    if not isinstance(value, tuple):
        return ()

    safe_items = ()
    for readiness_evidence_item in value:
        safe_items = safe_items + (
            _safe_readiness_evidence_item(readiness_evidence_item),
        )
    return safe_items


def _reason_text(reason_code: str) -> str:
    for code, text in _REASON_TEXT_ENTRIES:
        if code == reason_code:
            return text
    return "Unknown local noop runner readiness build result."


def _add_reason(reason_codes: list[str], reason_code: str) -> None:
    reason_codes.append(reason_code)


def _add_field(
    fields: list[tuple[str, str]],
    *,
    reason_code: str,
    field: str,
) -> None:
    fields.append((reason_code, field))


def _add_readiness_evidence_item_violation(
    readiness_evidence_item_violations: list[dict[str, object]],
    *,
    readiness_evidence_item_index: int,
    readiness_evidence_id: str,
    reason_code: str,
    field: str,
) -> None:
    readiness_evidence_item_violations.append(
        {
            "readiness_evidence_item_index": readiness_evidence_item_index,
            "readiness_evidence_id": readiness_evidence_id,
            "reason_code": reason_code,
            "field": field,
        }
    )


def _ordered_reason_codes(reason_codes: tuple[str, ...]) -> tuple[str, ...]:
    ordered = ()
    for reason_code in REASON_PRIORITY:
        if reason_code in reason_codes and reason_code not in ordered:
            ordered = ordered + (reason_code,)
    return ordered


def _ordered_fields(fields: tuple[tuple[str, str], ...]) -> tuple[str, ...]:
    ordered = ()
    for reason_code in REASON_PRIORITY:
        for entry_reason_code, field in fields:
            if entry_reason_code == reason_code:
                ordered = ordered + (field,)
    return ordered


def _ordered_readiness_evidence_item_violations(
    readiness_evidence_item_violations: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    ordered = ()
    for reason_code in REASON_PRIORITY:
        for violation in readiness_evidence_item_violations:
            if violation["reason_code"] == reason_code:
                ordered = ordered + (violation,)
    return ordered


def _has_exact_readiness_evidence_item_keys(
    readiness_evidence_item: dict[str, object],
) -> bool:
    if len(readiness_evidence_item) != len(_READINESS_EVIDENCE_ITEM_KEYS):
        return False
    for key in _READINESS_EVIDENCE_ITEM_KEYS:
        if key not in readiness_evidence_item:
            return False
    return True


def _readiness_evidence_id_from(readiness_evidence_item: object) -> str:
    if not isinstance(readiness_evidence_item, dict):
        return ""
    return _safe_string(readiness_evidence_item.get("readiness_evidence_id"))


def _known_readiness_evidence_ids(
    readiness_evidence_items: object,
) -> tuple[str, ...]:
    if not isinstance(readiness_evidence_items, tuple):
        return ()

    known_ids = ()
    for readiness_evidence_item in readiness_evidence_items:
        readiness_evidence_id = _readiness_evidence_id_from(
            readiness_evidence_item
        )
        if _is_nonblank_string(readiness_evidence_id):
            known_ids = known_ids + (readiness_evidence_id,)
    return known_ids


def explain_local_noop_runner_readiness_build(
    *,
    run_id: str,
    local_noop_runner_readiness_id: str,
    readiness_kind: str,
    mode: str,
    expected_terminal_status: str,
    local_noop_runner_envelope_ref: str,
    local_noop_runner_envelope_buildable_marker: bool,
    public_url_created: bool,
    public_url_is_null: bool,
    readiness_evidence_items: tuple[dict[str, object], ...],
    required_readiness_evidence_ids: tuple[str, ...],
    missing_readiness_evidence_ids: tuple[str, ...],
    blocking_readiness_evidence_ids: tuple[str, ...],
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    """Explain whether a caller-supplied runner readiness shape is buildable."""

    reason_codes = []
    field_entries = []
    readiness_evidence_item_violations = []

    if not _is_nonblank_string(run_id):
        _add_reason(reason_codes, "RUN_ID_MISSING")
        _add_field(field_entries, reason_code="RUN_ID_MISSING", field="run_id")

    if not _is_nonblank_string(local_noop_runner_readiness_id):
        _add_reason(reason_codes, "LOCAL_NOOP_RUNNER_READINESS_ID_MISSING")
        _add_field(
            field_entries,
            reason_code="LOCAL_NOOP_RUNNER_READINESS_ID_MISSING",
            field="local_noop_runner_readiness_id",
        )

    if readiness_kind != _READINESS_KIND:
        _add_reason(
            reason_codes,
            "READINESS_KIND_NOT_LOCAL_NOOP_RUNNER_READINESS",
        )
        _add_field(
            field_entries,
            reason_code="READINESS_KIND_NOT_LOCAL_NOOP_RUNNER_READINESS",
            field="readiness_kind",
        )

    if mode != _NOOP_MODE:
        _add_reason(reason_codes, "MODE_NOT_NOOP")
        _add_field(field_entries, reason_code="MODE_NOT_NOOP", field="mode")

    if expected_terminal_status == _PASS_PUBLISHED:
        _add_reason(reason_codes, "PASS_PUBLISHED_FORBIDDEN")
        _add_field(
            field_entries,
            reason_code="PASS_PUBLISHED_FORBIDDEN",
            field="expected_terminal_status",
        )

    if expected_terminal_status != _NOOP_COMPLETED:
        _add_reason(reason_codes, "EXPECTED_TERMINAL_STATUS_NOT_NOOP_COMPLETED")
        _add_field(
            field_entries,
            reason_code="EXPECTED_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
            field="expected_terminal_status",
        )

    if not _is_nonblank_string(local_noop_runner_envelope_ref):
        _add_reason(reason_codes, "LOCAL_NOOP_RUNNER_ENVELOPE_REF_MISSING")
        _add_field(
            field_entries,
            reason_code="LOCAL_NOOP_RUNNER_ENVELOPE_REF_MISSING",
            field="local_noop_runner_envelope_ref",
        )

    if local_noop_runner_envelope_buildable_marker is not True:
        _add_reason(
            reason_codes,
            "LOCAL_NOOP_RUNNER_ENVELOPE_BUILDABLE_MARKER_NOT_TRUE",
        )
        _add_field(
            field_entries,
            reason_code="LOCAL_NOOP_RUNNER_ENVELOPE_BUILDABLE_MARKER_NOT_TRUE",
            field="local_noop_runner_envelope_buildable_marker",
        )

    if public_url_is_null is not True:
        _add_reason(reason_codes, "PUBLIC_URL_IS_NULL_NOT_TRUE")
        _add_field(
            field_entries,
            reason_code="PUBLIC_URL_IS_NULL_NOT_TRUE",
            field="public_url",
        )

    if public_url_created is not False:
        _add_reason(reason_codes, "PUBLIC_URL_CREATED_NOT_FALSE")
        _add_field(
            field_entries,
            reason_code="PUBLIC_URL_CREATED_NOT_FALSE",
            field="public_url_created",
        )

    if (
        not isinstance(readiness_evidence_items, tuple)
        or readiness_evidence_items == ()
    ):
        _add_reason(reason_codes, "READINESS_EVIDENCE_ITEMS_MISSING")
        _add_field(
            field_entries,
            reason_code="READINESS_EVIDENCE_ITEMS_MISSING",
            field="readiness_evidence_items",
        )

    if not _is_nonempty_string_tuple(required_readiness_evidence_ids):
        _add_reason(reason_codes, "REQUIRED_READINESS_EVIDENCE_IDS_MISSING")
        _add_field(
            field_entries,
            reason_code="REQUIRED_READINESS_EVIDENCE_IDS_MISSING",
            field="required_readiness_evidence_ids",
        )

    if (
        not isinstance(missing_readiness_evidence_ids, tuple)
        or missing_readiness_evidence_ids != ()
    ):
        _add_reason(reason_codes, "MISSING_READINESS_EVIDENCE_IDS_DECLARED")
        _add_field(
            field_entries,
            reason_code="MISSING_READINESS_EVIDENCE_IDS_DECLARED",
            field="missing_readiness_evidence_ids",
        )

    known_readiness_evidence_ids = _known_readiness_evidence_ids(
        readiness_evidence_items
    )
    if not isinstance(blocking_readiness_evidence_ids, tuple):
        _add_reason(reason_codes, "BLOCKING_READINESS_EVIDENCE_ID_UNKNOWN")
        _add_field(
            field_entries,
            reason_code="BLOCKING_READINESS_EVIDENCE_ID_UNKNOWN",
            field="blocking_readiness_evidence_ids",
        )
    else:
        for blocking_readiness_evidence_id in blocking_readiness_evidence_ids:
            if (
                not _is_nonblank_string(blocking_readiness_evidence_id)
                or blocking_readiness_evidence_id
                not in known_readiness_evidence_ids
            ):
                _add_reason(
                    reason_codes,
                    "BLOCKING_READINESS_EVIDENCE_ID_UNKNOWN",
                )
                _add_field(
                    field_entries,
                    reason_code="BLOCKING_READINESS_EVIDENCE_ID_UNKNOWN",
                    field="blocking_readiness_evidence_ids",
                )

    if not _is_nonblank_string(created_at):
        _add_reason(reason_codes, "CREATED_AT_MISSING")
        _add_field(
            field_entries,
            reason_code="CREATED_AT_MISSING",
            field="created_at",
        )

    if not _is_nonblank_string(timestamp_policy):
        _add_reason(reason_codes, "TIMESTAMP_POLICY_MISSING")
        _add_field(
            field_entries,
            reason_code="TIMESTAMP_POLICY_MISSING",
            field="timestamp_policy",
        )

    if not _is_nonempty_string_tuple(source_of_truth):
        _add_reason(reason_codes, "SOURCE_OF_TRUTH_MISSING")
        _add_field(
            field_entries,
            reason_code="SOURCE_OF_TRUTH_MISSING",
            field="source_of_truth",
        )

    seen_readiness_evidence_ids = ()
    if isinstance(readiness_evidence_items, tuple):
        for index, readiness_evidence_item in enumerate(readiness_evidence_items):
            readiness_evidence_id = _readiness_evidence_id_from(
                readiness_evidence_item
            )
            if not isinstance(readiness_evidence_item, dict):
                _add_reason(reason_codes, "READINESS_EVIDENCE_ITEM_NOT_DICT")
                _add_field(
                    field_entries,
                    reason_code="READINESS_EVIDENCE_ITEM_NOT_DICT",
                    field=f"readiness_evidence_items[{index}]",
                )
                _add_readiness_evidence_item_violation(
                    readiness_evidence_item_violations,
                    readiness_evidence_item_index=index,
                    readiness_evidence_id="",
                    reason_code="READINESS_EVIDENCE_ITEM_NOT_DICT",
                    field=f"readiness_evidence_items[{index}]",
                )
                continue

            if not _has_exact_readiness_evidence_item_keys(
                readiness_evidence_item
            ):
                _add_reason(reason_codes, "READINESS_EVIDENCE_ITEM_KEYS_INVALID")
                _add_field(
                    field_entries,
                    reason_code="READINESS_EVIDENCE_ITEM_KEYS_INVALID",
                    field=f"readiness_evidence_items[{index}].keys",
                )
                _add_readiness_evidence_item_violation(
                    readiness_evidence_item_violations,
                    readiness_evidence_item_index=index,
                    readiness_evidence_id=readiness_evidence_id,
                    reason_code="READINESS_EVIDENCE_ITEM_KEYS_INVALID",
                    field="keys",
                )

            for field_name, reason_code in (
                _READINESS_EVIDENCE_ITEM_STRING_FIELDS
            ):
                if not _is_nonblank_string(
                    readiness_evidence_item.get(field_name)
                ):
                    _add_reason(reason_codes, reason_code)
                    _add_field(
                        field_entries,
                        reason_code=reason_code,
                        field=(
                            f"readiness_evidence_items[{index}]."
                            f"{field_name}"
                        ),
                    )
                    _add_readiness_evidence_item_violation(
                        readiness_evidence_item_violations,
                        readiness_evidence_item_index=index,
                        readiness_evidence_id=readiness_evidence_id,
                        reason_code=reason_code,
                        field=field_name,
                    )

            if not _is_nonempty_string_tuple(
                readiness_evidence_item.get("evidence_refs")
            ):
                _add_reason(reason_codes, "READINESS_EVIDENCE_REFS_MISSING")
                _add_field(
                    field_entries,
                    reason_code="READINESS_EVIDENCE_REFS_MISSING",
                    field=f"readiness_evidence_items[{index}].evidence_refs",
                )
                _add_readiness_evidence_item_violation(
                    readiness_evidence_item_violations,
                    readiness_evidence_item_index=index,
                    readiness_evidence_id=readiness_evidence_id,
                    reason_code="READINESS_EVIDENCE_REFS_MISSING",
                    field="evidence_refs",
                )

            if (
                _is_nonblank_string(readiness_evidence_id)
                and readiness_evidence_id in seen_readiness_evidence_ids
            ):
                _add_reason(reason_codes, "READINESS_EVIDENCE_ID_DUPLICATE")
                _add_field(
                    field_entries,
                    reason_code="READINESS_EVIDENCE_ID_DUPLICATE",
                    field=(
                        f"readiness_evidence_items[{index}]."
                        "readiness_evidence_id"
                    ),
                )
                _add_readiness_evidence_item_violation(
                    readiness_evidence_item_violations,
                    readiness_evidence_item_index=index,
                    readiness_evidence_id=readiness_evidence_id,
                    reason_code="READINESS_EVIDENCE_ID_DUPLICATE",
                    field="readiness_evidence_id",
                )

            if _is_nonblank_string(readiness_evidence_id):
                seen_readiness_evidence_ids = (
                    seen_readiness_evidence_ids + (readiness_evidence_id,)
                )

            if (
                _is_nonempty_string_tuple(required_readiness_evidence_ids)
                and _is_nonblank_string(readiness_evidence_id)
                and readiness_evidence_id not in required_readiness_evidence_ids
            ):
                _add_reason(reason_codes, "READINESS_EVIDENCE_ID_NOT_REQUIRED")
                _add_field(
                    field_entries,
                    reason_code="READINESS_EVIDENCE_ID_NOT_REQUIRED",
                    field=(
                        f"readiness_evidence_items[{index}]."
                        "readiness_evidence_id"
                    ),
                )
                _add_readiness_evidence_item_violation(
                    readiness_evidence_item_violations,
                    readiness_evidence_item_index=index,
                    readiness_evidence_id=readiness_evidence_id,
                    reason_code="READINESS_EVIDENCE_ID_NOT_REQUIRED",
                    field="readiness_evidence_id",
                )

            for field_name in _FORBIDDEN_READINESS_EVIDENCE_ITEM_FIELDS:
                if field_name in readiness_evidence_item:
                    _add_reason(
                        reason_codes,
                        "READINESS_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT",
                    )
                    _add_field(
                        field_entries,
                        reason_code=(
                            "READINESS_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT"
                        ),
                        field=(
                            f"readiness_evidence_items[{index}].{field_name}"
                        ),
                    )
                    _add_readiness_evidence_item_violation(
                        readiness_evidence_item_violations,
                        readiness_evidence_item_index=index,
                        readiness_evidence_id=readiness_evidence_id,
                        reason_code=(
                            "READINESS_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT"
                        ),
                        field=field_name,
                    )

    if _is_nonempty_string_tuple(required_readiness_evidence_ids):
        for required_readiness_evidence_id in required_readiness_evidence_ids:
            if required_readiness_evidence_id not in known_readiness_evidence_ids:
                _add_reason(reason_codes, "REQUIRED_READINESS_EVIDENCE_MISSING")
                _add_field(
                    field_entries,
                    reason_code="REQUIRED_READINESS_EVIDENCE_MISSING",
                    field=(
                        "required_readiness_evidence_ids."
                        f"{required_readiness_evidence_id}"
                    ),
                )

    readiness_violations = _ordered_reason_codes(tuple(reason_codes))
    buildable = readiness_violations == ()
    reason_code = (
        "LOCAL_NOOP_RUNNER_READINESS_BUILDABLE"
        if buildable
        else readiness_violations[0]
    )

    source = {
        "mode": _safe_string(mode),
        "expected_terminal_status": _safe_expected_terminal_status(
            expected_terminal_status
        ),
        "local_noop_runner_envelope_ref": _safe_string(
            local_noop_runner_envelope_ref
        ),
        "local_noop_runner_envelope_buildable_marker": (
            local_noop_runner_envelope_buildable_marker
        ),
        "public_url": None,
        "public_url_created": False,
        "source_of_truth": _safe_string_tuple(source_of_truth),
    }
    local_noop_runner_readiness = {
        "run_id": _safe_string(run_id),
        "local_noop_runner_readiness_id": _safe_string(
            local_noop_runner_readiness_id
        ),
        "readiness_kind": _safe_string(readiness_kind),
        "mode": _safe_string(mode),
        "expected_terminal_status": _safe_expected_terminal_status(
            expected_terminal_status
        ),
        "local_noop_runner_envelope_ref": _safe_string(
            local_noop_runner_envelope_ref
        ),
        "local_noop_runner_envelope_buildable_marker": (
            local_noop_runner_envelope_buildable_marker
        ),
        "public_url": None,
        "public_url_created": False,
        "readiness_evidence_items": _safe_readiness_evidence_items(
            readiness_evidence_items
        ),
        "required_readiness_evidence_ids": _safe_string_tuple(
            required_readiness_evidence_ids
        ),
        "missing_readiness_evidence_ids": _safe_string_tuple(
            missing_readiness_evidence_ids
        ),
        "blocking_readiness_evidence_ids": _safe_string_tuple(
            blocking_readiness_evidence_ids
        ),
        "created_at": _safe_string(created_at),
        "timestamp_policy": _safe_string(timestamp_policy),
        "source_of_truth": _safe_string_tuple(source_of_truth),
        "notes": _safe_string_tuple(notes),
    }

    return {
        "buildable": buildable,
        "reason_code": reason_code,
        "reason": _reason_text(reason_code),
        "source": source,
        "local_noop_runner_readiness": local_noop_runner_readiness,
        "readiness_violations": readiness_violations,
        "missing_or_invalid_fields": _ordered_fields(tuple(field_entries)),
        "readiness_evidence_item_violations": (
            _ordered_readiness_evidence_item_violations(
                tuple(readiness_evidence_item_violations)
            )
        ),
        "invariant_refs": _INVARIANT_REFS,
    }


def is_local_noop_runner_readiness_buildable(
    *,
    run_id: str,
    local_noop_runner_readiness_id: str,
    readiness_kind: str,
    mode: str,
    expected_terminal_status: str,
    local_noop_runner_envelope_ref: str,
    local_noop_runner_envelope_buildable_marker: bool,
    public_url_created: bool,
    public_url_is_null: bool,
    readiness_evidence_items: tuple[dict[str, object], ...],
    required_readiness_evidence_ids: tuple[str, ...],
    missing_readiness_evidence_ids: tuple[str, ...],
    blocking_readiness_evidence_ids: tuple[str, ...],
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> bool:
    """Return whether the local noop runner readiness shape is buildable."""

    return bool(
        explain_local_noop_runner_readiness_build(
            run_id=run_id,
            local_noop_runner_readiness_id=local_noop_runner_readiness_id,
            readiness_kind=readiness_kind,
            mode=mode,
            expected_terminal_status=expected_terminal_status,
            local_noop_runner_envelope_ref=local_noop_runner_envelope_ref,
            local_noop_runner_envelope_buildable_marker=(
                local_noop_runner_envelope_buildable_marker
            ),
            public_url_created=public_url_created,
            public_url_is_null=public_url_is_null,
            readiness_evidence_items=readiness_evidence_items,
            required_readiness_evidence_ids=required_readiness_evidence_ids,
            missing_readiness_evidence_ids=missing_readiness_evidence_ids,
            blocking_readiness_evidence_ids=blocking_readiness_evidence_ids,
            created_at=created_at,
            timestamp_policy=timestamp_policy,
            source_of_truth=source_of_truth,
            notes=notes,
        )["buildable"]
    )
