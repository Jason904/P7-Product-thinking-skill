#!/usr/bin/env python3
"""P2B-1 stability / no-audit stress replay for the local semantic reviewer."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import re
from pathlib import Path
from typing import Any

import yaml


SCENARIOS: dict[str, dict[str, Any]] = {
    "v7_failure_no_audit_should_not_pass": {
        "base_sample_id": "v7_failure",
        "remove_sources": ["regression_audit"],
        "no_audit": True,
        "expected_daily_decision": ["REVIEW", "REWRITE_MODULE", "REWRITE_CASE", "FAIL_DAILY", "PUBLISH_BLOCK"],
        "expected_publish_allowed": False,
        "expected_quality_origin": "content_quality_or_no_audit_uncertainty",
    },
    "v7_failure_without_self_review_should_not_pass": {
        "base_sample_id": "v7_failure",
        "text_transforms": ["remove_self_review_sections"],
        "expected_daily_decision": ["REVIEW", "REWRITE_MODULE", "REWRITE_CASE", "FAIL_DAILY", "PUBLISH_BLOCK"],
        "expected_publish_allowed": False,
        "expected_quality_origin": "content_quality",
    },
    "v7_failure_without_reader_html_should_not_pass_or_review": {
        "base_sample_id": "v7_failure",
        "remove_sources": ["reader_html"],
        "expected_daily_decision": ["REVIEW", "REWRITE_MODULE", "REWRITE_CASE", "FAIL_DAILY", "PUBLISH_BLOCK"],
        "expected_publish_allowed": False,
        "expected_quality_origin": "content_quality_plus_input_missing",
    },
    "v7_failure_without_source_notes_should_not_pass_or_review": {
        "base_sample_id": "v7_failure",
        "remove_sources": ["source_notes"],
        "expected_daily_decision": ["REVIEW", "REWRITE_MODULE", "REWRITE_CASE", "FAIL_DAILY", "PUBLISH_BLOCK"],
        "expected_publish_allowed": False,
        "expected_quality_origin": "content_quality_plus_input_missing",
    },
    "v3_without_self_review_should_still_pass_or_review_not_fail": {
        "base_sample_id": "v3_target",
        "text_transforms": ["remove_self_review_sections"],
        "expected_daily_decision": ["PASS", "REVIEW"],
        "expected_not_decision": ["FAIL_DAILY", "PUBLISH_BLOCK", "REPLACE_CASE"],
        "expected_quality_origin": "good_sample_with_self_review_removed",
    },
    "v6_without_quality_report_should_still_pass_or_review_not_fail": {
        "base_sample_id": "v6_target",
        "remove_sources": ["quality_report"],
        "expected_daily_decision": ["PASS", "REVIEW"],
        "expected_not_decision": ["FAIL_DAILY", "PUBLISH_BLOCK", "REPLACE_CASE"],
        "expected_quality_origin": "good_sample_with_auxiliary_report_removed",
    },
    "case_order_changed_should_not_change_daily_decision": {
        "base_sample_id": "v6_target",
        "text_transforms": ["swap_case_a_and_case_b"],
        "expected_daily_decision": ["PASS", "REVIEW"],
        "expected_not_decision": ["FAIL_DAILY", "PUBLISH_BLOCK", "REPLACE_CASE"],
        "compare_to_base_sample": "v6_target",
        "expected_quality_origin": "input_order_perturbation",
    },
    "repeated_run_same_input_should_be_deterministic": {
        "base_sample_id": "v6_target",
        "repeat_same_input": True,
        "expected_daily_decision": ["PASS"],
        "expected_publish_allowed": True,
        "expected_quality_origin": "determinism_check",
    },
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--scenario", choices=sorted(SCENARIOS), action="append")
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    rubric_dir = project_root / "docs" / "quality" / "rubric-v2.1"
    live = load_live_module(project_root)
    scenarios = args.scenario or list(SCENARIOS)
    results = [
        run_scenario(project_root, rubric_dir, live, scenario_id)
        for scenario_id in scenarios
    ]
    report_path = rubric_dir / "live-reviewer-stability-report.md"
    report_path.write_text(build_report(results), encoding="utf-8")
    print(
        yaml.safe_dump(
            {
                "completed": True,
                "stage": "P2B-1 stability / no-audit stress",
                "report_path": live.rel(project_root, report_path),
                "scenario_count": len(results),
                "results": results,
            },
            allow_unicode=True,
            sort_keys=False,
        ),
        end="",
    )
    return 0


def run_scenario(
    project_root: Path,
    rubric_dir: Path,
    live: Any,
    scenario_id: str,
) -> dict[str, Any]:
    scenario = SCENARIOS[scenario_id]
    base_sample_id = scenario["base_sample_id"]
    base_config = live.SAMPLE_CONFIGS[base_sample_id]
    config = copy.deepcopy(base_config)
    output_dir = rubric_dir / "generated-replay" / "stability" / scenario_id
    output_dir.mkdir(parents=True, exist_ok=True)

    source_map = {
        role: path
        for role, path in config["sources"].items()
        if role not in set(scenario.get("remove_sources", []))
    }
    sources = live.read_sources(project_root, source_map)
    perturbation_manifest = build_perturbation_manifest(
        scenario_id,
        scenario,
        source_map,
        base_config,
    )
    apply_source_transforms(sources, scenario.get("text_transforms", []), perturbation_manifest)

    anchors = live.read_yaml(rubric_dir / "rubric-score-anchors.yaml")["items"]
    no_audit = bool(scenario.get("no_audit"))
    raw = live.build_raw_response(base_sample_id, config, sources, no_audit=no_audit)
    raw["stability_scenario"] = {
        "scenario_id": scenario_id,
        "stage": "P2B-1",
        "base_sample_id": base_sample_id,
        "expected_quality_origin": scenario["expected_quality_origin"],
    }
    failures = live.build_failure_objects(base_sample_id, raw)
    payload = live.build_reviewer_output(base_sample_id, config, raw, anchors, failures)
    claim_map = {
        case["case_id"]: case["claim_evidence_map"][0]
        for case in payload["case_reviews"]
    }
    validator_result = live.validate_outputs(base_sample_id, rubric_dir, payload, claim_map, failures)
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
        for case in payload["case_reviews"]:
            if payload["daily_decision"] != "PASS":
                case["publish_allowed"] = case["case_decision"] == "PASS"
        validator_result = live.validate_outputs(base_sample_id, rubric_dir, payload, claim_map, failures)

    determinism = None
    if scenario.get("repeat_same_input"):
        determinism = run_determinism_check(live, base_sample_id, config, sources, anchors, no_audit)
        perturbation_manifest["determinism_check"] = determinism

    paths = {
        "raw": output_dir / "raw-reviewer-response.json",
        "reviewer": output_dir / "live-reviewer-output.json",
        "claim_map": output_dir / "live-claim-evidence-map.json",
        "failures": output_dir / "live-failure-objects.json",
        "log": output_dir / "live-generation-log.yaml",
        "validator": output_dir / "live-validator-result.yaml",
        "manifest": output_dir / "perturbation-manifest.yaml",
    }
    live.write_json(paths["raw"], raw)
    live.write_json(paths["reviewer"], payload)
    live.write_json(paths["claim_map"], claim_map)
    live.write_json(paths["failures"], failures)

    validator_result["stability_scenario"] = scenario_id
    validator_result["expected_daily_decision"] = scenario["expected_daily_decision"]
    validator_result["input_missing"] = scenario.get("remove_sources", [])
    validator_result["failure_origin"] = classify_stability_failure_origin(validator_result, scenario)
    if determinism is not None:
        validator_result["determinism_check"] = determinism
    live.write_yaml(paths["validator"], validator_result)

    log = live.build_generation_log(
        project_root,
        rubric_dir,
        output_dir,
        base_sample_id,
        sources,
        {
            "reviewer": paths["reviewer"],
            "claim_map": paths["claim_map"],
            "failures": paths["failures"],
            "log": paths["log"],
            "validator": paths["validator"],
            "raw": paths["raw"],
            "manifest": paths["manifest"],
        },
        validator_result,
        no_audit=no_audit,
    )
    log.update(
        {
            "stage": "P2B-1",
            "stability_scenario": scenario_id,
            "base_sample_id": base_sample_id,
            "live_llm_review": False,
            "local_semantic_reviewer": True,
            "not_daily_production_pipeline": True,
            "not_p2c": True,
            "perturbations": perturbation_manifest["perturbations"],
        }
    )
    live.write_yaml(paths["log"], log)
    live.write_yaml(paths["manifest"], perturbation_manifest)

    return {
        "scenario_id": scenario_id,
        "base_sample_id": base_sample_id,
        "daily_decision": payload["daily_decision"],
        "publish_allowed": payload["publish_allowed"],
        "failure_types": validator_result["failure_types"],
        "failure_origin": validator_result["failure_origin"],
        "output_dir": live.rel(project_root, output_dir),
    }


def build_perturbation_manifest(
    scenario_id: str,
    scenario: dict[str, Any],
    source_map: dict[str, str],
    base_config: dict[str, Any],
) -> dict[str, Any]:
    removed = sorted(set(base_config["sources"]) - set(source_map))
    perturbations = []
    for role in removed:
        perturbations.append(
            {
                "type": "remove_source",
                "role": role,
                "original_path": base_config["sources"][role],
            }
        )
    for transform in scenario.get("text_transforms", []):
        perturbations.append({"type": "text_transform", "name": transform})
    if scenario.get("repeat_same_input"):
        perturbations.append({"type": "repeat_same_input", "runs": 2})
    return {
        "scenario_id": scenario_id,
        "stage": "P2B-1 stability / no-audit stress",
        "base_sample_id": scenario["base_sample_id"],
        "synthetic_payload_used": False,
        "p1_recorded_payload_used_as_generation": False,
        "local_semantic_reviewer": True,
        "live_llm_review": False,
        "not_p2c": True,
        "source_roles_after_perturbation": sorted(source_map),
        "removed_source_roles": removed,
        "perturbations": perturbations,
        "expected_daily_decision": scenario["expected_daily_decision"],
        "expected_quality_origin": scenario["expected_quality_origin"],
    }


def apply_source_transforms(
    sources: dict[str, Any],
    transforms: list[str],
    manifest: dict[str, Any],
) -> None:
    for transform in transforms:
        if transform == "remove_self_review_sections":
            apply_text_transform(sources, "training_markdown", remove_self_review_sections, transform, manifest)
            if "regression_audit" in sources:
                apply_text_transform(sources, "regression_audit", mask_self_review_audit_mentions, transform, manifest)
        elif transform == "swap_case_a_and_case_b":
            apply_text_transform(sources, "training_markdown", swap_case_a_and_case_b, transform, manifest)
        else:
            raise ValueError(f"Unknown stability transform: {transform}")


def apply_text_transform(
    sources: dict[str, Any],
    role: str,
    transform_func: Any,
    transform_name: str,
    manifest: dict[str, Any],
) -> None:
    if role not in sources:
        return
    before = sources[role]["text"]
    after = transform_func(before)
    sources[role]["text"] = after
    sources[role]["bytes"] = len(after.encode("utf-8"))
    sources[role]["sha256"] = sha256_text(after)
    manifest["perturbations"].append(
        {
            "type": "applied_text_transform",
            "name": transform_name,
            "role": role,
            "changed": before != after,
            "original_sha256": sha256_text(before),
            "perturbed_sha256": sources[role]["sha256"],
        }
    )


def remove_self_review_sections(text: str) -> str:
    pattern = re.compile(r"(?ms)^【Insight Quality Audit】\n.*?(?=^【训练能力】|^## 七、今日训练复盘|^### Case [ABC]|^【Case】|\Z)")
    return pattern.sub("", text)


def mask_self_review_audit_mentions(text: str) -> str:
    return re.sub(r"(?im)^.*self-score.*\n?", "", text)


def swap_case_a_and_case_b(text: str) -> str:
    deep_start = text.find("## 四、今日 3 个深度 case")
    if deep_start == -1:
        return text
    next_section = text.find("## 五、今日自主训练题", deep_start)
    if next_section == -1:
        next_section = len(text)
    prefix = text[:deep_start]
    deep = text[deep_start:next_section]
    suffix = text[next_section:]
    matches = list(re.finditer(r"(?m)^### Case ([ABC])(?:：([^\n]+))?\s*$", deep))
    if len(matches) < 3:
        return text
    blocks = []
    for index, match in enumerate(matches[:3]):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(deep)
        blocks.append(deep[match.start():end])
    header = deep[:matches[0].start()]
    swapped = header + blocks[1] + "\n" + blocks[0] + "\n" + blocks[2]
    return prefix + swapped + suffix


def run_determinism_check(
    live: Any,
    sample_id: str,
    config: dict[str, Any],
    sources: dict[str, Any],
    anchors: dict[str, Any],
    no_audit: bool,
) -> dict[str, Any]:
    first = build_canonical_bundle(live, sample_id, config, sources, anchors, no_audit)
    second = build_canonical_bundle(live, sample_id, config, sources, anchors, no_audit)
    first_hashes = {name: stable_hash(payload) for name, payload in first.items()}
    second_hashes = {name: stable_hash(payload) for name, payload in second.items()}
    return {
        "canonical_hashes_match": first_hashes == second_hashes,
        "first_hashes": first_hashes,
        "second_hashes": second_hashes,
    }


def build_canonical_bundle(
    live: Any,
    sample_id: str,
    config: dict[str, Any],
    sources: dict[str, Any],
    anchors: dict[str, Any],
    no_audit: bool,
) -> dict[str, Any]:
    raw = live.build_raw_response(sample_id, config, copy.deepcopy(sources), no_audit=no_audit)
    failures = live.build_failure_objects(sample_id, raw)
    payload = live.build_reviewer_output(sample_id, config, raw, anchors, failures)
    claim_map = {
        case["case_id"]: case["claim_evidence_map"][0]
        for case in payload["case_reviews"]
    }
    return {
        "raw": scrub_volatile(raw),
        "payload": scrub_volatile(payload),
        "claim_map": claim_map,
        "failures": failures,
    }


def scrub_volatile(payload: Any) -> Any:
    if isinstance(payload, dict):
        return {
            key: scrub_volatile(value)
            for key, value in payload.items()
            if key not in {"generated_at", "reviewed_at", "created_at"}
        }
    if isinstance(payload, list):
        return [scrub_volatile(value) for value in payload]
    return payload


def stable_hash(payload: Any) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def classify_stability_failure_origin(
    validator_result: dict[str, Any],
    scenario: dict[str, Any],
) -> dict[str, bool]:
    input_missing = bool(scenario.get("remove_sources"))
    categories = validator_result.get("failure_categories", {})
    return {
        "content_quality": bool(categories.get("content_quality_failure")),
        "input_missing": input_missing,
        "html_integrity": bool(categories.get("html_rendering_integrity_failure")),
        "source_evidence": bool(categories.get("source_evidence_failure")),
        "self_review_inflation": bool(categories.get("self_review_inflation")),
    }


def build_report(results: list[dict[str, Any]]) -> str:
    lines = [
        "# P2B-1 Stability / No-Audit Stress Report",
        "",
        "## Boundary",
        "",
        "- Stage: P2B-1 stability / no-audit stress.",
        "- Reviewer: local semantic reviewer.",
        "- Not a live LLM reviewer.",
        "- Does not enter P2C and does not connect to the daily production chain.",
        "- This stage does not enter P2C.",
        "- P1 recorded payloads are not used as generation results.",
        "",
        "## Purpose",
        "",
        "This stage checks whether input perturbations and missing auxiliary audit inputs cause bad samples to be mistakenly released or good samples to be incorrectly hard-failed.",
        "",
        "## Results",
        "",
        "| Scenario | Base | Decision | Publish | Failure origin | Output |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for result in results:
        origin = ", ".join(
            key for key, value in result["failure_origin"].items() if value
        ) or "none"
        lines.append(
            f"| `{result['scenario_id']}` | `{result['base_sample_id']}` | "
            f"`{result['daily_decision']}` | `{result['publish_allowed']}` | "
            f"{origin} | `{result['output_dir']}` |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- V7 perturbations must remain non-PASS; if they fail, the report separates content-quality failures from missing-input risk.",
            "- V3/V6 perturbations may become REVIEW when auxiliary evidence is missing, but they must not become FAIL_DAILY unless the evidence loss creates a defensible hard block.",
            "- Case-order perturbation verifies that the daily decision does not depend on case ordering.",
            "- Repeated-run perturbation verifies deterministic reviewer behavior after removing timestamp fields.",
            "",
        ]
    )
    return "\n".join(lines)


def load_live_module(project_root: Path) -> Any:
    path = project_root / "scripts" / "run_live_reviewer_generation.py"
    spec = importlib.util.spec_from_file_location("run_live_reviewer_generation", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    raise SystemExit(main())
