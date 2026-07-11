"""Assemble one validated run-ledger entry candidate in memory."""

import re
from typing import Final

from .local_noop_final_runner_result_assembler import (
    INVARIANT_REFS as _P2D44_INVARIANT_REFS,
    REASON_CODES as _P2D44_REASON_CODES,
    REASON_PRIORITY as _P2D44_REASON_PRIORITY,
)
from .run_version_provenance_assembler import (
    COMPONENT_EVIDENCE_ITEM_KEYS as _P2D45V_EVIDENCE_KEYS,
    COMPONENT_VERSION_FIELDS as _COMPONENT_VERSION_FIELDS,
    DIAGNOSTIC_PATHS as _P2D45V_DIAGNOSTIC_PATHS,
    INVARIANT_REFS as _P2D45V_INVARIANT_REFS,
    REASON_CODES as _P2D45V_REASON_CODES,
    REASON_PRIORITY as _P2D45V_REASON_PRIORITY,
    REASON_STRINGS as _P2D45V_REASON_STRINGS,
    RESOLVED_VERSION_PATTERN as _P2D45V_RESOLVED_VERSION_PATTERN,
    SCHEMA_VERSION as _P2D45V_SCHEMA_VERSION,
)


SCHEMA_VERSION: Final[str] = "p2d45.run_ledger_entry.v1"
ASSEMBLY_SCOPE: Final[str] = "run_ledger_entry_in_memory_only"
ENTRY_KIND: Final[str] = "run_ledger_entry"
VERSION_PATTERN: Final[str] = _P2D45V_RESOLVED_VERSION_PATTERN

VALID_SUCCESS: Final[str] = "VALID_SUCCESS"
VALID_BLOCKED: Final[str] = "VALID_BLOCKED"
INVALID: Final[str] = "INVALID"

REASON_CODES: Final[tuple[str, ...]] = (
    "RUN_LEDGER_ENTRY_ASSEMBLED_IN_MEMORY",
    "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
    "RUN_LEDGER_ENTRY_ID_INVALID",
    "P2D44_FINAL_RUNNER_RESULT_INVALID",
    "P2D44_FINAL_RUNNER_RESULT_NOT_ASSEMBLED",
    "P2D45V_PROVENANCE_RESULT_INVALID",
    "P2D45V_PROVENANCE_NOT_ASSEMBLED",
    "P2D45V_SCHEMA_VERSION_INCOMPATIBLE",
    "PASS_PUBLISHED_FORBIDDEN",
    "MODE_NOT_NOOP",
    "LEDGER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
    "PUBLIC_URL_NON_NULL",
    "PUBLIC_URL_CREATED_NOT_FALSE",
    "RUN_ID_MISMATCH",
    "P2D44_SOURCE_COHERENCE_MISMATCH",
    "P2D45V_PROVENANCE_COHERENCE_MISMATCH",
    "RUNNER_EVIDENCE_PROJECTION_INVALID",
    "VERSION_EVIDENCE_PROJECTION_INVALID",
)

RUN_LEDGER_ENTRY_ASSEMBLER_REASON_CODES: Final[tuple[str, ...]] = REASON_CODES

REASON_PRIORITY: Final[tuple[str, ...]] = (
    "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
    "RUN_LEDGER_ENTRY_ID_INVALID",
    "P2D44_FINAL_RUNNER_RESULT_INVALID",
    "P2D45V_PROVENANCE_RESULT_INVALID",
    "P2D44_FINAL_RUNNER_RESULT_NOT_ASSEMBLED",
    "P2D45V_PROVENANCE_NOT_ASSEMBLED",
    "P2D45V_SCHEMA_VERSION_INCOMPATIBLE",
    "PASS_PUBLISHED_FORBIDDEN",
    "MODE_NOT_NOOP",
    "LEDGER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
    "PUBLIC_URL_NON_NULL",
    "PUBLIC_URL_CREATED_NOT_FALSE",
    "RUN_ID_MISMATCH",
    "P2D44_SOURCE_COHERENCE_MISMATCH",
    "P2D45V_PROVENANCE_COHERENCE_MISMATCH",
    "RUNNER_EVIDENCE_PROJECTION_INVALID",
    "VERSION_EVIDENCE_PROJECTION_INVALID",
    "RUN_LEDGER_ENTRY_ASSEMBLED_IN_MEMORY",
)

REASON_STRINGS: Final[tuple[tuple[str, str], ...]] = (
    (
        "RUN_LEDGER_ENTRY_ASSEMBLED_IN_MEMORY",
        "A deterministic run-ledger entry candidate was assembled in memory.",
    ),
    (
        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
        "A forbidden field or namespace was supplied; caller key names and values are suppressed.",
    ),
    (
        "RUN_LEDGER_ENTRY_ID_INVALID",
        "run_ledger_entry_id must be an exact nonblank string.",
    ),
    (
        "P2D44_FINAL_RUNNER_RESULT_INVALID",
        "The complete P2D-44 final runner-result assembly is invalid.",
    ),
    (
        "P2D44_FINAL_RUNNER_RESULT_NOT_ASSEMBLED",
        "P2D-44 returned a valid blocked envelope and did not assemble a final runner-result object.",
    ),
    (
        "P2D45V_PROVENANCE_RESULT_INVALID",
        "The complete P2D-45V run-version provenance assembly is invalid.",
    ),
    (
        "P2D45V_PROVENANCE_NOT_ASSEMBLED",
        "P2D-45V returned a valid blocked envelope and did not assemble run-version provenance.",
    ),
    (
        "P2D45V_SCHEMA_VERSION_INCOMPATIBLE",
        "The P2D-45V provenance schema version is incompatible.",
    ),
    (
        "PASS_PUBLISHED_FORBIDDEN",
        "PASS_PUBLISHED is forbidden at this run-ledger entry boundary.",
    ),
    ("MODE_NOT_NOOP", "The recorded mode must be noop."),
    (
        "LEDGER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
        "The recorded ledger terminal status must be NOOP_COMPLETED.",
    ),
    ("PUBLIC_URL_NON_NULL", "The recorded public URL must be null."),
    (
        "PUBLIC_URL_CREATED_NOT_FALSE",
        "The recorded public URL-created marker must be false.",
    ),
    ("RUN_ID_MISMATCH", "The P2D-44 and P2D-45V run IDs do not match."),
    (
        "P2D44_SOURCE_COHERENCE_MISMATCH",
        "The P2D-44 source and final runner-result object are not coherent.",
    ),
    (
        "P2D45V_PROVENANCE_COHERENCE_MISMATCH",
        "The P2D-45V source and run-version provenance object are not coherent.",
    ),
    (
        "RUNNER_EVIDENCE_PROJECTION_INVALID",
        "The validated runner evidence cannot be projected safely.",
    ),
    (
        "VERSION_EVIDENCE_PROJECTION_INVALID",
        "The validated version evidence cannot be projected safely.",
    ),
)

DIAGNOSTIC_PATHS: Final[tuple[tuple[str, tuple[str, ...]], ...]] = (
    ("RUN_LEDGER_ENTRY_ASSEMBLED_IN_MEMORY", ()),
    (
        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
        ("p2d45a.forbidden_field_or_namespace",),
    ),
    ("RUN_LEDGER_ENTRY_ID_INVALID", ("run_ledger_entry_id",)),
    (
        "P2D44_FINAL_RUNNER_RESULT_INVALID",
        ("local_noop_final_runner_result_assembly",),
    ),
    (
        "P2D44_FINAL_RUNNER_RESULT_NOT_ASSEMBLED",
        ("local_noop_final_runner_result_assembly",),
    ),
    (
        "P2D45V_PROVENANCE_RESULT_INVALID",
        ("run_version_provenance_assembly",),
    ),
    (
        "P2D45V_PROVENANCE_NOT_ASSEMBLED",
        ("run_version_provenance_assembly",),
    ),
    (
        "P2D45V_SCHEMA_VERSION_INCOMPATIBLE",
        ("run_version_provenance.schema_version",),
    ),
    ("PASS_PUBLISHED_FORBIDDEN", ("interpreted_semantic_fields",)),
    ("MODE_NOT_NOOP", ("local_noop_runner_result.mode",)),
    (
        "LEDGER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
        ("local_noop_runner_result.runner_terminal_status",),
    ),
    ("PUBLIC_URL_NON_NULL", ("local_noop_runner_result.public_url",)),
    (
        "PUBLIC_URL_CREATED_NOT_FALSE",
        ("local_noop_runner_result.public_url_created",),
    ),
    ("RUN_ID_MISMATCH", ("run_id",)),
    (
        "P2D44_SOURCE_COHERENCE_MISMATCH",
        ("local_noop_final_runner_result_assembly.source",),
    ),
    (
        "P2D45V_PROVENANCE_COHERENCE_MISMATCH",
        ("run_version_provenance_assembly.source",),
    ),
    (
        "RUNNER_EVIDENCE_PROJECTION_INVALID",
        ("local_noop_runner_result.runner_evidence_items",),
    ),
    (
        "VERSION_EVIDENCE_PROJECTION_INVALID",
        ("run_version_provenance.resolved_component_version_evidence_items",),
    ),
)

INVARIANT_REFS: Final[tuple[str, ...]] = (
    "run_ledger_entry_assembler_only",
    "assembler_pure_in_memory_only",
    "assembler_accepts_complete_p2d44_and_p2d45v_results",
    "upstream_envelope_classification_is_three_way",
    "valid_success_envelope_requires_complete_success_contract",
    "valid_blocked_envelope_requires_complete_blocked_contract",
    "malformed_envelope_is_invalid",
    "valid_blocked_and_invalid_are_mutually_exclusive",
    "nested_upstream_bypass_rejected",
    "upstream_assemblers_not_invoked",
    "upstream_contract_constants_only_dependency",
    "explicit_run_ledger_entry_id_required",
    "run_ledger_entry_id_is_opaque_caller_identity",
    "run_ledger_entry_id_not_generated_or_derived",
    "run_id_projected_from_p2d44",
    "p2d44_and_p2d45v_run_ids_must_match",
    "p2d44_source_and_result_coherence_required",
    "p2d45v_source_and_provenance_coherence_required",
    "exactly_five_component_versions_required",
    "component_version_order_fixed",
    "direct_ledger_version_fields_are_authoritative",
    "version_evidence_projection_must_match_direct_versions",
    "run_version_provenance_id_link_required",
    "run_version_provenance_schema_compatibility_required",
    "resolver_refs_are_opaque",
    "evidence_refs_are_opaque",
    "no_actual_resolver_payload_in_ledger",
    "runner_evidence_projected_without_value_change",
    "runner_evidence_notes_not_projected",
    "failed_runner_evidence_may_be_recorded",
    "known_blocking_evidence_ids_are_evidence_only",
    "source_of_truth_combines_p2d44_then_p2d45v",
    "source_of_truth_order_and_duplicates_preserved",
    "independent_timestamps_not_compared",
    "independent_policies_not_compared",
    "caller_input_not_mutated",
    "output_containers_are_fresh",
    "nonempty_output_tuples_are_identity_isolated",
    "empty_tuple_identity_not_required",
    "blocked_output_is_fixed_and_caller_safe",
    "unknown_keys_block_and_are_suppressed",
    "aliases_and_wrong_path_keys_block",
    "validation_is_cycle_and_depth_safe",
    "scalar_strings_are_not_scanned_as_keys",
    "mode_noop_required",
    "ledger_terminal_status_must_be_noop_completed",
    "recorded_terminal_status_is_upstream_metadata_only",
    "public_url_must_be_null",
    "public_url_created_must_be_false",
    "pass_published_forbidden",
    "no_quality_pass_no_public_url",
    "run_ledger_entry_assembled_means_in_memory_candidate_only",
    "assembly_not_runtime_completion",
    "assembly_not_state_decision",
    "assembly_not_state_transition",
    "assembly_not_ledger_persistence",
    "assembly_not_publish_authorization",
    "assembly_not_publication",
    "assembly_not_public_url_creation",
    "assembly_not_notification",
    "no_file_or_artifact_io",
    "no_run_ledger_yaml_read_or_write",
    "no_git_or_release_inspection",
    "no_clock_or_environment_access",
    "no_resolver_execution",
    "no_runtime_or_external_api_call",
    "no_live_model_call",
)

_P2D44_ROOT_KEYS: Final[tuple[str, ...]] = (
    "final_result_object_assembled",
    "reason_code",
    "reason",
    "source",
    "local_noop_runner_result",
    "assembly_violations",
    "missing_or_invalid_fields",
    "result_validation_violations",
    "invariant_refs",
)
_P2D44_SOURCE_KEYS: Final[tuple[str, ...]] = (
    "p2d43_decision_created",
    "p2d43_reason_code",
    "p2d42_consumed",
    "p2d42_reason_code",
    "p2d33_buildable",
    "p2d33_reason_code",
    "p2d35_buildable",
    "p2d35_reason_code",
    "run_id",
    "local_noop_runner_result_id",
    "local_noop_runner_result_candidate_id",
    "local_noop_e2e_contract_ref",
    "mode",
    "runner_terminal_status",
    "public_url",
    "public_url_created",
    "source_of_truth",
)
_P2D44_RESULT_KEYS: Final[tuple[str, ...]] = (
    "run_id",
    "local_noop_runner_result_id",
    "result_kind",
    "mode",
    "runner_terminal_status",
    "local_noop_e2e_contract_ref",
    "local_noop_e2e_contract_buildable_marker",
    "public_url",
    "public_url_created",
    "runner_evidence_items",
    "required_runner_evidence_ids",
    "missing_runner_evidence_ids",
    "blocking_runner_evidence_ids",
    "created_at",
    "timestamp_policy",
    "source_of_truth",
    "notes",
)
_P2D44_EVIDENCE_KEYS: Final[tuple[str, ...]] = (
    "runner_evidence_id",
    "runner_evidence_role",
    "artifact_ref",
    "artifact_kind",
    "evidence_status",
    "producer_ref",
    "evidence_refs",
    "notes",
)
_P2D44_DIAGNOSTIC_RECORD_KEYS: Final[tuple[str, ...]] = (
    "reason_code",
    "field",
)

_P2D45V_ROOT_KEYS: Final[tuple[str, ...]] = (
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
_P2D45V_SOURCE_KEYS: Final[tuple[str, ...]] = (
    "assembly_scope",
    "schema_version",
    "run_version_provenance_id",
    "run_id",
    "component_version_count",
    "resolved_at",
    "resolution_policy",
    "source_of_truth",
)
_P2D45V_PROVENANCE_KEYS: Final[tuple[str, ...]] = (
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
_P2D45V_COHERENCE_RECORD_KEYS: Final[tuple[str, ...]] = (
    "component_index",
    "version_field",
    "reason_code",
    "field",
)

_OUTPUT_KEYS: Final[tuple[str, ...]] = (
    "run_ledger_entry_assembled",
    "reason_code",
    "reason",
    "source",
    "run_ledger_entry",
    "assembly_violations",
    "missing_or_invalid_fields",
    "coherence_violations",
    "invariant_refs",
)
_SUCCESS_SOURCE_KEYS: Final[tuple[str, ...]] = (
    "assembly_scope",
    "schema_version",
    "run_ledger_entry_id",
    "run_id",
    "local_noop_runner_result_id",
    "run_version_provenance_id",
    "run_version_provenance_schema_version",
    "mode",
    "ledger_terminal_status",
    "public_url",
    "public_url_created",
    "component_version_count",
    "source_of_truth",
)
_ENTRY_KEYS: Final[tuple[str, ...]] = (
    "schema_version",
    "run_ledger_entry_id",
    "run_id",
    "entry_kind",
    "mode",
    "ledger_terminal_status",
    "local_noop_runner_result_id",
    "local_noop_e2e_contract_ref",
    "public_url",
    "public_url_created",
    "runner_evidence_items",
    "required_runner_evidence_ids",
    "missing_runner_evidence_ids",
    "blocking_runner_evidence_ids",
    "runner_result_created_at",
    "runner_result_timestamp_policy",
    "run_version_provenance_id",
    "run_version_provenance_schema_version",
    "skill_version",
    "rubric_version",
    "generator_version",
    "renderer_version",
    "publisher_version",
    "resolved_component_version_evidence_items",
    "version_provenance_resolved_at",
    "version_provenance_resolution_policy",
    "source_of_truth",
)
_PROJECTED_RUNNER_EVIDENCE_KEYS: Final[tuple[str, ...]] = (
    "runner_evidence_id",
    "runner_evidence_role",
    "artifact_ref",
    "artifact_kind",
    "evidence_status",
    "producer_ref",
    "evidence_refs",
)

_P2D44_SUCCESS_REASON: Final[str] = (
    "A final local noop runner-result object was assembled in memory."
)
_P2D44_REASON_STRINGS: Final[tuple[tuple[str, str], ...]] = (
    (
        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
        "A forbidden field or namespace was supplied.",
    ),
    (
        "P2D43_DECISION_RESULT_INVALID",
        "The complete P2D-43 decision result is invalid.",
    ),
    (
        "P2D42_CONSUMPTION_RESULT_INVALID",
        "The complete P2D-42 consumption result is invalid.",
    ),
    (
        "P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID",
        "The complete P2D-33 E2E contract build result is invalid.",
    ),
    (
        "FINAL_RUNNER_RESULT_ID_INVALID",
        "A nonblank caller-supplied final runner-result ID is required.",
    ),
    (
        "FINAL_RUNNER_RESULT_ID_NOT_DISTINCT",
        "The final runner-result ID must be distinct from upstream identities.",
    ),
    (
        "CROSS_LAYER_COHERENCE_MISMATCH",
        "The validated upstream results are not coherent.",
    ),
    (
        "PASS_PUBLISHED_FORBIDDEN",
        "PASS_PUBLISHED is forbidden at this noop boundary.",
    ),
    (
        "EVIDENCE_PROJECTION_INVALID",
        "The candidate evidence cannot be projected safely.",
    ),
    (
        "P2D35_BUILD_RESULT_REJECTED",
        "The P2D-35 result builder rejected the validated input.",
    ),
    (
        "P2D35_BUILD_RESULT_INVALID",
        "The P2D-35 result builder returned an invalid result.",
    ),
    (
        "P2D35_OUTPUT_COHERENCE_MISMATCH",
        "The P2D-35 result is not coherent with validated inputs.",
    ),
)
_P2D44_SAFE_PATHS: Final[tuple[tuple[str, tuple[str, ...]], ...]] = (
    ("FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT", ("p2d44.forbidden_field_or_namespace",)),
    ("P2D43_DECISION_RESULT_INVALID", (
        "p2d44.p2d43_result", "p2d44.p2d43_result.keys",
        "p2d44.p2d43_result.source.keys", "p2d44.p2d43_result.decision.keys",
    )),
    ("P2D42_CONSUMPTION_RESULT_INVALID", (
        "p2d44.p2d42_result", "p2d44.p2d42_result.keys",
        "p2d44.p2d42_result.source.keys", "p2d44.p2d42_result.candidate.keys",
        "p2d44.p2d42_result.receipt.keys",
    )),
    ("P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID", (
        "p2d44.p2d33_result", "p2d44.p2d33_result.keys",
        "p2d44.p2d33_result.source.keys", "p2d44.p2d33_result.contract.keys",
    )),
    ("FINAL_RUNNER_RESULT_ID_INVALID", ("p2d44.local_noop_runner_result_id",)),
    ("FINAL_RUNNER_RESULT_ID_NOT_DISTINCT", ("p2d44.local_noop_runner_result_id",)),
    ("CROSS_LAYER_COHERENCE_MISMATCH", ("p2d44.cross_layer_coherence",)),
    ("PASS_PUBLISHED_FORBIDDEN", (
        "p2d44.p2d42_result.candidate.evidence_items.keys",
        "p2d44.p2d42_result.candidate.keys",
        "p2d44.p2d33_result.contract.keys", "p2d44.p2d35_result",
    )),
    ("EVIDENCE_PROJECTION_INVALID", ("p2d44.p2d42_result.candidate.evidence_items.keys",)),
    ("P2D35_BUILD_RESULT_REJECTED", ("p2d44.p2d35_result",)),
    ("P2D35_BUILD_RESULT_INVALID", (
        "p2d44.p2d35_result", "p2d44.p2d35_result.keys",
        "p2d44.p2d35_result.source.keys",
        "p2d44.p2d35_result.local_noop_runner_result.keys",
    )),
    ("P2D35_OUTPUT_COHERENCE_MISMATCH", (
        "p2d44.p2d35_result", "p2d44.p2d35_result.source.keys",
    )),
)


def _fresh_tuple(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(value for value in values)


def _is_nonblank_string(value: object) -> bool:
    return type(value) is str and value.strip() != ""


def _is_valid_version(value: object) -> bool:
    if type(value) is not str:
        return False
    return re.fullmatch(VERSION_PATTERN, value) is not None


def _is_string_tuple(value: object, *, nonempty: bool = False) -> bool:
    if type(value) is not tuple:
        return False
    if nonempty and len(value) == 0:
        return False
    for item in value:
        if type(item) is not str:
            return False
    if nonempty:
        for item in value:
            if item.strip() == "":
                return False
    return True


def _is_empty_tuple(value: object) -> bool:
    return type(value) is tuple and len(value) == 0


def _fixed_string(value: object, expected: str) -> bool:
    return type(value) is str and value == expected


def _fixed_int(value: object, expected: int) -> bool:
    return type(value) is int and value == expected


def _same_string_tuples(left: object, right: object) -> bool:
    if not _is_string_tuple(left) or not _is_string_tuple(right):
        return False
    if len(left) != len(right):
        return False
    for index, item in enumerate(left):
        if item != right[index]:
            return False
    return True


def _exact_keys(value: object, expected: tuple[str, ...]) -> bool:
    if type(value) is not dict:
        return False
    actual = tuple(value.keys())
    for key in actual:
        if type(key) is not str:
            return False
    if len(actual) != len(expected):
        return False
    for index, key in enumerate(actual):
        if key != expected[index]:
            return False
    return True


def _shape_has_forbidden_key(value: object, expected: tuple[str, ...]) -> bool:
    if type(value) is not dict:
        return False
    keys = tuple(value.keys())
    for key in keys:
        if type(key) is not str:
            return True
    for key in keys:
        if key not in expected:
            return True
    return False


def _same(left: object, right: object) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is str:
        return left == right
    if type(left) is bool:
        return left is right
    if type(left) is int:
        return left == right
    if left is None:
        return True
    if type(left) is tuple:
        return _same_string_tuples(left, right)
    return False


def _lookup(entries: tuple[tuple[str, object], ...], key: object) -> object:
    if type(key) is not str:
        return ()
    for known_key, value in entries:
        if known_key == key:
            return value
    return ()


def _p2d44_reason(code: str) -> str:
    value = _lookup(_P2D44_REASON_STRINGS, code)
    return value if type(value) is str else ""


def _p2d45v_reason(code: str) -> str:
    value = _lookup(_P2D45V_REASON_STRINGS, code)
    return value if type(value) is str else ""


def _p2d45v_paths(code: str) -> tuple[str, ...]:
    value = _lookup(_P2D45V_DIAGNOSTIC_PATHS, code)
    return value if type(value) is tuple else ()


def _reason_text(code: str) -> str:
    value = _lookup(REASON_STRINGS, code)
    return value if type(value) is str else "Run-ledger entry was not assembled."


def _paths(code: str) -> tuple[str, ...]:
    value = _lookup(DIAGNOSTIC_PATHS, code)
    return value if type(value) is tuple else ()


def _ordered(codes: list[str]) -> tuple[str, ...]:
    return tuple(code for code in REASON_PRIORITY if code in codes)


def _p2d44_blocked_diagnostics_valid(value: dict[str, object]) -> bool:
    violations = value["assembly_violations"]
    fields = value["missing_or_invalid_fields"]
    records = value["result_validation_violations"]
    if not _is_string_tuple(violations, nonempty=True):
        return False
    allowed = _P2D44_REASON_CODES[1:]
    for code in violations:
        if code not in allowed:
            return False
    if len(set(violations)) != len(violations):
        return False
    expected_violations = tuple(
        code for code in _P2D44_REASON_PRIORITY if code in violations
    )
    if not _same_string_tuples(expected_violations, violations):
        return False
    reason_code = value["reason_code"]
    reason = value["reason"]
    if type(reason_code) is not str or type(reason) is not str:
        return False
    if reason_code != violations[0] or reason != _p2d44_reason(violations[0]):
        return False
    if type(records) is not tuple or not _is_string_tuple(fields):
        return False
    previous_rank = -1
    projected_fields = []
    seen_records = []
    record_codes = []
    for record in records:
        if not _exact_keys(record, _P2D44_DIAGNOSTIC_RECORD_KEYS):
            return False
        code = record["reason_code"]
        field = record["field"]
        if type(code) is not str or type(field) is not str:
            return False
        safe_paths = _lookup(_P2D44_SAFE_PATHS, code)
        if not _is_string_tuple(safe_paths):
            return False
        if code not in violations or field not in safe_paths:
            return False
        rank = _P2D44_REASON_PRIORITY.index(code)
        if rank < previous_rank:
            return False
        previous_rank = rank
        pair = (code, field)
        if pair in seen_records:
            return False
        seen_records.append(pair)
        record_codes.append(code)
        if field not in projected_fields:
            projected_fields.append(field)
    if not _same_string_tuples(tuple(projected_fields), fields):
        return False
    return all(code in record_codes for code in violations)


def _p2d45v_component_label_valid(
    index: int,
    label: str,
    code: str,
) -> bool:
    fallback_label_codes = (
        "COMPONENT_EVIDENCE_ITEM_NOT_DICT",
        "COMPONENT_EVIDENCE_ITEM_KEYS_INVALID",
        "COMPONENT_VERSION_FIELD_INVALID",
    )
    if code in fallback_label_codes:
        if index < len(_COMPONENT_VERSION_FIELDS):
            return label == _COMPONENT_VERSION_FIELDS[index]
        return label == ""

    if code == "COMPONENT_VERSION_FIELD_DUPLICATE":
        return index > 0 and label in _COMPONENT_VERSION_FIELDS

    if code == "COMPONENT_VERSION_ORDER_INVALID":
        if label not in _COMPONENT_VERSION_FIELDS:
            return False
        return index != _COMPONENT_VERSION_FIELDS.index(label)

    value_validation_codes = (
        "RESOLVED_VERSION_INVALID",
        "RESOLUTION_STATUS_NOT_RESOLVED",
        "RESOLVER_REF_INVALID",
        "EVIDENCE_REF_INVALID",
    )
    if code not in value_validation_codes:
        return False
    if index < len(_COMPONENT_VERSION_FIELDS):
        return label in _COMPONENT_VERSION_FIELDS
    return label == "" or label in _COMPONENT_VERSION_FIELDS


def _p2d45v_records_at_index(
    records: tuple[tuple[str, int, str, str], ...],
    index: int,
) -> tuple[tuple[str, int, str, str], ...]:
    return tuple(record for record in records if record[1] == index)


def _p2d45v_record_present(
    records: tuple[tuple[str, int, str, str], ...],
    *,
    code: str,
    index: int,
    label: str,
) -> bool:
    for record_code, record_index, record_label, _field in records:
        if (
            record_code == code
            and record_index == index
            and record_label == label
        ):
            return True
    return False


def _p2d45v_component_index_state(
    records: tuple[tuple[str, int, str, str], ...],
    *,
    index: int,
    forbidden_present: bool,
) -> tuple[bool, str, str]:
    """Return the strongest producer-visible state for one item index."""

    indexed = _p2d45v_records_at_index(records, index)
    if not indexed:
        if index >= len(_COMPONENT_VERSION_FIELDS):
            return False, "", ""
        return True, "canonical", _COMPONENT_VERSION_FIELDS[index]

    codes = []
    for code, _record_index, _label, _field in indexed:
        if code in codes:
            return False, "", ""
        codes.append(code)

    if "COMPONENT_EVIDENCE_ITEM_NOT_DICT" in codes:
        if len(indexed) != 1:
            return False, "", ""
        return True, "noncanonical", ""

    has_keys = "COMPONENT_EVIDENCE_ITEM_KEYS_INVALID" in codes
    has_field = "COMPONENT_VERSION_FIELD_INVALID" in codes
    has_duplicate = "COMPONENT_VERSION_FIELD_DUPLICATE" in codes
    has_order = "COMPONENT_VERSION_ORDER_INVALID" in codes
    value_codes = (
        "RESOLVED_VERSION_INVALID",
        "RESOLUTION_STATUS_NOT_RESOLVED",
        "RESOLVER_REF_INVALID",
        "EVIDENCE_REF_INVALID",
    )
    fallback = (
        _COMPONENT_VERSION_FIELDS[index]
        if index < len(_COMPONENT_VERSION_FIELDS)
        else ""
    )

    if has_field:
        if has_duplicate or has_order:
            return False, "", ""
        for code, _record_index, label, _field in indexed:
            if code in value_codes and label != fallback:
                return False, "", ""
        return True, "noncanonical", ""

    # Without a field-invalid record, an expected-position value label can be
    # the actual canonical field; the published envelope cannot prove that it
    # came from the producer's positional fallback.
    actual_labels = []
    for code, _record_index, label, _field in indexed:
        if code in value_codes or code in (
            "COMPONENT_VERSION_FIELD_DUPLICATE",
            "COMPONENT_VERSION_ORDER_INVALID",
        ):
            if label not in _COMPONENT_VERSION_FIELDS:
                return False, "", ""
            if label not in actual_labels:
                actual_labels.append(label)
    if len(actual_labels) > 1:
        return False, "", ""
    if actual_labels:
        actual_label = actual_labels[0]
        expected_order = (
            index != _COMPONENT_VERSION_FIELDS.index(actual_label)
        )
        if has_order is not expected_order:
            return False, "", ""
        return True, "canonical", actual_label

    if not has_keys:
        return False, "", ""
    if index >= len(_COMPONENT_VERSION_FIELDS):
        # A keys-only surplus record requires the producer's non-string-key
        # short circuit, which also publishes the forbidden-key reason.
        if not forbidden_present:
            return False, "", ""
        return True, "noncanonical", ""
    # With a published forbidden-key reason, keys-only can be either a
    # reordered canonical item or a non-string-key short circuit.  Preserve
    # that ambiguity; without it, reordered expected canonical is mandatory.
    if forbidden_present:
        return True, "optional_expected", _COMPONENT_VERSION_FIELDS[index]
    return True, "canonical", _COMPONENT_VERSION_FIELDS[index]


def _p2d45v_component_length_reachable(
    violations: tuple[str, ...],
    records: tuple[tuple[str, int, str, str], ...],
    length: int,
) -> bool:
    count_invalid = "COMPONENT_EVIDENCE_COUNT_INVALID" in violations
    if count_invalid != (length != len(_COMPONENT_VERSION_FIELDS)):
        return False
    for _code, index, _label, _field in records:
        if index >= length:
            return False

    forbidden_present = "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT" in violations
    states = []
    for index in range(length):
        state_valid, state_kind, state_label = (
            _p2d45v_component_index_state(
                records,
                index=index,
                forbidden_present=forbidden_present,
            )
        )
        if not state_valid:
            return False
        states.append((state_kind, state_label))

    for component_label in _COMPONENT_VERSION_FIELDS:
        possible_seen_states = [False]
        for index, state in enumerate(states):
            state_kind, state_label = state
            has_duplicate = _p2d45v_record_present(
                records,
                code="COMPONENT_VERSION_FIELD_DUPLICATE",
                index=index,
                label=component_label,
            )
            next_seen_states = []
            if state_kind == "canonical" and state_label == component_label:
                for already_seen in possible_seen_states:
                    if (
                        has_duplicate is already_seen
                        and True not in next_seen_states
                    ):
                        next_seen_states.append(True)
            elif (
                state_kind == "optional_expected"
                and state_label == component_label
            ):
                if has_duplicate:
                    return False
                for already_seen in possible_seen_states:
                    if already_seen not in next_seen_states:
                        next_seen_states.append(already_seen)
                    if not already_seen and True not in next_seen_states:
                        next_seen_states.append(True)
            else:
                if has_duplicate:
                    return False
                next_seen_states = list(possible_seen_states)
            if not next_seen_states:
                return False
            possible_seen_states = next_seen_states
    return True


def _p2d45v_coherence_collection_reachable(
    violations: tuple[str, ...],
    records: tuple[tuple[str, int, str, str], ...],
) -> bool:
    """Validate deterministic consequences published by P2D-45V."""

    component_items_invalid = (
        "COMPONENT_EVIDENCE_ITEMS_INVALID" in violations
    )
    if component_items_invalid:
        return (
            "COMPONENT_EVIDENCE_COUNT_INVALID" not in violations
            and len(records) == 0
        )

    count_invalid = "COMPONENT_EVIDENCE_COUNT_INVALID" in violations
    maximum_index = -1
    for _code, index, _label, _field in records:
        if index > maximum_index:
            maximum_index = index

    candidate_lengths = []
    if not count_invalid:
        candidate_lengths.append(len(_COMPONENT_VERSION_FIELDS))
    elif maximum_index >= len(_COMPONENT_VERSION_FIELDS):
        candidate_lengths.append(maximum_index + 1)
    else:
        for length in range(
            maximum_index + 1,
            len(_COMPONENT_VERSION_FIELDS),
        ):
            candidate_lengths.append(length)

    for length in candidate_lengths:
        if _p2d45v_component_length_reachable(
            violations,
            records,
            length,
        ):
            return True
    return False


def _p2d45v_blocked_diagnostics_valid(value: dict[str, object]) -> bool:
    violations = value["assembly_violations"]
    fields = value["missing_or_invalid_fields"]
    records = value["coherence_violations"]
    if not _is_string_tuple(violations, nonempty=True):
        return False
    allowed = _P2D45V_REASON_CODES[1:]
    for code in violations:
        if code not in allowed:
            return False
    if len(set(violations)) != len(violations):
        return False
    expected_violations = tuple(
        code for code in _P2D45V_REASON_PRIORITY if code in violations
    )
    if not _same_string_tuples(expected_violations, violations):
        return False
    reason_code = value["reason_code"]
    reason = value["reason"]
    if type(reason_code) is not str or type(reason) is not str:
        return False
    if reason_code != violations[0] or reason != _p2d45v_reason(violations[0]):
        return False
    expected_fields = []
    for code in violations:
        for field in _p2d45v_paths(code):
            if field not in expected_fields:
                expected_fields.append(field)
    if not _is_string_tuple(fields) or type(records) is not tuple:
        return False
    if not _same_string_tuples(fields, tuple(expected_fields)):
        return False
    component_codes = (
        "COMPONENT_EVIDENCE_ITEM_NOT_DICT",
        "COMPONENT_EVIDENCE_ITEM_KEYS_INVALID",
        "COMPONENT_VERSION_FIELD_INVALID",
        "COMPONENT_VERSION_FIELD_DUPLICATE",
        "COMPONENT_VERSION_ORDER_INVALID",
        "RESOLVED_VERSION_INVALID",
        "RESOLUTION_STATUS_NOT_RESOLVED",
        "RESOLVER_REF_INVALID",
        "EVIDENCE_REF_INVALID",
    )
    previous = (-1, -1)
    seen = []
    record_codes = []
    validated_records = []
    for record in records:
        if not _exact_keys(record, _P2D45V_COHERENCE_RECORD_KEYS):
            return False
        index = record["component_index"]
        label = record["version_field"]
        code = record["reason_code"]
        field = record["field"]
        if (
            type(index) is not int
            or type(label) is not str
            or type(code) is not str
            or type(field) is not str
        ):
            return False
        if index < 0:
            return False
        safe_paths = _p2d45v_paths(code)
        if not _is_string_tuple(safe_paths):
            return False
        if code not in violations or code not in component_codes or field not in safe_paths:
            return False
        if not _p2d45v_component_label_valid(index, label, code):
            return False
        ordering = (_P2D45V_REASON_PRIORITY.index(code), index)
        if ordering < previous or (code, index, label, field) in seen:
            return False
        previous = ordering
        seen.append((code, index, label, field))
        record_codes.append(code)
        validated_records.append((code, index, label, field))
    if not all(
        code not in component_codes or code in record_codes
        for code in violations
    ):
        return False
    return _p2d45v_coherence_collection_reachable(
        violations,
        tuple(validated_records),
    )


def _p2d44_evidence_valid(items: object) -> bool:
    if type(items) is not tuple or len(items) == 0:
        return False
    for item in items:
        if not _exact_keys(item, _P2D44_EVIDENCE_KEYS):
            return False
    for item in items:
        for key in _P2D44_EVIDENCE_KEYS[:6]:
            if not _is_nonblank_string(item[key]):
                return False
        if not _is_string_tuple(item["evidence_refs"], nonempty=True):
            return False
        if not _is_string_tuple(item["notes"]):
            return False
    identifiers = []
    for item in items:
        evidence_id = item["runner_evidence_id"]
        evidence_status = item["evidence_status"]
        if evidence_status == "PASS_PUBLISHED":
            return False
        if evidence_id in identifiers:
            return False
        identifiers.append(evidence_id)
    return True


def _p2d44_success_valid(value: dict[str, object]) -> bool:
    source = value["source"]
    result = value["local_noop_runner_result"]
    if not _exact_keys(source, _P2D44_SOURCE_KEYS) or not _exact_keys(result, _P2D44_RESULT_KEYS):
        return False
    if (
        not _fixed_string(
            value["reason_code"],
            "LOCAL_NOOP_FINAL_RUNNER_RESULT_OBJECT_ASSEMBLED",
        )
        or not _fixed_string(value["reason"], _P2D44_SUCCESS_REASON)
        or not _is_empty_tuple(value["assembly_violations"])
        or not _is_empty_tuple(value["missing_or_invalid_fields"])
        or not _is_empty_tuple(value["result_validation_violations"])
        or not _same_string_tuples(
            value["invariant_refs"], _P2D44_INVARIANT_REFS
        )
    ):
        return False
    expected_source = (
        source["p2d43_decision_created"] is True
        and _fixed_string(
            source["p2d43_reason_code"],
            "LOCAL_NOOP_TERMINAL_RESULT_ASSEMBLY_DECISION_CREATED",
        )
        and source["p2d42_consumed"] is True
        and _fixed_string(
            source["p2d42_reason_code"],
            "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_CONSUMED_IN_MEMORY",
        )
        and source["p2d33_buildable"] is True
        and _fixed_string(
            source["p2d33_reason_code"],
            "LOCAL_NOOP_E2E_CONTRACT_BUILDABLE",
        )
        and source["p2d35_buildable"] is True
        and _fixed_string(
            source["p2d35_reason_code"],
            "LOCAL_NOOP_RUNNER_RESULT_BUILDABLE",
        )
        and _is_nonblank_string(source["run_id"])
        and _is_nonblank_string(source["local_noop_runner_result_id"])
        and _is_nonblank_string(source["local_noop_runner_result_candidate_id"])
        and _is_nonblank_string(source["local_noop_e2e_contract_ref"])
        and _fixed_string(source["mode"], "noop")
        and _fixed_string(
            source["runner_terminal_status"], "NOOP_COMPLETED"
        )
        and source["public_url"] is None
        and source["public_url_created"] is False
        and _is_string_tuple(source["source_of_truth"], nonempty=True)
    )
    expected_result = (
        _is_nonblank_string(result["run_id"])
        and _is_nonblank_string(result["local_noop_runner_result_id"])
        and _fixed_string(result["result_kind"], "local_noop_runner_result")
        and _fixed_string(result["mode"], "noop")
        and _fixed_string(result["runner_terminal_status"], "NOOP_COMPLETED")
        and _is_nonblank_string(result["local_noop_e2e_contract_ref"])
        and result["local_noop_e2e_contract_buildable_marker"] is True
        and result["public_url"] is None
        and result["public_url_created"] is False
        and _p2d44_evidence_valid(result["runner_evidence_items"])
        and _is_string_tuple(result["required_runner_evidence_ids"], nonempty=True)
        and _is_empty_tuple(result["missing_runner_evidence_ids"])
        and _is_string_tuple(result["blocking_runner_evidence_ids"])
        and _is_nonblank_string(result["created_at"])
        and _is_nonblank_string(result["timestamp_policy"])
        and _is_string_tuple(result["source_of_truth"], nonempty=True)
        and _is_string_tuple(result["notes"])
    )
    if not expected_source or not expected_result:
        return False
    evidence_ids = tuple(item["runner_evidence_id"] for item in result["runner_evidence_items"])
    if not _same_string_tuples(result["required_runner_evidence_ids"], evidence_ids):
        return False
    if any(item not in evidence_ids for item in result["blocking_runner_evidence_ids"]):
        return False
    final_result_id = result["local_noop_runner_result_id"]
    candidate_id = source["local_noop_runner_result_candidate_id"]
    e2e_contract_id = source["local_noop_e2e_contract_ref"]
    if final_result_id == candidate_id or final_result_id == e2e_contract_id:
        return False
    coherence_pairs = (
        (source["run_id"], result["run_id"]),
        (source["local_noop_runner_result_id"], result["local_noop_runner_result_id"]),
        (source["local_noop_e2e_contract_ref"], result["local_noop_e2e_contract_ref"]),
        (source["mode"], result["mode"]),
        (source["runner_terminal_status"], result["runner_terminal_status"]),
        (source["public_url"], result["public_url"]),
        (source["public_url_created"], result["public_url_created"]),
        (source["source_of_truth"], result["source_of_truth"]),
    )
    return all(_same(left, right) for left, right in coherence_pairs)


def _p2d44_blocked_valid(value: dict[str, object]) -> bool:
    source = value["source"]
    if not _exact_keys(source, _P2D44_SOURCE_KEYS):
        return False
    return (
        source["p2d43_decision_created"] is False
        and _fixed_string(source["p2d43_reason_code"], "")
        and source["p2d42_consumed"] is False
        and _fixed_string(source["p2d42_reason_code"], "")
        and source["p2d33_buildable"] is False
        and _fixed_string(source["p2d33_reason_code"], "")
        and source["p2d35_buildable"] is False
        and _fixed_string(source["p2d35_reason_code"], "")
        and _fixed_string(source["run_id"], "")
        and _fixed_string(source["local_noop_runner_result_id"], "")
        and _fixed_string(
            source["local_noop_runner_result_candidate_id"], ""
        )
        and _fixed_string(source["local_noop_e2e_contract_ref"], "")
        and _fixed_string(source["mode"], "")
        and _fixed_string(source["runner_terminal_status"], "")
        and source["public_url"] is None
        and source["public_url_created"] is False
        and _is_empty_tuple(source["source_of_truth"])
        and type(value["local_noop_runner_result"]) is dict
        and len(value["local_noop_runner_result"]) == 0
        and _same_string_tuples(
            value["invariant_refs"], _P2D44_INVARIANT_REFS
        )
        and _p2d44_blocked_diagnostics_valid(value)
    )


def _classify_p2d44(value: object) -> tuple[str, bool, dict[str, object]]:
    forbidden = _shape_has_forbidden_key(value, _P2D44_ROOT_KEYS)
    if not _exact_keys(value, _P2D44_ROOT_KEYS):
        return INVALID, forbidden, {}
    marker = value["final_result_object_assembled"]
    if type(marker) is not bool:
        return INVALID, forbidden, {}
    source = value["source"]
    nested = value["local_noop_runner_result"]
    forbidden = forbidden or _shape_has_forbidden_key(source, _P2D44_SOURCE_KEYS)
    if marker is True:
        forbidden = forbidden or _shape_has_forbidden_key(nested, _P2D44_RESULT_KEYS)
        if _exact_keys(nested, _P2D44_RESULT_KEYS):
            items = nested["runner_evidence_items"]
            if type(items) is tuple:
                for item in items:
                    forbidden = forbidden or _shape_has_forbidden_key(item, _P2D44_EVIDENCE_KEYS)
        if _p2d44_success_valid(value):
            return VALID_SUCCESS, forbidden, value
        return INVALID, forbidden, {}
    if _p2d44_blocked_valid(value):
        return VALID_BLOCKED, forbidden, {}
    if type(value["result_validation_violations"]) is tuple:
        for record in value["result_validation_violations"]:
            forbidden = forbidden or _shape_has_forbidden_key(record, _P2D44_DIAGNOSTIC_RECORD_KEYS)
    return INVALID, forbidden, {}


def _p2d45v_evidence_valid(items: object, provenance: dict[str, object]) -> bool:
    if type(items) is not tuple or len(items) != 5:
        return False
    for item in items:
        if not _exact_keys(item, _P2D45V_EVIDENCE_KEYS):
            return False
    for index, item in enumerate(items):
        field = _COMPONENT_VERSION_FIELDS[index]
        version_field = item["version_field"]
        resolved_version = item["resolved_version"]
        resolution_status = item["resolution_status"]
        if (
            not _fixed_string(version_field, field)
            or not _is_valid_version(resolved_version)
            or not _fixed_string(resolution_status, "resolved")
            or not _is_nonblank_string(item["resolver_ref"])
            or not _is_nonblank_string(item["evidence_ref"])
        ):
            return False
    for index, item in enumerate(items):
        field = _COMPONENT_VERSION_FIELDS[index]
        resolved_version = item["resolved_version"]
        direct_version = provenance[field]
        if not _is_valid_version(direct_version):
            return False
        if resolved_version != direct_version:
            return False
    return True


def _p2d45v_success_valid(value: dict[str, object]) -> bool:
    source = value["source"]
    provenance = value["run_version_provenance"]
    if not _exact_keys(source, _P2D45V_SOURCE_KEYS) or not _exact_keys(provenance, _P2D45V_PROVENANCE_KEYS):
        return False
    if (
        not _fixed_string(
            value["reason_code"],
            "RUN_VERSION_PROVENANCE_ASSEMBLED_IN_MEMORY",
        )
        or not _fixed_string(
            value["reason"],
            _p2d45v_reason("RUN_VERSION_PROVENANCE_ASSEMBLED_IN_MEMORY"),
        )
        or not _is_empty_tuple(value["assembly_violations"])
        or not _is_empty_tuple(value["missing_or_invalid_fields"])
        or not _is_empty_tuple(value["coherence_violations"])
        or not _same_string_tuples(
            value["invariant_refs"], _P2D45V_INVARIANT_REFS
        )
    ):
        return False
    source_valid = (
        _fixed_string(
            source["assembly_scope"],
            "run_version_provenance_in_memory_only",
        )
        and _fixed_string(source["schema_version"], _P2D45V_SCHEMA_VERSION)
        and _is_nonblank_string(source["run_version_provenance_id"])
        and _is_nonblank_string(source["run_id"])
        and _fixed_int(source["component_version_count"], 5)
        and _is_nonblank_string(source["resolved_at"])
        and _is_nonblank_string(source["resolution_policy"])
        and _is_string_tuple(source["source_of_truth"], nonempty=True)
    )
    provenance_valid = (
        _fixed_string(
            provenance["schema_version"], _P2D45V_SCHEMA_VERSION
        )
        and _is_nonblank_string(provenance["run_version_provenance_id"])
        and _is_nonblank_string(provenance["run_id"])
        and all(
            _is_valid_version(provenance[field])
            for field in _COMPONENT_VERSION_FIELDS
        )
        and _p2d45v_evidence_valid(provenance["resolved_component_version_evidence_items"], provenance)
        and _is_nonblank_string(provenance["resolved_at"])
        and _is_nonblank_string(provenance["resolution_policy"])
        and _is_string_tuple(provenance["source_of_truth"], nonempty=True)
    )
    if not source_valid or not provenance_valid:
        return False
    if provenance["run_version_provenance_id"] == provenance["run_id"]:
        return False
    pairs = (
        (source["schema_version"], provenance["schema_version"]),
        (source["run_version_provenance_id"], provenance["run_version_provenance_id"]),
        (source["run_id"], provenance["run_id"]),
        (source["resolved_at"], provenance["resolved_at"]),
        (source["resolution_policy"], provenance["resolution_policy"]),
        (source["source_of_truth"], provenance["source_of_truth"]),
    )
    return all(_same(left, right) for left, right in pairs)


def _p2d45v_blocked_valid(value: dict[str, object]) -> bool:
    source = value["source"]
    return (
        _exact_keys(source, ("assembly_scope", "schema_version", "component_version_count"))
        and _fixed_string(
            source["assembly_scope"],
            "run_version_provenance_in_memory_only",
        )
        and _fixed_string(source["schema_version"], _P2D45V_SCHEMA_VERSION)
        and _fixed_int(source["component_version_count"], 0)
        and type(value["run_version_provenance"]) is dict
        and len(value["run_version_provenance"]) == 0
        and _same_string_tuples(
            value["invariant_refs"], _P2D45V_INVARIANT_REFS
        )
        and _p2d45v_blocked_diagnostics_valid(value)
    )


def _classify_p2d45v(value: object) -> tuple[str, bool, dict[str, object]]:
    forbidden = _shape_has_forbidden_key(value, _P2D45V_ROOT_KEYS)
    if not _exact_keys(value, _P2D45V_ROOT_KEYS):
        return INVALID, forbidden, {}
    marker = value["version_provenance_assembled"]
    if type(marker) is not bool:
        return INVALID, forbidden, {}
    source = value["source"]
    nested = value["run_version_provenance"]
    expected_source = _P2D45V_SOURCE_KEYS if marker else (
        "assembly_scope", "schema_version", "component_version_count",
    )
    forbidden = forbidden or _shape_has_forbidden_key(source, expected_source)
    if marker is True:
        forbidden = forbidden or _shape_has_forbidden_key(nested, _P2D45V_PROVENANCE_KEYS)
        if _exact_keys(nested, _P2D45V_PROVENANCE_KEYS):
            items = nested["resolved_component_version_evidence_items"]
            if type(items) is tuple:
                for item in items:
                    forbidden = forbidden or _shape_has_forbidden_key(item, _P2D45V_EVIDENCE_KEYS)
        if _p2d45v_success_valid(value):
            return VALID_SUCCESS, forbidden, value
        return INVALID, forbidden, {}
    if _p2d45v_blocked_valid(value):
        return VALID_BLOCKED, forbidden, {}
    if type(value["coherence_violations"]) is tuple:
        for record in value["coherence_violations"]:
            forbidden = forbidden or _shape_has_forbidden_key(record, _P2D45V_COHERENCE_RECORD_KEYS)
    return INVALID, forbidden, {}


def _add(codes: list[str], code: str) -> None:
    if code not in codes:
        codes.append(code)


def _blocked_source() -> dict[str, object]:
    return {
        "assembly_scope": ASSEMBLY_SCOPE,
        "schema_version": SCHEMA_VERSION,
        "component_version_count": 0,
    }


def _blocked_result(codes: list[str]) -> dict[str, object]:
    violations = _ordered(codes)
    reason_code = violations[0]
    fields = []
    records = []
    for code in violations:
        for field in _paths(code):
            if field not in fields:
                fields.append(field)
            records.append({"reason_code": code, "field": field})
    return {
        "run_ledger_entry_assembled": False,
        "reason_code": reason_code,
        "reason": _reason_text(reason_code),
        "source": _blocked_source(),
        "run_ledger_entry": {},
        "assembly_violations": tuple(code for code in violations),
        "missing_or_invalid_fields": tuple(field for field in fields),
        "coherence_violations": tuple(dict(record) for record in records),
        "invariant_refs": tuple(item for item in INVARIANT_REFS),
    }


def _project_runner_evidence(items: tuple[dict[str, object], ...]) -> tuple[dict[str, object], ...]:
    projected = []
    for item in items:
        projected.append({
            "runner_evidence_id": item["runner_evidence_id"],
            "runner_evidence_role": item["runner_evidence_role"],
            "artifact_ref": item["artifact_ref"],
            "artifact_kind": item["artifact_kind"],
            "evidence_status": item["evidence_status"],
            "producer_ref": item["producer_ref"],
            "evidence_refs": _fresh_tuple(item["evidence_refs"]),
        })
    return tuple(item for item in projected)


def _project_version_evidence(items: tuple[dict[str, object], ...]) -> tuple[dict[str, object], ...]:
    projected = []
    for item in items:
        projected.append({
            "version_field": item["version_field"],
            "resolved_version": item["resolved_version"],
            "resolution_status": item["resolution_status"],
            "resolver_ref": item["resolver_ref"],
            "evidence_ref": item["evidence_ref"],
        })
    return tuple(item for item in projected)


def assemble_run_ledger_entry(
    *,
    local_noop_final_runner_result_assembly: dict[str, object],
    run_version_provenance_assembly: dict[str, object],
    run_ledger_entry_id: str,
) -> dict[str, object]:
    """Assemble a validated, caller-safe run-ledger entry candidate."""

    codes = []
    p2d44_status, p2d44_forbidden, p2d44 = _classify_p2d44(
        local_noop_final_runner_result_assembly
    )
    p2d45v_status, p2d45v_forbidden, p2d45v = _classify_p2d45v(
        run_version_provenance_assembly
    )
    if p2d44_forbidden or p2d45v_forbidden:
        _add(codes, "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT")
    if type(run_ledger_entry_id) is not str or run_ledger_entry_id.strip() == "":
        _add(codes, "RUN_LEDGER_ENTRY_ID_INVALID")
    if p2d44_status == INVALID:
        _add(codes, "P2D44_FINAL_RUNNER_RESULT_INVALID")
    elif p2d44_status == VALID_BLOCKED:
        _add(codes, "P2D44_FINAL_RUNNER_RESULT_NOT_ASSEMBLED")
    if p2d45v_status == INVALID:
        _add(codes, "P2D45V_PROVENANCE_RESULT_INVALID")
    elif p2d45v_status == VALID_BLOCKED:
        _add(codes, "P2D45V_PROVENANCE_NOT_ASSEMBLED")

    if p2d44_status == VALID_SUCCESS and p2d45v_status == VALID_SUCCESS:
        runner = p2d44["local_noop_runner_result"]
        runner_source = p2d44["source"]
        provenance = p2d45v["run_version_provenance"]
        provenance_source = p2d45v["source"]
        if provenance["schema_version"] != _P2D45V_SCHEMA_VERSION:
            _add(codes, "P2D45V_SCHEMA_VERSION_INCOMPATIBLE")
        semantic_values = (
            runner["runner_terminal_status"],
            *(item["evidence_status"] for item in runner["runner_evidence_items"]),
            *(item["resolution_status"] for item in provenance["resolved_component_version_evidence_items"]),
        )
        if "PASS_PUBLISHED" in semantic_values:
            _add(codes, "PASS_PUBLISHED_FORBIDDEN")
        if runner["mode"] != "noop":
            _add(codes, "MODE_NOT_NOOP")
        if runner["runner_terminal_status"] != "NOOP_COMPLETED":
            _add(codes, "LEDGER_TERMINAL_STATUS_NOT_NOOP_COMPLETED")
        if runner["public_url"] is not None:
            _add(codes, "PUBLIC_URL_NON_NULL")
        if runner["public_url_created"] is not False:
            _add(codes, "PUBLIC_URL_CREATED_NOT_FALSE")
        if not _same(runner["run_id"], provenance["run_id"]):
            _add(codes, "RUN_ID_MISMATCH")
        p2d44_pairs = (
            (runner_source["run_id"], runner["run_id"]),
            (runner_source["local_noop_runner_result_id"], runner["local_noop_runner_result_id"]),
            (runner_source["local_noop_e2e_contract_ref"], runner["local_noop_e2e_contract_ref"]),
            (runner_source["mode"], runner["mode"]),
            (runner_source["runner_terminal_status"], runner["runner_terminal_status"]),
            (runner_source["public_url"], runner["public_url"]),
            (runner_source["public_url_created"], runner["public_url_created"]),
            (runner_source["source_of_truth"], runner["source_of_truth"]),
        )
        if not all(_same(left, right) for left, right in p2d44_pairs):
            _add(codes, "P2D44_SOURCE_COHERENCE_MISMATCH")
        p2d45v_pairs = (
            (provenance_source["schema_version"], provenance["schema_version"]),
            (provenance_source["run_version_provenance_id"], provenance["run_version_provenance_id"]),
            (provenance_source["run_id"], provenance["run_id"]),
            (provenance_source["resolved_at"], provenance["resolved_at"]),
            (provenance_source["resolution_policy"], provenance["resolution_policy"]),
            (provenance_source["source_of_truth"], provenance["source_of_truth"]),
        )
        if provenance_source["component_version_count"] != 5 or not all(
            _same(left, right) for left, right in p2d45v_pairs
        ):
            _add(codes, "P2D45V_PROVENANCE_COHERENCE_MISMATCH")
        if not _p2d44_evidence_valid(runner["runner_evidence_items"]):
            _add(codes, "RUNNER_EVIDENCE_PROJECTION_INVALID")
        if not _p2d45v_evidence_valid(
            provenance["resolved_component_version_evidence_items"], provenance
        ):
            _add(codes, "VERSION_EVIDENCE_PROJECTION_INVALID")

    if codes:
        return _blocked_result(codes)

    runner = p2d44["local_noop_runner_result"]
    provenance = p2d45v["run_version_provenance"]
    combined_source_of_truth = _fresh_tuple(runner["source_of_truth"]) + _fresh_tuple(
        provenance["source_of_truth"]
    )
    projected_runner_evidence = _project_runner_evidence(runner["runner_evidence_items"])
    projected_version_evidence = _project_version_evidence(
        provenance["resolved_component_version_evidence_items"]
    )
    entry = {
        "schema_version": SCHEMA_VERSION,
        "run_ledger_entry_id": run_ledger_entry_id,
        "run_id": runner["run_id"],
        "entry_kind": ENTRY_KIND,
        "mode": runner["mode"],
        "ledger_terminal_status": runner["runner_terminal_status"],
        "local_noop_runner_result_id": runner["local_noop_runner_result_id"],
        "local_noop_e2e_contract_ref": runner["local_noop_e2e_contract_ref"],
        "public_url": runner["public_url"],
        "public_url_created": runner["public_url_created"],
        "runner_evidence_items": projected_runner_evidence,
        "required_runner_evidence_ids": _fresh_tuple(runner["required_runner_evidence_ids"]),
        "missing_runner_evidence_ids": (),
        "blocking_runner_evidence_ids": _fresh_tuple(runner["blocking_runner_evidence_ids"]),
        "runner_result_created_at": runner["created_at"],
        "runner_result_timestamp_policy": runner["timestamp_policy"],
        "run_version_provenance_id": provenance["run_version_provenance_id"],
        "run_version_provenance_schema_version": provenance["schema_version"],
        "skill_version": provenance["skill_version"],
        "rubric_version": provenance["rubric_version"],
        "generator_version": provenance["generator_version"],
        "renderer_version": provenance["renderer_version"],
        "publisher_version": provenance["publisher_version"],
        "resolved_component_version_evidence_items": projected_version_evidence,
        "version_provenance_resolved_at": provenance["resolved_at"],
        "version_provenance_resolution_policy": provenance["resolution_policy"],
        "source_of_truth": combined_source_of_truth,
    }
    return {
        "run_ledger_entry_assembled": True,
        "reason_code": "RUN_LEDGER_ENTRY_ASSEMBLED_IN_MEMORY",
        "reason": _reason_text("RUN_LEDGER_ENTRY_ASSEMBLED_IN_MEMORY"),
        "source": {
            "assembly_scope": ASSEMBLY_SCOPE,
            "schema_version": SCHEMA_VERSION,
            "run_ledger_entry_id": run_ledger_entry_id,
            "run_id": runner["run_id"],
            "local_noop_runner_result_id": runner["local_noop_runner_result_id"],
            "run_version_provenance_id": provenance["run_version_provenance_id"],
            "run_version_provenance_schema_version": provenance["schema_version"],
            "mode": runner["mode"],
            "ledger_terminal_status": runner["runner_terminal_status"],
            "public_url": runner["public_url"],
            "public_url_created": runner["public_url_created"],
            "component_version_count": 5,
            "source_of_truth": _fresh_tuple(combined_source_of_truth),
        },
        "run_ledger_entry": entry,
        "assembly_violations": (),
        "missing_or_invalid_fields": (),
        "coherence_violations": (),
        "invariant_refs": tuple(item for item in INVARIANT_REFS),
    }


def is_run_ledger_entry_assembled(
    *,
    local_noop_final_runner_result_assembly: dict[str, object],
    run_version_provenance_assembly: dict[str, object],
    run_ledger_entry_id: str,
) -> bool:
    """Return the exact built-in assembly marker from one assembler call."""

    return assemble_run_ledger_entry(
        local_noop_final_runner_result_assembly=local_noop_final_runner_result_assembly,
        run_version_provenance_assembly=run_version_provenance_assembly,
        run_ledger_entry_id=run_ledger_entry_id,
    )["run_ledger_entry_assembled"]
