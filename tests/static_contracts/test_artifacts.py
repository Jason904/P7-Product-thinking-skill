"""Static import-only contract tests for artifact constants."""

from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))

from ai_daily_publishing_system.core import artifacts


def test_artifact_catalog_contains_required_entries():
    expected_artifact_names = (
        "runtime-context.yaml",
        "runtime profile snapshot / config snapshot reference",
        "adapter-preflight-result.yaml",
        "source-manifest.yaml",
        "source-notes.md",
        "training-report.md",
        "reader.html",
        "validator-result.yaml",
        "rubric-review.stub.json",
        "rubric-review.json",
        "audit-review.stub.json",
        "audit-review.json",
        "publish-ledger.yaml",
        "notification-ledger.yaml",
        "artifact-hash.yaml",
        "run-ledger.yaml",
        "failure-package.yaml",
        "badcase-record.yaml",
    )

    assert artifacts.ARTIFACT_NAMES == expected_artifact_names
    assert len(artifacts.ARTIFACT_NAMES) == 18
    assert len(frozenset(artifacts.ARTIFACT_NAMES)) == len(artifacts.ARTIFACT_NAMES)


def test_artifact_classification_covers_catalog():
    classified_artifacts = frozenset(artifacts.ARTIFACT_CLASSIFICATION_BY_NAME)
    categorized_artifacts = (
        artifacts.PUBLIC_CANDIDATE_ARTIFACTS
        | artifacts.PUBLIC_SAFE_RENDER_SOURCE_ARTIFACTS
        | artifacts.PRIVATE_EVIDENCE_ARTIFACTS
        | artifacts.LEDGER_ARTIFACTS
        | artifacts.FAILURE_EVIDENCE_ARTIFACTS
        | artifacts.GOVERNANCE_EVIDENCE_ARTIFACTS
    )
    category_count = (
        len(artifacts.PUBLIC_CANDIDATE_ARTIFACTS)
        + len(artifacts.PUBLIC_SAFE_RENDER_SOURCE_ARTIFACTS)
        + len(artifacts.PRIVATE_EVIDENCE_ARTIFACTS)
        + len(artifacts.LEDGER_ARTIFACTS)
        + len(artifacts.FAILURE_EVIDENCE_ARTIFACTS)
        + len(artifacts.GOVERNANCE_EVIDENCE_ARTIFACTS)
    )

    assert classified_artifacts == frozenset(artifacts.ARTIFACT_NAMES)
    assert categorized_artifacts == frozenset(artifacts.ARTIFACT_NAMES)
    assert category_count == len(artifacts.ARTIFACT_NAMES)
    assert frozenset(artifacts.ARTIFACT_CLASSIFICATION_BY_NAME.values()) == frozenset(
        (
            artifacts.PUBLIC_CANDIDATE,
            artifacts.PUBLIC_SAFE_RENDER_SOURCE,
            artifacts.PRIVATE_EVIDENCE,
            artifacts.LEDGER,
            artifacts.FAILURE_EVIDENCE,
            artifacts.GOVERNANCE_EVIDENCE,
        )
    )


def test_public_candidate_boundary():
    assert artifacts.PUBLIC_CANDIDATE_ARTIFACTS == frozenset(("reader.html",))
    assert artifacts.PUBLIC_SAFE_RENDER_SOURCE_ARTIFACTS == frozenset(
        ("training-report.md",)
    )
    assert artifacts.ARTIFACT_CLASSIFICATION_BY_NAME["reader.html"] == (
        artifacts.PUBLIC_CANDIDATE
    )
    assert artifacts.ARTIFACT_CLASSIFICATION_BY_NAME["training-report.md"] == (
        artifacts.PUBLIC_SAFE_RENDER_SOURCE
    )
    assert "training-report.md" not in artifacts.PUBLIC_CANDIDATE_ARTIFACTS


def test_hash_phases_are_exact():
    assert artifacts.HASH_PHASES == (
        "pre-gate draft",
        "pre-gate update",
        "final",
    )


def test_write_order_contains_required_17_steps():
    assert len(artifacts.WRITE_ORDER_STEPS) == 17
    assert tuple(step["step"] for step in artifacts.WRITE_ORDER_STEPS) == tuple(
        str(index) for index in range(1, 18)
    )

    write_order_by_step = {
        step["step"]: (step["artifacts"], step["phase"])
        for step in artifacts.WRITE_ORDER_STEPS
    }
    expected_key_steps = {
        "1": (("runtime-context.yaml",), "runtime context"),
        "6": (("training-report.md",), "canonical report content"),
        "7": (("reader.html",), "public candidate"),
        "8": (
            ("artifact-hash.yaml",),
            "pre-gate draft for present pre-gate artifacts",
        ),
        "12": (
            ("artifact-hash.yaml",),
            "pre-gate update after review artifacts",
        ),
        "13": (
            ("run-ledger.yaml",),
            "Daily Publish Gate decision in run ledger draft",
        ),
        "14": (("publish-ledger.yaml",), "noop publish ledger"),
        "15": (("notification-ledger.yaml",), "noop notification ledger"),
        "16": (("artifact-hash.yaml",), "final update and finalize"),
        "17": (("run-ledger.yaml",), "final ledger seal"),
    }

    assert expected_key_steps.items() <= write_order_by_step.items()


def test_artifact_shape_fields_are_declared():
    assert artifacts.ARTIFACT_INVENTORY_FIELDS == (
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
    assert artifacts.ARTIFACT_WRITE_RESULT_FIELDS == (
        "artifact_name",
        "classification",
        "write_status",
        "artifact_reference",
        "actual_status",
        "redaction_status",
        "failure_state",
        "notes",
    )
    assert artifacts.ARTIFACT_SINK_RESULT_FIELDS == (
        "sink_name",
        "sink_mode",
        "accepted_artifacts",
        "rejected_artifacts",
        "write_results",
        "failure_state",
        "redaction_status",
        "notes",
    )


def test_artifact_invariants_capture_visibility_and_hash_boundaries():
    assert artifacts.ARTIFACT_INVARIANTS == (
        "reader.html only public candidate",
        "training-report.md not public candidate",
        "private evidence never rendered into public candidate",
        "present-only hash rule: only present artifacts may have hash entries",
        "skipped/absent artifacts are not hashed as present",
        "final hash before NOOP_COMPLETED",
        "no public URL",
        "no artifact examples",
    )
