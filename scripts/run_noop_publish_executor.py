#!/usr/bin/env python3
"""Run the P2C-4 no-op publish executor.

The executor consumes a P2C-3 manual publish review package and writes a final
publish execution plan plus safety decision. It is intentionally a no-op: it
never updates the public site, sends notifications, performs formal publishing,
enables automatic publishing, or calls live LLM review.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


RUBRIC_DIR_REL = Path("docs/quality/rubric-v2.1")
DEFAULT_POLICY_REL = RUBRIC_DIR_REL / "p2c4-noop-publish-executor-policy.yaml"
DEFAULT_OUTPUT_REL = RUBRIC_DIR_REL / "shadow-runs" / "p2c4-noop-publish-executor"
DECISION_NAME = "noop-publish-execution-decision.yaml"
REPORT_NAME = "noop-publish-execution-report.md"
PLAN_NAME = "noop-publish-execution-plan.yaml"

REQUIRED_PACKAGE_FILES = {
    "source-release-candidate-manifest.yaml": "SOURCE_RELEASE_CANDIDATE_MANIFEST_MISSING",
    "source-human-confirmation-decision.yaml": "SOURCE_HUMAN_CONFIRMATION_DECISION_MISSING",
    "manual-publish-review-decision.yaml": "MANUAL_PUBLISH_REVIEW_DECISION_MISSING",
    "final-human-publish-checklist.md": "FINAL_HUMAN_PUBLISH_CHECKLIST_MISSING",
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
    parser.add_argument("--manual-publish-review-package", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_REL)
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    decision = run_noop_publish_executor(
        project_root=project_root,
        policy_path=resolve_path(project_root, args.policy),
        manual_publish_review_package=resolve_path(
            project_root,
            args.manual_publish_review_package,
        ),
        output_dir=resolve_path(project_root, args.output_dir),
    )
    print(yaml.safe_dump(decision, allow_unicode=True, sort_keys=False), end="")
    return 0


def run_noop_publish_executor(
    *,
    project_root: Path,
    policy_path: Path,
    manual_publish_review_package: Path,
    output_dir: Path,
) -> dict[str, Any]:
    policy = read_yaml(policy_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    manual_decision_path = manual_publish_review_package / "manual-publish-review-decision.yaml"
    manual_decision = read_yaml(manual_decision_path) if manual_decision_path.is_file() else {}
    source_documents = read_source_documents(manual_publish_review_package)

    planned_actions = normalize_planned_actions(policy["planned_actions"])
    blocked_reasons = derive_blocked_reasons(
        package_dir=manual_publish_review_package,
        manual_decision=manual_decision,
        source_documents=source_documents,
    )
    blocked = bool(blocked_reasons)
    safe_to_run_real_publish_later = not blocked

    decision = {
        "stage": "P2C-4",
        "executor_type": "noop_publish_executor",
        "policy_path": rel(project_root, policy_path),
        "source_manual_publish_review_package": rel(project_root, manual_publish_review_package),
        "dry_run": True,
        "noop": True,
        "publish_executed": False,
        "formal_publish_allowed": False,
        "public_site_updated": False,
        "user_notification_sent": False,
        "live_llm_review": False,
        "automatic_publishing": False,
        "requires_explicit_final_publish_command": bool(
            policy["requires_explicit_final_publish_command"]
        ),
        "requires_final_human_publish_confirmation": bool(
            policy["requires_final_human_publish_confirmation"]
        ),
        "safe_to_run_real_publish_later": safe_to_run_real_publish_later,
        "blocked": blocked,
        "blocked_reasons": blocked_reasons,
        "planned_actions": planned_actions,
        "next_action": (
            "Route to explicit final publish command review. No publish side effects were executed."
            if safe_to_run_real_publish_later
            else "Resolve blocked reasons before any final publish command review."
        ),
    }

    execution_plan = {
        "stage": "P2C-4",
        "executor_type": "noop_publish_executor",
        "dry_run": True,
        "noop": True,
        "publish_executed": False,
        "formal_publish_allowed": False,
        "planned_actions": planned_actions,
    }
    write_yaml(output_dir / DECISION_NAME, decision)
    write_yaml(output_dir / PLAN_NAME, execution_plan)
    (output_dir / REPORT_NAME).write_text(build_report(decision), encoding="utf-8")
    return decision


def read_source_documents(package_dir: Path) -> list[dict[str, Any]]:
    documents: list[dict[str, Any]] = []
    for file_name in (
        "source-release-candidate-manifest.yaml",
        "source-human-confirmation-decision.yaml",
        "manual-publish-review-decision.yaml",
    ):
        path = package_dir / file_name
        if path.is_file():
            documents.append(read_yaml(path))
    return documents


def derive_blocked_reasons(
    *,
    package_dir: Path,
    manual_decision: dict[str, Any],
    source_documents: list[dict[str, Any]],
) -> list[str]:
    reasons: list[str] = []
    if not package_dir.is_dir():
        reasons.append("MANUAL_PUBLISH_REVIEW_PACKAGE_MISSING")
        return reasons

    for file_name, reason in REQUIRED_PACKAGE_FILES.items():
        if not (package_dir / file_name).is_file():
            reasons.append(reason)

    if manual_decision:
        if not bool(manual_decision.get("manual_publish_review_ready", False)):
            reasons.append("MANUAL_PUBLISH_REVIEW_NOT_READY")
        if bool(manual_decision.get("blocked", False)):
            reasons.append("MANUAL_PUBLISH_REVIEW_NOT_READY")
        if not bool(manual_decision.get("requires_final_human_publish_confirmation", False)):
            reasons.append("FINAL_HUMAN_PUBLISH_CONFIRMATION_NOT_REQUIRED")

    for flag, reason in BOUNDARY_FLAGS.items():
        if any(bool(document.get(flag, False)) for document in source_documents):
            reasons.append(reason)

    return unique_preserving_order(reasons)


def normalize_planned_actions(actions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "action": str(action["action"]),
            "side_effect": bool(action["side_effect"]),
            "executed": False,
        }
        for action in actions
    ]


def build_report(decision: dict[str, Any]) -> str:
    blocked_reasons = decision["blocked_reasons"] or ["No P2C-4 no-op executor blockers."]
    rows = [
        "| Action | Side effect | Executed |",
        "| --- | --- | --- |",
    ]
    for action in decision["planned_actions"]:
        rows.append(
            f"| {action['action']} | {action['side_effect']} | {action['executed']} |"
        )
    return "\n".join(
        [
            "# P2C-4 No-op Publish Execution Runtime Report",
            "",
            "## Boundary",
            "",
            "- No formal publish.",
            "- No public site update.",
            "- No user notification.",
            "- No automatic publishing.",
            "- No live LLM review.",
            "- Dry-run only.",
            "- No-op only.",
            "- Publish executed is false.",
            "",
            "## Decision",
            "",
            f"- Source manual publish review package: `{decision['source_manual_publish_review_package']}`.",
            f"- Dry run: `{decision['dry_run']}`.",
            f"- No-op: `{decision['noop']}`.",
            f"- Publish executed: `{decision['publish_executed']}`.",
            f"- Safe to run real publish later: `{decision['safe_to_run_real_publish_later']}`.",
            f"- Formal publish allowed: `{decision['formal_publish_allowed']}`.",
            f"- Public site updated: `{decision['public_site_updated']}`.",
            f"- User notification sent: `{decision['user_notification_sent']}`.",
            f"- Automatic publishing: `{decision['automatic_publishing']}`.",
            f"- Blocked: `{decision['blocked']}`.",
            "",
            "## Planned Actions",
            "",
            *rows,
            "",
            "## Blocked Reasons",
            "",
            *[f"- {reason}" for reason in blocked_reasons],
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
