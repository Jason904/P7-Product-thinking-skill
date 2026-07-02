"""Static artifact contract constants for the AI Daily Publishing System."""

from typing import Final

RUNTIME_CONTEXT_ARTIFACT: Final[str] = "runtime-context.yaml"
RUNTIME_PROFILE_SNAPSHOT_CONFIG_SNAPSHOT_REFERENCE: Final[str] = (
    "runtime profile snapshot / config snapshot reference"
)
ADAPTER_PREFLIGHT_RESULT_ARTIFACT: Final[str] = "adapter-preflight-result.yaml"
SOURCE_MANIFEST_ARTIFACT: Final[str] = "source-manifest.yaml"
SOURCE_NOTES_ARTIFACT: Final[str] = "source-notes.md"
TRAINING_REPORT_ARTIFACT: Final[str] = "training-report.md"
READER_HTML_ARTIFACT: Final[str] = "reader.html"
VALIDATOR_RESULT_ARTIFACT: Final[str] = "validator-result.yaml"
RUBRIC_REVIEW_STUB_ARTIFACT: Final[str] = "rubric-review.stub.json"
RUBRIC_REVIEW_ARTIFACT: Final[str] = "rubric-review.json"
AUDIT_REVIEW_STUB_ARTIFACT: Final[str] = "audit-review.stub.json"
AUDIT_REVIEW_ARTIFACT: Final[str] = "audit-review.json"
PUBLISH_LEDGER_ARTIFACT: Final[str] = "publish-ledger.yaml"
NOTIFICATION_LEDGER_ARTIFACT: Final[str] = "notification-ledger.yaml"
ARTIFACT_HASH_ARTIFACT: Final[str] = "artifact-hash.yaml"
RUN_LEDGER_ARTIFACT: Final[str] = "run-ledger.yaml"
FAILURE_PACKAGE_ARTIFACT: Final[str] = "failure-package.yaml"
BADCASE_RECORD_ARTIFACT: Final[str] = "badcase-record.yaml"

ARTIFACT_NAMES: Final[tuple[str, ...]] = (
    RUNTIME_CONTEXT_ARTIFACT,
    RUNTIME_PROFILE_SNAPSHOT_CONFIG_SNAPSHOT_REFERENCE,
    ADAPTER_PREFLIGHT_RESULT_ARTIFACT,
    SOURCE_MANIFEST_ARTIFACT,
    SOURCE_NOTES_ARTIFACT,
    TRAINING_REPORT_ARTIFACT,
    READER_HTML_ARTIFACT,
    VALIDATOR_RESULT_ARTIFACT,
    RUBRIC_REVIEW_STUB_ARTIFACT,
    RUBRIC_REVIEW_ARTIFACT,
    AUDIT_REVIEW_STUB_ARTIFACT,
    AUDIT_REVIEW_ARTIFACT,
    PUBLISH_LEDGER_ARTIFACT,
    NOTIFICATION_LEDGER_ARTIFACT,
    ARTIFACT_HASH_ARTIFACT,
    RUN_LEDGER_ARTIFACT,
    FAILURE_PACKAGE_ARTIFACT,
    BADCASE_RECORD_ARTIFACT,
)

PUBLIC_CANDIDATE: Final[str] = "public_candidate"
PUBLIC_SAFE_RENDER_SOURCE: Final[str] = "public_safe_render_source"
PRIVATE_EVIDENCE: Final[str] = "private_evidence"
LEDGER: Final[str] = "ledger"
FAILURE_EVIDENCE: Final[str] = "failure_evidence"
GOVERNANCE_EVIDENCE: Final[str] = "governance_evidence"

PUBLIC_CANDIDATE_ARTIFACTS: Final[frozenset[str]] = frozenset(
    (READER_HTML_ARTIFACT,)
)

PUBLIC_SAFE_RENDER_SOURCE_ARTIFACTS: Final[frozenset[str]] = frozenset(
    (TRAINING_REPORT_ARTIFACT,)
)

PRIVATE_EVIDENCE_ARTIFACTS: Final[frozenset[str]] = frozenset(
    (
        SOURCE_MANIFEST_ARTIFACT,
        SOURCE_NOTES_ARTIFACT,
        VALIDATOR_RESULT_ARTIFACT,
        RUBRIC_REVIEW_STUB_ARTIFACT,
        RUBRIC_REVIEW_ARTIFACT,
        AUDIT_REVIEW_STUB_ARTIFACT,
        AUDIT_REVIEW_ARTIFACT,
    )
)

LEDGER_ARTIFACTS: Final[frozenset[str]] = frozenset(
    (
        RUNTIME_CONTEXT_ARTIFACT,
        RUNTIME_PROFILE_SNAPSHOT_CONFIG_SNAPSHOT_REFERENCE,
        ADAPTER_PREFLIGHT_RESULT_ARTIFACT,
        PUBLISH_LEDGER_ARTIFACT,
        NOTIFICATION_LEDGER_ARTIFACT,
        ARTIFACT_HASH_ARTIFACT,
        RUN_LEDGER_ARTIFACT,
    )
)

FAILURE_EVIDENCE_ARTIFACTS: Final[frozenset[str]] = frozenset(
    (FAILURE_PACKAGE_ARTIFACT,)
)

GOVERNANCE_EVIDENCE_ARTIFACTS: Final[frozenset[str]] = frozenset(
    (BADCASE_RECORD_ARTIFACT,)
)

ARTIFACT_CLASSIFICATION_BY_NAME: Final[dict[str, str]] = {
    RUNTIME_CONTEXT_ARTIFACT: LEDGER,
    RUNTIME_PROFILE_SNAPSHOT_CONFIG_SNAPSHOT_REFERENCE: LEDGER,
    ADAPTER_PREFLIGHT_RESULT_ARTIFACT: LEDGER,
    SOURCE_MANIFEST_ARTIFACT: PRIVATE_EVIDENCE,
    SOURCE_NOTES_ARTIFACT: PRIVATE_EVIDENCE,
    TRAINING_REPORT_ARTIFACT: PUBLIC_SAFE_RENDER_SOURCE,
    READER_HTML_ARTIFACT: PUBLIC_CANDIDATE,
    VALIDATOR_RESULT_ARTIFACT: PRIVATE_EVIDENCE,
    RUBRIC_REVIEW_STUB_ARTIFACT: PRIVATE_EVIDENCE,
    RUBRIC_REVIEW_ARTIFACT: PRIVATE_EVIDENCE,
    AUDIT_REVIEW_STUB_ARTIFACT: PRIVATE_EVIDENCE,
    AUDIT_REVIEW_ARTIFACT: PRIVATE_EVIDENCE,
    PUBLISH_LEDGER_ARTIFACT: LEDGER,
    NOTIFICATION_LEDGER_ARTIFACT: LEDGER,
    ARTIFACT_HASH_ARTIFACT: LEDGER,
    RUN_LEDGER_ARTIFACT: LEDGER,
    FAILURE_PACKAGE_ARTIFACT: FAILURE_EVIDENCE,
    BADCASE_RECORD_ARTIFACT: GOVERNANCE_EVIDENCE,
}

HASH_PHASES: Final[tuple[str, ...]] = (
    "pre-gate draft",
    "pre-gate update",
    "final",
)

ARTIFACT_INVENTORY_FIELDS: Final[tuple[str, ...]] = (
    "artifact_name",
    "classification",
    "expected_presence",
    "actual_status",
    "path_reference",
    "required_for_state",
    "required_for_gate",
    "hash_required_phase",
    "redaction_status",
    "notes",
)

ARTIFACT_WRITE_RESULT_FIELDS: Final[tuple[str, ...]] = (
    "artifact_name",
    "classification",
    "write_status",
    "artifact_reference",
    "actual_status",
    "redaction_status",
    "failure_state",
    "notes",
)

ARTIFACT_SINK_RESULT_FIELDS: Final[tuple[str, ...]] = (
    "sink_name",
    "sink_mode",
    "accepted_artifacts",
    "rejected_artifacts",
    "write_results",
    "failure_state",
    "redaction_status",
    "notes",
)

WRITE_ORDER_STEPS: Final[tuple[dict[str, object], ...]] = (
    {
        "step": "1",
        "artifacts": (RUNTIME_CONTEXT_ARTIFACT,),
        "phase": "runtime context",
    },
    {
        "step": "2",
        "artifacts": (RUNTIME_PROFILE_SNAPSHOT_CONFIG_SNAPSHOT_REFERENCE,),
        "phase": "profile and config reference",
    },
    {
        "step": "3",
        "artifacts": (ADAPTER_PREFLIGHT_RESULT_ARTIFACT,),
        "phase": "adapter preflight",
    },
    {
        "step": "4",
        "artifacts": (SOURCE_MANIFEST_ARTIFACT,),
        "phase": "source manifest",
    },
    {
        "step": "5",
        "artifacts": (SOURCE_NOTES_ARTIFACT,),
        "phase": "source notes",
    },
    {
        "step": "6",
        "artifacts": (TRAINING_REPORT_ARTIFACT,),
        "phase": "canonical report content",
    },
    {
        "step": "7",
        "artifacts": (READER_HTML_ARTIFACT,),
        "phase": "public candidate",
    },
    {
        "step": "8",
        "artifacts": (ARTIFACT_HASH_ARTIFACT,),
        "phase": "pre-gate draft for present pre-gate artifacts",
    },
    {
        "step": "9",
        "artifacts": (VALIDATOR_RESULT_ARTIFACT,),
        "phase": "validator result",
    },
    {
        "step": "10",
        "artifacts": (RUBRIC_REVIEW_STUB_ARTIFACT, RUBRIC_REVIEW_ARTIFACT),
        "phase": "rubric review result",
    },
    {
        "step": "11",
        "artifacts": (AUDIT_REVIEW_STUB_ARTIFACT, AUDIT_REVIEW_ARTIFACT),
        "phase": "audit review result",
    },
    {
        "step": "12",
        "artifacts": (ARTIFACT_HASH_ARTIFACT,),
        "phase": "pre-gate update after review artifacts",
    },
    {
        "step": "13",
        "artifacts": (RUN_LEDGER_ARTIFACT,),
        "phase": "Daily Publish Gate decision in run ledger draft",
    },
    {
        "step": "14",
        "artifacts": (PUBLISH_LEDGER_ARTIFACT,),
        "phase": "noop publish ledger",
    },
    {
        "step": "15",
        "artifacts": (NOTIFICATION_LEDGER_ARTIFACT,),
        "phase": "noop notification ledger",
    },
    {
        "step": "16",
        "artifacts": (ARTIFACT_HASH_ARTIFACT,),
        "phase": "final update and finalize",
    },
    {
        "step": "17",
        "artifacts": (RUN_LEDGER_ARTIFACT,),
        "phase": "final ledger seal",
    },
)

ARTIFACT_INVARIANTS: Final[tuple[str, ...]] = (
    "reader.html only public candidate",
    "training-report.md not public candidate",
    "private evidence never rendered into public candidate",
    "present-only hash rule: only present artifacts may have hash entries",
    "skipped/absent artifacts are not hashed as present",
    "final hash before NOOP_COMPLETED",
    "no public URL",
    "no artifact examples",
)
