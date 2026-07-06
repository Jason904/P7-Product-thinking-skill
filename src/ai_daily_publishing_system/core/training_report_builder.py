"""Pure Training Report Builder contract explanation helpers."""

from typing import Final


REASON_CODES: Final[tuple[str, ...]] = (
    "TRAINING_REPORT_BUILDABLE",
    "RUN_ID_MISSING",
    "TRAINING_REPORT_ID_MISSING",
    "SOURCE_MANIFEST_REF_MISSING",
    "SOURCE_NOTES_REF_MISSING",
    "REPORT_SECTIONS_MISSING",
    "REQUIRED_SECTION_IDS_MISSING",
    "MISSING_SECTION_IDS_DECLARED",
    "REDACTION_STATUS_MISSING",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "SECTION_NOT_DICT",
    "SECTION_KEYS_INVALID",
    "SECTION_ID_MISSING",
    "SECTION_ROLE_MISSING",
    "SECTION_TITLE_MISSING",
    "SECTION_TEXT_MISSING",
    "SECTION_SOURCE_REFS_MISSING",
    "SECTION_CITATION_MARKERS_MISSING",
    "SECTION_REDACTION_STATUS_MISSING",
    "SECTION_INCLUDE_IN_READER_NOT_BOOL",
    "INCLUDE_IN_READER_TRUE",
    "SECTION_ID_DUPLICATE",
    "SECTION_ID_NOT_REQUIRED",
    "REQUIRED_SECTION_MISSING",
    "SECTION_FORBIDDEN_RAW_FIELD_PRESENT",
)

TRAINING_REPORT_BUILD_REASON_CODES: Final[tuple[str, ...]] = REASON_CODES

REASON_PRIORITY: Final[tuple[str, ...]] = (
    "RUN_ID_MISSING",
    "TRAINING_REPORT_ID_MISSING",
    "SOURCE_MANIFEST_REF_MISSING",
    "SOURCE_NOTES_REF_MISSING",
    "REPORT_SECTIONS_MISSING",
    "REQUIRED_SECTION_IDS_MISSING",
    "MISSING_SECTION_IDS_DECLARED",
    "REDACTION_STATUS_MISSING",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "SECTION_NOT_DICT",
    "SECTION_KEYS_INVALID",
    "SECTION_ID_MISSING",
    "SECTION_ROLE_MISSING",
    "SECTION_TITLE_MISSING",
    "SECTION_TEXT_MISSING",
    "SECTION_SOURCE_REFS_MISSING",
    "SECTION_CITATION_MARKERS_MISSING",
    "SECTION_REDACTION_STATUS_MISSING",
    "SECTION_INCLUDE_IN_READER_NOT_BOOL",
    "INCLUDE_IN_READER_TRUE",
    "SECTION_ID_DUPLICATE",
    "SECTION_ID_NOT_REQUIRED",
    "REQUIRED_SECTION_MISSING",
    "SECTION_FORBIDDEN_RAW_FIELD_PRESENT",
    "TRAINING_REPORT_BUILDABLE",
)

_SECTION_KEYS: Final[tuple[str, ...]] = (
    "section_id",
    "section_role",
    "section_title",
    "section_text",
    "source_refs",
    "citation_markers",
    "redaction_status",
    "include_in_reader",
    "notes",
)

_FORBIDDEN_SECTION_FIELDS: Final[tuple[str, ...]] = (
    "rendered_markdown",
    "markdown",
    "html",
    "raw_content",
    "content",
    "source_content",
    "source_manifest",
    "source_manifest_content",
    "source_notes",
    "source_notes_content",
    "training_report_content",
    "report_markdown",
    "reader_html",
    "generated_summary",
    "llm_summary",
    "inferred_fact",
    "model_output",
    "raw_model_output",
    "prompt",
    "raw_prompt",
    "source_url",
    "raw_url",
    "url",
    "public_url",
    "file_path",
    "path",
    "local_path",
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
    "should_read_source_notes",
    "should_read_source",
    "should_read_file",
    "should_call_web",
    "should_call_github",
    "should_call_notion",
    "should_summarize",
    "should_render_markdown",
    "should_write_training_report",
    "should_write_reader",
    "source_manifest_read",
    "source_notes_read",
    "source_content_read",
    "file_read_executed",
    "web_called",
    "github_called",
    "notion_called",
    "llm_called",
    "markdown_rendered",
    "training_report_written",
    "reader_written",
    "public_url_created",
)

_INVARIANT_REFS: Final[tuple[str, ...]] = (
    "training_report_builder_only",
    "builder_not_source_manifest_reader",
    "builder_not_source_notes_reader",
    "builder_not_source_reader",
    "builder_not_file_reader",
    "builder_not_web_fetcher",
    "builder_not_github_fetcher",
    "builder_not_notion_fetcher",
    "builder_not_llm_summarizer",
    "builder_not_markdown_renderer",
    "builder_not_training_report_writer",
    "builder_not_reader_writer",
    "report_sections_are_caller_supplied",
    "section_text_is_caller_supplied",
    "source_manifest_ref_opaque",
    "source_notes_ref_opaque",
    "source_refs_opaque",
    "citation_markers_opaque",
    "training_report_private_evidence",
    "training_report_not_public_candidate",
    "reader_html_only_public_candidate",
    "no_source_manifest_read",
    "no_source_notes_read",
    "no_source_content_read",
    "no_url_fetch",
    "no_file_read",
    "no_raw_content",
    "no_raw_url",
    "no_rendered_markdown",
    "no_llm_summary",
    "no_inferred_fact_generation",
    "no_hash_calculation",
    "no_existing_builder_or_policy_call",
    "no_gate_execution",
    "no_transition_execution",
    "no_runtime_execution",
    "no_adapter_execution",
    "no_publish",
    "no_notification",
    "no_public_url_behavior",
    "include_in_reader_forbidden",
    "no_quality_pass_no_public_url",
    "noop_completed_not_pass_published",
)


def explain_training_report_build(
    *,
    run_id: str,
    training_report_id: str,
    source_manifest_ref: str,
    source_notes_ref: str,
    report_sections: tuple[dict[str, object], ...],
    required_section_ids: tuple[str, ...],
    missing_section_ids: tuple[str, ...],
    redaction_status: str,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    """Explain whether caller-supplied training report evidence is buildable."""
    report_violations = []
    section_violations = []

    _add_top_level_violations(
        report_violations,
        run_id=run_id,
        training_report_id=training_report_id,
        source_manifest_ref=source_manifest_ref,
        source_notes_ref=source_notes_ref,
        report_sections=report_sections,
        required_section_ids=required_section_ids,
        missing_section_ids=missing_section_ids,
        redaction_status=redaction_status,
        created_at=created_at,
        timestamp_policy=timestamp_policy,
        source_of_truth=source_of_truth,
    )
    _add_section_violations(
        section_violations,
        report_sections=report_sections,
        required_section_ids=required_section_ids,
    )

    ordered_report_violations = _ordered_report_violations(
        report_violations,
        section_violations,
    )
    ordered_section_violations = _ordered_section_violations(section_violations)
    missing_or_invalid_fields = _ordered_missing_or_invalid_fields(
        report_violations,
        ordered_section_violations,
    )
    buildable = ordered_report_violations == ()
    reason_code = "TRAINING_REPORT_BUILDABLE"
    if not buildable:
        reason_code = ordered_report_violations[0]

    return {
        "buildable": buildable,
        "reason_code": reason_code,
        "reason": _reason_for_code(reason_code),
        "source": {
            "source_manifest_ref": source_manifest_ref,
            "source_notes_ref": source_notes_ref,
            "source_of_truth": _tuple_or_empty(source_of_truth),
        },
        "training_report": {
            "run_id": run_id,
            "training_report_id": training_report_id,
            "source_manifest_ref": source_manifest_ref,
            "source_notes_ref": source_notes_ref,
            "report_sections": _normalized_report_sections(report_sections),
            "required_section_ids": _tuple_or_empty(required_section_ids),
            "missing_section_ids": _tuple_or_empty(missing_section_ids),
            "redaction_status": redaction_status,
            "created_at": created_at,
            "timestamp_policy": timestamp_policy,
            "source_of_truth": _tuple_or_empty(source_of_truth),
            "notes": _tuple_or_empty(notes),
        },
        "report_violations": ordered_report_violations,
        "missing_or_invalid_fields": missing_or_invalid_fields,
        "section_violations": ordered_section_violations,
        "invariant_refs": _INVARIANT_REFS,
    }


def is_training_report_buildable(
    *,
    run_id: str,
    training_report_id: str,
    source_manifest_ref: str,
    source_notes_ref: str,
    report_sections: tuple[dict[str, object], ...],
    required_section_ids: tuple[str, ...],
    missing_section_ids: tuple[str, ...],
    redaction_status: str,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> bool:
    """Return the buildable projection from explain_training_report_build."""
    return explain_training_report_build(
        run_id=run_id,
        training_report_id=training_report_id,
        source_manifest_ref=source_manifest_ref,
        source_notes_ref=source_notes_ref,
        report_sections=report_sections,
        required_section_ids=required_section_ids,
        missing_section_ids=missing_section_ids,
        redaction_status=redaction_status,
        created_at=created_at,
        timestamp_policy=timestamp_policy,
        source_of_truth=source_of_truth,
        notes=notes,
    )["buildable"]


def _add_top_level_violations(
    violations,
    *,
    run_id: str,
    training_report_id: str,
    source_manifest_ref: str,
    source_notes_ref: str,
    report_sections: tuple[dict[str, object], ...],
    required_section_ids: tuple[str, ...],
    missing_section_ids: tuple[str, ...],
    redaction_status: str,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
) -> None:
    if _is_blank_string(run_id):
        violations.append(("RUN_ID_MISSING", "run_id"))
    if _is_blank_string(training_report_id):
        violations.append(("TRAINING_REPORT_ID_MISSING", "training_report_id"))
    if _is_blank_string(source_manifest_ref):
        violations.append(("SOURCE_MANIFEST_REF_MISSING", "source_manifest_ref"))
    if _is_blank_string(source_notes_ref):
        violations.append(("SOURCE_NOTES_REF_MISSING", "source_notes_ref"))
    if not isinstance(report_sections, tuple) or report_sections == ():
        violations.append(("REPORT_SECTIONS_MISSING", "report_sections"))
    if not isinstance(required_section_ids, tuple) or required_section_ids == ():
        violations.append(("REQUIRED_SECTION_IDS_MISSING", "required_section_ids"))
    if missing_section_ids != ():
        violations.append(("MISSING_SECTION_IDS_DECLARED", "missing_section_ids"))
    if _is_blank_string(redaction_status):
        violations.append(("REDACTION_STATUS_MISSING", "redaction_status"))
    if _is_blank_string(created_at):
        violations.append(("CREATED_AT_MISSING", "created_at"))
    if _is_blank_string(timestamp_policy):
        violations.append(("TIMESTAMP_POLICY_MISSING", "timestamp_policy"))
    if not isinstance(source_of_truth, tuple) or source_of_truth == ():
        violations.append(("SOURCE_OF_TRUTH_MISSING", "source_of_truth"))


def _add_section_violations(
    violations,
    *,
    report_sections: tuple[dict[str, object], ...],
    required_section_ids: tuple[str, ...],
) -> None:
    if not isinstance(report_sections, tuple):
        return

    seen_section_ids = []
    valid_section_ids = []
    required_ids = _tuple_or_empty(required_section_ids)

    for section_index, section in enumerate(report_sections):
        if not isinstance(section, dict):
            violations.append(
                _section_violation(
                    section_index,
                    "",
                    "SECTION_NOT_DICT",
                    "report_sections",
                )
            )
            continue

        section_id = _section_id(section)
        if not _section_has_expected_keys(section):
            violations.append(
                _section_violation(
                    section_index,
                    section_id,
                    "SECTION_KEYS_INVALID",
                    "section_keys",
                )
            )

        _add_section_field_violations(
            violations,
            section_index=section_index,
            section=section,
            section_id=section_id,
        )

        if section_id != "":
            if section_id in seen_section_ids:
                violations.append(
                    _section_violation(
                        section_index,
                        section_id,
                        "SECTION_ID_DUPLICATE",
                        "section_id",
                    )
                )
            else:
                seen_section_ids.append(section_id)

            if section_id not in required_ids:
                violations.append(
                    _section_violation(
                        section_index,
                        section_id,
                        "SECTION_ID_NOT_REQUIRED",
                        "section_id",
                    )
                )
            elif section_id not in valid_section_ids:
                valid_section_ids.append(section_id)

        _add_forbidden_section_field_violations(
            violations,
            section_index=section_index,
            section=section,
            section_id=section_id,
        )

    for required_section_id in required_ids:
        if required_section_id not in valid_section_ids:
            violations.append(
                _section_violation(
                    -1,
                    required_section_id,
                    "REQUIRED_SECTION_MISSING",
                    "required_section_ids",
                )
            )


def _add_section_field_violations(
    violations,
    *,
    section_index: int,
    section: dict[str, object],
    section_id: str,
) -> None:
    if _is_blank_string(section.get("section_id")):
        violations.append(
            _section_violation(
                section_index,
                section_id,
                "SECTION_ID_MISSING",
                "section_id",
            )
        )
    if _is_blank_string(section.get("section_role")):
        violations.append(
            _section_violation(
                section_index,
                section_id,
                "SECTION_ROLE_MISSING",
                "section_role",
            )
        )
    if _is_blank_string(section.get("section_title")):
        violations.append(
            _section_violation(
                section_index,
                section_id,
                "SECTION_TITLE_MISSING",
                "section_title",
            )
        )
    if _is_blank_string(section.get("section_text")):
        violations.append(
            _section_violation(
                section_index,
                section_id,
                "SECTION_TEXT_MISSING",
                "section_text",
            )
        )
    if not _is_non_empty_string_tuple(section.get("source_refs")):
        violations.append(
            _section_violation(
                section_index,
                section_id,
                "SECTION_SOURCE_REFS_MISSING",
                "source_refs",
            )
        )
    if not _is_non_empty_string_tuple(section.get("citation_markers")):
        violations.append(
            _section_violation(
                section_index,
                section_id,
                "SECTION_CITATION_MARKERS_MISSING",
                "citation_markers",
            )
        )
    if _is_blank_string(section.get("redaction_status")):
        violations.append(
            _section_violation(
                section_index,
                section_id,
                "SECTION_REDACTION_STATUS_MISSING",
                "redaction_status",
            )
        )

    include_in_reader = section.get("include_in_reader")
    if not isinstance(include_in_reader, bool):
        violations.append(
            _section_violation(
                section_index,
                section_id,
                "SECTION_INCLUDE_IN_READER_NOT_BOOL",
                "include_in_reader",
            )
        )
    elif include_in_reader is True:
        violations.append(
            _section_violation(
                section_index,
                section_id,
                "INCLUDE_IN_READER_TRUE",
                "include_in_reader",
            )
        )


def _add_forbidden_section_field_violations(
    violations,
    *,
    section_index: int,
    section: dict[str, object],
    section_id: str,
) -> None:
    for field in _FORBIDDEN_SECTION_FIELDS:
        if field in section:
            violations.append(
                _section_violation(
                    section_index,
                    section_id,
                    "SECTION_FORBIDDEN_RAW_FIELD_PRESENT",
                    field,
                )
            )


def _ordered_report_violations(report_violations, section_violations) -> tuple[str, ...]:
    ordered = []
    for reason_code in REASON_PRIORITY:
        if reason_code == "TRAINING_REPORT_BUILDABLE":
            continue
        if _top_level_reason_present(report_violations, reason_code):
            ordered.append(reason_code)
        elif _section_reason_present(section_violations, reason_code):
            ordered.append(reason_code)
    return tuple(ordered)


def _ordered_section_violations(section_violations) -> tuple[dict[str, object], ...]:
    ordered = []
    for reason_code in REASON_PRIORITY:
        if reason_code == "TRAINING_REPORT_BUILDABLE":
            continue
        for violation in section_violations:
            if violation["reason_code"] == reason_code:
                ordered.append(violation)
    return tuple(ordered)


def _ordered_missing_or_invalid_fields(
    report_violations,
    ordered_section_violations: tuple[dict[str, object], ...],
) -> tuple[str, ...]:
    fields = []
    for reason_code in REASON_PRIORITY:
        if reason_code == "TRAINING_REPORT_BUILDABLE":
            continue
        for violation_reason_code, field in report_violations:
            if violation_reason_code == reason_code and field not in fields:
                fields.append(field)
        for violation in ordered_section_violations:
            field = violation["field"]
            if violation["reason_code"] == reason_code and field not in fields:
                fields.append(field)
    return tuple(fields)


def _top_level_reason_present(violations, reason_code: str) -> bool:
    for violation_reason_code, _field in violations:
        if violation_reason_code == reason_code:
            return True
    return False


def _section_reason_present(violations, reason_code: str) -> bool:
    for violation in violations:
        if violation["reason_code"] == reason_code:
            return True
    return False


def _section_violation(
    section_index: int,
    section_id: str,
    reason_code: str,
    field: str,
) -> dict[str, object]:
    return {
        "section_index": section_index,
        "section_id": section_id,
        "reason_code": reason_code,
        "field": field,
    }


def _normalized_report_sections(
    report_sections: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    if not isinstance(report_sections, tuple):
        return ()

    normalized_sections = []
    for section in report_sections:
        normalized_sections.append(_normalized_section(section))
    return tuple(normalized_sections)


def _normalized_section(section) -> dict[str, object]:
    if not isinstance(section, dict):
        return _empty_section()

    return {
        "section_id": _string_or_empty(section.get("section_id")),
        "section_role": _string_or_empty(section.get("section_role")),
        "section_title": _string_or_empty(section.get("section_title")),
        "section_text": _string_or_empty(section.get("section_text")),
        "source_refs": _string_tuple_or_empty(section.get("source_refs")),
        "citation_markers": _string_tuple_or_empty(section.get("citation_markers")),
        "redaction_status": _string_or_empty(section.get("redaction_status")),
        "include_in_reader": False,
        "notes": _tuple_or_empty(section.get("notes")),
    }


def _empty_section() -> dict[str, object]:
    return {
        "section_id": "",
        "section_role": "",
        "section_title": "",
        "section_text": "",
        "source_refs": (),
        "citation_markers": (),
        "redaction_status": "",
        "include_in_reader": False,
        "notes": (),
    }


def _section_has_expected_keys(section: dict[str, object]) -> bool:
    for key in section:
        if key not in _SECTION_KEYS:
            return False
    for key in _SECTION_KEYS:
        if key not in section:
            return False
    return True


def _section_id(section: dict[str, object]) -> str:
    return _string_or_empty(section.get("section_id")).strip()


def _is_blank_string(value) -> bool:
    if not isinstance(value, str):
        return True
    return value.strip() == ""


def _is_non_empty_string_tuple(value) -> bool:
    if not isinstance(value, tuple) or value == ():
        return False
    for item in value:
        if _is_blank_string(item):
            return False
    return True


def _string_or_empty(value) -> str:
    if isinstance(value, str):
        return value
    return ""


def _string_tuple_or_empty(value) -> tuple[str, ...]:
    if not isinstance(value, tuple):
        return ()
    for item in value:
        if not isinstance(item, str):
            return ()
    return value


def _tuple_or_empty(value) -> tuple[object, ...]:
    if isinstance(value, tuple):
        return value
    return ()


def _reason_for_code(reason_code: str) -> str:
    if reason_code == "TRAINING_REPORT_BUILDABLE":
        return "Training report build contract is satisfied."
    return reason_code.lower().replace("_", " ")
