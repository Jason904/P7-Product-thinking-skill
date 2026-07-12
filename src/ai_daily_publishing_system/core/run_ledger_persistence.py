"""Frozen skeleton for deterministic run-ledger persistence."""

import os
from errno import EEXIST, ELOOP, ENOENT, ENOTDIR
from hashlib import sha256
from re import fullmatch
from stat import S_IMODE, S_ISDIR, S_ISREG
from typing import Final, Optional


SCHEMA_VERSION: Final[str] = "p2d45.run_ledger_persistence.v1"
BOUNDARY_SCOPE: Final[str] = "run_ledger_persistence_boundary"
ARTIFACT_NAME: Final[str] = "run-ledger.yaml"
SERIALIZATION_FORMAT: Final[str] = "canonical_json_yaml_1_2_subset"
CONTENT_DIGEST_ALGORITHM: Final[str] = "sha256"

ARTIFACT_STATUSES: Final[tuple[str, ...]] = (
    "BUILT",
    "NOT_ELIGIBLE",
    "INVALID",
    "SERIALIZATION_FAILED",
)
PERSISTENCE_STATUSES: Final[tuple[str, ...]] = (
    "WRITTEN",
    "ALREADY_IDENTICAL",
    "NOT_ELIGIBLE",
    "INVALID",
    "AUTHORIZATION_FAILED",
    "SERIALIZATION_FAILED",
    "CONFLICT",
    "IO_FAILED",
    "DURABILITY_UNCONFIRMED",
    "PERSISTED_CLEANUP_WARNING",
)
WRITE_DISPOSITIONS: Final[tuple[str, ...]] = (
    "WRITTEN",
    "ALREADY_IDENTICAL",
    "DURABILITY_UNCONFIRMED",
)

REASON_CODES: Final[tuple[str, ...]] = (
    "P2D45A_SUCCESS_ENVELOPE_INVALID",
    "P2D45A_ENVELOPE_NOT_ELIGIBLE",
    "RUN_LEDGER_SERIALIZATION_FAILED",
    "DESTINATION_ROOT_INVALID",
    "DESTINATION_PATH_UNSAFE",
    "FILESYSTEM_CAPABILITY_UNAVAILABLE",
    "EXISTING_TARGET_INSPECTION_FAILED",
    "RUN_LEDGER_CONFLICT",
    "PRE_FINALIZATION_IO_FAILED",
    "TEMP_NAME_GENERATION_FAILED",
    "TEMP_FILE_CREATE_FAILED",
    "TEMP_INODE_VALIDATION_FAILED",
    "TEMP_FILE_WRITE_FAILED",
    "TEMP_FILE_FSYNC_FAILED",
    "ATOMIC_CREATE_FAILED",
    "FINAL_IDENTITY_VERIFICATION_FAILED",
    "FINAL_DURABILITY_UNCONFIRMED",
    "FINAL_INSPECTION_CLOSE_FAILED",
    "TEMP_FILE_CLOSE_FAILED",
    "TEMP_CLEANUP_FAILED",
    "PERSISTED_CLEANUP_WARNING",
    "RUN_LEDGER_PERSISTENCE_ARTIFACT_BUILT",
    "RUN_LEDGER_ALREADY_PERSISTED_IDENTICAL",
    "RUN_LEDGER_PERSISTED",
)
REASON_PRIORITY: Final[tuple[str, ...]] = REASON_CODES
REASON_STRINGS: Final[tuple[tuple[str, str], ...]] = (
    (
        "P2D45A_SUCCESS_ENVELOPE_INVALID",
        "The complete P2D-45A success envelope is invalid.",
    ),
    (
        "P2D45A_ENVELOPE_NOT_ELIGIBLE",
        "The P2D-45A envelope is not eligible for persistence.",
    ),
    (
        "RUN_LEDGER_SERIALIZATION_FAILED",
        "The validated run-ledger entry could not be serialized under the canonical JSON YAML-subset contract.",
    ),
    (
        "DESTINATION_ROOT_INVALID",
        "The authorized Ops root does not satisfy the fixed local destination contract.",
    ),
    (
        "DESTINATION_PATH_UNSAFE",
        "The internally generated destination cannot be traversed safely.",
    ),
    (
        "FILESYSTEM_CAPABILITY_UNAVAILABLE",
        "A required local POSIX filesystem capability is unavailable.",
    ),
    (
        "EXISTING_TARGET_INSPECTION_FAILED",
        "The existing deterministic target could not be inspected safely.",
    ),
    (
        "RUN_LEDGER_CONFLICT",
        "The deterministic target already contains different bytes.",
    ),
    (
        "PRE_FINALIZATION_IO_FAILED",
        "A filesystem operation failed before atomic finalization; operating-system details are suppressed.",
    ),
    (
        "TEMP_NAME_GENERATION_FAILED",
        "A valid private temporary-file name could not be generated.",
    ),
    (
        "TEMP_FILE_CREATE_FAILED",
        "The same-directory temporary file could not be created.",
    ),
    (
        "TEMP_INODE_VALIDATION_FAILED",
        "The temporary descriptor did not retain the required regular-file identity, mode, and size contract.",
    ),
    (
        "TEMP_FILE_WRITE_FAILED",
        "The complete serialized content could not be written to the temporary file.",
    ),
    (
        "TEMP_FILE_FSYNC_FAILED",
        "Temporary-file durability could not be established before finalization.",
    ),
    (
        "ATOMIC_CREATE_FAILED",
        "The create-only atomic finalization operation failed.",
    ),
    (
        "FINAL_IDENTITY_VERIFICATION_FAILED",
        "The final name may exist, but continuity with the fsynced temporary inode could not be verified.",
    ),
    (
        "FINAL_DURABILITY_UNCONFIRMED",
        "The final path may contain the expected bytes, but durable persistence is unconfirmed.",
    ),
    (
        "FINAL_INSPECTION_CLOSE_FAILED",
        "A final-inspection descriptor could not be closed before durable persistence was established.",
    ),
    (
        "TEMP_FILE_CLOSE_FAILED",
        "The temporary-file descriptor could not be closed before durable persistence was established.",
    ),
    (
        "TEMP_CLEANUP_FAILED",
        "Temporary-file cleanup failed before final durability was established; an orphan may remain.",
    ),
    (
        "PERSISTED_CLEANUP_WARNING",
        "The expected final artifact is durable, but post-persistence descriptor or temporary-file cleanup is incomplete or unconfirmed; an orphan may remain.",
    ),
    (
        "RUN_LEDGER_PERSISTENCE_ARTIFACT_BUILT",
        "A deterministic run-ledger persistence artifact was built in memory.",
    ),
    (
        "RUN_LEDGER_ALREADY_PERSISTED_IDENTICAL",
        "The identical run-ledger artifact was already durably present.",
    ),
    (
        "RUN_LEDGER_PERSISTED",
        "The run-ledger artifact was durably written.",
    ),
)
DIAGNOSTIC_PATHS: Final[tuple[tuple[str, tuple[str, ...]], ...]] = (
    ("P2D45A_SUCCESS_ENVELOPE_INVALID", ("run_ledger_entry_assembly",)),
    ("P2D45A_ENVELOPE_NOT_ELIGIBLE", ("run_ledger_entry_assembly",)),
    ("RUN_LEDGER_SERIALIZATION_FAILED", ("run_ledger_entry",)),
    ("DESTINATION_ROOT_INVALID", ("authorized_ops_root",)),
    ("DESTINATION_PATH_UNSAFE", ("authorized_destination",)),
    ("FILESYSTEM_CAPABILITY_UNAVAILABLE", ("filesystem_capability",)),
    ("EXISTING_TARGET_INSPECTION_FAILED", ("persistence_io",)),
    ("RUN_LEDGER_CONFLICT", ("artifact_relative_path",)),
    ("PRE_FINALIZATION_IO_FAILED", ("persistence_io",)),
    ("TEMP_NAME_GENERATION_FAILED", ("persistence_io",)),
    ("TEMP_FILE_CREATE_FAILED", ("persistence_io",)),
    ("TEMP_INODE_VALIDATION_FAILED", ("persistence_io",)),
    ("TEMP_FILE_WRITE_FAILED", ("persistence_io",)),
    ("TEMP_FILE_FSYNC_FAILED", ("persistence_io",)),
    ("ATOMIC_CREATE_FAILED", ("persistence_io",)),
    ("FINAL_IDENTITY_VERIFICATION_FAILED", ("persistence_io",)),
    ("FINAL_DURABILITY_UNCONFIRMED", ("persistence_io",)),
    ("FINAL_INSPECTION_CLOSE_FAILED", ("persistence_io",)),
    ("TEMP_FILE_CLOSE_FAILED", ("persistence_io",)),
    ("TEMP_CLEANUP_FAILED", ("persistence_io",)),
    ("PERSISTED_CLEANUP_WARNING", ("persistence_io",)),
    ("RUN_LEDGER_PERSISTENCE_ARTIFACT_BUILT", ()),
    ("RUN_LEDGER_ALREADY_PERSISTED_IDENTICAL", ()),
    ("RUN_LEDGER_PERSISTED", ()),
)

INVARIANT_REFS: Final[tuple[str, ...]] = (
    "P2D45_P_COMPLETE_ENVELOPE_TRUST_BOUNDARY",
    "P2D45_P_EXACT_SUCCESS_REQUIRED",
    "P2D45_P_NESTED_ENTRY_BYPASS_FORBIDDEN",
    "P2D45_P_CALLER_BYTES_FORBIDDEN",
    "P2D45_P_PURE_ARTIFACT_BUILDER",
    "P2D45_P_EXPLICIT_EFFECT_API",
    "P2D45_P_CANONICAL_JSON_YAML12_SUBSET",
    "P2D45_P_UTF8_ONE_FINAL_LF",
    "P2D45_P_SHA256_EXACT_BYTES",
    "P2D45_P_NO_SEMANTIC_MUTATION",
    "P2D45_P_AUTHORIZED_ROOT_EXPLICIT",
    "P2D45_P_NO_CWD_DESTINATION",
    "P2D45_P_NO_ENV_DESTINATION",
    "P2D45_P_ROOT_COMPONENT_NOFOLLOW",
    "P2D45_P_ROOT_DESCRIPTOR_CAPABILITY",
    "P2D45_P_PREPROVISIONED_LEDGER_PARENTS",
    "P2D45_P_HASHED_ENTRY_DIRECTORY",
    "P2D45_P_RELATIVE_RESULT_PATH_ONLY",
    "P2D45_P_NO_PATH_ESCAPE",
    "P2D45_P_NO_SYMLINK_ESCAPE",
    "P2D45_P_TEMP_NAMESPACE_PRIVATE",
    "P2D45_P_TEMP_COLLISIONS_BOUNDED",
    "P2D45_P_TEMP_NAME_NEVER_EXPOSED",
    "P2D45_P_TEMP_REGULAR_FILE_REQUIRED",
    "P2D45_P_TEMP_DESCRIPTOR_STAYS_OPEN",
    "P2D45_P_TEMP_IDENTITY_STABLE",
    "P2D45_P_COMPLETE_SHORT_WRITE_LOOP",
    "P2D45_P_TEMP_FSYNC_BEFORE_LINK",
    "P2D45_P_CREATE_ONLY_HARD_LINK",
    "P2D45_P_NO_OVERWRITE_FALLBACK",
    "P2D45_P_FINAL_TEMP_INODE_CONTINUITY",
    "P2D45_P_FINAL_SIZE_CONTINUITY",
    "P2D45_P_FINAL_DIRECTORY_FSYNC_REQUIRED",
    "P2D45_P_POST_FSYNC_FINAL_REVALIDATION",
    "P2D45_P_EXISTING_READ_BOUNDED",
    "P2D45_P_EXISTING_IDENTITY_STABLE",
    "P2D45_P_IDENTICAL_BYTES_IDEMPOTENT",
    "P2D45_P_DIFFERENT_BYTES_CONFLICT",
    "P2D45_P_NO_PARTIAL_FINAL_FILE",
    "P2D45_P_DURABILITY_UNCERTAINTY_EXPLICIT",
    "P2D45_P_DURABLE_CLEANUP_WARNING_PRESERVES_TRUTH",
    "P2D45_P_MULTI_VIOLATIONS_DETERMINISTIC",
    "P2D45_P_NO_EXCEPTION_TEXT",
    "P2D45_P_NO_ABSOLUTE_PATH_LEAKAGE",
    "P2D45_P_NO_OS_ERROR_LEAKAGE",
    "P2D45_P_NO_ORPHAN_SCAN_AUTHORITY",
    "P2D45_P_LOCAL_POSIX_ROOT_EXTERNALLY_ATTESTED",
    "P2D45_P_NO_NETWORK_FILESYSTEM_DETECTION_CLAIM",
    "P2D45_P_PERSISTENCE_NOT_RUNTIME",
    "P2D45_P_PERSISTENCE_NOT_TRANSITION",
    "P2D45_P_PERSISTENCE_NOT_QUALITY_PASS",
    "P2D45_P_PERSISTENCE_NOT_PUBLICATION",
    "P2D45_P_NO_PUBLIC_URL",
    "P2D45_P_NOOP_COMPLETED_IS_METADATA_ONLY",
    "P2D45_P_PASS_PUBLISHED_FORBIDDEN",
    "P2D45_P_PERSISTENCE_NOT_NOTIFICATION",
)

ARTIFACT_RESULT_KEYS: Final[tuple[str, ...]] = (
    "persistence_artifact_built",
    "artifact_status",
    "reason_code",
    "reason",
    "source",
    "persistence_artifact",
    "artifact_violations",
    "missing_or_invalid_fields",
    "diagnostic_records",
    "invariant_refs",
)
PERSISTENCE_RESULT_KEYS: Final[tuple[str, ...]] = (
    "run_ledger_persisted",
    "persistence_status",
    "reason_code",
    "reason",
    "source",
    "persistence_evidence",
    "persistence_violations",
    "missing_or_invalid_fields",
    "diagnostic_records",
    "invariant_refs",
)
SOURCE_KEYS: Final[tuple[str, ...]] = (
    "boundary_scope",
    "schema_version",
    "artifact_name",
    "serialization_format",
    "content_digest_algorithm",
)
PERSISTENCE_ARTIFACT_KEYS: Final[tuple[str, ...]] = (
    "run_ledger_entry_id",
    "run_id",
    "artifact_relative_path",
    "serialization_format",
    "serialized_content",
    "content_digest_algorithm",
    "content_digest",
)
PERSISTENCE_EVIDENCE_KEYS: Final[tuple[str, ...]] = (
    "run_ledger_entry_id",
    "run_id",
    "artifact_relative_path",
    "serialization_format",
    "content_digest_algorithm",
    "content_digest",
    "write_disposition",
)
DIAGNOSTIC_RECORD_KEYS: Final[tuple[str, ...]] = (
    "reason_code",
    "field",
)
REQUIRED_CAPABILITIES: Final[tuple[str, ...]] = (
    "os.open",
    "os.read",
    "os.write",
    "os.close",
    "os.fstat",
    "os.fsync",
    "os.mkdir",
    "os.link",
    "os.unlink",
    "directory_file_descriptors",
    "src_dir_fd",
    "dst_dir_fd",
    "O_DIRECTORY",
    "O_NOFOLLOW",
    "O_CREAT | O_EXCL",
    "create_only_hard_link",
    "file_fsync",
    "directory_fsync",
    "st_mtime_ns",
)

_P2D45A_ROOT_KEYS: Final[tuple[str, ...]] = (
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
_P2D45A_SUCCESS_SOURCE_KEYS: Final[tuple[str, ...]] = (
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
_P2D45A_BLOCKED_SOURCE_KEYS: Final[tuple[str, ...]] = (
    "assembly_scope",
    "schema_version",
    "component_version_count",
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
_RUNNER_EVIDENCE_KEYS: Final[tuple[str, ...]] = (
    "runner_evidence_id",
    "runner_evidence_role",
    "artifact_ref",
    "artifact_kind",
    "evidence_status",
    "producer_ref",
    "evidence_refs",
)
_VERSION_FIELDS: Final[tuple[str, ...]] = (
    "skill_version",
    "rubric_version",
    "generator_version",
    "renderer_version",
    "publisher_version",
)
_VERSION_EVIDENCE_KEYS: Final[tuple[str, ...]] = (
    "version_field",
    "resolved_version",
    "resolution_status",
    "resolver_ref",
    "evidence_ref",
)
_P2D45A_INVARIANTS: Final[tuple[str, ...]] = (
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
_P2D45A_FAILURE_DETAILS: Final[
    tuple[tuple[str, str, str], ...]
] = (
    (
        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
        "A forbidden field or namespace was supplied; caller key names and values are suppressed.",
        "p2d45a.forbidden_field_or_namespace",
    ),
    (
        "RUN_LEDGER_ENTRY_ID_INVALID",
        "run_ledger_entry_id must be an exact nonblank string.",
        "run_ledger_entry_id",
    ),
    (
        "P2D44_FINAL_RUNNER_RESULT_INVALID",
        "The complete P2D-44 final runner-result assembly is invalid.",
        "local_noop_final_runner_result_assembly",
    ),
    (
        "P2D45V_PROVENANCE_RESULT_INVALID",
        "The complete P2D-45V run-version provenance assembly is invalid.",
        "run_version_provenance_assembly",
    ),
    (
        "P2D44_FINAL_RUNNER_RESULT_NOT_ASSEMBLED",
        "P2D-44 returned a valid blocked envelope and did not assemble a final runner-result object.",
        "local_noop_final_runner_result_assembly",
    ),
    (
        "P2D45V_PROVENANCE_NOT_ASSEMBLED",
        "P2D-45V returned a valid blocked envelope and did not assemble run-version provenance.",
        "run_version_provenance_assembly",
    ),
    (
        "P2D45V_SCHEMA_VERSION_INCOMPATIBLE",
        "The P2D-45V provenance schema version is incompatible.",
        "run_version_provenance.schema_version",
    ),
    (
        "PASS_PUBLISHED_FORBIDDEN",
        "PASS_PUBLISHED is forbidden at this run-ledger entry boundary.",
        "interpreted_semantic_fields",
    ),
    ("MODE_NOT_NOOP", "The recorded mode must be noop.", "local_noop_runner_result.mode"),
    (
        "LEDGER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
        "The recorded ledger terminal status must be NOOP_COMPLETED.",
        "local_noop_runner_result.runner_terminal_status",
    ),
    ("PUBLIC_URL_NON_NULL", "The recorded public URL must be null.", "local_noop_runner_result.public_url"),
    (
        "PUBLIC_URL_CREATED_NOT_FALSE",
        "The recorded public URL-created marker must be false.",
        "local_noop_runner_result.public_url_created",
    ),
    ("RUN_ID_MISMATCH", "The P2D-44 and P2D-45V run IDs do not match.", "run_id"),
    (
        "P2D44_SOURCE_COHERENCE_MISMATCH",
        "The P2D-44 source and final runner-result object are not coherent.",
        "local_noop_final_runner_result_assembly.source",
    ),
    (
        "P2D45V_PROVENANCE_COHERENCE_MISMATCH",
        "The P2D-45V source and run-version provenance object are not coherent.",
        "run_version_provenance_assembly.source",
    ),
    (
        "RUNNER_EVIDENCE_PROJECTION_INVALID",
        "The validated runner evidence cannot be projected safely.",
        "local_noop_runner_result.runner_evidence_items",
    ),
    (
        "VERSION_EVIDENCE_PROJECTION_INVALID",
        "The validated version evidence cannot be projected safely.",
        "run_version_provenance.resolved_component_version_evidence_items",
    ),
)
_TEMP_NAME_PATTERN: Final[str] = r"\.run-ledger\.tmp-[0-9a-f]{32}"
_VERSION_PATTERN: Final[str] = r"[A-Za-z0-9][A-Za-z0-9._+\-]{0,127}"
_MAX_TEMP_ATTEMPTS: Final[int] = 8
_MAX_READ_SIZE: Final[int] = 65536

_os_open = os.open
_os_read = os.read
_os_write = os.write
_os_close = os.close
_os_fstat = os.fstat
_os_fsync = os.fsync
_os_mkdir = os.mkdir
_os_link = os.link
_os_unlink = os.unlink


def _new_temp_name() -> str:
    import secrets

    return ".run-ledger.tmp-" + secrets.token_hex(16)


def _source() -> dict[str, object]:
    return {
        "boundary_scope": BOUNDARY_SCOPE,
        "schema_version": SCHEMA_VERSION,
        "artifact_name": ARTIFACT_NAME,
        "serialization_format": SERIALIZATION_FORMAT,
        "content_digest_algorithm": CONTENT_DIGEST_ALGORITHM,
    }


def _fresh_tuple(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(value for value in values)


def _exact_keys(value: object, expected: tuple[str, ...]) -> bool:
    if type(value) is not dict:
        return False
    keys = tuple(value.keys())
    for key in keys:
        if type(key) is not str:
            return False
    if len(keys) != len(expected):
        return False
    for index, key in enumerate(keys):
        if key != expected[index]:
            return False
    return True


def _exact_string(value: object, expected: str) -> bool:
    return type(value) is str and value == expected


def _nonblank_string(value: object) -> bool:
    return type(value) is str and value.strip() != ""


def _string_tuple(value: object, *, nonempty: bool = False) -> bool:
    if type(value) is not tuple or (nonempty and len(value) == 0):
        return False
    for item in value:
        if type(item) is not str or (nonempty and item.strip() == ""):
            return False
    return True


def _same_string_tuple(left: object, right: object) -> bool:
    if not _string_tuple(left) or not _string_tuple(right):
        return False
    if len(left) != len(right):
        return False
    for index, item in enumerate(left):
        if item != right[index]:
            return False
    return True


def _empty_tuple(value: object) -> bool:
    return type(value) is tuple and len(value) == 0


def _valid_version(value: object) -> bool:
    return type(value) is str and fullmatch(_VERSION_PATTERN, value) is not None


def _valid_runner_evidence(value: object) -> bool:
    if type(value) is not tuple or len(value) == 0:
        return False
    identifiers = []
    for item in value:
        if not _exact_keys(item, _RUNNER_EVIDENCE_KEYS):
            return False
        for key in _RUNNER_EVIDENCE_KEYS[:6]:
            if not _nonblank_string(item[key]):
                return False
        if not _string_tuple(item["evidence_refs"], nonempty=True):
            return False
        if item["evidence_status"] == "PASS_PUBLISHED":
            return False
        identifier = item["runner_evidence_id"]
        if identifier in identifiers:
            return False
        identifiers.append(identifier)
    return True


def _valid_version_evidence(value: object, entry: dict[str, object]) -> bool:
    if type(value) is not tuple or len(value) != len(_VERSION_FIELDS):
        return False
    for index, item in enumerate(value):
        if not _exact_keys(item, _VERSION_EVIDENCE_KEYS):
            return False
        field = _VERSION_FIELDS[index]
        if (
            not _exact_string(item["version_field"], field)
            or not _valid_version(item["resolved_version"])
            or not _exact_string(item["resolution_status"], "resolved")
            or not _nonblank_string(item["resolver_ref"])
            or not _nonblank_string(item["evidence_ref"])
            or not _valid_version(entry[field])
            or item["resolved_version"] != entry[field]
        ):
            return False
    return True


def _success_envelope_valid(value: object) -> bool:
    if not _exact_keys(value, _P2D45A_ROOT_KEYS):
        return False
    if value["run_ledger_entry_assembled"] is not True:
        return False
    source = value["source"]
    entry = value["run_ledger_entry"]
    if (
        not _exact_keys(source, _P2D45A_SUCCESS_SOURCE_KEYS)
        or not _exact_keys(entry, _ENTRY_KEYS)
        or not _exact_string(value["reason_code"], "RUN_LEDGER_ENTRY_ASSEMBLED_IN_MEMORY")
        or not _exact_string(
            value["reason"],
            "A deterministic run-ledger entry candidate was assembled in memory.",
        )
        or not _empty_tuple(value["assembly_violations"])
        or not _empty_tuple(value["missing_or_invalid_fields"])
        or not _empty_tuple(value["coherence_violations"])
        or not _same_string_tuple(value["invariant_refs"], _P2D45A_INVARIANTS)
    ):
        return False
    if (
        not _exact_string(source["assembly_scope"], "run_ledger_entry_in_memory_only")
        or not _exact_string(source["schema_version"], "p2d45.run_ledger_entry.v1")
        or not _nonblank_string(source["run_ledger_entry_id"])
        or not _nonblank_string(source["run_id"])
        or not _nonblank_string(source["local_noop_runner_result_id"])
        or not _nonblank_string(source["run_version_provenance_id"])
        or not _exact_string(
            source["run_version_provenance_schema_version"],
            "p2d45.run_version_provenance.v1",
        )
        or not _exact_string(source["mode"], "noop")
        or not _exact_string(source["ledger_terminal_status"], "NOOP_COMPLETED")
        or source["public_url"] is not None
        or source["public_url_created"] is not False
        or type(source["component_version_count"]) is not int
        or source["component_version_count"] != 5
        or not _string_tuple(source["source_of_truth"], nonempty=True)
    ):
        return False
    if (
        not _exact_string(entry["schema_version"], "p2d45.run_ledger_entry.v1")
        or not _nonblank_string(entry["run_ledger_entry_id"])
        or not _nonblank_string(entry["run_id"])
        or not _exact_string(entry["entry_kind"], "run_ledger_entry")
        or not _exact_string(entry["mode"], "noop")
        or not _exact_string(entry["ledger_terminal_status"], "NOOP_COMPLETED")
        or not _nonblank_string(entry["local_noop_runner_result_id"])
        or not _nonblank_string(entry["local_noop_e2e_contract_ref"])
        or entry["public_url"] is not None
        or entry["public_url_created"] is not False
        or not _valid_runner_evidence(entry["runner_evidence_items"])
        or not _string_tuple(entry["required_runner_evidence_ids"], nonempty=True)
        or not _empty_tuple(entry["missing_runner_evidence_ids"])
        or not _string_tuple(entry["blocking_runner_evidence_ids"])
        or not _nonblank_string(entry["runner_result_created_at"])
        or not _nonblank_string(entry["runner_result_timestamp_policy"])
        or not _nonblank_string(entry["run_version_provenance_id"])
        or not _exact_string(
            entry["run_version_provenance_schema_version"],
            "p2d45.run_version_provenance.v1",
        )
        or not all(_valid_version(entry[field]) for field in _VERSION_FIELDS)
        or not _valid_version_evidence(
            entry["resolved_component_version_evidence_items"], entry
        )
        or not _nonblank_string(entry["version_provenance_resolved_at"])
        or not _nonblank_string(entry["version_provenance_resolution_policy"])
        or not _string_tuple(entry["source_of_truth"], nonempty=True)
    ):
        return False
    evidence_ids = tuple(
        item["runner_evidence_id"] for item in entry["runner_evidence_items"]
    )
    if not _same_string_tuple(entry["required_runner_evidence_ids"], evidence_ids):
        return False
    for identifier in entry["blocking_runner_evidence_ids"]:
        if identifier not in evidence_ids:
            return False
    pairs = (
        (source["schema_version"], entry["schema_version"]),
        (source["run_ledger_entry_id"], entry["run_ledger_entry_id"]),
        (source["run_id"], entry["run_id"]),
        (source["local_noop_runner_result_id"], entry["local_noop_runner_result_id"]),
        (source["run_version_provenance_id"], entry["run_version_provenance_id"]),
        (
            source["run_version_provenance_schema_version"],
            entry["run_version_provenance_schema_version"],
        ),
        (source["mode"], entry["mode"]),
        (source["ledger_terminal_status"], entry["ledger_terminal_status"]),
        (source["public_url"], entry["public_url"]),
        (source["public_url_created"], entry["public_url_created"]),
    )
    for left, right in pairs:
        if type(left) is not type(right) or left != right:
            return False
    return _same_string_tuple(source["source_of_truth"], entry["source_of_truth"])


def _failure_detail(code: str) -> tuple[str, str]:
    for known_code, reason, field in _P2D45A_FAILURE_DETAILS:
        if known_code == code:
            return reason, field
    return "", ""


def _blocked_envelope_valid(value: object) -> bool:
    if not _exact_keys(value, _P2D45A_ROOT_KEYS):
        return False
    if value["run_ledger_entry_assembled"] is not False:
        return False
    source = value["source"]
    nested = value["run_ledger_entry"]
    if (
        not _exact_keys(source, _P2D45A_BLOCKED_SOURCE_KEYS)
        or type(nested) is not dict
        or len(nested) != 0
        or not _exact_string(source["assembly_scope"], "run_ledger_entry_in_memory_only")
        or not _exact_string(source["schema_version"], "p2d45.run_ledger_entry.v1")
        or type(source["component_version_count"]) is not int
        or source["component_version_count"] != 0
        or not _same_string_tuple(value["invariant_refs"], _P2D45A_INVARIANTS)
    ):
        return False
    violations = value["assembly_violations"]
    fields = value["missing_or_invalid_fields"]
    records = value["coherence_violations"]
    if not _string_tuple(violations, nonempty=True) or not _string_tuple(fields):
        return False
    if type(records) is not tuple or len(records) != len(violations):
        return False
    allowed = tuple(item[0] for item in _P2D45A_FAILURE_DETAILS)
    previous_rank = -1
    expected_fields = []
    for index, code in enumerate(violations):
        if code not in allowed:
            return False
        rank = allowed.index(code)
        if rank <= previous_rank:
            return False
        previous_rank = rank
        reason, field = _failure_detail(code)
        if field not in expected_fields:
            expected_fields.append(field)
        record = records[index]
        if (
            not _exact_keys(record, ("reason_code", "field"))
            or not _exact_string(record["reason_code"], code)
            or not _exact_string(record["field"], field)
        ):
            return False
    first_reason, _first_field = _failure_detail(violations[0])
    return (
        _exact_string(value["reason_code"], violations[0])
        and _exact_string(value["reason"], first_reason)
        and _same_string_tuple(fields, tuple(expected_fields))
    )


def _reason_text(code: str) -> str:
    for known_code, reason in REASON_STRINGS:
        if known_code == code:
            return reason
    return ""


def _diagnostic_path(code: str) -> tuple[str, ...]:
    for known_code, paths in DIAGNOSTIC_PATHS:
        if known_code == code:
            return paths
    return ()


def _ordered_codes(codes: list[str]) -> tuple[str, ...]:
    return tuple(code for code in REASON_PRIORITY if code in codes)


def _diagnostics(codes: tuple[str, ...]) -> tuple[tuple[str, ...], tuple[dict[str, str], ...]]:
    fields = []
    records = []
    for code in codes:
        for field in _diagnostic_path(code):
            if field not in fields:
                fields.append(field)
            records.append({"reason_code": code, "field": field})
    return tuple(field for field in fields), tuple(dict(record) for record in records)


def _artifact_result(*, status: str, reason_code: str, artifact: dict[str, object]) -> dict[str, object]:
    violations = () if status == "BUILT" else (reason_code,)
    fields, records = _diagnostics(violations)
    return {
        "persistence_artifact_built": status == "BUILT",
        "artifact_status": status,
        "reason_code": reason_code,
        "reason": _reason_text(reason_code),
        "source": _source(),
        "persistence_artifact": dict(artifact),
        "artifact_violations": _fresh_tuple(violations),
        "missing_or_invalid_fields": _fresh_tuple(fields),
        "diagnostic_records": tuple(dict(record) for record in records),
        "invariant_refs": _fresh_tuple(INVARIANT_REFS),
    }


def _persistence_result(
    *,
    status: str,
    persisted: bool,
    codes: list[str],
    artifact: dict[str, object],
    disposition: str = "",
) -> dict[str, object]:
    violations = _ordered_codes(codes)
    reason_code = violations[0] if violations else (
        "RUN_LEDGER_PERSISTED"
        if status == "WRITTEN"
        else "RUN_LEDGER_ALREADY_PERSISTED_IDENTICAL"
    )
    fields, records = _diagnostics(violations)
    evidence = {}
    if disposition:
        evidence = {
            "run_ledger_entry_id": artifact["run_ledger_entry_id"],
            "run_id": artifact["run_id"],
            "artifact_relative_path": artifact["artifact_relative_path"],
            "serialization_format": artifact["serialization_format"],
            "content_digest_algorithm": artifact["content_digest_algorithm"],
            "content_digest": artifact["content_digest"],
            "write_disposition": disposition,
        }
    return {
        "run_ledger_persisted": persisted,
        "persistence_status": status,
        "reason_code": reason_code,
        "reason": _reason_text(reason_code),
        "source": _source(),
        "persistence_evidence": dict(evidence),
        "persistence_violations": _fresh_tuple(violations),
        "missing_or_invalid_fields": _fresh_tuple(fields),
        "diagnostic_records": tuple(dict(record) for record in records),
        "invariant_refs": _fresh_tuple(INVARIANT_REFS),
    }


def _project_entry(entry: dict[str, object]) -> dict[str, object]:
    projected = {}
    for key in _ENTRY_KEYS:
        value = entry[key]
        if key == "runner_evidence_items":
            projected[key] = [
                {
                    nested_key: (
                        [item for item in item[nested_key]]
                        if nested_key == "evidence_refs"
                        else item[nested_key]
                    )
                    for nested_key in _RUNNER_EVIDENCE_KEYS
                }
                for item in value
            ]
        elif key == "resolved_component_version_evidence_items":
            projected[key] = [
                {nested_key: item[nested_key] for nested_key in _VERSION_EVIDENCE_KEYS}
                for item in value
            ]
        elif type(value) is tuple:
            projected[key] = [item for item in value]
        else:
            projected[key] = value
    return projected


def build_run_ledger_persistence_artifact(
    *,
    run_ledger_entry_assembly: dict[str, object],
) -> dict[str, object]:
    """Build one canonical, deterministic persistence artifact in memory."""

    if _success_envelope_valid(run_ledger_entry_assembly):
        entry = run_ledger_entry_assembly["run_ledger_entry"]
        projected = _project_entry(entry)
        try:
            import json

            serialized_text = json.dumps(
                projected,
                ensure_ascii=False,
                allow_nan=False,
                sort_keys=False,
                indent=2,
                separators=(",", ": "),
            )
            serialized_content = (serialized_text + "\n").encode("utf-8", "strict")
        except Exception:
            return _artifact_result(
                status="SERIALIZATION_FAILED",
                reason_code="RUN_LEDGER_SERIALIZATION_FAILED",
                artifact={},
            )
        entry_id = entry["run_ledger_entry_id"]
        entry_digest = sha256(entry_id.encode("utf-8", "strict")).hexdigest()
        artifact = {
            "run_ledger_entry_id": entry_id,
            "run_id": entry["run_id"],
            "artifact_relative_path": (
                "runs/by-entry-id/sha256-" + entry_digest + "/" + ARTIFACT_NAME
            ),
            "serialization_format": SERIALIZATION_FORMAT,
            "serialized_content": serialized_content,
            "content_digest_algorithm": CONTENT_DIGEST_ALGORITHM,
            "content_digest": sha256(serialized_content).hexdigest(),
        }
        return _artifact_result(
            status="BUILT",
            reason_code="RUN_LEDGER_PERSISTENCE_ARTIFACT_BUILT",
            artifact=artifact,
        )
    if _blocked_envelope_valid(run_ledger_entry_assembly):
        return _artifact_result(
            status="NOT_ELIGIBLE",
            reason_code="P2D45A_ENVELOPE_NOT_ELIGIBLE",
            artifact={},
        )
    return _artifact_result(
        status="INVALID",
        reason_code="P2D45A_SUCCESS_ENVELOPE_INVALID",
        artifact={},
    )


def _valid_root(value: object) -> bool:
    if type(value) is not str or value == "" or value.strip() == "" or "\x00" in value:
        return False
    if not value.startswith("/") or (value != "/" and value.startswith("//")):
        return False
    if value != "/" and (value.endswith("/") or "//" in value):
        return False
    if os.path.normpath(value) != value:
        return False
    if value == "/":
        return True
    components = value.split("/")[1:]
    return all(component not in ("", ".", "..") for component in components)


def _capabilities_available() -> bool:
    wrappers = (
        _os_open, _os_read, _os_write, _os_close, _os_fstat, _os_fsync,
        _os_mkdir, _os_link, _os_unlink,
    )
    if not all(callable(wrapper) for wrapper in wrappers):
        return False
    for name in ("O_DIRECTORY", "O_NOFOLLOW", "O_CREAT", "O_EXCL"):
        if type(getattr(os, name, None)) is not int:
            return False
    return (
        all(function in os.supports_dir_fd for function in (os.open, os.mkdir, os.link, os.unlink))
        and os.link in os.supports_follow_symlinks
    )


def _directory_flags() -> int:
    return os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW


def _final_flags() -> int:
    return os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK


def _safe_close(fd: int, codes: list[str], code: str) -> bool:
    try:
        _os_close(fd)
    except Exception:
        if code not in codes:
            codes.append(code)
        return False
    return True


def _stat_directory(fd: int) -> bool:
    value = _os_fstat(fd)
    return S_ISDIR(value.st_mode)


def _open_directory_component(
    name: str,
    parent_fd: int,
    *,
    root_component: bool,
) -> tuple[list[str], int]:
    ordinary_code = (
        "DESTINATION_ROOT_INVALID"
        if root_component
        else "DESTINATION_PATH_UNSAFE"
    )
    try:
        descriptor = _os_open(name, _directory_flags(), dir_fd=parent_fd)
    except OSError as error:
        if error.errno == ELOOP:
            return ["DESTINATION_PATH_UNSAFE"], -1
        if error.errno == ENOTDIR:
            try:
                probe = _os_open(
                    name,
                    os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                    dir_fd=parent_fd,
                )
            except OSError as probe_error:
                if probe_error.errno == ELOOP:
                    return ["DESTINATION_PATH_UNSAFE"], -1
                return [ordinary_code], -1
            except Exception:
                return ["PRE_FINALIZATION_IO_FAILED"], -1
            codes = [ordinary_code]
            _safe_close(probe, codes, "PRE_FINALIZATION_IO_FAILED")
            return codes, -1
        if error.errno == ENOENT:
            return [ordinary_code], -1
        return ["PRE_FINALIZATION_IO_FAILED"], -1
    except Exception:
        return ["PRE_FINALIZATION_IO_FAILED"], -1
    try:
        if not _stat_directory(descriptor):
            codes = [ordinary_code]
            _safe_close(descriptor, codes, "PRE_FINALIZATION_IO_FAILED")
            return codes, -1
    except Exception:
        codes = ["PRE_FINALIZATION_IO_FAILED"]
        _safe_close(descriptor, codes, "PRE_FINALIZATION_IO_FAILED")
        return codes, -1
    return [], descriptor


def _close_owned(
    descriptors: list[int],
    *,
    durable: bool,
    codes: Optional[list[str]] = None,
) -> bool:
    failed = False
    while descriptors:
        descriptor = descriptors.pop()
        try:
            _os_close(descriptor)
        except Exception:
            failed = True
    if failed and not durable and codes is not None:
        if "PRE_FINALIZATION_IO_FAILED" not in codes:
            codes.append("PRE_FINALIZATION_IO_FAILED")
    return failed


def _open_authorized_entry_directory(
    root: str,
    entry_directory: str,
) -> tuple[list[str], int, list[int]]:
    owned = []
    try:
        current = _os_open("/", _directory_flags())
        owned.append(current)
        if not _stat_directory(current):
            codes = ["DESTINATION_ROOT_INVALID"]
            _close_owned(owned, durable=False, codes=codes)
            return codes, -1, []
    except Exception:
        codes = ["PRE_FINALIZATION_IO_FAILED"]
        _close_owned(owned, durable=False, codes=codes)
        return codes, -1, []
    for component in root.split("/")[1:]:
        if component == "":
            continue
        codes, next_descriptor = _open_directory_component(
            component, current, root_component=True
        )
        if codes:
            _close_owned(owned, durable=False, codes=codes)
            return codes, -1, []
        current = next_descriptor
        owned.append(current)
    for component in ("runs", "by-entry-id"):
        codes, next_descriptor = _open_directory_component(
            component, current, root_component=False
        )
        if codes:
            _close_owned(owned, durable=False, codes=codes)
            return codes, -1, []
        current = next_descriptor
        owned.append(current)
    parent_fsync_required = False
    try:
        entry_fd = _os_open(entry_directory, _directory_flags(), dir_fd=current)
    except OSError as error:
        if error.errno == ELOOP:
            codes = ["DESTINATION_PATH_UNSAFE"]
            _close_owned(owned, durable=False, codes=codes)
            return codes, -1, []
        if error.errno != ENOENT:
            code = "DESTINATION_PATH_UNSAFE" if error.errno == ENOTDIR else "PRE_FINALIZATION_IO_FAILED"
            codes = [code]
            _close_owned(owned, durable=False, codes=codes)
            return codes, -1, []
        parent_fsync_required = True
        try:
            _os_mkdir(entry_directory, 0o700, dir_fd=current)
        except OSError as create_error:
            if create_error.errno != EEXIST:
                code = "DESTINATION_PATH_UNSAFE" if create_error.errno in (ELOOP, ENOTDIR) else "PRE_FINALIZATION_IO_FAILED"
                codes = [code]
                _close_owned(owned, durable=False, codes=codes)
                return codes, -1, []
        except Exception:
            codes = ["PRE_FINALIZATION_IO_FAILED"]
            _close_owned(owned, durable=False, codes=codes)
            return codes, -1, []
        try:
            entry_fd = _os_open(entry_directory, _directory_flags(), dir_fd=current)
        except OSError as reopen_error:
            code = "DESTINATION_PATH_UNSAFE" if reopen_error.errno in (ELOOP, ENOTDIR) else "PRE_FINALIZATION_IO_FAILED"
            codes = [code]
            _close_owned(owned, durable=False, codes=codes)
            return codes, -1, []
        except Exception:
            codes = ["PRE_FINALIZATION_IO_FAILED"]
            _close_owned(owned, durable=False, codes=codes)
            return codes, -1, []
    except Exception:
        codes = ["PRE_FINALIZATION_IO_FAILED"]
        _close_owned(owned, durable=False, codes=codes)
        return codes, -1, []
    try:
        if not _stat_directory(entry_fd):
            codes = ["DESTINATION_PATH_UNSAFE"]
            _safe_close(entry_fd, codes, "PRE_FINALIZATION_IO_FAILED")
            _close_owned(owned, durable=False, codes=codes)
            return codes, -1, []
    except Exception:
        codes = ["PRE_FINALIZATION_IO_FAILED"]
        _safe_close(entry_fd, codes, "PRE_FINALIZATION_IO_FAILED")
        _close_owned(owned, durable=False, codes=codes)
        return codes, -1, []
    if parent_fsync_required:
        try:
            _os_fsync(current)
        except Exception:
            codes = ["PRE_FINALIZATION_IO_FAILED"]
            _safe_close(entry_fd, codes, "PRE_FINALIZATION_IO_FAILED")
            _close_owned(owned, durable=False, codes=codes)
            return codes, -1, []
    owned.append(entry_fd)
    return [], entry_fd, owned


def _stable_stat(left: object, right: object) -> bool:
    try:
        return (
            S_ISREG(left.st_mode)
            and S_ISREG(right.st_mode)
            and left.st_dev == right.st_dev
            and left.st_ino == right.st_ino
            and left.st_mode == right.st_mode
            and left.st_size == right.st_size
            and left.st_mtime_ns == right.st_mtime_ns
        )
    except Exception:
        return False


def _temp_identity_valid(initial: object, current: object, expected_size: int) -> bool:
    try:
        return (
            S_ISREG(current.st_mode)
            and initial.st_dev == current.st_dev
            and initial.st_ino == current.st_ino
            and initial.st_mode == current.st_mode
            and current.st_size == expected_size
        )
    except Exception:
        return False


def _final_identity_valid(temp: object, final: object, expected_size: int) -> bool:
    try:
        return (
            S_ISREG(final.st_mode)
            and temp.st_dev == final.st_dev
            and temp.st_ino == final.st_ino
            and temp.st_mode == final.st_mode
            and final.st_size == expected_size
        )
    except Exception:
        return False


def _inspect_existing(entry_fd: int, expected: bytes) -> tuple[str, list[int], object]:
    descriptors = []
    try:
        descriptor = _os_open(ARTIFACT_NAME, _final_flags(), dir_fd=entry_fd)
        descriptors.append(descriptor)
    except OSError as error:
        if error.errno == ENOENT:
            return "ABSENT", descriptors, None
        if error.errno in (ELOOP, ENOTDIR):
            return "UNSAFE", descriptors, None
        return "INSPECTION_FAILED", descriptors, None
    except Exception:
        return "INSPECTION_FAILED", descriptors, None
    try:
        first = _os_fstat(descriptor)
    except Exception:
        return "INSPECTION_FAILED", descriptors, None
    try:
        if not S_ISREG(first.st_mode):
            return "UNSAFE", descriptors, None
        expected_length = len(expected)
        if first.st_size != expected_length:
            second = _os_fstat(descriptor)
            return ("CONFLICT" if _stable_stat(first, second) else "INSPECTION_FAILED"), descriptors, first
        retained = bytearray()
        while len(retained) < expected_length:
            request = min(_MAX_READ_SIZE, expected_length - len(retained))
            chunk = _os_read(descriptor, request)
            if type(chunk) is not bytes:
                return "INSPECTION_FAILED", descriptors, first
            if len(chunk) == 0:
                break
            if len(chunk) > request:
                return "INSPECTION_FAILED", descriptors, first
            retained.extend(chunk)
        if len(retained) != expected_length:
            return "INSPECTION_FAILED", descriptors, first
        extra = _os_read(descriptor, 1)
        if type(extra) is not bytes or len(extra) != 0:
            return "INSPECTION_FAILED", descriptors, first
        second = _os_fstat(descriptor)
        if not _stable_stat(first, second):
            return "INSPECTION_FAILED", descriptors, first
        if bytes(retained) != expected:
            return "CONFLICT", descriptors, first
        return "IDENTICAL", descriptors, first
    except Exception:
        return "INSPECTION_FAILED", descriptors, first


def _establish_existing_durability(
    entry_fd: int,
    descriptors: list[int],
    first: object,
) -> str:
    descriptor = descriptors[0]
    try:
        _os_fsync(descriptor)
        after_file_fsync = _os_fstat(descriptor)
        if not _stable_stat(first, after_file_fsync):
            return "INSPECTION_FAILED"
        _os_fsync(entry_fd)
        reopened = _os_open(ARTIFACT_NAME, _final_flags(), dir_fd=entry_fd)
        descriptors.append(reopened)
        after_directory_fsync = _os_fstat(reopened)
        if not _stable_stat(first, after_directory_fsync):
            return "INSPECTION_FAILED"
        _os_fsync(entry_fd)
    except Exception:
        return "DURABILITY_UNCONFIRMED"
    return "DURABLE"


def _close_final_descriptors(descriptors: list[int], codes: list[str]) -> bool:
    failed = False
    for descriptor in reversed(descriptors):
        if not _safe_close(descriptor, codes, "FINAL_INSPECTION_CLOSE_FAILED"):
            failed = True
    descriptors.clear()
    return failed


def _trusted_temp_unlink(
    *,
    entry_fd: int,
    temp_fd: int,
    temp_name: str,
    codes: list[str],
) -> bool:
    verifier_fd = -1
    continuity_proven = False
    try:
        verifier_fd = _os_open(temp_name, _final_flags(), dir_fd=entry_fd)
        trusted_stat = _os_fstat(temp_fd)
        verifier_stat = _os_fstat(verifier_fd)
        continuity_proven = (
            S_ISREG(trusted_stat.st_mode)
            and S_ISREG(verifier_stat.st_mode)
            and trusted_stat.st_dev == verifier_stat.st_dev
            and trusted_stat.st_ino == verifier_stat.st_ino
        )
    except Exception:
        continuity_proven = False
    if verifier_fd >= 0:
        if not _safe_close(verifier_fd, codes, "TEMP_FILE_CLOSE_FAILED"):
            continuity_proven = False
    if not continuity_proven:
        return False
    try:
        _os_unlink(temp_name, dir_fd=entry_fd)
        _os_fsync(entry_fd)
    except Exception:
        return False
    return True


def _cleanup_temp_before_durability(
    *,
    entry_fd: int,
    temp_fd: int,
    temp_name: str,
    codes: list[str],
    retain_name: bool = False,
) -> None:
    if retain_name:
        if "TEMP_CLEANUP_FAILED" not in codes:
            codes.append("TEMP_CLEANUP_FAILED")
    else:
        if not _trusted_temp_unlink(
            entry_fd=entry_fd,
            temp_fd=temp_fd,
            temp_name=temp_name,
            codes=codes,
        ):
            if "TEMP_CLEANUP_FAILED" not in codes:
                codes.append("TEMP_CLEANUP_FAILED")
    _safe_close(temp_fd, codes, "TEMP_FILE_CLOSE_FAILED")


def _cleanup_after_durability(
    *,
    entry_fd: int,
    final_descriptors: list[int],
    temp_fd: int,
    temp_name: str,
    owned: list[int],
) -> bool:
    cleanup_codes = []
    failed = _close_final_descriptors(final_descriptors, cleanup_codes)
    if not _trusted_temp_unlink(
        entry_fd=entry_fd,
        temp_fd=temp_fd,
        temp_name=temp_name,
        codes=cleanup_codes,
    ):
        failed = True
    if not _safe_close(temp_fd, cleanup_codes, "TEMP_FILE_CLOSE_FAILED"):
        failed = True
    if _close_owned(owned, durable=True):
        failed = True
    return failed


def _artifact_status_result(artifact_result: dict[str, object]) -> dict[str, object]:
    status = artifact_result["artifact_status"]
    return _persistence_result(
        status=status,
        persisted=False,
        codes=[artifact_result["reason_code"]],
        artifact={},
    )


def persist_run_ledger_entry(
    *,
    run_ledger_entry_assembly: dict[str, object],
    authorized_ops_root: str,
) -> dict[str, object]:
    """Persist one built artifact through a descriptor-relative POSIX boundary."""

    artifact_result = build_run_ledger_persistence_artifact(
        run_ledger_entry_assembly=run_ledger_entry_assembly
    )
    if artifact_result["artifact_status"] != "BUILT":
        return _artifact_status_result(artifact_result)
    artifact = artifact_result["persistence_artifact"]
    if not _valid_root(authorized_ops_root):
        return _persistence_result(
            status="AUTHORIZATION_FAILED",
            persisted=False,
            codes=["DESTINATION_ROOT_INVALID"],
            artifact=artifact,
        )
    if not _capabilities_available():
        return _persistence_result(
            status="IO_FAILED",
            persisted=False,
            codes=["FILESYSTEM_CAPABILITY_UNAVAILABLE"],
            artifact=artifact,
        )
    entry_directory = artifact["artifact_relative_path"].split("/")[2]
    open_codes, entry_fd, owned = _open_authorized_entry_directory(
        authorized_ops_root, entry_directory
    )
    if open_codes:
        primary = _ordered_codes(open_codes)[0]
        status = "AUTHORIZATION_FAILED" if primary in (
            "DESTINATION_ROOT_INVALID", "DESTINATION_PATH_UNSAFE"
        ) else "IO_FAILED"
        return _persistence_result(
            status=status,
            persisted=False,
            codes=open_codes,
            artifact=artifact,
        )
    expected = artifact["serialized_content"]
    existing_status, existing_fds, existing_stat = _inspect_existing(entry_fd, expected)
    if existing_status == "UNSAFE":
        codes = ["DESTINATION_PATH_UNSAFE"]
        _close_final_descriptors(existing_fds, codes)
        _close_owned(owned, durable=False, codes=codes)
        return _persistence_result(
            status="AUTHORIZATION_FAILED", persisted=False, codes=codes, artifact=artifact
        )
    if existing_status == "INSPECTION_FAILED":
        codes = ["EXISTING_TARGET_INSPECTION_FAILED"]
        _close_final_descriptors(existing_fds, codes)
        _close_owned(owned, durable=False, codes=codes)
        return _persistence_result(
            status="IO_FAILED", persisted=False, codes=codes, artifact=artifact
        )
    if existing_status == "CONFLICT":
        codes = ["RUN_LEDGER_CONFLICT"]
        _close_final_descriptors(existing_fds, codes)
        _close_owned(owned, durable=False, codes=codes)
        return _persistence_result(
            status="CONFLICT", persisted=False, codes=codes, artifact=artifact
        )
    if existing_status == "IDENTICAL":
        durability = _establish_existing_durability(entry_fd, existing_fds, existing_stat)
        if durability != "DURABLE":
            code = (
                "EXISTING_TARGET_INSPECTION_FAILED"
                if durability == "INSPECTION_FAILED"
                else "FINAL_DURABILITY_UNCONFIRMED"
            )
            codes = [code]
            _close_final_descriptors(existing_fds, codes)
            _close_owned(owned, durable=False, codes=codes)
            return _persistence_result(
                status=("IO_FAILED" if durability == "INSPECTION_FAILED" else "DURABILITY_UNCONFIRMED"),
                persisted=False,
                codes=codes,
                artifact=artifact,
                disposition=("" if durability == "INSPECTION_FAILED" else "DURABILITY_UNCONFIRMED"),
            )
        cleanup_failed = _close_final_descriptors(existing_fds, [])
        cleanup_failed = _close_owned(owned, durable=True) or cleanup_failed
        if cleanup_failed:
            return _persistence_result(
                status="PERSISTED_CLEANUP_WARNING",
                persisted=True,
                codes=["PERSISTED_CLEANUP_WARNING"],
                artifact=artifact,
                disposition="ALREADY_IDENTICAL",
            )
        return _persistence_result(
            status="ALREADY_IDENTICAL",
            persisted=True,
            codes=[],
            artifact=artifact,
            disposition="ALREADY_IDENTICAL",
        )

    temp_name = ""
    temp_fd = -1
    for _attempt in range(_MAX_TEMP_ATTEMPTS):
        try:
            candidate = _new_temp_name()
        except Exception:
            codes = ["TEMP_NAME_GENERATION_FAILED"]
            _close_owned(owned, durable=False, codes=codes)
            return _persistence_result(
                status="IO_FAILED",
                persisted=False,
                codes=codes,
                artifact=artifact,
            )
        if type(candidate) is not str or fullmatch(_TEMP_NAME_PATTERN, candidate) is None:
            codes = ["TEMP_NAME_GENERATION_FAILED"]
            _close_owned(owned, durable=False, codes=codes)
            return _persistence_result(
                status="IO_FAILED",
                persisted=False,
                codes=codes,
                artifact=artifact,
            )
        try:
            temp_fd = _os_open(
                candidate,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                0o600,
                dir_fd=entry_fd,
            )
            temp_name = candidate
            break
        except OSError as error:
            if error.errno == EEXIST:
                continue
            codes = ["TEMP_FILE_CREATE_FAILED"]
            _close_owned(owned, durable=False, codes=codes)
            return _persistence_result(
                status="IO_FAILED",
                persisted=False,
                codes=codes,
                artifact=artifact,
            )
        except Exception:
            codes = ["TEMP_FILE_CREATE_FAILED"]
            _close_owned(owned, durable=False, codes=codes)
            return _persistence_result(
                status="IO_FAILED",
                persisted=False,
                codes=codes,
                artifact=artifact,
            )
    if temp_fd < 0:
        codes = ["TEMP_FILE_CREATE_FAILED"]
        _close_owned(owned, durable=False, codes=codes)
        return _persistence_result(
            status="IO_FAILED",
            persisted=False,
            codes=codes,
            artifact=artifact,
        )
    try:
        initial_temp_stat = _os_fstat(temp_fd)
    except Exception:
        codes = ["PRE_FINALIZATION_IO_FAILED"]
        _cleanup_temp_before_durability(
            entry_fd=entry_fd, temp_fd=temp_fd, temp_name=temp_name, codes=codes
        )
        _close_owned(owned, durable=False, codes=codes)
        return _persistence_result(
            status="IO_FAILED", persisted=False, codes=codes, artifact=artifact
        )
    try:
        initial_valid = (
            S_ISREG(initial_temp_stat.st_mode)
            and initial_temp_stat.st_size == 0
            and S_IMODE(initial_temp_stat.st_mode) == 0o600
        )
    except Exception:
        initial_valid = False
    if not initial_valid:
        codes = ["TEMP_INODE_VALIDATION_FAILED"]
        _cleanup_temp_before_durability(
            entry_fd=entry_fd, temp_fd=temp_fd, temp_name=temp_name, codes=codes
        )
        _close_owned(owned, durable=False, codes=codes)
        return _persistence_result(
            status="IO_FAILED", persisted=False, codes=codes, artifact=artifact
        )
    offset = 0
    try:
        while offset < len(expected):
            progress = _os_write(temp_fd, expected[offset:])
            if type(progress) is not int or progress <= 0 or progress > len(expected) - offset:
                raise OSError()
            offset += progress
    except Exception:
        codes = ["TEMP_FILE_WRITE_FAILED"]
        _cleanup_temp_before_durability(
            entry_fd=entry_fd, temp_fd=temp_fd, temp_name=temp_name, codes=codes
        )
        _close_owned(owned, durable=False, codes=codes)
        return _persistence_result(
            status="IO_FAILED", persisted=False, codes=codes, artifact=artifact
        )
    try:
        _os_fsync(temp_fd)
    except Exception:
        codes = ["TEMP_FILE_FSYNC_FAILED"]
        _cleanup_temp_before_durability(
            entry_fd=entry_fd, temp_fd=temp_fd, temp_name=temp_name, codes=codes
        )
        _close_owned(owned, durable=False, codes=codes)
        return _persistence_result(
            status="IO_FAILED", persisted=False, codes=codes, artifact=artifact
        )
    try:
        final_temp_stat = _os_fstat(temp_fd)
    except Exception:
        codes = ["PRE_FINALIZATION_IO_FAILED"]
        _cleanup_temp_before_durability(
            entry_fd=entry_fd, temp_fd=temp_fd, temp_name=temp_name, codes=codes
        )
        _close_owned(owned, durable=False, codes=codes)
        return _persistence_result(
            status="IO_FAILED", persisted=False, codes=codes, artifact=artifact
        )
    if not _temp_identity_valid(initial_temp_stat, final_temp_stat, len(expected)):
        codes = ["TEMP_INODE_VALIDATION_FAILED"]
        _cleanup_temp_before_durability(
            entry_fd=entry_fd, temp_fd=temp_fd, temp_name=temp_name, codes=codes
        )
        _close_owned(owned, durable=False, codes=codes)
        return _persistence_result(
            status="IO_FAILED", persisted=False, codes=codes, artifact=artifact
        )
    final_descriptors = []
    try:
        _os_link(
            temp_name,
            ARTIFACT_NAME,
            src_dir_fd=entry_fd,
            dst_dir_fd=entry_fd,
            follow_symlinks=False,
        )
    except Exception as link_error:
        was_eexist = (
            isinstance(link_error, OSError)
            and link_error.errno == EEXIST
        )
        winner_status, winner_fds, winner_stat = _inspect_existing(
            entry_fd, expected
        )
        if winner_status == "IDENTICAL":
            same_trusted_inode = _final_identity_valid(
                final_temp_stat, winner_stat, len(expected)
            )
            if not was_eexist and same_trusted_inode:
                final_descriptors = winner_fds
            else:
                durability = _establish_existing_durability(
                    entry_fd, winner_fds, winner_stat
                )
                if durability == "DURABLE":
                    cleanup_failed = _cleanup_after_durability(
                        entry_fd=entry_fd,
                        final_descriptors=winner_fds,
                        temp_fd=temp_fd,
                        temp_name=temp_name,
                        owned=owned,
                    )
                    if cleanup_failed:
                        return _persistence_result(
                            status="PERSISTED_CLEANUP_WARNING",
                            persisted=True,
                            codes=["PERSISTED_CLEANUP_WARNING"],
                            artifact=artifact,
                            disposition="ALREADY_IDENTICAL",
                        )
                    return _persistence_result(
                        status="ALREADY_IDENTICAL",
                        persisted=True,
                        codes=[],
                        artifact=artifact,
                        disposition="ALREADY_IDENTICAL",
                    )
                primary = (
                    "FINAL_DURABILITY_UNCONFIRMED"
                    if durability == "DURABILITY_UNCONFIRMED"
                    else "EXISTING_TARGET_INSPECTION_FAILED"
                )
                status = (
                    "DURABILITY_UNCONFIRMED"
                    if durability == "DURABILITY_UNCONFIRMED"
                    else "IO_FAILED"
                )
                codes = [primary]
                _close_final_descriptors(winner_fds, codes)
                _cleanup_temp_before_durability(
                    entry_fd=entry_fd,
                    temp_fd=temp_fd,
                    temp_name=temp_name,
                    codes=codes,
                )
                _close_owned(owned, durable=False, codes=codes)
                return _persistence_result(
                    status=status,
                    persisted=False,
                    codes=codes,
                    artifact=artifact,
                    disposition=(
                        "DURABILITY_UNCONFIRMED"
                        if status == "DURABILITY_UNCONFIRMED"
                        else ""
                    ),
                )
        elif not was_eexist and winner_status == "ABSENT":
            primary, status = "ATOMIC_CREATE_FAILED", "IO_FAILED"
        elif winner_status == "CONFLICT":
            primary, status = "RUN_LEDGER_CONFLICT", "CONFLICT"
        elif winner_status == "UNSAFE":
            primary, status = "DESTINATION_PATH_UNSAFE", "AUTHORIZATION_FAILED"
        elif not was_eexist:
            codes = ["FINAL_IDENTITY_VERIFICATION_FAILED"]
            _close_final_descriptors(winner_fds, codes)
            _cleanup_temp_before_durability(
                entry_fd=entry_fd,
                temp_fd=temp_fd,
                temp_name=temp_name,
                codes=codes,
                retain_name=True,
            )
            _close_owned(owned, durable=False, codes=codes)
            return _persistence_result(
                status="DURABILITY_UNCONFIRMED",
                persisted=False,
                codes=codes,
                artifact=artifact,
                disposition="DURABILITY_UNCONFIRMED",
            )
        else:
            primary, status = "EXISTING_TARGET_INSPECTION_FAILED", "IO_FAILED"
        if not final_descriptors:
            codes = [primary]
            _close_final_descriptors(winner_fds, codes)
            _cleanup_temp_before_durability(
                entry_fd=entry_fd,
                temp_fd=temp_fd,
                temp_name=temp_name,
                codes=codes,
            )
            _close_owned(owned, durable=False, codes=codes)
            return _persistence_result(
                status=status,
                persisted=False,
                codes=codes,
                artifact=artifact,
                disposition=(
                    "DURABILITY_UNCONFIRMED"
                    if status == "DURABILITY_UNCONFIRMED"
                    else ""
                ),
            )

    if not final_descriptors:
        try:
            final_before = _os_open(
                ARTIFACT_NAME, _final_flags(), dir_fd=entry_fd
            )
            final_descriptors.append(final_before)
            before_stat = _os_fstat(final_before)
            if not _final_identity_valid(
                final_temp_stat, before_stat, len(expected)
            ):
                raise ValueError()
        except Exception:
            codes = ["FINAL_IDENTITY_VERIFICATION_FAILED"]
            _close_final_descriptors(final_descriptors, codes)
            _cleanup_temp_before_durability(
                entry_fd=entry_fd,
                temp_fd=temp_fd,
                temp_name=temp_name,
                codes=codes,
                retain_name=True,
            )
            _close_owned(owned, durable=False, codes=codes)
            return _persistence_result(
                status="DURABILITY_UNCONFIRMED",
                persisted=False,
                codes=codes,
                artifact=artifact,
                disposition="DURABILITY_UNCONFIRMED",
            )
    try:
        _os_fsync(entry_fd)
    except Exception:
        codes = ["FINAL_DURABILITY_UNCONFIRMED"]
        _close_final_descriptors(final_descriptors, codes)
        _cleanup_temp_before_durability(
            entry_fd=entry_fd, temp_fd=temp_fd, temp_name=temp_name, codes=codes
        )
        _close_owned(owned, durable=False, codes=codes)
        return _persistence_result(
            status="DURABILITY_UNCONFIRMED",
            persisted=False,
            codes=codes,
            artifact=artifact,
            disposition="DURABILITY_UNCONFIRMED",
        )
    try:
        final_after = _os_open(ARTIFACT_NAME, _final_flags(), dir_fd=entry_fd)
        final_descriptors.append(final_after)
        after_stat = _os_fstat(final_after)
        if not _final_identity_valid(final_temp_stat, after_stat, len(expected)):
            raise ValueError()
    except Exception:
        codes = ["FINAL_IDENTITY_VERIFICATION_FAILED"]
        _close_final_descriptors(final_descriptors, codes)
        _cleanup_temp_before_durability(
            entry_fd=entry_fd,
            temp_fd=temp_fd,
            temp_name=temp_name,
            codes=codes,
            retain_name=True,
        )
        _close_owned(owned, durable=False, codes=codes)
        return _persistence_result(
            status="DURABILITY_UNCONFIRMED",
            persisted=False,
            codes=codes,
            artifact=artifact,
            disposition="DURABILITY_UNCONFIRMED",
        )
    cleanup_failed = _cleanup_after_durability(
        entry_fd=entry_fd,
        final_descriptors=final_descriptors,
        temp_fd=temp_fd,
        temp_name=temp_name,
        owned=owned,
    )
    if cleanup_failed:
        return _persistence_result(
            status="PERSISTED_CLEANUP_WARNING",
            persisted=True,
            codes=["PERSISTED_CLEANUP_WARNING"],
            artifact=artifact,
            disposition="WRITTEN",
        )
    return _persistence_result(
        status="WRITTEN",
        persisted=True,
        codes=[],
        artifact=artifact,
        disposition="WRITTEN",
    )
