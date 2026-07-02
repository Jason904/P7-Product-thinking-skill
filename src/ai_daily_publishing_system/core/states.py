"""Static state contract constants for the AI Daily Publishing System."""

from typing import Final

SCHEDULED_OR_STARTED: Final[str] = "SCHEDULED_OR_STARTED"
CONFIG_BLOCKED: Final[str] = "CONFIG_BLOCKED"
RETRIEVING: Final[str] = "RETRIEVING"
GENERATING: Final[str] = "GENERATING"
RENDERING: Final[str] = "RENDERING"
VALIDATING: Final[str] = "VALIDATING"
EVALUATING: Final[str] = "EVALUATING"
AUDITING: Final[str] = "AUDITING"
PUBLISH_ALLOWED: Final[str] = "PUBLISH_ALLOWED"
REVIEW_BLOCKED: Final[str] = "REVIEW_BLOCKED"
SYSTEM_FAILED: Final[str] = "SYSTEM_FAILED"
ADAPTER_FAILED: Final[str] = "ADAPTER_FAILED"
NOOP_COMPLETED: Final[str] = "NOOP_COMPLETED"
BADCASE_CREATED: Final[str] = "BADCASE_CREATED"

PASS_PUBLISHED_EXTERNAL_LABEL: Final[str] = "PASS_PUBLISHED"

MVP_STATES: Final[tuple[str, ...]] = (
    SCHEDULED_OR_STARTED,
    CONFIG_BLOCKED,
    RETRIEVING,
    GENERATING,
    RENDERING,
    VALIDATING,
    EVALUATING,
    AUDITING,
    PUBLISH_ALLOWED,
    REVIEW_BLOCKED,
    SYSTEM_FAILED,
    ADAPTER_FAILED,
    NOOP_COMPLETED,
    BADCASE_CREATED,
)

INITIAL_STATES: Final[frozenset[str]] = frozenset((SCHEDULED_OR_STARTED,))

ACTIVE_STATES: Final[frozenset[str]] = frozenset(
    (
        RETRIEVING,
        GENERATING,
        RENDERING,
        VALIDATING,
        EVALUATING,
        AUDITING,
    )
)

INTERMEDIATE_ELIGIBILITY_STATES: Final[frozenset[str]] = frozenset(
    (PUBLISH_ALLOWED,)
)

RUNTIME_TERMINAL_STATES: Final[frozenset[str]] = frozenset(
    (
        CONFIG_BLOCKED,
        REVIEW_BLOCKED,
        SYSTEM_FAILED,
        ADAPTER_FAILED,
        NOOP_COMPLETED,
    )
)

GOVERNANCE_FOLLOW_ON_STATES: Final[frozenset[str]] = frozenset(
    (BADCASE_CREATED,)
)

STATE_CATEGORIES: Final[dict[str, frozenset[str]]] = {
    "initial": INITIAL_STATES,
    "active": ACTIVE_STATES,
    "intermediate_eligibility": INTERMEDIATE_ELIGIBILITY_STATES,
    "runtime_terminal_outcomes": RUNTIME_TERMINAL_STATES,
    "governance_follow_on": GOVERNANCE_FOLLOW_ON_STATES,
}

RUNTIME_FAILURE_SOURCE_STATES: Final[frozenset[str]] = frozenset(
    (
        SCHEDULED_OR_STARTED,
        RETRIEVING,
        GENERATING,
        RENDERING,
        VALIDATING,
        EVALUATING,
        AUDITING,
        PUBLISH_ALLOWED,
    )
)

ADAPTER_FAILURE_SOURCE_STATES: Final[frozenset[str]] = frozenset(
    (
        RETRIEVING,
        GENERATING,
        RENDERING,
        VALIDATING,
        EVALUATING,
        AUDITING,
        PUBLISH_ALLOWED,
    )
)

TRANSITION_RECORD_FIELDS: Final[tuple[str, ...]] = (
    "from_state",
    "to_state",
    "reason_code",
    "evidence_refs",
    "condition",
    "is_allowed",
    "source_of_truth",
    "notes",
)

ALLOWED_TRANSITIONS: Final[tuple[dict[str, object], ...]] = (
    {
        "from_state": SCHEDULED_OR_STARTED,
        "to_state": CONFIG_BLOCKED,
        "reason_code": "ADAPTER_CONFIGURATION_BLOCKED",
        "evidence_refs": ("adapter-preflight-result.yaml",),
        "condition": "configuration_or_adapter_preflight_blocked",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "configuration or adapter preflight did not pass",
    },
    {
        "from_state": SCHEDULED_OR_STARTED,
        "to_state": RETRIEVING,
        "reason_code": "ADAPTER_PREFLIGHT_PASS",
        "evidence_refs": ("adapter-preflight-result.yaml",),
        "condition": "adapter_preflight_pass",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "adapter preflight pass",
    },
    {
        "from_state": RETRIEVING,
        "to_state": GENERATING,
        "reason_code": "RETRIEVAL_CONTRACT_COMPLETED",
        "evidence_refs": ("source-manifest.yaml", "source-notes.md"),
        "condition": "required_retrieval_contract_completed",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "required retrieval contract completed",
    },
    {
        "from_state": GENERATING,
        "to_state": RENDERING,
        "reason_code": "GENERATION_CONTRACT_COMPLETED",
        "evidence_refs": ("training-report.md",),
        "condition": "required_generation_contract_completed",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "required generation contract completed",
    },
    {
        "from_state": RENDERING,
        "to_state": VALIDATING,
        "reason_code": "RENDERING_CONTRACT_COMPLETED",
        "evidence_refs": ("reader.html",),
        "condition": "required_rendering_contract_completed",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "required rendering contract completed",
    },
    {
        "from_state": VALIDATING,
        "to_state": EVALUATING,
        "reason_code": "VALIDATION_CONTRACT_COMPLETED",
        "evidence_refs": ("validator-result.yaml",),
        "condition": "required_validation_contract_completed",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "required validation contract completed",
    },
    {
        "from_state": EVALUATING,
        "to_state": AUDITING,
        "reason_code": "RUBRIC_PASS",
        "evidence_refs": ("rubric-review.stub.json", "rubric-review.json"),
        "condition": "rubric_pass",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "rubric pass",
    },
    {
        "from_state": EVALUATING,
        "to_state": REVIEW_BLOCKED,
        "reason_code": "RUBRIC_BLOCKED_OR_INVALID",
        "evidence_refs": ("rubric-review.stub.json", "rubric-review.json"),
        "condition": "rubric_blocked_or_invalid",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "rubric blocked or invalid",
    },
    {
        "from_state": AUDITING,
        "to_state": REVIEW_BLOCKED,
        "reason_code": "AUDIT_OR_DAILY_PUBLISH_GATE_BLOCKED",
        "evidence_refs": ("audit-review.stub.json", "audit-review.json"),
        "condition": "audit_or_daily_publish_gate_blocked",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "audit or Daily Publish Gate blocked",
    },
    {
        "from_state": AUDITING,
        "to_state": PUBLISH_ALLOWED,
        "reason_code": "DAILY_PUBLISH_GATE_PASS",
        "evidence_refs": ("run-ledger.yaml",),
        "condition": "daily_publish_gate_pass",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "Daily Publish Gate pass",
    },
    {
        "from_state": PUBLISH_ALLOWED,
        "to_state": NOOP_COMPLETED,
        "reason_code": "NOOP_CONTRACT_COMPLETED",
        "evidence_refs": ("publish-ledger.yaml", "notification-ledger.yaml"),
        "condition": "noop_contract_completed",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "noop contract completed",
    },
    {
        "from_state": CONFIG_BLOCKED,
        "to_state": BADCASE_CREATED,
        "reason_code": "PERSISTENT_OR_USER_REPORTED",
        "evidence_refs": ("failure-package.yaml",),
        "condition": "persistent_or_user_reported",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "persistent or user reported configuration block",
    },
    {
        "from_state": REVIEW_BLOCKED,
        "to_state": BADCASE_CREATED,
        "reason_code": "BADCASE_REQUIRED_FOR_TERMINAL_OUTCOME",
        "evidence_refs": ("failure-package.yaml",),
        "condition": "badcase_required_for_terminal_outcome",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "badcase required for terminal outcome",
    },
    {
        "from_state": SYSTEM_FAILED,
        "to_state": BADCASE_CREATED,
        "reason_code": "BADCASE_REQUIRED_FOR_TERMINAL_OUTCOME",
        "evidence_refs": ("failure-package.yaml",),
        "condition": "badcase_required_for_terminal_outcome",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "badcase required for terminal outcome",
    },
    {
        "from_state": ADAPTER_FAILED,
        "to_state": BADCASE_CREATED,
        "reason_code": "BADCASE_REQUIRED_FOR_TERMINAL_OUTCOME",
        "evidence_refs": ("failure-package.yaml",),
        "condition": "badcase_required_for_terminal_outcome",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "badcase required for terminal outcome",
    },
    {
        "from_state": SCHEDULED_OR_STARTED,
        "to_state": SYSTEM_FAILED,
        "reason_code": "RUNTIME_FAILURE_CLASSIFIED",
        "evidence_refs": ("failure-package.yaml",),
        "condition": "runtime_failure_classified",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "runtime failure source expansion",
    },
    {
        "from_state": RETRIEVING,
        "to_state": SYSTEM_FAILED,
        "reason_code": "RUNTIME_FAILURE_CLASSIFIED",
        "evidence_refs": ("failure-package.yaml",),
        "condition": "runtime_failure_classified",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "runtime failure source expansion",
    },
    {
        "from_state": GENERATING,
        "to_state": SYSTEM_FAILED,
        "reason_code": "RUNTIME_FAILURE_CLASSIFIED",
        "evidence_refs": ("failure-package.yaml",),
        "condition": "runtime_failure_classified",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "runtime failure source expansion",
    },
    {
        "from_state": RENDERING,
        "to_state": SYSTEM_FAILED,
        "reason_code": "RUNTIME_FAILURE_CLASSIFIED",
        "evidence_refs": ("failure-package.yaml",),
        "condition": "runtime_failure_classified",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "runtime failure source expansion",
    },
    {
        "from_state": VALIDATING,
        "to_state": SYSTEM_FAILED,
        "reason_code": "RUNTIME_FAILURE_CLASSIFIED",
        "evidence_refs": ("failure-package.yaml",),
        "condition": "runtime_failure_classified",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "runtime failure source expansion",
    },
    {
        "from_state": EVALUATING,
        "to_state": SYSTEM_FAILED,
        "reason_code": "RUNTIME_FAILURE_CLASSIFIED",
        "evidence_refs": ("failure-package.yaml",),
        "condition": "runtime_failure_classified",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "runtime failure source expansion",
    },
    {
        "from_state": AUDITING,
        "to_state": SYSTEM_FAILED,
        "reason_code": "RUNTIME_FAILURE_CLASSIFIED",
        "evidence_refs": ("failure-package.yaml",),
        "condition": "runtime_failure_classified",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "runtime failure source expansion",
    },
    {
        "from_state": PUBLISH_ALLOWED,
        "to_state": SYSTEM_FAILED,
        "reason_code": "RUNTIME_FAILURE_CLASSIFIED",
        "evidence_refs": ("failure-package.yaml",),
        "condition": "runtime_failure_classified",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "runtime failure source expansion",
    },
    {
        "from_state": RETRIEVING,
        "to_state": ADAPTER_FAILED,
        "reason_code": "ADAPTER_EXECUTION_FAILED",
        "evidence_refs": ("failure-package.yaml",),
        "condition": "adapter_preflight_passed_then_execution_failed",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "adapter failure source expansion",
    },
    {
        "from_state": GENERATING,
        "to_state": ADAPTER_FAILED,
        "reason_code": "ADAPTER_EXECUTION_FAILED",
        "evidence_refs": ("failure-package.yaml",),
        "condition": "adapter_preflight_passed_then_execution_failed",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "adapter failure source expansion",
    },
    {
        "from_state": RENDERING,
        "to_state": ADAPTER_FAILED,
        "reason_code": "ADAPTER_EXECUTION_FAILED",
        "evidence_refs": ("failure-package.yaml",),
        "condition": "adapter_preflight_passed_then_execution_failed",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "adapter failure source expansion",
    },
    {
        "from_state": VALIDATING,
        "to_state": ADAPTER_FAILED,
        "reason_code": "ADAPTER_EXECUTION_FAILED",
        "evidence_refs": ("failure-package.yaml",),
        "condition": "adapter_preflight_passed_then_execution_failed",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "adapter failure source expansion",
    },
    {
        "from_state": EVALUATING,
        "to_state": ADAPTER_FAILED,
        "reason_code": "ADAPTER_EXECUTION_FAILED",
        "evidence_refs": ("failure-package.yaml",),
        "condition": "adapter_preflight_passed_then_execution_failed",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "adapter failure source expansion",
    },
    {
        "from_state": AUDITING,
        "to_state": ADAPTER_FAILED,
        "reason_code": "ADAPTER_EXECUTION_FAILED",
        "evidence_refs": ("failure-package.yaml",),
        "condition": "adapter_preflight_passed_then_execution_failed",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "adapter failure source expansion",
    },
    {
        "from_state": PUBLISH_ALLOWED,
        "to_state": ADAPTER_FAILED,
        "reason_code": "ADAPTER_EXECUTION_FAILED",
        "evidence_refs": ("failure-package.yaml",),
        "condition": "adapter_preflight_passed_then_execution_failed",
        "is_allowed": True,
        "source_of_truth": "P2D-2f section 4",
        "notes": "adapter failure source expansion",
    },
)

FORBIDDEN_TRANSITIONS: Final[tuple[dict[str, object], ...]] = (
    {
        "from_state": SCHEDULED_OR_STARTED,
        "to_state": PUBLISH_ALLOWED,
        "reason_code": "PRE_GATE_PUBLISH_ELIGIBILITY_FORBIDDEN",
        "evidence_refs": (),
        "condition": "none",
        "is_allowed": False,
        "source_of_truth": "P2D-2f section 5",
        "notes": "publish eligibility cannot precede gate evidence",
    },
    {
        "from_state": SCHEDULED_OR_STARTED,
        "to_state": NOOP_COMPLETED,
        "reason_code": "PRE_GATE_NOOP_COMPLETION_FORBIDDEN",
        "evidence_refs": (),
        "condition": "none",
        "is_allowed": False,
        "source_of_truth": "P2D-2f section 5",
        "notes": "noop completion cannot precede the runtime path",
    },
    {
        "from_state": CONFIG_BLOCKED,
        "to_state": RETRIEVING,
        "reason_code": "CONFIG_BLOCKED_TO_ACTIVE_FORBIDDEN",
        "evidence_refs": (),
        "condition": "same_run",
        "is_allowed": False,
        "source_of_truth": "P2D-2f section 5",
        "notes": "same-run terminal to active transition forbidden",
    },
    {
        "from_state": REVIEW_BLOCKED,
        "to_state": PUBLISH_ALLOWED,
        "reason_code": "REVIEW_BLOCKED_TO_PUBLISH_ALLOWED_FORBIDDEN",
        "evidence_refs": (),
        "condition": "same_run",
        "is_allowed": False,
        "source_of_truth": "P2D-2f section 5",
        "notes": "blocked review cannot claim publish eligibility",
    },
    {
        "from_state": SYSTEM_FAILED,
        "to_state": NOOP_COMPLETED,
        "reason_code": "SYSTEM_FAILED_TO_NOOP_COMPLETED_FORBIDDEN",
        "evidence_refs": (),
        "condition": "same_run",
        "is_allowed": False,
        "source_of_truth": "P2D-2f section 5",
        "notes": "system failure cannot claim noop success",
    },
    {
        "from_state": ADAPTER_FAILED,
        "to_state": NOOP_COMPLETED,
        "reason_code": "ADAPTER_FAILED_TO_NOOP_COMPLETED_FORBIDDEN",
        "evidence_refs": (),
        "condition": "same_run",
        "is_allowed": False,
        "source_of_truth": "P2D-2f section 5",
        "notes": "adapter failure cannot claim noop success",
    },
    {
        "from_state": PUBLISH_ALLOWED,
        "to_state": PASS_PUBLISHED_EXTERNAL_LABEL,
        "reason_code": "PUBLISH_ALLOWED_TO_PASS_PUBLISHED_FORBIDDEN",
        "evidence_refs": (),
        "condition": "mvp_noop",
        "is_allowed": False,
        "source_of_truth": "P2D-2f section 5",
        "notes": "PASS_PUBLISHED is an external reference label only",
    },
    {
        "from_state": NOOP_COMPLETED,
        "to_state": PASS_PUBLISHED_EXTERNAL_LABEL,
        "reason_code": "NOOP_COMPLETED_TO_PASS_PUBLISHED_FORBIDDEN",
        "evidence_refs": (),
        "condition": "mvp_noop",
        "is_allowed": False,
        "source_of_truth": "P2D-2f section 5",
        "notes": "NOOP_COMPLETED is not PASS_PUBLISHED",
    },
    {
        "from_state": "runtime_terminal_outcome",
        "to_state": "initial_active_or_intermediate_state",
        "reason_code": "TERMINAL_TO_ACTIVE_SAME_RUN_FORBIDDEN",
        "evidence_refs": (),
        "condition": "same_run",
        "is_allowed": False,
        "source_of_truth": "P2D-2f section 5",
        "notes": "same-run terminal to active transition family forbidden",
    },
    {
        "from_state": "any_state",
        "to_state": "public_url_claim",
        "reason_code": "PUBLIC_URL_CLAIM_FORBIDDEN",
        "evidence_refs": (),
        "condition": "mvp_noop",
        "is_allowed": False,
        "source_of_truth": "P2D-2f section 5",
        "notes": "public URL creation, reservation, faking, or implication forbidden",
    },
)

SAME_RUN_TERMINAL_TO_ACTIVE_SOURCE_STATES: Final[frozenset[str]] = (
    RUNTIME_TERMINAL_STATES
)

SAME_RUN_TERMINAL_TO_ACTIVE_DESTINATION_STATES: Final[frozenset[str]] = frozenset(
    (
        SCHEDULED_OR_STARTED,
        RETRIEVING,
        GENERATING,
        RENDERING,
        VALIDATING,
        EVALUATING,
        AUDITING,
        PUBLISH_ALLOWED,
    )
)

STATE_INVARIANTS: Final[tuple[str, ...]] = (
    "PASS_PUBLISHED excluded from MVP state enum",
    "NOOP_COMPLETED != PASS_PUBLISHED",
    "PUBLISH_ALLOWED is eligibility-only and non-terminal",
    "terminal-to-active same-run transitions forbidden",
    "blocked/failed states cannot claim success",
    "public URL creation/reservation/faking/implying is forbidden",
)
