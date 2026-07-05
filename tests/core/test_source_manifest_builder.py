"""Tests for the pure source manifest buildability helpers."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import source_manifest_builder as builder


EXPECTED_RESULT_KEYS = (
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

EXPECTED_MANIFEST_KEYS = (
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

EXPECTED_ENTRY_KEYS = (
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

EXPECTED_REASON_CODES = (
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

FORBIDDEN_ENTRY_FIELDS = (
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


def _entry(**overrides):
    values = {
        "source_ref": "source-001",
        "source_id": "manual-source-001",
        "source_kind": "manual_note",
        "source_title": "Manual source",
        "source_visibility": "private",
        "source_role": "evidence",
        "retrieval_mode": "caller_supplied",
        "retrieval_status": "declared",
        "redaction_status": "pass",
        "content_ref": "content-ref-001",
        "notes": ("caller supplied only",),
    }
    values.update(overrides)
    return values


def _build_kwargs(**overrides):
    values = {
        "run_id": "run-001",
        "source_manifest_id": "source-manifest-001",
        "source_entries": (_entry(),),
        "required_source_refs": ("source-001",),
        "optional_source_refs": (),
        "missing_source_refs": (),
        "redaction_status": "pass",
        "created_at": "caller-supplied-created-at",
        "timestamp_policy": "caller_supplied_no_time_parsing",
        "source_of_truth": ("p2d-24",),
        "notes": ("shape-only",),
    }
    values.update(overrides)
    return values


def _explain(**overrides):
    return builder.explain_source_manifest_build(**_build_kwargs(**overrides))


def _keys_without_invariant_refs(value):
    keys = []
    if isinstance(value, dict):
        for key, child in value.items():
            keys.append(key)
            if key != "invariant_refs":
                keys.extend(_keys_without_invariant_refs(child))
    elif isinstance(value, tuple):
        for child in value:
            keys.extend(_keys_without_invariant_refs(child))
    return tuple(keys)


def test_valid_source_manifest_buildable():
    result = _explain()
    assert result["buildable"] is True
    assert result["reason_code"] == "SOURCE_MANIFEST_BUILDABLE"
    assert result["manifest_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()
    assert result["entry_violations"] == ()
    assert "builder_not_retriever" in result["invariant_refs"]
    assert result["source"] == "caller_supplied_source_manifest_arguments"


def test_exact_top_level_result_keys():
    assert tuple(_explain().keys()) == EXPECTED_RESULT_KEYS


def test_exact_manifest_keys():
    assert tuple(_explain()["manifest"].keys()) == EXPECTED_MANIFEST_KEYS


def test_exact_source_entry_keys():
    entry = _explain()["manifest"]["source_entries"][0]
    assert tuple(entry.keys()) == EXPECTED_ENTRY_KEYS


def test_required_manifest_field_violations():
    cases = (
        ("run_id", " ", "RUN_ID_MISSING", "run_id"),
        (
            "source_manifest_id",
            "",
            "SOURCE_MANIFEST_ID_MISSING",
            "source_manifest_id",
        ),
        ("redaction_status", "", "REDACTION_STATUS_MISSING", "redaction_status"),
        ("created_at", "", "CREATED_AT_MISSING", "created_at"),
        ("timestamp_policy", "", "TIMESTAMP_POLICY_MISSING", "timestamp_policy"),
        ("source_of_truth", (), "SOURCE_OF_TRUTH_MISSING", "source_of_truth"),
    )
    for field, value, reason_code, invalid_field in cases:
        result = _explain(**{field: value})
        assert reason_code in result["manifest_violations"]
        assert invalid_field in result["missing_or_invalid_fields"]


def test_missing_source_refs_blocks():
    result = _explain(missing_source_refs=("source-002",))
    assert result["buildable"] is False
    assert result["reason_code"] == "MISSING_SOURCE_REFS_DECLARED"
    assert "missing_source_refs" in result["missing_or_invalid_fields"]


def test_source_entries_non_empty():
    result = _explain(source_entries=())
    assert result["buildable"] is False
    assert result["reason_code"] == "SOURCE_ENTRIES_MISSING"
    assert "SOURCE_ENTRIES_MISSING" in result["manifest_violations"]


def test_required_source_refs_non_empty():
    result = _explain(required_source_refs=())
    assert result["buildable"] is False
    assert result["reason_code"] == "REQUIRED_SOURCE_REFS_MISSING"
    assert "required_source_refs" in result["missing_or_invalid_fields"]


def test_non_dict_source_entry():
    for entry in ("not-a-dict",):
        result = _explain(source_entries=(entry,))
        assert result["reason_code"] == "ENTRY_NOT_DICT"
        assert "ENTRY_NOT_DICT" in result["manifest_violations"]
        assert "source_entries" in result["missing_or_invalid_fields"]
        assert {
            "entry_index": 0,
            "source_ref": "",
            "reason_code": "ENTRY_NOT_DICT",
            "field": "source_entries",
        } in result["entry_violations"]


def test_missing_required_source_entry_keys():
    cases = (
        ("source_ref", "ENTRY_SOURCE_REF_MISSING"),
        ("source_id", "ENTRY_SOURCE_ID_MISSING"),
        ("source_kind", "ENTRY_SOURCE_KIND_MISSING"),
        ("source_title", "ENTRY_SOURCE_TITLE_MISSING"),
        ("source_visibility", "ENTRY_SOURCE_VISIBILITY_MISSING"),
        ("source_role", "ENTRY_SOURCE_ROLE_MISSING"),
        ("retrieval_mode", "ENTRY_RETRIEVAL_MODE_MISSING"),
        ("retrieval_status", "ENTRY_RETRIEVAL_STATUS_MISSING"),
        ("redaction_status", "ENTRY_REDACTION_STATUS_MISSING"),
        ("content_ref", "ENTRY_CONTENT_REF_MISSING"),
    )
    for field_name, expected_reason in cases:
        entry = _entry()
        del entry[field_name]
        result = _explain(source_entries=(entry,))
        assert result["reason_code"] == "ENTRY_KEYS_INVALID"
        assert "ENTRY_KEYS_INVALID" in result["manifest_violations"]
        assert expected_reason in result["manifest_violations"]
        assert field_name in result["missing_or_invalid_fields"]


def test_source_ref_unique():
    result = _explain(source_entries=(_entry(), _entry(source_id="manual-source-002")))
    assert result["buildable"] is False
    assert "ENTRY_SOURCE_REF_DUPLICATE" in result["manifest_violations"]
    assert {
        "entry_index": 1,
        "source_ref": "source-001",
        "reason_code": "ENTRY_SOURCE_REF_DUPLICATE",
        "field": "source_ref",
    } in result["entry_violations"]


def test_source_ref_declared_in_required_or_optional_refs():
    optional_result = _explain(
        source_entries=(_entry(source_ref="source-optional"),),
        required_source_refs=("source-001",),
        optional_source_refs=("source-optional",),
    )
    assert "ENTRY_SOURCE_REF_NOT_DECLARED" not in optional_result["manifest_violations"]

    undeclared_result = _explain(source_entries=(_entry(source_ref="source-999"),))
    assert "ENTRY_SOURCE_REF_NOT_DECLARED" in undeclared_result["manifest_violations"]
    assert "source_ref" in undeclared_result["missing_or_invalid_fields"]


def test_every_required_source_ref_must_have_entry():
    result = _explain(required_source_refs=("source-001", "source-002"))
    assert "REQUIRED_SOURCE_REF_ENTRY_MISSING" in result["manifest_violations"]
    assert {
        "entry_index": -1,
        "source_ref": "source-002",
        "reason_code": "REQUIRED_SOURCE_REF_ENTRY_MISSING",
        "field": "required_source_refs",
    } in result["entry_violations"]


def test_source_visibility_catalog():
    for source_visibility in ("private", "public", "internal"):
        assert _explain(source_entries=(_entry(source_visibility=source_visibility),))[
            "buildable"
        ] is True

    result = _explain(source_entries=(_entry(source_visibility="partner"),))
    assert "ENTRY_SOURCE_VISIBILITY_INVALID" in result["manifest_violations"]
    assert "source_visibility" in result["missing_or_invalid_fields"]


def test_source_role_catalog():
    for source_role in ("evidence", "context", "reference"):
        assert _explain(source_entries=(_entry(source_role=source_role),))[
            "buildable"
        ] is True

    result = _explain(source_entries=(_entry(source_role="owner"),))
    assert "ENTRY_SOURCE_ROLE_INVALID" in result["manifest_violations"]
    assert "source_role" in result["missing_or_invalid_fields"]


def test_retrieval_mode_catalog():
    for retrieval_mode in ("caller_supplied", "manual_local_noop"):
        assert _explain(source_entries=(_entry(retrieval_mode=retrieval_mode),))[
            "buildable"
        ] is True

    result = _explain(source_entries=(_entry(retrieval_mode="web_fetch"),))
    assert "ENTRY_RETRIEVAL_MODE_INVALID" in result["manifest_violations"]
    assert "retrieval_mode" in result["missing_or_invalid_fields"]


def test_blank_and_invalid_catalog_fields():
    cases = (
        (
            "source_visibility",
            " ",
            "ENTRY_SOURCE_VISIBILITY_MISSING",
        ),
        (
            "source_role",
            " ",
            "ENTRY_SOURCE_ROLE_MISSING",
        ),
        (
            "retrieval_mode",
            " ",
            "ENTRY_RETRIEVAL_MODE_MISSING",
        ),
        (
            "source_visibility",
            "secret",
            "ENTRY_SOURCE_VISIBILITY_INVALID",
        ),
        (
            "source_role",
            "primary",
            "ENTRY_SOURCE_ROLE_INVALID",
        ),
        (
            "retrieval_mode",
            "web_fetch",
            "ENTRY_RETRIEVAL_MODE_INVALID",
        ),
    )
    for field_name, value, expected_reason in cases:
        result = _explain(source_entries=(_entry(**{field_name: value}),))
        assert expected_reason in result["manifest_violations"]
        assert field_name in result["missing_or_invalid_fields"]


def test_source_kind_non_empty_opaque():
    assert _explain(source_entries=(_entry(source_kind="custom_provider_kind"),))[
        "buildable"
    ] is True

    result = _explain(source_entries=(_entry(source_kind=" "),))
    assert "ENTRY_SOURCE_KIND_MISSING" in result["manifest_violations"]
    assert "source_kind" in result["missing_or_invalid_fields"]


def test_retrieval_status_non_empty_opaque():
    assert _explain(source_entries=(_entry(retrieval_status="caller_declared_ready"),))[
        "buildable"
    ] is True

    result = _explain(source_entries=(_entry(retrieval_status=""),))
    assert "ENTRY_RETRIEVAL_STATUS_MISSING" in result["manifest_violations"]
    assert "retrieval_status" in result["missing_or_invalid_fields"]


def test_content_ref_non_empty_opaque():
    assert _explain(source_entries=(_entry(content_ref="opaque-content-ref-alpha"),))[
        "buildable"
    ] is True

    result = _explain(source_entries=(_entry(content_ref=""),))
    assert "ENTRY_CONTENT_REF_MISSING" in result["manifest_violations"]
    assert "content_ref" in result["missing_or_invalid_fields"]


def test_no_raw_url_or_path_leakage():
    entry = _entry(raw_url="suppressed", url="suppressed", path="suppressed")
    result = _explain(source_entries=(entry,))
    keys = _keys_without_invariant_refs(result)
    assert "raw_url" not in keys
    assert "url" not in keys
    assert "path" not in keys
    assert "ENTRY_FORBIDDEN_RAW_FIELD_PRESENT" in result["manifest_violations"]


def test_no_raw_content_leakage():
    entry = _entry(raw_content="suppressed", content="suppressed")
    result = _explain(source_entries=(entry,))
    keys = _keys_without_invariant_refs(result)
    assert "raw_content" not in keys
    assert "content" not in keys
    assert tuple(result["manifest"]["source_entries"][0].keys()) == EXPECTED_ENTRY_KEYS


def test_no_file_web_github_notion_fetch_markers_as_executable_fields():
    entry = _entry(
        source_fetch_result="suppressed",
        source_reader_result="suppressed",
        retriever_result="suppressed",
        fetch_executed=True,
        file_read_executed=True,
        web_called=True,
        github_called=True,
        notion_called=True,
    )
    result = _explain(source_entries=(entry,))
    keys = _keys_without_invariant_refs(result)
    for forbidden_key in (
        "source_fetch_result",
        "source_reader_result",
        "retriever_result",
        "fetch_executed",
        "file_read_executed",
        "web_called",
        "github_called",
        "notion_called",
    ):
        assert forbidden_key not in keys
    assert "ENTRY_FORBIDDEN_RAW_FIELD_PRESENT" in result["manifest_violations"]


def test_no_public_url_fields():
    entry = _entry(public_url="suppressed", public_url_created=True)
    result = _explain(source_entries=(entry,))
    keys = _keys_without_invariant_refs(result)
    assert "public_url" not in keys
    assert "public_url_created" not in keys
    assert "no_public_url_behavior" in result["invariant_refs"]


def test_no_credentials_env_config_adapter_driver_leakage():
    entry = _entry(
        credentials="suppressed",
        raw_credentials="suppressed",
        env_vars="suppressed",
        raw_env_vars="suppressed",
        config="suppressed",
        raw_config="suppressed",
        adapter_outputs="suppressed",
        driver_object="suppressed",
    )
    result = _explain(source_entries=(entry,))
    keys = _keys_without_invariant_refs(result)
    for forbidden_key in (
        "credentials",
        "raw_credentials",
        "env_vars",
        "raw_env_vars",
        "config",
        "raw_config",
        "adapter_outputs",
        "driver_object",
    ):
        assert forbidden_key not in keys
    assert "ENTRY_FORBIDDEN_RAW_FIELD_PRESENT" in result["manifest_violations"]


def test_no_should_flags():
    entry = _entry(
        should_fetch=True,
        should_read_file=True,
        should_call_web=True,
        should_call_github=True,
        should_call_notion=True,
        should_summarize=True,
        should_write_manifest=True,
    )
    result = _explain(source_entries=(entry,))
    keys = _keys_without_invariant_refs(result)
    for forbidden_key in (
        "should_fetch",
        "should_read_file",
        "should_call_web",
        "should_call_github",
        "should_call_notion",
        "should_summarize",
        "should_write_manifest",
    ):
        assert forbidden_key not in keys
    assert "ENTRY_FORBIDDEN_RAW_FIELD_PRESENT" in result["manifest_violations"]


def test_every_forbidden_entry_field_is_rejected_and_suppressed():
    for forbidden_field in FORBIDDEN_ENTRY_FIELDS:
        result = _explain(
            source_entries=(_entry(**{forbidden_field: "suppressed"}),)
        )
        keys = _keys_without_invariant_refs(result)
        assert forbidden_field not in keys
        assert "ENTRY_KEYS_INVALID" in result["manifest_violations"]
        assert "ENTRY_FORBIDDEN_RAW_FIELD_PRESENT" in result[
            "manifest_violations"
        ]
        assert {
            "entry_index": 0,
            "source_ref": "source-001",
            "reason_code": "ENTRY_FORBIDDEN_RAW_FIELD_PRESENT",
            "field": "forbidden_raw_field",
        } in result["entry_violations"]


def test_reason_priority_and_all_violations():
    invalid_entry = {
        "source_ref": "",
        "source_id": "",
        "source_kind": "",
        "source_title": "",
        "source_visibility": "partner",
        "source_role": "owner",
        "retrieval_mode": "web_fetch",
        "retrieval_status": "",
        "redaction_status": "",
        "content_ref": "",
        "notes": (),
        "raw_url": "suppressed",
    }
    result = _explain(
        run_id="",
        source_manifest_id="",
        source_entries=(invalid_entry,),
        required_source_refs=(),
        missing_source_refs=("source-002",),
        redaction_status="",
        created_at="",
        timestamp_policy="",
        source_of_truth=(),
    )
    assert result["reason_code"] == "RUN_ID_MISSING"
    assert result["reason_code"] == result["manifest_violations"][0]
    assert result["manifest_violations"] == (
        "RUN_ID_MISSING",
        "SOURCE_MANIFEST_ID_MISSING",
        "REQUIRED_SOURCE_REFS_MISSING",
        "MISSING_SOURCE_REFS_DECLARED",
        "REDACTION_STATUS_MISSING",
        "CREATED_AT_MISSING",
        "TIMESTAMP_POLICY_MISSING",
        "SOURCE_OF_TRUTH_MISSING",
        "ENTRY_KEYS_INVALID",
        "ENTRY_SOURCE_REF_MISSING",
        "ENTRY_SOURCE_ID_MISSING",
        "ENTRY_SOURCE_KIND_MISSING",
        "ENTRY_SOURCE_TITLE_MISSING",
        "ENTRY_SOURCE_VISIBILITY_INVALID",
        "ENTRY_SOURCE_ROLE_INVALID",
        "ENTRY_RETRIEVAL_MODE_INVALID",
        "ENTRY_RETRIEVAL_STATUS_MISSING",
        "ENTRY_REDACTION_STATUS_MISSING",
        "ENTRY_CONTENT_REF_MISSING",
        "ENTRY_FORBIDDEN_RAW_FIELD_PRESENT",
    )


def test_entry_reason_priority_with_mutually_compatible_entries():
    blank_entry = {
        "source_ref": "",
        "source_id": "",
        "source_kind": "",
        "source_title": "",
        "source_visibility": " ",
        "source_role": " ",
        "retrieval_mode": " ",
        "retrieval_status": "",
        "redaction_status": "",
        "content_ref": "",
        "notes": (),
        "raw_url": "suppressed",
    }
    invalid_catalog_entry = _entry(
        source_ref="duplicate-ref",
        source_visibility="secret",
        source_role="primary",
        retrieval_mode="web_fetch",
    )
    duplicate_entry = _entry(
        source_ref="duplicate-ref",
        source_id="manual-source-duplicate",
    )
    result = _explain(
        source_entries=(
            "not-a-dict",
            blank_entry,
            invalid_catalog_entry,
            duplicate_entry,
        ),
        required_source_refs=("required-missing",),
    )
    assert result["reason_code"] == "ENTRY_NOT_DICT"
    assert result["reason_code"] == result["manifest_violations"][0]
    assert result["manifest_violations"] == (
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


def test_every_reason_code_has_a_behavior_scenario():
    valid_result = _explain()
    manifest_result = _explain(
        run_id="",
        source_manifest_id="",
        source_entries=(),
        required_source_refs=(),
        missing_source_refs=("source-002",),
        redaction_status="",
        created_at="",
        timestamp_policy="",
        source_of_truth=(),
    )
    entry_result = _explain(
        source_entries=(
            "not-a-dict",
            {
                "source_ref": "",
                "source_id": "",
                "source_kind": "",
                "source_title": "",
                "source_visibility": " ",
                "source_role": " ",
                "retrieval_mode": " ",
                "retrieval_status": "",
                "redaction_status": "",
                "content_ref": "",
                "notes": (),
                "raw_url": "suppressed",
            },
            _entry(
                source_ref="duplicate-ref",
                source_visibility="secret",
                source_role="primary",
                retrieval_mode="web_fetch",
            ),
            _entry(
                source_ref="duplicate-ref",
                source_id="manual-source-duplicate",
            ),
        ),
        required_source_refs=("required-missing",),
    )
    observed_reason_codes = {
        valid_result["reason_code"],
        *manifest_result["manifest_violations"],
        *entry_result["manifest_violations"],
    }
    assert observed_reason_codes == set(EXPECTED_REASON_CODES)
    assert manifest_result["reason_code"] == manifest_result[
        "manifest_violations"
    ][0]
    assert entry_result["reason_code"] == entry_result["manifest_violations"][0]


def test_missing_or_invalid_fields_collection():
    result = _explain(
        run_id="",
        source_entries=(_entry(source_id="", retrieval_mode="web_fetch"),),
    )
    assert result["missing_or_invalid_fields"] == (
        "run_id",
        "source_id",
        "retrieval_mode",
    )


def test_entry_violations_records():
    result = _explain(source_entries=(_entry(source_id="", source_role="owner"),))
    assert {
        "entry_index": 0,
        "source_ref": "source-001",
        "reason_code": "ENTRY_SOURCE_ID_MISSING",
        "field": "source_id",
    } in result["entry_violations"]
    assert {
        "entry_index": 0,
        "source_ref": "source-001",
        "reason_code": "ENTRY_SOURCE_ROLE_INVALID",
        "field": "source_role",
    } in result["entry_violations"]


def test_bool_wrapper_parity():
    kwargs = _build_kwargs()
    result = builder.explain_source_manifest_build(**kwargs)
    assert builder.is_source_manifest_buildable(**kwargs) is result["buildable"]

    blocked_kwargs = _build_kwargs(run_id="")
    blocked_result = builder.explain_source_manifest_build(**blocked_kwargs)
    assert (
        builder.is_source_manifest_buildable(**blocked_kwargs)
        is blocked_result["buildable"]
    )


def test_exact_reason_catalog():
    assert builder.REASON_CODES == EXPECTED_REASON_CODES


def test_forbidden_pseudo_reason_codes_absent():
    forbidden_reason_codes = (
        "WEB_FETCH_FORBIDDEN",
        "GITHUB_FETCH_FORBIDDEN",
        "NOTION_FETCH_FORBIDDEN",
        "FILE_READ_FORBIDDEN",
        "SOURCE_CONTENT_READ_FORBIDDEN",
        "LLM_SUMMARY_FORBIDDEN",
        "MANIFEST_WRITE_FORBIDDEN",
        "PUBLIC_URL_CREATION_FORBIDDEN",
    )
    for reason_code in forbidden_reason_codes:
        assert reason_code not in builder.REASON_CODES


def test_no_forbidden_module_namespace_imports():
    forbidden_names = (
        "states",
        "gates",
        "artifacts",
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
        "subprocess",
        "requests",
    )
    for name in forbidden_names:
        assert name not in builder.__dict__


def test_no_full_result_repr_blanket_scan_issue():
    result = _explain()
    assert "no_raw_content" in result["invariant_refs"]
    assert "no_raw_url" in result["invariant_refs"]
    keys = _keys_without_invariant_refs(result)
    assert "raw_content" not in keys
    assert "raw_url" not in keys
