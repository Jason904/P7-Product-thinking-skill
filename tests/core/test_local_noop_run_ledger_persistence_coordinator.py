"""Frozen 34-test S1 contract for the P2D-47 persistence coordinator."""

import ast
import gc
import inspect
import types
import weakref

import pytest

from ai_daily_publishing_system.core import (
    local_noop_run_ledger_persistence_coordinator as sut,
)


P2D47_ROOT_KEYS = (
    "orchestration_receipt_created", "orchestration_status", "accepted",
    "warning", "reason_code", "reason", "source", "persistence_evidence",
    "orchestration_violations", "missing_or_invalid_fields",
    "diagnostic_records", "invariant_refs",
)
P2D47_STATUSES = (
    "PERSISTENCE_COORDINATION_ACCEPTED",
    "PERSISTENCE_COORDINATION_ACCEPTED_WITH_WARNING",
    "PERSISTENCE_COORDINATION_REJECTED",
    "PERSISTENCE_COORDINATION_INVALID",
    "PERSISTENCE_COORDINATION_UNCONFIRMED",
)
P2D47_BOOLEAN_MATRIX = (
    ("PERSISTENCE_COORDINATION_ACCEPTED", True, True, False),
    ("PERSISTENCE_COORDINATION_ACCEPTED_WITH_WARNING", True, True, True),
    ("PERSISTENCE_COORDINATION_REJECTED", True, False, False),
    ("PERSISTENCE_COORDINATION_INVALID", False, False, False),
    ("PERSISTENCE_COORDINATION_UNCONFIRMED", False, False, False),
)
P2D47_PROHIBITED_STATUS_VOCABULARY = (
    "RUN_COMPLETED", "COMPLETED", "TRANSITIONED", "PASS",
    "PASS_PUBLISHED", "PUBLISHED", "NOOP_COMPLETED", "PUBLISH_ALLOWED",
)
P2D47_SOURCE_KEYS = (
    "boundary_scope", "schema_version", "persistence_boundary_scope",
    "persistence_schema_version", "consumption_boundary_scope",
    "consumption_schema_version", "upstream_artifact_name",
    "upstream_persistence_status", "upstream_reason_code",
    "upstream_write_disposition", "consumption_decision_status",
    "consumption_reason_code",
)
P2D47_SOURCE_FIXED_VALUES = (
    ("boundary_scope", "local_noop_run_ledger_persistence_coordinator"),
    ("schema_version", "p2d47.local_noop_run_ledger_persistence_coordinator.v1"),
    ("persistence_boundary_scope", "run_ledger_persistence_boundary"),
    ("persistence_schema_version", "p2d45.run_ledger_persistence.v1"),
    ("consumption_boundary_scope", "run_ledger_persistence_consumption_decision"),
    ("consumption_schema_version", "p2d46.run_ledger_persistence_consumption_decision.v1"),
    ("upstream_artifact_name", "run-ledger.yaml"),
)
P2D47_SAFE_EVIDENCE_KEYS = (
    "artifact_relative_path", "serialization_format",
    "content_digest_algorithm", "content_digest", "write_disposition",
)
P2D47_DIAGNOSTIC_PATHS = (
    "p2d47.persistence_invocation",
    "p2d47.consumption_invocation",
    "p2d47.consumption_result",
)
P2D47_REASON_PAIRS = (
    ("P2D47_PERSISTENCE_ACCEPTED", "The exact P2D-46 decision accepted durable run-ledger persistence without warning."),
    ("P2D47_PERSISTENCE_ACCEPTED_WITH_WARNING", "The exact P2D-46 decision accepted durable run-ledger persistence with a preserved cleanup warning."),
    ("P2D47_PERSISTENCE_REJECTED", "The exact P2D-46 decision did not accept the persistence result."),
    ("P2D47_PERSISTENCE_DECISION_INVALID", "The exact P2D-46 decision classified the P2D-45 persistence result as invalid."),
    ("P2D47_PERSISTENCE_INVOCATION_OUTCOME_UNCONFIRMED", "P2D-45 raised an exception, so the persistence invocation outcome is unconfirmed."),
    ("P2D47_CONSUMPTION_INVOCATION_OUTCOME_UNCONFIRMED", "P2D-46 raised an exception, so consumption of the persistence result is unconfirmed."),
    ("P2D47_CONSUMPTION_RESULT_INVALID", "The P2D-46 return value did not satisfy the exact frozen consumption-decision contract."),
)
P2D47_REASON_PRIORITY = (
    "P2D47_PERSISTENCE_INVOCATION_OUTCOME_UNCONFIRMED",
    "P2D47_CONSUMPTION_INVOCATION_OUTCOME_UNCONFIRMED",
    "P2D47_CONSUMPTION_RESULT_INVALID",
    "P2D47_PERSISTENCE_DECISION_INVALID",
    "P2D47_PERSISTENCE_REJECTED",
    "P2D47_PERSISTENCE_ACCEPTED_WITH_WARNING",
    "P2D47_PERSISTENCE_ACCEPTED",
)
P2D47_INVARIANTS = (
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

P2D46_ROOT_KEYS = (
    "decision_created", "decision_status", "accepted", "warning",
    "reason_code", "reason", "source", "persistence_evidence",
    "decision_violations", "missing_or_invalid_fields",
    "diagnostic_records", "invariant_refs",
)
P2D46_SOURCE_KEYS = (
    "boundary_scope", "schema_version", "upstream_boundary_scope",
    "upstream_schema_version", "upstream_artifact_name",
    "upstream_persistence_status", "upstream_reason_code",
    "upstream_write_disposition",
)
P2D46_SOURCE_FIXED_VALUES = (
    ("boundary_scope", "run_ledger_persistence_consumption_decision"),
    ("schema_version", "p2d46.run_ledger_persistence_consumption_decision.v1"),
    ("upstream_boundary_scope", "run_ledger_persistence_boundary"),
    ("upstream_schema_version", "p2d45.run_ledger_persistence.v1"),
    ("upstream_artifact_name", "run-ledger.yaml"),
)
P2D46_SAFE_EVIDENCE_KEYS = P2D47_SAFE_EVIDENCE_KEYS
P2D46_STATUSES = (
    "PERSISTENCE_ACCEPTED", "PERSISTENCE_ACCEPTED_WITH_WARNING",
    "PERSISTENCE_NOT_ACCEPTED", "PERSISTENCE_RESULT_INVALID",
)
P2D46_BOOLEAN_MATRIX = (
    ("PERSISTENCE_ACCEPTED", True, True, False),
    ("PERSISTENCE_ACCEPTED_WITH_WARNING", True, True, True),
    ("PERSISTENCE_NOT_ACCEPTED", True, False, False),
    ("PERSISTENCE_RESULT_INVALID", False, False, False),
)
P2D46_REASON_PAIRS = (
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
P2D46_INVALID_REASON_PATH_PAIRS = (
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
P2D46_NORMAL_FAMILY_MATRIX = (
    ("WRITTEN", ("RUN_LEDGER_PERSISTED",)),
    ("ALREADY_IDENTICAL", ("RUN_LEDGER_ALREADY_PERSISTED_IDENTICAL",)),
    ("NOT_ELIGIBLE", ("P2D45A_ENVELOPE_NOT_ELIGIBLE",)),
    ("INVALID", ("P2D45A_SUCCESS_ENVELOPE_INVALID",)),
    ("AUTHORIZATION_FAILED", ("DESTINATION_ROOT_INVALID", "DESTINATION_PATH_UNSAFE")),
    ("SERIALIZATION_FAILED", ("RUN_LEDGER_SERIALIZATION_FAILED",)),
    ("CONFLICT", ("RUN_LEDGER_CONFLICT",)),
    ("IO_FAILED", (
        "FILESYSTEM_CAPABILITY_UNAVAILABLE", "EXISTING_TARGET_INSPECTION_FAILED",
        "PRE_FINALIZATION_IO_FAILED", "TEMP_NAME_GENERATION_FAILED",
        "TEMP_FILE_CREATE_FAILED", "TEMP_INODE_VALIDATION_FAILED",
        "TEMP_FILE_WRITE_FAILED", "TEMP_FILE_FSYNC_FAILED", "ATOMIC_CREATE_FAILED",
    )),
    ("DURABILITY_UNCONFIRMED", (
        "FINAL_IDENTITY_VERIFICATION_FAILED", "FINAL_DURABILITY_UNCONFIRMED",
        "PRE_FINALIZATION_IO_FAILED",
    )),
    ("PERSISTED_CLEANUP_WARNING", ("PERSISTED_CLEANUP_WARNING",)),
)
P2D46_IMPOSSIBLE_PRE_SURFACES = (
    ("AUTHORIZATION_FAILED", "PRE_FINALIZATION_IO_FAILED"),
    ("CONFLICT", "PRE_FINALIZATION_IO_FAILED"),
)

ENTRY_DIGEST = "5ecbc192017833e40d812cac9daec51f310ef4b492502fb63ca0821588ce9b29"
RELATIVE_PATH = "runs/by-entry-id/sha256-" + ENTRY_DIGEST + "/run-ledger.yaml"
CONTENT_DIGEST = "a" * 64


def _lookup(entries, key):
    for known, value in entries:
        if known == key:
            return value
    return ""


def _safe_evidence(disposition):
    if not disposition:
        return {}
    return {
        "artifact_relative_path": RELATIVE_PATH,
        "serialization_format": "canonical_json_yaml_1_2_subset",
        "content_digest_algorithm": "sha256",
        "content_digest": CONTENT_DIGEST,
        "write_disposition": disposition,
    }


def _p2d46_decision(
    decision_status="PERSISTENCE_ACCEPTED",
    *,
    upstream_status="WRITTEN",
    upstream_reason_code="RUN_LEDGER_PERSISTED",
    disposition="WRITTEN",
    reason_code="P2D46_WRITTEN_ACCEPTED",
):
    matrix = {row[0]: row[1:] for row in P2D46_BOOLEAN_MATRIX}
    created, accepted, warning = matrix[decision_status]
    invalid_path = _lookup(P2D46_INVALID_REASON_PATH_PAIRS, reason_code)
    invalid = decision_status == "PERSISTENCE_RESULT_INVALID"
    evidence = _safe_evidence(disposition)
    return {
        "decision_created": created,
        "decision_status": decision_status,
        "accepted": accepted,
        "warning": warning,
        "reason_code": reason_code,
        "reason": _lookup(P2D46_REASON_PAIRS, reason_code),
        "source": {
            "boundary_scope": "run_ledger_persistence_consumption_decision",
            "schema_version": "p2d46.run_ledger_persistence_consumption_decision.v1",
            "upstream_boundary_scope": "run_ledger_persistence_boundary",
            "upstream_schema_version": "p2d45.run_ledger_persistence.v1",
            "upstream_artifact_name": "run-ledger.yaml",
            "upstream_persistence_status": upstream_status,
            "upstream_reason_code": upstream_reason_code,
            "upstream_write_disposition": disposition,
        },
        "persistence_evidence": evidence,
        "decision_violations": (reason_code,) if invalid else (),
        "missing_or_invalid_fields": (invalid_path,) if invalid else (),
        "diagnostic_records": ({
            "reason_code": reason_code,
            "field": invalid_path,
        },) if invalid else (),
        "invariant_refs": tuple(value for value in P2D46_INVARIANTS),
    }


def _written_decision():
    return _p2d46_decision()


def _identical_decision():
    return _p2d46_decision(
        upstream_status="ALREADY_IDENTICAL",
        upstream_reason_code="RUN_LEDGER_ALREADY_PERSISTED_IDENTICAL",
        disposition="ALREADY_IDENTICAL",
        reason_code="P2D46_ALREADY_IDENTICAL_ACCEPTED",
    )


def _warning_decision(disposition="WRITTEN"):
    return _p2d46_decision(
        "PERSISTENCE_ACCEPTED_WITH_WARNING",
        upstream_status="PERSISTED_CLEANUP_WARNING",
        upstream_reason_code="PERSISTED_CLEANUP_WARNING",
        disposition=disposition,
        reason_code="P2D46_CLEANUP_WARNING_ACCEPTED",
    )


def _rejected_decision(status, upstream_reason_code, reason_code, disposition=""):
    return _p2d46_decision(
        "PERSISTENCE_NOT_ACCEPTED",
        upstream_status=status,
        upstream_reason_code=upstream_reason_code,
        disposition=disposition,
        reason_code=reason_code,
    )


def _invalid_decision(reason_code):
    return _p2d46_decision(
        "PERSISTENCE_RESULT_INVALID",
        upstream_status="",
        upstream_reason_code="",
        disposition="",
        reason_code=reason_code,
    )


def _patch_siblings(monkeypatch, persistence_stub, consumption_stub):
    monkeypatch.setattr(
        sut._run_ledger_persistence,
        "persist_run_ledger_entry",
        persistence_stub,
    )
    monkeypatch.setattr(
        sut._run_ledger_persistence_consumption_decision,
        "build_run_ledger_persistence_consumption_decision",
        consumption_stub,
    )


def _default_persistence_stub(
    *, run_ledger_entry_assembly, authorized_ops_root
):
    del run_ledger_entry_assembly, authorized_ops_root
    return {"opaque": "exact-p2d45-return"}


def _consumption_stub_returning(decision):
    def stub(*, run_ledger_persistence_result):
        del run_ledger_persistence_result
        return decision
    return stub


def _call():
    return sut.coordinate_local_noop_run_ledger_persistence(
        run_ledger_entry_assembly={"opaque": "assembly"},
        authorized_ops_root="/authorized/ops/root",
    )


def _assert_receipt(result, status, accepted, warning, reason_code):
    assert type(result) is dict
    assert tuple(result) == P2D47_ROOT_KEYS
    assert result["orchestration_status"] == status
    assert result["accepted"] is accepted
    assert result["warning"] is warning
    assert result["reason_code"] == reason_code
    assert result["reason"] == _lookup(P2D47_REASON_PAIRS, reason_code)
    assert tuple(result["source"]) == P2D47_SOURCE_KEYS
    assert result["invariant_refs"] == P2D47_INVARIANTS


def _assert_no_secret_strings(value, secrets):
    pending = [value]
    seen_container_ids = set()
    while pending:
        current = pending.pop()
        if type(current) is str:
            for secret in secrets:
                if type(secret) is str and secret:
                    assert secret not in current, "secret string leaked into receipt"
            continue
        if type(current) not in (dict, list, tuple, set, frozenset):
            continue
        container_id = id(current)
        if container_id in seen_container_ids:
            continue
        seen_container_ids.add(container_id)
        if type(current) is dict:
            for key, item in dict.items(current):
                pending.append(key)
                pending.append(item)
        else:
            for item in current:
                pending.append(item)


def test_public_api_signature_annotations_and_single_function_surface_are_exact():
    function = sut.coordinate_local_noop_run_ledger_persistence
    signature = inspect.signature(function)
    assert tuple(signature.parameters) == (
        "run_ledger_entry_assembly", "authorized_ops_root",
    )
    parameters = tuple(signature.parameters.values())
    assert all(
        parameter.kind is inspect.Parameter.KEYWORD_ONLY
        for parameter in parameters
    )
    assert all(
        parameter.default is inspect.Parameter.empty
        for parameter in parameters
    )
    assert tuple(parameter.annotation for parameter in parameters) == (
        dict[str, object], str,
    )
    assert signature.return_annotation == dict[str, object]
    tree = ast.parse(inspect.getsource(sut))
    functions = tuple(
        node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
    )
    assert len(functions) == 1
    assert functions[0].name == "coordinate_local_noop_run_ledger_persistence"
    function_body = functions[0].body
    assert function_body
    assert not all(isinstance(statement, ast.Pass) for statement in function_body)
    not_implemented_error_raises = tuple(
        node
        for node in ast.walk(functions[0])
        if isinstance(node, ast.Raise)
        and (
            (
                isinstance(node.exc, ast.Name)
                and node.exc.id == "NotImplementedError"
            )
            or (
                isinstance(node.exc, ast.Call)
                and isinstance(node.exc.func, ast.Name)
                and node.exc.func.id == "NotImplementedError"
            )
        )
    )
    assert not (
        len(function_body) == 1
        and isinstance(function_body[0], ast.Raise)
        and function_body[0] in not_implemented_error_raises
    )
    assert not not_implemented_error_raises
    assert not any(isinstance(node, ast.AsyncFunctionDef) for node in ast.walk(tree))


def test_sibling_import_form_and_dependency_surface_are_exact():
    tree = ast.parse(inspect.getsource(sut))
    imports = tuple(
        (
            node.module,
            tuple((alias.name, alias.asname) for alias in node.names),
        )
        for node in tree.body
        if isinstance(node, ast.ImportFrom)
    )
    assert imports == (
        (
            "ai_daily_publishing_system.core",
            (("run_ledger_persistence", "_run_ledger_persistence"),),
        ),
        (
            "ai_daily_publishing_system.core",
            ((
                "run_ledger_persistence_consumption_decision",
                "_run_ledger_persistence_consumption_decision",
            ),),
        ),
    )
    assert not any(isinstance(node, ast.Import) for node in ast.walk(tree))
    imported_modules = {
        name: value.__name__
        for name, value in vars(sut).items()
        if isinstance(value, types.ModuleType)
    }
    assert imported_modules == {
        "_run_ledger_persistence": (
            "ai_daily_publishing_system.core.run_ledger_persistence"
        ),
        "_run_ledger_persistence_consumption_decision": (
            "ai_daily_publishing_system.core."
            "run_ledger_persistence_consumption_decision"
        ),
    }


def test_p2d47_root_status_boolean_and_prohibited_status_catalogs_are_exact():
    assert sut._P2D47_ROOT_KEYS == P2D47_ROOT_KEYS
    assert sut._P2D47_STATUSES == P2D47_STATUSES
    assert sut._P2D47_BOOLEAN_MATRIX == P2D47_BOOLEAN_MATRIX
    assert (
        sut._P2D47_PROHIBITED_STATUS_VOCABULARY
        == P2D47_PROHIBITED_STATUS_VOCABULARY
    )
    assert set(P2D47_STATUSES).isdisjoint(P2D47_PROHIBITED_STATUS_VOCABULARY)


def test_p2d47_source_evidence_diagnostic_and_reason_catalogs_are_exact():
    assert sut._P2D47_SOURCE_KEYS == P2D47_SOURCE_KEYS
    assert sut._P2D47_SOURCE_FIXED_VALUES == P2D47_SOURCE_FIXED_VALUES
    assert sut._P2D47_SAFE_EVIDENCE_KEYS == P2D47_SAFE_EVIDENCE_KEYS
    assert sut._P2D47_DIAGNOSTIC_PATHS == P2D47_DIAGNOSTIC_PATHS
    assert sut._P2D47_REASON_PAIRS == P2D47_REASON_PAIRS
    assert sut._P2D47_REASON_PRIORITY == P2D47_REASON_PRIORITY
    assert len(P2D47_REASON_PAIRS) == len(P2D47_REASON_PRIORITY) == 7


def test_p2d47_invariant_catalog_is_exact_and_ordered():
    assert sut._P2D47_INVARIANTS == P2D47_INVARIANTS
    assert len(P2D47_INVARIANTS) == 26


def test_p2d46_validation_catalogs_are_exact_and_ordered():
    assert sut._P2D46_ROOT_KEYS == P2D46_ROOT_KEYS
    assert sut._P2D46_SOURCE_KEYS == P2D46_SOURCE_KEYS
    assert sut._P2D46_SOURCE_FIXED_VALUES == P2D46_SOURCE_FIXED_VALUES
    assert sut._P2D46_SAFE_EVIDENCE_KEYS == P2D46_SAFE_EVIDENCE_KEYS
    assert sut._P2D46_STATUSES == P2D46_STATUSES
    assert sut._P2D46_BOOLEAN_MATRIX == P2D46_BOOLEAN_MATRIX
    assert sut._P2D46_REASON_PAIRS == P2D46_REASON_PAIRS
    assert sut._P2D46_INVALID_REASON_PATH_PAIRS == P2D46_INVALID_REASON_PATH_PAIRS
    assert sut._P2D46_INVARIANTS == P2D46_INVARIANTS
    assert sut._P2D46_SERIALIZATION_FORMAT == "canonical_json_yaml_1_2_subset"
    assert sut._P2D46_CONTENT_DIGEST_ALGORITHM == "sha256"
    assert sut._P2D46_WRITE_DISPOSITIONS == (
        "WRITTEN", "ALREADY_IDENTICAL", "DURABILITY_UNCONFIRMED",
    )
    assert sut._P2D46_NORMAL_FAMILY_MATRIX == P2D46_NORMAL_FAMILY_MATRIX
    assert sut._P2D46_IMPOSSIBLE_PRE_SURFACES == P2D46_IMPOSSIBLE_PRE_SURFACES
    assert len(P2D46_REASON_PAIRS) == 23
    assert len(P2D46_INVALID_REASON_PATH_PAIRS) == 13
    assert len(P2D46_INVARIANTS) == 24


def test_written_decision_maps_to_accepted_receipt(monkeypatch):
    decision = _written_decision()
    _patch_siblings(
        monkeypatch, _default_persistence_stub,
        _consumption_stub_returning(decision),
    )
    result = _call()
    _assert_receipt(
        result, "PERSISTENCE_COORDINATION_ACCEPTED", True, False,
        "P2D47_PERSISTENCE_ACCEPTED",
    )


def test_already_identical_decision_maps_to_accepted_receipt(monkeypatch):
    decision = _identical_decision()
    _patch_siblings(
        monkeypatch, _default_persistence_stub,
        _consumption_stub_returning(decision),
    )
    result = _call()
    _assert_receipt(
        result, "PERSISTENCE_COORDINATION_ACCEPTED", True, False,
        "P2D47_PERSISTENCE_ACCEPTED",
    )
    assert result["source"]["upstream_write_disposition"] == "ALREADY_IDENTICAL"


def test_written_cleanup_warning_maps_to_warning_receipt(monkeypatch):
    decision = _warning_decision("WRITTEN")
    _patch_siblings(
        monkeypatch, _default_persistence_stub,
        _consumption_stub_returning(decision),
    )
    result = _call()
    _assert_receipt(
        result, "PERSISTENCE_COORDINATION_ACCEPTED_WITH_WARNING", True, True,
        "P2D47_PERSISTENCE_ACCEPTED_WITH_WARNING",
    )
    assert result["persistence_evidence"]["write_disposition"] == "WRITTEN"


def test_already_identical_cleanup_warning_maps_to_warning_receipt(monkeypatch):
    decision = _warning_decision("ALREADY_IDENTICAL")
    _patch_siblings(
        monkeypatch, _default_persistence_stub,
        _consumption_stub_returning(decision),
    )
    result = _call()
    _assert_receipt(
        result, "PERSISTENCE_COORDINATION_ACCEPTED_WITH_WARNING", True, True,
        "P2D47_PERSISTENCE_ACCEPTED_WITH_WARNING",
    )
    assert (
        result["persistence_evidence"]["write_disposition"]
        == "ALREADY_IDENTICAL"
    )


def test_all_coherent_non_durability_rejected_families_map_to_rejected_receipts(
    monkeypatch,
):
    cases = (
        ("AUTHORIZATION_FAILED", "DESTINATION_ROOT_INVALID", "P2D46_AUTHORIZATION_FAILED_REJECTED"),
        ("AUTHORIZATION_FAILED", "DESTINATION_PATH_UNSAFE", "P2D46_AUTHORIZATION_FAILED_REJECTED"),
        ("SERIALIZATION_FAILED", "RUN_LEDGER_SERIALIZATION_FAILED", "P2D46_SERIALIZATION_FAILED_REJECTED"),
        ("CONFLICT", "RUN_LEDGER_CONFLICT", "P2D46_CONFLICT_REJECTED"),
        ("IO_FAILED", "FILESYSTEM_CAPABILITY_UNAVAILABLE", "P2D46_IO_FAILED_REJECTED"),
        ("IO_FAILED", "EXISTING_TARGET_INSPECTION_FAILED", "P2D46_IO_FAILED_REJECTED"),
        ("IO_FAILED", "PRE_FINALIZATION_IO_FAILED", "P2D46_IO_FAILED_REJECTED"),
        ("IO_FAILED", "TEMP_NAME_GENERATION_FAILED", "P2D46_IO_FAILED_REJECTED"),
        ("IO_FAILED", "TEMP_FILE_CREATE_FAILED", "P2D46_IO_FAILED_REJECTED"),
        ("IO_FAILED", "TEMP_INODE_VALIDATION_FAILED", "P2D46_IO_FAILED_REJECTED"),
        ("IO_FAILED", "TEMP_FILE_WRITE_FAILED", "P2D46_IO_FAILED_REJECTED"),
        ("IO_FAILED", "TEMP_FILE_FSYNC_FAILED", "P2D46_IO_FAILED_REJECTED"),
        ("IO_FAILED", "ATOMIC_CREATE_FAILED", "P2D46_IO_FAILED_REJECTED"),
        ("NOT_ELIGIBLE", "P2D45A_ENVELOPE_NOT_ELIGIBLE", "P2D46_NOT_ELIGIBLE_REJECTED"),
        ("INVALID", "P2D45A_SUCCESS_ENVELOPE_INVALID", "P2D46_UPSTREAM_INVALID_REJECTED"),
    )
    assert len(cases) == 15
    for status, upstream_reason, decision_reason in cases:
        decision = _rejected_decision(
            status, upstream_reason, decision_reason,
        )
        _patch_siblings(
            monkeypatch, _default_persistence_stub,
            _consumption_stub_returning(decision),
        )
        result = _call()
        _assert_receipt(
            result, "PERSISTENCE_COORDINATION_REJECTED", False, False,
            "P2D47_PERSISTENCE_REJECTED",
        )
        assert result["source"]["upstream_persistence_status"] == status
        assert result["source"]["upstream_reason_code"] == upstream_reason


def test_durability_unconfirmed_family_maps_to_rejected_receipt_with_safe_evidence(
    monkeypatch,
):
    cases = (
        "FINAL_IDENTITY_VERIFICATION_FAILED",
        "FINAL_DURABILITY_UNCONFIRMED",
        "PRE_FINALIZATION_IO_FAILED",
    )
    assert len(cases) == 3
    for upstream_reason in cases:
        decision = _rejected_decision(
            "DURABILITY_UNCONFIRMED",
            upstream_reason,
            "P2D46_DURABILITY_UNCONFIRMED_REJECTED",
            "DURABILITY_UNCONFIRMED",
        )
        _patch_siblings(
            monkeypatch, _default_persistence_stub,
            _consumption_stub_returning(decision),
        )
        result = _call()
        _assert_receipt(
            result, "PERSISTENCE_COORDINATION_REJECTED", False, False,
            "P2D47_PERSISTENCE_REJECTED",
        )
        assert tuple(result["persistence_evidence"]) == P2D47_SAFE_EVIDENCE_KEYS
        assert (
            result["persistence_evidence"]["write_disposition"]
            == "DURABILITY_UNCONFIRMED"
        )


def test_all_exact_p2d46_invalid_decisions_map_to_p2d47_decision_invalid(
    monkeypatch,
):
    reason_codes = tuple(code for code, _path in P2D46_INVALID_REASON_PATH_PAIRS)
    assert len(reason_codes) == 13
    for reason_code in reason_codes:
        decision = _invalid_decision(reason_code)
        _patch_siblings(
            monkeypatch, _default_persistence_stub,
            _consumption_stub_returning(decision),
        )
        result = _call()
        _assert_receipt(
            result, "PERSISTENCE_COORDINATION_INVALID", False, False,
            "P2D47_PERSISTENCE_DECISION_INVALID",
        )
        assert result["source"]["consumption_reason_code"] == reason_code


def test_p2d45_is_called_exactly_once_with_exact_input_objects(monkeypatch):
    def fail_operation(self, other=None):
        del self, other
        raise AssertionError("hostile caller object inspected")

    Hostile = type(
        "HostileIdentity",
        (),
        {
            "__eq__": fail_operation,
            "__hash__": fail_operation,
            "__repr__": fail_operation,
            "__iter__": fail_operation,
        },
    )
    assembly = Hostile()
    root = Hostile()
    p45_calls = []
    persistence_result = {"p2d45": "opaque"}
    decision = _written_decision()

    def persistence_stub(*, run_ledger_entry_assembly, authorized_ops_root):
        p45_calls.append((run_ledger_entry_assembly, authorized_ops_root))
        return persistence_result

    _patch_siblings(
        monkeypatch, persistence_stub, _consumption_stub_returning(decision),
    )
    result = sut.coordinate_local_noop_run_ledger_persistence(
        run_ledger_entry_assembly=assembly,
        authorized_ops_root=root,
    )
    _assert_receipt(
        result, "PERSISTENCE_COORDINATION_ACCEPTED", True, False,
        "P2D47_PERSISTENCE_ACCEPTED",
    )
    assert len(p45_calls) == 1

    assembly_identity_is_exact = p45_calls[0][0] is assembly
    root_identity_is_exact = p45_calls[0][1] is root

    assert assembly_identity_is_exact is True
    assert root_identity_is_exact is True


def test_p2d46_receives_exact_p2d45_return_by_identity_after_p2d45(monkeypatch):
    events = []
    persistence_result = {"p2d45": "exact-object"}
    decision = _written_decision()

    def persistence_stub(*, run_ledger_entry_assembly, authorized_ops_root):
        del run_ledger_entry_assembly, authorized_ops_root
        events.append("p2d45-return")
        return persistence_result

    def consumption_stub(*, run_ledger_persistence_result):
        events.append(("p2d46-call", run_ledger_persistence_result))
        return decision

    _patch_siblings(monkeypatch, persistence_stub, consumption_stub)
    result = _call()
    _assert_receipt(
        result, "PERSISTENCE_COORDINATION_ACCEPTED", True, False,
        "P2D47_PERSISTENCE_ACCEPTED",
    )
    assert events[0] == "p2d45-return"
    assert events[1][0] == "p2d46-call"
    assert events[1][1] is persistence_result
    assert len(events) == 2


def test_p2d46_is_not_called_when_p2d45_raises_exception(monkeypatch):
    calls = {"p2d45": 0, "p2d46": 0}

    def persistence_stub(*, run_ledger_entry_assembly, authorized_ops_root):
        del run_ledger_entry_assembly, authorized_ops_root
        calls["p2d45"] += 1
        raise RuntimeError("private-persistence-detail")

    def consumption_stub(*, run_ledger_persistence_result):
        del run_ledger_persistence_result
        calls["p2d46"] += 1
        return _written_decision()

    _patch_siblings(monkeypatch, persistence_stub, consumption_stub)
    result = _call()
    _assert_receipt(
        result, "PERSISTENCE_COORDINATION_UNCONFIRMED", False, False,
        "P2D47_PERSISTENCE_INVOCATION_OUTCOME_UNCONFIRMED",
    )
    assert calls == {"p2d45": 1, "p2d46": 0}


def test_p2d45_exception_is_suppressed_without_detail_leakage(monkeypatch):
    secret = "p2d45-exception-private-detail"

    def persistence_stub(*, run_ledger_entry_assembly, authorized_ops_root):
        del run_ledger_entry_assembly, authorized_ops_root
        raise ValueError(secret)

    _patch_siblings(
        monkeypatch, persistence_stub,
        _consumption_stub_returning(_written_decision()),
    )
    result = _call()
    _assert_receipt(
        result, "PERSISTENCE_COORDINATION_UNCONFIRMED", False, False,
        "P2D47_PERSISTENCE_INVOCATION_OUTCOME_UNCONFIRMED",
    )
    _assert_no_secret_strings(result, (secret,))
    assert result["persistence_evidence"] == {}


def test_p2d46_exception_is_suppressed_without_detail_leakage(monkeypatch):
    secret = "p2d46-exception-private-detail"
    persistence_result = {"raw-p2d45-secret": "not-for-output"}

    def persistence_stub(*, run_ledger_entry_assembly, authorized_ops_root):
        del run_ledger_entry_assembly, authorized_ops_root
        return persistence_result

    def consumption_stub(*, run_ledger_persistence_result):
        assert run_ledger_persistence_result is persistence_result
        raise LookupError(secret)

    _patch_siblings(monkeypatch, persistence_stub, consumption_stub)
    result = _call()
    _assert_receipt(
        result, "PERSISTENCE_COORDINATION_UNCONFIRMED", False, False,
        "P2D47_CONSUMPTION_INVOCATION_OUTCOME_UNCONFIRMED",
    )
    _assert_no_secret_strings(
        result, (secret, "raw-p2d45-secret", "not-for-output"),
    )


def test_malformed_p2d46_root_maps_only_to_consumption_result_invalid(monkeypatch):
    cases = (None, [], {"decision_created": True})
    for malformed in cases:
        _patch_siblings(
            monkeypatch, _default_persistence_stub,
            _consumption_stub_returning(malformed),
        )
        result = _call()
        _assert_receipt(
            result, "PERSISTENCE_COORDINATION_INVALID", False, False,
            "P2D47_CONSUMPTION_RESULT_INVALID",
        )
        assert result["orchestration_violations"] == (
            "P2D47_CONSUMPTION_RESULT_INVALID",
        )


def test_malformed_p2d46_source_maps_only_to_consumption_result_invalid(monkeypatch):
    cases = []
    missing = _written_decision()
    missing["source"].pop("upstream_reason_code")
    cases.append(missing)
    reordered = _written_decision()
    reordered["source"] = dict(reversed(tuple(reordered["source"].items())))
    cases.append(reordered)
    incompatible = _written_decision()
    incompatible["source"]["schema_version"] = "p2d46.future.v2"
    cases.append(incompatible)
    for malformed in cases:
        _patch_siblings(
            monkeypatch, _default_persistence_stub,
            _consumption_stub_returning(malformed),
        )
        result = _call()
        _assert_receipt(
            result, "PERSISTENCE_COORDINATION_INVALID", False, False,
            "P2D47_CONSUMPTION_RESULT_INVALID",
        )


def test_malformed_p2d46_evidence_maps_only_to_consumption_result_invalid(
    monkeypatch,
):
    cases = []
    unknown = _written_decision()
    unknown["persistence_evidence"]["caller_secret"] = "private"
    cases.append(unknown)
    wrong_digest = _written_decision()
    wrong_digest["persistence_evidence"]["content_digest"] = "not-sha256"
    cases.append(wrong_digest)
    mismatched = _written_decision()
    mismatched["persistence_evidence"]["write_disposition"] = "ALREADY_IDENTICAL"
    cases.append(mismatched)
    for malformed in cases:
        _patch_siblings(
            monkeypatch, _default_persistence_stub,
            _consumption_stub_returning(malformed),
        )
        result = _call()
        _assert_receipt(
            result, "PERSISTENCE_COORDINATION_INVALID", False, False,
            "P2D47_CONSUMPTION_RESULT_INVALID",
        )


def test_malformed_p2d46_status_or_boolean_matrix_maps_only_to_consumption_result_invalid(
    monkeypatch,
):
    cases = []
    unknown_status = _written_decision()
    unknown_status["decision_status"] = "PERSISTENCE_COMPLETE"
    cases.append(unknown_status)
    wrong_created = _written_decision()
    wrong_created["decision_created"] = False
    cases.append(wrong_created)
    wrong_accepted = _written_decision()
    wrong_accepted["accepted"] = False
    cases.append(wrong_accepted)
    wrong_warning = _written_decision()
    wrong_warning["warning"] = True
    cases.append(wrong_warning)
    for malformed in cases:
        _patch_siblings(
            monkeypatch, _default_persistence_stub,
            _consumption_stub_returning(malformed),
        )
        result = _call()
        _assert_receipt(
            result, "PERSISTENCE_COORDINATION_INVALID", False, False,
            "P2D47_CONSUMPTION_RESULT_INVALID",
        )


def test_malformed_p2d46_reason_contract_maps_only_to_consumption_result_invalid(
    monkeypatch,
):
    cases = []
    wrong_text = _written_decision()
    wrong_text["reason"] = "caller supplied reason"
    cases.append(wrong_text)
    unknown_reason = _written_decision()
    unknown_reason["reason_code"] = "P2D46_UNKNOWN"
    cases.append(unknown_reason)
    forged_authorization_pre = _rejected_decision(
        "AUTHORIZATION_FAILED", "PRE_FINALIZATION_IO_FAILED",
        "P2D46_AUTHORIZATION_FAILED_REJECTED",
    )
    cases.append(forged_authorization_pre)
    forged_conflict_pre = _rejected_decision(
        "CONFLICT", "PRE_FINALIZATION_IO_FAILED", "P2D46_CONFLICT_REJECTED",
    )
    cases.append(forged_conflict_pre)
    assert tuple(
        (
            value["source"]["upstream_persistence_status"],
            value["source"]["upstream_reason_code"],
        )
        for value in cases[-2:]
    ) == P2D46_IMPOSSIBLE_PRE_SURFACES
    for index, malformed in enumerate(cases):
        _patch_siblings(
            monkeypatch, _default_persistence_stub,
            _consumption_stub_returning(malformed),
        )
        result = _call()
        _assert_receipt(
            result, "PERSISTENCE_COORDINATION_INVALID", False, False,
            "P2D47_CONSUMPTION_RESULT_INVALID",
        )
        if index >= 2:
            assert tuple(
                result["source"][key] for key in P2D47_SOURCE_KEYS[7:]
            ) == ("", "", "", "", "")
            assert result["persistence_evidence"] == {}


def test_malformed_p2d46_diagnostic_family_maps_only_to_consumption_result_invalid(
    monkeypatch,
):
    cases = []
    invalid = _invalid_decision("P2D46_RESULT_KEYS_INVALID")
    invalid["decision_violations"] = ()
    cases.append(invalid)
    invalid = _invalid_decision("P2D46_RESULT_KEYS_INVALID")
    invalid["missing_or_invalid_fields"] = ("caller.secret",)
    cases.append(invalid)
    invalid = _invalid_decision("P2D46_RESULT_KEYS_INVALID")
    invalid["diagnostic_records"] = ({
        "reason_code": "P2D46_RESULT_KEYS_INVALID",
        "field": "caller.secret",
    },)
    cases.append(invalid)
    for malformed in cases:
        _patch_siblings(
            monkeypatch, _default_persistence_stub,
            _consumption_stub_returning(malformed),
        )
        result = _call()
        _assert_receipt(
            result, "PERSISTENCE_COORDINATION_INVALID", False, False,
            "P2D47_CONSUMPTION_RESULT_INVALID",
        )


def test_malformed_p2d46_invariants_map_only_to_consumption_result_invalid(
    monkeypatch,
):
    cases = (
        P2D46_INVARIANTS[:-1],
        tuple(reversed(P2D46_INVARIANTS)),
        P2D46_INVARIANTS + ("P2D46_P_UNKNOWN",),
    )
    for invariants in cases:
        malformed = _written_decision()
        malformed["invariant_refs"] = invariants
        _patch_siblings(
            monkeypatch, _default_persistence_stub,
            _consumption_stub_returning(malformed),
        )
        result = _call()
        _assert_receipt(
            result, "PERSISTENCE_COORDINATION_INVALID", False, False,
            "P2D47_CONSUMPTION_RESULT_INVALID",
        )


def test_exception_is_caught_but_baseexception_subclasses_propagate(monkeypatch):
    scanner_secret = "scanner-private-detail"
    safe_structures = (
        [[[["safe"]]]],
        {1: "safe"},
        {"count": 3, "detail": None},
        {"safe": [1, 2.0, True, None]},
        ("safe", 3, None),
        {"safe", 3},
        frozenset(("safe", 3)),
    )
    for safe_structure in safe_structures:
        _assert_no_secret_strings(safe_structure, (scanner_secret, ""))

    cyclic_list = ["safe"]
    cyclic_list.append(cyclic_list)
    cyclic_dict = {"detail": "safe"}
    cyclic_dict["cycle"] = cyclic_dict
    _assert_no_secret_strings(cyclic_list, (scanner_secret,))
    _assert_no_secret_strings(cyclic_dict, (scanner_secret,))

    leaking_structures = (
        scanner_secret,
        "prefix-" + scanner_secret,
        scanner_secret + "-suffix",
        "prefix-" + scanner_secret + "-suffix",
        repr((scanner_secret,)),
        {"detail": "exception:" + scanner_secret},
        {"key-" + scanner_secret: "safe"},
        ["safe", ("nested", "x" + scanner_secret + "y")],
    )
    for leaking_structure in leaking_structures:
        with pytest.raises(AssertionError):
            _assert_no_secret_strings(leaking_structure, (scanner_secret,))

    class _HostileOrdinaryException(Exception):
        def __init__(self, private_detail, inspection_calls):
            super().__init__(private_detail)
            self._inspection_calls = inspection_calls

        def __str__(self):
            self._inspection_calls["str"] += 1
            raise AssertionError("ordinary exception stringification attempted")

        def __repr__(self):
            self._inspection_calls["repr"] += 1
            raise AssertionError("ordinary exception representation attempted")

    persistence_detail = "ordinary-p2d45-private-detail"
    persistence_inspection_calls = {"str": 0, "repr": 0}
    persistence_calls = {"p2d45": 0, "p2d46": 0}
    persistence_signal = _HostileOrdinaryException(
        persistence_detail,
        persistence_inspection_calls,
    )

    def ordinary_persistence(*, run_ledger_entry_assembly, authorized_ops_root):
        del run_ledger_entry_assembly, authorized_ops_root
        persistence_calls["p2d45"] += 1
        raise persistence_signal

    def persistence_path_consumption(*, run_ledger_persistence_result):
        del run_ledger_persistence_result
        persistence_calls["p2d46"] += 1
        return _written_decision()

    _patch_siblings(
        monkeypatch,
        ordinary_persistence,
        persistence_path_consumption,
    )
    result = _call()
    _assert_receipt(
        result, "PERSISTENCE_COORDINATION_UNCONFIRMED", False, False,
        "P2D47_PERSISTENCE_INVOCATION_OUTCOME_UNCONFIRMED",
    )
    _assert_no_secret_strings(result, (persistence_detail,))
    assert persistence_calls["p2d45"] == 1
    assert persistence_calls["p2d46"] == 0
    assert persistence_inspection_calls["str"] == 0
    assert persistence_inspection_calls["repr"] == 0

    consumption_detail = "ordinary-p2d46-private-detail"
    consumption_inspection_calls = {"str": 0, "repr": 0}
    consumption_calls = {"p2d45": 0, "p2d46": 0}
    consumption_signal = _HostileOrdinaryException(
        consumption_detail,
        consumption_inspection_calls,
    )
    persistence_result = {"opaque": "normal-p2d45-return"}

    def ordinary_path_persistence(
        *, run_ledger_entry_assembly, authorized_ops_root
    ):
        del run_ledger_entry_assembly, authorized_ops_root
        consumption_calls["p2d45"] += 1
        return persistence_result

    def ordinary_consumption(*, run_ledger_persistence_result):
        del run_ledger_persistence_result
        consumption_calls["p2d46"] += 1
        raise consumption_signal

    _patch_siblings(
        monkeypatch,
        ordinary_path_persistence,
        ordinary_consumption,
    )
    result = _call()
    _assert_receipt(
        result, "PERSISTENCE_COORDINATION_UNCONFIRMED", False, False,
        "P2D47_CONSUMPTION_INVOCATION_OUTCOME_UNCONFIRMED",
    )
    _assert_no_secret_strings(result, (consumption_detail,))
    assert consumption_calls["p2d45"] == 1
    assert consumption_calls["p2d46"] == 1
    assert consumption_inspection_calls["str"] == 0
    assert consumption_inspection_calls["repr"] == 0

    exception_types = (KeyboardInterrupt, SystemExit, GeneratorExit)
    assert len(exception_types) == 3

    for exception_type in exception_types:
        calls = {"p2d45": 0, "p2d46": 0}
        signal = exception_type("p2d45-must-propagate")

        def baseexception_persistence(
            *, run_ledger_entry_assembly, authorized_ops_root
        ):
            del run_ledger_entry_assembly, authorized_ops_root
            calls["p2d45"] += 1
            raise signal

        def consumption_not_expected(*, run_ledger_persistence_result):
            del run_ledger_persistence_result
            calls["p2d46"] += 1
            return _written_decision()

        _patch_siblings(
            monkeypatch,
            baseexception_persistence,
            consumption_not_expected,
        )
        with pytest.raises(exception_type) as captured:
            _call()

        captured_type_is_exact = captured.type is exception_type
        captured_value_is_exact = captured.value is signal

        assert captured_type_is_exact is True
        assert captured_value_is_exact is True
        assert calls["p2d45"] == 1
        assert calls["p2d46"] == 0

    for exception_type in exception_types:
        calls = {"p2d45": 0, "p2d46": 0}
        signal = exception_type("p2d46-must-propagate")
        persistence_result = {"opaque": "normal-p2d45-return"}

        def baseexception_path_persistence(
            *, run_ledger_entry_assembly, authorized_ops_root
        ):
            del run_ledger_entry_assembly, authorized_ops_root
            calls["p2d45"] += 1
            return persistence_result

        def baseexception_consumption(*, run_ledger_persistence_result):
            del run_ledger_persistence_result
            calls["p2d46"] += 1
            raise signal

        _patch_siblings(
            monkeypatch,
            baseexception_path_persistence,
            baseexception_consumption,
        )
        with pytest.raises(exception_type) as captured:
            _call()

        captured_type_is_exact = captured.type is exception_type
        captured_value_is_exact = captured.value is signal

        assert captured_type_is_exact is True
        assert captured_value_is_exact is True
        assert calls["p2d45"] == 1
        assert calls["p2d46"] == 1


def test_no_retry_fallback_or_alternate_persistence_path_is_attempted(monkeypatch):
    calls = {"p2d45": 0, "p2d46": 0}

    def persistence_stub(*, run_ledger_entry_assembly, authorized_ops_root):
        del run_ledger_entry_assembly, authorized_ops_root
        calls["p2d45"] += 1
        raise OSError("single-attempt-only")

    def consumption_stub(*, run_ledger_persistence_result):
        del run_ledger_persistence_result
        calls["p2d46"] += 1
        return _written_decision()

    _patch_siblings(monkeypatch, persistence_stub, consumption_stub)
    result = _call()
    _assert_receipt(
        result, "PERSISTENCE_COORDINATION_UNCONFIRMED", False, False,
        "P2D47_PERSISTENCE_INVOCATION_OUTCOME_UNCONFIRMED",
    )
    assert calls == {"p2d45": 1, "p2d46": 0}
    production_names = {
        node.id
        for node in ast.walk(ast.parse(inspect.getsource(sut)))
        if isinstance(node, ast.Name)
    }
    assert production_names.isdisjoint({
        "retry", "fallback", "alternate_persistence", "open", "Path",
    })


def test_hostile_assembly_and_root_are_forwarded_without_coordinator_inspection(
    monkeypatch,
):
    calls = {"eq": 0, "hash": 0, "repr": 0, "iter": 0}

    def fail_eq(self, other=None):
        del self, other
        calls["eq"] += 1
        raise AssertionError("caller equality invoked")

    def fail_hash(self):
        del self
        calls["hash"] += 1
        raise AssertionError("caller hashing invoked")

    def fail_repr(self):
        del self
        calls["repr"] += 1
        raise AssertionError("caller representation invoked")

    def fail_iter(self):
        del self
        calls["iter"] += 1
        raise AssertionError("caller iteration invoked")

    Hostile = type(
        "Hostile",
        (),
        {
            "__eq__": fail_eq,
            "__hash__": fail_hash,
            "__repr__": fail_repr,
            "__iter__": fail_iter,
        },
    )
    assembly = Hostile()
    root = Hostile()
    persistence_result = {"opaque": "p2d45"}

    def persistence_stub(*, run_ledger_entry_assembly, authorized_ops_root):
        assert run_ledger_entry_assembly is assembly
        assert authorized_ops_root is root
        return persistence_result

    def consumption_stub(*, run_ledger_persistence_result):
        assert run_ledger_persistence_result is persistence_result
        return _written_decision()

    _patch_siblings(monkeypatch, persistence_stub, consumption_stub)
    result = sut.coordinate_local_noop_run_ledger_persistence(
        run_ledger_entry_assembly=assembly,
        authorized_ops_root=root,
    )
    _assert_receipt(
        result, "PERSISTENCE_COORDINATION_ACCEPTED", True, False,
        "P2D47_PERSISTENCE_ACCEPTED",
    )
    assert calls == {"eq": 0, "hash": 0, "repr": 0, "iter": 0}


def test_safe_evidence_projection_is_exact_fresh_and_allowlisted(monkeypatch):
    decision = _written_decision()
    decision_evidence = decision["persistence_evidence"]
    _patch_siblings(
        monkeypatch, _default_persistence_stub,
        _consumption_stub_returning(decision),
    )
    result = _call()
    evidence = result["persistence_evidence"]
    assert tuple(evidence) == P2D47_SAFE_EVIDENCE_KEYS
    assert evidence == decision_evidence
    assert evidence is not decision_evidence
    assert evidence["artifact_relative_path"] == RELATIVE_PATH
    assert evidence["serialization_format"] == "canonical_json_yaml_1_2_subset"
    assert evidence["content_digest_algorithm"] == "sha256"
    assert evidence["content_digest"] == CONTENT_DIGEST
    assert evidence["write_disposition"] == "WRITTEN"
    decision_evidence["content_digest"] = "b" * 64
    assert evidence["content_digest"] == CONTENT_DIGEST


def test_root_ids_bytes_paths_raw_results_and_exception_details_are_suppressed(
    monkeypatch,
):
    assembly_secret = "assembly-secret-id"
    root_secret = "/root/private/authorized-ops-secret"
    raw_secret = "raw-p2d45-secret"
    bytes_secret = b"raw-private-bytes"
    exception_secret = "private-exception-detail"
    assembly = {"caller_id": assembly_secret}
    persistence_result = {
        "raw": raw_secret,
        "bytes": bytes_secret,
        "path": root_secret,
    }

    def persistence_stub(*, run_ledger_entry_assembly, authorized_ops_root):
        assert run_ledger_entry_assembly is assembly
        assert authorized_ops_root is root_secret
        return persistence_result

    _patch_siblings(
        monkeypatch, persistence_stub,
        _consumption_stub_returning(_written_decision()),
    )
    receipt = sut.coordinate_local_noop_run_ledger_persistence(
        run_ledger_entry_assembly=assembly,
        authorized_ops_root=root_secret,
    )
    _assert_no_secret_strings(
        receipt,
        (assembly_secret, root_secret, raw_secret, exception_secret),
    )

    def p2d45_exception(*, run_ledger_entry_assembly, authorized_ops_root):
        del run_ledger_entry_assembly, authorized_ops_root
        raise RuntimeError(exception_secret)

    _patch_siblings(
        monkeypatch, p2d45_exception,
        _consumption_stub_returning(_written_decision()),
    )
    _assert_no_secret_strings(
        _call(),
        (assembly_secret, root_secret, raw_secret, exception_secret),
    )

    def p2d46_exception(*, run_ledger_persistence_result):
        del run_ledger_persistence_result
        raise RuntimeError(exception_secret)

    _patch_siblings(
        monkeypatch, persistence_stub, p2d46_exception,
    )
    _assert_no_secret_strings(
        sut.coordinate_local_noop_run_ledger_persistence(
            run_ledger_entry_assembly=assembly,
            authorized_ops_root=root_secret,
        ),
        (assembly_secret, root_secret, raw_secret, exception_secret),
    )


def test_inputs_and_sibling_results_are_not_mutated_aliased_or_retained(
    monkeypatch,
):
    class Marker:
        pass

    assembly_marker = Marker()
    raw_marker = Marker()
    assembly = {"marker": assembly_marker}
    root = "/authorized/root"
    persistence_result = {"marker": raw_marker}
    decision = _written_decision()
    assembly_snapshot = dict(assembly)
    persistence_snapshot = dict(persistence_result)
    decision_source = decision["source"]
    decision_evidence = decision["persistence_evidence"]
    assembly_marker_ref = weakref.ref(assembly_marker)
    raw_marker_ref = weakref.ref(raw_marker)
    persistence_holder = [persistence_result]
    assembly_identity_holder = [assembly]
    persistence_identity_holder = [persistence_result]
    decision_holder = [decision]

    def persistence_stub(*, run_ledger_entry_assembly, authorized_ops_root):
        assert run_ledger_entry_assembly is assembly_identity_holder.pop()
        assert authorized_ops_root is root
        return persistence_holder.pop()

    def consumption_stub(*, run_ledger_persistence_result):
        assert run_ledger_persistence_result is persistence_identity_holder.pop()
        return decision_holder.pop()

    _patch_siblings(monkeypatch, persistence_stub, consumption_stub)
    result = sut.coordinate_local_noop_run_ledger_persistence(
        run_ledger_entry_assembly=assembly,
        authorized_ops_root=root,
    )
    assert assembly == assembly_snapshot
    assert persistence_result == persistence_snapshot
    assert result is not assembly
    assert result is not persistence_result
    assert result is not decision
    assert result["source"] is not decision_source
    assert result["persistence_evidence"] is not decision_evidence
    assert result["invariant_refs"] is not decision["invariant_refs"]
    del assembly_snapshot, persistence_snapshot
    del assembly, persistence_result, assembly_marker, raw_marker
    gc.collect()
    assert assembly_marker_ref() is None
    assert raw_marker_ref() is None


def test_every_call_returns_fresh_mutable_result_containers(monkeypatch):
    decision = _written_decision()
    _patch_siblings(
        monkeypatch, _default_persistence_stub,
        _consumption_stub_returning(decision),
    )
    first = _call()
    second = _call()
    assert first is not second
    for field in ("source", "persistence_evidence"):
        assert first[field] is not second[field]
        assert first[field] is not decision[field]
        assert second[field] is not decision[field]
    for field in (
        "orchestration_violations", "missing_or_invalid_fields",
        "diagnostic_records", "invariant_refs",
    ):
        if first[field]:
            assert first[field] is not second[field]
    first["source"]["upstream_reason_code"] = "mutated"
    first["persistence_evidence"]["content_digest"] = "mutated"
    assert second["source"]["upstream_reason_code"] == "RUN_LEDGER_PERSISTED"
    assert second["persistence_evidence"]["content_digest"] == CONTENT_DIGEST


def test_cross_call_mutation_isolation_holds_for_all_receipt_families(
    monkeypatch,
):
    decisions = (
        _written_decision(),
        _warning_decision(),
        _rejected_decision(
            "CONFLICT", "RUN_LEDGER_CONFLICT", "P2D46_CONFLICT_REJECTED",
        ),
        _invalid_decision("P2D46_RESULT_KEYS_INVALID"),
    )
    for decision in decisions:
        _patch_siblings(
            monkeypatch, _default_persistence_stub,
            _consumption_stub_returning(decision),
        )
        first = _call()
        first["source"]["upstream_reason_code"] = "mutated"
        first["persistence_evidence"]["caller"] = "mutated"
        second = _call()
        assert second["source"]["upstream_reason_code"] != "mutated"
        assert "caller" not in second["persistence_evidence"]
        assert second["invariant_refs"] == P2D47_INVARIANTS

    calls = {"count": 0}

    def failing_persistence(*, run_ledger_entry_assembly, authorized_ops_root):
        del run_ledger_entry_assembly, authorized_ops_root
        calls["count"] += 1
        raise OSError("unconfirmed")

    _patch_siblings(
        monkeypatch, failing_persistence,
        _consumption_stub_returning(_written_decision()),
    )
    first = _call()
    first["source"]["upstream_reason_code"] = "mutated"
    second = _call()
    assert second["source"]["upstream_reason_code"] == ""
    assert second["orchestration_status"] == "PERSISTENCE_COORDINATION_UNCONFIRMED"
    assert calls["count"] == 2


def test_no_final_hash_transition_noop_completed_quality_publication_url_or_notification_authority_leaks(
    monkeypatch,
):
    sibling_aliases = (
        "_run_ledger_persistence",
        "_run_ledger_persistence_consumption_decision",
    )
    allowed_sibling_attributes = (
        ("_run_ledger_persistence", "persist_run_ledger_entry"),
        (
            "_run_ledger_persistence_consumption_decision",
            "build_run_ledger_persistence_consumption_decision",
        ),
    )
    forbidden_dynamic_access_names = (
        "getattr",
        "hasattr",
        "setattr",
        "delattr",
        "vars",
        "dir",
        "compile",
        "eval",
        "exec",
        "__import__",
        "__builtins__",
        "builtins",
        "importlib",
        "globals",
        "locals",
    )
    forbidden_subscript_keys = {
        "__globals__",
        "__builtins__",
        "__import__",
        "__dict__",
        "__getattribute__",
        "__loader__",
        "__spec__",
    }
    assert len(sibling_aliases) == 2
    assert len(allowed_sibling_attributes) == 2

    production_tree = ast.parse(inspect.getsource(sut))
    parents = {}
    for parent in ast.walk(production_tree):
        for child in ast.iter_child_nodes(parent):
            parents[id(child)] = parent

    sibling_name_uses = tuple(
        node
        for node in ast.walk(production_tree)
        if isinstance(node, ast.Name) and node.id in sibling_aliases
    )
    for name_node in sibling_name_uses:
        parent = parents[id(name_node)]
        assert isinstance(parent, ast.Attribute)
        assert parent.value is name_node

    observed_sibling_attributes = tuple(
        ((node.value.id, node.attr), node)
        for node in ast.walk(production_tree)
        if (
            isinstance(node, ast.Attribute)
            and isinstance(node.value, ast.Name)
            and node.value.id in sibling_aliases
        )
    )
    observed_sibling_pairs = tuple(
        pair for pair, _node in observed_sibling_attributes
    )
    assert set(observed_sibling_pairs).issubset(allowed_sibling_attributes)
    for allowed_pair in allowed_sibling_attributes:
        assert observed_sibling_pairs.count(allowed_pair) <= 1

    direct_call_function_ids = {
        id(node.func)
        for node in ast.walk(production_tree)
        if isinstance(node, ast.Call)
    }
    for _pair, attribute_node in observed_sibling_attributes:
        assert id(attribute_node) in direct_call_function_ids

    dynamic_name_uses = {
        node.id
        for node in ast.walk(production_tree)
        if (
            isinstance(node, ast.Name)
            and node.id in forbidden_dynamic_access_names
        )
    }
    dynamic_attribute_uses = {
        node.attr
        for node in ast.walk(production_tree)
        if (
            isinstance(node, ast.Attribute)
            and node.attr in forbidden_dynamic_access_names
        )
    }
    dunder_attribute_uses = {
        node.attr
        for node in ast.walk(production_tree)
        if (
            isinstance(node, ast.Attribute)
            and node.attr.startswith("__")
            and node.attr.endswith("__")
        )
    }
    assert dynamic_name_uses == set()
    assert dynamic_attribute_uses == set()
    assert dunder_attribute_uses == set()

    importlib_imports = tuple(
        imported_name
        for node in ast.walk(production_tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for imported_name in (
            tuple(alias.name for alias in node.names)
            if isinstance(node, ast.Import)
            else (node.module or "",)
        )
        if imported_name.split(".", 1)[0] == "importlib"
    )
    assert importlib_imports == ()

    sibling_subscript_lookups = tuple(
        node
        for node in ast.walk(production_tree)
        if (
            isinstance(node, ast.Subscript)
            and (
                (
                    isinstance(node.value, ast.Name)
                    and node.value.id in sibling_aliases
                )
                or (
                    isinstance(node.value, ast.Attribute)
                    and isinstance(node.value.value, ast.Name)
                    and node.value.value.id in sibling_aliases
                )
            )
        )
    )
    assert sibling_subscript_lookups == ()

    forbidden_static_subscript_lookups = tuple(
        (node.slice.value, node)
        for node in ast.walk(production_tree)
        if (
            isinstance(node, ast.Subscript)
            and isinstance(node.slice, ast.Constant)
            and type(node.slice.value) is str
            and node.slice.value in forbidden_subscript_keys
        )
    )
    assert forbidden_static_subscript_lookups == ()

    dynamic_callable_sources = tuple(
        node.func
        for node in ast.walk(production_tree)
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, (ast.Subscript, ast.Call, ast.Lambda))
        )
    )
    assert dynamic_callable_sources == ()

    decisions = (
        _written_decision(),
        _warning_decision("ALREADY_IDENTICAL"),
        _rejected_decision(
            "DURABILITY_UNCONFIRMED",
            "FINAL_DURABILITY_UNCONFIRMED",
            "P2D46_DURABILITY_UNCONFIRMED_REJECTED",
            "DURABILITY_UNCONFIRMED",
        ),
    )
    forbidden_keys = {
        "final_hash", "final_content_hash", "run_completed", "completion",
        "transition", "transition_request", "transition_executed",
        "noop_completed", "NOOP_COMPLETED", "quality_pass", "gate_pass",
        "pass_published", "PASS_PUBLISHED", "publish_allowed",
        "publish_authorization", "publication", "published", "public_url",
        "public_url_created", "notification", "notification_sent",
    }
    for decision in decisions:
        _patch_siblings(
            monkeypatch, _default_persistence_stub,
            _consumption_stub_returning(decision),
        )
        result = _call()
        keys = set()
        stack = [result]
        while stack:
            value = stack.pop()
            if type(value) is dict:
                keys.update(value.keys())
                stack.extend(value.values())
            elif type(value) is tuple or type(value) is list:
                stack.extend(value)
        assert forbidden_keys.isdisjoint(keys)
        assert result["orchestration_status"] in P2D47_STATUSES
        assert (
            result["orchestration_status"]
            not in P2D47_PROHIBITED_STATUS_VOCABULARY
        )
        assert "content_digest" in result["persistence_evidence"]
        assert "final_hash" not in result["persistence_evidence"]
