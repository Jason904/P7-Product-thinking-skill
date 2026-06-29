#!/usr/bin/env python3
"""Build a P2C-1 shadow-only observation ledger.

P2C-1 records a multi-day shadow-only observation window. It does not publish,
does not notify users, does not update a public site, and does not promote
shadow PASS into formal P2C authority.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml


RUBRIC_DIR_REL = Path("docs/quality/rubric-v2.1")
DEFAULT_POLICY_REL = RUBRIC_DIR_REL / "p2c1-shadow-observation-policy.yaml"
DEFAULT_OUTPUT_REL = RUBRIC_DIR_REL / "shadow-runs" / "p2c1-observation"
LEDGER_NAME = "shadow-observation-ledger.yaml"
REPORT_NAME = "shadow-observation-report.md"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY_REL)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_REL)
    parser.add_argument("--shadow-run", type=Path, action="append", default=[])
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    policy_path = resolve_path(project_root, args.policy)
    output_dir = resolve_output_dir(project_root, args.output_dir)
    shadow_dirs = [resolve_path(project_root, path) for path in args.shadow_run]
    ledger = build_observation_ledger(
        project_root=project_root,
        policy_path=policy_path,
        output_dir=output_dir,
        shadow_dirs=shadow_dirs,
    )
    print(yaml.safe_dump(ledger, allow_unicode=True, sort_keys=False), end="")
    return 0


def build_observation_ledger(
    *,
    project_root: Path,
    policy_path: Path,
    output_dir: Path,
    shadow_dirs: list[Path],
) -> dict[str, Any]:
    policy = read_yaml(policy_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    day_entries = [
        analyze_shadow_day(
            project_root=project_root,
            shadow_dir=shadow_dir,
            policy=policy,
        )
        for shadow_dir in shadow_dirs
    ]
    day_entries.sort(key=lambda item: item["date"])

    required_days = int(policy["observation_window"]["required_days"])
    blocked_reasons = [
        reason
        for day in day_entries
        for reason in day["blocked_reasons"]
    ]
    observed_days = len(day_entries)
    if blocked_reasons:
        observation_status = "OBSERVATION_BLOCKED"
    elif observed_days < required_days:
        observation_status = "OBSERVATION_INCOMPLETE"
        blocked_reasons.append(
            f"Observed {observed_days}/{required_days} required shadow days."
        )
    else:
        observation_status = "OBSERVATION_READY"

    ledger = {
        **runtime_contract(policy),
        "stage": "P2C-1",
        "policy_path": rel(project_root, policy_path),
        "observation_status": observation_status,
        "observation_window": {
            "required_days": required_days,
            "observed_days": observed_days,
            "dates": [
                public_day_entry(day)
                for day in day_entries
            ],
        },
        "blocked_reasons": blocked_reasons,
        "promotion_gate": build_promotion_gate(policy, observation_status, blocked_reasons),
    }

    write_yaml(output_dir / LEDGER_NAME, ledger)
    (output_dir / REPORT_NAME).write_text(build_runtime_report(ledger), encoding="utf-8")
    return ledger


def analyze_shadow_day(
    *,
    project_root: Path,
    shadow_dir: Path,
    policy: dict[str, Any],
) -> dict[str, Any]:
    required_artifacts = list(policy["required_artifacts"])
    result_path = shadow_dir / "shadow-review-result.yaml"
    missing_artifacts = [
        name for name in required_artifacts
        if not (shadow_dir / name).is_file()
    ]
    blocked_reasons = [
        f"{rel(project_root, shadow_dir)} missing {name}"
        for name in missing_artifacts
    ]

    if result_path.is_file():
        result = read_yaml(result_path)
    else:
        result = {}

    date = str(result.get("date") or infer_date(shadow_dir))
    reviewer_decision = str(result.get("reviewer_decision") or "MISSING")
    blocked_decisions = set(policy["blocked_decisions"])
    if reviewer_decision in blocked_decisions:
        blocked_reasons.append(f"{date} reviewer_decision={reviewer_decision} blocks P2C-2.")

    observed_formal_publish_allowed = bool(result.get("formal_publish_allowed", False))
    if observed_formal_publish_allowed:
        blocked_reasons.append(f"{date} formal_publish_allowed=true is forbidden in P2C-1.")

    for flag in policy["forbidden_flags"]:
        if bool(result.get(flag, False)):
            blocked_reasons.append(f"{date} {flag}=true is forbidden in P2C-1.")

    if not bool(result.get("shadow_only", True)):
        blocked_reasons.append(f"{date} shadow_only=false is forbidden in P2C-1.")
    if not bool(result.get("not_formal_p2c", True)):
        blocked_reasons.append(f"{date} not_formal_p2c=false is forbidden in P2C-1.")

    return {
        "date": date,
        "source_shadow_dir": rel(project_root, shadow_dir),
        "reviewer_decision": reviewer_decision,
        "shadow_publish_allowed": bool(result.get("shadow_publish_allowed", False)),
        "formal_publish_allowed": False,
        "source_formal_publish_allowed": observed_formal_publish_allowed,
        "failure_package_created": bool(result.get("failure_package_created", False)),
        "human_confirmed": bool(result.get("human_confirmed", False)),
        "public_site_updated": False,
        "source_public_site_updated": bool(result.get("public_site_updated", False)),
        "user_notification_sent": False,
        "source_user_notification_sent": bool(result.get("user_notification_sent", False)),
        "live_llm_review": False,
        "source_live_llm_review": bool(result.get("live_llm_review", False)),
        "required_artifacts_present": not missing_artifacts,
        "missing_artifacts": missing_artifacts,
        "blocked_reasons": blocked_reasons,
    }


def public_day_entry(day: dict[str, Any]) -> dict[str, Any]:
    return {
        "date": day["date"],
        "reviewer_decision": day["reviewer_decision"],
        "shadow_publish_allowed": day["shadow_publish_allowed"],
        "formal_publish_allowed": False,
        "failure_package_created": day["failure_package_created"],
        "human_confirmed": day["human_confirmed"],
        "required_artifacts_present": day["required_artifacts_present"],
        "missing_artifacts": day["missing_artifacts"],
        "source_shadow_dir": day["source_shadow_dir"],
    }


def build_promotion_gate(
    policy: dict[str, Any],
    observation_status: str,
    blocked_reasons: list[str],
) -> dict[str, Any]:
    if observation_status == "OBSERVATION_READY":
        reason = policy["promotion_gate"]["reason"]
    elif observation_status == "OBSERVATION_INCOMPLETE":
        reason = "Observation window is incomplete. P2C-2 remains blocked."
    else:
        reason = "; ".join(blocked_reasons)
    return {
        "eligible_for_p2c2": False,
        "reason": reason,
    }


def runtime_contract(policy: dict[str, Any]) -> dict[str, Any]:
    return {
        "shadow_only": bool(policy["shadow_only"]),
        "not_formal_p2c": bool(policy["not_formal_p2c"]),
        "formal_publish_allowed": False,
        "public_site_updated": False,
        "user_notification_sent": False,
        "live_llm_review": False,
        "human_confirmation_required": bool(policy["human_confirmation_required"]),
    }


def build_runtime_report(ledger: dict[str, Any]) -> str:
    rows = [
        "| Date | Reviewer decision | Shadow publish allowed | Formal publish allowed | Failure package created | Human confirmed |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for day in ledger["observation_window"]["dates"]:
        rows.append(
            (
                f"| {day['date']} | {day['reviewer_decision']} | "
                f"{str(day['shadow_publish_allowed']).lower()} | false | "
                f"{str(day['failure_package_created']).lower()} | "
                f"{str(day['human_confirmed']).lower()} |"
            )
        )
    blocked = ledger["blocked_reasons"] or ["No blocking observation defects; human confirmation still required."]
    return "\n".join(
        [
            "# P2C-1 Shadow Observation Runtime Report",
            "",
            "## Boundary",
            "",
            "- Shadow-only observation.",
            "- Not formal P2C.",
            "- No public site update.",
            "- No user notification.",
            "- No live LLM review.",
            "- No automatic publishing.",
            "- Human confirmation required.",
            "",
            "## Status",
            "",
            f"- Observation status: `{ledger['observation_status']}`.",
            f"- Eligible for P2C-2: `{ledger['promotion_gate']['eligible_for_p2c2']}`.",
            f"- Reason: {ledger['promotion_gate']['reason']}",
            "",
            "## Days",
            "",
            *rows,
            "",
            "## Blocked Reasons",
            "",
            *[f"- {reason}" for reason in blocked],
            "",
        ]
    )


def resolve_path(project_root: Path, path: Path) -> Path:
    resolved = path.resolve() if path.is_absolute() else (project_root / path).resolve()
    return resolved


def resolve_output_dir(project_root: Path, path: Path) -> Path:
    return resolve_path(project_root, path)


def infer_date(path: Path) -> str:
    match = re.search(r"\d{4}-\d{2}-\d{2}", str(path))
    return match.group(0) if match else path.name


def read_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def rel(project_root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(project_root))


if __name__ == "__main__":
    raise SystemExit(main())
