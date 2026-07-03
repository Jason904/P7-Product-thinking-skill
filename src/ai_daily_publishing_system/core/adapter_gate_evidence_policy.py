"""Pure Adapter Gate evidence policy guard for the publishing system."""

from typing import Final

from ai_daily_publishing_system.core import gates


ADAPTER_GATE_EVIDENCE_ALLOWED: Final[str] = (
    "ADAPTER_GATE_EVIDENCE_ALLOWED"
)
RUNTIME_CONTEXT_MISSING: Final[str] = "RUNTIME_CONTEXT_MISSING"
RUNTIME_PROFILE_SNAPSHOT_REF_MISSING: Final[str] = (
    "RUNTIME_PROFILE_SNAPSHOT_REF_MISSING"
)
RUNTIME_PROFILE_MODE_NOT_MANUAL_LOCAL_NOOP: Final[str] = (
    "RUNTIME_PROFILE_MODE_NOT_MANUAL_LOCAL_NOOP"
)
CONFIG_SNAPSHOT_REF_MISSING: Final[str] = (
    "CONFIG_SNAPSHOT_REF_MISSING"
)
ADAPTER_CONFIGURATION_NOT_DECLARED: Final[str] = (
    "ADAPTER_CONFIGURATION_NOT_DECLARED"
)
REQUIRED_CREDENTIAL_MARKERS_MISSING: Final[str] = (
    "REQUIRED_CREDENTIAL_MARKERS_MISSING"
)
CREDENTIAL_REDACTION_NOT_PASSED: Final[str] = (
    "CREDENTIAL_REDACTION_NOT_PASSED"
)
PUBLISH_MODE_NOT_NOOP: Final[str] = "PUBLISH_MODE_NOT_NOOP"
NOTIFICATION_MODE_NOT_NOOP: Final[str] = (
    "NOTIFICATION_MODE_NOT_NOOP"
)
EVAL_MODE_NOT_DECLARED: Final[str] = "EVAL_MODE_NOT_DECLARED"
ADAPTER_CAPABILITY_MARKERS_MISSING: Final[str] = (
    "ADAPTER_CAPABILITY_MARKERS_MISSING"
)
NOOP_POLICY_MARKERS_MISSING: Final[str] = (
    "NOOP_POLICY_MARKERS_MISSING"
)
DISABLED_EXTERNAL_ADAPTERS_NOT_DECLARED: Final[str] = (
    "DISABLED_EXTERNAL_ADAPTERS_NOT_DECLARED"
)
ENVIRONMENT_SAFETY_MARKER_MISSING: Final[str] = (
    "ENVIRONMENT_SAFETY_MARKER_MISSING"
)
BLOCKING_ADAPTER_MARKERS_PRESENT: Final[str] = (
    "BLOCKING_ADAPTER_MARKERS_PRESENT"
)

ADAPTER_GATE_EVIDENCE_POLICY_REASON_CODES: Final[tuple[str, ...]] = (
    RUNTIME_CONTEXT_MISSING,
    RUNTIME_PROFILE_SNAPSHOT_REF_MISSING,
    RUNTIME_PROFILE_MODE_NOT_MANUAL_LOCAL_NOOP,
    CONFIG_SNAPSHOT_REF_MISSING,
    ADAPTER_CONFIGURATION_NOT_DECLARED,
    REQUIRED_CREDENTIAL_MARKERS_MISSING,
    CREDENTIAL_REDACTION_NOT_PASSED,
    PUBLISH_MODE_NOT_NOOP,
    NOTIFICATION_MODE_NOT_NOOP,
    EVAL_MODE_NOT_DECLARED,
    ADAPTER_CAPABILITY_MARKERS_MISSING,
    NOOP_POLICY_MARKERS_MISSING,
    DISABLED_EXTERNAL_ADAPTERS_NOT_DECLARED,
    ENVIRONMENT_SAFETY_MARKER_MISSING,
    BLOCKING_ADAPTER_MARKERS_PRESENT,
    ADAPTER_GATE_EVIDENCE_ALLOWED,
)

_POLICY_SOURCE: Final[str] = (
    "adapter_gate_evidence_policy.explain_adapter_gate_evidence_policy"
)
_LOCAL_POLICY_INVARIANTS: Final[tuple[str, ...]] = (
    "adapter_gate_evidence_policy_only",
    "evidence_policy_not_adapter_gate_execution",
    "allowed_not_adapter_gate_pass",
    "allowed_not_retrieving",
    "blocked_not_config_blocked",
    "no_runtime_context_config_or_credential_read",
    "no_adapter_preflight",
    "no_external_adapter_call",
    "no_raw_credentials",
    "no_quality_pass_no_public_url",
    "no_artifact_or_review_io",
    "no_hash_calculation",
    "no_ledger_write",
    "no_publish_or_notification",
    "no_public_url_behavior",
    "external_agents_cannot_bypass_later_gates",
)
_POLICY_INVARIANTS: Final[tuple[str, ...]] = (
    gates.GATE_INVARIANTS + _LOCAL_POLICY_INVARIANTS
)
_REASON_TEXT_ENTRIES: Final[tuple[tuple[str, str], ...]] = (
    (
        RUNTIME_CONTEXT_MISSING,
        "Caller-supplied runtime context presence marker is missing; "
        "the policy does not read runtime context.",
    ),
    (
        RUNTIME_PROFILE_SNAPSHOT_REF_MISSING,
        "Caller-supplied runtime profile snapshot reference marker is "
        "missing; the policy does not parse profile references.",
    ),
    (
        RUNTIME_PROFILE_MODE_NOT_MANUAL_LOCAL_NOOP,
        "Caller-supplied runtime profile mode marker does not confirm "
        "the manual_local_noop MVP mode.",
    ),
    (
        CONFIG_SNAPSHOT_REF_MISSING,
        "Caller-supplied config snapshot reference marker is missing; "
        "the policy does not read configuration.",
    ),
    (
        ADAPTER_CONFIGURATION_NOT_DECLARED,
        "Caller-supplied Adapter configuration declaration marker is "
        "missing.",
    ),
    (
        REQUIRED_CREDENTIAL_MARKERS_MISSING,
        "Caller-supplied required credential presence markers are "
        "missing; the policy does not read credential values.",
    ),
    (
        CREDENTIAL_REDACTION_NOT_PASSED,
        "Caller-supplied credential redaction marker has not passed; "
        "the policy does not perform redaction.",
    ),
    (
        PUBLISH_MODE_NOT_NOOP,
        "Caller-supplied publish mode marker does not confirm noop.",
    ),
    (
        NOTIFICATION_MODE_NOT_NOOP,
        "Caller-supplied notification mode marker does not confirm "
        "noop or disabled behavior.",
    ),
    (
        EVAL_MODE_NOT_DECLARED,
        "Caller-supplied eval mode declaration marker is missing; the "
        "policy does not execute evaluation.",
    ),
    (
        ADAPTER_CAPABILITY_MARKERS_MISSING,
        "Caller-supplied Adapter capability markers are missing; the "
        "policy does not probe Adapter capabilities.",
    ),
    (
        NOOP_POLICY_MARKERS_MISSING,
        "Caller-supplied noop policy markers are missing.",
    ),
    (
        DISABLED_EXTERNAL_ADAPTERS_NOT_DECLARED,
        "Caller-supplied declaration that external Adapters are "
        "disabled is missing.",
    ),
    (
        ENVIRONMENT_SAFETY_MARKER_MISSING,
        "Caller-supplied environment safety marker is missing; the "
        "policy does not read the environment.",
    ),
    (
        BLOCKING_ADAPTER_MARKERS_PRESENT,
        "Caller-supplied blocking Adapter markers are present; the "
        "policy does not parse Adapter failures.",
    ),
    (
        ADAPTER_GATE_EVIDENCE_ALLOWED,
        "Caller-supplied evidence markers satisfy the static Adapter "
        "Gate evidence policy. This does not mean Adapter Gate PASS, "
        "does not produce RETRIEVING, and executes no gate, mapping, "
        "transition, runtime/config/credential read, Adapter preflight "
        "or call, artifact or review IO, hash calculation, ledger "
        "write, publish, notification, or public URL behavior.",
    ),
)


def _reason_text(reason_code: str) -> str:
    for code, text in _REASON_TEXT_ENTRIES:
        if code == reason_code:
            return text
    return "Unknown Adapter Gate evidence policy result."


def _decision(
    *,
    markers: dict[str, bool],
    allowed: bool,
    reason_code: str,
    missing_evidence_markers: tuple[str, ...],
    failed_policy_markers: tuple[str, ...],
    mode_policy_violations: tuple[str, ...],
    adapter_policy_violations: tuple[str, ...],
) -> dict[str, object]:
    return {
        "allowed": allowed,
        "reason_code": reason_code,
        "reason": _reason_text(reason_code),
        "source": _POLICY_SOURCE,
        **markers,
        "missing_evidence_markers": missing_evidence_markers,
        "failed_policy_markers": failed_policy_markers,
        "mode_policy_violations": mode_policy_violations,
        "adapter_policy_violations": adapter_policy_violations,
        "invariant_refs": _POLICY_INVARIANTS,
    }


def explain_adapter_gate_evidence_policy(
    *,
    runtime_context_present: bool,
    runtime_profile_snapshot_ref_present: bool,
    runtime_profile_mode_is_manual_local_noop: bool,
    config_snapshot_ref_present: bool,
    adapter_configuration_declared: bool,
    required_credential_markers_present: bool,
    credential_redaction_passed: bool,
    publish_mode_is_noop: bool,
    notification_mode_is_noop: bool,
    eval_mode_declared: bool,
    adapter_capability_markers_present: bool,
    noop_policy_markers_present: bool,
    disabled_external_adapters_declared: bool,
    environment_safety_marker_present: bool,
    blocking_adapter_markers_present: bool,
) -> dict[str, object]:
    """Explain caller-supplied Adapter Gate evidence marker policy."""
    markers = {
        "runtime_context_present": runtime_context_present,
        "runtime_profile_snapshot_ref_present": (
            runtime_profile_snapshot_ref_present
        ),
        "runtime_profile_mode_is_manual_local_noop": (
            runtime_profile_mode_is_manual_local_noop
        ),
        "config_snapshot_ref_present": config_snapshot_ref_present,
        "adapter_configuration_declared": adapter_configuration_declared,
        "required_credential_markers_present": (
            required_credential_markers_present
        ),
        "credential_redaction_passed": credential_redaction_passed,
        "publish_mode_is_noop": publish_mode_is_noop,
        "notification_mode_is_noop": notification_mode_is_noop,
        "eval_mode_declared": eval_mode_declared,
        "adapter_capability_markers_present": (
            adapter_capability_markers_present
        ),
        "noop_policy_markers_present": noop_policy_markers_present,
        "disabled_external_adapters_declared": (
            disabled_external_adapters_declared
        ),
        "environment_safety_marker_present": (
            environment_safety_marker_present
        ),
        "blocking_adapter_markers_present": (
            blocking_adapter_markers_present
        ),
    }
    missing_evidence_markers = tuple(
        marker_name
        for marker_name, marker_present in (
            ("runtime_context_present", runtime_context_present),
            (
                "runtime_profile_snapshot_ref_present",
                runtime_profile_snapshot_ref_present,
            ),
            (
                "config_snapshot_ref_present",
                config_snapshot_ref_present,
            ),
            (
                "adapter_configuration_declared",
                adapter_configuration_declared,
            ),
            (
                "required_credential_markers_present",
                required_credential_markers_present,
            ),
            ("eval_mode_declared", eval_mode_declared),
            (
                "adapter_capability_markers_present",
                adapter_capability_markers_present,
            ),
            (
                "noop_policy_markers_present",
                noop_policy_markers_present,
            ),
            (
                "disabled_external_adapters_declared",
                disabled_external_adapters_declared,
            ),
            (
                "environment_safety_marker_present",
                environment_safety_marker_present,
            ),
        )
        if marker_present is False
    )
    failed_policy_markers = tuple(
        marker_name
        for marker_name, marker_failed in (
            (
                "runtime_profile_mode_is_manual_local_noop",
                runtime_profile_mode_is_manual_local_noop is False,
            ),
            (
                "credential_redaction_passed",
                credential_redaction_passed is False,
            ),
            (
                "publish_mode_is_noop",
                publish_mode_is_noop is False,
            ),
            (
                "notification_mode_is_noop",
                notification_mode_is_noop is False,
            ),
            (
                "blocking_adapter_markers_present",
                blocking_adapter_markers_present is True,
            ),
        )
        if marker_failed
    )
    mode_policy_violations = tuple(
        marker_name
        for marker_name, marker_violated in (
            (
                "runtime_profile_mode_is_manual_local_noop",
                runtime_profile_mode_is_manual_local_noop is False,
            ),
            (
                "publish_mode_is_noop",
                publish_mode_is_noop is False,
            ),
            (
                "notification_mode_is_noop",
                notification_mode_is_noop is False,
            ),
        )
        if marker_violated
    )
    adapter_policy_violations = tuple(
        marker_name
        for marker_name, marker_violated in (
            (
                "adapter_configuration_declared",
                adapter_configuration_declared is False,
            ),
            (
                "adapter_capability_markers_present",
                adapter_capability_markers_present is False,
            ),
            (
                "disabled_external_adapters_declared",
                disabled_external_adapters_declared is False,
            ),
            (
                "blocking_adapter_markers_present",
                blocking_adapter_markers_present is True,
            ),
        )
        if marker_violated
    )
    prioritized_failures = (
        (runtime_context_present is False, RUNTIME_CONTEXT_MISSING),
        (
            runtime_profile_snapshot_ref_present is False,
            RUNTIME_PROFILE_SNAPSHOT_REF_MISSING,
        ),
        (
            runtime_profile_mode_is_manual_local_noop is False,
            RUNTIME_PROFILE_MODE_NOT_MANUAL_LOCAL_NOOP,
        ),
        (
            config_snapshot_ref_present is False,
            CONFIG_SNAPSHOT_REF_MISSING,
        ),
        (
            adapter_configuration_declared is False,
            ADAPTER_CONFIGURATION_NOT_DECLARED,
        ),
        (
            required_credential_markers_present is False,
            REQUIRED_CREDENTIAL_MARKERS_MISSING,
        ),
        (
            credential_redaction_passed is False,
            CREDENTIAL_REDACTION_NOT_PASSED,
        ),
        (publish_mode_is_noop is False, PUBLISH_MODE_NOT_NOOP),
        (
            notification_mode_is_noop is False,
            NOTIFICATION_MODE_NOT_NOOP,
        ),
        (eval_mode_declared is False, EVAL_MODE_NOT_DECLARED),
        (
            adapter_capability_markers_present is False,
            ADAPTER_CAPABILITY_MARKERS_MISSING,
        ),
        (
            noop_policy_markers_present is False,
            NOOP_POLICY_MARKERS_MISSING,
        ),
        (
            disabled_external_adapters_declared is False,
            DISABLED_EXTERNAL_ADAPTERS_NOT_DECLARED,
        ),
        (
            environment_safety_marker_present is False,
            ENVIRONMENT_SAFETY_MARKER_MISSING,
        ),
        (
            blocking_adapter_markers_present is True,
            BLOCKING_ADAPTER_MARKERS_PRESENT,
        ),
    )

    for is_blocked, reason_code in prioritized_failures:
        if is_blocked:
            return _decision(
                markers=markers,
                allowed=False,
                reason_code=reason_code,
                missing_evidence_markers=missing_evidence_markers,
                failed_policy_markers=failed_policy_markers,
                mode_policy_violations=mode_policy_violations,
                adapter_policy_violations=adapter_policy_violations,
            )

    return _decision(
        markers=markers,
        allowed=True,
        reason_code=ADAPTER_GATE_EVIDENCE_ALLOWED,
        missing_evidence_markers=missing_evidence_markers,
        failed_policy_markers=failed_policy_markers,
        mode_policy_violations=mode_policy_violations,
        adapter_policy_violations=adapter_policy_violations,
    )


def is_adapter_gate_evidence_allowed(
    *,
    runtime_context_present: bool,
    runtime_profile_snapshot_ref_present: bool,
    runtime_profile_mode_is_manual_local_noop: bool,
    config_snapshot_ref_present: bool,
    adapter_configuration_declared: bool,
    required_credential_markers_present: bool,
    credential_redaction_passed: bool,
    publish_mode_is_noop: bool,
    notification_mode_is_noop: bool,
    eval_mode_declared: bool,
    adapter_capability_markers_present: bool,
    noop_policy_markers_present: bool,
    disabled_external_adapters_declared: bool,
    environment_safety_marker_present: bool,
    blocking_adapter_markers_present: bool,
) -> bool:
    """Return only the boolean result from the evidence explanation."""
    return bool(
        explain_adapter_gate_evidence_policy(
            runtime_context_present=runtime_context_present,
            runtime_profile_snapshot_ref_present=(
                runtime_profile_snapshot_ref_present
            ),
            runtime_profile_mode_is_manual_local_noop=(
                runtime_profile_mode_is_manual_local_noop
            ),
            config_snapshot_ref_present=config_snapshot_ref_present,
            adapter_configuration_declared=adapter_configuration_declared,
            required_credential_markers_present=(
                required_credential_markers_present
            ),
            credential_redaction_passed=credential_redaction_passed,
            publish_mode_is_noop=publish_mode_is_noop,
            notification_mode_is_noop=notification_mode_is_noop,
            eval_mode_declared=eval_mode_declared,
            adapter_capability_markers_present=(
                adapter_capability_markers_present
            ),
            noop_policy_markers_present=noop_policy_markers_present,
            disabled_external_adapters_declared=(
                disabled_external_adapters_declared
            ),
            environment_safety_marker_present=(
                environment_safety_marker_present
            ),
            blocking_adapter_markers_present=(
                blocking_adapter_markers_present
            ),
        )["allowed"]
    )
