"""Build pure local noop run assembly buildability explanations."""

from typing import Final


REASON_CODES: Final[tuple[str, ...]] = (
    "LOCAL_NOOP_RUN_ASSEMBLY_BUILDABLE",
    "RUN_ID_MISSING",
    "LOCAL_NOOP_RUN_ASSEMBLY_ID_MISSING",
    "ASSEMBLY_KIND_NOT_LOCAL_NOOP_RUN",
    "MODE_NOT_NOOP",
    "COMPLETION_STATUS_NOT_NOOP_COMPLETED",
    "PASS_PUBLISHED_FORBIDDEN",
    "GATE_INPUT_REF_MISSING",
    "GATE_INPUT_STATUS_MISSING",
    "PUBLIC_URL_IS_NULL_NOT_TRUE",
    "PUBLIC_URL_CREATED_NOT_FALSE",
    "COMPLETION_EVIDENCE_ITEMS_MISSING",
    "REQUIRED_COMPLETION_EVIDENCE_IDS_MISSING",
    "MISSING_COMPLETION_EVIDENCE_IDS_DECLARED",
    "BLOCKING_COMPLETION_EVIDENCE_ID_UNKNOWN",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "COMPLETION_EVIDENCE_ITEM_NOT_DICT",
    "COMPLETION_EVIDENCE_ITEM_KEYS_INVALID",
    "COMPLETION_EVIDENCE_ID_MISSING",
    "COMPLETION_EVIDENCE_ROLE_MISSING",
    "COMPLETION_EVIDENCE_ARTIFACT_REF_MISSING",
    "COMPLETION_EVIDENCE_ARTIFACT_KIND_MISSING",
    "COMPLETION_EVIDENCE_STATUS_MISSING",
    "COMPLETION_EVIDENCE_PRODUCER_REF_MISSING",
    "COMPLETION_EVIDENCE_REFS_MISSING",
    "COMPLETION_EVIDENCE_ID_DUPLICATE",
    "COMPLETION_EVIDENCE_ID_NOT_REQUIRED",
    "REQUIRED_COMPLETION_EVIDENCE_MISSING",
    "COMPLETION_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT",
)

LOCAL_NOOP_RUN_ASSEMBLY_BUILD_REASON_CODES: Final[tuple[str, ...]] = (
    REASON_CODES
)

REASON_PRIORITY: Final[tuple[str, ...]] = (
    "RUN_ID_MISSING",
    "LOCAL_NOOP_RUN_ASSEMBLY_ID_MISSING",
    "ASSEMBLY_KIND_NOT_LOCAL_NOOP_RUN",
    "MODE_NOT_NOOP",
    "PASS_PUBLISHED_FORBIDDEN",
    "COMPLETION_STATUS_NOT_NOOP_COMPLETED",
    "GATE_INPUT_REF_MISSING",
    "GATE_INPUT_STATUS_MISSING",
    "PUBLIC_URL_IS_NULL_NOT_TRUE",
    "PUBLIC_URL_CREATED_NOT_FALSE",
    "COMPLETION_EVIDENCE_ITEMS_MISSING",
    "REQUIRED_COMPLETION_EVIDENCE_IDS_MISSING",
    "MISSING_COMPLETION_EVIDENCE_IDS_DECLARED",
    "BLOCKING_COMPLETION_EVIDENCE_ID_UNKNOWN",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "COMPLETION_EVIDENCE_ITEM_NOT_DICT",
    "COMPLETION_EVIDENCE_ITEM_KEYS_INVALID",
    "COMPLETION_EVIDENCE_ID_MISSING",
    "COMPLETION_EVIDENCE_ROLE_MISSING",
    "COMPLETION_EVIDENCE_ARTIFACT_REF_MISSING",
    "COMPLETION_EVIDENCE_ARTIFACT_KIND_MISSING",
    "COMPLETION_EVIDENCE_STATUS_MISSING",
    "COMPLETION_EVIDENCE_PRODUCER_REF_MISSING",
    "COMPLETION_EVIDENCE_REFS_MISSING",
    "COMPLETION_EVIDENCE_ID_DUPLICATE",
    "COMPLETION_EVIDENCE_ID_NOT_REQUIRED",
    "REQUIRED_COMPLETION_EVIDENCE_MISSING",
    "COMPLETION_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT",
    "LOCAL_NOOP_RUN_ASSEMBLY_BUILDABLE",
)

_LOCAL_NOOP_ASSEMBLY_KIND: Final[str] = "local_noop_run"
_NOOP_MODE: Final[str] = "noop"
_NOOP_COMPLETED: Final[str] = "NOOP_COMPLETED"
_PASS_PUBLISHED: Final[str] = "PASS_PUBLISHED"

_COMPLETION_EVIDENCE_ITEM_KEYS: Final[tuple[str, ...]] = (
    "completion_evidence_id",
    "completion_evidence_role",
    "artifact_ref",
    "artifact_kind",
    "completion_evidence_status",
    "producer_ref",
    "evidence_refs",
    "notes",
)

_COMPLETION_EVIDENCE_ITEM_STRING_FIELDS: Final[
    tuple[tuple[str, str], ...]
] = (
    ("completion_evidence_id", "COMPLETION_EVIDENCE_ID_MISSING"),
    ("completion_evidence_role", "COMPLETION_EVIDENCE_ROLE_MISSING"),
    ("artifact_ref", "COMPLETION_EVIDENCE_ARTIFACT_REF_MISSING"),
    ("artifact_kind", "COMPLETION_EVIDENCE_ARTIFACT_KIND_MISSING"),
    (
        "completion_evidence_status",
        "COMPLETION_EVIDENCE_STATUS_MISSING",
    ),
    ("producer_ref", "COMPLETION_EVIDENCE_PRODUCER_REF_MISSING"),
)

_FORBIDDEN_COMPLETION_EVIDENCE_ITEM_FIELDS: Final[tuple[str, ...]] = (
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
    "gate_result",
    "publish_result",
    "notification_result",
    "ledger_write_result",
    "transition_result",
    "runtime_result",
    "adapter_result",
    "noop_completion_result",
    "should_fetch",
    "should_read_reader",
    "should_read_training_report",
    "should_read_validator_result",
    "should_read_rubric_review",
    "should_read_audit_review",
    "should_read_gate_input",
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
    "reader_read",
    "training_report_read",
    "validator_result_read",
    "rubric_review_read",
    "audit_review_read",
    "gate_input_read",
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
    "published",
    "notified",
    "ledger_written",
    "public_url_created_executed",
)

_INVARIANT_REFS: Final[tuple[str, ...]] = (
    "local_noop_run_assembly_builder_only",
    "builder_not_reader_reader",
    "builder_not_training_report_reader",
    "builder_not_validator_result_reader",
    "builder_not_rubric_review_reader",
    "builder_not_audit_review_reader",
    "builder_not_gate_input_reader",
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
    "builder_not_publisher",
    "builder_not_ledger_writer",
    "builder_not_notifier",
    "completion_evidence_items_are_caller_supplied",
    "completion_evidence_status_is_caller_supplied",
    "gate_input_ref_is_caller_supplied",
    "gate_input_status_is_caller_supplied",
    "gate_input_ref_opaque",
    "artifact_refs_opaque",
    "evidence_refs_opaque",
    "local_noop_run_governance_evidence_bundle",
    "local_noop_run_not_gate_decision",
    "local_noop_run_not_publish_artifact",
    "local_noop_run_not_public_candidate",
    "mode_noop_required",
    "public_url_must_be_null",
    "public_url_created_must_be_false",
    "completion_status_must_be_noop_completed",
    "noop_completed_not_pass_published",
    "pass_published_forbidden",
    "mode_noop_not_publish",
    "candidate_artifact_not_public_url",
    "gate_input_status_not_quality_pass",
    "gate_input_status_not_gate_pass",
    "gate_input_status_not_publish_allowed",
    "completion_evidence_status_not_quality_pass",
    "completion_evidence_status_not_gate_pass",
    "completion_evidence_status_not_publish_allowed",
    "buildable_not_quality_pass",
    "buildable_not_eval_pass",
    "buildable_not_audit_pass",
    "buildable_not_gate_pass",
    "buildable_not_publish_allowed",
    "buildable_not_review_blocked",
    "buildable_not_pass_published",
    "buildable_not_public_url_created",
    "blocking_completion_evidence_ids_are_evidence_only",
    "blocking_completion_evidence_ids_do_not_execute_gate",
    "blocking_completion_evidence_ids_do_not_execute_noop_completion",
    "no_reader_read",
    "no_training_report_read",
    "no_validator_result_read",
    "no_rubric_review_read",
    "no_audit_review_read",
    "no_gate_input_read",
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


def _safe_completion_status(value: object) -> str:
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


def _safe_completion_evidence_item(
    completion_evidence_item: object,
) -> dict[str, object]:
    if not isinstance(completion_evidence_item, dict):
        return {
            "completion_evidence_id": "",
            "completion_evidence_role": "",
            "artifact_ref": "",
            "artifact_kind": "",
            "completion_evidence_status": "",
            "producer_ref": "",
            "evidence_refs": (),
            "notes": (),
        }

    return {
        "completion_evidence_id": _safe_string(
            completion_evidence_item.get("completion_evidence_id")
        ),
        "completion_evidence_role": _safe_string(
            completion_evidence_item.get("completion_evidence_role")
        ),
        "artifact_ref": _safe_string(
            completion_evidence_item.get("artifact_ref")
        ),
        "artifact_kind": _safe_string(
            completion_evidence_item.get("artifact_kind")
        ),
        "completion_evidence_status": _safe_string(
            completion_evidence_item.get("completion_evidence_status")
        ),
        "producer_ref": _safe_string(
            completion_evidence_item.get("producer_ref")
        ),
        "evidence_refs": _safe_string_tuple(
            completion_evidence_item.get("evidence_refs")
        ),
        "notes": _safe_string_tuple(completion_evidence_item.get("notes")),
    }


def _safe_completion_evidence_items(
    value: object,
) -> tuple[dict[str, object], ...]:
    if not isinstance(value, tuple):
        return ()

    safe_items = ()
    for completion_evidence_item in value:
        safe_items = safe_items + (
            _safe_completion_evidence_item(completion_evidence_item),
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


def _add_completion_evidence_item_violation(
    completion_evidence_item_violations: list[dict[str, object]],
    *,
    completion_evidence_item_index: int,
    completion_evidence_id: str,
    reason_code: str,
    field: str,
) -> None:
    completion_evidence_item_violations.append(
        {
            "completion_evidence_item_index": (
                completion_evidence_item_index
            ),
            "completion_evidence_id": completion_evidence_id,
            "reason_code": reason_code,
            "field": field,
        }
    )


def _ordered_reason_codes(reason_codes: tuple[str, ...]) -> tuple[str, ...]:
    ordered = ()
    for reason_code in REASON_PRIORITY:
        if reason_code == "LOCAL_NOOP_RUN_ASSEMBLY_BUILDABLE":
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


def _ordered_completion_evidence_item_violations(
    completion_evidence_item_violations: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    return tuple(
        sorted(
            completion_evidence_item_violations,
            key=lambda item: (
                _reason_rank(_safe_string(item.get("reason_code"))),
                item.get("completion_evidence_item_index"),
                _safe_string(item.get("field")),
            ),
        )
    )


def _completion_evidence_id_from(completion_evidence_item: object) -> str:
    if not isinstance(completion_evidence_item, dict):
        return ""
    return _safe_string(completion_evidence_item.get("completion_evidence_id"))


def _known_completion_evidence_ids(
    completion_evidence_items: object,
) -> tuple[str, ...]:
    if not isinstance(completion_evidence_items, tuple):
        return ()

    completion_evidence_ids = ()
    for completion_evidence_item in completion_evidence_items:
        completion_evidence_id = _completion_evidence_id_from(
            completion_evidence_item
        )
        if _is_nonblank_string(completion_evidence_id):
            completion_evidence_ids = (
                completion_evidence_ids + (completion_evidence_id,)
            )
    return completion_evidence_ids


def _has_exact_completion_evidence_item_keys(
    completion_evidence_item: dict[str, object],
) -> bool:
    for expected_key in _COMPLETION_EVIDENCE_ITEM_KEYS:
        if expected_key not in completion_evidence_item:
            return False
    for key in completion_evidence_item:
        if key not in _COMPLETION_EVIDENCE_ITEM_KEYS:
            return False
    return True


def explain_local_noop_run_assembly_build(
    *,
    run_id: str,
    local_noop_run_assembly_id: str,
    assembly_kind: str,
    mode: str,
    completion_status: str,
    gate_input_ref: str,
    gate_input_status: str,
    public_url_created: bool,
    public_url_is_null: bool,
    completion_evidence_items: tuple[dict[str, object], ...],
    required_completion_evidence_ids: tuple[str, ...],
    missing_completion_evidence_ids: tuple[str, ...],
    blocking_completion_evidence_ids: tuple[str, ...],
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    """Explain whether a caller-supplied local noop assembly is buildable."""

    reason_codes = []
    field_entries = []
    completion_evidence_item_violations = []

    if not _is_nonblank_string(run_id):
        _add_reason(reason_codes, "RUN_ID_MISSING")
        _add_field(field_entries, reason_code="RUN_ID_MISSING", field="run_id")

    if not _is_nonblank_string(local_noop_run_assembly_id):
        _add_reason(reason_codes, "LOCAL_NOOP_RUN_ASSEMBLY_ID_MISSING")
        _add_field(
            field_entries,
            reason_code="LOCAL_NOOP_RUN_ASSEMBLY_ID_MISSING",
            field="local_noop_run_assembly_id",
        )

    if assembly_kind != _LOCAL_NOOP_ASSEMBLY_KIND:
        _add_reason(reason_codes, "ASSEMBLY_KIND_NOT_LOCAL_NOOP_RUN")
        _add_field(
            field_entries,
            reason_code="ASSEMBLY_KIND_NOT_LOCAL_NOOP_RUN",
            field="assembly_kind",
        )

    if mode != _NOOP_MODE:
        _add_reason(reason_codes, "MODE_NOT_NOOP")
        _add_field(
            field_entries,
            reason_code="MODE_NOT_NOOP",
            field="mode",
        )

    if completion_status == _PASS_PUBLISHED:
        _add_reason(reason_codes, "PASS_PUBLISHED_FORBIDDEN")
        _add_field(
            field_entries,
            reason_code="PASS_PUBLISHED_FORBIDDEN",
            field="completion_status",
        )

    if completion_status != _NOOP_COMPLETED:
        _add_reason(reason_codes, "COMPLETION_STATUS_NOT_NOOP_COMPLETED")
        _add_field(
            field_entries,
            reason_code="COMPLETION_STATUS_NOT_NOOP_COMPLETED",
            field="completion_status",
        )

    if not _is_nonblank_string(gate_input_ref):
        _add_reason(reason_codes, "GATE_INPUT_REF_MISSING")
        _add_field(
            field_entries,
            reason_code="GATE_INPUT_REF_MISSING",
            field="gate_input_ref",
        )

    if not _is_nonblank_string(gate_input_status):
        _add_reason(reason_codes, "GATE_INPUT_STATUS_MISSING")
        _add_field(
            field_entries,
            reason_code="GATE_INPUT_STATUS_MISSING",
            field="gate_input_status",
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
        not isinstance(completion_evidence_items, tuple)
        or completion_evidence_items == ()
    ):
        _add_reason(reason_codes, "COMPLETION_EVIDENCE_ITEMS_MISSING")
        _add_field(
            field_entries,
            reason_code="COMPLETION_EVIDENCE_ITEMS_MISSING",
            field="completion_evidence_items",
        )

    if not _is_nonempty_string_tuple(required_completion_evidence_ids):
        _add_reason(
            reason_codes,
            "REQUIRED_COMPLETION_EVIDENCE_IDS_MISSING",
        )
        _add_field(
            field_entries,
            reason_code="REQUIRED_COMPLETION_EVIDENCE_IDS_MISSING",
            field="required_completion_evidence_ids",
        )

    if (
        not isinstance(missing_completion_evidence_ids, tuple)
        or missing_completion_evidence_ids != ()
    ):
        _add_reason(
            reason_codes,
            "MISSING_COMPLETION_EVIDENCE_IDS_DECLARED",
        )
        _add_field(
            field_entries,
            reason_code="MISSING_COMPLETION_EVIDENCE_IDS_DECLARED",
            field="missing_completion_evidence_ids",
        )

    known_completion_evidence_ids = _known_completion_evidence_ids(
        completion_evidence_items
    )
    if not isinstance(blocking_completion_evidence_ids, tuple):
        _add_reason(
            reason_codes,
            "BLOCKING_COMPLETION_EVIDENCE_ID_UNKNOWN",
        )
        _add_field(
            field_entries,
            reason_code="BLOCKING_COMPLETION_EVIDENCE_ID_UNKNOWN",
            field="blocking_completion_evidence_ids",
        )
    else:
        for blocking_completion_evidence_id in (
            blocking_completion_evidence_ids
        ):
            if (
                not _is_nonblank_string(blocking_completion_evidence_id)
                or blocking_completion_evidence_id
                not in known_completion_evidence_ids
            ):
                _add_reason(
                    reason_codes,
                    "BLOCKING_COMPLETION_EVIDENCE_ID_UNKNOWN",
                )
                _add_field(
                    field_entries,
                    reason_code="BLOCKING_COMPLETION_EVIDENCE_ID_UNKNOWN",
                    field="blocking_completion_evidence_ids",
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

    seen_completion_evidence_ids = ()
    if isinstance(completion_evidence_items, tuple):
        for completion_evidence_item_index, completion_evidence_item in (
            enumerate(completion_evidence_items)
        ):
            completion_evidence_id = _completion_evidence_id_from(
                completion_evidence_item
            )

            if not isinstance(completion_evidence_item, dict):
                _add_reason(
                    reason_codes,
                    "COMPLETION_EVIDENCE_ITEM_NOT_DICT",
                )
                _add_field(
                    field_entries,
                    reason_code="COMPLETION_EVIDENCE_ITEM_NOT_DICT",
                    field=(
                        "completion_evidence_items"
                        f"[{completion_evidence_item_index}]"
                    ),
                )
                _add_completion_evidence_item_violation(
                    completion_evidence_item_violations,
                    completion_evidence_item_index=(
                        completion_evidence_item_index
                    ),
                    completion_evidence_id="",
                    reason_code="COMPLETION_EVIDENCE_ITEM_NOT_DICT",
                    field="completion_evidence_items",
                )
                continue

            for key in completion_evidence_item:
                if key in _FORBIDDEN_COMPLETION_EVIDENCE_ITEM_FIELDS:
                    _add_reason(
                        reason_codes,
                        "COMPLETION_EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT",
                    )
                    _add_field(
                        field_entries,
                        reason_code=(
                            "COMPLETION_EVIDENCE_ITEM_"
                            "FORBIDDEN_RAW_FIELD_PRESENT"
                        ),
                        field=(
                            "completion_evidence_items"
                            f"[{completion_evidence_item_index}].{key}"
                        ),
                    )
                    _add_completion_evidence_item_violation(
                        completion_evidence_item_violations,
                        completion_evidence_item_index=(
                            completion_evidence_item_index
                        ),
                        completion_evidence_id=completion_evidence_id,
                        reason_code=(
                            "COMPLETION_EVIDENCE_ITEM_"
                            "FORBIDDEN_RAW_FIELD_PRESENT"
                        ),
                        field=key,
                    )

            if not _has_exact_completion_evidence_item_keys(
                completion_evidence_item
            ):
                _add_reason(
                    reason_codes,
                    "COMPLETION_EVIDENCE_ITEM_KEYS_INVALID",
                )
                _add_field(
                    field_entries,
                    reason_code="COMPLETION_EVIDENCE_ITEM_KEYS_INVALID",
                    field=(
                        "completion_evidence_items"
                        f"[{completion_evidence_item_index}].keys"
                    ),
                )
                _add_completion_evidence_item_violation(
                    completion_evidence_item_violations,
                    completion_evidence_item_index=(
                        completion_evidence_item_index
                    ),
                    completion_evidence_id=completion_evidence_id,
                    reason_code="COMPLETION_EVIDENCE_ITEM_KEYS_INVALID",
                    field="keys",
                )

            for field, missing_reason_code in (
                _COMPLETION_EVIDENCE_ITEM_STRING_FIELDS
            ):
                if not _is_nonblank_string(
                    completion_evidence_item.get(field)
                ):
                    _add_reason(reason_codes, missing_reason_code)
                    _add_field(
                        field_entries,
                        reason_code=missing_reason_code,
                        field=(
                            "completion_evidence_items"
                            f"[{completion_evidence_item_index}].{field}"
                        ),
                    )
                    _add_completion_evidence_item_violation(
                        completion_evidence_item_violations,
                        completion_evidence_item_index=(
                            completion_evidence_item_index
                        ),
                        completion_evidence_id=completion_evidence_id,
                        reason_code=missing_reason_code,
                        field=field,
                    )

            if not _is_nonempty_string_tuple(
                completion_evidence_item.get("evidence_refs")
            ):
                _add_reason(
                    reason_codes,
                    "COMPLETION_EVIDENCE_REFS_MISSING",
                )
                _add_field(
                    field_entries,
                    reason_code="COMPLETION_EVIDENCE_REFS_MISSING",
                    field=(
                        "completion_evidence_items"
                        f"[{completion_evidence_item_index}].evidence_refs"
                    ),
                )
                _add_completion_evidence_item_violation(
                    completion_evidence_item_violations,
                    completion_evidence_item_index=(
                        completion_evidence_item_index
                    ),
                    completion_evidence_id=completion_evidence_id,
                    reason_code="COMPLETION_EVIDENCE_REFS_MISSING",
                    field="evidence_refs",
                )

            if _is_nonblank_string(completion_evidence_id):
                if completion_evidence_id in seen_completion_evidence_ids:
                    _add_reason(
                        reason_codes,
                        "COMPLETION_EVIDENCE_ID_DUPLICATE",
                    )
                    _add_field(
                        field_entries,
                        reason_code="COMPLETION_EVIDENCE_ID_DUPLICATE",
                        field=(
                            "completion_evidence_items"
                            f"[{completion_evidence_item_index}]."
                            "completion_evidence_id"
                        ),
                    )
                    _add_completion_evidence_item_violation(
                        completion_evidence_item_violations,
                        completion_evidence_item_index=(
                            completion_evidence_item_index
                        ),
                        completion_evidence_id=completion_evidence_id,
                        reason_code="COMPLETION_EVIDENCE_ID_DUPLICATE",
                        field="completion_evidence_id",
                    )
                else:
                    seen_completion_evidence_ids = (
                        seen_completion_evidence_ids
                        + (completion_evidence_id,)
                    )

                if (
                    _is_nonempty_string_tuple(required_completion_evidence_ids)
                    and completion_evidence_id
                    not in required_completion_evidence_ids
                ):
                    _add_reason(
                        reason_codes,
                        "COMPLETION_EVIDENCE_ID_NOT_REQUIRED",
                    )
                    _add_field(
                        field_entries,
                        reason_code="COMPLETION_EVIDENCE_ID_NOT_REQUIRED",
                        field=(
                            "completion_evidence_items"
                            f"[{completion_evidence_item_index}]."
                            "completion_evidence_id"
                        ),
                    )
                    _add_completion_evidence_item_violation(
                        completion_evidence_item_violations,
                        completion_evidence_item_index=(
                            completion_evidence_item_index
                        ),
                        completion_evidence_id=completion_evidence_id,
                        reason_code="COMPLETION_EVIDENCE_ID_NOT_REQUIRED",
                        field="completion_evidence_id",
                    )

    if _is_nonempty_string_tuple(required_completion_evidence_ids):
        for required_completion_evidence_id in (
            required_completion_evidence_ids
        ):
            if (
                required_completion_evidence_id
                not in known_completion_evidence_ids
            ):
                _add_reason(
                    reason_codes,
                    "REQUIRED_COMPLETION_EVIDENCE_MISSING",
                )
                _add_field(
                    field_entries,
                    reason_code="REQUIRED_COMPLETION_EVIDENCE_MISSING",
                    field=(
                        "required_completion_evidence_ids."
                        f"{required_completion_evidence_id}"
                    ),
                )

    assembly_violations = _ordered_reason_codes(tuple(reason_codes))
    missing_or_invalid_fields = _ordered_fields(tuple(field_entries))
    ordered_completion_evidence_item_violations = (
        _ordered_completion_evidence_item_violations(
            tuple(completion_evidence_item_violations)
        )
    )
    buildable = assembly_violations == ()
    reason_code = "LOCAL_NOOP_RUN_ASSEMBLY_BUILDABLE"
    if not buildable:
        reason_code = assembly_violations[0]

    reason = "Local noop run assembly is buildable."
    if not buildable:
        reason = (
            f"{reason_code} prevents local noop run assembly buildability."
        )

    return {
        "buildable": buildable,
        "reason_code": reason_code,
        "reason": reason,
        "source": {
            "gate_input_ref": _safe_string(gate_input_ref),
            "gate_input_status": _safe_string(gate_input_status),
            "mode": _safe_string(mode),
            "completion_status": _safe_completion_status(completion_status),
            "public_url": None,
            "public_url_created": public_url_created,
            "source_of_truth": _safe_string_tuple(source_of_truth),
        },
        "local_noop_run_assembly": {
            "run_id": _safe_string(run_id),
            "local_noop_run_assembly_id": _safe_string(
                local_noop_run_assembly_id
            ),
            "assembly_kind": _safe_string(assembly_kind),
            "mode": _safe_string(mode),
            "completion_status": _safe_completion_status(completion_status),
            "gate_input_ref": _safe_string(gate_input_ref),
            "gate_input_status": _safe_string(gate_input_status),
            "public_url": None,
            "public_url_created": public_url_created,
            "completion_evidence_items": _safe_completion_evidence_items(
                completion_evidence_items
            ),
            "required_completion_evidence_ids": _safe_string_tuple(
                required_completion_evidence_ids
            ),
            "missing_completion_evidence_ids": _safe_string_tuple(
                missing_completion_evidence_ids
            ),
            "blocking_completion_evidence_ids": _safe_string_tuple(
                blocking_completion_evidence_ids
            ),
            "created_at": _safe_string(created_at),
            "timestamp_policy": _safe_string(timestamp_policy),
            "source_of_truth": _safe_string_tuple(source_of_truth),
            "notes": _safe_string_tuple(notes),
        },
        "assembly_violations": assembly_violations,
        "missing_or_invalid_fields": missing_or_invalid_fields,
        "completion_evidence_item_violations": (
            ordered_completion_evidence_item_violations
        ),
        "invariant_refs": _INVARIANT_REFS,
    }


def is_local_noop_run_assembly_buildable(
    *,
    run_id: str,
    local_noop_run_assembly_id: str,
    assembly_kind: str,
    mode: str,
    completion_status: str,
    gate_input_ref: str,
    gate_input_status: str,
    public_url_created: bool,
    public_url_is_null: bool,
    completion_evidence_items: tuple[dict[str, object], ...],
    required_completion_evidence_ids: tuple[str, ...],
    missing_completion_evidence_ids: tuple[str, ...],
    blocking_completion_evidence_ids: tuple[str, ...],
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> bool:
    """Return whether the caller-supplied local noop assembly is buildable."""

    return bool(
        explain_local_noop_run_assembly_build(
            run_id=run_id,
            local_noop_run_assembly_id=local_noop_run_assembly_id,
            assembly_kind=assembly_kind,
            mode=mode,
            completion_status=completion_status,
            gate_input_ref=gate_input_ref,
            gate_input_status=gate_input_status,
            public_url_created=public_url_created,
            public_url_is_null=public_url_is_null,
            completion_evidence_items=completion_evidence_items,
            required_completion_evidence_ids=required_completion_evidence_ids,
            missing_completion_evidence_ids=missing_completion_evidence_ids,
            blocking_completion_evidence_ids=blocking_completion_evidence_ids,
            created_at=created_at,
            timestamp_policy=timestamp_policy,
            source_of_truth=source_of_truth,
            notes=notes,
        )["buildable"]
    )
