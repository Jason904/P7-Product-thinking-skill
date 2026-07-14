"""Frozen P2D-47 coordinator skeleton for bounded P2D-45 to P2D-46 coordination.

This boundary has no final-close, transition, achieved NOOP_COMPLETED, quality,
publication, public-URL, or notification authority.
"""

from ai_daily_publishing_system.core import (
    run_ledger_persistence as _run_ledger_persistence,
)
from ai_daily_publishing_system.core import (
    run_ledger_persistence_consumption_decision as _run_ledger_persistence_consumption_decision,
)


_P2D47_ROOT_KEYS = (
    "orchestration_receipt_created",
    "orchestration_status",
    "accepted",
    "warning",
    "reason_code",
    "reason",
    "source",
    "persistence_evidence",
    "orchestration_violations",
    "missing_or_invalid_fields",
    "diagnostic_records",
    "invariant_refs",
)
_P2D47_STATUSES = (
    "PERSISTENCE_COORDINATION_ACCEPTED",
    "PERSISTENCE_COORDINATION_ACCEPTED_WITH_WARNING",
    "PERSISTENCE_COORDINATION_REJECTED",
    "PERSISTENCE_COORDINATION_INVALID",
    "PERSISTENCE_COORDINATION_UNCONFIRMED",
)
_P2D47_BOOLEAN_MATRIX = (
    ("PERSISTENCE_COORDINATION_ACCEPTED", True, True, False),
    ("PERSISTENCE_COORDINATION_ACCEPTED_WITH_WARNING", True, True, True),
    ("PERSISTENCE_COORDINATION_REJECTED", True, False, False),
    ("PERSISTENCE_COORDINATION_INVALID", False, False, False),
    ("PERSISTENCE_COORDINATION_UNCONFIRMED", False, False, False),
)
_P2D47_PROHIBITED_STATUS_VOCABULARY = (
    "RUN_COMPLETED",
    "COMPLETED",
    "TRANSITIONED",
    "PASS",
    "PASS_PUBLISHED",
    "PUBLISHED",
    "NOOP_COMPLETED",
    "PUBLISH_ALLOWED",
)
_P2D47_SOURCE_KEYS = (
    "boundary_scope",
    "schema_version",
    "persistence_boundary_scope",
    "persistence_schema_version",
    "consumption_boundary_scope",
    "consumption_schema_version",
    "upstream_artifact_name",
    "upstream_persistence_status",
    "upstream_reason_code",
    "upstream_write_disposition",
    "consumption_decision_status",
    "consumption_reason_code",
)
_P2D47_SOURCE_FIXED_VALUES = (
    ("boundary_scope", "local_noop_run_ledger_persistence_coordinator"),
    ("schema_version", "p2d47.local_noop_run_ledger_persistence_coordinator.v1"),
    ("persistence_boundary_scope", "run_ledger_persistence_boundary"),
    ("persistence_schema_version", "p2d45.run_ledger_persistence.v1"),
    ("consumption_boundary_scope", "run_ledger_persistence_consumption_decision"),
    ("consumption_schema_version", "p2d46.run_ledger_persistence_consumption_decision.v1"),
    ("upstream_artifact_name", "run-ledger.yaml"),
)
_P2D47_SAFE_EVIDENCE_KEYS = (
    "artifact_relative_path",
    "serialization_format",
    "content_digest_algorithm",
    "content_digest",
    "write_disposition",
)
_P2D47_DIAGNOSTIC_PATHS = (
    "p2d47.persistence_invocation",
    "p2d47.consumption_invocation",
    "p2d47.consumption_result",
)
_P2D47_REASON_PAIRS = (
    (
        "P2D47_PERSISTENCE_ACCEPTED",
        "The exact P2D-46 decision accepted durable run-ledger persistence without warning.",
    ),
    (
        "P2D47_PERSISTENCE_ACCEPTED_WITH_WARNING",
        "The exact P2D-46 decision accepted durable run-ledger persistence with a preserved cleanup warning.",
    ),
    (
        "P2D47_PERSISTENCE_REJECTED",
        "The exact P2D-46 decision did not accept the persistence result.",
    ),
    (
        "P2D47_PERSISTENCE_DECISION_INVALID",
        "The exact P2D-46 decision classified the P2D-45 persistence result as invalid.",
    ),
    (
        "P2D47_PERSISTENCE_INVOCATION_OUTCOME_UNCONFIRMED",
        "P2D-45 raised an exception, so the persistence invocation outcome is unconfirmed.",
    ),
    (
        "P2D47_CONSUMPTION_INVOCATION_OUTCOME_UNCONFIRMED",
        "P2D-46 raised an exception, so consumption of the persistence result is unconfirmed.",
    ),
    (
        "P2D47_CONSUMPTION_RESULT_INVALID",
        "The P2D-46 return value did not satisfy the exact frozen consumption-decision contract.",
    ),
)
_P2D47_REASON_PRIORITY = (
    "P2D47_PERSISTENCE_INVOCATION_OUTCOME_UNCONFIRMED",
    "P2D47_CONSUMPTION_INVOCATION_OUTCOME_UNCONFIRMED",
    "P2D47_CONSUMPTION_RESULT_INVALID",
    "P2D47_PERSISTENCE_DECISION_INVALID",
    "P2D47_PERSISTENCE_REJECTED",
    "P2D47_PERSISTENCE_ACCEPTED_WITH_WARNING",
    "P2D47_PERSISTENCE_ACCEPTED",
)
_P2D47_INVARIANTS = (
    "P2D47_P_COORDINATOR_ONLY_AUTHORITY",
    "P2D47_P_INPUTS_FORWARDED_WITHOUT_INSPECTION_OR_RETENTION",
    "P2D47_P_P2D45_CALLED_AT_MOST_ONCE",
    "P2D47_P_P2D46_CALLED_AT_MOST_ONCE",
    "P2D47_P_P2D45_NORMAL_RETURN_STRICTLY_PRECEDES_P2D46",
    "P2D47_P_EXACT_P2D45_RETURN_OBJECT_IDENTITY_FORWARDED",
    "P2D47_P_EXACT_P2D46_RETURN_CONTRACT_REQUIRED",
    "P2D47_P_CATCH_EXCEPTION_ONLY",
    "P2D47_P_BASEEXCEPTION_PROPAGATES",
    "P2D47_P_EXCEPTION_OBJECT_DETAILS_SUPPRESSED_AND_NOT_RETAINED",
    "P2D47_P_NO_RETRY_FALLBACK_OR_ALTERNATE_PERSISTENCE",
    "P2D47_P_EFFECT_ONLY_THROUGH_P2D45",
    "P2D47_P_NO_DIRECT_FILESYSTEM",
    "P2D47_P_P2D46_PERSISTENCE_CLASSIFICATION_AUTHORITATIVE",
    "P2D47_P_ACCEPTED_IS_NOT_RUN_COMPLETED",
    "P2D47_P_ACCEPTED_WITH_WARNING_IS_NOT_RUN_COMPLETED",
    "P2D47_P_CLEANUP_WARNING_PRESERVED",
    "P2D47_P_NO_TRANSITION_REQUEST_OR_EXECUTION",
    "P2D47_P_NOT_FINAL_RUN_LEDGER_CLOSE",
    "P2D47_P_NO_FINAL_HASH_AUTHORITY",
    "P2D47_P_NO_RUNTIME_QUALITY_PUBLICATION_OR_NOTIFICATION",
    "P2D47_P_SAFE_EVIDENCE_ALLOWLIST_ONLY",
    "P2D47_P_CALLER_SIBLING_AND_EXCEPTION_DETAILS_SUPPRESSED",
    "P2D47_P_RESULT_CONTAINERS_FRESH_AND_NONALIASED",
    "P2D47_P_NOOP_COMPLETED_ABSENT_FROM_OUTPUT_STATUS_VOCABULARY",
    "P2D47_P_PASS_PUBLISHED_FORBIDDEN",
)

_P2D46_ROOT_KEYS = (
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
_P2D46_SOURCE_KEYS = (
    "boundary_scope",
    "schema_version",
    "upstream_boundary_scope",
    "upstream_schema_version",
    "upstream_artifact_name",
    "upstream_persistence_status",
    "upstream_reason_code",
    "upstream_write_disposition",
)
_P2D46_SOURCE_FIXED_VALUES = (
    ("boundary_scope", "run_ledger_persistence_consumption_decision"),
    ("schema_version", "p2d46.run_ledger_persistence_consumption_decision.v1"),
    ("upstream_boundary_scope", "run_ledger_persistence_boundary"),
    ("upstream_schema_version", "p2d45.run_ledger_persistence.v1"),
    ("upstream_artifact_name", "run-ledger.yaml"),
)
_P2D46_SAFE_EVIDENCE_KEYS = (
    "artifact_relative_path",
    "serialization_format",
    "content_digest_algorithm",
    "content_digest",
    "write_disposition",
)
_P2D46_STATUSES = (
    "PERSISTENCE_ACCEPTED",
    "PERSISTENCE_ACCEPTED_WITH_WARNING",
    "PERSISTENCE_NOT_ACCEPTED",
    "PERSISTENCE_RESULT_INVALID",
)
_P2D46_BOOLEAN_MATRIX = (
    ("PERSISTENCE_ACCEPTED", True, True, False),
    ("PERSISTENCE_ACCEPTED_WITH_WARNING", True, True, True),
    ("PERSISTENCE_NOT_ACCEPTED", True, False, False),
    ("PERSISTENCE_RESULT_INVALID", False, False, False),
)
_P2D46_REASON_PAIRS = (
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
_P2D46_INVALID_REASON_PATH_PAIRS = (
    ("P2D46_RESULT_NOT_EXACT_DICT", "run_ledger_persistence_result"),
    ("P2D46_FORBIDDEN_BYPASS", "p2d46.forbidden_bypass"),
    ("P2D46_RESULT_KEYS_INVALID", "run_ledger_persistence_result.keys"),
    ("P2D46_RESULT_FIELD_TYPE_INVALID", "run_ledger_persistence_result.scalar_fields"),
    ("P2D46_SOURCE_CONTRACT_INVALID", "run_ledger_persistence_result.source"),
    ("P2D46_EVIDENCE_CONTRACT_INVALID", "run_ledger_persistence_result.persistence_evidence"),
    ("P2D46_STATUS_UNKNOWN", "run_ledger_persistence_result.persistence_status"),
    ("P2D46_REASON_CONTRACT_INVALID", "run_ledger_persistence_result.reason_contract"),
    ("P2D46_VIOLATIONS_CONTRACT_INVALID", "run_ledger_persistence_result.persistence_violations"),
    ("P2D46_FIELDS_CONTRACT_INVALID", "run_ledger_persistence_result.missing_or_invalid_fields"),
    ("P2D46_DIAGNOSTICS_CONTRACT_INVALID", "run_ledger_persistence_result.diagnostic_records"),
    ("P2D46_INVARIANTS_CONTRACT_INVALID", "run_ledger_persistence_result.invariant_refs"),
    ("P2D46_COHERENCE_INVALID", "run_ledger_persistence_result.coherence"),
)
_P2D46_INVARIANTS = (
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
_P2D46_SERIALIZATION_FORMAT = "canonical_json_yaml_1_2_subset"
_P2D46_CONTENT_DIGEST_ALGORITHM = "sha256"
_P2D46_WRITE_DISPOSITIONS = (
    "WRITTEN",
    "ALREADY_IDENTICAL",
    "DURABILITY_UNCONFIRMED",
)
_P2D46_NORMAL_FAMILY_MATRIX = (
    ("WRITTEN", ("RUN_LEDGER_PERSISTED",)),
    ("ALREADY_IDENTICAL", ("RUN_LEDGER_ALREADY_PERSISTED_IDENTICAL",)),
    ("NOT_ELIGIBLE", ("P2D45A_ENVELOPE_NOT_ELIGIBLE",)),
    ("INVALID", ("P2D45A_SUCCESS_ENVELOPE_INVALID",)),
    ("AUTHORIZATION_FAILED", ("DESTINATION_ROOT_INVALID", "DESTINATION_PATH_UNSAFE")),
    ("SERIALIZATION_FAILED", ("RUN_LEDGER_SERIALIZATION_FAILED",)),
    ("CONFLICT", ("RUN_LEDGER_CONFLICT",)),
    (
        "IO_FAILED",
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
        (
            "FINAL_IDENTITY_VERIFICATION_FAILED",
            "FINAL_DURABILITY_UNCONFIRMED",
            "PRE_FINALIZATION_IO_FAILED",
        ),
    ),
    ("PERSISTED_CLEANUP_WARNING", ("PERSISTED_CLEANUP_WARNING",)),
)
_P2D46_IMPOSSIBLE_PRE_SURFACES = (
    ("AUTHORIZATION_FAILED", "PRE_FINALIZATION_IO_FAILED"),
    ("CONFLICT", "PRE_FINALIZATION_IO_FAILED"),
)


def coordinate_local_noop_run_ledger_persistence(
    *,
    run_ledger_entry_assembly: dict[str, object],
    authorized_ops_root: str,
) -> dict[str, object]:
    invocation_failure_reason_code = ""
    try:
        persistence_result = _run_ledger_persistence.persist_run_ledger_entry(
            run_ledger_entry_assembly=run_ledger_entry_assembly,
            authorized_ops_root=authorized_ops_root,
        )
    except Exception:
        invocation_failure_reason_code = (
            "P2D47_PERSISTENCE_INVOCATION_OUTCOME_UNCONFIRMED"
        )

    if invocation_failure_reason_code == "":
        try:
            consumption_result = (
                _run_ledger_persistence_consumption_decision
                .build_run_ledger_persistence_consumption_decision(
                    run_ledger_persistence_result=persistence_result,
                )
            )
        except Exception:
            invocation_failure_reason_code = (
                "P2D47_CONSUMPTION_INVOCATION_OUTCOME_UNCONFIRMED"
            )

    decision_contract_valid = invocation_failure_reason_code == ""
    decision_created = False
    decision_status = ""
    decision_accepted = False
    decision_warning = False
    decision_reason_code = ""
    decision_reason = ""
    decision_violations: tuple[object, ...] = ()
    decision_missing_or_invalid_fields: tuple[object, ...] = ()
    decision_diagnostic_records: tuple[object, ...] = ()
    decision_invariant_refs: tuple[object, ...] = ()

    source_upstream_persistence_status = ""
    source_upstream_reason_code = ""
    source_upstream_write_disposition = ""

    evidence_present = False
    evidence_artifact_relative_path = ""
    evidence_serialization_format = ""
    evidence_content_digest_algorithm = ""
    evidence_content_digest = ""
    evidence_write_disposition = ""

    if decision_contract_valid:
        if type(consumption_result) is not dict:
            decision_contract_valid = False

    if decision_contract_valid:
        decision_root_keys = tuple(dict.keys(consumption_result))
        decision_root_key_types_exact = True
        decision_root_key_index = 0
        while decision_root_key_index < len(decision_root_keys):
            if type(decision_root_keys[decision_root_key_index]) is not str:
                decision_root_key_types_exact = False
            decision_root_key_index += 1
        if (
            not decision_root_key_types_exact
            or decision_root_keys != _P2D46_ROOT_KEYS
        ):
            decision_contract_valid = False

    if decision_contract_valid:
        decision_created_candidate = consumption_result[
            "decision_created"
        ]
        decision_status_candidate = consumption_result["decision_status"]
        decision_accepted_candidate = consumption_result["accepted"]
        decision_warning_candidate = consumption_result["warning"]
        decision_reason_code_candidate = consumption_result["reason_code"]
        decision_reason_candidate = consumption_result["reason"]
        if (
            type(decision_created_candidate) is not bool
            or type(decision_status_candidate) is not str
            or type(decision_accepted_candidate) is not bool
            or type(decision_warning_candidate) is not bool
            or type(decision_reason_code_candidate) is not str
            or type(decision_reason_candidate) is not str
        ):
            decision_contract_valid = False
        else:
            decision_created = decision_created_candidate
            decision_status = decision_status_candidate
            decision_accepted = decision_accepted_candidate
            decision_warning = decision_warning_candidate
            decision_reason_code = decision_reason_code_candidate
            decision_reason = decision_reason_candidate

    if decision_contract_valid:
        source_candidate = consumption_result["source"]
        if type(source_candidate) is not dict:
            decision_contract_valid = False
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
                or source_keys != _P2D46_SOURCE_KEYS
            ):
                decision_contract_valid = False
            else:
                source_values: list[str] = []
                source_value_index = 0
                while (
                    source_value_index < len(_P2D46_SOURCE_KEYS)
                    and decision_contract_valid
                ):
                    source_value = source_candidate[
                        _P2D46_SOURCE_KEYS[source_value_index]
                    ]
                    if type(source_value) is not str:
                        decision_contract_valid = False
                    else:
                        source_values.append(source_value)
                    source_value_index += 1

                source_fixed_index = 0
                while (
                    source_fixed_index < len(_P2D46_SOURCE_FIXED_VALUES)
                    and decision_contract_valid
                ):
                    if (
                        source_values[source_fixed_index]
                        != _P2D46_SOURCE_FIXED_VALUES[source_fixed_index][1]
                    ):
                        decision_contract_valid = False
                    source_fixed_index += 1

                if decision_contract_valid:
                    source_upstream_persistence_status = source_values[5]
                    source_upstream_reason_code = source_values[6]
                    source_upstream_write_disposition = source_values[7]

    if decision_contract_valid:
        evidence_candidate = consumption_result["persistence_evidence"]
        if type(evidence_candidate) is not dict:
            decision_contract_valid = False
        else:
            evidence_keys = tuple(dict.keys(evidence_candidate))
            evidence_key_types_exact = True
            evidence_key_index = 0
            while evidence_key_index < len(evidence_keys):
                if type(evidence_keys[evidence_key_index]) is not str:
                    evidence_key_types_exact = False
                evidence_key_index += 1

            if not evidence_key_types_exact:
                decision_contract_valid = False
            elif evidence_keys == ():
                evidence_present = False
            elif evidence_keys != _P2D46_SAFE_EVIDENCE_KEYS:
                decision_contract_valid = False
            else:
                evidence_values: list[str] = []
                evidence_value_index = 0
                while (
                    evidence_value_index < len(_P2D46_SAFE_EVIDENCE_KEYS)
                    and decision_contract_valid
                ):
                    evidence_value = evidence_candidate[
                        _P2D46_SAFE_EVIDENCE_KEYS[evidence_value_index]
                    ]
                    if type(evidence_value) is not str:
                        decision_contract_valid = False
                    else:
                        evidence_values.append(evidence_value)
                    evidence_value_index += 1

                if decision_contract_valid:
                    evidence_artifact_relative_path = evidence_values[0]
                    evidence_serialization_format = evidence_values[1]
                    evidence_content_digest_algorithm = evidence_values[2]
                    evidence_content_digest = evidence_values[3]
                    evidence_write_disposition = evidence_values[4]

                    artifact_path_prefix = "runs/by-entry-id/sha256-"
                    artifact_path_suffix = "/run-ledger.yaml"
                    artifact_path_digest = ""
                    if (
                        evidence_artifact_relative_path.startswith(
                            artifact_path_prefix
                        )
                        and evidence_artifact_relative_path.endswith(
                            artifact_path_suffix
                        )
                    ):
                        artifact_path_digest = evidence_artifact_relative_path[
                            len(artifact_path_prefix):
                            -len(artifact_path_suffix)
                        ]

                    artifact_path_digest_valid = (
                        len(artifact_path_digest) == 64
                    )
                    artifact_path_digest_index = 0
                    while (
                        artifact_path_digest_index
                        < len(artifact_path_digest)
                        and artifact_path_digest_valid
                    ):
                        if (
                            artifact_path_digest[artifact_path_digest_index]
                            not in "0123456789abcdef"
                        ):
                            artifact_path_digest_valid = False
                        artifact_path_digest_index += 1

                    content_digest_valid = (
                        len(evidence_content_digest) == 64
                    )
                    content_digest_index = 0
                    while (
                        content_digest_index < len(evidence_content_digest)
                        and content_digest_valid
                    ):
                        if (
                            evidence_content_digest[content_digest_index]
                            not in "0123456789abcdef"
                        ):
                            content_digest_valid = False
                        content_digest_index += 1

                    if (
                        not artifact_path_digest_valid
                        or evidence_serialization_format
                        != _P2D46_SERIALIZATION_FORMAT
                        or evidence_content_digest_algorithm
                        != _P2D46_CONTENT_DIGEST_ALGORITHM
                        or not content_digest_valid
                        or evidence_write_disposition
                        not in _P2D46_WRITE_DISPOSITIONS
                    ):
                        decision_contract_valid = False
                    else:
                        evidence_present = True

    if decision_contract_valid:
        if decision_status not in _P2D46_STATUSES:
            decision_contract_valid = False
        else:
            boolean_family_matched = False
            boolean_matrix_index = 0
            while boolean_matrix_index < len(_P2D46_BOOLEAN_MATRIX):
                boolean_row = _P2D46_BOOLEAN_MATRIX[boolean_matrix_index]
                if decision_status == boolean_row[0]:
                    boolean_family_matched = True
                    if (
                        decision_created is not boolean_row[1]
                        or decision_accepted is not boolean_row[2]
                        or decision_warning is not boolean_row[3]
                    ):
                        decision_contract_valid = False
                boolean_matrix_index += 1
            if not boolean_family_matched:
                decision_contract_valid = False

    if decision_contract_valid:
        expected_decision_reason = ""
        decision_reason_known = False
        decision_reason_index = 0
        while decision_reason_index < len(_P2D46_REASON_PAIRS):
            reason_pair = _P2D46_REASON_PAIRS[decision_reason_index]
            if decision_reason_code == reason_pair[0]:
                expected_decision_reason = reason_pair[1]
                decision_reason_known = True
            decision_reason_index += 1
        if (
            not decision_reason_known
            or decision_reason != expected_decision_reason
        ):
            decision_contract_valid = False

    if decision_contract_valid:
        decision_violations_candidate = consumption_result[
            "decision_violations"
        ]
        decision_missing_candidate = consumption_result[
            "missing_or_invalid_fields"
        ]
        decision_diagnostics_candidate = consumption_result[
            "diagnostic_records"
        ]
        decision_invariants_candidate = consumption_result["invariant_refs"]
        if (
            type(decision_violations_candidate) is not tuple
            or type(decision_missing_candidate) is not tuple
            or type(decision_diagnostics_candidate) is not tuple
            or type(decision_invariants_candidate) is not tuple
        ):
            decision_contract_valid = False
        else:
            decision_violations = decision_violations_candidate
            decision_missing_or_invalid_fields = decision_missing_candidate
            decision_diagnostic_records = decision_diagnostics_candidate
            decision_invariant_refs = decision_invariants_candidate

    if decision_contract_valid:
        tuple_fields = (
            decision_violations,
            decision_missing_or_invalid_fields,
            decision_invariant_refs,
        )
        tuple_field_index = 0
        while (
            tuple_field_index < len(tuple_fields)
            and decision_contract_valid
        ):
            tuple_field = tuple_fields[tuple_field_index]
            tuple_item_index = 0
            while tuple_item_index < len(tuple_field):
                if type(tuple_field[tuple_item_index]) is not str:
                    decision_contract_valid = False
                tuple_item_index += 1
            tuple_field_index += 1

    if decision_contract_valid:
        diagnostic_index = 0
        while (
            diagnostic_index < len(decision_diagnostic_records)
            and decision_contract_valid
        ):
            diagnostic_record = decision_diagnostic_records[diagnostic_index]
            if type(diagnostic_record) is not dict:
                decision_contract_valid = False
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
                    or diagnostic_keys != ("reason_code", "field")
                ):
                    decision_contract_valid = False
                else:
                    diagnostic_reason = diagnostic_record["reason_code"]
                    diagnostic_field = diagnostic_record["field"]
                    if (
                        type(diagnostic_reason) is not str
                        or type(diagnostic_field) is not str
                    ):
                        decision_contract_valid = False
            diagnostic_index += 1

    if decision_contract_valid:
        if decision_invariant_refs != _P2D46_INVARIANTS:
            decision_contract_valid = False

    if decision_contract_valid:
        if decision_status == "PERSISTENCE_RESULT_INVALID":
            invalid_reason_path = ""
            invalid_reason_index = 0
            while invalid_reason_index < len(
                _P2D46_INVALID_REASON_PATH_PAIRS
            ):
                invalid_pair = _P2D46_INVALID_REASON_PATH_PAIRS[
                    invalid_reason_index
                ]
                if decision_reason_code == invalid_pair[0]:
                    invalid_reason_path = invalid_pair[1]
                invalid_reason_index += 1

            if (
                invalid_reason_path == ""
                or source_upstream_persistence_status != ""
                or source_upstream_reason_code != ""
                or source_upstream_write_disposition != ""
                or evidence_present
                or decision_violations != (decision_reason_code,)
                or decision_missing_or_invalid_fields
                != (invalid_reason_path,)
                or len(decision_diagnostic_records) != 1
            ):
                decision_contract_valid = False
            else:
                invalid_diagnostic = decision_diagnostic_records[0]
                if (
                    invalid_diagnostic["reason_code"]
                    != decision_reason_code
                    or invalid_diagnostic["field"] != invalid_reason_path
                ):
                    decision_contract_valid = False
        else:
            normal_family_matched = False
            normal_family_index = 0
            while normal_family_index < len(_P2D46_NORMAL_FAMILY_MATRIX):
                normal_family = _P2D46_NORMAL_FAMILY_MATRIX[
                    normal_family_index
                ]
                if (
                    source_upstream_persistence_status == normal_family[0]
                    and source_upstream_reason_code in normal_family[1]
                ):
                    normal_family_matched = True
                    expected_decision_reason_code = _P2D46_REASON_PAIRS[
                        normal_family_index
                    ][0]
                    expected_decision_status = "PERSISTENCE_NOT_ACCEPTED"
                    evidence_contract_matched = not evidence_present

                    if normal_family[0] == "WRITTEN":
                        expected_decision_status = "PERSISTENCE_ACCEPTED"
                        evidence_contract_matched = (
                            evidence_present
                            and source_upstream_write_disposition == "WRITTEN"
                            and evidence_write_disposition == "WRITTEN"
                        )
                    elif normal_family[0] == "ALREADY_IDENTICAL":
                        expected_decision_status = "PERSISTENCE_ACCEPTED"
                        evidence_contract_matched = (
                            evidence_present
                            and source_upstream_write_disposition
                            == "ALREADY_IDENTICAL"
                            and evidence_write_disposition
                            == "ALREADY_IDENTICAL"
                        )
                    elif normal_family[0] == "DURABILITY_UNCONFIRMED":
                        evidence_contract_matched = (
                            evidence_present
                            and source_upstream_write_disposition
                            == "DURABILITY_UNCONFIRMED"
                            and evidence_write_disposition
                            == "DURABILITY_UNCONFIRMED"
                        )
                    elif normal_family[0] == "PERSISTED_CLEANUP_WARNING":
                        expected_decision_status = (
                            "PERSISTENCE_ACCEPTED_WITH_WARNING"
                        )
                        evidence_contract_matched = (
                            evidence_present
                            and source_upstream_write_disposition
                            in ("WRITTEN", "ALREADY_IDENTICAL")
                            and evidence_write_disposition
                            == source_upstream_write_disposition
                        )
                    else:
                        evidence_contract_matched = (
                            not evidence_present
                            and source_upstream_write_disposition == ""
                        )

                    impossible_surface = False
                    impossible_index = 0
                    while impossible_index < len(
                        _P2D46_IMPOSSIBLE_PRE_SURFACES
                    ):
                        impossible_pair = _P2D46_IMPOSSIBLE_PRE_SURFACES[
                            impossible_index
                        ]
                        if (
                            source_upstream_persistence_status
                            == impossible_pair[0]
                            and source_upstream_reason_code
                            == impossible_pair[1]
                        ):
                            impossible_surface = True
                        impossible_index += 1

                    if (
                        decision_status != expected_decision_status
                        or decision_reason_code
                        != expected_decision_reason_code
                        or not evidence_contract_matched
                        or impossible_surface
                    ):
                        decision_contract_valid = False
                normal_family_index += 1

            if (
                not normal_family_matched
                or decision_violations != ()
                or decision_missing_or_invalid_fields != ()
                or decision_diagnostic_records != ()
            ):
                decision_contract_valid = False

    if invocation_failure_reason_code != "":
        orchestration_reason_code = invocation_failure_reason_code
        orchestration_status = "PERSISTENCE_COORDINATION_UNCONFIRMED"
    elif not decision_contract_valid:
        orchestration_reason_code = "P2D47_CONSUMPTION_RESULT_INVALID"
        orchestration_status = "PERSISTENCE_COORDINATION_INVALID"
    elif decision_status == "PERSISTENCE_ACCEPTED":
        orchestration_reason_code = "P2D47_PERSISTENCE_ACCEPTED"
        orchestration_status = "PERSISTENCE_COORDINATION_ACCEPTED"
    elif decision_status == "PERSISTENCE_ACCEPTED_WITH_WARNING":
        orchestration_reason_code = (
            "P2D47_PERSISTENCE_ACCEPTED_WITH_WARNING"
        )
        orchestration_status = (
            "PERSISTENCE_COORDINATION_ACCEPTED_WITH_WARNING"
        )
    elif decision_status == "PERSISTENCE_NOT_ACCEPTED":
        orchestration_reason_code = "P2D47_PERSISTENCE_REJECTED"
        orchestration_status = "PERSISTENCE_COORDINATION_REJECTED"
    else:
        orchestration_reason_code = "P2D47_PERSISTENCE_DECISION_INVALID"
        orchestration_status = "PERSISTENCE_COORDINATION_INVALID"

    orchestration_receipt_created = False
    orchestration_accepted = False
    orchestration_warning = False
    orchestration_boolean_index = 0
    while orchestration_boolean_index < len(_P2D47_BOOLEAN_MATRIX):
        orchestration_boolean_row = _P2D47_BOOLEAN_MATRIX[
            orchestration_boolean_index
        ]
        if orchestration_status == orchestration_boolean_row[0]:
            orchestration_receipt_created = orchestration_boolean_row[1]
            orchestration_accepted = orchestration_boolean_row[2]
            orchestration_warning = orchestration_boolean_row[3]
        orchestration_boolean_index += 1

    orchestration_reason = ""
    orchestration_reason_index = 0
    while orchestration_reason_index < len(_P2D47_REASON_PAIRS):
        orchestration_reason_pair = _P2D47_REASON_PAIRS[
            orchestration_reason_index
        ]
        if orchestration_reason_code == orchestration_reason_pair[0]:
            orchestration_reason = orchestration_reason_pair[1]
        orchestration_reason_index += 1

    if decision_contract_valid:
        projected_upstream_persistence_status = (
            source_upstream_persistence_status
        )
        projected_upstream_reason_code = source_upstream_reason_code
        projected_upstream_write_disposition = (
            source_upstream_write_disposition
        )
        projected_consumption_decision_status = decision_status
        projected_consumption_reason_code = decision_reason_code
    else:
        projected_upstream_persistence_status = ""
        projected_upstream_reason_code = ""
        projected_upstream_write_disposition = ""
        projected_consumption_decision_status = ""
        projected_consumption_reason_code = ""

    projected_source: dict[str, object] = {
        "boundary_scope": _P2D47_SOURCE_FIXED_VALUES[0][1],
        "schema_version": _P2D47_SOURCE_FIXED_VALUES[1][1],
        "persistence_boundary_scope": _P2D47_SOURCE_FIXED_VALUES[2][1],
        "persistence_schema_version": _P2D47_SOURCE_FIXED_VALUES[3][1],
        "consumption_boundary_scope": _P2D47_SOURCE_FIXED_VALUES[4][1],
        "consumption_schema_version": _P2D47_SOURCE_FIXED_VALUES[5][1],
        "upstream_artifact_name": _P2D47_SOURCE_FIXED_VALUES[6][1],
        "upstream_persistence_status": projected_upstream_persistence_status,
        "upstream_reason_code": projected_upstream_reason_code,
        "upstream_write_disposition": projected_upstream_write_disposition,
        "consumption_decision_status": projected_consumption_decision_status,
        "consumption_reason_code": projected_consumption_reason_code,
    }

    if decision_contract_valid and evidence_present:
        projected_evidence: dict[str, object] = {
            "artifact_relative_path": evidence_artifact_relative_path,
            "serialization_format": evidence_serialization_format,
            "content_digest_algorithm": evidence_content_digest_algorithm,
            "content_digest": evidence_content_digest,
            "write_disposition": evidence_write_disposition,
        }
    else:
        projected_evidence = {}

    diagnostic_path = ""
    if orchestration_reason_code == (
        "P2D47_PERSISTENCE_INVOCATION_OUTCOME_UNCONFIRMED"
    ):
        diagnostic_path = _P2D47_DIAGNOSTIC_PATHS[0]
    elif orchestration_reason_code == (
        "P2D47_CONSUMPTION_INVOCATION_OUTCOME_UNCONFIRMED"
    ):
        diagnostic_path = _P2D47_DIAGNOSTIC_PATHS[1]
    elif orchestration_status == "PERSISTENCE_COORDINATION_INVALID":
        diagnostic_path = _P2D47_DIAGNOSTIC_PATHS[2]

    if diagnostic_path == "":
        orchestration_violations: tuple[str, ...] = ()
        orchestration_missing_or_invalid_fields: tuple[str, ...] = ()
        orchestration_diagnostic_records: tuple[dict[str, str], ...] = ()
    else:
        orchestration_violations = (orchestration_reason_code,)
        orchestration_missing_or_invalid_fields = (diagnostic_path,)
        orchestration_diagnostic_records = ({
            "reason_code": orchestration_reason_code,
            "field": diagnostic_path,
        },)

    orchestration_invariant_refs: tuple[str, ...] = ()
    invariant_index = 0
    while invariant_index < len(_P2D47_INVARIANTS):
        orchestration_invariant_refs += (_P2D47_INVARIANTS[invariant_index],)
        invariant_index += 1

    return {
        "orchestration_receipt_created": orchestration_receipt_created,
        "orchestration_status": orchestration_status,
        "accepted": orchestration_accepted,
        "warning": orchestration_warning,
        "reason_code": orchestration_reason_code,
        "reason": orchestration_reason,
        "source": projected_source,
        "persistence_evidence": projected_evidence,
        "orchestration_violations": orchestration_violations,
        "missing_or_invalid_fields": orchestration_missing_or_invalid_fields,
        "diagnostic_records": orchestration_diagnostic_records,
        "invariant_refs": orchestration_invariant_refs,
    }
