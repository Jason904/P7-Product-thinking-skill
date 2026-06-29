#!/usr/bin/env python3
"""Generate P2A reviewer payloads from real training artifacts.

P2A intentionally uses a recorded generator. It reads the real source files,
records their hashes, and emits governance payloads from P1 calibration
fixtures. This proves the file-to-payload-to-validator plumbing without
claiming live semantic review.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


SAMPLE_IDS = ("v3_target", "v6_target", "v7_failure")
PROMPT_VERSION = "p2a-recorded-generator-v1"
GENERATION_METHOD = "recorded_fixture_replay"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--sample-id", choices=SAMPLE_IDS, required=True)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    rubric_dir = project_root / "docs" / "quality" / "rubric-v2.1"
    output_dir = (
        args.output_dir.resolve()
        if args.output_dir
        else rubric_dir / "generated-replay" / args.sample_id
    )
    result = generate_payload(project_root, rubric_dir, args.sample_id, output_dir)
    print(yaml.safe_dump(result, allow_unicode=True, sort_keys=False), end="")
    return 0 if result["completed"] else 1


def generate_payload(
    project_root: Path,
    rubric_dir: Path,
    sample_id: str,
    output_dir: Path,
) -> dict[str, Any]:
    if sample_id not in SAMPLE_IDS:
        raise ValueError(f"unsupported sample_id: {sample_id}")

    fixture_dir = rubric_dir / "fixtures" / "calibration" / sample_id
    manifest = read_yaml(fixture_dir / "source-manifest.yaml")
    source_records = collect_source_records(project_root, manifest)
    for source in source_records:
        if not source["exists"]:
            raise FileNotFoundError(source["path"])

    output_dir.mkdir(parents=True, exist_ok=True)

    reviewer_output = read_json(fixture_dir / "reviewer-output.json")
    top_claim_map = build_case_claim_evidence_map(reviewer_output, fixture_dir)
    failure_objects = read_json(fixture_dir / "failure-objects.json") if (
        fixture_dir / "failure-objects.json"
    ).exists() else []

    reviewer_output = copy.deepcopy(reviewer_output)
    reviewer_output["reviewer_id"] = "p2a-recorded-generator"
    reviewer_output["reviewed_at"] = utc_now()
    reviewer_output.setdefault("review_notes", "")
    reviewer_output["review_notes"] = (
        "P2A recorded replay: payload generated from P1 calibration fixture after "
        "reading real source artifacts. Original self-review content is not used "
        "as release evidence."
    )

    reviewer_path = output_dir / "reviewer-output.json"
    claim_map_path = output_dir / "claim-evidence-map.json"
    failure_path = output_dir / "failure-objects.json"
    validator_path = output_dir / "validator-result.yaml"
    log_path = output_dir / "generation-log.yaml"

    write_json(reviewer_path, reviewer_output)
    write_json(claim_map_path, top_claim_map)
    write_json(failure_path, failure_objects)

    validator_result = validate_outputs(
        rubric_dir=rubric_dir,
        sample_id=sample_id,
        reviewer_output=reviewer_output,
        claim_evidence_map=top_claim_map,
        failure_objects=failure_objects,
        fixture_dir=fixture_dir,
    )
    write_yaml(validator_path, validator_result)

    generation_log = {
        "sample_id": sample_id,
        "created_at": utc_now(),
        "prompt_version": PROMPT_VERSION,
        "generation_method": GENERATION_METHOD,
        "recorded_generation": True,
        "not_live_llm_review": True,
        "input_files": source_records,
        "rubric_dir": rel(project_root, rubric_dir),
        "fixture_dir": rel(project_root, fixture_dir),
        "output_paths": {
            "reviewer_output_path": rel(project_root, reviewer_path),
            "claim_evidence_map_path": rel(project_root, claim_map_path),
            "failure_objects_path": rel(project_root, failure_path),
            "generation_log_path": rel(project_root, log_path),
            "validator_result_path": rel(project_root, validator_path),
        },
        "validator_result": {
            "validator_status": validator_result["validator_status"],
            "reviewer_error_count": len(validator_result["reviewer_errors"]),
            "claim_evidence_map_error_count": len(validator_result["claim_evidence_map_errors"]),
            "failure_object_error_count": len(validator_result["failure_object_errors"]),
        },
        "self_review_policy": {
            "rule_id": "self_review_is_subject_not_authority",
            "ignored_as_release_evidence": True,
            "note": "Insight Quality Audit / self-review text is treated as reviewed content, never as a release authority.",
        },
    }
    write_yaml(log_path, generation_log)

    return {
        "completed": True,
        "sample_id": sample_id,
        "output_dir": rel(project_root, output_dir),
        "validator_status": validator_result["validator_status"],
        "daily_decision": reviewer_output["daily_decision"],
        "publish_allowed": reviewer_output["publish_allowed"],
        "recorded_generation": True,
        "not_live_llm_review": True,
    }


def collect_source_records(project_root: Path, manifest: dict[str, Any]) -> list[dict[str, Any]]:
    paths: list[str] = []
    for key in ("source_markdown", "source_html"):
        value = manifest.get(key)
        if value:
            paths.append(value)
    for value in manifest.get("source_records") or []:
        if value not in paths:
            paths.append(value)

    records = []
    for path_text in paths:
        path = project_root / path_text
        record = {
            "path": path_text,
            "exists": path.is_file(),
            "role": source_role(path_text, manifest),
            "bytes": path.stat().st_size if path.is_file() else 0,
            "sha256": sha256_file(path) if path.is_file() else None,
        }
        records.append(record)
    return records


def source_role(path_text: str, manifest: dict[str, Any]) -> str:
    if path_text == manifest.get("source_markdown"):
        return "training_markdown"
    if path_text == manifest.get("source_html"):
        return "reader_html"
    return "source_record_or_audit"


def build_case_claim_evidence_map(
    reviewer_output: dict[str, Any],
    fixture_dir: Path,
) -> dict[str, Any]:
    by_case = {}
    for case_review in reviewer_output.get("case_reviews", []):
        maps = case_review.get("claim_evidence_map") or []
        if maps:
            by_case[case_review["case_id"]] = maps[0]

    if not by_case and (fixture_dir / "claim-evidence-map.json").exists():
        claim_map = read_json(fixture_dir / "claim-evidence-map.json")
        by_case[claim_map["case_id"]] = claim_map

    return by_case


def validate_outputs(
    rubric_dir: Path,
    sample_id: str,
    reviewer_output: dict[str, Any],
    claim_evidence_map: dict[str, Any],
    failure_objects: list[dict[str, Any]],
    fixture_dir: Path,
) -> dict[str, Any]:
    validator = load_validator(rubric_dir)
    reviewer_errors = validator.validate_reviewer_output(reviewer_output, rubric_dir)
    claim_errors: list[str] = []
    for case_id, case_map in sorted(claim_evidence_map.items()):
        claim_errors.extend(
            f"{case_id}.{error}"
            for error in validator.validate_claim_evidence_map(case_map, rubric_dir)
        )
    failure_errors: list[str] = []
    for index, failure in enumerate(failure_objects):
        failure_errors.extend(
            f"failure_objects[{index}].{error}"
            for error in validator.validate_failure_object(failure, rubric_dir)
        )

    expected = read_yaml(fixture_dir / "source-manifest.yaml")
    fixture_reviewer = read_json(fixture_dir / "reviewer-output.json")
    generated_failure_types = [failure["failure_type"] for failure in failure_objects]
    expected_failure_types = expected.get("expected_failure_types") or []
    case_decisions_match = [
        generated["case_decision"] == recorded["case_decision"]
        for generated, recorded in zip(
            reviewer_output.get("case_reviews", []),
            fixture_reviewer.get("case_reviews", []),
        )
    ]

    validator_status = "PASS" if not (reviewer_errors or claim_errors or failure_errors) else "FAIL"
    failure_categories = classify_failure_categories(generated_failure_types)

    return {
        "sample_id": sample_id,
        "validator_status": validator_status,
        "reviewer_errors": reviewer_errors,
        "claim_evidence_map_errors": claim_errors,
        "failure_object_errors": failure_errors,
        "daily_decision": reviewer_output["daily_decision"],
        "publish_allowed": reviewer_output["publish_allowed"],
        "failure_types": generated_failure_types,
        "failure_categories": failure_categories,
        "golden_comparison": {
            "fixture_dir": rel(rubric_dir.parent.parent.parent, fixture_dir),
            "daily_decision": reviewer_output["daily_decision"],
            "expected_daily_decision": expected.get("expected_decision"),
            "daily_decision_matches_expected": matches_expected(
                reviewer_output["daily_decision"],
                expected.get("expected_decision"),
            ),
            "publish_allowed": reviewer_output["publish_allowed"],
            "expected_publish_allowed": expected.get("expected_publish_allowed"),
            "publish_allowed_matches_expected": reviewer_output["publish_allowed"]
            == expected.get("expected_publish_allowed"),
            "case_decisions_match_recorded_fixture": all(case_decisions_match),
            "s_level_items_match_recorded_fixture": compare_s_level_items(
                reviewer_output,
                fixture_reviewer,
            ),
            "failure_types_match_expected": set(expected_failure_types).issubset(
                set(generated_failure_types)
            ),
            "caps_applied_match_recorded_fixture": compare_caps(
                reviewer_output,
                fixture_reviewer,
            ),
        },
    }


def classify_failure_categories(failure_types: list[str]) -> dict[str, bool]:
    failure_set = set(failure_types)
    return {
        "content_quality_failure": bool(
            failure_set
            & {
                "EMPTY_8Q_REASONING",
                "INCOMPLETE_8Q_FIELDS",
                "DISCONNECTED_8Q_CHAIN",
                "BOILERPLATE_REASONING",
                "WEAK_CAUSAL_CHAIN",
                "NO_CAUSAL_MECHANISM",
                "CASE_DEPTH_IMBALANCE",
            }
        ),
        "html_rendering_integrity_failure": bool(
            failure_set & {"HTML_CONTENT_LOSS", "HTML_EMPTY_SECTION"}
        ),
        "source_evidence_failure": bool(
            failure_set
            & {
                "NO_AB_EVIDENCE_FOR_CORE_CLAIM",
                "CLAIM_EVIDENCE_MISMATCH",
                "SOURCE_UNTRACEABLE",
                "C_OR_D_FACT_SUPPORTS_CORE_CLAIM",
            }
        ),
        "self_review_inflation": "SELF_REVIEW_INFLATION" in failure_set,
    }


def matches_expected(actual: str, expected: Any) -> bool:
    if isinstance(expected, list):
        return actual in expected
    return actual == expected


def compare_s_level_items(generated: dict[str, Any], recorded: dict[str, Any]) -> bool:
    return s_level_snapshot(generated) == s_level_snapshot(recorded)


def s_level_snapshot(payload: dict[str, Any]) -> list[tuple[str, str, int, str]]:
    snapshot = []
    for case in payload.get("case_reviews", []):
        for item in case.get("item_reviews", []):
            if item.get("level") == "S":
                snapshot.append(
                    (
                        case.get("case_id"),
                        item.get("item_id"),
                        item.get("final_score"),
                        item.get("decision"),
                    )
                )
    return snapshot


def compare_caps(generated: dict[str, Any], recorded: dict[str, Any]) -> bool:
    return caps_snapshot(generated) == caps_snapshot(recorded)


def caps_snapshot(payload: dict[str, Any]) -> list[tuple[str, str, tuple[str, ...]]]:
    snapshot = []
    for case in payload.get("case_reviews", []):
        for item in case.get("item_reviews", []):
            reasons = tuple(cap.get("reason", "") for cap in item.get("caps_applied", []))
            if reasons:
                snapshot.append((case.get("case_id"), item.get("item_id"), reasons))
    return snapshot


def load_validator(rubric_dir: Path):
    path = rubric_dir / "rubric_governance_validator.py"
    spec = importlib.util.spec_from_file_location("rubric_governance_validator", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def read_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def write_yaml(path: Path, payload: Any) -> None:
    path.write_text(yaml.safe_dump(payload, allow_unicode=True, sort_keys=False), encoding="utf-8")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
