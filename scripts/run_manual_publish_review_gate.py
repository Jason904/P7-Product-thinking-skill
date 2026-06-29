#!/usr/bin/env python3
"""Run the P2C-3 manual publish review dry-run gate.

The gate consumes a P2C-2 release-candidate package and decides whether it is
ready for a separate manual publish review. It never performs formal publishing,
public website updates, notifications, automatic publishing, or live LLM review.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Any

import yaml


RUBRIC_DIR_REL = Path("docs/quality/rubric-v2.1")
DEFAULT_POLICY_REL = RUBRIC_DIR_REL / "p2c3-manual-publish-review-policy.yaml"
DEFAULT_OUTPUT_REL = RUBRIC_DIR_REL / "shadow-runs" / "p2c3-manual-publish-review"
DECISION_NAME = "manual-publish-review-decision.yaml"
REPORT_NAME = "manual-publish-review-report.md"
PACKAGE_DIR_NAME = "manual-publish-review-package"

REQUIRED_PACKAGE_FILES = {
    "release-candidate-manifest.yaml": "RELEASE_CANDIDATE_MANIFEST_MISSING",
    "source-observation-ledger.yaml": "SOURCE_OBSERVATION_LEDGER_MISSING",
    "human-confirmation-decision.yaml": "HUMAN_CONFIRMATION_DECISION_MISSING",
    "manual-publish-review-checklist.md": "MANUAL_PUBLISH_CHECKLIST_MISSING",
}

BOUNDARY_FLAGS = {
    "formal_publish_allowed": "FORMAL_PUBLISH_ALREADY_ALLOWED",
    "public_site_updated": "PUBLIC_SITE_ALREADY_UPDATED",
    "user_notification_sent": "USER_NOTIFICATION_ALREADY_SENT",
    "live_llm_review": "LIVE_LLM_REVIEW_USED",
    "automatic_publishing": "AUTOMATIC_PUBLISHING_ENABLED",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY_REL)
    parser.add_argument("--release-candidate-package", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_REL)
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    decision = run_manual_publish_review_gate(
        project_root=project_root,
        policy_path=resolve_path(project_root, args.policy),
        release_candidate_package=resolve_path(project_root, args.release_candidate_package),
        output_dir=resolve_path(project_root, args.output_dir),
    )
    print(yaml.safe_dump(decision, allow_unicode=True, sort_keys=False), end="")
    return 0


def run_manual_publish_review_gate(
    *,
    project_root: Path,
    policy_path: Path,
    release_candidate_package: Path,
    output_dir: Path,
) -> dict[str, Any]:
    policy = read_yaml(policy_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_package_dir = output_dir / PACKAGE_DIR_NAME
    if output_package_dir.exists():
        shutil.rmtree(output_package_dir)
    output_package_dir.mkdir(parents=True, exist_ok=True)

    source_manifest_path = release_candidate_package / "release-candidate-manifest.yaml"
    source_decision_path = release_candidate_package / "human-confirmation-decision.yaml"

    manifest = read_yaml(source_manifest_path) if source_manifest_path.is_file() else {}
    human_decision = read_yaml(source_decision_path) if source_decision_path.is_file() else {}
    blocked_reasons = derive_blocked_reasons(
        package_dir=release_candidate_package,
        manifest=manifest,
        human_decision=human_decision,
    )
    blocked = bool(blocked_reasons)
    manual_publish_review_ready = not blocked

    decision = {
        "stage": "P2C-3",
        "gate_type": "manual_publish_review_dry_run",
        "policy_path": rel(project_root, policy_path),
        "source_release_candidate_package": rel(project_root, release_candidate_package),
        "not_formal_publish": True,
        "manual_publish_review_ready": manual_publish_review_ready,
        "manual_publish_review_ready_is_not_publish": bool(
            policy["manual_publish_review_ready_is_not_publish"]
        ),
        "formal_publish_allowed": False,
        "public_site_updated": False,
        "user_notification_sent": False,
        "live_llm_review": False,
        "automatic_publishing": False,
        "requires_final_human_publish_confirmation": bool(
            policy["requires_final_human_publish_confirmation"]
        ),
        "blocked": blocked,
        "blocked_reasons": blocked_reasons,
        "manual_publish_review_package_path": rel(project_root, output_package_dir),
        "source_release_candidate_created": bool(
            manifest.get("release_candidate_created", human_decision.get("release_candidate_created", False))
        ),
        "source_release_candidate_blocked": bool(human_decision.get("blocked", False)),
        "next_action": (
            "Route to manual publish review. Final human publish confirmation is still required."
            if manual_publish_review_ready
            else "Resolve blocked reasons before manual publish review."
        ),
    }

    write_yaml(output_dir / DECISION_NAME, decision)
    (output_dir / REPORT_NAME).write_text(build_report(decision), encoding="utf-8")
    write_manual_publish_review_package(
        project_root=project_root,
        source_package_dir=release_candidate_package,
        output_package_dir=output_package_dir,
        decision=decision,
    )
    return decision


def derive_blocked_reasons(
    *,
    package_dir: Path,
    manifest: dict[str, Any],
    human_decision: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if not package_dir.is_dir():
        reasons.append("RELEASE_CANDIDATE_PACKAGE_MISSING")
        return reasons

    for file_name, reason in REQUIRED_PACKAGE_FILES.items():
        if not (package_dir / file_name).is_file():
            reasons.append(reason)

    if manifest and not bool(manifest.get("release_candidate_created", False)):
        reasons.append("RELEASE_CANDIDATE_NOT_CREATED")
    if human_decision and not bool(human_decision.get("release_candidate_created", False)):
        reasons.append("RELEASE_CANDIDATE_NOT_CREATED")

    if bool(human_decision.get("blocked", False)):
        reasons.append("RELEASE_CANDIDATE_BLOCKED")

    if manifest and not bool(manifest.get("release_candidate_is_not_publish", False)):
        reasons.append("RELEASE_CANDIDATE_IS_PUBLISH")
    if human_decision and not bool(human_decision.get("release_candidate_is_not_publish", False)):
        reasons.append("RELEASE_CANDIDATE_IS_PUBLISH")

    if manifest and not bool(
        manifest.get("manual_publish_review_required_after_release_candidate", False)
    ):
        reasons.append("MANUAL_PUBLISH_REVIEW_NOT_REQUIRED")

    for flag, reason in BOUNDARY_FLAGS.items():
        if bool(manifest.get(flag, False)) or bool(human_decision.get(flag, False)):
            reasons.append(reason)

    return unique_preserving_order(reasons)


def write_manual_publish_review_package(
    *,
    project_root: Path,
    source_package_dir: Path,
    output_package_dir: Path,
    decision: dict[str, Any],
) -> None:
    copy_or_write_missing_marker(
        source_package_dir / "release-candidate-manifest.yaml",
        output_package_dir / "source-release-candidate-manifest.yaml",
        "RELEASE_CANDIDATE_MANIFEST_MISSING",
    )
    copy_or_write_missing_marker(
        source_package_dir / "human-confirmation-decision.yaml",
        output_package_dir / "source-human-confirmation-decision.yaml",
        "HUMAN_CONFIRMATION_DECISION_MISSING",
    )
    write_yaml(output_package_dir / DECISION_NAME, decision)
    (output_package_dir / "final-human-publish-checklist.md").write_text(
        build_final_human_publish_checklist(project_root, source_package_dir, decision),
        encoding="utf-8",
    )


def copy_or_write_missing_marker(source: Path, destination: Path, reason: str) -> None:
    if source.is_file():
        shutil.copyfile(source, destination)
        return
    write_yaml(
        destination,
        {
            "source_file": source.name,
            "source_missing": True,
            "blocked_reason": reason,
        },
    )


def build_report(decision: dict[str, Any]) -> str:
    blocked_reasons = decision["blocked_reasons"] or ["No P2C-3 dry-run gate blockers."]
    return "\n".join(
        [
            "# P2C-3 Manual Publish Review Runtime Report",
            "",
            "## Boundary",
            "",
            "- Not formal publish.",
            "- No public site update.",
            "- No user notification.",
            "- No automatic publishing.",
            "- No live LLM review.",
            "- Manual publish review ready is not publish.",
            "- Final human publish confirmation is still required.",
            "",
            "## Decision",
            "",
            f"- Source release candidate package: `{decision['source_release_candidate_package']}`.",
            f"- Manual publish review ready: `{decision['manual_publish_review_ready']}`.",
            f"- Formal publish allowed: `{decision['formal_publish_allowed']}`.",
            f"- Public site updated: `{decision['public_site_updated']}`.",
            f"- User notification sent: `{decision['user_notification_sent']}`.",
            f"- Automatic publishing: `{decision['automatic_publishing']}`.",
            f"- Blocked: `{decision['blocked']}`.",
            "",
            "## Blocked Reasons",
            "",
            *[f"- {reason}" for reason in blocked_reasons],
            "",
        ]
    )


def build_final_human_publish_checklist(
    project_root: Path,
    source_package_dir: Path,
    decision: dict[str, Any],
) -> str:
    return "\n".join(
        [
            "# Final Human Publish Checklist",
            "",
            "- Confirm P2C-3 is only a manual publish review dry-run gate.",
            f"- Source release candidate package: `{rel(project_root, source_package_dir)}`.",
            "- Confirm manual publish review ready is not formal publish.",
            "- Confirm no public website update has happened.",
            "- Confirm no user notification has been sent.",
            "- Confirm automatic publishing remains disabled.",
            "- Confirm live LLM review was not used for this gate.",
            "- Confirm final human publish confirmation is still required.",
            f"- Gate decision blocked: `{decision['blocked']}`.",
            "",
        ]
    )


def resolve_path(project_root: Path, path: Path) -> Path:
    return path.resolve() if path.is_absolute() else (project_root / path).resolve()


def read_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def unique_preserving_order(items: list[str]) -> list[str]:
    seen = set()
    output = []
    for item in items:
        if item not in seen:
            output.append(item)
            seen.add(item)
    return output


def rel(project_root: Path, path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(project_root))
    except ValueError:
        return str(resolved)


if __name__ == "__main__":
    raise SystemExit(main())
