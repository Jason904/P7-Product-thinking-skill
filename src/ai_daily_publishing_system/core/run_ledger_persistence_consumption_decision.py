"""Frozen P2D-46 persistence-result consumption-decision skeleton."""

from typing import Final


P2D46_BOUNDARY_SCOPE: Final[str] = (
    "run_ledger_persistence_consumption_decision"
)
P2D46_SCHEMA_VERSION: Final[str] = (
    "p2d46.run_ledger_persistence_consumption_decision.v1"
)
P2D45_PINNED_COMMIT: Final[str] = (
    "ff342ea526025e6663fba35c338c022ca5da754e"
)
P2D45_SCHEMA_VERSION: Final[str] = "p2d45.run_ledger_persistence.v1"

P2D46_RESULT_KEYS: Final[tuple[str, ...]] = (
    "decision_created",
    "decision_status",
    "accepted",
    "warning",
    "reason_code",
    "reason",
    "source",
    "persistence_evidence",
    "decision_violations",
    "missing_or_invalid_fields",
    "diagnostic_records",
    "invariant_refs",
)
P2D46_SOURCE_KEYS: Final[tuple[str, ...]] = (
    "boundary_scope",
    "schema_version",
    "upstream_boundary_scope",
    "upstream_schema_version",
    "upstream_artifact_name",
    "upstream_persistence_status",
    "upstream_reason_code",
    "upstream_write_disposition",
)
P2D46_SAFE_EVIDENCE_KEYS: Final[tuple[str, ...]] = (
    "artifact_relative_path",
    "serialization_format",
    "content_digest_algorithm",
    "content_digest",
    "write_disposition",
)
P2D46_DIAGNOSTIC_RECORD_KEYS: Final[tuple[str, ...]] = (
    "reason_code",
    "field",
)
P2D46_DECISION_STATUSES: Final[tuple[str, ...]] = (
    "PERSISTENCE_ACCEPTED",
    "PERSISTENCE_ACCEPTED_WITH_WARNING",
    "PERSISTENCE_NOT_ACCEPTED",
    "PERSISTENCE_RESULT_INVALID",
)
P2D46_BOOLEAN_MATRIX: Final[
    tuple[tuple[str, bool, bool, bool], ...]
] = (
    ("PERSISTENCE_ACCEPTED", True, True, False),
    ("PERSISTENCE_ACCEPTED_WITH_WARNING", True, True, True),
    ("PERSISTENCE_NOT_ACCEPTED", True, False, False),
    ("PERSISTENCE_RESULT_INVALID", False, False, False),
)

P2D46_REASON_CODES: Final[tuple[str, ...]] = (
    "P2D46_WRITTEN_ACCEPTED",
    "P2D46_ALREADY_IDENTICAL_ACCEPTED",
    "P2D46_NOT_ELIGIBLE_REJECTED",
    "P2D46_UPSTREAM_INVALID_REJECTED",
    "P2D46_AUTHORIZATION_FAILED_REJECTED",
    "P2D46_SERIALIZATION_FAILED_REJECTED",
    "P2D46_CONFLICT_REJECTED",
    "P2D46_IO_FAILED_REJECTED",
    "P2D46_DURABILITY_UNCONFIRMED_REJECTED",
    "P2D46_CLEANUP_WARNING_ACCEPTED",
    "P2D46_RESULT_NOT_EXACT_DICT",
    "P2D46_FORBIDDEN_BYPASS",
    "P2D46_RESULT_KEYS_INVALID",
    "P2D46_RESULT_FIELD_TYPE_INVALID",
    "P2D46_SOURCE_CONTRACT_INVALID",
    "P2D46_EVIDENCE_CONTRACT_INVALID",
    "P2D46_STATUS_UNKNOWN",
    "P2D46_REASON_CONTRACT_INVALID",
    "P2D46_VIOLATIONS_CONTRACT_INVALID",
    "P2D46_FIELDS_CONTRACT_INVALID",
    "P2D46_DIAGNOSTICS_CONTRACT_INVALID",
    "P2D46_INVARIANTS_CONTRACT_INVALID",
    "P2D46_COHERENCE_INVALID",
)
P2D46_VALIDATION_REASON_CODES: Final[tuple[str, ...]] = (
    "P2D46_RESULT_NOT_EXACT_DICT",
    "P2D46_FORBIDDEN_BYPASS",
    "P2D46_RESULT_KEYS_INVALID",
    "P2D46_RESULT_FIELD_TYPE_INVALID",
    "P2D46_SOURCE_CONTRACT_INVALID",
    "P2D46_EVIDENCE_CONTRACT_INVALID",
    "P2D46_STATUS_UNKNOWN",
    "P2D46_REASON_CONTRACT_INVALID",
    "P2D46_VIOLATIONS_CONTRACT_INVALID",
    "P2D46_FIELDS_CONTRACT_INVALID",
    "P2D46_DIAGNOSTICS_CONTRACT_INVALID",
    "P2D46_INVARIANTS_CONTRACT_INVALID",
    "P2D46_COHERENCE_INVALID",
)
P2D46_REASON_STRINGS: Final[tuple[tuple[str, str], ...]] = (
    (
        "P2D46_WRITTEN_ACCEPTED",
        "The coherent P2D-45 WRITTEN result was accepted as durable run-ledger persistence.",
    ),
    (
        "P2D46_ALREADY_IDENTICAL_ACCEPTED",
        "The coherent P2D-45 ALREADY_IDENTICAL result was accepted as durable run-ledger persistence.",
    ),
    (
        "P2D46_NOT_ELIGIBLE_REJECTED",
        "The coherent P2D-45 NOT_ELIGIBLE result was not accepted as persistence.",
    ),
    (
        "P2D46_UPSTREAM_INVALID_REJECTED",
        "The coherent P2D-45 INVALID result was not accepted as persistence.",
    ),
    (
        "P2D46_AUTHORIZATION_FAILED_REJECTED",
        "The coherent P2D-45 AUTHORIZATION_FAILED result was not accepted as persistence.",
    ),
    (
        "P2D46_SERIALIZATION_FAILED_REJECTED",
        "The coherent P2D-45 SERIALIZATION_FAILED result was not accepted as persistence.",
    ),
    (
        "P2D46_CONFLICT_REJECTED",
        "The coherent P2D-45 CONFLICT result was not accepted as persistence.",
    ),
    (
        "P2D46_IO_FAILED_REJECTED",
        "The coherent P2D-45 IO_FAILED result was not accepted as persistence.",
    ),
    (
        "P2D46_DURABILITY_UNCONFIRMED_REJECTED",
        "The coherent P2D-45 DURABILITY_UNCONFIRMED result was not accepted as persistence.",
    ),
    (
        "P2D46_CLEANUP_WARNING_ACCEPTED",
        "The coherent P2D-45 cleanup-warning result was accepted as persisted with warning.",
    ),
    (
        "P2D46_RESULT_NOT_EXACT_DICT",
        "The P2D-45 persistence result must be an exact built-in dict.",
    ),
    (
        "P2D46_FORBIDDEN_BYPASS",
        "A forbidden persistence-result bypass shape was supplied.",
    ),
    (
        "P2D46_RESULT_KEYS_INVALID",
        "The P2D-45 persistence result must contain the exact ordered result keys.",
    ),
    (
        "P2D46_RESULT_FIELD_TYPE_INVALID",
        "A P2D-45 persistence result scalar field has an invalid exact type.",
    ),
    (
        "P2D46_SOURCE_CONTRACT_INVALID",
        "The P2D-45 persistence source contract is invalid or incompatible.",
    ),
    (
        "P2D46_EVIDENCE_CONTRACT_INVALID",
        "The P2D-45 persistence evidence contract is invalid.",
    ),
    (
        "P2D46_STATUS_UNKNOWN",
        "The P2D-45 persistence status is unknown.",
    ),
    (
        "P2D46_REASON_CONTRACT_INVALID",
        "The P2D-45 reason code or fixed reason text is invalid.",
    ),
    (
        "P2D46_VIOLATIONS_CONTRACT_INVALID",
        "The P2D-45 persistence violation tuple is invalid.",
    ),
    (
        "P2D46_FIELDS_CONTRACT_INVALID",
        "The P2D-45 missing-or-invalid field tuple is invalid.",
    ),
    (
        "P2D46_DIAGNOSTICS_CONTRACT_INVALID",
        "The P2D-45 diagnostic record tuple is invalid.",
    ),
    (
        "P2D46_INVARIANTS_CONTRACT_INVALID",
        "The P2D-45 invariant reference tuple is invalid.",
    ),
    (
        "P2D46_COHERENCE_INVALID",
        "The complete P2D-45 persistence result is internally incoherent.",
    ),
)
P2D46_DIAGNOSTIC_PATHS: Final[tuple[str, ...]] = (
    "run_ledger_persistence_result",
    "p2d46.forbidden_bypass",
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
P2D46_FORBIDDEN_BYPASS_SIGNATURES: Final[tuple[str, ...]] = (
    "run_ledger_persistence_result",
    "normalized_run_ledger_persistence_result",
    "run_ledger_entry_assembly",
    "run_ledger_entry_assembled",
    "run_ledger_entry",
    "persistence_artifact_built",
    "artifact_status",
    "persistence_artifact",
    "serialized_content",
    "authorized_ops_root",
)
P2D46_INVARIANT_REFS: Final[tuple[str, ...]] = (
    "P2D46_P_COMPLETE_P2D45_RESULT_REQUIRED",
    "P2D46_P_PURE_IN_MEMORY_DECISION",
    "P2D46_P_EXACT_UPSTREAM_COHERENCE_REQUIRED",
    "P2D46_P_STATUS_ALONE_INSUFFICIENT",
    "P2D46_P_LEDGER_PERSISTED_NOT_RUN_COMPLETED",
    "P2D46_P_NO_TRANSITION_AUTHORITY",
    "P2D46_P_NO_RUNTIME_EXECUTION",
    "P2D46_P_NO_QUALITY_PASS",
    "P2D46_P_NO_PUBLIC_URL",
    "P2D46_P_PASS_PUBLISHED_FORBIDDEN",
    "P2D46_P_NOTIFICATION_FORBIDDEN",
    "P2D46_P_PERSISTED_CLEANUP_WARNING_REMAINS_WARNING",
    "P2D46_P_DURABILITY_UNCONFIRMED_NEVER_ACCEPTED_AS_SUCCESS",
    "P2D46_P_BLOCKED_UPSTREAM_FAILS_CLOSED",
    "P2D46_P_MALFORMED_UPSTREAM_INVALID",
    "P2D46_P_RESULT_MUST_BE_FRESH",
    "P2D46_P_CALLER_DATA_SUPPRESSED",
    "P2D46_P_SAFE_EVIDENCE_ALLOWLIST_ONLY",
    "P2D46_P_UNKNOWN_KEYS_REJECTED_AND_SUPPRESSED",
    "P2D46_P_BYPASS_FORBIDDEN",
    "P2D46_P_NO_UPSTREAM_INVOCATION",
    "P2D46_P_NO_FILESYSTEM_OR_OPS_ROOT",
    "P2D46_P_NO_RETRY_EXECUTION",
    "P2D46_P_DOWNSTREAM_INSPECTION_DECLARATIVE_ONLY",
)
P2D46_PROHIBITED_STATUS_VOCABULARY: Final[tuple[str, ...]] = (
    "RUN_COMPLETED",
    "COMPLETED",
    "TRANSITIONED",
    "PASS",
    "PASS_PUBLISHED",
    "PUBLISHED",
    "NOOP_COMPLETED",
    "PUBLISH_ALLOWED",
)

P2D45_RESULT_KEYS: Final[tuple[str, ...]] = (
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
P2D45_SOURCE_KEYS: Final[tuple[str, ...]] = (
    "boundary_scope",
    "schema_version",
    "artifact_name",
    "serialization_format",
    "content_digest_algorithm",
)
P2D45_SOURCE_VALUES: Final[tuple[tuple[str, str], ...]] = (
    ("boundary_scope", "run_ledger_persistence_boundary"),
    ("schema_version", "p2d45.run_ledger_persistence.v1"),
    ("artifact_name", "run-ledger.yaml"),
    ("serialization_format", "canonical_json_yaml_1_2_subset"),
    ("content_digest_algorithm", "sha256"),
)
P2D45_EVIDENCE_KEYS: Final[tuple[str, ...]] = (
    "run_ledger_entry_id",
    "run_id",
    "artifact_relative_path",
    "serialization_format",
    "content_digest_algorithm",
    "content_digest",
    "write_disposition",
)
P2D45_STATUSES: Final[tuple[str, ...]] = (
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
P2D45_WRITE_DISPOSITIONS: Final[tuple[str, ...]] = (
    "WRITTEN",
    "ALREADY_IDENTICAL",
    "DURABILITY_UNCONFIRMED",
)
P2D45_STATUS_CONTRACT: Final[
    tuple[
        tuple[str, bool, tuple[str, ...], bool, tuple[str, ...]],
        ...,
    ]
] = (
    ("WRITTEN", True, ("WRITTEN",), True, ("RUN_LEDGER_PERSISTED",)),
    (
        "ALREADY_IDENTICAL",
        True,
        ("ALREADY_IDENTICAL",),
        True,
        ("RUN_LEDGER_ALREADY_PERSISTED_IDENTICAL",),
    ),
    (
        "NOT_ELIGIBLE",
        False,
        (),
        False,
        ("P2D45A_ENVELOPE_NOT_ELIGIBLE",),
    ),
    (
        "INVALID",
        False,
        (),
        False,
        ("P2D45A_SUCCESS_ENVELOPE_INVALID",),
    ),
    (
        "AUTHORIZATION_FAILED",
        False,
        (),
        False,
        ("DESTINATION_ROOT_INVALID", "DESTINATION_PATH_UNSAFE"),
    ),
    (
        "SERIALIZATION_FAILED",
        False,
        (),
        False,
        ("RUN_LEDGER_SERIALIZATION_FAILED",),
    ),
    ("CONFLICT", False, (), False, ("RUN_LEDGER_CONFLICT",)),
    (
        "IO_FAILED",
        False,
        (),
        False,
        (
            "FILESYSTEM_CAPABILITY_UNAVAILABLE",
            "EXISTING_TARGET_INSPECTION_FAILED",
            "PRE_FINALIZATION_IO_FAILED",
            "TEMP_NAME_GENERATION_FAILED",
            "TEMP_FILE_CREATE_FAILED",
            "TEMP_INODE_VALIDATION_FAILED",
            "TEMP_FILE_WRITE_FAILED",
            "TEMP_FILE_FSYNC_FAILED",
            "ATOMIC_CREATE_FAILED",
        ),
    ),
    (
        "DURABILITY_UNCONFIRMED",
        False,
        ("DURABILITY_UNCONFIRMED",),
        True,
        (
            "FINAL_IDENTITY_VERIFICATION_FAILED",
            "FINAL_DURABILITY_UNCONFIRMED",
        ),
    ),
    (
        "PERSISTED_CLEANUP_WARNING",
        True,
        ("WRITTEN", "ALREADY_IDENTICAL"),
        True,
        ("PERSISTED_CLEANUP_WARNING",),
    ),
)
P2D45_REASON_CODES: Final[tuple[str, ...]] = (
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
P2D45_REASON_PRIORITY: Final[tuple[str, ...]] = (
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
P2D45_REASON_STRINGS: Final[tuple[tuple[str, str], ...]] = (
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
P2D45_DIAGNOSTIC_PATHS: Final[
    tuple[tuple[str, tuple[str, ...]], ...]
] = (
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
P2D45_INVARIANT_REFS: Final[tuple[str, ...]] = (
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

P2D45_AUTHORIZATION_GRAMMAR: Final[
    tuple[tuple[str, tuple[str, ...]], ...]
] = (
    ("DESTINATION_ROOT_INVALID", ("PRE_FINALIZATION_IO_FAILED",)),
    (
        "DESTINATION_PATH_UNSAFE",
        (
            "PRE_FINALIZATION_IO_FAILED",
            "FINAL_INSPECTION_CLOSE_FAILED",
            "TEMP_FILE_CLOSE_FAILED",
            "TEMP_CLEANUP_FAILED",
        ),
    ),
)
P2D45_IO_GRAMMAR: Final[tuple[tuple[str, tuple[str, ...]], ...]] = (
    ("FILESYSTEM_CAPABILITY_UNAVAILABLE", ()),
    (
        "EXISTING_TARGET_INSPECTION_FAILED",
        (
            "PRE_FINALIZATION_IO_FAILED",
            "FINAL_INSPECTION_CLOSE_FAILED",
            "TEMP_FILE_CLOSE_FAILED",
            "TEMP_CLEANUP_FAILED",
        ),
    ),
    (
        "PRE_FINALIZATION_IO_FAILED",
        ("TEMP_FILE_CLOSE_FAILED", "TEMP_CLEANUP_FAILED"),
    ),
    ("TEMP_NAME_GENERATION_FAILED", ("PRE_FINALIZATION_IO_FAILED",)),
    ("TEMP_FILE_CREATE_FAILED", ("PRE_FINALIZATION_IO_FAILED",)),
    (
        "TEMP_INODE_VALIDATION_FAILED",
        (
            "PRE_FINALIZATION_IO_FAILED",
            "TEMP_FILE_CLOSE_FAILED",
            "TEMP_CLEANUP_FAILED",
        ),
    ),
    (
        "TEMP_FILE_WRITE_FAILED",
        (
            "PRE_FINALIZATION_IO_FAILED",
            "TEMP_FILE_CLOSE_FAILED",
            "TEMP_CLEANUP_FAILED",
        ),
    ),
    (
        "TEMP_FILE_FSYNC_FAILED",
        (
            "PRE_FINALIZATION_IO_FAILED",
            "TEMP_FILE_CLOSE_FAILED",
            "TEMP_CLEANUP_FAILED",
        ),
    ),
    (
        "ATOMIC_CREATE_FAILED",
        (
            "PRE_FINALIZATION_IO_FAILED",
            "TEMP_FILE_CLOSE_FAILED",
            "TEMP_CLEANUP_FAILED",
        ),
    ),
)
P2D45_DURABILITY_GRAMMAR: Final[
    tuple[tuple[str, tuple[str, ...], tuple[str, ...]], ...]
] = (
    (
        "FINAL_IDENTITY_VERIFICATION_FAILED",
        ("TEMP_CLEANUP_FAILED",),
        (
            "PRE_FINALIZATION_IO_FAILED",
            "FINAL_INSPECTION_CLOSE_FAILED",
            "TEMP_FILE_CLOSE_FAILED",
        ),
    ),
    (
        "FINAL_DURABILITY_UNCONFIRMED",
        (),
        (
            "PRE_FINALIZATION_IO_FAILED",
            "FINAL_INSPECTION_CLOSE_FAILED",
            "TEMP_FILE_CLOSE_FAILED",
            "TEMP_CLEANUP_FAILED",
        ),
    ),
)


def build_run_ledger_persistence_consumption_decision(
    *,
    run_ledger_persistence_result: dict[str, object],
) -> dict[str, object]:
    """Validate and classify one complete frozen P2D-45 result."""

    selected_validation_reason = ""
    root_keys: tuple[object, ...] = ()
    root_key_types_exact = False

    run_ledger_persisted = False
    persistence_status = ""
    upstream_reason_code = ""
    upstream_reason = ""
    persistence_violations: tuple[object, ...] = ()

    evidence_present = False
    evidence_artifact_relative_path = ""
    evidence_serialization_format = ""
    evidence_content_digest_algorithm = ""
    evidence_content_digest = ""
    evidence_write_disposition = ""

    decision_status = "PERSISTENCE_RESULT_INVALID"
    decision_accepted = False
    decision_warning = False
    decision_reason_code = ""

    # A. Reject non-exact roots before equality, hashing, iteration, or display.
    if type(run_ledger_persistence_result) is not dict:
        selected_validation_reason = "P2D46_RESULT_NOT_EXACT_DICT"

    # B. Inspect built-in keys only. Key types are proven before comparison,
    # and a bypass is rejected without touching its value.
    if selected_validation_reason == "":
        root_keys = tuple(dict.keys(run_ledger_persistence_result))
        root_key_types_exact = True
        root_key_index = 0
        while root_key_index < len(root_keys):
            if type(root_keys[root_key_index]) is not str:
                root_key_types_exact = False
            root_key_index += 1

        bypass_detected = False
        root_key_index = 0
        while root_key_index < len(root_keys) and not bypass_detected:
            root_key = root_keys[root_key_index]
            if type(root_key) is str:
                bypass_index = 0
                while (
                    bypass_index < len(P2D46_FORBIDDEN_BYPASS_SIGNATURES)
                    and not bypass_detected
                ):
                    if (
                        root_key
                        == P2D46_FORBIDDEN_BYPASS_SIGNATURES[bypass_index]
                    ):
                        bypass_detected = True
                    bypass_index += 1
            root_key_index += 1
        if bypass_detected:
            selected_validation_reason = "P2D46_FORBIDDEN_BYPASS"

    # C. Require the exact ordered root and exact scalar types.
    if selected_validation_reason == "":
        if (
            not root_key_types_exact
            or root_keys != P2D45_RESULT_KEYS
        ):
            selected_validation_reason = "P2D46_RESULT_KEYS_INVALID"

    if selected_validation_reason == "":
        persisted_candidate = dict.__getitem__(
            run_ledger_persistence_result,
            "run_ledger_persisted",
        )
        if type(persisted_candidate) is not bool:
            selected_validation_reason = "P2D46_RESULT_FIELD_TYPE_INVALID"
        else:
            run_ledger_persisted = persisted_candidate

    if selected_validation_reason == "":
        status_candidate = dict.__getitem__(
            run_ledger_persistence_result,
            "persistence_status",
        )
        if type(status_candidate) is not str:
            selected_validation_reason = "P2D46_RESULT_FIELD_TYPE_INVALID"
        else:
            persistence_status = status_candidate

    if selected_validation_reason == "":
        reason_code_candidate = dict.__getitem__(
            run_ledger_persistence_result,
            "reason_code",
        )
        if type(reason_code_candidate) is not str:
            selected_validation_reason = "P2D46_RESULT_FIELD_TYPE_INVALID"
        else:
            upstream_reason_code = reason_code_candidate

    if selected_validation_reason == "":
        reason_candidate = dict.__getitem__(
            run_ledger_persistence_result,
            "reason",
        )
        if type(reason_candidate) is not str:
            selected_validation_reason = "P2D46_RESULT_FIELD_TYPE_INVALID"
        else:
            upstream_reason = reason_candidate

    # D. Validate the copied P2D-45 source without trusting nested iteration.
    if selected_validation_reason == "":
        source_candidate = dict.__getitem__(
            run_ledger_persistence_result,
            "source",
        )
        if type(source_candidate) is not dict:
            selected_validation_reason = "P2D46_SOURCE_CONTRACT_INVALID"
        else:
            source_keys = tuple(dict.keys(source_candidate))
            source_key_types_exact = True
            source_key_index = 0
            while source_key_index < len(source_keys):
                if type(source_keys[source_key_index]) is not str:
                    source_key_types_exact = False
                source_key_index += 1
            if (
                not source_key_types_exact
                or source_keys != P2D45_SOURCE_KEYS
            ):
                selected_validation_reason = "P2D46_SOURCE_CONTRACT_INVALID"
            else:
                source_values: list[str] = []
                source_value_index = 0
                while (
                    source_value_index < len(P2D45_SOURCE_KEYS)
                    and selected_validation_reason == ""
                ):
                    source_value = dict.__getitem__(
                        source_candidate,
                        P2D45_SOURCE_KEYS[source_value_index],
                    )
                    if type(source_value) is not str:
                        selected_validation_reason = (
                            "P2D46_SOURCE_CONTRACT_INVALID"
                        )
                    else:
                        source_values.append(source_value)
                    source_value_index += 1
                if selected_validation_reason == "":
                    source_value_index = 0
                    while (
                        source_value_index < len(P2D45_SOURCE_VALUES)
                        and selected_validation_reason == ""
                    ):
                        if (
                            source_values[source_value_index]
                            != P2D45_SOURCE_VALUES[source_value_index][1]
                        ):
                            selected_validation_reason = (
                                "P2D46_SOURCE_CONTRACT_INVALID"
                            )
                        source_value_index += 1

    # E. Validate evidence at its fixed boundary. The local digest executes
    # only after the complete seven-string envelope has passed fixed checks.
    if selected_validation_reason == "":
        evidence_candidate = dict.__getitem__(
            run_ledger_persistence_result,
            "persistence_evidence",
        )
        if type(evidence_candidate) is not dict:
            selected_validation_reason = "P2D46_EVIDENCE_CONTRACT_INVALID"
        else:
            evidence_keys = tuple(dict.keys(evidence_candidate))
            evidence_key_types_exact = True
            evidence_key_index = 0
            while evidence_key_index < len(evidence_keys):
                if type(evidence_keys[evidence_key_index]) is not str:
                    evidence_key_types_exact = False
                evidence_key_index += 1

            if not evidence_key_types_exact:
                selected_validation_reason = "P2D46_EVIDENCE_CONTRACT_INVALID"
            elif evidence_keys == ():
                evidence_present = False
            elif evidence_keys != P2D45_EVIDENCE_KEYS:
                selected_validation_reason = "P2D46_EVIDENCE_CONTRACT_INVALID"
            else:
                evidence_values: list[str] = []
                evidence_value_index = 0
                while (
                    evidence_value_index < len(P2D45_EVIDENCE_KEYS)
                    and selected_validation_reason == ""
                ):
                    evidence_value = dict.__getitem__(
                        evidence_candidate,
                        P2D45_EVIDENCE_KEYS[evidence_value_index],
                    )
                    if type(evidence_value) is not str:
                        selected_validation_reason = (
                            "P2D46_EVIDENCE_CONTRACT_INVALID"
                        )
                    else:
                        evidence_values.append(evidence_value)
                    evidence_value_index += 1

                if selected_validation_reason == "":
                    evidence_entry_id = evidence_values[0]
                    evidence_run_id = evidence_values[1]
                    evidence_artifact_relative_path = evidence_values[2]
                    evidence_serialization_format = evidence_values[3]
                    evidence_content_digest_algorithm = evidence_values[4]
                    evidence_content_digest = evidence_values[5]
                    evidence_write_disposition = evidence_values[6]

                    if (
                        evidence_entry_id.strip() == ""
                        or evidence_run_id.strip() == ""
                        or evidence_serialization_format
                        != "canonical_json_yaml_1_2_subset"
                        or evidence_content_digest_algorithm != "sha256"
                        or evidence_write_disposition
                        not in P2D45_WRITE_DISPOSITIONS
                    ):
                        selected_validation_reason = (
                            "P2D46_EVIDENCE_CONTRACT_INVALID"
                        )

                if selected_validation_reason == "":
                    content_digest_valid = (
                        len(evidence_content_digest) == 64
                    )
                    digest_character_index = 0
                    while (
                        digest_character_index < len(evidence_content_digest)
                        and content_digest_valid
                    ):
                        if (
                            evidence_content_digest[digest_character_index]
                            not in "0123456789abcdef"
                        ):
                            content_digest_valid = False
                        digest_character_index += 1
                    if not content_digest_valid:
                        selected_validation_reason = (
                            "P2D46_EVIDENCE_CONTRACT_INVALID"
                        )

                if selected_validation_reason == "":
                    try:
                        entry_id_bytes = evidence_entry_id.encode(
                            "utf-8",
                            "strict",
                        )
                    except UnicodeEncodeError:
                        selected_validation_reason = (
                            "P2D46_EVIDENCE_CONTRACT_INVALID"
                        )

                if selected_validation_reason == "":
                    padded_entry_id = bytearray(entry_id_bytes)
                    entry_id_bit_length = len(entry_id_bytes) * 8
                    padded_entry_id.append(0x80)
                    while len(padded_entry_id) % 64 != 56:
                        padded_entry_id.append(0)
                    padded_entry_id.extend(
                        entry_id_bit_length.to_bytes(8, "big")
                    )

                    round_constants = (
                        0x428A2F98, 0x71374491, 0xB5C0FBCF,
                        0xE9B5DBA5, 0x3956C25B, 0x59F111F1,
                        0x923F82A4, 0xAB1C5ED5, 0xD807AA98,
                        0x12835B01, 0x243185BE, 0x550C7DC3,
                        0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7,
                        0xC19BF174, 0xE49B69C1, 0xEFBE4786,
                        0x0FC19DC6, 0x240CA1CC, 0x2DE92C6F,
                        0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
                        0x983E5152, 0xA831C66D, 0xB00327C8,
                        0xBF597FC7, 0xC6E00BF3, 0xD5A79147,
                        0x06CA6351, 0x14292967, 0x27B70A85,
                        0x2E1B2138, 0x4D2C6DFC, 0x53380D13,
                        0x650A7354, 0x766A0ABB, 0x81C2C92E,
                        0x92722C85, 0xA2BFE8A1, 0xA81A664B,
                        0xC24B8B70, 0xC76C51A3, 0xD192E819,
                        0xD6990624, 0xF40E3585, 0x106AA070,
                        0x19A4C116, 0x1E376C08, 0x2748774C,
                        0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A,
                        0x5B9CCA4F, 0x682E6FF3, 0x748F82EE,
                        0x78A5636F, 0x84C87814, 0x8CC70208,
                        0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7,
                        0xC67178F2,
                    )
                    mask_32 = 0xFFFFFFFF
                    hash_word_0 = 0x6A09E667
                    hash_word_1 = 0xBB67AE85
                    hash_word_2 = 0x3C6EF372
                    hash_word_3 = 0xA54FF53A
                    hash_word_4 = 0x510E527F
                    hash_word_5 = 0x9B05688C
                    hash_word_6 = 0x1F83D9AB
                    hash_word_7 = 0x5BE0CD19

                    block_start = 0
                    while block_start < len(padded_entry_id):
                        message_schedule = [0] * 64
                        schedule_index = 0
                        while schedule_index < 16:
                            word_start = block_start + schedule_index * 4
                            message_schedule[schedule_index] = (
                                padded_entry_id[word_start] << 24
                                | padded_entry_id[word_start + 1] << 16
                                | padded_entry_id[word_start + 2] << 8
                                | padded_entry_id[word_start + 3]
                            )
                            schedule_index += 1
                        while schedule_index < 64:
                            sigma_word = message_schedule[
                                schedule_index - 15
                            ]
                            small_sigma_0 = (
                                (
                                    (sigma_word >> 7)
                                    | (sigma_word << 25)
                                )
                                ^ (
                                    (sigma_word >> 18)
                                    | (sigma_word << 14)
                                )
                                ^ (sigma_word >> 3)
                            ) & mask_32
                            sigma_word = message_schedule[
                                schedule_index - 2
                            ]
                            small_sigma_1 = (
                                (
                                    (sigma_word >> 17)
                                    | (sigma_word << 15)
                                )
                                ^ (
                                    (sigma_word >> 19)
                                    | (sigma_word << 13)
                                )
                                ^ (sigma_word >> 10)
                            ) & mask_32
                            message_schedule[schedule_index] = (
                                message_schedule[schedule_index - 16]
                                + small_sigma_0
                                + message_schedule[schedule_index - 7]
                                + small_sigma_1
                            ) & mask_32
                            schedule_index += 1

                        working_0 = hash_word_0
                        working_1 = hash_word_1
                        working_2 = hash_word_2
                        working_3 = hash_word_3
                        working_4 = hash_word_4
                        working_5 = hash_word_5
                        working_6 = hash_word_6
                        working_7 = hash_word_7

                        round_index = 0
                        while round_index < 64:
                            big_sigma_1 = (
                                (
                                    (working_4 >> 6)
                                    | (working_4 << 26)
                                )
                                ^ (
                                    (working_4 >> 11)
                                    | (working_4 << 21)
                                )
                                ^ (
                                    (working_4 >> 25)
                                    | (working_4 << 7)
                                )
                            ) & mask_32
                            choice = (
                                (working_4 & working_5)
                                ^ (
                                    ((~working_4) & mask_32)
                                    & working_6
                                )
                            )
                            temporary_1 = (
                                working_7
                                + big_sigma_1
                                + choice
                                + round_constants[round_index]
                                + message_schedule[round_index]
                            ) & mask_32
                            big_sigma_0 = (
                                (
                                    (working_0 >> 2)
                                    | (working_0 << 30)
                                )
                                ^ (
                                    (working_0 >> 13)
                                    | (working_0 << 19)
                                )
                                ^ (
                                    (working_0 >> 22)
                                    | (working_0 << 10)
                                )
                            ) & mask_32
                            majority = (
                                (working_0 & working_1)
                                ^ (working_0 & working_2)
                                ^ (working_1 & working_2)
                            )
                            temporary_2 = (
                                big_sigma_0 + majority
                            ) & mask_32

                            working_7 = working_6
                            working_6 = working_5
                            working_5 = working_4
                            working_4 = (
                                working_3 + temporary_1
                            ) & mask_32
                            working_3 = working_2
                            working_2 = working_1
                            working_1 = working_0
                            working_0 = (
                                temporary_1 + temporary_2
                            ) & mask_32
                            round_index += 1

                        hash_word_0 = (
                            hash_word_0 + working_0
                        ) & mask_32
                        hash_word_1 = (
                            hash_word_1 + working_1
                        ) & mask_32
                        hash_word_2 = (
                            hash_word_2 + working_2
                        ) & mask_32
                        hash_word_3 = (
                            hash_word_3 + working_3
                        ) & mask_32
                        hash_word_4 = (
                            hash_word_4 + working_4
                        ) & mask_32
                        hash_word_5 = (
                            hash_word_5 + working_5
                        ) & mask_32
                        hash_word_6 = (
                            hash_word_6 + working_6
                        ) & mask_32
                        hash_word_7 = (
                            hash_word_7 + working_7
                        ) & mask_32
                        block_start += 64

                    entry_id_digest = (
                        f"{hash_word_0:08x}{hash_word_1:08x}"
                        f"{hash_word_2:08x}{hash_word_3:08x}"
                        f"{hash_word_4:08x}{hash_word_5:08x}"
                        f"{hash_word_6:08x}{hash_word_7:08x}"
                    )
                    expected_artifact_relative_path = (
                        "runs/by-entry-id/sha256-"
                        + entry_id_digest
                        + "/run-ledger.yaml"
                    )
                    if (
                        evidence_artifact_relative_path
                        != expected_artifact_relative_path
                    ):
                        selected_validation_reason = (
                            "P2D46_EVIDENCE_CONTRACT_INVALID"
                        )
                    else:
                        evidence_present = True

    # F. An independently valid scalar status must use the frozen vocabulary.
    if selected_validation_reason == "":
        if persistence_status not in P2D45_STATUSES:
            selected_validation_reason = "P2D46_STATUS_UNKNOWN"

    # G. Reason codes and their text are a fixed, inseparable pair.
    if selected_validation_reason == "":
        expected_upstream_reason = ""
        upstream_reason_known = False
        upstream_reason_index = 0
        while upstream_reason_index < len(P2D45_REASON_STRINGS):
            reason_entry = P2D45_REASON_STRINGS[upstream_reason_index]
            if upstream_reason_code == reason_entry[0]:
                expected_upstream_reason = reason_entry[1]
                upstream_reason_known = True
            upstream_reason_index += 1
        if (
            not upstream_reason_known
            or upstream_reason != expected_upstream_reason
        ):
            selected_validation_reason = "P2D46_REASON_CONTRACT_INVALID"

    # H. Violations are an exact built-in tuple in frozen priority order.
    if selected_validation_reason == "":
        violations_candidate = dict.__getitem__(
            run_ledger_persistence_result,
            "persistence_violations",
        )
        if type(violations_candidate) is not tuple:
            selected_validation_reason = (
                "P2D46_VIOLATIONS_CONTRACT_INVALID"
            )
        else:
            violation_types_exact = True
            violation_index = 0
            while (
                violation_index < len(violations_candidate)
                and violation_types_exact
            ):
                if type(violations_candidate[violation_index]) is not str:
                    violation_types_exact = False
                violation_index += 1

            if not violation_types_exact:
                selected_validation_reason = (
                    "P2D46_VIOLATIONS_CONTRACT_INVALID"
                )
            else:
                expected_violations: tuple[str, ...] = ()
                priority_index = 0
                while priority_index < len(P2D45_REASON_PRIORITY):
                    priority_reason = P2D45_REASON_PRIORITY[priority_index]
                    if priority_reason in violations_candidate:
                        expected_violations += (priority_reason,)
                    priority_index += 1
                if (
                    len(expected_violations) != len(violations_candidate)
                    or expected_violations != violations_candidate
                    or (
                        len(violations_candidate) > 0
                        and upstream_reason_code != violations_candidate[0]
                    )
                ):
                    selected_validation_reason = (
                        "P2D46_VIOLATIONS_CONTRACT_INVALID"
                    )
                else:
                    persistence_violations = violations_candidate

    # I. Recompute fields from the accepted violation tuple.
    if selected_validation_reason == "":
        fields_candidate = dict.__getitem__(
            run_ledger_persistence_result,
            "missing_or_invalid_fields",
        )
        if type(fields_candidate) is not tuple:
            selected_validation_reason = "P2D46_FIELDS_CONTRACT_INVALID"
        else:
            field_types_exact = True
            field_index = 0
            while field_index < len(fields_candidate) and field_types_exact:
                if type(fields_candidate[field_index]) is not str:
                    field_types_exact = False
                field_index += 1

            expected_fields: tuple[str, ...] = ()
            violation_index = 0
            while violation_index < len(persistence_violations):
                path_catalog_index = 0
                while path_catalog_index < len(P2D45_DIAGNOSTIC_PATHS):
                    path_entry = P2D45_DIAGNOSTIC_PATHS[path_catalog_index]
                    if persistence_violations[violation_index] == path_entry[0]:
                        path_index = 0
                        while path_index < len(path_entry[1]):
                            if path_entry[1][path_index] not in expected_fields:
                                expected_fields += (path_entry[1][path_index],)
                            path_index += 1
                    path_catalog_index += 1
                violation_index += 1

            if (
                not field_types_exact
                or fields_candidate != expected_fields
            ):
                selected_validation_reason = "P2D46_FIELDS_CONTRACT_INVALID"

    # J. Recompute every exact diagnostic record and its key order.
    if selected_validation_reason == "":
        diagnostics_candidate = dict.__getitem__(
            run_ledger_persistence_result,
            "diagnostic_records",
        )
        if type(diagnostics_candidate) is not tuple:
            selected_validation_reason = (
                "P2D46_DIAGNOSTICS_CONTRACT_INVALID"
            )
        else:
            expected_diagnostic_pairs: tuple[tuple[str, str], ...] = ()
            violation_index = 0
            while violation_index < len(persistence_violations):
                path_catalog_index = 0
                while path_catalog_index < len(P2D45_DIAGNOSTIC_PATHS):
                    path_entry = P2D45_DIAGNOSTIC_PATHS[path_catalog_index]
                    if persistence_violations[violation_index] == path_entry[0]:
                        path_index = 0
                        while path_index < len(path_entry[1]):
                            expected_diagnostic_pairs += (
                                (
                                    persistence_violations[violation_index],
                                    path_entry[1][path_index],
                                ),
                            )
                            path_index += 1
                    path_catalog_index += 1
                violation_index += 1

            if len(diagnostics_candidate) != len(expected_diagnostic_pairs):
                selected_validation_reason = (
                    "P2D46_DIAGNOSTICS_CONTRACT_INVALID"
                )
            else:
                diagnostic_index = 0
                while (
                    diagnostic_index < len(diagnostics_candidate)
                    and selected_validation_reason == ""
                ):
                    diagnostic_record = diagnostics_candidate[diagnostic_index]
                    if type(diagnostic_record) is not dict:
                        selected_validation_reason = (
                            "P2D46_DIAGNOSTICS_CONTRACT_INVALID"
                        )
                    else:
                        diagnostic_keys = tuple(dict.keys(diagnostic_record))
                        diagnostic_key_types_exact = True
                        diagnostic_key_index = 0
                        while diagnostic_key_index < len(diagnostic_keys):
                            if type(diagnostic_keys[diagnostic_key_index]) is not str:
                                diagnostic_key_types_exact = False
                            diagnostic_key_index += 1
                        if (
                            not diagnostic_key_types_exact
                            or diagnostic_keys != P2D46_DIAGNOSTIC_RECORD_KEYS
                        ):
                            selected_validation_reason = (
                                "P2D46_DIAGNOSTICS_CONTRACT_INVALID"
                            )
                        else:
                            diagnostic_reason = dict.__getitem__(
                                diagnostic_record,
                                "reason_code",
                            )
                            if type(diagnostic_reason) is not str:
                                selected_validation_reason = (
                                    "P2D46_DIAGNOSTICS_CONTRACT_INVALID"
                                )
                            else:
                                diagnostic_field = dict.__getitem__(
                                    diagnostic_record,
                                    "field",
                                )
                                if type(diagnostic_field) is not str:
                                    selected_validation_reason = (
                                        "P2D46_DIAGNOSTICS_CONTRACT_INVALID"
                                    )
                                elif (
                                    diagnostic_reason,
                                    diagnostic_field,
                                ) != expected_diagnostic_pairs[diagnostic_index]:
                                    selected_validation_reason = (
                                        "P2D46_DIAGNOSTICS_CONTRACT_INVALID"
                                    )
                    diagnostic_index += 1

    # K. Require the complete copied invariant tuple, byte-for-byte in order.
    if selected_validation_reason == "":
        invariants_candidate = dict.__getitem__(
            run_ledger_persistence_result,
            "invariant_refs",
        )
        if type(invariants_candidate) is not tuple:
            selected_validation_reason = (
                "P2D46_INVARIANTS_CONTRACT_INVALID"
            )
        else:
            invariant_types_exact = True
            invariant_index = 0
            while (
                invariant_index < len(invariants_candidate)
                and invariant_types_exact
            ):
                if type(invariants_candidate[invariant_index]) is not str:
                    invariant_types_exact = False
                invariant_index += 1
            if (
                not invariant_types_exact
                or invariants_candidate != P2D45_INVARIANT_REFS
            ):
                selected_validation_reason = (
                    "P2D46_INVARIANTS_CONTRACT_INVALID"
                )

    # L. Apply each status grammar independently. A structurally valid but
    # incoherent upstream fact is classified as a P2D-46 invalid result.
    if selected_validation_reason == "":
        coherent = False

        if persistence_status == "WRITTEN":
            coherent = (
                run_ledger_persisted
                and evidence_present
                and evidence_write_disposition == "WRITTEN"
                and upstream_reason_code == "RUN_LEDGER_PERSISTED"
                and persistence_violations == ()
            )
            if coherent:
                decision_status = "PERSISTENCE_ACCEPTED"
                decision_accepted = True
                decision_reason_code = "P2D46_WRITTEN_ACCEPTED"

        elif persistence_status == "ALREADY_IDENTICAL":
            coherent = (
                run_ledger_persisted
                and evidence_present
                and evidence_write_disposition == "ALREADY_IDENTICAL"
                and upstream_reason_code
                == "RUN_LEDGER_ALREADY_PERSISTED_IDENTICAL"
                and persistence_violations == ()
            )
            if coherent:
                decision_status = "PERSISTENCE_ACCEPTED"
                decision_accepted = True
                decision_reason_code = "P2D46_ALREADY_IDENTICAL_ACCEPTED"

        elif persistence_status == "NOT_ELIGIBLE":
            coherent = (
                not run_ledger_persisted
                and not evidence_present
                and upstream_reason_code == "P2D45A_ENVELOPE_NOT_ELIGIBLE"
                and persistence_violations
                == ("P2D45A_ENVELOPE_NOT_ELIGIBLE",)
            )
            if coherent:
                decision_status = "PERSISTENCE_NOT_ACCEPTED"
                decision_reason_code = "P2D46_NOT_ELIGIBLE_REJECTED"

        elif persistence_status == "INVALID":
            coherent = (
                not run_ledger_persisted
                and not evidence_present
                and upstream_reason_code == "P2D45A_SUCCESS_ENVELOPE_INVALID"
                and persistence_violations
                == ("P2D45A_SUCCESS_ENVELOPE_INVALID",)
            )
            if coherent:
                decision_status = "PERSISTENCE_NOT_ACCEPTED"
                decision_reason_code = "P2D46_UPSTREAM_INVALID_REJECTED"

        elif persistence_status == "AUTHORIZATION_FAILED":
            if not run_ledger_persisted and not evidence_present:
                grammar_index = 0
                while grammar_index < len(P2D45_AUTHORIZATION_GRAMMAR):
                    grammar_entry = P2D45_AUTHORIZATION_GRAMMAR[grammar_index]
                    if grammar_entry[0] in persistence_violations:
                        grammar_match = True
                        violation_index = 0
                        while (
                            violation_index < len(persistence_violations)
                            and grammar_match
                        ):
                            violation_code = persistence_violations[
                                violation_index
                            ]
                            if (
                                violation_code != grammar_entry[0]
                                and violation_code not in grammar_entry[1]
                            ):
                                grammar_match = False
                            violation_index += 1
                        if grammar_match:
                            coherent = True
                    grammar_index += 1
            if coherent:
                decision_status = "PERSISTENCE_NOT_ACCEPTED"
                decision_reason_code = (
                    "P2D46_AUTHORIZATION_FAILED_REJECTED"
                )

        elif persistence_status == "SERIALIZATION_FAILED":
            coherent = (
                not run_ledger_persisted
                and not evidence_present
                and upstream_reason_code == "RUN_LEDGER_SERIALIZATION_FAILED"
                and persistence_violations
                == ("RUN_LEDGER_SERIALIZATION_FAILED",)
            )
            if coherent:
                decision_status = "PERSISTENCE_NOT_ACCEPTED"
                decision_reason_code = (
                    "P2D46_SERIALIZATION_FAILED_REJECTED"
                )

        elif persistence_status == "CONFLICT":
            if (
                not run_ledger_persisted
                and not evidence_present
                and "RUN_LEDGER_CONFLICT" in persistence_violations
            ):
                conflict_auxiliaries = (
                    "PRE_FINALIZATION_IO_FAILED",
                    "FINAL_INSPECTION_CLOSE_FAILED",
                    "TEMP_FILE_CLOSE_FAILED",
                    "TEMP_CLEANUP_FAILED",
                )
                coherent = True
                violation_index = 0
                while (
                    violation_index < len(persistence_violations)
                    and coherent
                ):
                    violation_code = persistence_violations[violation_index]
                    if (
                        violation_code != "RUN_LEDGER_CONFLICT"
                        and violation_code not in conflict_auxiliaries
                    ):
                        coherent = False
                    violation_index += 1
            if coherent:
                decision_status = "PERSISTENCE_NOT_ACCEPTED"
                decision_reason_code = "P2D46_CONFLICT_REJECTED"

        elif persistence_status == "IO_FAILED":
            if not run_ledger_persisted and not evidence_present:
                grammar_index = 0
                while grammar_index < len(P2D45_IO_GRAMMAR):
                    grammar_entry = P2D45_IO_GRAMMAR[grammar_index]
                    if grammar_entry[0] in persistence_violations:
                        grammar_match = True
                        violation_index = 0
                        while (
                            violation_index < len(persistence_violations)
                            and grammar_match
                        ):
                            violation_code = persistence_violations[
                                violation_index
                            ]
                            if (
                                violation_code != grammar_entry[0]
                                and violation_code not in grammar_entry[1]
                            ):
                                grammar_match = False
                            violation_index += 1
                        if grammar_match:
                            coherent = True
                    grammar_index += 1
            if coherent:
                decision_status = "PERSISTENCE_NOT_ACCEPTED"
                decision_reason_code = "P2D46_IO_FAILED_REJECTED"

        elif persistence_status == "DURABILITY_UNCONFIRMED":
            if (
                not run_ledger_persisted
                and evidence_present
                and evidence_write_disposition == "DURABILITY_UNCONFIRMED"
            ):
                grammar_index = 0
                while grammar_index < len(P2D45_DURABILITY_GRAMMAR):
                    grammar_entry = P2D45_DURABILITY_GRAMMAR[grammar_index]
                    if grammar_entry[0] in persistence_violations:
                        grammar_match = True
                        required_index = 0
                        while required_index < len(grammar_entry[1]):
                            if (
                                grammar_entry[1][required_index]
                                not in persistence_violations
                            ):
                                grammar_match = False
                            required_index += 1
                        violation_index = 0
                        while (
                            violation_index < len(persistence_violations)
                            and grammar_match
                        ):
                            violation_code = persistence_violations[
                                violation_index
                            ]
                            if (
                                violation_code != grammar_entry[0]
                                and violation_code not in grammar_entry[1]
                                and violation_code not in grammar_entry[2]
                            ):
                                grammar_match = False
                            violation_index += 1
                        if grammar_match:
                            coherent = True
                    grammar_index += 1
            if coherent:
                decision_status = "PERSISTENCE_NOT_ACCEPTED"
                decision_reason_code = (
                    "P2D46_DURABILITY_UNCONFIRMED_REJECTED"
                )

        elif persistence_status == "PERSISTED_CLEANUP_WARNING":
            coherent = (
                run_ledger_persisted
                and evidence_present
                and evidence_write_disposition in ("WRITTEN", "ALREADY_IDENTICAL")
                and upstream_reason_code == "PERSISTED_CLEANUP_WARNING"
                and persistence_violations == ("PERSISTED_CLEANUP_WARNING",)
            )
            if coherent:
                decision_status = "PERSISTENCE_ACCEPTED_WITH_WARNING"
                decision_accepted = True
                decision_warning = True
                decision_reason_code = "P2D46_CLEANUP_WARNING_ACCEPTED"

        if not coherent:
            selected_validation_reason = "P2D46_COHERENCE_INVALID"

    # M. Allocate a wholly fresh output. Invalid results never project caller
    # outcome fields; valid results project only the five safe evidence keys.
    if selected_validation_reason != "":
        invalid_reason = ""
        invalid_path = ""
        validation_index = 0
        while validation_index < len(P2D46_VALIDATION_REASON_CODES):
            if (
                selected_validation_reason
                == P2D46_VALIDATION_REASON_CODES[validation_index]
            ):
                invalid_path = P2D46_DIAGNOSTIC_PATHS[validation_index]
            validation_index += 1
        reason_index = 0
        while reason_index < len(P2D46_REASON_STRINGS):
            reason_entry = P2D46_REASON_STRINGS[reason_index]
            if selected_validation_reason == reason_entry[0]:
                invalid_reason = reason_entry[1]
            reason_index += 1

        invalid_diagnostic = {
            "reason_code": selected_validation_reason,
            "field": invalid_path,
        }
        return {
            "decision_created": False,
            "decision_status": "PERSISTENCE_RESULT_INVALID",
            "accepted": False,
            "warning": False,
            "reason_code": selected_validation_reason,
            "reason": invalid_reason,
            "source": {
                "boundary_scope": P2D46_BOUNDARY_SCOPE,
                "schema_version": P2D46_SCHEMA_VERSION,
                "upstream_boundary_scope": "run_ledger_persistence_boundary",
                "upstream_schema_version": P2D45_SCHEMA_VERSION,
                "upstream_artifact_name": "run-ledger.yaml",
                "upstream_persistence_status": "",
                "upstream_reason_code": "",
                "upstream_write_disposition": "",
            },
            "persistence_evidence": {},
            "decision_violations": (selected_validation_reason,),
            "missing_or_invalid_fields": (invalid_path,),
            "diagnostic_records": (invalid_diagnostic,),
            "invariant_refs": P2D46_INVARIANT_REFS,
        }

    decision_reason = ""
    reason_index = 0
    while reason_index < len(P2D46_REASON_STRINGS):
        reason_entry = P2D46_REASON_STRINGS[reason_index]
        if decision_reason_code == reason_entry[0]:
            decision_reason = reason_entry[1]
        reason_index += 1

    if evidence_present:
        projected_evidence: dict[str, object] = {
            "artifact_relative_path": evidence_artifact_relative_path,
            "serialization_format": evidence_serialization_format,
            "content_digest_algorithm": evidence_content_digest_algorithm,
            "content_digest": evidence_content_digest,
            "write_disposition": evidence_write_disposition,
        }
    else:
        projected_evidence = {}

    return {
        "decision_created": True,
        "decision_status": decision_status,
        "accepted": decision_accepted,
        "warning": decision_warning,
        "reason_code": decision_reason_code,
        "reason": decision_reason,
        "source": {
            "boundary_scope": P2D46_BOUNDARY_SCOPE,
            "schema_version": P2D46_SCHEMA_VERSION,
            "upstream_boundary_scope": "run_ledger_persistence_boundary",
            "upstream_schema_version": P2D45_SCHEMA_VERSION,
            "upstream_artifact_name": "run-ledger.yaml",
            "upstream_persistence_status": persistence_status,
            "upstream_reason_code": upstream_reason_code,
            "upstream_write_disposition": evidence_write_disposition,
        },
        "persistence_evidence": projected_evidence,
        "decision_violations": (),
        "missing_or_invalid_fields": (),
        "diagnostic_records": (),
        "invariant_refs": P2D46_INVARIANT_REFS,
    }
