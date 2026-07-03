"""Pure artifact inventory policy guard for the AI Daily Publishing System."""

from typing import Final

from ai_daily_publishing_system.core import artifacts


ARTIFACT_INVENTORY_ALLOWED: Final[str] = "ARTIFACT_INVENTORY_ALLOWED"
EMPTY_ARTIFACT_INVENTORY: Final[str] = "EMPTY_ARTIFACT_INVENTORY"
UNKNOWN_ARTIFACT: Final[str] = "UNKNOWN_ARTIFACT"
PUBLIC_CANDIDATE_NOT_IN_INVENTORY: Final[str] = (
    "PUBLIC_CANDIDATE_NOT_IN_INVENTORY"
)
DAILY_GATE_INPUT_NOT_IN_INVENTORY: Final[str] = (
    "DAILY_GATE_INPUT_NOT_IN_INVENTORY"
)
TRAINING_REPORT_MARKED_PUBLIC: Final[str] = (
    "TRAINING_REPORT_MARKED_PUBLIC"
)
PRIVATE_EVIDENCE_MARKED_PUBLIC: Final[str] = (
    "PRIVATE_EVIDENCE_MARKED_PUBLIC"
)
LEDGER_MARKED_PUBLIC: Final[str] = "LEDGER_MARKED_PUBLIC"
FAILURE_EVIDENCE_MARKED_PUBLIC: Final[str] = (
    "FAILURE_EVIDENCE_MARKED_PUBLIC"
)
GOVERNANCE_EVIDENCE_MARKED_PUBLIC: Final[str] = (
    "GOVERNANCE_EVIDENCE_MARKED_PUBLIC"
)
# Static forward-compatible fallback for a future known non-reader artifact
# with no dedicated public-candidate reason under the closed catalog.
NON_READER_PUBLIC_CANDIDATE: Final[str] = "NON_READER_PUBLIC_CANDIDATE"
POST_GATE_ARTIFACT_USED_AS_DAILY_GATE_INPUT: Final[str] = (
    "POST_GATE_ARTIFACT_USED_AS_DAILY_GATE_INPUT"
)
MISSING_PRE_GATE_HASH_EVIDENCE: Final[str] = (
    "MISSING_PRE_GATE_HASH_EVIDENCE"
)
PUBLIC_URL_BEHAVIOR_FORBIDDEN: Final[str] = "PUBLIC_URL_BEHAVIOR_FORBIDDEN"

_POLICY_SOURCE: Final[str] = (
    "artifact_inventory_policy.explain_artifact_inventory_policy"
)
_ARTIFACT_CATALOG_SOURCE: Final[str] = "artifacts.ARTIFACT_NAMES"
_PUBLIC_CANDIDATE_SOURCE: Final[str] = (
    "artifacts.PUBLIC_CANDIDATE_ARTIFACTS"
)
_CLASSIFICATION_SOURCE: Final[str] = (
    "artifacts.ARTIFACT_CLASSIFICATION_BY_NAME"
)
_PRE_GATE_HASH_SOURCE: Final[str] = (
    "caller-supplied pre_gate_hash_evidence_present"
)

_KNOWN_ARTIFACT_NAMES: Final[frozenset[str]] = frozenset(
    artifacts.ARTIFACT_NAMES
)
_POST_GATE_DAILY_GATE_INPUT_ARTIFACTS: Final[frozenset[str]] = frozenset(
    (
        artifacts.PUBLISH_LEDGER_ARTIFACT,
        artifacts.NOTIFICATION_LEDGER_ARTIFACT,
        artifacts.RUN_LEDGER_ARTIFACT,
    )
)
_DEDICATED_PUBLIC_BLOCK_ARTIFACTS: Final[frozenset[str]] = (
    artifacts.PUBLIC_SAFE_RENDER_SOURCE_ARTIFACTS
    | artifacts.PRIVATE_EVIDENCE_ARTIFACTS
    | artifacts.LEDGER_ARTIFACTS
    | artifacts.FAILURE_EVIDENCE_ARTIFACTS
    | artifacts.GOVERNANCE_EVIDENCE_ARTIFACTS
)
_POLICY_INVARIANTS: Final[tuple[str, ...]] = artifacts.ARTIFACT_INVARIANTS + (
    "generated post-gate ledgers are not Daily Publish Gate inputs",
    (
        "artifact inventory policy does not read files, write files, "
        "calculate hashes, write ledgers, publish, send notification, "
        "or create public URLs"
    ),
)


def _ordered_unique(values: tuple[str, ...]) -> tuple[str, ...]:
    ordered_values = ()
    seen_values = set()
    for value in values:
        if value not in seen_values:
            ordered_values = ordered_values + (value,)
            seen_values.add(value)
    return ordered_values


def _select_names(
    names: tuple[str, ...],
    selected_names: frozenset[str],
) -> tuple[str, ...]:
    return tuple(
        name for name in _ordered_unique(names) if name in selected_names
    )


def _unknown_names(
    artifact_names: tuple[str, ...],
    public_candidate_names: tuple[str, ...],
    daily_gate_input_names: tuple[str, ...],
) -> tuple[str, ...]:
    caller_supplied_names = (
        artifact_names + public_candidate_names + daily_gate_input_names
    )
    return tuple(
        name
        for name in _ordered_unique(caller_supplied_names)
        if name not in _KNOWN_ARTIFACT_NAMES
    )


def _missing_names(
    candidate_names: tuple[str, ...],
    inventory_names: frozenset[str],
) -> tuple[str, ...]:
    return tuple(
        name
        for name in _ordered_unique(candidate_names)
        if name not in inventory_names
    )


def _non_reader_public_candidates(
    public_candidate_names: tuple[str, ...],
) -> tuple[str, ...]:
    return tuple(
        name
        for name in _ordered_unique(public_candidate_names)
        if name in _KNOWN_ARTIFACT_NAMES
        and name not in artifacts.PUBLIC_CANDIDATE_ARTIFACTS
        and name not in _DEDICATED_PUBLIC_BLOCK_ARTIFACTS
    )


def _decision(
    artifact_names: tuple[str, ...],
    public_candidate_names: tuple[str, ...],
    daily_gate_input_names: tuple[str, ...],
    pre_gate_hash_evidence_present: bool,
    allowed: bool,
    reason_code: str,
    reason: str,
    source: str,
    unknown_artifact_names: tuple[str, ...],
    public_candidate_violations: tuple[str, ...],
    private_public_leak_candidates: tuple[str, ...],
    post_gate_daily_input_violations: tuple[str, ...],
    missing_inventory_artifacts: tuple[str, ...],
) -> dict[str, object]:
    return {
        "allowed": allowed,
        "reason_code": reason_code,
        "reason": reason,
        "source": source,
        "artifact_names": artifact_names,
        "public_candidate_names": public_candidate_names,
        "daily_gate_input_names": daily_gate_input_names,
        "pre_gate_hash_evidence_present": pre_gate_hash_evidence_present,
        "unknown_artifact_names": unknown_artifact_names,
        "public_candidate_violations": public_candidate_violations,
        "private_public_leak_candidates": private_public_leak_candidates,
        "post_gate_daily_input_violations": (
            post_gate_daily_input_violations
        ),
        "missing_inventory_artifacts": missing_inventory_artifacts,
        "invariant_refs": _POLICY_INVARIANTS,
    }


def explain_artifact_inventory_policy(
    artifact_names: tuple[str, ...],
    public_candidate_names: tuple[str, ...],
    daily_gate_input_names: tuple[str, ...],
    pre_gate_hash_evidence_present: bool,
) -> dict[str, object]:
    """Return a static inventory policy decision without side effects."""
    inventory_names = frozenset(artifact_names)
    unknown_artifact_names = _unknown_names(
        artifact_names,
        public_candidate_names,
        daily_gate_input_names,
    )
    public_candidate_missing_names = _missing_names(
        public_candidate_names,
        inventory_names,
    )
    daily_gate_input_missing_names = _missing_names(
        daily_gate_input_names,
        inventory_names,
    )
    missing_inventory_artifacts = _ordered_unique(
        public_candidate_missing_names + daily_gate_input_missing_names
    )
    training_report_public_candidates = _select_names(
        public_candidate_names,
        artifacts.PUBLIC_SAFE_RENDER_SOURCE_ARTIFACTS,
    )
    private_public_leak_candidates = _select_names(
        public_candidate_names,
        artifacts.PRIVATE_EVIDENCE_ARTIFACTS,
    )
    ledger_public_candidates = _select_names(
        public_candidate_names,
        artifacts.LEDGER_ARTIFACTS,
    )
    failure_public_candidates = _select_names(
        public_candidate_names,
        artifacts.FAILURE_EVIDENCE_ARTIFACTS,
    )
    governance_public_candidates = _select_names(
        public_candidate_names,
        artifacts.GOVERNANCE_EVIDENCE_ARTIFACTS,
    )
    non_reader_public_candidates = _non_reader_public_candidates(
        public_candidate_names
    )
    public_candidate_violations = _ordered_unique(
        training_report_public_candidates
        + private_public_leak_candidates
        + ledger_public_candidates
        + failure_public_candidates
        + governance_public_candidates
        + non_reader_public_candidates
    )
    post_gate_daily_input_violations = _select_names(
        daily_gate_input_names,
        _POST_GATE_DAILY_GATE_INPUT_ARTIFACTS,
    )

    if len(artifact_names) == 0:
        return _decision(
            artifact_names=artifact_names,
            public_candidate_names=public_candidate_names,
            daily_gate_input_names=daily_gate_input_names,
            pre_gate_hash_evidence_present=(
                pre_gate_hash_evidence_present
            ),
            allowed=False,
            reason_code=EMPTY_ARTIFACT_INVENTORY,
            reason="Caller-supplied artifact inventory must be non-empty.",
            source=_POLICY_SOURCE,
            unknown_artifact_names=unknown_artifact_names,
            public_candidate_violations=public_candidate_violations,
            private_public_leak_candidates=private_public_leak_candidates,
            post_gate_daily_input_violations=(
                post_gate_daily_input_violations
            ),
            missing_inventory_artifacts=missing_inventory_artifacts,
        )

    if unknown_artifact_names:
        return _decision(
            artifact_names=artifact_names,
            public_candidate_names=public_candidate_names,
            daily_gate_input_names=daily_gate_input_names,
            pre_gate_hash_evidence_present=(
                pre_gate_hash_evidence_present
            ),
            allowed=False,
            reason_code=UNKNOWN_ARTIFACT,
            reason=(
                "Every caller-supplied artifact name must be declared in "
                "the static artifact catalog."
            ),
            source=_ARTIFACT_CATALOG_SOURCE,
            unknown_artifact_names=unknown_artifact_names,
            public_candidate_violations=public_candidate_violations,
            private_public_leak_candidates=private_public_leak_candidates,
            post_gate_daily_input_violations=(
                post_gate_daily_input_violations
            ),
            missing_inventory_artifacts=missing_inventory_artifacts,
        )

    if public_candidate_missing_names:
        return _decision(
            artifact_names=artifact_names,
            public_candidate_names=public_candidate_names,
            daily_gate_input_names=daily_gate_input_names,
            pre_gate_hash_evidence_present=(
                pre_gate_hash_evidence_present
            ),
            allowed=False,
            reason_code=PUBLIC_CANDIDATE_NOT_IN_INVENTORY,
            reason=(
                "Every public candidate must also be present in the "
                "caller-supplied artifact inventory."
            ),
            source=_POLICY_SOURCE,
            unknown_artifact_names=unknown_artifact_names,
            public_candidate_violations=public_candidate_violations,
            private_public_leak_candidates=private_public_leak_candidates,
            post_gate_daily_input_violations=(
                post_gate_daily_input_violations
            ),
            missing_inventory_artifacts=missing_inventory_artifacts,
        )

    if post_gate_daily_input_violations:
        return _decision(
            artifact_names=artifact_names,
            public_candidate_names=public_candidate_names,
            daily_gate_input_names=daily_gate_input_names,
            pre_gate_hash_evidence_present=(
                pre_gate_hash_evidence_present
            ),
            allowed=False,
            reason_code=POST_GATE_ARTIFACT_USED_AS_DAILY_GATE_INPUT,
            reason=(
                "Generated post-gate ledger artifacts must not be used "
                "as Daily Gate inputs."
            ),
            source=_POLICY_SOURCE,
            unknown_artifact_names=unknown_artifact_names,
            public_candidate_violations=public_candidate_violations,
            private_public_leak_candidates=private_public_leak_candidates,
            post_gate_daily_input_violations=(
                post_gate_daily_input_violations
            ),
            missing_inventory_artifacts=missing_inventory_artifacts,
        )

    if daily_gate_input_missing_names:
        return _decision(
            artifact_names=artifact_names,
            public_candidate_names=public_candidate_names,
            daily_gate_input_names=daily_gate_input_names,
            pre_gate_hash_evidence_present=(
                pre_gate_hash_evidence_present
            ),
            allowed=False,
            reason_code=DAILY_GATE_INPUT_NOT_IN_INVENTORY,
            reason=(
                "Every Daily Gate input must also be present in the "
                "caller-supplied artifact inventory."
            ),
            source=_POLICY_SOURCE,
            unknown_artifact_names=unknown_artifact_names,
            public_candidate_violations=public_candidate_violations,
            private_public_leak_candidates=private_public_leak_candidates,
            post_gate_daily_input_violations=(
                post_gate_daily_input_violations
            ),
            missing_inventory_artifacts=missing_inventory_artifacts,
        )

    if training_report_public_candidates:
        return _decision(
            artifact_names=artifact_names,
            public_candidate_names=public_candidate_names,
            daily_gate_input_names=daily_gate_input_names,
            pre_gate_hash_evidence_present=(
                pre_gate_hash_evidence_present
            ),
            allowed=False,
            reason_code=TRAINING_REPORT_MARKED_PUBLIC,
            reason=(
                "training-report.md is public-safe render source and "
                "canonical report content, not a public candidate."
            ),
            source=_CLASSIFICATION_SOURCE,
            unknown_artifact_names=unknown_artifact_names,
            public_candidate_violations=public_candidate_violations,
            private_public_leak_candidates=private_public_leak_candidates,
            post_gate_daily_input_violations=(
                post_gate_daily_input_violations
            ),
            missing_inventory_artifacts=missing_inventory_artifacts,
        )

    if private_public_leak_candidates:
        return _decision(
            artifact_names=artifact_names,
            public_candidate_names=public_candidate_names,
            daily_gate_input_names=daily_gate_input_names,
            pre_gate_hash_evidence_present=(
                pre_gate_hash_evidence_present
            ),
            allowed=False,
            reason_code=PRIVATE_EVIDENCE_MARKED_PUBLIC,
            reason="Private evidence artifacts cannot be public candidates.",
            source=_CLASSIFICATION_SOURCE,
            unknown_artifact_names=unknown_artifact_names,
            public_candidate_violations=public_candidate_violations,
            private_public_leak_candidates=private_public_leak_candidates,
            post_gate_daily_input_violations=(
                post_gate_daily_input_violations
            ),
            missing_inventory_artifacts=missing_inventory_artifacts,
        )

    if ledger_public_candidates:
        return _decision(
            artifact_names=artifact_names,
            public_candidate_names=public_candidate_names,
            daily_gate_input_names=daily_gate_input_names,
            pre_gate_hash_evidence_present=(
                pre_gate_hash_evidence_present
            ),
            allowed=False,
            reason_code=LEDGER_MARKED_PUBLIC,
            reason="Ledger artifacts cannot be public candidates.",
            source=_CLASSIFICATION_SOURCE,
            unknown_artifact_names=unknown_artifact_names,
            public_candidate_violations=public_candidate_violations,
            private_public_leak_candidates=private_public_leak_candidates,
            post_gate_daily_input_violations=(
                post_gate_daily_input_violations
            ),
            missing_inventory_artifacts=missing_inventory_artifacts,
        )

    if failure_public_candidates:
        return _decision(
            artifact_names=artifact_names,
            public_candidate_names=public_candidate_names,
            daily_gate_input_names=daily_gate_input_names,
            pre_gate_hash_evidence_present=(
                pre_gate_hash_evidence_present
            ),
            allowed=False,
            reason_code=FAILURE_EVIDENCE_MARKED_PUBLIC,
            reason="Failure evidence cannot be a public candidate.",
            source=_CLASSIFICATION_SOURCE,
            unknown_artifact_names=unknown_artifact_names,
            public_candidate_violations=public_candidate_violations,
            private_public_leak_candidates=private_public_leak_candidates,
            post_gate_daily_input_violations=(
                post_gate_daily_input_violations
            ),
            missing_inventory_artifacts=missing_inventory_artifacts,
        )

    if governance_public_candidates:
        return _decision(
            artifact_names=artifact_names,
            public_candidate_names=public_candidate_names,
            daily_gate_input_names=daily_gate_input_names,
            pre_gate_hash_evidence_present=(
                pre_gate_hash_evidence_present
            ),
            allowed=False,
            reason_code=GOVERNANCE_EVIDENCE_MARKED_PUBLIC,
            reason="Governance evidence cannot be a public candidate.",
            source=_CLASSIFICATION_SOURCE,
            unknown_artifact_names=unknown_artifact_names,
            public_candidate_violations=public_candidate_violations,
            private_public_leak_candidates=private_public_leak_candidates,
            post_gate_daily_input_violations=(
                post_gate_daily_input_violations
            ),
            missing_inventory_artifacts=missing_inventory_artifacts,
        )

    if non_reader_public_candidates:
        return _decision(
            artifact_names=artifact_names,
            public_candidate_names=public_candidate_names,
            daily_gate_input_names=daily_gate_input_names,
            pre_gate_hash_evidence_present=(
                pre_gate_hash_evidence_present
            ),
            allowed=False,
            reason_code=NON_READER_PUBLIC_CANDIDATE,
            reason="reader.html is the only allowed public candidate.",
            source=_PUBLIC_CANDIDATE_SOURCE,
            unknown_artifact_names=unknown_artifact_names,
            public_candidate_violations=public_candidate_violations,
            private_public_leak_candidates=private_public_leak_candidates,
            post_gate_daily_input_violations=(
                post_gate_daily_input_violations
            ),
            missing_inventory_artifacts=missing_inventory_artifacts,
        )

    if pre_gate_hash_evidence_present is False:
        return _decision(
            artifact_names=artifact_names,
            public_candidate_names=public_candidate_names,
            daily_gate_input_names=daily_gate_input_names,
            pre_gate_hash_evidence_present=(
                pre_gate_hash_evidence_present
            ),
            allowed=False,
            reason_code=MISSING_PRE_GATE_HASH_EVIDENCE,
            reason=(
                "Caller-supplied pre-gate hash evidence marker must be "
                "present before Daily Gate-ready inventory is allowed."
            ),
            source=_PRE_GATE_HASH_SOURCE,
            unknown_artifact_names=unknown_artifact_names,
            public_candidate_violations=public_candidate_violations,
            private_public_leak_candidates=private_public_leak_candidates,
            post_gate_daily_input_violations=(
                post_gate_daily_input_violations
            ),
            missing_inventory_artifacts=missing_inventory_artifacts,
        )

    return _decision(
        artifact_names=artifact_names,
        public_candidate_names=public_candidate_names,
        daily_gate_input_names=daily_gate_input_names,
        pre_gate_hash_evidence_present=pre_gate_hash_evidence_present,
        allowed=True,
        reason_code=ARTIFACT_INVENTORY_ALLOWED,
        reason=(
            "Caller-supplied artifact inventory fields satisfy the "
            "static catalog, public/private, pre-gate, and post-gate "
            "inventory policy; no artifact IO, hash calculation, gate "
            "execution, ledger write, publish action, notification "
            "action, or public URL behavior is executed."
        ),
        source=_POLICY_SOURCE,
        unknown_artifact_names=unknown_artifact_names,
        public_candidate_violations=public_candidate_violations,
        private_public_leak_candidates=private_public_leak_candidates,
        post_gate_daily_input_violations=(
            post_gate_daily_input_violations
        ),
        missing_inventory_artifacts=missing_inventory_artifacts,
    )


def is_artifact_inventory_allowed(
    artifact_names: tuple[str, ...],
    public_candidate_names: tuple[str, ...],
    daily_gate_input_names: tuple[str, ...],
    pre_gate_hash_evidence_present: bool,
) -> bool:
    """Return only the boolean result from the inventory explanation."""
    return bool(
        explain_artifact_inventory_policy(
            artifact_names,
            public_candidate_names,
            daily_gate_input_names,
            pre_gate_hash_evidence_present,
        )["allowed"]
    )
