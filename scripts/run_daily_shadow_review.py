#!/usr/bin/env python3
"""Run a P2B-4 pre-production shadow review.

The shadow run keeps every intermediate artifact, but never publishes and never
updates any live website content.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import yaml


RUBRIC_DIR_REL = Path("docs/quality/rubric-v2.1")
SHADOW_ROOT_REL = RUBRIC_DIR_REL / "shadow-runs"
DEFAULT_DATE = "2026-06-28"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--date", default=DEFAULT_DATE)
    parser.add_argument("--training-md", type=Path)
    parser.add_argument("--source-notes", type=Path)
    parser.add_argument("--quality-report", type=Path)
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    date = args.date
    source_training = resolve_training_source(project_root, date, args.training_md)
    source_notes = resolve_optional_source(
        project_root,
        args.source_notes,
        [
            Path("outputs/daily-training") / date / "source-notes.md",
            Path("outputs/daily-training") / date / "source-notes-p2b3.md",
        ],
    )
    quality_report = resolve_optional_source(
        project_root,
        args.quality_report,
        [
            Path("outputs/daily-training") / date / "quality-report.md",
            Path("outputs/daily-training") / date / "training-v8-quality-report.md",
        ],
    )

    result = run_shadow_review(
        project_root=project_root,
        date=date,
        source_training=source_training,
        source_notes=source_notes,
        quality_report=quality_report,
    )
    print(yaml.safe_dump(result, allow_unicode=True, sort_keys=False), end="")
    return 0


def run_shadow_review(
    *,
    project_root: Path,
    date: str,
    source_training: Path,
    source_notes: Path | None,
    quality_report: Path | None,
) -> dict[str, Any]:
    rubric_dir = project_root / RUBRIC_DIR_REL
    shadow_dir = project_root / SHADOW_ROOT_REL / date
    failure_package_dir = shadow_dir / "shadow-failure-package"
    shadow_dir.mkdir(parents=True, exist_ok=True)
    failure_package_dir.mkdir(parents=True, exist_ok=True)

    training_path = shadow_dir / "training.md"
    reader_path = shadow_dir / "reader.html"
    source_notes_path = shadow_dir / "source-notes.md"
    source_training_text = source_training.read_text(encoding="utf-8")
    training_path.write_text(source_training_text, encoding="utf-8")
    if source_notes:
        source_notes_path.write_text(source_notes.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        source_notes_path.write_text(
            "# Shadow Source Notes\n\nNo source-notes file was available for this shadow run.\n",
            encoding="utf-8",
        )

    renderer = load_module(
        project_root / "skill" / "scripts" / "render_training_reader_html.py",
        "shadow_render_training_reader_html",
    )
    reader_path.write_text(
        renderer.render_reader_html(source_training_text, source_name="training.md"),
        encoding="utf-8",
    )

    live = load_module(
        project_root / "scripts" / "run_live_reviewer_generation.py",
        "shadow_run_live_reviewer_generation",
    )
    source_map = {
        "training_markdown": rel(project_root, training_path),
        "reader_html": rel(project_root, reader_path),
        "source_notes": rel(project_root, source_notes_path),
    }
    if quality_report:
        quality_copy = shadow_dir / "quality-report.md"
        quality_copy.write_text(quality_report.read_text(encoding="utf-8"), encoding="utf-8")
        source_map["quality_report"] = rel(project_root, quality_copy)
    sources = live.read_sources(project_root, source_map)
    anchors = live.read_yaml(rubric_dir / "rubric-score-anchors.yaml")["items"]
    sample_id = f"shadow_{date.replace('-', '_')}"
    config = {
        "case_titles": infer_case_titles(source_training_text),
        "sources": source_map,
    }
    raw = live.build_raw_response(sample_id, config, sources, no_audit=False)
    raw["shadow_run"] = {
        "stage": "P2B-4",
        "date": date,
        "source_training": rel(project_root, source_training),
        "reader_html": rel(project_root, reader_path),
        "not_live_llm_reviewer": True,
        "not_p2c": True,
        "not_daily_production_pipeline": True,
    }
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
        "validator": shadow_dir / "shadow-review-result.yaml",
        "log": shadow_dir / "shadow-generation-log.yaml",
        "manifest": shadow_dir / "source-manifest.yaml",
    }
    live.write_json(paths["raw"], raw)
    live.write_json(paths["reviewer"], payload)
    live.write_json(paths["claim_map"], claim_map)
    live.write_json(paths["failures"], failures)

    shadow_result = build_shadow_result(
        date=date,
        sample_id=sample_id,
        payload=payload,
        validator_result=validator_result,
        failures=failures,
        failure_package_dir=failure_package_dir,
        project_root=project_root,
    )
    live.write_yaml(paths["validator"], shadow_result)
    manifest = build_source_manifest(
        project_root=project_root,
        date=date,
        source_training=source_training,
        source_notes=source_notes,
        quality_report=quality_report,
        source_map=source_map,
        shadow_dir=shadow_dir,
    )
    live.write_yaml(paths["manifest"], manifest)
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
    log.update(
        {
            "stage": "P2B-4",
            "shadow_run": True,
            "local_semantic_reviewer": True,
            "live_llm_review": False,
            "not_daily_production_pipeline": True,
            "not_p2c": True,
            "shadow_publish_allowed": False,
            "formal_publish_allowed": False,
            "self_review_used_as_release_authority": False,
            "historical_audit_used_as_release_authority": False,
        }
    )
    live.write_yaml(paths["log"], log)

    if payload["daily_decision"] != "PASS" or not payload["publish_allowed"]:
        write_failure_package(
            project_root=project_root,
            package_dir=failure_package_dir,
            shadow_dir=shadow_dir,
            failures=failures,
            payload=payload,
            claim_map=claim_map,
            shadow_result=shadow_result,
            manifest=manifest,
        )
    else:
        write_pass_hold_package(
            project_root=project_root,
            package_dir=failure_package_dir,
            shadow_result=shadow_result,
        )

    report_path = rubric_dir / "shadow-run-report.md"
    report_path.write_text(build_report(shadow_result, manifest), encoding="utf-8")

    return {
        "completed": True,
        "stage": "P2B-4 pre-production shadow run",
        "date": date,
        "shadow_dir": rel(project_root, shadow_dir),
        "report_path": rel(project_root, report_path),
        "reviewer_decision": payload["daily_decision"],
        "reviewer_publish_allowed": payload["publish_allowed"],
        "shadow_publish_allowed": False,
        "failure_package_dir": rel(project_root, failure_package_dir),
    }


def build_shadow_result(
    *,
    date: str,
    sample_id: str,
    payload: dict[str, Any],
    validator_result: dict[str, Any],
    failures: list[dict[str, Any]],
    failure_package_dir: Path,
    project_root: Path,
) -> dict[str, Any]:
    decision = payload["daily_decision"]
    reviewer_publish_allowed = bool(payload["publish_allowed"])
    needs_failure_package = decision != "PASS" or not reviewer_publish_allowed
    return {
        "stage": "P2B-4 pre-production shadow run",
        "date": date,
        "sample_id": sample_id,
        "local_semantic_reviewer": True,
        "live_llm_review": False,
        "not_p2c": True,
        "not_daily_production_pipeline": True,
        "website_updated": False,
        "user_notification_sent": False,
        "shadow_pass_is_formal_pass": False,
        "reviewer_decision": decision,
        "reviewer_publish_allowed": reviewer_publish_allowed,
        "shadow_publish_allowed": False,
        "formal_publish_allowed": False,
        "manual_confirmation_required_before_p2c": True,
        "governance_validator_status": validator_result["schema_and_governance_payload_status"],
        "governance_decision": validator_result["governance_decision"],
        "publish_blocked": True,
        "failure_types": validator_result["failure_types"],
        "failure_package_required": needs_failure_package,
        "failure_package_path": rel(project_root, failure_package_dir),
        "failure_package_created": needs_failure_package,
        "failure_count": len(failures),
        "self_review_used_as_release_authority": False,
        "historical_audit_used_as_release_authority": False,
        "next_action": (
            "Route the shadow failure package back to content / reviewer governance repair."
            if needs_failure_package
            else "Hold for human confirmation before any P2C decision."
        ),
    }


def build_source_manifest(
    *,
    project_root: Path,
    date: str,
    source_training: Path,
    source_notes: Path | None,
    quality_report: Path | None,
    source_map: dict[str, str],
    shadow_dir: Path,
) -> dict[str, Any]:
    return {
        "stage": "P2B-4 pre-production shadow run",
        "date": date,
        "real_input": True,
        "synthetic_fixture": False,
        "governance_generated_input_allowed": True,
        "source_training_markdown": rel(project_root, source_training),
        "source_reader_html": source_map["reader_html"],
        "source_notes": rel(project_root, source_notes) if source_notes else None,
        "quality_or_audit_report": rel(project_root, quality_report) if quality_report else None,
        "shadow_training_markdown": rel(project_root, shadow_dir / "training.md"),
        "shadow_reader_html": rel(project_root, shadow_dir / "reader.html"),
        "local_semantic_reviewer": True,
        "live_llm_review": False,
        "not_daily_production_pipeline": True,
        "not_p2c": True,
        "website_updated": False,
        "user_notification_sent": False,
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
    write_yaml(
        package_dir / "package-manifest.yaml",
        {
            "stage": "P2B-4 pre-production shadow run",
            "package_type": "shadow_failure_package",
            "failure_package_required": True,
            "shadow_pass_is_formal_pass": False,
            "manual_confirmation_required_before_p2c": True,
            "source_shadow_dir": rel(project_root, shadow_dir),
            "entrypoints": {
                "failure_objects": "failure-objects.json",
                "reviewer_output": "reviewer-output.json",
                "claim_evidence_map": "claim-evidence-map.json",
                "shadow_review_result": "shadow-review-result.yaml",
                "source_manifest": "source-manifest.yaml",
                "repair_actions": "repair-actions.yaml",
            },
        },
    )
    write_json(package_dir / "failure-objects.json", failures)
    write_json(package_dir / "reviewer-output.json", payload)
    write_json(package_dir / "claim-evidence-map.json", claim_map)
    write_yaml(package_dir / "shadow-review-result.yaml", shadow_result)
    write_yaml(package_dir / "source-manifest.yaml", manifest)
    write_yaml(
        package_dir / "repair-actions.yaml",
        {
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
            "return_path": "content_repair and system_repair queues before P2C.",
        },
    )


def write_pass_hold_package(
    *,
    project_root: Path,
    package_dir: Path,
    shadow_result: dict[str, Any],
) -> None:
    write_yaml(
        package_dir / "package-manifest.yaml",
        {
            "stage": "P2B-4 pre-production shadow run",
            "failure_package_required": False,
            "shadow_pass_is_formal_pass": False,
            "manual_confirmation_required_before_p2c": True,
            "shadow_result": shadow_result,
            "package_dir": rel(project_root, package_dir),
        },
    )


def build_report(shadow_result: dict[str, Any], manifest: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# P2B-4 Pre-production Shadow Run Report",
            "",
            "## Boundary",
            "",
            "- Reviewer: local semantic reviewer.",
            "- Not a live LLM reviewer.",
            "- Does not enter P2C.",
            "- Does not connect to the daily production chain.",
            "- Does not publish or update website content.",
            "- Does not send real user notifications.",
            "- Shadow PASS is not formal PASS.",
            "- Self-review tables and historical audit reports are evidence inputs only, not release authority.",
            "",
            "## Input",
            "",
            f"- Date: `{shadow_result['date']}`.",
            f"- Training Markdown: `{manifest['shadow_training_markdown']}`.",
            f"- Reader HTML: `{manifest['shadow_reader_html']}`.",
            f"- Source notes: `{manifest['source_notes'] or 'not available'}`.",
            f"- Quality / audit report: `{manifest['quality_or_audit_report'] or 'not available'}`.",
            "",
            "## Result",
            "",
            f"- Reviewer decision: `{shadow_result['reviewer_decision']}`.",
            f"- Reviewer publish allowed: `{shadow_result['reviewer_publish_allowed']}`.",
            f"- Shadow publish allowed: `{shadow_result['shadow_publish_allowed']}`.",
            f"- Formal publish allowed: `{shadow_result['formal_publish_allowed']}`.",
            f"- Governance validator status: `{shadow_result['governance_validator_status']}`.",
            f"- Failure package required: `{shadow_result['failure_package_required']}`.",
            f"- Failure package path: `{shadow_result['failure_package_path']}`.",
            "",
            "## Next Action",
            "",
            f"- {shadow_result['next_action']}",
            "",
        ]
    )


def resolve_training_source(project_root: Path, date: str, explicit: Path | None) -> Path:
    if explicit:
        path = (project_root / explicit).resolve() if not explicit.is_absolute() else explicit
        if not path.is_file():
            raise FileNotFoundError(path)
        return path
    date_dir = project_root / "outputs" / "daily-training" / date
    candidates = [
        date_dir / "training.md",
        date_dir / "training-v8-review-boilerplate.md",
        date_dir / "training-v8-pass.md",
    ]
    candidates.extend(sorted(date_dir.glob("training*.md")))
    for path in candidates:
        if path.is_file():
            return path
    raise FileNotFoundError(f"No training markdown found for {date}")


def resolve_optional_source(
    project_root: Path,
    explicit: Path | None,
    candidates: list[Path],
) -> Path | None:
    if explicit:
        path = (project_root / explicit).resolve() if not explicit.is_absolute() else explicit
        if not path.is_file():
            raise FileNotFoundError(path)
        return path
    for candidate in candidates:
        path = project_root / candidate
        if path.is_file():
            return path
    return None


def infer_case_titles(markdown: str) -> dict[str, str]:
    import re

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


def rel(project_root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(project_root))


if __name__ == "__main__":
    raise SystemExit(main())
