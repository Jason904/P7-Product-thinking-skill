"""Focused contract tests for the pure Artifact Hash Manifest builder."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import artifact_hash_manifest_builder as builder


REQUIRED_RESULT_FIELDS = {
    "buildable",
    "reason_code",
    "reason",
    "source",
    "manifest",
    "manifest_violations",
    "missing_or_invalid_fields",
    "entry_violations",
    "invariant_refs",
}

REQUIRED_MANIFEST_FIELDS = (
    "run_id",
    "manifest_id",
    "hash_phase",
    "hash_algorithm",
    "artifact_hash_entries",
    "required_artifact_refs",
    "optional_artifact_refs",
    "missing_artifact_refs",
    "redaction_status",
    "public_url_created",
    "public_url",
    "created_at",
    "timestamp_policy",
    "source_of_truth",
    "notes",
)

REQUIRED_ENTRY_FIELDS = (
    "artifact_ref",
    "artifact_role",
    "artifact_visibility",
    "artifact_phase",
    "hash_algorithm",
    "digest",
    "digest_source",
    "redaction_status",
    "notes",
)

REQUIRED_ENTRY_VIOLATION_FIELDS = {
    "entry_index",
    "artifact_ref",
    "reason_code",
    "fields",
}

FORBIDDEN_RESULT_KEYS = {
    "public_url_is_null",
    "raw_public_url",
    "credential_values",
    "raw_credentials",
    "runtime_context",
    "config_snapshot",
    "adapter_outputs",
    "adapter_preflight_result",
    "review_content",
    "artifact_contents",
    "artifact_paths",
    "file_paths",
    "artifact_hash_values_to_calculate",
    "artifact_hash_values",
    "ledger_path",
    "artifact_hash_path",
    "run_ledger_path",
    "failure_package_path",
    "badcase_record_path",
    "should_write_artifact_hash",
    "should_calculate_hash",
    "should_write_ledger",
    "should_transition",
    "should_publish",
    "should_notify",
    "hash_calculated",
    "artifact_read",
    "file_stat_checked",
    "file_exists_checked",
    "gate_executed",
    "transition_executed",
    "ledger_written",
    "artifact_hash_written",
    "published",
    "notification_sent",
    "public_url_reserved",
    "public_url_faked",
    "runtime_context_read",
    "config_read",
    "credential_read",
    "adapter_preflight_executed",
    "adapter_executed",
    "external_api_called",
    "review_read",
    "file_stat",
    "file_exists_check",
    "publisher",
    "notifier",
    "public_url_generated",
    "generated_state",
    "generated_transition",
    "gate_execution_result",
    "transition_execution_result",
}

FORBIDDEN_ENTRY_KEYS = {
    "public_url",
    "artifact_path",
    "file_path",
    "size_bytes",
    "mtime",
    "content",
    "artifact_contents",
    "hash_calculated",
    "path_checked",
    "stat_checked",
}


def _entry(**overrides):
    values = {
        "artifact_ref": "reader.html",
        "artifact_role": "public_candidate",
        "artifact_visibility": "public_candidate",
        "artifact_phase": "final",
        "hash_algorithm": "sha256",
        "digest": "caller-supplied-digest",
        "digest_source": "caller_supplied_no_hash_calculation",
        "redaction_status": "pass",
        "notes": (),
    }
    values.update(overrides)
    return values


def _valid_values():
    return {
        "run_id": "run-001",
        "manifest_id": "artifact-hash-001",
        "hash_phase": "final",
        "hash_algorithm": "sha256",
        "artifact_hash_entries": (_entry(),),
        "required_artifact_refs": ("reader.html",),
        "optional_artifact_refs": (),
        "missing_artifact_refs": (),
        "redaction_status": "pass",
        "public_url_created": False,
        "public_url_is_null": True,
        "created_at": "caller-supplied-created-at",
        "timestamp_policy": "caller_supplied_no_datetime_parsing",
        "source_of_truth": ("p2d-2g", "p2d-17"),
        "notes": ("shape-only",),
    }


def _explain(**overrides):
    values = _valid_values()
    values.update(overrides)
    return builder.explain_artifact_hash_manifest_build(**values)


def test_valid_artifact_hash_manifest_is_buildable():
    result = _explain()

    assert result["buildable"] is True
    assert result["reason_code"] == "ARTIFACT_HASH_MANIFEST_BUILDABLE"
    assert result["manifest"]["public_url"] is None
    assert result["manifest_violations"] == ()
    assert result["entry_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()


def test_optional_artifact_refs_empty_is_buildable():
    result = _explain(optional_artifact_refs=())

    assert result["buildable"] is True
    assert result["manifest"]["optional_artifact_refs"] == ()


def test_optional_artifact_entry_declared_in_optional_refs_is_buildable():
    optional_entry = _entry(
        artifact_ref="training-report.md",
        artifact_role="public_safe_render_source",
        artifact_visibility="private_evidence",
    )
    result = _explain(
        artifact_hash_entries=(_entry(), optional_entry),
        required_artifact_refs=("reader.html",),
        optional_artifact_refs=("training-report.md",),
    )

    assert result["buildable"] is True
    assert result["manifest"]["artifact_hash_entries"] == (
        _entry(),
        optional_entry,
    )


def test_result_manifest_and_entry_shapes_are_exact():
    result = _explain()
    entry = result["manifest"]["artifact_hash_entries"][0]

    assert set(result) == REQUIRED_RESULT_FIELDS
    assert tuple(result["manifest"].keys()) == REQUIRED_MANIFEST_FIELDS
    assert tuple(entry.keys()) == REQUIRED_ENTRY_FIELDS
    assert FORBIDDEN_ENTRY_KEYS.isdisjoint(entry)


def test_required_manifest_field_violations_block_with_dedicated_reasons():
    cases = (
        ("run_id", "", "RUN_ID_MISSING", ("run_id",)),
        ("manifest_id", "", "MANIFEST_ID_MISSING", ("manifest_id",)),
        ("hash_phase", "", "HASH_PHASE_MISSING", ("hash_phase",)),
        (
            "hash_algorithm",
            "",
            "HASH_ALGORITHM_MISSING",
            ("hash_algorithm",),
        ),
        (
            "artifact_hash_entries",
            (),
            "ARTIFACT_HASH_ENTRIES_MISSING",
            ("artifact_hash_entries",),
        ),
        (
            "required_artifact_refs",
            (),
            "REQUIRED_ARTIFACT_REFS_MISSING",
            ("required_artifact_refs",),
        ),
        (
            "redaction_status",
            "",
            "REDACTION_STATUS_MISSING",
            ("redaction_status",),
        ),
        ("created_at", "", "CREATED_AT_MISSING", ("created_at",)),
        (
            "timestamp_policy",
            "",
            "TIMESTAMP_POLICY_MISSING",
            ("timestamp_policy",),
        ),
        (
            "source_of_truth",
            (),
            "SOURCE_OF_TRUTH_MISSING",
            ("source_of_truth",),
        ),
    )

    for field_name, value, reason_code, invalid_fields in cases:
        result = _explain(**{field_name: value})

        assert result["buildable"] is False
        assert result["reason_code"] == reason_code
        assert result["manifest_violations"] == (reason_code,)
        assert result["missing_or_invalid_fields"] == invalid_fields


def test_whitespace_manifest_strings_are_missing():
    cases = (
        ("run_id", "   ", "RUN_ID_MISSING"),
        ("manifest_id", "   ", "MANIFEST_ID_MISSING"),
        ("hash_phase", "   ", "HASH_PHASE_MISSING"),
        ("hash_algorithm", "   ", "HASH_ALGORITHM_MISSING"),
        ("redaction_status", "   ", "REDACTION_STATUS_MISSING"),
        ("created_at", "   ", "CREATED_AT_MISSING"),
        ("timestamp_policy", "   ", "TIMESTAMP_POLICY_MISSING"),
    )

    for field_name, value, reason_code in cases:
        result = _explain(**{field_name: value})

        assert result["buildable"] is False
        assert result["reason_code"] == reason_code


def test_entry_not_dict_blocks_with_stable_detail():
    result = _explain(artifact_hash_entries=("not-a-dict",))

    assert result["buildable"] is False
    assert result["reason_code"] == "ARTIFACT_HASH_ENTRY_NOT_DICT"
    assert result["manifest_violations"] == ("ARTIFACT_HASH_ENTRY_NOT_DICT",)
    assert result["entry_violations"] == (
        {
            "entry_index": 0,
            "artifact_ref": "",
            "reason_code": "ARTIFACT_HASH_ENTRY_NOT_DICT",
            "fields": ("artifact_hash_entries[]",),
        },
    )
    assert set(result["entry_violations"][0]) == REQUIRED_ENTRY_VIOLATION_FIELDS


def test_invalid_entry_keys_block():
    entry = dict(_entry())
    entry["public_url"] = "https://example.test/daily"
    result = _explain(artifact_hash_entries=(entry,))

    assert result["buildable"] is False
    assert result["reason_code"] == "ARTIFACT_HASH_ENTRY_KEYS_INVALID"
    assert result["entry_violations"] == (
        {
            "entry_index": 0,
            "artifact_ref": "reader.html",
            "reason_code": "ARTIFACT_HASH_ENTRY_KEYS_INVALID",
            "fields": ("artifact_hash_entries[].keys",),
        },
    )
    assert "https://example.test/daily" not in repr(result)
    assert "public_url" not in result["manifest"]["artifact_hash_entries"][0]


def test_empty_entry_fields_block():
    cases = (
        ("artifact_ref", "", "artifact_hash_entries[].artifact_ref"),
        ("artifact_role", "", "artifact_hash_entries[].artifact_role"),
        (
            "artifact_visibility",
            "",
            "artifact_hash_entries[].artifact_visibility",
        ),
        ("artifact_phase", "", "artifact_hash_entries[].artifact_phase"),
        ("hash_algorithm", "", "artifact_hash_entries[].hash_algorithm"),
        ("digest", "", "artifact_hash_entries[].digest"),
        ("digest_source", "", "artifact_hash_entries[].digest_source"),
        ("redaction_status", "", "artifact_hash_entries[].redaction_status"),
    )

    for field_name, value, invalid_field in cases:
        result = _explain(artifact_hash_entries=(_entry(**{field_name: value}),))

        assert result["buildable"] is False
        assert result["reason_code"] == "ARTIFACT_HASH_ENTRY_FIELD_MISSING"
        assert result["entry_violations"][0]["fields"] == (invalid_field,)
        assert invalid_field in result["missing_or_invalid_fields"]


def test_whitespace_entry_strings_are_missing():
    result = _explain(artifact_hash_entries=(_entry(digest="   "),))

    assert result["buildable"] is False
    assert result["reason_code"] == "ARTIFACT_HASH_ENTRY_FIELD_MISSING"
    assert result["entry_violations"][0]["fields"] == (
        "artifact_hash_entries[].digest",
    )


def test_entry_notes_non_tuple_blocks():
    result = _explain(artifact_hash_entries=(_entry(notes=("not", "tuple")),))
    assert result["buildable"] is True

    blocked = _explain(artifact_hash_entries=(_entry(notes=["not-tuple"]),))
    assert blocked["buildable"] is False
    assert blocked["reason_code"] == "ARTIFACT_HASH_ENTRY_FIELD_MISSING"
    assert blocked["entry_violations"][0]["fields"] == (
        "artifact_hash_entries[].notes",
    )


def test_entry_algorithm_mismatch_blocks():
    result = _explain(
        hash_algorithm="sha256",
        artifact_hash_entries=(_entry(hash_algorithm="sha512"),),
    )

    assert result["buildable"] is False
    assert result["reason_code"] == "ARTIFACT_HASH_ENTRY_ALGORITHM_MISMATCH"
    assert result["entry_violations"] == (
        {
            "entry_index": 0,
            "artifact_ref": "reader.html",
            "reason_code": "ARTIFACT_HASH_ENTRY_ALGORITHM_MISMATCH",
            "fields": ("artifact_hash_entries[].hash_algorithm",),
        },
    )


def test_duplicate_entry_artifact_ref_blocks():
    result = _explain(artifact_hash_entries=(_entry(), _entry()))

    assert result["buildable"] is False
    assert result["reason_code"] == "DUPLICATE_ARTIFACT_HASH_ENTRY_REF"
    assert result["entry_violations"] == (
        {
            "entry_index": 1,
            "artifact_ref": "reader.html",
            "reason_code": "DUPLICATE_ARTIFACT_HASH_ENTRY_REF",
            "fields": ("artifact_hash_entries[].artifact_ref",),
        },
    )


def test_missing_artifact_refs_declared_blocks():
    result = _explain(missing_artifact_refs=("validator-result.yaml",))

    assert result["buildable"] is False
    assert result["reason_code"] == "MISSING_ARTIFACT_REFS_DECLARED"
    assert result["missing_or_invalid_fields"] == ("missing_artifact_refs",)


def test_required_artifact_ref_without_hash_entry_blocks():
    result = _explain(
        required_artifact_refs=("reader.html", "validator-result.yaml"),
        artifact_hash_entries=(_entry(),),
    )

    assert result["buildable"] is False
    assert result["reason_code"] == "REQUIRED_ARTIFACT_REF_WITHOUT_HASH_ENTRY"
    assert result["missing_or_invalid_fields"] == ("required_artifact_refs",)


def test_undeclared_entry_ref_blocks():
    result = _explain(
        required_artifact_refs=("reader.html",),
        optional_artifact_refs=(),
        artifact_hash_entries=(
            _entry(),
            _entry(artifact_ref="validator-result.yaml"),
        ),
    )

    assert result["buildable"] is False
    assert result["reason_code"] == "HASH_ENTRY_FOR_UNDECLARED_ARTIFACT_REF"
    assert result["entry_violations"] == (
        {
            "entry_index": 1,
            "artifact_ref": "validator-result.yaml",
            "reason_code": "HASH_ENTRY_FOR_UNDECLARED_ARTIFACT_REF",
            "fields": ("artifact_hash_entries[].artifact_ref",),
        },
    )


def test_public_url_created_true_blocks():
    result = _explain(public_url_created=True)

    assert result["buildable"] is False
    assert result["reason_code"] == "PUBLIC_URL_CREATED_TRUE"
    assert result["missing_or_invalid_fields"] == ("public_url_created",)
    assert result["manifest"]["public_url_created"] is True
    assert result["manifest"]["public_url"] is None


def test_public_url_is_null_false_blocks_without_echoing_url():
    result = _explain(public_url_is_null=False)

    assert result["buildable"] is False
    assert result["reason_code"] == "PUBLIC_URL_NON_NULL"
    assert result["missing_or_invalid_fields"] == ("public_url",)
    assert result["manifest"]["public_url"] is None
    assert "public_url_is_null" not in result
    assert "public_url_is_null" not in result["manifest"]


def test_manifest_always_returns_public_url_none():
    results = (
        _explain(),
        _explain(public_url_created=True),
        _explain(public_url_is_null=False),
    )

    for result in results:
        assert result["manifest"]["public_url"] is None


def test_no_raw_url_string_appears_in_valid_or_url_marker_results():
    results = (
        _explain(),
        _explain(public_url_created=True),
        _explain(public_url_is_null=False),
    )

    for result in results:
        assert "https://" not in repr(result)
        assert "raw_public_url" not in result
        assert "raw_public_url" not in result["manifest"]


def test_digest_is_caller_supplied_without_format_validation_or_calculation():
    result = _explain(
        artifact_hash_entries=(
            _entry(
                digest="caller supplied nonstandard digest marker",
                digest_source="caller_supplied_no_file_read",
            ),
        ),
    )

    assert result["buildable"] is True
    assert result["manifest"]["artifact_hash_entries"][0]["digest"] == (
        "caller supplied nonstandard digest marker"
    )
    assert "hash_calculated" not in result
    assert "hash_calculated" not in result["manifest"]


def test_optional_artifact_refs_missing_reason_is_not_declared():
    optional_missing = "OPTIONAL_ARTIFACT_REFS_MISSING"

    assert optional_missing not in builder.ARTIFACT_HASH_MANIFEST_BUILD_REASON_CODES
    assert optional_missing not in builder.__dict__


def test_forbidden_pseudo_reason_codes_are_not_declared():
    forbidden_codes = {
        "ARTIFACT_HASH_WRITE_FORBIDDEN",
        "HASH_CALCULATION_FORBIDDEN",
        "ARTIFACT_READ_FORBIDDEN",
        "FILE_STAT_FORBIDDEN",
        "LEDGER_WRITE_FORBIDDEN",
        "GATE_EXECUTION_FORBIDDEN",
        "TRANSITION_EXECUTION_FORBIDDEN",
        "PUBLISH_FORBIDDEN",
        "NOTIFICATION_FORBIDDEN",
        "PUBLIC_URL_CREATION_FORBIDDEN",
    }

    assert forbidden_codes.isdisjoint(
        builder.ARTIFACT_HASH_MANIFEST_BUILD_REASON_CODES
    )
    assert forbidden_codes.isdisjoint(builder.__dict__)


def test_reason_priority_and_all_violations_are_collected():
    result = _explain(
        run_id="",
        manifest_id="",
        hash_phase="",
        hash_algorithm="sha256",
        artifact_hash_entries=(
            _entry(hash_algorithm="sha512", digest=""),
            _entry(),
            _entry(artifact_ref="undeclared.html"),
        ),
        required_artifact_refs=("reader.html", "validator-result.yaml"),
        optional_artifact_refs=(),
        missing_artifact_refs=("validator-result.yaml",),
        redaction_status="",
        public_url_created=True,
        public_url_is_null=False,
        created_at="",
        timestamp_policy="",
        source_of_truth=(),
    )

    assert result["buildable"] is False
    assert result["reason_code"] == "RUN_ID_MISSING"
    assert result["manifest_violations"] == (
        "RUN_ID_MISSING",
        "MANIFEST_ID_MISSING",
        "HASH_PHASE_MISSING",
        "ARTIFACT_HASH_ENTRY_FIELD_MISSING",
        "ARTIFACT_HASH_ENTRY_ALGORITHM_MISMATCH",
        "DUPLICATE_ARTIFACT_HASH_ENTRY_REF",
        "MISSING_ARTIFACT_REFS_DECLARED",
        "REQUIRED_ARTIFACT_REF_WITHOUT_HASH_ENTRY",
        "HASH_ENTRY_FOR_UNDECLARED_ARTIFACT_REF",
        "REDACTION_STATUS_MISSING",
        "CREATED_AT_MISSING",
        "TIMESTAMP_POLICY_MISSING",
        "SOURCE_OF_TRUTH_MISSING",
        "PUBLIC_URL_CREATED_TRUE",
        "PUBLIC_URL_NON_NULL",
    )
    assert result["missing_or_invalid_fields"] == (
        "run_id",
        "manifest_id",
        "hash_phase",
        "artifact_hash_entries[].digest",
        "artifact_hash_entries[].hash_algorithm",
        "artifact_hash_entries[].artifact_ref",
        "missing_artifact_refs",
        "required_artifact_refs",
        "redaction_status",
        "created_at",
        "timestamp_policy",
        "source_of_truth",
        "public_url_created",
        "public_url",
    )


def test_entry_violations_details_are_stable():
    result = _explain(
        artifact_hash_entries=(
            _entry(digest=""),
            _entry(hash_algorithm="sha512"),
            _entry(),
            _entry(artifact_ref="undeclared.html"),
        )
    )

    assert result["entry_violations"] == (
        {
            "entry_index": 0,
            "artifact_ref": "reader.html",
            "reason_code": "ARTIFACT_HASH_ENTRY_FIELD_MISSING",
            "fields": ("artifact_hash_entries[].digest",),
        },
        {
            "entry_index": 1,
            "artifact_ref": "reader.html",
            "reason_code": "ARTIFACT_HASH_ENTRY_ALGORITHM_MISMATCH",
            "fields": ("artifact_hash_entries[].hash_algorithm",),
        },
        {
            "entry_index": 1,
            "artifact_ref": "reader.html",
            "reason_code": "DUPLICATE_ARTIFACT_HASH_ENTRY_REF",
            "fields": ("artifact_hash_entries[].artifact_ref",),
        },
        {
            "entry_index": 2,
            "artifact_ref": "reader.html",
            "reason_code": "DUPLICATE_ARTIFACT_HASH_ENTRY_REF",
            "fields": ("artifact_hash_entries[].artifact_ref",),
        },
        {
            "entry_index": 3,
            "artifact_ref": "undeclared.html",
            "reason_code": "HASH_ENTRY_FOR_UNDECLARED_ARTIFACT_REF",
            "fields": ("artifact_hash_entries[].artifact_ref",),
        },
    )
    for entry_violation in result["entry_violations"]:
        assert set(entry_violation) == REQUIRED_ENTRY_VIOLATION_FIELDS


def test_bool_wrapper_matches_explanation():
    cases = (
        _valid_values(),
        dict(_valid_values(), run_id=""),
        dict(
            _valid_values(),
            artifact_hash_entries=(_entry(digest=""),),
        ),
        dict(_valid_values(), public_url_is_null=False),
    )

    for values in cases:
        explanation = builder.explain_artifact_hash_manifest_build(**values)

        assert (
            builder.is_artifact_hash_manifest_buildable(**values)
            is explanation["buildable"]
        )


def test_reason_catalog_contains_only_executable_reason_codes():
    assert builder.ARTIFACT_HASH_MANIFEST_BUILD_REASON_CODES == (
        "RUN_ID_MISSING",
        "MANIFEST_ID_MISSING",
        "HASH_PHASE_MISSING",
        "HASH_ALGORITHM_MISSING",
        "ARTIFACT_HASH_ENTRIES_MISSING",
        "ARTIFACT_HASH_ENTRY_NOT_DICT",
        "ARTIFACT_HASH_ENTRY_KEYS_INVALID",
        "ARTIFACT_HASH_ENTRY_FIELD_MISSING",
        "ARTIFACT_HASH_ENTRY_ALGORITHM_MISMATCH",
        "DUPLICATE_ARTIFACT_HASH_ENTRY_REF",
        "REQUIRED_ARTIFACT_REFS_MISSING",
        "MISSING_ARTIFACT_REFS_DECLARED",
        "REQUIRED_ARTIFACT_REF_WITHOUT_HASH_ENTRY",
        "HASH_ENTRY_FOR_UNDECLARED_ARTIFACT_REF",
        "REDACTION_STATUS_MISSING",
        "CREATED_AT_MISSING",
        "TIMESTAMP_POLICY_MISSING",
        "SOURCE_OF_TRUTH_MISSING",
        "PUBLIC_URL_CREATED_TRUE",
        "PUBLIC_URL_NON_NULL",
        "ARTIFACT_HASH_MANIFEST_BUILDABLE",
    )


def test_no_raw_credential_adapter_review_artifact_path_hash_or_ledger_values_appear():
    result = _explain()
    forbidden_values = (
        "secret-token",
        "provider-secret-value",
        "adapter-output-body",
        "review-content-body",
        "artifact-body-content",
        "artifact/path/value",
        "file/path/value",
        "hash-value-to-calculate",
        "ledger/path/value",
    )
    rendered_result = repr(result)

    for forbidden_value in forbidden_values:
        assert forbidden_value not in rendered_result


def test_buildable_result_does_not_imply_execution_or_io():
    result = _explain()

    assert result["buildable"] is True
    assert FORBIDDEN_RESULT_KEYS.isdisjoint(result)
    assert FORBIDDEN_RESULT_KEYS.isdisjoint(result["manifest"])
    assert "artifact_hash_manifest_builder_only" in result["invariant_refs"]
    assert "builder_not_artifact_hash_writer" in result["invariant_refs"]
    assert "builder_not_hash_calculator" in result["invariant_refs"]
    assert "builder_not_hash_manager" in result["invariant_refs"]
    assert "builder_not_artifact_reader" in result["invariant_refs"]
    assert "builder_not_file_stat_checker" in result["invariant_refs"]
    assert "builder_not_file_exists_checker" in result["invariant_refs"]
    assert "builder_not_ledger_writer" in result["invariant_refs"]
    assert "builder_not_gate_execution" in result["invariant_refs"]
    assert "builder_not_transition_mapping" in result["invariant_refs"]
    assert "builder_not_transition_execution" in result["invariant_refs"]
    assert "buildable_not_artifact_hash_write" in result["invariant_refs"]
    assert "buildable_not_hash_calculation" in result["invariant_refs"]
    assert "buildable_not_artifact_read" in result["invariant_refs"]
    assert "buildable_not_file_stat" in result["invariant_refs"]
    assert "buildable_not_publish" in result["invariant_refs"]
    assert "buildable_not_notification" in result["invariant_refs"]
    assert "buildable_not_public_url" in result["invariant_refs"]


def test_module_namespace_does_not_import_forbidden_modules_or_io_libraries():
    forbidden_names = {
        "states",
        "gates",
        "artifacts",
        "gate_decision_mapper",
        "transition_guard",
        "adapter_gate_evidence_policy",
        "adapter_gate_decision_policy",
        "daily_gate_evidence_policy",
        "daily_gate_decision_policy",
        "gate_decision_envelope_builder",
        "run_ledger_entry_builder",
        "failure_package_builder",
        "badcase_record_builder",
        "artifact_inventory_policy",
        "noop_completion_policy",
        "badcase_creation_policy",
        "pathlib",
        "os",
        "datetime",
        "hashlib",
        "subprocess",
        "requests",
    }

    assert forbidden_names.isdisjoint(builder.__dict__)


def test_result_does_not_imply_runtime_config_adapter_hash_ledger_or_url_behavior():
    results = (
        _explain(),
        _explain(public_url_is_null=False),
    )

    for result in results:
        assert FORBIDDEN_RESULT_KEYS.isdisjoint(result)
        assert FORBIDDEN_RESULT_KEYS.isdisjoint(result["manifest"])
        assert "no_runtime_context_config_or_credential_read" in (
            result["invariant_refs"]
        )
        assert "no_adapter_preflight" in result["invariant_refs"]
        assert "no_external_adapter_call" in result["invariant_refs"]
        assert "no_raw_credentials" in result["invariant_refs"]
        assert "no_raw_public_url" in result["invariant_refs"]
        assert "no_quality_pass_no_public_url" in result["invariant_refs"]
        assert "no_artifact_or_review_io" in result["invariant_refs"]
        assert "no_hashlib" in result["invariant_refs"]
        assert "no_hash_calculation" in result["invariant_refs"]
        assert "no_ledger_write" in result["invariant_refs"]
        assert "no_artifact_hash_write" in result["invariant_refs"]
        assert "no_public_url_behavior" in result["invariant_refs"]


def test_invariant_refs_capture_no_existing_policy_or_builder_calls():
    result = _explain()
    required_invariants = {
        "no_artifact_inventory_policy_call",
        "no_gate_decision_envelope_builder_call",
        "no_run_ledger_entry_builder_call",
        "no_failure_package_builder_call",
        "no_badcase_record_builder_call",
    }

    assert required_invariants <= set(result["invariant_refs"])


def test_no_forbidden_payload_object_path_or_control_inputs_are_in_result():
    result = _explain()
    forbidden_names = (
        "runtime_context",
        "config_snapshot",
        "credential_values",
        "raw_credentials",
        "raw_public_url",
        "adapter_outputs",
        "review_content",
        "artifact_contents",
        "artifact_paths",
        "file_paths",
        "artifact_hash_values_to_calculate",
        "ledger_path",
        "artifact_hash_path",
        "run_ledger_path",
        "failure_package_path",
        "badcase_record_path",
        "gate_decision_envelope",
        "run_ledger_entry",
        "failure_package",
        "badcase_record",
        "should_write_artifact_hash",
        "should_calculate_hash",
        "should_write_ledger",
        "should_transition",
        "should_publish",
        "should_notify",
    )

    for forbidden_name in forbidden_names:
        assert forbidden_name not in result
        assert forbidden_name not in result["manifest"]
