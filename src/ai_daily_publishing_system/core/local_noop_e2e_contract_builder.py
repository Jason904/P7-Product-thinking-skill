"""Build pure local noop E2E dry-run contract buildability explanations."""

from typing import Final


REASON_CODES: Final[tuple[str, ...]] = (
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

LOCAL_NOOP_E2E_CONTRACT_BUILD_REASON_CODES: Final[tuple[str, ...]] = (
    REASON_CODES
)

REASON_PRIORITY: Final[tuple[str, ...]] = (
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

_CONTRACT_KIND: Final[str] = "local_noop_e2e_dry_run_contract"
_NOOP_MODE: Final[str] = "noop"
_NOOP_COMPLETED: Final[str] = "NOOP_COMPLETED"
_PASS_PUBLISHED: Final[str] = "PASS_PUBLISHED"

_DRY_RUN_EVIDENCE_ITEM_KEYS: Final[tuple[str, ...]] = (
    "dry_run_evidence_id",
    "dry_run_evidence_role",
    "artifact_ref",
    "artifact_kind",
    "evidence_status",
    "producer_ref",
    "evidence_refs",
    "notes",
)

_DRY_RUN_EVIDENCE_ITEM_STRING_FIELDS: Final[
    tuple[tuple[str, str], ...]
] = (
    ("dry_run_evidence_id", "DRY_RUN_EVIDENCE_ID_MISSING"),
    ("dry_run_evidence_role", "DRY_RUN_EVIDENCE_ROLE_MISSING"),
    ("artifact_ref", "DRY_RUN_EVIDENCE_ARTIFACT_REF_MISSING"),
    ("artifact_kind", "DRY_RUN_EVIDENCE_ARTIFACT_KIND_MISSING"),
    ("evidence_status", "DRY_RUN_EVIDENCE_STATUS_MISSING"),
    ("producer_ref", "DRY_RUN_EVIDENCE_PRODUCER_REF_MISSING"),
)

_FORBIDDEN_DRY_RUN_EVIDENCE_ITEM_FIELDS: Final[tuple[str, ...]] = (
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

_INVARIANT_REFS: Final[tuple[str, ...]] = (
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


def _safe_dry_run_evidence_item(
    dry_run_evidence_item: object,
) -> dict[str, object]:
    if not isinstance(dry_run_evidence_item, dict):
        return {
            "dry_run_evidence_id": "",
            "dry_run_evidence_role": "",
            "artifact_ref": "",
            "artifact_kind": "",
            "evidence_status": "",
            "producer_ref": "",
            "evidence_refs": (),
            "notes": (),
        }

    return {
        "dry_run_evidence_id": _safe_string(
            dry_run_evidence_item.get("dry_run_evidence_id")
        ),
        "dry_run_evidence_role": _safe_string(
            dry_run_evidence_item.get("dry_run_evidence_role")
        ),
        "artifact_ref": _safe_string(
            dry_run_evidence_item.get("artifact_ref")
        ),
        "artifact_kind": _safe_string(
            dry_run_evidence_item.get("artifact_kind")
        ),
        "evidence_status": _safe_string(
            dry_run_evidence_item.get("evidence_status")
        ),
        "producer_ref": _safe_string(
            dry_run_evidence_item.get("producer_ref")
        ),
        "evidence_refs": _safe_string_tuple(
            dry_run_evidence_item.get("evidence_refs")
        ),
        "notes": _safe_string_tuple(dry_run_evidence_item.get("notes")),
    }


def _safe_dry_run_evidence_items(
    value: object,
) -> tuple[dict[str, object], ...]:
    if not isinstance(value, tuple):
        return ()

    safe_items = ()
    for dry_run_evidence_item in value:
        safe_items = safe_items + (
            _safe_dry_run_evidence_item(dry_run_evidence_item),
        )
    return safe_items


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


def _add_dry_run_evidence_item_violation(
    dry_run_evidence_item_violations: list[dict[str, object]],
    *,
    dry_run_evidence_item_index: int,
    dry_run_evidence_id: str,
    reason_code: str,
    field: str,
) -> None:
    dry_run_evidence_item_violations.append(
        {
            "dry_run_evidence_item_index": dry_run_evidence_item_index,
            "dry_run_evidence_id": dry_run_evidence_id,
            "reason_code": reason_code,
            "field": field,
        }
    )


def _ordered_reason_codes(reason_codes: tuple[str, ...]) -> tuple[str, ...]:
    ordered = ()
    for reason_code in REASON_PRIORITY:
        if reason_code == "LOCAL_NOOP_E2E_CONTRACT_BUILDABLE":
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


def _ordered_dry_run_evidence_item_violations(
    dry_run_evidence_item_violations: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    return tuple(
        sorted(
            dry_run_evidence_item_violations,
            key=lambda item: (
                _reason_rank(_safe_string(item.get("reason_code"))),
                item.get("dry_run_evidence_item_index"),
                _safe_string(item.get("field")),
            ),
        )
    )


def _dry_run_evidence_id_from(dry_run_evidence_item: object) -> str:
    if not isinstance(dry_run_evidence_item, dict):
        return ""
    return _safe_string(dry_run_evidence_item.get("dry_run_evidence_id"))


def _known_dry_run_evidence_ids(
    dry_run_evidence_items: object,
) -> tuple[str, ...]:
    if not isinstance(dry_run_evidence_items, tuple):
        return ()

    dry_run_evidence_ids = ()
    for dry_run_evidence_item in dry_run_evidence_items:
        dry_run_evidence_id = _dry_run_evidence_id_from(
            dry_run_evidence_item
        )
        if _is_nonblank_string(dry_run_evidence_id):
            dry_run_evidence_ids = (
                dry_run_evidence_ids + (dry_run_evidence_id,)
            )
    return dry_run_evidence_ids


def _has_exact_dry_run_evidence_item_keys(
    dry_run_evidence_item: dict[str, object],
) -> bool:
    for expected_key in _DRY_RUN_EVIDENCE_ITEM_KEYS:
        if expected_key not in dry_run_evidence_item:
            return False
    for key in dry_run_evidence_item:
        if key not in _DRY_RUN_EVIDENCE_ITEM_KEYS:
            return False
    return True


def explain_local_noop_e2e_contract_build(
    *,
    run_id: str,
    local_noop_e2e_contract_id: str,
    contract_kind: str,
    mode: str,
    e2e_terminal_status: str,
    gate_input_ref: str,
    gate_input_buildable_marker: bool,
    local_noop_run_assembly_ref: str,
    local_noop_run_buildable_marker: bool,
    public_url_created: bool,
    public_url_is_null: bool,
    dry_run_evidence_items: tuple[dict[str, object], ...],
    required_dry_run_evidence_ids: tuple[str, ...],
    missing_dry_run_evidence_ids: tuple[str, ...],
    blocking_dry_run_evidence_ids: tuple[str, ...],
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    """Explain whether a caller-supplied local noop E2E contract is buildable."""

    reason_codes = []
    field_entries = []
    dry_run_evidence_item_violations = []

    if not _is_nonblank_string(run_id):
        _add_reason(reason_codes, "RUN_ID_MISSING")
        _add_field(field_entries, reason_code="RUN_ID_MISSING", field="run_id")

    if not _is_nonblank_string(local_noop_e2e_contract_id):
        _add_reason(reason_codes, "LOCAL_NOOP_E2E_CONTRACT_ID_MISSING")
        _add_field(
            field_entries,
            reason_code="LOCAL_NOOP_E2E_CONTRACT_ID_MISSING",
            field="local_noop_e2e_contract_id",
        )

    if contract_kind != _CONTRACT_KIND:
        _add_reason(
            reason_codes,
            "CONTRACT_KIND_NOT_LOCAL_NOOP_E2E_DRY_RUN_CONTRACT",
        )
        _add_field(
            field_entries,
            reason_code=(
                "CONTRACT_KIND_NOT_LOCAL_NOOP_E2E_DRY_RUN_CONTRACT"
            ),
            field="contract_kind",
        )

    if mode != _NOOP_MODE:
        _add_reason(reason_codes, "MODE_NOT_NOOP")
        _add_field(
            field_entries,
            reason_code="MODE_NOT_NOOP",
            field="mode",
        )

    if e2e_terminal_status == _PASS_PUBLISHED:
        _add_reason(reason_codes, "PASS_PUBLISHED_FORBIDDEN")
        _add_field(
            field_entries,
            reason_code="PASS_PUBLISHED_FORBIDDEN",
            field="e2e_terminal_status",
        )

    if e2e_terminal_status != _NOOP_COMPLETED:
        _add_reason(reason_codes, "E2E_TERMINAL_STATUS_NOT_NOOP_COMPLETED")
        _add_field(
            field_entries,
            reason_code="E2E_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
            field="e2e_terminal_status",
        )

    if not _is_nonblank_string(gate_input_ref):
        _add_reason(reason_codes, "GATE_INPUT_REF_MISSING")
        _add_field(
            field_entries,
            reason_code="GATE_INPUT_REF_MISSING",
            field="gate_input_ref",
        )

    if gate_input_buildable_marker is not True:
        _add_reason(reason_codes, "GATE_INPUT_BUILDABLE_MARKER_NOT_TRUE")
        _add_field(
            field_entries,
            reason_code="GATE_INPUT_BUILDABLE_MARKER_NOT_TRUE",
            field="gate_input_buildable_marker",
        )

    if not _is_nonblank_string(local_noop_run_assembly_ref):
        _add_reason(reason_codes, "LOCAL_NOOP_RUN_ASSEMBLY_REF_MISSING")
        _add_field(
            field_entries,
            reason_code="LOCAL_NOOP_RUN_ASSEMBLY_REF_MISSING",
            field="local_noop_run_assembly_ref",
        )

    if local_noop_run_buildable_marker is not True:
        _add_reason(reason_codes, "LOCAL_NOOP_RUN_BUILDABLE_MARKER_NOT_TRUE")
        _add_field(
            field_entries,
            reason_code="LOCAL_NOOP_RUN_BUILDABLE_MARKER_NOT_TRUE",
            field="local_noop_run_buildable_marker",
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
        not isinstance(dry_run_evidence_items, tuple)
        or dry_run_evidence_items == ()
    ):
        _add_reason(reason_codes, "DRY_RUN_EVIDENCE_ITEMS_MISSING")
        _add_field(
            field_entries,
            reason_code="DRY_RUN_EVIDENCE_ITEMS_MISSING",
            field="dry_run_evidence_items",
        )

    if not _is_nonempty_string_tuple(required_dry_run_evidence_ids):
        _add_reason(reason_codes, "REQUIRED_DRY_RUN_EVIDENCE_IDS_MISSING")
        _add_field(
            field_entries,
            reason_code="REQUIRED_DRY_RUN_EVIDENCE_IDS_MISSING",
            field="required_dry_run_evidence_ids",
        )

    if (
        not isinstance(missing_dry_run_evidence_ids, tuple)
        or missing_dry_run_evidence_ids != ()
    ):
        _add_reason(reason_codes, "MISSING_DRY_RUN_EVIDENCE_IDS_DECLARED")
        _add_field(
            field_entries,
            reason_code="MISSING_DRY_RUN_EVIDENCE_IDS_DECLARED",
            field="missing_dry_run_evidence_ids",
        )

    known_dry_run_evidence_ids = _known_dry_run_evidence_ids(
        dry_run_evidence_items
    )
    if not isinstance(blocking_dry_run_evidence_ids, tuple):
        _add_reason(reason_codes, "BLOCKING_DRY_RUN_EVIDENCE_ID_UNKNOWN")
        _add_field(
            field_entries,
            reason_code="BLOCKING_DRY_RUN_EVIDENCE_ID_UNKNOWN",
            field="blocking_dry_run_evidence_ids",
        )
    else:
        for blocking_dry_run_evidence_id in blocking_dry_run_evidence_ids:
            if (
                not _is_nonblank_string(blocking_dry_run_evidence_id)
                or blocking_dry_run_evidence_id
                not in known_dry_run_evidence_ids
            ):
                _add_reason(
                    reason_codes,
                    "BLOCKING_DRY_RUN_EVIDENCE_ID_UNKNOWN",
                )
                _add_field(
                    field_entries,
                    reason_code="BLOCKING_DRY_RUN_EVIDENCE_ID_UNKNOWN",
                    field="blocking_dry_run_evidence_ids",
                )
                break

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

    seen_dry_run_evidence_ids = ()
    if isinstance(dry_run_evidence_items, tuple):
        for dry_run_evidence_item_index, dry_run_evidence_item in enumerate(
            dry_run_evidence_items
        ):
            dry_run_evidence_id = _dry_run_evidence_id_from(
                dry_run_evidence_item
            )

            if not isinstance(dry_run_evidence_item, dict):
                _add_reason(reason_codes, "DRY_RUN_EVIDENCE_ITEM_NOT_DICT")
                _add_field(
                    field_entries,
                    reason_code="DRY_RUN_EVIDENCE_ITEM_NOT_DICT",
                    field=(
                        "dry_run_evidence_items"
                        f"[{dry_run_evidence_item_index}]"
                    ),
                )
                _add_dry_run_evidence_item_violation(
                    dry_run_evidence_item_violations,
                    dry_run_evidence_item_index=dry_run_evidence_item_index,
                    dry_run_evidence_id="",
                    reason_code="DRY_RUN_EVIDENCE_ITEM_NOT_DICT",
                    field="dry_run_evidence_items",
                )
                continue

            for key in dry_run_evidence_item:
                if key in _FORBIDDEN_DRY_RUN_EVIDENCE_ITEM_FIELDS:
                    _add_reason(
                        reason_codes,
                        "DRY_RUN_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT",
                    )
                    _add_field(
                        field_entries,
                        reason_code=(
                            "DRY_RUN_EVIDENCE_ITEM_"
                            "FORBIDDEN_RAW_FIELD_PRESENT"
                        ),
                        field=(
                            "dry_run_evidence_items"
                            f"[{dry_run_evidence_item_index}].{key}"
                        ),
                    )
                    _add_dry_run_evidence_item_violation(
                        dry_run_evidence_item_violations,
                        dry_run_evidence_item_index=(
                            dry_run_evidence_item_index
                        ),
                        dry_run_evidence_id=dry_run_evidence_id,
                        reason_code=(
                            "DRY_RUN_EVIDENCE_ITEM_"
                            "FORBIDDEN_RAW_FIELD_PRESENT"
                        ),
                        field=key,
                    )

            if not _has_exact_dry_run_evidence_item_keys(
                dry_run_evidence_item
            ):
                _add_reason(
                    reason_codes,
                    "DRY_RUN_EVIDENCE_ITEM_KEYS_INVALID",
                )
                _add_field(
                    field_entries,
                    reason_code="DRY_RUN_EVIDENCE_ITEM_KEYS_INVALID",
                    field=(
                        "dry_run_evidence_items"
                        f"[{dry_run_evidence_item_index}].keys"
                    ),
                )
                _add_dry_run_evidence_item_violation(
                    dry_run_evidence_item_violations,
                    dry_run_evidence_item_index=(
                        dry_run_evidence_item_index
                    ),
                    dry_run_evidence_id=dry_run_evidence_id,
                    reason_code="DRY_RUN_EVIDENCE_ITEM_KEYS_INVALID",
                    field="keys",
                )

            for field, missing_reason_code in (
                _DRY_RUN_EVIDENCE_ITEM_STRING_FIELDS
            ):
                if not _is_nonblank_string(dry_run_evidence_item.get(field)):
                    _add_reason(reason_codes, missing_reason_code)
                    _add_field(
                        field_entries,
                        reason_code=missing_reason_code,
                        field=(
                            "dry_run_evidence_items"
                            f"[{dry_run_evidence_item_index}].{field}"
                        ),
                    )
                    _add_dry_run_evidence_item_violation(
                        dry_run_evidence_item_violations,
                        dry_run_evidence_item_index=(
                            dry_run_evidence_item_index
                        ),
                        dry_run_evidence_id=dry_run_evidence_id,
                        reason_code=missing_reason_code,
                        field=field,
                    )

            if not _is_nonempty_string_tuple(
                dry_run_evidence_item.get("evidence_refs")
            ):
                _add_reason(reason_codes, "DRY_RUN_EVIDENCE_REFS_MISSING")
                _add_field(
                    field_entries,
                    reason_code="DRY_RUN_EVIDENCE_REFS_MISSING",
                    field=(
                        "dry_run_evidence_items"
                        f"[{dry_run_evidence_item_index}].evidence_refs"
                    ),
                )
                _add_dry_run_evidence_item_violation(
                    dry_run_evidence_item_violations,
                    dry_run_evidence_item_index=(
                        dry_run_evidence_item_index
                    ),
                    dry_run_evidence_id=dry_run_evidence_id,
                    reason_code="DRY_RUN_EVIDENCE_REFS_MISSING",
                    field="evidence_refs",
                )

            if _is_nonblank_string(dry_run_evidence_id):
                if dry_run_evidence_id in seen_dry_run_evidence_ids:
                    _add_reason(
                        reason_codes,
                        "DRY_RUN_EVIDENCE_ID_DUPLICATE",
                    )
                    _add_field(
                        field_entries,
                        reason_code="DRY_RUN_EVIDENCE_ID_DUPLICATE",
                        field=(
                            "dry_run_evidence_items"
                            f"[{dry_run_evidence_item_index}]."
                            "dry_run_evidence_id"
                        ),
                    )
                    _add_dry_run_evidence_item_violation(
                        dry_run_evidence_item_violations,
                        dry_run_evidence_item_index=(
                            dry_run_evidence_item_index
                        ),
                        dry_run_evidence_id=dry_run_evidence_id,
                        reason_code="DRY_RUN_EVIDENCE_ID_DUPLICATE",
                        field="dry_run_evidence_id",
                    )
                else:
                    seen_dry_run_evidence_ids = (
                        seen_dry_run_evidence_ids
                        + (dry_run_evidence_id,)
                    )

                if (
                    _is_nonempty_string_tuple(required_dry_run_evidence_ids)
                    and dry_run_evidence_id
                    not in required_dry_run_evidence_ids
                ):
                    _add_reason(
                        reason_codes,
                        "DRY_RUN_EVIDENCE_ID_NOT_REQUIRED",
                    )
                    _add_field(
                        field_entries,
                        reason_code="DRY_RUN_EVIDENCE_ID_NOT_REQUIRED",
                        field=(
                            "dry_run_evidence_items"
                            f"[{dry_run_evidence_item_index}]."
                            "dry_run_evidence_id"
                        ),
                    )
                    _add_dry_run_evidence_item_violation(
                        dry_run_evidence_item_violations,
                        dry_run_evidence_item_index=(
                            dry_run_evidence_item_index
                        ),
                        dry_run_evidence_id=dry_run_evidence_id,
                        reason_code="DRY_RUN_EVIDENCE_ID_NOT_REQUIRED",
                        field="dry_run_evidence_id",
                    )

    if _is_nonempty_string_tuple(required_dry_run_evidence_ids):
        for required_dry_run_evidence_id in required_dry_run_evidence_ids:
            if required_dry_run_evidence_id not in known_dry_run_evidence_ids:
                _add_reason(
                    reason_codes,
                    "REQUIRED_DRY_RUN_EVIDENCE_MISSING",
                )
                _add_field(
                    field_entries,
                    reason_code="REQUIRED_DRY_RUN_EVIDENCE_MISSING",
                    field=(
                        "required_dry_run_evidence_ids."
                        f"{required_dry_run_evidence_id}"
                    ),
                )

    contract_violations = _ordered_reason_codes(tuple(reason_codes))
    missing_or_invalid_fields = _ordered_fields(tuple(field_entries))
    ordered_dry_run_evidence_item_violations = (
        _ordered_dry_run_evidence_item_violations(
            tuple(dry_run_evidence_item_violations)
        )
    )
    buildable = contract_violations == ()
    reason_code = "LOCAL_NOOP_E2E_CONTRACT_BUILDABLE"
    if not buildable:
        reason_code = contract_violations[0]

    reason = "Local noop E2E dry-run contract is buildable."
    if not buildable:
        reason = (
            f"{reason_code} prevents local noop E2E dry-run "
            "contract buildability."
        )

    return {
        "buildable": buildable,
        "reason_code": reason_code,
        "reason": reason,
        "source": {
            "gate_input_ref": _safe_string(gate_input_ref),
            "gate_input_buildable_marker": gate_input_buildable_marker,
            "local_noop_run_assembly_ref": _safe_string(
                local_noop_run_assembly_ref
            ),
            "local_noop_run_buildable_marker": (
                local_noop_run_buildable_marker
            ),
            "mode": _safe_string(mode),
            "e2e_terminal_status": _safe_terminal_status(
                e2e_terminal_status
            ),
            "public_url": None,
            "public_url_created": public_url_created,
            "source_of_truth": _safe_string_tuple(source_of_truth),
        },
        "local_noop_e2e_contract": {
            "run_id": _safe_string(run_id),
            "local_noop_e2e_contract_id": _safe_string(
                local_noop_e2e_contract_id
            ),
            "contract_kind": _safe_string(contract_kind),
            "mode": _safe_string(mode),
            "e2e_terminal_status": _safe_terminal_status(
                e2e_terminal_status
            ),
            "gate_input_ref": _safe_string(gate_input_ref),
            "gate_input_buildable_marker": gate_input_buildable_marker,
            "local_noop_run_assembly_ref": _safe_string(
                local_noop_run_assembly_ref
            ),
            "local_noop_run_buildable_marker": (
                local_noop_run_buildable_marker
            ),
            "public_url": None,
            "public_url_created": public_url_created,
            "dry_run_evidence_items": _safe_dry_run_evidence_items(
                dry_run_evidence_items
            ),
            "required_dry_run_evidence_ids": _safe_string_tuple(
                required_dry_run_evidence_ids
            ),
            "missing_dry_run_evidence_ids": _safe_string_tuple(
                missing_dry_run_evidence_ids
            ),
            "blocking_dry_run_evidence_ids": _safe_string_tuple(
                blocking_dry_run_evidence_ids
            ),
            "created_at": _safe_string(created_at),
            "timestamp_policy": _safe_string(timestamp_policy),
            "source_of_truth": _safe_string_tuple(source_of_truth),
            "notes": _safe_string_tuple(notes),
        },
        "contract_violations": contract_violations,
        "missing_or_invalid_fields": missing_or_invalid_fields,
        "dry_run_evidence_item_violations": (
            ordered_dry_run_evidence_item_violations
        ),
        "invariant_refs": _INVARIANT_REFS,
    }


def is_local_noop_e2e_contract_buildable(
    *,
    run_id: str,
    local_noop_e2e_contract_id: str,
    contract_kind: str,
    mode: str,
    e2e_terminal_status: str,
    gate_input_ref: str,
    gate_input_buildable_marker: bool,
    local_noop_run_assembly_ref: str,
    local_noop_run_buildable_marker: bool,
    public_url_created: bool,
    public_url_is_null: bool,
    dry_run_evidence_items: tuple[dict[str, object], ...],
    required_dry_run_evidence_ids: tuple[str, ...],
    missing_dry_run_evidence_ids: tuple[str, ...],
    blocking_dry_run_evidence_ids: tuple[str, ...],
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> bool:
    """Return whether the caller-supplied local noop E2E contract is buildable."""

    return bool(
        explain_local_noop_e2e_contract_build(
            run_id=run_id,
            local_noop_e2e_contract_id=local_noop_e2e_contract_id,
            contract_kind=contract_kind,
            mode=mode,
            e2e_terminal_status=e2e_terminal_status,
            gate_input_ref=gate_input_ref,
            gate_input_buildable_marker=gate_input_buildable_marker,
            local_noop_run_assembly_ref=local_noop_run_assembly_ref,
            local_noop_run_buildable_marker=local_noop_run_buildable_marker,
            public_url_created=public_url_created,
            public_url_is_null=public_url_is_null,
            dry_run_evidence_items=dry_run_evidence_items,
            required_dry_run_evidence_ids=required_dry_run_evidence_ids,
            missing_dry_run_evidence_ids=missing_dry_run_evidence_ids,
            blocking_dry_run_evidence_ids=blocking_dry_run_evidence_ids,
            created_at=created_at,
            timestamp_policy=timestamp_policy,
            source_of_truth=source_of_truth,
            notes=notes,
        )["buildable"]
    )
