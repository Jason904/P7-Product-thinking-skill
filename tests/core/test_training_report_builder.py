import sys
from pathlib import Path


SRC = Path(__file__).parents[2] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


import ai_daily_publishing_system.core.training_report_builder as builder  # noqa: E402
from ai_daily_publishing_system.core.training_report_builder import (  # noqa: E402
    REASON_CODES,
    REASON_PRIORITY,
    TRAINING_REPORT_BUILD_REASON_CODES,
    explain_training_report_build,
    is_training_report_buildable,
)


TOP_LEVEL_KEYS = (
    "buildable",
    "reason_code",
    "reason",
    "source",
    "training_report",
    "report_violations",
    "missing_or_invalid_fields",
    "section_violations",
    "invariant_refs",
)

TRAINING_REPORT_KEYS = (
    "run_id",
    "training_report_id",
    "source_manifest_ref",
    "source_notes_ref",
    "report_sections",
    "required_section_ids",
    "missing_section_ids",
    "redaction_status",
    "created_at",
    "timestamp_policy",
    "source_of_truth",
    "notes",
)

SECTION_KEYS = (
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

FORBIDDEN_SECTION_FIELDS = (
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

REQUIRED_INVARIANT_REFS = (
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

FORBIDDEN_PSEUDO_REASON_CODES = (
    "SOURCE_MANIFEST_READ_FORBIDDEN",
    "SOURCE_NOTES_READ_FORBIDDEN",
    "SOURCE_CONTENT_READ_FORBIDDEN",
    "FILE_READ_FORBIDDEN",
    "WEB_FETCH_FORBIDDEN",
    "GITHUB_FETCH_FORBIDDEN",
    "NOTION_FETCH_FORBIDDEN",
    "LLM_SUMMARY_FORBIDDEN",
    "MARKDOWN_RENDER_FORBIDDEN",
    "TRAINING_REPORT_WRITE_FORBIDDEN",
    "READER_WRITE_FORBIDDEN",
    "PUBLIC_URL_CREATION_FORBIDDEN",
)

FORBIDDEN_MODULE_NAMES = (
    "states",
    "gates",
    "artifacts",
    "source_manifest_builder",
    "source_notes_builder",
    "runtime_context_snapshot_builder",
    "runtime_profile_snapshot_builder",
    "config_snapshot_builder",
    "adapter_preflight_result_builder",
    "adapter_gate_evidence_policy",
    "adapter_gate_decision_policy",
    "daily_gate_evidence_policy",
    "daily_gate_decision_policy",
    "gate_decision_mapper",
    "transition_guard",
    "noop_completion_policy",
    "artifact_inventory_policy",
    "gate_decision_envelope_builder",
    "run_ledger_entry_builder",
    "failure_package_builder",
    "badcase_record_builder",
    "artifact_hash_manifest_builder",
    "publish_ledger_entry_builder",
    "notification_ledger_entry_builder",
    "pathlib",
    "os",
    "datetime",
    "hashlib",
    "logging",
    "subprocess",
    "requests",
)


def _section(section_id):
    return {
        "section_id": section_id,
        "section_role": "analysis",
        "section_title": "Insight",
        "section_text": "Caller supplied training report evidence.",
        "source_refs": ("source-ref-1",),
        "citation_markers": ("[1]",),
        "redaction_status": "redacted",
        "include_in_reader": False,
        "notes": ("caller supplied",),
    }


def _valid_kwargs():
    return {
        "run_id": "run-001",
        "training_report_id": "training-report-001",
        "source_manifest_ref": "manifest-ref-001",
        "source_notes_ref": "notes-ref-001",
        "report_sections": (_section("overview"), _section("takeaways")),
        "required_section_ids": ("overview", "takeaways"),
        "missing_section_ids": (),
        "redaction_status": "redacted",
        "created_at": "2026-07-06T00:00:00Z",
        "timestamp_policy": "caller_supplied",
        "source_of_truth": ("source_manifest_ref", "source_notes_ref"),
        "notes": ("private training report evidence only",),
    }


def _payload_keys(value):
    keys = []
    if isinstance(value, dict):
        for key, nested_value in value.items():
            keys.append(key)
            if key != "invariant_refs":
                keys.extend(_payload_keys(nested_value))
    elif isinstance(value, tuple):
        for nested_value in value:
            keys.extend(_payload_keys(nested_value))
    return tuple(keys)


def test_reason_code_constants_are_stable():
    expected_codes = (
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
    expected_priority = (
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

    assert REASON_CODES == expected_codes
    assert TRAINING_REPORT_BUILD_REASON_CODES == expected_codes
    assert REASON_PRIORITY == expected_priority


def test_explain_training_report_build_returns_buildable_private_evidence_contract():
    result = explain_training_report_build(**_valid_kwargs())

    assert tuple(result) == TOP_LEVEL_KEYS
    assert result["buildable"] is True
    assert result["reason_code"] == "TRAINING_REPORT_BUILDABLE"
    assert result["report_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()
    assert result["section_violations"] == ()
    assert "builder_not_source_manifest_reader" in result["invariant_refs"]
    assert "builder_not_source_notes_reader" in result["invariant_refs"]
    assert "training_report_private_evidence" in result["invariant_refs"]
    assert "include_in_reader_forbidden" in result["invariant_refs"]
    assert set(REQUIRED_INVARIANT_REFS).issubset(result["invariant_refs"])

    training_report = result["training_report"]
    assert tuple(training_report) == TRAINING_REPORT_KEYS
    assert training_report["source_manifest_ref"] == "manifest-ref-001"
    assert training_report["source_notes_ref"] == "notes-ref-001"
    assert training_report["required_section_ids"] == ("overview", "takeaways")
    assert training_report["report_sections"][0]["section_text"] == (
        "Caller supplied training report evidence."
    )

    for section in training_report["report_sections"]:
        assert tuple(section) == SECTION_KEYS
        assert section["include_in_reader"] is False
        assert "content" not in section
        assert "raw_content" not in section
        assert "source_url" not in section
        assert "rendered_markdown" not in section

    assert is_training_report_buildable(**_valid_kwargs()) is True


def test_explain_training_report_build_collects_top_level_violations_by_priority():
    kwargs = _valid_kwargs()
    kwargs.update(
        {
            "run_id": " ",
            "training_report_id": "",
            "source_manifest_ref": " ",
            "source_notes_ref": "",
            "report_sections": (),
            "required_section_ids": (),
            "missing_section_ids": ("overview",),
            "redaction_status": " ",
            "created_at": "",
            "timestamp_policy": " ",
            "source_of_truth": (),
        }
    )

    result = explain_training_report_build(**kwargs)

    assert result["buildable"] is False
    assert result["reason_code"] == "RUN_ID_MISSING"
    assert result["report_violations"] == (
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
    )
    assert result["missing_or_invalid_fields"] == (
        "run_id",
        "training_report_id",
        "source_manifest_ref",
        "source_notes_ref",
        "report_sections",
        "required_section_ids",
        "missing_section_ids",
        "redaction_status",
        "created_at",
        "timestamp_policy",
        "source_of_truth",
    )
    assert is_training_report_buildable(**kwargs) is False


def test_explain_training_report_build_collects_section_violations_without_leaking_raw_fields():
    invalid_section = {
        "section_id": " ",
        "section_role": "",
        "section_title": " ",
        "section_text": "",
        "source_refs": ("",),
        "citation_markers": ("[1]", ""),
        "redaction_status": " ",
        "include_in_reader": "no",
        "notes": (),
        "raw_content": "must not leak",
        "url": "https://example.invalid/must-not-leak",
    }
    include_candidate = _section("overview")
    include_candidate["include_in_reader"] = True
    duplicate_section = _section("overview")
    extra_section = _section("extra")
    kwargs = _valid_kwargs()
    kwargs.update(
        {
            "report_sections": (
                "not-a-section",
                invalid_section,
                include_candidate,
                duplicate_section,
                extra_section,
            ),
            "required_section_ids": ("overview", "takeaways"),
        }
    )

    result = explain_training_report_build(**kwargs)

    assert result["buildable"] is False
    assert result["reason_code"] == "SECTION_NOT_DICT"
    assert result["report_violations"] == (
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
    assert {
        violation["reason_code"] for violation in result["section_violations"]
    } == set(result["report_violations"])
    assert result["section_violations"][0] == {
        "section_index": 0,
        "section_id": "",
        "reason_code": "SECTION_NOT_DICT",
        "field": "report_sections",
    }

    training_report = result["training_report"]
    for section in training_report["report_sections"]:
        assert tuple(section) == SECTION_KEYS
        assert section["include_in_reader"] is False
        assert "raw_content" not in section
        assert "url" not in section


def test_each_missing_section_key_is_rejected_and_normalized_to_exact_shape():
    field_reason_codes = {
        "section_id": "SECTION_ID_MISSING",
        "section_role": "SECTION_ROLE_MISSING",
        "section_title": "SECTION_TITLE_MISSING",
        "section_text": "SECTION_TEXT_MISSING",
        "source_refs": "SECTION_SOURCE_REFS_MISSING",
        "citation_markers": "SECTION_CITATION_MARKERS_MISSING",
        "redaction_status": "SECTION_REDACTION_STATUS_MISSING",
        "include_in_reader": "SECTION_INCLUDE_IN_READER_NOT_BOOL",
    }

    for missing_key in SECTION_KEYS:
        section = _section("overview")
        del section[missing_key]
        kwargs = _valid_kwargs()
        kwargs.update(
            {
                "report_sections": (section,),
                "required_section_ids": ("overview",),
            }
        )

        result = explain_training_report_build(**kwargs)

        assert "SECTION_KEYS_INVALID" in result["report_violations"]
        if missing_key in field_reason_codes:
            assert field_reason_codes[missing_key] in result["report_violations"]
        assert tuple(result["training_report"]["report_sections"][0]) == SECTION_KEYS


def test_source_refs_and_citation_markers_require_non_empty_string_tuples():
    invalid_values = (None, [], (), ("",), ("ref", ""), ("ref", 1))
    field_reason_codes = (
        ("source_refs", "SECTION_SOURCE_REFS_MISSING"),
        ("citation_markers", "SECTION_CITATION_MARKERS_MISSING"),
    )

    for field, reason_code in field_reason_codes:
        for invalid_value in invalid_values:
            section = _section("overview")
            section[field] = invalid_value
            kwargs = _valid_kwargs()
            kwargs.update(
                {
                    "report_sections": (section,),
                    "required_section_ids": ("overview",),
                }
            )

            result = explain_training_report_build(**kwargs)

            assert reason_code in result["report_violations"]


def test_every_forbidden_section_field_is_rejected_and_suppressed():
    for forbidden_field in FORBIDDEN_SECTION_FIELDS:
        section = _section("overview")
        section[forbidden_field] = "forbidden-value"
        kwargs = _valid_kwargs()
        kwargs.update(
            {
                "report_sections": (section,),
                "required_section_ids": ("overview",),
            }
        )

        result = explain_training_report_build(**kwargs)
        normalized_section = result["training_report"]["report_sections"][0]

        assert "SECTION_KEYS_INVALID" in result["report_violations"]
        assert (
            "SECTION_FORBIDDEN_RAW_FIELD_PRESENT"
            in result["report_violations"]
        )
        assert {
            "section_index": 0,
            "section_id": "overview",
            "reason_code": "SECTION_FORBIDDEN_RAW_FIELD_PRESENT",
            "field": forbidden_field,
        } in result["section_violations"]
        assert forbidden_field not in normalized_section


def test_result_payload_excludes_all_forbidden_leakage_and_execution_fields():
    payload_keys = set(_payload_keys(explain_training_report_build(**_valid_kwargs())))

    for forbidden_field in FORBIDDEN_SECTION_FIELDS:
        assert forbidden_field not in payload_keys


def test_forbidden_pseudo_reason_codes_are_absent():
    module_names = set(builder.__dict__)

    for reason_code in FORBIDDEN_PSEUDO_REASON_CODES:
        assert reason_code not in REASON_CODES
        assert reason_code not in module_names


def test_module_namespace_has_no_forbidden_dependencies_or_builder_entrypoint():
    module_names = set(builder.__dict__)

    for forbidden_name in FORBIDDEN_MODULE_NAMES:
        assert forbidden_name not in module_names

    assert "build_training_report" not in module_names
    assert "Final" in module_names
