"""Static gate contract constants for the AI Daily Publishing System."""

from typing import Final

ADAPTER_CONFIGURATION_GATE: Final[str] = "Adapter Configuration Gate"
DAILY_PUBLISH_GATE: Final[str] = "Daily Publish Gate"

PASS: Final[str] = "PASS"
BLOCKED: Final[str] = "BLOCKED"

GATE_NAMES: Final[tuple[str, ...]] = (
    ADAPTER_CONFIGURATION_GATE,
    DAILY_PUBLISH_GATE,
)

GATE_DECISIONS: Final[tuple[str, ...]] = (
    PASS,
    BLOCKED,
)

SHARED_GATE_DECISION_ENVELOPE_FIELDS: Final[tuple[str, ...]] = (
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

ADAPTER_CONFIGURATION_GATE_INPUT_FIELDS: Final[tuple[str, ...]] = (
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

ADAPTER_CONFIGURATION_GATE_PAYLOAD_FIELDS: Final[tuple[str, ...]] = (
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

DAILY_PUBLISH_GATE_INPUT_FIELDS: Final[tuple[str, ...]] = (
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

DAILY_PUBLISH_GATE_PAYLOAD_FIELDS: Final[tuple[str, ...]] = (
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

UPSTREAM_COMPATIBILITY_MAPPING: Final[dict[str, str]] = {
    "run_id": "Shared Gate Decision Envelope",
    "status: PASS | BLOCKED": "decision: PASS | BLOCKED",
    "checked_at": "checked_at / timestamp_policy",
    "reason_codes": "Shared Gate Decision Envelope",
    "redaction_status": "Shared Gate Decision Envelope",
    "public_url_created": "Shared Gate Decision Envelope",
    "maps_to_state": "to_state",
    "profile_name": "Adapter Configuration Gate Payload",
    "checked_adapters": "Adapter Configuration Gate Payload",
    "blocking_adapters": "Adapter Configuration Gate Payload",
    "redacted_message": "Adapter Configuration Gate Payload",
    "input_evidence_refs": "Shared Gate Decision Envelope",
    "blocking_checks": "Daily Publish Gate Payload",
    "noop_url_policy": "Daily Publish Gate Payload",
}

GATE_TO_STATE_MAPPINGS: Final[dict[tuple[str, str], str]] = {
    (ADAPTER_CONFIGURATION_GATE, PASS): "RETRIEVING",
    (ADAPTER_CONFIGURATION_GATE, BLOCKED): "CONFIG_BLOCKED",
    (DAILY_PUBLISH_GATE, PASS): "PUBLISH_ALLOWED",
    (DAILY_PUBLISH_GATE, BLOCKED): "REVIEW_BLOCKED",
}

FORBIDDEN_GATE_MAPPINGS: Final[tuple[dict[str, str], ...]] = (
    {
        "gate_name": ADAPTER_CONFIGURATION_GATE,
        "decision": BLOCKED,
        "forbidden_result": "RETRIEVING",
        "reason": "blocked adapter configuration cannot proceed to retrieval",
    },
    {
        "gate_name": DAILY_PUBLISH_GATE,
        "decision": BLOCKED,
        "forbidden_result": "PUBLISH_ALLOWED",
        "reason": "blocked Daily Publish Gate cannot grant eligibility",
    },
    {
        "gate_name": DAILY_PUBLISH_GATE,
        "decision": PASS,
        "forbidden_result": "NOOP_COMPLETED",
        "reason": "Daily Publish Gate pass is not noop completion",
    },
    {
        "gate_name": DAILY_PUBLISH_GATE,
        "decision": PASS,
        "forbidden_result": "PASS_PUBLISHED",
        "reason": "PASS_PUBLISHED is excluded from MVP",
    },
    {
        "gate_name": "any gate",
        "decision": "any",
        "forbidden_result": "public URL creation",
        "reason": "gate decisions cannot create public URLs",
    },
    {
        "gate_name": "any gate",
        "decision": "any",
        "forbidden_result": "real publish",
        "reason": "gate decisions cannot publish",
    },
    {
        "gate_name": "any gate",
        "decision": "any",
        "forbidden_result": "notification send",
        "reason": "gate decisions cannot send notifications",
    },
)

ADAPTER_CONFIGURATION_GATE_REASON_CODES: Final[tuple[str, ...]] = (
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

DAILY_PUBLISH_GATE_REASON_CODES: Final[tuple[str, ...]] = (
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

GATE_INVARIANTS: Final[tuple[str, ...]] = (
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
