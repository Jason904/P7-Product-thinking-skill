"""Build pure rubric review artifact buildability explanations."""

from typing import Final


REASON_CODES: Final[tuple[str, ...]] = (
    "RUBRIC_REVIEW_BUILDABLE",
    "RUN_ID_MISSING",
    "RUBRIC_REVIEW_ID_MISSING",
    "REVIEW_KIND_MISSING",
    "ARTIFACT_REFS_MISSING",
    "RUBRIC_CRITERIA_MISSING",
    "REQUIRED_CRITERION_IDS_MISSING",
    "MISSING_CRITERION_IDS_DECLARED",
    "BLOCKING_CRITERION_ID_UNKNOWN",
    "RUBRIC_OUTCOME_MISSING",
    "SCORE_TOTAL_MISSING",
    "SCORE_THRESHOLD_MISSING",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "CRITERION_NOT_DICT",
    "CRITERION_KEYS_INVALID",
    "CRITERION_ID_MISSING",
    "CRITERION_ROLE_MISSING",
    "CRITERION_TARGET_ARTIFACT_REF_MISSING",
    "CRITERION_TARGET_ARTIFACT_KIND_MISSING",
    "CRITERION_STATUS_MISSING",
    "CRITERION_SEVERITY_MISSING",
    "CRITERION_SCORE_MISSING",
    "CRITERION_MAX_SCORE_MISSING",
    "CRITERION_FINDING_MISSING",
    "CRITERION_EVIDENCE_REFS_MISSING",
    "CRITERION_ID_DUPLICATE",
    "CRITERION_ID_NOT_REQUIRED",
    "REQUIRED_CRITERION_MISSING",
    "CRITERION_FORBIDDEN_RAW_FIELD_PRESENT",
)

RUBRIC_REVIEW_BUILD_REASON_CODES: Final[tuple[str, ...]] = REASON_CODES

REASON_PRIORITY: Final[tuple[str, ...]] = (
    "RUN_ID_MISSING",
    "RUBRIC_REVIEW_ID_MISSING",
    "REVIEW_KIND_MISSING",
    "ARTIFACT_REFS_MISSING",
    "RUBRIC_CRITERIA_MISSING",
    "REQUIRED_CRITERION_IDS_MISSING",
    "MISSING_CRITERION_IDS_DECLARED",
    "BLOCKING_CRITERION_ID_UNKNOWN",
    "RUBRIC_OUTCOME_MISSING",
    "SCORE_TOTAL_MISSING",
    "SCORE_THRESHOLD_MISSING",
    "CREATED_AT_MISSING",
    "TIMESTAMP_POLICY_MISSING",
    "SOURCE_OF_TRUTH_MISSING",
    "CRITERION_NOT_DICT",
    "CRITERION_KEYS_INVALID",
    "CRITERION_ID_MISSING",
    "CRITERION_ROLE_MISSING",
    "CRITERION_TARGET_ARTIFACT_REF_MISSING",
    "CRITERION_TARGET_ARTIFACT_KIND_MISSING",
    "CRITERION_STATUS_MISSING",
    "CRITERION_SEVERITY_MISSING",
    "CRITERION_SCORE_MISSING",
    "CRITERION_MAX_SCORE_MISSING",
    "CRITERION_FINDING_MISSING",
    "CRITERION_EVIDENCE_REFS_MISSING",
    "CRITERION_ID_DUPLICATE",
    "CRITERION_ID_NOT_REQUIRED",
    "REQUIRED_CRITERION_MISSING",
    "CRITERION_FORBIDDEN_RAW_FIELD_PRESENT",
    "RUBRIC_REVIEW_BUILDABLE",
)

_CRITERION_KEYS: Final[tuple[str, ...]] = (
    "criterion_id",
    "criterion_role",
    "target_artifact_ref",
    "target_artifact_kind",
    "criterion_status",
    "severity",
    "score",
    "max_score",
    "finding",
    "evidence_refs",
    "notes",
)

_CRITERION_STRING_FIELDS: Final[tuple[tuple[str, str], ...]] = (
    ("criterion_id", "CRITERION_ID_MISSING"),
    ("criterion_role", "CRITERION_ROLE_MISSING"),
    ("target_artifact_ref", "CRITERION_TARGET_ARTIFACT_REF_MISSING"),
    ("target_artifact_kind", "CRITERION_TARGET_ARTIFACT_KIND_MISSING"),
    ("criterion_status", "CRITERION_STATUS_MISSING"),
    ("severity", "CRITERION_SEVERITY_MISSING"),
    ("score", "CRITERION_SCORE_MISSING"),
    ("max_score", "CRITERION_MAX_SCORE_MISSING"),
    ("finding", "CRITERION_FINDING_MISSING"),
)

_FORBIDDEN_CRITERION_FIELDS: Final[tuple[str, ...]] = (
    "raw_rubric_output",
    "raw_review_output",
    "review_output",
    "rubric_output",
    "raw_judge_output",
    "judge_output",
    "llm_judge_output",
    "llm_output",
    "raw_llm_output",
    "human_review_output",
    "human_review_result",
    "score_computation",
    "computed_score",
    "computed_total",
    "computed_threshold",
    "score_explanation",
    "raw_score_explanation",
    "quality_pass",
    "rubric_pass",
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
    "audit_result",
    "gate_result",
    "publish_result",
    "should_fetch",
    "should_read_reader",
    "should_read_training_report",
    "should_read_validator_result",
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
    "should_score",
    "should_validate",
    "should_run_validator",
    "should_eval",
    "should_audit",
    "should_gate",
    "should_publish",
    "should_create_public_url",
    "reader_read",
    "training_report_read",
    "validator_result_read",
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
    "rubric_executed",
    "validator_executed",
    "eval_executed",
    "audit_executed",
    "gate_executed",
    "published",
    "public_url_created",
)

_INVARIANT_REFS: Final[tuple[str, ...]] = (
    "rubric_review_builder_only",
    "builder_not_reader_reader",
    "builder_not_training_report_reader",
    "builder_not_validator_result_reader",
    "builder_not_source_manifest_reader",
    "builder_not_source_notes_reader",
    "builder_not_source_reader",
    "builder_not_file_reader",
    "builder_not_web_fetcher",
    "builder_not_github_fetcher",
    "builder_not_rss_fetcher",
    "builder_not_notion_fetcher",
    "builder_not_llm_judge",
    "builder_not_human_reviewer",
    "builder_not_rubric_executor",
    "builder_not_score_computer",
    "builder_not_validator_executor",
    "builder_not_eval_executor",
    "builder_not_audit_executor",
    "builder_not_gate_executor",
    "builder_not_publisher",
    "rubric_criteria_are_caller_supplied",
    "criterion_findings_are_caller_supplied",
    "criterion_scores_are_caller_supplied",
    "artifact_refs_opaque",
    "target_artifact_refs_opaque",
    "evidence_refs_opaque",
    "rubric_review_governance_evidence",
    "rubric_review_not_public_candidate",
    "rubric_outcome_not_quality_pass",
    "rubric_outcome_not_publish_allowed",
    "score_total_not_quality_pass",
    "score_threshold_not_publish_gate",
    "buildable_not_rubric_pass",
    "buildable_not_quality_pass",
    "buildable_not_eval_pass",
    "buildable_not_audit_pass",
    "buildable_not_publish_allowed",
    "buildable_not_public_url_created",
    "blocking_criterion_ids_are_gate_evidence_only",
    "blocking_criterion_ids_do_not_execute_gate",
    "no_reader_read",
    "no_training_report_read",
    "no_validator_result_read",
    "no_source_manifest_read",
    "no_source_notes_read",
    "no_source_content_read",
    "no_url_fetch",
    "no_rss_fetch",
    "no_file_read",
    "no_raw_content",
    "no_raw_url",
    "no_generated_review",
    "no_llm_summary",
    "no_llm_judge",
    "no_human_review_workflow",
    "no_score_computation",
    "no_inferred_fact_generation",
    "no_hash_calculation",
    "no_existing_builder_or_policy_call",
    "no_rubric_execution",
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


def _safe_criterion(criterion: object) -> dict[str, object]:
    if not isinstance(criterion, dict):
        return {
            "criterion_id": "",
            "criterion_role": "",
            "target_artifact_ref": "",
            "target_artifact_kind": "",
            "criterion_status": "",
            "severity": "",
            "score": "",
            "max_score": "",
            "finding": "",
            "evidence_refs": (),
            "notes": (),
        }

    return {
        "criterion_id": _safe_string(criterion.get("criterion_id")),
        "criterion_role": _safe_string(criterion.get("criterion_role")),
        "target_artifact_ref": _safe_string(
            criterion.get("target_artifact_ref")
        ),
        "target_artifact_kind": _safe_string(
            criterion.get("target_artifact_kind")
        ),
        "criterion_status": _safe_string(criterion.get("criterion_status")),
        "severity": _safe_string(criterion.get("severity")),
        "score": _safe_string(criterion.get("score")),
        "max_score": _safe_string(criterion.get("max_score")),
        "finding": _safe_string(criterion.get("finding")),
        "evidence_refs": _safe_string_tuple(criterion.get("evidence_refs")),
        "notes": _safe_string_tuple(criterion.get("notes")),
    }


def _safe_criteria(value: object) -> tuple[dict[str, object], ...]:
    if not isinstance(value, tuple):
        return ()

    criteria = []
    for criterion in value:
        criteria.append(_safe_criterion(criterion))
    return tuple(criteria)


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


def _add_criterion_violation(
    criterion_violations: list[dict[str, object]],
    *,
    criterion_index: int,
    criterion_id: str,
    reason_code: str,
    field: str,
) -> None:
    criterion_violations.append(
        {
            "criterion_index": criterion_index,
            "criterion_id": criterion_id,
            "reason_code": reason_code,
            "field": field,
        }
    )


def _ordered_reason_codes(reason_codes: tuple[str, ...]) -> tuple[str, ...]:
    ordered = []
    for reason_code in REASON_PRIORITY:
        if reason_code == "RUBRIC_REVIEW_BUILDABLE":
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


def _ordered_criterion_violations(
    criterion_violations: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    return tuple(
        sorted(
            criterion_violations,
            key=lambda item: (
                _reason_rank(_safe_string(item.get("reason_code"))),
                item.get("criterion_index"),
                _safe_string(item.get("field")),
            ),
        )
    )


def _criterion_id_from(criterion: object) -> str:
    if not isinstance(criterion, dict):
        return ""
    return _safe_string(criterion.get("criterion_id"))


def _known_criterion_ids(
    rubric_criteria: object,
) -> tuple[str, ...]:
    if not isinstance(rubric_criteria, tuple):
        return ()

    criterion_ids = []
    for criterion in rubric_criteria:
        criterion_id = _criterion_id_from(criterion)
        if _is_nonblank_string(criterion_id):
            criterion_ids.append(criterion_id)
    return tuple(criterion_ids)


def explain_rubric_review_build(
    *,
    run_id: str,
    rubric_review_id: str,
    review_kind: str,
    artifact_refs: tuple[str, ...],
    rubric_criteria: tuple[dict[str, object], ...],
    required_criterion_ids: tuple[str, ...],
    missing_criterion_ids: tuple[str, ...],
    blocking_criterion_ids: tuple[str, ...],
    rubric_outcome: str,
    score_total: str,
    score_threshold: str,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    """Explain whether a caller-supplied rubric review is buildable."""

    reason_codes = []
    field_entries = []
    criterion_violations = []

    if not _is_nonblank_string(run_id):
        _add_reason(reason_codes, "RUN_ID_MISSING")
        _add_field(field_entries, reason_code="RUN_ID_MISSING", field="run_id")

    if not _is_nonblank_string(rubric_review_id):
        _add_reason(reason_codes, "RUBRIC_REVIEW_ID_MISSING")
        _add_field(
            field_entries,
            reason_code="RUBRIC_REVIEW_ID_MISSING",
            field="rubric_review_id",
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

    if not isinstance(rubric_criteria, tuple) or rubric_criteria == ():
        _add_reason(reason_codes, "RUBRIC_CRITERIA_MISSING")
        _add_field(
            field_entries,
            reason_code="RUBRIC_CRITERIA_MISSING",
            field="rubric_criteria",
        )

    if not _is_nonempty_string_tuple(required_criterion_ids):
        _add_reason(reason_codes, "REQUIRED_CRITERION_IDS_MISSING")
        _add_field(
            field_entries,
            reason_code="REQUIRED_CRITERION_IDS_MISSING",
            field="required_criterion_ids",
        )

    if missing_criterion_ids != ():
        _add_reason(reason_codes, "MISSING_CRITERION_IDS_DECLARED")
        _add_field(
            field_entries,
            reason_code="MISSING_CRITERION_IDS_DECLARED",
            field="missing_criterion_ids",
        )

    known_criterion_ids = _known_criterion_ids(rubric_criteria)
    if not isinstance(blocking_criterion_ids, tuple):
        _add_reason(reason_codes, "BLOCKING_CRITERION_ID_UNKNOWN")
        _add_field(
            field_entries,
            reason_code="BLOCKING_CRITERION_ID_UNKNOWN",
            field="blocking_criterion_ids",
        )
    else:
        for blocking_criterion_id in blocking_criterion_ids:
            if (
                not _is_nonblank_string(blocking_criterion_id)
                or blocking_criterion_id not in known_criterion_ids
            ):
                _add_reason(reason_codes, "BLOCKING_CRITERION_ID_UNKNOWN")
                _add_field(
                    field_entries,
                    reason_code="BLOCKING_CRITERION_ID_UNKNOWN",
                    field="blocking_criterion_ids",
                )
                break

    if not _is_nonblank_string(rubric_outcome):
        _add_reason(reason_codes, "RUBRIC_OUTCOME_MISSING")
        _add_field(
            field_entries,
            reason_code="RUBRIC_OUTCOME_MISSING",
            field="rubric_outcome",
        )

    if not _is_nonblank_string(score_total):
        _add_reason(reason_codes, "SCORE_TOTAL_MISSING")
        _add_field(
            field_entries,
            reason_code="SCORE_TOTAL_MISSING",
            field="score_total",
        )

    if not _is_nonblank_string(score_threshold):
        _add_reason(reason_codes, "SCORE_THRESHOLD_MISSING")
        _add_field(
            field_entries,
            reason_code="SCORE_THRESHOLD_MISSING",
            field="score_threshold",
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

    seen_criterion_ids = []
    if isinstance(rubric_criteria, tuple):
        for criterion_index, criterion in enumerate(rubric_criteria):
            criterion_id = _criterion_id_from(criterion)

            if not isinstance(criterion, dict):
                _add_reason(reason_codes, "CRITERION_NOT_DICT")
                _add_field(
                    field_entries,
                    reason_code="CRITERION_NOT_DICT",
                    field=f"rubric_criteria[{criterion_index}]",
                )
                _add_criterion_violation(
                    criterion_violations,
                    criterion_index=criterion_index,
                    criterion_id="",
                    reason_code="CRITERION_NOT_DICT",
                    field="rubric_criteria",
                )
                continue

            criterion_keys = tuple(criterion.keys())
            for key in criterion_keys:
                if key in _FORBIDDEN_CRITERION_FIELDS:
                    _add_reason(
                        reason_codes,
                        "CRITERION_FORBIDDEN_RAW_FIELD_PRESENT",
                    )
                    _add_field(
                        field_entries,
                        reason_code="CRITERION_FORBIDDEN_RAW_FIELD_PRESENT",
                        field=f"rubric_criteria[{criterion_index}].{key}",
                    )
                    _add_criterion_violation(
                        criterion_violations,
                        criterion_index=criterion_index,
                        criterion_id=criterion_id,
                        reason_code=(
                            "CRITERION_FORBIDDEN_RAW_FIELD_PRESENT"
                        ),
                        field=key,
                    )

            if set(criterion_keys) != set(_CRITERION_KEYS):
                _add_reason(reason_codes, "CRITERION_KEYS_INVALID")
                _add_field(
                    field_entries,
                    reason_code="CRITERION_KEYS_INVALID",
                    field=f"rubric_criteria[{criterion_index}].keys",
                )
                _add_criterion_violation(
                    criterion_violations,
                    criterion_index=criterion_index,
                    criterion_id=criterion_id,
                    reason_code="CRITERION_KEYS_INVALID",
                    field="keys",
                )

            for field, missing_reason_code in _CRITERION_STRING_FIELDS:
                if not _is_nonblank_string(criterion.get(field)):
                    _add_reason(reason_codes, missing_reason_code)
                    _add_field(
                        field_entries,
                        reason_code=missing_reason_code,
                        field=f"rubric_criteria[{criterion_index}].{field}",
                    )
                    _add_criterion_violation(
                        criterion_violations,
                        criterion_index=criterion_index,
                        criterion_id=criterion_id,
                        reason_code=missing_reason_code,
                        field=field,
                    )

            if not _is_nonempty_string_tuple(criterion.get("evidence_refs")):
                _add_reason(reason_codes, "CRITERION_EVIDENCE_REFS_MISSING")
                _add_field(
                    field_entries,
                    reason_code="CRITERION_EVIDENCE_REFS_MISSING",
                    field=f"rubric_criteria[{criterion_index}].evidence_refs",
                )
                _add_criterion_violation(
                    criterion_violations,
                    criterion_index=criterion_index,
                    criterion_id=criterion_id,
                    reason_code="CRITERION_EVIDENCE_REFS_MISSING",
                    field="evidence_refs",
                )

            if _is_nonblank_string(criterion_id):
                if criterion_id in seen_criterion_ids:
                    _add_reason(reason_codes, "CRITERION_ID_DUPLICATE")
                    _add_field(
                        field_entries,
                        reason_code="CRITERION_ID_DUPLICATE",
                        field=f"rubric_criteria[{criterion_index}].criterion_id",
                    )
                    _add_criterion_violation(
                        criterion_violations,
                        criterion_index=criterion_index,
                        criterion_id=criterion_id,
                        reason_code="CRITERION_ID_DUPLICATE",
                        field="criterion_id",
                    )
                else:
                    seen_criterion_ids.append(criterion_id)

                if (
                    _is_nonempty_string_tuple(required_criterion_ids)
                    and criterion_id not in required_criterion_ids
                ):
                    _add_reason(reason_codes, "CRITERION_ID_NOT_REQUIRED")
                    _add_field(
                        field_entries,
                        reason_code="CRITERION_ID_NOT_REQUIRED",
                        field=f"rubric_criteria[{criterion_index}].criterion_id",
                    )
                    _add_criterion_violation(
                        criterion_violations,
                        criterion_index=criterion_index,
                        criterion_id=criterion_id,
                        reason_code="CRITERION_ID_NOT_REQUIRED",
                        field="criterion_id",
                    )

    if _is_nonempty_string_tuple(required_criterion_ids):
        for required_criterion_id in required_criterion_ids:
            if required_criterion_id not in known_criterion_ids:
                _add_reason(reason_codes, "REQUIRED_CRITERION_MISSING")
                _add_field(
                    field_entries,
                    reason_code="REQUIRED_CRITERION_MISSING",
                    field=f"required_criterion_ids.{required_criterion_id}",
                )

    rubric_violations = _ordered_reason_codes(tuple(reason_codes))
    missing_or_invalid_fields = _ordered_fields(tuple(field_entries))
    ordered_criterion_violations = _ordered_criterion_violations(
        tuple(criterion_violations)
    )
    buildable = rubric_violations == ()
    reason_code = "RUBRIC_REVIEW_BUILDABLE"
    if not buildable:
        reason_code = rubric_violations[0]

    reason = "Rubric review artifact is buildable."
    if not buildable:
        reason = f"{reason_code} prevents rubric review buildability."

    return {
        "buildable": buildable,
        "reason_code": reason_code,
        "reason": reason,
        "source": {
            "artifact_refs": _safe_string_tuple(artifact_refs),
            "source_of_truth": _safe_string_tuple(source_of_truth),
        },
        "rubric_review": {
            "run_id": _safe_string(run_id),
            "rubric_review_id": _safe_string(rubric_review_id),
            "review_kind": _safe_string(review_kind),
            "artifact_refs": _safe_string_tuple(artifact_refs),
            "rubric_criteria": _safe_criteria(rubric_criteria),
            "required_criterion_ids": _safe_string_tuple(
                required_criterion_ids
            ),
            "missing_criterion_ids": _safe_string_tuple(missing_criterion_ids),
            "blocking_criterion_ids": _safe_string_tuple(
                blocking_criterion_ids
            ),
            "rubric_outcome": _safe_string(rubric_outcome),
            "score_total": _safe_string(score_total),
            "score_threshold": _safe_string(score_threshold),
            "created_at": _safe_string(created_at),
            "timestamp_policy": _safe_string(timestamp_policy),
            "source_of_truth": _safe_string_tuple(source_of_truth),
            "notes": _safe_string_tuple(notes),
        },
        "rubric_violations": rubric_violations,
        "missing_or_invalid_fields": missing_or_invalid_fields,
        "criterion_violations": ordered_criterion_violations,
        "invariant_refs": _INVARIANT_REFS,
    }


def is_rubric_review_buildable(
    *,
    run_id: str,
    rubric_review_id: str,
    review_kind: str,
    artifact_refs: tuple[str, ...],
    rubric_criteria: tuple[dict[str, object], ...],
    required_criterion_ids: tuple[str, ...],
    missing_criterion_ids: tuple[str, ...],
    blocking_criterion_ids: tuple[str, ...],
    rubric_outcome: str,
    score_total: str,
    score_threshold: str,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> bool:
    """Return whether the caller-supplied rubric review is buildable."""

    return bool(
        explain_rubric_review_build(
            run_id=run_id,
            rubric_review_id=rubric_review_id,
            review_kind=review_kind,
            artifact_refs=artifact_refs,
            rubric_criteria=rubric_criteria,
            required_criterion_ids=required_criterion_ids,
            missing_criterion_ids=missing_criterion_ids,
            blocking_criterion_ids=blocking_criterion_ids,
            rubric_outcome=rubric_outcome,
            score_total=score_total,
            score_threshold=score_threshold,
            created_at=created_at,
            timestamp_policy=timestamp_policy,
            source_of_truth=source_of_truth,
            notes=notes,
        )["buildable"]
    )
