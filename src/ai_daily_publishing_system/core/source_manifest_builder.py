"""Pure source manifest buildability explanation helpers."""

from typing import Final


REASON_CODES: Final[tuple[str, ...]] = (
    "SOURCE_MANIFEST_BUILDABLE",
    "RUN_ID_MISSING",
    "SOURCE_MANIFEST_ID_MISSING",
    "SOURCE_ENTRIES_MISSING",
    "REQUIRED_SOURCE_REFS_MISSING",
    "MISSING_SOURCE_REFS_DECLARED",
    "REDACTION_STATUS_MISSING",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "ENTRY_NOT_DICT",
    "ENTRY_KEYS_INVALID",
    "ENTRY_SOURCE_REF_MISSING",
    "ENTRY_SOURCE_ID_MISSING",
    "ENTRY_SOURCE_KIND_MISSING",
    "ENTRY_SOURCE_TITLE_MISSING",
    "ENTRY_SOURCE_VISIBILITY_MISSING",
    "ENTRY_SOURCE_VISIBILITY_INVALID",
    "ENTRY_SOURCE_ROLE_MISSING",
    "ENTRY_SOURCE_ROLE_INVALID",
    "ENTRY_RETRIEVAL_MODE_MISSING",
    "ENTRY_RETRIEVAL_MODE_INVALID",
    "ENTRY_RETRIEVAL_STATUS_MISSING",
    "ENTRY_REDACTION_STATUS_MISSING",
    "ENTRY_CONTENT_REF_MISSING",
    "ENTRY_SOURCE_REF_DUPLICATE",
    "ENTRY_SOURCE_REF_NOT_DECLARED",
    "REQUIRED_SOURCE_REF_ENTRY_MISSING",
    "ENTRY_FORBIDDEN_RAW_FIELD_PRESENT",
)

_REASON_PRIORITY: Final[tuple[str, ...]] = (
    "RUN_ID_MISSING",
    "SOURCE_MANIFEST_ID_MISSING",
    "SOURCE_ENTRIES_MISSING",
    "REQUIRED_SOURCE_REFS_MISSING",
    "MISSING_SOURCE_REFS_DECLARED",
    "REDACTION_STATUS_MISSING",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "ENTRY_NOT_DICT",
    "ENTRY_KEYS_INVALID",
    "ENTRY_SOURCE_REF_MISSING",
    "ENTRY_SOURCE_ID_MISSING",
    "ENTRY_SOURCE_KIND_MISSING",
    "ENTRY_SOURCE_TITLE_MISSING",
    "ENTRY_SOURCE_VISIBILITY_MISSING",
    "ENTRY_SOURCE_VISIBILITY_INVALID",
    "ENTRY_SOURCE_ROLE_MISSING",
    "ENTRY_SOURCE_ROLE_INVALID",
    "ENTRY_RETRIEVAL_MODE_MISSING",
    "ENTRY_RETRIEVAL_MODE_INVALID",
    "ENTRY_RETRIEVAL_STATUS_MISSING",
    "ENTRY_REDACTION_STATUS_MISSING",
    "ENTRY_CONTENT_REF_MISSING",
    "ENTRY_SOURCE_REF_DUPLICATE",
    "ENTRY_SOURCE_REF_NOT_DECLARED",
    "REQUIRED_SOURCE_REF_ENTRY_MISSING",
    "ENTRY_FORBIDDEN_RAW_FIELD_PRESENT",
    "SOURCE_MANIFEST_BUILDABLE",
)

_RESULT_KEYS: Final[tuple[str, ...]] = (
    "buildable",
    "reason_code",
    "reason",
    "source",
    "manifest",
    "manifest_violations",
    "missing_or_invalid_fields",
    "entry_violations",
    "invariant_refs",
)

_MANIFEST_KEYS: Final[tuple[str, ...]] = (
    "run_id",
    "source_manifest_id",
    "source_entries",
    "required_source_refs",
    "optional_source_refs",
    "missing_source_refs",
    "redaction_status",
    "created_at",
    "timestamp_policy",
    "source_of_truth",
    "notes",
)

_ENTRY_KEYS: Final[tuple[str, ...]] = (
    "source_ref",
    "source_id",
    "source_kind",
    "source_title",
    "source_visibility",
    "source_role",
    "retrieval_mode",
    "retrieval_status",
    "redaction_status",
    "content_ref",
    "notes",
)

_ENTRY_STRING_KEYS: Final[tuple[str, ...]] = (
    "source_ref",
    "source_id",
    "source_kind",
    "source_title",
    "source_visibility",
    "source_role",
    "retrieval_mode",
    "retrieval_status",
    "redaction_status",
    "content_ref",
)

_FORBIDDEN_ENTRY_KEYS: Final[tuple[str, ...]] = (
    "raw_url",
    "url",
    "source_url",
    "public_url",
    "file_path",
    "path",
    "local_path",
    "raw_content",
    "content",
    "source_content",
    "artifact_contents",
    "fetched_content",
    "html",
    "markdown",
    "text",
    "body",
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
    "should_fetch",
    "should_read_file",
    "should_call_web",
    "should_call_github",
    "should_call_notion",
    "should_summarize",
    "should_write_manifest",
    "fetch_executed",
    "file_read_executed",
    "web_called",
    "github_called",
    "notion_called",
    "llm_called",
    "manifest_written",
    "public_url_created",
)

_ALLOWED_SOURCE_VISIBILITIES: Final[tuple[str, ...]] = (
    "private",
    "public",
    "internal",
)
_ALLOWED_SOURCE_ROLES: Final[tuple[str, ...]] = (
    "evidence",
    "context",
    "reference",
)
_ALLOWED_RETRIEVAL_MODES: Final[tuple[str, ...]] = (
    "caller_supplied",
    "manual_local_noop",
)

_INVARIANT_REFS: Final[tuple[str, ...]] = (
    "source_manifest_builder_only",
    "builder_not_retriever",
    "builder_not_source_reader",
    "builder_not_file_reader",
    "builder_not_web_fetcher",
    "builder_not_github_fetcher",
    "builder_not_notion_fetcher",
    "builder_not_llm_summarizer",
    "builder_not_manifest_writer",
    "buildable_not_manifest_write",
    "buildable_not_source_fetch",
    "buildable_not_source_read",
    "buildable_not_content_validation",
    "source_entries_are_caller_supplied",
    "source_kind_opaque",
    "content_ref_opaque",
    "no_url_fetch",
    "no_file_read",
    "no_source_content_read",
    "no_raw_content",
    "no_raw_url",
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
    "no_quality_pass_no_public_url",
)


def explain_source_manifest_build(
    *,
    run_id: str,
    source_manifest_id: str,
    source_entries: tuple[dict[str, object], ...],
    required_source_refs: tuple[str, ...],
    optional_source_refs: tuple[str, ...],
    missing_source_refs: tuple[str, ...],
    redaction_status: str,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    """Explain whether caller-supplied source manifest data is buildable."""
    records: list[dict[str, object]] = []

    _collect_manifest_violations(
        records=records,
        run_id=run_id,
        source_manifest_id=source_manifest_id,
        source_entries=source_entries,
        required_source_refs=required_source_refs,
        missing_source_refs=missing_source_refs,
        redaction_status=redaction_status,
        created_at=created_at,
        timestamp_policy=timestamp_policy,
        source_of_truth=source_of_truth,
    )
    _collect_entry_violations(
        records=records,
        source_entries=source_entries,
        required_source_refs=required_source_refs,
        optional_source_refs=optional_source_refs,
    )

    ordered_records = _order_records(records)
    manifest_violations = _unique_reason_codes(ordered_records)
    reason_code = "SOURCE_MANIFEST_BUILDABLE"
    if manifest_violations != ():
        reason_code = manifest_violations[0]
    buildable = manifest_violations == ()

    result = {
        "buildable": buildable,
        "reason_code": reason_code,
        "reason": _reason_for(reason_code),
        "source": "caller_supplied_source_manifest_arguments",
        "manifest": {
            "run_id": run_id,
            "source_manifest_id": source_manifest_id,
            "source_entries": _normalize_entries(source_entries),
            "required_source_refs": required_source_refs,
            "optional_source_refs": optional_source_refs,
            "missing_source_refs": missing_source_refs,
            "redaction_status": redaction_status,
            "created_at": created_at,
            "timestamp_policy": timestamp_policy,
            "source_of_truth": source_of_truth,
            "notes": notes,
        },
        "manifest_violations": manifest_violations,
        "missing_or_invalid_fields": _missing_or_invalid_fields(ordered_records),
        "entry_violations": _entry_violations(ordered_records),
        "invariant_refs": _INVARIANT_REFS,
    }
    return result


def is_source_manifest_buildable(
    *,
    run_id: str,
    source_manifest_id: str,
    source_entries: tuple[dict[str, object], ...],
    required_source_refs: tuple[str, ...],
    optional_source_refs: tuple[str, ...],
    missing_source_refs: tuple[str, ...],
    redaction_status: str,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> bool:
    """Return the buildable flag from the source manifest explanation."""
    return explain_source_manifest_build(
        run_id=run_id,
        source_manifest_id=source_manifest_id,
        source_entries=source_entries,
        required_source_refs=required_source_refs,
        optional_source_refs=optional_source_refs,
        missing_source_refs=missing_source_refs,
        redaction_status=redaction_status,
        created_at=created_at,
        timestamp_policy=timestamp_policy,
        source_of_truth=source_of_truth,
        notes=notes,
    )["buildable"]


def _collect_manifest_violations(
    *,
    records: list[dict[str, object]],
    run_id: str,
    source_manifest_id: str,
    source_entries: tuple[dict[str, object], ...],
    required_source_refs: tuple[str, ...],
    missing_source_refs: tuple[str, ...],
    redaction_status: str,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
) -> None:
    if _is_blank_string(run_id):
        _add_record(records, "RUN_ID_MISSING", "run_id", -1, "")
    if _is_blank_string(source_manifest_id):
        _add_record(
            records,
            "SOURCE_MANIFEST_ID_MISSING",
            "source_manifest_id",
            -1,
            "",
        )
    if source_entries == ():
        _add_record(records, "SOURCE_ENTRIES_MISSING", "source_entries", -1, "")
    if required_source_refs == ():
        _add_record(
            records,
            "REQUIRED_SOURCE_REFS_MISSING",
            "required_source_refs",
            -1,
            "",
        )
    if missing_source_refs != ():
        _add_record(
            records,
            "MISSING_SOURCE_REFS_DECLARED",
            "missing_source_refs",
            -1,
            "",
        )
    if _is_blank_string(redaction_status):
        _add_record(
            records,
            "REDACTION_STATUS_MISSING",
            "redaction_status",
            -1,
            "",
        )
    if _is_blank_string(created_at):
        _add_record(records, "CREATED_AT_MISSING", "created_at", -1, "")
    if _is_blank_string(timestamp_policy):
        _add_record(
            records,
            "TIMESTAMP_POLICY_MISSING",
            "timestamp_policy",
            -1,
            "",
        )
    if source_of_truth == ():
        _add_record(
            records,
            "SOURCE_OF_TRUTH_MISSING",
            "source_of_truth",
            -1,
            "",
        )


def _collect_entry_violations(
    *,
    records: list[dict[str, object]],
    source_entries: tuple[dict[str, object], ...],
    required_source_refs: tuple[str, ...],
    optional_source_refs: tuple[str, ...],
) -> None:
    declared_refs = required_source_refs + optional_source_refs
    seen_refs: list[str] = []

    entry_index = 0
    for entry in source_entries:
        source_ref = _source_ref_for_record(entry)
        if not isinstance(entry, dict):
            _add_record(records, "ENTRY_NOT_DICT", "source_entries", entry_index, "")
            entry_index += 1
            continue

        if _entry_keys_invalid(entry):
            _add_record(
                records,
                "ENTRY_KEYS_INVALID",
                "source_entry_keys",
                entry_index,
                source_ref,
            )

        _collect_entry_string_violations(records, entry, entry_index, source_ref)
        _collect_entry_catalog_violations(records, entry, entry_index, source_ref)

        if source_ref != "":
            if source_ref in seen_refs:
                _add_record(
                    records,
                    "ENTRY_SOURCE_REF_DUPLICATE",
                    "source_ref",
                    entry_index,
                    source_ref,
                )
            else:
                seen_refs.append(source_ref)
            if source_ref not in declared_refs:
                _add_record(
                    records,
                    "ENTRY_SOURCE_REF_NOT_DECLARED",
                    "source_ref",
                    entry_index,
                    source_ref,
                )

        if _contains_forbidden_entry_key(entry):
            _add_record(
                records,
                "ENTRY_FORBIDDEN_RAW_FIELD_PRESENT",
                "forbidden_raw_field",
                entry_index,
                source_ref,
            )

        entry_index += 1

    for required_source_ref in required_source_refs:
        if required_source_ref not in seen_refs:
            _add_record(
                records,
                "REQUIRED_SOURCE_REF_ENTRY_MISSING",
                "required_source_refs",
                -1,
                required_source_ref,
            )


def _collect_entry_string_violations(
    records: list[dict[str, object]],
    entry: dict[str, object],
    entry_index: int,
    source_ref: str,
) -> None:
    for key in _ENTRY_STRING_KEYS:
        if _is_blank_string(entry.get(key)):
            _add_record(
                records,
                _missing_reason_for_entry_key(key),
                key,
                entry_index,
                source_ref,
            )


def _collect_entry_catalog_violations(
    records: list[dict[str, object]],
    entry: dict[str, object],
    entry_index: int,
    source_ref: str,
) -> None:
    source_visibility = entry.get("source_visibility")
    if (
        not _is_blank_string(source_visibility)
        and source_visibility not in _ALLOWED_SOURCE_VISIBILITIES
    ):
        _add_record(
            records,
            "ENTRY_SOURCE_VISIBILITY_INVALID",
            "source_visibility",
            entry_index,
            source_ref,
        )

    source_role = entry.get("source_role")
    if not _is_blank_string(source_role) and source_role not in _ALLOWED_SOURCE_ROLES:
        _add_record(
            records,
            "ENTRY_SOURCE_ROLE_INVALID",
            "source_role",
            entry_index,
            source_ref,
        )

    retrieval_mode = entry.get("retrieval_mode")
    if (
        not _is_blank_string(retrieval_mode)
        and retrieval_mode not in _ALLOWED_RETRIEVAL_MODES
    ):
        _add_record(
            records,
            "ENTRY_RETRIEVAL_MODE_INVALID",
            "retrieval_mode",
            entry_index,
            source_ref,
        )


def _missing_reason_for_entry_key(key: str) -> str:
    if key == "source_ref":
        return "ENTRY_SOURCE_REF_MISSING"
    if key == "source_id":
        return "ENTRY_SOURCE_ID_MISSING"
    if key == "source_kind":
        return "ENTRY_SOURCE_KIND_MISSING"
    if key == "source_title":
        return "ENTRY_SOURCE_TITLE_MISSING"
    if key == "source_visibility":
        return "ENTRY_SOURCE_VISIBILITY_MISSING"
    if key == "source_role":
        return "ENTRY_SOURCE_ROLE_MISSING"
    if key == "retrieval_mode":
        return "ENTRY_RETRIEVAL_MODE_MISSING"
    if key == "retrieval_status":
        return "ENTRY_RETRIEVAL_STATUS_MISSING"
    if key == "redaction_status":
        return "ENTRY_REDACTION_STATUS_MISSING"
    return "ENTRY_CONTENT_REF_MISSING"


def _contains_forbidden_entry_key(entry: dict[str, object]) -> bool:
    for key in _FORBIDDEN_ENTRY_KEYS:
        if key in entry:
            return True
    return False


def _entry_keys_invalid(entry: dict[str, object]) -> bool:
    if len(entry) != len(_ENTRY_KEYS):
        return True
    for key in _ENTRY_KEYS:
        if key not in entry:
            return True
    return False


def _normalize_entries(
    source_entries: tuple[dict[str, object], ...]
) -> tuple[dict[str, object], ...]:
    normalized_entries: list[dict[str, object]] = []
    for entry in source_entries:
        normalized_entries.append(_normalize_entry(entry))
    return tuple(normalized_entries)


def _normalize_entry(entry: object) -> dict[str, object]:
    if not isinstance(entry, dict):
        return {
            "source_ref": "",
            "source_id": "",
            "source_kind": "",
            "source_title": "",
            "source_visibility": "",
            "source_role": "",
            "retrieval_mode": "",
            "retrieval_status": "",
            "redaction_status": "",
            "content_ref": "",
            "notes": (),
        }
    return {
        "source_ref": entry.get("source_ref", ""),
        "source_id": entry.get("source_id", ""),
        "source_kind": entry.get("source_kind", ""),
        "source_title": entry.get("source_title", ""),
        "source_visibility": entry.get("source_visibility", ""),
        "source_role": entry.get("source_role", ""),
        "retrieval_mode": entry.get("retrieval_mode", ""),
        "retrieval_status": entry.get("retrieval_status", ""),
        "redaction_status": entry.get("redaction_status", ""),
        "content_ref": entry.get("content_ref", ""),
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


def _entry_violations(
    records: tuple[dict[str, object], ...]
) -> tuple[dict[str, object], ...]:
    entry_records: list[dict[str, object]] = []
    for record in records:
        entry_index = int(record["entry_index"])
        if entry_index >= 0 or record["reason_code"] == "REQUIRED_SOURCE_REF_ENTRY_MISSING":
            entry_records.append(
                {
                    "entry_index": entry_index,
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
    source_ref: str,
) -> None:
    records.append(
        {
            "reason_code": reason_code,
            "field": field,
            "entry_index": entry_index,
            "source_ref": source_ref,
        }
    )


def _source_ref_for_record(entry: object) -> str:
    if isinstance(entry, dict):
        value = entry.get("source_ref")
        if isinstance(value, str) and value.strip() != "":
            return value
    return ""


def _is_blank_string(value: object) -> bool:
    return not isinstance(value, str) or value.strip() == ""


def _reason_for(reason_code: str) -> str:
    if reason_code == "SOURCE_MANIFEST_BUILDABLE":
        return "Source manifest is buildable from caller-supplied metadata."
    return "Source manifest is not buildable: " + reason_code
