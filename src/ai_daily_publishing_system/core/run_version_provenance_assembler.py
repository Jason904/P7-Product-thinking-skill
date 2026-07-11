"""Assemble resolver-attested run version provenance in memory."""

import re
from typing import Final


COMPONENT_VERSION_FIELDS: Final[tuple[str, ...]] = (
    "skill_version",
    "rubric_version",
    "generator_version",
    "renderer_version",
    "publisher_version",
)

COMPONENT_EVIDENCE_ITEM_KEYS: Final[tuple[str, ...]] = (
    "version_field",
    "resolved_version",
    "resolution_status",
    "resolver_ref",
    "evidence_ref",
)

SCHEMA_VERSION: Final[str] = "p2d45.run_version_provenance.v1"
ASSEMBLY_SCOPE: Final[str] = "run_version_provenance_in_memory_only"
RESOLVED_VERSION_PATTERN: Final[str] = (
    r"[A-Za-z0-9][A-Za-z0-9._+-]{0,127}"
)

REASON_CODES: Final[tuple[str, ...]] = (
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

RUN_VERSION_PROVENANCE_ASSEMBLER_REASON_CODES: Final[tuple[str, ...]] = (
    REASON_CODES
)

REASON_PRIORITY: Final[tuple[str, ...]] = (
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

REASON_STRINGS: Final[tuple[tuple[str, str], ...]] = (
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

DIAGNOSTIC_PATHS: Final[
    tuple[tuple[str, tuple[str, ...]], ...]
] = (
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

INVARIANT_REFS: Final[tuple[str, ...]] = (
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

FORBIDDEN_EXACT_NAMES: Final[tuple[str, ...]] = (
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

FORBIDDEN_PREFIXES: Final[tuple[str, ...]] = (
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

FORBIDDEN_SUFFIXES: Final[tuple[str, ...]] = (
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

_CALLER_ARGUMENT_KEYS: Final[tuple[str, ...]] = (
    "run_id",
    "run_version_provenance_id",
    "resolved_component_version_evidence_items",
    "resolved_at",
    "resolution_policy",
    "source_of_truth",
)

_OUTPUT_ROOT_KEYS: Final[tuple[str, ...]] = (
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

_SUCCESS_SOURCE_KEYS: Final[tuple[str, ...]] = (
    "assembly_scope",
    "schema_version",
    "run_version_provenance_id",
    "run_id",
    "component_version_count",
    "resolved_at",
    "resolution_policy",
    "source_of_truth",
)

_NESTED_PROVENANCE_KEYS: Final[tuple[str, ...]] = (
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

_COHERENCE_RECORD_KEYS: Final[tuple[str, ...]] = (
    "component_index",
    "version_field",
    "reason_code",
    "field",
)

_SCAN_CONTEXT_ROOT: Final[str] = "root"
_SCAN_CONTEXT_COMPONENT_ITEM: Final[str] = "component_item"
_SCAN_CONTEXT_OTHER: Final[str] = "other"
_FORBIDDEN_FIELD_SENTINEL: Final[str] = (
    "p2d45v.forbidden_field_or_namespace"
)


def _is_nonblank_exact_string(value: object) -> bool:
    return type(value) is str and value.strip() != ""


def _is_valid_resolved_version(value: object) -> bool:
    return type(value) is str and re.fullmatch(
        RESOLVED_VERSION_PATTERN,
        value,
    ) is not None


def _is_valid_source_of_truth(value: object) -> bool:
    if type(value) is not tuple or len(value) == 0:
        return False
    for item in value:
        if not _is_nonblank_exact_string(item):
            return False
    return True


def _fresh_tuple(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(value for value in values)


def _has_exact_keys(
    value: dict[str, object],
    expected_keys: tuple[str, ...],
) -> bool:
    keys = tuple(value.keys())
    if len(keys) != len(expected_keys):
        return False
    for index, key in enumerate(keys):
        if type(key) is not str or key != expected_keys[index]:
            return False
    return True


def _has_only_exact_string_keys(value: dict[str, object]) -> bool:
    for key in value.keys():
        if type(key) is not str:
            return False
    return True


def _reason_text(reason_code: str) -> str:
    for known_code, reason in REASON_STRINGS:
        if known_code == reason_code:
            return reason
    return "Run version provenance was not assembled."


def _diagnostic_paths(reason_code: str) -> tuple[str, ...]:
    for known_code, paths in DIAGNOSTIC_PATHS:
        if known_code == reason_code:
            return paths
    return ()


def _add_issue(
    reason_codes: list[str],
    field_entries: list[tuple[str, str]],
    reason_code: str,
) -> None:
    if reason_code not in reason_codes:
        reason_codes.append(reason_code)
    for field in _diagnostic_paths(reason_code):
        entry = (reason_code, field)
        if entry not in field_entries:
            field_entries.append(entry)


def _safe_component_label(index: int, value: object) -> str:
    if type(value) is str and value in COMPONENT_VERSION_FIELDS:
        return value
    if 0 <= index < len(COMPONENT_VERSION_FIELDS):
        return COMPONENT_VERSION_FIELDS[index]
    return ""


def _add_component_issue(
    reason_codes: list[str],
    field_entries: list[tuple[str, str]],
    component_entries: list[tuple[str, int, str, str]],
    *,
    reason_code: str,
    component_index: int,
    version_field: object,
) -> None:
    _add_issue(reason_codes, field_entries, reason_code)
    paths = _diagnostic_paths(reason_code)
    field = paths[0] if paths else ""
    entry = (
        reason_code,
        component_index,
        _safe_component_label(component_index, version_field),
        field,
    )
    if entry not in component_entries:
        component_entries.append(entry)


def _ordered_reason_codes(reason_codes: list[str]) -> tuple[str, ...]:
    return tuple(
        reason_code
        for reason_code in REASON_PRIORITY
        if reason_code in reason_codes
    )


def _ordered_fields(
    field_entries: list[tuple[str, str]],
) -> tuple[str, ...]:
    ordered_fields = []
    for reason_code in REASON_PRIORITY:
        for entry_reason, field in field_entries:
            if entry_reason == reason_code and field not in ordered_fields:
                ordered_fields.append(field)
    return tuple(field for field in ordered_fields)


def _coherence_records(
    component_entries: list[tuple[str, int, str, str]],
) -> tuple[dict[str, object], ...]:
    ordered_entries = sorted(
        component_entries,
        key=lambda entry: (REASON_PRIORITY.index(entry[0]), entry[1]),
    )
    records = []
    for reason_code, component_index, version_field, field in ordered_entries:
        record = {
            "component_index": component_index,
            "version_field": version_field,
            "reason_code": reason_code,
            "field": field,
        }
        if record not in records:
            records.append(record)
    return tuple(record for record in records)


def _normalized_key(key: object) -> str:
    if type(key) is not str:
        return ""
    return key.strip().casefold().replace("-", "_").replace(" ", "_")


def _allowed_keys_for_scan_context(
    scan_context: str,
) -> tuple[str, ...]:
    if scan_context == _SCAN_CONTEXT_ROOT:
        return _CALLER_ARGUMENT_KEYS
    if scan_context == _SCAN_CONTEXT_COMPONENT_ITEM:
        return COMPONENT_EVIDENCE_ITEM_KEYS
    return ()


def _scan_forbidden_keys(
    value: object,
    *,
    reason_codes: list[str],
    field_entries: list[tuple[str, str]],
) -> None:
    stack = [(value, _SCAN_CONTEXT_ROOT)]
    visited: set[tuple[int, str]] = set()

    while stack:
        current, scan_context = stack.pop()
        if type(current) not in (dict, list, tuple):
            continue

        visited_key = (id(current), scan_context)
        if visited_key in visited:
            continue
        visited.add(visited_key)

        children = []
        if type(current) is dict:
            allowed_keys = _allowed_keys_for_scan_context(scan_context)
            for key, nested_value in current.items():
                raw_key_is_exactly_approved = (
                    type(key) is str
                    and key in allowed_keys
                )
                if not raw_key_is_exactly_approved:
                    _add_issue(
                        reason_codes,
                        field_entries,
                        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
                    )
                if (
                    scan_context == _SCAN_CONTEXT_ROOT
                    and key == (
                        "resolved_component_version_evidence_items"
                    )
                    and type(nested_value) is tuple
                ):
                    for item in nested_value:
                        children.append(
                            (item, _SCAN_CONTEXT_COMPONENT_ITEM)
                        )
                else:
                    children.append((nested_value, _SCAN_CONTEXT_OTHER))
        else:
            child_context = _SCAN_CONTEXT_OTHER
            for nested_value in current:
                children.append((nested_value, child_context))

        for child in reversed(children):
            stack.append(child)


def _copy_component_evidence_items(
    items: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    copied_items = []
    for item in items:
        copied_items.append(
            {
                "version_field": item["version_field"],
                "resolved_version": item["resolved_version"],
                "resolution_status": item["resolution_status"],
                "resolver_ref": item["resolver_ref"],
                "evidence_ref": item["evidence_ref"],
            }
        )
    return tuple(item for item in copied_items)


def _fresh_invariants() -> tuple[str, ...]:
    return tuple(invariant for invariant in INVARIANT_REFS)


def _blocked_source() -> dict[str, object]:
    return {
        "assembly_scope": ASSEMBLY_SCOPE,
        "schema_version": SCHEMA_VERSION,
        "component_version_count": 0,
    }


def _blocked_result(
    reason_codes: list[str],
    field_entries: list[tuple[str, str]],
    component_entries: list[tuple[str, int, str, str]],
) -> dict[str, object]:
    violations = _ordered_reason_codes(reason_codes)
    reason_code = violations[0]
    return {
        "version_provenance_assembled": False,
        "reason_code": reason_code,
        "reason": _reason_text(reason_code),
        "source": _blocked_source(),
        "run_version_provenance": {},
        "assembly_violations": violations,
        "missing_or_invalid_fields": _ordered_fields(field_entries),
        "coherence_violations": _coherence_records(component_entries),
        "invariant_refs": _fresh_invariants(),
    }


def assemble_run_version_provenance(
    *,
    run_id: str,
    run_version_provenance_id: str,
    resolved_component_version_evidence_items: tuple[
        dict[str, object], ...
    ],
    resolved_at: str,
    resolution_policy: str,
    source_of_truth: tuple[str, ...],
) -> dict[str, object]:
    """Assemble resolver-attested run version provenance in memory."""

    reason_codes = []
    field_entries = []
    component_entries = []
    caller_argument_envelope = {
        "run_id": run_id,
        "run_version_provenance_id": run_version_provenance_id,
        "resolved_component_version_evidence_items": (
            resolved_component_version_evidence_items
        ),
        "resolved_at": resolved_at,
        "resolution_policy": resolution_policy,
        "source_of_truth": source_of_truth,
    }
    _scan_forbidden_keys(
        caller_argument_envelope,
        reason_codes=reason_codes,
        field_entries=field_entries,
    )

    run_id_is_valid = _is_nonblank_exact_string(run_id)
    provenance_id_is_valid = _is_nonblank_exact_string(
        run_version_provenance_id
    )
    if not run_id_is_valid:
        _add_issue(reason_codes, field_entries, "RUN_ID_INVALID")
    if not provenance_id_is_valid:
        _add_issue(
            reason_codes,
            field_entries,
            "RUN_VERSION_PROVENANCE_ID_INVALID",
        )
    if (
        run_id_is_valid
        and provenance_id_is_valid
        and run_version_provenance_id == run_id
    ):
        _add_issue(
            reason_codes,
            field_entries,
            "RUN_VERSION_PROVENANCE_ID_NOT_DISTINCT",
        )

    safely_inspectable_items = []
    canonical_entries = []
    if type(resolved_component_version_evidence_items) is not tuple:
        _add_issue(
            reason_codes,
            field_entries,
            "COMPONENT_EVIDENCE_ITEMS_INVALID",
        )
    else:
        if len(resolved_component_version_evidence_items) != len(
            COMPONENT_VERSION_FIELDS
        ):
            _add_issue(
                reason_codes,
                field_entries,
                "COMPONENT_EVIDENCE_COUNT_INVALID",
            )

        for index, item in enumerate(
            resolved_component_version_evidence_items
        ):
            if type(item) is not dict:
                _add_component_issue(
                    reason_codes,
                    field_entries,
                    component_entries,
                    reason_code="COMPONENT_EVIDENCE_ITEM_NOT_DICT",
                    component_index=index,
                    version_field=None,
                )
                continue
            keys_are_exact = _has_exact_keys(
                item,
                COMPONENT_EVIDENCE_ITEM_KEYS,
            )
            if not keys_are_exact:
                _add_component_issue(
                    reason_codes,
                    field_entries,
                    component_entries,
                    reason_code="COMPONENT_EVIDENCE_ITEM_KEYS_INVALID",
                    component_index=index,
                    version_field=None,
                )
            if not _has_only_exact_string_keys(item):
                continue

            version_field = (
                item["version_field"]
                if "version_field" in item
                else None
            )
            safely_inspectable_items.append((index, item, version_field))
            if (
                type(version_field) is not str
                or version_field not in COMPONENT_VERSION_FIELDS
            ):
                _add_component_issue(
                    reason_codes,
                    field_entries,
                    component_entries,
                    reason_code="COMPONENT_VERSION_FIELD_INVALID",
                    component_index=index,
                    version_field=version_field,
                )
            else:
                canonical_entries.append((index, version_field))

        seen_version_fields = ()
        for index, version_field in canonical_entries:
            if version_field in seen_version_fields:
                _add_component_issue(
                    reason_codes,
                    field_entries,
                    component_entries,
                    reason_code="COMPONENT_VERSION_FIELD_DUPLICATE",
                    component_index=index,
                    version_field=version_field,
                )
            else:
                seen_version_fields = seen_version_fields + (
                    version_field,
                )

        for index, version_field in canonical_entries:
            canonical_index = COMPONENT_VERSION_FIELDS.index(version_field)
            if index != canonical_index:
                _add_component_issue(
                    reason_codes,
                    field_entries,
                    component_entries,
                    reason_code="COMPONENT_VERSION_ORDER_INVALID",
                    component_index=index,
                    version_field=version_field,
                )

        for index, item, version_field in safely_inspectable_items:
            resolved_version = (
                item["resolved_version"]
                if "resolved_version" in item
                else None
            )
            resolution_status = (
                item["resolution_status"]
                if "resolution_status" in item
                else None
            )
            resolver_ref = (
                item["resolver_ref"]
                if "resolver_ref" in item
                else None
            )
            evidence_ref = (
                item["evidence_ref"]
                if "evidence_ref" in item
                else None
            )
            if not _is_valid_resolved_version(resolved_version):
                _add_component_issue(
                    reason_codes,
                    field_entries,
                    component_entries,
                    reason_code="RESOLVED_VERSION_INVALID",
                    component_index=index,
                    version_field=version_field,
                )
            if (
                type(resolution_status) is not str
                or resolution_status != "resolved"
            ):
                _add_component_issue(
                    reason_codes,
                    field_entries,
                    component_entries,
                    reason_code="RESOLUTION_STATUS_NOT_RESOLVED",
                    component_index=index,
                    version_field=version_field,
                )
            if not _is_nonblank_exact_string(resolver_ref):
                _add_component_issue(
                    reason_codes,
                    field_entries,
                    component_entries,
                    reason_code="RESOLVER_REF_INVALID",
                    component_index=index,
                    version_field=version_field,
                )
            if not _is_nonblank_exact_string(evidence_ref):
                _add_component_issue(
                    reason_codes,
                    field_entries,
                    component_entries,
                    reason_code="EVIDENCE_REF_INVALID",
                    component_index=index,
                    version_field=version_field,
                )

    if not _is_nonblank_exact_string(resolved_at):
        _add_issue(reason_codes, field_entries, "RESOLVED_AT_INVALID")
    if not _is_nonblank_exact_string(resolution_policy):
        _add_issue(reason_codes, field_entries, "RESOLUTION_POLICY_INVALID")
    if not _is_valid_source_of_truth(source_of_truth):
        _add_issue(reason_codes, field_entries, "SOURCE_OF_TRUTH_INVALID")

    if reason_codes:
        return _blocked_result(
            reason_codes,
            field_entries,
            component_entries,
        )

    copied_evidence_items = _copy_component_evidence_items(
        resolved_component_version_evidence_items
    )
    provenance_source_of_truth = _fresh_tuple(source_of_truth)
    success_source_of_truth = _fresh_tuple(source_of_truth)
    run_version_provenance = {
        "schema_version": SCHEMA_VERSION,
        "run_version_provenance_id": run_version_provenance_id,
        "run_id": run_id,
        "skill_version": copied_evidence_items[0]["resolved_version"],
        "rubric_version": copied_evidence_items[1]["resolved_version"],
        "generator_version": copied_evidence_items[2]["resolved_version"],
        "renderer_version": copied_evidence_items[3]["resolved_version"],
        "publisher_version": copied_evidence_items[4]["resolved_version"],
        "resolved_component_version_evidence_items": (
            copied_evidence_items
        ),
        "resolved_at": resolved_at,
        "resolution_policy": resolution_policy,
        "source_of_truth": provenance_source_of_truth,
    }
    return {
        "version_provenance_assembled": True,
        "reason_code": "RUN_VERSION_PROVENANCE_ASSEMBLED_IN_MEMORY",
        "reason": _reason_text(
            "RUN_VERSION_PROVENANCE_ASSEMBLED_IN_MEMORY"
        ),
        "source": {
            "assembly_scope": ASSEMBLY_SCOPE,
            "schema_version": SCHEMA_VERSION,
            "run_version_provenance_id": run_version_provenance_id,
            "run_id": run_id,
            "component_version_count": 5,
            "resolved_at": resolved_at,
            "resolution_policy": resolution_policy,
            "source_of_truth": success_source_of_truth,
        },
        "run_version_provenance": run_version_provenance,
        "assembly_violations": (),
        "missing_or_invalid_fields": (),
        "coherence_violations": (),
        "invariant_refs": _fresh_invariants(),
    }


def is_run_version_provenance_assembled(
    *,
    run_id: str,
    run_version_provenance_id: str,
    resolved_component_version_evidence_items: tuple[
        dict[str, object], ...
    ],
    resolved_at: str,
    resolution_policy: str,
    source_of_truth: tuple[str, ...],
) -> bool:
    """Return only whether run version provenance was assembled."""

    result = assemble_run_version_provenance(
        run_id=run_id,
        run_version_provenance_id=run_version_provenance_id,
        resolved_component_version_evidence_items=(
            resolved_component_version_evidence_items
        ),
        resolved_at=resolved_at,
        resolution_policy=resolution_policy,
        source_of_truth=source_of_truth,
    )
    return result["version_provenance_assembled"]
