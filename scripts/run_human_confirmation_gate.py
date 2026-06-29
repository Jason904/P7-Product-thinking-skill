#!/usr/bin/env python3
"""Run the P2C-2 human confirmation gate.

The gate consumes a P2C-1 observation ledger and an explicit human-confirmed
flag. It may create a release-candidate decision package, but it never performs
formal publishing, public website updates, notifications, or live LLM review.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Any

import yaml


RUBRIC_DIR_REL = Path("docs/quality/rubric-v2.1")
DEFAULT_POLICY_REL = RUBRIC_DIR_REL / "p2c2-human-confirmation-policy.yaml"
DEFAULT_OUTPUT_REL = RUBRIC_DIR_REL / "shadow-runs" / "p2c2-human-confirmation"
DECISION_NAME = "human-confirmation-decision.yaml"
REPORT_NAME = "human-confirmation-report.md"
PACKAGE_DIR_NAME = "release-candidate-package"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY_REL)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_REL)
    parser.add_argument("--human-confirmed", action="store_true")
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    decision = run_human_confirmation_gate(
        project_root=project_root,
        policy_path=resolve_path(project_root, args.policy),
        ledger_path=resolve_path(project_root, args.ledger),
        output_dir=resolve_path(project_root, args.output_dir),
        human_confirmed=args.human_confirmed,
    )
    print(yaml.safe_dump(decision, allow_unicode=True, sort_keys=False), end="")
    return 0


def run_human_confirmation_gate(
    *,
    project_root: Path,
    policy_path: Path,
    ledger_path: Path,
    output_dir: Path,
    human_confirmed: bool,
) -> dict[str, Any]:
    policy = read_yaml(policy_path)
    ledger = read_yaml(ledger_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    package_dir = output_dir / PACKAGE_DIR_NAME
    if package_dir.exists():
        shutil.rmtree(package_dir)

    blocked_reasons = derive_blocked_reasons(ledger, human_confirmed)
    blocked = bool(blocked_reasons)
    release_candidate_created = not blocked
    eligible_for_manual_publish_review = release_candidate_created

    decision = {
        "stage": "P2C-2",
        "gate_type": "human_confirmation_gate",
        "policy_path": rel(project_root, policy_path),
        "source_observation_ledger": rel(project_root, ledger_path),
        "shadow_only_source": bool(ledger.get("shadow_only", True)),
        "not_formal_publish": True,
        "release_candidate_created": release_candidate_created,
        "human_confirmed": human_confirmed,
        "formal_publish_allowed": False,
        "public_site_updated": False,
        "user_notification_sent": False,
        "live_llm_review": False,
        "requires_manual_publish_step": bool(
            policy["manual_publish_review_required_after_release_candidate"]
        ),
        "eligible_for_manual_publish_review": eligible_for_manual_publish_review,
        "blocked": blocked,
        "blocked_reasons": blocked_reasons,
        "source_observation_status": str(ledger.get("observation_status", "MISSING")),
        "release_candidate_package_path": (
            rel(project_root, package_dir) if release_candidate_created else None
        ),
        "release_candidate_is_not_publish": bool(policy["release_candidate_is_not_publish"]),
        "next_action": (
            "Route to manual publish review. Do not publish automatically."
            if release_candidate_created
            else "Resolve blocked reasons before creating a release candidate."
        ),
    }

    write_yaml(output_dir / DECISION_NAME, decision)
    (output_dir / REPORT_NAME).write_text(build_report(decision), encoding="utf-8")
    if release_candidate_created:
        write_release_candidate_package(
            project_root=project_root,
            package_dir=package_dir,
            ledger_path=ledger_path,
            decision=decision,
        )
    return decision


def derive_blocked_reasons(ledger: dict[str, Any], human_confirmed: bool) -> list[str]:
    reasons: list[str] = []
    status = str(ledger.get("observation_status", "MISSING"))
    if status == "OBSERVATION_BLOCKED":
        reasons.append("OBSERVATION_BLOCKED")
    elif status == "OBSERVATION_INCOMPLETE":
        reasons.append("OBSERVATION_INCOMPLETE")
    elif status != "OBSERVATION_READY":
        reasons.append(status)

    if status == "OBSERVATION_READY" and not human_confirmed:
        reasons.append("HUMAN_CONFIRMATION_MISSING")

    if bool(ledger.get("formal_publish_allowed", False)):
        reasons.append("FORMAL_PUBLISH_ALREADY_ALLOWED")
    if bool(ledger.get("public_site_updated", False)):
        reasons.append("PUBLIC_SITE_ALREADY_UPDATED")
    if bool(ledger.get("user_notification_sent", False)):
        reasons.append("USER_NOTIFICATION_ALREADY_SENT")
    if bool(ledger.get("live_llm_review", False)):
        reasons.append("LIVE_LLM_REVIEW_USED")

    return unique_preserving_order(reasons)


def write_release_candidate_package(
    *,
    project_root: Path,
    package_dir: Path,
    ledger_path: Path,
    decision: dict[str, Any],
) -> None:
    package_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ledger_path, package_dir / "source-observation-ledger.yaml")
    write_yaml(package_dir / "human-confirmation-decision.yaml", decision)
    write_yaml(
        package_dir / "release-candidate-manifest.yaml",
        {
            "stage": "P2C-2",
            "package_type": "release_candidate_decision_package",
            "release_candidate_created": True,
            "release_candidate_is_not_publish": True,
            "manual_publish_review_required_after_release_candidate": True,
            "formal_publish_allowed": False,
            "public_site_updated": False,
            "user_notification_sent": False,
            "live_llm_review": False,
            "requires_manual_publish_step": True,
            "source_observation_ledger": "source-observation-ledger.yaml",
            "decision": "human-confirmation-decision.yaml",
            "manual_publish_review_checklist": "manual-publish-review-checklist.md",
        },
    )
    (package_dir / "manual-publish-review-checklist.md").write_text(
        build_manual_publish_review_checklist(project_root, ledger_path, decision),
        encoding="utf-8",
    )


def build_report(decision: dict[str, Any]) -> str:
    blocked_reasons = decision["blocked_reasons"] or ["No P2C-2 gate blockers."]
    return "\n".join(
        [
            "# P2C-2 Human Confirmation Runtime Report",
            "",
            "## Boundary",
            "",
            "- Not formal publish.",
            "- No public site update.",
            "- No user notification.",
            "- No automatic publishing.",
            "- Release candidate is not publish.",
            "- Manual publish review still required.",
            "",
            "## Decision",
            "",
            f"- Source observation status: `{decision['source_observation_status']}`.",
            f"- Human confirmed: `{decision['human_confirmed']}`.",
            f"- Release candidate created: `{decision['release_candidate_created']}`.",
            f"- Eligible for manual publish review: `{decision['eligible_for_manual_publish_review']}`.",
            f"- Formal publish allowed: `{decision['formal_publish_allowed']}`.",
            f"- Blocked: `{decision['blocked']}`.",
            "",
            "## Blocked Reasons",
            "",
            *[f"- {reason}" for reason in blocked_reasons],
            "",
        ]
    )


def build_manual_publish_review_checklist(
    project_root: Path,
    ledger_path: Path,
    decision: dict[str, Any],
) -> str:
    return "\n".join(
        [
            "# Manual Publish Review Checklist",
            "",
            "- Confirm the source P2C-1 observation ledger was reviewed by a human.",
            f"- Source ledger: `{rel(project_root, ledger_path)}`.",
            "- Confirm release candidate is not formal publish.",
            "- Confirm no public website update has happened.",
            "- Confirm no user notification has been sent.",
            "- Confirm no live LLM review was used for this gate.",
            "- Confirm a separate manual publish review step is still required.",
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
    return str(path.resolve().relative_to(project_root))


if __name__ == "__main__":
    raise SystemExit(main())
