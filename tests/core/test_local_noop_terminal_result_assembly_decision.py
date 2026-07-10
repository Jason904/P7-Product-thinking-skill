"""Tests for the pure local noop terminal-result assembly decision."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import (  # noqa: E402
    local_noop_terminal_result_assembly_decision as decision,
)


RESULT_KEYS = (
    "decision_created",
    "reason_code",
    "reason",
    "source",
    "local_noop_terminal_result_assembly_decision",
    "decision_violations",
    "missing_or_invalid_fields",
    "decision_validation_violations",
    "invariant_refs",
)

OUTPUT_SOURCE_KEYS = (
    "p2d42_consumed",
    "p2d42_reason_code",
    "local_noop_runner_result_candidate_id",
    "local_noop_runner_consumption_receipt_kind",
    "mode",
    "candidate_runner_terminal_status",
    "public_url",
    "public_url_created",
    "source_of_truth",
)

DECISION_KEYS = (
    "decision_kind",
    "decision_value",
    "decision_scope",
    "run_id",
    "local_noop_runner_result_candidate_id",
    "local_noop_runner_consumption_receipt_kind",
    "mode",
    "public_url",
    "public_url_created",
)

ROOT_KEYS = (
    "consumed",
    "reason_code",
    "reason",
    "source",
    "normalized_local_noop_runner_result_candidate",
    "local_noop_runner_consumption_receipt",
    "consumption_violations",
    "missing_or_invalid_fields",
    "result_candidate_evidence_item_violations",
    "invariant_refs",
)

SOURCE_KEYS = (
    "p2d41_assembled",
    "p2d41_reason_code",
    "local_noop_runner_result_candidate_id",
    "candidate_kind",
    "mode",
    "public_url",
    "public_url_created",
    "source_of_truth",
)

CANDIDATE_KEYS = (
    "run_id",
    "local_noop_runner_result_candidate_id",
    "candidate_kind",
    "mode",
    "runner_terminal_status",
    "local_noop_runner_readiness_ref",
    "local_noop_runner_readiness_id",
    "local_noop_runner_readiness_buildable_marker",
    "public_url",
    "public_url_created",
    "result_candidate_evidence_items",
    "required_result_candidate_evidence_ids",
    "missing_result_candidate_evidence_ids",
    "blocking_result_candidate_evidence_ids",
    "created_at",
    "timestamp_policy",
    "source_of_truth",
    "notes",
)

RECEIPT_KEYS = (
    "receipt_kind",
    "consumption_scope",
    "run_id",
    "local_noop_runner_result_candidate_id",
    "candidate_kind",
    "mode",
    "public_url",
    "public_url_created",
)

EVIDENCE_ITEM_KEYS = (
    "result_candidate_evidence_id",
    "result_candidate_evidence_role",
    "artifact_ref",
    "artifact_kind",
    "evidence_status",
    "producer_ref",
    "evidence_refs",
    "notes",
)

VALIDATION_VIOLATION_KEYS = (
    "reason_code",
    "field",
)

REASON_CODES = (
    "LOCAL_NOOP_TERMINAL_RESULT_ASSEMBLY_DECISION_CREATED",
    "P2D42_CONSUMER_RESULT_NOT_DICT",
    "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
    "P2D42_CONSUMER_RESULT_KEYS_INVALID",
    "P2D42_CONSUMED_MARKER_NOT_TRUE",
    "P2D42_CONSUMPTION_REASON_CODE_INVALID",
    "P2D42_CONSUMPTION_REASON_MISSING",
    "P2D42_CONSUMPTION_VIOLATIONS_NOT_EMPTY",
    "P2D42_MISSING_OR_INVALID_FIELDS_NOT_EMPTY",
    "P2D42_EVIDENCE_ITEM_VIOLATIONS_NOT_EMPTY",
    "P2D42_INVARIANT_REFS_INVALID",
    "P2D42_REQUIRED_INVARIANT_REF_MISSING",
    "P2D42_SOURCE_NOT_DICT",
    "P2D42_SOURCE_KEYS_INVALID",
    "P2D42_SOURCE_FIELD_INVALID",
    "P2D42_NORMALIZED_CANDIDATE_NOT_DICT",
    "P2D42_NORMALIZED_CANDIDATE_KEYS_INVALID",
    "P2D42_NORMALIZED_CANDIDATE_FIELD_INVALID",
    "PASS_PUBLISHED_FORBIDDEN",
    "MODE_NOT_NOOP",
    "RUNNER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
    "PUBLIC_URL_NOT_NULL",
    "PUBLIC_URL_CREATED_NOT_FALSE",
    "P2D42_EVIDENCE_ITEM_NOT_DICT",
    "P2D42_EVIDENCE_ITEM_KEYS_INVALID",
    "P2D42_EVIDENCE_ITEM_FIELD_INVALID",
    "P2D42_EVIDENCE_RELATIONSHIP_INVALID",
    "P2D42_RECEIPT_NOT_DICT",
    "P2D42_RECEIPT_KEYS_INVALID",
    "P2D42_RECEIPT_KIND_INVALID",
    "P2D42_RECEIPT_SCOPE_INVALID",
    "P2D42_RECEIPT_FIELD_INVALID",
    "P2D42_SOURCE_CANDIDATE_RECEIPT_MISMATCH",
)

REASON_PRIORITY = (
    "P2D42_CONSUMER_RESULT_NOT_DICT",
    "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT",
    "P2D42_CONSUMER_RESULT_KEYS_INVALID",
    "P2D42_CONSUMED_MARKER_NOT_TRUE",
    "P2D42_CONSUMPTION_REASON_CODE_INVALID",
    "P2D42_CONSUMPTION_REASON_MISSING",
    "P2D42_CONSUMPTION_VIOLATIONS_NOT_EMPTY",
    "P2D42_MISSING_OR_INVALID_FIELDS_NOT_EMPTY",
    "P2D42_EVIDENCE_ITEM_VIOLATIONS_NOT_EMPTY",
    "P2D42_INVARIANT_REFS_INVALID",
    "P2D42_REQUIRED_INVARIANT_REF_MISSING",
    "P2D42_SOURCE_NOT_DICT",
    "P2D42_SOURCE_KEYS_INVALID",
    "P2D42_NORMALIZED_CANDIDATE_NOT_DICT",
    "P2D42_NORMALIZED_CANDIDATE_KEYS_INVALID",
    "P2D42_RECEIPT_NOT_DICT",
    "P2D42_RECEIPT_KEYS_INVALID",
    "PASS_PUBLISHED_FORBIDDEN",
    "MODE_NOT_NOOP",
    "RUNNER_TERMINAL_STATUS_NOT_NOOP_COMPLETED",
    "PUBLIC_URL_NOT_NULL",
    "PUBLIC_URL_CREATED_NOT_FALSE",
    "P2D42_SOURCE_FIELD_INVALID",
    "P2D42_NORMALIZED_CANDIDATE_FIELD_INVALID",
    "P2D42_EVIDENCE_ITEM_NOT_DICT",
    "P2D42_EVIDENCE_ITEM_KEYS_INVALID",
    "P2D42_EVIDENCE_ITEM_FIELD_INVALID",
    "P2D42_EVIDENCE_RELATIONSHIP_INVALID",
    "P2D42_RECEIPT_KIND_INVALID",
    "P2D42_RECEIPT_SCOPE_INVALID",
    "P2D42_RECEIPT_FIELD_INVALID",
    "P2D42_SOURCE_CANDIDATE_RECEIPT_MISMATCH",
    "LOCAL_NOOP_TERMINAL_RESULT_ASSEMBLY_DECISION_CREATED",
)

REQUIRED_P2D42_INVARIANT_REFS = (
    "local_noop_runner_result_candidate_consumer_only",
    "consumer_pure_in_memory_only",
    "consumer_accepts_full_p2d41_assembly",
    "consumer_rejects_nested_candidate_bypass",
    "full_p2d41_wrapper_requires_assembled_true",
    "full_p2d41_wrapper_requires_empty_violations",
    "consume_means_validate_and_normalize_only",
    "consumed_true_means_accepted_and_normalized_in_memory_only",
    "source_candidate_lockins_must_match",
    "unknown_keys_block_and_are_suppressed",
    "forbidden_fields_block_and_are_suppressed",
    "normalized_candidate_returned_only_when_consumed",
    "consumption_receipt_returned_only_when_consumed",
    "consumption_receipt_not_runner_result",
    "consumed_not_noop_completion_execution",
    "consumed_not_state_transition",
    "consumed_not_runner_result_created",
    "consumed_not_noop_completed_achievement",
    "no_sibling_module_import",
    "no_prior_builder_or_policy_call",
    "no_file_read",
    "no_artifact_read",
    "no_run_ledger_yaml_read",
    "no_run_ledger_yaml_write",
    "no_publish",
    "no_notification",
    "mode_noop_required",
    "public_url_must_be_null",
    "public_url_created_must_be_false",
    "normalized_runner_terminal_status_must_be_noop_completed",
    "noop_completed_is_declarative_input_only",
    "pass_published_forbidden",
    "evidence_status_opaque_except_pass_published",
    "failed_evidence_status_may_be_consumed",
    "known_blocking_evidence_ids_are_evidence_only",
    "unknown_blocking_evidence_ids_block_consumption",
    "no_quality_pass_no_public_url",
)

INVARIANT_REFS = (
    "local_noop_terminal_result_assembly_decision_only",
    "decision_pure_in_memory_only",
    "decision_accepts_full_p2d42_consumer_result",
    "decision_rejects_normalized_candidate_bypass",
    "full_p2d42_wrapper_requires_consumed_true",
    "full_p2d42_wrapper_requires_exact_success_reason",
    "full_p2d42_wrapper_requires_empty_violations",
    "normalized_candidate_revalidated_not_trusted",
    "consumption_receipt_revalidated_not_trusted",
    "source_candidate_receipt_coherence_required",
    "exact_type_aware_coherence",
    "caller_input_not_mutated",
    "output_contains_refs_and_decision_only",
    "normalized_candidate_not_returned",
    "consumption_receipt_not_returned",
    "decision_created_means_declarative_decision_only",
    "decision_value_means_future_separately_authorized_assembly_only",
    "eligibility_not_execution_authorization",
    "candidate_runner_terminal_status_is_metadata_only",
    "noop_completed_not_top_level_outcome",
    "decision_not_runner_result",
    "decision_not_runner_execution",
    "decision_not_runtime_execution",
    "decision_not_adapter_execution",
    "decision_not_scheduler_execution",
    "decision_not_cli_or_manual_execution",
    "decision_not_argument_parsing",
    "decision_not_command_or_subprocess_execution",
    "decision_not_dry_run_or_e2e_execution",
    "decision_not_noop_completion_execution",
    "decision_not_state_transition",
    "decision_not_runner_result_created",
    "decision_not_noop_completed_achievement",
    "decision_not_ledger_write_authorization",
    "decision_not_quality_pass",
    "decision_not_gate_pass",
    "decision_not_publish_allowed",
    "decision_not_pass_published",
    "decision_not_public_url_created",
    "decision_not_notification_sent",
    "evidence_status_opaque_except_pass_published",
    "failed_evidence_status_may_be_assembly_eligible",
    "known_blocking_evidence_ids_are_evidence_only",
    "unknown_blocking_evidence_ids_block_decision",
    "unknown_keys_block_and_are_suppressed",
    "forbidden_fields_block_and_are_suppressed",
    "recursive_key_scan_does_not_scan_string_values",
    "no_sibling_module_import",
    "no_prior_builder_or_policy_call",
    "no_file_or_artifact_io",
    "no_config_env_credentials_read",
    "no_web_github_rss_notion_access",
    "no_llm_summary_or_judge",
    "no_run_ledger_yaml_read_or_write",
    "no_publish_or_notification",
    "mode_noop_required",
    "public_url_must_be_null",
    "public_url_created_must_be_false",
    "pass_published_forbidden",
    "no_quality_pass_no_public_url",
)

BLOCKED_SOURCE = {
    "p2d42_consumed": False,
    "p2d42_reason_code": "",
    "local_noop_runner_result_candidate_id": "",
    "local_noop_runner_consumption_receipt_kind": "",
    "mode": "",
    "candidate_runner_terminal_status": "",
    "public_url": None,
    "public_url_created": False,
    "source_of_truth": (),
}

FORBIDDEN_POSITIVE_FIELDS = (
    "eligible",
    "terminal_realization_eligible",
    "terminal_result_assembly_eligible",
    "executed",
    "completed",
    "realized",
    "terminal_reached",
    "noop_completed",
    "completion_achieved",
    "transitioned",
    "runner_result_created",
    "final_result_created",
    "ledger_written",
    "published",
    "notified",
    "quality_pass",
    "validator_pass",
    "rubric_pass",
    "audit_pass",
    "eval_pass",
    "gate_pass",
    "publish_allowed",
    "pass_published",
)

FORBIDDEN_DEPENDENCY_NAMES = (
    "argparse",
    "click",
    "typer",
    "subprocess",
    "os",
    "datetime",
    "hashlib",
    "logging",
    "requests",
    "httpx",
    "urllib",
    "feedparser",
    "local_noop_runner_result_candidate_consumer",
    "local_noop_runner_result_assembler",
    "local_noop_runner_result_builder",
    "local_noop_runner_readiness_builder",
    "local_noop_runner_envelope_builder",
    "local_noop_runner_skeleton_builder",
    "local_noop_cli_contract_builder",
    "noop_completion_policy",
    "transition_guard",
    "gate_decision_mapper",
)

_DEFAULT_RESULT = object()


def _evidence_item(**overrides):
    values = {
        "result_candidate_evidence_id": "result-candidate-evidence-001",
        "result_candidate_evidence_role": "local_noop_runner_readiness",
        "artifact_ref": "local-noop-runner-readiness-001",
        "artifact_kind": "local_noop_runner_readiness",
        "evidence_status": "passed",
        "producer_ref": "caller-supplied-result-candidate",
        "evidence_refs": ("local-noop-runner-readiness-001#noop",),
        "notes": ("caller-supplied-evidence-only",),
    }
    values.update(overrides)
    return values


def _candidate(**overrides):
    values = {
        "run_id": "run-001",
        "local_noop_runner_result_candidate_id": (
            "local-noop-runner-result-candidate-001"
        ),
        "candidate_kind": "local_noop_runner_result_candidate",
        "mode": "noop",
        "runner_terminal_status": "NOOP_COMPLETED",
        "local_noop_runner_readiness_ref": "local-noop-runner-readiness-001",
        "local_noop_runner_readiness_id": (
            "local-noop-runner-readiness-id-001"
        ),
        "local_noop_runner_readiness_buildable_marker": True,
        "public_url": None,
        "public_url_created": False,
        "result_candidate_evidence_items": (_evidence_item(),),
        "required_result_candidate_evidence_ids": (
            "result-candidate-evidence-001",
        ),
        "missing_result_candidate_evidence_ids": (),
        "blocking_result_candidate_evidence_ids": (),
        "created_at": "caller-supplied-created-at",
        "timestamp_policy": "caller_supplied_no_datetime_parsing",
        "source_of_truth": ("p2d-42",),
        "notes": ("structured-only",),
    }
    values.update(overrides)
    return values


def _source(candidate):
    return {
        "p2d41_assembled": True,
        "p2d41_reason_code": (
            "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_ASSEMBLED"
        ),
        "local_noop_runner_result_candidate_id": candidate[
            "local_noop_runner_result_candidate_id"
        ],
        "candidate_kind": candidate["candidate_kind"],
        "mode": candidate["mode"],
        "public_url": candidate["public_url"],
        "public_url_created": candidate["public_url_created"],
        "source_of_truth": candidate["source_of_truth"],
    }


def _receipt(candidate):
    return {
        "receipt_kind": (
            "local_noop_runner_result_candidate_consumption_receipt"
        ),
        "consumption_scope": (
            "pure_in_memory_validation_and_normalization_only"
        ),
        "run_id": candidate["run_id"],
        "local_noop_runner_result_candidate_id": candidate[
            "local_noop_runner_result_candidate_id"
        ],
        "candidate_kind": candidate["candidate_kind"],
        "mode": candidate["mode"],
        "public_url": candidate["public_url"],
        "public_url_created": candidate["public_url_created"],
    }


def _valid_result():
    candidate = _candidate()
    return {
        "consumed": True,
        "reason_code": (
            "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_CONSUMED_IN_MEMORY"
        ),
        "reason": "The complete P2D-41 candidate was consumed in memory.",
        "source": _source(candidate),
        "normalized_local_noop_runner_result_candidate": candidate,
        "local_noop_runner_consumption_receipt": _receipt(candidate),
        "consumption_violations": (),
        "missing_or_invalid_fields": (),
        "result_candidate_evidence_item_violations": (),
        "invariant_refs": REQUIRED_P2D42_INVARIANT_REFS,
    }


def _decide(value=_DEFAULT_RESULT):
    if value is _DEFAULT_RESULT:
        value = _valid_result()
    return decision.decide_local_noop_terminal_result_assembly(
        local_noop_runner_result_candidate_consumption=value,
    )


def _assert_blocked(result):
    assert result["decision_created"] is False
    assert tuple(result.keys()) == RESULT_KEYS
    assert result["decision_violations"] != ()
    assert result["source"] == BLOCKED_SOURCE
    assert result["local_noop_terminal_result_assembly_decision"] == {}
    assert result["invariant_refs"] == INVARIANT_REFS
    for violation in result["decision_validation_violations"]:
        assert tuple(violation.keys()) == VALIDATION_VIOLATION_KEYS


def _payload_keys(value, skip_invariants=True):
    keys = ()
    if isinstance(value, dict):
        for key, nested in value.items():
            keys = keys + (key,)
            if not (skip_invariants and key == "invariant_refs"):
                keys = keys + _payload_keys(nested, skip_invariants)
    elif isinstance(value, tuple) or isinstance(value, list):
        for nested in value:
            keys = keys + _payload_keys(nested, skip_invariants)
    return keys


def _scalar_strings(value, skip_invariants=True):
    strings = ()
    if isinstance(value, dict):
        for key, nested in value.items():
            if skip_invariants and key == "invariant_refs":
                continue
            strings = strings + _scalar_strings(nested, skip_invariants)
    elif isinstance(value, tuple) or isinstance(value, list):
        for nested in value:
            strings = strings + _scalar_strings(nested, skip_invariants)
    elif isinstance(value, str):
        strings = strings + (value,)
    return strings


def _module_code_names():
    names = ()
    for value in decision.__dict__.values():
        code = getattr(value, "__code__", None)
        if code is not None:
            names = names + tuple(code.co_names)
    return names


def test_reason_code_constants_are_exact_and_stably_prioritized():
    assert decision.REASON_CODES == REASON_CODES
    assert (
        decision.LOCAL_NOOP_TERMINAL_RESULT_ASSEMBLY_DECISION_REASON_CODES
        == REASON_CODES
    )
    assert decision.REASON_PRIORITY == REASON_PRIORITY


def test_valid_complete_p2d42_result_creates_exact_decision():
    result = _decide()

    assert result["decision_created"] is True
    assert result["reason_code"] == (
        "LOCAL_NOOP_TERMINAL_RESULT_ASSEMBLY_DECISION_CREATED"
    )
    assert result["decision_violations"] == ()
    assert result["missing_or_invalid_fields"] == ()
    assert result["decision_validation_violations"] == ()
    assert tuple(result.keys()) == RESULT_KEYS


def test_success_source_is_exact_allowlisted_projection():
    result = _decide()
    source = result["source"]

    assert tuple(source.keys()) == OUTPUT_SOURCE_KEYS
    assert source == {
        "p2d42_consumed": True,
        "p2d42_reason_code": (
            "LOCAL_NOOP_RUNNER_RESULT_CANDIDATE_CONSUMED_IN_MEMORY"
        ),
        "local_noop_runner_result_candidate_id": (
            "local-noop-runner-result-candidate-001"
        ),
        "local_noop_runner_consumption_receipt_kind": (
            "local_noop_runner_result_candidate_consumption_receipt"
        ),
        "mode": "noop",
        "candidate_runner_terminal_status": "NOOP_COMPLETED",
        "public_url": None,
        "public_url_created": False,
        "source_of_truth": ("p2d-42",),
    }


def test_success_decision_shape_and_semantics_are_exact():
    envelope = _decide()["local_noop_terminal_result_assembly_decision"]

    assert tuple(envelope.keys()) == DECISION_KEYS
    assert envelope == {
        "decision_kind": "local_noop_terminal_result_assembly_decision",
        "decision_value": "NOOP_TERMINAL_RESULT_ASSEMBLY_ELIGIBLE",
        "decision_scope": (
            "future_separately_authorized_pure_terminal_result_assembly_only"
        ),
        "run_id": "run-001",
        "local_noop_runner_result_candidate_id": (
            "local-noop-runner-result-candidate-001"
        ),
        "local_noop_runner_consumption_receipt_kind": (
            "local_noop_runner_result_candidate_consumption_receipt"
        ),
        "mode": "noop",
        "public_url": None,
        "public_url_created": False,
    }


def test_normalized_candidate_only_bypass_blocks_with_root_reason():
    candidate = _valid_result()[
        "normalized_local_noop_runner_result_candidate"
    ]
    result = _decide(candidate)

    _assert_blocked(result)
    assert result["reason_code"] == "P2D42_CONSUMER_RESULT_KEYS_INVALID"
    assert result["missing_or_invalid_fields"][0] == (
        "p2d42_consumer_result.keys"
    )


def test_non_dict_input_blocks_with_fixed_source():
    for value in (None, (), [], "consumer-result"):
        result = _decide(value)
        _assert_blocked(result)
        assert result["reason_code"] == "P2D42_CONSUMER_RESULT_NOT_DICT"


def test_root_missing_and_extra_keys_block_without_echo():
    missing = _valid_result()
    missing.pop("reason")
    extra = _valid_result()
    extra["unknown-root-secret"] = "root-secret-value"

    for value in (missing, extra):
        result = _decide(value)
        _assert_blocked(result)
        assert "P2D42_CONSUMER_RESULT_KEYS_INVALID" in result[
            "decision_violations"
        ]
        assert "p2d42_consumer_result.keys" in result[
            "missing_or_invalid_fields"
        ]
        assert "unknown-root-secret" not in _scalar_strings(result)
        assert "root-secret-value" not in _scalar_strings(result)


def test_nested_mapping_exact_shapes_are_enforced():
    cases = ()
    for container_key, reason_code, field in (
        ("source", "P2D42_SOURCE_KEYS_INVALID", "source"),
        (
            "normalized_local_noop_runner_result_candidate",
            "P2D42_NORMALIZED_CANDIDATE_KEYS_INVALID",
            "candidate",
        ),
        (
            "local_noop_runner_consumption_receipt",
            "P2D42_RECEIPT_KEYS_INVALID",
            "receipt",
        ),
    ):
        missing = _valid_result()
        mapping = missing[container_key]
        mapping.pop(tuple(mapping.keys())[0])
        cases = cases + ((missing, reason_code),)

        extra = _valid_result()
        extra[container_key][f"unknown_{field}"] = "not-echoed"
        cases = cases + ((extra, reason_code),)

    for value, reason_code in cases:
        result = _decide(value)
        _assert_blocked(result)
        assert reason_code in result["decision_violations"]
        assert "not-echoed" not in _scalar_strings(result)


def test_evidence_item_exact_shape_is_enforced():
    for operation in ("missing", "extra"):
        value = _valid_result()
        item = value[
            "normalized_local_noop_runner_result_candidate"
        ]["result_candidate_evidence_items"][0]
        if operation == "missing":
            item.pop("artifact_kind")
        else:
            item["unknown_evidence_key"] = "evidence-secret"
        result = _decide(value)
        _assert_blocked(result)
        assert "P2D42_EVIDENCE_ITEM_KEYS_INVALID" in result[
            "decision_violations"
        ]
        assert (
            "p2d42_consumer_result.normalized_candidate."
            "evidence_items[0].keys"
        ) in result["missing_or_invalid_fields"]
        assert "evidence-secret" not in _scalar_strings(result)


def test_consumed_marker_requires_exact_true():
    for consumed in (False, 1, 0, None, "true"):
        value = _valid_result()
        value["consumed"] = consumed
        result = _decide(value)
        _assert_blocked(result)
        assert "P2D42_CONSUMED_MARKER_NOT_TRUE" in result[
            "decision_violations"
        ]


def test_upstream_reason_code_and_nonblank_reason_are_required():
    invalid_code = _valid_result()
    invalid_code["reason_code"] = "CALLER_REASON"
    blank_reason = _valid_result()
    blank_reason["reason"] = "  "

    result = _decide(invalid_code)
    assert "P2D42_CONSUMPTION_REASON_CODE_INVALID" in result[
        "decision_violations"
    ]
    result = _decide(blank_reason)
    assert "P2D42_CONSUMPTION_REASON_MISSING" in result[
        "decision_violations"
    ]


def test_upstream_violation_tuples_must_be_empty():
    fields = (
        ("consumption_violations", "P2D42_CONSUMPTION_VIOLATIONS_NOT_EMPTY"),
        (
            "missing_or_invalid_fields",
            "P2D42_MISSING_OR_INVALID_FIELDS_NOT_EMPTY",
        ),
        (
            "result_candidate_evidence_item_violations",
            "P2D42_EVIDENCE_ITEM_VIOLATIONS_NOT_EMPTY",
        ),
    )
    for field, reason_code in fields:
        value = _valid_result()
        value[field] = ("caller-violation",)
        result = _decide(value)
        _assert_blocked(result)
        assert reason_code in result["decision_violations"]
        assert "caller-violation" not in _scalar_strings(result)


def test_required_upstream_invariant_refs_are_enforced():
    invalid_values = ((), [], ("",), (1,))
    for invariant_refs in invalid_values:
        value = _valid_result()
        value["invariant_refs"] = invariant_refs
        result = _decide(value)
        _assert_blocked(result)
        assert "P2D42_INVARIANT_REFS_INVALID" in result[
            "decision_violations"
        ]

    for required_ref in REQUIRED_P2D42_INVARIANT_REFS:
        value = _valid_result()
        value["invariant_refs"] = tuple(
            ref for ref in REQUIRED_P2D42_INVARIANT_REFS
            if ref != required_ref
        )
        result = _decide(value)
        _assert_blocked(result)
        assert "P2D42_REQUIRED_INVARIANT_REF_MISSING" in result[
            "decision_violations"
        ]


def test_p2d42_source_success_projection_is_revalidated():
    changes = (
        ("p2d41_assembled", 1),
        ("p2d41_reason_code", "WRONG"),
        ("local_noop_runner_result_candidate_id", ""),
        ("candidate_kind", "wrong"),
        ("source_of_truth", ()),
    )
    for field, invalid_value in changes:
        value = _valid_result()
        value["source"][field] = invalid_value
        result = _decide(value)
        _assert_blocked(result)
        assert "P2D42_SOURCE_FIELD_INVALID" in result[
            "decision_violations"
        ]


def test_required_candidate_scalar_fields_are_revalidated():
    fields = (
        "run_id",
        "local_noop_runner_result_candidate_id",
        "local_noop_runner_readiness_ref",
        "local_noop_runner_readiness_id",
        "created_at",
        "timestamp_policy",
    )
    for field in fields:
        value = _valid_result()
        value["normalized_local_noop_runner_result_candidate"][field] = " "
        result = _decide(value)
        _assert_blocked(result)
        assert "P2D42_NORMALIZED_CANDIDATE_FIELD_INVALID" in result[
            "decision_violations"
        ]


def test_candidate_kind_readiness_source_and_notes_are_revalidated():
    changes = (
        ("candidate_kind", "wrong"),
        ("local_noop_runner_readiness_buildable_marker", 1),
        ("source_of_truth", ()),
        ("notes", []),
    )
    for field, invalid_value in changes:
        value = _valid_result()
        value["normalized_local_noop_runner_result_candidate"][field] = (
            invalid_value
        )
        result = _decide(value)
        _assert_blocked(result)
        assert "P2D42_NORMALIZED_CANDIDATE_FIELD_INVALID" in result[
            "decision_violations"
        ]


def test_receipt_kind_scope_and_fields_are_revalidated():
    changes = (
        ("receipt_kind", "wrong"),
        ("consumption_scope", "wrong"),
        ("run_id", ""),
        ("local_noop_runner_result_candidate_id", ""),
        ("candidate_kind", "wrong"),
    )
    expected = (
        "P2D42_RECEIPT_KIND_INVALID",
        "P2D42_RECEIPT_SCOPE_INVALID",
        "P2D42_RECEIPT_FIELD_INVALID",
        "P2D42_RECEIPT_FIELD_INVALID",
        "P2D42_RECEIPT_FIELD_INVALID",
    )
    for index, change in enumerate(changes):
        field, invalid_value = change
        value = _valid_result()
        value["local_noop_runner_consumption_receipt"][field] = invalid_value
        result = _decide(value)
        _assert_blocked(result)
        assert expected[index] in result["decision_violations"]


def test_exact_coherence_matrix_constants_are_locked():
    assert decision._SOURCE_CANDIDATE_COHERENCE_FIELDS == (
        "local_noop_runner_result_candidate_id",
        "candidate_kind",
        "mode",
        "public_url",
        "public_url_created",
        "source_of_truth",
    )
    assert decision._CANDIDATE_RECEIPT_COHERENCE_FIELDS == (
        "run_id",
        "local_noop_runner_result_candidate_id",
        "candidate_kind",
        "mode",
        "public_url",
        "public_url_created",
    )
    assert decision._SOURCE_RECEIPT_COHERENCE_FIELDS == (
        "local_noop_runner_result_candidate_id",
        "candidate_kind",
        "mode",
        "public_url",
        "public_url_created",
    )


def test_every_source_candidate_coherence_field_is_compared():
    for field in decision._SOURCE_CANDIDATE_COHERENCE_FIELDS:
        value = _valid_result()
        value["source"][field] = "source-only-mismatch"
        result = _decide(value)
        _assert_blocked(result)
        assert "P2D42_SOURCE_CANDIDATE_RECEIPT_MISMATCH" in result[
            "decision_violations"
        ]


def test_every_candidate_receipt_coherence_field_is_compared():
    for field in decision._CANDIDATE_RECEIPT_COHERENCE_FIELDS:
        value = _valid_result()
        value["local_noop_runner_consumption_receipt"][field] = (
            "receipt-only-mismatch"
        )
        result = _decide(value)
        _assert_blocked(result)
        assert "P2D42_SOURCE_CANDIDATE_RECEIPT_MISMATCH" in result[
            "decision_violations"
        ]


def test_source_receipt_coherence_fields_are_compared_directly():
    for field in decision._SOURCE_RECEIPT_COHERENCE_FIELDS:
        value = _valid_result()
        value["source"][field] = "shared-mismatch"
        value[
            "normalized_local_noop_runner_result_candidate"
        ][field] = "shared-mismatch"
        result = _decide(value)
        _assert_blocked(result)
        assert "P2D42_SOURCE_CANDIDATE_RECEIPT_MISMATCH" in result[
            "decision_violations"
        ]


def test_nonexistent_cross_container_fields_are_not_compared():
    assert "run_id" not in decision._SOURCE_CANDIDATE_COHERENCE_FIELDS
    assert "run_id" not in decision._SOURCE_RECEIPT_COHERENCE_FIELDS
    assert "source_of_truth" not in (
        decision._CANDIDATE_RECEIPT_COHERENCE_FIELDS
    )
    assert "runner_terminal_status" not in (
        decision._SOURCE_CANDIDATE_COHERENCE_FIELDS
        + decision._CANDIDATE_RECEIPT_COHERENCE_FIELDS
        + decision._SOURCE_RECEIPT_COHERENCE_FIELDS
    )
    assert "receipt_kind" not in decision._SOURCE_CANDIDATE_COHERENCE_FIELDS


def test_coherence_comparison_is_exactly_type_aware():
    assert decision._values_match_exactly(True, True) is True
    assert decision._values_match_exactly(False, False) is True
    assert decision._values_match_exactly(True, 1) is False
    assert decision._values_match_exactly(False, 0) is False

    value = _valid_result()
    value["source"]["public_url_created"] = 0
    value[
        "normalized_local_noop_runner_result_candidate"
    ]["public_url_created"] = 0
    value["local_noop_runner_consumption_receipt"]["public_url_created"] = 0
    result = _decide(value)
    _assert_blocked(result)
    assert "PUBLIC_URL_CREATED_NOT_FALSE" in result["decision_violations"]


def test_noop_completed_is_candidate_metadata_only():
    result = _decide()
    strings = _scalar_strings(result)
    keys = _payload_keys(result)

    assert strings.count("NOOP_COMPLETED") == 1
    assert result["source"]["candidate_runner_terminal_status"] == (
        "NOOP_COMPLETED"
    )
    assert result["reason_code"] != "NOOP_COMPLETED"
    assert "runner_terminal_status" not in result
    for forbidden_field in FORBIDDEN_POSITIVE_FIELDS:
        assert forbidden_field not in keys


def test_failed_evidence_and_known_blocker_remain_structurally_acceptable():
    value = _valid_result()
    candidate = value["normalized_local_noop_runner_result_candidate"]
    candidate["result_candidate_evidence_items"][0][
        "evidence_status"
    ] = "failed"
    candidate["blocking_result_candidate_evidence_ids"] = (
        "result-candidate-evidence-001",
    )

    result = _decide(value)
    assert result["decision_created"] is True
    assert result["decision_violations"] == ()


def test_unknown_blank_and_non_tuple_blocking_ids_block():
    for blocking_ids in (("unknown",), ("",), ["result-candidate-evidence-001"]):
        value = _valid_result()
        value["normalized_local_noop_runner_result_candidate"][
            "blocking_result_candidate_evidence_ids"
        ] = blocking_ids
        result = _decide(value)
        _assert_blocked(result)
        assert "P2D42_EVIDENCE_RELATIONSHIP_INVALID" in result[
            "decision_violations"
        ]


def test_evidence_id_relationships_are_bidirectional_and_unique():
    values = ()
    duplicate = _valid_result()
    duplicate["normalized_local_noop_runner_result_candidate"][
        "result_candidate_evidence_items"
    ] = (_evidence_item(), _evidence_item())
    values = values + (duplicate,)

    unrequired = _valid_result()
    unrequired["normalized_local_noop_runner_result_candidate"][
        "required_result_candidate_evidence_ids"
    ] = ("another-id",)
    values = values + (unrequired,)

    missing = _valid_result()
    missing["normalized_local_noop_runner_result_candidate"][
        "missing_result_candidate_evidence_ids"
    ] = ("result-candidate-evidence-001",)
    values = values + (missing,)

    for value in values:
        result = _decide(value)
        _assert_blocked(result)
        assert "P2D42_EVIDENCE_RELATIONSHIP_INVALID" in result[
            "decision_violations"
        ]


def test_pass_published_runner_status_blocks_and_is_suppressed():
    value = _valid_result()
    value["normalized_local_noop_runner_result_candidate"][
        "runner_terminal_status"
    ] = "PASS_PUBLISHED"
    result = _decide(value)

    _assert_blocked(result)
    assert "PASS_PUBLISHED_FORBIDDEN" in result["decision_violations"]
    assert "PASS_PUBLISHED" not in _scalar_strings(result)


def test_pass_published_evidence_status_blocks_and_is_suppressed():
    value = _valid_result()
    value["normalized_local_noop_runner_result_candidate"][
        "result_candidate_evidence_items"
    ][0]["evidence_status"] = "PASS_PUBLISHED"
    result = _decide(value)

    _assert_blocked(result)
    assert "PASS_PUBLISHED_FORBIDDEN" in result["decision_violations"]
    assert "PASS_PUBLISHED" not in _scalar_strings(result)


def test_pass_published_literal_in_opaque_strings_does_not_block():
    value = _valid_result()
    value["reason"] = "PASS_PUBLISHED is opaque reason text"
    candidate = value["normalized_local_noop_runner_result_candidate"]
    candidate["notes"] = ("PASS_PUBLISHED in candidate notes",)
    candidate["source_of_truth"] = ("PASS_PUBLISHED source ref",)
    value["source"]["source_of_truth"] = candidate["source_of_truth"]
    item = candidate["result_candidate_evidence_items"][0]
    item["artifact_ref"] = "PASS_PUBLISHED artifact ref"
    item["producer_ref"] = "PASS_PUBLISHED producer ref"
    item["evidence_refs"] = ("PASS_PUBLISHED evidence ref",)
    item["notes"] = ("PASS_PUBLISHED evidence note",)
    value["invariant_refs"] = REQUIRED_P2D42_INVARIANT_REFS + (
        "PASS_PUBLISHED opaque invariant text",
    )

    result = _decide(value)
    assert result["decision_created"] is True


def test_public_url_contract_is_exact_across_all_containers():
    for container_key in (
        "source",
        "normalized_local_noop_runner_result_candidate",
        "local_noop_runner_consumption_receipt",
    ):
        value = _valid_result()
        value[container_key]["public_url"] = "https://forbidden.example"
        result = _decide(value)
        _assert_blocked(result)
        assert "PUBLIC_URL_NOT_NULL" in result["decision_violations"]
        assert "https://forbidden.example" not in _scalar_strings(result)


def test_unknown_and_forbidden_keys_are_safely_suppressed():
    unknown = _valid_result()
    unknown["unknown_parent"] = "unknown-caller-value"
    forbidden = _valid_result()
    forbidden["Quality-Pass"] = "forbidden-caller-value"

    for value in (unknown, forbidden):
        result = _decide(value)
        _assert_blocked(result)
        assert result["source"] == BLOCKED_SOURCE
        assert "unknown_parent" not in _scalar_strings(result)
        assert "unknown-caller-value" not in _scalar_strings(result)
        assert "Quality-Pass" not in _scalar_strings(result)
        assert "forbidden-caller-value" not in _scalar_strings(result)

    result = _decide(forbidden)
    assert "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT" in result[
        "decision_violations"
    ]
    assert (
        "p2d42_consumer_result.forbidden_field_or_namespace"
        in result["missing_or_invalid_fields"]
    )


def test_unknown_parent_path_and_nested_forbidden_data_never_leak():
    value = _valid_result()
    value["caller-parent-secret"] = {
        "decision_created": True,
        "caller-child-secret": "caller-value-secret",
    }
    result = _decide(value)

    _assert_blocked(result)
    strings = _scalar_strings(result)
    fields = result["missing_or_invalid_fields"]
    assert "caller-parent-secret" not in strings
    assert "caller-child-secret" not in strings
    assert "caller-value-secret" not in strings
    for field in fields:
        assert "caller" not in field


def test_recursive_forbidden_scanner_traverses_dict_list_and_tuple():
    nested_values = (
        {"quality_pass": True},
        [{"decision_created": True}],
        ({"publish_allowed": True},),
    )
    for nested_value in nested_values:
        value = _valid_result()
        value["unknown_parent"] = nested_value
        result = _decide(value)
        _assert_blocked(result)
        assert "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT" in result[
            "decision_violations"
        ]


def test_self_referential_dict_is_cycle_safe_and_detects_forbidden_key():
    cycle_dict: dict[str, object] = {}
    cycle_dict["self"] = cycle_dict
    cycle_dict["raw-command"] = "cycle-dict-secret"
    value = _valid_result()
    value["unknown_cycle_parent"] = cycle_dict

    result = _decide(value)

    _assert_blocked(result)
    assert cycle_dict["self"] is cycle_dict
    assert cycle_dict["raw-command"] == "cycle-dict-secret"
    assert "P2D42_CONSUMER_RESULT_KEYS_INVALID" in result[
        "decision_violations"
    ]
    assert "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT" in result[
        "decision_violations"
    ]
    assert set(result["decision_violations"]).issubset(set(REASON_CODES))
    assert (
        "p2d42_consumer_result.forbidden_field_or_namespace"
        in result["missing_or_invalid_fields"]
    )
    output_strings = _scalar_strings(result)
    output_keys = _payload_keys(result)
    for caller_value in (
        "unknown_cycle_parent",
        "raw-command",
        "raw_command",
        "cycle-dict-secret",
    ):
        assert caller_value not in output_strings
        assert caller_value not in output_keys


def test_self_referential_list_is_cycle_safe_for_invalid_tuple_field():
    cycle_list: list[object] = []
    cycle_list.append(cycle_list)
    cycle_list.append("cycle-list-secret")
    value = _valid_result()
    value["normalized_local_noop_runner_result_candidate"]["notes"] = (
        cycle_list
    )

    result = _decide(value)

    _assert_blocked(result)
    assert cycle_list[0] is cycle_list
    assert cycle_list[1] == "cycle-list-secret"
    assert "P2D42_NORMALIZED_CANDIDATE_FIELD_INVALID" in result[
        "decision_violations"
    ]
    assert "cycle-list-secret" not in _scalar_strings(result)


def test_indirect_cycle_is_cycle_safe_and_uses_existing_shape_reason():
    first: dict[str, object] = {}
    second: list[object] = [first]
    first["next"] = second
    value = _valid_result()
    value["unknown_indirect_cycle"] = first

    result = _decide(value)

    _assert_blocked(result)
    assert first["next"] is second
    assert second[0] is first
    assert "P2D42_CONSUMER_RESULT_KEYS_INVALID" in result[
        "decision_violations"
    ]
    assert set(result["decision_violations"]).issubset(set(REASON_CODES))
    assert "unknown_indirect_cycle" not in _payload_keys(result)
    assert "unknown_indirect_cycle" not in _scalar_strings(result)


def test_deeply_nested_finite_container_uses_no_recursion_depth():
    nested: object = {"raw-command": "deep-container-secret"}
    for _ in range(1500):
        nested = [nested]
    value = _valid_result()
    value["unknown_deeply_nested"] = nested

    result = _decide(value)

    _assert_blocked(result)
    assert "P2D42_CONSUMER_RESULT_KEYS_INVALID" in result[
        "decision_violations"
    ]
    assert "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT" in result[
        "decision_violations"
    ]
    assert (
        "p2d42_consumer_result.forbidden_field_or_namespace"
        in result["missing_or_invalid_fields"]
    )
    output_strings = _scalar_strings(result)
    output_keys = _payload_keys(result)
    for caller_value in (
        "unknown_deeply_nested",
        "raw-command",
        "raw_command",
        "deep-container-secret",
    ):
        assert caller_value not in output_strings
        assert caller_value not in output_keys


def test_non_dict_source_candidate_and_receipt_block_safely():
    cases = (
        ("source", "P2D42_SOURCE_NOT_DICT"),
        (
            "normalized_local_noop_runner_result_candidate",
            "P2D42_NORMALIZED_CANDIDATE_NOT_DICT",
        ),
        (
            "local_noop_runner_consumption_receipt",
            "P2D42_RECEIPT_NOT_DICT",
        ),
    )
    non_dict_values = (
        ["nested-contract-secret"],
        ("nested-contract-secret",),
        "nested-contract-secret",
        None,
    )
    for container_key, reason_code in cases:
        for non_dict_value in non_dict_values:
            value = _valid_result()
            value[container_key] = non_dict_value

            result = _decide(value)

            _assert_blocked(result)
            assert reason_code in result["decision_violations"]
            assert "nested-contract-secret" not in _scalar_strings(result)


def test_non_dict_evidence_items_block_safely():
    non_dict_values = (
        ["evidence-item-secret"],
        ("evidence-item-secret",),
        "evidence-item-secret",
        None,
    )
    for non_dict_value in non_dict_values:
        value = _valid_result()
        candidate = value[
            "normalized_local_noop_runner_result_candidate"
        ]
        candidate["result_candidate_evidence_items"] = (non_dict_value,)

        result = _decide(value)

        _assert_blocked(result)
        assert "P2D42_EVIDENCE_ITEM_NOT_DICT" in result[
            "decision_violations"
        ]
        assert "evidence-item-secret" not in _scalar_strings(result)


def test_declared_schema_keys_are_legal_only_at_approved_paths():
    for wrong_path_key in (
        "consumed",
        "runner_terminal_status",
        "receipt_kind",
        "result_candidate_evidence_id",
    ):
        value = _valid_result()
        value["source"]["unknown_parent"] = {wrong_path_key: "not-echoed"}
        result = _decide(value)
        _assert_blocked(result)
        assert "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT" in result[
            "decision_violations"
        ]
        assert "not-echoed" not in _scalar_strings(result)


def test_blocked_source_and_empty_decision_are_fixed_for_every_failure():
    values = ()
    root_failure = _valid_result()
    root_failure["consumed"] = False
    values = values + (root_failure,)
    candidate_failure = _valid_result()
    candidate_failure["normalized_local_noop_runner_result_candidate"][
        "mode"
    ] = "live-secret-mode"
    values = values + (candidate_failure,)
    receipt_failure = _valid_result()
    receipt_failure["local_noop_runner_consumption_receipt"][
        "receipt_kind"
    ] = "caller-secret-receipt"
    values = values + (receipt_failure,)

    for value in values:
        result = _decide(value)
        _assert_blocked(result)
        assert result["source"] == BLOCKED_SOURCE
        assert result["local_noop_terminal_result_assembly_decision"] == {}


def test_reason_text_is_fixed_and_never_echoes_caller_reason():
    value = _valid_result()
    value["reason_code"] = "caller-secret-code"
    value["reason"] = "caller-secret-reason"
    result = _decide(value)

    _assert_blocked(result)
    assert result["reason"] == (
        "The P2D-42 reason code must declare in-memory consumption."
    )
    assert "caller-secret-code" not in _scalar_strings(result)
    assert "caller-secret-reason" not in _scalar_strings(result)


def test_input_is_not_mutated_and_outputs_are_fresh():
    value = _valid_result()
    expected = _valid_result()

    first = _decide(value)
    second = _decide(value)

    assert value == expected
    assert first["source"] is not value["source"]
    assert first["source"] is not second["source"]
    first_decision = first["local_noop_terminal_result_assembly_decision"]
    second_decision = second["local_noop_terminal_result_assembly_decision"]
    assert first_decision is not value[
        "normalized_local_noop_runner_result_candidate"
    ]
    assert first_decision is not value["local_noop_runner_consumption_receipt"]
    assert first_decision is not second_decision


def test_complete_candidate_receipt_and_final_result_are_not_returned():
    result = _decide()
    keys = _payload_keys(result)

    assert "normalized_local_noop_runner_result_candidate" not in keys
    assert "local_noop_runner_consumption_receipt" not in keys
    assert "local_noop_runner_result" not in keys
    assert "local_noop_runner_result_id" not in keys
    assert "result_kind" not in keys


def test_decision_created_is_the_only_approved_positive_boolean():
    result = _decide()
    keys = _payload_keys(result)

    assert result["decision_created"] is True
    for forbidden_field in FORBIDDEN_POSITIVE_FIELDS:
        assert forbidden_field not in keys


def test_validation_records_have_exact_safe_keys_and_paths():
    value = _valid_result()
    value["source"]["unknown-source-key"] = "caller-secret"
    result = _decide(value)

    _assert_blocked(result)
    for record in result["decision_validation_violations"]:
        assert tuple(record.keys()) == VALIDATION_VIOLATION_KEYS
        assert isinstance(record["reason_code"], str)
        assert isinstance(record["field"], str)
        assert "unknown-source-key" not in record["field"]
        assert "caller-secret" not in record["field"]


def test_all_violations_are_deduplicated_and_priority_ordered():
    value = _valid_result()
    value["Quality-Pass"] = True
    value["consumed"] = False
    value["reason_code"] = "wrong"
    value["reason"] = ""
    candidate = value["normalized_local_noop_runner_result_candidate"]
    candidate["mode"] = "live"
    candidate["runner_terminal_status"] = "PASS_PUBLISHED"

    result = _decide(value)
    expected = tuple(
        code for code in REASON_PRIORITY
        if code != REASON_PRIORITY[-1]
        and code in result["decision_violations"]
    )
    assert result["decision_violations"] == expected
    assert len(result["decision_violations"]) == len(
        set(result["decision_violations"])
    )
    assert result["reason_code"] == "FORBIDDEN_FIELD_OR_NAMESPACE_PRESENT"


def test_output_invariant_refs_are_exact_and_ordered():
    assert _decide()["invariant_refs"] == INVARIANT_REFS
    assert decision._INVARIANT_REFS == INVARIANT_REFS


def test_public_api_is_keyword_only_and_bool_wrapper_matches():
    decide_code = decision.decide_local_noop_terminal_result_assembly.__code__
    bool_code = (
        decision.is_local_noop_terminal_result_assembly_decision_created.__code__
    )
    assert decide_code.co_argcount == 0
    assert decide_code.co_kwonlyargcount == 1
    assert bool_code.co_argcount == 0
    assert bool_code.co_kwonlyargcount == 1

    valid = _valid_result()
    assert decision.is_local_noop_terminal_result_assembly_decision_created(
        local_noop_runner_result_candidate_consumption=valid,
    ) is True
    invalid = _valid_result()
    invalid["consumed"] = False
    assert decision.is_local_noop_terminal_result_assembly_decision_created(
        local_noop_runner_result_candidate_consumption=invalid,
    ) is False


def test_production_module_has_no_forbidden_dependencies_or_repr_scan():
    names = _module_code_names()
    namespace = decision.__dict__

    for forbidden_name in FORBIDDEN_DEPENDENCY_NAMES:
        assert forbidden_name not in namespace
        assert forbidden_name not in names
    assert "open" not in names
    assert "getenv" not in names
    assert "environ" not in names
    assert "repr" not in names


def test_production_module_has_no_mutable_global_contract_values():
    for name, value in decision.__dict__.items():
        if name.startswith("__") or name == "Final" or callable(value):
            continue
        assert not isinstance(value, dict)
        assert not isinstance(value, list)
        assert not isinstance(value, set)


def test_python_39_contract_uses_no_pep604_annotations():
    functions = (
        decision.decide_local_noop_terminal_result_assembly,
        decision.is_local_noop_terminal_result_assembly_decision_created,
    )
    for function in functions:
        for annotation in function.__annotations__.values():
            assert "|" not in str(annotation)


def test_input_mapping_order_does_not_change_output_order():
    value = _valid_result()
    reordered = {}
    for key in reversed(tuple(value.keys())):
        reordered[key] = value[key]

    result = _decide(reordered)
    assert result["decision_created"] is True
    assert tuple(result.keys()) == RESULT_KEYS
    assert tuple(result["source"].keys()) == OUTPUT_SOURCE_KEYS
    assert tuple(
        result["local_noop_terminal_result_assembly_decision"].keys()
    ) == DECISION_KEYS
