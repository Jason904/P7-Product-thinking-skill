"""Build pure audit review artifact buildability explanations."""

from typing import Final


REASON_CODES: Final[tuple[str, ...]] = (
    "AUDIT_REVIEW_BUILDABLE",
    "RUN_ID_MISSING",
    "AUDIT_REVIEW_ID_MISSING",
    "REVIEW_KIND_MISSING",
    "ARTIFACT_REFS_MISSING",
    "AUDIT_CHECKS_MISSING",
    "REQUIRED_AUDIT_CHECK_IDS_MISSING",
    "MISSING_AUDIT_CHECK_IDS_DECLARED",
    "BLOCKING_AUDIT_CHECK_ID_UNKNOWN",
    "AUDIT_OUTCOME_MISSING",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "AUDIT_CHECK_NOT_DICT",
    "AUDIT_CHECK_KEYS_INVALID",
    "AUDIT_CHECK_ID_MISSING",
    "AUDIT_CHECK_ROLE_MISSING",
    "AUDIT_CHECK_TARGET_ARTIFACT_REF_MISSING",
    "AUDIT_CHECK_TARGET_ARTIFACT_KIND_MISSING",
    "AUDIT_CHECK_STATUS_MISSING",
    "AUDIT_CHECK_SEVERITY_MISSING",
    "AUDIT_CHECK_FINDING_MISSING",
    "AUDIT_CHECK_EVIDENCE_REFS_MISSING",
    "AUDIT_CHECK_ID_DUPLICATE",
    "AUDIT_CHECK_ID_NOT_REQUIRED",
    "REQUIRED_AUDIT_CHECK_MISSING",
    "AUDIT_CHECK_FORBIDDEN_RAW_FIELD_PRESENT",
)

AUDIT_REVIEW_BUILD_REASON_CODES: Final[tuple[str, ...]] = REASON_CODES

REASON_PRIORITY: Final[tuple[str, ...]] = (
    "RUN_ID_MISSING",
    "AUDIT_REVIEW_ID_MISSING",
    "REVIEW_KIND_MISSING",
    "ARTIFACT_REFS_MISSING",
    "AUDIT_CHECKS_MISSING",
    "REQUIRED_AUDIT_CHECK_IDS_MISSING",
    "MISSING_AUDIT_CHECK_IDS_DECLARED",
    "BLOCKING_AUDIT_CHECK_ID_UNKNOWN",
    "AUDIT_OUTCOME_MISSING",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "AUDIT_CHECK_NOT_DICT",
    "AUDIT_CHECK_KEYS_INVALID",
    "AUDIT_CHECK_ID_MISSING",
    "AUDIT_CHECK_ROLE_MISSING",
    "AUDIT_CHECK_TARGET_ARTIFACT_REF_MISSING",
    "AUDIT_CHECK_TARGET_ARTIFACT_KIND_MISSING",
    "AUDIT_CHECK_STATUS_MISSING",
    "AUDIT_CHECK_SEVERITY_MISSING",
    "AUDIT_CHECK_FINDING_MISSING",
    "AUDIT_CHECK_EVIDENCE_REFS_MISSING",
    "AUDIT_CHECK_ID_DUPLICATE",
    "AUDIT_CHECK_ID_NOT_REQUIRED",
    "REQUIRED_AUDIT_CHECK_MISSING",
    "AUDIT_CHECK_FORBIDDEN_RAW_FIELD_PRESENT",
    "AUDIT_REVIEW_BUILDABLE",
)

_AUDIT_CHECK_KEYS: Final[tuple[str, ...]] = (
    "audit_check_id",
    "audit_check_role",
    "target_artifact_ref",
    "target_artifact_kind",
    "audit_status",
    "severity",
    "finding",
    "evidence_refs",
    "notes",
)

_AUDIT_CHECK_STRING_FIELDS: Final[tuple[tuple[str, str], ...]] = (
    ("audit_check_id", "AUDIT_CHECK_ID_MISSING"),
    ("audit_check_role", "AUDIT_CHECK_ROLE_MISSING"),
    ("target_artifact_ref", "AUDIT_CHECK_TARGET_ARTIFACT_REF_MISSING"),
    ("target_artifact_kind", "AUDIT_CHECK_TARGET_ARTIFACT_KIND_MISSING"),
    ("audit_status", "AUDIT_CHECK_STATUS_MISSING"),
    ("severity", "AUDIT_CHECK_SEVERITY_MISSING"),
    ("finding", "AUDIT_CHECK_FINDING_MISSING"),
)

_FORBIDDEN_AUDIT_CHECK_FIELDS: Final[tuple[str, ...]] = (
    "raw_audit_output",
    "raw_review_output",
    "review_output",
    "audit_output",
    "raw_judge_output",
    "judge_output",
    "llm_judge_output",
    "llm_audit_output",
    "human_audit_output",
    "human_review_output",
    "audit_execution_result",
    "audit_result",
    "policy_execution_result",
    "policy_result",
    "policy_decision",
    "policy_pass",
    "quality_pass",
    "rubric_pass",
    "validator_pass",
    "eval_pass",
    "audit_pass",
    "gate_pass",
    "publish_allowed",
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
    "validator_result",
    "validator_result_content",
    "rubric_review",
    "rubric_review_content",
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
    "validator_result_path",
    "rubric_review_path",
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
    "judge_execution_result",
    "eval_result",
    "gate_result",
    "publish_result",
    "should_fetch",
    "should_read_reader",
    "should_read_training_report",
    "should_read_validator_result",
    "should_read_rubric_review",
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
    "reader_read",
    "training_report_read",
    "validator_result_read",
    "rubric_review_read",
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
    "public_url_created",
)

_INVARIANT_REFS: Final[tuple[str, ...]] = (
    "audit_review_builder_only",
    "builder_not_reader_reader",
    "builder_not_training_report_reader",
    "builder_not_validator_result_reader",
    "builder_not_rubric_review_reader",
    "builder_not_source_manifest_reader",
    "builder_not_source_notes_reader",
    "builder_not_source_reader",
    "builder_not_file_reader",
    "builder_not_web_fetcher",
    "builder_not_github_fetcher",
    "builder_not_rss_fetcher",
    "builder_not_notion_fetcher",
    "builder_not_llm_judge",
    "builder_not_human_auditor",
    "builder_not_audit_executor",
    "builder_not_policy_executor",
    "builder_not_validator_executor",
    "builder_not_eval_executor",
    "builder_not_gate_executor",
    "builder_not_publisher",
    "audit_checks_are_caller_supplied",
    "audit_findings_are_caller_supplied",
    "audit_outcome_is_caller_supplied",
    "artifact_refs_opaque",
    "target_artifact_refs_opaque",
    "evidence_refs_opaque",
    "audit_review_governance_evidence",
    "audit_review_not_public_candidate",
    "audit_outcome_not_quality_pass",
    "audit_outcome_not_gate_pass",
    "audit_outcome_not_publish_allowed",
    "buildable_not_audit_pass",
    "buildable_not_quality_pass",
    "buildable_not_eval_pass",
    "buildable_not_gate_pass",
    "buildable_not_publish_allowed",
    "buildable_not_public_url_created",
    "blocking_audit_check_ids_are_gate_evidence_only",
    "blocking_audit_check_ids_do_not_execute_gate",
    "no_reader_read",
    "no_training_report_read",
    "no_validator_result_read",
    "no_rubric_review_read",
    "no_source_manifest_read",
    "no_source_notes_read",
    "no_source_content_read",
    "no_url_fetch",
    "no_rss_fetch",
    "no_file_read",
    "no_raw_content",
    "no_raw_url",
    "no_generated_audit",
    "no_llm_summary",
    "no_llm_judge",
    "no_human_audit_workflow",
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


def _safe_audit_check(audit_check: object) -> dict[str, object]:
    if not isinstance(audit_check, dict):
        return {
            "audit_check_id": "",
            "audit_check_role": "",
            "target_artifact_ref": "",
            "target_artifact_kind": "",
            "audit_status": "",
            "severity": "",
            "finding": "",
            "evidence_refs": (),
            "notes": (),
        }

    return {
        "audit_check_id": _safe_string(audit_check.get("audit_check_id")),
        "audit_check_role": _safe_string(audit_check.get("audit_check_role")),
        "target_artifact_ref": _safe_string(
            audit_check.get("target_artifact_ref")
        ),
        "target_artifact_kind": _safe_string(
            audit_check.get("target_artifact_kind")
        ),
        "audit_status": _safe_string(audit_check.get("audit_status")),
        "severity": _safe_string(audit_check.get("severity")),
        "finding": _safe_string(audit_check.get("finding")),
        "evidence_refs": _safe_string_tuple(audit_check.get("evidence_refs")),
        "notes": _safe_string_tuple(audit_check.get("notes")),
    }


def _safe_audit_checks(value: object) -> tuple[dict[str, object], ...]:
    if not isinstance(value, tuple):
        return ()

    audit_checks = []
    for audit_check in value:
        audit_checks.append(_safe_audit_check(audit_check))
    return tuple(audit_checks)


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


def _add_audit_check_violation(
    audit_check_violations: list[dict[str, object]],
    *,
    audit_check_index: int,
    audit_check_id: str,
    reason_code: str,
    field: str,
) -> None:
    audit_check_violations.append(
        {
            "audit_check_index": audit_check_index,
            "audit_check_id": audit_check_id,
            "reason_code": reason_code,
            "field": field,
        }
    )


def _ordered_reason_codes(reason_codes: tuple[str, ...]) -> tuple[str, ...]:
    ordered = []
    for reason_code in REASON_PRIORITY:
        if reason_code == "AUDIT_REVIEW_BUILDABLE":
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


def _ordered_audit_check_violations(
    audit_check_violations: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    return tuple(
        sorted(
            audit_check_violations,
            key=lambda item: (
                _reason_rank(_safe_string(item.get("reason_code"))),
                item.get("audit_check_index"),
                _safe_string(item.get("field")),
            ),
        )
    )


def _audit_check_id_from(audit_check: object) -> str:
    if not isinstance(audit_check, dict):
        return ""
    return _safe_string(audit_check.get("audit_check_id"))


def _known_audit_check_ids(
    audit_checks: object,
) -> tuple[str, ...]:
    if not isinstance(audit_checks, tuple):
        return ()

    audit_check_ids = []
    for audit_check in audit_checks:
        audit_check_id = _audit_check_id_from(audit_check)
        if _is_nonblank_string(audit_check_id):
            audit_check_ids.append(audit_check_id)
    return tuple(audit_check_ids)


def explain_audit_review_build(
    *,
    run_id: str,
    audit_review_id: str,
    review_kind: str,
    artifact_refs: tuple[str, ...],
    audit_checks: tuple[dict[str, object], ...],
    required_audit_check_ids: tuple[str, ...],
    missing_audit_check_ids: tuple[str, ...],
    blocking_audit_check_ids: tuple[str, ...],
    audit_outcome: str,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    """Explain whether a caller-supplied audit review is buildable."""

    reason_codes = []
    field_entries = []
    audit_check_violations = []

    if not _is_nonblank_string(run_id):
        _add_reason(reason_codes, "RUN_ID_MISSING")
        _add_field(field_entries, reason_code="RUN_ID_MISSING", field="run_id")

    if not _is_nonblank_string(audit_review_id):
        _add_reason(reason_codes, "AUDIT_REVIEW_ID_MISSING")
        _add_field(
            field_entries,
            reason_code="AUDIT_REVIEW_ID_MISSING",
            field="audit_review_id",
        )

    if not _is_nonblank_string(review_kind):
        _add_reason(reason_codes, "REVIEW_KIND_MISSING")
        _add_field(
            field_entries,
            reason_code="REVIEW_KIND_MISSING",
            field="review_kind",
        )

    if not _is_nonempty_string_tuple(artifact_refs):
        _add_reason(reason_codes, "ARTIFACT_REFS_MISSING")
        _add_field(
            field_entries,
            reason_code="ARTIFACT_REFS_MISSING",
            field="artifact_refs",
        )

    if not isinstance(audit_checks, tuple) or audit_checks == ():
        _add_reason(reason_codes, "AUDIT_CHECKS_MISSING")
        _add_field(
            field_entries,
            reason_code="AUDIT_CHECKS_MISSING",
            field="audit_checks",
        )

    if not _is_nonempty_string_tuple(required_audit_check_ids):
        _add_reason(reason_codes, "REQUIRED_AUDIT_CHECK_IDS_MISSING")
        _add_field(
            field_entries,
            reason_code="REQUIRED_AUDIT_CHECK_IDS_MISSING",
            field="required_audit_check_ids",
        )

    if missing_audit_check_ids != ():
        _add_reason(reason_codes, "MISSING_AUDIT_CHECK_IDS_DECLARED")
        _add_field(
            field_entries,
            reason_code="MISSING_AUDIT_CHECK_IDS_DECLARED",
            field="missing_audit_check_ids",
        )

    known_audit_check_ids = _known_audit_check_ids(audit_checks)
    if not isinstance(blocking_audit_check_ids, tuple):
        _add_reason(reason_codes, "BLOCKING_AUDIT_CHECK_ID_UNKNOWN")
        _add_field(
            field_entries,
            reason_code="BLOCKING_AUDIT_CHECK_ID_UNKNOWN",
            field="blocking_audit_check_ids",
        )
    else:
        for blocking_audit_check_id in blocking_audit_check_ids:
            if (
                not _is_nonblank_string(blocking_audit_check_id)
                or blocking_audit_check_id not in known_audit_check_ids
            ):
                _add_reason(
                    reason_codes,
                    "BLOCKING_AUDIT_CHECK_ID_UNKNOWN",
                )
                _add_field(
                    field_entries,
                    reason_code="BLOCKING_AUDIT_CHECK_ID_UNKNOWN",
                    field="blocking_audit_check_ids",
                )
                break

    if not _is_nonblank_string(audit_outcome):
        _add_reason(reason_codes, "AUDIT_OUTCOME_MISSING")
        _add_field(
            field_entries,
            reason_code="AUDIT_OUTCOME_MISSING",
            field="audit_outcome",
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

    seen_audit_check_ids = []
    if isinstance(audit_checks, tuple):
        for audit_check_index, audit_check in enumerate(audit_checks):
            audit_check_id = _audit_check_id_from(audit_check)

            if not isinstance(audit_check, dict):
                _add_reason(reason_codes, "AUDIT_CHECK_NOT_DICT")
                _add_field(
                    field_entries,
                    reason_code="AUDIT_CHECK_NOT_DICT",
                    field=f"audit_checks[{audit_check_index}]",
                )
                _add_audit_check_violation(
                    audit_check_violations,
                    audit_check_index=audit_check_index,
                    audit_check_id="",
                    reason_code="AUDIT_CHECK_NOT_DICT",
                    field="audit_checks",
                )
                continue

            audit_check_keys = tuple(audit_check.keys())
            for key in audit_check_keys:
                if key in _FORBIDDEN_AUDIT_CHECK_FIELDS:
                    _add_reason(
                        reason_codes,
                        "AUDIT_CHECK_FORBIDDEN_RAW_FIELD_PRESENT",
                    )
                    _add_field(
                        field_entries,
                        reason_code="AUDIT_CHECK_FORBIDDEN_RAW_FIELD_PRESENT",
                        field=f"audit_checks[{audit_check_index}].{key}",
                    )
                    _add_audit_check_violation(
                        audit_check_violations,
                        audit_check_index=audit_check_index,
                        audit_check_id=audit_check_id,
                        reason_code=(
                            "AUDIT_CHECK_FORBIDDEN_RAW_FIELD_PRESENT"
                        ),
                        field=key,
                    )

            if set(audit_check_keys) != set(_AUDIT_CHECK_KEYS):
                _add_reason(reason_codes, "AUDIT_CHECK_KEYS_INVALID")
                _add_field(
                    field_entries,
                    reason_code="AUDIT_CHECK_KEYS_INVALID",
                    field=f"audit_checks[{audit_check_index}].keys",
                )
                _add_audit_check_violation(
                    audit_check_violations,
                    audit_check_index=audit_check_index,
                    audit_check_id=audit_check_id,
                    reason_code="AUDIT_CHECK_KEYS_INVALID",
                    field="keys",
                )

            for field, missing_reason_code in _AUDIT_CHECK_STRING_FIELDS:
                if not _is_nonblank_string(audit_check.get(field)):
                    _add_reason(reason_codes, missing_reason_code)
                    _add_field(
                        field_entries,
                        reason_code=missing_reason_code,
                        field=f"audit_checks[{audit_check_index}].{field}",
                    )
                    _add_audit_check_violation(
                        audit_check_violations,
                        audit_check_index=audit_check_index,
                        audit_check_id=audit_check_id,
                        reason_code=missing_reason_code,
                        field=field,
                    )

            if not _is_nonempty_string_tuple(audit_check.get("evidence_refs")):
                _add_reason(reason_codes, "AUDIT_CHECK_EVIDENCE_REFS_MISSING")
                _add_field(
                    field_entries,
                    reason_code="AUDIT_CHECK_EVIDENCE_REFS_MISSING",
                    field=f"audit_checks[{audit_check_index}].evidence_refs",
                )
                _add_audit_check_violation(
                    audit_check_violations,
                    audit_check_index=audit_check_index,
                    audit_check_id=audit_check_id,
                    reason_code="AUDIT_CHECK_EVIDENCE_REFS_MISSING",
                    field="evidence_refs",
                )

            if _is_nonblank_string(audit_check_id):
                if audit_check_id in seen_audit_check_ids:
                    _add_reason(reason_codes, "AUDIT_CHECK_ID_DUPLICATE")
                    _add_field(
                        field_entries,
                        reason_code="AUDIT_CHECK_ID_DUPLICATE",
                        field=(
                            f"audit_checks[{audit_check_index}]."
                            "audit_check_id"
                        ),
                    )
                    _add_audit_check_violation(
                        audit_check_violations,
                        audit_check_index=audit_check_index,
                        audit_check_id=audit_check_id,
                        reason_code="AUDIT_CHECK_ID_DUPLICATE",
                        field="audit_check_id",
                    )
                else:
                    seen_audit_check_ids.append(audit_check_id)

                if (
                    _is_nonempty_string_tuple(required_audit_check_ids)
                    and audit_check_id not in required_audit_check_ids
                ):
                    _add_reason(reason_codes, "AUDIT_CHECK_ID_NOT_REQUIRED")
                    _add_field(
                        field_entries,
                        reason_code="AUDIT_CHECK_ID_NOT_REQUIRED",
                        field=(
                            f"audit_checks[{audit_check_index}]."
                            "audit_check_id"
                        ),
                    )
                    _add_audit_check_violation(
                        audit_check_violations,
                        audit_check_index=audit_check_index,
                        audit_check_id=audit_check_id,
                        reason_code="AUDIT_CHECK_ID_NOT_REQUIRED",
                        field="audit_check_id",
                    )

    if _is_nonempty_string_tuple(required_audit_check_ids):
        for required_audit_check_id in required_audit_check_ids:
            if required_audit_check_id not in known_audit_check_ids:
                _add_reason(reason_codes, "REQUIRED_AUDIT_CHECK_MISSING")
                _add_field(
                    field_entries,
                    reason_code="REQUIRED_AUDIT_CHECK_MISSING",
                    field=f"required_audit_check_ids.{required_audit_check_id}",
                )

    audit_violations = _ordered_reason_codes(tuple(reason_codes))
    missing_or_invalid_fields = _ordered_fields(tuple(field_entries))
    ordered_audit_check_violations = _ordered_audit_check_violations(
        tuple(audit_check_violations)
    )
    buildable = audit_violations == ()
    reason_code = "AUDIT_REVIEW_BUILDABLE"
    if not buildable:
        reason_code = audit_violations[0]

    reason = "Audit review artifact is buildable."
    if not buildable:
        reason = f"{reason_code} prevents audit review buildability."

    return {
        "buildable": buildable,
        "reason_code": reason_code,
        "reason": reason,
        "source": {
            "artifact_refs": _safe_string_tuple(artifact_refs),
            "source_of_truth": _safe_string_tuple(source_of_truth),
        },
        "audit_review": {
            "run_id": _safe_string(run_id),
            "audit_review_id": _safe_string(audit_review_id),
            "review_kind": _safe_string(review_kind),
            "artifact_refs": _safe_string_tuple(artifact_refs),
            "audit_checks": _safe_audit_checks(audit_checks),
            "required_audit_check_ids": _safe_string_tuple(
                required_audit_check_ids
            ),
            "missing_audit_check_ids": _safe_string_tuple(
                missing_audit_check_ids
            ),
            "blocking_audit_check_ids": _safe_string_tuple(
                blocking_audit_check_ids
            ),
            "audit_outcome": _safe_string(audit_outcome),
            "created_at": _safe_string(created_at),
            "timestamp_policy": _safe_string(timestamp_policy),
            "source_of_truth": _safe_string_tuple(source_of_truth),
            "notes": _safe_string_tuple(notes),
        },
        "audit_violations": audit_violations,
        "missing_or_invalid_fields": missing_or_invalid_fields,
        "audit_check_violations": ordered_audit_check_violations,
        "invariant_refs": _INVARIANT_REFS,
    }


def is_audit_review_buildable(
    *,
    run_id: str,
    audit_review_id: str,
    review_kind: str,
    artifact_refs: tuple[str, ...],
    audit_checks: tuple[dict[str, object], ...],
    required_audit_check_ids: tuple[str, ...],
    missing_audit_check_ids: tuple[str, ...],
    blocking_audit_check_ids: tuple[str, ...],
    audit_outcome: str,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> bool:
    """Return whether the caller-supplied audit review is buildable."""

    return bool(
        explain_audit_review_build(
            run_id=run_id,
            audit_review_id=audit_review_id,
            review_kind=review_kind,
            artifact_refs=artifact_refs,
            audit_checks=audit_checks,
            required_audit_check_ids=required_audit_check_ids,
            missing_audit_check_ids=missing_audit_check_ids,
            blocking_audit_check_ids=blocking_audit_check_ids,
            audit_outcome=audit_outcome,
            created_at=created_at,
            timestamp_policy=timestamp_policy,
            source_of_truth=source_of_truth,
            notes=notes,
        )["buildable"]
    )
