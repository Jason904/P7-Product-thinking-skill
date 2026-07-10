"""Tests for the pure final local noop runner-result assembler."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import (  # noqa: E402
    local_noop_final_runner_result_assembler as assembler,
)


RESULT_KEYS = (
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
SOURCE_KEYS = (
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
FINAL_RESULT_KEYS = (
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
RUNNER_EVIDENCE_KEYS = (
    "runner_evidence_id",
    "runner_evidence_role",
    "artifact_ref",
    "artifact_kind",
    "evidence_status",
    "producer_ref",
    "evidence_refs",
    "notes",
)
BLOCKED_SOURCE = {
    "p2d43_decision_created": False,
    "p2d43_reason_code": "",
    "p2d42_consumed": False,
    "p2d42_reason_code": "",
    "p2d33_buildable": False,
    "p2d33_reason_code": "",
    "p2d35_buildable": False,
    "p2d35_reason_code": "",
    "run_id": "",
    "local_noop_runner_result_id": "",
    "local_noop_runner_result_candidate_id": "",
    "local_noop_e2e_contract_ref": "",
    "mode": "",
    "runner_terminal_status": "",
    "public_url": None,
    "public_url_created": False,
    "source_of_truth": (),
}


def _candidate_evidence(**overrides):
    value = {
        "result_candidate_evidence_id": "candidate-evidence-001",
        "result_candidate_evidence_role": "local_noop_runner_readiness",
        "artifact_ref": "local-noop-runner-readiness-001",
        "artifact_kind": "local_noop_runner_readiness",
        "evidence_status": "passed",
        "producer_ref": "p2d-41",
        "evidence_refs": ("readiness-001#result",),
        "notes": ("candidate-evidence",),
    }
    value.update(overrides)
    return value


def _dry_run_evidence(**overrides):
    value = {
        "dry_run_evidence_id": "dry-run-evidence-001",
        "dry_run_evidence_role": "local_noop_e2e_contract",
        "artifact_ref": "local-noop-run-assembly-001",
        "artifact_kind": "local_noop_run_assembly",
        "evidence_status": "passed",
        "producer_ref": "p2d-32",
        "evidence_refs": ("run-assembly-001#e2e",),
        "notes": ("e2e-evidence",),
    }
    value.update(overrides)
    return value


def _candidate(**overrides):
    value = {
        "run_id": "run-001",
        "local_noop_runner_result_candidate_id": "candidate-001",
        "candidate_kind": "local_noop_runner_result_candidate",
        "mode": "noop",
        "runner_terminal_status": "NOOP_COMPLETED",
        "local_noop_runner_readiness_ref": "readiness-001",
        "local_noop_runner_readiness_id": "readiness-id-001",
        "local_noop_runner_readiness_buildable_marker": True,
        "public_url": None,
        "public_url_created": False,
        "result_candidate_evidence_items": (_candidate_evidence(),),
        "required_result_candidate_evidence_ids": ("candidate-evidence-001",),
        "missing_result_candidate_evidence_ids": (),
        "blocking_result_candidate_evidence_ids": (),
        "created_at": "candidate-created-at",
        "timestamp_policy": "candidate_timestamp_policy",
        "source_of_truth": ("p2d-42", "candidate-source"),
        "notes": ("candidate-note",),
    }
    value.update(overrides)
    return value


def _p2d42(candidate=None):
    if candidate is None:
        candidate = _candidate()
    source = {
        "p2d41_assembled": True,
        "p2d41_reason_code": "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_ASSEMBLED",
        "local_noop_runner_result_candidate_id": candidate[
            "local_noop_runner_result_candidate_id"
        ],
        "candidate_kind": candidate["candidate_kind"],
        "mode": candidate["mode"],
        "public_url": candidate["public_url"],
        "public_url_created": candidate["public_url_created"],
        "source_of_truth": candidate["source_of_truth"],
    }
    receipt = {
        "receipt_kind": "local_noop_runner_result_candidate_consumption_receipt",
        "consumption_scope": "pure_in_memory_validation_and_normalization_only",
        "run_id": candidate["run_id"],
        "local_noop_runner_result_candidate_id": candidate[
            "local_noop_runner_result_candidate_id"
        ],
        "candidate_kind": candidate["candidate_kind"],
        "mode": candidate["mode"],
        "public_url": candidate["public_url"],
        "public_url_created": candidate["public_url_created"],
    }
    return {
        "consumed": True,
        "reason_code": "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_CONSUMED_IN_MEMORY",
        "reason": "Consumed in memory.",
        "source": source,
        "normalized_local_noop_runner_result_candidate": candidate,
        "local_noop_runner_consumption_receipt": receipt,
        "consumption_violations": (),
        "missing_or_invalid_fields": (),
        "result_candidate_evidence_item_violations": (),
        "invariant_refs": assembler._P2D42_REQUIRED_INVARIANTS,
    }


def _p2d43(candidate=None):
    if candidate is None:
        candidate = _candidate()
    source = {
        "p2d42_consumed": True,
        "p2d42_reason_code": "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_CONSUMED_IN_MEMORY",
        "local_noop_runner_result_candidate_id": candidate[
            "local_noop_runner_result_candidate_id"
        ],
        "local_noop_runner_consumption_receipt_kind": (
            "local_noop_runner_result_candidate_consumption_receipt"
        ),
        "mode": candidate["mode"],
        "candidate_runner_terminal_status": candidate["runner_terminal_status"],
        "public_url": candidate["public_url"],
        "public_url_created": candidate["public_url_created"],
        "source_of_truth": candidate["source_of_truth"],
    }
    decision = {
        "decision_kind": "local_noop_terminal_result_assembly_decision",
        "decision_value": "NOOP_TERMINAL_RESULT_ASSEMBLY_ELIGIBLE",
        "decision_scope": (
            "future_separately_authorized_pure_terminal_result_assembly_only"
        ),
        "run_id": candidate["run_id"],
        "local_noop_runner_result_candidate_id": candidate[
            "local_noop_runner_result_candidate_id"
        ],
        "local_noop_runner_consumption_receipt_kind": (
            "local_noop_runner_result_candidate_consumption_receipt"
        ),
        "mode": candidate["mode"],
        "public_url": candidate["public_url"],
        "public_url_created": candidate["public_url_created"],
    }
    return {
        "decision_created": True,
        "reason_code": "LOCAL_NOOP_TERMINAL_RESULT_ASSEMBLY_DECISION_CREATED",
        "reason": "Decision created in memory.",
        "source": source,
        "local_noop_terminal_result_assembly_decision": decision,
        "decision_violations": (),
        "missing_or_invalid_fields": (),
        "decision_validation_violations": (),
        "invariant_refs": assembler._P2D43_REQUIRED_INVARIANTS,
    }


def _p2d33(candidate=None, **overrides):
    if candidate is None:
        candidate = _candidate()
    contract = {
        "run_id": candidate["run_id"],
        "local_noop_e2e_contract_id": "e2e-contract-001",
        "contract_kind": "local_noop_e2e_dry_run_contract",
        "mode": candidate["mode"],
        "e2e_terminal_status": candidate["runner_terminal_status"],
        "gate_input_ref": "gate-input-001",
        "gate_input_buildable_marker": True,
        "local_noop_run_assembly_ref": "run-assembly-001",
        "local_noop_run_buildable_marker": True,
        "public_url": candidate["public_url"],
        "public_url_created": candidate["public_url_created"],
        "dry_run_evidence_items": (_dry_run_evidence(),),
        "required_dry_run_evidence_ids": ("dry-run-evidence-001",),
        "missing_dry_run_evidence_ids": (),
        "blocking_dry_run_evidence_ids": (),
        "created_at": "e2e-created-at",
        "timestamp_policy": "e2e_timestamp_policy",
        "source_of_truth": ("p2d-33", "e2e-source"),
        "notes": ("e2e-note",),
    }
    source = {
        "gate_input_ref": contract["gate_input_ref"],
        "gate_input_buildable_marker": contract["gate_input_buildable_marker"],
        "local_noop_run_assembly_ref": contract["local_noop_run_assembly_ref"],
        "local_noop_run_buildable_marker": contract[
            "local_noop_run_buildable_marker"
        ],
        "mode": contract["mode"],
        "e2e_terminal_status": contract["e2e_terminal_status"],
        "public_url": contract["public_url"],
        "public_url_created": contract["public_url_created"],
        "source_of_truth": contract["source_of_truth"],
    }
    value = {
        "buildable": True,
        "reason_code": "LOCAL_NOOP_E2E_CONTRACT_BUILDABLE",
        "reason": "E2E contract is buildable.",
        "source": source,
        "local_noop_e2e_contract": contract,
        "contract_violations": (),
        "missing_or_invalid_fields": (),
        "dry_run_evidence_item_violations": (),
        "invariant_refs": assembler._P2D33_REQUIRED_INVARIANTS,
    }
    value.update(overrides)
    return value


def _inputs(**overrides):
    candidate = _candidate()
    value = {
        "local_noop_terminal_result_assembly_decision_result": _p2d43(candidate),
        "local_noop_runner_result_candidate_consumption": _p2d42(candidate),
        "local_noop_e2e_contract_build_result": _p2d33(candidate),
        "local_noop_runner_result_id": "final-result-001",
    }
    value.update(overrides)
    return value


def _assemble(**overrides):
    return assembler.assemble_local_noop_final_runner_result(**_inputs(**overrides))


def _assert_blocked(result):
    assert result["final_result_object_assembled"] is False
    assert tuple(result.keys()) == RESULT_KEYS
    assert result["source"] == BLOCKED_SOURCE
    assert result["local_noop_runner_result"] == {}
    assert result["assembly_violations"] != ()
    assert result["invariant_refs"] == assembler.INVARIANT_REFS
    for violation in result["result_validation_violations"]:
        assert tuple(violation.keys()) == ("reason_code", "field")


def _payload_keys(value):
    keys = ()
    if isinstance(value, dict):
        for key, nested in value.items():
            keys = keys + (key,)
            if key != "invariant_refs":
                keys = keys + _payload_keys(nested)
    elif isinstance(value, tuple) or isinstance(value, list):
        for nested in value:
            keys = keys + _payload_keys(nested)
    return keys


def _structurally_valid_rejected_p2d35_result(valid):
    valid_source = valid["source"]
    valid_result = valid["local_noop_runner_result"]
    evidence_items = tuple(
        {
            "runner_evidence_id": item["runner_evidence_id"],
            "runner_evidence_role": item["runner_evidence_role"],
            "artifact_ref": item["artifact_ref"],
            "artifact_kind": item["artifact_kind"],
            "evidence_status": item["evidence_status"],
            "producer_ref": item["producer_ref"],
            "evidence_refs": tuple(value for value in item["evidence_refs"]),
            "notes": tuple(value for value in item["notes"]),
        }
        for item in valid_result["runner_evidence_items"]
    )
    return {
        "buildable": False,
        "reason_code": "RUN_ID_MISSING",
        "reason": "Structurally valid rejected P2D-35 test fixture.",
        "source": {
            "local_noop_e2e_contract_ref": valid_source[
                "local_noop_e2e_contract_ref"
            ],
            "local_noop_e2e_contract_buildable_marker": valid_source[
                "local_noop_e2e_contract_buildable_marker"
            ],
            "mode": valid_source["mode"],
            "runner_terminal_status": valid_source["runner_terminal_status"],
            "public_url": valid_source["public_url"],
            "public_url_created": valid_source["public_url_created"],
            "source_of_truth": tuple(
                value for value in valid_source["source_of_truth"]
            ),
        },
        "local_noop_runner_result": {
            "run_id": valid_result["run_id"],
            "local_noop_runner_result_id": valid_result[
                "local_noop_runner_result_id"
            ],
            "result_kind": valid_result["result_kind"],
            "mode": valid_result["mode"],
            "runner_terminal_status": valid_result["runner_terminal_status"],
            "local_noop_e2e_contract_ref": valid_result[
                "local_noop_e2e_contract_ref"
            ],
            "local_noop_e2e_contract_buildable_marker": valid_result[
                "local_noop_e2e_contract_buildable_marker"
            ],
            "public_url": valid_result["public_url"],
            "public_url_created": valid_result["public_url_created"],
            "runner_evidence_items": evidence_items,
            "required_runner_evidence_ids": tuple(
                value for value in valid_result["required_runner_evidence_ids"]
            ),
            "missing_runner_evidence_ids": tuple(
                value for value in valid_result["missing_runner_evidence_ids"]
            ),
            "blocking_runner_evidence_ids": tuple(
                value for value in valid_result["blocking_runner_evidence_ids"]
            ),
            "created_at": valid_result["created_at"],
            "timestamp_policy": valid_result["timestamp_policy"],
            "source_of_truth": tuple(
                value for value in valid_result["source_of_truth"]
            ),
            "notes": tuple(value for value in valid_result["notes"]),
        },
        "result_violations": ("RUN_ID_MISSING",),
        "missing_or_invalid_fields": ("run_id",),
        "runner_evidence_item_violations": (),
        "invariant_refs": tuple(value for value in valid["invariant_refs"]),
    }


def test_catalogs_and_public_api_are_exact():
    assert assembler.REASON_CODES == (
        "LOCAL_NOOP_FINAL_RUNNER_RESULT_OBJECT_ASSEMBLED",
        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
        "P2D43_DECISION_RESULT_INVALID",
        "P2D42_CONSUMPTION_RESULT_INVALID",
        "P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID",
        "FINAL_RUNNER_RESULT_ID_INVALID",
        "FINAL_RUNNER_RESULT_ID_NOT_DISTINCT",
        "CROSS_LAYER_COHERENCE_MISMATCH",
        "PASS_PUBLISHED_FORBIDDEN",
        "EVIDENCE_PROJECTION_INVALID",
        "P2D35_BUILD_RESULT_REJECTED",
        "P2D35_BUILD_RESULT_INVALID",
        "P2D35_OUTPUT_COHERENCE_MISMATCH",
    )
    assert assembler.LOCAL_NOOP_FINAL_RUNNER_RESULT_ASSEMBLER_REASON_CODES == assembler.REASON_CODES
    assert assembler.REASON_PRIORITY == (
        "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
        "P2D43_DECISION_RESULT_INVALID",
        "P2D42_CONSUMPTION_RESULT_INVALID",
        "P2D33_E2E_CONTRACT_BUILD_RESULT_INVALID",
        "FINAL_RUNNER_RESULT_ID_INVALID",
        "FINAL_RUNNER_RESULT_ID_NOT_DISTINCT",
        "PASS_PUBLISHED_FORBIDDEN",
        "CROSS_LAYER_COHERENCE_MISMATCH",
        "EVIDENCE_PROJECTION_INVALID",
        "P2D35_BUILD_RESULT_REJECTED",
        "P2D35_BUILD_RESULT_INVALID",
        "P2D35_OUTPUT_COHERENCE_MISMATCH",
        "LOCAL_NOOP_FINAL_RUNNER_RESULT_OBJECT_ASSEMBLED",
    )
    assert assembler.INVARIANT_REFS == (
        "local_noop_final_runner_result_assembler_only",
        "assembler_pure_in_memory_only",
        "assembler_accepts_complete_p2d43_p2d42_p2d33_results",
        "nested_decision_candidate_contract_bypass_rejected",
        "explicit_final_runner_result_id_required",
        "final_runner_result_id_is_opaque_caller_identity",
        "final_runner_result_id_not_generated_or_derived",
        "final_runner_result_id_distinct_from_candidate_and_e2e_ids",
        "p2d33_supplies_e2e_contract_provenance",
        "readiness_reference_not_used_as_e2e_contract_reference",
        "p2d35_is_only_allowed_sibling_dependency",
        "p2d35_called_only_after_complete_validation",
        "p2d35_called_exactly_once_on_valid_input",
        "p2d35_not_called_on_upstream_failure",
        "p2d35_bool_wrapper_not_called",
        "p2d35_output_revalidated",
        "p2d35_blocked_output_not_returned_as_final_result",
        "p2d35_output_returned_as_fresh_projection",
        "candidate_evidence_projected_without_value_change",
        "candidate_evidence_identity_preserved",
        "candidate_evidence_role_preserved",
        "source_of_truth_combines_p2d33_then_p2d42",
        "source_of_truth_order_and_duplicates_preserved",
        "caller_input_not_mutated",
        "final_result_output_not_aliased",
        "final_result_object_assembled_means_in_memory_object_only",
        "noop_completed_is_nested_declarative_metadata_only",
        "final_result_not_runner_execution",
        "final_result_not_e2e_execution",
        "final_result_not_runtime_execution",
        "final_result_not_noop_completion_execution",
        "final_result_not_state_transition",
        "final_result_not_external_noop_completed_achievement",
        "final_result_not_ledger_write_authorization",
        "final_result_not_ledger_persistence",
        "final_result_not_cli_or_manual_invocation",
        "final_result_not_quality_pass",
        "final_result_not_gate_pass",
        "final_result_not_publish_allowed",
        "final_result_not_pass_published",
        "final_result_not_public_url_created",
        "final_result_not_notification_sent",
        "failed_evidence_may_be_assembled",
        "known_blocking_evidence_ids_are_evidence_only",
        "unknown_blocking_evidence_ids_block_assembly",
        "unknown_keys_block_and_are_suppressed",
        "forbidden_fields_block_and_are_suppressed",
        "recursive_key_scan_is_cycle_and_depth_safe",
        "recursive_key_scan_does_not_scan_scalar_strings",
        "mode_noop_required",
        "public_url_must_be_null",
        "public_url_created_must_be_false",
        "pass_published_forbidden",
        "no_file_or_artifact_io",
        "no_config_env_credentials_read",
        "no_run_ledger_yaml_read_or_write",
        "no_runtime_cli_command_or_subprocess",
        "no_completion_transition_gate_eval_audit_execution",
        "no_publish_or_notification",
        "no_quality_pass_no_public_url",
    )
    assert assembler.assemble_local_noop_final_runner_result.__code__.co_argcount == 0
    assert assembler.assemble_local_noop_final_runner_result.__code__.co_kwonlyargcount == 4
    assert assembler.is_local_noop_final_runner_result_object_assembled.__code__.co_argcount == 0
    assert assembler.is_local_noop_final_runner_result_object_assembled.__code__.co_kwonlyargcount == 4


def test_valid_assembly_has_exact_shape_mapping_and_fresh_output():
    inputs = _inputs()
    result = assembler.assemble_local_noop_final_runner_result(**inputs)

    assert result["final_result_object_assembled"] is True
    assert result["reason_code"] == "LOCAL_NOOP_FINAL_RUNNER_RESULT_OBJECT_ASSEMBLED"
    assert tuple(result.keys()) == RESULT_KEYS
    assert tuple(result["source"].keys()) == SOURCE_KEYS
    assert tuple(result["local_noop_runner_result"].keys()) == FINAL_RESULT_KEYS
    final_result = result["local_noop_runner_result"]
    assert final_result["local_noop_runner_result_id"] == "final-result-001"
    assert final_result["local_noop_e2e_contract_ref"] == "e2e-contract-001"
    assert final_result["local_noop_e2e_contract_buildable_marker"] is True
    assert final_result["source_of_truth"] == (
        "p2d-33", "e2e-source", "p2d-42", "candidate-source"
    )
    evidence = final_result["runner_evidence_items"][0]
    assert tuple(evidence.keys()) == RUNNER_EVIDENCE_KEYS
    assert evidence["runner_evidence_id"] == "candidate-evidence-001"
    assert evidence["runner_evidence_role"] == "local_noop_runner_readiness"
    input_candidate = inputs["local_noop_runner_result_candidate_consumption"][
        "normalized_local_noop_runner_result_candidate"
    ]
    assert final_result is not input_candidate
    assert evidence is not input_candidate["result_candidate_evidence_items"][0]
    assert result["source"] is not inputs["local_noop_terminal_result_assembly_decision_result"]["source"]


def test_exact_p2d35_call_and_boolean_wrapper_each_call_once():
    inputs = _inputs()
    original = assembler.explain_local_noop_runner_result_build
    calls = []

    def spy(**kwargs):
        calls.append(dict(kwargs))
        return original(**kwargs)

    assembler.explain_local_noop_runner_result_build = spy
    try:
        result = assembler.assemble_local_noop_final_runner_result(**inputs)
        assert result["final_result_object_assembled"] is True
        assert len(calls) == 1
        assert calls[0]["run_id"] == "run-001"
        assert calls[0]["local_noop_e2e_contract_ref"] == "e2e-contract-001"
        assert calls[0]["public_url_is_null"] is True
        assert calls[0]["source_of_truth"] == (
            "p2d-33", "e2e-source", "p2d-42", "candidate-source"
        )
        calls.clear()
        assert assembler.is_local_noop_final_runner_result_object_assembled(**inputs) is True
        assert len(calls) == 1
    finally:
        assembler.explain_local_noop_runner_result_build = original


def test_invalid_inputs_do_not_call_p2d35_or_leak_caller_data():
    inputs = _inputs()
    inputs["local_noop_terminal_result_assembly_decision_result"]["decision_created"] = False
    original = assembler.explain_local_noop_runner_result_build
    calls = []

    def spy(**kwargs):
        calls.append(dict(kwargs))
        return original(**kwargs)

    assembler.explain_local_noop_runner_result_build = spy
    try:
        result = assembler.assemble_local_noop_final_runner_result(**inputs)
    finally:
        assembler.explain_local_noop_runner_result_build = original
    _assert_blocked(result)
    assert calls == []
    assert "final-result-001" not in str(result)
    assert "candidate-001" not in str(result)


def test_nested_only_bypasses_and_malformed_wrappers_block():
    inputs = _inputs()
    for key, nested_key in (
        ("local_noop_terminal_result_assembly_decision_result", "local_noop_terminal_result_assembly_decision"),
        ("local_noop_runner_result_candidate_consumption", "normalized_local_noop_runner_result_candidate"),
        ("local_noop_e2e_contract_build_result", "local_noop_e2e_contract"),
    ):
        value = _inputs()
        value[key] = value[key][nested_key]
        _assert_blocked(assembler.assemble_local_noop_final_runner_result(**value))
    value = _inputs()
    value["local_noop_e2e_contract_build_result"]["unknown"] = "value"
    _assert_blocked(assembler.assemble_local_noop_final_runner_result(**value))


def test_result_id_rules_and_exact_type_distinctness():
    for value in ("", "   ", 1, None):
        result = _assemble(local_noop_runner_result_id=value)
        _assert_blocked(result)
        assert result["reason_code"] == "FINAL_RUNNER_RESULT_ID_INVALID"
    for value in ("candidate-001", "e2e-contract-001"):
        result = _assemble(local_noop_runner_result_id=value)
        _assert_blocked(result)
        assert result["reason_code"] == "FINAL_RUNNER_RESULT_ID_NOT_DISTINCT"
    assert _assemble(local_noop_runner_result_id="unrelated-final-id")[
        "final_result_object_assembled"
    ] is True


def test_cross_layer_coherence_is_type_aware_and_source_timestamps_are_independent():
    cases = (
        ("mode", "real"),
        ("runner_terminal_status", "DONE"),
        ("public_url_created", True),
    )
    for field, replacement in cases:
        value = _inputs()
        value["local_noop_runner_result_candidate_consumption"][
            "normalized_local_noop_runner_result_candidate"
        ][field] = replacement
        result = assembler.assemble_local_noop_final_runner_result(**value)
        _assert_blocked(result)
        assert "CROSS_LAYER_COHERENCE_MISMATCH" in result["assembly_violations"]
    value = _inputs()
    candidate = value["local_noop_runner_result_candidate_consumption"][
        "normalized_local_noop_runner_result_candidate"
    ]
    candidate["created_at"] = "different-candidate-time"
    candidate["timestamp_policy"] = "different-policy"
    value["local_noop_e2e_contract_build_result"]["local_noop_e2e_contract"][
        "created_at"
    ] = "other-e2e-time"
    value["local_noop_e2e_contract_build_result"]["local_noop_e2e_contract"][
        "timestamp_policy"
    ] = "other-e2e-policy"
    assert assembler.assemble_local_noop_final_runner_result(**value)[
        "final_result_object_assembled"
    ] is True
    value = _inputs()
    value["local_noop_e2e_contract_build_result"]["local_noop_e2e_contract"][
        "public_url_created"
    ] = 0
    _assert_blocked(assembler.assemble_local_noop_final_runner_result(**value))


def test_evidence_projection_failed_and_known_blocking_are_allowed_unknown_and_pass_block():
    value = _inputs()
    candidate = value["local_noop_runner_result_candidate_consumption"][
        "normalized_local_noop_runner_result_candidate"
    ]
    candidate["result_candidate_evidence_items"][0]["evidence_status"] = "failed"
    candidate["blocking_result_candidate_evidence_ids"] = ("candidate-evidence-001",)
    result = assembler.assemble_local_noop_final_runner_result(**value)
    assert result["final_result_object_assembled"] is True
    assert result["local_noop_runner_result"]["runner_evidence_items"][0][
        "evidence_status"
    ] == "failed"
    value = _inputs()
    value["local_noop_runner_result_candidate_consumption"][
        "normalized_local_noop_runner_result_candidate"
    ]["blocking_result_candidate_evidence_ids"] = ("unknown",)
    _assert_blocked(assembler.assemble_local_noop_final_runner_result(**value))
    value = _inputs()
    value["local_noop_runner_result_candidate_consumption"][
        "normalized_local_noop_runner_result_candidate"
    ]["result_candidate_evidence_items"][0]["evidence_status"] = "PASS_PUBLISHED"
    result = assembler.assemble_local_noop_final_runner_result(**value)
    _assert_blocked(result)
    assert result["reason_code"] == "PASS_PUBLISHED_FORBIDDEN"


def test_structurally_valid_rejected_p2d35_result_is_rejected_without_leakage():
    inputs = _inputs()
    original = assembler.explain_local_noop_runner_result_build
    calls = []
    returned_results = []

    def rejected_stub(**kwargs):
        calls.append(dict(kwargs))
        rejected = _structurally_valid_rejected_p2d35_result(original(**kwargs))
        returned_results.append(rejected)
        return rejected

    assembler.explain_local_noop_runner_result_build = rejected_stub
    try:
        result = assembler.assemble_local_noop_final_runner_result(**inputs)
    finally:
        assembler.explain_local_noop_runner_result_build = original

    _assert_blocked(result)
    assert len(calls) == 1
    assert len(returned_results) == 1
    assert result["reason_code"] == "P2D35_BUILD_RESULT_REJECTED"
    assert "P2D35_BUILD_RESULT_INVALID" not in result["assembly_violations"]
    assert result["source"] == BLOCKED_SOURCE
    assert result["local_noop_runner_result"] == {}
    assert "p2d44.p2d35_result" in result["missing_or_invalid_fields"]
    assert result is not returned_results[0]
    assert result["source"] is not returned_results[0]["source"]
    assert result["local_noop_runner_result"] is not returned_results[0][
        "local_noop_runner_result"
    ]
    for leaked in (
        "Structurally valid rejected P2D-35 test fixture.",
        "final-result-001",
        "candidate-001",
        "e2e-contract-001",
        "local_noop_terminal_result_assembly_decision_result",
        "local_noop_runner_result_candidate_consumption",
        "local_noop_e2e_contract_build_result",
    ):
        assert leaked not in str(result)


def test_scanner_is_cycle_and_depth_safe_and_does_not_scan_scalar_strings():
    value = _inputs()
    cycle = {}
    cycle["completed"] = True
    cycle["self"] = cycle
    value["local_noop_terminal_result_assembly_decision_result"]["extra"] = cycle
    result = assembler.assemble_local_noop_final_runner_result(**value)
    _assert_blocked(result)
    assert result["reason_code"] == "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"
    assert "p2d44.forbidden_field_or_namespace" in result[
        "missing_or_invalid_fields"
    ]
    value = _inputs()
    nested = []
    current = nested
    for _ in range(1500):
        next_value = []
        current.append(next_value)
        current = next_value
    value["local_noop_e2e_contract_build_result"]["extra"] = nested
    _assert_blocked(assembler.assemble_local_noop_final_runner_result(**value))
    value = _inputs()
    value["local_noop_runner_result_candidate_consumption"][
        "normalized_local_noop_runner_result_candidate"
    ]["notes"] = ("PASS_PUBLISHED",)
    assert assembler.assemble_local_noop_final_runner_result(**value)[
        "final_result_object_assembled"
    ] is True


def test_boundary_semantics_and_input_immutability():
    inputs = _inputs()
    original_notes = inputs["local_noop_runner_result_candidate_consumption"][
        "normalized_local_noop_runner_result_candidate"
    ]["notes"]
    result = assembler.assemble_local_noop_final_runner_result(**inputs)
    assert inputs["local_noop_runner_result_candidate_consumption"][
        "normalized_local_noop_runner_result_candidate"
    ]["notes"] == original_notes
    payload_keys = _payload_keys(result)
    for forbidden in (
        "completed", "executed", "realized", "terminal_reached",
        "noop_completed", "completion_achieved", "transitioned",
        "runner_executed", "ledger_written", "published", "notified",
        "publish_allowed", "quality_pass", "gate_pass", "eval_pass",
        "audit_pass",
    ):
        assert forbidden not in payload_keys
    assert result["source"]["runner_terminal_status"] == "NOOP_COMPLETED"
    assert result["local_noop_runner_result"]["runner_terminal_status"] == (
        "NOOP_COMPLETED"
    )
    for key, value in result["source"].items():
        if key != "runner_terminal_status":
            assert value != "NOOP_COMPLETED"
    for key, value in result["local_noop_runner_result"].items():
        if key != "runner_terminal_status":
            assert value != "NOOP_COMPLETED"
    assert result["source"]["public_url"] is None
    assert result["source"]["public_url_created"] is False
    assert result["local_noop_runner_result"]["public_url"] is None
    assert result["local_noop_runner_result"]["public_url_created"] is False


def test_tuple_projection_is_fresh_at_every_nonempty_boundary():
    evidence_refs = tuple(["readiness-001#result", "readiness-001#detail"])
    evidence_notes = tuple(["candidate-evidence", "candidate-evidence-note"])
    candidate_evidence = _candidate_evidence(
        evidence_refs=evidence_refs,
        notes=evidence_notes,
    )
    runner_evidence_items = tuple([candidate_evidence])
    required_ids = tuple(["candidate-evidence-001"])
    blocking_ids = tuple(["candidate-evidence-001"])
    candidate_notes = tuple(["candidate-note", "candidate-note-detail"])
    candidate_source = tuple(["shared-source", "candidate-source"])
    contract_source = tuple(["contract-source", "shared-source"])
    candidate = _candidate(
        result_candidate_evidence_items=runner_evidence_items,
        required_result_candidate_evidence_ids=required_ids,
        blocking_result_candidate_evidence_ids=blocking_ids,
        source_of_truth=candidate_source,
        notes=candidate_notes,
    )
    p2d33 = _p2d33(candidate)
    p2d33["local_noop_e2e_contract"]["source_of_truth"] = contract_source
    p2d33["source"]["source_of_truth"] = contract_source
    inputs = {
        "local_noop_terminal_result_assembly_decision_result": _p2d43(candidate),
        "local_noop_runner_result_candidate_consumption": _p2d42(candidate),
        "local_noop_e2e_contract_build_result": p2d33,
        "local_noop_runner_result_id": "final-result-001",
    }
    original = assembler.explain_local_noop_runner_result_build
    calls = []
    p2d35_results = []

    def spy(**kwargs):
        calls.append(dict(kwargs))
        built = original(**kwargs)
        p2d35_results.append(built)
        return built

    assembler.explain_local_noop_runner_result_build = spy
    try:
        result = assembler.assemble_local_noop_final_runner_result(**inputs)
    finally:
        assembler.explain_local_noop_runner_result_build = original

    assert result["final_result_object_assembled"] is True
    assert len(calls) == 1
    assert len(p2d35_results) == 1
    kwargs = calls[0]
    assert kwargs["runner_evidence_items"] == runner_evidence_items
    assert kwargs["runner_evidence_items"] is not runner_evidence_items
    assert kwargs["runner_evidence_items"][0] is not candidate_evidence
    assert kwargs["runner_evidence_items"][0]["evidence_refs"] == evidence_refs
    assert kwargs["runner_evidence_items"][0]["evidence_refs"] is not evidence_refs
    assert kwargs["runner_evidence_items"][0]["notes"] == evidence_notes
    assert kwargs["runner_evidence_items"][0]["notes"] is not evidence_notes
    assert kwargs["required_runner_evidence_ids"] == required_ids
    assert kwargs["required_runner_evidence_ids"] is not required_ids
    assert kwargs["blocking_runner_evidence_ids"] == blocking_ids
    assert kwargs["blocking_runner_evidence_ids"] is not blocking_ids
    assert kwargs["notes"] == candidate_notes
    assert kwargs["notes"] is not candidate_notes
    assert kwargs["source_of_truth"] == (
        "contract-source", "shared-source", "shared-source", "candidate-source"
    )
    assert kwargs["source_of_truth"] is not contract_source
    assert kwargs["source_of_truth"] is not candidate_source

    p2d35_result = p2d35_results[0]
    p2d35_final = p2d35_result["local_noop_runner_result"]
    final_result = result["local_noop_runner_result"]
    assert final_result["runner_evidence_items"] == p2d35_final["runner_evidence_items"]
    assert final_result["runner_evidence_items"] is not p2d35_final["runner_evidence_items"]
    assert final_result["runner_evidence_items"] is not runner_evidence_items
    assert final_result["runner_evidence_items"][0] is not p2d35_final["runner_evidence_items"][0]
    assert final_result["runner_evidence_items"][0] is not candidate_evidence
    assert final_result["runner_evidence_items"][0]["evidence_refs"] == p2d35_final["runner_evidence_items"][0]["evidence_refs"]
    assert final_result["runner_evidence_items"][0]["evidence_refs"] is not p2d35_final["runner_evidence_items"][0]["evidence_refs"]
    assert final_result["runner_evidence_items"][0]["evidence_refs"] is not evidence_refs
    assert final_result["runner_evidence_items"][0]["notes"] == p2d35_final["runner_evidence_items"][0]["notes"]
    assert final_result["runner_evidence_items"][0]["notes"] is not p2d35_final["runner_evidence_items"][0]["notes"]
    assert final_result["runner_evidence_items"][0]["notes"] is not evidence_notes
    assert final_result["required_runner_evidence_ids"] == p2d35_final["required_runner_evidence_ids"]
    assert final_result["required_runner_evidence_ids"] is not p2d35_final["required_runner_evidence_ids"]
    assert final_result["required_runner_evidence_ids"] is not required_ids
    assert final_result["blocking_runner_evidence_ids"] == p2d35_final["blocking_runner_evidence_ids"]
    assert final_result["blocking_runner_evidence_ids"] is not p2d35_final["blocking_runner_evidence_ids"]
    assert final_result["blocking_runner_evidence_ids"] is not blocking_ids
    assert final_result["notes"] == p2d35_final["notes"]
    assert final_result["notes"] is not p2d35_final["notes"]
    assert final_result["notes"] is not candidate_notes
    assert final_result["source_of_truth"] == p2d35_final["source_of_truth"]
    assert final_result["source_of_truth"] is not p2d35_final["source_of_truth"]
    assert final_result["source_of_truth"] is not contract_source
    assert final_result["source_of_truth"] is not candidate_source
    assert result["source"]["source_of_truth"] == p2d35_result["source"]["source_of_truth"]
    assert result["source"]["source_of_truth"] is not p2d35_result["source"]["source_of_truth"]
    assert result["source"]["source_of_truth"] is not final_result["source_of_truth"]
    assert candidate_evidence["evidence_refs"] == evidence_refs
    assert candidate_evidence["notes"] == evidence_notes
    assert candidate["result_candidate_evidence_items"] == runner_evidence_items
    assert candidate["required_result_candidate_evidence_ids"] == required_ids
    assert candidate["blocking_result_candidate_evidence_ids"] == blocking_ids
    assert candidate["notes"] == candidate_notes

    empty_candidate = _candidate(
        blocking_result_candidate_evidence_ids=(),
        notes=(),
    )
    empty_result = assembler.assemble_local_noop_final_runner_result(
        local_noop_terminal_result_assembly_decision_result=_p2d43(empty_candidate),
        local_noop_runner_result_candidate_consumption=_p2d42(empty_candidate),
        local_noop_e2e_contract_build_result=_p2d33(empty_candidate),
        local_noop_runner_result_id="final-result-empty-tuples",
    )
    assert empty_result["final_result_object_assembled"] is True
    for value in (
        empty_result["local_noop_runner_result"]["missing_runner_evidence_ids"],
        empty_result["local_noop_runner_result"]["blocking_runner_evidence_ids"],
        empty_result["local_noop_runner_result"]["notes"],
    ):
        assert type(value) is tuple
        assert value == ()


def test_p2d35_receives_the_complete_exact_argument_map():
    inputs = _inputs()
    candidate = inputs["local_noop_runner_result_candidate_consumption"][
        "normalized_local_noop_runner_result_candidate"
    ]
    contract = inputs["local_noop_e2e_contract_build_result"]["local_noop_e2e_contract"]
    original = assembler.explain_local_noop_runner_result_build
    calls = []

    def spy(**kwargs):
        calls.append(dict(kwargs))
        return original(**kwargs)

    assembler.explain_local_noop_runner_result_build = spy
    try:
        result = assembler.assemble_local_noop_final_runner_result(**inputs)
    finally:
        assembler.explain_local_noop_runner_result_build = original

    assert result["final_result_object_assembled"] is True
    assert len(calls) == 1
    kwargs = calls[0]
    assert set(kwargs) == {
        "run_id",
        "local_noop_runner_result_id",
        "result_kind",
        "mode",
        "runner_terminal_status",
        "local_noop_e2e_contract_ref",
        "local_noop_e2e_contract_buildable_marker",
        "public_url_created",
        "public_url_is_null",
        "runner_evidence_items",
        "required_runner_evidence_ids",
        "missing_runner_evidence_ids",
        "blocking_runner_evidence_ids",
        "created_at",
        "timestamp_policy",
        "source_of_truth",
        "notes",
    }
    assert type(kwargs["run_id"]) is str
    assert kwargs["run_id"] == candidate["run_id"]
    assert type(kwargs["local_noop_runner_result_id"]) is str
    assert kwargs["local_noop_runner_result_id"] == inputs["local_noop_runner_result_id"]
    assert type(kwargs["result_kind"]) is str
    assert kwargs["result_kind"] == "local_noop_runner_result"
    assert type(kwargs["mode"]) is str
    assert kwargs["mode"] == "noop"
    assert type(kwargs["runner_terminal_status"]) is str
    assert kwargs["runner_terminal_status"] == "NOOP_COMPLETED"
    assert type(kwargs["local_noop_e2e_contract_ref"]) is str
    assert kwargs["local_noop_e2e_contract_ref"] == contract["local_noop_e2e_contract_id"]
    assert type(kwargs["local_noop_e2e_contract_buildable_marker"]) is bool
    assert kwargs["local_noop_e2e_contract_buildable_marker"] is True
    assert type(kwargs["public_url_is_null"]) is bool
    assert kwargs["public_url_is_null"] is True
    assert type(kwargs["public_url_created"]) is bool
    assert kwargs["public_url_created"] is False
    assert type(kwargs["runner_evidence_items"]) is tuple
    assert len(kwargs["runner_evidence_items"]) == 1
    evidence = kwargs["runner_evidence_items"][0]
    candidate_evidence = candidate["result_candidate_evidence_items"][0]
    assert tuple(evidence.keys()) == RUNNER_EVIDENCE_KEYS
    for key in RUNNER_EVIDENCE_KEYS[:6]:
        assert type(evidence[key]) is str
    assert evidence["runner_evidence_id"] == candidate_evidence["result_candidate_evidence_id"]
    assert evidence["runner_evidence_role"] == candidate_evidence["result_candidate_evidence_role"]
    assert evidence["artifact_ref"] == candidate_evidence["artifact_ref"]
    assert evidence["artifact_kind"] == candidate_evidence["artifact_kind"]
    assert evidence["evidence_status"] == candidate_evidence["evidence_status"]
    assert evidence["producer_ref"] == candidate_evidence["producer_ref"]
    assert evidence["evidence_refs"] == candidate_evidence["evidence_refs"]
    assert evidence["notes"] == candidate_evidence["notes"]
    assert type(kwargs["required_runner_evidence_ids"]) is tuple
    assert kwargs["required_runner_evidence_ids"] == candidate["required_result_candidate_evidence_ids"]
    assert type(kwargs["missing_runner_evidence_ids"]) is tuple
    assert kwargs["missing_runner_evidence_ids"] == ()
    assert type(kwargs["blocking_runner_evidence_ids"]) is tuple
    assert kwargs["blocking_runner_evidence_ids"] == candidate["blocking_result_candidate_evidence_ids"]
    assert type(kwargs["created_at"]) is str
    assert kwargs["created_at"] == candidate["created_at"]
    assert type(kwargs["timestamp_policy"]) is str
    assert kwargs["timestamp_policy"] == candidate["timestamp_policy"]
    assert type(kwargs["source_of_truth"]) is tuple
    assert kwargs["source_of_truth"] == contract["source_of_truth"] + candidate["source_of_truth"]
    assert kwargs["source_of_truth"] == (
        "p2d-33", "e2e-source", "p2d-42", "candidate-source"
    )
    assert type(kwargs["notes"]) is tuple
    assert kwargs["notes"] == candidate["notes"]


def test_every_invalid_gate_blocks_before_p2d35():
    cases = []

    def add_case(name, mutate):
        value = _inputs()
        mutate(value)
        cases.append((name, value))

    add_case(
        "malformed_p2d43_wrapper",
        lambda value: value.__setitem__(
            "local_noop_terminal_result_assembly_decision_result", None
        ),
    )
    add_case(
        "p2d43_success_marker",
        lambda value: value["local_noop_terminal_result_assembly_decision_result"].__setitem__(
            "decision_created", False
        ),
    )
    add_case(
        "p2d43_success_reason",
        lambda value: value["local_noop_terminal_result_assembly_decision_result"].__setitem__(
            "reason_code", "OTHER_REASON"
        ),
    )
    add_case(
        "p2d43_diagnostics",
        lambda value: value["local_noop_terminal_result_assembly_decision_result"].__setitem__(
            "decision_violations", ("failed",)
        ),
    )
    add_case(
        "p2d43_invariants",
        lambda value: value["local_noop_terminal_result_assembly_decision_result"].__setitem__(
            "invariant_refs", ()
        ),
    )
    add_case(
        "malformed_p2d42_wrapper",
        lambda value: value.__setitem__(
            "local_noop_runner_result_candidate_consumption", None
        ),
    )
    add_case(
        "p2d42_success_marker",
        lambda value: value["local_noop_runner_result_candidate_consumption"].__setitem__(
            "consumed", False
        ),
    )
    add_case(
        "p2d42_success_reason",
        lambda value: value["local_noop_runner_result_candidate_consumption"].__setitem__(
            "reason_code", "OTHER_REASON"
        ),
    )
    add_case(
        "p2d42_diagnostics",
        lambda value: value["local_noop_runner_result_candidate_consumption"].__setitem__(
            "consumption_violations", ("failed",)
        ),
    )
    add_case(
        "p2d42_invariants",
        lambda value: value["local_noop_runner_result_candidate_consumption"].__setitem__(
            "invariant_refs", ()
        ),
    )
    add_case(
        "malformed_p2d33_wrapper",
        lambda value: value.__setitem__(
            "local_noop_e2e_contract_build_result", None
        ),
    )
    add_case(
        "p2d33_success_marker",
        lambda value: value["local_noop_e2e_contract_build_result"].__setitem__(
            "buildable", False
        ),
    )
    add_case(
        "p2d33_success_reason",
        lambda value: value["local_noop_e2e_contract_build_result"].__setitem__(
            "reason_code", "OTHER_REASON"
        ),
    )
    add_case(
        "p2d33_diagnostics",
        lambda value: value["local_noop_e2e_contract_build_result"].__setitem__(
            "contract_violations", ("failed",)
        ),
    )
    add_case(
        "p2d33_invariants",
        lambda value: value["local_noop_e2e_contract_build_result"].__setitem__(
            "invariant_refs", ()
        ),
    )
    add_case(
        "blank_result_id",
        lambda value: value.__setitem__("local_noop_runner_result_id", " "),
    )
    add_case(
        "non_string_result_id",
        lambda value: value.__setitem__("local_noop_runner_result_id", 1),
    )
    add_case(
        "candidate_result_id",
        lambda value: value.__setitem__("local_noop_runner_result_id", "candidate-001"),
    )
    add_case(
        "e2e_contract_result_id",
        lambda value: value.__setitem__("local_noop_runner_result_id", "e2e-contract-001"),
    )
    add_case(
        "p2d43_p2d42_coherence",
        lambda value: value["local_noop_terminal_result_assembly_decision_result"][
            "local_noop_terminal_result_assembly_decision"
        ].__setitem__("run_id", "run-002"),
    )
    add_case(
        "p2d33_p2d42_coherence",
        lambda value: value["local_noop_e2e_contract_build_result"][
            "local_noop_e2e_contract"
        ].__setitem__("run_id", "run-002"),
    )
    add_case(
        "p2d33_p2d43_coherence",
        lambda value: value["local_noop_e2e_contract_build_result"][
            "local_noop_e2e_contract"
        ].__setitem__("run_id", "run-003"),
    )
    add_case(
        "invalid_evidence_projection",
        lambda value: value["local_noop_runner_result_candidate_consumption"][
            "normalized_local_noop_runner_result_candidate"
        ].__setitem__("result_candidate_evidence_items", ()),
    )
    add_case(
        "unknown_blocking_evidence_id",
        lambda value: value["local_noop_runner_result_candidate_consumption"][
            "normalized_local_noop_runner_result_candidate"
        ].__setitem__("blocking_result_candidate_evidence_ids", ("unknown",)),
    )
    add_case(
        "pass_published_approved_status",
        lambda value: value["local_noop_runner_result_candidate_consumption"][
            "normalized_local_noop_runner_result_candidate"
        ]["result_candidate_evidence_items"][0].__setitem__(
            "evidence_status", "PASS_PUBLISHED"
        ),
    )
    add_case(
        "forbidden_field",
        lambda value: value["local_noop_e2e_contract_build_result"].__setitem__(
            "completed", True
        ),
    )

    original = assembler.explain_local_noop_runner_result_build
    calls = []

    def spy(**kwargs):
        calls.append(dict(kwargs))
        return original(**kwargs)

    assembler.explain_local_noop_runner_result_build = spy
    try:
        for name, value in cases:
            calls.clear()
            result = assembler.assemble_local_noop_final_runner_result(**value)
            _assert_blocked(result)
            assert calls == [], name
    finally:
        assembler.explain_local_noop_runner_result_build = original


def test_complete_cross_layer_coherence_matrix_and_exact_boolean_types():
    cases = []

    def add_case(name, mutate):
        value = _inputs()
        mutate(value)
        cases.append((name, value))

    add_case(
        "p2d43_decision_run_id",
        lambda value: value["local_noop_terminal_result_assembly_decision_result"][
            "local_noop_terminal_result_assembly_decision"
        ].__setitem__("run_id", "run-002"),
    )
    add_case(
        "p2d43_decision_candidate_id",
        lambda value: value["local_noop_terminal_result_assembly_decision_result"][
            "local_noop_terminal_result_assembly_decision"
        ].__setitem__("local_noop_runner_result_candidate_id", "candidate-002"),
    )
    add_case(
        "p2d43_source_candidate_id",
        lambda value: value["local_noop_terminal_result_assembly_decision_result"][
            "source"
        ].__setitem__("local_noop_runner_result_candidate_id", "candidate-003"),
    )
    add_case(
        "p2d43_decision_mode",
        lambda value: value["local_noop_terminal_result_assembly_decision_result"][
            "local_noop_terminal_result_assembly_decision"
        ].__setitem__("mode", "not-noop"),
    )
    add_case(
        "p2d43_source_mode",
        lambda value: value["local_noop_terminal_result_assembly_decision_result"][
            "source"
        ].__setitem__("mode", "not-noop"),
    )
    add_case(
        "p2d42_source_mode",
        lambda value: value["local_noop_runner_result_candidate_consumption"][
            "source"
        ].__setitem__("mode", "not-noop"),
    )
    add_case(
        "p2d42_receipt_mode",
        lambda value: value["local_noop_runner_result_candidate_consumption"][
            "local_noop_runner_consumption_receipt"
        ].__setitem__("mode", "not-noop"),
    )
    add_case(
        "p2d43_source_candidate_runner_terminal_status",
        lambda value: value["local_noop_terminal_result_assembly_decision_result"][
            "source"
        ].__setitem__("candidate_runner_terminal_status", "NOT_NOOP_COMPLETED"),
    )
    add_case(
        "p2d43_decision_public_url",
        lambda value: value["local_noop_terminal_result_assembly_decision_result"][
            "local_noop_terminal_result_assembly_decision"
        ].__setitem__("public_url", "unexpected-url"),
    )
    add_case(
        "p2d43_source_public_url",
        lambda value: value["local_noop_terminal_result_assembly_decision_result"][
            "source"
        ].__setitem__("public_url", "unexpected-url"),
    )
    add_case(
        "p2d42_source_public_url",
        lambda value: value["local_noop_runner_result_candidate_consumption"][
            "source"
        ].__setitem__("public_url", "unexpected-url"),
    )
    add_case(
        "p2d42_receipt_public_url",
        lambda value: value["local_noop_runner_result_candidate_consumption"][
            "local_noop_runner_consumption_receipt"
        ].__setitem__("public_url", "unexpected-url"),
    )
    add_case(
        "p2d43_decision_public_url_created",
        lambda value: value["local_noop_terminal_result_assembly_decision_result"][
            "local_noop_terminal_result_assembly_decision"
        ].__setitem__("public_url_created", True),
    )
    add_case(
        "p2d43_source_public_url_created",
        lambda value: value["local_noop_terminal_result_assembly_decision_result"][
            "source"
        ].__setitem__("public_url_created", True),
    )
    add_case(
        "p2d42_source_public_url_created",
        lambda value: value["local_noop_runner_result_candidate_consumption"][
            "source"
        ].__setitem__("public_url_created", True),
    )
    add_case(
        "p2d42_receipt_public_url_created",
        lambda value: value["local_noop_runner_result_candidate_consumption"][
            "local_noop_runner_consumption_receipt"
        ].__setitem__("public_url_created", True),
    )
    add_case(
        "p2d43_source_source_of_truth",
        lambda value: value["local_noop_terminal_result_assembly_decision_result"][
            "source"
        ].__setitem__("source_of_truth", ("decision-source-only",)),
    )
    add_case(
        "p2d42_source_source_of_truth",
        lambda value: value["local_noop_runner_result_candidate_consumption"][
            "source"
        ].__setitem__("source_of_truth", ("consumer-source-only",)),
    )
    add_case(
        "p2d42_source_candidate_id",
        lambda value: value["local_noop_runner_result_candidate_consumption"][
            "source"
        ].__setitem__("local_noop_runner_result_candidate_id", "candidate-004"),
    )
    add_case(
        "p2d42_receipt_candidate_id",
        lambda value: value["local_noop_runner_result_candidate_consumption"][
            "local_noop_runner_consumption_receipt"
        ].__setitem__("local_noop_runner_result_candidate_id", "candidate-005"),
    )
    def p2d43_decision_public_url_created_true_vs_one(value):
        value["local_noop_terminal_result_assembly_decision_result"][
            "local_noop_terminal_result_assembly_decision"
        ]["public_url_created"] = True
        value["local_noop_runner_result_candidate_consumption"][
            "normalized_local_noop_runner_result_candidate"
        ]["public_url_created"] = 1

    add_case(
        "p2d43_decision_public_url_created_true_vs_one",
        p2d43_decision_public_url_created_true_vs_one,
    )
    add_case(
        "p2d43_source_public_url_created_false_vs_zero",
        lambda value: value["local_noop_runner_result_candidate_consumption"][
            "normalized_local_noop_runner_result_candidate"
        ].__setitem__("public_url_created", 0),
    )
    add_case(
        "p2d33_p2d42_run_id",
        lambda value: value["local_noop_e2e_contract_build_result"][
            "local_noop_e2e_contract"
        ].__setitem__("run_id", "run-002"),
    )
    add_case(
        "p2d33_p2d42_mode",
        lambda value: value["local_noop_e2e_contract_build_result"][
            "local_noop_e2e_contract"
        ].__setitem__("mode", "not-noop"),
    )
    add_case(
        "p2d33_p2d42_terminal_status",
        lambda value: value["local_noop_e2e_contract_build_result"][
            "local_noop_e2e_contract"
        ].__setitem__("e2e_terminal_status", "NOT_NOOP_COMPLETED"),
    )
    add_case(
        "p2d33_p2d42_public_url",
        lambda value: value["local_noop_e2e_contract_build_result"][
            "local_noop_e2e_contract"
        ].__setitem__("public_url", "unexpected-url"),
    )
    add_case(
        "p2d33_p2d42_public_url_created",
        lambda value: value["local_noop_e2e_contract_build_result"][
            "local_noop_e2e_contract"
        ].__setitem__("public_url_created", True),
    )

    def p2d33_p2d43_run_id(value):
        candidate = value["local_noop_runner_result_candidate_consumption"][
            "normalized_local_noop_runner_result_candidate"
        ]
        candidate["run_id"] = "run-002"
        value["local_noop_runner_result_candidate_consumption"][
            "local_noop_runner_consumption_receipt"
        ]["run_id"] = "run-002"
        value["local_noop_terminal_result_assembly_decision_result"][
            "local_noop_terminal_result_assembly_decision"
        ]["run_id"] = "run-002"

    def p2d33_p2d43_mode(value):
        value["local_noop_runner_result_candidate_consumption"][
            "normalized_local_noop_runner_result_candidate"
        ]["mode"] = "not-noop"
        value["local_noop_runner_result_candidate_consumption"]["source"]["mode"] = "not-noop"
        value["local_noop_runner_result_candidate_consumption"][
            "local_noop_runner_consumption_receipt"
        ]["mode"] = "not-noop"
        value["local_noop_terminal_result_assembly_decision_result"]["source"]["mode"] = "not-noop"
        value["local_noop_terminal_result_assembly_decision_result"][
            "local_noop_terminal_result_assembly_decision"
        ]["mode"] = "not-noop"

    def p2d33_p2d43_terminal_status(value):
        value["local_noop_runner_result_candidate_consumption"][
            "normalized_local_noop_runner_result_candidate"
        ]["runner_terminal_status"] = "NOT_NOOP_COMPLETED"
        value["local_noop_terminal_result_assembly_decision_result"]["source"][
            "candidate_runner_terminal_status"
        ] = "NOT_NOOP_COMPLETED"

    def p2d33_p2d43_public_url(value):
        value["local_noop_runner_result_candidate_consumption"][
            "normalized_local_noop_runner_result_candidate"
        ]["public_url"] = "unexpected-url"
        value["local_noop_runner_result_candidate_consumption"]["source"][
            "public_url"
        ] = "unexpected-url"
        value["local_noop_runner_result_candidate_consumption"][
            "local_noop_runner_consumption_receipt"
        ]["public_url"] = "unexpected-url"
        value["local_noop_terminal_result_assembly_decision_result"]["source"][
            "public_url"
        ] = "unexpected-url"
        value["local_noop_terminal_result_assembly_decision_result"][
            "local_noop_terminal_result_assembly_decision"
        ]["public_url"] = "unexpected-url"

    def p2d33_p2d43_public_url_created(value):
        value["local_noop_runner_result_candidate_consumption"][
            "normalized_local_noop_runner_result_candidate"
        ]["public_url_created"] = True
        value["local_noop_runner_result_candidate_consumption"]["source"][
            "public_url_created"
        ] = True
        value["local_noop_runner_result_candidate_consumption"][
            "local_noop_runner_consumption_receipt"
        ]["public_url_created"] = True
        value["local_noop_terminal_result_assembly_decision_result"]["source"][
            "public_url_created"
        ] = True
        value["local_noop_terminal_result_assembly_decision_result"][
            "local_noop_terminal_result_assembly_decision"
        ]["public_url_created"] = True

    add_case("p2d33_p2d43_run_id", p2d33_p2d43_run_id)
    add_case("p2d33_p2d43_mode", p2d33_p2d43_mode)
    add_case("p2d33_p2d43_terminal_status", p2d33_p2d43_terminal_status)
    add_case("p2d33_p2d43_public_url", p2d33_p2d43_public_url)
    add_case("p2d33_p2d43_public_url_created", p2d33_p2d43_public_url_created)

    original = assembler.explain_local_noop_runner_result_build
    calls = []

    def spy(**kwargs):
        calls.append(dict(kwargs))
        return original(**kwargs)

    assembler.explain_local_noop_runner_result_build = spy
    try:
        for name, value in cases:
            calls.clear()
            result = assembler.assemble_local_noop_final_runner_result(**value)
            _assert_blocked(result)
            assert "CROSS_LAYER_COHERENCE_MISMATCH" in result["assembly_violations"], name
            assert calls == [], name
            assert result["source"] == BLOCKED_SOURCE, name
            assert result["local_noop_runner_result"] == {}, name
            assert "p2d44.cross_layer_coherence" in result[
                "missing_or_invalid_fields"
            ], name
            assert all(
                violation["field"].startswith("p2d44.")
                for violation in result["result_validation_violations"]
            ), name
            payload = str(result)
            for leaked in (
                "final-result-001",
                "candidate-001",
                "e2e-contract-001",
                "run-002",
                "run-003",
                "candidate-002",
                "candidate-003",
                "candidate-004",
                "candidate-005",
                "not-noop",
                "NOT_NOOP_COMPLETED",
                "unexpected-url",
                "decision-source-only",
                "consumer-source-only",
                "local_noop_terminal_result_assembly_decision_result",
                "local_noop_runner_result_candidate_consumption",
                "local_noop_e2e_contract_build_result",
            ):
                assert leaked not in payload, name
    finally:
        assembler.explain_local_noop_runner_result_build = original

    assert assembler._values_match_exactly(True, 1) is False
    assert assembler._values_match_exactly(False, 0) is False

    value = _inputs()
    candidate = value["local_noop_runner_result_candidate_consumption"][
        "normalized_local_noop_runner_result_candidate"
    ]
    candidate["created_at"] = "candidate-time-only"
    candidate["timestamp_policy"] = "candidate-policy-only"
    contract = value["local_noop_e2e_contract_build_result"]["local_noop_e2e_contract"]
    contract["created_at"] = "contract-time-only"
    contract["timestamp_policy"] = "contract-policy-only"
    contract["source_of_truth"] = ("contract-source-only",)
    contract["notes"] = ("contract-note-only",)
    value["local_noop_e2e_contract_build_result"]["source"]["source_of_truth"] = (
        "contract-source-only",
    )
    allowed_calls = []

    def allowed_spy(**kwargs):
        allowed_calls.append(dict(kwargs))
        return original(**kwargs)

    assembler.explain_local_noop_runner_result_build = allowed_spy
    try:
        result = assembler.assemble_local_noop_final_runner_result(**value)
    finally:
        assembler.explain_local_noop_runner_result_build = original

    assert result["final_result_object_assembled"] is True
    assert len(allowed_calls) == 1
    final_result = result["local_noop_runner_result"]
    assert final_result["created_at"] == candidate["created_at"]
    assert final_result["timestamp_policy"] == candidate["timestamp_policy"]
    assert final_result["notes"] == candidate["notes"]
    assert final_result["source_of_truth"] == (
        "contract-source-only",
        "p2d-42",
        "candidate-source",
    )


def test_source_of_truth_order_duplicates_and_fresh_projection_are_exact():
    candidate_source = tuple(["shared-source", "candidate-source"])
    contract_source = tuple(["contract-source", "shared-source"])
    candidate = _candidate(source_of_truth=candidate_source)
    p2d33 = _p2d33(candidate)
    p2d33["local_noop_e2e_contract"]["source_of_truth"] = contract_source
    p2d33["source"]["source_of_truth"] = contract_source
    inputs = {
        "local_noop_terminal_result_assembly_decision_result": _p2d43(candidate),
        "local_noop_runner_result_candidate_consumption": _p2d42(candidate),
        "local_noop_e2e_contract_build_result": p2d33,
        "local_noop_runner_result_id": "final-result-001",
    }
    original = assembler.explain_local_noop_runner_result_build
    calls = []
    p2d35_results = []

    def spy(**kwargs):
        calls.append(dict(kwargs))
        built = original(**kwargs)
        p2d35_results.append(built)
        return built

    assembler.explain_local_noop_runner_result_build = spy
    try:
        result = assembler.assemble_local_noop_final_runner_result(**inputs)
    finally:
        assembler.explain_local_noop_runner_result_build = original

    expected = (
        "contract-source",
        "shared-source",
        "shared-source",
        "candidate-source",
    )
    assert result["final_result_object_assembled"] is True
    assert calls[0]["source_of_truth"] == expected
    assert result["source"]["source_of_truth"] == expected
    assert result["local_noop_runner_result"]["source_of_truth"] == expected
    assert calls[0]["source_of_truth"] is not contract_source
    assert calls[0]["source_of_truth"] is not candidate_source
    assert result["source"]["source_of_truth"] is not p2d35_results[0]["source"]["source_of_truth"]
    assert result["local_noop_runner_result"]["source_of_truth"] is not p2d35_results[0]["local_noop_runner_result"]["source_of_truth"]
    assert result["source"]["source_of_truth"] is not result["local_noop_runner_result"]["source_of_truth"]


def test_p2d35_invalid_output_coherence_and_exception_are_safe():
    original = assembler.explain_local_noop_runner_result_build

    def non_dict(**kwargs):
        return "malformed secret"

    def wrong_root_keys(**kwargs):
        built = original(**kwargs)
        built.pop("invariant_refs")
        return built

    def malformed_source(**kwargs):
        built = original(**kwargs)
        built["source"] = {}
        return built

    def malformed_nested_result(**kwargs):
        built = original(**kwargs)
        built["local_noop_runner_result"] = {}
        return built

    def malformed_runner_evidence_item(**kwargs):
        built = original(**kwargs)
        built["local_noop_runner_result"]["runner_evidence_items"] = ({},)
        return built

    def incoherent_result(**kwargs):
        built = original(**kwargs)
        built["local_noop_runner_result"]["created_at"] = "wrong-created-at"
        return built

    def raises_once(**kwargs):
        raise RuntimeError("hidden builder exception")

    cases = (
        ("non_dict", non_dict, "P2D35_BUILD_RESULT_INVALID"),
        ("wrong_root_keys", wrong_root_keys, "P2D35_BUILD_RESULT_INVALID"),
        ("malformed_source", malformed_source, "P2D35_BUILD_RESULT_INVALID"),
        ("malformed_nested_result", malformed_nested_result, "P2D35_BUILD_RESULT_INVALID"),
        ("malformed_runner_evidence_item", malformed_runner_evidence_item, "P2D35_BUILD_RESULT_INVALID"),
        ("incoherent_result", incoherent_result, "P2D35_OUTPUT_COHERENCE_MISMATCH"),
        ("exception", raises_once, "P2D35_BUILD_RESULT_INVALID"),
    )
    for name, stub, reason_code in cases:
        calls = []

        def spy(**kwargs):
            calls.append(dict(kwargs))
            return stub(**kwargs)

        assembler.explain_local_noop_runner_result_build = spy
        try:
            result = assembler.assemble_local_noop_final_runner_result(**_inputs())
        finally:
            assembler.explain_local_noop_runner_result_build = original
        _assert_blocked(result)
        assert result["reason_code"] == reason_code, name
        assert calls and len(calls) == 1, name
        assert "caller secret" not in str(result), name
        assert "malformed secret" not in str(result), name
        assert "hidden builder exception" not in str(result), name


def test_success_output_shape_and_semantic_boundaries_are_exact():
    result = _assemble()
    assert result["final_result_object_assembled"] is True
    assert tuple(result.keys()) == RESULT_KEYS
    assert tuple(result["source"].keys()) == SOURCE_KEYS
    assert tuple(result["local_noop_runner_result"].keys()) == FINAL_RESULT_KEYS
    assert result["source"]["public_url"] is None
    assert result["source"]["public_url_created"] is False
    assert result["local_noop_runner_result"]["public_url"] is None
    assert result["local_noop_runner_result"]["public_url_created"] is False
    payload_keys = _payload_keys(result)
    for forbidden in (
        "completed", "executed", "realized", "terminal_reached",
        "noop_completed", "completion_achieved", "transitioned",
        "runner_executed", "ledger_written", "published", "notified",
        "publish_allowed", "quality_pass", "gate_pass", "eval_pass",
        "audit_pass",
    ):
        assert forbidden not in payload_keys
    terminal_values = (
        result["source"]["runner_terminal_status"],
        result["local_noop_runner_result"]["runner_terminal_status"],
    )
    assert terminal_values == ("NOOP_COMPLETED", "NOOP_COMPLETED")
    for key, value in result["source"].items():
        if key != "runner_terminal_status":
            assert value != "NOOP_COMPLETED"
    for key, value in result["local_noop_runner_result"].items():
        if key != "runner_terminal_status":
            assert value != "NOOP_COMPLETED"
