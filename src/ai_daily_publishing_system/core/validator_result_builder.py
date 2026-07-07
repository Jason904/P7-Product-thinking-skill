"""Build pure validator result buildability explanations."""

from typing import Final


REASON_CODES: Final[tuple[str, ...]] = (
    "VALIDATOR_RESULT_BUILDABLE",
    "RUN_ID_MISSING",
    "VALIDATOR_RESULT_ID_MISSING",
    "ARTIFACT_REFS_MISSING",
    "VALIDATION_CHECKS_MISSING",
    "REQUIRED_CHECK_IDS_MISSING",
    "MISSING_CHECK_IDS_DECLARED",
    "BLOCKING_CHECK_ID_UNKNOWN",
    "VALIDATOR_OUTCOME_MISSING",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "CHECK_NOT_DICT",
    "CHECK_KEYS_INVALID",
    "CHECK_ID_MISSING",
    "CHECK_ROLE_MISSING",
    "CHECK_TARGET_ARTIFACT_REF_MISSING",
    "CHECK_TARGET_ARTIFACT_KIND_MISSING",
    "CHECK_STATUS_MISSING",
    "CHECK_SEVERITY_MISSING",
    "CHECK_FINDING_MISSING",
    "CHECK_EVIDENCE_REFS_MISSING",
    "CHECK_ID_DUPLICATE",
    "CHECK_ID_NOT_REQUIRED",
    "REQUIRED_CHECK_MISSING",
    "CHECK_FORBIDDEN_RAW_FIELD_PRESENT",
)

VALIDATOR_RESULT_BUILD_REASON_CODES: Final[tuple[str, ...]] = REASON_CODES

REASON_PRIORITY: Final[tuple[str, ...]] = (
    "RUN_ID_MISSING",
    "VALIDATOR_RESULT_ID_MISSING",
    "ARTIFACT_REFS_MISSING",
    "VALIDATION_CHECKS_MISSING",
    "REQUIRED_CHECK_IDS_MISSING",
    "MISSING_CHECK_IDS_DECLARED",
    "BLOCKING_CHECK_ID_UNKNOWN",
    "VALIDATOR_OUTCOME_MISSING",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "CHECK_NOT_DICT",
    "CHECK_KEYS_INVALID",
    "CHECK_ID_MISSING",
    "CHECK_ROLE_MISSING",
    "CHECK_TARGET_ARTIFACT_REF_MISSING",
    "CHECK_TARGET_ARTIFACT_KIND_MISSING",
    "CHECK_STATUS_MISSING",
    "CHECK_SEVERITY_MISSING",
    "CHECK_FINDING_MISSING",
    "CHECK_EVIDENCE_REFS_MISSING",
    "CHECK_ID_DUPLICATE",
    "CHECK_ID_NOT_REQUIRED",
    "REQUIRED_CHECK_MISSING",
    "CHECK_FORBIDDEN_RAW_FIELD_PRESENT",
    "VALIDATOR_RESULT_BUILDABLE",
)

_RESULT_KEYS: Final[tuple[str, ...]] = (
    "buildable",
    "reason_code",
    "reason",
    "source",
    "validator_result",
    "validator_violations",
    "missing_or_invalid_fields",
    "check_violations",
    "invariant_refs",
)

_CHECK_KEYS: Final[tuple[str, ...]] = (
    "check_id",
    "check_role",
    "target_artifact_ref",
    "target_artifact_kind",
    "check_status",
    "severity",
    "finding",
    "evidence_refs",
    "notes",
)

_CHECK_STRING_FIELDS: Final[tuple[tuple[str, str], ...]] = (
    ("check_id", "CHECK_ID_MISSING"),
    ("check_role", "CHECK_ROLE_MISSING"),
    ("target_artifact_ref", "CHECK_TARGET_ARTIFACT_REF_MISSING"),
    ("target_artifact_kind", "CHECK_TARGET_ARTIFACT_KIND_MISSING"),
    ("check_status", "CHECK_STATUS_MISSING"),
    ("severity", "CHECK_SEVERITY_MISSING"),
    ("finding", "CHECK_FINDING_MISSING"),
)

_FORBIDDEN_CHECK_FIELDS: Final[tuple[str, ...]] = (
    "raw_validation_output",
    "raw_validator_output",
    "validation_output",
    "validator_output",
    "schema_validation_result",
    "html_validation_result",
    "link_check_result",
    "content_quality_result",
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
    "reader_artifact",
    "reader_artifact_content",
    "source_manifest",
    "source_manifest_content",
    "source_notes",
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
    "reader_path",
    "training_report_path",
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
    "gate_result",
    "publish_result",
    "should_fetch",
    "should_read_reader",
    "should_read_training_report",
    "should_read_source_manifest",
    "should_read_source_notes",
    "should_read_source",
    "should_read_file",
    "should_call_web",
    "should_call_github",
    "should_call_rss",
    "should_call_notion",
    "should_validate",
    "should_run_validator",
    "should_eval",
    "should_audit",
    "should_gate",
    "should_publish",
    "should_create_public_url",
    "reader_read",
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
    "validator_executed",
    "eval_executed",
    "audit_executed",
    "gate_executed",
    "published",
    "public_url_created",
)

_INVARIANT_REFS: Final[tuple[str, ...]] = (
    "validator_result_builder_only",
    "builder_not_reader_reader",
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
    "builder_not_validator_executor",
    "builder_not_eval_executor",
    "builder_not_audit_executor",
    "builder_not_gate_executor",
    "builder_not_publisher",
    "validation_checks_are_caller_supplied",
    "check_findings_are_caller_supplied",
    "artifact_refs_opaque",
    "target_artifact_refs_opaque",
    "evidence_refs_opaque",
    "validator_result_governance_evidence",
    "validator_result_not_public_candidate",
    "validator_outcome_not_quality_pass",
    "validator_outcome_not_publish_allowed",
    "buildable_not_validator_pass",
    "buildable_not_quality_pass",
    "buildable_not_eval_pass",
    "buildable_not_audit_pass",
    "buildable_not_publish_allowed",
    "buildable_not_public_url_created",
    "blocking_check_ids_are_gate_evidence_only",
    "blocking_check_ids_do_not_execute_gate",
    "no_reader_read",
    "no_training_report_read",
    "no_source_manifest_read",
    "no_source_notes_read",
    "no_source_content_read",
    "no_url_fetch",
    "no_rss_fetch",
    "no_file_read",
    "no_raw_content",
    "no_raw_url",
    "no_generated_validation",
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


def _safe_check(check: object) -> dict[str, object]:
    if not isinstance(check, dict):
        return {
            "check_id": "",
            "check_role": "",
            "target_artifact_ref": "",
            "target_artifact_kind": "",
            "check_status": "",
            "severity": "",
            "finding": "",
            "evidence_refs": (),
            "notes": (),
        }

    return {
        "check_id": _safe_string(check.get("check_id")),
        "check_role": _safe_string(check.get("check_role")),
        "target_artifact_ref": _safe_string(check.get("target_artifact_ref")),
        "target_artifact_kind": _safe_string(check.get("target_artifact_kind")),
        "check_status": _safe_string(check.get("check_status")),
        "severity": _safe_string(check.get("severity")),
        "finding": _safe_string(check.get("finding")),
        "evidence_refs": _safe_string_tuple(check.get("evidence_refs")),
        "notes": _safe_string_tuple(check.get("notes")),
    }


def _safe_checks(value: object) -> tuple[dict[str, object], ...]:
    if not isinstance(value, tuple):
        return ()

    checks = []
    for check in value:
        checks.append(_safe_check(check))
    return tuple(checks)


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


def _add_check_violation(
    check_violations: list[dict[str, object]],
    *,
    check_index: int,
    check_id: str,
    reason_code: str,
    field: str,
) -> None:
    check_violations.append(
        {
            "check_index": check_index,
            "check_id": check_id,
            "reason_code": reason_code,
            "field": field,
        }
    )


def _ordered_reason_codes(reason_codes: tuple[str, ...]) -> tuple[str, ...]:
    ordered = []
    for reason_code in REASON_PRIORITY:
        if reason_code == "VALIDATOR_RESULT_BUILDABLE":
            continue
        if reason_code in reason_codes and reason_code not in ordered:
            ordered.append(reason_code)
    return tuple(ordered)


def _ordered_fields(field_entries: tuple[tuple[str, str], ...]) -> tuple[str, ...]:
    ordered_entries = sorted(field_entries, key=lambda item: (_reason_rank(item[0]), item[1]))
    fields = []
    for unused_reason_code, field in ordered_entries:
        if field not in fields:
            fields.append(field)
    return tuple(fields)


def _ordered_check_violations(
    check_violations: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    return tuple(
        sorted(
            check_violations,
            key=lambda item: (
                _reason_rank(_safe_string(item.get("reason_code"))),
                item.get("check_index"),
                _safe_string(item.get("field")),
            ),
        )
    )


def _check_id_from(check: object) -> str:
    if not isinstance(check, dict):
        return ""
    return _safe_string(check.get("check_id"))


def _known_check_ids(validation_checks: object) -> tuple[str, ...]:
    if not isinstance(validation_checks, tuple):
        return ()

    check_ids = []
    for check in validation_checks:
        check_id = _check_id_from(check)
        if _is_nonblank_string(check_id):
            check_ids.append(check_id)
    return tuple(check_ids)


def explain_validator_result_build(
    *,
    run_id: str,
    validator_result_id: str,
    artifact_refs: tuple[str, ...],
    validation_checks: tuple[dict[str, object], ...],
    required_check_ids: tuple[str, ...],
    missing_check_ids: tuple[str, ...],
    blocking_check_ids: tuple[str, ...],
    validator_outcome: str,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    """Explain whether a caller-supplied validator result is buildable."""

    reason_codes = []
    field_entries = []
    check_violations = []

    if not _is_nonblank_string(run_id):
        _add_reason(reason_codes, "RUN_ID_MISSING")
        _add_field(field_entries, reason_code="RUN_ID_MISSING", field="run_id")

    if not _is_nonblank_string(validator_result_id):
        _add_reason(reason_codes, "VALIDATOR_RESULT_ID_MISSING")
        _add_field(
            field_entries,
            reason_code="VALIDATOR_RESULT_ID_MISSING",
            field="validator_result_id",
        )

    if not _is_nonempty_string_tuple(artifact_refs):
        _add_reason(reason_codes, "ARTIFACT_REFS_MISSING")
        _add_field(
            field_entries,
            reason_code="ARTIFACT_REFS_MISSING",
            field="artifact_refs",
        )

    if not isinstance(validation_checks, tuple) or validation_checks == ():
        _add_reason(reason_codes, "VALIDATION_CHECKS_MISSING")
        _add_field(
            field_entries,
            reason_code="VALIDATION_CHECKS_MISSING",
            field="validation_checks",
        )

    if not _is_nonempty_string_tuple(required_check_ids):
        _add_reason(reason_codes, "REQUIRED_CHECK_IDS_MISSING")
        _add_field(
            field_entries,
            reason_code="REQUIRED_CHECK_IDS_MISSING",
            field="required_check_ids",
        )

    if missing_check_ids != ():
        _add_reason(reason_codes, "MISSING_CHECK_IDS_DECLARED")
        _add_field(
            field_entries,
            reason_code="MISSING_CHECK_IDS_DECLARED",
            field="missing_check_ids",
        )

    known_check_ids = _known_check_ids(validation_checks)
    if not isinstance(blocking_check_ids, tuple):
        _add_reason(reason_codes, "BLOCKING_CHECK_ID_UNKNOWN")
        _add_field(
            field_entries,
            reason_code="BLOCKING_CHECK_ID_UNKNOWN",
            field="blocking_check_ids",
        )
    else:
        for blocking_check_id in blocking_check_ids:
            if (
                not _is_nonblank_string(blocking_check_id)
                or blocking_check_id not in known_check_ids
            ):
                _add_reason(reason_codes, "BLOCKING_CHECK_ID_UNKNOWN")
                _add_field(
                    field_entries,
                    reason_code="BLOCKING_CHECK_ID_UNKNOWN",
                    field="blocking_check_ids",
                )
                break

    if not _is_nonblank_string(validator_outcome):
        _add_reason(reason_codes, "VALIDATOR_OUTCOME_MISSING")
        _add_field(
            field_entries,
            reason_code="VALIDATOR_OUTCOME_MISSING",
            field="validator_outcome",
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

    seen_check_ids = []
    if isinstance(validation_checks, tuple):
        for check_index, check in enumerate(validation_checks):
            check_id = _check_id_from(check)

            if not isinstance(check, dict):
                _add_reason(reason_codes, "CHECK_NOT_DICT")
                _add_field(
                    field_entries,
                    reason_code="CHECK_NOT_DICT",
                    field=f"validation_checks[{check_index}]",
                )
                _add_check_violation(
                    check_violations,
                    check_index=check_index,
                    check_id="",
                    reason_code="CHECK_NOT_DICT",
                    field="validation_checks",
                )
                continue

            check_keys = tuple(check.keys())
            for key in check_keys:
                if key in _FORBIDDEN_CHECK_FIELDS:
                    _add_reason(reason_codes, "CHECK_FORBIDDEN_RAW_FIELD_PRESENT")
                    _add_field(
                        field_entries,
                        reason_code="CHECK_FORBIDDEN_RAW_FIELD_PRESENT",
                        field=f"validation_checks[{check_index}].{key}",
                    )
                    _add_check_violation(
                        check_violations,
                        check_index=check_index,
                        check_id=check_id,
                        reason_code="CHECK_FORBIDDEN_RAW_FIELD_PRESENT",
                        field=key,
                    )

            if set(check_keys) != set(_CHECK_KEYS):
                _add_reason(reason_codes, "CHECK_KEYS_INVALID")
                _add_field(
                    field_entries,
                    reason_code="CHECK_KEYS_INVALID",
                    field=f"validation_checks[{check_index}].keys",
                )
                _add_check_violation(
                    check_violations,
                    check_index=check_index,
                    check_id=check_id,
                    reason_code="CHECK_KEYS_INVALID",
                    field="keys",
                )

            for field, missing_reason_code in _CHECK_STRING_FIELDS:
                if not _is_nonblank_string(check.get(field)):
                    _add_reason(reason_codes, missing_reason_code)
                    _add_field(
                        field_entries,
                        reason_code=missing_reason_code,
                        field=f"validation_checks[{check_index}].{field}",
                    )
                    _add_check_violation(
                        check_violations,
                        check_index=check_index,
                        check_id=check_id,
                        reason_code=missing_reason_code,
                        field=field,
                    )

            if not _is_nonempty_string_tuple(check.get("evidence_refs")):
                _add_reason(reason_codes, "CHECK_EVIDENCE_REFS_MISSING")
                _add_field(
                    field_entries,
                    reason_code="CHECK_EVIDENCE_REFS_MISSING",
                    field=f"validation_checks[{check_index}].evidence_refs",
                )
                _add_check_violation(
                    check_violations,
                    check_index=check_index,
                    check_id=check_id,
                    reason_code="CHECK_EVIDENCE_REFS_MISSING",
                    field="evidence_refs",
                )

            if _is_nonblank_string(check_id):
                if check_id in seen_check_ids:
                    _add_reason(reason_codes, "CHECK_ID_DUPLICATE")
                    _add_field(
                        field_entries,
                        reason_code="CHECK_ID_DUPLICATE",
                        field=f"validation_checks[{check_index}].check_id",
                    )
                    _add_check_violation(
                        check_violations,
                        check_index=check_index,
                        check_id=check_id,
                        reason_code="CHECK_ID_DUPLICATE",
                        field="check_id",
                    )
                else:
                    seen_check_ids.append(check_id)

                if (
                    _is_nonempty_string_tuple(required_check_ids)
                    and check_id not in required_check_ids
                ):
                    _add_reason(reason_codes, "CHECK_ID_NOT_REQUIRED")
                    _add_field(
                        field_entries,
                        reason_code="CHECK_ID_NOT_REQUIRED",
                        field=f"validation_checks[{check_index}].check_id",
                    )
                    _add_check_violation(
                        check_violations,
                        check_index=check_index,
                        check_id=check_id,
                        reason_code="CHECK_ID_NOT_REQUIRED",
                        field="check_id",
                    )

    if _is_nonempty_string_tuple(required_check_ids):
        for required_check_id in required_check_ids:
            if required_check_id not in known_check_ids:
                _add_reason(reason_codes, "REQUIRED_CHECK_MISSING")
                _add_field(
                    field_entries,
                    reason_code="REQUIRED_CHECK_MISSING",
                    field=f"required_check_ids.{required_check_id}",
                )

    validator_violations = _ordered_reason_codes(tuple(reason_codes))
    missing_or_invalid_fields = _ordered_fields(tuple(field_entries))
    ordered_check_violations = _ordered_check_violations(tuple(check_violations))
    buildable = validator_violations == ()
    reason_code = "VALIDATOR_RESULT_BUILDABLE"
    if not buildable:
        reason_code = validator_violations[0]

    reason = "Validator result artifact is buildable."
    if not buildable:
        reason = f"{reason_code} prevents validator result buildability."

    return {
        "buildable": buildable,
        "reason_code": reason_code,
        "reason": reason,
        "source": {
            "artifact_refs": _safe_string_tuple(artifact_refs),
            "source_of_truth": _safe_string_tuple(source_of_truth),
        },
        "validator_result": {
            "run_id": _safe_string(run_id),
            "validator_result_id": _safe_string(validator_result_id),
            "artifact_refs": _safe_string_tuple(artifact_refs),
            "validation_checks": _safe_checks(validation_checks),
            "required_check_ids": _safe_string_tuple(required_check_ids),
            "missing_check_ids": _safe_string_tuple(missing_check_ids),
            "blocking_check_ids": _safe_string_tuple(blocking_check_ids),
            "validator_outcome": _safe_string(validator_outcome),
            "created_at": _safe_string(created_at),
            "timestamp_policy": _safe_string(timestamp_policy),
            "source_of_truth": _safe_string_tuple(source_of_truth),
            "notes": _safe_string_tuple(notes),
        },
        "validator_violations": validator_violations,
        "missing_or_invalid_fields": missing_or_invalid_fields,
        "check_violations": ordered_check_violations,
        "invariant_refs": _INVARIANT_REFS,
    }


def is_validator_result_buildable(
    *,
    run_id: str,
    validator_result_id: str,
    artifact_refs: tuple[str, ...],
    validation_checks: tuple[dict[str, object], ...],
    required_check_ids: tuple[str, ...],
    missing_check_ids: tuple[str, ...],
    blocking_check_ids: tuple[str, ...],
    validator_outcome: str,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> bool:
    """Return whether the caller-supplied validator result is buildable."""

    return bool(
        explain_validator_result_build(
            run_id=run_id,
            validator_result_id=validator_result_id,
            artifact_refs=artifact_refs,
            validation_checks=validation_checks,
            required_check_ids=required_check_ids,
            missing_check_ids=missing_check_ids,
            blocking_check_ids=blocking_check_ids,
            validator_outcome=validator_outcome,
            created_at=created_at,
            timestamp_policy=timestamp_policy,
            source_of_truth=source_of_truth,
            notes=notes,
        )["buildable"]
    )
