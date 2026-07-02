"""Static import-only contract tests for gate constants."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import gates


def test_gate_names_and_decisions_are_declared():
    assert gates.GATE_NAMES == (
        "Adapter Configuration Gate",
        "Daily Publish Gate",
    )
    assert gates.GATE_DECISIONS == ("PASS", "BLOCKED")


def test_shared_gate_decision_envelope_fields():
    assert gates.SHARED_GATE_DECISION_ENVELOPE_FIELDS == (
        "run_id",
        "gate_name",
        "decision",
        "from_state",
        "to_state",
        "reason_codes",
        "blocking_reasons",
        "evidence_refs",
        "input_evidence_refs",
        "required_inputs_present",
        "missing_inputs",
        "redaction_status",
        "public_url_created",
        "public_url",
        "checked_at",
        "timestamp_policy",
        "source_of_truth",
        "notes",
    )


def test_adapter_gate_fields():
    assert gates.ADAPTER_CONFIGURATION_GATE_INPUT_FIELDS == (
        "runtime_context_present",
        "runtime_profile_snapshot_ref",
        "runtime_profile_name",
        "runtime_profile_mode",
        "config_snapshot_ref",
        "adapter_configuration_declared",
        "required_credentials_presence_markers",
        "redaction_status",
        "publish_mode",
        "notification_mode",
        "eval_mode",
        "adapter_capability_markers",
        "noop_policy_markers",
        "disabled_external_adapters_declared",
        "environment_safety_marker",
    )
    assert gates.ADAPTER_CONFIGURATION_GATE_PAYLOAD_FIELDS == (
        "profile_name",
        "checked_adapters",
        "blocking_adapters",
        "redacted_message",
        "adapter_capability_markers",
        "noop_policy_markers",
        "runtime_profile_ref",
        "config_snapshot_ref",
        "credential_presence_markers",
        "environment_safety_marker",
    )


def test_daily_publish_gate_fields():
    assert gates.DAILY_PUBLISH_GATE_INPUT_FIELDS == (
        "required_source_presence",
        "source_manifest_ref",
        "training_report_present",
        "reader_html_present",
        "validator_result",
        "rubric_review_result",
        "audit_review_result",
        "artifact_inventory",
        "pre_gate_artifact_hash_evidence",
        "public_private_leak_check_result",
        "noop_publish_config",
        "noop_url_policy",
        "declared_public_url_null_marker",
        "declared_public_url_created_false_marker",
        "credential_redaction_status",
        "blocking_risk_flags",
        "evidence_completeness_marker",
    )
    assert gates.DAILY_PUBLISH_GATE_PAYLOAD_FIELDS == (
        "blocking_checks",
        "validator_result_ref",
        "rubric_review_result_ref",
        "audit_review_result_ref",
        "artifact_inventory_ref",
        "pre_gate_hash_ref",
        "noop_url_policy",
        "public_private_leak_check_ref",
        "credential_redaction_ref",
    )


def test_reason_code_catalogs_include_required_codes():
    assert gates.ADAPTER_CONFIGURATION_GATE_REASON_CODES == (
        "RUNTIME_CONTEXT_MISSING",
        "CONFIG_SNAPSHOT_MISSING",
        "ADAPTER_CONFIG_MISSING",
        "CREDENTIAL_MARKER_MISSING",
        "PROFILE_MODE_STRUCTURE_INVALID",
        "ADAPTER_CAPABILITY_MARKERS_MISSING",
        "NOOP_POLICY_MARKERS_MISSING",
        "RAW_CREDENTIAL_EXPOSED",
        "EXTERNAL_ADAPTER_ENABLED_IN_MVP",
        "UNSAFE_ENVIRONMENT",
        "AMBIGUOUS_RUNTIME_MODE",
        "REAL_EXTERNAL_API_ATTEMPTED",
    )
    assert gates.DAILY_PUBLISH_GATE_REASON_CODES == (
        "REQUIRED_SOURCE_MISSING",
        "TRAINING_REPORT_MISSING",
        "READER_HTML_MISSING",
        "VALIDATOR_RESULT_MISSING",
        "VALIDATOR_NOT_PASS",
        "RUBRIC_REVIEW_MISSING",
        "RUBRIC_NOT_PASS",
        "AUDIT_REVIEW_MISSING",
        "AUDIT_NOT_PASS",
        "REVIEW_STUB_WITHOUT_EXPLICIT_PASS",
        "PREGATE_HASH_MISSING",
        "ARTIFACT_INVENTORY_MISSING",
        "PRIVATE_EVIDENCE_LEAK",
        "PUBLIC_CANDIDATE_MISCLASSIFIED",
        "TRAINING_REPORT_MISCLASSIFIED_AS_PUBLIC",
        "NOOP_PUBLIC_URL_NON_NULL",
        "NOOP_PUBLIC_URL_CREATED_TRUE",
        "CREDENTIAL_EXPOSURE",
        "BLOCKING_RISK_PRESENT",
        "EVIDENCE_INCOMPLETE",
        "REAL_PUBLISH_ATTEMPTED",
        "REAL_NOTIFICATION_ATTEMPTED",
    )
    assert "NOOP_PUBLIC_URL_NON_NULL" in gates.DAILY_PUBLISH_GATE_REASON_CODES
    assert "NOOP_PUBLIC_URL_CREATED_TRUE" in gates.DAILY_PUBLISH_GATE_REASON_CODES


def test_gate_to_state_mappings_match_contract():
    assert gates.GATE_TO_STATE_MAPPINGS == {
        ("Adapter Configuration Gate", "PASS"): "RETRIEVING",
        ("Adapter Configuration Gate", "BLOCKED"): "CONFIG_BLOCKED",
        ("Daily Publish Gate", "PASS"): "PUBLISH_ALLOWED",
        ("Daily Publish Gate", "BLOCKED"): "REVIEW_BLOCKED",
    }


def test_forbidden_gate_mappings_are_declared():
    forbidden_mappings = {
        (mapping["gate_name"], mapping["decision"], mapping["forbidden_result"])
        for mapping in gates.FORBIDDEN_GATE_MAPPINGS
    }
    expected_forbidden_mappings = {
        ("Adapter Configuration Gate", "BLOCKED", "RETRIEVING"),
        ("Daily Publish Gate", "BLOCKED", "PUBLISH_ALLOWED"),
        ("Daily Publish Gate", "PASS", "NOOP_COMPLETED"),
        ("Daily Publish Gate", "PASS", "PASS_PUBLISHED"),
        ("any gate", "any", "public URL creation"),
        ("any gate", "any", "real publish"),
        ("any gate", "any", "notification send"),
    }

    assert expected_forbidden_mappings <= forbidden_mappings


def test_gate_invariants_capture_no_public_url_boundary():
    assert gates.GATE_INVARIANTS == (
        "no quality PASS, no public URL",
        "Adapter PASS -> RETRIEVING",
        "Adapter BLOCKED -> CONFIG_BLOCKED",
        "Daily PASS -> PUBLISH_ALLOWED",
        "Daily BLOCKED -> REVIEW_BLOCKED",
        "Daily PASS cannot go to NOOP_COMPLETED",
        "Daily PASS cannot go to PASS_PUBLISHED",
        "NOOP_PUBLIC_URL_NON_NULL covers public_url != null",
        "NOOP_PUBLIC_URL_CREATED_TRUE covers public_url_created == true, including public_url == null",
        "generated ledgers after the gate are not Daily Publish Gate inputs",
        "malformed noop ledger after the gate prevents NOOP_COMPLETED",
        "PUBLISH_ALLOWED remains eligibility-only",
        "PASS_PUBLISHED remains excluded from MVP",
    )
