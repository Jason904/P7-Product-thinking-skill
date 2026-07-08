"""Build pure run ledger draft buildability explanations."""

from typing import Final


REASON_CODES: Final[tuple[str, ...]] = (
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

RUN_LEDGER_DRAFT_BUILD_REASON_CODES: Final[tuple[str, ...]] = (
    REASON_CODES
)

REASON_PRIORITY: Final[tuple[str, ...]] = (
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

_DRAFT_KIND: Final[str] = "run_ledger_draft"
_NOOP_MODE: Final[str] = "noop"
_NOOP_COMPLETED: Final[str] = "NOOP_COMPLETED"
_PASS_PUBLISHED: Final[str] = "PASS_PUBLISHED"

_LEDGER_DRAFT_EVIDENCE_ITEM_KEYS: Final[tuple[str, ...]] = (
    "ledger_draft_evidence_id",
    "ledger_draft_evidence_role",
    "artifact_ref",
    "artifact_kind",
    "evidence_status",
    "producer_ref",
    "evidence_refs",
    "notes",
)

_LEDGER_DRAFT_EVIDENCE_ITEM_STRING_FIELDS: Final[
    tuple[tuple[str, str], ...]
] = (
    ("ledger_draft_evidence_id", "LEDGER_DRAFT_EVIDENCE_ID_MISSING"),
    ("ledger_draft_evidence_role", "LEDGER_DRAFT_EVIDENCE_ROLE_MISSING"),
    ("artifact_ref", "LEDGER_DRAFT_EVIDENCE_ARTIFACT_REF_MISSING"),
    ("artifact_kind", "LEDGER_DRAFT_EVIDENCE_ARTIFACT_KIND_MISSING"),
    ("evidence_status", "LEDGER_DRAFT_EVIDENCE_STATUS_MISSING"),
    ("producer_ref", "LEDGER_DRAFT_EVIDENCE_PRODUCER_REF_MISSING"),
)

_FORBIDDEN_LEDGER_DRAFT_EVIDENCE_ITEM_FIELDS: Final[tuple[str, ...]] = (
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

_INVARIANT_REFS: Final[tuple[str, ...]] = (
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

_REASON_TEXT_ENTRIES: Final[tuple[tuple[str, str], ...]] = (
    ("RUN_ID_MISSING", "A non-empty caller-supplied run_id is required."),
    (
        "RUN_LEDGER_DRAFT_ID_MISSING",
        "A non-empty caller-supplied run_ledger_draft_id is required.",
    ),
    (
        "DRAFT_KIND_NOT_RUN_LEDGER_DRAFT",
        "draft_kind must be run_ledger_draft.",
    ),
    ("MODE_NOT_NOOP", "mode must be noop."),
    (
        "PASS_PUBLISHED_FORBIDDEN",
        "PASS_PUBLISHED is forbidden for run ledger drafts.",
    ),
    (
        "LEDGER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
        "ledger_terminal_status must be NOOP_COMPLETED.",
    ),
    (
        "LOCAL_NOOP_RUNNER_RESULT_REF_MISSING",
        "A caller-supplied local noop runner result ref is required.",
    ),
    (
        "LOCAL_NOOP_RUNNER_RESULT_BUILDABLE_MARKER_NOT_TRUE",
        "The caller-supplied local noop runner result buildable marker must "
        "be true.",
    ),
    (
        "PUBLIC_URL_IS_NULL_NOT_TRUE",
        "The caller-supplied public URL null marker must be true.",
    ),
    (
        "PUBLIC_URL_CREATED_NOT_FALSE",
        "public_url_created must remain false.",
    ),
    (
        "LEDGER_DRAFT_EVIDENCE_ITEMS_MISSING",
        "At least one ledger draft evidence item is required.",
    ),
    (
        "REQUIRED_LEDGER_DRAFT_EVIDENCE_IDS_MISSING",
        "At least one required ledger draft evidence id is required.",
    ),
    (
        "MISSING_LEDGER_DRAFT_EVIDENCE_IDS_DECLARED",
        "missing_ledger_draft_evidence_ids must be an empty tuple.",
    ),
    (
        "BLOCKING_LEDGER_DRAFT_EVIDENCE_ID_UNKNOWN",
        "Blocking ledger draft evidence ids must be known non-empty ids.",
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
        "LEDGER_DRAFT_EVIDENCE_ITEM_NOT_DICT",
        "Every ledger draft evidence item must be a dict.",
    ),
    (
        "LEDGER_DRAFT_EVIDENCE_ITEM_KEYS_INVALID",
        "Every ledger draft evidence item must contain the exact expected keys.",
    ),
    (
        "LEDGER_DRAFT_EVIDENCE_ID_MISSING",
        "Every ledger draft evidence item requires a non-empty ledger_draft_evidence_id.",
    ),
    (
        "LEDGER_DRAFT_EVIDENCE_ROLE_MISSING",
        "Every ledger draft evidence item requires a non-empty ledger_draft_evidence_role.",
    ),
    (
        "LEDGER_DRAFT_EVIDENCE_ARTIFACT_REF_MISSING",
        "Every ledger draft evidence item requires a non-empty artifact_ref.",
    ),
    (
        "LEDGER_DRAFT_EVIDENCE_ARTIFACT_KIND_MISSING",
        "Every ledger draft evidence item requires a non-empty artifact_kind.",
    ),
    (
        "LEDGER_DRAFT_EVIDENCE_STATUS_MISSING",
        "Every ledger draft evidence item requires a non-empty evidence_status.",
    ),
    (
        "LEDGER_DRAFT_EVIDENCE_PRODUCER_REF_MISSING",
        "Every ledger draft evidence item requires a non-empty producer_ref.",
    ),
    (
        "LEDGER_DRAFT_EVIDENCE_REFS_MISSING",
        "Every ledger draft evidence item requires non-empty evidence_refs.",
    ),
    (
        "LEDGER_DRAFT_EVIDENCE_ID_DUPLICATE",
        "ledger_draft_evidence_id values must be unique.",
    ),
    (
        "LEDGER_DRAFT_EVIDENCE_ID_NOT_REQUIRED",
        "Every ledger_draft_evidence_id must be declared as required.",
    ),
    (
        "REQUIRED_LEDGER_DRAFT_EVIDENCE_MISSING",
        "Every required ledger draft evidence id must have one evidence item.",
    ),
    (
        "LEDGER_DRAFT_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT",
        "Ledger draft evidence items must not contain raw, execution, URL, IO, "
        "publish, ledger, notification, or policy fields.",
    ),
    (
        "RUN_LEDGER_DRAFT_BUILDABLE",
        "The caller-supplied fields can build the run ledger draft "
        "shape. This does not write run-ledger.yaml, execute a runner, "
        "runtime, dry-run, E2E, noop completion, transition, gate, policy, "
        "validator, eval, audit, publish, ledger write, notification, "
        "artifact read, existing builder call, or public URL behavior.",
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


def _safe_terminal_status(value: object) -> str:
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


def _safe_ledger_draft_evidence_item(
    ledger_draft_evidence_item: object,
) -> dict[str, object]:
    if not isinstance(ledger_draft_evidence_item, dict):
        return {
            "ledger_draft_evidence_id": "",
            "ledger_draft_evidence_role": "",
            "artifact_ref": "",
            "artifact_kind": "",
            "evidence_status": "",
            "producer_ref": "",
            "evidence_refs": (),
            "notes": (),
        }

    return {
        "ledger_draft_evidence_id": _safe_string(
            ledger_draft_evidence_item.get("ledger_draft_evidence_id")
        ),
        "ledger_draft_evidence_role": _safe_string(
            ledger_draft_evidence_item.get("ledger_draft_evidence_role")
        ),
        "artifact_ref": _safe_string(ledger_draft_evidence_item.get("artifact_ref")),
        "artifact_kind": _safe_string(
            ledger_draft_evidence_item.get("artifact_kind")
        ),
        "evidence_status": _safe_string(
            ledger_draft_evidence_item.get("evidence_status")
        ),
        "producer_ref": _safe_string(
            ledger_draft_evidence_item.get("producer_ref")
        ),
        "evidence_refs": _safe_string_tuple(
            ledger_draft_evidence_item.get("evidence_refs")
        ),
        "notes": _safe_string_tuple(ledger_draft_evidence_item.get("notes")),
    }


def _safe_ledger_draft_evidence_items(
    value: object,
) -> tuple[dict[str, object], ...]:
    if not isinstance(value, tuple):
        return ()

    safe_items = ()
    for ledger_draft_evidence_item in value:
        safe_items = safe_items + (
            _safe_ledger_draft_evidence_item(ledger_draft_evidence_item),
        )
    return safe_items


def _reason_text(reason_code: str) -> str:
    for code, text in _REASON_TEXT_ENTRIES:
        if code == reason_code:
            return text
    return "Unknown run ledger draft build result."


def _reason_rank(reason_code: str) -> int:
    if reason_code in REASON_PRIORITY:
        return REASON_PRIORITY.index(reason_code)
    return len(REASON_PRIORITY)


def _add_reason(reason_codes: list[str], reason_code: str) -> None:
    reason_codes.append(reason_code)


def _add_field(
    fields: list[tuple[str, str]],
    *,
    reason_code: str,
    field: str,
) -> None:
    fields.append((reason_code, field))


def _add_ledger_draft_evidence_item_violation(
    ledger_draft_evidence_item_violations: list[dict[str, object]],
    *,
    ledger_draft_evidence_item_index: int,
    ledger_draft_evidence_id: str,
    reason_code: str,
    field: str,
) -> None:
    ledger_draft_evidence_item_violations.append(
        {
            "ledger_draft_evidence_item_index": ledger_draft_evidence_item_index,
            "ledger_draft_evidence_id": ledger_draft_evidence_id,
            "reason_code": reason_code,
            "field": field,
        }
    )


def _ordered_reason_codes(reason_codes: tuple[str, ...]) -> tuple[str, ...]:
    ordered = ()
    for reason_code in REASON_PRIORITY:
        if reason_code == "RUN_LEDGER_DRAFT_BUILDABLE":
            continue
        if reason_code in reason_codes and reason_code not in ordered:
            ordered = ordered + (reason_code,)
    return ordered


def _ordered_fields(field_entries: tuple[tuple[str, str], ...]) -> tuple[str, ...]:
    ordered_entries = sorted(
        field_entries,
        key=lambda item: (_reason_rank(item[0]), item[1]),
    )
    fields = ()
    for unused_reason_code, field in ordered_entries:
        if field not in fields:
            fields = fields + (field,)
    return fields


def _ordered_ledger_draft_evidence_item_violations(
    ledger_draft_evidence_item_violations: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    return tuple(
        sorted(
            ledger_draft_evidence_item_violations,
            key=lambda item: (
                _reason_rank(_safe_string(item.get("reason_code"))),
                item.get("ledger_draft_evidence_item_index"),
                _safe_string(item.get("field")),
            ),
        )
    )


def _ledger_draft_evidence_id_from(ledger_draft_evidence_item: object) -> str:
    if not isinstance(ledger_draft_evidence_item, dict):
        return ""
    return _safe_string(ledger_draft_evidence_item.get("ledger_draft_evidence_id"))


def _known_ledger_draft_evidence_ids(
    ledger_draft_evidence_items: object,
) -> tuple[str, ...]:
    if not isinstance(ledger_draft_evidence_items, tuple):
        return ()

    ledger_draft_evidence_ids = ()
    for ledger_draft_evidence_item in ledger_draft_evidence_items:
        ledger_draft_evidence_id = _ledger_draft_evidence_id_from(ledger_draft_evidence_item)
        if _is_nonblank_string(ledger_draft_evidence_id):
            ledger_draft_evidence_ids = ledger_draft_evidence_ids + (ledger_draft_evidence_id,)
    return ledger_draft_evidence_ids


def _has_exact_ledger_draft_evidence_item_keys(
    ledger_draft_evidence_item: dict[str, object],
) -> bool:
    for expected_key in _LEDGER_DRAFT_EVIDENCE_ITEM_KEYS:
        if expected_key not in ledger_draft_evidence_item:
            return False
    for key in ledger_draft_evidence_item:
        if key not in _LEDGER_DRAFT_EVIDENCE_ITEM_KEYS:
            return False
    return True


def explain_run_ledger_draft_build(
    *,
    run_id: str,
    run_ledger_draft_id: str,
    draft_kind: str,
    mode: str,
    ledger_terminal_status: str,
    local_noop_runner_result_ref: str,
    local_noop_runner_result_buildable_marker: bool,
    public_url_created: bool,
    public_url_is_null: bool,
    ledger_draft_evidence_items: tuple[dict[str, object], ...],
    required_ledger_draft_evidence_ids: tuple[str, ...],
    missing_ledger_draft_evidence_ids: tuple[str, ...],
    blocking_ledger_draft_evidence_ids: tuple[str, ...],
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    """Explain whether a caller-supplied run ledger draft is buildable."""

    reason_codes = []
    field_entries = []
    ledger_draft_evidence_item_violations = []

    if not _is_nonblank_string(run_id):
        _add_reason(reason_codes, "RUN_ID_MISSING")
        _add_field(field_entries, reason_code="RUN_ID_MISSING", field="run_id")

    if not _is_nonblank_string(run_ledger_draft_id):
        _add_reason(reason_codes, "RUN_LEDGER_DRAFT_ID_MISSING")
        _add_field(
            field_entries,
            reason_code="RUN_LEDGER_DRAFT_ID_MISSING",
            field="run_ledger_draft_id",
        )

    if draft_kind != _DRAFT_KIND:
        _add_reason(
            reason_codes,
            "DRAFT_KIND_NOT_RUN_LEDGER_DRAFT",
        )
        _add_field(
            field_entries,
            reason_code="DRAFT_KIND_NOT_RUN_LEDGER_DRAFT",
            field="draft_kind",
        )

    if mode != _NOOP_MODE:
        _add_reason(reason_codes, "MODE_NOT_NOOP")
        _add_field(
            field_entries,
            reason_code="MODE_NOT_NOOP",
            field="mode",
        )

    if ledger_terminal_status == _PASS_PUBLISHED:
        _add_reason(reason_codes, "PASS_PUBLISHED_FORBIDDEN")
        _add_field(
            field_entries,
            reason_code="PASS_PUBLISHED_FORBIDDEN",
            field="ledger_terminal_status",
        )

    if ledger_terminal_status != _NOOP_COMPLETED:
        _add_reason(
            reason_codes,
            "LEDGER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
        )
        _add_field(
            field_entries,
            reason_code="LEDGER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
            field="ledger_terminal_status",
        )

    if not _is_nonblank_string(local_noop_runner_result_ref):
        _add_reason(reason_codes, "LOCAL_NOOP_RUNNER_RESULT_REF_MISSING")
        _add_field(
            field_entries,
            reason_code="LOCAL_NOOP_RUNNER_RESULT_REF_MISSING",
            field="local_noop_runner_result_ref",
        )

    if local_noop_runner_result_buildable_marker is not True:
        _add_reason(
            reason_codes,
            "LOCAL_NOOP_RUNNER_RESULT_BUILDABLE_MARKER_NOT_TRUE",
        )
        _add_field(
            field_entries,
            reason_code="LOCAL_NOOP_RUNNER_RESULT_BUILDABLE_MARKER_NOT_TRUE",
            field="local_noop_runner_result_buildable_marker",
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
        not isinstance(ledger_draft_evidence_items, tuple)
        or ledger_draft_evidence_items == ()
    ):
        _add_reason(reason_codes, "LEDGER_DRAFT_EVIDENCE_ITEMS_MISSING")
        _add_field(
            field_entries,
            reason_code="LEDGER_DRAFT_EVIDENCE_ITEMS_MISSING",
            field="ledger_draft_evidence_items",
        )

    if not _is_nonempty_string_tuple(required_ledger_draft_evidence_ids):
        _add_reason(reason_codes, "REQUIRED_LEDGER_DRAFT_EVIDENCE_IDS_MISSING")
        _add_field(
            field_entries,
            reason_code="REQUIRED_LEDGER_DRAFT_EVIDENCE_IDS_MISSING",
            field="required_ledger_draft_evidence_ids",
        )

    if (
        not isinstance(missing_ledger_draft_evidence_ids, tuple)
        or missing_ledger_draft_evidence_ids != ()
    ):
        _add_reason(reason_codes, "MISSING_LEDGER_DRAFT_EVIDENCE_IDS_DECLARED")
        _add_field(
            field_entries,
            reason_code="MISSING_LEDGER_DRAFT_EVIDENCE_IDS_DECLARED",
            field="missing_ledger_draft_evidence_ids",
        )

    known_ledger_draft_evidence_ids = _known_ledger_draft_evidence_ids(
        ledger_draft_evidence_items
    )
    if not isinstance(blocking_ledger_draft_evidence_ids, tuple):
        _add_reason(reason_codes, "BLOCKING_LEDGER_DRAFT_EVIDENCE_ID_UNKNOWN")
        _add_field(
            field_entries,
            reason_code="BLOCKING_LEDGER_DRAFT_EVIDENCE_ID_UNKNOWN",
            field="blocking_ledger_draft_evidence_ids",
        )
    else:
        for blocking_ledger_draft_evidence_id in blocking_ledger_draft_evidence_ids:
            if (
                not _is_nonblank_string(blocking_ledger_draft_evidence_id)
                or blocking_ledger_draft_evidence_id not in known_ledger_draft_evidence_ids
            ):
                _add_reason(
                    reason_codes,
                    "BLOCKING_LEDGER_DRAFT_EVIDENCE_ID_UNKNOWN",
                )
                _add_field(
                    field_entries,
                    reason_code="BLOCKING_LEDGER_DRAFT_EVIDENCE_ID_UNKNOWN",
                    field="blocking_ledger_draft_evidence_ids",
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

    seen_ledger_draft_evidence_ids = ()
    if isinstance(ledger_draft_evidence_items, tuple):
        for index, ledger_draft_evidence_item in enumerate(ledger_draft_evidence_items):
            ledger_draft_evidence_id = _ledger_draft_evidence_id_from(
                ledger_draft_evidence_item
            )
            if not isinstance(ledger_draft_evidence_item, dict):
                _add_reason(reason_codes, "LEDGER_DRAFT_EVIDENCE_ITEM_NOT_DICT")
                _add_field(
                    field_entries,
                    reason_code="LEDGER_DRAFT_EVIDENCE_ITEM_NOT_DICT",
                    field=f"ledger_draft_evidence_items[{index}]",
                )
                _add_ledger_draft_evidence_item_violation(
                    ledger_draft_evidence_item_violations,
                    ledger_draft_evidence_item_index=index,
                    ledger_draft_evidence_id="",
                    reason_code="LEDGER_DRAFT_EVIDENCE_ITEM_NOT_DICT",
                    field=f"ledger_draft_evidence_items[{index}]",
                )
                continue

            if not _has_exact_ledger_draft_evidence_item_keys(ledger_draft_evidence_item):
                _add_reason(reason_codes, "LEDGER_DRAFT_EVIDENCE_ITEM_KEYS_INVALID")
                _add_field(
                    field_entries,
                    reason_code="LEDGER_DRAFT_EVIDENCE_ITEM_KEYS_INVALID",
                    field=f"ledger_draft_evidence_items[{index}].keys",
                )
                _add_ledger_draft_evidence_item_violation(
                    ledger_draft_evidence_item_violations,
                    ledger_draft_evidence_item_index=index,
                    ledger_draft_evidence_id=ledger_draft_evidence_id,
                    reason_code="LEDGER_DRAFT_EVIDENCE_ITEM_KEYS_INVALID",
                    field="keys",
                )

            for field_name, reason_code in _LEDGER_DRAFT_EVIDENCE_ITEM_STRING_FIELDS:
                if not _is_nonblank_string(ledger_draft_evidence_item.get(field_name)):
                    _add_reason(reason_codes, reason_code)
                    _add_field(
                        field_entries,
                        reason_code=reason_code,
                        field=f"ledger_draft_evidence_items[{index}].{field_name}",
                    )
                    _add_ledger_draft_evidence_item_violation(
                        ledger_draft_evidence_item_violations,
                        ledger_draft_evidence_item_index=index,
                        ledger_draft_evidence_id=ledger_draft_evidence_id,
                        reason_code=reason_code,
                        field=field_name,
                    )

            if not _is_nonempty_string_tuple(
                ledger_draft_evidence_item.get("evidence_refs")
            ):
                _add_reason(reason_codes, "LEDGER_DRAFT_EVIDENCE_REFS_MISSING")
                _add_field(
                    field_entries,
                    reason_code="LEDGER_DRAFT_EVIDENCE_REFS_MISSING",
                    field=f"ledger_draft_evidence_items[{index}].evidence_refs",
                )
                _add_ledger_draft_evidence_item_violation(
                    ledger_draft_evidence_item_violations,
                    ledger_draft_evidence_item_index=index,
                    ledger_draft_evidence_id=ledger_draft_evidence_id,
                    reason_code="LEDGER_DRAFT_EVIDENCE_REFS_MISSING",
                    field="evidence_refs",
                )

            if (
                _is_nonblank_string(ledger_draft_evidence_id)
                and ledger_draft_evidence_id in seen_ledger_draft_evidence_ids
            ):
                _add_reason(reason_codes, "LEDGER_DRAFT_EVIDENCE_ID_DUPLICATE")
                _add_field(
                    field_entries,
                    reason_code="LEDGER_DRAFT_EVIDENCE_ID_DUPLICATE",
                    field=(
                        f"ledger_draft_evidence_items[{index}]."
                        "ledger_draft_evidence_id"
                    ),
                )
                _add_ledger_draft_evidence_item_violation(
                    ledger_draft_evidence_item_violations,
                    ledger_draft_evidence_item_index=index,
                    ledger_draft_evidence_id=ledger_draft_evidence_id,
                    reason_code="LEDGER_DRAFT_EVIDENCE_ID_DUPLICATE",
                    field="ledger_draft_evidence_id",
                )

            if _is_nonblank_string(ledger_draft_evidence_id):
                seen_ledger_draft_evidence_ids = (
                    seen_ledger_draft_evidence_ids + (ledger_draft_evidence_id,)
                )

            if (
                _is_nonempty_string_tuple(required_ledger_draft_evidence_ids)
                and _is_nonblank_string(ledger_draft_evidence_id)
                and ledger_draft_evidence_id not in required_ledger_draft_evidence_ids
            ):
                _add_reason(reason_codes, "LEDGER_DRAFT_EVIDENCE_ID_NOT_REQUIRED")
                _add_field(
                    field_entries,
                    reason_code="LEDGER_DRAFT_EVIDENCE_ID_NOT_REQUIRED",
                    field=(
                        f"ledger_draft_evidence_items[{index}]."
                        "ledger_draft_evidence_id"
                    ),
                )
                _add_ledger_draft_evidence_item_violation(
                    ledger_draft_evidence_item_violations,
                    ledger_draft_evidence_item_index=index,
                    ledger_draft_evidence_id=ledger_draft_evidence_id,
                    reason_code="LEDGER_DRAFT_EVIDENCE_ID_NOT_REQUIRED",
                    field="ledger_draft_evidence_id",
                )

            for field_name in _FORBIDDEN_LEDGER_DRAFT_EVIDENCE_ITEM_FIELDS:
                if field_name in ledger_draft_evidence_item:
                    _add_reason(
                        reason_codes,
                        "LEDGER_DRAFT_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT",
                    )
                    _add_field(
                        field_entries,
                        reason_code=(
                            "LEDGER_DRAFT_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT"
                        ),
                        field=f"ledger_draft_evidence_items[{index}].{field_name}",
                    )
                    _add_ledger_draft_evidence_item_violation(
                        ledger_draft_evidence_item_violations,
                        ledger_draft_evidence_item_index=index,
                        ledger_draft_evidence_id=ledger_draft_evidence_id,
                        reason_code=(
                            "LEDGER_DRAFT_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT"
                        ),
                        field=field_name,
                    )

    if _is_nonempty_string_tuple(required_ledger_draft_evidence_ids):
        for required_ledger_draft_evidence_id in required_ledger_draft_evidence_ids:
            if required_ledger_draft_evidence_id not in known_ledger_draft_evidence_ids:
                _add_reason(reason_codes, "REQUIRED_LEDGER_DRAFT_EVIDENCE_MISSING")
                _add_field(
                    field_entries,
                    reason_code="REQUIRED_LEDGER_DRAFT_EVIDENCE_MISSING",
                    field=(
                        "required_ledger_draft_evidence_ids."
                        f"{required_ledger_draft_evidence_id}"
                    ),
                )

    draft_violations = _ordered_reason_codes(tuple(reason_codes))
    buildable = draft_violations == ()
    reason_code = (
        "RUN_LEDGER_DRAFT_BUILDABLE"
        if buildable
        else draft_violations[0]
    )

    source = {
        "local_noop_runner_result_ref": _safe_string(
            local_noop_runner_result_ref
        ),
        "local_noop_runner_result_buildable_marker": (
            local_noop_runner_result_buildable_marker
        ),
        "mode": _safe_string(mode),
        "ledger_terminal_status": _safe_terminal_status(
            ledger_terminal_status
        ),
        "public_url": None,
        "public_url_created": False,
        "source_of_truth": _safe_string_tuple(source_of_truth),
    }
    run_ledger_draft = {
        "run_id": _safe_string(run_id),
        "run_ledger_draft_id": _safe_string(
            run_ledger_draft_id
        ),
        "draft_kind": _safe_string(draft_kind),
        "mode": _safe_string(mode),
        "ledger_terminal_status": _safe_terminal_status(
            ledger_terminal_status
        ),
        "local_noop_runner_result_ref": _safe_string(
            local_noop_runner_result_ref
        ),
        "local_noop_runner_result_buildable_marker": (
            local_noop_runner_result_buildable_marker
        ),
        "public_url": None,
        "public_url_created": False,
        "ledger_draft_evidence_items": _safe_ledger_draft_evidence_items(
            ledger_draft_evidence_items
        ),
        "required_ledger_draft_evidence_ids": _safe_string_tuple(
            required_ledger_draft_evidence_ids
        ),
        "missing_ledger_draft_evidence_ids": _safe_string_tuple(
            missing_ledger_draft_evidence_ids
        ),
        "blocking_ledger_draft_evidence_ids": _safe_string_tuple(
            blocking_ledger_draft_evidence_ids
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
        "run_ledger_draft": run_ledger_draft,
        "draft_violations": draft_violations,
        "missing_or_invalid_fields": _ordered_fields(tuple(field_entries)),
        "ledger_draft_evidence_item_violations": (
            _ordered_ledger_draft_evidence_item_violations(
                tuple(ledger_draft_evidence_item_violations)
            )
        ),
        "invariant_refs": _INVARIANT_REFS,
    }


def is_run_ledger_draft_buildable(
    *,
    run_id: str,
    run_ledger_draft_id: str,
    draft_kind: str,
    mode: str,
    ledger_terminal_status: str,
    local_noop_runner_result_ref: str,
    local_noop_runner_result_buildable_marker: bool,
    public_url_created: bool,
    public_url_is_null: bool,
    ledger_draft_evidence_items: tuple[dict[str, object], ...],
    required_ledger_draft_evidence_ids: tuple[str, ...],
    missing_ledger_draft_evidence_ids: tuple[str, ...],
    blocking_ledger_draft_evidence_ids: tuple[str, ...],
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> bool:
    """Return whether the run ledger draft shape is buildable."""

    return bool(
        explain_run_ledger_draft_build(
            run_id=run_id,
            run_ledger_draft_id=run_ledger_draft_id,
            draft_kind=draft_kind,
            mode=mode,
            ledger_terminal_status=ledger_terminal_status,
            local_noop_runner_result_ref=local_noop_runner_result_ref,
            local_noop_runner_result_buildable_marker=(
                local_noop_runner_result_buildable_marker
            ),
            public_url_created=public_url_created,
            public_url_is_null=public_url_is_null,
            ledger_draft_evidence_items=ledger_draft_evidence_items,
            required_ledger_draft_evidence_ids=required_ledger_draft_evidence_ids,
            missing_ledger_draft_evidence_ids=missing_ledger_draft_evidence_ids,
            blocking_ledger_draft_evidence_ids=blocking_ledger_draft_evidence_ids,
            created_at=created_at,
            timestamp_policy=timestamp_policy,
            source_of_truth=source_of_truth,
            notes=notes,
        )["buildable"]
    )
