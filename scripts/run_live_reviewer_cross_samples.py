#!/usr/bin/env python3
"""P2B-2 cross-date / cross-topic real sample replay for the local reviewer."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
from pathlib import Path
from typing import Any

import yaml


SAMPLE_DEFINITIONS: dict[str, dict[str, Any]] = {
    "2026_06_25_training_v2": {
        "date": "2026-06-25",
        "expected_class": "FAIL",
        "why_selected": "Real early draft with three cases but missing the required 8Q reasoning structure; useful bad sample.",
        "case_titles": {
            "case_a": "V2 Case A",
            "case_b": "V2 Case B",
            "case_c": "V2 Case C",
        },
        "sources": {
            "training_markdown": "outputs/daily-training/2026-06-25/training-v2.md",
        },
    },
    "2026_06_25_training_v3": {
        "date": "2026-06-25",
        "expected_class": "PASS",
        "why_selected": "Real target-quality sample used as content depth baseline.",
        "case_titles": {
            "case_a": "V3 target Case A",
            "case_b": "V3 target Case B",
            "case_c": "V3 target Case C",
        },
        "sources": {
            "training_markdown": "outputs/daily-training/2026-06-25/training-v3.md",
        },
    },
    "2026_06_25_training_v4_raw": {
        "date": "2026-06-25",
        "expected_class": "PASS",
        "why_selected": "Real post-V3 iteration with full 8Q, PREP/SCQA, audit, and asset cards.",
        "case_titles": {
            "case_a": "V4 Case A",
            "case_b": "V4 Case B",
            "case_c": "V4 Case C",
        },
        "sources": {
            "training_markdown": "outputs/daily-training/2026-06-25/training-v4-raw.md",
        },
        "available_but_not_used": {
            "raw_html_not_reader": "outputs/daily-training/2026-06-25/training-v4-raw.html",
        },
    },
    "2026_06_25_training_v5_raw": {
        "date": "2026-06-25",
        "expected_class": "PASS",
        "why_selected": "Real later iteration with different AI product / open-source topics and complete semantic modules.",
        "case_titles": {
            "case_a": "Qwen-AgentWorld 开源语言世界模型",
            "case_b": "xAI Grok + Interactive Brokers 交易工作流集成",
            "case_c": "OpenAI Codex Remote 工程控制平面",
        },
        "sources": {
            "training_markdown": "outputs/daily-training/2026-06-25/training-v5-raw.md",
            "source_notes": "outputs/daily-training/2026-06-25/source-notes-v5.md",
            "quality_report": "outputs/daily-training/2026-06-25/training-v5-quality-report.md",
        },
        "available_but_not_used": {
            "raw_html_not_reader": "outputs/daily-training/2026-06-25/training-v5-raw.html",
        },
    },
    "2026_06_25_training_v6_raw": {
        "date": "2026-06-25",
        "expected_class": "PASS",
        "why_selected": "Real accepted reader baseline with full Markdown and reader HTML.",
        "case_titles": {
            "case_a": "OpenAI + Broadcom Jalapeño 推理芯片",
            "case_b": "Mistral Connectors 企业治理控制",
            "case_c": "Google Thinking to Recall",
        },
        "sources": {
            "training_markdown": "outputs/daily-training/2026-06-25/training-v6-raw.md",
            "reader_html": "outputs/daily-training/2026-06-25/training-v6-reader.html",
            "source_notes": "outputs/daily-training/2026-06-25/source-notes-v6.md",
            "quality_report": "outputs/daily-training/2026-06-25/training-v6-quality-report.md",
        },
    },
    "2026_06_26_training_v7_raw": {
        "date": "2026-06-26",
        "expected_class": "FAIL",
        "why_selected": "Real known regression sample from the V6/V7 audit.",
        "case_titles": {
            "case_a": "OpenRouter MCP Server 模型路由进入 Agent 工具链",
            "case_b": "Runway Agent 2.0 从生成资产走向营销实验闭环",
            "case_c": "Vercel Eve 文件系统优先的 Durable Agent 框架",
        },
        "sources": {
            "training_markdown": "outputs/daily-training/2026-06-26/training-v7-raw.md",
            "reader_html": "outputs/daily-training/2026-06-26/training-v7-reader.html",
            "source_notes": "outputs/daily-training/2026-06-26/source-notes-v7.md",
            "regression_audit": "outputs/daily-training/2026-06-26/v6-v7-regression-audit.md",
            "quality_report": "outputs/daily-training/2026-06-26/training-v7-quality-report.md",
        },
    },
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--sample-id", choices=sorted(SAMPLE_DEFINITIONS), action="append")
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    rubric_dir = project_root / "docs" / "quality" / "rubric-v2.1"
    live = load_live_module(project_root)
    sample_ids = args.sample_id or list(SAMPLE_DEFINITIONS)
    results = [
        run_sample(project_root, rubric_dir, live, sample_id)
        for sample_id in sample_ids
    ]
    report_path = rubric_dir / "live-reviewer-cross-sample-report.md"
    report_path.write_text(build_report(results, rubric_dir), encoding="utf-8")
    print(
        yaml.safe_dump(
            {
                "completed": True,
                "stage": "P2B-2 cross-date / cross-topic real sample replay",
                "report_path": live.rel(project_root, report_path),
                "sample_count": len(results),
                "date_count": len({item["date"] for item in results}),
                "results": results,
            },
            allow_unicode=True,
            sort_keys=False,
        ),
        end="",
    )
    return 0


def run_sample(
    project_root: Path,
    rubric_dir: Path,
    live: Any,
    sample_id: str,
) -> dict[str, Any]:
    definition = SAMPLE_DEFINITIONS[sample_id]
    output_dir = rubric_dir / "generated-replay" / "cross-samples" / sample_id
    output_dir.mkdir(parents=True, exist_ok=True)
    sources = live.read_sources(project_root, definition["sources"])
    anchors = live.read_yaml(rubric_dir / "rubric-score-anchors.yaml")["items"]
    config = {
        "case_titles": definition["case_titles"],
        "sources": definition["sources"],
    }
    raw = live.build_raw_response(sample_id, config, sources, no_audit=False)
    raw["cross_sample"] = {
        "stage": "P2B-2",
        "sample_id": sample_id,
        "date": definition["date"],
        "expected_class": definition["expected_class"],
        "why_selected": definition["why_selected"],
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

    diff = build_expected_diff(sample_id, definition, payload, validator_result)
    manifest = build_source_manifest(project_root, sample_id, definition, sources)
    validator_result["cross_sample"] = {
        "sample_id": sample_id,
        "expected_class": definition["expected_class"],
        "expected_diff_status": diff["status"],
        "failure_origin": classify_failure_origin(validator_result, definition),
    }

    paths = {
        "raw": output_dir / "raw-reviewer-response.json",
        "reviewer": output_dir / "live-reviewer-output.json",
        "claim_map": output_dir / "live-claim-evidence-map.json",
        "failures": output_dir / "live-failure-objects.json",
        "log": output_dir / "live-generation-log.yaml",
        "validator": output_dir / "live-validator-result.yaml",
        "diff": output_dir / "live-vs-expected-diff.yaml",
        "manifest": output_dir / "source-manifest.yaml",
    }
    live.write_json(paths["raw"], raw)
    live.write_json(paths["reviewer"], payload)
    live.write_json(paths["claim_map"], claim_map)
    live.write_json(paths["failures"], failures)
    live.write_yaml(paths["validator"], validator_result)
    live.write_yaml(paths["diff"], diff)
    live.write_yaml(paths["manifest"], manifest)
    log = live.build_generation_log(
        project_root,
        rubric_dir,
        output_dir,
        sample_id,
        sources,
        {
            "reviewer": paths["reviewer"],
            "claim_map": paths["claim_map"],
            "failures": paths["failures"],
            "log": paths["log"],
            "validator": paths["validator"],
            "raw": paths["raw"],
            "diff": paths["diff"],
            "manifest": paths["manifest"],
        },
        validator_result,
        no_audit=False,
    )
    log.update(
        {
            "stage": "P2B-2",
            "cross_sample_id": sample_id,
            "local_semantic_reviewer": True,
            "live_llm_review": False,
            "not_daily_production_pipeline": True,
            "not_p2c": True,
            "expected_class": definition["expected_class"],
            "expected_class_used_for_decision": False,
            "historical_audit_used_as_release_authority": False,
            "self_review_used_as_release_authority": False,
        }
    )
    live.write_yaml(paths["log"], log)
    return {
        "sample_id": sample_id,
        "date": definition["date"],
        "expected_class": definition["expected_class"],
        "daily_decision": payload["daily_decision"],
        "publish_allowed": payload["publish_allowed"],
        "status": diff["status"],
        "failure_types": validator_result["failure_types"],
        "failure_origin": validator_result["cross_sample"]["failure_origin"],
        "output_dir": live.rel(project_root, output_dir),
    }


def build_source_manifest(
    project_root: Path,
    sample_id: str,
    definition: dict[str, Any],
    sources: dict[str, Any],
) -> dict[str, Any]:
    roles = {}
    for role in ("training_markdown", "reader_html", "source_notes", "regression_audit", "quality_report"):
        if role in definition["sources"]:
            data = sources[role]
            roles[role] = {
                "path": data["path"],
                "exists": True,
                "bytes": data["bytes"],
                "sha256": data["sha256"],
            }
        else:
            roles[role] = {"exists": False}
    return {
        "sample_id": sample_id,
        "stage": "P2B-2 cross-date / cross-topic real sample replay",
        "real_sample": True,
        "synthetic_fixture": False,
        "date": definition["date"],
        "expected_class": definition["expected_class"],
        "why_selected": definition["why_selected"],
        "sources": roles,
        "available_but_not_used": available_but_not_used(project_root, definition),
        "source_count": sum(1 for value in roles.values() if value.get("exists")),
        "local_semantic_reviewer": True,
        "live_llm_review": False,
        "not_p2c": True,
        "project_root": str(project_root),
    }


def available_but_not_used(project_root: Path, definition: dict[str, Any]) -> dict[str, Any]:
    output = {}
    for role, path_text in definition.get("available_but_not_used", {}).items():
        path = project_root / path_text
        output[role] = {
            "path": path_text,
            "exists": path.is_file(),
            "reason_not_used": "Historical raw HTML is not the structured reader HTML expected by G6/G7/G8.",
        }
    return output


def build_expected_diff(
    sample_id: str,
    definition: dict[str, Any],
    payload: dict[str, Any],
    validator_result: dict[str, Any],
) -> dict[str, Any]:
    expected = definition["expected_class"]
    decision = payload["daily_decision"]
    publish = payload["publish_allowed"]
    if expected == "PASS":
        acceptable = decision in {"PASS", "REVIEW"} and decision != "FAIL_DAILY" and not (
            decision == "PASS" and not publish
        )
        note = "Good sample may PASS or REVIEW, but must not hard-fail."
    elif expected == "REVIEW":
        acceptable = decision in {"REVIEW", "REWRITE_MODULE", "REWRITE_CASE", "USER_REVIEW_REQUIRED"} and not publish
        note = "Review sample must explain why it cannot be automatically released."
    else:
        acceptable = decision != "PASS" and not publish
        note = "Bad sample must not PASS."
    return {
        "sample_id": sample_id,
        "expected_class": expected,
        "actual_daily_decision": decision,
        "actual_publish_allowed": publish,
        "status": "MATCH" if acceptable else "MISMATCH",
        "policy": note,
        "failure_types": validator_result["failure_types"],
        "reviewer_output_valid": validator_result["schema_and_governance_payload_status"] == "PASS",
        "self_review_used_as_release_authority": False,
        "historical_audit_used_as_release_authority": False,
    }


def classify_failure_origin(
    validator_result: dict[str, Any],
    definition: dict[str, Any],
) -> dict[str, bool]:
    categories = validator_result.get("failure_categories", {})
    return {
        "content_quality": bool(categories.get("content_quality_failure")),
        "input_missing": bool(
            categories.get("html_rendering_integrity_failure")
            or categories.get("source_evidence_failure")
        ),
        "html_integrity": bool(categories.get("html_rendering_integrity_failure")),
        "source_evidence": bool(categories.get("source_evidence_failure")),
        "self_review_inflation": bool(categories.get("self_review_inflation")),
        "human_confirmation_needed": definition["expected_class"] == "REVIEW",
    }


def build_report(results: list[dict[str, Any]], rubric_dir: Path) -> str:
    dates = sorted({item["date"] for item in results})
    review_class_samples = [item for item in results if item["expected_class"] == "REVIEW"]
    p2b3 = load_p2b3_supplement_status(rubric_dir)
    combined_dates = sorted(set(dates) | set(p2b3["dates"]))
    combined_review_count = len(review_class_samples) + p2b3["review_count"]
    p2b3_blockers = []
    if len(combined_dates) < 3:
        p2b3_blockers.append(
            f"third_real_date_missing: found {len(combined_dates)} real dates ({', '.join(combined_dates)}), need >= 3"
        )
    if combined_review_count < 2:
        p2b3_blockers.append(
            f"review_borderline_samples_missing: found {combined_review_count} REVIEW samples, need >= 2"
        )
    p2b3_status = (
        "READY_WITH_2026_06_28_SUPPLEMENT"
        if not p2b3_blockers and p2b3["sample_count"]
        else "READY"
        if not p2b3_blockers
        else "BLOCKED_MISSING_REAL_SAMPLES"
    )
    pass_samples = [item for item in results if item["daily_decision"] == "PASS"]
    review_samples = [
        item for item in results
        if item["daily_decision"] in {"REVIEW", "REWRITE_MODULE", "REWRITE_CASE", "USER_REVIEW_REQUIRED"}
    ]
    fail_samples = [
        item for item in results
        if item["daily_decision"] in {"FAIL_DAILY", "PUBLISH_BLOCK", "REPLACE_CASE"}
    ]
    lines = [
        "# P2B-2 Cross-Sample Local Reviewer Report",
        "",
        "## Boundary",
        "",
        "- Stage: P2B-2 cross-date / cross-topic real sample replay.",
        "- Reviewer: local semantic reviewer.",
        "- Not a live LLM reviewer.",
        "- Does not enter P2C and does not connect to the daily production chain.",
        "- P1 governance validator is not modified by this stage.",
        "- Self-review tables and historical audit reports are evidence inputs only, not release authority.",
        "",
        "## Historical Sample Availability",
        "",
        f"- Real sample count: {len(results)}.",
        f"- Covered dates: {', '.join(dates)}.",
        f"- Date coverage status: {'OK' if len(dates) >= 3 else 'INSUFFICIENT_REAL_HISTORY'}",
        "- Current repository only contains real daily-training outputs for two dates. No synthetic fixture is used to pretend third-date coverage.",
        "",
        "## P2B-3 Readiness",
        "",
        f"- P2B-3 status: `{p2b3_status}`.",
        f"- P2B-2 corpus date count: {len(dates)} / required >= 3 for P2B-3.",
        f"- P2B-2 corpus REVIEW / borderline expected sample count: {len(review_class_samples)} / required >= 2 for P2B-3.",
        f"- P2B-3 supplement sample count: {p2b3['sample_count']}.",
        f"- Combined real date count: {len(combined_dates)} / required >= 3.",
        f"- Combined REVIEW / borderline expected sample count: {combined_review_count} / required >= 2.",
        "- Synthetic fixtures are not allowed to satisfy these counts.",
        "- P2B-2 original 6-sample corpus remains insufficient by itself; P2B-3 uses the explicit 2026-06-28 supplement when present.",
        "",
        "### P2B-3 Blockers",
        "",
        *([f"- `{item}`" for item in p2b3_blockers] or ["- None when the 2026-06-28 P2B-3 supplement is present and green."]),
        "",
        "## Results",
        "",
        "| Sample | Date | Expected | Decision | Publish | Failure origin | Output |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for result in results:
        origin = ", ".join(
            key for key, value in result["failure_origin"].items() if value
        ) or "none"
        lines.append(
            f"| `{result['sample_id']}` | `{result['date']}` | `{result['expected_class']}` | "
            f"`{result['daily_decision']}` | `{result['publish_allowed']}` | {origin} | `{result['output_dir']}` |"
        )
    lines.extend(
        [
            "",
            "## PASS Samples",
            "",
            *[f"- `{item['sample_id']}`" for item in pass_samples],
            "",
            "## REVIEW / REWRITE Hold Samples",
            "",
            *[
                f"- `{item['sample_id']}`: cannot auto-release because `{', '.join(item['failure_types']) or 'manual review boundary'}`."
                for item in review_samples
            ],
            "",
            "## FAIL Samples",
            "",
            *[
                f"- `{item['sample_id']}`: `{item['daily_decision']}` with `{', '.join(item['failure_types'])}`."
                for item in fail_samples
            ],
            "",
            "## Manual Confirmation",
            "",
            "- No sample is released because of self-review score.",
            "- No sample is released because of historical audit alone.",
            "- Third-date coverage requires additional real historical daily-training output before this can be claimed as full cross-date validation.",
            "",
        ]
    )
    return "\n".join(lines)


def load_p2b3_supplement_status(rubric_dir: Path) -> dict[str, Any]:
    root = rubric_dir / "generated-replay" / "p2b3-samples"
    output = {
        "sample_count": 0,
        "dates": [],
        "review_count": 0,
        "samples": [],
    }
    if not root.exists():
        return output
    dates: set[str] = set()
    review_count = 0
    samples = []
    for path in sorted(root.glob("*/source-manifest.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not data.get("real_sample") or data.get("synthetic_fixture"):
            continue
        sample = {
            "sample_id": data.get("sample_id"),
            "date": data.get("date"),
            "expected_class": data.get("expected_class"),
            "path": str(path.parent),
        }
        samples.append(sample)
        if data.get("date"):
            dates.add(str(data["date"]))
        if data.get("expected_class") in {"REVIEW", "BORDERLINE"}:
            review_count += 1
    output.update(
        {
            "sample_count": len(samples),
            "dates": sorted(dates),
            "review_count": review_count,
            "samples": samples,
        }
    )
    return output


def load_live_module(project_root: Path) -> Any:
    path = project_root / "scripts" / "run_live_reviewer_generation.py"
    spec = importlib.util.spec_from_file_location("run_live_reviewer_generation", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    raise SystemExit(main())
