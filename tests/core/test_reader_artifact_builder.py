"""Tests for the pure reader artifact buildability builder."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import reader_artifact_builder as builder


EXPECTED_RESULT_KEYS = {
    "buildable",
    "reason_code",
    "reason",
    "source",
    "reader_artifact",
    "reader_violations",
    "missing_or_invalid_fields",
    "block_violations",
    "invariant_refs",
}

EXPECTED_READER_ARTIFACT_KEYS = {
    "run_id",
    "reader_artifact_id",
    "training_report_ref",
    "reader_blocks",
    "required_block_ids",
    "missing_block_ids",
    "redaction_status",
    "public_candidate_policy",
    "created_at",
    "timestamp_policy",
    "source_of_truth",
    "notes",
}

EXPECTED_BLOCK_KEYS = {
    "block_id",
    "block_role",
    "block_title",
    "block_text",
    "training_report_section_refs",
    "citation_markers",
    "redaction_status",
    "notes",
}

BLOCK_VIOLATION_KEYS = {
    "block_index",
    "block_id",
    "reason_code",
    "field",
}

MISSING_BLOCK_KEY_EXPECTATIONS = (
    ("block_id", "BLOCK_ID_MISSING"),
    ("block_role", "BLOCK_ROLE_MISSING"),
    ("block_title", "BLOCK_TITLE_MISSING"),
    ("block_text", "BLOCK_TEXT_MISSING"),
    (
        "training_report_section_refs",
        "BLOCK_TRAINING_REPORT_SECTION_REFS_MISSING",
    ),
    ("citation_markers", "BLOCK_CITATION_MARKERS_MISSING"),
    ("redaction_status", "BLOCK_REDACTION_STATUS_MISSING"),
    ("notes", "BLOCK_KEYS_INVALID"),
)

EXPECTED_REASON_CODES = (
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

EXPECTED_REASON_PRIORITY = EXPECTED_REASON_CODES[1:] + (
    "READER_ARTIFACT_BUILDABLE",
)

REQUIRED_INVARIANT_REFS = (
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

FORBIDDEN_FIELDS = (
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


def _block(**overrides):
    values = {
        "block_id": "block-001",
        "block_role": "summary",
        "block_title": "Reader insight",
        "block_text": "Caller supplied reader block.",
        "training_report_section_refs": ("section-001",),
        "citation_markers": ("section-001#note-001",),
        "redaction_status": "pass",
        "notes": ("shape-only",),
    }
    values.update(overrides)
    return values


def _valid_values():
    return {
        "run_id": "run-001",
        "reader_artifact_id": "reader-artifact-001",
        "training_report_ref": "training-report-001",
        "reader_blocks": (_block(),),
        "required_block_ids": ("block-001",),
        "missing_block_ids": (),
        "redaction_status": "pass",
        "public_candidate_policy": "reader_html_only_public_candidate_no_url",
        "created_at": "caller-supplied-created-at",
        "timestamp_policy": "caller_supplied_no_datetime_parsing",
        "source_of_truth": ("p2d-27",),
        "notes": ("structured-only",),
    }


def _explain(**overrides):
    values = _valid_values()
    values.update(overrides)
    return builder.explain_reader_artifact_build(**values)


def _all_nested_keys(value):
    keys = set()
    if isinstance(value, dict):
        keys.update(value)
        for nested_value in value.values():
            keys.update(_all_nested_keys(nested_value))
    elif isinstance(value, tuple):
        for nested_value in value:
            keys.update(_all_nested_keys(nested_value))
    return keys


def test_reason_code_constants_are_exact_and_stably_prioritized():
    assert builder.REASON_CODES == EXPECTED_REASON_CODES
    assert builder.READER_ARTIFACT_BUILD_REASON_CODES == EXPECTED_REASON_CODES
    assert builder.REASON_PRIORITY == EXPECTED_REASON_PRIORITY


def test_valid_reader_artifact_is_buildable_with_exact_result_shapes():
    result = _explain()

    assert result["buildable"] is True
    assert result["reason_code"] == "READER_ARTIFACT_BUILDABLE"
    assert result["reader_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()
    assert result["block_violations"] == ()
    assert set(result) == EXPECTED_RESULT_KEYS
    assert set(result["source"]) == {"training_report_ref", "source_of_truth"}
    assert set(result["reader_artifact"]) == EXPECTED_READER_ARTIFACT_KEYS
    assert set(result["reader_artifact"]["reader_blocks"][0]) == EXPECTED_BLOCK_KEYS
    assert result["reader_artifact"]["reader_blocks"][0]["block_text"] == (
        "Caller supplied reader block."
    )
    assert result["source"] == {
        "training_report_ref": "training-report-001",
        "source_of_truth": ("p2d-27",),
    }


def test_boolean_api_is_a_buildability_projection():
    values = _valid_values()

    assert builder.is_reader_artifact_buildable(**values) is True
    values["run_id"] = " "
    assert builder.is_reader_artifact_buildable(**values) is False


def test_public_apis_are_keyword_only():
    values = _valid_values()
    positional_values = tuple(values.values())

    for function in (
        builder.explain_reader_artifact_build,
        builder.is_reader_artifact_buildable,
    ):
        try:
            function(*positional_values)
        except TypeError:
            pass
        else:
            assert False, "public API accepted positional arguments"


def test_required_top_level_fields_report_their_reason_codes():
    cases = (
        ("run_id", " ", "RUN_ID_MISSING"),
        ("reader_artifact_id", "", "READER_ARTIFACT_ID_MISSING"),
        ("training_report_ref", "\t", "TRAINING_REPORT_REF_MISSING"),
        ("reader_blocks", (), "READER_BLOCKS_MISSING"),
        ("reader_blocks", [], "READER_BLOCKS_MISSING"),
        ("required_block_ids", (), "REQUIRED_BLOCK_IDS_MISSING"),
        ("required_block_ids", [], "REQUIRED_BLOCK_IDS_MISSING"),
        ("missing_block_ids", ("block-001",), "MISSING_BLOCK_IDS_DECLARED"),
        ("redaction_status", " ", "REDACTION_STATUS_MISSING"),
        (
            "public_candidate_policy",
            "",
            "PUBLIC_CANDIDATE_POLICY_MISSING",
        ),
        ("created_at", "\n", "CREATED_AT_MISSING"),
        ("timestamp_policy", "", "TIMESTAMP_POLICY_MISSING"),
        ("source_of_truth", (), "SOURCE_OF_TRUTH_MISSING"),
        ("source_of_truth", [], "SOURCE_OF_TRUTH_MISSING"),
    )

    for field, invalid_value, reason_code in cases:
        result = _explain(**{field: invalid_value})
        assert result["buildable"] is False
        assert reason_code in result["reader_violations"]
        assert field in result["missing_or_invalid_fields"]


def test_training_report_ref_and_public_policy_remain_opaque():
    result = _explain(
        training_report_ref="opaque://not-read-or-fetched",
        public_candidate_policy="opaque-policy-marker",
    )

    assert result["buildable"] is True
    assert result["source"]["training_report_ref"] == (
        "opaque://not-read-or-fetched"
    )
    assert result["reader_artifact"]["public_candidate_policy"] == (
        "opaque-policy-marker"
    )


def test_non_dict_block_is_rejected_and_normalized_to_the_exact_shape():
    result = _explain(reader_blocks=("not-a-dict",))

    assert result["reason_code"] == "BLOCK_NOT_DICT"
    assert result["reader_violations"] == (
        "BLOCK_NOT_DICT",
        "REQUIRED_BLOCK_MISSING",
    )
    assert set(result["reader_artifact"]["reader_blocks"][0]) == EXPECTED_BLOCK_KEYS
    assert set(result["block_violations"][0]) == {
        "block_index",
        "block_id",
        "reason_code",
        "field",
    }


def test_each_missing_block_key_is_rejected_and_normalized_to_exact_shape():
    for missing_key, expected_reason in MISSING_BLOCK_KEY_EXPECTATIONS:
        incomplete_block = _block()
        del incomplete_block[missing_key]

        result = _explain(reader_blocks=(incomplete_block,))
        normalized_block = result["reader_artifact"]["reader_blocks"][0]

        assert result["buildable"] is False
        assert "BLOCK_KEYS_INVALID" in result["reader_violations"]
        assert expected_reason in result["reader_violations"]
        assert (
            missing_key in result["missing_or_invalid_fields"]
            or "reader_blocks" in result["missing_or_invalid_fields"]
        )
        assert set(normalized_block) == EXPECTED_BLOCK_KEYS
        assert set(normalized_block) - EXPECTED_BLOCK_KEYS == set()
        assert all(
            set(violation) == BLOCK_VIOLATION_KEYS
            for violation in result["block_violations"]
        )


def test_extra_block_keys_are_rejected_without_leaking_extras():
    extra_key = _block(extra_metadata="not-returned")
    extra_result = _explain(reader_blocks=(extra_key,))

    assert "BLOCK_KEYS_INVALID" in extra_result["reader_violations"]
    assert "extra_metadata" not in _all_nested_keys(extra_result)
    assert set(extra_result["reader_artifact"]["reader_blocks"][0]) == (
        EXPECTED_BLOCK_KEYS
    )


def test_required_block_string_fields_must_be_non_empty_strings():
    cases = (
        ("block_id", " ", "BLOCK_ID_MISSING"),
        ("block_role", "", "BLOCK_ROLE_MISSING"),
        ("block_title", "\t", "BLOCK_TITLE_MISSING"),
        ("block_text", "", "BLOCK_TEXT_MISSING"),
        ("redaction_status", "\n", "BLOCK_REDACTION_STATUS_MISSING"),
    )

    for field, invalid_value, reason_code in cases:
        result = _explain(reader_blocks=(_block(**{field: invalid_value}),))
        assert reason_code in result["reader_violations"]
        assert field in result["missing_or_invalid_fields"]


def test_block_text_is_non_empty_and_caller_supplied():
    supplied_text = "A caller-composed observation; do not summarize it."
    result = _explain(reader_blocks=(_block(block_text=supplied_text),))

    assert result["buildable"] is True
    assert result["reader_artifact"]["reader_blocks"][0]["block_text"] == (
        supplied_text
    )


def test_training_report_section_refs_are_non_empty_opaque_string_tuples():
    invalid_values = (
        (),
        [],
        ("",),
        (" ",),
        ("section-001", 2),
    )

    for invalid_value in invalid_values:
        result = _explain(
            reader_blocks=(
                _block(training_report_section_refs=invalid_value),
            )
        )
        assert "BLOCK_TRAINING_REPORT_SECTION_REFS_MISSING" in (
            result["reader_violations"]
        )

    opaque = ("opaque-section-ref", "not-a-file-read")
    valid = _explain(
        reader_blocks=(_block(training_report_section_refs=opaque),)
    )
    assert valid["buildable"] is True
    assert valid["reader_artifact"]["reader_blocks"][0][
        "training_report_section_refs"
    ] == opaque


def test_citation_markers_are_non_empty_opaque_string_tuples():
    invalid_values = (
        (),
        [],
        ("",),
        ("\t",),
        ("citation-001", None),
    )

    for invalid_value in invalid_values:
        result = _explain(
            reader_blocks=(_block(citation_markers=invalid_value),)
        )
        assert "BLOCK_CITATION_MARKERS_MISSING" in result["reader_violations"]

    opaque = ("section-001#marker-001",)
    valid = _explain(reader_blocks=(_block(citation_markers=opaque),))
    assert valid["buildable"] is True
    assert valid["reader_artifact"]["reader_blocks"][0][
        "citation_markers"
    ] == opaque


def test_block_ids_must_be_unique():
    duplicate = _block(block_title="Duplicate")
    result = _explain(reader_blocks=(_block(), duplicate))

    assert result["reason_code"] == "BLOCK_ID_DUPLICATE"
    assert "BLOCK_ID_DUPLICATE" in result["reader_violations"]
    assert all(
        set(violation)
        == {"block_index", "block_id", "reason_code", "field"}
        for violation in result["block_violations"]
    )


def test_block_id_must_be_required():
    result = _explain(
        reader_blocks=(_block(block_id="block-unexpected"),),
    )

    assert "BLOCK_ID_NOT_REQUIRED" in result["reader_violations"]
    assert "REQUIRED_BLOCK_MISSING" in result["reader_violations"]


def test_every_required_block_id_must_have_a_block():
    result = _explain(
        required_block_ids=("block-001", "block-002"),
    )

    assert result["reason_code"] == "REQUIRED_BLOCK_MISSING"
    assert result["block_violations"][-1] == {
        "block_index": -1,
        "block_id": "block-002",
        "reason_code": "REQUIRED_BLOCK_MISSING",
        "field": "required_block_ids",
    }


def test_forbidden_raw_render_path_url_and_execution_fields_are_rejected():
    for forbidden_field in FORBIDDEN_FIELDS:
        block = _block()
        block[forbidden_field] = "must-not-leak"
        result = _explain(reader_blocks=(block,))

        assert "BLOCK_FORBIDDEN_RAW_FIELD_PRESENT" in (
            result["reader_violations"]
        )
        assert forbidden_field in result["missing_or_invalid_fields"]
        assert forbidden_field not in _all_nested_keys(result)


def test_result_contains_no_raw_html_markdown_source_or_public_url_leakage():
    prohibited_groups = (
        {
            "html",
            "raw_html",
            "rendered_html",
            "reader_html",
            "reader_html_content",
        },
        {
            "markdown",
            "raw_markdown",
            "rendered_markdown",
            "report_markdown",
        },
        {
            "training_report",
            "source_manifest",
            "source_notes",
            "source_content",
            "raw_content",
        },
        {
            "public_url",
            "publish_url",
            "deployment_url",
            "hosting_target",
        },
        {
            "credentials",
            "env_vars",
            "config",
            "adapter_outputs",
            "driver_object",
        },
        {
            "should_fetch",
            "should_read_source",
            "should_render_html",
            "should_write_reader",
            "should_publish",
            "should_create_public_url",
        },
        {
            "reader_written",
            "published",
            "public_url_created",
            "publish_result",
            "reader_write_result",
        },
    )
    result_keys = _all_nested_keys(_explain())

    for prohibited_group in prohibited_groups:
        assert result_keys.isdisjoint(prohibited_group)


def test_all_violations_are_collected_in_global_reason_priority_order():
    invalid_block = {
        "block_id": "duplicate",
        "block_role": "",
        "block_title": "",
        "block_text": "",
        "training_report_section_refs": (),
        "citation_markers": (),
        "redaction_status": "",
        "raw_html": "<p>forbidden</p>",
    }
    result = _explain(
        run_id="",
        reader_artifact_id="",
        training_report_ref="",
        reader_blocks=(invalid_block, dict(invalid_block)),
        required_block_ids=("required",),
        missing_block_ids=("declared-missing",),
        redaction_status="",
        public_candidate_policy="",
        created_at="",
        timestamp_policy="",
        source_of_truth=(),
    )

    assert result["reader_violations"] == (
        "RUN_ID_MISSING",
        "READER_ARTIFACT_ID_MISSING",
        "TRAINING_REPORT_REF_MISSING",
        "MISSING_BLOCK_IDS_DECLARED",
        "REDACTION_STATUS_MISSING",
        "PUBLIC_CANDIDATE_POLICY_MISSING",
        "CREATED_AT_MISSING",
        "TIMESTAMP_POLICY_MISSING",
        "SOURCE_OF_TRUTH_MISSING",
        "BLOCK_KEYS_INVALID",
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
    assert result["reason_code"] == "RUN_ID_MISSING"
    assert result["buildable"] is False
    assert tuple(
        builder.REASON_PRIORITY.index(code)
        for code in result["reader_violations"]
    ) == tuple(
        sorted(
            builder.REASON_PRIORITY.index(code)
            for code in result["reader_violations"]
        )
    )


def test_invariant_refs_cover_reader_public_candidate_boundaries():
    result = _explain()

    assert isinstance(result["invariant_refs"], tuple)
    assert set(REQUIRED_INVARIANT_REFS).issubset(
        set(result["invariant_refs"])
    )
