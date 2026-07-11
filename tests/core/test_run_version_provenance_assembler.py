"""Contract tests for the pure run version provenance assembler."""

import inspect
import sys
import types

from ai_daily_publishing_system.core import run_version_provenance_assembler as builder


ROOT_KEYS = (
    "version_provenance_assembled",
    "reason_code",
    "reason",
    "source",
    "run_version_provenance",
    "assembly_violations",
    "missing_or_invalid_fields",
    "coherence_violations",
    "invariant_refs",
)

SUCCESS_SOURCE_KEYS = (
    "assembly_scope",
    "schema_version",
    "run_version_provenance_id",
    "run_id",
    "component_version_count",
    "resolved_at",
    "resolution_policy",
    "source_of_truth",
)

BLOCKED_SOURCE_KEYS = (
    "assembly_scope",
    "schema_version",
    "component_version_count",
)

PROVENANCE_KEYS = (
    "schema_version",
    "run_version_provenance_id",
    "run_id",
    "skill_version",
    "rubric_version",
    "generator_version",
    "renderer_version",
    "publisher_version",
    "resolved_component_version_evidence_items",
    "resolved_at",
    "resolution_policy",
    "source_of_truth",
)

COHERENCE_RECORD_KEYS = (
    "component_index",
    "version_field",
    "reason_code",
    "field",
)

EXPECTED_FORBIDDEN_EXACT_NAMES = (
    "version_provenance_assembled",
    "versions_resolved",
    "resolution_executed",
    "resolver_executed",
    "runtime_versions_verified",
    "release_verified",
    "completed",
    "executed",
    "terminal_reached",
    "noop_completed",
    "quality_pass",
    "validator_pass",
    "rubric_pass",
    "audit_pass",
    "eval_pass",
    "gate_pass",
    "policy_pass",
    "publish_allowed",
    "pass_published",
    "published",
    "notified",
    "notification_sent",
    "public_url",
    "public_url_value",
    "publish_url",
    "deployment_url",
    "hosting_url",
    "live_url",
    "real_url",
    "ledger_written",
    "run_ledger_written",
    "ledger_entry",
    "run_ledger_entry",
    "run_ledger_yaml",
    "ledger_file_path",
    "path",
    "file_path",
    "local_path",
    "filesystem_path",
    "content",
    "payload",
    "raw",
    "full",
    "config",
    "configuration",
    "env",
    "environment",
    "env_vars",
    "credentials",
    "secrets",
    "token",
    "cookies",
    "command",
    "shell_command",
    "cli_command",
    "argv",
    "args",
    "parsed_args",
    "stdout",
    "stderr",
    "exit_code",
    "subprocess_result",
    "network_result",
    "provider_result",
    "adapter_result",
    "runtime_result",
    "runner_result",
    "resolver_result",
    "resolution_result",
    "release_result",
    "resolver_output",
    "resolution_output",
    "release_output",
    "release_manifest",
    "release_manifest_payload",
    "release_tag",
    "release_commit",
    "release_commit_sha",
    "git_branch",
    "git_tag",
    "git_commit",
    "git_commit_sha",
    "checksum",
    "release_checksum",
    "resolved_component_payload",
    "raw_payload",
    "full_payload",
    "raw_content",
    "full_content",
    "raw_object",
    "full_object",
)

EXPECTED_FORBIDDEN_PREFIXES = (
    "should_",
    "raw_",
    "full_",
    "actual_",
    "execution_",
    "completion_",
    "runtime_",
    "runner_execution_",
    "resolver_",
    "resolved_",
    "resolution_",
    "release_",
    "quality_",
    "gate_",
    "eval_",
    "audit_",
    "publish_",
    "publication_",
    "notification_",
    "public_url_",
    "ledger_",
    "run_ledger_",
    "filesystem_",
    "file_",
    "path_",
    "config_",
    "configuration_",
    "environment_",
    "env_",
    "credential_",
    "secret_",
    "cli_",
    "command_",
    "subprocess_",
    "network_",
    "provider_",
    "adapter_",
    "git_",
    "source_",
)

EXPECTED_FORBIDDEN_SUFFIXES = (
    "_payload",
    "_content",
    "_path",
    "_command",
    "_output",
    "_result",
    "_execution",
    "_executed",
    "_completed",
    "_reached",
    "_verified",
    "_written",
    "_persisted",
    "_published",
    "_notified",
    "_credentials",
    "_secrets",
    "_token",
    "_cookie",
    "_cookies",
)

EXPECTED_REASON_CODES = (
    "RUN_VERSION_PROVENANCE_ASSEMBLED_IN_MEMORY",
    "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
    "RUN_ID_INVALID",
    "RUN_VERSION_PROVENANCE_ID_INVALID",
    "RUN_VERSION_PROVENANCE_ID_NOT_DISTINCT",
    "COMPONENT_EVIDENCE_ITEMS_INVALID",
    "COMPONENT_EVIDENCE_COUNT_INVALID",
    "COMPONENT_EVIDENCE_ITEM_NOT_DICT",
    "COMPONENT_EVIDENCE_ITEM_KEYS_INVALID",
    "COMPONENT_VERSION_FIELD_INVALID",
    "COMPONENT_VERSION_FIELD_DUPLICATE",
    "COMPONENT_VERSION_ORDER_INVALID",
    "RESOLVED_VERSION_INVALID",
    "RESOLUTION_STATUS_NOT_RESOLVED",
    "RESOLVER_REF_INVALID",
    "EVIDENCE_REF_INVALID",
    "RESOLVED_AT_INVALID",
    "RESOLUTION_POLICY_INVALID",
    "SOURCE_OF_TRUTH_INVALID",
)

EXPECTED_REASON_PRIORITY = (
    "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
    "RUN_ID_INVALID",
    "RUN_VERSION_PROVENANCE_ID_INVALID",
    "RUN_VERSION_PROVENANCE_ID_NOT_DISTINCT",
    "COMPONENT_EVIDENCE_ITEMS_INVALID",
    "COMPONENT_EVIDENCE_COUNT_INVALID",
    "COMPONENT_EVIDENCE_ITEM_NOT_DICT",
    "COMPONENT_EVIDENCE_ITEM_KEYS_INVALID",
    "COMPONENT_VERSION_FIELD_INVALID",
    "COMPONENT_VERSION_FIELD_DUPLICATE",
    "COMPONENT_VERSION_ORDER_INVALID",
    "RESOLVED_VERSION_INVALID",
    "RESOLUTION_STATUS_NOT_RESOLVED",
    "RESOLVER_REF_INVALID",
    "EVIDENCE_REF_INVALID",
    "RESOLVED_AT_INVALID",
    "RESOLUTION_POLICY_INVALID",
    "SOURCE_OF_TRUTH_INVALID",
    "RUN_VERSION_PROVENANCE_ASSEMBLED_IN_MEMORY",
)

EXPECTED_REASON_STRINGS = (
    (
        "RUN_VERSION_PROVENANCE_ASSEMBLED_IN_MEMORY",
        "A complete, structurally valid, caller-supplied "
        "resolver-attested five-component run version provenance object "
        "was assembled in memory; no resolver or I/O was executed.",
    ),
    (
        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
        "A forbidden field or namespace was supplied; caller key names "
        "and values are suppressed.",
    ),
    ("RUN_ID_INVALID", "run_id must be an exact nonblank string."),
    (
        "RUN_VERSION_PROVENANCE_ID_INVALID",
        "run_version_provenance_id must be an exact nonblank string.",
    ),
    (
        "RUN_VERSION_PROVENANCE_ID_NOT_DISTINCT",
        "run_version_provenance_id must be distinct from run_id.",
    ),
    (
        "COMPONENT_EVIDENCE_ITEMS_INVALID",
        "resolved_component_version_evidence_items must be an exact tuple.",
    ),
    (
        "COMPONENT_EVIDENCE_COUNT_INVALID",
        "resolved_component_version_evidence_items must contain exactly "
        "five items.",
    ),
    (
        "COMPONENT_EVIDENCE_ITEM_NOT_DICT",
        "Every component evidence item must be an exact dict.",
    ),
    (
        "COMPONENT_EVIDENCE_ITEM_KEYS_INVALID",
        "Every component evidence item must contain the exact expected "
        "keys in the exact expected order.",
    ),
    (
        "COMPONENT_VERSION_FIELD_INVALID",
        "Every version_field must be an exact canonical component name.",
    ),
    (
        "COMPONENT_VERSION_FIELD_DUPLICATE",
        "Each canonical version_field may appear exactly once.",
    ),
    (
        "COMPONENT_VERSION_ORDER_INVALID",
        "Canonical version fields must appear in the fixed component order.",
    ),
    (
        "RESOLVED_VERSION_INVALID",
        "Every resolved_version must satisfy the exact 1-to-128-character "
        "version syntax.",
    ),
    (
        "RESOLUTION_STATUS_NOT_RESOLVED",
        "Every caller-supplied resolution_status must be exactly resolved.",
    ),
    (
        "RESOLVER_REF_INVALID",
        "Every resolver_ref must be an exact nonblank opaque string.",
    ),
    (
        "EVIDENCE_REF_INVALID",
        "Every evidence_ref must be an exact nonblank opaque string.",
    ),
    (
        "RESOLVED_AT_INVALID",
        "resolved_at must be an exact nonblank opaque timestamp string.",
    ),
    (
        "RESOLUTION_POLICY_INVALID",
        "resolution_policy must be an exact nonblank opaque policy "
        "identifier.",
    ),
    (
        "SOURCE_OF_TRUTH_INVALID",
        "source_of_truth must be a nonempty exact tuple of exact nonblank "
        "strings.",
    ),
)

EXPECTED_DIAGNOSTIC_PATHS = (
    ("RUN_VERSION_PROVENANCE_ASSEMBLED_IN_MEMORY", ()),
    (
        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
        ("p2d45v.forbidden_field_or_namespace",),
    ),
    ("RUN_ID_INVALID", ("run_id",)),
    (
        "RUN_VERSION_PROVENANCE_ID_INVALID",
        ("run_version_provenance_id",),
    ),
    (
        "RUN_VERSION_PROVENANCE_ID_NOT_DISTINCT",
        ("run_version_provenance_id",),
    ),
    (
        "COMPONENT_EVIDENCE_ITEMS_INVALID",
        ("resolved_component_version_evidence_items",),
    ),
    (
        "COMPONENT_EVIDENCE_COUNT_INVALID",
        ("resolved_component_version_evidence_items",),
    ),
    (
        "COMPONENT_EVIDENCE_ITEM_NOT_DICT",
        ("resolved_component_version_evidence_items[]",),
    ),
    (
        "COMPONENT_EVIDENCE_ITEM_KEYS_INVALID",
        ("resolved_component_version_evidence_items[].keys",),
    ),
    (
        "COMPONENT_VERSION_FIELD_INVALID",
        ("resolved_component_version_evidence_items[].version_field",),
    ),
    (
        "COMPONENT_VERSION_FIELD_DUPLICATE",
        ("resolved_component_version_evidence_items[].version_field",),
    ),
    (
        "COMPONENT_VERSION_ORDER_INVALID",
        ("resolved_component_version_evidence_items[].version_field",),
    ),
    (
        "RESOLVED_VERSION_INVALID",
        ("resolved_component_version_evidence_items[].resolved_version",),
    ),
    (
        "RESOLUTION_STATUS_NOT_RESOLVED",
        ("resolved_component_version_evidence_items[].resolution_status",),
    ),
    (
        "RESOLVER_REF_INVALID",
        ("resolved_component_version_evidence_items[].resolver_ref",),
    ),
    (
        "EVIDENCE_REF_INVALID",
        ("resolved_component_version_evidence_items[].evidence_ref",),
    ),
    ("RESOLVED_AT_INVALID", ("resolved_at",)),
    ("RESOLUTION_POLICY_INVALID", ("resolution_policy",)),
    ("SOURCE_OF_TRUTH_INVALID", ("source_of_truth",)),
)

EXPECTED_INVARIANTS = (
    "run_version_provenance_assembler_only",
    "assembler_pure_in_memory_only",
    "exactly_five_component_versions_required",
    "component_version_order_fixed",
    "one_evidence_item_per_component_required",
    "noop_publisher_requires_explicit_publisher_version",
    "component_evidence_items_are_caller_supplied_resolver_attestations",
    "resolution_status_is_caller_supplied_attestation_only",
    "assembler_does_not_resolve_component_versions",
    "assembler_does_not_execute_resolver",
    "assembler_does_not_fetch_release",
    "assembler_does_not_inspect_files_skill_or_rubric",
    "assembler_does_not_inspect_git_or_release_metadata",
    "resolved_version_syntax_is_exact",
    "resolution_status_must_equal_resolved",
    "resolver_refs_are_opaque",
    "evidence_refs_are_opaque",
    "resolved_at_is_opaque_caller_evidence",
    "resolution_policy_is_opaque_caller_identifier",
    "component_versions_are_never_inferred",
    "duplicate_component_version_values_allowed",
    "shared_resolver_refs_allowed",
    "shared_evidence_refs_allowed",
    "source_of_truth_order_and_duplicates_preserved",
    "caller_input_not_mutated",
    "output_containers_are_fresh",
    "nonempty_output_tuples_are_identity_isolated",
    "empty_tuple_identity_not_required",
    "blocked_output_is_fixed_and_caller_safe",
    "unknown_keys_block_and_are_suppressed",
    "forbidden_fields_block_and_are_suppressed",
    "recursive_key_scan_is_cycle_and_depth_safe",
    "recursive_key_scan_does_not_scan_scalar_strings",
    (
        "version_provenance_assembled_means_structurally_valid_"
        "in_memory_object_only"
    ),
    "version_provenance_assembled_not_independent_version_verification",
    "version_provenance_assembled_not_runtime_execution",
    "version_provenance_assembled_not_ledger_entry_assembly",
    "version_provenance_assembled_not_ledger_persistence",
    "version_provenance_assembled_not_completion_or_transition",
    "version_provenance_assembled_not_quality_pass",
    "version_provenance_assembled_not_gate_pass",
    "version_provenance_assembled_not_publish_authorization",
    "no_file_or_artifact_io",
    "no_config_env_or_credential_access",
    "no_cli_command_or_subprocess",
    "no_network_or_provider_call",
    "no_actual_resolver_result_payload",
    "no_public_url_behavior",
    "no_publish_or_notification",
    "no_upstream_or_sibling_call",
)


def _item(
    version_field,
    *,
    resolved_version=None,
    resolution_status="resolved",
    resolver_ref="stable-release-resolver",
    evidence_ref="stable-release-manifest",
):
    if resolved_version is None:
        resolved_version = "v1.0.0"
    return {
        "version_field": version_field,
        "resolved_version": resolved_version,
        "resolution_status": resolution_status,
        "resolver_ref": resolver_ref,
        "evidence_ref": evidence_ref,
    }


def _items():
    versions = (
        "v5.0",
        "2.1",
        "generator-3.4.5",
        "b7fa46263f0db28a780656e28bacf74503cb5395",
        "noop-publisher-1.0",
    )
    return tuple(
        _item(version_field, resolved_version=versions[index])
        for index, version_field in enumerate(
            builder.COMPONENT_VERSION_FIELDS
        )
    )


def _valid_values():
    return {
        "run_id": "run-2026-07-10",
        "run_version_provenance_id": "run-version-provenance-2026-07-10",
        "resolved_component_version_evidence_items": _items(),
        "resolved_at": "2026-07-10T09:00:00+08:00",
        "resolution_policy": "latest-stable-release",
        "source_of_truth": (
            "stable-release-manifest",
            "release-attestation",
        ),
    }


def _assemble(**overrides):
    values = _valid_values()
    values.update(overrides)
    return builder.assemble_run_version_provenance(**values)


def _replace_item(items, index, **updates):
    copied_items = [dict(item) for item in items]
    copied_items[index].update(updates)
    return tuple(item for item in copied_items)


def _all_nested_keys(value):
    keys = set()
    stack = [value]
    visited = set()
    while stack:
        current = stack.pop()
        if type(current) not in (dict, list, tuple):
            continue
        if id(current) in visited:
            continue
        visited.add(id(current))
        if type(current) is dict:
            for key, nested in current.items():
                if type(key) is str:
                    keys.add(key)
                stack.append(nested)
        else:
            for nested in current:
                stack.append(nested)
    return keys


def _all_scalar_strings(value):
    strings = set()
    stack = [value]
    visited = set()
    while stack:
        current = stack.pop()
        if type(current) is str:
            strings.add(current)
            continue
        if type(current) not in (dict, list, tuple):
            continue
        if id(current) in visited:
            continue
        visited.add(id(current))
        if type(current) is dict:
            for nested in current.values():
                stack.append(nested)
        else:
            for nested in current:
                stack.append(nested)
    return strings


def test_exact_component_schema_and_fixed_constants():
    assert builder.COMPONENT_VERSION_FIELDS == (
        "skill_version",
        "rubric_version",
        "generator_version",
        "renderer_version",
        "publisher_version",
    )
    assert builder.COMPONENT_EVIDENCE_ITEM_KEYS == (
        "version_field",
        "resolved_version",
        "resolution_status",
        "resolver_ref",
        "evidence_ref",
    )
    assert builder.SCHEMA_VERSION == "p2d45.run_version_provenance.v1"
    assert builder.ASSEMBLY_SCOPE == "run_version_provenance_in_memory_only"
    assert builder.FORBIDDEN_EXACT_NAMES == EXPECTED_FORBIDDEN_EXACT_NAMES
    assert builder.FORBIDDEN_PREFIXES == EXPECTED_FORBIDDEN_PREFIXES
    assert builder.FORBIDDEN_SUFFIXES == EXPECTED_FORBIDDEN_SUFFIXES


def test_public_apis_are_exact_keyword_only_and_annotated():
    expected_names = (
        "run_id",
        "run_version_provenance_id",
        "resolved_component_version_evidence_items",
        "resolved_at",
        "resolution_policy",
        "source_of_truth",
    )
    expected_annotations = (
        str,
        str,
        tuple[dict[str, object], ...],
        str,
        str,
        tuple[str, ...],
    )
    cases = (
        (builder.assemble_run_version_provenance, dict[str, object]),
        (builder.is_run_version_provenance_assembled, bool),
    )
    for function, return_annotation in cases:
        signature = inspect.signature(function)
        assert tuple(signature.parameters) == expected_names
        for index, parameter in enumerate(signature.parameters.values()):
            assert parameter.kind is inspect.Parameter.KEYWORD_ONLY
            assert parameter.default is inspect.Parameter.empty
            assert parameter.annotation == expected_annotations[index]
        assert signature.return_annotation == return_annotation
    assert builder.assemble_run_version_provenance.__doc__ == (
        "Assemble resolver-attested run version provenance in memory."
    )
    assert builder.is_run_version_provenance_assembled.__doc__ == (
        "Return only whether run version provenance was assembled."
    )


def test_bool_wrapper_calls_assembler_once_without_patching():
    values = _valid_values()
    assembler_code = builder.assemble_run_version_provenance.__code__
    call_count = 0

    def profile(frame, event, argument):
        del argument
        nonlocal call_count
        if event == "call" and frame.f_code is assembler_code:
            call_count += 1

    previous_profile = sys.getprofile()
    sys.setprofile(profile)
    try:
        assembled = builder.is_run_version_provenance_assembled(**values)
    finally:
        sys.setprofile(previous_profile)

    assert assembled is True
    assert type(assembled) is bool
    assert call_count == 1


def test_valid_five_component_provenance_has_exact_shapes_and_mappings():
    values = _valid_values()
    result = builder.assemble_run_version_provenance(**values)

    assert tuple(result) == ROOT_KEYS
    assert result["version_provenance_assembled"] is True
    assert result["reason_code"] == (
        "RUN_VERSION_PROVENANCE_ASSEMBLED_IN_MEMORY"
    )
    assert tuple(result["source"]) == SUCCESS_SOURCE_KEYS
    assert result["source"] == {
        "assembly_scope": "run_version_provenance_in_memory_only",
        "schema_version": "p2d45.run_version_provenance.v1",
        "run_version_provenance_id": values[
            "run_version_provenance_id"
        ],
        "run_id": values["run_id"],
        "component_version_count": 5,
        "resolved_at": values["resolved_at"],
        "resolution_policy": values["resolution_policy"],
        "source_of_truth": values["source_of_truth"],
    }

    provenance = result["run_version_provenance"]
    assert tuple(provenance) == PROVENANCE_KEYS
    assert provenance["schema_version"] == (
        "p2d45.run_version_provenance.v1"
    )
    assert provenance["run_version_provenance_id"] == values[
        "run_version_provenance_id"
    ]
    assert provenance["run_id"] == values["run_id"]
    assert provenance["skill_version"] == "v5.0"
    assert provenance["rubric_version"] == "2.1"
    assert provenance["generator_version"] == "generator-3.4.5"
    assert provenance["renderer_version"] == (
        "b7fa46263f0db28a780656e28bacf74503cb5395"
    )
    assert provenance["publisher_version"] == "noop-publisher-1.0"
    assert provenance["resolved_at"] == values["resolved_at"]
    assert provenance["resolution_policy"] == values["resolution_policy"]
    assert provenance["source_of_truth"] == values["source_of_truth"]
    for evidence_item in provenance[
        "resolved_component_version_evidence_items"
    ]:
        assert tuple(evidence_item) == builder.COMPONENT_EVIDENCE_ITEM_KEYS
    assert result["assembly_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()
    assert result["coherence_violations"] == ()
    assert result["invariant_refs"] == EXPECTED_INVARIANTS


def test_component_count_missing_unknown_duplicate_and_order_block():
    valid_items = _items()

    missing = _assemble(
        resolved_component_version_evidence_items=valid_items[:4]
    )
    assert "COMPONENT_EVIDENCE_COUNT_INVALID" in missing[
        "assembly_violations"
    ]

    duplicate_items = _replace_item(
        valid_items,
        1,
        version_field="skill_version",
    )
    duplicate = _assemble(
        resolved_component_version_evidence_items=duplicate_items
    )
    assert "COMPONENT_VERSION_FIELD_DUPLICATE" in duplicate[
        "assembly_violations"
    ]
    assert "COMPONENT_VERSION_ORDER_INVALID" in duplicate[
        "assembly_violations"
    ]

    unknown_items = _replace_item(
        valid_items,
        2,
        version_field="caller_unknown_component",
    )
    unknown = _assemble(
        resolved_component_version_evidence_items=unknown_items
    )
    assert "COMPONENT_VERSION_FIELD_INVALID" in unknown[
        "assembly_violations"
    ]
    assert "caller_unknown_component" not in _all_scalar_strings(unknown)

    reordered_items = list(valid_items)
    reordered_items[0], reordered_items[1] = (
        reordered_items[1],
        reordered_items[0],
    )
    reordered = _assemble(
        resolved_component_version_evidence_items=tuple(
            item for item in reordered_items
        )
    )
    assert reordered["assembly_violations"] == (
        "COMPONENT_VERSION_ORDER_INVALID",
    )


def test_surplus_canonical_component_collects_count_duplicate_and_order():
    surplus_items = _items() + (_item("skill_version"),)
    result = _assemble(
        resolved_component_version_evidence_items=surplus_items
    )
    assert result["assembly_violations"] == (
        "COMPONENT_EVIDENCE_COUNT_INVALID",
        "COMPONENT_VERSION_FIELD_DUPLICATE",
        "COMPONENT_VERSION_ORDER_INVALID",
    )
    assert result["coherence_violations"] == (
        {
            "component_index": 5,
            "version_field": "skill_version",
            "reason_code": "COMPONENT_VERSION_FIELD_DUPLICATE",
            "field": (
                "resolved_component_version_evidence_items[].version_field"
            ),
        },
        {
            "component_index": 5,
            "version_field": "skill_version",
            "reason_code": "COMPONENT_VERSION_ORDER_INVALID",
            "field": (
                "resolved_component_version_evidence_items[].version_field"
            ),
        },
    )

    unknown_surplus_items = _items() + (
        _item("surplus-caller-secret-component"),
    )
    unknown = _assemble(
        resolved_component_version_evidence_items=unknown_surplus_items
    )
    assert unknown["assembly_violations"] == (
        "COMPONENT_EVIDENCE_COUNT_INVALID",
        "COMPONENT_VERSION_FIELD_INVALID",
    )
    assert unknown["coherence_violations"] == (
        {
            "component_index": 5,
            "version_field": "",
            "reason_code": "COMPONENT_VERSION_FIELD_INVALID",
            "field": (
                "resolved_component_version_evidence_items[].version_field"
            ),
        },
    )
    assert "surplus-caller-secret-component" not in _all_scalar_strings(
        unknown
    )


def test_outer_tuple_and_item_dict_subclasses_are_rejected():
    tuple_subtype = type("TupleSubtype", (tuple,), {})
    dict_subtype = type("DictSubtype", (dict,), {})

    outer = _assemble(
        resolved_component_version_evidence_items=tuple_subtype(_items())
    )
    assert outer["reason_code"] == "COMPONENT_EVIDENCE_ITEMS_INVALID"

    items = list(_items())
    items[2] = dict_subtype(items[2])
    nested = _assemble(
        resolved_component_version_evidence_items=tuple(
            item for item in items
        )
    )
    assert nested["reason_code"] == "COMPONENT_EVIDENCE_ITEM_NOT_DICT"
    assert nested["coherence_violations"] == (
        {
            "component_index": 2,
            "version_field": "generator_version",
            "reason_code": "COMPONENT_EVIDENCE_ITEM_NOT_DICT",
            "field": "resolved_component_version_evidence_items[]",
        },
    )


def test_missing_extra_and_reordered_evidence_keys_are_rejected():
    valid_items = _items()
    missing_item = dict(valid_items[0])
    del missing_item["evidence_ref"]

    reordered_item = {
        "resolved_version": valid_items[0]["resolved_version"],
        "version_field": valid_items[0]["version_field"],
        "resolution_status": valid_items[0]["resolution_status"],
        "resolver_ref": valid_items[0]["resolver_ref"],
        "evidence_ref": valid_items[0]["evidence_ref"],
    }

    for invalid_item in (missing_item, reordered_item):
        items = list(valid_items)
        items[0] = invalid_item
        result = _assemble(
            resolved_component_version_evidence_items=tuple(
                item for item in items
            )
        )
        assert result["reason_code"] == (
            "COMPONENT_EVIDENCE_ITEM_KEYS_INVALID"
        )
        assert result["missing_or_invalid_fields"][0] == (
            "resolved_component_version_evidence_items[].keys"
        )

    for unknown_key in (
        "harmless_extra",
        "unexpected_metadata",
        "another_unknown_key",
    ):
        extra_item = dict(valid_items[0])
        extra_item[unknown_key] = "suppressed-extra-value"
        items = list(valid_items)
        items[0] = extra_item
        result = _assemble(
            resolved_component_version_evidence_items=tuple(items)
        )
        assert result["reason_code"] == (
            "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"
        )
        assert result["assembly_violations"] == (
            "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
            "COMPONENT_EVIDENCE_ITEM_KEYS_INVALID",
        )
        assert unknown_key not in _all_nested_keys(result)
        assert "suppressed-extra-value" not in _all_scalar_strings(result)

    non_string_key_item = dict(valid_items[0])
    non_string_key_item[17] = "suppressed-non-string-key-value"
    items = list(valid_items)
    items[0] = non_string_key_item
    non_string_key_result = _assemble(
        resolved_component_version_evidence_items=tuple(items)
    )
    assert non_string_key_result["reason_code"] == (
        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"
    )
    assert non_string_key_result["assembly_violations"] == (
        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
        "COMPONENT_EVIDENCE_ITEM_KEYS_INVALID",
    )
    assert "suppressed-non-string-key-value" not in _all_scalar_strings(
        non_string_key_result
    )

    missing_items = list(valid_items)
    missing_items[0] = missing_item
    missing_result = _assemble(
        resolved_component_version_evidence_items=tuple(
            item for item in missing_items
        )
    )
    assert "EVIDENCE_REF_INVALID" in missing_result["assembly_violations"]
    assert missing_result["missing_or_invalid_fields"] == (
        "resolved_component_version_evidence_items[].keys",
        "resolved_component_version_evidence_items[].evidence_ref",
    )


def test_exact_string_types_and_verbatim_opaque_values():
    string_subtype = type("StringSubtype", (str,), {})
    invalid_values = (None, False, True, 0, 1, string_subtype("value"))

    for invalid in invalid_values:
        assert _assemble(run_id=invalid)["reason_code"] == "RUN_ID_INVALID"
        assert _assemble(run_version_provenance_id=invalid)[
            "reason_code"
        ] == "RUN_VERSION_PROVENANCE_ID_INVALID"
        assert _assemble(resolved_at=invalid)["reason_code"] == (
            "RESOLVED_AT_INVALID"
        )
        assert _assemble(resolution_policy=invalid)["reason_code"] == (
            "RESOLUTION_POLICY_INVALID"
        )

    items = _items()
    for field, reason_code in (
        ("version_field", "COMPONENT_VERSION_FIELD_INVALID"),
        ("resolved_version", "RESOLVED_VERSION_INVALID"),
        ("resolution_status", "RESOLUTION_STATUS_NOT_RESOLVED"),
        ("resolver_ref", "RESOLVER_REF_INVALID"),
        ("evidence_ref", "EVIDENCE_REF_INVALID"),
    ):
        invalid_items = _replace_item(items, 0, **{field: string_subtype("x")})
        result = _assemble(
            resolved_component_version_evidence_items=invalid_items
        )
        assert reason_code in result["assembly_violations"]

    verbatim_items = _replace_item(
        items,
        0,
        resolver_ref="  resolver ref  ",
        evidence_ref="  evidence ref  ",
    )
    verbatim = _assemble(
        run_id="  run id  ",
        run_version_provenance_id="  provenance id  ",
        resolved_component_version_evidence_items=verbatim_items,
        resolved_at="  timestamp evidence  ",
        resolution_policy="  policy id  ",
        source_of_truth=("  source ref  ",),
    )
    assert verbatim["version_provenance_assembled"] is True
    provenance = verbatim["run_version_provenance"]
    assert provenance["run_id"] == "  run id  "
    assert provenance["run_version_provenance_id"] == "  provenance id  "
    assert provenance["resolved_at"] == "  timestamp evidence  "
    assert provenance["resolution_policy"] == "  policy id  "
    assert provenance["source_of_truth"] == ("  source ref  ",)
    assert provenance["resolved_component_version_evidence_items"][0][
        "resolver_ref"
    ] == "  resolver ref  "


def test_version_syntax_boundaries_and_examples():
    valid_versions = (
        "a",
        "a" + "b" * 127,
        "v5.0",
        "b7fa46263f0db28a780656e28bacf74503cb5395",
        "noop-publisher-1.0",
        "A_1+build-7.2",
    )
    for version in valid_versions:
        items = _replace_item(_items(), 0, resolved_version=version)
        result = _assemble(
            resolved_component_version_evidence_items=items
        )
        assert result["version_provenance_assembled"] is True
        assert result["run_version_provenance"]["skill_version"] == version

    invalid_versions = (
        "",
        "a" * 129,
        ".v1",
        "-v1",
        "_v1",
        "+v1",
        "v 1",
        "版本1",
        "v/1",
        "v:1",
        "v1\n",
        " v1",
        "v1 ",
    )
    for version in invalid_versions:
        items = _replace_item(_items(), 0, resolved_version=version)
        result = _assemble(
            resolved_component_version_evidence_items=items
        )
        assert "RESOLVED_VERSION_INVALID" in result["assembly_violations"]


def test_equal_versions_and_shared_refs_are_allowed():
    items = tuple(
        _item(
            version_field,
            resolved_version="same-version-1.0",
            resolver_ref="shared-resolver-ref",
            evidence_ref="shared-evidence-ref",
        )
        for version_field in builder.COMPONENT_VERSION_FIELDS
    )
    result = _assemble(resolved_component_version_evidence_items=items)
    assert result["version_provenance_assembled"] is True
    provenance = result["run_version_provenance"]
    for version_field in builder.COMPONENT_VERSION_FIELDS:
        assert provenance[version_field] == "same-version-1.0"


def test_wrong_resolution_status_including_pass_published_is_rejected():
    for status in ("", "RESOLVED", "PASS", "PASS_PUBLISHED", False, 1):
        items = _replace_item(_items(), 4, resolution_status=status)
        result = _assemble(
            resolved_component_version_evidence_items=items
        )
        assert "RESOLUTION_STATUS_NOT_RESOLVED" in result[
            "assembly_violations"
        ]
        assert "PASS_PUBLISHED_FORBIDDEN" not in builder.REASON_CODES


def test_id_validation_distinctness_and_no_unapproved_distinctness():
    for invalid in ("", " ", "\t", None, False, 1):
        assert _assemble(run_id=invalid)["reason_code"] == "RUN_ID_INVALID"
        assert _assemble(run_version_provenance_id=invalid)[
            "reason_code"
        ] == "RUN_VERSION_PROVENANCE_ID_INVALID"

    same = _assemble(
        run_id="same-id",
        run_version_provenance_id="same-id",
    )
    assert same["reason_code"] == (
        "RUN_VERSION_PROVENANCE_ID_NOT_DISTINCT"
    )

    shared_scalar = "shared-opaque-value"
    items = tuple(
        _item(
            field,
            resolved_version=shared_scalar,
            resolver_ref=shared_scalar,
            evidence_ref=shared_scalar,
        )
        for field in builder.COMPONENT_VERSION_FIELDS
    )
    allowed = _assemble(
        run_id=shared_scalar,
        run_version_provenance_id="different-provenance-id",
        resolved_component_version_evidence_items=items,
        resolved_at=shared_scalar,
        resolution_policy=shared_scalar,
        source_of_truth=(shared_scalar,),
    )
    assert allowed["version_provenance_assembled"] is True


def test_resolved_at_policy_and_source_of_truth_validation():
    for invalid in ("", " ", "\n", None, False, 1):
        assert _assemble(resolved_at=invalid)["reason_code"] == (
            "RESOLVED_AT_INVALID"
        )
        assert _assemble(resolution_policy=invalid)["reason_code"] == (
            "RESOLUTION_POLICY_INVALID"
        )

    tuple_subtype = type("SourceTupleSubtype", (tuple,), {})
    string_subtype = type("SourceStringSubtype", (str,), {})
    invalid_sources = (
        (),
        [],
        ["source"],
        tuple_subtype(("source",)),
        ("",),
        (" ",),
        (False,),
        (1,),
        (string_subtype("source"),),
    )
    for source in invalid_sources:
        result = _assemble(source_of_truth=source)
        assert "SOURCE_OF_TRUTH_INVALID" in result["assembly_violations"]


def test_source_order_duplicates_and_separate_freshness_are_preserved():
    source = ("manifest", "manifest", "attestation", "manifest")
    result = _assemble(source_of_truth=source)
    nested_source = result["run_version_provenance"]["source_of_truth"]
    success_source = result["source"]["source_of_truth"]
    assert nested_source == source
    assert success_source == source
    assert nested_source is not source
    assert success_source is not source
    assert nested_source is not success_source


def test_reason_catalog_strings_paths_priority_and_alias_are_exact():
    assert builder.REASON_CODES == EXPECTED_REASON_CODES
    assert builder.RUN_VERSION_PROVENANCE_ASSEMBLER_REASON_CODES == (
        EXPECTED_REASON_CODES
    )
    assert builder.REASON_PRIORITY == EXPECTED_REASON_PRIORITY
    assert builder.REASON_PRIORITY[-1] == (
        "RUN_VERSION_PROVENANCE_ASSEMBLED_IN_MEMORY"
    )
    assert builder.REASON_STRINGS == EXPECTED_REASON_STRINGS
    assert builder.DIAGNOSTIC_PATHS == EXPECTED_DIAGNOSTIC_PATHS
    assert tuple(code for code, reason in builder.REASON_STRINGS) == (
        EXPECTED_REASON_CODES
    )
    assert all(reason != "" for code, reason in builder.REASON_STRINGS)
    assert tuple(code for code, paths in builder.DIAGNOSTIC_PATHS) == (
        EXPECTED_REASON_CODES
    )


def test_first_reason_and_complete_violation_collection_are_deterministic():
    result = _assemble(
        run_id="",
        run_version_provenance_id="",
        resolved_component_version_evidence_items=[
            {"completed": "caller-secret"}
        ],
        resolved_at="",
        resolution_policy="",
        source_of_truth=(),
    )
    assert result["reason_code"] == "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"
    assert result["assembly_violations"] == (
        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
        "RUN_ID_INVALID",
        "RUN_VERSION_PROVENANCE_ID_INVALID",
        "COMPONENT_EVIDENCE_ITEMS_INVALID",
        "RESOLVED_AT_INVALID",
        "RESOLUTION_POLICY_INVALID",
        "SOURCE_OF_TRUTH_INVALID",
    )
    assert result["missing_or_invalid_fields"] == (
        "p2d45v.forbidden_field_or_namespace",
        "run_id",
        "run_version_provenance_id",
        "resolved_component_version_evidence_items",
        "resolved_at",
        "resolution_policy",
        "source_of_truth",
    )
    assert len(result["assembly_violations"]) == len(
        set(result["assembly_violations"])
    )


def test_blocked_source_provenance_and_caller_leakage_are_fixed_safe():
    secret_values = (
        "caller-secret-run-id",
        "caller-secret-provenance-id",
        "caller-secret-version",
        "caller-secret-resolver-ref",
        "caller-secret-evidence-ref",
        "caller-secret-resolved-at",
        "caller-secret-policy",
        "caller-secret-source",
        "caller-secret-component",
    )
    items = list(_items())
    items[2] = _item(
        secret_values[8],
        resolved_version=secret_values[2],
        resolver_ref=secret_values[3],
        evidence_ref=secret_values[4],
    )
    result = _assemble(
        run_id=secret_values[0],
        run_version_provenance_id=secret_values[1],
        resolved_component_version_evidence_items=tuple(
            item for item in items
        ),
        resolved_at=secret_values[5],
        resolution_policy=secret_values[6],
        source_of_truth=(secret_values[7],),
    )
    assert result["version_provenance_assembled"] is False
    assert tuple(result) == ROOT_KEYS
    assert tuple(result["source"]) == BLOCKED_SOURCE_KEYS
    assert result["source"] == {
        "assembly_scope": "run_version_provenance_in_memory_only",
        "schema_version": "p2d45.run_version_provenance.v1",
        "component_version_count": 0,
    }
    assert result["run_version_provenance"] == {}
    scalar_strings = _all_scalar_strings(result)
    for secret in secret_values:
        assert secret not in scalar_strings


def test_coherence_records_are_safe_exact_ordered_and_deduplicated():
    items = _items()
    invalid_items = _replace_item(
        items,
        0,
        resolved_version="bad version",
        resolution_status="PASS_PUBLISHED",
    )
    invalid_items = _replace_item(
        invalid_items,
        1,
        version_field="skill_version",
    )
    result = _assemble(
        resolved_component_version_evidence_items=invalid_items
    )
    records = result["coherence_violations"]
    assert all(tuple(record) == COHERENCE_RECORD_KEYS for record in records)
    assert records == (
        {
            "component_index": 1,
            "version_field": "skill_version",
            "reason_code": "COMPONENT_VERSION_FIELD_DUPLICATE",
            "field": (
                "resolved_component_version_evidence_items[].version_field"
            ),
        },
        {
            "component_index": 1,
            "version_field": "skill_version",
            "reason_code": "COMPONENT_VERSION_ORDER_INVALID",
            "field": (
                "resolved_component_version_evidence_items[].version_field"
            ),
        },
        {
            "component_index": 0,
            "version_field": "skill_version",
            "reason_code": "RESOLVED_VERSION_INVALID",
            "field": (
                "resolved_component_version_evidence_items[].resolved_version"
            ),
        },
        {
            "component_index": 0,
            "version_field": "skill_version",
            "reason_code": "RESOLUTION_STATUS_NOT_RESOLVED",
            "field": (
                "resolved_component_version_evidence_items[].resolution_status"
            ),
        },
    )
    assert len(records) == len(
        {
            (
                record["component_index"],
                record["version_field"],
                record["reason_code"],
                record["field"],
            )
            for record in records
        }
    )


def test_invalid_component_names_use_safe_expected_labels():
    items = _replace_item(
        _items(),
        3,
        version_field="caller-secret-component-name",
    )
    result = _assemble(resolved_component_version_evidence_items=items)
    assert result["coherence_violations"] == (
        {
            "component_index": 3,
            "version_field": "renderer_version",
            "reason_code": "COMPONENT_VERSION_FIELD_INVALID",
            "field": (
                "resolved_component_version_evidence_items[].version_field"
            ),
        },
    )
    assert "caller-secret-component-name" not in _all_scalar_strings(result)


def test_invariant_catalog_is_exact_and_fresh_in_every_output():
    first = _assemble()
    second = _assemble()
    blocked = _assemble(run_id="")
    assert builder.INVARIANT_REFS == EXPECTED_INVARIANTS
    assert first["invariant_refs"] == EXPECTED_INVARIANTS
    assert second["invariant_refs"] == EXPECTED_INVARIANTS
    assert blocked["invariant_refs"] == EXPECTED_INVARIANTS
    assert first["invariant_refs"] is not builder.INVARIANT_REFS
    assert second["invariant_refs"] is not builder.INVARIANT_REFS
    assert blocked["invariant_refs"] is not builder.INVARIANT_REFS
    assert first["invariant_refs"] is not second["invariant_refs"]


def test_input_containers_are_not_mutated():
    values = _valid_values()
    caller_items = values["resolved_component_version_evidence_items"]
    caller_item_snapshots = tuple(dict(item) for item in caller_items)
    caller_source = values["source_of_truth"]

    builder.assemble_run_version_provenance(**values)

    assert values["resolved_component_version_evidence_items"] is caller_items
    assert values["source_of_truth"] is caller_source
    assert caller_items == caller_item_snapshots
    for index, item in enumerate(caller_items):
        assert item == caller_item_snapshots[index]


def test_success_evidence_source_and_outputs_are_fresh_across_calls():
    values = _valid_values()
    caller_items = values["resolved_component_version_evidence_items"]
    caller_source = values["source_of_truth"]
    first = builder.assemble_run_version_provenance(**values)
    second = builder.assemble_run_version_provenance(**values)

    first_provenance = first["run_version_provenance"]
    second_provenance = second["run_version_provenance"]
    first_items = first_provenance[
        "resolved_component_version_evidence_items"
    ]
    second_items = second_provenance[
        "resolved_component_version_evidence_items"
    ]

    assert first is not second
    assert first["source"] is not second["source"]
    assert first_provenance is not second_provenance
    assert first_items == caller_items
    assert first_items is not caller_items
    assert second_items is not caller_items
    assert first_items is not second_items
    for index, caller_item in enumerate(caller_items):
        assert first_items[index] == caller_item
        assert first_items[index] is not caller_item
        assert second_items[index] is not caller_item
        assert first_items[index] is not second_items[index]

    first_nested_source = first_provenance["source_of_truth"]
    first_success_source = first["source"]["source_of_truth"]
    second_nested_source = second_provenance["source_of_truth"]
    second_success_source = second["source"]["source_of_truth"]
    assert first_nested_source == caller_source
    assert first_nested_source is not caller_source
    assert second_nested_source == caller_source
    assert second_nested_source is not caller_source
    assert first_success_source is not caller_source
    assert second_success_source is not caller_source
    assert first_success_source == second_success_source
    assert first_success_source is not second_success_source
    assert first_nested_source is not first_success_source
    assert second_nested_source is not second_success_source
    assert first_nested_source is not second_nested_source


def test_failure_containers_are_fresh_across_calls():
    items = _replace_item(_items(), 0, resolved_version="bad version")
    first = _assemble(resolved_component_version_evidence_items=items)
    second = _assemble(resolved_component_version_evidence_items=items)
    assert first is not second
    assert first["source"] is not second["source"]
    assert first["run_version_provenance"] is not second[
        "run_version_provenance"
    ]
    assert first["assembly_violations"] is not second[
        "assembly_violations"
    ]
    assert first["missing_or_invalid_fields"] is not second[
        "missing_or_invalid_fields"
    ]
    assert first["coherence_violations"] is not second[
        "coherence_violations"
    ]
    assert first["coherence_violations"][0] is not second[
        "coherence_violations"
    ][0]


def test_empty_tuple_diagnostics_have_exact_semantics():
    result = _assemble()
    for field in (
        "assembly_violations",
        "missing_or_invalid_fields",
        "coherence_violations",
    ):
        assert type(result[field]) is tuple
        assert result[field] == ()


def test_every_forbidden_exact_name_prefix_and_suffix_blocks_safely():
    for forbidden_name in EXPECTED_FORBIDDEN_EXACT_NAMES:
        items = list(_items())
        item = dict(items[0])
        item[forbidden_name] = "caller-secret"
        items[0] = item
        result = _assemble(
            resolved_component_version_evidence_items=tuple(
                value for value in items
            )
        )
        assert result["reason_code"] == (
            "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"
        )
        assert forbidden_name not in _all_nested_keys(result)
        assert "caller-secret" not in _all_scalar_strings(result)

    for forbidden_prefix in EXPECTED_FORBIDDEN_PREFIXES:
        forbidden_name = forbidden_prefix + "probe"
        items = list(_items())
        item = dict(items[1])
        item[forbidden_name] = "prefix-secret"
        items[1] = item
        result = _assemble(
            resolved_component_version_evidence_items=tuple(
                value for value in items
            )
        )
        assert result["reason_code"] == (
            "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"
        )

    for forbidden_suffix in EXPECTED_FORBIDDEN_SUFFIXES:
        forbidden_name = "probe" + forbidden_suffix
        items = list(_items())
        item = dict(items[2])
        item[forbidden_name] = "suffix-secret"
        items[2] = item
        result = _assemble(
            resolved_component_version_evidence_items=tuple(
                value for value in items
            )
        )
        assert result["reason_code"] == (
            "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"
        )


def test_normalized_forbidden_variants_and_declared_wrong_paths_block():
    variants = (
        "PASS-PUBLISHED",
        " Pass Published ",
        "LEDGER-WRITTEN",
        " runtime-result ",
    )
    for forbidden_name in variants:
        items = list(_items())
        item = dict(items[0])
        item[forbidden_name] = "caller-secret"
        items[0] = item
        result = _assemble(
            resolved_component_version_evidence_items=tuple(
                value for value in items
            )
        )
        assert result["reason_code"] == (
            "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"
        )

    items = list(_items())
    item = dict(items[0])
    item["run_id"] = "wrong-path-secret"
    items[0] = item
    wrong_path = _assemble(
        resolved_component_version_evidence_items=tuple(
            value for value in items
        )
    )
    assert wrong_path["reason_code"] == (
        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"
    )
    assert "wrong-path-secret" not in _all_scalar_strings(wrong_path)

    nested_items = _replace_item(
        _items(),
        0,
        resolver_ref={"source_of_truth": "nested-secret"},
    )
    nested_wrong_path = _assemble(
        resolved_component_version_evidence_items=nested_items
    )
    assert nested_wrong_path["reason_code"] == (
        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"
    )
    assert "nested-secret" not in _all_scalar_strings(nested_wrong_path)


def test_normalized_approved_component_key_aliases_are_forbidden():
    blocked_source = {
        "assembly_scope": "run_version_provenance_in_memory_only",
        "schema_version": "p2d45.run_version_provenance.v1",
        "component_version_count": 0,
    }
    extra_aliases = (
        "Resolved-Version",
        "resolved-version",
        "resolved version",
    )
    for alias_key in extra_aliases:
        items = list(_items())
        item = dict(items[0])
        item[alias_key] = "normalized-component-alias-secret"
        items[0] = item
        result = _assemble(
            resolved_component_version_evidence_items=tuple(items)
        )

        assert result["version_provenance_assembled"] is False
        assert result["reason_code"] == (
            "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"
        )
        assert result["assembly_violations"] == (
            "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
            "COMPONENT_EVIDENCE_ITEM_KEYS_INVALID",
        )
        assert result["source"] == blocked_source
        assert result["run_version_provenance"] == {}
        assert alias_key not in _all_nested_keys(result)
        assert alias_key not in result["reason"]
        assert "normalized-component-alias-secret" not in (
            _all_scalar_strings(result)
        )

    replacement_aliases = (
        "version-field",
        "version field",
        " version_field",
    )
    for alias_key in replacement_aliases:
        items = list(_items())
        item = dict(items[0])
        del item["version_field"]
        item[alias_key] = "normalized-component-alias-secret"
        items[0] = item
        result = _assemble(
            resolved_component_version_evidence_items=tuple(items)
        )

        assert result["version_provenance_assembled"] is False
        assert result["reason_code"] == (
            "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"
        )
        assert result["assembly_violations"] == (
            "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
            "COMPONENT_EVIDENCE_ITEM_KEYS_INVALID",
            "COMPONENT_VERSION_FIELD_INVALID",
        )
        assert result["source"] == blocked_source
        assert result["run_version_provenance"] == {}
        assert alias_key not in _all_nested_keys(result)
        assert alias_key not in result["reason"]
        assert "normalized-component-alias-secret" not in (
            _all_scalar_strings(result)
        )


def test_root_key_alias_literals_block_in_other_context():
    root_aliases = (
        "Run-ID",
        "run id",
        " run_id",
        "Resolved-At",
        "resolution-policy",
        "source of truth",
    )
    for alias_key in root_aliases:
        nested_alias = {alias_key: "root-alias-caller-secret"}
        result = _assemble(source_of_truth=(nested_alias,))

        assert result["version_provenance_assembled"] is False
        assert result["reason_code"] == (
            "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"
        )
        assert result["assembly_violations"] == (
            "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
            "SOURCE_OF_TRUTH_INVALID",
        )
        assert result["source"] == {
            "assembly_scope": "run_version_provenance_in_memory_only",
            "schema_version": "p2d45.run_version_provenance.v1",
            "component_version_count": 0,
        }
        assert result["run_version_provenance"] == {}
        assert alias_key not in _all_nested_keys(result)
        assert alias_key not in result["reason"]
        assert "root-alias-caller-secret" not in _all_scalar_strings(result)
        assert nested_alias[alias_key] == "root-alias-caller-secret"


def test_shared_component_item_is_reinspected_in_wrong_path_context():
    items = _items()
    shared_item = items[0]
    caller_source = (shared_item,)
    item_snapshot = dict(shared_item)

    result = _assemble(
        resolved_component_version_evidence_items=items,
        source_of_truth=caller_source,
    )

    assert result["reason_code"] == (
        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"
    )
    assert result["assembly_violations"] == (
        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
        "SOURCE_OF_TRUTH_INVALID",
    )
    assert shared_item is items[0]
    assert caller_source[0] is shared_item
    assert shared_item == item_snapshot
    assert "version_field" not in _all_nested_keys(result)


def test_scalar_strings_resembling_forbidden_keys_are_not_scanned():
    items = _replace_item(
        _items(),
        0,
        resolved_version="PASS_PUBLISHED",
        resolver_ref="ledger_written",
        evidence_ref="raw_payload",
    )
    result = _assemble(
        resolved_component_version_evidence_items=items,
        resolved_at="runtime_result",
        resolution_policy="publish_allowed",
        source_of_truth=(
            "Resolved-Version",
            "run-id",
            "path",
            "published",
            "raw_payload",
            "git_commit",
        ),
    )
    assert result["version_provenance_assembled"] is True
    assert result["run_version_provenance"]["skill_version"] == (
        "PASS_PUBLISHED"
    )


def test_dict_and_list_cycles_are_safe_and_caller_owned():
    dict_cycle = {}
    dict_cycle["self"] = dict_cycle
    dict_cycle["completed"] = "cycle-secret"
    items = _replace_item(_items(), 0, resolver_ref=dict_cycle)
    dict_result = _assemble(
        resolved_component_version_evidence_items=items
    )
    assert dict_result["reason_code"] == (
        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"
    )
    assert "RESOLVER_REF_INVALID" in dict_result["assembly_violations"]
    assert dict_cycle["self"] is dict_cycle
    assert dict_cycle["completed"] == "cycle-secret"
    assert "cycle-secret" not in _all_scalar_strings(dict_result)

    list_cycle = []
    list_cycle.append(list_cycle)
    list_cycle.append({"runtime-result": "list-cycle-secret"})
    list_items = _replace_item(_items(), 1, evidence_ref=list_cycle)
    list_result = _assemble(
        resolved_component_version_evidence_items=list_items
    )
    assert list_result["reason_code"] == (
        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"
    )
    assert "EVIDENCE_REF_INVALID" in list_result["assembly_violations"]
    assert list_cycle[0] is list_cycle
    assert "list-cycle-secret" not in _all_scalar_strings(list_result)


def test_list_tuple_cyclic_graph_is_deterministic_and_caller_owned():
    def fail_repr(value):
        del value
        raise AssertionError("repr must not be called for cyclic graph")

    unrepresentable_type = type(
        "CyclicGraphUnrepresentable",
        (),
        {"__repr__": fail_repr},
    )
    unrepresentable = unrepresentable_type()
    cycle_list = []
    cycle_tuple = (cycle_list,)
    cycle_list.append(cycle_tuple)
    cycle_list.append(
        {"another_unknown_key": "list-tuple-cycle-caller-secret"}
    )
    cycle_list.append(unrepresentable)

    items = _replace_item(_items(), 0, resolver_ref=cycle_list)
    result = _assemble(resolved_component_version_evidence_items=items)

    assert result["reason_code"] == (
        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"
    )
    assert result["assembly_violations"] == (
        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
        "RESOLVER_REF_INVALID",
    )
    assert result["source"] == {
        "assembly_scope": "run_version_provenance_in_memory_only",
        "schema_version": "p2d45.run_version_provenance.v1",
        "component_version_count": 0,
    }
    assert result["run_version_provenance"] == {}
    assert len(cycle_list) == 3
    assert cycle_list[0] is cycle_tuple
    assert cycle_tuple[0] is cycle_list
    assert cycle_list[1]["another_unknown_key"] == (
        "list-tuple-cycle-caller-secret"
    )
    assert cycle_list[2] is unrepresentable
    assert "another_unknown_key" not in _all_nested_keys(result)
    assert "list-tuple-cycle-caller-secret" not in _all_scalar_strings(
        result
    )


def test_deep_finite_nesting_uses_no_python_recursion():
    deep_root = {}
    cursor = deep_root
    for index in range(1500):
        next_value = {}
        cursor["node"] = next_value
        cursor = next_value
    cursor["ledger-written"] = "deep-secret"

    items = _replace_item(_items(), 2, resolver_ref=deep_root)
    result = _assemble(resolved_component_version_evidence_items=items)
    assert result["reason_code"] == "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"
    assert "RESOLVER_REF_INVALID" in result["assembly_violations"]
    assert "deep-secret" not in _all_scalar_strings(result)


def test_objects_with_failing_repr_are_never_represented_or_leaked():
    def fail_repr(value):
        del value
        raise AssertionError("repr must not be called")

    unrepresentable_type = type(
        "Unrepresentable",
        (),
        {"__repr__": fail_repr},
    )
    unrepresentable = unrepresentable_type()
    result = _assemble(source_of_truth=(unrepresentable,))
    assert result["reason_code"] == "SOURCE_OF_TRUTH_INVALID"
    assert result["run_version_provenance"] == {}


def test_semantic_positive_fields_are_not_emitted():
    forbidden_positive_fields = {
        "versions_resolved",
        "resolution_executed",
        "resolver_executed",
        "runtime_versions_verified",
        "release_verified",
        "completed",
        "executed",
        "terminal_reached",
        "noop_completed",
        "quality_pass",
        "gate_pass",
        "publish_allowed",
        "published",
        "ledger_written",
    }
    for result in (_assemble(), _assemble(run_id="")):
        keys = _all_nested_keys(result)
        assert forbidden_positive_fields.isdisjoint(keys)
        assert "version_provenance_assembled" in keys
    success_items = _assemble()["run_version_provenance"][
        "resolved_component_version_evidence_items"
    ]
    assert all(item["resolution_status"] == "resolved" for item in success_items)


def test_production_namespace_has_only_approved_imports_and_no_siblings():
    imported_modules = {
        value.__name__
        for value in builder.__dict__.values()
        if isinstance(value, types.ModuleType)
    }
    assert imported_modules == {"re"}
    assert builder.Final is not None
    for forbidden_name in (
        "pathlib",
        "os",
        "datetime",
        "hashlib",
        "logging",
        "subprocess",
        "argparse",
        "click",
        "typer",
        "yaml",
        "json",
        "inspect",
        "ast",
        "requests",
        "httpx",
        "urllib",
        "git",
        "explain_local_noop_runner_result_build",
        "runtime_context_snapshot_builder",
        "run_ledger_entry_builder",
        "resolver",
    ):
        assert forbidden_name not in builder.__dict__
