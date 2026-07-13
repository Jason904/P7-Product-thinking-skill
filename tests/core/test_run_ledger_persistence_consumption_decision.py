"""Frozen 44-test contract for the P2D-46 decision boundary."""

import ast
import inspect

from ai_daily_publishing_system.core import (
    run_ledger_persistence_consumption_decision as sut,
)


RESULT_KEYS = (
    "decision_created", "decision_status", "accepted", "warning",
    "reason_code", "reason", "source", "persistence_evidence",
    "decision_violations", "missing_or_invalid_fields",
    "diagnostic_records", "invariant_refs",
)
SOURCE_KEYS = (
    "boundary_scope", "schema_version", "upstream_boundary_scope",
    "upstream_schema_version", "upstream_artifact_name",
    "upstream_persistence_status", "upstream_reason_code",
    "upstream_write_disposition",
)
SAFE_EVIDENCE_KEYS = (
    "artifact_relative_path", "serialization_format",
    "content_digest_algorithm", "content_digest", "write_disposition",
)
DECISION_STATUSES = (
    "PERSISTENCE_ACCEPTED", "PERSISTENCE_ACCEPTED_WITH_WARNING",
    "PERSISTENCE_NOT_ACCEPTED", "PERSISTENCE_RESULT_INVALID",
)
BOOLEAN_MATRIX = (
    ("PERSISTENCE_ACCEPTED", True, True, False),
    ("PERSISTENCE_ACCEPTED_WITH_WARNING", True, True, True),
    ("PERSISTENCE_NOT_ACCEPTED", True, False, False),
    ("PERSISTENCE_RESULT_INVALID", False, False, False),
)
P2D46_REASON_CODES = (
    "P2D46_WRITTEN_ACCEPTED", "P2D46_ALREADY_IDENTICAL_ACCEPTED",
    "P2D46_NOT_ELIGIBLE_REJECTED", "P2D46_UPSTREAM_INVALID_REJECTED",
    "P2D46_AUTHORIZATION_FAILED_REJECTED",
    "P2D46_SERIALIZATION_FAILED_REJECTED", "P2D46_CONFLICT_REJECTED",
    "P2D46_IO_FAILED_REJECTED", "P2D46_DURABILITY_UNCONFIRMED_REJECTED",
    "P2D46_CLEANUP_WARNING_ACCEPTED", "P2D46_RESULT_NOT_EXACT_DICT",
    "P2D46_FORBIDDEN_BYPASS", "P2D46_RESULT_KEYS_INVALID",
    "P2D46_RESULT_FIELD_TYPE_INVALID", "P2D46_SOURCE_CONTRACT_INVALID",
    "P2D46_EVIDENCE_CONTRACT_INVALID", "P2D46_STATUS_UNKNOWN",
    "P2D46_REASON_CONTRACT_INVALID", "P2D46_VIOLATIONS_CONTRACT_INVALID",
    "P2D46_FIELDS_CONTRACT_INVALID", "P2D46_DIAGNOSTICS_CONTRACT_INVALID",
    "P2D46_INVARIANTS_CONTRACT_INVALID", "P2D46_COHERENCE_INVALID",
)
VALIDATION_REASONS = P2D46_REASON_CODES[10:]
P2D46_REASON_STRINGS = (
    ("P2D46_WRITTEN_ACCEPTED", "The coherent P2D-45 WRITTEN result was accepted as durable run-ledger persistence."),
    ("P2D46_ALREADY_IDENTICAL_ACCEPTED", "The coherent P2D-45 ALREADY_IDENTICAL result was accepted as durable run-ledger persistence."),
    ("P2D46_NOT_ELIGIBLE_REJECTED", "The coherent P2D-45 NOT_ELIGIBLE result was not accepted as persistence."),
    ("P2D46_UPSTREAM_INVALID_REJECTED", "The coherent P2D-45 INVALID result was not accepted as persistence."),
    ("P2D46_AUTHORIZATION_FAILED_REJECTED", "The coherent P2D-45 AUTHORIZATION_FAILED result was not accepted as persistence."),
    ("P2D46_SERIALIZATION_FAILED_REJECTED", "The coherent P2D-45 SERIALIZATION_FAILED result was not accepted as persistence."),
    ("P2D46_CONFLICT_REJECTED", "The coherent P2D-45 CONFLICT result was not accepted as persistence."),
    ("P2D46_IO_FAILED_REJECTED", "The coherent P2D-45 IO_FAILED result was not accepted as persistence."),
    ("P2D46_DURABILITY_UNCONFIRMED_REJECTED", "The coherent P2D-45 DURABILITY_UNCONFIRMED result was not accepted as persistence."),
    ("P2D46_CLEANUP_WARNING_ACCEPTED", "The coherent P2D-45 cleanup-warning result was accepted as persisted with warning."),
    ("P2D46_RESULT_NOT_EXACT_DICT", "The P2D-45 persistence result must be an exact built-in dict."),
    ("P2D46_FORBIDDEN_BYPASS", "A forbidden persistence-result bypass shape was supplied."),
    ("P2D46_RESULT_KEYS_INVALID", "The P2D-45 persistence result must contain the exact ordered result keys."),
    ("P2D46_RESULT_FIELD_TYPE_INVALID", "A P2D-45 persistence result scalar field has an invalid exact type."),
    ("P2D46_SOURCE_CONTRACT_INVALID", "The P2D-45 persistence source contract is invalid or incompatible."),
    ("P2D46_EVIDENCE_CONTRACT_INVALID", "The P2D-45 persistence evidence contract is invalid."),
    ("P2D46_STATUS_UNKNOWN", "The P2D-45 persistence status is unknown."),
    ("P2D46_REASON_CONTRACT_INVALID", "The P2D-45 reason code or fixed reason text is invalid."),
    ("P2D46_VIOLATIONS_CONTRACT_INVALID", "The P2D-45 persistence violation tuple is invalid."),
    ("P2D46_FIELDS_CONTRACT_INVALID", "The P2D-45 missing-or-invalid field tuple is invalid."),
    ("P2D46_DIAGNOSTICS_CONTRACT_INVALID", "The P2D-45 diagnostic record tuple is invalid."),
    ("P2D46_INVARIANTS_CONTRACT_INVALID", "The P2D-45 invariant reference tuple is invalid."),
    ("P2D46_COHERENCE_INVALID", "The complete P2D-45 persistence result is internally incoherent."),
)
DIAGNOSTIC_PATHS = (
    "run_ledger_persistence_result", "p2d46.forbidden_bypass",
    "run_ledger_persistence_result.keys",
    "run_ledger_persistence_result.scalar_fields",
    "run_ledger_persistence_result.source",
    "run_ledger_persistence_result.persistence_evidence",
    "run_ledger_persistence_result.persistence_status",
    "run_ledger_persistence_result.reason_contract",
    "run_ledger_persistence_result.persistence_violations",
    "run_ledger_persistence_result.missing_or_invalid_fields",
    "run_ledger_persistence_result.diagnostic_records",
    "run_ledger_persistence_result.invariant_refs",
    "run_ledger_persistence_result.coherence",
)
BYPASS_SIGNATURES = (
    "run_ledger_persistence_result", "normalized_run_ledger_persistence_result",
    "run_ledger_entry_assembly", "run_ledger_entry_assembled",
    "run_ledger_entry", "persistence_artifact_built", "artifact_status",
    "persistence_artifact", "serialized_content", "authorized_ops_root",
)
P2D46_INVARIANTS = (
    "P2D46_P_COMPLETE_P2D45_RESULT_REQUIRED",
    "P2D46_P_PURE_IN_MEMORY_DECISION",
    "P2D46_P_EXACT_UPSTREAM_COHERENCE_REQUIRED",
    "P2D46_P_STATUS_ALONE_INSUFFICIENT",
    "P2D46_P_LEDGER_PERSISTED_NOT_RUN_COMPLETED",
    "P2D46_P_NO_TRANSITION_AUTHORITY", "P2D46_P_NO_RUNTIME_EXECUTION",
    "P2D46_P_NO_QUALITY_PASS", "P2D46_P_NO_PUBLIC_URL",
    "P2D46_P_PASS_PUBLISHED_FORBIDDEN", "P2D46_P_NOTIFICATION_FORBIDDEN",
    "P2D46_P_PERSISTED_CLEANUP_WARNING_REMAINS_WARNING",
    "P2D46_P_DURABILITY_UNCONFIRMED_NEVER_ACCEPTED_AS_SUCCESS",
    "P2D46_P_BLOCKED_UPSTREAM_FAILS_CLOSED",
    "P2D46_P_MALFORMED_UPSTREAM_INVALID", "P2D46_P_RESULT_MUST_BE_FRESH",
    "P2D46_P_CALLER_DATA_SUPPRESSED", "P2D46_P_SAFE_EVIDENCE_ALLOWLIST_ONLY",
    "P2D46_P_UNKNOWN_KEYS_REJECTED_AND_SUPPRESSED",
    "P2D46_P_BYPASS_FORBIDDEN", "P2D46_P_NO_UPSTREAM_INVOCATION",
    "P2D46_P_NO_FILESYSTEM_OR_OPS_ROOT", "P2D46_P_NO_RETRY_EXECUTION",
    "P2D46_P_DOWNSTREAM_INSPECTION_DECLARATIVE_ONLY",
)
PROHIBITED_STATUSES = (
    "RUN_COMPLETED", "COMPLETED", "TRANSITIONED", "PASS",
    "PASS_PUBLISHED", "PUBLISHED", "NOOP_COMPLETED", "PUBLISH_ALLOWED",
)

P2D45_RESULT_KEYS = (
    "run_ledger_persisted", "persistence_status", "reason_code", "reason",
    "source", "persistence_evidence", "persistence_violations",
    "missing_or_invalid_fields", "diagnostic_records", "invariant_refs",
)
P2D45_SOURCE_KEYS = (
    "boundary_scope", "schema_version", "artifact_name",
    "serialization_format", "content_digest_algorithm",
)
P2D45_SOURCE = (
    ("boundary_scope", "run_ledger_persistence_boundary"),
    ("schema_version", "p2d45.run_ledger_persistence.v1"),
    ("artifact_name", "run-ledger.yaml"),
    ("serialization_format", "canonical_json_yaml_1_2_subset"),
    ("content_digest_algorithm", "sha256"),
)
P2D45_EVIDENCE_KEYS = (
    "run_ledger_entry_id", "run_id", "artifact_relative_path",
    "serialization_format", "content_digest_algorithm", "content_digest",
    "write_disposition",
)
P2D45_STATUSES = (
    "WRITTEN", "ALREADY_IDENTICAL", "NOT_ELIGIBLE", "INVALID",
    "AUTHORIZATION_FAILED", "SERIALIZATION_FAILED", "CONFLICT", "IO_FAILED",
    "DURABILITY_UNCONFIRMED", "PERSISTED_CLEANUP_WARNING",
)
P2D45_DISPOSITIONS = ("WRITTEN", "ALREADY_IDENTICAL", "DURABILITY_UNCONFIRMED")
P2D45_STATUS_CONTRACT = (
    ("WRITTEN", True, ("WRITTEN",), True, ("RUN_LEDGER_PERSISTED",)),
    ("ALREADY_IDENTICAL", True, ("ALREADY_IDENTICAL",), True, ("RUN_LEDGER_ALREADY_PERSISTED_IDENTICAL",)),
    ("NOT_ELIGIBLE", False, (), False, ("P2D45A_ENVELOPE_NOT_ELIGIBLE",)),
    ("INVALID", False, (), False, ("P2D45A_SUCCESS_ENVELOPE_INVALID",)),
    ("AUTHORIZATION_FAILED", False, (), False, ("DESTINATION_ROOT_INVALID", "DESTINATION_PATH_UNSAFE")),
    ("SERIALIZATION_FAILED", False, (), False, ("RUN_LEDGER_SERIALIZATION_FAILED",)),
    ("CONFLICT", False, (), False, ("RUN_LEDGER_CONFLICT",)),
    ("IO_FAILED", False, (), False, (
        "FILESYSTEM_CAPABILITY_UNAVAILABLE", "EXISTING_TARGET_INSPECTION_FAILED",
        "PRE_FINALIZATION_IO_FAILED", "TEMP_NAME_GENERATION_FAILED",
        "TEMP_FILE_CREATE_FAILED", "TEMP_INODE_VALIDATION_FAILED",
        "TEMP_FILE_WRITE_FAILED", "TEMP_FILE_FSYNC_FAILED", "ATOMIC_CREATE_FAILED",
    )),
    ("DURABILITY_UNCONFIRMED", False, ("DURABILITY_UNCONFIRMED",), True, (
        "FINAL_IDENTITY_VERIFICATION_FAILED", "FINAL_DURABILITY_UNCONFIRMED",
    )),
    ("PERSISTED_CLEANUP_WARNING", True, ("WRITTEN", "ALREADY_IDENTICAL"), True, ("PERSISTED_CLEANUP_WARNING",)),
)
P2D45_REASON_CODES = (
    "P2D45A_SUCCESS_ENVELOPE_INVALID", "P2D45A_ENVELOPE_NOT_ELIGIBLE",
    "RUN_LEDGER_SERIALIZATION_FAILED", "DESTINATION_ROOT_INVALID",
    "DESTINATION_PATH_UNSAFE", "FILESYSTEM_CAPABILITY_UNAVAILABLE",
    "EXISTING_TARGET_INSPECTION_FAILED", "RUN_LEDGER_CONFLICT",
    "PRE_FINALIZATION_IO_FAILED", "TEMP_NAME_GENERATION_FAILED",
    "TEMP_FILE_CREATE_FAILED", "TEMP_INODE_VALIDATION_FAILED",
    "TEMP_FILE_WRITE_FAILED", "TEMP_FILE_FSYNC_FAILED", "ATOMIC_CREATE_FAILED",
    "FINAL_IDENTITY_VERIFICATION_FAILED", "FINAL_DURABILITY_UNCONFIRMED",
    "FINAL_INSPECTION_CLOSE_FAILED", "TEMP_FILE_CLOSE_FAILED",
    "TEMP_CLEANUP_FAILED", "PERSISTED_CLEANUP_WARNING",
    "RUN_LEDGER_PERSISTENCE_ARTIFACT_BUILT",
    "RUN_LEDGER_ALREADY_PERSISTED_IDENTICAL", "RUN_LEDGER_PERSISTED",
)
P2D45_REASON_STRINGS = (
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
P2D45_PATHS = (
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
P2D45_INVARIANTS = (
    "P2D45_P_COMPLETE_ENVELOPE_TRUST_BOUNDARY", "P2D45_P_EXACT_SUCCESS_REQUIRED",
    "P2D45_P_NESTED_ENTRY_BYPASS_FORBIDDEN", "P2D45_P_CALLER_BYTES_FORBIDDEN",
    "P2D45_P_PURE_ARTIFACT_BUILDER", "P2D45_P_EXPLICIT_EFFECT_API",
    "P2D45_P_CANONICAL_JSON_YAML12_SUBSET", "P2D45_P_UTF8_ONE_FINAL_LF",
    "P2D45_P_SHA256_EXACT_BYTES", "P2D45_P_NO_SEMANTIC_MUTATION",
    "P2D45_P_AUTHORIZED_ROOT_EXPLICIT", "P2D45_P_NO_CWD_DESTINATION",
    "P2D45_P_NO_ENV_DESTINATION", "P2D45_P_ROOT_COMPONENT_NOFOLLOW",
    "P2D45_P_ROOT_DESCRIPTOR_CAPABILITY", "P2D45_P_PREPROVISIONED_LEDGER_PARENTS",
    "P2D45_P_HASHED_ENTRY_DIRECTORY", "P2D45_P_RELATIVE_RESULT_PATH_ONLY",
    "P2D45_P_NO_PATH_ESCAPE", "P2D45_P_NO_SYMLINK_ESCAPE",
    "P2D45_P_TEMP_NAMESPACE_PRIVATE", "P2D45_P_TEMP_COLLISIONS_BOUNDED",
    "P2D45_P_TEMP_NAME_NEVER_EXPOSED", "P2D45_P_TEMP_REGULAR_FILE_REQUIRED",
    "P2D45_P_TEMP_DESCRIPTOR_STAYS_OPEN", "P2D45_P_TEMP_IDENTITY_STABLE",
    "P2D45_P_COMPLETE_SHORT_WRITE_LOOP", "P2D45_P_TEMP_FSYNC_BEFORE_LINK",
    "P2D45_P_CREATE_ONLY_HARD_LINK", "P2D45_P_NO_OVERWRITE_FALLBACK",
    "P2D45_P_FINAL_TEMP_INODE_CONTINUITY", "P2D45_P_FINAL_SIZE_CONTINUITY",
    "P2D45_P_FINAL_DIRECTORY_FSYNC_REQUIRED", "P2D45_P_POST_FSYNC_FINAL_REVALIDATION",
    "P2D45_P_EXISTING_READ_BOUNDED", "P2D45_P_EXISTING_IDENTITY_STABLE",
    "P2D45_P_IDENTICAL_BYTES_IDEMPOTENT", "P2D45_P_DIFFERENT_BYTES_CONFLICT",
    "P2D45_P_NO_PARTIAL_FINAL_FILE", "P2D45_P_DURABILITY_UNCERTAINTY_EXPLICIT",
    "P2D45_P_DURABLE_CLEANUP_WARNING_PRESERVES_TRUTH",
    "P2D45_P_MULTI_VIOLATIONS_DETERMINISTIC", "P2D45_P_NO_EXCEPTION_TEXT",
    "P2D45_P_NO_ABSOLUTE_PATH_LEAKAGE", "P2D45_P_NO_OS_ERROR_LEAKAGE",
    "P2D45_P_NO_ORPHAN_SCAN_AUTHORITY", "P2D45_P_LOCAL_POSIX_ROOT_EXTERNALLY_ATTESTED",
    "P2D45_P_NO_NETWORK_FILESYSTEM_DETECTION_CLAIM", "P2D45_P_PERSISTENCE_NOT_RUNTIME",
    "P2D45_P_PERSISTENCE_NOT_TRANSITION", "P2D45_P_PERSISTENCE_NOT_QUALITY_PASS",
    "P2D45_P_PERSISTENCE_NOT_PUBLICATION", "P2D45_P_NO_PUBLIC_URL",
    "P2D45_P_NOOP_COMPLETED_IS_METADATA_ONLY", "P2D45_P_PASS_PUBLISHED_FORBIDDEN",
    "P2D45_P_PERSISTENCE_NOT_NOTIFICATION",
)
AUTH_GRAMMAR = (
    ("DESTINATION_ROOT_INVALID", ("PRE_FINALIZATION_IO_FAILED",)),
    ("DESTINATION_PATH_UNSAFE", (
        "PRE_FINALIZATION_IO_FAILED", "FINAL_INSPECTION_CLOSE_FAILED",
        "TEMP_FILE_CLOSE_FAILED", "TEMP_CLEANUP_FAILED",
    )),
)
IO_GRAMMAR = (
    ("FILESYSTEM_CAPABILITY_UNAVAILABLE", ()),
    ("EXISTING_TARGET_INSPECTION_FAILED", (
        "PRE_FINALIZATION_IO_FAILED", "FINAL_INSPECTION_CLOSE_FAILED",
        "TEMP_FILE_CLOSE_FAILED", "TEMP_CLEANUP_FAILED",
    )),
    ("PRE_FINALIZATION_IO_FAILED", ("TEMP_FILE_CLOSE_FAILED", "TEMP_CLEANUP_FAILED")),
    ("TEMP_NAME_GENERATION_FAILED", ("PRE_FINALIZATION_IO_FAILED",)),
    ("TEMP_FILE_CREATE_FAILED", ("PRE_FINALIZATION_IO_FAILED",)),
    ("TEMP_INODE_VALIDATION_FAILED", (
        "PRE_FINALIZATION_IO_FAILED", "TEMP_FILE_CLOSE_FAILED", "TEMP_CLEANUP_FAILED",
    )),
    ("TEMP_FILE_WRITE_FAILED", (
        "PRE_FINALIZATION_IO_FAILED", "TEMP_FILE_CLOSE_FAILED", "TEMP_CLEANUP_FAILED",
    )),
    ("TEMP_FILE_FSYNC_FAILED", (
        "PRE_FINALIZATION_IO_FAILED", "TEMP_FILE_CLOSE_FAILED", "TEMP_CLEANUP_FAILED",
    )),
    ("ATOMIC_CREATE_FAILED", (
        "PRE_FINALIZATION_IO_FAILED", "TEMP_FILE_CLOSE_FAILED", "TEMP_CLEANUP_FAILED",
    )),
)
DURABILITY_GRAMMAR = (
    ("FINAL_IDENTITY_VERIFICATION_FAILED", ("TEMP_CLEANUP_FAILED",), (
        "PRE_FINALIZATION_IO_FAILED", "FINAL_INSPECTION_CLOSE_FAILED",
        "TEMP_FILE_CLOSE_FAILED",
    )),
    ("FINAL_DURABILITY_UNCONFIRMED", (), (
        "PRE_FINALIZATION_IO_FAILED", "FINAL_INSPECTION_CLOSE_FAILED",
        "TEMP_FILE_CLOSE_FAILED", "TEMP_CLEANUP_FAILED",
    )),
)

ENTRY_DIGEST = "5ecbc192017833e40d812cac9daec51f310ef4b492502fb63ca0821588ce9b29"
RELATIVE_PATH = "runs/by-entry-id/sha256-" + ENTRY_DIGEST + "/run-ledger.yaml"


def _lookup(entries, key):
    for known, value in entries:
        if known == key:
            return value
    return ""


def _ordered(codes):
    return tuple(code for code in P2D45_REASON_CODES if code in codes)


def _fields(codes):
    values = ()
    for code in codes:
        paths = _lookup(P2D45_PATHS, code)
        for path in paths:
            if path not in values:
                values = values + (path,)
    return values


def _records(codes):
    values = ()
    for code in codes:
        for path in _lookup(P2D45_PATHS, code):
            values = values + ({"reason_code": code, "field": path},)
    return values


def _evidence(disposition):
    return {
        "run_ledger_entry_id": "ledger-entry-001",
        "run_id": "run-001",
        "artifact_relative_path": RELATIVE_PATH,
        "serialization_format": "canonical_json_yaml_1_2_subset",
        "content_digest_algorithm": "sha256",
        "content_digest": "a" * 64,
        "write_disposition": disposition,
    }


def _upstream(status, *, codes=None, disposition="", persisted=None):
    defaults = (
        ("WRITTEN", (), "RUN_LEDGER_PERSISTED", True, "WRITTEN"),
        ("ALREADY_IDENTICAL", (), "RUN_LEDGER_ALREADY_PERSISTED_IDENTICAL", True, "ALREADY_IDENTICAL"),
        ("NOT_ELIGIBLE", ("P2D45A_ENVELOPE_NOT_ELIGIBLE",), "P2D45A_ENVELOPE_NOT_ELIGIBLE", False, ""),
        ("INVALID", ("P2D45A_SUCCESS_ENVELOPE_INVALID",), "P2D45A_SUCCESS_ENVELOPE_INVALID", False, ""),
        ("AUTHORIZATION_FAILED", ("DESTINATION_ROOT_INVALID",), "DESTINATION_ROOT_INVALID", False, ""),
        ("SERIALIZATION_FAILED", ("RUN_LEDGER_SERIALIZATION_FAILED",), "RUN_LEDGER_SERIALIZATION_FAILED", False, ""),
        ("CONFLICT", ("RUN_LEDGER_CONFLICT",), "RUN_LEDGER_CONFLICT", False, ""),
        ("IO_FAILED", ("FILESYSTEM_CAPABILITY_UNAVAILABLE",), "FILESYSTEM_CAPABILITY_UNAVAILABLE", False, ""),
        ("DURABILITY_UNCONFIRMED", ("FINAL_DURABILITY_UNCONFIRMED",), "FINAL_DURABILITY_UNCONFIRMED", False, "DURABILITY_UNCONFIRMED"),
        ("PERSISTED_CLEANUP_WARNING", ("PERSISTED_CLEANUP_WARNING",), "PERSISTED_CLEANUP_WARNING", True, "WRITTEN"),
    )
    selected = ()
    for row in defaults:
        if row[0] == status:
            selected = row
    assert selected != ()
    selected_codes = selected[1] if codes is None else _ordered(codes)
    selected_reason = selected[2] if codes is None else selected_codes[0]
    selected_persisted = selected[3] if persisted is None else persisted
    selected_disposition = disposition or selected[4]
    evidence = _evidence(selected_disposition) if selected_disposition else {}
    return {
        "run_ledger_persisted": selected_persisted,
        "persistence_status": status,
        "reason_code": selected_reason,
        "reason": _lookup(P2D45_REASON_STRINGS, selected_reason),
        "source": {key: value for key, value in P2D45_SOURCE},
        "persistence_evidence": evidence,
        "persistence_violations": selected_codes,
        "missing_or_invalid_fields": _fields(selected_codes),
        "diagnostic_records": _records(selected_codes),
        "invariant_refs": tuple(value for value in P2D45_INVARIANTS),
    }


def _call(value):
    return sut.build_run_ledger_persistence_consumption_decision(
        run_ledger_persistence_result=value,
    )


def _assert_status(result, expected):
    assert type(result) is dict
    assert "decision_status" in result
    assert type(result["decision_status"]) is str
    assert result["decision_status"] == expected


def _assert_invalid(result, reason_code):
    _assert_status(result, "PERSISTENCE_RESULT_INVALID")
    assert "reason_code" in result
    assert result["reason_code"] == reason_code
    assert result["decision_created"] is False
    assert result["accepted"] is False
    assert result["warning"] is False


def test_public_api_signature_is_exact():
    signature = inspect.signature(
        sut.build_run_ledger_persistence_consumption_decision
    )
    assert tuple(signature.parameters) == ("run_ledger_persistence_result",)
    parameter = tuple(signature.parameters.values())[0]
    assert parameter.kind is inspect.Parameter.KEYWORD_ONLY
    assert parameter.default is inspect.Parameter.empty
    assert parameter.annotation == dict[str, object]
    assert signature.return_annotation == dict[str, object]


def test_contract_catalogs_and_key_orders_are_exact():
    assert sut.P2D46_RESULT_KEYS == RESULT_KEYS
    assert sut.P2D46_SOURCE_KEYS == SOURCE_KEYS
    assert sut.P2D46_SAFE_EVIDENCE_KEYS == SAFE_EVIDENCE_KEYS
    assert sut.P2D46_DECISION_STATUSES == DECISION_STATUSES
    assert sut.P2D46_BOOLEAN_MATRIX == BOOLEAN_MATRIX
    assert sut.P2D46_REASON_CODES == P2D46_REASON_CODES
    assert sut.P2D46_VALIDATION_REASON_CODES == VALIDATION_REASONS
    assert sut.P2D46_REASON_STRINGS == P2D46_REASON_STRINGS
    assert sut.P2D46_DIAGNOSTIC_PATHS == DIAGNOSTIC_PATHS
    assert sut.P2D46_FORBIDDEN_BYPASS_SIGNATURES == BYPASS_SIGNATURES
    assert sut.P2D46_INVARIANT_REFS == P2D46_INVARIANTS
    assert sut.P2D46_PROHIBITED_STATUS_VOCABULARY == PROHIBITED_STATUSES
    assert sut.P2D45_RESULT_KEYS == P2D45_RESULT_KEYS
    assert sut.P2D45_SOURCE_KEYS == P2D45_SOURCE_KEYS
    assert sut.P2D45_SOURCE_VALUES == P2D45_SOURCE
    assert sut.P2D45_EVIDENCE_KEYS == P2D45_EVIDENCE_KEYS
    assert sut.P2D45_STATUSES == P2D45_STATUSES
    assert sut.P2D45_WRITE_DISPOSITIONS == P2D45_DISPOSITIONS
    assert sut.P2D45_STATUS_CONTRACT == P2D45_STATUS_CONTRACT
    assert sut.P2D45_REASON_CODES == P2D45_REASON_CODES
    assert sut.P2D45_REASON_PRIORITY == P2D45_REASON_CODES
    assert sut.P2D45_REASON_STRINGS == P2D45_REASON_STRINGS
    assert sut.P2D45_DIAGNOSTIC_PATHS == P2D45_PATHS
    assert sut.P2D45_INVARIANT_REFS == P2D45_INVARIANTS
    assert sut.P2D45_AUTHORIZATION_GRAMMAR == AUTH_GRAMMAR
    assert sut.P2D45_IO_GRAMMAR == IO_GRAMMAR
    assert sut.P2D45_DURABILITY_GRAMMAR == DURABILITY_GRAMMAR
    assert sut.P2D45_PINNED_COMMIT == "ff342ea526025e6663fba35c338c022ca5da754e"
    assert sut.P2D45_SCHEMA_VERSION == "p2d45.run_ledger_persistence.v1"
    assert (len(P2D46_REASON_CODES), len(P2D46_INVARIANTS)) == (23, 24)
    assert (len(P2D45_REASON_CODES), len(P2D45_INVARIANTS)) == (24, 56)


def test_source_evidence_and_diagnostic_shapes_are_exact():
    assert SOURCE_KEYS == sut.P2D46_SOURCE_KEYS
    assert SAFE_EVIDENCE_KEYS == sut.P2D46_SAFE_EVIDENCE_KEYS
    assert sut.P2D46_DIAGNOSTIC_RECORD_KEYS == ("reason_code", "field")
    assert tuple(key for key, _value in P2D45_SOURCE) == P2D45_SOURCE_KEYS
    assert P2D45_EVIDENCE_KEYS == sut.P2D45_EVIDENCE_KEYS


def test_public_surface_exposes_exactly_one_function():
    functions = tuple(
        value for value in vars(sut).values()
        if inspect.isfunction(value) and value.__module__ == sut.__name__
    )
    assert functions == (sut.build_run_ledger_persistence_consumption_decision,)


def test_skeleton_placeholder_is_deterministic_fail_closed():
    expected = {
        "decision_created": False,
        "decision_status": "PERSISTENCE_RESULT_INVALID",
        "accepted": False,
        "warning": False,
        "reason_code": "P2D46_RESULT_NOT_EXACT_DICT",
        "reason": "The P2D-45 persistence result must be an exact built-in dict.",
        "source": {
            "boundary_scope": "run_ledger_persistence_consumption_decision",
            "schema_version": "p2d46.run_ledger_persistence_consumption_decision.v1",
            "upstream_boundary_scope": "run_ledger_persistence_boundary",
            "upstream_schema_version": "p2d45.run_ledger_persistence.v1",
            "upstream_artifact_name": "run-ledger.yaml",
            "upstream_persistence_status": "",
            "upstream_reason_code": "",
            "upstream_write_disposition": "",
        },
        "persistence_evidence": {},
        "decision_violations": ("P2D46_RESULT_NOT_EXACT_DICT",),
        "missing_or_invalid_fields": ("run_ledger_persistence_result",),
        "diagnostic_records": ({
            "reason_code": "P2D46_RESULT_NOT_EXACT_DICT",
            "field": "run_ledger_persistence_result",
        },),
        "invariant_refs": P2D46_INVARIANTS,
    }
    first = _call(None)
    second = _call(None)
    assert first == expected
    assert second == expected
    assert first is not second
    assert first["source"] is not second["source"]
    assert first["persistence_evidence"] is not second["persistence_evidence"]
    assert first["diagnostic_records"] is not second["diagnostic_records"]
    assert first["diagnostic_records"][0] is not second["diagnostic_records"][0]


def test_production_module_has_no_filesystem_runtime_or_external_dependencies():
    tree = ast.parse(inspect.getsource(sut))
    imports = tuple(
        (node.module, tuple(alias.name for alias in node.names))
        for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
    )
    assert imports == (("typing", ("Final",)),)
    assert not any(isinstance(node, ast.Import) for node in ast.walk(tree))
    forbidden = {
        "open", "os", "pathlib", "tempfile", "subprocess", "json", "yaml",
        "hashlib", "importlib", "exec", "eval", "runtime", "transition",
        "publisher", "publication", "notification", "requests", "httpx",
    }
    names = {
        node.id for node in ast.walk(tree) if isinstance(node, ast.Name)
    }
    assert names.isdisjoint(forbidden)


def test_output_catalogs_contain_no_completion_quality_or_publication_names():
    assert set(DECISION_STATUSES).isdisjoint(PROHIBITED_STATUSES)
    assert set(P2D46_REASON_CODES).isdisjoint(PROHIBITED_STATUSES)
    assert "P2D46_P_PASS_PUBLISHED_FORBIDDEN" in P2D46_INVARIANTS


def test_retry_metadata_is_absent_from_public_contract():
    public_names = RESULT_KEYS + SOURCE_KEYS + SAFE_EVIDENCE_KEYS + DECISION_STATUSES
    assert all("retry" not in value.casefold() for value in public_names)


def test_written_result_is_persistence_accepted():
    result = _call(_upstream("WRITTEN"))
    _assert_status(result, "PERSISTENCE_ACCEPTED")
    assert result["accepted"] is True and result["warning"] is False
    assert result["reason_code"] == "P2D46_WRITTEN_ACCEPTED"


def test_already_identical_result_is_persistence_accepted():
    result = _call(_upstream("ALREADY_IDENTICAL"))
    _assert_status(result, "PERSISTENCE_ACCEPTED")
    assert result["source"]["upstream_write_disposition"] == "ALREADY_IDENTICAL"


def test_cleanup_warning_written_is_accepted_with_warning():
    result = _call(_upstream("PERSISTED_CLEANUP_WARNING"))
    _assert_status(result, "PERSISTENCE_ACCEPTED_WITH_WARNING")
    assert result["accepted"] is True and result["warning"] is True


def test_cleanup_warning_identical_is_accepted_with_warning():
    upstream = _upstream("PERSISTED_CLEANUP_WARNING", disposition="ALREADY_IDENTICAL")
    result = _call(upstream)
    _assert_status(result, "PERSISTENCE_ACCEPTED_WITH_WARNING")
    assert result["persistence_evidence"]["write_disposition"] == "ALREADY_IDENTICAL"


def test_not_eligible_result_is_not_accepted():
    result = _call(_upstream("NOT_ELIGIBLE"))
    _assert_status(result, "PERSISTENCE_NOT_ACCEPTED")
    assert result["decision_created"] is True and result["accepted"] is False


def test_upstream_invalid_status_is_not_accepted_but_is_not_malformed():
    result = _call(_upstream("INVALID"))
    _assert_status(result, "PERSISTENCE_NOT_ACCEPTED")
    assert result["reason_code"] == "P2D46_UPSTREAM_INVALID_REJECTED"


def test_authorization_root_failure_is_not_accepted():
    result = _call(_upstream("AUTHORIZATION_FAILED"))
    _assert_status(result, "PERSISTENCE_NOT_ACCEPTED")
    assert result["source"]["upstream_reason_code"] == "DESTINATION_ROOT_INVALID"


def test_authorization_anchor_grammars_and_auxiliaries_are_exact():
    root_singleton = _upstream("AUTHORIZATION_FAILED")
    _assert_status(_call(root_singleton), "PERSISTENCE_NOT_ACCEPTED")
    root_compound = _upstream(
        "AUTHORIZATION_FAILED",
        codes=("DESTINATION_ROOT_INVALID", "PRE_FINALIZATION_IO_FAILED"),
    )
    _assert_status(_call(root_compound), "PERSISTENCE_NOT_ACCEPTED")
    path_combinations = (
        ("DESTINATION_PATH_UNSAFE",),
        ("DESTINATION_PATH_UNSAFE", "PRE_FINALIZATION_IO_FAILED"),
        ("DESTINATION_PATH_UNSAFE", "FINAL_INSPECTION_CLOSE_FAILED"),
        ("DESTINATION_PATH_UNSAFE", "TEMP_FILE_CLOSE_FAILED"),
        ("DESTINATION_PATH_UNSAFE", "TEMP_CLEANUP_FAILED"),
        ("DESTINATION_PATH_UNSAFE", "PRE_FINALIZATION_IO_FAILED", "TEMP_CLEANUP_FAILED"),
        ("DESTINATION_PATH_UNSAFE", "FINAL_INSPECTION_CLOSE_FAILED", "TEMP_FILE_CLOSE_FAILED"),
        ("DESTINATION_PATH_UNSAFE", "PRE_FINALIZATION_IO_FAILED", "FINAL_INSPECTION_CLOSE_FAILED", "TEMP_FILE_CLOSE_FAILED", "TEMP_CLEANUP_FAILED"),
    )
    for codes in path_combinations:
        result = _call(_upstream("AUTHORIZATION_FAILED", codes=codes))
        _assert_status(result, "PERSISTENCE_NOT_ACCEPTED")
        assert result["source"]["upstream_reason_code"] == "DESTINATION_PATH_UNSAFE"
    invalid_codes = (
        ("DESTINATION_ROOT_INVALID", "FINAL_INSPECTION_CLOSE_FAILED"),
        ("DESTINATION_ROOT_INVALID", "TEMP_FILE_CLOSE_FAILED"),
        ("DESTINATION_ROOT_INVALID", "TEMP_CLEANUP_FAILED"),
        ("DESTINATION_ROOT_INVALID", "DESTINATION_PATH_UNSAFE"),
        ("RUN_LEDGER_CONFLICT",),
        ("TEMP_CLEANUP_FAILED",),
    )
    for codes in invalid_codes:
        _assert_invalid(
            _call(_upstream("AUTHORIZATION_FAILED", codes=codes)),
            "P2D46_COHERENCE_INVALID",
        )
    malformed = _upstream(
        "AUTHORIZATION_FAILED",
        codes=("DESTINATION_PATH_UNSAFE", "TEMP_CLEANUP_FAILED"),
    )
    variants = []
    for field, value in (
        ("run_ledger_persisted", True),
        ("persistence_evidence", _evidence("WRITTEN")),
        ("reason", "wrong fixed text"),
        ("missing_or_invalid_fields", ("wrong",)),
        ("diagnostic_records", ({"reason_code": "wrong", "field": "wrong"},)),
    ):
        variant = dict(malformed)
        variant[field] = value
        variants.append(variant)
    duplicate = dict(malformed)
    duplicate["persistence_violations"] = (
        "DESTINATION_PATH_UNSAFE", "TEMP_CLEANUP_FAILED", "TEMP_CLEANUP_FAILED",
    )
    variants.append(duplicate)
    wrong_order = dict(malformed)
    wrong_order["persistence_violations"] = (
        "TEMP_CLEANUP_FAILED", "DESTINATION_PATH_UNSAFE",
    )
    variants.append(wrong_order)
    for variant in variants:
        _assert_status(_call(variant), "PERSISTENCE_RESULT_INVALID")


def test_serialization_failure_is_not_accepted():
    result = _call(_upstream("SERIALIZATION_FAILED"))
    _assert_status(result, "PERSISTENCE_NOT_ACCEPTED")
    assert result["reason_code"] == "P2D46_SERIALIZATION_FAILED_REJECTED"


def test_conflict_single_and_compound_variants_are_not_accepted():
    singleton = _call(_upstream("CONFLICT"))
    _assert_status(singleton, "PERSISTENCE_NOT_ACCEPTED")
    combinations = (
        ("RUN_LEDGER_CONFLICT", "PRE_FINALIZATION_IO_FAILED"),
        ("RUN_LEDGER_CONFLICT", "FINAL_INSPECTION_CLOSE_FAILED"),
        ("RUN_LEDGER_CONFLICT", "TEMP_FILE_CLOSE_FAILED"),
        ("RUN_LEDGER_CONFLICT", "TEMP_CLEANUP_FAILED"),
        ("RUN_LEDGER_CONFLICT", "PRE_FINALIZATION_IO_FAILED", "FINAL_INSPECTION_CLOSE_FAILED", "TEMP_FILE_CLOSE_FAILED", "TEMP_CLEANUP_FAILED"),
    )
    for codes in combinations:
        _assert_status(
            _call(_upstream("CONFLICT", codes=codes)),
            "PERSISTENCE_NOT_ACCEPTED",
        )


def test_every_io_failure_anchor_maps_to_not_accepted():
    _assert_status(_call(_upstream("IO_FAILED")), "PERSISTENCE_NOT_ACCEPTED")
    all_auxiliaries = (
        "PRE_FINALIZATION_IO_FAILED", "FINAL_INSPECTION_CLOSE_FAILED",
        "TEMP_FILE_CLOSE_FAILED", "TEMP_CLEANUP_FAILED",
    )
    for anchor, allowed in IO_GRAMMAR:
        base = (anchor,) if anchor != "PRE_FINALIZATION_IO_FAILED" else (anchor,)
        _assert_status(
            _call(_upstream("IO_FAILED", codes=base)),
            "PERSISTENCE_NOT_ACCEPTED",
        )
        for auxiliary in allowed:
            codes = _ordered(base + (auxiliary,))
            result = _call(_upstream("IO_FAILED", codes=codes))
            _assert_status(result, "PERSISTENCE_NOT_ACCEPTED")
            assert result["source"]["upstream_reason_code"] == codes[0]
        if allowed:
            full = _ordered(base + allowed)
            _assert_status(
                _call(_upstream("IO_FAILED", codes=full)),
                "PERSISTENCE_NOT_ACCEPTED",
            )
        for forbidden in all_auxiliaries:
            if forbidden != anchor and forbidden not in allowed:
                _assert_status(
                    _call(_upstream("IO_FAILED", codes=base + (forbidden,))),
                    "PERSISTENCE_RESULT_INVALID",
                )
    close_only_valid_anchor = _upstream(
        "IO_FAILED",
        codes=("EXISTING_TARGET_INSPECTION_FAILED", "FINAL_INSPECTION_CLOSE_FAILED"),
    )
    _assert_status(_call(close_only_valid_anchor), "PERSISTENCE_NOT_ACCEPTED")


def test_io_cleanup_only_tuple_is_invalid():
    _assert_status(_call(_upstream("IO_FAILED")), "PERSISTENCE_NOT_ACCEPTED")
    for codes in (
        ("TEMP_FILE_CLOSE_FAILED",),
        ("TEMP_CLEANUP_FAILED",),
        ("TEMP_FILE_CLOSE_FAILED", "TEMP_CLEANUP_FAILED"),
    ):
        _assert_invalid(
            _call(_upstream("IO_FAILED", codes=codes)),
            "P2D46_COHERENCE_INVALID",
        )


def test_identity_unconfirmed_is_not_accepted():
    valid = _upstream(
        "DURABILITY_UNCONFIRMED",
        codes=("FINAL_IDENTITY_VERIFICATION_FAILED", "TEMP_CLEANUP_FAILED"),
    )
    _assert_status(_call(valid), "PERSISTENCE_NOT_ACCEPTED")
    missing_cleanup = _upstream(
        "DURABILITY_UNCONFIRMED",
        codes=("FINAL_IDENTITY_VERIFICATION_FAILED",),
    )
    _assert_invalid(_call(missing_cleanup), "P2D46_COHERENCE_INVALID")


def test_final_durability_unconfirmed_is_not_accepted():
    result = _call(_upstream("DURABILITY_UNCONFIRMED"))
    _assert_status(result, "PERSISTENCE_NOT_ACCEPTED")
    assert result["accepted"] is False and result["warning"] is False


def test_durability_anchor_grammars_and_reason_priority_are_exact():
    identity = _upstream(
        "DURABILITY_UNCONFIRMED",
        codes=("FINAL_IDENTITY_VERIFICATION_FAILED", "TEMP_CLEANUP_FAILED"),
    )
    _assert_status(_call(identity), "PERSISTENCE_NOT_ACCEPTED")
    final = _upstream("DURABILITY_UNCONFIRMED")
    _assert_status(_call(final), "PERSISTENCE_NOT_ACCEPTED")
    displaced = _upstream(
        "DURABILITY_UNCONFIRMED",
        codes=("PRE_FINALIZATION_IO_FAILED", "FINAL_DURABILITY_UNCONFIRMED"),
    )
    displaced_result = _call(displaced)
    _assert_status(displaced_result, "PERSISTENCE_NOT_ACCEPTED")
    assert displaced_result["source"]["upstream_reason_code"] == "PRE_FINALIZATION_IO_FAILED"
    invalid_codes = (
        ("FINAL_IDENTITY_VERIFICATION_FAILED",),
        ("FINAL_IDENTITY_VERIFICATION_FAILED", "FINAL_DURABILITY_UNCONFIRMED", "TEMP_CLEANUP_FAILED"),
        ("TEMP_CLEANUP_FAILED",),
    )
    for codes in invalid_codes:
        _assert_status(
            _call(_upstream("DURABILITY_UNCONFIRMED", codes=codes)),
            "PERSISTENCE_RESULT_INVALID",
        )
    wrong_disposition = _upstream("DURABILITY_UNCONFIRMED")
    wrong_disposition["persistence_evidence"]["write_disposition"] = "WRITTEN"
    _assert_status(_call(wrong_disposition), "PERSISTENCE_RESULT_INVALID")
    missing_evidence = _upstream("DURABILITY_UNCONFIRMED")
    missing_evidence["persistence_evidence"] = {}
    _assert_status(_call(missing_evidence), "PERSISTENCE_RESULT_INVALID")


def test_evidence_path_digest_and_entry_id_must_be_coherent():
    valid = _upstream("WRITTEN")
    _assert_status(_call(valid), "PERSISTENCE_ACCEPTED")
    wrong_path = _upstream("WRITTEN")
    wrong_path["persistence_evidence"]["artifact_relative_path"] = (
        "runs/by-entry-id/sha256-" + "0" * 64 + "/run-ledger.yaml"
    )
    _assert_invalid(_call(wrong_path), "P2D46_EVIDENCE_CONTRACT_INVALID")
    wrong_digest = _upstream("WRITTEN")
    wrong_digest["persistence_evidence"]["content_digest"] = "not-sha256"
    _assert_invalid(_call(wrong_digest), "P2D46_EVIDENCE_CONTRACT_INVALID")


def test_status_alone_never_establishes_acceptance():
    valid = _upstream("WRITTEN")
    _assert_status(_call(valid), "PERSISTENCE_ACCEPTED")
    variants = []
    for field, value in (
        ("run_ledger_persisted", False),
        ("reason_code", "RUN_LEDGER_ALREADY_PERSISTED_IDENTICAL"),
        ("persistence_evidence", {}),
        ("persistence_violations", ("RUN_LEDGER_CONFLICT",)),
    ):
        variant = _upstream("WRITTEN")
        variant[field] = value
        variants.append(variant)
    for variant in variants:
        _assert_status(_call(variant), "PERSISTENCE_RESULT_INVALID")


def test_reason_violation_field_and_diagnostic_contract_is_recomputed():
    valid = _upstream("CONFLICT", codes=(
        "RUN_LEDGER_CONFLICT", "PRE_FINALIZATION_IO_FAILED", "TEMP_CLEANUP_FAILED",
    ))
    _assert_status(_call(valid), "PERSISTENCE_NOT_ACCEPTED")
    variants = []
    for field, value in (
        ("reason", "caller text"),
        ("missing_or_invalid_fields", ("wrong",)),
        ("diagnostic_records", ()),
    ):
        variant = dict(valid)
        variant[field] = value
        variants.append(variant)
    for variant in variants:
        _assert_status(_call(variant), "PERSISTENCE_RESULT_INVALID")


def test_exact_complete_p2d45_invariant_tuple_is_required():
    valid = _upstream("WRITTEN")
    _assert_status(_call(valid), "PERSISTENCE_ACCEPTED")
    for invariants in (
        P2D45_INVARIANTS[:-1],
        tuple(reversed(P2D45_INVARIANTS)),
        P2D45_INVARIANTS + ("UNKNOWN_INVARIANT",),
    ):
        value = _upstream("WRITTEN")
        value["invariant_refs"] = invariants
        _assert_invalid(_call(value), "P2D46_INVARIANTS_CONTRACT_INVALID")


def test_decision_truth_table_is_exact_for_all_ten_upstream_statuses():
    rows = (
        ("WRITTEN", "PERSISTENCE_ACCEPTED", True, False),
        ("ALREADY_IDENTICAL", "PERSISTENCE_ACCEPTED", True, False),
        ("NOT_ELIGIBLE", "PERSISTENCE_NOT_ACCEPTED", False, False),
        ("INVALID", "PERSISTENCE_NOT_ACCEPTED", False, False),
        ("AUTHORIZATION_FAILED", "PERSISTENCE_NOT_ACCEPTED", False, False),
        ("SERIALIZATION_FAILED", "PERSISTENCE_NOT_ACCEPTED", False, False),
        ("CONFLICT", "PERSISTENCE_NOT_ACCEPTED", False, False),
        ("IO_FAILED", "PERSISTENCE_NOT_ACCEPTED", False, False),
        ("DURABILITY_UNCONFIRMED", "PERSISTENCE_NOT_ACCEPTED", False, False),
        ("PERSISTED_CLEANUP_WARNING", "PERSISTENCE_ACCEPTED_WITH_WARNING", True, True),
    )
    first_status, first_expected, _accepted, _warning = rows[0]
    _assert_status(_call(_upstream(first_status)), first_expected)
    for status, expected, accepted, warning in rows:
        result = _call(_upstream(status))
        _assert_status(result, expected)
        assert result["decision_created"] is True
        assert result["accepted"] is accepted
        assert result["warning"] is warning


def test_valid_output_family_shapes_are_exact():
    accepted = _call(_upstream("WRITTEN"))
    _assert_status(accepted, "PERSISTENCE_ACCEPTED")
    for upstream in (
        _upstream("WRITTEN"), _upstream("PERSISTED_CLEANUP_WARNING"),
        _upstream("CONFLICT"),
    ):
        result = _call(upstream)
        assert tuple(result) == RESULT_KEYS
        assert tuple(result["source"]) == SOURCE_KEYS
        assert result["decision_violations"] == ()
        assert result["missing_or_invalid_fields"] == ()
        assert result["diagnostic_records"] == ()


def test_missing_unknown_and_reordered_root_keys_are_invalid():
    _assert_status(_call(_upstream("WRITTEN")), "PERSISTENCE_ACCEPTED")
    missing = _upstream("WRITTEN")
    missing.pop("reason")
    unknown = _upstream("WRITTEN")
    unknown["caller_secret"] = "not echoed"
    original = _upstream("WRITTEN")
    reordered = {key: original[key] for key in reversed(tuple(original))}
    for value in (missing, unknown, reordered):
        _assert_invalid(_call(value), "P2D46_RESULT_KEYS_INVALID")


def test_nested_persistence_result_bypass_is_invalid():
    _assert_status(_call(_upstream("WRITTEN")), "PERSISTENCE_ACCEPTED")
    value = {"run_ledger_persistence_result": _upstream("WRITTEN")}
    _assert_invalid(_call(value), "P2D46_FORBIDDEN_BYPASS")


def test_raw_p2d45a_assembly_bypass_is_invalid():
    _assert_status(_call(_upstream("WRITTEN")), "PERSISTENCE_ACCEPTED")
    for value in (
        {"run_ledger_entry_assembly": {}},
        {"run_ledger_entry_assembled": True},
        {"run_ledger_entry": {}},
    ):
        _assert_invalid(_call(value), "P2D46_FORBIDDEN_BYPASS")


def test_artifact_and_normalized_fragment_bypasses_are_invalid():
    _assert_status(_call(_upstream("WRITTEN")), "PERSISTENCE_ACCEPTED")
    for signature in (
        "normalized_run_ledger_persistence_result", "persistence_artifact_built",
        "artifact_status", "persistence_artifact", "serialized_content",
        "authorized_ops_root",
    ):
        _assert_invalid(_call({signature: "hostile"}), "P2D46_FORBIDDEN_BYPASS")


def test_non_dict_custom_mapping_and_dict_subclass_are_invalid():
    _assert_status(_call(_upstream("WRITTEN")), "PERSISTENCE_ACCEPTED")
    class CustomMapping:
        pass
    class DictSubclass(dict):
        pass
    for value in (None, CustomMapping(), DictSubclass(_upstream("WRITTEN"))):
        _assert_invalid(_call(value), "P2D46_RESULT_NOT_EXACT_DICT")


def test_cycles_and_excessive_depth_fail_without_traversal_or_recursion():
    _assert_status(_call(_upstream("WRITTEN")), "PERSISTENCE_ACCEPTED")
    cycle = {}
    cycle["run_ledger_persistence_result"] = cycle
    _assert_invalid(_call(cycle), "P2D46_FORBIDDEN_BYPASS")
    deep = []
    cursor = deep
    for _index in range(2000):
        nested = []
        cursor.append(nested)
        cursor = nested
    value = _upstream("WRITTEN")
    value["source"] = deep
    _assert_invalid(_call(value), "P2D46_SOURCE_CONTRACT_INVALID")


def test_wrong_scalar_types_and_bool_as_int_are_invalid():
    _assert_status(_call(_upstream("WRITTEN")), "PERSISTENCE_ACCEPTED")
    cases = (
        ("run_ledger_persisted", 1),
        ("persistence_status", True),
        ("reason_code", 7),
        ("reason", False),
    )
    for field, replacement in cases:
        value = _upstream("WRITTEN")
        value[field] = replacement
        _assert_invalid(_call(value), "P2D46_RESULT_FIELD_TYPE_INVALID")


def test_unknown_status_reason_invariant_and_schema_version_are_invalid_and_suppressed():
    _assert_status(_call(_upstream("WRITTEN")), "PERSISTENCE_ACCEPTED")
    values = []
    unknown_status = _upstream("WRITTEN")
    unknown_status["persistence_status"] = "CALLER_SECRET_STATUS"
    values.append((unknown_status, "P2D46_STATUS_UNKNOWN"))
    unknown_reason = _upstream("WRITTEN")
    unknown_reason["reason_code"] = "CALLER_SECRET_REASON"
    values.append((unknown_reason, "P2D46_REASON_CONTRACT_INVALID"))
    unknown_invariant = _upstream("WRITTEN")
    unknown_invariant["invariant_refs"] = P2D45_INVARIANTS + ("CALLER_SECRET_INVARIANT",)
    values.append((unknown_invariant, "P2D46_INVARIANTS_CONTRACT_INVALID"))
    for schema in ("p2d45.run_ledger_persistence.v2", "future.secret.schema.v99"):
        future = _upstream("WRITTEN")
        future["source"]["schema_version"] = schema
        values.append((future, "P2D46_SOURCE_CONTRACT_INVALID"))
    for value, reason in values:
        result = _call(value)
        _assert_invalid(result, reason)
        rendered = str(result)
        assert "CALLER_SECRET" not in rendered
        assert "future.secret.schema" not in rendered


def test_unexpected_nested_container_types_are_invalid():
    _assert_status(_call(_upstream("WRITTEN")), "PERSISTENCE_ACCEPTED")
    cases = (
        ("source", ()),
        ("persistence_evidence", []),
        ("persistence_violations", []),
        ("missing_or_invalid_fields", []),
        ("diagnostic_records", []),
        ("invariant_refs", []),
    )
    for field, replacement in cases:
        value = _upstream("WRITTEN")
        value[field] = replacement
        _assert_status(_call(value), "PERSISTENCE_RESULT_INVALID")


def test_hostile_eq_hash_repr_str_and_iteration_are_never_invoked():
    _assert_status(_call(_upstream("WRITTEN")), "PERSISTENCE_ACCEPTED")
    calls = {"eq": 0, "hash": 0, "repr": 0, "str": 0, "iter": 0}
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
        def __iter__(self):
            calls["iter"] += 1
            raise AssertionError("iter")
    result = _call(Hostile())
    _assert_invalid(result, "P2D46_RESULT_NOT_EXACT_DICT")
    assert calls == {"eq": 0, "hash": 0, "repr": 0, "str": 0, "iter": 0}


def test_input_is_not_mutated_or_retained():
    upstream = _upstream("WRITTEN")
    expected = _upstream("WRITTEN")
    result = _call(upstream)
    _assert_status(result, "PERSISTENCE_ACCEPTED")
    assert upstream == expected
    assert result is not upstream
    assert result["source"] is not upstream["source"]
    assert result["persistence_evidence"] is not upstream["persistence_evidence"]


def test_repeated_outputs_have_fresh_nested_containers():
    first_valid = _call(_upstream("WRITTEN"))
    _assert_status(first_valid, "PERSISTENCE_ACCEPTED")
    first = _call(None)
    second = _call(None)
    assert first is not second
    assert first["source"] is not second["source"]
    assert first["persistence_evidence"] is not second["persistence_evidence"]
    assert first["diagnostic_records"] is not second["diagnostic_records"]
    assert len(first["diagnostic_records"]) == 1
    assert len(second["diagnostic_records"]) == 1
    assert first["diagnostic_records"][0] is not second["diagnostic_records"][0]


def test_mutating_input_after_return_cannot_change_output():
    upstream = _upstream("WRITTEN")
    result = _call(upstream)
    _assert_status(result, "PERSISTENCE_ACCEPTED")
    expected = dict(result["persistence_evidence"])
    upstream["persistence_evidence"]["content_digest"] = "b" * 64
    upstream["source"]["schema_version"] = "mutated"
    assert result["persistence_evidence"] == expected
    assert result["source"]["upstream_schema_version"] == "p2d45.run_ledger_persistence.v1"


def test_mutating_one_output_cannot_change_another_call():
    first = _call(_upstream("WRITTEN"))
    _assert_status(first, "PERSISTENCE_ACCEPTED")
    second = _call(_upstream("WRITTEN"))
    _assert_status(second, "PERSISTENCE_ACCEPTED")
    first["source"]["boundary_scope"] = "mutated"
    first["persistence_evidence"]["content_digest"] = "mutated"
    assert second["source"]["boundary_scope"] == "run_ledger_persistence_consumption_decision"
    assert second["persistence_evidence"]["content_digest"] == "a" * 64


def test_safe_evidence_allowlist_and_caller_detail_suppression_are_exact():
    upstream = _upstream("WRITTEN")
    result = _call(upstream)
    _assert_status(result, "PERSISTENCE_ACCEPTED")
    assert tuple(result["persistence_evidence"]) == SAFE_EVIDENCE_KEYS
    assert "run_ledger_entry_id" not in result["persistence_evidence"]
    assert "run_id" not in result["persistence_evidence"]
    hostile = _upstream("WRITTEN")
    hostile["caller_absolute_path"] = "/private/ops/secret"
    invalid = _call(hostile)
    _assert_status(invalid, "PERSISTENCE_RESULT_INVALID")
    rendered = str(invalid)
    assert "/private/ops/secret" not in rendered
    assert "caller_absolute_path" not in rendered
