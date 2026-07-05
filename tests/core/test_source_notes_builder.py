"""Focused contract tests for the pure Source Notes builder."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import source_notes_builder as builder


RESULT_KEYS = (
    "buildable",
    "reason_code",
    "reason",
    "source",
    "source_notes",
    "notes_violations",
    "missing_or_invalid_fields",
    "entry_violations",
    "invariant_refs",
)

SOURCE_NOTES_KEYS = (
    "run_id",
    "source_notes_id",
    "source_manifest_ref",
    "note_entries",
    "required_source_refs",
    "missing_source_refs",
    "redaction_status",
    "created_at",
    "timestamp_policy",
    "source_of_truth",
    "notes",
)

NOTE_ENTRY_KEYS = (
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

REASON_CODES = (
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

REASON_PRIORITY = (
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

FORBIDDEN_ENTRY_FIELDS = (
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


def _name(*parts: str) -> str:
    return "_".join(parts)


FORBIDDEN_PSEUDO_REASON_CODES = (
    _name("SOURCE", "MANIFEST", "READ", "FORBIDDEN"),
    _name("SOURCE", "CONTENT", "READ", "FORBIDDEN"),
    _name("FILE", "READ", "FORBIDDEN"),
    _name("WEB", "FETCH", "FORBIDDEN"),
    _name("GITHUB", "FETCH", "FORBIDDEN"),
    _name("NOTION", "FETCH", "FORBIDDEN"),
    _name("LLM", "SUMMARY", "FORBIDDEN"),
    _name("MARKDOWN", "RENDER", "FORBIDDEN"),
    _name("SOURCE", "NOTES", "WRITE", "FORBIDDEN"),
    _name("TRAINING", "REPORT", "WRITE", "FORBIDDEN"),
    _name("READER", "WRITE", "FORBIDDEN"),
    _name("PUBLIC", "URL", "CREATION", "FORBIDDEN"),
)

FORBIDDEN_MODULE_NAMES = (
    "states",
    "gates",
    "artifacts",
    _name("source", "manifest", "builder"),
    _name("runtime", "context", "snapshot", "builder"),
    _name("runtime", "profile", "snapshot", "builder"),
    _name("config", "snapshot", "builder"),
    _name("adapter", "preflight", "result", "builder"),
    _name("adapter", "gate", "evidence", "policy"),
    _name("adapter", "gate", "decision", "policy"),
    _name("daily", "gate", "evidence", "policy"),
    _name("daily", "gate", "decision", "policy"),
    _name("gate", "decision", "mapper"),
    _name("transition", "guard"),
    _name("noop", "completion", "policy"),
    "pathlib",
    "os",
    "date" + "time",
    "hash" + "lib",
    "logging",
    "sub" + "process",
    "request" + "s",
)


def _note(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "note_id": "note-001",
        "source_ref": "source-001",
        "evidence_role": "primary",
        "note_kind": "observation",
        "note_text": "Caller supplied note.",
        "citation_marker": "source-001#note-001",
        "redaction_status": "pass",
        "include_in_training_report": True,
        "include_in_reader": False,
        "notes": ("shape-only",),
    }
    values.update(overrides)
    return values


def _valid_values() -> dict[str, object]:
    return {
        "run_id": "run-001",
        "source_notes_id": "source-notes-001",
        "source_manifest_ref": "source-manifest-001",
        "note_entries": (_note(),),
        "required_source_refs": ("source-001",),
        "missing_source_refs": (),
        "redaction_status": "pass",
        "created_at": "caller-supplied-created-at",
        "timestamp_policy": "caller_supplied_no_datetime_parsing",
        "source_of_truth": ("p2d-25",),
        "notes": ("structured-only",),
    }


def _explain(**overrides: object) -> dict[str, object]:
    values = _valid_values()
    values.update(overrides)
    return builder.explain_source_notes_build(**values)


def _payload_keys(value: object) -> tuple[str, ...]:
    keys: list[str] = []
    if isinstance(value, dict):
        for key, nested_value in value.items():
            keys.append(key)
            if key != "invariant_refs":
                keys.extend(_payload_keys(nested_value))
    elif isinstance(value, tuple):
        for nested_value in value:
            keys.extend(_payload_keys(nested_value))
    return tuple(keys)


def test_valid_source_notes_are_buildable():
    result = _explain()

    assert result["buildable"] is True
    assert result["reason_code"] == "SOURCE_NOTES_BUILDABLE"
    assert result["reason"] == (
        "Source notes are buildable from caller-supplied structured notes."
    )
    assert result["source"] == "caller_supplied_source_notes_arguments"
    assert result["notes_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()
    assert result["entry_violations"] == ()
    assert result["source_notes"]["note_entries"][0]["note_text"] == (
        "Caller supplied note."
    )


def test_public_api_is_keyword_only():
    values = tuple(_valid_values().values())

    try:
        builder.explain_source_notes_build(*values)
    except TypeError as exc:
        assert "positional" in str(exc)
    else:
        assert False

    try:
        builder.is_source_notes_buildable(*values)
    except TypeError as exc:
        assert "positional" in str(exc)
    else:
        assert False


def test_result_source_notes_and_note_entry_shapes_are_exact():
    result = _explain()
    source_notes = result["source_notes"]
    note_entry = source_notes["note_entries"][0]

    assert tuple(result.keys()) == RESULT_KEYS
    assert set(result) == set(RESULT_KEYS)
    assert tuple(source_notes.keys()) == SOURCE_NOTES_KEYS
    assert set(source_notes) == set(SOURCE_NOTES_KEYS)
    assert tuple(note_entry.keys()) == NOTE_ENTRY_KEYS
    assert set(note_entry) == set(NOTE_ENTRY_KEYS)


def test_required_top_level_field_violations_are_collected():
    cases = (
        ("run_id", " ", "RUN_ID_MISSING"),
        ("source_notes_id", "", "SOURCE_NOTES_ID_MISSING"),
        ("source_manifest_ref", " ", "SOURCE_MANIFEST_REF_MISSING"),
        ("note_entries", (), "NOTE_ENTRIES_MISSING"),
        ("required_source_refs", (), "REQUIRED_SOURCE_REFS_MISSING"),
        (
            "missing_source_refs",
            ("source-001",),
            "MISSING_SOURCE_REFS_DECLARED",
        ),
        ("redaction_status", "", "REDACTION_STATUS_MISSING"),
        ("created_at", " ", "CREATED_AT_MISSING"),
        ("timestamp_policy", "", "TIMESTAMP_POLICY_MISSING"),
        ("source_of_truth", (), "SOURCE_OF_TRUTH_MISSING"),
    )

    for field, invalid_value, reason_code in cases:
        result = _explain(**{field: invalid_value})

        assert result["buildable"] is False
        assert reason_code in result["notes_violations"]
        assert field in result["missing_or_invalid_fields"]


def test_source_manifest_ref_is_preserved_as_an_opaque_non_empty_ref():
    result = _explain(source_manifest_ref="opaque://manifest/ref#v1")

    assert result["buildable"] is True
    assert result["source_notes"]["source_manifest_ref"] == (
        "opaque://manifest/ref#v1"
    )
    assert "source_manifest" not in result["source_notes"]


def test_non_dict_note_entry_is_rejected_and_normalized():
    result = _explain(note_entries=("not-a-dict",))
    entry = result["source_notes"]["note_entries"][0]

    assert result["reason_code"] == "ENTRY_NOT_DICT"
    assert "ENTRY_NOT_DICT" in result["notes_violations"]
    assert "note_entries" in result["missing_or_invalid_fields"]
    assert tuple(entry.keys()) == NOTE_ENTRY_KEYS
    assert entry == {
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
    assert {
        "entry_index": 0,
        "note_id": "",
        "source_ref": "",
        "reason_code": "ENTRY_NOT_DICT",
        "field": "note_entries",
    } in result["entry_violations"]


def test_missing_note_entry_keys_have_shape_and_field_violations():
    cases = (
        ("note_id", "ENTRY_NOTE_ID_MISSING"),
        ("source_ref", "ENTRY_SOURCE_REF_MISSING"),
        ("evidence_role", "ENTRY_EVIDENCE_ROLE_MISSING"),
        ("note_kind", "ENTRY_NOTE_KIND_MISSING"),
        ("note_text", "ENTRY_NOTE_TEXT_MISSING"),
        ("citation_marker", "ENTRY_CITATION_MARKER_MISSING"),
        ("redaction_status", "ENTRY_REDACTION_STATUS_MISSING"),
        (
            "include_in_training_report",
            "ENTRY_INCLUDE_IN_TRAINING_REPORT_NOT_BOOL",
        ),
        ("include_in_reader", "ENTRY_INCLUDE_IN_READER_NOT_BOOL"),
        ("notes", "ENTRY_KEYS_INVALID"),
    )

    for field, expected_reason in cases:
        entry = _note()
        del entry[field]
        result = _explain(note_entries=(entry,))

        assert "ENTRY_KEYS_INVALID" in result["notes_violations"]
        assert expected_reason in result["notes_violations"]
        assert "note_entry_keys" in result["missing_or_invalid_fields"]
        if field != "notes":
            assert field in result["missing_or_invalid_fields"]
        assert tuple(
            result["source_notes"]["note_entries"][0].keys()
        ) == NOTE_ENTRY_KEYS


def test_required_note_entry_strings_must_be_non_empty():
    cases = (
        ("note_id", "ENTRY_NOTE_ID_MISSING"),
        ("source_ref", "ENTRY_SOURCE_REF_MISSING"),
        ("evidence_role", "ENTRY_EVIDENCE_ROLE_MISSING"),
        ("note_kind", "ENTRY_NOTE_KIND_MISSING"),
        ("note_text", "ENTRY_NOTE_TEXT_MISSING"),
        ("citation_marker", "ENTRY_CITATION_MARKER_MISSING"),
        ("redaction_status", "ENTRY_REDACTION_STATUS_MISSING"),
    )

    for field, expected_reason in cases:
        result = _explain(note_entries=(_note(**{field: " "}),))

        assert expected_reason in result["notes_violations"]
        assert field in result["missing_or_invalid_fields"]


def test_note_id_must_be_unique():
    duplicate = _note(
        source_ref="source-002",
        citation_marker="source-002#note-001",
    )
    result = _explain(
        note_entries=(_note(), duplicate),
        required_source_refs=("source-001", "source-002"),
    )

    assert "ENTRY_NOTE_ID_DUPLICATE" in result["notes_violations"]
    assert {
        "entry_index": 1,
        "note_id": "note-001",
        "source_ref": "source-002",
        "reason_code": "ENTRY_NOTE_ID_DUPLICATE",
        "field": "note_id",
    } in result["entry_violations"]


def test_source_ref_must_be_required():
    result = _explain(
        note_entries=(
            _note(
                source_ref="source-optional",
                citation_marker="source-optional#note-001",
            ),
        )
    )

    assert "ENTRY_SOURCE_REF_NOT_REQUIRED" in result["notes_violations"]
    assert "REQUIRED_SOURCE_REF_NOTE_MISSING" in result["notes_violations"]
    assert "source_ref" in result["missing_or_invalid_fields"]


def test_every_required_source_ref_must_have_a_note_entry():
    result = _explain(
        required_source_refs=("source-001", "source-002"),
    )

    assert "REQUIRED_SOURCE_REF_NOTE_MISSING" in result["notes_violations"]
    assert {
        "entry_index": -1,
        "note_id": "",
        "source_ref": "source-002",
        "reason_code": "REQUIRED_SOURCE_REF_NOTE_MISSING",
        "field": "required_source_refs",
    } in result["entry_violations"]


def test_note_text_and_citation_marker_remain_caller_supplied_and_opaque():
    result = _explain(
        note_entries=(
            _note(
                note_text="Exact caller note; do not summarize.",
                citation_marker="opaque-citation://source-001#L4",
            ),
        )
    )
    entry = result["source_notes"]["note_entries"][0]

    assert result["buildable"] is True
    assert entry["note_text"] == "Exact caller note; do not summarize."
    assert entry["citation_marker"] == "opaque-citation://source-001#L4"
    assert "generated_summary" not in entry
    assert "llm_summary" not in entry


def test_include_markers_are_boolean_and_reader_must_remain_false():
    training_result = _explain(
        note_entries=(_note(include_in_training_report="yes"),)
    )
    reader_type_result = _explain(
        note_entries=(_note(include_in_reader=0),)
    )
    reader_true_result = _explain(
        note_entries=(_note(include_in_reader=True),)
    )
    training_false_result = _explain(
        note_entries=(_note(include_in_training_report=False),)
    )

    assert (
        "ENTRY_INCLUDE_IN_TRAINING_REPORT_NOT_BOOL"
        in training_result["notes_violations"]
    )
    assert (
        "ENTRY_INCLUDE_IN_READER_NOT_BOOL"
        in reader_type_result["notes_violations"]
    )
    assert "INCLUDE_IN_READER_TRUE" in reader_true_result["notes_violations"]
    assert training_false_result["buildable"] is True


def test_forbidden_raw_render_content_path_url_fetch_and_write_fields_block():
    for forbidden_field in FORBIDDEN_ENTRY_FIELDS:
        entry = _note(**{forbidden_field: "forbidden-value"})
        result = _explain(note_entries=(entry,))
        normalized_entry = result["source_notes"]["note_entries"][0]

        assert "ENTRY_KEYS_INVALID" in result["notes_violations"]
        assert (
            "ENTRY_FORBIDDEN_RAW_FIELD_PRESENT"
            in result["notes_violations"]
        )
        assert "forbidden_raw_field" in result["missing_or_invalid_fields"]
        assert forbidden_field not in normalized_entry


def test_result_payload_excludes_forbidden_leakage_and_execution_flags():
    result = _explain()
    payload_keys = set(_payload_keys(result))

    for forbidden_field in FORBIDDEN_ENTRY_FIELDS:
        assert forbidden_field not in payload_keys

    assert "rendered_markdown" not in payload_keys
    assert "source_manifest" not in payload_keys
    assert "source_content" not in payload_keys
    assert "raw_content" not in payload_keys
    assert "public_url" not in payload_keys
    assert "credentials" not in payload_keys
    assert "raw_credentials" not in payload_keys
    assert "env_vars" not in payload_keys
    assert "raw_config" not in payload_keys
    assert "adapter_outputs" not in payload_keys
    assert "driver_object" not in payload_keys


def test_reason_priority_collects_all_applicable_violations():
    invalid_entry = _note(
        note_id="",
        source_ref="source-other",
        evidence_role="",
        note_kind="",
        note_text="",
        citation_marker="",
        redaction_status="",
        include_in_training_report="yes",
        include_in_reader=True,
        raw_content="forbidden",
    )
    duplicate_entry = _note(
        note_id="duplicate-note",
        source_ref="source-other-2",
        citation_marker="other-2#duplicate",
    )
    duplicate_again = _note(
        note_id="duplicate-note",
        source_ref="source-other-3",
        citation_marker="other-3#duplicate",
    )
    result = _explain(
        run_id="",
        source_notes_id="",
        source_manifest_ref="",
        note_entries=(
            "not-a-dict",
            invalid_entry,
            duplicate_entry,
            duplicate_again,
        ),
        required_source_refs=("source-required",),
        missing_source_refs=("source-required",),
        redaction_status="",
        created_at="",
        timestamp_policy="",
        source_of_truth=(),
    )

    assert result["reason_code"] == result["notes_violations"][0]
    assert result["notes_violations"] == (
        "RUN_ID_MISSING",
        "SOURCE_NOTES_ID_MISSING",
        "SOURCE_MANIFEST_REF_MISSING",
        "MISSING_SOURCE_REFS_DECLARED",
        "REDACTION_STATUS_MISSING",
        "CREATED_AT_MISSING",
        "TIMESTAMP_POLICY_MISSING",
        "SOURCE_OF_TRUTH_MISSING",
        "ENTRY_NOT_DICT",
        "ENTRY_KEYS_INVALID",
        "ENTRY_NOTE_ID_MISSING",
        "ENTRY_EVIDENCE_ROLE_MISSING",
        "ENTRY_NOTE_KIND_MISSING",
        "ENTRY_NOTE_TEXT_MISSING",
        "ENTRY_CITATION_MARKER_MISSING",
        "ENTRY_REDACTION_STATUS_MISSING",
        "ENTRY_INCLUDE_IN_TRAINING_REPORT_NOT_BOOL",
        "INCLUDE_IN_READER_TRUE",
        "ENTRY_NOTE_ID_DUPLICATE",
        "ENTRY_SOURCE_REF_NOT_REQUIRED",
        "REQUIRED_SOURCE_REF_NOTE_MISSING",
        "ENTRY_FORBIDDEN_RAW_FIELD_PRESENT",
    )


def test_empty_collections_follow_declared_reason_priority():
    result = _explain(
        run_id="",
        source_notes_id="",
        source_manifest_ref="",
        note_entries=(),
        required_source_refs=(),
    )

    assert result["notes_violations"][:5] == (
        "RUN_ID_MISSING",
        "SOURCE_NOTES_ID_MISSING",
        "SOURCE_MANIFEST_REF_MISSING",
        "NOTE_ENTRIES_MISSING",
        "REQUIRED_SOURCE_REFS_MISSING",
    )


def test_missing_or_invalid_fields_are_stable_and_unique():
    result = _explain(
        run_id="",
        note_entries=(
            _note(note_id="", note_text=""),
            _note(
                note_id="",
                source_ref="source-002",
                note_text="",
                citation_marker="source-002#blank",
            ),
        ),
        required_source_refs=("source-001", "source-002"),
    )

    assert result["missing_or_invalid_fields"] == (
        "run_id",
        "note_id",
        "note_text",
    )


def test_entry_violations_have_stable_record_shape():
    result = _explain(
        note_entries=(
            _note(note_text=""),
            _note(
                note_id="note-002",
                source_ref="source-other",
                citation_marker="source-other#note-002",
            ),
        ),
    )

    for record in result["entry_violations"]:
        assert tuple(record.keys()) == (
            "entry_index",
            "note_id",
            "source_ref",
            "reason_code",
            "field",
        )

    assert {
        "entry_index": 0,
        "note_id": "note-001",
        "source_ref": "source-001",
        "reason_code": "ENTRY_NOTE_TEXT_MISSING",
        "field": "note_text",
    } in result["entry_violations"]
    assert {
        "entry_index": 1,
        "note_id": "note-002",
        "source_ref": "source-other",
        "reason_code": "ENTRY_SOURCE_REF_NOT_REQUIRED",
        "field": "source_ref",
    } in result["entry_violations"]


def test_bool_wrapper_matches_explanation_buildable_flag():
    valid_values = _valid_values()
    invalid_values = _valid_values()
    invalid_values["source_notes_id"] = ""

    assert builder.is_source_notes_buildable(**valid_values) is (
        builder.explain_source_notes_build(**valid_values)["buildable"]
    )
    assert builder.is_source_notes_buildable(**invalid_values) is (
        builder.explain_source_notes_build(**invalid_values)["buildable"]
    )


def test_reason_catalog_and_priority_are_exact():
    assert builder.REASON_CODES == REASON_CODES
    assert builder.SOURCE_NOTES_BUILD_REASON_CODES == REASON_CODES
    assert builder.REASON_PRIORITY == REASON_PRIORITY
    assert set(builder.REASON_CODES) == set(builder.REASON_PRIORITY)


def test_forbidden_pseudo_reason_codes_are_absent():
    module_values = set(builder.__dict__)

    for reason_code in FORBIDDEN_PSEUDO_REASON_CODES:
        assert reason_code not in builder.REASON_CODES
        assert reason_code not in module_values


def test_module_namespace_has_no_forbidden_imports_or_builders():
    module_names = set(builder.__dict__)

    for forbidden_name in FORBIDDEN_MODULE_NAMES:
        assert forbidden_name not in module_names

    assert "build_source_notes" not in module_names
    assert "Final" in module_names
