"""Complete contract tests for the run-ledger persistence boundary."""

import ast
import errno
import hashlib
import inspect
import json
import os
import stat
import types

from ai_daily_publishing_system.core import run_ledger_persistence as sut


ARTIFACT_STATUSES = (
    "BUILT", "NOT_ELIGIBLE", "INVALID", "SERIALIZATION_FAILED",
)
PERSISTENCE_STATUSES = (
    "WRITTEN", "ALREADY_IDENTICAL", "NOT_ELIGIBLE", "INVALID",
    "AUTHORIZATION_FAILED", "SERIALIZATION_FAILED", "CONFLICT",
    "IO_FAILED", "DURABILITY_UNCONFIRMED", "PERSISTED_CLEANUP_WARNING",
)
WRITE_DISPOSITIONS = (
    "WRITTEN", "ALREADY_IDENTICAL", "DURABILITY_UNCONFIRMED",
)
REASON_CODES = (
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
REASON_STRINGS = (
    ("P2D45A_SUCCESS_ENVELOPE_INVALID", "The complete P2D-45A success envelope is invalid."),
    ("P2D45A_ENVELOPE_NOT_ELIGIBLE", "The P2D-45A envelope is not eligible for persistence."),
    ("RUN_LEDGER_SERIALIZATION_FAILED", "The validated run-ledger entry could not be serialized under the canonical JSON YAML-subset contract."),
    ("DESTINATION_ROOT_INVALID", "The authorized Ops root does not satisfy the fixed local destination contract."),
    ("DESTINATION_PATH_UNSAFE", "The internally generated destination cannot be traversed safely."),
    ("FILESYSTEM_CAPABILITY_UNAVAILABLE", "A required local POSIX filesystem capability is unavailable."),
    ("EXISTING_TARGET_INSPECTION_FAILED", "The existing deterministic target could not be inspected safely."),
    ("RUN_LEDGER_CONFLICT", "The deterministic target already contains different bytes."),
    ("PRE_FINALIZATION_IO_FAILED", "A filesystem operation failed before atomic finalization; operating-system details are suppressed."),
    ("TEMP_NAME_GENERATION_FAILED", "A valid private temporary-file name could not be generated."),
    ("TEMP_FILE_CREATE_FAILED", "The same-directory temporary file could not be created."),
    ("TEMP_INODE_VALIDATION_FAILED", "The temporary descriptor did not retain the required regular-file identity, mode, and size contract."),
    ("TEMP_FILE_WRITE_FAILED", "The complete serialized content could not be written to the temporary file."),
    ("TEMP_FILE_FSYNC_FAILED", "Temporary-file durability could not be established before finalization."),
    ("ATOMIC_CREATE_FAILED", "The create-only atomic finalization operation failed."),
    ("FINAL_IDENTITY_VERIFICATION_FAILED", "The final name may exist, but continuity with the fsynced temporary inode could not be verified."),
    ("FINAL_DURABILITY_UNCONFIRMED", "The final path may contain the expected bytes, but durable persistence is unconfirmed."),
    ("FINAL_INSPECTION_CLOSE_FAILED", "A final-inspection descriptor could not be closed before durable persistence was established."),
    ("TEMP_FILE_CLOSE_FAILED", "The temporary-file descriptor could not be closed before durable persistence was established."),
    ("TEMP_CLEANUP_FAILED", "Temporary-file cleanup failed before final durability was established; an orphan may remain."),
    ("PERSISTED_CLEANUP_WARNING", "The expected final artifact is durable, but post-persistence descriptor or temporary-file cleanup is incomplete or unconfirmed; an orphan may remain."),
    ("RUN_LEDGER_PERSISTENCE_ARTIFACT_BUILT", "A deterministic run-ledger persistence artifact was built in memory."),
    ("RUN_LEDGER_ALREADY_PERSISTED_IDENTICAL", "The identical run-ledger artifact was already durably present."),
    ("RUN_LEDGER_PERSISTED", "The run-ledger artifact was durably written."),
)
DIAGNOSTIC_PATHS = (
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
INVARIANTS = (
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
ARTIFACT_RESULT_KEYS = (
    "persistence_artifact_built", "artifact_status", "reason_code", "reason",
    "source", "persistence_artifact", "artifact_violations",
    "missing_or_invalid_fields", "diagnostic_records", "invariant_refs",
)
PERSISTENCE_RESULT_KEYS = (
    "run_ledger_persisted", "persistence_status", "reason_code", "reason",
    "source", "persistence_evidence", "persistence_violations",
    "missing_or_invalid_fields", "diagnostic_records", "invariant_refs",
)
SOURCE_KEYS = (
    "boundary_scope", "schema_version", "artifact_name",
    "serialization_format", "content_digest_algorithm",
)
SOURCE = {
    "boundary_scope": "run_ledger_persistence_boundary",
    "schema_version": "p2d45.run_ledger_persistence.v1",
    "artifact_name": "run-ledger.yaml",
    "serialization_format": "canonical_json_yaml_1_2_subset",
    "content_digest_algorithm": "sha256",
}
PERSISTENCE_ARTIFACT_KEYS = (
    "run_ledger_entry_id", "run_id", "artifact_relative_path",
    "serialization_format", "serialized_content", "content_digest_algorithm",
    "content_digest",
)
PERSISTENCE_EVIDENCE_KEYS = (
    "run_ledger_entry_id", "run_id", "artifact_relative_path",
    "serialization_format", "content_digest_algorithm", "content_digest",
    "write_disposition",
)
DIAGNOSTIC_RECORD_KEYS = ("reason_code", "field")
REQUIRED_CAPABILITIES = (
    "os.open", "os.read", "os.write", "os.close", "os.fstat", "os.fsync",
    "os.mkdir", "os.link", "os.unlink", "directory_file_descriptors",
    "src_dir_fd", "dst_dir_fd", "O_DIRECTORY", "O_NOFOLLOW",
    "O_CREAT | O_EXCL", "create_only_hard_link", "file_fsync",
    "directory_fsync", "st_mtime_ns",
)

P2D45A_ROOT_KEYS = (
    "run_ledger_entry_assembled", "reason_code", "reason", "source",
    "run_ledger_entry", "assembly_violations", "missing_or_invalid_fields",
    "coherence_violations", "invariant_refs",
)
P2D45A_SUCCESS_SOURCE_KEYS = (
    "assembly_scope", "schema_version", "run_ledger_entry_id", "run_id",
    "local_noop_runner_result_id", "run_version_provenance_id",
    "run_version_provenance_schema_version", "mode", "ledger_terminal_status",
    "public_url", "public_url_created", "component_version_count",
    "source_of_truth",
)
P2D45A_ENTRY_KEYS = (
    "schema_version", "run_ledger_entry_id", "run_id", "entry_kind", "mode",
    "ledger_terminal_status", "local_noop_runner_result_id",
    "local_noop_e2e_contract_ref", "public_url", "public_url_created",
    "runner_evidence_items", "required_runner_evidence_ids",
    "missing_runner_evidence_ids", "blocking_runner_evidence_ids",
    "runner_result_created_at", "runner_result_timestamp_policy",
    "run_version_provenance_id", "run_version_provenance_schema_version",
    "skill_version", "rubric_version", "generator_version", "renderer_version",
    "publisher_version", "resolved_component_version_evidence_items",
    "version_provenance_resolved_at", "version_provenance_resolution_policy",
    "source_of_truth",
)
P2D45A_RUNNER_EVIDENCE_KEYS = (
    "runner_evidence_id", "runner_evidence_role", "artifact_ref",
    "artifact_kind", "evidence_status", "producer_ref", "evidence_refs",
)
P2D45A_VERSION_EVIDENCE_KEYS = (
    "version_field", "resolved_version", "resolution_status", "resolver_ref",
    "evidence_ref",
)
P2D45A_INVARIANTS = (
    "run_ledger_entry_assembler_only", "assembler_pure_in_memory_only",
    "assembler_accepts_complete_p2d44_and_p2d45v_results",
    "upstream_envelope_classification_is_three_way",
    "valid_success_envelope_requires_complete_success_contract",
    "valid_blocked_envelope_requires_complete_blocked_contract",
    "malformed_envelope_is_invalid", "valid_blocked_and_invalid_are_mutually_exclusive",
    "nested_upstream_bypass_rejected", "upstream_assemblers_not_invoked",
    "upstream_contract_constants_only_dependency", "explicit_run_ledger_entry_id_required",
    "run_ledger_entry_id_is_opaque_caller_identity", "run_ledger_entry_id_not_generated_or_derived",
    "run_id_projected_from_p2d44", "p2d44_and_p2d45v_run_ids_must_match",
    "p2d44_source_and_result_coherence_required", "p2d45v_source_and_provenance_coherence_required",
    "exactly_five_component_versions_required", "component_version_order_fixed",
    "direct_ledger_version_fields_are_authoritative", "version_evidence_projection_must_match_direct_versions",
    "run_version_provenance_id_link_required", "run_version_provenance_schema_compatibility_required",
    "resolver_refs_are_opaque", "evidence_refs_are_opaque", "no_actual_resolver_payload_in_ledger",
    "runner_evidence_projected_without_value_change", "runner_evidence_notes_not_projected",
    "failed_runner_evidence_may_be_recorded", "known_blocking_evidence_ids_are_evidence_only",
    "source_of_truth_combines_p2d44_then_p2d45v", "source_of_truth_order_and_duplicates_preserved",
    "independent_timestamps_not_compared", "independent_policies_not_compared", "caller_input_not_mutated",
    "output_containers_are_fresh", "nonempty_output_tuples_are_identity_isolated",
    "empty_tuple_identity_not_required", "blocked_output_is_fixed_and_caller_safe",
    "unknown_keys_block_and_are_suppressed", "aliases_and_wrong_path_keys_block",
    "validation_is_cycle_and_depth_safe", "scalar_strings_are_not_scanned_as_keys", "mode_noop_required",
    "ledger_terminal_status_must_be_noop_completed", "recorded_terminal_status_is_upstream_metadata_only",
    "public_url_must_be_null", "public_url_created_must_be_false", "pass_published_forbidden",
    "no_quality_pass_no_public_url", "run_ledger_entry_assembled_means_in_memory_candidate_only",
    "assembly_not_runtime_completion", "assembly_not_state_decision", "assembly_not_state_transition",
    "assembly_not_ledger_persistence", "assembly_not_publish_authorization", "assembly_not_publication",
    "assembly_not_public_url_creation", "assembly_not_notification", "no_file_or_artifact_io",
    "no_run_ledger_yaml_read_or_write", "no_git_or_release_inspection", "no_clock_or_environment_access",
    "no_resolver_execution", "no_runtime_or_external_api_call", "no_live_model_call",
)
VERSION_FIELDS = (
    "skill_version", "rubric_version", "generator_version",
    "renderer_version", "publisher_version",
)
ENTRY_ID_DIGEST = "5ecbc192017833e40d812cac9daec51f310ef4b492502fb63ca0821588ce9b29"
SECOND_ENTRY_ID_DIGEST = "064aa6068dca0e795c7a434ff11449c857170759808b3b19748e317df9d231ff"
ARTIFACT_RELATIVE_PATH = (
    "runs/by-entry-id/sha256-" + ENTRY_ID_DIGEST + "/run-ledger.yaml"
)


def _version_items():
    values = ("skill-1", "rubric-2", "generator-3", "renderer-4", "publisher-5")
    return tuple(
        {
            "version_field": field,
            "resolved_version": values[index],
            "resolution_status": "resolved",
            "resolver_ref": "resolver-ref",
            "evidence_ref": "evidence-ref",
        }
        for index, field in enumerate(VERSION_FIELDS)
    )


def _entry():
    return {
        "schema_version": "p2d45.run_ledger_entry.v1",
        "run_ledger_entry_id": "ledger-entry-001",
        "run_id": "run-001",
        "entry_kind": "run_ledger_entry",
        "mode": "noop",
        "ledger_terminal_status": "NOOP_COMPLETED",
        "local_noop_runner_result_id": "runner-result-001",
        "local_noop_e2e_contract_ref": "e2e-contract-001",
        "public_url": None,
        "public_url_created": False,
        "runner_evidence_items": ({
            "runner_evidence_id": "runner-evidence-001",
            "runner_evidence_role": "local_noop_runner_result",
            "artifact_ref": "runner-artifact-001",
            "artifact_kind": "local_noop_runner_result",
            "evidence_status": "passed",
            "producer_ref": "p2d-44",
            "evidence_refs": ("artifact#evidence",),
        },),
        "required_runner_evidence_ids": ("runner-evidence-001",),
        "missing_runner_evidence_ids": (),
        "blocking_runner_evidence_ids": (),
        "runner_result_created_at": "runner-created-at",
        "runner_result_timestamp_policy": "runner-timestamp-policy",
        "run_version_provenance_id": "provenance-001",
        "run_version_provenance_schema_version": "p2d45.run_version_provenance.v1",
        "skill_version": "skill-1",
        "rubric_version": "rubric-2",
        "generator_version": "generator-3",
        "renderer_version": "renderer-4",
        "publisher_version": "publisher-5",
        "resolved_component_version_evidence_items": _version_items(),
        "version_provenance_resolved_at": "provenance-resolved-at",
        "version_provenance_resolution_policy": "stable-release-policy",
        "source_of_truth": ("p2d-44", "shared-source", "p2d-45v", "shared-source"),
    }


def _success_envelope():
    entry = _entry()
    return {
        "run_ledger_entry_assembled": True,
        "reason_code": "RUN_LEDGER_ENTRY_ASSEMBLED_IN_MEMORY",
        "reason": "A deterministic run-ledger entry candidate was assembled in memory.",
        "source": {
            "assembly_scope": "run_ledger_entry_in_memory_only",
            "schema_version": "p2d45.run_ledger_entry.v1",
            "run_ledger_entry_id": "ledger-entry-001",
            "run_id": "run-001",
            "local_noop_runner_result_id": "runner-result-001",
            "run_version_provenance_id": "provenance-001",
            "run_version_provenance_schema_version": "p2d45.run_version_provenance.v1",
            "mode": "noop",
            "ledger_terminal_status": "NOOP_COMPLETED",
            "public_url": None,
            "public_url_created": False,
            "component_version_count": 5,
            "source_of_truth": ("p2d-44", "shared-source", "p2d-45v", "shared-source"),
        },
        "run_ledger_entry": entry,
        "assembly_violations": (),
        "missing_or_invalid_fields": (),
        "coherence_violations": (),
        "invariant_refs": P2D45A_INVARIANTS,
    }


def _blocked_envelope():
    return {
        "run_ledger_entry_assembled": False,
        "reason_code": "RUN_LEDGER_ENTRY_ID_INVALID",
        "reason": "run_ledger_entry_id must be an exact nonblank string.",
        "source": {
            "assembly_scope": "run_ledger_entry_in_memory_only",
            "schema_version": "p2d45.run_ledger_entry.v1",
            "component_version_count": 0,
        },
        "run_ledger_entry": {},
        "assembly_violations": ("RUN_LEDGER_ENTRY_ID_INVALID",),
        "missing_or_invalid_fields": ("run_ledger_entry_id",),
        "coherence_violations": ({
            "reason_code": "RUN_LEDGER_ENTRY_ID_INVALID",
            "field": "run_ledger_entry_id",
        },),
        "invariant_refs": P2D45A_INVARIANTS,
    }


GOLDEN_BYTES = (
    '{\n'
    '  "schema_version": "p2d45.run_ledger_entry.v1",\n'
    '  "run_ledger_entry_id": "ledger-entry-001",\n'
    '  "run_id": "run-001",\n'
    '  "entry_kind": "run_ledger_entry",\n'
    '  "mode": "noop",\n'
    '  "ledger_terminal_status": "NOOP_COMPLETED",\n'
    '  "local_noop_runner_result_id": "runner-result-001",\n'
    '  "local_noop_e2e_contract_ref": "e2e-contract-001",\n'
    '  "public_url": null,\n'
    '  "public_url_created": false,\n'
    '  "runner_evidence_items": [\n'
    '    {\n'
    '      "runner_evidence_id": "runner-evidence-001",\n'
    '      "runner_evidence_role": "local_noop_runner_result",\n'
    '      "artifact_ref": "runner-artifact-001",\n'
    '      "artifact_kind": "local_noop_runner_result",\n'
    '      "evidence_status": "passed",\n'
    '      "producer_ref": "p2d-44",\n'
    '      "evidence_refs": [\n'
    '        "artifact#evidence"\n'
    '      ]\n'
    '    }\n'
    '  ],\n'
    '  "required_runner_evidence_ids": [\n'
    '    "runner-evidence-001"\n'
    '  ],\n'
    '  "missing_runner_evidence_ids": [],\n'
    '  "blocking_runner_evidence_ids": [],\n'
    '  "runner_result_created_at": "runner-created-at",\n'
    '  "runner_result_timestamp_policy": "runner-timestamp-policy",\n'
    '  "run_version_provenance_id": "provenance-001",\n'
    '  "run_version_provenance_schema_version": "p2d45.run_version_provenance.v1",\n'
    '  "skill_version": "skill-1",\n'
    '  "rubric_version": "rubric-2",\n'
    '  "generator_version": "generator-3",\n'
    '  "renderer_version": "renderer-4",\n'
    '  "publisher_version": "publisher-5",\n'
    '  "resolved_component_version_evidence_items": [\n'
    '    {\n'
    '      "version_field": "skill_version",\n'
    '      "resolved_version": "skill-1",\n'
    '      "resolution_status": "resolved",\n'
    '      "resolver_ref": "resolver-ref",\n'
    '      "evidence_ref": "evidence-ref"\n'
    '    },\n'
    '    {\n'
    '      "version_field": "rubric_version",\n'
    '      "resolved_version": "rubric-2",\n'
    '      "resolution_status": "resolved",\n'
    '      "resolver_ref": "resolver-ref",\n'
    '      "evidence_ref": "evidence-ref"\n'
    '    },\n'
    '    {\n'
    '      "version_field": "generator_version",\n'
    '      "resolved_version": "generator-3",\n'
    '      "resolution_status": "resolved",\n'
    '      "resolver_ref": "resolver-ref",\n'
    '      "evidence_ref": "evidence-ref"\n'
    '    },\n'
    '    {\n'
    '      "version_field": "renderer_version",\n'
    '      "resolved_version": "renderer-4",\n'
    '      "resolution_status": "resolved",\n'
    '      "resolver_ref": "resolver-ref",\n'
    '      "evidence_ref": "evidence-ref"\n'
    '    },\n'
    '    {\n'
    '      "version_field": "publisher_version",\n'
    '      "resolved_version": "publisher-5",\n'
    '      "resolution_status": "resolved",\n'
    '      "resolver_ref": "resolver-ref",\n'
    '      "evidence_ref": "evidence-ref"\n'
    '    }\n'
    '  ],\n'
    '  "version_provenance_resolved_at": "provenance-resolved-at",\n'
    '  "version_provenance_resolution_policy": "stable-release-policy",\n'
    '  "source_of_truth": [\n'
    '    "p2d-44",\n'
    '    "shared-source",\n'
    '    "p2d-45v",\n'
    '    "shared-source"\n'
    '  ]\n'
    '}\n'
).encode("utf-8")
GOLDEN_DIGEST = "8cf31104b135cad03f07a6f71ce63f19b919913a0f77c610f0e2379fa4db7fd0"


def _artifact(envelope=None):
    return sut.build_run_ledger_persistence_artifact(
        run_ledger_entry_assembly=(
            _success_envelope() if envelope is None else envelope
        )
    )


def _ops_root(tmp_path):
    root = tmp_path / "ops-root"
    (root / "runs" / "by-entry-id").mkdir(parents=True)
    return root


def _persist(tmp_path, envelope=None, root=None):
    selected_root = _ops_root(tmp_path) if root is None else root
    return sut.persist_run_ledger_entry(
        run_ledger_entry_assembly=(
            _success_envelope() if envelope is None else envelope
        ),
        authorized_ops_root=str(selected_root),
    )


def _assert_fixed_invalid(result, *, persistence):
    expected_keys = PERSISTENCE_RESULT_KEYS if persistence else ARTIFACT_RESULT_KEYS
    violation_key = "persistence_violations" if persistence else "artifact_violations"
    nested_key = "persistence_evidence" if persistence else "persistence_artifact"
    assert tuple(result) == expected_keys
    assert result["reason_code"] == "P2D45A_SUCCESS_ENVELOPE_INVALID"
    assert result["reason"] == "The complete P2D-45A success envelope is invalid."
    assert result[violation_key] == ("P2D45A_SUCCESS_ENVELOPE_INVALID",)
    assert result["missing_or_invalid_fields"] == ("run_ledger_entry_assembly",)
    assert result["diagnostic_records"] == ({
        "reason_code": "P2D45A_SUCCESS_ENVELOPE_INVALID",
        "field": "run_ledger_entry_assembly",
    },)
    assert result[nested_key] == {}
    assert result["source"] == SOURCE
    assert result["invariant_refs"] == INVARIANTS


def _spy(monkeypatch, name, events):
    original = getattr(sut, name)

    def wrapper(*args, **kwargs):
        events.append((name, args, kwargs))
        return original(*args, **kwargs)

    monkeypatch.setattr(sut, name, wrapper)
    return original


def _assert_non_invalid(result):
    assert result["persistence_status"] != "INVALID"


def test_public_api_signatures_are_exact():
    cases = (
        (sut.build_run_ledger_persistence_artifact, ("run_ledger_entry_assembly",), (dict[str, object],)),
        (sut.persist_run_ledger_entry, ("run_ledger_entry_assembly", "authorized_ops_root"), (dict[str, object], str)),
    )
    for function, names, annotations in cases:
        signature = inspect.signature(function)
        assert tuple(signature.parameters) == names
        for index, parameter in enumerate(signature.parameters.values()):
            assert parameter.kind is inspect.Parameter.KEYWORD_ONLY
            assert parameter.default is inspect.Parameter.empty
            assert parameter.annotation == annotations[index]
        assert signature.return_annotation == dict[str, object]


def test_contract_catalogs_are_exact():
    assert sut.ARTIFACT_STATUSES == ARTIFACT_STATUSES
    assert sut.PERSISTENCE_STATUSES == PERSISTENCE_STATUSES
    assert sut.WRITE_DISPOSITIONS == WRITE_DISPOSITIONS
    assert sut.REASON_CODES == REASON_CODES
    assert sut.REASON_PRIORITY == REASON_CODES
    assert sut.REASON_STRINGS == REASON_STRINGS
    assert sut.DIAGNOSTIC_PATHS == DIAGNOSTIC_PATHS
    assert sut.INVARIANT_REFS == INVARIANTS
    assert sut.ARTIFACT_RESULT_KEYS == ARTIFACT_RESULT_KEYS
    assert sut.PERSISTENCE_RESULT_KEYS == PERSISTENCE_RESULT_KEYS
    assert sut.SOURCE_KEYS == SOURCE_KEYS
    assert sut.PERSISTENCE_ARTIFACT_KEYS == PERSISTENCE_ARTIFACT_KEYS
    assert sut.PERSISTENCE_EVIDENCE_KEYS == PERSISTENCE_EVIDENCE_KEYS
    assert sut.DIAGNOSTIC_RECORD_KEYS == DIAGNOSTIC_RECORD_KEYS
    assert len(REASON_CODES) == 24
    assert len(INVARIANTS) == 56


def test_exact_p2d45a_success_envelope_builds_artifact():
    result = _artifact()
    assert result["persistence_artifact_built"] is True
    assert result["artifact_status"] == "BUILT"
    assert result["reason_code"] == "RUN_LEDGER_PERSISTENCE_ARTIFACT_BUILT"
    assert tuple(result["persistence_artifact"]) == PERSISTENCE_ARTIFACT_KEYS
    assert result["artifact_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()
    assert result["diagnostic_records"] == ()


def test_non_success_marker_is_not_eligible_without_filesystem_effect(monkeypatch):
    calls = []
    _spy(monkeypatch, "_os_open", calls)
    artifact = _artifact(_blocked_envelope())
    assert artifact["artifact_status"] == "NOT_ELIGIBLE"
    assert artifact["persistence_artifact_built"] is False
    assert artifact["reason_code"] == "P2D45A_ENVELOPE_NOT_ELIGIBLE"
    assert artifact["artifact_violations"] == ("P2D45A_ENVELOPE_NOT_ELIGIBLE",)
    assert calls == []


def test_malformed_success_envelope_is_invalid():
    malformed = _success_envelope()
    malformed["reason"] = "caller-controlled"
    _assert_fixed_invalid(_artifact(malformed), persistence=False)
    _assert_fixed_invalid(
        sut.persist_run_ledger_entry(
            run_ledger_entry_assembly=malformed,
            authorized_ops_root="/not-inspected-by-skeleton",
        ),
        persistence=True,
    )


def test_nested_run_ledger_entry_bypass_is_invalid():
    _assert_fixed_invalid(_artifact({"run_ledger_entry": _entry()}), persistence=False)


def test_unknown_keys_and_hostile_values_are_suppressed():
    calls = {"eq": 0, "hash": 0, "repr": 0, "str": 0}

    class Hostile:
        def __eq__(self, other):
            calls["eq"] += 1
            raise AssertionError(other)

        def __hash__(self):
            calls["hash"] += 1
            raise AssertionError("hash")

        def __repr__(self):
            calls["repr"] += 1
            raise AssertionError("repr")

        def __str__(self):
            calls["str"] += 1
            raise AssertionError("str")

    envelope = _success_envelope()
    hostile = Hostile()
    envelope["unknown"] = hostile
    artifact = _artifact(envelope)
    persistence = sut.persist_run_ledger_entry(
        run_ledger_entry_assembly=envelope,
        authorized_ops_root=hostile,
    )
    _assert_fixed_invalid(artifact, persistence=False)
    _assert_fixed_invalid(persistence, persistence=True)
    assert calls == {"eq": 0, "hash": 0, "repr": 0, "str": 0}


def test_artifact_builder_does_not_mutate_or_retain_input():
    invalid_input = {"caller": ["value"]}
    invalid_result = _artifact(invalid_input)
    invalid_input["caller"].append("later")
    assert "later" not in str(invalid_result)
    success_input = _success_envelope()
    expected = _success_envelope()
    built = _artifact(success_input)
    success_input["run_ledger_entry"]["run_id"] = "mutated"
    assert built["artifact_status"] == "BUILT"
    assert built["persistence_artifact"]["run_id"] == "run-001"
    assert expected["run_ledger_entry"]["run_id"] == "run-001"


def test_canonical_json_yaml_subset_golden_bytes_are_exact():
    result = _artifact()
    assert result["artifact_status"] == "BUILT"
    assert result["persistence_artifact_built"] is True
    artifact = result["persistence_artifact"]
    assert tuple(artifact) == PERSISTENCE_ARTIFACT_KEYS
    assert artifact["serialized_content"] == GOLDEN_BYTES


def test_tuple_projection_and_key_order_are_exact():
    artifact = _artifact()["persistence_artifact"]
    assert tuple(artifact) == PERSISTENCE_ARTIFACT_KEYS
    content = artifact["serialized_content"]
    assert b'"runner_evidence_items": [' in content
    assert b'"missing_runner_evidence_ids": []' in content
    assert content.find(b'"skill_version"') < content.find(b'"publisher_version"')


def test_unicode_null_boolean_and_final_newline_are_exact():
    envelope = _success_envelope()
    envelope["run_ledger_entry"]["runner_result_created_at"] = "时间"
    envelope["source"]["source_of_truth"] = ("时间",)
    envelope["run_ledger_entry"]["source_of_truth"] = ("时间",)
    result = _artifact(envelope)
    assert result["artifact_status"] == "BUILT"
    assert result["persistence_artifact_built"] is True
    artifact = result["persistence_artifact"]
    assert tuple(artifact) == PERSISTENCE_ARTIFACT_KEYS
    content = artifact["serialized_content"]
    assert "时间".encode("utf-8") in content
    assert b'"public_url": null' in content
    assert b'"public_url_created": false' in content
    assert content.endswith(b"\n") and not content.endswith(b"\n\n")


def test_serialization_is_repeatable_and_alias_tag_free():
    first_result = _artifact()
    assert first_result["artifact_status"] == "BUILT"
    assert first_result["persistence_artifact_built"] is True
    first_artifact = first_result["persistence_artifact"]
    assert tuple(first_artifact) == PERSISTENCE_ARTIFACT_KEYS
    first = first_artifact["serialized_content"]

    second_result = _artifact()
    assert second_result["artifact_status"] == "BUILT"
    assert second_result["persistence_artifact_built"] is True
    second_artifact = second_result["persistence_artifact"]
    assert tuple(second_artifact) == PERSISTENCE_ARTIFACT_KEYS
    second = second_artifact["serialized_content"]
    assert first == second == GOLDEN_BYTES
    assert all(marker not in first for marker in (b"&id", b"*id", b"!!", b"%YAML"))


def test_content_digest_is_sha256_of_exact_bytes():
    result = _artifact()
    assert result["artifact_status"] == "BUILT"
    assert result["persistence_artifact_built"] is True
    artifact = result["persistence_artifact"]
    assert tuple(artifact) == PERSISTENCE_ARTIFACT_KEYS
    assert artifact["content_digest"] == GOLDEN_DIGEST
    assert hashlib.sha256(GOLDEN_BYTES).hexdigest() == GOLDEN_DIGEST


def test_artifact_relative_path_hashes_entry_id():
    result = _artifact()
    assert result["artifact_status"] == "BUILT"
    assert result["persistence_artifact_built"] is True
    artifact = result["persistence_artifact"]
    assert tuple(artifact) == PERSISTENCE_ARTIFACT_KEYS
    assert artifact["artifact_relative_path"] == ARTIFACT_RELATIVE_PATH
    assert ENTRY_ID_DIGEST == hashlib.sha256(b"ledger-entry-001").hexdigest()


def test_absolute_dotdot_and_separator_identity_text_cannot_control_path():
    envelope = _success_envelope()
    hostile_id = "/../../caller//selected/run-ledger.yaml"
    envelope["source"]["run_ledger_entry_id"] = hostile_id
    envelope["run_ledger_entry"]["run_ledger_entry_id"] = hostile_id
    result = _artifact(envelope)
    assert result["artifact_status"] == "BUILT"
    assert result["persistence_artifact_built"] is True
    artifact = result["persistence_artifact"]
    assert tuple(artifact) == PERSISTENCE_ARTIFACT_KEYS
    expected_hash = hashlib.sha256(hostile_id.encode("utf-8")).hexdigest()
    assert artifact["artifact_relative_path"] == (
        "runs/by-entry-id/sha256-" + expected_hash + "/run-ledger.yaml"
    )
    assert hostile_id not in artifact["artifact_relative_path"]


def test_persist_invokes_artifact_builder_exactly_once_and_accepts_no_caller_bytes(monkeypatch, tmp_path):
    calls = []
    original = sut.build_run_ledger_persistence_artifact

    def spy(*, run_ledger_entry_assembly):
        calls.append(run_ledger_entry_assembly)
        return original(run_ledger_entry_assembly=run_ledger_entry_assembly)

    monkeypatch.setattr(sut, "build_run_ledger_persistence_artifact", spy)
    result = _persist(tmp_path)
    assert len(calls) == 1
    assert calls[0]["run_ledger_entry_assembled"] is True
    assert result["persistence_status"] != "INVALID"
    assert tuple(inspect.signature(sut.persist_run_ledger_entry).parameters) == (
        "run_ledger_entry_assembly", "authorized_ops_root",
    )


def test_result_truth_table_and_shapes_are_exact(monkeypatch, tmp_path):
    reason_by_code = dict(REASON_STRINGS)

    def assert_artifact_common(
        result,
        *,
        status,
        built,
        reason_code,
        violations,
        fields,
        records,
    ):
        assert tuple(result) == ARTIFACT_RESULT_KEYS
        assert type(result["persistence_artifact_built"]) is bool
        assert type(result["artifact_status"]) is str
        assert type(result["reason_code"]) is str
        assert type(result["reason"]) is str
        assert type(result["source"]) is dict
        assert type(result["persistence_artifact"]) is dict
        assert type(result["artifact_violations"]) is tuple
        assert type(result["missing_or_invalid_fields"]) is tuple
        assert type(result["diagnostic_records"]) is tuple
        assert type(result["invariant_refs"]) is tuple
        assert result["persistence_artifact_built"] is built
        assert result["artifact_status"] == status
        assert result["reason_code"] == reason_code
        assert result["reason"] == reason_by_code[reason_code]
        assert tuple(result["source"]) == SOURCE_KEYS
        assert result["source"] == SOURCE
        assert all(type(value) is str for value in result["source"].values())
        assert result["artifact_violations"] == violations
        assert result["missing_or_invalid_fields"] == fields
        assert all(type(item) is str for item in result["artifact_violations"])
        assert all(
            type(item) is str for item in result["missing_or_invalid_fields"]
        )
        assert result["diagnostic_records"] == records
        assert all(
            type(record) is dict
            and tuple(record) == DIAGNOSTIC_RECORD_KEYS
            and type(record["reason_code"]) is str
            and type(record["field"]) is str
            for record in result["diagnostic_records"]
        )
        assert result["invariant_refs"] == INVARIANTS
        assert all(type(item) is str for item in result["invariant_refs"])
        rendered = str(result)
        assert "private caller detail" not in rendered
        assert "private serialization detail" not in rendered
        assert "private os detail" not in rendered
        assert str(tmp_path) not in rendered
        assert ".run-ledger.tmp-" not in rendered

    def assert_artifact_present(result):
        artifact = result["persistence_artifact"]
        assert tuple(artifact) == PERSISTENCE_ARTIFACT_KEYS
        assert type(artifact["run_ledger_entry_id"]) is str
        assert type(artifact["run_id"]) is str
        assert type(artifact["artifact_relative_path"]) is str
        assert type(artifact["serialization_format"]) is str
        assert type(artifact["serialized_content"]) is bytes
        assert type(artifact["content_digest_algorithm"]) is str
        assert type(artifact["content_digest"]) is str

    def assert_artifact_absent(result):
        assert type(result["persistence_artifact"]) is dict
        assert result["persistence_artifact"] == {}

    def assert_persistence_common(
        result,
        *,
        status,
        persisted,
        reason_code,
        violations,
        fields,
        records,
    ):
        assert tuple(result) == PERSISTENCE_RESULT_KEYS
        assert type(result["run_ledger_persisted"]) is bool
        assert type(result["persistence_status"]) is str
        assert type(result["reason_code"]) is str
        assert type(result["reason"]) is str
        assert type(result["source"]) is dict
        assert type(result["persistence_evidence"]) is dict
        assert type(result["persistence_violations"]) is tuple
        assert type(result["missing_or_invalid_fields"]) is tuple
        assert type(result["diagnostic_records"]) is tuple
        assert type(result["invariant_refs"]) is tuple
        assert result["run_ledger_persisted"] is persisted
        assert result["persistence_status"] == status
        assert result["reason_code"] == reason_code
        assert result["reason"] == reason_by_code[reason_code]
        assert tuple(result["source"]) == SOURCE_KEYS
        assert result["source"] == SOURCE
        assert all(type(value) is str for value in result["source"].values())
        assert result["persistence_violations"] == violations
        assert result["missing_or_invalid_fields"] == fields
        assert all(
            type(item) is str for item in result["persistence_violations"]
        )
        assert all(
            type(item) is str for item in result["missing_or_invalid_fields"]
        )
        assert result["diagnostic_records"] == records
        assert all(
            type(record) is dict
            and tuple(record) == DIAGNOSTIC_RECORD_KEYS
            and type(record["reason_code"]) is str
            and type(record["field"]) is str
            for record in result["diagnostic_records"]
        )
        assert result["invariant_refs"] == INVARIANTS
        assert all(type(item) is str for item in result["invariant_refs"])

    def assert_evidence_present(result, disposition):
        evidence = result["persistence_evidence"]
        assert tuple(evidence) == PERSISTENCE_EVIDENCE_KEYS
        assert all(type(value) is str for value in evidence.values())
        assert evidence["write_disposition"] == disposition

    def assert_evidence_absent(result):
        assert type(result["persistence_evidence"]) is dict
        assert result["persistence_evidence"] == {}

    built = _artifact()
    not_eligible = _artifact(_blocked_envelope())
    invalid_envelope = {"private caller detail": ["do not retain"]}
    invalid = _artifact(invalid_envelope)
    with monkeypatch.context() as patcher:
        def fail_serialization(*args, **kwargs):
            del args, kwargs
            raise TypeError("private serialization detail")

        patcher.setattr(json, "dumps", fail_serialization)
        serialization_failed = _artifact()

    assert_artifact_common(
        built,
        status="BUILT",
        built=True,
        reason_code="RUN_LEDGER_PERSISTENCE_ARTIFACT_BUILT",
        violations=(),
        fields=(),
        records=(),
    )
    assert_artifact_present(built)
    assert_artifact_common(
        not_eligible,
        status="NOT_ELIGIBLE",
        built=False,
        reason_code="P2D45A_ENVELOPE_NOT_ELIGIBLE",
        violations=("P2D45A_ENVELOPE_NOT_ELIGIBLE",),
        fields=("run_ledger_entry_assembly",),
        records=({
            "reason_code": "P2D45A_ENVELOPE_NOT_ELIGIBLE",
            "field": "run_ledger_entry_assembly",
        },),
    )
    assert_artifact_absent(not_eligible)
    assert_artifact_common(
        invalid,
        status="INVALID",
        built=False,
        reason_code="P2D45A_SUCCESS_ENVELOPE_INVALID",
        violations=("P2D45A_SUCCESS_ENVELOPE_INVALID",),
        fields=("run_ledger_entry_assembly",),
        records=({
            "reason_code": "P2D45A_SUCCESS_ENVELOPE_INVALID",
            "field": "run_ledger_entry_assembly",
        },),
    )
    assert_artifact_absent(invalid)
    assert_artifact_common(
        serialization_failed,
        status="SERIALIZATION_FAILED",
        built=False,
        reason_code="RUN_LEDGER_SERIALIZATION_FAILED",
        violations=("RUN_LEDGER_SERIALIZATION_FAILED",),
        fields=("run_ledger_entry",),
        records=({
            "reason_code": "RUN_LEDGER_SERIALIZATION_FAILED",
            "field": "run_ledger_entry",
        },),
    )
    assert_artifact_absent(serialization_failed)

    written_root = _ops_root(tmp_path / "truth-written")
    written = _persist(tmp_path, root=written_root)
    already_identical = _persist(tmp_path, root=written_root)
    not_eligible_persistence = sut.persist_run_ledger_entry(
        run_ledger_entry_assembly=_blocked_envelope(),
        authorized_ops_root="/not-inspected-for-not-eligible",
    )
    invalid_persistence = sut.persist_run_ledger_entry(
        run_ledger_entry_assembly=invalid_envelope,
        authorized_ops_root="/not-inspected-for-invalid",
    )
    authorization_failed = sut.persist_run_ledger_entry(
        run_ledger_entry_assembly=_success_envelope(),
        authorized_ops_root=str(tmp_path) + "//invalid-root",
    )
    with monkeypatch.context() as patcher:
        patcher.setattr(json, "dumps", fail_serialization)
        serialization_failed_persistence = sut.persist_run_ledger_entry(
            run_ledger_entry_assembly=_success_envelope(),
            authorized_ops_root="/not-inspected-for-serialization",
        )

    conflict_root = _ops_root(tmp_path / "truth-conflict")
    assert _persist(tmp_path, root=conflict_root)["persistence_status"] == "WRITTEN"
    changed = _success_envelope()
    changed["source"]["source_of_truth"] = ("changed",)
    changed["run_ledger_entry"]["source_of_truth"] = ("changed",)
    conflict = _persist(tmp_path, envelope=changed, root=conflict_root)

    io_root = _ops_root(tmp_path / "truth-io")
    with monkeypatch.context() as patcher:
        def fail_open(*args, **kwargs):
            del args, kwargs
            raise OSError(errno.EIO, "private os detail")

        patcher.setattr(sut, "_os_open", fail_open)
        io_failed = _persist(tmp_path, root=io_root)

    durability_root = _ops_root(tmp_path / "truth-durability")
    with monkeypatch.context() as patcher:
        linked = []
        original_link = sut._os_link
        original_fsync = sut._os_fsync

        def track_link(*args, **kwargs):
            value = original_link(*args, **kwargs)
            linked.append(True)
            return value

        def fail_final_directory_fsync(fd):
            if linked and stat.S_ISDIR(os.fstat(fd).st_mode):
                raise OSError(errno.EIO, "private durability detail")
            return original_fsync(fd)

        patcher.setattr(sut, "_os_link", track_link)
        patcher.setattr(sut, "_os_fsync", fail_final_directory_fsync)
        durability_unconfirmed = _persist(tmp_path, root=durability_root)

    cleanup_root = _ops_root(tmp_path / "truth-cleanup")
    with monkeypatch.context() as patcher:
        def fail_unlink(*args, **kwargs):
            del args, kwargs
            raise OSError(errno.EIO, "private cleanup detail")

        patcher.setattr(sut, "_os_unlink", fail_unlink)
        cleanup_warning = _persist(tmp_path, root=cleanup_root)

    assert_persistence_common(
        written,
        status="WRITTEN",
        persisted=True,
        reason_code="RUN_LEDGER_PERSISTED",
        violations=(),
        fields=(),
        records=(),
    )
    assert_evidence_present(written, "WRITTEN")
    assert_persistence_common(
        already_identical,
        status="ALREADY_IDENTICAL",
        persisted=True,
        reason_code="RUN_LEDGER_ALREADY_PERSISTED_IDENTICAL",
        violations=(),
        fields=(),
        records=(),
    )
    assert_evidence_present(already_identical, "ALREADY_IDENTICAL")
    assert_persistence_common(
        not_eligible_persistence,
        status="NOT_ELIGIBLE",
        persisted=False,
        reason_code="P2D45A_ENVELOPE_NOT_ELIGIBLE",
        violations=("P2D45A_ENVELOPE_NOT_ELIGIBLE",),
        fields=("run_ledger_entry_assembly",),
        records=({
            "reason_code": "P2D45A_ENVELOPE_NOT_ELIGIBLE",
            "field": "run_ledger_entry_assembly",
        },),
    )
    assert_evidence_absent(not_eligible_persistence)
    assert_persistence_common(
        invalid_persistence,
        status="INVALID",
        persisted=False,
        reason_code="P2D45A_SUCCESS_ENVELOPE_INVALID",
        violations=("P2D45A_SUCCESS_ENVELOPE_INVALID",),
        fields=("run_ledger_entry_assembly",),
        records=({
            "reason_code": "P2D45A_SUCCESS_ENVELOPE_INVALID",
            "field": "run_ledger_entry_assembly",
        },),
    )
    assert_evidence_absent(invalid_persistence)
    assert_persistence_common(
        authorization_failed,
        status="AUTHORIZATION_FAILED",
        persisted=False,
        reason_code="DESTINATION_ROOT_INVALID",
        violations=("DESTINATION_ROOT_INVALID",),
        fields=("authorized_ops_root",),
        records=({
            "reason_code": "DESTINATION_ROOT_INVALID",
            "field": "authorized_ops_root",
        },),
    )
    assert_evidence_absent(authorization_failed)
    assert_persistence_common(
        serialization_failed_persistence,
        status="SERIALIZATION_FAILED",
        persisted=False,
        reason_code="RUN_LEDGER_SERIALIZATION_FAILED",
        violations=("RUN_LEDGER_SERIALIZATION_FAILED",),
        fields=("run_ledger_entry",),
        records=({
            "reason_code": "RUN_LEDGER_SERIALIZATION_FAILED",
            "field": "run_ledger_entry",
        },),
    )
    assert_evidence_absent(serialization_failed_persistence)
    assert_persistence_common(
        conflict,
        status="CONFLICT",
        persisted=False,
        reason_code="RUN_LEDGER_CONFLICT",
        violations=("RUN_LEDGER_CONFLICT",),
        fields=("artifact_relative_path",),
        records=({
            "reason_code": "RUN_LEDGER_CONFLICT",
            "field": "artifact_relative_path",
        },),
    )
    assert_evidence_absent(conflict)
    assert_persistence_common(
        io_failed,
        status="IO_FAILED",
        persisted=False,
        reason_code="PRE_FINALIZATION_IO_FAILED",
        violations=("PRE_FINALIZATION_IO_FAILED",),
        fields=("persistence_io",),
        records=({
            "reason_code": "PRE_FINALIZATION_IO_FAILED",
            "field": "persistence_io",
        },),
    )
    assert_evidence_absent(io_failed)
    assert_persistence_common(
        durability_unconfirmed,
        status="DURABILITY_UNCONFIRMED",
        persisted=False,
        reason_code="FINAL_DURABILITY_UNCONFIRMED",
        violations=(
            "FINAL_DURABILITY_UNCONFIRMED",
            "TEMP_CLEANUP_FAILED",
        ),
        fields=("persistence_io",),
        records=(
            {
                "reason_code": "FINAL_DURABILITY_UNCONFIRMED",
                "field": "persistence_io",
            },
            {
                "reason_code": "TEMP_CLEANUP_FAILED",
                "field": "persistence_io",
            },
        ),
    )
    assert_evidence_present(durability_unconfirmed, "DURABILITY_UNCONFIRMED")
    assert_persistence_common(
        cleanup_warning,
        status="PERSISTED_CLEANUP_WARNING",
        persisted=True,
        reason_code="PERSISTED_CLEANUP_WARNING",
        violations=("PERSISTED_CLEANUP_WARNING",),
        fields=("persistence_io",),
        records=({
            "reason_code": "PERSISTED_CLEANUP_WARNING",
            "field": "persistence_io",
        },),
    )
    assert_evidence_present(cleanup_warning, "WRITTEN")

    for result in (
        written,
        already_identical,
        not_eligible_persistence,
        invalid_persistence,
        authorization_failed,
        serialization_failed_persistence,
        conflict,
        io_failed,
        durability_unconfirmed,
        cleanup_warning,
    ):
        rendered = str(result)
        assert "private caller detail" not in rendered
        assert str(tmp_path) not in rendered
        assert ".run-ledger.tmp-" not in rendered
        assert "private serialization detail" not in rendered
        assert "private os detail" not in rendered
        assert "private durability detail" not in rendered
        assert "private cleanup detail" not in rendered
        assert "errno" not in rendered


def test_supported_capability_catalog_is_exact():
    assert sut.REQUIRED_CAPABILITIES == REQUIRED_CAPABILITIES
    assert len(REQUIRED_CAPABILITIES) == 19


def test_root_slash_is_opened_as_the_initial_capability(monkeypatch, tmp_path):
    virtual_fds = {
        "root": 101,
        "runs": 102,
        "by_entry_id": 103,
        "entry": 104,
        "temp": 105,
        "final_before_fsync": 106,
        "final_after_fsync": 107,
    }
    directory_fds = {
        virtual_fds["root"],
        virtual_fds["runs"],
        virtual_fds["by_entry_id"],
        virtual_fds["entry"],
    }
    regular_fds = {
        virtual_fds["temp"],
        virtual_fds["final_before_fsync"],
        virtual_fds["final_after_fsync"],
    }
    open_events = []
    other_events = []
    entry_directory_created = {"value": False}
    final_linked = {"value": False}
    temp_present = {"value": False}
    serialized = bytearray()
    final_open_count = {"value": 0}
    read_offsets = {}
    temp_name = ".run-ledger.tmp-11111111111111111111111111111111"
    entry_directory = "sha256-" + ENTRY_ID_DIGEST

    def virtual_open(path, *args, **kwargs):
        dir_fd = kwargs.get("dir_fd")
        descriptor = None
        if path == "/":
            assert dir_fd is None
            descriptor = virtual_fds["root"]
        elif path == "runs":
            assert dir_fd == virtual_fds["root"]
            descriptor = virtual_fds["runs"]
        elif path == "by-entry-id":
            assert dir_fd == virtual_fds["runs"]
            descriptor = virtual_fds["by_entry_id"]
        elif path == entry_directory:
            assert dir_fd == virtual_fds["by_entry_id"]
            if not entry_directory_created["value"]:
                open_events.append((path, args, dict(kwargs), None))
                raise FileNotFoundError(errno.ENOENT, "virtual missing entry")
            descriptor = virtual_fds["entry"]
        elif path == temp_name:
            assert dir_fd == virtual_fds["entry"]
            temp_present["value"] = True
            descriptor = virtual_fds["temp"]
        elif path == "run-ledger.yaml":
            assert dir_fd == virtual_fds["entry"]
            if not final_linked["value"]:
                open_events.append((path, args, dict(kwargs), None))
                raise FileNotFoundError(errno.ENOENT, "virtual missing final")
            final_open_count["value"] += 1
            descriptor = (
                virtual_fds["final_before_fsync"]
                if final_open_count["value"] == 1
                else virtual_fds["final_after_fsync"]
            )
        else:
            raise AssertionError("unexpected virtual open path")
        open_events.append((path, args, dict(kwargs), descriptor))
        return descriptor

    def virtual_fstat(fd):
        assert fd in directory_fds | regular_fds
        if fd in directory_fds:
            return types.SimpleNamespace(
                st_dev=1,
                st_ino=fd,
                st_mode=stat.S_IFDIR | 0o700,
                st_size=0,
                st_mtime_ns=1,
            )
        return types.SimpleNamespace(
            st_dev=1,
            st_ino=500,
            st_mode=stat.S_IFREG | 0o600,
            st_size=len(serialized),
            st_mtime_ns=1,
        )

    def virtual_mkdir(path, mode=0o777, *, dir_fd=None):
        assert path == entry_directory
        assert mode == 0o700
        assert dir_fd == virtual_fds["by_entry_id"]
        assert entry_directory_created["value"] is False
        entry_directory_created["value"] = True
        other_events.append(("mkdir", path, dir_fd))

    def virtual_write(fd, data):
        assert fd == virtual_fds["temp"]
        assert type(data) is bytes
        serialized.extend(data)
        other_events.append(("write", fd, len(data)))
        return len(data)

    def virtual_fsync(fd):
        assert fd in directory_fds | regular_fds
        other_events.append(("fsync", fd))

    def virtual_link(
        source,
        destination,
        *,
        src_dir_fd=None,
        dst_dir_fd=None,
        follow_symlinks=True,
    ):
        assert source == temp_name
        assert destination == "run-ledger.yaml"
        assert src_dir_fd == dst_dir_fd == virtual_fds["entry"]
        assert follow_symlinks is False
        assert temp_present["value"] is True
        final_linked["value"] = True
        other_events.append(("link", source, destination))

    def virtual_unlink(path, *, dir_fd=None):
        assert path == temp_name
        assert dir_fd == virtual_fds["entry"]
        assert final_linked["value"] is True
        temp_present["value"] = False
        other_events.append(("unlink", path, dir_fd))

    def virtual_close(fd):
        assert fd in directory_fds | regular_fds
        other_events.append(("close", fd))

    def virtual_read(fd, size):
        assert fd in {
            virtual_fds["final_before_fsync"],
            virtual_fds["final_after_fsync"],
        }
        assert 0 < size <= 65536
        offset = read_offsets.get(fd, 0)
        chunk = bytes(serialized[offset:offset + size])
        read_offsets[fd] = offset + len(chunk)
        other_events.append(("read", fd, size))
        return chunk

    monkeypatch.setattr(sut, "_os_open", virtual_open)
    monkeypatch.setattr(sut, "_os_fstat", virtual_fstat)
    monkeypatch.setattr(sut, "_os_mkdir", virtual_mkdir)
    monkeypatch.setattr(sut, "_os_write", virtual_write)
    monkeypatch.setattr(sut, "_os_fsync", virtual_fsync)
    monkeypatch.setattr(sut, "_os_link", virtual_link)
    monkeypatch.setattr(sut, "_os_unlink", virtual_unlink)
    monkeypatch.setattr(sut, "_os_close", virtual_close)
    monkeypatch.setattr(sut, "_os_read", virtual_read)
    monkeypatch.setattr(sut, "_new_temp_name", lambda: temp_name)

    result = sut.persist_run_ledger_entry(
        run_ledger_entry_assembly=_success_envelope(),
        authorized_ops_root="/",
    )

    assert open_events
    assert open_events[0][0] == "/"
    assert open_events[0][2].get("dir_fd") is None
    assert any(
        path == "runs" and kwargs.get("dir_fd") == virtual_fds["root"]
        for path, _args, kwargs, _fd in open_events
    )
    assert any(
        path == "by-entry-id"
        and kwargs.get("dir_fd") == virtual_fds["runs"]
        for path, _args, kwargs, _fd in open_events
    )
    assert all(
        path == "/" or not str(path).startswith("/")
        for path, _args, _kwargs, _fd in open_events
    )
    assert all(path != "/runs" for path, _args, _kwargs, _fd in open_events)
    assert all(
        fd is None or fd in directory_fds | regular_fds
        for _path, _args, _kwargs, fd in open_events
    )
    assert entry_directory_created["value"] is True
    assert final_linked["value"] is True
    assert temp_present["value"] is False
    assert len(serialized) == len(GOLDEN_BYTES)
    assert bytes(serialized) == GOLDEN_BYTES
    assert ("link", temp_name, "run-ledger.yaml") in other_events
    assert result["persistence_status"] == "WRITTEN"
    assert result["run_ledger_persisted"] is True
    assert tuple(tmp_path.iterdir()) == ()

    raced_fds = {
        "root": 201,
        "runs": 202,
        "by_entry_id": 203,
        "entry": 204,
    }
    raced_directory_fds = set(raced_fds.values())
    raced_events = []
    raced_entry_open_count = {"value": 0}
    raced_entry_directory = "sha256-" + ENTRY_ID_DIGEST

    def raced_open(path, *args, **kwargs):
        dir_fd = kwargs.get("dir_fd")
        if path == "/":
            assert dir_fd is None
            descriptor = raced_fds["root"]
        elif path == "runs":
            assert dir_fd == raced_fds["root"]
            descriptor = raced_fds["runs"]
        elif path == "by-entry-id":
            assert dir_fd == raced_fds["runs"]
            descriptor = raced_fds["by_entry_id"]
        elif path == raced_entry_directory:
            assert dir_fd == raced_fds["by_entry_id"]
            raced_entry_open_count["value"] += 1
            if raced_entry_open_count["value"] == 1:
                raced_events.append(("entry-open-enoent", dir_fd))
                raise FileNotFoundError(errno.ENOENT, "raced entry absent")
            raced_events.append(("entry-reopen", dir_fd))
            descriptor = raced_fds["entry"]
        else:
            raced_events.append(("forbidden-open", path, dir_fd))
            raise AssertionError("later persistence open reached")
        raced_events.append(("open", path, descriptor))
        return descriptor

    def raced_fstat(fd):
        assert fd in raced_directory_fds
        raced_events.append(("fstat-directory", fd))
        return types.SimpleNamespace(
            st_dev=2,
            st_ino=fd,
            st_mode=stat.S_IFDIR | 0o700,
            st_size=0,
            st_mtime_ns=2,
        )

    def raced_mkdir(path, mode=0o777, *, dir_fd=None):
        assert path == raced_entry_directory
        assert mode == 0o700
        assert dir_fd == raced_fds["by_entry_id"]
        raced_events.append(("mkdir-eexist", path, dir_fd))
        raise FileExistsError(errno.EEXIST, "raced creator won")

    def raced_fsync(fd):
        raced_events.append(("fsync", fd))
        if fd == raced_fds["by_entry_id"]:
            raise OSError(errno.EIO, "raced parent fsync detail")
        raise AssertionError("unexpected fsync target")

    def raced_close(fd):
        assert fd in raced_directory_fds
        raced_events.append(("close", fd))

    def forbidden_temp_name():
        raced_events.append(("forbidden-temp-name",))
        return ".run-ledger.tmp-22222222222222222222222222222222"

    def forbidden_write(*args, **kwargs):
        raced_events.append(("forbidden-write", args, kwargs))
        raise AssertionError("write reached")

    def forbidden_link(*args, **kwargs):
        raced_events.append(("forbidden-link", args, kwargs))
        raise AssertionError("link reached")

    with monkeypatch.context() as patcher:
        patcher.setattr(sut, "_os_open", raced_open)
        patcher.setattr(sut, "_os_fstat", raced_fstat)
        patcher.setattr(sut, "_os_mkdir", raced_mkdir)
        patcher.setattr(sut, "_os_fsync", raced_fsync)
        patcher.setattr(sut, "_os_close", raced_close)
        patcher.setattr(sut, "_os_write", forbidden_write)
        patcher.setattr(sut, "_os_link", forbidden_link)
        patcher.setattr(sut, "_new_temp_name", forbidden_temp_name)
        raced_result = sut.persist_run_ledger_entry(
            run_ledger_entry_assembly=_success_envelope(),
            authorized_ops_root="/",
        )

    assert raced_entry_open_count["value"] == 2
    assert ("mkdir-eexist", raced_entry_directory, raced_fds["by_entry_id"]) in raced_events
    assert ("entry-reopen", raced_fds["by_entry_id"]) in raced_events
    assert ("fstat-directory", raced_fds["entry"]) in raced_events
    assert ("fsync", raced_fds["by_entry_id"]) in raced_events
    assert not any(event[0].startswith("forbidden") for event in raced_events)
    assert raced_result["run_ledger_persisted"] is False
    assert raced_result["persistence_status"] == "IO_FAILED"
    assert raced_result["reason_code"] == "PRE_FINALIZATION_IO_FAILED"
    assert raced_result["persistence_evidence"] == {}
    assert raced_result["persistence_violations"] == (
        "PRE_FINALIZATION_IO_FAILED",
    )
    assert raced_result["missing_or_invalid_fields"] == (
        "persistence_io",
    )
    assert raced_result["diagnostic_records"] == ({
        "reason_code": "PRE_FINALIZATION_IO_FAILED",
        "field": "persistence_io",
    },)
    raced_rendered = str(raced_result)
    assert "raced parent fsync detail" not in raced_rendered
    assert "raced creator won" not in raced_rendered
    assert "errno" not in raced_rendered
    assert ".run-ledger.tmp-" not in raced_rendered
    assert tuple(tmp_path.iterdir()) == ()


def test_canonical_absolute_root_is_opened_component_by_component(monkeypatch, tmp_path):
    events = []
    _spy(monkeypatch, "_os_open", events)
    root = _ops_root(tmp_path)
    result = _persist(tmp_path, root=root)
    _assert_non_invalid(result)
    opened = tuple(event[1][0] for event in events)
    assert len(opened) >= 1
    assert opened[0] == "/"
    assert str(root) not in opened[1:]
    assert "runs" in opened and "by-entry-id" in opened


def test_duplicate_root_separators_are_rejected(monkeypatch, tmp_path):
    calls = []
    _spy(monkeypatch, "_os_open", calls)
    root = str(tmp_path) + "//ops-root"
    result = sut.persist_run_ledger_entry(
        run_ledger_entry_assembly=_success_envelope(),
        authorized_ops_root=root,
    )
    assert result["persistence_status"] == "AUTHORIZATION_FAILED"
    assert result["reason_code"] == "DESTINATION_ROOT_INVALID"
    assert calls == []


def test_trailing_root_separator_is_rejected_except_for_root(monkeypatch, tmp_path):
    calls = []
    _spy(monkeypatch, "_os_open", calls)
    result = sut.persist_run_ledger_entry(
        run_ledger_entry_assembly=_success_envelope(),
        authorized_ops_root=str(tmp_path) + "/",
    )
    assert result["persistence_status"] == "AUTHORIZATION_FAILED"
    assert calls == []
    assert os.path.normpath("/") == "/"


def test_dot_and_dotdot_root_components_are_rejected(monkeypatch, tmp_path):
    for suffix in ("/./ops", "/../ops"):
        calls = []
        _spy(monkeypatch, "_os_open", calls)
        result = sut.persist_run_ledger_entry(
            run_ledger_entry_assembly=_success_envelope(),
            authorized_ops_root=str(tmp_path) + suffix,
        )
        assert result["persistence_status"] == "AUTHORIZATION_FAILED"
        assert result["reason_code"] == "DESTINATION_ROOT_INVALID"
        assert calls == []


def test_final_root_symlink_is_rejected(tmp_path):
    real_root = _ops_root(tmp_path)
    root_marker = real_root / "caller-root-marker.bin"
    root_marker_bytes = b"caller root target must remain unchanged"
    root_marker.write_bytes(root_marker_bytes)
    root_target_entries_before = tuple(sorted(
        path.relative_to(real_root)
        for path in real_root.rglob("*")
    ))
    root_target_stat_before = real_root.stat()
    link = tmp_path / "ops-link"
    link.symlink_to(real_root, target_is_directory=True)
    result = sut.persist_run_ledger_entry(
        run_ledger_entry_assembly=_success_envelope(),
        authorized_ops_root=str(link),
    )
    assert tuple(result) == PERSISTENCE_RESULT_KEYS
    assert result["run_ledger_persisted"] is False
    assert result["persistence_status"] == "AUTHORIZATION_FAILED"
    assert result["reason_code"] == "DESTINATION_PATH_UNSAFE"
    assert tuple(result["source"]) == SOURCE_KEYS
    assert result["source"] == SOURCE
    assert result["persistence_evidence"] == {}
    assert result["persistence_violations"] == (
        "DESTINATION_PATH_UNSAFE",
    )
    assert result["missing_or_invalid_fields"] == (
        "authorized_destination",
    )
    assert result["diagnostic_records"] == ({
        "reason_code": "DESTINATION_PATH_UNSAFE",
        "field": "authorized_destination",
    },)
    assert link.exists()
    assert link.is_symlink()
    assert real_root.is_dir()
    assert root_marker.read_bytes() == root_marker_bytes
    assert tuple(sorted(
        path.relative_to(real_root)
        for path in real_root.rglob("*")
    )) == root_target_entries_before
    root_target_stat_after = real_root.stat()
    assert (
        root_target_stat_after.st_dev,
        root_target_stat_after.st_ino,
        root_target_stat_after.st_mode,
        root_target_stat_after.st_size,
        root_target_stat_after.st_mtime_ns,
    ) == (
        root_target_stat_before.st_dev,
        root_target_stat_before.st_ino,
        root_target_stat_before.st_mode,
        root_target_stat_before.st_size,
        root_target_stat_before.st_mtime_ns,
    )
    assert tuple((real_root / "runs" / "by-entry-id").iterdir()) == ()
    assert tuple(real_root.rglob(".run-ledger.tmp-*")) == ()
    assert tuple(real_root.rglob("run-ledger.yaml")) == ()
    root_rendered = str(result)
    assert str(link) not in root_rendered
    assert str(real_root) not in root_rendered
    assert "Too many levels of symbolic links" not in root_rendered
    assert "ELOOP" not in root_rendered
    assert "OSError" not in root_rendered
    assert "FileNotFoundError" not in root_rendered
    assert "errno" not in root_rendered
    assert ".run-ledger.tmp-" not in root_rendered
    assert "public_url" not in result
    assert "publish_authorization" not in result

    def iter_result_keys_and_leaf_values(value):
        if type(value) is dict:
            for key, nested_value in value.items():
                yield key
                yield from iter_result_keys_and_leaf_values(nested_value)
            return

        if type(value) in (list, tuple):
            for item in value:
                yield from iter_result_keys_and_leaf_values(item)
            return

        yield value

    root_tokens = tuple(iter_result_keys_and_leaf_values(result))
    assert "PASS_PUBLISHED" not in root_tokens
    assert "P2D45_P_PASS_PUBLISHED_FORBIDDEN" in root_tokens

    runs_root = tmp_path / "runs-symlink-root"
    runs_root.mkdir()
    runs_target = tmp_path / "runs-symlink-target"
    runs_target.mkdir()
    (runs_root / "runs").symlink_to(runs_target, target_is_directory=True)
    runs_before = tuple(runs_target.iterdir())
    runs_result = sut.persist_run_ledger_entry(
        run_ledger_entry_assembly=_success_envelope(),
        authorized_ops_root=str(runs_root),
    )
    assert runs_result["run_ledger_persisted"] is False
    assert runs_result["persistence_status"] == "AUTHORIZATION_FAILED"
    assert runs_result["reason_code"] == "DESTINATION_PATH_UNSAFE"
    assert runs_result["persistence_evidence"] == {}
    assert runs_result["persistence_violations"] == (
        "DESTINATION_PATH_UNSAFE",
    )
    assert runs_result["missing_or_invalid_fields"] == (
        "authorized_destination",
    )
    assert runs_result["diagnostic_records"] == ({
        "reason_code": "DESTINATION_PATH_UNSAFE",
        "field": "authorized_destination",
    },)
    assert tuple(runs_target.iterdir()) == runs_before
    assert (runs_root / "runs").is_symlink()

    by_entry_root = tmp_path / "by-entry-id-symlink-root"
    (by_entry_root / "runs").mkdir(parents=True)
    by_entry_target = tmp_path / "by-entry-id-symlink-target"
    by_entry_target.mkdir()
    (by_entry_root / "runs" / "by-entry-id").symlink_to(
        by_entry_target,
        target_is_directory=True,
    )
    by_entry_before = tuple(by_entry_target.iterdir())
    by_entry_result = sut.persist_run_ledger_entry(
        run_ledger_entry_assembly=_success_envelope(),
        authorized_ops_root=str(by_entry_root),
    )
    assert by_entry_result["run_ledger_persisted"] is False
    assert by_entry_result["persistence_status"] == "AUTHORIZATION_FAILED"
    assert by_entry_result["reason_code"] == "DESTINATION_PATH_UNSAFE"
    assert by_entry_result["persistence_evidence"] == {}
    assert by_entry_result["persistence_violations"] == (
        "DESTINATION_PATH_UNSAFE",
    )
    assert by_entry_result["missing_or_invalid_fields"] == (
        "authorized_destination",
    )
    assert by_entry_result["diagnostic_records"] == ({
        "reason_code": "DESTINATION_PATH_UNSAFE",
        "field": "authorized_destination",
    },)
    assert tuple(by_entry_target.iterdir()) == by_entry_before
    assert (by_entry_root / "runs" / "by-entry-id").is_symlink()

    for symlink_result, symlink_root in (
        (runs_result, runs_root),
        (by_entry_result, by_entry_root),
    ):
        rendered = str(symlink_result)
        assert str(symlink_root) not in rendered
        assert ".run-ledger.tmp-" not in rendered
        assert "errno" not in rendered


def test_ancestor_root_symlink_is_rejected(tmp_path):
    real_parent = tmp_path / "real-parent"
    root = real_parent / "ops-root"
    (root / "runs" / "by-entry-id").mkdir(parents=True)
    link_parent = tmp_path / "linked-parent"
    link_parent.symlink_to(real_parent, target_is_directory=True)
    result = sut.persist_run_ledger_entry(
        run_ledger_entry_assembly=_success_envelope(),
        authorized_ops_root=str(link_parent / "ops-root"),
    )
    assert result["persistence_status"] == "AUTHORIZATION_FAILED"
    assert result["reason_code"] == "DESTINATION_PATH_UNSAFE"


def test_missing_root_component_is_authorization_failure(monkeypatch, tmp_path):
    calls = []
    _spy(monkeypatch, "_os_open", calls)
    result = sut.persist_run_ledger_entry(
        run_ledger_entry_assembly=_success_envelope(),
        authorized_ops_root=str(tmp_path / "missing"),
    )
    assert result["persistence_status"] == "AUTHORIZATION_FAILED"
    assert result["reason_code"] == "DESTINATION_ROOT_INVALID"
    assert calls

    mkdir_events = []
    original_mkdir = sut._os_mkdir

    def track_mkdir(*args, **kwargs):
        mkdir_events.append((args, kwargs))
        return original_mkdir(*args, **kwargs)

    missing_runs_root = tmp_path / "missing-runs-root"
    missing_runs_root.mkdir()
    missing_runs_start = len(calls)
    with monkeypatch.context() as patcher:
        patcher.setattr(sut, "_os_mkdir", track_mkdir)
        missing_runs_result = sut.persist_run_ledger_entry(
            run_ledger_entry_assembly=_success_envelope(),
            authorized_ops_root=str(missing_runs_root),
        )
    missing_runs_calls = calls[missing_runs_start:]

    missing_by_entry_root = tmp_path / "missing-by-entry-id-root"
    (missing_by_entry_root / "runs").mkdir(parents=True)
    missing_by_entry_start = len(calls)
    with monkeypatch.context() as patcher:
        patcher.setattr(sut, "_os_mkdir", track_mkdir)
        missing_by_entry_result = sut.persist_run_ledger_entry(
            run_ledger_entry_assembly=_success_envelope(),
            authorized_ops_root=str(missing_by_entry_root),
        )
    missing_by_entry_calls = calls[missing_by_entry_start:]

    assert any(event[1][0] == "runs" for event in missing_runs_calls)
    assert missing_runs_result["run_ledger_persisted"] is False
    assert missing_runs_result["persistence_status"] == "AUTHORIZATION_FAILED"
    assert missing_runs_result["reason_code"] == "DESTINATION_PATH_UNSAFE"
    assert missing_runs_result["persistence_evidence"] == {}
    assert missing_runs_result["persistence_violations"] == (
        "DESTINATION_PATH_UNSAFE",
    )
    assert missing_runs_result["missing_or_invalid_fields"] == (
        "authorized_destination",
    )
    assert missing_runs_result["diagnostic_records"] == ({
        "reason_code": "DESTINATION_PATH_UNSAFE",
        "field": "authorized_destination",
    },)
    assert not (missing_runs_root / "runs").exists()

    assert any(
        event[1][0] == "by-entry-id" for event in missing_by_entry_calls
    )
    assert missing_by_entry_result["run_ledger_persisted"] is False
    assert missing_by_entry_result["persistence_status"] == (
        "AUTHORIZATION_FAILED"
    )
    assert missing_by_entry_result["reason_code"] == "DESTINATION_PATH_UNSAFE"
    assert missing_by_entry_result["persistence_evidence"] == {}
    assert missing_by_entry_result["persistence_violations"] == (
        "DESTINATION_PATH_UNSAFE",
    )
    assert missing_by_entry_result["missing_or_invalid_fields"] == (
        "authorized_destination",
    )
    assert missing_by_entry_result["diagnostic_records"] == ({
        "reason_code": "DESTINATION_PATH_UNSAFE",
        "field": "authorized_destination",
    },)
    assert not (missing_by_entry_root / "runs" / "by-entry-id").exists()
    assert mkdir_events == []
    assert result["missing_or_invalid_fields"] == ("authorized_ops_root",)
    assert result["diagnostic_records"] == ({
        "reason_code": "DESTINATION_ROOT_INVALID",
        "field": "authorized_ops_root",
    },)
    for classified_result, classified_root in (
        (result, tmp_path / "missing"),
        (missing_runs_result, missing_runs_root),
        (missing_by_entry_result, missing_by_entry_root),
    ):
        rendered = str(classified_result)
        assert str(classified_root) not in rendered
        assert ".run-ledger.tmp-" not in rendered
        assert "errno" not in rendered


def test_non_directory_root_component_is_authorization_failure(monkeypatch, tmp_path):
    root_file = tmp_path / "root-file"
    root_file.write_bytes(b"not a directory")
    fstats = []
    _spy(monkeypatch, "_os_fstat", fstats)
    result = sut.persist_run_ledger_entry(
        run_ledger_entry_assembly=_success_envelope(),
        authorized_ops_root=str(root_file),
    )
    assert result["persistence_status"] == "AUTHORIZATION_FAILED"
    assert result["reason_code"] == "DESTINATION_ROOT_INVALID"
    assert fstats or result["reason_code"] == "DESTINATION_ROOT_INVALID"

    runs_file_root = tmp_path / "runs-file-root"
    runs_file_root.mkdir()
    runs_file = runs_file_root / "runs"
    runs_file.write_bytes(b"internal runs is not a directory")
    runs_result = sut.persist_run_ledger_entry(
        run_ledger_entry_assembly=_success_envelope(),
        authorized_ops_root=str(runs_file_root),
    )

    by_entry_file_root = tmp_path / "by-entry-id-file-root"
    (by_entry_file_root / "runs").mkdir(parents=True)
    by_entry_file = by_entry_file_root / "runs" / "by-entry-id"
    by_entry_file.write_bytes(b"internal by-entry-id is not a directory")
    by_entry_result = sut.persist_run_ledger_entry(
        run_ledger_entry_assembly=_success_envelope(),
        authorized_ops_root=str(by_entry_file_root),
    )

    assert runs_result["run_ledger_persisted"] is False
    assert runs_result["persistence_status"] == "AUTHORIZATION_FAILED"
    assert runs_result["reason_code"] == "DESTINATION_PATH_UNSAFE"
    assert runs_result["persistence_evidence"] == {}
    assert runs_result["persistence_violations"] == (
        "DESTINATION_PATH_UNSAFE",
    )
    assert runs_result["missing_or_invalid_fields"] == (
        "authorized_destination",
    )
    assert runs_result["diagnostic_records"] == ({
        "reason_code": "DESTINATION_PATH_UNSAFE",
        "field": "authorized_destination",
    },)
    assert runs_file.read_bytes() == b"internal runs is not a directory"

    assert by_entry_result["run_ledger_persisted"] is False
    assert by_entry_result["persistence_status"] == "AUTHORIZATION_FAILED"
    assert by_entry_result["reason_code"] == "DESTINATION_PATH_UNSAFE"
    assert by_entry_result["persistence_evidence"] == {}
    assert by_entry_result["persistence_violations"] == (
        "DESTINATION_PATH_UNSAFE",
    )
    assert by_entry_result["missing_or_invalid_fields"] == (
        "authorized_destination",
    )
    assert by_entry_result["diagnostic_records"] == ({
        "reason_code": "DESTINATION_PATH_UNSAFE",
        "field": "authorized_destination",
    },)
    assert by_entry_file.read_bytes() == (
        b"internal by-entry-id is not a directory"
    )

    assert result["missing_or_invalid_fields"] == ("authorized_ops_root",)
    assert result["diagnostic_records"] == ({
        "reason_code": "DESTINATION_ROOT_INVALID",
        "field": "authorized_ops_root",
    },)
    for classified_result, classified_root in (
        (result, root_file),
        (runs_result, runs_file_root),
        (by_entry_result, by_entry_file_root),
    ):
        rendered = str(classified_result)
        assert str(classified_root) not in rendered
        assert ".run-ledger.tmp-" not in rendered
        assert "errno" not in rendered


def test_root_permission_failure_is_safe_io_failure(monkeypatch, tmp_path):
    reached = []

    def fail_open(*args, **kwargs):
        reached.append((args, kwargs))
        raise PermissionError(errno.EACCES, "private root detail")

    monkeypatch.setattr(sut, "_os_open", fail_open)
    result = _persist(tmp_path)
    assert reached
    assert result["persistence_status"] == "IO_FAILED"
    assert result["reason_code"] == "PRE_FINALIZATION_IO_FAILED"
    assert "private root detail" not in str(result)


def test_component_replacement_after_open_cannot_redirect_descriptor(monkeypatch, tmp_path):
    root = _ops_root(tmp_path)
    events = []
    original = sut._os_open

    def replacing_open(path, *args, **kwargs):
        descriptor = original(path, *args, **kwargs)
        events.append(path)
        if path == "ops-root":
            replacement = tmp_path / "replacement"
            replacement.mkdir(exist_ok=True)
            moved = tmp_path / "opened-root"
            root.rename(moved)
            replacement.rename(root)
        return descriptor

    monkeypatch.setattr(sut, "_os_open", replacing_open)
    result = _persist(tmp_path, root=root)
    assert "ops-root" in events
    assert result["persistence_status"] in ("WRITTEN", "PERSISTED_CLEANUP_WARNING")


def test_injected_temp_name_is_used_exactly_once(monkeypatch, tmp_path):
    name = ".run-ledger.tmp-11111111111111111111111111111111"
    generated = []
    open_events = []
    creation_events = []
    verifier_events = []
    lifecycle_events = []
    link_sources = []
    unlink_targets = []

    def new_name():
        generated.append(name)
        return name

    original_open = sut._os_open
    original_link = sut._os_link
    original_unlink = sut._os_unlink

    def track_open(path, flags, *args, **kwargs):
        if path == name:
            creation = (
                flags & os.O_CREAT
                and flags & os.O_EXCL
                and flags & os.O_NOFOLLOW
            )
            verifier = (
                not flags & os.O_CREAT
                and not flags & os.O_EXCL
                and flags & os.O_NOFOLLOW
                and "dir_fd" in kwargs
            )
            assert creation or verifier
            event = ("creation" if creation else "verifier", path)
            open_events.append(event)
            lifecycle_events.append(event)
            if creation:
                creation_events.append(event)
            else:
                verifier_events.append(event)
        return original_open(path, flags, *args, **kwargs)

    def track_link(source, *args, **kwargs):
        link_sources.append(source)
        lifecycle_events.append(("link", source))
        return original_link(source, *args, **kwargs)

    def track_unlink(target, *args, **kwargs):
        unlink_targets.append(target)
        lifecycle_events.append(("unlink", target))
        return original_unlink(target, *args, **kwargs)

    monkeypatch.setattr(sut, "_new_temp_name", new_name)
    monkeypatch.setattr(sut, "_os_open", track_open)
    monkeypatch.setattr(sut, "_os_link", track_link)
    monkeypatch.setattr(sut, "_os_unlink", track_unlink)
    result = _persist(tmp_path)
    assert len(generated) == 1
    assert len(set(generated)) == 1
    assert generated == [name]
    assert len(creation_events) == 1
    assert len(verifier_events) == 1
    assert creation_events == [("creation", name)]
    assert verifier_events == [("verifier", name)]
    assert open_events == [("creation", name), ("verifier", name)]
    assert link_sources == [name]
    assert unlink_targets == [name]
    assert lifecycle_events == [
        ("creation", name),
        ("link", name),
        ("verifier", name),
        ("unlink", name),
    ]
    assert "persistence_status" in result
    assert result["persistence_status"] == "WRITTEN"


def test_temp_name_collision_then_success_retries_with_new_name(monkeypatch, tmp_path):
    collision_name = ".run-ledger.tmp-11111111111111111111111111111111"
    successful_name = ".run-ledger.tmp-22222222222222222222222222222222"
    names = (collision_name, successful_name)
    generated = []
    open_events = []
    creation_events = []
    verifier_events = []
    lifecycle_events = []
    link_sources = []
    unlink_targets = []
    cleanup_fsyncs = []
    unlink_completed = False
    original_open = sut._os_open
    original_link = sut._os_link
    original_unlink = sut._os_unlink
    original_fsync = sut._os_fsync

    def new_name():
        assert len(generated) < len(names)
        name = names[len(generated)]
        generated.append(name)
        return name

    def injected_open(path, flags, *args, **kwargs):
        if path in names:
            creation = (
                flags & os.O_CREAT
                and flags & os.O_EXCL
                and flags & os.O_NOFOLLOW
            )
            verifier = (
                not flags & os.O_CREAT
                and not flags & os.O_EXCL
                and flags & os.O_NOFOLLOW
                and "dir_fd" in kwargs
            )
            assert creation or verifier
            role = "creation" if creation else "verifier"
            event = (role, path)
            open_events.append(event)
            lifecycle_events.append(event)
            if creation:
                creation_events.append(event)
            else:
                verifier_events.append(event)
            if role == "creation" and path == collision_name:
                raise FileExistsError(errno.EEXIST, "collision")
        return original_open(path, flags, *args, **kwargs)

    def track_link(source, *args, **kwargs):
        link_sources.append(source)
        lifecycle_events.append(("link", source))
        return original_link(source, *args, **kwargs)

    def track_unlink(target, *args, **kwargs):
        nonlocal unlink_completed
        result = original_unlink(target, *args, **kwargs)
        unlink_targets.append(target)
        lifecycle_events.append(("unlink", target))
        unlink_completed = True
        return result

    def track_fsync(fd):
        result = original_fsync(fd)
        if unlink_completed:
            cleanup_fsyncs.append(fd)
            lifecycle_events.append(("cleanup-fsync", successful_name))
        return result

    monkeypatch.setattr(sut, "_new_temp_name", new_name)
    monkeypatch.setattr(sut, "_os_open", injected_open)
    monkeypatch.setattr(sut, "_os_link", track_link)
    monkeypatch.setattr(sut, "_os_unlink", track_unlink)
    monkeypatch.setattr(sut, "_os_fsync", track_fsync)
    result = _persist(tmp_path)
    assert len(generated) == 2
    assert len(set(generated)) == 2
    assert generated == [collision_name, successful_name]
    assert len(creation_events) == 2
    assert len(verifier_events) == 1
    assert creation_events == [
        ("creation", collision_name),
        ("creation", successful_name),
    ]
    assert verifier_events == [("verifier", successful_name)]
    assert open_events == [
        ("creation", collision_name),
        ("creation", successful_name),
        ("verifier", successful_name),
    ]
    assert link_sources == [successful_name]
    assert collision_name not in link_sources
    assert unlink_targets == [successful_name]
    assert collision_name not in unlink_targets
    assert len(cleanup_fsyncs) == 1
    assert lifecycle_events == [
        ("creation", collision_name),
        ("creation", successful_name),
        ("link", successful_name),
        ("verifier", successful_name),
        ("unlink", successful_name),
        ("cleanup-fsync", successful_name),
    ]
    assert "persistence_status" in result
    assert result["persistence_status"] == "WRITTEN"


def test_temp_name_collision_exhaustion_is_bounded(monkeypatch, tmp_path):
    attempts = []

    def collide(path, *args, **kwargs):
        if str(path).startswith(".run-ledger.tmp-"):
            attempts.append(path)
            raise FileExistsError(errno.EEXIST, "collision")
        return os.open(path, *args, **kwargs)

    monkeypatch.setattr(sut, "_new_temp_name", lambda: ".run-ledger.tmp-11111111111111111111111111111111")
    monkeypatch.setattr(sut, "_os_open", collide)
    result = _persist(tmp_path)
    assert len(attempts) == 8
    assert result["persistence_status"] == "IO_FAILED"
    assert result["reason_code"] == "TEMP_FILE_CREATE_FAILED"


def test_malformed_temp_name_is_rejected_before_open(monkeypatch, tmp_path):
    opens = []
    _spy(monkeypatch, "_os_open", opens)
    monkeypatch.setattr(sut, "_new_temp_name", lambda: "../caller-temp")
    result = _persist(tmp_path)
    assert all(event[1][0] != "../caller-temp" for event in opens)
    assert result["persistence_status"] == "IO_FAILED"
    assert result["reason_code"] == "TEMP_NAME_GENERATION_FAILED"


def test_temp_name_generator_exception_is_suppressed(monkeypatch, tmp_path):
    reached = []

    def fail():
        reached.append(True)
        raise RuntimeError("private generator detail")

    monkeypatch.setattr(sut, "_new_temp_name", fail)
    result = _persist(tmp_path)
    assert reached == [True]
    assert result["reason_code"] == "TEMP_NAME_GENERATION_FAILED"
    assert "private generator detail" not in str(result)


def test_non_collision_temp_create_error_is_fixed_failure(monkeypatch, tmp_path):
    reached = []
    original_open = sut._os_open

    def fail_temp(path, *args, **kwargs):
        if str(path).startswith(".run-ledger.tmp-"):
            reached.append(path)
            raise OSError(errno.EIO, "private create detail")
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(sut, "_new_temp_name", lambda: ".run-ledger.tmp-11111111111111111111111111111111")
    monkeypatch.setattr(sut, "_os_open", fail_temp)
    result = _persist(tmp_path)
    assert len(reached) == 1
    assert result["reason_code"] == "TEMP_FILE_CREATE_FAILED"
    assert "private create detail" not in str(result)


def test_temp_close_failure_before_durability_is_compound_io_failure(monkeypatch, tmp_path):
    name = ".run-ledger.tmp-11111111111111111111111111111111"
    active_roles = {}
    role_assignments = []
    original_temp_fds = []
    verifier_fds = []
    final_fds = []
    close_attempts = []
    events = []
    uses_after_failed_original_close = []
    original_close_failed = False
    unlink_completed = False
    original_open = sut._os_open
    original_close = sut._os_close
    original_fstat = sut._os_fstat
    original_fsync = sut._os_fsync
    original_unlink = sut._os_unlink
    original_write = sut._os_write

    def track_open(path, flags, *args, **kwargs):
        fd = original_open(path, flags, *args, **kwargs)
        if path == name:
            creation = (
                flags & os.O_CREAT
                and flags & os.O_EXCL
                and flags & os.O_NOFOLLOW
            )
            verifier = (
                not flags & os.O_CREAT
                and not flags & os.O_EXCL
                and flags & os.O_NOFOLLOW
                and "dir_fd" in kwargs
            )
            assert creation or verifier
            role = "original-temp" if creation else "verifier"
            active_roles[fd] = role
            if role == "original-temp":
                original_temp_fds.append(fd)
            else:
                verifier_fds.append(fd)
                events.append("verifier-open")
        elif path == "run-ledger.yaml":
            role = "final-inspection"
            active_roles[fd] = role
            final_fds.append(fd)
        else:
            role = "owned-directory"
            active_roles[fd] = role
        role_assignments.append((fd, role))
        return fd

    def track_fstat(fd):
        assert fd in active_roles
        if original_close_failed and fd in original_temp_fds:
            uses_after_failed_original_close.append(("fstat", fd))
        return original_fstat(fd)

    def fail_write(fd, data):
        assert fd in active_roles
        if original_close_failed and fd in original_temp_fds:
            uses_after_failed_original_close.append(("write", fd))
        if active_roles[fd] == "original-temp":
            raise OSError(errno.EIO, "write detail")
        return original_write(fd, data)

    def fail_close(fd):
        nonlocal original_close_failed
        assert fd in active_roles
        role = active_roles[fd]
        close_attempts.append(role)
        if role == "original-temp":
            events.append("original-temp-close-failed")
            original_close_failed = True
            raise OSError(errno.EIO, "close detail")
        result = original_close(fd)
        if role == "verifier":
            events.append("verifier-close")
        if fd in active_roles:
            del active_roles[fd]
        return result

    def track_unlink(target, *args, **kwargs):
        nonlocal unlink_completed
        assert events.count("verifier-close") == 1
        result = original_unlink(target, *args, **kwargs)
        events.append("temp-unlink")
        unlink_completed = True
        return result

    def track_fsync(fd):
        assert fd in active_roles
        if original_close_failed and fd in original_temp_fds:
            uses_after_failed_original_close.append(("fsync", fd))
        result = original_fsync(fd)
        if unlink_completed:
            events.append("cleanup-fsync")
        return result

    monkeypatch.setattr(sut, "_new_temp_name", lambda: name)
    monkeypatch.setattr(sut, "_os_open", track_open)
    monkeypatch.setattr(sut, "_os_fstat", track_fstat)
    monkeypatch.setattr(sut, "_os_fsync", track_fsync)
    monkeypatch.setattr(sut, "_os_unlink", track_unlink)
    monkeypatch.setattr(sut, "_os_write", fail_write)
    monkeypatch.setattr(sut, "_os_close", fail_close)
    result = _persist(tmp_path)
    assert len(original_temp_fds) == 1
    assert len(verifier_fds) == 1
    assert final_fds == []
    owned_assignments = [
        role for _, role in role_assignments if role == "owned-directory"
    ]
    assert close_attempts.count("owned-directory") == len(owned_assignments)
    assert close_attempts.count("verifier") == 1
    assert close_attempts.count("original-temp") == 1
    assert events == [
        "verifier-open",
        "verifier-close",
        "temp-unlink",
        "cleanup-fsync",
        "original-temp-close-failed",
    ]
    assert uses_after_failed_original_close == []
    assert "persistence_status" in result
    assert "reason_code" in result
    assert "persistence_violations" in result
    assert "missing_or_invalid_fields" in result
    assert "diagnostic_records" in result
    assert result["persistence_status"] == "IO_FAILED"
    assert result["reason_code"] == "TEMP_FILE_WRITE_FAILED"
    assert result["persistence_violations"] == (
        "TEMP_FILE_WRITE_FAILED", "TEMP_FILE_CLOSE_FAILED",
    )
    assert result["missing_or_invalid_fields"] == ("persistence_io",)
    assert result["diagnostic_records"] == (
        {"reason_code": "TEMP_FILE_WRITE_FAILED", "field": "persistence_io"},
        {"reason_code": "TEMP_FILE_CLOSE_FAILED", "field": "persistence_io"},
    )
    assert "TEMP_CLEANUP_FAILED" not in result["persistence_violations"]


def test_temp_name_is_never_exposed_after_effectful_failure(monkeypatch, tmp_path):
    name = ".run-ledger.tmp-deaddeaddeaddeaddeaddeaddeaddead"
    reached = []
    original_open = sut._os_open

    def fail_temp(path, *args, **kwargs):
        if path == name:
            reached.append(path)
            raise OSError(errno.EIO, name)
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(sut, "_new_temp_name", lambda: name)
    monkeypatch.setattr(sut, "_os_open", fail_temp)
    result = _persist(tmp_path)
    assert reached == [name]
    assert result["persistence_status"] == "IO_FAILED"
    assert name not in str(result)


def test_temp_descriptor_remains_open_through_hard_link(monkeypatch, tmp_path):
    events = []
    temp_fds = []
    original_open = sut._os_open
    original_link = sut._os_link
    original_close = sut._os_close

    def track_open(path, *args, **kwargs):
        fd = original_open(path, *args, **kwargs)
        if str(path).startswith(".run-ledger.tmp-"):
            temp_fds.append(fd)
            events.append(("temp-open", fd))
        return fd

    def track_link(*args, **kwargs):
        events.append(("link", tuple(temp_fds)))
        return original_link(*args, **kwargs)

    def track_close(fd):
        if fd in temp_fds:
            events.append(("temp-close", fd))
        return original_close(fd)

    monkeypatch.setattr(sut, "_os_open", track_open)
    monkeypatch.setattr(sut, "_os_link", track_link)
    monkeypatch.setattr(sut, "_os_close", track_close)
    result = _persist(tmp_path)
    assert result["persistence_status"] == "WRITTEN"
    assert result["run_ledger_persisted"] is True
    labels = tuple(event[0] for event in events)
    assert "temp-open" in labels
    assert "link" in labels
    assert "temp-close" in labels
    assert labels.index("temp-open") < labels.index("link") < labels.index("temp-close")


def test_temp_first_and_second_fstat_preserve_identity_and_mode(monkeypatch, tmp_path):
    temp_fds = []
    observations = []
    original_open = sut._os_open
    original_fstat = sut._os_fstat

    def track_open(path, *args, **kwargs):
        fd = original_open(path, *args, **kwargs)
        if str(path).startswith(".run-ledger.tmp-"):
            temp_fds.append(fd)
        return fd

    def track_fstat(fd):
        value = original_fstat(fd)
        if fd in temp_fds:
            observations.append((value.st_dev, value.st_ino, value.st_mode, value.st_size))
        return value

    monkeypatch.setattr(sut, "_os_open", track_open)
    monkeypatch.setattr(sut, "_os_fstat", track_fstat)
    result = _persist(tmp_path)
    assert len(observations) >= 2
    assert observations[0][:3] == observations[1][:3]
    assert stat.S_ISREG(observations[0][2])
    assert observations[0][3] == 0 and observations[1][3] == len(GOLDEN_BYTES)
    assert result["persistence_status"] == "WRITTEN"


def test_final_inode_matches_still_open_temp_inode(monkeypatch, tmp_path):
    temp_stats = []
    final_stats = []
    fd_kind = {}
    original_open = sut._os_open
    original_fstat = sut._os_fstat

    def track_open(path, *args, **kwargs):
        fd = original_open(path, *args, **kwargs)
        if str(path).startswith(".run-ledger.tmp-"):
            fd_kind[fd] = "temp"
        elif path == "run-ledger.yaml":
            fd_kind[fd] = "final"
        return fd

    def track_fstat(fd):
        value = original_fstat(fd)
        target = temp_stats if fd_kind.get(fd) == "temp" else final_stats
        if fd in fd_kind:
            target.append((value.st_dev, value.st_ino, value.st_size))
        return value

    monkeypatch.setattr(sut, "_os_open", track_open)
    monkeypatch.setattr(sut, "_os_fstat", track_fstat)
    result = _persist(tmp_path)
    assert temp_stats and final_stats
    assert final_stats[0][:2] == temp_stats[-1][:2]
    assert result["persistence_status"] == "WRITTEN"


def test_final_inode_mismatch_is_durability_unconfirmed(monkeypatch, tmp_path):
    final_fds = []
    original_open = sut._os_open
    original_fstat = sut._os_fstat

    class FakeStat:
        st_dev = 999999
        st_ino = 999999
        st_mode = stat.S_IFREG | 0o600
        st_size = len(GOLDEN_BYTES)
        st_mtime_ns = 1

    def track_open(path, *args, **kwargs):
        fd = original_open(path, *args, **kwargs)
        if path == "run-ledger.yaml":
            final_fds.append(fd)
        return fd

    def mismatch(fd):
        return FakeStat() if fd in final_fds else original_fstat(fd)

    monkeypatch.setattr(sut, "_os_open", track_open)
    monkeypatch.setattr(sut, "_os_fstat", mismatch)
    result = _persist(tmp_path)
    assert final_fds
    assert result["persistence_status"] == "DURABILITY_UNCONFIRMED"
    assert result["reason_code"] == "FINAL_IDENTITY_VERIFICATION_FAILED"
    assert result["persistence_evidence"]["write_disposition"] == "DURABILITY_UNCONFIRMED"


def test_final_size_mismatch_is_durability_unconfirmed(monkeypatch, tmp_path):
    final_fds = []
    original_open = sut._os_open
    original_fstat = sut._os_fstat

    def track_open(path, *args, **kwargs):
        fd = original_open(path, *args, **kwargs)
        if path == "run-ledger.yaml":
            final_fds.append(fd)
        return fd

    def mismatch(fd):
        value = original_fstat(fd)
        if fd not in final_fds:
            return value
        return types.SimpleNamespace(
            st_dev=value.st_dev, st_ino=value.st_ino, st_mode=value.st_mode,
            st_size=value.st_size + 1, st_mtime_ns=value.st_mtime_ns,
        )

    monkeypatch.setattr(sut, "_os_open", track_open)
    monkeypatch.setattr(sut, "_os_fstat", mismatch)
    result = _persist(tmp_path)
    assert final_fds
    assert result["persistence_status"] == "DURABILITY_UNCONFIRMED"
    assert result["reason_code"] == "FINAL_IDENTITY_VERIFICATION_FAILED"


def test_success_close_and_cleanup_order_is_exact(monkeypatch, tmp_path):
    events = []
    active_roles = {}
    role_assignments = []
    final_open_count = 0
    original_temp_fstat_count = 0
    entry_fd = -1
    link_completed = False
    unlink_completed = False
    unlink_targets = []
    original_open = sut._os_open
    original_close = sut._os_close
    original_fstat = sut._os_fstat
    original_write = sut._os_write
    original_link = sut._os_link
    original_unlink = sut._os_unlink
    original_fsync = sut._os_fsync

    def track_open(path, flags, *args, **kwargs):
        nonlocal entry_fd, final_open_count
        fd = original_open(path, flags, *args, **kwargs)
        if str(path).startswith(".run-ledger.tmp-"):
            creation = (
                flags & os.O_CREAT
                and flags & os.O_EXCL
                and flags & os.O_NOFOLLOW
            )
            verifier = (
                not flags & os.O_CREAT
                and not flags & os.O_EXCL
                and flags & os.O_NOFOLLOW
                and "dir_fd" in kwargs
            )
            assert creation or verifier
            if creation:
                role = "original-temp"
                assert "dir_fd" in kwargs
                entry_fd = kwargs["dir_fd"]
                assert entry_fd in active_roles
                active_roles[entry_fd] = "entry-directory"
                events.append("temp-creation")
            else:
                role = "verifier"
                events.append("verifier-open")
        elif path == "run-ledger.yaml":
            final_open_count += 1
            role = "final-before" if final_open_count == 1 else "final-after"
        else:
            role = "owned-directory"
        active_roles[fd] = role
        role_assignments.append((fd, role))
        return fd

    def track_fstat(fd):
        nonlocal original_temp_fstat_count
        assert fd in active_roles
        role = active_roles[fd]
        value = original_fstat(fd)
        if role == "original-temp":
            original_temp_fstat_count += 1
            if original_temp_fstat_count == 1:
                events.append("initial-temp-validation")
            elif original_temp_fstat_count == 2:
                events.append("final-temp-validation")
            else:
                events.append("trusted-temp-fstat")
        elif role == "final-before":
            events.append("first-final-inspection")
        elif role == "final-after":
            events.append("post-fsync-final-revalidation")
        elif role == "verifier":
            events.append("verifier-fstat")
        return value

    def track_write(fd, data):
        assert fd in active_roles
        assert active_roles[fd] == "original-temp"
        events.append("write")
        return original_write(fd, data)

    def track_link(*args, **kwargs):
        nonlocal link_completed
        result = original_link(*args, **kwargs)
        events.append("hard-link")
        link_completed = True
        return result

    def track_close(fd):
        assert fd in active_roles
        role = active_roles[fd]
        result = original_close(fd)
        del active_roles[fd]
        if role in ("final-before", "final-after"):
            events.append("final-close")
        elif role == "verifier":
            events.append("verifier-close")
        elif role == "original-temp":
            events.append("original-temp-close")
        elif role in ("owned-directory", "entry-directory"):
            events.append("owned-close")
        return result

    def track_unlink(target, *args, **kwargs):
        nonlocal unlink_completed
        result = original_unlink(target, *args, **kwargs)
        unlink_targets.append(target)
        events.append("temp-unlink")
        unlink_completed = True
        return result

    def track_fsync(fd):
        assert fd in active_roles
        role = active_roles[fd]
        result = original_fsync(fd)
        if role == "original-temp":
            events.append("temp-fsync")
        elif fd == entry_fd and link_completed and not unlink_completed:
            events.append("entry-durability-fsync")
        elif fd == entry_fd and unlink_completed:
            events.append("cleanup-entry-fsync")
        return result

    monkeypatch.setattr(sut, "_os_open", track_open)
    monkeypatch.setattr(sut, "_os_close", track_close)
    monkeypatch.setattr(sut, "_os_fstat", track_fstat)
    monkeypatch.setattr(sut, "_os_write", track_write)
    monkeypatch.setattr(sut, "_os_link", track_link)
    monkeypatch.setattr(sut, "_os_unlink", track_unlink)
    monkeypatch.setattr(sut, "_os_fsync", track_fsync)
    result = _persist(tmp_path)
    assert "persistence_status" in result
    assert "run_ledger_persisted" in result
    assert result["persistence_status"] == "WRITTEN"
    assert result["run_ledger_persisted"] is True
    expected_lifecycle = (
        "temp-creation",
        "initial-temp-validation",
        "write",
        "temp-fsync",
        "final-temp-validation",
        "hard-link",
        "first-final-inspection",
        "entry-durability-fsync",
        "post-fsync-final-revalidation",
        "final-close",
        "final-close",
        "verifier-open",
        "trusted-temp-fstat",
        "verifier-fstat",
        "verifier-close",
        "temp-unlink",
        "cleanup-entry-fsync",
        "original-temp-close",
    )
    assert tuple(event for event in events if event != "owned-close") == expected_lifecycle
    owned_close_started = False
    for event in events:
        if event == "owned-close":
            owned_close_started = True
        else:
            assert not owned_close_started
    owned_assignments = [
        role for _, role in role_assignments
        if role in ("owned-directory", "entry-directory")
    ]
    assert events.count("owned-close") == len(owned_assignments)
    assert events.count("final-close") == 2
    assert events.count("verifier-open") == 1
    assert events.count("verifier-fstat") == 1
    assert events.count("verifier-close") == 1
    assert events.count("cleanup-entry-fsync") == 1
    assert events.count("original-temp-close") == 1
    assert len(unlink_targets) == 1
    assert unlink_targets[0].startswith(".run-ledger.tmp-")
    assert "run-ledger.yaml" not in unlink_targets
    assert active_roles == {}


def test_temp_close_failure_after_durability_is_cleanup_warning(monkeypatch, tmp_path):
    temp_fds = []
    original_open = sut._os_open
    original_close = sut._os_close

    def track_open(path, *args, **kwargs):
        fd = original_open(path, *args, **kwargs)
        if str(path).startswith(".run-ledger.tmp-"):
            temp_fds.append(fd)
        return fd

    def fail_close(fd):
        if fd in temp_fds:
            raise OSError(errno.EIO, "temp close")
        return original_close(fd)

    monkeypatch.setattr(sut, "_os_open", track_open)
    monkeypatch.setattr(sut, "_os_close", fail_close)
    result = _persist(tmp_path)
    assert temp_fds
    assert result["persistence_status"] == "PERSISTED_CLEANUP_WARNING"
    assert result["run_ledger_persisted"] is True
    assert result["persistence_evidence"]["write_disposition"] == "WRITTEN"

    owned_root = _ops_root(tmp_path / "durable-owned-close-failure")
    owned_target = owned_root / ARTIFACT_RELATIVE_PATH
    owned_directory_fds = []
    fd_usage_events = []
    owned_unlink_paths = []
    selected_owned_fd = {"value": None}
    original_owned_open = sut._os_open
    original_owned_read = sut._os_read
    original_owned_write = sut._os_write
    original_owned_fstat = sut._os_fstat
    original_owned_fsync = sut._os_fsync
    original_owned_mkdir = sut._os_mkdir
    original_owned_link = sut._os_link
    original_owned_close = original_close
    original_owned_unlink = sut._os_unlink

    def fd_refs(*values):
        return tuple(value for value in values if type(value) is int)

    def track_owned_open(path, *args, **kwargs):
        fd_usage_events.append(("open", fd_refs(kwargs.get("dir_fd"))))
        fd = original_owned_open(path, *args, **kwargs)
        if stat.S_ISDIR(os.fstat(fd).st_mode):
            owned_directory_fds.append(fd)
        return fd

    def track_owned_read(fd, size):
        fd_usage_events.append(("read", (fd,)))
        return original_owned_read(fd, size)

    def track_owned_write(fd, data):
        fd_usage_events.append(("write", (fd,)))
        return original_owned_write(fd, data)

    def track_owned_fstat(fd):
        fd_usage_events.append(("fstat", (fd,)))
        return original_owned_fstat(fd)

    def track_owned_fsync(fd):
        fd_usage_events.append(("fsync", (fd,)))
        return original_owned_fsync(fd)

    def track_owned_mkdir(path, mode=0o777, *, dir_fd=None):
        fd_usage_events.append(("mkdir", fd_refs(dir_fd)))
        return original_owned_mkdir(path, mode, dir_fd=dir_fd)

    def track_owned_link(*args, **kwargs):
        fd_usage_events.append((
            "link",
            fd_refs(kwargs.get("src_dir_fd"), kwargs.get("dst_dir_fd")),
        ))
        return original_owned_link(*args, **kwargs)

    def fail_one_owned_close(fd):
        fd_usage_events.append(("close-attempt", (fd,)))
        if fd in owned_directory_fds:
            if selected_owned_fd["value"] is None:
                selected_owned_fd["value"] = fd
                fd_usage_events.append(("close-failed", (fd,)))
                original_owned_close(fd)
                raise OSError(errno.EIO, "private durable owned close detail")
        return original_owned_close(fd)

    def track_owned_unlink(path, *, dir_fd=None):
        fd_usage_events.append(("unlink", fd_refs(dir_fd)))
        owned_unlink_paths.append(path)
        return original_owned_unlink(path, dir_fd=dir_fd)

    with monkeypatch.context() as patcher:
        patcher.setattr(sut, "_os_open", track_owned_open)
        patcher.setattr(sut, "_os_read", track_owned_read)
        patcher.setattr(sut, "_os_write", track_owned_write)
        patcher.setattr(sut, "_os_fstat", track_owned_fstat)
        patcher.setattr(sut, "_os_fsync", track_owned_fsync)
        patcher.setattr(sut, "_os_mkdir", track_owned_mkdir)
        patcher.setattr(sut, "_os_link", track_owned_link)
        patcher.setattr(sut, "_os_close", fail_one_owned_close)
        patcher.setattr(sut, "_os_unlink", track_owned_unlink)
        owned_result = _persist(tmp_path, root=owned_root)

    assert selected_owned_fd["value"] is not None
    owned_attempt_event = (
        "close-attempt",
        (selected_owned_fd["value"],),
    )
    owned_failure_event = (
        "close-failed",
        (selected_owned_fd["value"],),
    )
    assert owned_attempt_event in fd_usage_events
    assert fd_usage_events.count(owned_attempt_event) == 1
    assert owned_failure_event in fd_usage_events
    assert fd_usage_events.count(owned_failure_event) == 1
    owned_failure_index = fd_usage_events.index(owned_failure_event)
    later_fd_usage_events = fd_usage_events[owned_failure_index + 1:]
    assert all(
        selected_owned_fd["value"] not in referenced_fds
        for _operation, referenced_fds in later_fd_usage_events
    )
    assert "run-ledger.yaml" not in owned_unlink_paths
    assert owned_target.read_bytes() == GOLDEN_BYTES
    assert owned_result["run_ledger_persisted"] is True
    assert owned_result["persistence_status"] == "PERSISTED_CLEANUP_WARNING"
    assert owned_result["reason_code"] == "PERSISTED_CLEANUP_WARNING"
    assert owned_result["persistence_violations"] == (
        "PERSISTED_CLEANUP_WARNING",
    )
    assert owned_result["missing_or_invalid_fields"] == (
        "persistence_io",
    )
    assert owned_result["diagnostic_records"] == ({
        "reason_code": "PERSISTED_CLEANUP_WARNING",
        "field": "persistence_io",
    },)
    assert owned_result["persistence_evidence"] == {
        "run_ledger_entry_id": "ledger-entry-001",
        "run_id": "run-001",
        "artifact_relative_path": ARTIFACT_RELATIVE_PATH,
        "serialization_format": "canonical_json_yaml_1_2_subset",
        "content_digest_algorithm": "sha256",
        "content_digest": GOLDEN_DIGEST,
        "write_disposition": "WRITTEN",
    }
    owned_rendered = str(owned_result)
    assert str(owned_root) not in owned_rendered
    assert ".run-ledger.tmp-" not in owned_rendered
    assert "private durable owned close detail" not in owned_rendered
    assert "errno" not in owned_rendered


def test_final_inspection_close_failure_after_durability_is_cleanup_warning(monkeypatch, tmp_path):
    new_write_root = _ops_root(tmp_path / "cleanup-new-write")
    identical_root = _ops_root(tmp_path / "cleanup-existing-identical")
    identical_seed = _persist(tmp_path, root=identical_root)
    assert identical_seed["persistence_status"] == "WRITTEN"

    def run_scenario(*, root, temp_name):
        target = root / ARTIFACT_RELATIVE_PATH
        before_exists = target.exists()
        before_bytes = target.read_bytes() if before_exists else None
        before_stat = target.stat() if before_exists else None
        with monkeypatch.context() as patcher:
            final_fds = []
            final_open_count = []
            close_failure_events = []
            link_events = []
            unlink_events = []
            durability_events = []
            state = {
                "linked": False,
                "existing_file_fsynced": False,
                "final_directory_fsynced": False,
            }
            original_open = sut._os_open
            original_close = sut._os_close
            original_link = sut._os_link
            original_unlink = sut._os_unlink
            original_fsync = sut._os_fsync

            def track_open(path, *args, **kwargs):
                fd = original_open(path, *args, **kwargs)
                if path == "run-ledger.yaml":
                    final_fds.append(fd)
                    final_open_count.append(fd)
                return fd

            def fail_close(fd):
                if fd in final_fds and not close_failure_events:
                    close_failure_events.append((
                        fd,
                        state["final_directory_fsynced"],
                        len(final_open_count),
                    ))
                    raise OSError(
                        errno.EIO,
                        "final inspection close errno=5 private detail",
                    )
                return original_close(fd)

            def track_link(*args, **kwargs):
                value = original_link(*args, **kwargs)
                state["linked"] = True
                link_events.append((args, kwargs))
                return value

            def track_unlink(*args, **kwargs):
                unlink_events.append((args, kwargs))
                return original_unlink(*args, **kwargs)

            def track_fsync(fd):
                value = original_fsync(fd)
                if fd in final_fds:
                    state["existing_file_fsynced"] = True
                    durability_events.append(("final-file-fsync", fd))
                elif stat.S_ISDIR(os.fstat(fd).st_mode) and (
                    state["linked"] or state["existing_file_fsynced"]
                ):
                    state["final_directory_fsynced"] = True
                    durability_events.append(("final-directory-fsync", fd))
                return value

            patcher.setattr(sut, "_os_open", track_open)
            patcher.setattr(sut, "_os_close", fail_close)
            patcher.setattr(sut, "_os_link", track_link)
            patcher.setattr(sut, "_os_unlink", track_unlink)
            patcher.setattr(sut, "_os_fsync", track_fsync)
            patcher.setattr(sut, "_new_temp_name", lambda: temp_name)
            result = _persist(tmp_path, root=root)
        return {
            "result": result,
            "target": target,
            "before_exists": before_exists,
            "before_bytes": before_bytes,
            "before_stat": before_stat,
            "final_fds": tuple(final_fds),
            "final_open_count": tuple(final_open_count),
            "close_failure_events": tuple(close_failure_events),
            "link_events": tuple(link_events),
            "unlink_events": tuple(unlink_events),
            "durability_events": tuple(durability_events),
            "temp_name": temp_name,
            "root": root,
        }

    new_write = run_scenario(
        root=new_write_root,
        temp_name=".run-ledger.tmp-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )
    identical = run_scenario(
        root=identical_root,
        temp_name=".run-ledger.tmp-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    )

    new_result = new_write["result"]
    assert new_write["before_exists"] is False
    assert new_write["before_bytes"] is None
    assert new_write["before_stat"] is None
    assert new_result["persistence_status"] == "PERSISTED_CLEANUP_WARNING"
    assert new_result["run_ledger_persisted"] is True
    assert new_result["reason_code"] == "PERSISTED_CLEANUP_WARNING"
    assert new_result["persistence_violations"] == (
        "PERSISTED_CLEANUP_WARNING",
    )
    assert new_result["missing_or_invalid_fields"] == ("persistence_io",)
    assert new_result["diagnostic_records"] == ({
        "reason_code": "PERSISTED_CLEANUP_WARNING",
        "field": "persistence_io",
    },)
    assert type(new_result["persistence_evidence"]) is dict
    assert tuple(new_result["persistence_evidence"]) == PERSISTENCE_EVIDENCE_KEYS
    assert new_result["persistence_evidence"]["write_disposition"] == "WRITTEN"
    assert new_write["target"].is_file()
    assert new_write["target"].read_bytes() == GOLDEN_BYTES
    assert len(new_write["link_events"]) == 1
    assert all(
        event[0][0] != "run-ledger.yaml"
        for event in new_write["unlink_events"]
    )
    assert new_write["final_fds"]
    assert len(new_write["final_open_count"]) >= 2
    assert len(new_write["close_failure_events"]) == 1
    assert new_write["close_failure_events"][0][1] is True
    assert new_write["close_failure_events"][0][2] >= 2
    assert new_write["durability_events"]
    new_rendered = str(new_result)
    assert str(new_write_root) not in new_rendered
    assert new_write["temp_name"] not in new_rendered
    assert "final inspection close errno=5 private detail" not in new_rendered
    assert "errno" not in new_rendered
    assert "public_url" not in new_result
    assert "notification_result" not in new_result
    assert "transition" not in new_result
    assert "quality_pass" not in new_result
    assert "PASS_PUBLISHED" not in new_result["persistence_evidence"].values()

    identical_result = identical["result"]
    assert identical["before_exists"] is True
    assert identical["before_bytes"] == GOLDEN_BYTES
    assert identical["before_stat"] is not None
    assert identical_result["persistence_status"] == "PERSISTED_CLEANUP_WARNING"
    assert identical_result["run_ledger_persisted"] is True
    assert identical_result["reason_code"] == "PERSISTED_CLEANUP_WARNING"
    assert identical_result["persistence_violations"] == (
        "PERSISTED_CLEANUP_WARNING",
    )
    assert identical_result["missing_or_invalid_fields"] == (
        "persistence_io",
    )
    assert identical_result["diagnostic_records"] == ({
        "reason_code": "PERSISTED_CLEANUP_WARNING",
        "field": "persistence_io",
    },)
    assert type(identical_result["persistence_evidence"]) is dict
    assert tuple(identical_result["persistence_evidence"]) == PERSISTENCE_EVIDENCE_KEYS
    assert identical_result["persistence_evidence"][
        "write_disposition"
    ] == "ALREADY_IDENTICAL"
    assert identical["target"].is_file()
    assert identical["target"].read_bytes() == GOLDEN_BYTES
    after_identical_stat = identical["target"].stat()
    assert after_identical_stat.st_dev == identical["before_stat"].st_dev
    assert after_identical_stat.st_ino == identical["before_stat"].st_ino
    assert after_identical_stat.st_size == identical["before_stat"].st_size
    assert after_identical_stat.st_mtime_ns == identical["before_stat"].st_mtime_ns
    assert identical["link_events"] == ()
    assert all(
        event[0][0] != "run-ledger.yaml"
        for event in identical["unlink_events"]
    )
    assert identical["final_fds"]
    assert len(identical["final_open_count"]) >= 2
    assert len(identical["close_failure_events"]) == 1
    assert identical["close_failure_events"][0][1] is True
    assert identical["close_failure_events"][0][2] >= 2
    assert identical["durability_events"]
    identical_rendered = str(identical_result)
    assert str(identical_root) not in identical_rendered
    assert identical["temp_name"] not in identical_rendered
    assert "final inspection close errno=5 private detail" not in identical_rendered
    assert "errno" not in identical_rendered
    assert "public_url" not in identical_result
    assert "notification_result" not in identical_result
    assert "transition" not in identical_result
    assert "quality_pass" not in identical_result
    assert "PASS_PUBLISHED" not in identical_result[
        "persistence_evidence"
    ].values()


def test_compound_identity_close_and_cleanup_failures_preserve_precedence(monkeypatch, tmp_path):
    active_roles = {}
    final_fds = []
    original_temp_fds = []
    verifier_fds = []
    close_attempts = []
    owned_close_successes = []
    unlink_targets = []
    original_open = sut._os_open
    original_close = sut._os_close
    original_fstat = sut._os_fstat
    original_unlink = sut._os_unlink

    def track_open(path, flags, *args, **kwargs):
        fd = original_open(path, flags, *args, **kwargs)
        if path == "run-ledger.yaml":
            active_roles[fd] = "final-inspection"
            final_fds.append(fd)
        elif str(path).startswith(".run-ledger.tmp-"):
            creation = (
                flags & os.O_CREAT
                and flags & os.O_EXCL
                and flags & os.O_NOFOLLOW
            )
            verifier = (
                not flags & os.O_CREAT
                and not flags & os.O_EXCL
                and flags & os.O_NOFOLLOW
                and "dir_fd" in kwargs
            )
            assert creation or verifier
            if creation:
                active_roles[fd] = "original-temp"
                original_temp_fds.append(fd)
            else:
                active_roles[fd] = "verifier"
                verifier_fds.append(fd)
        else:
            active_roles[fd] = "owned-directory"
        return fd

    def mismatch(fd):
        value = original_fstat(fd)
        if fd in active_roles and active_roles[fd] == "final-inspection":
            return types.SimpleNamespace(
                st_dev=value.st_dev, st_ino=value.st_ino + 1,
                st_mode=value.st_mode, st_size=value.st_size,
                st_mtime_ns=value.st_mtime_ns,
            )
        return value

    def scoped_close(fd):
        assert fd in active_roles
        role = active_roles[fd]
        close_attempts.append(role)
        if role in ("final-inspection", "original-temp"):
            raise OSError(errno.EIO, "close")
        result = original_close(fd)
        owned_close_successes.append(fd)
        del active_roles[fd]
        return result

    def track_unlink(target, *args, **kwargs):
        unlink_targets.append(target)
        return original_unlink(target, *args, **kwargs)

    monkeypatch.setattr(sut, "_os_open", track_open)
    monkeypatch.setattr(sut, "_os_fstat", mismatch)
    monkeypatch.setattr(sut, "_os_close", scoped_close)
    monkeypatch.setattr(sut, "_os_unlink", track_unlink)
    result = _persist(tmp_path)
    assert len(final_fds) == 1
    assert len(original_temp_fds) == 1
    assert verifier_fds == []
    assert close_attempts.count("final-inspection") == 1
    assert close_attempts.count("original-temp") == 1
    assert close_attempts.count("owned-directory") == len(owned_close_successes)
    assert len(owned_close_successes) > 0
    assert unlink_targets == []
    assert "persistence_status" in result
    assert "reason_code" in result
    assert "persistence_violations" in result
    assert "missing_or_invalid_fields" in result
    assert "diagnostic_records" in result
    assert result["persistence_status"] == "DURABILITY_UNCONFIRMED"
    assert result["reason_code"] == "FINAL_IDENTITY_VERIFICATION_FAILED"
    assert result["persistence_violations"] == (
        "FINAL_IDENTITY_VERIFICATION_FAILED",
        "FINAL_INSPECTION_CLOSE_FAILED",
        "TEMP_FILE_CLOSE_FAILED",
        "TEMP_CLEANUP_FAILED",
    )
    assert result["missing_or_invalid_fields"] == ("persistence_io",)
    assert result["diagnostic_records"] == (
        {
            "reason_code": "FINAL_IDENTITY_VERIFICATION_FAILED",
            "field": "persistence_io",
        },
        {
            "reason_code": "FINAL_INSPECTION_CLOSE_FAILED",
            "field": "persistence_io",
        },
        {
            "reason_code": "TEMP_FILE_CLOSE_FAILED",
            "field": "persistence_io",
        },
        {
            "reason_code": "TEMP_CLEANUP_FAILED",
            "field": "persistence_io",
        },
    )
    assert len(set(result["persistence_violations"])) == 4
    assert "PRE_FINALIZATION_IO_FAILED" not in result["persistence_violations"]


def test_stable_size_mismatch_conflicts_without_read(monkeypatch, tmp_path):
    root = _ops_root(tmp_path)
    first = _persist(tmp_path, root=root)
    assert first["persistence_status"] == "WRITTEN"
    target = root / ARTIFACT_RELATIVE_PATH
    target.write_bytes(b"different-size")
    reads = []
    _spy(monkeypatch, "_os_read", reads)
    result = _persist(tmp_path, root=root)
    assert result["persistence_status"] == "CONFLICT"
    assert result["reason_code"] == "RUN_LEDGER_CONFLICT"
    assert reads == []

    owned_directory_fds = []
    owned_fd_usage_events = []
    selected_owned_fd = {"value": None}
    original_open = sut._os_open
    original_read = sut._os_read
    original_close = sut._os_close
    original_fstat = sut._os_fstat
    original_fsync = sut._os_fsync
    original_mkdir = sut._os_mkdir
    original_unlink = sut._os_unlink
    original_link = sut._os_link
    original_write = sut._os_write

    def owned_fd_refs(*values):
        return tuple(value for value in values if type(value) is int)

    def track_owned_open(path, *args, **kwargs):
        owned_fd_usage_events.append((
            "open",
            owned_fd_refs(kwargs.get("dir_fd")),
        ))
        fd = original_open(path, *args, **kwargs)
        if stat.S_ISDIR(os.fstat(fd).st_mode):
            owned_directory_fds.append(fd)
        return fd

    def track_owned_read(fd, size):
        owned_fd_usage_events.append(("read", (fd,)))
        return original_read(fd, size)

    def fail_one_owned_close(fd):
        owned_fd_usage_events.append(("close-attempt", (fd,)))
        if fd in owned_directory_fds:
            if selected_owned_fd["value"] is None:
                selected_owned_fd["value"] = fd
                owned_fd_usage_events.append(("close-failed", (fd,)))
                original_close(fd)
                raise OSError(errno.EIO, "private pre-durable close detail")
        return original_close(fd)

    def track_owned_fstat(fd):
        owned_fd_usage_events.append(("fstat", (fd,)))
        return original_fstat(fd)

    def track_owned_fsync(fd):
        owned_fd_usage_events.append(("fsync", (fd,)))
        return original_fsync(fd)

    def track_owned_mkdir(path, mode=0o777, *, dir_fd=None):
        owned_fd_usage_events.append((
            "mkdir",
            owned_fd_refs(dir_fd),
        ))
        return original_mkdir(path, mode, dir_fd=dir_fd)

    def track_owned_unlink(path, *, dir_fd=None):
        owned_fd_usage_events.append((
            "unlink",
            owned_fd_refs(dir_fd),
        ))
        return original_unlink(path, dir_fd=dir_fd)

    def track_owned_link(*args, **kwargs):
        owned_fd_usage_events.append((
            "link",
            owned_fd_refs(
                kwargs.get("src_dir_fd"),
                kwargs.get("dst_dir_fd"),
            ),
        ))
        return original_link(*args, **kwargs)

    def track_owned_write(fd, data):
        owned_fd_usage_events.append(("write", (fd,)))
        return original_write(fd, data)

    with monkeypatch.context() as patcher:
        patcher.setattr(sut, "_os_open", track_owned_open)
        patcher.setattr(sut, "_os_read", track_owned_read)
        patcher.setattr(sut, "_os_close", fail_one_owned_close)
        patcher.setattr(sut, "_os_fstat", track_owned_fstat)
        patcher.setattr(sut, "_os_fsync", track_owned_fsync)
        patcher.setattr(sut, "_os_mkdir", track_owned_mkdir)
        patcher.setattr(sut, "_os_unlink", track_owned_unlink)
        patcher.setattr(sut, "_os_link", track_owned_link)
        patcher.setattr(sut, "_os_write", track_owned_write)
        owned_result = _persist(tmp_path, root=root)

    assert selected_owned_fd["value"] is not None
    attempt_event = ("close-attempt", (selected_owned_fd["value"],))
    failure_event = ("close-failed", (selected_owned_fd["value"],))
    assert attempt_event in owned_fd_usage_events
    assert owned_fd_usage_events.count(attempt_event) == 1
    assert failure_event in owned_fd_usage_events
    assert owned_fd_usage_events.count(failure_event) == 1
    failure_index = owned_fd_usage_events.index(failure_event)
    later_owned_fd_usage_events = owned_fd_usage_events[failure_index + 1:]
    assert all(
        selected_owned_fd["value"] not in referenced_fds
        for _operation, referenced_fds in later_owned_fd_usage_events
    )
    assert reads == []
    assert owned_result["run_ledger_persisted"] is False
    assert owned_result["persistence_status"] == "CONFLICT"
    assert owned_result["reason_code"] == "RUN_LEDGER_CONFLICT"
    assert owned_result["persistence_evidence"] == {}
    assert owned_result["persistence_violations"] == (
        "RUN_LEDGER_CONFLICT",
        "PRE_FINALIZATION_IO_FAILED",
    )
    assert owned_result["missing_or_invalid_fields"] == (
        "artifact_relative_path",
        "persistence_io",
    )
    assert owned_result["diagnostic_records"] == (
        {
            "reason_code": "RUN_LEDGER_CONFLICT",
            "field": "artifact_relative_path",
        },
        {
            "reason_code": "PRE_FINALIZATION_IO_FAILED",
            "field": "persistence_io",
        },
    )
    owned_rendered = str(owned_result)
    assert str(root) not in owned_rendered
    assert "private pre-durable close detail" not in owned_rendered
    assert "errno" not in owned_rendered


def test_existing_target_read_requests_are_bounded(monkeypatch, tmp_path):
    root = _ops_root(tmp_path)
    first = _persist(tmp_path, root=root)
    assert first["persistence_status"] == "WRITTEN"
    requests = []
    original_read = sut._os_read

    def bounded_read(fd, size):
        requests.append(size)
        return original_read(fd, size)

    monkeypatch.setattr(sut, "_os_read", bounded_read)
    result = _persist(tmp_path, root=root)
    assert requests
    assert max(requests) <= 65536
    assert sum(requests) <= len(GOLDEN_BYTES) + 1
    assert result["persistence_status"] == "ALREADY_IDENTICAL"


def test_exact_stable_existing_bytes_are_identical_success(tmp_path):
    root = _ops_root(tmp_path)
    first = _persist(tmp_path, root=root)
    second = _persist(tmp_path, root=root)
    assert first["persistence_status"] == "WRITTEN"
    assert second["persistence_status"] == "ALREADY_IDENTICAL"
    assert second["run_ledger_persisted"] is True
    assert second["persistence_evidence"]["write_disposition"] == "ALREADY_IDENTICAL"
    assert (root / ARTIFACT_RELATIVE_PATH).read_bytes() == GOLDEN_BYTES


def test_exact_size_different_bytes_are_conflict(tmp_path):
    root = _ops_root(tmp_path)
    first = _persist(tmp_path, root=root)
    assert first["persistence_status"] == "WRITTEN"
    target = root / ARTIFACT_RELATIVE_PATH
    target.write_bytes(b"x" * len(GOLDEN_BYTES))
    result = _persist(tmp_path, root=root)
    assert result["persistence_status"] == "CONFLICT"
    assert result["run_ledger_persisted"] is False
    assert result["persistence_evidence"] == {}


def test_existing_target_truncation_during_read_is_unstable(monkeypatch, tmp_path):
    root = _ops_root(tmp_path)
    assert _persist(tmp_path, root=root)["persistence_status"] == "WRITTEN"
    reads = []

    def premature_eof(fd, size):
        reads.append((fd, size))
        return b""

    monkeypatch.setattr(sut, "_os_read", premature_eof)
    result = _persist(tmp_path, root=root)
    assert reads
    assert result["persistence_status"] == "IO_FAILED"
    assert result["reason_code"] == "EXISTING_TARGET_INSPECTION_FAILED"


def test_existing_target_extension_during_read_is_unstable(monkeypatch, tmp_path):
    root = _ops_root(tmp_path)
    assert _persist(tmp_path, root=root)["persistence_status"] == "WRITTEN"
    calls = []
    original_read = sut._os_read

    def extended(fd, size):
        calls.append(size)
        data = original_read(fd, size)
        return data if data else b"x"

    monkeypatch.setattr(sut, "_os_read", extended)
    result = _persist(tmp_path, root=root)
    assert calls
    assert result["persistence_status"] == "IO_FAILED"
    assert result["reason_code"] == "EXISTING_TARGET_INSPECTION_FAILED"


def test_second_fstat_mismatch_is_unstable(monkeypatch, tmp_path):
    root = _ops_root(tmp_path)
    assert _persist(tmp_path, root=root)["persistence_status"] == "WRITTEN"
    target_fds = []
    counts = {}
    original_open = sut._os_open
    original_fstat = sut._os_fstat

    def track_open(path, *args, **kwargs):
        fd = original_open(path, *args, **kwargs)
        if path == "run-ledger.yaml":
            target_fds.append(fd)
        return fd

    def changed(fd):
        value = original_fstat(fd)
        counts[fd] = counts.get(fd, 0) + 1
        if fd in target_fds and counts[fd] == 2:
            return types.SimpleNamespace(
                st_dev=value.st_dev, st_ino=value.st_ino, st_mode=value.st_mode,
                st_size=value.st_size, st_mtime_ns=value.st_mtime_ns + 1,
            )
        return value

    monkeypatch.setattr(sut, "_os_open", track_open)
    monkeypatch.setattr(sut, "_os_fstat", changed)
    result = _persist(tmp_path, root=root)
    assert target_fds
    assert result["persistence_status"] == "IO_FAILED"
    assert result["reason_code"] == "EXISTING_TARGET_INSPECTION_FAILED"


def test_path_replacement_after_comparison_is_detected(monkeypatch, tmp_path):
    root = _ops_root(tmp_path)
    assert _persist(tmp_path, root=root)["persistence_status"] == "WRITTEN"
    target = root / ARTIFACT_RELATIVE_PATH
    opens = []
    original_open = sut._os_open

    def replace_before_reopen(path, *args, **kwargs):
        if path == "run-ledger.yaml":
            opens.append(path)
            if len(opens) == 2:
                replacement = target.with_name("replacement")
                replacement.write_bytes(GOLDEN_BYTES)
                target.unlink()
                replacement.rename(target)
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(sut, "_os_open", replace_before_reopen)
    result = _persist(tmp_path, root=root)
    assert len(opens) >= 2
    assert result["persistence_status"] == "IO_FAILED"
    assert result["reason_code"] == "EXISTING_TARGET_INSPECTION_FAILED"


def test_existing_target_read_error_is_suppressed(monkeypatch, tmp_path):
    root = _ops_root(tmp_path)
    assert _persist(tmp_path, root=root)["persistence_status"] == "WRITTEN"
    reached = []

    def fail_read(fd, size):
        reached.append((fd, size))
        raise OSError(errno.EIO, "private read detail")

    monkeypatch.setattr(sut, "_os_read", fail_read)
    result = _persist(tmp_path, root=root)
    assert reached
    assert result["reason_code"] == "EXISTING_TARGET_INSPECTION_FAILED"
    assert "private read detail" not in str(result)


def test_existing_final_symlink_is_unsafe(tmp_path):
    root = _ops_root(tmp_path)
    entry_dir = root / "runs" / "by-entry-id" / ("sha256-" + ENTRY_ID_DIGEST)
    entry_dir.mkdir()
    outside = tmp_path / "outside"
    outside.write_bytes(GOLDEN_BYTES)
    (entry_dir / "run-ledger.yaml").symlink_to(outside)
    result = _persist(tmp_path, root=root)
    assert result["persistence_status"] == "AUTHORIZATION_FAILED"
    assert result["reason_code"] == "DESTINATION_PATH_UNSAFE"
    assert outside.read_bytes() == GOLDEN_BYTES


def test_existing_nonregular_target_is_unsafe(tmp_path):
    root = _ops_root(tmp_path)
    entry_dir = root / "runs" / "by-entry-id" / ("sha256-" + ENTRY_ID_DIGEST)
    entry_dir.mkdir()
    os.mkfifo(entry_dir / "run-ledger.yaml")
    result = _persist(tmp_path, root=root)
    assert result["persistence_status"] == "AUTHORIZATION_FAILED"
    assert result["reason_code"] == "DESTINATION_PATH_UNSAFE"


def test_identical_existing_file_fsync_failure_is_durability_unconfirmed(monkeypatch, tmp_path):
    root = _ops_root(tmp_path)
    assert _persist(tmp_path, root=root)["persistence_status"] == "WRITTEN"
    target_fds = []
    original_open = sut._os_open
    original_fsync = sut._os_fsync

    def track_open(path, *args, **kwargs):
        fd = original_open(path, *args, **kwargs)
        if path == "run-ledger.yaml":
            target_fds.append(fd)
        return fd

    def fail_target(fd):
        if fd in target_fds:
            raise OSError(errno.EIO, "file fsync")
        return original_fsync(fd)

    monkeypatch.setattr(sut, "_os_open", track_open)
    monkeypatch.setattr(sut, "_os_fsync", fail_target)
    result = _persist(tmp_path, root=root)
    assert target_fds
    assert result["persistence_status"] == "DURABILITY_UNCONFIRMED"
    assert result["reason_code"] == "FINAL_DURABILITY_UNCONFIRMED"
    assert result["persistence_evidence"]["write_disposition"] == "DURABILITY_UNCONFIRMED"


def test_identical_existing_directory_fsync_failure_is_durability_unconfirmed(monkeypatch, tmp_path):
    root = _ops_root(tmp_path)
    assert _persist(tmp_path, root=root)["persistence_status"] == "WRITTEN"
    reached = []
    original_fsync = sut._os_fsync

    def fail_directory(fd):
        mode = os.fstat(fd).st_mode
        if stat.S_ISDIR(mode) and reached:
            raise OSError(errno.EIO, "directory fsync")
        if stat.S_ISDIR(mode):
            reached.append(fd)
        return original_fsync(fd)

    monkeypatch.setattr(sut, "_os_fsync", fail_directory)
    result = _persist(tmp_path, root=root)
    assert reached
    assert result["persistence_status"] == "DURABILITY_UNCONFIRMED"
    assert result["reason_code"] == "FINAL_DURABILITY_UNCONFIRMED"


def test_existing_target_initial_fstat_failure_is_safe_io_failure(monkeypatch, tmp_path):
    root = _ops_root(tmp_path)
    assert _persist(tmp_path, root=root)["persistence_status"] == "WRITTEN"
    target_fds = []
    original_open = sut._os_open
    original_fstat = sut._os_fstat

    def track_open(path, *args, **kwargs):
        fd = original_open(path, *args, **kwargs)
        if path == "run-ledger.yaml":
            target_fds.append(fd)
        return fd

    def fail_fstat(fd):
        if fd in target_fds:
            raise OSError(errno.EIO, "private fstat")
        return original_fstat(fd)

    monkeypatch.setattr(sut, "_os_open", track_open)
    monkeypatch.setattr(sut, "_os_fstat", fail_fstat)
    result = _persist(tmp_path, root=root)
    assert target_fds
    assert result["persistence_status"] == "IO_FAILED"
    assert result["reason_code"] == "EXISTING_TARGET_INSPECTION_FAILED"


def test_target_absent_is_written_create_only(tmp_path):
    root = _ops_root(tmp_path)
    result = _persist(tmp_path, root=root)
    target = root / ARTIFACT_RELATIVE_PATH
    assert result["persistence_status"] == "WRITTEN"
    assert result["run_ledger_persisted"] is True
    assert result["persistence_evidence"]["write_disposition"] == "WRITTEN"
    assert target.read_bytes() == GOLDEN_BYTES
    assert tuple(target.parent.glob(".run-ledger.tmp-*")) == ()


def test_different_existing_bytes_remain_unchanged_after_conflict(tmp_path):
    root = _ops_root(tmp_path)
    entry_dir = root / "runs" / "by-entry-id" / ("sha256-" + ENTRY_ID_DIGEST)
    entry_dir.mkdir()
    target = entry_dir / "run-ledger.yaml"
    before = b"different durable bytes"
    target.write_bytes(before)
    result = _persist(tmp_path, root=root)
    assert result["persistence_status"] == "CONFLICT"
    assert target.read_bytes() == before


def test_short_writes_complete_before_finalization(monkeypatch, tmp_path):
    writes = []
    original_write = sut._os_write

    def short_write(fd, data):
        portion = data[:max(1, len(data) // 3)]
        writes.append(len(portion))
        return original_write(fd, portion)

    monkeypatch.setattr(sut, "_os_write", short_write)
    result = _persist(tmp_path)
    assert len(writes) > 1
    assert sum(writes) == len(GOLDEN_BYTES)
    assert result["persistence_status"] == "WRITTEN"


def test_temp_write_failure_with_successful_cleanup_has_single_violation(monkeypatch, tmp_path):
    reached = []

    def fail_write(fd, data):
        reached.append((fd, len(data)))
        raise OSError(errno.EIO, "write")

    monkeypatch.setattr(sut, "_os_write", fail_write)
    result = _persist(tmp_path)
    assert reached
    assert result["persistence_status"] == "IO_FAILED"
    assert result["persistence_violations"] == ("TEMP_FILE_WRITE_FAILED",)


def test_temp_fsync_failure_with_successful_cleanup_has_single_violation(monkeypatch, tmp_path):
    reached = []
    original_fsync = sut._os_fsync

    def fail_file(fd):
        if stat.S_ISREG(os.fstat(fd).st_mode):
            reached.append(fd)
            raise OSError(errno.EIO, "temp fsync")
        return original_fsync(fd)

    monkeypatch.setattr(sut, "_os_fsync", fail_file)
    result = _persist(tmp_path)
    assert reached
    assert result["persistence_violations"] == ("TEMP_FILE_FSYNC_FAILED",)


def test_atomic_link_race_with_identical_winner_returns_already_identical(monkeypatch, tmp_path):
    reached = []
    original_link = sut._os_link

    def winner(*args, **kwargs):
        reached.append((args, kwargs))
        original_link(*args, **kwargs)
        raise FileExistsError(errno.EEXIST, "winner")

    monkeypatch.setattr(sut, "_os_link", winner)
    result = _persist(tmp_path)
    assert reached
    assert result["persistence_status"] == "ALREADY_IDENTICAL"
    assert result["persistence_evidence"]["write_disposition"] == "ALREADY_IDENTICAL"

    replacement_root = _ops_root(tmp_path / "identical-winner-replacement")
    replacement_temp_name = (
        ".run-ledger.tmp-33333333333333333333333333333333"
    )
    replacement_bytes = b"unrelated-identical-winner-temp"
    replacement_state = {
        "linked": False,
        "directory_fsyncs": 0,
        "replaced": False,
    }
    replacement_events = []
    replacement_temp_fds = []
    replacement_final_snapshot = {}
    original_open = sut._os_open
    original_fsync = sut._os_fsync
    original_unlink = sut._os_unlink
    original_close = sut._os_close
    replacement_target = replacement_root / ARTIFACT_RELATIVE_PATH
    replacement_path = replacement_target.parent / replacement_temp_name

    def track_replacement_open(path, *args, **kwargs):
        fd = original_open(path, *args, **kwargs)
        if path == replacement_temp_name:
            replacement_temp_fds.append(fd)
            replacement_events.append(("temp-open", fd))
        return fd

    def effectful_identical_winner(*args, **kwargs):
        value = original_link(*args, **kwargs)
        replacement_state["linked"] = True
        replacement_events.append(("link-effect", args, kwargs))
        raise FileExistsError(errno.EEXIST, "private identical winner")

    def replace_after_winner_durability(fd):
        value = original_fsync(fd)
        if replacement_state["linked"] and stat.S_ISDIR(os.fstat(fd).st_mode):
            replacement_state["directory_fsyncs"] += 1
            replacement_events.append(("winner-directory-fsync", fd))
            if (
                replacement_state["directory_fsyncs"] == 2
                and not replacement_state["replaced"]
            ):
                before = replacement_target.stat()
                replacement_final_snapshot.update({
                    "st_dev": before.st_dev,
                    "st_ino": before.st_ino,
                    "st_size": before.st_size,
                    "st_mtime_ns": before.st_mtime_ns,
                    "bytes": replacement_target.read_bytes(),
                })
                os.unlink(replacement_temp_name, dir_fd=fd)
                replacement_fd = os.open(
                    replacement_temp_name,
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                    0o600,
                    dir_fd=fd,
                )
                try:
                    os.write(replacement_fd, replacement_bytes)
                    replacement_stat = os.fstat(replacement_fd)
                    replacement_final_snapshot["replacement_inode"] = (
                        replacement_stat.st_dev,
                        replacement_stat.st_ino,
                    )
                finally:
                    os.close(replacement_fd)
                replacement_state["replaced"] = True
                replacement_events.append(("temp-replaced", fd))
        return value

    def track_replacement_unlink(path, *, dir_fd=None):
        replacement_events.append(("production-unlink", path, dir_fd))
        return original_unlink(path, dir_fd=dir_fd)

    def track_replacement_close(fd):
        if fd in replacement_temp_fds:
            replacement_events.append(("temp-close-attempt", fd))
        return original_close(fd)

    with monkeypatch.context() as patcher:
        patcher.setattr(sut, "_new_temp_name", lambda: replacement_temp_name)
        patcher.setattr(sut, "_os_open", track_replacement_open)
        patcher.setattr(sut, "_os_link", effectful_identical_winner)
        patcher.setattr(sut, "_os_fsync", replace_after_winner_durability)
        patcher.setattr(sut, "_os_unlink", track_replacement_unlink)
        patcher.setattr(sut, "_os_close", track_replacement_close)
        replacement_result = _persist(tmp_path, root=replacement_root)

    assert replacement_state == {
        "linked": True,
        "directory_fsyncs": 2,
        "replaced": True,
    }
    assert replacement_final_snapshot["bytes"] == GOLDEN_BYTES
    assert replacement_temp_fds
    assert sum(
        event[0] == "temp-close-attempt"
        and event[1] == replacement_temp_fds[0]
        for event in replacement_events
    ) == 1
    assert not any(
        event[0] == "production-unlink" and event[1] == replacement_temp_name
        for event in replacement_events
    )
    assert replacement_path.read_bytes() == replacement_bytes
    after = replacement_target.stat()
    assert (
        after.st_dev,
        after.st_ino,
        after.st_size,
        after.st_mtime_ns,
    ) == (
        replacement_final_snapshot["st_dev"],
        replacement_final_snapshot["st_ino"],
        replacement_final_snapshot["st_size"],
        replacement_final_snapshot["st_mtime_ns"],
    )
    assert replacement_target.read_bytes() == GOLDEN_BYTES
    assert replacement_result["run_ledger_persisted"] is True
    assert replacement_result["persistence_status"] == (
        "PERSISTED_CLEANUP_WARNING"
    )
    assert replacement_result["reason_code"] == "PERSISTED_CLEANUP_WARNING"
    assert replacement_result["persistence_violations"] == (
        "PERSISTED_CLEANUP_WARNING",
    )
    assert replacement_result["missing_or_invalid_fields"] == (
        "persistence_io",
    )
    assert replacement_result["diagnostic_records"] == ({
        "reason_code": "PERSISTED_CLEANUP_WARNING",
        "field": "persistence_io",
    },)
    assert replacement_result["persistence_evidence"] == {
        "run_ledger_entry_id": "ledger-entry-001",
        "run_id": "run-001",
        "artifact_relative_path": ARTIFACT_RELATIVE_PATH,
        "serialization_format": "canonical_json_yaml_1_2_subset",
        "content_digest_algorithm": "sha256",
        "content_digest": GOLDEN_DIGEST,
        "write_disposition": "ALREADY_IDENTICAL",
    }
    replacement_rendered = str(replacement_result)
    assert str(replacement_root) not in replacement_rendered
    assert replacement_temp_name not in replacement_rendered
    assert "private identical winner" not in replacement_rendered
    assert "errno" not in replacement_rendered


def test_atomic_link_race_with_different_winner_returns_conflict(monkeypatch, tmp_path):
    reached = []

    def winner(src, dst, *, src_dir_fd, dst_dir_fd, follow_symlinks):
        del src, follow_symlinks
        reached.append(dst)
        fd = os.open(dst, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600, dir_fd=dst_dir_fd)
        os.write(fd, b"different winner")
        os.close(fd)
        raise FileExistsError(errno.EEXIST, "winner")

    monkeypatch.setattr(sut, "_os_link", winner)
    result = _persist(tmp_path)
    assert reached == ["run-ledger.yaml"]
    assert result["persistence_status"] == "CONFLICT"
    assert result["reason_code"] == "RUN_LEDGER_CONFLICT"


def test_atomic_link_failure_without_winner_is_io_failure(monkeypatch, tmp_path):
    reached = []
    original_link = sut._os_link

    def fail(*args, **kwargs):
        reached.append((args, kwargs))
        raise OSError(errno.EIO, "link failure")

    monkeypatch.setattr(sut, "_os_link", fail)
    result = _persist(tmp_path)
    assert reached
    assert result["persistence_status"] == "IO_FAILED"
    assert result["reason_code"] == "ATOMIC_CREATE_FAILED"

    effect_root = _ops_root(tmp_path / "effectful-non-eexist-link")
    effect_temp_name = ".run-ledger.tmp-66666666666666666666666666666666"
    effect_target = effect_root / ARTIFACT_RELATIVE_PATH
    effect_events = []
    original_unlink = sut._os_unlink

    def link_then_raise(*args, **kwargs):
        value = original_link(*args, **kwargs)
        effect_events.append(("link-effect", args, kwargs))
        raise OSError(errno.EIO, "private post-link exception")

    def track_effect_unlink(path, *, dir_fd=None):
        effect_events.append(("unlink", path, dir_fd))
        return original_unlink(path, dir_fd=dir_fd)

    with monkeypatch.context() as patcher:
        patcher.setattr(sut, "_new_temp_name", lambda: effect_temp_name)
        patcher.setattr(sut, "_os_link", link_then_raise)
        patcher.setattr(sut, "_os_unlink", track_effect_unlink)
        effect_result = _persist(tmp_path, root=effect_root)

    uncertain_root = _ops_root(tmp_path / "uncertain-non-eexist-link")
    uncertain_temp_name = (
        ".run-ledger.tmp-77777777777777777777777777777777"
    )
    uncertain_target = uncertain_root / ARTIFACT_RELATIVE_PATH
    uncertain_temp_path = uncertain_target.parent / uncertain_temp_name
    uncertain_state = {"linked": False}
    uncertain_events = []
    original_open = sut._os_open

    def uncertain_link_then_raise(*args, **kwargs):
        value = original_link(*args, **kwargs)
        uncertain_state["linked"] = True
        uncertain_events.append(("link-effect", args, kwargs))
        raise OSError(errno.EIO, "private ambiguous link exception")

    def fail_uncertain_final_open(path, *args, **kwargs):
        if uncertain_state["linked"] and path == "run-ledger.yaml":
            uncertain_events.append(("final-inspection-failed", path))
            raise OSError(errno.EIO, "private final inspection detail")
        return original_open(path, *args, **kwargs)

    def track_uncertain_unlink(path, *, dir_fd=None):
        uncertain_events.append(("unlink", path, dir_fd))
        return original_unlink(path, dir_fd=dir_fd)

    with monkeypatch.context() as patcher:
        patcher.setattr(sut, "_new_temp_name", lambda: uncertain_temp_name)
        patcher.setattr(sut, "_os_link", uncertain_link_then_raise)
        patcher.setattr(sut, "_os_open", fail_uncertain_final_open)
        patcher.setattr(sut, "_os_unlink", track_uncertain_unlink)
        uncertain_result = _persist(tmp_path, root=uncertain_root)

    assert any(event[0] == "link-effect" for event in effect_events)
    assert not any(
        event[0] == "unlink" and event[1] == "run-ledger.yaml"
        for event in effect_events
    )
    assert effect_target.read_bytes() == GOLDEN_BYTES
    assert effect_result["run_ledger_persisted"] is True
    assert effect_result["persistence_status"] == "WRITTEN"
    assert effect_result["reason_code"] == "RUN_LEDGER_PERSISTED"
    assert effect_result["reason"] == (
        "The run-ledger artifact was durably written."
    )
    assert effect_result["persistence_violations"] == ()
    assert effect_result["missing_or_invalid_fields"] == ()
    assert effect_result["diagnostic_records"] == ()
    assert effect_result["persistence_evidence"] == {
        "run_ledger_entry_id": "ledger-entry-001",
        "run_id": "run-001",
        "artifact_relative_path": ARTIFACT_RELATIVE_PATH,
        "serialization_format": "canonical_json_yaml_1_2_subset",
        "content_digest_algorithm": "sha256",
        "content_digest": GOLDEN_DIGEST,
        "write_disposition": "WRITTEN",
    }
    effect_rendered = str(effect_result)
    assert str(effect_root) not in effect_rendered
    assert effect_temp_name not in effect_rendered
    assert "private post-link exception" not in effect_rendered
    assert "errno" not in effect_rendered

    assert uncertain_state["linked"] is True
    assert ("final-inspection-failed", "run-ledger.yaml") in uncertain_events
    assert not any(
        event[0] == "unlink" and event[1] == "run-ledger.yaml"
        for event in uncertain_events
    )
    assert not any(
        event[0] == "unlink" and event[1] == uncertain_temp_name
        for event in uncertain_events
    )
    assert uncertain_target.read_bytes() == GOLDEN_BYTES
    assert uncertain_temp_path.is_file()
    assert uncertain_result["run_ledger_persisted"] is False
    assert uncertain_result["persistence_status"] == "DURABILITY_UNCONFIRMED"
    assert uncertain_result["reason_code"] == (
        "FINAL_IDENTITY_VERIFICATION_FAILED"
    )
    assert uncertain_result["reason"] == (
        "The final name may exist, but continuity with the fsynced temporary "
        "inode could not be verified."
    )
    assert uncertain_result["persistence_violations"] == (
        "FINAL_IDENTITY_VERIFICATION_FAILED",
        "TEMP_CLEANUP_FAILED",
    )
    assert uncertain_result["missing_or_invalid_fields"] == (
        "persistence_io",
    )
    assert uncertain_result["diagnostic_records"] == (
        {
            "reason_code": "FINAL_IDENTITY_VERIFICATION_FAILED",
            "field": "persistence_io",
        },
        {
            "reason_code": "TEMP_CLEANUP_FAILED",
            "field": "persistence_io",
        },
    )
    assert uncertain_result["persistence_evidence"] == {
        "run_ledger_entry_id": "ledger-entry-001",
        "run_id": "run-001",
        "artifact_relative_path": ARTIFACT_RELATIVE_PATH,
        "serialization_format": "canonical_json_yaml_1_2_subset",
        "content_digest_algorithm": "sha256",
        "content_digest": GOLDEN_DIGEST,
        "write_disposition": "DURABILITY_UNCONFIRMED",
    }
    uncertain_rendered = str(uncertain_result)
    assert str(uncertain_root) not in uncertain_rendered
    assert uncertain_temp_name not in uncertain_rendered
    assert "private ambiguous link exception" not in uncertain_rendered
    assert "private final inspection detail" not in uncertain_rendered
    assert "errno" not in uncertain_rendered


def test_directory_fsync_after_link_failure_is_durability_unconfirmed(monkeypatch, tmp_path):
    linked = []
    original_link = sut._os_link
    original_fsync = sut._os_fsync

    def track_link(*args, **kwargs):
        value = original_link(*args, **kwargs)
        linked.append(True)
        return value

    def fail_after_link(fd):
        if linked and stat.S_ISDIR(os.fstat(fd).st_mode):
            raise OSError(errno.EIO, "directory fsync")
        return original_fsync(fd)

    monkeypatch.setattr(sut, "_os_link", track_link)
    monkeypatch.setattr(sut, "_os_fsync", fail_after_link)
    result = _persist(tmp_path)
    assert linked
    assert result["persistence_status"] == "DURABILITY_UNCONFIRMED"
    assert result["reason_code"] == "FINAL_DURABILITY_UNCONFIRMED"


def test_temp_unlink_after_durable_final_failure_is_cleanup_warning(monkeypatch, tmp_path):
    original_unlink = sut._os_unlink
    reached = []

    def fail_unlink(*args, **kwargs):
        reached.append((args, kwargs))
        raise OSError(errno.EIO, "unlink")

    monkeypatch.setattr(sut, "_os_unlink", fail_unlink)
    result = _persist(tmp_path)
    assert reached
    assert result["persistence_status"] == "PERSISTED_CLEANUP_WARNING"
    assert result["run_ledger_persisted"] is True
    assert result["persistence_evidence"]["write_disposition"] == "WRITTEN"

    replacement_root = _ops_root(tmp_path / "durable-new-write-replacement")
    replacement_temp_name = (
        ".run-ledger.tmp-44444444444444444444444444444444"
    )
    replacement_bytes = b"unrelated-durable-new-write-temp"
    replacement_target = replacement_root / ARTIFACT_RELATIVE_PATH
    replacement_path = replacement_target.parent / replacement_temp_name
    replacement_state = {"linked": False, "replaced": False}
    replacement_events = []
    final_fds = []
    temp_fds = []
    original_open = sut._os_open
    original_fstat = sut._os_fstat
    original_link = sut._os_link
    original_close = sut._os_close

    def track_replacement_open(path, *args, **kwargs):
        fd = original_open(path, *args, **kwargs)
        if path == "run-ledger.yaml":
            final_fds.append(fd)
        elif path == replacement_temp_name:
            temp_fds.append(fd)
        return fd

    def track_replacement_link(*args, **kwargs):
        value = original_link(*args, **kwargs)
        replacement_state["linked"] = True
        replacement_events.append(("link", args, kwargs))
        return value

    def replace_after_final_revalidation(fd):
        value = original_fstat(fd)
        if (
            replacement_state["linked"]
            and fd in final_fds
            and len(final_fds) >= 2
            and fd == final_fds[1]
            and not replacement_state["replaced"]
        ):
            assert replacement_target.read_bytes() == GOLDEN_BYTES
            replacement_path.unlink()
            replacement_path.write_bytes(replacement_bytes)
            replacement_path.chmod(0o600)
            replacement_state["replaced"] = True
            replacement_events.append(("temp-replaced", fd))
        return value

    def track_replacement_unlink(path, *, dir_fd=None):
        replacement_events.append(("production-unlink", path, dir_fd))
        return original_unlink(path, dir_fd=dir_fd)

    def track_replacement_close(fd):
        if fd in temp_fds:
            replacement_events.append(("temp-close-attempt", fd))
        return original_close(fd)

    with monkeypatch.context() as patcher:
        patcher.setattr(sut, "_new_temp_name", lambda: replacement_temp_name)
        patcher.setattr(sut, "_os_open", track_replacement_open)
        patcher.setattr(sut, "_os_link", track_replacement_link)
        patcher.setattr(sut, "_os_fstat", replace_after_final_revalidation)
        patcher.setattr(sut, "_os_unlink", track_replacement_unlink)
        patcher.setattr(sut, "_os_close", track_replacement_close)
        replacement_result = _persist(tmp_path, root=replacement_root)

    assert replacement_state == {"linked": True, "replaced": True}
    assert len(final_fds) >= 2
    assert temp_fds
    assert sum(
        event[0] == "temp-close-attempt" and event[1] == temp_fds[0]
        for event in replacement_events
    ) == 1
    assert not any(
        event[0] == "production-unlink" and event[1] == replacement_temp_name
        for event in replacement_events
    )
    assert not any(
        event[0] == "production-unlink" and event[1] == "run-ledger.yaml"
        for event in replacement_events
    )
    assert replacement_target.read_bytes() == GOLDEN_BYTES
    assert replacement_path.read_bytes() == replacement_bytes
    assert replacement_result["run_ledger_persisted"] is True
    assert replacement_result["persistence_status"] == (
        "PERSISTED_CLEANUP_WARNING"
    )
    assert replacement_result["reason_code"] == "PERSISTED_CLEANUP_WARNING"
    assert replacement_result["persistence_violations"] == (
        "PERSISTED_CLEANUP_WARNING",
    )
    assert replacement_result["missing_or_invalid_fields"] == (
        "persistence_io",
    )
    assert replacement_result["diagnostic_records"] == ({
        "reason_code": "PERSISTED_CLEANUP_WARNING",
        "field": "persistence_io",
    },)
    assert replacement_result["persistence_evidence"] == {
        "run_ledger_entry_id": "ledger-entry-001",
        "run_id": "run-001",
        "artifact_relative_path": ARTIFACT_RELATIVE_PATH,
        "serialization_format": "canonical_json_yaml_1_2_subset",
        "content_digest_algorithm": "sha256",
        "content_digest": GOLDEN_DIGEST,
        "write_disposition": "WRITTEN",
    }
    replacement_rendered = str(replacement_result)
    assert str(replacement_root) not in replacement_rendered
    assert replacement_temp_name not in replacement_rendered
    assert "errno" not in replacement_rendered


def test_directory_fsync_after_cleanup_failure_is_cleanup_warning(monkeypatch, tmp_path):
    unlinked = []
    original_unlink = sut._os_unlink
    original_fsync = sut._os_fsync

    def track_unlink(*args, **kwargs):
        value = original_unlink(*args, **kwargs)
        unlinked.append(True)
        return value

    def fail_cleanup_fsync(fd):
        if unlinked and stat.S_ISDIR(os.fstat(fd).st_mode):
            raise OSError(errno.EIO, "cleanup fsync")
        return original_fsync(fd)

    monkeypatch.setattr(sut, "_os_unlink", track_unlink)
    monkeypatch.setattr(sut, "_os_fsync", fail_cleanup_fsync)
    result = _persist(tmp_path)
    assert unlinked
    assert result["persistence_status"] == "PERSISTED_CLEANUP_WARNING"
    assert result["persistence_evidence"]["write_disposition"] == "WRITTEN"


def test_compound_temp_write_and_cleanup_failures_are_aggregated(monkeypatch, tmp_path):
    original_unlink = sut._os_unlink
    original_fsync = sut._os_fsync
    monkeypatch.setattr(sut, "_os_write", lambda fd, data: (_ for _ in ()).throw(OSError(errno.EIO, "write")))
    monkeypatch.setattr(sut, "_os_unlink", lambda *args, **kwargs: (_ for _ in ()).throw(OSError(errno.EIO, "unlink")))
    result = _persist(tmp_path)
    assert result["persistence_status"] == "IO_FAILED"
    assert result["persistence_violations"] == ("TEMP_FILE_WRITE_FAILED", "TEMP_CLEANUP_FAILED")

    cleanup_root = _ops_root(tmp_path / "cleanup-fsync-failure")
    cleanup_state = {"unlinked": False}
    cleanup_events = []

    def fail_write(fd, data):
        cleanup_events.append(("write-failed", fd, len(data)))
        raise OSError(errno.EIO, "private write detail")

    def succeed_unlink(path, *, dir_fd=None):
        value = original_unlink(path, dir_fd=dir_fd)
        cleanup_state["unlinked"] = True
        cleanup_events.append(("unlink-succeeded", path, dir_fd))
        return value

    def fail_cleanup_fsync(fd):
        if cleanup_state["unlinked"] and stat.S_ISDIR(os.fstat(fd).st_mode):
            cleanup_events.append(("cleanup-fsync-failed", fd))
            raise OSError(errno.EIO, "private cleanup fsync detail")
        return original_fsync(fd)

    with monkeypatch.context() as patcher:
        patcher.setattr(sut, "_os_write", fail_write)
        patcher.setattr(sut, "_os_unlink", succeed_unlink)
        patcher.setattr(sut, "_os_fsync", fail_cleanup_fsync)
        cleanup_result = _persist(tmp_path, root=cleanup_root)

    assert any(event[0] == "write-failed" for event in cleanup_events)
    unlink_events = [
        event for event in cleanup_events if event[0] == "unlink-succeeded"
    ]
    cleanup_fsync_events = [
        event for event in cleanup_events
        if event[0] == "cleanup-fsync-failed"
    ]
    assert len(unlink_events) == 1
    assert len(cleanup_fsync_events) == 1
    assert cleanup_events.index(unlink_events[0]) < cleanup_events.index(
        cleanup_fsync_events[0]
    )
    assert cleanup_result["run_ledger_persisted"] is False
    assert cleanup_result["persistence_status"] == "IO_FAILED"
    assert cleanup_result["reason_code"] == "TEMP_FILE_WRITE_FAILED"
    assert cleanup_result["persistence_evidence"] == {}
    assert cleanup_result["persistence_violations"] == (
        "TEMP_FILE_WRITE_FAILED",
        "TEMP_CLEANUP_FAILED",
    )
    assert cleanup_result["missing_or_invalid_fields"] == (
        "persistence_io",
    )
    assert cleanup_result["diagnostic_records"] == (
        {
            "reason_code": "TEMP_FILE_WRITE_FAILED",
            "field": "persistence_io",
        },
        {
            "reason_code": "TEMP_CLEANUP_FAILED",
            "field": "persistence_io",
        },
    )
    assert not (cleanup_root / ARTIFACT_RELATIVE_PATH).exists()
    cleanup_rendered = str(cleanup_result)
    assert str(cleanup_root) not in cleanup_rendered
    assert ".run-ledger.tmp-" not in cleanup_rendered
    assert "private write detail" not in cleanup_rendered
    assert "private cleanup fsync detail" not in cleanup_rendered
    assert "errno" not in cleanup_rendered


def test_compound_temp_fsync_and_cleanup_failures_are_aggregated(monkeypatch, tmp_path):
    original_fsync = sut._os_fsync

    def fail_file(fd):
        if stat.S_ISREG(os.fstat(fd).st_mode):
            raise OSError(errno.EIO, "fsync")
        return original_fsync(fd)

    monkeypatch.setattr(sut, "_os_fsync", fail_file)
    monkeypatch.setattr(sut, "_os_unlink", lambda *args, **kwargs: (_ for _ in ()).throw(OSError(errno.EIO, "unlink")))
    result = _persist(tmp_path)
    assert result["persistence_violations"] == ("TEMP_FILE_FSYNC_FAILED", "TEMP_CLEANUP_FAILED")


def test_compound_final_durability_and_cleanup_failures_are_aggregated(monkeypatch, tmp_path):
    linked = []
    original_link = sut._os_link
    original_fsync = sut._os_fsync

    def track_link(*args, **kwargs):
        value = original_link(*args, **kwargs)
        linked.append(True)
        return value

    def fail_final(fd):
        if linked and stat.S_ISDIR(os.fstat(fd).st_mode):
            raise OSError(errno.EIO, "final fsync")
        return original_fsync(fd)

    monkeypatch.setattr(sut, "_os_link", track_link)
    monkeypatch.setattr(sut, "_os_fsync", fail_final)
    monkeypatch.setattr(sut, "_os_unlink", lambda *args, **kwargs: (_ for _ in ()).throw(OSError(errno.EIO, "unlink")))
    result = _persist(tmp_path)
    assert result["persistence_status"] == "DURABILITY_UNCONFIRMED"
    assert result["persistence_violations"] == ("FINAL_DURABILITY_UNCONFIRMED", "TEMP_CLEANUP_FAILED")


def test_compound_atomic_create_and_cleanup_failures_are_aggregated(monkeypatch, tmp_path):
    real_unlink = sut._os_unlink
    monkeypatch.setattr(sut, "_os_link", lambda *args, **kwargs: (_ for _ in ()).throw(OSError(errno.EIO, "link")))
    monkeypatch.setattr(sut, "_os_unlink", lambda *args, **kwargs: (_ for _ in ()).throw(OSError(errno.EIO, "unlink")))
    result = _persist(tmp_path)
    assert result["persistence_violations"] == ("ATOMIC_CREATE_FAILED", "TEMP_CLEANUP_FAILED")

    replacement_root = _ops_root(tmp_path / "pre-durable-temp-replacement")
    replacement_temp_name = (
        ".run-ledger.tmp-55555555555555555555555555555555"
    )
    replacement_bytes = b"unrelated-pre-durable-temp"
    replacement_target = replacement_root / ARTIFACT_RELATIVE_PATH
    replacement_path = replacement_target.parent / replacement_temp_name
    temp_open_fds = []
    temp_fstat_events = []
    replacement_events = []
    inode_proofs = []
    original_open = sut._os_open
    original_fstat = sut._os_fstat

    def track_temp_open(path, *args, **kwargs):
        fd = original_open(path, *args, **kwargs)
        if path == replacement_temp_name:
            temp_open_fds.append(fd)
            replacement_events.append(("temp-open", fd))
        return fd

    def track_temp_fstat(fd):
        value = original_fstat(fd)
        if fd in temp_open_fds:
            temp_fstat_events.append((fd, value.st_dev, value.st_ino))
        return value

    def replace_then_fail_link(
        source,
        destination,
        *,
        src_dir_fd=None,
        dst_dir_fd=None,
        follow_symlinks=True,
    ):
        assert source == replacement_temp_name
        assert destination == "run-ledger.yaml"
        assert src_dir_fd == dst_dir_fd
        assert follow_symlinks is False
        assert temp_open_fds
        trusted_before = os.fstat(temp_open_fds[0])
        os.unlink(source, dir_fd=src_dir_fd)
        replacement_fd = os.open(
            source,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            0o600,
            dir_fd=src_dir_fd,
        )
        try:
            os.write(replacement_fd, replacement_bytes)
            replacement_stat = os.fstat(replacement_fd)
        finally:
            os.close(replacement_fd)
        trusted_after = os.fstat(temp_open_fds[0])
        inode_proofs.append((
            (trusted_before.st_dev, trusted_before.st_ino),
            (trusted_after.st_dev, trusted_after.st_ino),
            (replacement_stat.st_dev, replacement_stat.st_ino),
        ))
        replacement_events.append(("temp-replaced-before-link-error",))
        raise OSError(errno.EIO, "private link effect detail")

    def track_production_unlink(path, *, dir_fd=None):
        replacement_events.append(("production-unlink", path, dir_fd))
        return real_unlink(path, dir_fd=dir_fd)

    with monkeypatch.context() as patcher:
        patcher.setattr(sut, "_new_temp_name", lambda: replacement_temp_name)
        patcher.setattr(sut, "_os_open", track_temp_open)
        patcher.setattr(sut, "_os_fstat", track_temp_fstat)
        patcher.setattr(sut, "_os_link", replace_then_fail_link)
        patcher.setattr(sut, "_os_unlink", track_production_unlink)
        replacement_result = _persist(tmp_path, root=replacement_root)

    assert len(inode_proofs) == 1
    trusted_before, trusted_after, replacement_inode = inode_proofs[0]
    assert trusted_before == trusted_after
    assert replacement_inode != trusted_after
    assert len(temp_open_fds) >= 2
    assert any(fd == temp_open_fds[1] for fd, _dev, _ino in temp_fstat_events)
    assert not any(
        event[0] == "production-unlink" and event[1] == replacement_temp_name
        for event in replacement_events
    )
    assert replacement_path.read_bytes() == replacement_bytes
    assert not replacement_target.exists()
    assert replacement_result["run_ledger_persisted"] is False
    assert replacement_result["persistence_status"] == "IO_FAILED"
    assert replacement_result["reason_code"] == "ATOMIC_CREATE_FAILED"
    assert replacement_result["persistence_evidence"] == {}
    assert replacement_result["persistence_violations"] == (
        "ATOMIC_CREATE_FAILED",
        "TEMP_CLEANUP_FAILED",
    )
    assert replacement_result["missing_or_invalid_fields"] == (
        "persistence_io",
    )
    assert replacement_result["diagnostic_records"] == (
        {
            "reason_code": "ATOMIC_CREATE_FAILED",
            "field": "persistence_io",
        },
        {
            "reason_code": "TEMP_CLEANUP_FAILED",
            "field": "persistence_io",
        },
    )
    replacement_rendered = str(replacement_result)
    assert str(replacement_root) not in replacement_rendered
    assert replacement_temp_name not in replacement_rendered
    assert "private link effect detail" not in replacement_rendered
    assert "errno" not in replacement_rendered


def test_compound_pre_finalization_and_cleanup_failures_are_aggregated(monkeypatch, tmp_path):
    calls = []
    original_fstat = sut._os_fstat

    def fail_temp_fstat(fd):
        value = original_fstat(fd)
        if stat.S_ISREG(value.st_mode):
            calls.append(fd)
            raise OSError(errno.EIO, "fstat")
        return value

    monkeypatch.setattr(sut, "_os_fstat", fail_temp_fstat)
    monkeypatch.setattr(sut, "_os_unlink", lambda *args, **kwargs: (_ for _ in ()).throw(OSError(errno.EIO, "unlink")))
    result = _persist(tmp_path)
    assert calls
    assert result["persistence_status"] == "IO_FAILED"
    assert result["persistence_violations"] == ("PRE_FINALIZATION_IO_FAILED", "TEMP_CLEANUP_FAILED")


def test_all_public_result_families_use_fresh_containers(monkeypatch, tmp_path):
    def mutable_container_ids(value):
        identifiers = set()
        stack = [value]
        while stack:
            current = stack.pop()
            if type(current) in (dict, list):
                if id(current) in identifiers:
                    continue
                identifiers.add(id(current))
                if type(current) is dict:
                    stack.extend(current.keys())
                    stack.extend(current.values())
                else:
                    stack.extend(current)
            elif type(current) is tuple:
                stack.extend(current)
        return identifiers

    def assert_fresh_pair(
        first,
        second,
        *,
        caller,
        expected_caller,
        family_key,
        expected_family,
        nested_key,
    ):
        assert first[family_key] == expected_family
        assert second[family_key] == expected_family
        assert first is not second
        assert first["source"] is not second["source"]
        assert first[nested_key] is not second[nested_key]
        caller_mutables = mutable_container_ids(caller)
        assert mutable_container_ids(first).isdisjoint(caller_mutables)
        assert mutable_container_ids(second).isdisjoint(caller_mutables)
        assert caller == expected_caller
        first["source"]["boundary_scope"] = "mutated-first-source"
        first[nested_key]["test_mutation"] = "first-only"
        assert second["source"] == SOURCE
        assert "test_mutation" not in second[nested_key]
        assert caller == expected_caller

    def assert_fresh_pair_without_diagnostics(first, second, **kwargs):
        assert first["diagnostic_records"] == ()
        assert second["diagnostic_records"] == ()
        assert_fresh_pair(first, second, **kwargs)

    def assert_fresh_pair_with_diagnostics(first, second, **kwargs):
        assert first["diagnostic_records"]
        assert second["diagnostic_records"]
        assert first["diagnostic_records"] is not second["diagnostic_records"]
        assert first["diagnostic_records"][0] is not second[
            "diagnostic_records"
        ][0]
        expected_second_record = dict(second["diagnostic_records"][0])
        assert_fresh_pair(first, second, **kwargs)
        first["diagnostic_records"][0]["field"] = "mutated-first-field"
        assert second["diagnostic_records"][0] == expected_second_record
        assert kwargs["caller"] == kwargs["expected_caller"]

    def build(caller):
        return sut.build_run_ledger_persistence_artifact(
            run_ledger_entry_assembly=caller,
        )

    def persist(caller, root):
        return sut.persist_run_ledger_entry(
            run_ledger_entry_assembly=caller,
            authorized_ops_root=str(root),
        )

    artifact_built_caller = _success_envelope()
    artifact_built_expected = _success_envelope()
    artifact_built_first = build(artifact_built_caller)
    artifact_built_second = build(artifact_built_caller)

    artifact_not_eligible_caller = _blocked_envelope()
    artifact_not_eligible_expected = _blocked_envelope()
    artifact_not_eligible_first = build(artifact_not_eligible_caller)
    artifact_not_eligible_second = build(artifact_not_eligible_caller)

    artifact_invalid_caller = {"bad": ["value"]}
    artifact_invalid_expected = {"bad": ["value"]}
    artifact_invalid_first = build(artifact_invalid_caller)
    artifact_invalid_second = build(artifact_invalid_caller)

    artifact_serialization_caller = _success_envelope()
    artifact_serialization_expected = _success_envelope()
    with monkeypatch.context() as patcher:
        def fail_serialization(*args, **kwargs):
            del args, kwargs
            raise TypeError("private serialization detail")

        patcher.setattr(json, "dumps", fail_serialization)
        artifact_serialization_first = build(artifact_serialization_caller)
        artifact_serialization_second = build(artifact_serialization_caller)

    persistence_written_caller = _success_envelope()
    persistence_written_expected = _success_envelope()
    written_root_one = _ops_root(tmp_path / "fresh-written-one")
    written_root_two = _ops_root(tmp_path / "fresh-written-two")
    persistence_written_first = persist(
        persistence_written_caller,
        written_root_one,
    )
    persistence_written_second = persist(
        persistence_written_caller,
        written_root_two,
    )

    persistence_identical_caller = _success_envelope()
    persistence_identical_expected = _success_envelope()
    identical_root_one = _ops_root(tmp_path / "fresh-identical-one")
    identical_root_two = _ops_root(tmp_path / "fresh-identical-two")
    assert _persist(tmp_path, root=identical_root_one)[
        "persistence_status"
    ] == "WRITTEN"
    assert _persist(tmp_path, root=identical_root_two)[
        "persistence_status"
    ] == "WRITTEN"
    persistence_identical_first = persist(
        persistence_identical_caller,
        identical_root_one,
    )
    persistence_identical_second = persist(
        persistence_identical_caller,
        identical_root_two,
    )

    persistence_not_eligible_caller = _blocked_envelope()
    persistence_not_eligible_expected = _blocked_envelope()
    persistence_not_eligible_first = persist(
        persistence_not_eligible_caller,
        "/not-inspected-not-eligible-one",
    )
    persistence_not_eligible_second = persist(
        persistence_not_eligible_caller,
        "/not-inspected-not-eligible-two",
    )

    persistence_invalid_caller = {"bad": ["value"]}
    persistence_invalid_expected = {"bad": ["value"]}
    persistence_invalid_first = persist(
        persistence_invalid_caller,
        "/not-inspected-invalid-one",
    )
    persistence_invalid_second = persist(
        persistence_invalid_caller,
        "/not-inspected-invalid-two",
    )

    persistence_authorization_caller = _success_envelope()
    persistence_authorization_expected = _success_envelope()
    persistence_authorization_first = persist(
        persistence_authorization_caller,
        str(tmp_path) + "//invalid-root-one",
    )
    persistence_authorization_second = persist(
        persistence_authorization_caller,
        str(tmp_path) + "//invalid-root-two",
    )

    persistence_serialization_caller = _success_envelope()
    persistence_serialization_expected = _success_envelope()
    with monkeypatch.context() as patcher:
        patcher.setattr(json, "dumps", fail_serialization)
        persistence_serialization_first = persist(
            persistence_serialization_caller,
            "/not-inspected-serialization-one",
        )
        persistence_serialization_second = persist(
            persistence_serialization_caller,
            "/not-inspected-serialization-two",
        )

    persistence_conflict_caller = _success_envelope()
    persistence_conflict_caller["source"]["source_of_truth"] = ("changed",)
    persistence_conflict_caller["run_ledger_entry"]["source_of_truth"] = (
        "changed",
    )
    persistence_conflict_expected = _success_envelope()
    persistence_conflict_expected["source"]["source_of_truth"] = (
        "changed",
    )
    persistence_conflict_expected["run_ledger_entry"]["source_of_truth"] = (
        "changed",
    )
    conflict_root_one = _ops_root(tmp_path / "fresh-conflict-one")
    conflict_root_two = _ops_root(tmp_path / "fresh-conflict-two")
    assert _persist(tmp_path, root=conflict_root_one)[
        "persistence_status"
    ] == "WRITTEN"
    assert _persist(tmp_path, root=conflict_root_two)[
        "persistence_status"
    ] == "WRITTEN"
    persistence_conflict_first = persist(
        persistence_conflict_caller,
        conflict_root_one,
    )
    persistence_conflict_second = persist(
        persistence_conflict_caller,
        conflict_root_two,
    )

    persistence_io_caller = _success_envelope()
    persistence_io_expected = _success_envelope()
    io_root_one = _ops_root(tmp_path / "fresh-io-one")
    io_root_two = _ops_root(tmp_path / "fresh-io-two")
    with monkeypatch.context() as patcher:
        def fail_open(*args, **kwargs):
            del args, kwargs
            raise OSError(errno.EIO, "private open detail")

        patcher.setattr(sut, "_os_open", fail_open)
        persistence_io_first = persist(persistence_io_caller, io_root_one)
        persistence_io_second = persist(persistence_io_caller, io_root_two)

    persistence_durability_caller = _success_envelope()
    persistence_durability_expected = _success_envelope()
    durability_root_one = _ops_root(tmp_path / "fresh-durability-one")
    durability_root_two = _ops_root(tmp_path / "fresh-durability-two")
    assert _persist(tmp_path, root=durability_root_one)[
        "persistence_status"
    ] == "WRITTEN"
    assert _persist(tmp_path, root=durability_root_two)[
        "persistence_status"
    ] == "WRITTEN"
    with monkeypatch.context() as patcher:
        target_fds = []
        original_open = sut._os_open
        original_fsync = sut._os_fsync

        def track_open(path, *args, **kwargs):
            fd = original_open(path, *args, **kwargs)
            if path == "run-ledger.yaml":
                target_fds.append(fd)
            return fd

        def fail_target_fsync(fd):
            if fd in target_fds:
                raise OSError(errno.EIO, "private fsync detail")
            return original_fsync(fd)

        patcher.setattr(sut, "_os_open", track_open)
        patcher.setattr(sut, "_os_fsync", fail_target_fsync)
        persistence_durability_first = persist(
            persistence_durability_caller,
            durability_root_one,
        )
        persistence_durability_second = persist(
            persistence_durability_caller,
            durability_root_two,
        )

    persistence_cleanup_caller = _success_envelope()
    persistence_cleanup_expected = _success_envelope()
    cleanup_root_one = _ops_root(tmp_path / "fresh-cleanup-one")
    cleanup_root_two = _ops_root(tmp_path / "fresh-cleanup-two")
    with monkeypatch.context() as patcher:
        def fail_unlink(*args, **kwargs):
            del args, kwargs
            raise OSError(errno.EIO, "private unlink detail")

        patcher.setattr(sut, "_os_unlink", fail_unlink)
        persistence_cleanup_first = persist(
            persistence_cleanup_caller,
            cleanup_root_one,
        )
        persistence_cleanup_second = persist(
            persistence_cleanup_caller,
            cleanup_root_two,
        )

    assert_fresh_pair_without_diagnostics(
        artifact_built_first,
        artifact_built_second,
        caller=artifact_built_caller,
        expected_caller=artifact_built_expected,
        family_key="artifact_status",
        expected_family="BUILT",
        nested_key="persistence_artifact",
    )
    assert_fresh_pair_with_diagnostics(
        artifact_not_eligible_first,
        artifact_not_eligible_second,
        caller=artifact_not_eligible_caller,
        expected_caller=artifact_not_eligible_expected,
        family_key="artifact_status",
        expected_family="NOT_ELIGIBLE",
        nested_key="persistence_artifact",
    )
    assert_fresh_pair_with_diagnostics(
        artifact_invalid_first,
        artifact_invalid_second,
        caller=artifact_invalid_caller,
        expected_caller=artifact_invalid_expected,
        family_key="artifact_status",
        expected_family="INVALID",
        nested_key="persistence_artifact",
    )
    assert_fresh_pair_with_diagnostics(
        artifact_serialization_first,
        artifact_serialization_second,
        caller=artifact_serialization_caller,
        expected_caller=artifact_serialization_expected,
        family_key="artifact_status",
        expected_family="SERIALIZATION_FAILED",
        nested_key="persistence_artifact",
    )
    assert_fresh_pair_without_diagnostics(
        persistence_written_first,
        persistence_written_second,
        caller=persistence_written_caller,
        expected_caller=persistence_written_expected,
        family_key="persistence_status",
        expected_family="WRITTEN",
        nested_key="persistence_evidence",
    )
    assert_fresh_pair_without_diagnostics(
        persistence_identical_first,
        persistence_identical_second,
        caller=persistence_identical_caller,
        expected_caller=persistence_identical_expected,
        family_key="persistence_status",
        expected_family="ALREADY_IDENTICAL",
        nested_key="persistence_evidence",
    )
    assert_fresh_pair_with_diagnostics(
        persistence_not_eligible_first,
        persistence_not_eligible_second,
        caller=persistence_not_eligible_caller,
        expected_caller=persistence_not_eligible_expected,
        family_key="persistence_status",
        expected_family="NOT_ELIGIBLE",
        nested_key="persistence_evidence",
    )
    assert_fresh_pair_with_diagnostics(
        persistence_invalid_first,
        persistence_invalid_second,
        caller=persistence_invalid_caller,
        expected_caller=persistence_invalid_expected,
        family_key="persistence_status",
        expected_family="INVALID",
        nested_key="persistence_evidence",
    )
    assert_fresh_pair_with_diagnostics(
        persistence_authorization_first,
        persistence_authorization_second,
        caller=persistence_authorization_caller,
        expected_caller=persistence_authorization_expected,
        family_key="persistence_status",
        expected_family="AUTHORIZATION_FAILED",
        nested_key="persistence_evidence",
    )
    assert_fresh_pair_with_diagnostics(
        persistence_serialization_first,
        persistence_serialization_second,
        caller=persistence_serialization_caller,
        expected_caller=persistence_serialization_expected,
        family_key="persistence_status",
        expected_family="SERIALIZATION_FAILED",
        nested_key="persistence_evidence",
    )
    assert_fresh_pair_with_diagnostics(
        persistence_conflict_first,
        persistence_conflict_second,
        caller=persistence_conflict_caller,
        expected_caller=persistence_conflict_expected,
        family_key="persistence_status",
        expected_family="CONFLICT",
        nested_key="persistence_evidence",
    )
    assert_fresh_pair_with_diagnostics(
        persistence_io_first,
        persistence_io_second,
        caller=persistence_io_caller,
        expected_caller=persistence_io_expected,
        family_key="persistence_status",
        expected_family="IO_FAILED",
        nested_key="persistence_evidence",
    )
    assert_fresh_pair_with_diagnostics(
        persistence_durability_first,
        persistence_durability_second,
        caller=persistence_durability_caller,
        expected_caller=persistence_durability_expected,
        family_key="persistence_status",
        expected_family="DURABILITY_UNCONFIRMED",
        nested_key="persistence_evidence",
    )
    assert_fresh_pair_with_diagnostics(
        persistence_cleanup_first,
        persistence_cleanup_second,
        caller=persistence_cleanup_caller,
        expected_caller=persistence_cleanup_expected,
        family_key="persistence_status",
        expected_family="PERSISTED_CLEANUP_WARNING",
        nested_key="persistence_evidence",
    )


def test_absolute_root_and_temp_name_are_suppressed_after_reached_io_path(monkeypatch, tmp_path):
    root = _ops_root(tmp_path)
    name = ".run-ledger.tmp-deaddeaddeaddeaddeaddeaddeaddead"
    reached = []
    original_open = sut._os_open

    def fail(path, *args, **kwargs):
        if path == name:
            reached.append(path)
            raise OSError(errno.EIO, str(root) + "/" + name)
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(sut, "_new_temp_name", lambda: name)
    monkeypatch.setattr(sut, "_os_open", fail)
    result = _persist(tmp_path, root=root)
    assert reached == [name]
    assert result["persistence_status"] == "IO_FAILED"
    rendered = str(result)
    assert str(root) not in rendered and name not in rendered


def test_exception_errno_and_temp_details_are_suppressed_after_reached_cleanup_path(monkeypatch, tmp_path):
    detail = "errno=5 private-temp-detail"
    reached = []

    def fail_unlink(*args, **kwargs):
        reached.append((args, kwargs))
        raise OSError(errno.EIO, detail)

    monkeypatch.setattr(sut, "_os_unlink", fail_unlink)
    result = _persist(tmp_path)
    assert reached
    assert result["persistence_status"] == "PERSISTED_CLEANUP_WARNING"
    assert detail not in str(result)


def test_persistence_never_imports_runtime_transition_gate_publish_or_notification():
    imported_modules = {
        value.__name__ for value in vars(sut).values() if isinstance(value, types.ModuleType)
    }
    assert imported_modules == {"os"}
    tree = ast.parse(inspect.getsource(sut))
    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    forbidden = {
        "runtime", "transition", "gate", "publisher", "publication",
        "notifier", "notification", "requests", "httpx", "subprocess",
    }
    assert imported.isdisjoint(forbidden)


def test_no_quality_pass_no_public_url_and_pass_published_forbidden():
    assert "P2D45_P_PERSISTENCE_NOT_QUALITY_PASS" in INVARIANTS
    assert "P2D45_P_NO_PUBLIC_URL" in INVARIANTS
    assert "P2D45_P_PASS_PUBLISHED_FORBIDDEN" in INVARIANTS
    assert "P2D45_P_PERSISTENCE_NOT_NOTIFICATION" in INVARIANTS
    assert "PASS_PUBLISHED" not in ARTIFACT_STATUSES
    assert "PASS_PUBLISHED" not in PERSISTENCE_STATUSES
    assert "NOOP_COMPLETED" not in ARTIFACT_STATUSES
    assert "NOOP_COMPLETED" not in PERSISTENCE_STATUSES


def test_noop_completed_remains_metadata_only_in_built_and_persisted_results(tmp_path):
    artifact = _artifact()
    assert artifact["artifact_status"] == "BUILT"
    assert artifact["persistence_artifact"]["serialized_content"] == GOLDEN_BYTES
    result = _persist(tmp_path)
    assert result["persistence_status"] == "WRITTEN"
    assert result["run_ledger_persisted"] is True
    assert "NOOP_COMPLETED" not in result["persistence_evidence"].values()
    assert "quality_pass" not in result and "public_url" not in result


def test_different_entry_ids_with_same_run_id_use_distinct_paths():
    first_result = _artifact()
    assert first_result["artifact_status"] == "BUILT"
    assert first_result["persistence_artifact_built"] is True
    first_artifact = first_result["persistence_artifact"]
    assert tuple(first_artifact) == PERSISTENCE_ARTIFACT_KEYS
    first = first_artifact["artifact_relative_path"]

    second_envelope = _success_envelope()
    second_envelope["source"]["run_ledger_entry_id"] = "ledger-entry-002"
    second_envelope["run_ledger_entry"]["run_ledger_entry_id"] = "ledger-entry-002"
    second_result = _artifact(second_envelope)
    assert second_result["artifact_status"] == "BUILT"
    assert second_result["persistence_artifact_built"] is True
    second_artifact = second_result["persistence_artifact"]
    assert tuple(second_artifact) == PERSISTENCE_ARTIFACT_KEYS
    second = second_artifact["artifact_relative_path"]
    assert first == "runs/by-entry-id/sha256-" + ENTRY_ID_DIGEST + "/run-ledger.yaml"
    assert second == "runs/by-entry-id/sha256-" + SECOND_ENTRY_ID_DIGEST + "/run-ledger.yaml"
    assert first != second


def test_same_entry_id_with_different_content_conflicts(tmp_path):
    root = _ops_root(tmp_path)
    first = _persist(tmp_path, root=root)
    changed = _success_envelope()
    changed["source"]["source_of_truth"] = ("changed",)
    changed["run_ledger_entry"]["source_of_truth"] = ("changed",)
    second = _persist(tmp_path, envelope=changed, root=root)
    assert first["persistence_status"] == "WRITTEN"
    assert second["persistence_status"] == "CONFLICT"
    assert second["reason_code"] == "RUN_LEDGER_CONFLICT"
    assert second["run_ledger_persisted"] is False


def test_no_filesystem_type_detection_is_claimed():
    assert "P2D45_P_LOCAL_POSIX_ROOT_EXTERNALLY_ATTESTED" in INVARIANTS
    assert "P2D45_P_NO_NETWORK_FILESYSTEM_DETECTION_CLAIM" in INVARIANTS
    namespace = set(vars(sut))
    assert {"statfs", "statvfs", "mount", "findmnt", "diskutil"}.isdisjoint(namespace)
