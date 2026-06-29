#!/usr/bin/env python3
"""Run P2C-0 shadow-only integration after daily training output.

This script connects the existing local semantic reviewer to a daily training
artifact, writes a shadow decision/report, and never enters formal P2C
publication, public website update, or user notification flows.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

import yaml


RUBRIC_DIR_REL = Path("docs/quality/rubric-v2.1")
SHADOW_ROOT_REL = RUBRIC_DIR_REL / "shadow-runs"
DEFAULT_DATE = "2026-06-28"
DEFAULT_SOURCE_NOTES_NAME = "source-notes-p2b3.md"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--date", default=DEFAULT_DATE)
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--training-md", type=Path, required=True)
    parser.add_argument("--source-notes", type=Path)
    parser.add_argument("--reader-html", type=Path)
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    result = run_daily_shadow_integration(
        project_root=project_root,
        date=args.date,
        scenario=args.scenario,
        source_training=resolve_path(project_root, args.training_md),
        source_notes=resolve_optional_path(
            project_root,
            args.source_notes,
            [Path("outputs/daily-training") / args.date / DEFAULT_SOURCE_NOTES_NAME],
        ),
        source_reader=resolve_optional_path(project_root, args.reader_html, []),
    )
    print(yaml.safe_dump(result, allow_unicode=True, sort_keys=False), end="")
    return 0


def run_daily_shadow_integration(
    *,
    project_root: Path,
    date: str,
    scenario: str,
    source_training: Path,
    source_notes: Path | None,
    source_reader: Path | None = None,
) -> dict[str, Any]:
    scenario_slug = slugify(scenario)
    rubric_dir = project_root / RUBRIC_DIR_REL
    shadow_dir = project_root / SHADOW_ROOT_REL / date / f"p2c0-{scenario_slug}"
    reset_shadow_dir(project_root, shadow_dir)

    training_path = shadow_dir / "training.md"
    reader_path = shadow_dir / "reader.html"
    source_notes_path = shadow_dir / "source-notes.md"

    training_text = source_training.read_text(encoding="utf-8")
    training_path.write_text(training_text, encoding="utf-8")
    write_source_notes(source_notes_path, source_notes)
    write_reader_html(project_root, reader_path, training_text, source_reader)

    live = load_module(
        project_root / "scripts" / "run_live_reviewer_generation.py",
        "p2c0_run_live_reviewer_generation",
    )
    source_map = {
        "training_markdown": rel(project_root, training_path),
        "reader_html": rel(project_root, reader_path),
        "source_notes": rel(project_root, source_notes_path),
    }
    sources = live.read_sources(project_root, source_map)
    anchors = live.read_yaml(rubric_dir / "rubric-score-anchors.yaml")["items"]
    sample_id = f"p2c0_{date.replace('-', '_')}_{scenario_slug.replace('-', '_')}"
    config = {
        "case_titles": infer_case_titles(training_text),
        "sources": source_map,
    }

    raw = live.build_raw_response(sample_id, config, sources, no_audit=False)
    raw["shadow_run"] = build_shadow_run_contract(
        date=date,
        scenario=scenario_slug,
        source_training=rel(project_root, source_training),
        reader_html=rel(project_root, reader_path),
    )
    failures = live.build_failure_objects(sample_id, raw)
    payload = live.build_reviewer_output(sample_id, config, raw, anchors, failures)
    claim_map = {
        case["case_id"]: case["claim_evidence_map"][0]
        for case in payload["case_reviews"]
    }
    validator_result = live.validate_outputs(sample_id, rubric_dir, payload, claim_map, failures)
    final_release = live.derive_daily_decision(
        [case["case_decision"] for case in payload["case_reviews"]],
        failures,
        validator_result,
    )
    if (
        final_release["daily_decision"] != payload["daily_decision"]
        or final_release["publish_allowed"] != payload["publish_allowed"]
    ):
        payload["daily_decision"] = final_release["daily_decision"]
        payload["publish_allowed"] = final_release["publish_allowed"]
        validator_result = live.validate_outputs(sample_id, rubric_dir, payload, claim_map, failures)

    paths = {
        "raw": shadow_dir / "raw-reviewer-response.json",
        "reviewer": shadow_dir / "reviewer-output.json",
        "claim_map": shadow_dir / "claim-evidence-map.json",
        "failures": shadow_dir / "failure-objects.json",
        "result": shadow_dir / "shadow-review-result.yaml",
        "log": shadow_dir / "shadow-generation-log.yaml",
        "manifest": shadow_dir / "source-manifest.yaml",
        "report": shadow_dir / "shadow-run-report.md",
    }

    live.write_json(paths["raw"], raw)
    live.write_json(paths["reviewer"], payload)
    live.write_json(paths["claim_map"], claim_map)
    live.write_json(paths["failures"], failures)

    shadow_result = build_shadow_result(
        project_root=project_root,
        date=date,
        scenario=scenario_slug,
        sample_id=sample_id,
        payload=payload,
        validator_result=validator_result,
        failures=failures,
        shadow_dir=shadow_dir,
    )
    manifest = build_source_manifest(
        project_root=project_root,
        date=date,
        scenario=scenario_slug,
        source_training=source_training,
        source_notes=source_notes,
        source_reader=source_reader,
        shadow_dir=shadow_dir,
    )
    log = live.build_generation_log(
        project_root,
        rubric_dir,
        shadow_dir,
        sample_id,
        sources,
        paths,
        validator_result,
        no_audit=False,
    )
    log.update(build_runtime_contract())
    log.update(
        {
            "stage": "P2C-0",
            "date": date,
            "scenario": scenario_slug,
            "shadow_run": True,
            "shadow_publish_allowed": shadow_result["shadow_publish_allowed"],
            "formal_publish_allowed": False,
            "human_confirmation_required": True,
            "failure_package_required": shadow_result["failure_package_required"],
            "failure_package_created": shadow_result["failure_package_created"],
        }
    )

    live.write_yaml(paths["result"], shadow_result)
    live.write_yaml(paths["manifest"], manifest)
    live.write_yaml(paths["log"], log)

    if shadow_result["failure_package_required"]:
        write_failure_package(
            project_root=project_root,
            package_dir=shadow_dir / "shadow-failure-package",
            shadow_dir=shadow_dir,
            failures=failures,
            payload=payload,
            claim_map=claim_map,
            shadow_result=shadow_result,
            manifest=manifest,
        )

    paths["report"].write_text(
        build_shadow_run_report(shadow_result, manifest),
        encoding="utf-8",
    )

    return {
        "completed": True,
        "stage": "P2C-0",
        "date": date,
        "scenario": scenario_slug,
        "shadow_dir": rel(project_root, shadow_dir),
        "report_path": rel(project_root, paths["report"]),
        "reviewer_decision": payload["daily_decision"],
        "shadow_publish_allowed": shadow_result["shadow_publish_allowed"],
        "formal_publish_allowed": False,
        "human_confirmation_required": True,
        "failure_package_required": shadow_result["failure_package_required"],
        "failure_package_created": shadow_result["failure_package_created"],
    }


def build_shadow_run_contract(
    *,
    date: str,
    scenario: str,
    source_training: str,
    reader_html: str,
) -> dict[str, Any]:
    return {
        **build_runtime_contract(),
        "stage": "P2C-0",
        "date": date,
        "scenario": scenario,
        "source_training": source_training,
        "reader_html": reader_html,
        "shadow_pass_is_formal_pass": False,
        "automatic_publishing": False,
    }


def build_runtime_contract() -> dict[str, Any]:
    return {
        "shadow_only": True,
        "not_formal_p2c": True,
        "local_semantic_reviewer": True,
        "live_llm_review": False,
        "public_site_updated": False,
        "user_notification_sent": False,
        "formal_publish_allowed": False,
        "human_confirmation_required": True,
    }


def build_shadow_result(
    *,
    project_root: Path,
    date: str,
    scenario: str,
    sample_id: str,
    payload: dict[str, Any],
    validator_result: dict[str, Any],
    failures: list[dict[str, Any]],
    shadow_dir: Path,
) -> dict[str, Any]:
    reviewer_decision = payload["daily_decision"]
    reviewer_publish_allowed = bool(payload["publish_allowed"])
    failure_package_required = reviewer_decision != "PASS" or not reviewer_publish_allowed
    shadow_publish_allowed = reviewer_decision == "PASS" and reviewer_publish_allowed
    failure_package_dir = shadow_dir / "shadow-failure-package"
    return {
        **build_runtime_contract(),
        "stage": "P2C-0",
        "date": date,
        "scenario": scenario,
        "sample_id": sample_id,
        "reviewer_decision": reviewer_decision,
        "reviewer_publish_allowed": reviewer_publish_allowed,
        "shadow_publish_allowed": shadow_publish_allowed,
        "formal_publish_allowed": False,
        "human_confirmation_required": True,
        "failure_package_required": failure_package_required,
        "failure_package_created": failure_package_required,
        "failure_package_path": (
            rel(project_root, failure_package_dir) if failure_package_required else None
        ),
        "failure_count": len(failures),
        "failure_types": validator_result["failure_types"],
        "governance_validator_status": validator_result["schema_and_governance_payload_status"],
        "governance_decision": validator_result["governance_decision"],
        "governance_publish_allowed": validator_result["publish_allowed"],
        "formal_publish_blocked": True,
        "public_site_updated": False,
        "user_notification_sent": False,
        "shadow_pass_is_formal_pass": False,
        "not_daily_content_generation": True,
        "live_llm_generation": False,
        "next_action": (
            "Hold for human confirmation before any later P2C decision."
            if shadow_publish_allowed
            else "Route the shadow failure package to repair before any later P2C decision."
        ),
    }


def build_source_manifest(
    *,
    project_root: Path,
    date: str,
    scenario: str,
    source_training: Path,
    source_notes: Path | None,
    source_reader: Path | None,
    shadow_dir: Path,
) -> dict[str, Any]:
    return {
        **build_runtime_contract(),
        "stage": "P2C-0",
        "date": date,
        "scenario": scenario,
        "source_training_markdown": rel(project_root, source_training),
        "source_reader_html": rel(project_root, source_reader) if source_reader else None,
        "reader_html_generated_for_shadow_run": source_reader is None,
        "source_notes": rel(project_root, source_notes) if source_notes else None,
        "shadow_training_markdown": rel(project_root, shadow_dir / "training.md"),
        "shadow_reader_html": rel(project_root, shadow_dir / "reader.html"),
        "shadow_source_notes": rel(project_root, shadow_dir / "source-notes.md"),
        "runtime_artifact_dir": rel(project_root, shadow_dir),
        "no_live_llm_called": True,
        "no_public_site_write": True,
        "no_user_notification": True,
    }


def write_failure_package(
    *,
    project_root: Path,
    package_dir: Path,
    shadow_dir: Path,
    failures: list[dict[str, Any]],
    payload: dict[str, Any],
    claim_map: dict[str, Any],
    shadow_result: dict[str, Any],
    manifest: dict[str, Any],
) -> None:
    package_dir.mkdir(parents=True, exist_ok=True)
    write_yaml(
        package_dir / "source-manifest.yaml",
        manifest,
    )
    write_json(package_dir / "reviewer-output.json", payload)
    write_json(package_dir / "claim-evidence-map.json", claim_map)
    write_json(package_dir / "failure-objects.json", failures)
    write_yaml(package_dir / "shadow-review-result.yaml", shadow_result)
    write_yaml(
        package_dir / "repair-actions.yaml",
        {
            "stage": "P2C-0",
            "shadow_only": True,
            "formal_publish_allowed": False,
            "human_confirmation_required": True,
            "repair_targets": sorted(
                {
                    failure.get("content_repair_target")
                    for failure in failures
                    if failure.get("content_repair_target")
                }
            ),
            "system_repair_targets": sorted(
                {
                    target
                    for failure in failures
                    for target in failure.get("system_repair_target", [])
                }
            ),
            "must_rerun_gates": sorted(
                {
                    gate
                    for failure in failures
                    for gate in failure.get("must_rerun_gates", [])
                }
            ),
            "source_shadow_dir": rel(project_root, shadow_dir),
            "return_path": "Repair and rerun shadow-only review before any later P2C decision.",
        },
    )
    write_yaml(
        package_dir / "package-manifest.yaml",
        {
            "stage": "P2C-0",
            "package_type": "shadow_failure_package",
            "failure_package_required": True,
            "failure_package_created": True,
            "shadow_only": True,
            "not_formal_p2c": True,
            "shadow_pass_is_formal_pass": False,
            "formal_publish_allowed": False,
            "human_confirmation_required": True,
            "source_shadow_dir": rel(project_root, shadow_dir),
            "entrypoints": {
                "source_manifest": "source-manifest.yaml",
                "reviewer_output": "reviewer-output.json",
                "claim_evidence_map": "claim-evidence-map.json",
                "failure_objects": "failure-objects.json",
                "shadow_review_result": "shadow-review-result.yaml",
                "repair_actions": "repair-actions.yaml",
            },
        },
    )


def build_shadow_run_report(
    shadow_result: dict[str, Any],
    manifest: dict[str, Any],
) -> str:
    return "\n".join(
        [
            "# P2C-0 Shadow Run Report",
            "",
            "## Boundary",
            "",
            "- Shadow-only integration after daily training output.",
            "- Not formal P2C.",
            "- Local semantic reviewer only; no live LLM review.",
            "- No public site update.",
            "- No user notification.",
            "- No automatic publishing.",
            "- Human confirmation required.",
            "",
            "## Input",
            "",
            f"- Date: `{shadow_result['date']}`.",
            f"- Scenario: `{shadow_result['scenario']}`.",
            f"- Training Markdown: `{manifest['shadow_training_markdown']}`.",
            f"- Reader HTML: `{manifest['shadow_reader_html']}`.",
            f"- Source notes: `{manifest['shadow_source_notes']}`.",
            "",
            "## Decision",
            "",
            f"- Reviewer decision: `{shadow_result['reviewer_decision']}`.",
            f"- Shadow publish allowed: `{shadow_result['shadow_publish_allowed']}`.",
            f"- Formal publish allowed: `{shadow_result['formal_publish_allowed']}`.",
            f"- Human confirmation required: `{shadow_result['human_confirmation_required']}`.",
            f"- Failure package required: `{shadow_result['failure_package_required']}`.",
            f"- Failure package created: `{shadow_result['failure_package_created']}`.",
            "",
            "## Next Action",
            "",
            f"- {shadow_result['next_action']}",
            "",
        ]
    )


def write_reader_html(
    project_root: Path,
    reader_path: Path,
    training_text: str,
    source_reader: Path | None,
) -> None:
    if source_reader:
        reader_path.write_text(source_reader.read_text(encoding="utf-8"), encoding="utf-8")
        return
    renderer = load_module(
        project_root / "skill" / "scripts" / "render_training_reader_html.py",
        "p2c0_render_training_reader_html",
    )
    reader_path.write_text(
        renderer.render_reader_html(training_text, source_name="training.md"),
        encoding="utf-8",
    )


def write_source_notes(path: Path, source_notes: Path | None) -> None:
    if source_notes:
        path.write_text(source_notes.read_text(encoding="utf-8"), encoding="utf-8")
        return
    path.write_text(
        "# P2C-0 Shadow Source Notes\n\nNo source-notes file was available for this shadow run.\n",
        encoding="utf-8",
    )


def reset_shadow_dir(project_root: Path, shadow_dir: Path) -> None:
    root = (project_root / SHADOW_ROOT_REL).resolve()
    target = shadow_dir.resolve()
    if root not in target.parents:
        raise ValueError(f"Refusing to reset non-shadow directory: {target}")
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)


def resolve_path(project_root: Path, path: Path) -> Path:
    resolved = (project_root / path).resolve() if not path.is_absolute() else path.resolve()
    if not resolved.is_file():
        raise FileNotFoundError(resolved)
    return resolved


def resolve_optional_path(
    project_root: Path,
    explicit: Path | None,
    candidates: list[Path],
) -> Path | None:
    if explicit:
        return resolve_path(project_root, explicit)
    for candidate in candidates:
        path = project_root / candidate
        if path.is_file():
            return path.resolve()
    return None


def infer_case_titles(markdown: str) -> dict[str, str]:
    titles = {}
    for label, title in re.findall(r"(?m)^### Case ([ABC])：?([^\n]*)$", markdown):
        titles[f"case_{label.lower()}"] = title.strip() or f"Case {label}"
    for key, fallback in (("case_a", "Case A"), ("case_b", "Case B"), ("case_c", "Case C")):
        titles.setdefault(key, fallback)
    return titles


def load_module(path: Path, module_name: str) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_yaml(path: Path, data: Any) -> None:
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip()).strip("-").lower()
    return slug or "default"


def rel(project_root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(project_root))


if __name__ == "__main__":
    raise SystemExit(main())
