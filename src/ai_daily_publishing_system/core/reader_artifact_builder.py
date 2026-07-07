"""Build a deterministic, structured reader artifact candidate explanation."""

from typing import Final


REASON_CODES: Final[tuple[str, ...]] = (
    "READER_ARTIFACT_BUILDABLE",
    "RUN_ID_MISSING",
    "READER_ARTIFACT_ID_MISSING",
    "TRAINING_REPORT_REF_MISSING",
    "READER_BLOCKS_MISSING",
    "REQUIRED_BLOCK_IDS_MISSING",
    "MISSING_BLOCK_IDS_DECLARED",
    "REDACTION_STATUS_MISSING",
    "PUBLIC_CANDIDATE_POLICY_MISSING",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "BLOCK_NOT_DICT",
    "BLOCK_KEYS_INVALID",
    "BLOCK_ID_MISSING",
    "BLOCK_ROLE_MISSING",
    "BLOCK_TITLE_MISSING",
    "BLOCK_TEXT_MISSING",
    "BLOCK_TRAINING_REPORT_SECTION_REFS_MISSING",
    "BLOCK_CITATION_MARKERS_MISSING",
    "BLOCK_REDACTION_STATUS_MISSING",
    "BLOCK_ID_DUPLICATE",
    "BLOCK_ID_NOT_REQUIRED",
    "REQUIRED_BLOCK_MISSING",
    "BLOCK_FORBIDDEN_RAW_FIELD_PRESENT",
)

READER_ARTIFACT_BUILD_REASON_CODES: Final[tuple[str, ...]] = REASON_CODES

REASON_PRIORITY: Final[tuple[str, ...]] = (
    "RUN_ID_MISSING",
    "READER_ARTIFACT_ID_MISSING",
    "TRAINING_REPORT_REF_MISSING",
    "READER_BLOCKS_MISSING",
    "REQUIRED_BLOCK_IDS_MISSING",
    "MISSING_BLOCK_IDS_DECLARED",
    "REDACTION_STATUS_MISSING",
    "PUBLIC_CANDIDATE_POLICY_MISSING",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "BLOCK_NOT_DICT",
    "BLOCK_KEYS_INVALID",
    "BLOCK_ID_MISSING",
    "BLOCK_ROLE_MISSING",
    "BLOCK_TITLE_MISSING",
    "BLOCK_TEXT_MISSING",
    "BLOCK_TRAINING_REPORT_SECTION_REFS_MISSING",
    "BLOCK_CITATION_MARKERS_MISSING",
    "BLOCK_REDACTION_STATUS_MISSING",
    "BLOCK_ID_DUPLICATE",
    "BLOCK_ID_NOT_REQUIRED",
    "REQUIRED_BLOCK_MISSING",
    "BLOCK_FORBIDDEN_RAW_FIELD_PRESENT",
    "READER_ARTIFACT_BUILDABLE",
)

_BLOCK_KEYS: Final[tuple[str, ...]] = (
    "block_id",
    "block_role",
    "block_title",
    "block_text",
    "training_report_section_refs",
    "citation_markers",
    "redaction_status",
    "notes",
)

_FORBIDDEN_BLOCK_FIELDS: Final[tuple[str, ...]] = (
    "rendered_html",
    "html",
    "raw_html",
    "reader_html",
    "reader_html_content",
    "rendered_markdown",
    "markdown",
    "raw_markdown",
    "report_markdown",
    "training_report",
    "training_report_content",
    "training_report_markdown",
    "raw_content",
    "content",
    "source_content",
    "artifact_contents",
    "fetched_content",
    "text",
    "body",
    "raw_text",
    "source_manifest",
    "source_manifest_content",
    "source_notes",
    "source_notes_content",
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
    "publish_url",
    "deployment_url",
    "hosting_target",
    "file_path",
    "path",
    "local_path",
    "source_manifest_path",
    "source_notes_path",
    "training_report_path",
    "reader_path",
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
    "training_report_reader_result",
    "html_renderer_result",
    "markdown_renderer_result",
    "reader_write_result",
    "publish_result",
    "should_fetch",
    "should_read_training_report",
    "should_read_source_manifest",
    "should_read_source_notes",
    "should_read_source",
    "should_read_file",
    "should_call_web",
    "should_call_github",
    "should_call_rss",
    "should_call_notion",
    "should_summarize",
    "should_render_html",
    "should_render_markdown",
    "should_write_training_report",
    "should_write_reader",
    "should_publish",
    "should_create_public_url",
    "training_report_read",
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
    "html_rendered",
    "markdown_rendered",
    "training_report_written",
    "reader_written",
    "published",
    "public_url_created",
)

_INVARIANT_REFS: Final[tuple[str, ...]] = (
    "reader_artifact_builder_only",
    "builder_not_training_report_reader",
    "builder_not_source_manifest_reader",
    "builder_not_source_notes_reader",
    "builder_not_source_reader",
    "builder_not_file_reader",
    "builder_not_web_fetcher",
    "builder_not_github_fetcher",
    "builder_not_rss_fetcher",
    "builder_not_notion_fetcher",
    "builder_not_llm_summarizer",
    "builder_not_html_renderer",
    "builder_not_markdown_renderer",
    "builder_not_reader_writer",
    "builder_not_publisher",
    "reader_blocks_are_caller_supplied",
    "block_text_is_caller_supplied",
    "training_report_ref_opaque",
    "training_report_section_refs_opaque",
    "citation_markers_opaque",
    "reader_artifact_public_candidate_only",
    "reader_artifact_candidate_not_materialized_file",
    "reader_html_only_public_candidate",
    "public_candidate_not_public_url",
    "buildable_not_quality_pass",
    "buildable_not_publish_allowed",
    "buildable_not_public_url_created",
    "buildable_not_html_rendered",
    "buildable_not_reader_written",
    "no_training_report_read",
    "no_source_manifest_read",
    "no_source_notes_read",
    "no_source_content_read",
    "no_url_fetch",
    "no_rss_fetch",
    "no_file_read",
    "no_raw_content",
    "no_raw_url",
    "no_rendered_html",
    "no_rendered_markdown",
    "no_llm_summary",
    "no_inferred_fact_generation",
    "no_hash_calculation",
    "no_existing_builder_or_policy_call",
    "no_validator_execution",
    "no_eval_execution",
    "no_audit_execution",
    "no_gate_execution",
    "no_transition_execution",
    "no_runtime_execution",
    "no_adapter_execution",
    "no_publish",
    "no_notification",
    "no_public_url_behavior",
    "no_quality_pass_no_public_url",
    "noop_completed_not_pass_published",
)


def _is_missing_string(value: object) -> bool:
    return not isinstance(value, str) or value.strip() == ""


def _is_non_empty_string_tuple(value: object) -> bool:
    return (
        isinstance(value, tuple)
        and len(value) > 0
        and all(
            isinstance(item, str) and item.strip() != ""
            for item in value
        )
    )


def _has_exact_block_keys(block: dict[str, object]) -> bool:
    return (
        len(block) == len(_BLOCK_KEYS)
        and all(key in block for key in _BLOCK_KEYS)
    )


def _project_block(block: object) -> dict[str, object]:
    if not isinstance(block, dict):
        return {
            "block_id": "",
            "block_role": "",
            "block_title": "",
            "block_text": "",
            "training_report_section_refs": (),
            "citation_markers": (),
            "redaction_status": "",
            "notes": (),
        }
    return {
        "block_id": block.get("block_id", ""),
        "block_role": block.get("block_role", ""),
        "block_title": block.get("block_title", ""),
        "block_text": block.get("block_text", ""),
        "training_report_section_refs": block.get(
            "training_report_section_refs",
            (),
        ),
        "citation_markers": block.get("citation_markers", ()),
        "redaction_status": block.get("redaction_status", ""),
        "notes": block.get("notes", ()),
    }


def _reason_for_code(reason_code: str) -> str:
    if reason_code == "READER_ARTIFACT_BUILDABLE":
        return "The structured reader artifact candidate is buildable."
    return "The structured reader artifact candidate violates " + reason_code + "."


def explain_reader_artifact_build(
    *,
    run_id: str,
    reader_artifact_id: str,
    training_report_ref: str,
    reader_blocks: tuple[dict[str, object], ...],
    required_block_ids: tuple[str, ...],
    missing_block_ids: tuple[str, ...],
    redaction_status: str,
    public_candidate_policy: str,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    """Explain whether caller-supplied reader blocks form a buildable candidate."""

    violation_events: list[tuple[str, str, int]] = []
    block_violation_events: list[dict[str, object]] = []
    event_sequence = 0

    def add_violation(reason_code: str, field: str) -> None:
        nonlocal event_sequence
        violation_events.append((reason_code, field, event_sequence))
        event_sequence += 1

    def add_block_violation(
        block_index: int,
        block_id: object,
        reason_code: str,
        field: str,
    ) -> None:
        add_violation(reason_code, field)
        block_violation_events.append(
            {
                "block_index": block_index,
                "block_id": block_id if isinstance(block_id, str) else "",
                "reason_code": reason_code,
                "field": field,
            }
        )

    if _is_missing_string(run_id):
        add_violation("RUN_ID_MISSING", "run_id")
    if _is_missing_string(reader_artifact_id):
        add_violation("READER_ARTIFACT_ID_MISSING", "reader_artifact_id")
    if _is_missing_string(training_report_ref):
        add_violation("TRAINING_REPORT_REF_MISSING", "training_report_ref")

    reader_blocks_valid = (
        isinstance(reader_blocks, tuple) and len(reader_blocks) > 0
    )
    if not reader_blocks_valid:
        add_violation("READER_BLOCKS_MISSING", "reader_blocks")

    required_block_ids_valid = (
        isinstance(required_block_ids, tuple)
        and len(required_block_ids) > 0
    )
    if not required_block_ids_valid:
        add_violation("REQUIRED_BLOCK_IDS_MISSING", "required_block_ids")
    if missing_block_ids != ():
        add_violation("MISSING_BLOCK_IDS_DECLARED", "missing_block_ids")
    if _is_missing_string(redaction_status):
        add_violation("REDACTION_STATUS_MISSING", "redaction_status")
    if _is_missing_string(public_candidate_policy):
        add_violation(
            "PUBLIC_CANDIDATE_POLICY_MISSING",
            "public_candidate_policy",
        )
    if _is_missing_string(created_at):
        add_violation("CREATED_AT_MISSING", "created_at")
    if _is_missing_string(timestamp_policy):
        add_violation("TIMESTAMP_POLICY_MISSING", "timestamp_policy")
    if not isinstance(source_of_truth, tuple) or len(source_of_truth) == 0:
        add_violation("SOURCE_OF_TRUTH_MISSING", "source_of_truth")

    blocks_for_validation = reader_blocks if reader_blocks_valid else ()
    valid_block_ids: list[str] = []
    block_ids_by_index: list[tuple[int, str]] = []

    for block_index, block in enumerate(blocks_for_validation):
        if not isinstance(block, dict):
            add_block_violation(
                block_index,
                "",
                "BLOCK_NOT_DICT",
                "reader_blocks",
            )
            continue

        block_id = block.get("block_id", "")

        if not _has_exact_block_keys(block):
            add_block_violation(
                block_index,
                block_id,
                "BLOCK_KEYS_INVALID",
                "reader_blocks",
            )

        string_field_rules = (
            ("block_id", "BLOCK_ID_MISSING"),
            ("block_role", "BLOCK_ROLE_MISSING"),
            ("block_title", "BLOCK_TITLE_MISSING"),
            ("block_text", "BLOCK_TEXT_MISSING"),
            ("redaction_status", "BLOCK_REDACTION_STATUS_MISSING"),
        )
        for field, reason_code in string_field_rules:
            if _is_missing_string(block.get(field)):
                add_block_violation(
                    block_index,
                    block_id,
                    reason_code,
                    field,
                )

        if not _is_non_empty_string_tuple(
            block.get("training_report_section_refs")
        ):
            add_block_violation(
                block_index,
                block_id,
                "BLOCK_TRAINING_REPORT_SECTION_REFS_MISSING",
                "training_report_section_refs",
            )

        if not _is_non_empty_string_tuple(block.get("citation_markers")):
            add_block_violation(
                block_index,
                block_id,
                "BLOCK_CITATION_MARKERS_MISSING",
                "citation_markers",
            )

        if isinstance(block_id, str) and block_id.strip() != "":
            valid_block_ids.append(block_id)
            block_ids_by_index.append((block_index, block_id))
            if (
                required_block_ids_valid
                and block_id not in required_block_ids
            ):
                add_block_violation(
                    block_index,
                    block_id,
                    "BLOCK_ID_NOT_REQUIRED",
                    "block_id",
                )

        for forbidden_field in _FORBIDDEN_BLOCK_FIELDS:
            if forbidden_field in block:
                add_block_violation(
                    block_index,
                    block_id,
                    "BLOCK_FORBIDDEN_RAW_FIELD_PRESENT",
                    forbidden_field,
                )

    for block_index, block_id in block_ids_by_index:
        if valid_block_ids.count(block_id) > 1:
            add_block_violation(
                block_index,
                block_id,
                "BLOCK_ID_DUPLICATE",
                "block_id",
            )

    if required_block_ids_valid:
        for required_block_id in required_block_ids:
            if required_block_id not in valid_block_ids:
                add_block_violation(
                    -1,
                    required_block_id,
                    "REQUIRED_BLOCK_MISSING",
                    "required_block_ids",
                )

    ordered_events = sorted(
        violation_events,
        key=lambda event: (REASON_PRIORITY.index(event[0]), event[2]),
    )
    ordered_block_violations = tuple(
        sorted(
            block_violation_events,
            key=lambda event: (
                REASON_PRIORITY.index(str(event["reason_code"])),
                int(event["block_index"]),
                str(event["field"]),
            ),
        )
    )

    reader_violations_list: list[str] = []
    missing_or_invalid_fields_list: list[str] = []
    for reason_code, field, _ in ordered_events:
        if reason_code not in reader_violations_list:
            reader_violations_list.append(reason_code)
        if field not in missing_or_invalid_fields_list:
            missing_or_invalid_fields_list.append(field)

    reader_violations = tuple(reader_violations_list)
    missing_or_invalid_fields = tuple(missing_or_invalid_fields_list)
    buildable = reader_violations == ()
    reason_code = (
        "READER_ARTIFACT_BUILDABLE"
        if buildable
        else reader_violations[0]
    )

    projected_blocks = (
        tuple(_project_block(block) for block in reader_blocks)
        if isinstance(reader_blocks, tuple)
        else ()
    )

    return {
        "buildable": buildable,
        "reason_code": reason_code,
        "reason": _reason_for_code(reason_code),
        "source": {
            "training_report_ref": training_report_ref,
            "source_of_truth": source_of_truth,
        },
        "reader_artifact": {
            "run_id": run_id,
            "reader_artifact_id": reader_artifact_id,
            "training_report_ref": training_report_ref,
            "reader_blocks": projected_blocks,
            "required_block_ids": required_block_ids,
            "missing_block_ids": missing_block_ids,
            "redaction_status": redaction_status,
            "public_candidate_policy": public_candidate_policy,
            "created_at": created_at,
            "timestamp_policy": timestamp_policy,
            "source_of_truth": source_of_truth,
            "notes": notes,
        },
        "reader_violations": reader_violations,
        "missing_or_invalid_fields": missing_or_invalid_fields,
        "block_violations": ordered_block_violations,
        "invariant_refs": _INVARIANT_REFS,
    }


def is_reader_artifact_buildable(
    *,
    run_id: str,
    reader_artifact_id: str,
    training_report_ref: str,
    reader_blocks: tuple[dict[str, object], ...],
    required_block_ids: tuple[str, ...],
    missing_block_ids: tuple[str, ...],
    redaction_status: str,
    public_candidate_policy: str,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> bool:
    """Return the buildable flag from the structured explanation."""

    return bool(
        explain_reader_artifact_build(
            run_id=run_id,
            reader_artifact_id=reader_artifact_id,
            training_report_ref=training_report_ref,
            reader_blocks=reader_blocks,
            required_block_ids=required_block_ids,
            missing_block_ids=missing_block_ids,
            redaction_status=redaction_status,
            public_candidate_policy=public_candidate_policy,
            created_at=created_at,
            timestamp_policy=timestamp_policy,
            source_of_truth=source_of_truth,
            notes=notes,
        )["buildable"]
    )
