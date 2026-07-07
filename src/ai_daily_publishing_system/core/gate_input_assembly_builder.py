"""Build pure gate input assembly buildability explanations."""

from typing import Final


REASON_CODES: Final[tuple[str, ...]] = (
    "GATE_INPUT_ASSEMBLY_BUILDABLE",
    "RUN_ID_MISSING",
    "GATE_INPUT_ID_MISSING",
    "ASSEMBLY_KIND_MISSING",
    "CANDIDATE_ARTIFACT_REF_MISSING",
    "CANDIDATE_ARTIFACT_KIND_MISSING",
    "EVIDENCE_ITEMS_MISSING",
    "REQUIRED_EVIDENCE_IDS_MISSING",
    "MISSING_EVIDENCE_IDS_DECLARED",
    "BLOCKING_EVIDENCE_ID_UNKNOWN",
    "GATE_POLICY_REFS_MISSING",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "EVIDENCE_ITEM_NOT_DICT",
    "EVIDENCE_ITEM_KEYS_INVALID",
    "EVIDENCE_ID_MISSING",
    "EVIDENCE_ROLE_MISSING",
    "EVIDENCE_ARTIFACT_REF_MISSING",
    "EVIDENCE_ARTIFACT_KIND_MISSING",
    "EVIDENCE_STATUS_MISSING",
    "EVIDENCE_PRODUCER_REF_MISSING",
    "EVIDENCE_REFS_MISSING",
    "EVIDENCE_ID_DUPLICATE",
    "EVIDENCE_ID_NOT_REQUIRED",
    "REQUIRED_EVIDENCE_MISSING",
    "EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT",
)

GATE_INPUT_ASSEMBLY_BUILD_REASON_CODES: Final[tuple[str, ...]] = REASON_CODES

REASON_PRIORITY: Final[tuple[str, ...]] = (
    "RUN_ID_MISSING",
    "GATE_INPUT_ID_MISSING",
    "ASSEMBLY_KIND_MISSING",
    "CANDIDATE_ARTIFACT_REF_MISSING",
    "CANDIDATE_ARTIFACT_KIND_MISSING",
    "EVIDENCE_ITEMS_MISSING",
    "REQUIRED_EVIDENCE_IDS_MISSING",
    "MISSING_EVIDENCE_IDS_DECLARED",
    "BLOCKING_EVIDENCE_ID_UNKNOWN",
    "GATE_POLICY_REFS_MISSING",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "EVIDENCE_ITEM_NOT_DICT",
    "EVIDENCE_ITEM_KEYS_INVALID",
    "EVIDENCE_ID_MISSING",
    "EVIDENCE_ROLE_MISSING",
    "EVIDENCE_ARTIFACT_REF_MISSING",
    "EVIDENCE_ARTIFACT_KIND_MISSING",
    "EVIDENCE_STATUS_MISSING",
    "EVIDENCE_PRODUCER_REF_MISSING",
    "EVIDENCE_REFS_MISSING",
    "EVIDENCE_ID_DUPLICATE",
    "EVIDENCE_ID_NOT_REQUIRED",
    "REQUIRED_EVIDENCE_MISSING",
    "EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT",
    "GATE_INPUT_ASSEMBLY_BUILDABLE",
)

_EVIDENCE_ITEM_KEYS: Final[tuple[str, ...]] = (
    "evidence_id",
    "evidence_role",
    "artifact_ref",
    "artifact_kind",
    "evidence_status",
    "producer_ref",
    "evidence_refs",
    "notes",
)

_EVIDENCE_ITEM_STRING_FIELDS: Final[tuple[tuple[str, str], ...]] = (
    ("evidence_id", "EVIDENCE_ID_MISSING"),
    ("evidence_role", "EVIDENCE_ROLE_MISSING"),
    ("artifact_ref", "EVIDENCE_ARTIFACT_REF_MISSING"),
    ("artifact_kind", "EVIDENCE_ARTIFACT_KIND_MISSING"),
    ("evidence_status", "EVIDENCE_STATUS_MISSING"),
    ("producer_ref", "EVIDENCE_PRODUCER_REF_MISSING"),
)

_FORBIDDEN_EVIDENCE_ITEM_FIELDS: Final[tuple[str, ...]] = (
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
    "evidence_payload",
    "raw_evidence_payload",
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
    "noop_completed",
    "pass_published",
    "public_url",
    "publish_url",
    "deployment_url",
    "hosting_target",
    "public_url_created",
    "file_path",
    "path",
    "local_path",
    "reader_path",
    "training_report_path",
    "validator_result_path",
    "rubric_review_path",
    "audit_review_path",
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
    "should_fetch",
    "should_read_reader",
    "should_read_training_report",
    "should_read_validator_result",
    "should_read_rubric_review",
    "should_read_audit_review",
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
    "reader_read",
    "training_report_read",
    "validator_result_read",
    "rubric_review_read",
    "audit_review_read",
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
    "published",
    "notified",
    "ledger_written",
)

_INVARIANT_REFS: Final[tuple[str, ...]] = (
    "gate_input_assembly_builder_only",
    "builder_not_reader_reader",
    "builder_not_training_report_reader",
    "builder_not_validator_result_reader",
    "builder_not_rubric_review_reader",
    "builder_not_audit_review_reader",
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
    "builder_not_publisher",
    "builder_not_ledger_writer",
    "builder_not_notifier",
    "evidence_items_are_caller_supplied",
    "evidence_status_is_caller_supplied",
    "gate_policy_refs_are_caller_supplied",
    "candidate_artifact_ref_opaque",
    "artifact_refs_opaque",
    "evidence_refs_opaque",
    "gate_input_governance_evidence_bundle",
    "gate_input_not_gate_decision",
    "gate_input_not_public_candidate",
    "gate_input_not_publish_artifact",
    "candidate_artifact_not_public_url",
    "evidence_status_not_quality_pass",
    "evidence_status_not_gate_pass",
    "evidence_status_not_publish_allowed",
    "gate_policy_refs_not_policy_execution",
    "buildable_not_quality_pass",
    "buildable_not_eval_pass",
    "buildable_not_audit_pass",
    "buildable_not_gate_pass",
    "buildable_not_publish_allowed",
    "buildable_not_review_blocked",
    "buildable_not_noop_completed",
    "buildable_not_pass_published",
    "buildable_not_public_url_created",
    "blocking_evidence_ids_are_gate_evidence_only",
    "blocking_evidence_ids_do_not_execute_gate",
    "no_reader_read",
    "no_training_report_read",
    "no_validator_result_read",
    "no_rubric_review_read",
    "no_audit_review_read",
    "no_source_manifest_read",
    "no_source_notes_read",
    "no_source_content_read",
    "no_url_fetch",
    "no_rss_fetch",
    "no_file_read",
    "no_raw_content",
    "no_raw_url",
    "no_generated_gate_decision",
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
    "no_runtime_execution",
    "no_adapter_execution",
    "no_publish",
    "no_notification",
    "no_ledger_write",
    "no_public_url_behavior",
    "no_quality_pass_no_public_url",
    "noop_completed_not_pass_published",
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


def _safe_string_tuple(value: object) -> tuple[str, ...]:
    if not isinstance(value, tuple):
        return ()

    safe_values = []
    for item in value:
        if isinstance(item, str):
            safe_values.append(item)
    return tuple(safe_values)


def _safe_evidence_item(evidence_item: object) -> dict[str, object]:
    if not isinstance(evidence_item, dict):
        return {
            "evidence_id": "",
            "evidence_role": "",
            "artifact_ref": "",
            "artifact_kind": "",
            "evidence_status": "",
            "producer_ref": "",
            "evidence_refs": (),
            "notes": (),
        }

    return {
        "evidence_id": _safe_string(evidence_item.get("evidence_id")),
        "evidence_role": _safe_string(evidence_item.get("evidence_role")),
        "artifact_ref": _safe_string(evidence_item.get("artifact_ref")),
        "artifact_kind": _safe_string(evidence_item.get("artifact_kind")),
        "evidence_status": _safe_string(evidence_item.get("evidence_status")),
        "producer_ref": _safe_string(evidence_item.get("producer_ref")),
        "evidence_refs": _safe_string_tuple(evidence_item.get("evidence_refs")),
        "notes": _safe_string_tuple(evidence_item.get("notes")),
    }


def _safe_evidence_items(value: object) -> tuple[dict[str, object], ...]:
    if not isinstance(value, tuple):
        return ()

    evidence_items = []
    for evidence_item in value:
        evidence_items.append(_safe_evidence_item(evidence_item))
    return tuple(evidence_items)


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


def _add_evidence_item_violation(
    evidence_item_violations: list[dict[str, object]],
    *,
    evidence_item_index: int,
    evidence_id: str,
    reason_code: str,
    field: str,
) -> None:
    evidence_item_violations.append(
        {
            "evidence_item_index": evidence_item_index,
            "evidence_id": evidence_id,
            "reason_code": reason_code,
            "field": field,
        }
    )


def _ordered_reason_codes(reason_codes: tuple[str, ...]) -> tuple[str, ...]:
    ordered = []
    for reason_code in REASON_PRIORITY:
        if reason_code == "GATE_INPUT_ASSEMBLY_BUILDABLE":
            continue
        if reason_code in reason_codes and reason_code not in ordered:
            ordered.append(reason_code)
    return tuple(ordered)


def _ordered_fields(field_entries: tuple[tuple[str, str], ...]) -> tuple[str, ...]:
    ordered_entries = sorted(
        field_entries,
        key=lambda item: (_reason_rank(item[0]), item[1]),
    )
    fields = []
    for unused_reason_code, field in ordered_entries:
        if field not in fields:
            fields.append(field)
    return tuple(fields)


def _ordered_evidence_item_violations(
    evidence_item_violations: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    return tuple(
        sorted(
            evidence_item_violations,
            key=lambda item: (
                _reason_rank(_safe_string(item.get("reason_code"))),
                item.get("evidence_item_index"),
                _safe_string(item.get("field")),
            ),
        )
    )


def _evidence_id_from(evidence_item: object) -> str:
    if not isinstance(evidence_item, dict):
        return ""
    return _safe_string(evidence_item.get("evidence_id"))


def _known_evidence_ids(evidence_items: object) -> tuple[str, ...]:
    if not isinstance(evidence_items, tuple):
        return ()

    evidence_ids = []
    for evidence_item in evidence_items:
        evidence_id = _evidence_id_from(evidence_item)
        if _is_nonblank_string(evidence_id):
            evidence_ids.append(evidence_id)
    return tuple(evidence_ids)


def explain_gate_input_assembly_build(
    *,
    run_id: str,
    gate_input_id: str,
    assembly_kind: str,
    candidate_artifact_ref: str,
    candidate_artifact_kind: str,
    evidence_items: tuple[dict[str, object], ...],
    required_evidence_ids: tuple[str, ...],
    missing_evidence_ids: tuple[str, ...],
    blocking_evidence_ids: tuple[str, ...],
    gate_policy_refs: tuple[str, ...],
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    """Explain whether a caller-supplied gate input bundle is buildable."""

    reason_codes = []
    field_entries = []
    evidence_item_violations = []

    if not _is_nonblank_string(run_id):
        _add_reason(reason_codes, "RUN_ID_MISSING")
        _add_field(field_entries, reason_code="RUN_ID_MISSING", field="run_id")

    if not _is_nonblank_string(gate_input_id):
        _add_reason(reason_codes, "GATE_INPUT_ID_MISSING")
        _add_field(
            field_entries,
            reason_code="GATE_INPUT_ID_MISSING",
            field="gate_input_id",
        )

    if not _is_nonblank_string(assembly_kind):
        _add_reason(reason_codes, "ASSEMBLY_KIND_MISSING")
        _add_field(
            field_entries,
            reason_code="ASSEMBLY_KIND_MISSING",
            field="assembly_kind",
        )

    if not _is_nonblank_string(candidate_artifact_ref):
        _add_reason(reason_codes, "CANDIDATE_ARTIFACT_REF_MISSING")
        _add_field(
            field_entries,
            reason_code="CANDIDATE_ARTIFACT_REF_MISSING",
            field="candidate_artifact_ref",
        )

    if not _is_nonblank_string(candidate_artifact_kind):
        _add_reason(reason_codes, "CANDIDATE_ARTIFACT_KIND_MISSING")
        _add_field(
            field_entries,
            reason_code="CANDIDATE_ARTIFACT_KIND_MISSING",
            field="candidate_artifact_kind",
        )

    if not isinstance(evidence_items, tuple) or evidence_items == ():
        _add_reason(reason_codes, "EVIDENCE_ITEMS_MISSING")
        _add_field(
            field_entries,
            reason_code="EVIDENCE_ITEMS_MISSING",
            field="evidence_items",
        )

    if not _is_nonempty_string_tuple(required_evidence_ids):
        _add_reason(reason_codes, "REQUIRED_EVIDENCE_IDS_MISSING")
        _add_field(
            field_entries,
            reason_code="REQUIRED_EVIDENCE_IDS_MISSING",
            field="required_evidence_ids",
        )

    if missing_evidence_ids != ():
        _add_reason(reason_codes, "MISSING_EVIDENCE_IDS_DECLARED")
        _add_field(
            field_entries,
            reason_code="MISSING_EVIDENCE_IDS_DECLARED",
            field="missing_evidence_ids",
        )

    known_evidence_ids = _known_evidence_ids(evidence_items)
    if not isinstance(blocking_evidence_ids, tuple):
        _add_reason(reason_codes, "BLOCKING_EVIDENCE_ID_UNKNOWN")
        _add_field(
            field_entries,
            reason_code="BLOCKING_EVIDENCE_ID_UNKNOWN",
            field="blocking_evidence_ids",
        )
    else:
        for blocking_evidence_id in blocking_evidence_ids:
            if (
                not _is_nonblank_string(blocking_evidence_id)
                or blocking_evidence_id not in known_evidence_ids
            ):
                _add_reason(reason_codes, "BLOCKING_EVIDENCE_ID_UNKNOWN")
                _add_field(
                    field_entries,
                    reason_code="BLOCKING_EVIDENCE_ID_UNKNOWN",
                    field="blocking_evidence_ids",
                )
                break

    if not _is_nonempty_string_tuple(gate_policy_refs):
        _add_reason(reason_codes, "GATE_POLICY_REFS_MISSING")
        _add_field(
            field_entries,
            reason_code="GATE_POLICY_REFS_MISSING",
            field="gate_policy_refs",
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

    seen_evidence_ids = []
    if isinstance(evidence_items, tuple):
        for evidence_item_index, evidence_item in enumerate(evidence_items):
            evidence_id = _evidence_id_from(evidence_item)

            if not isinstance(evidence_item, dict):
                _add_reason(reason_codes, "EVIDENCE_ITEM_NOT_DICT")
                _add_field(
                    field_entries,
                    reason_code="EVIDENCE_ITEM_NOT_DICT",
                    field=f"evidence_items[{evidence_item_index}]",
                )
                _add_evidence_item_violation(
                    evidence_item_violations,
                    evidence_item_index=evidence_item_index,
                    evidence_id="",
                    reason_code="EVIDENCE_ITEM_NOT_DICT",
                    field="evidence_items",
                )
                continue

            evidence_item_keys = tuple(evidence_item.keys())
            for key in evidence_item_keys:
                if key in _FORBIDDEN_EVIDENCE_ITEM_FIELDS:
                    _add_reason(
                        reason_codes,
                        "EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT",
                    )
                    _add_field(
                        field_entries,
                        reason_code="EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT",
                        field=f"evidence_items[{evidence_item_index}].{key}",
                    )
                    _add_evidence_item_violation(
                        evidence_item_violations,
                        evidence_item_index=evidence_item_index,
                        evidence_id=evidence_id,
                        reason_code=(
                            "EVIDENCE_ITEM_FORBIDDEN_RAW_FIELD_PRESENT"
                        ),
                        field=key,
                    )

            if set(evidence_item_keys) != set(_EVIDENCE_ITEM_KEYS):
                _add_reason(reason_codes, "EVIDENCE_ITEM_KEYS_INVALID")
                _add_field(
                    field_entries,
                    reason_code="EVIDENCE_ITEM_KEYS_INVALID",
                    field=f"evidence_items[{evidence_item_index}].keys",
                )
                _add_evidence_item_violation(
                    evidence_item_violations,
                    evidence_item_index=evidence_item_index,
                    evidence_id=evidence_id,
                    reason_code="EVIDENCE_ITEM_KEYS_INVALID",
                    field="keys",
                )

            for field, missing_reason_code in _EVIDENCE_ITEM_STRING_FIELDS:
                if not _is_nonblank_string(evidence_item.get(field)):
                    _add_reason(reason_codes, missing_reason_code)
                    _add_field(
                        field_entries,
                        reason_code=missing_reason_code,
                        field=f"evidence_items[{evidence_item_index}].{field}",
                    )
                    _add_evidence_item_violation(
                        evidence_item_violations,
                        evidence_item_index=evidence_item_index,
                        evidence_id=evidence_id,
                        reason_code=missing_reason_code,
                        field=field,
                    )

            if not _is_nonempty_string_tuple(evidence_item.get("evidence_refs")):
                _add_reason(reason_codes, "EVIDENCE_REFS_MISSING")
                _add_field(
                    field_entries,
                    reason_code="EVIDENCE_REFS_MISSING",
                    field=f"evidence_items[{evidence_item_index}].evidence_refs",
                )
                _add_evidence_item_violation(
                    evidence_item_violations,
                    evidence_item_index=evidence_item_index,
                    evidence_id=evidence_id,
                    reason_code="EVIDENCE_REFS_MISSING",
                    field="evidence_refs",
                )

            if _is_nonblank_string(evidence_id):
                if evidence_id in seen_evidence_ids:
                    _add_reason(reason_codes, "EVIDENCE_ID_DUPLICATE")
                    _add_field(
                        field_entries,
                        reason_code="EVIDENCE_ID_DUPLICATE",
                        field=(
                            f"evidence_items[{evidence_item_index}]."
                            "evidence_id"
                        ),
                    )
                    _add_evidence_item_violation(
                        evidence_item_violations,
                        evidence_item_index=evidence_item_index,
                        evidence_id=evidence_id,
                        reason_code="EVIDENCE_ID_DUPLICATE",
                        field="evidence_id",
                    )
                else:
                    seen_evidence_ids.append(evidence_id)

                if (
                    _is_nonempty_string_tuple(required_evidence_ids)
                    and evidence_id not in required_evidence_ids
                ):
                    _add_reason(reason_codes, "EVIDENCE_ID_NOT_REQUIRED")
                    _add_field(
                        field_entries,
                        reason_code="EVIDENCE_ID_NOT_REQUIRED",
                        field=(
                            f"evidence_items[{evidence_item_index}]."
                            "evidence_id"
                        ),
                    )
                    _add_evidence_item_violation(
                        evidence_item_violations,
                        evidence_item_index=evidence_item_index,
                        evidence_id=evidence_id,
                        reason_code="EVIDENCE_ID_NOT_REQUIRED",
                        field="evidence_id",
                    )

    if _is_nonempty_string_tuple(required_evidence_ids):
        for required_evidence_id in required_evidence_ids:
            if required_evidence_id not in known_evidence_ids:
                _add_reason(reason_codes, "REQUIRED_EVIDENCE_MISSING")
                _add_field(
                    field_entries,
                    reason_code="REQUIRED_EVIDENCE_MISSING",
                    field=f"required_evidence_ids.{required_evidence_id}",
                )

    assembly_violations = _ordered_reason_codes(tuple(reason_codes))
    missing_or_invalid_fields = _ordered_fields(tuple(field_entries))
    ordered_evidence_item_violations = _ordered_evidence_item_violations(
        tuple(evidence_item_violations)
    )
    buildable = assembly_violations == ()
    reason_code = "GATE_INPUT_ASSEMBLY_BUILDABLE"
    if not buildable:
        reason_code = assembly_violations[0]

    reason = "Gate input assembly is buildable."
    if not buildable:
        reason = f"{reason_code} prevents gate input assembly buildability."

    return {
        "buildable": buildable,
        "reason_code": reason_code,
        "reason": reason,
        "source": {
            "candidate_artifact_ref": _safe_string(candidate_artifact_ref),
            "candidate_artifact_kind": _safe_string(candidate_artifact_kind),
            "gate_policy_refs": _safe_string_tuple(gate_policy_refs),
            "source_of_truth": _safe_string_tuple(source_of_truth),
        },
        "gate_input": {
            "run_id": _safe_string(run_id),
            "gate_input_id": _safe_string(gate_input_id),
            "assembly_kind": _safe_string(assembly_kind),
            "candidate_artifact_ref": _safe_string(candidate_artifact_ref),
            "candidate_artifact_kind": _safe_string(candidate_artifact_kind),
            "evidence_items": _safe_evidence_items(evidence_items),
            "required_evidence_ids": _safe_string_tuple(required_evidence_ids),
            "missing_evidence_ids": _safe_string_tuple(missing_evidence_ids),
            "blocking_evidence_ids": _safe_string_tuple(blocking_evidence_ids),
            "gate_policy_refs": _safe_string_tuple(gate_policy_refs),
            "created_at": _safe_string(created_at),
            "timestamp_policy": _safe_string(timestamp_policy),
            "source_of_truth": _safe_string_tuple(source_of_truth),
            "notes": _safe_string_tuple(notes),
        },
        "assembly_violations": assembly_violations,
        "missing_or_invalid_fields": missing_or_invalid_fields,
        "evidence_item_violations": ordered_evidence_item_violations,
        "invariant_refs": _INVARIANT_REFS,
    }


def is_gate_input_assembly_buildable(
    *,
    run_id: str,
    gate_input_id: str,
    assembly_kind: str,
    candidate_artifact_ref: str,
    candidate_artifact_kind: str,
    evidence_items: tuple[dict[str, object], ...],
    required_evidence_ids: tuple[str, ...],
    missing_evidence_ids: tuple[str, ...],
    blocking_evidence_ids: tuple[str, ...],
    gate_policy_refs: tuple[str, ...],
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> bool:
    """Return whether the caller-supplied gate input is buildable."""

    return bool(
        explain_gate_input_assembly_build(
            run_id=run_id,
            gate_input_id=gate_input_id,
            assembly_kind=assembly_kind,
            candidate_artifact_ref=candidate_artifact_ref,
            candidate_artifact_kind=candidate_artifact_kind,
            evidence_items=evidence_items,
            required_evidence_ids=required_evidence_ids,
            missing_evidence_ids=missing_evidence_ids,
            blocking_evidence_ids=blocking_evidence_ids,
            gate_policy_refs=gate_policy_refs,
            created_at=created_at,
            timestamp_policy=timestamp_policy,
            source_of_truth=source_of_truth,
            notes=notes,
        )["buildable"]
    )
