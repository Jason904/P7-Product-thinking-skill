"""Contract tests for the pure run-ledger entry assembler."""

import inspect
import types

from ai_daily_publishing_system.core import run_ledger_entry_assembler as sut


ROOT_KEYS = (
    "run_ledger_entry_assembled", "reason_code", "reason", "source",
    "run_ledger_entry", "assembly_violations", "missing_or_invalid_fields",
    "coherence_violations", "invariant_refs",
)
SUCCESS_SOURCE_KEYS = (
    "assembly_scope", "schema_version", "run_ledger_entry_id", "run_id",
    "local_noop_runner_result_id", "run_version_provenance_id",
    "run_version_provenance_schema_version", "mode", "ledger_terminal_status",
    "public_url", "public_url_created", "component_version_count",
    "source_of_truth",
)
ENTRY_KEYS = (
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
RUNNER_EVIDENCE_KEYS = (
    "runner_evidence_id", "runner_evidence_role", "artifact_ref",
    "artifact_kind", "evidence_status", "producer_ref", "evidence_refs",
)
VERSION_FIELDS = (
    "skill_version", "rubric_version", "generator_version",
    "renderer_version", "publisher_version",
)
VERSION_EVIDENCE_KEYS = (
    "version_field", "resolved_version", "resolution_status", "resolver_ref",
    "evidence_ref",
)
BLOCKED_SOURCE = {
    "assembly_scope": "run_ledger_entry_in_memory_only",
    "schema_version": "p2d45.run_ledger_entry.v1",
    "component_version_count": 0,
}
REASON_CODES = (
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
REASON_PRIORITY = (
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
REASON_STRINGS = (
    ("RUN_LEDGER_ENTRY_ASSEMBLED_IN_MEMORY", "A deterministic run-ledger entry candidate was assembled in memory."),
    ("FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT", "A forbidden field or namespace was supplied; caller key names and values are suppressed."),
    ("RUN_LEDGER_ENTRY_ID_INVALID", "run_ledger_entry_id must be an exact nonblank string."),
    ("P2D44_FINAL_RUNNER_RESULT_INVALID", "The complete P2D-44 final runner-result assembly is invalid."),
    ("P2D44_FINAL_RUNNER_RESULT_NOT_ASSEMBLED", "P2D-44 returned a valid blocked envelope and did not assemble a final runner-result object."),
    ("P2D45V_PROVENANCE_RESULT_INVALID", "The complete P2D-45V run-version provenance assembly is invalid."),
    ("P2D45V_PROVENANCE_NOT_ASSEMBLED", "P2D-45V returned a valid blocked envelope and did not assemble run-version provenance."),
    ("P2D45V_SCHEMA_VERSION_INCOMPATIBLE", "The P2D-45V provenance schema version is incompatible."),
    ("PASS_PUBLISHED_FORBIDDEN", "PASS_PUBLISHED is forbidden at this run-ledger entry boundary."),
    ("MODE_NOT_NOOP", "The recorded mode must be noop."),
    ("LEDGER_TERMINAL_STATUS_NOT_NOOP_COMPLETED", "The recorded ledger terminal status must be NOOP_COMPLETED."),
    ("PUBLIC_URL_NON_NULL", "The recorded public URL must be null."),
    ("PUBLIC_URL_CREATED_NOT_FALSE", "The recorded public URL-created marker must be false."),
    ("RUN_ID_MISMATCH", "The P2D-44 and P2D-45V run IDs do not match."),
    ("P2D44_SOURCE_COHERENCE_MISMATCH", "The P2D-44 source and final runner-result object are not coherent."),
    ("P2D45V_PROVENANCE_COHERENCE_MISMATCH", "The P2D-45V source and run-version provenance object are not coherent."),
    ("RUNNER_EVIDENCE_PROJECTION_INVALID", "The validated runner evidence cannot be projected safely."),
    ("VERSION_EVIDENCE_PROJECTION_INVALID", "The validated version evidence cannot be projected safely."),
)
DIAGNOSTIC_PATHS = (
    ("RUN_LEDGER_ENTRY_ASSEMBLED_IN_MEMORY", ()),
    ("FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT", ("p2d45a.forbidden_field_or_namespace",)),
    ("RUN_LEDGER_ENTRY_ID_INVALID", ("run_ledger_entry_id",)),
    ("P2D44_FINAL_RUNNER_RESULT_INVALID", ("local_noop_final_runner_result_assembly",)),
    ("P2D44_FINAL_RUNNER_RESULT_NOT_ASSEMBLED", ("local_noop_final_runner_result_assembly",)),
    ("P2D45V_PROVENANCE_RESULT_INVALID", ("run_version_provenance_assembly",)),
    ("P2D45V_PROVENANCE_NOT_ASSEMBLED", ("run_version_provenance_assembly",)),
    ("P2D45V_SCHEMA_VERSION_INCOMPATIBLE", ("run_version_provenance.schema_version",)),
    ("PASS_PUBLISHED_FORBIDDEN", ("interpreted_semantic_fields",)),
    ("MODE_NOT_NOOP", ("local_noop_runner_result.mode",)),
    ("LEDGER_TERMINAL_STATUS_NOT_NOOP_COMPLETED", ("local_noop_runner_result.runner_terminal_status",)),
    ("PUBLIC_URL_NON_NULL", ("local_noop_runner_result.public_url",)),
    ("PUBLIC_URL_CREATED_NOT_FALSE", ("local_noop_runner_result.public_url_created",)),
    ("RUN_ID_MISMATCH", ("run_id",)),
    ("P2D44_SOURCE_COHERENCE_MISMATCH", ("local_noop_final_runner_result_assembly.source",)),
    ("P2D45V_PROVENANCE_COHERENCE_MISMATCH", ("run_version_provenance_assembly.source",)),
    ("RUNNER_EVIDENCE_PROJECTION_INVALID", ("local_noop_runner_result.runner_evidence_items",)),
    ("VERSION_EVIDENCE_PROJECTION_INVALID", ("run_version_provenance.resolved_component_version_evidence_items",)),
)
INVARIANTS = (
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

P2D44_INVARIANTS = (
    "local_noop_final_runner_result_assembler_only", "assembler_pure_in_memory_only",
    "assembler_accepts_complete_p2d43_p2d42_p2d33_results",
    "nested_decision_candidate_contract_bypass_rejected",
    "explicit_final_runner_result_id_required", "final_runner_result_id_is_opaque_caller_identity",
    "final_runner_result_id_not_generated_or_derived",
    "final_runner_result_id_distinct_from_candidate_and_e2e_ids",
    "p2d33_supplies_e2e_contract_provenance", "readiness_reference_not_used_as_e2e_contract_reference",
    "p2d35_is_only_allowed_sibling_dependency", "p2d35_called_only_after_complete_validation",
    "p2d35_called_exactly_once_on_valid_input", "p2d35_not_called_on_upstream_failure",
    "p2d35_bool_wrapper_not_called", "p2d35_output_revalidated",
    "p2d35_blocked_output_not_returned_as_final_result", "p2d35_output_returned_as_fresh_projection",
    "candidate_evidence_projected_without_value_change", "candidate_evidence_identity_preserved",
    "candidate_evidence_role_preserved", "source_of_truth_combines_p2d33_then_p2d42",
    "source_of_truth_order_and_duplicates_preserved", "caller_input_not_mutated",
    "final_result_output_not_aliased", "final_result_object_assembled_means_in_memory_object_only",
    "noop_completed_is_nested_declarative_metadata_only", "final_result_not_runner_execution",
    "final_result_not_e2e_execution", "final_result_not_runtime_execution",
    "final_result_not_noop_completion_execution", "final_result_not_state_transition",
    "final_result_not_external_noop_completed_achievement", "final_result_not_ledger_write_authorization",
    "final_result_not_ledger_persistence", "final_result_not_cli_or_manual_invocation",
    "final_result_not_quality_pass", "final_result_not_gate_pass",
    "final_result_not_publish_allowed", "final_result_not_pass_published",
    "final_result_not_public_url_created", "final_result_not_notification_sent",
    "failed_evidence_may_be_assembled", "known_blocking_evidence_ids_are_evidence_only",
    "unknown_blocking_evidence_ids_block_assembly", "unknown_keys_block_and_are_suppressed",
    "forbidden_fields_block_and_are_suppressed", "recursive_key_scan_is_cycle_and_depth_safe",
    "recursive_key_scan_does_not_scan_scalar_strings", "mode_noop_required",
    "public_url_must_be_null", "public_url_created_must_be_false", "pass_published_forbidden",
    "no_file_or_artifact_io", "no_config_env_credentials_read",
    "no_run_ledger_yaml_read_or_write", "no_runtime_cli_command_or_subprocess",
    "no_completion_transition_gate_eval_audit_execution", "no_publish_or_notification",
    "no_quality_pass_no_public_url",
)
P2D45V_INVARIANTS = (
    "run_version_provenance_assembler_only", "assembler_pure_in_memory_only",
    "exactly_five_component_versions_required", "component_version_order_fixed",
    "one_evidence_item_per_component_required", "noop_publisher_requires_explicit_publisher_version",
    "component_evidence_items_are_caller_supplied_resolver_attestations",
    "resolution_status_is_caller_supplied_attestation_only",
    "assembler_does_not_resolve_component_versions", "assembler_does_not_execute_resolver",
    "assembler_does_not_fetch_release", "assembler_does_not_inspect_files_skill_or_rubric",
    "assembler_does_not_inspect_git_or_release_metadata", "resolved_version_syntax_is_exact",
    "resolution_status_must_equal_resolved", "resolver_refs_are_opaque", "evidence_refs_are_opaque",
    "resolved_at_is_opaque_caller_evidence", "resolution_policy_is_opaque_caller_identifier",
    "component_versions_are_never_inferred", "duplicate_component_version_values_allowed",
    "shared_resolver_refs_allowed", "shared_evidence_refs_allowed",
    "source_of_truth_order_and_duplicates_preserved", "caller_input_not_mutated",
    "output_containers_are_fresh", "nonempty_output_tuples_are_identity_isolated",
    "empty_tuple_identity_not_required", "blocked_output_is_fixed_and_caller_safe",
    "unknown_keys_block_and_are_suppressed", "forbidden_fields_block_and_are_suppressed",
    "recursive_key_scan_is_cycle_and_depth_safe", "recursive_key_scan_does_not_scan_scalar_strings",
    "version_provenance_assembled_means_structurally_valid_in_memory_object_only",
    "version_provenance_assembled_not_independent_version_verification",
    "version_provenance_assembled_not_runtime_execution",
    "version_provenance_assembled_not_ledger_entry_assembly",
    "version_provenance_assembled_not_ledger_persistence",
    "version_provenance_assembled_not_completion_or_transition",
    "version_provenance_assembled_not_quality_pass", "version_provenance_assembled_not_gate_pass",
    "version_provenance_assembled_not_publish_authorization", "no_file_or_artifact_io",
    "no_config_env_or_credential_access", "no_cli_command_or_subprocess",
    "no_network_or_provider_call", "no_actual_resolver_result_payload",
    "no_public_url_behavior", "no_publish_or_notification", "no_upstream_or_sibling_call",
)


def _runner_evidence(status="passed", notes=("runner note",), refs=("artifact#evidence",)):
    return {
        "runner_evidence_id": "runner-evidence-001",
        "runner_evidence_role": "local_noop_runner_result",
        "artifact_ref": "runner-artifact-001",
        "artifact_kind": "local_noop_runner_result",
        "evidence_status": status,
        "producer_ref": "p2d-44",
        "evidence_refs": refs,
        "notes": notes,
    }


def _p2d44(*, status="passed", blocking=(), notes=("runner note",), refs=("artifact#evidence",)):
    evidence = _runner_evidence(status=status, notes=notes, refs=refs)
    source_truth = ("p2d-44", "shared-source")
    result = {
        "run_id": "run-001",
        "local_noop_runner_result_id": "runner-result-001",
        "result_kind": "local_noop_runner_result",
        "mode": "noop",
        "runner_terminal_status": "NOOP_COMPLETED",
        "local_noop_e2e_contract_ref": "e2e-contract-001",
        "local_noop_e2e_contract_buildable_marker": True,
        "public_url": None,
        "public_url_created": False,
        "runner_evidence_items": (evidence,),
        "required_runner_evidence_ids": ("runner-evidence-001",),
        "missing_runner_evidence_ids": (),
        "blocking_runner_evidence_ids": blocking,
        "created_at": "runner-created-at",
        "timestamp_policy": "runner-timestamp-policy",
        "source_of_truth": source_truth,
        "notes": ("runner result note",),
    }
    return {
        "final_result_object_assembled": True,
        "reason_code": "LOCAL_NOOP_FINAL_RUNNER_RESULT_OBJECT_ASSEMBLED",
        "reason": "A final local noop runner-result object was assembled in memory.",
        "source": {
            "p2d43_decision_created": True,
            "p2d43_reason_code": "LOCAL_NOOP_TERMINAL_RESULT_ASSEMBLY_DECISION_CREATED",
            "p2d42_consumed": True,
            "p2d42_reason_code": "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_CONSUMED_IN_MEMORY",
            "p2d33_buildable": True,
            "p2d33_reason_code": "LOCAL_NOOP_E2E_CONTRACT_BUILDABLE",
            "p2d35_buildable": True,
            "p2d35_reason_code": "LOCAL_NOOP_RUNNER_RESULT_BUILDABLE",
            "run_id": "run-001",
            "local_noop_runner_result_id": "runner-result-001",
            "local_noop_runner_result_candidate_id": "runner-candidate-001",
            "local_noop_e2e_contract_ref": "e2e-contract-001",
            "mode": "noop",
            "runner_terminal_status": "NOOP_COMPLETED",
            "public_url": None,
            "public_url_created": False,
            "source_of_truth": source_truth,
        },
        "local_noop_runner_result": result,
        "assembly_violations": (),
        "missing_or_invalid_fields": (),
        "result_validation_violations": (),
        "invariant_refs": P2D44_INVARIANTS,
    }


def _blocked_p2d44():
    return {
        "final_result_object_assembled": False,
        "reason_code": "FINAL_RUNNER_RESULT_ID_INVALID",
        "reason": "A nonblank caller-supplied final runner-result ID is required.",
        "source": {
            "p2d43_decision_created": False, "p2d43_reason_code": "",
            "p2d42_consumed": False, "p2d42_reason_code": "",
            "p2d33_buildable": False, "p2d33_reason_code": "",
            "p2d35_buildable": False, "p2d35_reason_code": "", "run_id": "",
            "local_noop_runner_result_id": "", "local_noop_runner_result_candidate_id": "",
            "local_noop_e2e_contract_ref": "", "mode": "", "runner_terminal_status": "",
            "public_url": None, "public_url_created": False, "source_of_truth": (),
        },
        "local_noop_runner_result": {},
        "assembly_violations": ("FINAL_RUNNER_RESULT_ID_INVALID",),
        "missing_or_invalid_fields": ("p2d44.local_noop_runner_result_id",),
        "result_validation_violations": ({
            "reason_code": "FINAL_RUNNER_RESULT_ID_INVALID",
            "field": "p2d44.local_noop_runner_result_id",
        },),
        "invariant_refs": P2D44_INVARIANTS,
    }


def _version_items():
    versions = ("skill-1", "rubric-2", "generator-3", "renderer-4", "publisher-5")
    return tuple({
        "version_field": field,
        "resolved_version": versions[index],
        "resolution_status": "resolved",
        "resolver_ref": "resolver-ref",
        "evidence_ref": "evidence-ref",
    } for index, field in enumerate(VERSION_FIELDS))


def _p2d45v():
    items = _version_items()
    truth = ("p2d-45v", "shared-source")
    provenance = {
        "schema_version": "p2d45.run_version_provenance.v1",
        "run_version_provenance_id": "provenance-001",
        "run_id": "run-001",
        "skill_version": "skill-1",
        "rubric_version": "rubric-2",
        "generator_version": "generator-3",
        "renderer_version": "renderer-4",
        "publisher_version": "publisher-5",
        "resolved_component_version_evidence_items": items,
        "resolved_at": "provenance-resolved-at",
        "resolution_policy": "stable-release-policy",
        "source_of_truth": truth,
    }
    return {
        "version_provenance_assembled": True,
        "reason_code": "RUN_VERSION_PROVENANCE_ASSEMBLED_IN_MEMORY",
        "reason": "A complete, structurally valid, caller-supplied resolver-attested five-component run version provenance object was assembled in memory; no resolver or I/O was executed.",
        "source": {
            "assembly_scope": "run_version_provenance_in_memory_only",
            "schema_version": "p2d45.run_version_provenance.v1",
            "run_version_provenance_id": "provenance-001",
            "run_id": "run-001",
            "component_version_count": 5,
            "resolved_at": "provenance-resolved-at",
            "resolution_policy": "stable-release-policy",
            "source_of_truth": truth,
        },
        "run_version_provenance": provenance,
        "assembly_violations": (),
        "missing_or_invalid_fields": (),
        "coherence_violations": (),
        "invariant_refs": P2D45V_INVARIANTS,
    }


def _blocked_p2d45v():
    return {
        "version_provenance_assembled": False,
        "reason_code": "RUN_ID_INVALID",
        "reason": "run_id must be an exact nonblank string.",
        "source": {
            "assembly_scope": "run_version_provenance_in_memory_only",
            "schema_version": "p2d45.run_version_provenance.v1",
            "component_version_count": 0,
        },
        "run_version_provenance": {},
        "assembly_violations": ("RUN_ID_INVALID",),
        "missing_or_invalid_fields": ("run_id",),
        "coherence_violations": (),
        "invariant_refs": P2D45V_INVARIANTS,
    }


def _assemble(p2d44=None, p2d45v=None, entry_id="ledger-entry-001"):
    return sut.assemble_run_ledger_entry(
        local_noop_final_runner_result_assembly=_p2d44() if p2d44 is None else p2d44,
        run_version_provenance_assembly=_p2d45v() if p2d45v is None else p2d45v,
        run_ledger_entry_id=entry_id,
    )


def _assert_blocked(result):
    assert result["run_ledger_entry_assembled"] is False
    assert tuple(result.keys()) == ROOT_KEYS
    assert result["source"] == BLOCKED_SOURCE
    assert result["run_ledger_entry"] == {}


def test_fixed_schema_reason_path_and_invariant_catalogs_are_exact():
    assert sut.SCHEMA_VERSION == "p2d45.run_ledger_entry.v1"
    assert sut.ASSEMBLY_SCOPE == "run_ledger_entry_in_memory_only"
    assert sut.ENTRY_KIND == "run_ledger_entry"
    assert sut.REASON_CODES == REASON_CODES
    assert sut.RUN_LEDGER_ENTRY_ASSEMBLER_REASON_CODES == REASON_CODES
    assert sut.REASON_PRIORITY == REASON_PRIORITY
    assert sut.REASON_STRINGS == REASON_STRINGS
    assert sut.DIAGNOSTIC_PATHS == DIAGNOSTIC_PATHS
    assert sut.INVARIANT_REFS == INVARIANTS
    assert len(INVARIANTS) == 67


def test_public_apis_are_exact_keyword_only_annotated_and_have_no_defaults():
    expected_names = (
        "local_noop_final_runner_result_assembly",
        "run_version_provenance_assembly",
        "run_ledger_entry_id",
    )
    expected_annotations = (dict[str, object], dict[str, object], str)
    cases = (
        (sut.assemble_run_ledger_entry, "assemble_run_ledger_entry", dict[str, object]),
        (sut.is_run_ledger_entry_assembled, "is_run_ledger_entry_assembled", bool),
    )
    for function, expected_function_name, expected_return in cases:
        assert function.__name__ == expected_function_name
        signature = inspect.signature(function)
        assert tuple(signature.parameters) == expected_names
        assert len(signature.parameters) == 3
        for index, parameter in enumerate(signature.parameters.values()):
            assert parameter.kind is inspect.Parameter.KEYWORD_ONLY
            assert parameter.default is inspect.Parameter.empty
            assert parameter.annotation == expected_annotations[index]
            assert parameter.kind not in (
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD,
            )
        assert signature.return_annotation == expected_return


def test_bool_wrapper_calls_assembler_once_and_returns_exact_bool():
    original = sut.assemble_run_ledger_entry
    calls = []

    def spy(**values):
        calls.append(values)
        return {"run_ledger_entry_assembled": True}

    p2d44 = object()
    p2d45v = object()
    entry_id = object()
    sut.assemble_run_ledger_entry = spy
    try:
        marker = sut.is_run_ledger_entry_assembled(
            local_noop_final_runner_result_assembly=p2d44,
            run_version_provenance_assembly=p2d45v,
            run_ledger_entry_id=entry_id,
        )
    finally:
        sut.assemble_run_ledger_entry = original
    assert marker is True
    assert type(marker) is bool
    assert len(calls) == 1
    assert tuple(calls[0]) == (
        "local_noop_final_runner_result_assembly",
        "run_version_provenance_assembly",
        "run_ledger_entry_id",
    )
    assert calls[0]["local_noop_final_runner_result_assembly"] is p2d44
    assert calls[0]["run_version_provenance_assembly"] is p2d45v
    assert calls[0]["run_ledger_entry_id"] is entry_id


def test_test_module_uses_no_local_sys_path_mutation():
    assert "sys" not in globals()
    assert "SRC_ROOT" not in globals()


def test_valid_p2d44_success_envelope_classifies_success():
    assert _assemble()["run_ledger_entry_assembled"] is True
    for upstream_identity in ("runner-candidate-001", "e2e-contract-001"):
        p2d44 = _p2d44()
        p2d44["source"]["local_noop_runner_result_id"] = upstream_identity
        p2d44["local_noop_runner_result"][
            "local_noop_runner_result_id"
        ] = upstream_identity
        result = _assemble(p2d44=p2d44)
        assert result["reason_code"] == "P2D44_FINAL_RUNNER_RESULT_INVALID"
        assert result["assembly_violations"] == (
            "P2D44_FINAL_RUNNER_RESULT_INVALID",
        )
        assert "P2D44_FINAL_RUNNER_RESULT_NOT_ASSEMBLED" not in result[
            "assembly_violations"
        ]
        assert result["source"] == BLOCKED_SOURCE
        assert result["run_ledger_entry"] == {}


def test_valid_p2d44_blocked_envelope_classifies_not_assembled_only():
    result = _assemble(p2d44=_blocked_p2d44())
    assert result["assembly_violations"] == ("P2D44_FINAL_RUNNER_RESULT_NOT_ASSEMBLED",)


def test_malformed_p2d44_blocked_envelope_classifies_invalid_only():
    blocked = _blocked_p2d44()
    blocked["reason"] = "caller text"
    result = _assemble(p2d44=blocked)
    assert result["assembly_violations"] == ("P2D44_FINAL_RUNNER_RESULT_INVALID",)


def test_valid_p2d45v_success_envelope_classifies_success():
    assert _assemble()["run_ledger_entry_assembled"] is True
    p2d45v = _p2d45v()
    p2d45v["source"]["run_version_provenance_id"] = "run-001"
    p2d45v["run_version_provenance"][
        "run_version_provenance_id"
    ] = "run-001"
    result = _assemble(p2d45v=p2d45v)
    assert result["reason_code"] == "P2D45V_PROVENANCE_RESULT_INVALID"
    assert result["assembly_violations"] == (
        "P2D45V_PROVENANCE_RESULT_INVALID",
    )
    assert "P2D45V_PROVENANCE_NOT_ASSEMBLED" not in result[
        "assembly_violations"
    ]
    assert result["source"] == BLOCKED_SOURCE
    assert result["run_ledger_entry"] == {}


def test_valid_p2d45v_blocked_envelope_classifies_not_assembled_only():
    result = _assemble(p2d45v=_blocked_p2d45v())
    assert result["assembly_violations"] == ("P2D45V_PROVENANCE_NOT_ASSEMBLED",)

    def component_blocked(*, violations, reason, fields, records):
        value = _blocked_p2d45v()
        value["reason_code"] = violations[0]
        value["reason"] = reason
        value["assembly_violations"] = violations
        value["missing_or_invalid_fields"] = fields
        value["coherence_violations"] = records
        return value

    count_path = "resolved_component_version_evidence_items"
    item_path = "resolved_component_version_evidence_items[]"
    keys_path = "resolved_component_version_evidence_items[].keys"
    version_field_path = (
        "resolved_component_version_evidence_items[].version_field"
    )
    resolved_version_path = (
        "resolved_component_version_evidence_items[].resolved_version"
    )
    resolution_status_path = (
        "resolved_component_version_evidence_items[].resolution_status"
    )
    resolver_ref_path = (
        "resolved_component_version_evidence_items[].resolver_ref"
    )
    evidence_ref_path = (
        "resolved_component_version_evidence_items[].evidence_ref"
    )
    count_reason = (
        "resolved_component_version_evidence_items must contain exactly "
        "five items."
    )

    count_only_upstream = component_blocked(
        violations=("COMPONENT_EVIDENCE_COUNT_INVALID",),
        reason=count_reason,
        fields=(count_path,),
        records=(),
    )
    assert count_only_upstream == {
        "version_provenance_assembled": False,
        "reason_code": "COMPONENT_EVIDENCE_COUNT_INVALID",
        "reason": (
            "resolved_component_version_evidence_items must contain "
            "exactly five items."
        ),
        "source": {
            "assembly_scope": "run_version_provenance_in_memory_only",
            "schema_version": "p2d45.run_version_provenance.v1",
            "component_version_count": 0,
        },
        "run_version_provenance": {},
        "assembly_violations": (
            "COMPONENT_EVIDENCE_COUNT_INVALID",
        ),
        "missing_or_invalid_fields": (
            "resolved_component_version_evidence_items",
        ),
        "coherence_violations": (),
        "invariant_refs": P2D45V_INVARIANTS,
    }
    count_only_result = _assemble(p2d45v=count_only_upstream)
    assert tuple(count_only_result) == ROOT_KEYS
    assert count_only_result["run_ledger_entry_assembled"] is False
    assert count_only_result["reason_code"] == (
        "P2D45V_PROVENANCE_NOT_ASSEMBLED"
    )
    assert count_only_result["assembly_violations"] == (
        "P2D45V_PROVENANCE_NOT_ASSEMBLED",
    )
    assert "P2D45V_PROVENANCE_RESULT_INVALID" not in count_only_result[
        "assembly_violations"
    ]
    assert count_only_result["missing_or_invalid_fields"] == (
        "run_version_provenance_assembly",
    )
    assert count_only_result["coherence_violations"] == ({
        "reason_code": "P2D45V_PROVENANCE_NOT_ASSEMBLED",
        "field": "run_version_provenance_assembly",
    },)
    assert count_only_result["source"] == {
        "assembly_scope": "run_ledger_entry_in_memory_only",
        "schema_version": "p2d45.run_ledger_entry.v1",
        "component_version_count": 0,
    }
    assert count_only_result["run_ledger_entry"] == {}

    surplus_canonical_upstream = component_blocked(
        violations=(
            "COMPONENT_EVIDENCE_COUNT_INVALID",
            "COMPONENT_VERSION_FIELD_DUPLICATE",
            "COMPONENT_VERSION_ORDER_INVALID",
        ),
        reason=count_reason,
        fields=(count_path, version_field_path),
        records=(
            {
                "component_index": 5,
                "version_field": "skill_version",
                "reason_code": "COMPONENT_VERSION_FIELD_DUPLICATE",
                "field": version_field_path,
            },
            {
                "component_index": 5,
                "version_field": "skill_version",
                "reason_code": "COMPONENT_VERSION_ORDER_INVALID",
                "field": version_field_path,
            },
        ),
    )
    assert surplus_canonical_upstream == {
        "version_provenance_assembled": False,
        "reason_code": "COMPONENT_EVIDENCE_COUNT_INVALID",
        "reason": (
            "resolved_component_version_evidence_items must contain "
            "exactly five items."
        ),
        "source": {
            "assembly_scope": "run_version_provenance_in_memory_only",
            "schema_version": "p2d45.run_version_provenance.v1",
            "component_version_count": 0,
        },
        "run_version_provenance": {},
        "assembly_violations": (
            "COMPONENT_EVIDENCE_COUNT_INVALID",
            "COMPONENT_VERSION_FIELD_DUPLICATE",
            "COMPONENT_VERSION_ORDER_INVALID",
        ),
        "missing_or_invalid_fields": (
            "resolved_component_version_evidence_items",
            "resolved_component_version_evidence_items[].version_field",
        ),
        "coherence_violations": (
            {
                "component_index": 5,
                "version_field": "skill_version",
                "reason_code": "COMPONENT_VERSION_FIELD_DUPLICATE",
                "field": (
                    "resolved_component_version_evidence_items[]."
                    "version_field"
                ),
            },
            {
                "component_index": 5,
                "version_field": "skill_version",
                "reason_code": "COMPONENT_VERSION_ORDER_INVALID",
                "field": (
                    "resolved_component_version_evidence_items[]."
                    "version_field"
                ),
            },
        ),
        "invariant_refs": P2D45V_INVARIANTS,
    }
    surplus_canonical_result = _assemble(
        p2d45v=surplus_canonical_upstream
    )
    assert tuple(surplus_canonical_result) == ROOT_KEYS
    assert surplus_canonical_result["run_ledger_entry_assembled"] is False
    assert surplus_canonical_result["reason_code"] == (
        "P2D45V_PROVENANCE_NOT_ASSEMBLED"
    )
    assert surplus_canonical_result["assembly_violations"] == (
        "P2D45V_PROVENANCE_NOT_ASSEMBLED",
    )
    assert "P2D45V_PROVENANCE_RESULT_INVALID" not in (
        surplus_canonical_result["assembly_violations"]
    )
    assert surplus_canonical_result["missing_or_invalid_fields"] == (
        "run_version_provenance_assembly",
    )
    assert surplus_canonical_result["coherence_violations"] == ({
        "reason_code": "P2D45V_PROVENANCE_NOT_ASSEMBLED",
        "field": "run_version_provenance_assembly",
    },)
    assert surplus_canonical_result["source"] == {
        "assembly_scope": "run_ledger_entry_in_memory_only",
        "schema_version": "p2d45.run_ledger_entry.v1",
        "component_version_count": 0,
    }
    assert surplus_canonical_result["run_ledger_entry"] == {}

    reachable = (
        component_blocked(
            violations=("COMPONENT_EVIDENCE_ITEM_NOT_DICT",),
            reason="Every component evidence item must be an exact dict.",
            fields=(item_path,),
            records=({
                "component_index": 0,
                "version_field": "skill_version",
                "reason_code": "COMPONENT_EVIDENCE_ITEM_NOT_DICT",
                "field": item_path,
            },),
        ),
        component_blocked(
            violations=(
                "COMPONENT_EVIDENCE_COUNT_INVALID",
                "COMPONENT_VERSION_FIELD_INVALID",
                "RESOLVED_VERSION_INVALID",
            ),
            reason=count_reason,
            fields=(count_path, version_field_path, resolved_version_path),
            records=(
                {
                    "component_index": 5,
                    "version_field": "",
                    "reason_code": "COMPONENT_VERSION_FIELD_INVALID",
                    "field": version_field_path,
                },
                {
                    "component_index": 5,
                    "version_field": "",
                    "reason_code": "RESOLVED_VERSION_INVALID",
                    "field": resolved_version_path,
                },
            ),
        ),
        component_blocked(
            violations=(
                "COMPONENT_VERSION_FIELD_DUPLICATE",
                "COMPONENT_VERSION_ORDER_INVALID",
            ),
            reason="Each canonical version_field may appear exactly once.",
            fields=(version_field_path,),
            records=(
                {
                    "component_index": 1,
                    "version_field": "skill_version",
                    "reason_code": "COMPONENT_VERSION_FIELD_DUPLICATE",
                    "field": version_field_path,
                },
                {
                    "component_index": 1,
                    "version_field": "skill_version",
                    "reason_code": "COMPONENT_VERSION_ORDER_INVALID",
                    "field": version_field_path,
                },
            ),
        ),
        component_blocked(
            violations=("COMPONENT_VERSION_ORDER_INVALID",),
            reason=(
                "Canonical version fields must appear in the fixed "
                "component order."
            ),
            fields=(version_field_path,),
            records=(
                {
                    "component_index": 0,
                    "version_field": "rubric_version",
                    "reason_code": "COMPONENT_VERSION_ORDER_INVALID",
                    "field": version_field_path,
                },
                {
                    "component_index": 1,
                    "version_field": "skill_version",
                    "reason_code": "COMPONENT_VERSION_ORDER_INVALID",
                    "field": version_field_path,
                },
            ),
        ),
        component_blocked(
            violations=(
                "RESOLVED_VERSION_INVALID",
                "RESOLUTION_STATUS_NOT_RESOLVED",
                "RESOLVER_REF_INVALID",
                "EVIDENCE_REF_INVALID",
            ),
            reason=(
                "Every resolved_version must satisfy the exact "
                "1-to-128-character version syntax."
            ),
            fields=(
                resolved_version_path,
                resolution_status_path,
                resolver_ref_path,
                evidence_ref_path,
            ),
            records=(
                {
                    "component_index": 0,
                    "version_field": "skill_version",
                    "reason_code": "RESOLVED_VERSION_INVALID",
                    "field": resolved_version_path,
                },
                {
                    "component_index": 0,
                    "version_field": "skill_version",
                    "reason_code": "RESOLUTION_STATUS_NOT_RESOLVED",
                    "field": resolution_status_path,
                },
                {
                    "component_index": 0,
                    "version_field": "skill_version",
                    "reason_code": "RESOLVER_REF_INVALID",
                    "field": resolver_ref_path,
                },
                {
                    "component_index": 0,
                    "version_field": "skill_version",
                    "reason_code": "EVIDENCE_REF_INVALID",
                    "field": evidence_ref_path,
                },
            ),
        ),
        component_blocked(
            violations=(
                "COMPONENT_EVIDENCE_ITEM_KEYS_INVALID",
                "RESOLVED_VERSION_INVALID",
            ),
            reason=(
                "Every component evidence item must contain the exact "
                "expected keys in the exact expected order."
            ),
            fields=(keys_path, resolved_version_path),
            records=(
                {
                    "component_index": 2,
                    "version_field": "generator_version",
                    "reason_code": "COMPONENT_EVIDENCE_ITEM_KEYS_INVALID",
                    "field": keys_path,
                },
                {
                    "component_index": 2,
                    "version_field": "generator_version",
                    "reason_code": "RESOLVED_VERSION_INVALID",
                    "field": resolved_version_path,
                },
            ),
        ),
        component_blocked(
            violations=(
                "COMPONENT_VERSION_FIELD_INVALID",
                "RESOLVED_VERSION_INVALID",
            ),
            reason="Every version_field must be an exact canonical component name.",
            fields=(version_field_path, resolved_version_path),
            records=(
                {
                    "component_index": 2,
                    "version_field": "generator_version",
                    "reason_code": "COMPONENT_VERSION_FIELD_INVALID",
                    "field": version_field_path,
                },
                {
                    "component_index": 2,
                    "version_field": "generator_version",
                    "reason_code": "RESOLVED_VERSION_INVALID",
                    "field": resolved_version_path,
                },
            ),
        ),
    )
    for upstream in reachable:
        blocked_result = _assemble(p2d45v=upstream)
        assert blocked_result["reason_code"] == (
            "P2D45V_PROVENANCE_NOT_ASSEMBLED"
        )
        assert blocked_result["assembly_violations"] == (
            "P2D45V_PROVENANCE_NOT_ASSEMBLED",
        )
        assert blocked_result["source"] == BLOCKED_SOURCE
        assert blocked_result["run_ledger_entry"] == {}


def test_malformed_p2d45v_blocked_envelope_classifies_invalid_only():
    blocked = _blocked_p2d45v()
    blocked["missing_or_invalid_fields"] = ("caller-secret",)
    result = _assemble(p2d45v=blocked)
    assert result["assembly_violations"] == ("P2D45V_PROVENANCE_RESULT_INVALID",)

    def component_blocked(*, violations, reason, fields, records):
        value = _blocked_p2d45v()
        value["reason_code"] = violations[0]
        value["reason"] = reason
        value["assembly_violations"] = violations
        value["missing_or_invalid_fields"] = fields
        value["coherence_violations"] = records
        return value

    not_dict_reason = "Every component evidence item must be an exact dict."
    not_dict_path = "resolved_component_version_evidence_items[]"
    count_reason = (
        "resolved_component_version_evidence_items must contain exactly "
        "five items."
    )
    count_path = "resolved_component_version_evidence_items"
    version_field_path = (
        "resolved_component_version_evidence_items[].version_field"
    )
    resolved_version_path = (
        "resolved_component_version_evidence_items[].resolved_version"
    )
    keys_path = "resolved_component_version_evidence_items[].keys"

    missing_field_companion_upstream = component_blocked(
        violations=(
            "COMPONENT_EVIDENCE_COUNT_INVALID",
            "RESOLVED_VERSION_INVALID",
        ),
        reason=count_reason,
        fields=(count_path, resolved_version_path),
        records=({
            "component_index": 5,
            "version_field": "",
            "reason_code": "RESOLVED_VERSION_INVALID",
            "field": resolved_version_path,
        },),
    )
    assert missing_field_companion_upstream == {
        "version_provenance_assembled": False,
        "reason_code": "COMPONENT_EVIDENCE_COUNT_INVALID",
        "reason": (
            "resolved_component_version_evidence_items must contain "
            "exactly five items."
        ),
        "source": {
            "assembly_scope": "run_version_provenance_in_memory_only",
            "schema_version": "p2d45.run_version_provenance.v1",
            "component_version_count": 0,
        },
        "run_version_provenance": {},
        "assembly_violations": (
            "COMPONENT_EVIDENCE_COUNT_INVALID",
            "RESOLVED_VERSION_INVALID",
        ),
        "missing_or_invalid_fields": (
            "resolved_component_version_evidence_items",
            "resolved_component_version_evidence_items[].resolved_version",
        ),
        "coherence_violations": ({
            "component_index": 5,
            "version_field": "",
            "reason_code": "RESOLVED_VERSION_INVALID",
            "field": (
                "resolved_component_version_evidence_items[]."
                "resolved_version"
            ),
        },),
        "invariant_refs": P2D45V_INVARIANTS,
    }
    assert "COMPONENT_VERSION_FIELD_INVALID" not in (
        missing_field_companion_upstream["assembly_violations"]
    )
    assert version_field_path not in missing_field_companion_upstream[
        "missing_or_invalid_fields"
    ]
    missing_field_companion_result = _assemble(
        p2d45v=missing_field_companion_upstream
    )
    assert tuple(missing_field_companion_result) == ROOT_KEYS
    assert missing_field_companion_result[
        "run_ledger_entry_assembled"
    ] is False
    assert missing_field_companion_result["reason_code"] == (
        "P2D45V_PROVENANCE_RESULT_INVALID"
    )
    assert missing_field_companion_result["assembly_violations"] == (
        "P2D45V_PROVENANCE_RESULT_INVALID",
    )
    assert "P2D45V_PROVENANCE_NOT_ASSEMBLED" not in (
        missing_field_companion_result["assembly_violations"]
    )
    assert missing_field_companion_result["missing_or_invalid_fields"] == (
        "run_version_provenance_assembly",
    )
    assert missing_field_companion_result["coherence_violations"] == ({
        "reason_code": "P2D45V_PROVENANCE_RESULT_INVALID",
        "field": "run_version_provenance_assembly",
    },)
    assert all(
        "component_index" not in diagnostic
        and "version_field" not in diagnostic
        for diagnostic in missing_field_companion_result[
            "coherence_violations"
        ]
    )
    assert missing_field_companion_result["source"] == {
        "assembly_scope": "run_ledger_entry_in_memory_only",
        "schema_version": "p2d45.run_ledger_entry.v1",
        "component_version_count": 0,
    }
    assert missing_field_companion_result["run_ledger_entry"] == {}
    suppressed_upstream_diagnostics = (
        "COMPONENT_EVIDENCE_COUNT_INVALID",
        "RESOLVED_VERSION_INVALID",
        "COMPONENT_VERSION_FIELD_INVALID",
        count_reason,
        count_path,
        version_field_path,
        resolved_version_path,
        "component_index",
    )
    rendered_missing_field_result = str(missing_field_companion_result)
    assert all(
        diagnostic not in rendered_missing_field_result
        for diagnostic in suppressed_upstream_diagnostics
    )

    unreachable_cases = (
        component_blocked(
            violations=(
                "COMPONENT_EVIDENCE_ITEMS_INVALID",
                "COMPONENT_EVIDENCE_COUNT_INVALID",
            ),
            reason=(
                "resolved_component_version_evidence_items must be an "
                "exact tuple."
            ),
            fields=(count_path,),
            records=(),
        ),
        component_blocked(
            violations=("COMPONENT_EVIDENCE_ITEM_NOT_DICT",),
            reason=not_dict_reason,
            fields=(not_dict_path,),
            records=({
                "component_index": 0,
                "version_field": "",
                "reason_code": "COMPONENT_EVIDENCE_ITEM_NOT_DICT",
                "field": not_dict_path,
            },),
        ),
        component_blocked(
            violations=("COMPONENT_EVIDENCE_ITEM_NOT_DICT",),
            reason=not_dict_reason,
            fields=(not_dict_path,),
            records=({
                "component_index": 0,
                "version_field": "rubric_version",
                "reason_code": "COMPONENT_EVIDENCE_ITEM_NOT_DICT",
                "field": not_dict_path,
            },),
        ),
        component_blocked(
            violations=(
                "COMPONENT_EVIDENCE_COUNT_INVALID",
                "COMPONENT_EVIDENCE_ITEM_NOT_DICT",
            ),
            reason=count_reason,
            fields=(count_path, not_dict_path),
            records=({
                "component_index": 5,
                "version_field": "skill_version",
                "reason_code": "COMPONENT_EVIDENCE_ITEM_NOT_DICT",
                "field": not_dict_path,
            },),
        ),
        component_blocked(
            violations=("COMPONENT_VERSION_FIELD_DUPLICATE",),
            reason="Each canonical version_field may appear exactly once.",
            fields=(version_field_path,),
            records=({
                "component_index": 1,
                "version_field": "rubric_version",
                "reason_code": "COMPONENT_VERSION_FIELD_DUPLICATE",
                "field": version_field_path,
            },),
        ),
        component_blocked(
            violations=("COMPONENT_VERSION_ORDER_INVALID",),
            reason=(
                "Canonical version fields must appear in the fixed "
                "component order."
            ),
            fields=(version_field_path,),
            records=({
                "component_index": 0,
                "version_field": "rubric_version",
                "reason_code": "COMPONENT_VERSION_ORDER_INVALID",
                "field": version_field_path,
            },),
        ),
        component_blocked(
            violations=(
                "COMPONENT_VERSION_ORDER_INVALID",
                "RESOLVED_VERSION_INVALID",
            ),
            reason=(
                "Canonical version fields must appear in the fixed "
                "component order."
            ),
            fields=(version_field_path, resolved_version_path),
            records=(
                {
                    "component_index": 5,
                    "version_field": "skill_version",
                    "reason_code": "COMPONENT_VERSION_ORDER_INVALID",
                    "field": version_field_path,
                },
                {
                    "component_index": 5,
                    "version_field": "skill_version",
                    "reason_code": "RESOLVED_VERSION_INVALID",
                    "field": resolved_version_path,
                },
            ),
        ),
        component_blocked(
            violations=("RESOLVED_VERSION_INVALID",),
            reason=(
                "Every resolved_version must satisfy the exact "
                "1-to-128-character version syntax."
            ),
            fields=(resolved_version_path,),
            records=({
                "component_index": 5,
                "version_field": "",
                "reason_code": "RESOLVED_VERSION_INVALID",
                "field": resolved_version_path,
            },),
        ),
        component_blocked(
            violations=("RESOLVED_VERSION_INVALID",),
            reason=(
                "Every resolved_version must satisfy the exact "
                "1-to-128-character version syntax."
            ),
            fields=(resolved_version_path,),
            records=({
                "component_index": 1,
                "version_field": "skill_version",
                "reason_code": "RESOLVED_VERSION_INVALID",
                "field": resolved_version_path,
            },),
        ),
        component_blocked(
            violations=(
                "COMPONENT_EVIDENCE_ITEM_NOT_DICT",
                "RESOLVED_VERSION_INVALID",
            ),
            reason=not_dict_reason,
            fields=(not_dict_path, resolved_version_path),
            records=(
                {
                    "component_index": 0,
                    "version_field": "skill_version",
                    "reason_code": "COMPONENT_EVIDENCE_ITEM_NOT_DICT",
                    "field": not_dict_path,
                },
                {
                    "component_index": 0,
                    "version_field": "skill_version",
                    "reason_code": "RESOLVED_VERSION_INVALID",
                    "field": resolved_version_path,
                },
            ),
        ),
        component_blocked(
            violations=(
                "COMPONENT_EVIDENCE_ITEM_KEYS_INVALID",
                "RESOLVED_VERSION_INVALID",
            ),
            reason=(
                "Every component evidence item must contain the exact "
                "expected keys in the exact expected order."
            ),
            fields=(keys_path, resolved_version_path),
            records=(
                {
                    "component_index": 1,
                    "version_field": "rubric_version",
                    "reason_code": "COMPONENT_EVIDENCE_ITEM_KEYS_INVALID",
                    "field": keys_path,
                },
                {
                    "component_index": 1,
                    "version_field": "skill_version",
                    "reason_code": "RESOLVED_VERSION_INVALID",
                    "field": resolved_version_path,
                },
            ),
        ),
        component_blocked(
            violations=(
                "COMPONENT_EVIDENCE_COUNT_INVALID",
                "COMPONENT_EVIDENCE_ITEM_NOT_DICT",
            ),
            reason=count_reason,
            fields=(count_path, not_dict_path),
            records=({
                "component_index": 4,
                "version_field": "publisher_version",
                "reason_code": "COMPONENT_EVIDENCE_ITEM_NOT_DICT",
                "field": not_dict_path,
            },),
        ),
    )
    for malformed in unreachable_cases:
        result = _assemble(p2d45v=malformed)
        assert result["reason_code"] == "P2D45V_PROVENANCE_RESULT_INVALID"
        assert result["assembly_violations"] == (
            "P2D45V_PROVENANCE_RESULT_INVALID",
        )
        assert "P2D45V_PROVENANCE_NOT_ASSEMBLED" not in result[
            "assembly_violations"
        ]
        assert result["source"] == BLOCKED_SOURCE
        assert result["run_ledger_entry"] == {}
        rendered = str(result)
        assert "rubric_version" not in rendered
        assert "COMPONENT_EVIDENCE_ITEM_NOT_DICT" not in rendered
        assert not_dict_path not in rendered


def test_non_bool_upstream_assembly_markers_classify_invalid():
    p2d44 = _p2d44()
    p2d44["final_result_object_assembled"] = 1
    p2d45v = _p2d45v()
    p2d45v["version_provenance_assembled"] = 1
    result = _assemble(p2d44=p2d44, p2d45v=p2d45v)
    assert result["assembly_violations"] == (
        "P2D44_FINAL_RUNNER_RESULT_INVALID", "P2D45V_PROVENANCE_RESULT_INVALID",
    )


def test_both_upstream_envelopes_blocked_have_exact_reason_order():
    result = _assemble(p2d44=_blocked_p2d44(), p2d45v=_blocked_p2d45v())
    assert result["assembly_violations"] == (
        "P2D44_FINAL_RUNNER_RESULT_NOT_ASSEMBLED", "P2D45V_PROVENANCE_NOT_ASSEMBLED",
    )


def test_one_blocked_and_one_malformed_prioritizes_invalid():
    malformed = _blocked_p2d45v()
    malformed["reason_code"] = "UNKNOWN"
    result = _assemble(p2d44=_blocked_p2d44(), p2d45v=malformed)
    assert result["assembly_violations"] == (
        "P2D45V_PROVENANCE_RESULT_INVALID", "P2D44_FINAL_RUNNER_RESULT_NOT_ASSEMBLED",
    )


def test_valid_blocked_and_invalid_are_mutually_exclusive_per_input():
    valid_blocked = _assemble(p2d44=_blocked_p2d44())["assembly_violations"]
    malformed = _blocked_p2d44()
    malformed["assembly_violations"] = ()
    invalid = _assemble(p2d44=malformed)["assembly_violations"]
    assert "P2D44_FINAL_RUNNER_RESULT_INVALID" not in valid_blocked
    assert "P2D44_FINAL_RUNNER_RESULT_NOT_ASSEMBLED" not in invalid


def test_run_ledger_entry_id_equal_to_run_id_is_allowed():
    assert _assemble(entry_id="run-001")["run_ledger_entry_assembled"] is True


def test_run_ledger_entry_id_equal_to_runner_result_id_is_allowed():
    assert _assemble(entry_id="runner-result-001")["run_ledger_entry_assembled"] is True


def test_run_ledger_entry_id_equal_to_provenance_id_is_allowed():
    assert _assemble(entry_id="provenance-001")["run_ledger_entry_assembled"] is True


def test_blank_non_string_and_string_subclass_ledger_entry_ids_block():
    StringSubclass = type("StringSubclass", (str,), {})
    for value in (" ", 7, StringSubclass("opaque")):
        result = _assemble(entry_id=value)
        assert "RUN_LEDGER_ENTRY_ID_INVALID" in result["assembly_violations"]


def test_valid_inputs_produce_exact_root_source_and_entry_key_order():
    result = _assemble()
    assert tuple(result.keys()) == ROOT_KEYS
    assert tuple(result["source"].keys()) == SUCCESS_SOURCE_KEYS
    assert tuple(result["run_ledger_entry"].keys()) == ENTRY_KEYS


def test_p2d44_runner_evidence_projection_omits_notes():
    result = _assemble()
    evidence = result["run_ledger_entry"]["runner_evidence_items"][0]
    assert tuple(evidence.keys()) == RUNNER_EVIDENCE_KEYS
    assert "notes" not in evidence


def test_five_direct_versions_are_present_and_authoritative():
    entry = _assemble()["run_ledger_entry"]
    assert tuple(entry[field] for field in VERSION_FIELDS) == (
        "skill-1", "rubric-2", "generator-3", "renderer-4", "publisher-5",
    )
    for malformed in (".v1", "v/1", "v" * 129):
        p2d45v = _p2d45v()
        p2d45v["run_version_provenance"]["skill_version"] = malformed
        result = _assemble(p2d45v=p2d45v)
        assert result["reason_code"] == "P2D45V_PROVENANCE_RESULT_INVALID"
        assert result["assembly_violations"] == (
            "P2D45V_PROVENANCE_RESULT_INVALID",
        )
        assert "P2D45V_PROVENANCE_NOT_ASSEMBLED" not in result[
            "assembly_violations"
        ]
        assert result["source"] == BLOCKED_SOURCE


def test_option_d_evidence_items_have_exact_order_and_fields():
    items = _assemble()["run_ledger_entry"]["resolved_component_version_evidence_items"]
    assert tuple(item["version_field"] for item in items) == VERSION_FIELDS
    assert all(tuple(item.keys()) == VERSION_EVIDENCE_KEYS for item in items)


def test_direct_versions_equal_corresponding_evidence_versions():
    entry = _assemble()["run_ledger_entry"]
    items = entry["resolved_component_version_evidence_items"]
    assert all(entry[field] == items[index]["resolved_version"] for index, field in enumerate(VERSION_FIELDS))
    for malformed in ("-v1", "v 1", "a" * 129):
        p2d45v = _p2d45v()
        p2d45v["run_version_provenance"][
            "resolved_component_version_evidence_items"
        ][0]["resolved_version"] = malformed
        result = _assemble(p2d45v=p2d45v)
        assert result["reason_code"] == "P2D45V_PROVENANCE_RESULT_INVALID"
        assert result["assembly_violations"] == (
            "P2D45V_PROVENANCE_RESULT_INVALID",
        )
        assert "P2D45V_PROVENANCE_NOT_ASSEMBLED" not in result[
            "assembly_violations"
        ]
        assert result["source"] == BLOCKED_SOURCE


def test_source_of_truth_concatenation_preserves_order_and_duplicates():
    entry = _assemble()["run_ledger_entry"]
    assert entry["source_of_truth"] == (
        "p2d-44", "shared-source", "p2d-45v", "shared-source",
    )


def test_independent_timestamps_and_policies_are_not_compared():
    entry = _assemble()["run_ledger_entry"]
    assert entry["runner_result_created_at"] == "runner-created-at"
    assert entry["version_provenance_resolved_at"] == "provenance-resolved-at"
    assert entry["runner_result_timestamp_policy"] == "runner-timestamp-policy"
    assert entry["version_provenance_resolution_policy"] == "stable-release-policy"


def test_failed_runner_evidence_and_known_blocking_ids_remain_declarative():
    result = _assemble(p2d44=_p2d44(status="failed", blocking=("runner-evidence-001",)))
    entry = result["run_ledger_entry"]
    assert result["run_ledger_entry_assembled"] is True
    assert entry["runner_evidence_items"][0]["evidence_status"] == "failed"
    assert entry["blocking_runner_evidence_ids"] == ("runner-evidence-001",)


def test_run_id_mismatch_blocks():
    p2d45v = _p2d45v()
    p2d45v["source"]["run_id"] = "run-002"
    p2d45v["run_version_provenance"]["run_id"] = "run-002"
    _assert_blocked(_assemble(p2d45v=p2d45v))


def test_provenance_schema_mismatch_blocks():
    p2d45v = _p2d45v()
    p2d45v["source"]["schema_version"] = "p2d45.run_version_provenance.v2"
    p2d45v["run_version_provenance"]["schema_version"] = "p2d45.run_version_provenance.v2"
    _assert_blocked(_assemble(p2d45v=p2d45v))


def test_p2d44_source_and_nested_result_mismatch_blocks():
    p2d44 = _p2d44()
    p2d44["source"]["run_id"] = "run-other"
    _assert_blocked(_assemble(p2d44=p2d44))


def test_p2d45v_source_and_nested_provenance_mismatch_blocks():
    p2d45v = _p2d45v()
    p2d45v["source"]["run_version_provenance_id"] = "other-provenance"
    _assert_blocked(_assemble(p2d45v=p2d45v))


def test_mode_terminal_url_and_url_created_mismatches_block():
    for field, value in (
        ("mode", "live"), ("runner_terminal_status", "SYSTEM_FAILED"),
        ("public_url", "https://invalid.example"), ("public_url_created", True),
    ):
        p2d44 = _p2d44()
        p2d44["source"][field] = value
        p2d44["local_noop_runner_result"][field] = value
        _assert_blocked(_assemble(p2d44=p2d44))


def test_pass_published_blocks_in_interpreted_semantic_fields():
    p2d44 = _p2d44(status="PASS_PUBLISHED")
    result = _assemble(p2d44=p2d44)
    assert result["reason_code"] == "P2D44_FINAL_RUNNER_RESULT_INVALID"
    assert result["assembly_violations"] == (
        "P2D44_FINAL_RUNNER_RESULT_INVALID",
    )
    assert "P2D44_FINAL_RUNNER_RESULT_NOT_ASSEMBLED" not in result[
        "assembly_violations"
    ]
    assert result["source"] == BLOCKED_SOURCE
    assert result["run_ledger_entry"] == {}


def test_pass_published_text_inside_opaque_notes_or_refs_is_not_scanned():
    p2d44 = _p2d44(notes=("PASS_PUBLISHED",), refs=("ref/PASS_PUBLISHED",))
    assert _assemble(p2d44=p2d44)["run_ledger_entry_assembled"] is True


def test_unknown_alias_wrong_path_and_non_string_keys_block_safely():
    values = []
    unknown = _p2d44()
    unknown["caller_secret"] = "do-not-copy"
    values.append(unknown)
    alias = _p2d44()
    alias["source"]["Run ID"] = "alias"
    values.append(alias)
    wrong_path = _p2d44()
    wrong_path["source"]["run_ledger_entry"] = {}
    values.append(wrong_path)
    non_string = _p2d44()
    non_string["source"][7] = "value"
    values.append(non_string)
    for value in values:
        result = _assemble(p2d44=value)
        assert result["assembly_violations"][0] == "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"
        assert "do-not-copy" not in str(result)


def test_fixed_output_key_collisions_block_safely():
    p2d45v = _p2d45v()
    p2d45v["run_ledger_entry"] = {"run_id": "caller"}
    result = _assemble(p2d45v=p2d45v)
    assert result["assembly_violations"][0] == "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"
    assert result["run_ledger_entry"] == {}


def test_blocked_source_and_empty_entry_are_exact_and_fixed():
    result = _assemble(entry_id="")
    assert tuple(result["source"].keys()) == (
        "assembly_scope", "schema_version", "component_version_count",
    )
    assert result["source"] == BLOCKED_SOURCE
    assert type(result["run_ledger_entry"]) is dict and result["run_ledger_entry"] == {}


def test_upstream_blocked_diagnostics_are_validated_but_not_copied():
    upstream = _blocked_p2d44()
    result = _assemble(p2d44=upstream)
    assert result["reason"] == REASON_STRINGS[4][1]
    assert "FINAL_RUNNER_RESULT_ID_INVALID" not in result["assembly_violations"]
    assert "p2d44.local_noop_runner_result_id" not in result["missing_or_invalid_fields"]


def test_blocked_output_suppresses_all_caller_ids_versions_refs_times_and_policies():
    result = _assemble(entry_id="")
    forbidden = (
        "run-001", "runner-result-001", "provenance-001", "skill-1",
        "resolver-ref", "runner-created-at", "stable-release-policy",
    )
    rendered = str(result)
    assert all(value not in rendered for value in forbidden)


def test_reason_priority_strings_paths_and_count_are_exact():
    assert len(REASON_CODES) == 18
    assert len(REASON_PRIORITY) == 18
    assert len(REASON_STRINGS) == 18
    assert len(DIAGNOSTIC_PATHS) == 18
    assert sut.REASON_CODES == REASON_CODES
    assert sut.REASON_PRIORITY == REASON_PRIORITY
    assert sut.REASON_STRINGS == REASON_STRINGS
    assert sut.DIAGNOSTIC_PATHS == DIAGNOSTIC_PATHS


def test_multiple_independent_input_failures_are_deterministically_ordered():
    p2d44 = _p2d44()
    p2d44["unknown"] = "secret"
    p2d45v = _p2d45v()
    p2d45v["version_provenance_assembled"] = "true"
    result = _assemble(p2d44=p2d44, p2d45v=p2d45v, entry_id=" ")
    assert result["assembly_violations"] == (
        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT", "RUN_LEDGER_ENTRY_ID_INVALID",
        "P2D44_FINAL_RUNNER_RESULT_INVALID", "P2D45V_PROVENANCE_RESULT_INVALID",
    )


def test_coherence_records_have_exact_safe_shape_and_order():
    p2d44 = _p2d44()
    p2d44["unknown"] = "secret"
    result = _assemble(p2d44=p2d44, entry_id="")
    records = result["coherence_violations"]
    assert all(tuple(record.keys()) == ("reason_code", "field") for record in records)
    assert tuple(record["reason_code"] for record in records) == result["assembly_violations"]
    safe_paths = tuple(path for _, paths in DIAGNOSTIC_PATHS for path in paths)
    assert all(record["field"] in safe_paths for record in records)


def test_cycles_and_deep_unknown_values_block_without_recursion():
    p2d44 = _p2d44()
    cycle = {}
    cycle["cycle"] = cycle
    p2d44["unknown"] = cycle
    result = _assemble(p2d44=p2d44)
    assert result["reason_code"] == "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"
    assert result["assembly_violations"] == (
        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
        "P2D44_FINAL_RUNNER_RESULT_INVALID",
    )
    assert result["source"] == BLOCKED_SOURCE
    assert result["run_ledger_entry"] == {}
    assert cycle["cycle"] is cycle

    def fail_traversal(self):
        del self
        raise AssertionError("unknown payload traversed")

    NoTraverseList = type(
        "NoTraverseList",
        (list,),
        {"__iter__": fail_traversal},
    )
    deep = NoTraverseList()
    cursor = deep
    for _ in range(2000):
        nested = []
        cursor.append(nested)
        cursor = nested
    cursor.append("deep-caller-secret")
    p2d45v = _p2d45v()
    p2d45v["unknown"] = deep
    deep_result = _assemble(p2d45v=p2d45v)
    assert deep_result["reason_code"] == "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"
    assert deep_result["assembly_violations"] == (
        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
        "P2D45V_PROVENANCE_RESULT_INVALID",
    )
    assert deep_result["source"] == BLOCKED_SOURCE
    assert deep_result["run_ledger_entry"] == {}
    assert "deep-caller-secret" not in str(deep_result)
    assert deep[0][0][0] is not None


def test_shared_containers_are_validated_at_each_semantic_path():
    p2d44 = _p2d44()
    shared = p2d44["source"]
    p2d44["local_noop_runner_result"] = shared
    _assert_blocked(_assemble(p2d44=p2d44))


def test_objects_with_failing_repr_are_not_represented():
    calls = {"eq": 0, "hash": 0, "repr": 0}

    def fail_eq(self, other=None):
        del self, other
        calls["eq"] += 1
        raise AssertionError("caller-controlled equality invoked")

    def fail_hash(self):
        del self
        calls["hash"] += 1
        raise AssertionError("caller-controlled hashing invoked")

    def fail_repr(self):
        del self
        calls["repr"] += 1
        raise AssertionError("caller-controlled operation invoked")

    Hostile = type(
        "Hostile",
        (),
        {
            "__eq__": fail_eq,
            "__hash__": fail_hash,
            "__repr__": fail_repr,
        },
    )
    hostile = Hostile()

    def assert_hostile_absent(value):
        stack = [value]
        while stack:
            current = stack.pop()
            assert current is not hostile
            if type(current) is dict:
                stack.extend(current.keys())
                stack.extend(current.values())
            elif type(current) in (tuple, list):
                stack.extend(current)

    p2d44_reason_code = _p2d44()
    p2d44_reason_code["reason_code"] = hostile
    p2d44_reason = _p2d44()
    p2d44_reason["reason"] = hostile
    p2d44_source = _p2d44()
    p2d44_source["source"]["p2d43_reason_code"] = hostile
    p2d44_diagnostic = _blocked_p2d44()
    p2d44_diagnostic["result_validation_violations"][0][
        "reason_code"
    ] = hostile
    p2d44_violations = _blocked_p2d44()
    p2d44_violations["assembly_violations"] = (hostile,)
    for malformed in (
        p2d44_reason_code,
        p2d44_reason,
        p2d44_source,
        p2d44_diagnostic,
        p2d44_violations,
    ):
        result = _assemble(p2d44=malformed)
        assert result["reason_code"] == "P2D44_FINAL_RUNNER_RESULT_INVALID"
        assert result["assembly_violations"] == (
            "P2D44_FINAL_RUNNER_RESULT_INVALID",
        )
        assert "P2D44_FINAL_RUNNER_RESULT_NOT_ASSEMBLED" not in result[
            "assembly_violations"
        ]
        assert result["source"] == BLOCKED_SOURCE
        assert result["run_ledger_entry"] == {}
        assert_hostile_absent(result)

    p2d45v_direct = _p2d45v()
    p2d45v_direct["run_version_provenance"]["skill_version"] = hostile
    p2d45v_evidence = _p2d45v()
    p2d45v_evidence["run_version_provenance"][
        "resolved_component_version_evidence_items"
    ][0]["resolved_version"] = hostile
    p2d45v_violations = _blocked_p2d45v()
    p2d45v_violations["assembly_violations"] = (hostile,)
    for malformed in (
        p2d45v_direct,
        p2d45v_evidence,
        p2d45v_violations,
    ):
        result = _assemble(p2d45v=malformed)
        assert result["reason_code"] == "P2D45V_PROVENANCE_RESULT_INVALID"
        assert result["assembly_violations"] == (
            "P2D45V_PROVENANCE_RESULT_INVALID",
        )
        assert "P2D45V_PROVENANCE_NOT_ASSEMBLED" not in result[
            "assembly_violations"
        ]
        assert result["source"] == BLOCKED_SOURCE
        assert result["run_ledger_entry"] == {}
        assert_hostile_absent(result)

    assert calls == {"eq": 0, "hash": 0, "repr": 0}


def test_inputs_are_not_mutated():
    p2d44 = _p2d44()
    p2d45v = _p2d45v()
    expected44 = _p2d44()
    expected45 = _p2d45v()
    runner = p2d44["local_noop_runner_result"]
    runner_items = runner["runner_evidence_items"]
    runner_item = runner_items[0]
    runner_refs = runner_item["evidence_refs"]
    runner_required = runner["required_runner_evidence_ids"]
    runner_blocking = runner["blocking_runner_evidence_ids"]
    runner_source = runner["source_of_truth"]
    p2d44_source = p2d44["source"]
    p2d44_invariants = p2d44["invariant_refs"]
    provenance = p2d45v["run_version_provenance"]
    version_items = provenance["resolved_component_version_evidence_items"]
    version_item = version_items[0]
    version_source = provenance["source_of_truth"]
    p2d45v_source = p2d45v["source"]
    p2d45v_invariants = p2d45v["invariant_refs"]

    _assemble(p2d44=p2d44, p2d45v=p2d45v)

    assert p2d44 == expected44
    assert p2d45v == expected45
    assert p2d44["source"] is p2d44_source
    assert p2d44["local_noop_runner_result"] is runner
    assert runner["runner_evidence_items"] is runner_items
    assert runner_items[0] is runner_item
    assert runner_item["evidence_refs"] is runner_refs
    assert runner["required_runner_evidence_ids"] is runner_required
    assert runner["blocking_runner_evidence_ids"] is runner_blocking
    assert runner["source_of_truth"] is runner_source
    assert p2d44["invariant_refs"] is p2d44_invariants
    assert p2d45v["source"] is p2d45v_source
    assert p2d45v["run_version_provenance"] is provenance
    assert provenance["resolved_component_version_evidence_items"] is version_items
    assert version_items[0] is version_item
    assert provenance["source_of_truth"] is version_source
    assert p2d45v["invariant_refs"] is p2d45v_invariants


def test_success_output_containers_are_fresh():
    inputs44 = _p2d44(blocking=("runner-evidence-001",))
    inputs45 = _p2d45v()
    first = _assemble(p2d44=inputs44, p2d45v=inputs45)
    second = _assemble(p2d44=inputs44, p2d45v=inputs45)
    caller_runner = inputs44["local_noop_runner_result"]
    caller_runner_items = caller_runner["runner_evidence_items"]
    caller_versions = inputs45["run_version_provenance"]
    caller_version_items = caller_versions[
        "resolved_component_version_evidence_items"
    ]
    first_entry = first["run_ledger_entry"]
    second_entry = second["run_ledger_entry"]

    assert first is not second
    assert first is not inputs44
    assert first is not inputs45
    assert first["source"] is not second["source"]
    assert first["source"] is not inputs44["source"]
    assert first["source"] is not inputs45["source"]
    assert first_entry is not second_entry
    assert first_entry is not caller_runner
    assert first_entry is not caller_versions
    assert first["source"] is not first_entry
    assert second["source"] is not second_entry
    assert first_entry["runner_evidence_items"] is not caller_runner_items
    assert second_entry["runner_evidence_items"] is not caller_runner_items
    assert first_entry["runner_evidence_items"] is not second_entry[
        "runner_evidence_items"
    ]
    for index, caller_item in enumerate(caller_runner_items):
        first_item = first_entry["runner_evidence_items"][index]
        second_item = second_entry["runner_evidence_items"][index]
        assert first_item is not caller_item
        assert second_item is not caller_item
        assert first_item is not second_item
        assert first_item["evidence_refs"] is not caller_item["evidence_refs"]
        assert second_item["evidence_refs"] is not caller_item["evidence_refs"]
        assert first_item["evidence_refs"] is not second_item["evidence_refs"]
    for tuple_field in (
        "required_runner_evidence_ids",
        "blocking_runner_evidence_ids",
    ):
        assert first_entry[tuple_field] is not caller_runner[tuple_field]
        assert second_entry[tuple_field] is not caller_runner[tuple_field]
        assert first_entry[tuple_field] is not second_entry[tuple_field]
    first_version_items = first_entry[
        "resolved_component_version_evidence_items"
    ]
    second_version_items = second_entry[
        "resolved_component_version_evidence_items"
    ]
    assert first_version_items is not caller_version_items
    assert second_version_items is not caller_version_items
    assert first_version_items is not second_version_items
    for index, caller_item in enumerate(caller_version_items):
        assert first_version_items[index] is not caller_item
        assert second_version_items[index] is not caller_item
        assert first_version_items[index] is not second_version_items[index]
    assert first_entry["source_of_truth"] is not caller_runner["source_of_truth"]
    assert first_entry["source_of_truth"] is not caller_versions["source_of_truth"]
    assert first_entry["source_of_truth"] is not second_entry["source_of_truth"]
    assert first["source"]["source_of_truth"] is not first_entry["source_of_truth"]
    assert first["source"]["source_of_truth"] is not second["source"]["source_of_truth"]
    assert first["invariant_refs"] is not inputs44["invariant_refs"]
    assert first["invariant_refs"] is not inputs45["invariant_refs"]
    assert first["invariant_refs"] is not second["invariant_refs"]


def test_blocked_output_containers_are_fresh():
    first = _assemble(entry_id="")
    second = _assemble(entry_id="")
    assert first is not second
    assert first["source"] is not second["source"]
    assert first["run_ledger_entry"] is not second["run_ledger_entry"]
    assert first["run_ledger_entry"] == second["run_ledger_entry"] == {}
    assert first["assembly_violations"] != ()
    assert first["missing_or_invalid_fields"] != ()
    assert first["assembly_violations"] is not second["assembly_violations"]
    assert first["missing_or_invalid_fields"] is not second[
        "missing_or_invalid_fields"
    ]
    assert first["coherence_violations"] is not second["coherence_violations"]
    assert first["coherence_violations"][0] is not second["coherence_violations"][0]
    assert first["invariant_refs"] is not second["invariant_refs"]


def test_no_io_yaml_git_clock_environment_resolver_runtime_publish_or_notification_dependencies():
    forbidden_names = {
        "open", "Path", "pathlib", "os", "getenv", "environ", "datetime",
        "time", "clock", "yaml", "json", "subprocess", "hashlib", "logging",
        "argparse", "click", "typer", "requests", "httpx", "urllib", "socket",
        "git", "GitPython", "release", "resolver", "resolve", "runtime",
        "executor", "state_executor", "persistence", "persist", "writer",
        "publisher", "publish", "notification", "notify", "network", "ledger_io",
    }
    namespace = vars(sut)
    imported_modules = {
        value.__name__
        for value in namespace.values()
        if isinstance(value, types.ModuleType)
    }
    assert imported_modules == {"re"}
    functions = tuple(
        value for value in namespace.values() if inspect.isfunction(value)
    )
    assert sut.assemble_run_ledger_entry in functions
    assert sut.is_run_ledger_entry_assembled in functions
    referenced = {
        name
        for function in functions
        for name in function.__code__.co_names
    }
    namespace_names = set(namespace)
    assert forbidden_names.isdisjoint(referenced)
    assert forbidden_names.isdisjoint(namespace_names)


def test_no_execution_transition_quality_publication_or_persistence_fields_are_emitted():
    result = _assemble()
    forbidden = {
        "quality_pass", "gate_pass", "publish_allowed", "PASS_PUBLISHED",
        "transition", "state_decision", "ledger_written", "persistence_status",
        "notification_result", "publish_authorization", "assembly_timestamp",
    }
    stack = [result]
    keys = set()
    while stack:
        value = stack.pop()
        if type(value) is dict:
            keys.update(value.keys())
            stack.extend(value.values())
        elif type(value) in (tuple, list):
            stack.extend(value)
    assert forbidden.isdisjoint(keys)
