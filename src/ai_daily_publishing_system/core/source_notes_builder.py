"""Pure Source Notes buildability helpers for caller-supplied notes."""

from typing import Final


REASON_CODES: Final[tuple[str, ...]] = (
    "SOURCE_NOTES_BUILDABLE",
    "RUN_ID_MISSING",
    "SOURCE_NOTES_ID_MISSING",
    "SOURCE_MANIFEST_REF_MISSING",
    "NOTE_ENTRIES_MISSING",
    "REQUIRED_SOURCE_REFS_MISSING",
    "MISSING_SOURCE_REFS_DECLARED",
    "REDACTION_STATUS_MISSING",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "ENTRY_NOT_DICT",
    "ENTRY_KEYS_INVALID",
    "ENTRY_NOTE_ID_MISSING",
    "ENTRY_SOURCE_REF_MISSING",
    "ENTRY_EVIDENCE_ROLE_MISSING",
    "ENTRY_NOTE_KIND_MISSING",
    "ENTRY_NOTE_TEXT_MISSING",
    "ENTRY_CITATION_MARKER_MISSING",
    "ENTRY_REDACTION_STATUS_MISSING",
    "ENTRY_INCLUDE_IN_TRAINING_REPORT_NOT_BOOL",
    "ENTRY_INCLUDE_IN_READER_NOT_BOOL",
    "INCLUDE_IN_READER_TRUE",
    "ENTRY_NOTE_ID_DUPLICATE",
    "ENTRY_SOURCE_REF_NOT_REQUIRED",
    "REQUIRED_SOURCE_REF_NOTE_MISSING",
    "ENTRY_FORBIDDEN_RAW_FIELD_PRESENT",
)

SOURCE_NOTES_BUILD_REASON_CODES: Final[tuple[str, ...]] = REASON_CODES

_REASON_PRIORITY: Final[tuple[str, ...]] = (
    "RUN_ID_MISSING",
    "SOURCE_NOTES_ID_MISSING",
    "SOURCE_MANIFEST_REF_MISSING",
    "NOTE_ENTRIES_MISSING",
    "REQUIRED_SOURCE_REFS_MISSING",
    "MISSING_SOURCE_REFS_DECLARED",
    "REDACTION_STATUS_MISSING",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "ENTRY_NOT_DICT",
    "ENTRY_KEYS_INVALID",
    "ENTRY_NOTE_ID_MISSING",
    "ENTRY_SOURCE_REF_MISSING",
    "ENTRY_EVIDENCE_ROLE_MISSING",
    "ENTRY_NOTE_KIND_MISSING",
    "ENTRY_NOTE_TEXT_MISSING",
    "ENTRY_CITATION_MARKER_MISSING",
    "ENTRY_REDACTION_STATUS_MISSING",
    "ENTRY_INCLUDE_IN_TRAINING_REPORT_NOT_BOOL",
    "ENTRY_INCLUDE_IN_READER_NOT_BOOL",
    "INCLUDE_IN_READER_TRUE",
    "ENTRY_NOTE_ID_DUPLICATE",
    "ENTRY_SOURCE_REF_NOT_REQUIRED",
    "REQUIRED_SOURCE_REF_NOTE_MISSING",
    "ENTRY_FORBIDDEN_RAW_FIELD_PRESENT",
    "SOURCE_NOTES_BUILDABLE",
)

REASON_PRIORITY: Final[tuple[str, ...]] = _REASON_PRIORITY

_ENTRY_KEYS: Final[tuple[str, ...]] = (
    "note_id",
    "source_ref",
    "evidence_role",
    "note_kind",
    "note_text",
    "citation_marker",
    "redaction_status",
    "include_in_training_report",
    "include_in_reader",
    "notes",
)

_ENTRY_STRING_KEYS: Final[tuple[str, ...]] = (
    "note_id",
    "source_ref",
    "evidence_role",
    "note_kind",
    "note_text",
    "citation_marker",
    "redaction_status",
)

_FORBIDDEN_ENTRY_KEYS: Final[tuple[str, ...]] = (
    "rendered_markdown",
    "markdown",
    "html",
    "raw_content",
    "content",
    "source_content",
    "source_manifest",
    "source_manifest_content",
    "source_manifest_path",
    "source_notes_path",
    "training_report_path",
    "reader_path",
    "source_url",
    "raw_url",
    "url",
    "public_url",
    "file_path",
    "path",
    "local_path",
    "generated_summary",
    "llm_summary",
    "inferred_fact",
    "model_output",
    "raw_model_output",
    "artifact_contents",
    "fetched_content",
    "source_notes_content",
    "training_report_content",
    "reader_content",
    "text",
    "body",
    "prompt",
    "raw_prompt",
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
    "should_read_source_manifest",
    "should_read_source",
    "should_read_file",
    "should_fetch",
    "should_call_web",
    "should_call_github",
    "should_call_notion",
    "should_summarize",
    "should_render_markdown",
    "should_write_source_notes",
    "should_write_training_report",
    "should_write_reader",
    "should_write_manifest",
    "source_manifest_read",
    "source_content_read",
    "file_read_executed",
    "fetch_executed",
    "web_called",
    "github_called",
    "notion_called",
    "llm_called",
    "markdown_rendered",
    "source_notes_written",
    "training_report_written",
    "reader_written",
    "manifest_written",
    "public_url_created",
)

_INVARIANT_REFS: Final[tuple[str, ...]] = (
    "source_notes_builder_only",
    "builder_not_source_manifest_reader",
    "builder_not_source_reader",
    "builder_not_file_reader",
    "builder_not_web_fetcher",
    "builder_not_github_fetcher",
    "builder_not_notion_fetcher",
    "builder_not_llm_summarizer",
    "builder_not_markdown_renderer",
    "builder_not_source_notes_writer",
    "builder_not_training_report_writer",
    "builder_not_reader_writer",
    "buildable_not_source_notes_write",
    "buildable_not_source_manifest_read",
    "buildable_not_source_read",
    "buildable_not_markdown_render",
    "buildable_not_training_report_write",
    "buildable_not_reader_write",
    "note_entries_are_caller_supplied",
    "note_text_is_caller_supplied",
    "citation_marker_opaque",
    "source_manifest_ref_opaque",
    "no_source_manifest_read",
    "no_url_fetch",
    "no_file_read",
    "no_source_content_read",
    "no_raw_content",
    "no_raw_url",
    "no_rendered_markdown",
    "no_llm_summary",
    "no_inferred_fact_generation",
    "no_credentials",
    "no_raw_env_vars",
    "no_raw_config",
    "no_adapter_outputs",
    "no_driver_object",
    "no_hashlib",
    "no_hash_calculation",
    "no_public_url_behavior",
    "no_existing_builder_or_policy_call",
    "no_gate_execution",
    "no_transition_execution",
    "no_runtime_execution",
    "no_adapter_execution",
    "no_publish",
    "no_notification",
    "include_in_reader_forbidden",
    "include_in_training_report_marker_only",
    "no_quality_pass_no_public_url",
)


def explain_source_notes_build(
    *,
    run_id: str,
    source_notes_id: str,
    source_manifest_ref: str,
    note_entries: tuple[dict[str, object], ...],
    required_source_refs: tuple[str, ...],
    missing_source_refs: tuple[str, ...],
    redaction_status: str,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    """Explain whether caller-supplied structured source notes are buildable."""
    records: list[dict[str, object]] = []

    _collect_top_level_violations(
        records=records,
        run_id=run_id,
        source_notes_id=source_notes_id,
        source_manifest_ref=source_manifest_ref,
        note_entries=note_entries,
        required_source_refs=required_source_refs,
        missing_source_refs=missing_source_refs,
        redaction_status=redaction_status,
        created_at=created_at,
        timestamp_policy=timestamp_policy,
        source_of_truth=source_of_truth,
    )
    _collect_entry_violations(
        records=records,
        note_entries=note_entries,
        required_source_refs=required_source_refs,
    )

    ordered_records = _order_records(records)
    notes_violations = _unique_reason_codes(ordered_records)
    reason_code = "SOURCE_NOTES_BUILDABLE"
    if notes_violations != ():
        reason_code = notes_violations[0]
    buildable = notes_violations == ()

    return {
        "buildable": buildable,
        "reason_code": reason_code,
        "reason": _reason_for(reason_code),
        "source": "caller_supplied_source_notes_arguments",
        "source_notes": {
            "run_id": run_id,
            "source_notes_id": source_notes_id,
            "source_manifest_ref": source_manifest_ref,
            "note_entries": _normalize_entries(note_entries),
            "required_source_refs": required_source_refs,
            "missing_source_refs": missing_source_refs,
            "redaction_status": redaction_status,
            "created_at": created_at,
            "timestamp_policy": timestamp_policy,
            "source_of_truth": source_of_truth,
            "notes": notes,
        },
        "notes_violations": notes_violations,
        "missing_or_invalid_fields": _missing_or_invalid_fields(
            ordered_records
        ),
        "entry_violations": _entry_violation_records(ordered_records),
        "invariant_refs": _INVARIANT_REFS,
    }


def is_source_notes_buildable(
    *,
    run_id: str,
    source_notes_id: str,
    source_manifest_ref: str,
    note_entries: tuple[dict[str, object], ...],
    required_source_refs: tuple[str, ...],
    missing_source_refs: tuple[str, ...],
    redaction_status: str,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> bool:
    """Return the buildable flag from the Source Notes explanation."""
    return explain_source_notes_build(
        run_id=run_id,
        source_notes_id=source_notes_id,
        source_manifest_ref=source_manifest_ref,
        note_entries=note_entries,
        required_source_refs=required_source_refs,
        missing_source_refs=missing_source_refs,
        redaction_status=redaction_status,
        created_at=created_at,
        timestamp_policy=timestamp_policy,
        source_of_truth=source_of_truth,
        notes=notes,
    )["buildable"]


def _collect_top_level_violations(
    *,
    records: list[dict[str, object]],
    run_id: str,
    source_notes_id: str,
    source_manifest_ref: str,
    note_entries: tuple[dict[str, object], ...],
    required_source_refs: tuple[str, ...],
    missing_source_refs: tuple[str, ...],
    redaction_status: str,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
) -> None:
    if _is_blank_string(run_id):
        _add_record(records, "RUN_ID_MISSING", "run_id", -1, "", "")
    if _is_blank_string(source_notes_id):
        _add_record(
            records,
            "SOURCE_NOTES_ID_MISSING",
            "source_notes_id",
            -1,
            "",
            "",
        )
    if _is_blank_string(source_manifest_ref):
        _add_record(
            records,
            "SOURCE_MANIFEST_REF_MISSING",
            "source_manifest_ref",
            -1,
            "",
            "",
        )
    if note_entries == ():
        _add_record(
            records,
            "NOTE_ENTRIES_MISSING",
            "note_entries",
            -1,
            "",
            "",
        )
    if required_source_refs == ():
        _add_record(
            records,
            "REQUIRED_SOURCE_REFS_MISSING",
            "required_source_refs",
            -1,
            "",
            "",
        )
    if missing_source_refs != ():
        _add_record(
            records,
            "MISSING_SOURCE_REFS_DECLARED",
            "missing_source_refs",
            -1,
            "",
            "",
        )
    if _is_blank_string(redaction_status):
        _add_record(
            records,
            "REDACTION_STATUS_MISSING",
            "redaction_status",
            -1,
            "",
            "",
        )
    if _is_blank_string(created_at):
        _add_record(
            records,
            "CREATED_AT_MISSING",
            "created_at",
            -1,
            "",
            "",
        )
    if _is_blank_string(timestamp_policy):
        _add_record(
            records,
            "TIMESTAMP_POLICY_MISSING",
            "timestamp_policy",
            -1,
            "",
            "",
        )
    if source_of_truth == ():
        _add_record(
            records,
            "SOURCE_OF_TRUTH_MISSING",
            "source_of_truth",
            -1,
            "",
            "",
        )


def _collect_entry_violations(
    *,
    records: list[dict[str, object]],
    note_entries: tuple[dict[str, object], ...],
    required_source_refs: tuple[str, ...],
) -> None:
    seen_note_ids: list[str] = []
    covered_source_refs: list[str] = []

    entry_index = 0
    for entry in note_entries:
        note_id = _entry_string_for_record(entry, "note_id")
        source_ref = _entry_string_for_record(entry, "source_ref")
        if not isinstance(entry, dict):
            _add_record(
                records,
                "ENTRY_NOT_DICT",
                "note_entries",
                entry_index,
                "",
                "",
            )
            entry_index += 1
            continue

        if _entry_keys_invalid(entry):
            _add_record(
                records,
                "ENTRY_KEYS_INVALID",
                "note_entry_keys",
                entry_index,
                note_id,
                source_ref,
            )

        _collect_entry_string_violations(
            records,
            entry,
            entry_index,
            note_id,
            source_ref,
        )
        _collect_entry_bool_violations(
            records,
            entry,
            entry_index,
            note_id,
            source_ref,
        )

        if note_id != "":
            if note_id in seen_note_ids:
                _add_record(
                    records,
                    "ENTRY_NOTE_ID_DUPLICATE",
                    "note_id",
                    entry_index,
                    note_id,
                    source_ref,
                )
            else:
                seen_note_ids.append(note_id)

        if source_ref != "":
            if source_ref not in covered_source_refs:
                covered_source_refs.append(source_ref)
            if source_ref not in required_source_refs:
                _add_record(
                    records,
                    "ENTRY_SOURCE_REF_NOT_REQUIRED",
                    "source_ref",
                    entry_index,
                    note_id,
                    source_ref,
                )

        if _contains_forbidden_entry_key(entry):
            _add_record(
                records,
                "ENTRY_FORBIDDEN_RAW_FIELD_PRESENT",
                "forbidden_raw_field",
                entry_index,
                note_id,
                source_ref,
            )

        entry_index += 1

    for required_source_ref in required_source_refs:
        if required_source_ref not in covered_source_refs:
            _add_record(
                records,
                "REQUIRED_SOURCE_REF_NOTE_MISSING",
                "required_source_refs",
                -1,
                "",
                required_source_ref,
            )


def _collect_entry_string_violations(
    records: list[dict[str, object]],
    entry: dict[str, object],
    entry_index: int,
    note_id: str,
    source_ref: str,
) -> None:
    for key in _ENTRY_STRING_KEYS:
        if _is_blank_string(entry.get(key)):
            _add_record(
                records,
                _missing_reason_for_entry_key(key),
                key,
                entry_index,
                note_id,
                source_ref,
            )


def _collect_entry_bool_violations(
    records: list[dict[str, object]],
    entry: dict[str, object],
    entry_index: int,
    note_id: str,
    source_ref: str,
) -> None:
    training_marker = entry.get("include_in_training_report")
    if not isinstance(training_marker, bool):
        _add_record(
            records,
            "ENTRY_INCLUDE_IN_TRAINING_REPORT_NOT_BOOL",
            "include_in_training_report",
            entry_index,
            note_id,
            source_ref,
        )

    reader_marker = entry.get("include_in_reader")
    if not isinstance(reader_marker, bool):
        _add_record(
            records,
            "ENTRY_INCLUDE_IN_READER_NOT_BOOL",
            "include_in_reader",
            entry_index,
            note_id,
            source_ref,
        )
    elif reader_marker is True:
        _add_record(
            records,
            "INCLUDE_IN_READER_TRUE",
            "include_in_reader",
            entry_index,
            note_id,
            source_ref,
        )


def _missing_reason_for_entry_key(key: str) -> str:
    if key == "note_id":
        return "ENTRY_NOTE_ID_MISSING"
    if key == "source_ref":
        return "ENTRY_SOURCE_REF_MISSING"
    if key == "evidence_role":
        return "ENTRY_EVIDENCE_ROLE_MISSING"
    if key == "note_kind":
        return "ENTRY_NOTE_KIND_MISSING"
    if key == "note_text":
        return "ENTRY_NOTE_TEXT_MISSING"
    if key == "citation_marker":
        return "ENTRY_CITATION_MARKER_MISSING"
    return "ENTRY_REDACTION_STATUS_MISSING"


def _entry_keys_invalid(entry: dict[str, object]) -> bool:
    if len(entry) != len(_ENTRY_KEYS):
        return True
    for key in _ENTRY_KEYS:
        if key not in entry:
            return True
    return False


def _contains_forbidden_entry_key(entry: dict[str, object]) -> bool:
    for key in _FORBIDDEN_ENTRY_KEYS:
        if key in entry:
            return True
    return False


def _normalize_entries(
    note_entries: tuple[dict[str, object], ...]
) -> tuple[dict[str, object], ...]:
    normalized_entries: list[dict[str, object]] = []
    for entry in note_entries:
        normalized_entries.append(_normalize_entry(entry))
    return tuple(normalized_entries)


def _normalize_entry(entry: object) -> dict[str, object]:
    if not isinstance(entry, dict):
        return {
            "note_id": "",
            "source_ref": "",
            "evidence_role": "",
            "note_kind": "",
            "note_text": "",
            "citation_marker": "",
            "redaction_status": "",
            "include_in_training_report": False,
            "include_in_reader": False,
            "notes": (),
        }
    return {
        "note_id": entry.get("note_id", ""),
        "source_ref": entry.get("source_ref", ""),
        "evidence_role": entry.get("evidence_role", ""),
        "note_kind": entry.get("note_kind", ""),
        "note_text": entry.get("note_text", ""),
        "citation_marker": entry.get("citation_marker", ""),
        "redaction_status": entry.get("redaction_status", ""),
        "include_in_training_report": entry.get(
            "include_in_training_report",
            False,
        ),
        "include_in_reader": entry.get("include_in_reader", False),
        "notes": entry.get("notes", ()),
    }


def _order_records(
    records: list[dict[str, object]]
) -> tuple[dict[str, object], ...]:
    ordered_records: list[dict[str, object]] = []
    for reason_code in _REASON_PRIORITY:
        for record in records:
            if record["reason_code"] == reason_code:
                ordered_records.append(record)
    return tuple(ordered_records)


def _unique_reason_codes(
    records: tuple[dict[str, object], ...]
) -> tuple[str, ...]:
    reason_codes: list[str] = []
    for record in records:
        reason_code = str(record["reason_code"])
        if reason_code not in reason_codes:
            reason_codes.append(reason_code)
    return tuple(reason_codes)


def _missing_or_invalid_fields(
    records: tuple[dict[str, object], ...]
) -> tuple[str, ...]:
    fields: list[str] = []
    for record in records:
        field = str(record["field"])
        if field != "" and field not in fields:
            fields.append(field)
    return tuple(fields)


def _entry_violation_records(
    records: tuple[dict[str, object], ...]
) -> tuple[dict[str, object], ...]:
    entry_records: list[dict[str, object]] = []
    for record in records:
        entry_index = int(record["entry_index"])
        if (
            entry_index >= 0
            or record["reason_code"] == "REQUIRED_SOURCE_REF_NOTE_MISSING"
        ):
            entry_records.append(
                {
                    "entry_index": entry_index,
                    "note_id": record["note_id"],
                    "source_ref": record["source_ref"],
                    "reason_code": record["reason_code"],
                    "field": record["field"],
                }
            )
    return tuple(entry_records)


def _add_record(
    records: list[dict[str, object]],
    reason_code: str,
    field: str,
    entry_index: int,
    note_id: str,
    source_ref: str,
) -> None:
    records.append(
        {
            "reason_code": reason_code,
            "field": field,
            "entry_index": entry_index,
            "note_id": note_id,
            "source_ref": source_ref,
        }
    )


def _entry_string_for_record(entry: object, key: str) -> str:
    if isinstance(entry, dict):
        value = entry.get(key)
        if isinstance(value, str) and value.strip() != "":
            return value
    return ""


def _is_blank_string(value: object) -> bool:
    return not isinstance(value, str) or value.strip() == ""


def _reason_for(reason_code: str) -> str:
    if reason_code == "SOURCE_NOTES_BUILDABLE":
        return "Source notes are buildable from caller-supplied structured notes."
    return "Source notes are not buildable: " + reason_code
