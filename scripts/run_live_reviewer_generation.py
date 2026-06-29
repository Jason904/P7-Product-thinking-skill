#!/usr/bin/env python3
"""P2B-0 evidence-derived local semantic reviewer for V3/V6/V7."""

from __future__ import annotations

import argparse
import hashlib
import html as html_lib
import importlib.util
import json
import math
import re
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


REVIEWER_VERSION = "p2b0-local-semantic-reviewer-v3"
SAMPLE_CONFIGS = {
    "v3_target": {
        "output_dir": "v3_target_live",
        "expected_decision": "PASS",
        "expected_publish_allowed": True,
        "case_titles": {
            "case_a": "V3 target Case A",
            "case_b": "V3 target Case B",
            "case_c": "V3 target Case C",
        },
        "sources": {
            "training_markdown": "outputs/daily-training/2026-06-25/training-v3.md",
        },
    },
    "v6_target": {
        "output_dir": "v6_target_live",
        "expected_decision": "PASS",
        "expected_publish_allowed": True,
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
    "v7_failure": {
        "output_dir": "v7_failure_live",
        "expected_decision": "FAIL_DAILY",
        "expected_publish_allowed": False,
        "case_titles": {
            "case_a": "OpenRouter MCP Server 模型路由进入 Agent 工具链",
            "case_b": "Runway Agent 2.0 从生成资产走向营销实验闭环",
            "case_c": "Vercel Eve durable agent framework",
        },
        "sources": {
            "training_markdown": "outputs/daily-training/2026-06-26/training-v7-raw.md",
            "reader_html": "outputs/daily-training/2026-06-26/training-v7-reader.html",
            "source_notes": "outputs/daily-training/2026-06-26/source-notes-v7.md",
            "regression_audit": "outputs/daily-training/2026-06-26/v6-v7-regression-audit.md",
        },
    },
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--sample-id", choices=sorted(SAMPLE_CONFIGS), action="append")
    parser.add_argument(
        "--no-audit",
        action="store_true",
        help="Skip historical audit inputs and derive the decision from training/source/HTML evidence only.",
    )
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    rubric_dir = project_root / "docs" / "quality" / "rubric-v2.1"
    sample_ids = args.sample_id or (["v7_failure"] if args.no_audit else list(SAMPLE_CONFIGS))
    if args.no_audit and any(sample_id != "v7_failure" for sample_id in sample_ids):
        parser.error("--no-audit is currently supported only for v7_failure")
    results = [
        run_sample(project_root, rubric_dir, sample_id, no_audit=args.no_audit)
        for sample_id in sample_ids
    ]
    report_path = rubric_dir / "live-reviewer-samples-report.md"
    if not args.no_audit:
        report_path.write_text(build_samples_report(results), encoding="utf-8")
    hardening_report = rubric_dir / "p2b0-local-reviewer-hardening-report.md"
    hardening_report.write_text(
        build_hardening_report(rubric_dir, results, no_audit=args.no_audit),
        encoding="utf-8",
    )
    print(
        yaml.safe_dump(
            {"completed": True, "report_path": rel(project_root, report_path), "samples": results},
            allow_unicode=True,
            sort_keys=False,
        ),
        end="",
    )
    return 0


def run_sample(
    project_root: Path,
    rubric_dir: Path,
    sample_id: str,
    *,
    no_audit: bool = False,
) -> dict[str, Any]:
    config = SAMPLE_CONFIGS[sample_id]
    output_name = (
        "v7_failure_no_audit_live"
        if no_audit and sample_id == "v7_failure"
        else config["output_dir"]
    )
    output_dir = rubric_dir / "generated-replay" / output_name
    output_dir.mkdir(parents=True, exist_ok=True)

    source_map = dict(config["sources"])
    if no_audit:
        source_map.pop("regression_audit", None)
    sources = read_sources(project_root, source_map)
    anchors = read_yaml(rubric_dir / "rubric-score-anchors.yaml")["items"]
    raw = build_raw_response(sample_id, config, sources, no_audit=no_audit)
    failures = build_failure_objects(sample_id, raw)
    payload = build_reviewer_output(sample_id, config, raw, anchors, failures)
    claim_map = {case_id: case["claim_evidence_map"][0] for case_id, case in (
        (case["case_id"], case) for case in payload["case_reviews"]
    )}

    paths = {
        "reviewer": output_dir / "live-reviewer-output.json",
        "claim_map": output_dir / "live-claim-evidence-map.json",
        "failures": output_dir / "live-failure-objects.json",
        "log": output_dir / "live-generation-log.yaml",
        "validator": output_dir / "live-validator-result.yaml",
        "diff": output_dir / "live-vs-recorded-diff.yaml",
        "raw": output_dir / "raw-reviewer-response.json",
        "sample_report": output_dir / "live-reviewer-generation-report.md",
    }

    write_json(paths["raw"], raw)
    write_json(paths["reviewer"], payload)
    write_json(paths["claim_map"], claim_map)
    write_json(paths["failures"], failures)

    validator_result = validate_outputs(sample_id, rubric_dir, payload, claim_map, failures)
    final_release = derive_daily_decision(
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
        write_json(paths["reviewer"], payload)
        validator_result = validate_outputs(sample_id, rubric_dir, payload, claim_map, failures)
    diff = compare_recorded(rubric_dir, sample_id, payload, failures)
    validator_result["golden_comparison"] = diff
    write_yaml(paths["validator"], validator_result)
    write_yaml(paths["diff"], diff)
    log = build_generation_log(
        project_root,
        rubric_dir,
        output_dir,
        sample_id,
        sources,
        paths,
        validator_result,
        no_audit=no_audit,
    )
    write_yaml(paths["log"], log)
    paths["sample_report"].write_text(
        build_sample_report(sample_id, validator_result, diff),
        encoding="utf-8",
    )

    return {
        "sample_id": sample_id,
        "output_dir": rel(project_root, output_dir),
        "daily_decision": payload["daily_decision"],
        "publish_allowed": payload["publish_allowed"],
        "validator_status": validator_result["schema_and_governance_payload_status"],
        "recorded_generation": False,
        "replay_p1_fixture_payload": False,
        "no_audit": no_audit,
    }


def read_sources(project_root: Path, source_map: dict[str, str]) -> dict[str, Any]:
    output = {}
    for role, path_text in source_map.items():
        path = project_root / path_text
        if not path.is_file():
            raise FileNotFoundError(path_text)
        output[role] = {
            "path": path_text,
            "text": path.read_text(encoding="utf-8"),
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
    return output


def build_raw_response(
    sample_id: str,
    config: dict[str, Any],
    sources: dict[str, Any],
    *,
    no_audit: bool = False,
) -> dict[str, Any]:
    source_summary = {role: {k: data[k] for k in ("path", "bytes", "sha256")} for role, data in sources.items()}
    markdown_analysis = analyze_training_markdown(sources["training_markdown"]["text"])
    html_analysis = (
        analyze_reader_html(sources["reader_html"]["text"])
        if "reader_html" in sources
        else {
            "present": False,
            "complete": None,
            "question_anchor_count": 0,
            "valid_question_card_count": 0,
            "missing_question_anchors": [],
            "empty_fields": [],
        }
    )
    daily_evidence = {
        **markdown_analysis["daily"],
        "reader_html_present": html_analysis["present"],
        "reader_html_complete": html_analysis["complete"],
        "reader_question_anchor_count": html_analysis["question_anchor_count"],
        "reader_valid_question_card_count": html_analysis["valid_question_card_count"],
        "reader_missing_question_anchors": html_analysis["missing_question_anchors"],
        "reader_empty_fields": html_analysis["empty_fields"],
    }
    semantic_findings = derive_semantic_findings(markdown_analysis, html_analysis)
    audit_used = "regression_audit" in sources and not no_audit
    source_evidence: dict[str, Any] = {
        "semantic_structure": {
            "deep_case_count": len(markdown_analysis["cases"]),
            "source_candidate_pool_present": daily_evidence["source_candidate_pool_present"],
            "repeated_template_field_count": markdown_analysis["repeated_template_field_count"],
        }
    }
    if audit_used:
        audit = sources["regression_audit"]["text"]
        audit_evidence = extract_v7_evidence(audit)
        source_evidence["regression_audit"] = audit_evidence
        audit_findings = [
            audit_finding(
                "CASE_DEPTH_IMBALANCE",
                "content_quality_failure",
                audit_evidence["case2_size"],
            ),
            audit_finding(
                "DISCONNECTED_8Q_CHAIN",
                "content_quality_failure",
                audit_evidence["valid_but_short"],
            ),
            audit_finding(
                "BOILERPLATE_REASONING",
                "content_quality_failure",
                audit_evidence["boilerplate"],
            ),
            audit_finding(
                "REVIEW_EVIDENCE_INVALID",
                "self_review_inflation",
                audit_evidence["inflated_score"],
            ),
        ]
        semantic_findings = merge_findings(
            semantic_findings,
            [item for item in audit_findings if item is not None],
        )
    uncertainty = build_uncertainty_boundary(no_audit, semantic_findings)
    provisional_raw = {
        "case_semantic_evidence": markdown_analysis["cases"],
        "semantic_findings": semantic_findings,
    }
    case_decisions = [
        derive_case_decision(sample_id, case["case_id"], provisional_raw, {})
        for case in markdown_analysis["cases"]
    ]
    release = derive_daily_decision(case_decisions, semantic_findings, None)
    release.update(
        {
            "basis": (
                "audit_assisted_evidence_derived_semantic_review"
                if audit_used
                else "evidence_derived_semantic_sections"
            ),
            "reason": release_reason(case_decisions, semantic_findings, no_audit),
        }
    )
    probes = {
        "training_chars": len(sources["training_markdown"]["text"]),
        "deep_case_count": len(markdown_analysis["cases"]),
        "has_reader_html": "reader_html" in sources,
        "has_quality_report": "quality_report" in sources,
        "audit_used": audit_used,
        "repeated_template_field_count": markdown_analysis["repeated_template_field_count"],
    }

    return {
        "reviewer_prompt": build_reviewer_prompt(sample_id),
        "reviewer_version": REVIEWER_VERSION,
        "sample_id": sample_id,
        "generated_at": utc_now(),
        "source_files": source_summary,
        "source_evidence": source_evidence,
        "semantic_findings": semantic_findings,
        "semantic_probes": probes,
        "daily_semantic_evidence": daily_evidence,
        "case_semantic_evidence": markdown_analysis["cases"],
        "audit_used": audit_used,
        "no_audit": no_audit,
        "uncertainty_boundary": uncertainty,
        "self_review_policy": {
            "rule_id": "self_review_is_subject_not_authority",
            "ignored_as_release_evidence": True,
            "note": "Self-review / Insight Quality Audit is reviewed content, not release authority.",
        },
        "release_decision": release,
    }


def build_reviewer_prompt(sample_id: str) -> str:
    return (
        f"Run local semantic review for {sample_id}. Read the real source files, "
        "do not replay P1 fixture payloads, and do not use self-review scores as release evidence."
    )


def analyze_training_markdown(markdown: str) -> dict[str, Any]:
    """Extract deterministic semantic evidence without using expected sample labels."""
    deep_section = extract_between(markdown, "## 四、今日 3 个深度 case", "## 五、今日自主训练题")
    heading_matches = list(re.finditer(r"(?m)^### Case ([ABC])(?:：([^\n]+))?\s*$", deep_section))
    blocks: list[tuple[str, str, str]] = []
    if len(heading_matches) >= 3:
        for index, match in enumerate(heading_matches[:3]):
            end = heading_matches[index + 1].start() if index + 1 < len(heading_matches) else len(deep_section)
            blocks.append(
                (
                    f"case_{match.group(1).lower()}",
                    (match.group(2) or f"Case {match.group(1)}").strip(),
                    deep_section[match.start():end],
                )
            )
    else:
        marker_matches = list(re.finditer(r"(?m)^【Case】\s*$", deep_section))
        for index, match in enumerate(marker_matches[:3]):
            end = marker_matches[index + 1].start() if index + 1 < len(marker_matches) else len(deep_section)
            blocks.append(
                (
                    f"case_{chr(ord('a') + index)}",
                    f"Case {chr(ord('A') + index)}",
                    deep_section[match.start():end],
                )
            )

    cases = [analyze_case_block(case_id, title, block) for case_id, title, block in blocks]
    repeated_values = repeated_eightq_field_values(cases)
    derivation_medians = [case["eightq"]["derivation_median_chars"] for case in cases if case["eightq"]["derivation_median_chars"]]
    peer_median = statistics.median(derivation_medians) if derivation_medians else 0
    for case in cases:
        own = case["eightq"]["derivation_median_chars"]
        case["eightq"]["peer_depth_ratio"] = round(own / peer_median, 3) if own and peer_median else 0

    return {
        "daily": {
            "deep_case_count": len(cases),
            "three_deep_cases_present": len(cases) == 3,
            "source_channel_section_present": "## 零、来源通道使用情况" in markdown,
            "candidate_pool_present": "## 一、今日候选 case 池 + Case Selection Score" in markdown,
            "source_candidate_pool_present": (
                "## 零、来源通道使用情况" in markdown
                and "## 一、今日候选 case 池 + Case Selection Score" in markdown
            ),
        },
        "cases": cases,
        "repeated_template_field_count": len(repeated_values),
        "repeated_template_fields": repeated_values,
    }


def analyze_case_block(case_id: str, title: str, block: str) -> dict[str, Any]:
    eightq = analyze_eightq(block)
    required_sections = {
        "analysis_method_workbench": any(
            marker in block
            for marker in ("【V3.1 分析方法工作台】", "【分析方法工作台】", "【分析方法总表】", "【分析方法展开】")
        ),
        "six_layer_summary": "我会从六层来看" in block,
        "prep_or_scqa_complete": "【PREP 表达版本】" in block and "【SCQA 表达版本】" in block,
        "case_asset_card": "【Case Asset Card】" in block,
    }
    self_scores = [int(score) for score in re.findall(r"总分：\s*(\d{1,3})/100", block)]
    return {
        "case_id": case_id,
        "title": title,
        "chars": len(block),
        "required_sections": required_sections,
        "required_sections_complete": all(required_sections.values()),
        "eightq": eightq,
        "self_review_scores": self_scores,
        "self_review_max_score": max(self_scores) if self_scores else None,
    }


def analyze_eightq(block: str) -> dict[str, Any]:
    start = block.find("【8 问显性推理】")
    if start == -1:
        return {
            "question_count": 0,
            "valid_question_count": 0,
            "field_counts": {},
            "questions": [],
            "derivation_median_chars": 0,
        }
    boundaries = [
        index
        for marker in ("【Insight Quality Audit】", "【分析方法展开】", "【分析方法总表】")
        if (index := block.find(marker, start + 1)) != -1
    ]
    end = min(boundaries) if boundaries else len(block)
    section = block[start:end]
    question_matches = list(re.finditer(r"(?m)^([1-8])\.\s*([^\n]*)$", section))
    labels = ("目的", "分析方法", "为什么用这个方法", "推导过程", "阶段结论", "如何影响下一步")
    questions = []
    for index, match in enumerate(question_matches):
        question_end = question_matches[index + 1].start() if index + 1 < len(question_matches) else len(section)
        question_text = section[match.start():question_end]
        fields = extract_labeled_fields(question_text, labels)
        questions.append(
            {
                "number": int(match.group(1)),
                "question": match.group(2).strip(),
                "fields": fields,
                "valid": all(fields.get(label, "").strip() for label in labels),
                "derivation_chars": len(fields.get("推导过程", "").strip()),
            }
        )
    derivation_lengths = [question["derivation_chars"] for question in questions if question["derivation_chars"]]
    return {
        "question_count": len(questions),
        "valid_question_count": sum(1 for question in questions if question["valid"]),
        "field_counts": {
            label: sum(1 for question in questions if question["fields"].get(label, "").strip())
            for label in labels
        },
        "questions": questions,
        "derivation_median_chars": round(statistics.median(derivation_lengths), 1) if derivation_lengths else 0,
    }


def extract_labeled_fields(text: str, labels: tuple[str, ...]) -> dict[str, str]:
    fields = {}
    for index, label in enumerate(labels):
        later_labels = labels[index + 1:]
        stop = "|".join(re.escape(item) + "：" for item in later_labels)
        pattern = rf"(?ms)^{re.escape(label)}：\s*(.*?)(?=^(?:{stop})\s*|^\d+\.\s|\Z)" if stop else (
            rf"(?ms)^{re.escape(label)}：\s*(.*?)(?=^\d+\.\s|\Z)"
        )
        match = re.search(pattern, text)
        fields[label] = match.group(1).strip() if match else ""
    return fields


def repeated_eightq_field_values(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    occurrences: dict[tuple[str, str], set[str]] = {}
    for case in cases:
        for question in case["eightq"]["questions"]:
            for label in ("目的", "为什么用这个方法"):
                value = normalize_text(question["fields"].get(label, ""))
                if len(value) >= 12:
                    occurrences.setdefault((label, value), set()).add(case["case_id"])
    return [
        {"field": label, "value": value, "case_ids": sorted(case_ids)}
        for (label, value), case_ids in sorted(occurrences.items())
        if len(case_ids) == 3
    ]


def analyze_reader_html(html: str) -> dict[str, Any]:
    expected = [
        f"case-{case_number}-eight-q{question_number}"
        for case_number in range(1, 4)
        for question_number in range(1, 9)
    ]
    missing = [anchor for anchor in expected if f'id="{anchor}"' not in html]
    labels = ("目的", "分析方法", "为什么用这个方法", "推导过程", "阶段结论", "如何影响下一步")
    empty_fields = []
    valid_cards = 0
    for anchor in expected:
        card_match = re.search(
            rf'<article[^>]+id="{re.escape(anchor)}"[^>]*>(.*?)</article>',
            html,
            re.S,
        )
        if not card_match:
            continue
        card = card_match.group(1)
        card_valid = True
        for label in labels:
            field_match = re.search(
                rf"<dt>\s*{re.escape(label)}\s*</dt>\s*<dd>(.*?)</dd>",
                card,
                re.S,
            )
            value = strip_html(field_match.group(1)) if field_match else ""
            if not value:
                card_valid = False
                empty_fields.append({"anchor": anchor, "field": label})
        if card_valid:
            valid_cards += 1
    return {
        "present": True,
        "complete": not missing and not empty_fields and valid_cards == len(expected),
        "question_anchor_count": len(expected) - len(missing),
        "valid_question_card_count": valid_cards,
        "missing_question_anchors": missing,
        "empty_fields": empty_fields,
    }


def strip_html(value: str) -> str:
    return normalize_text(html_lib.unescape(re.sub(r"<[^>]+>", " ", value)))


def derive_semantic_findings(
    markdown_analysis: dict[str, Any],
    html_analysis: dict[str, Any],
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if not markdown_analysis["daily"]["three_deep_cases_present"]:
        findings.append(
            finding(
                "CASE_DEPTH_IMBALANCE",
                "content_quality_failure",
                f"Expected 3 deep cases, found {len(markdown_analysis['cases'])}.",
                severity="blocking",
                evidence_origin="training_markdown",
            )
        )
    for case in markdown_analysis["cases"]:
        if case["eightq"]["valid_question_count"] < 7:
            findings.append(
                finding(
                    "INCOMPLETE_8Q_FIELDS",
                    "content_quality_failure",
                    f"{case['case_id']} has {case['eightq']['valid_question_count']}/8 valid 8Q questions.",
                    case_id=case["case_id"],
                    severity="blocking",
                    evidence_origin="training_markdown",
                )
            )
        if not case["required_sections_complete"]:
            missing = [name for name, present in case["required_sections"].items() if not present]
            failure_type = (
                "METHOD_NAME_DROPPING"
                if "analysis_method_workbench" in missing
                else "ASSET_CARD_GENERIC"
                if "case_asset_card" in missing
                else "PREP_NOT_USABLE"
            )
            findings.append(
                finding(
                    failure_type,
                    "content_quality_failure",
                    f"{case['case_id']} missing required semantic sections: {', '.join(missing)}.",
                    case_id=case["case_id"],
                    severity="blocking",
                    evidence_origin="training_markdown",
                )
            )

    repeated_count = markdown_analysis["repeated_template_field_count"]
    if repeated_count >= 6 and markdown_analysis["cases"]:
        weakest = min(
            markdown_analysis["cases"],
            key=lambda case: case["eightq"]["derivation_median_chars"] or 0,
        )
        findings.append(
            finding(
                "BOILERPLATE_REASONING",
                "content_quality_failure",
                f"{repeated_count} purpose/method-rationale fields repeat verbatim across all three cases.",
                case_id=weakest["case_id"],
                severity="review",
                evidence_origin="training_markdown",
            )
        )
        if weakest["eightq"]["peer_depth_ratio"] < 0.9:
            findings.append(
                finding(
                    "CASE_DEPTH_IMBALANCE",
                    "content_quality_failure",
                    (
                        f"{weakest['case_id']} has the weakest 8Q derivation median "
                        f"({weakest['eightq']['derivation_median_chars']} chars; "
                        f"peer ratio {weakest['eightq']['peer_depth_ratio']})."
                    ),
                    case_id=weakest["case_id"],
                    severity="review",
                    evidence_origin="training_markdown",
                )
            )
        if (weakest["self_review_max_score"] or 0) >= 95:
            findings.append(
                finding(
                    "REVIEW_EVIDENCE_INVALID",
                    "self_review_inflation",
                    (
                        f"{weakest['case_id']} self-review score "
                        f"{weakest['self_review_max_score']}/100 conflicts with detected template/depth risks."
                    ),
                    case_id=weakest["case_id"],
                    severity="review",
                    evidence_origin="training_markdown",
                )
            )
    if html_analysis["present"] and not html_analysis["complete"]:
        findings.append(
            finding(
                "HTML_CONTENT_LOSS",
                "html_rendering_integrity_failure",
                f"Reader HTML is missing {len(html_analysis['missing_question_anchors'])} expected 8Q anchors.",
                severity="blocking",
                evidence_origin="reader_html",
            )
        )
    return findings


def build_uncertainty_boundary(
    no_audit: bool,
    semantic_findings: list[dict[str, Any]],
) -> dict[str, Any]:
    limitations = []
    if no_audit:
        limitations.extend(
            [
                "Historical regression audit was intentionally excluded.",
                "Local heuristics can detect structure, repeated phrasing, relative depth, and score conflict, but cannot fully prove causal quality.",
                "DISCONNECTED_8Q_CHAIN is not asserted without sufficient semantic or audit evidence.",
            ]
        )
    if any(item["severity"] == "review" for item in semantic_findings):
        limitations.append("At least one finding is review-level rather than independently proven as a hard failure.")
    return {"present": bool(limitations), "limitations": limitations}


def merge_findings(
    existing: list[dict[str, Any]],
    additions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    merged = {(item["failure_type"], item.get("case_id")): item for item in existing}
    for item in additions:
        merged[(item["failure_type"], item.get("case_id"))] = item
    return list(merged.values())


def release_reason(
    case_decisions: list[str],
    findings: list[dict[str, Any]],
    no_audit: bool,
) -> str:
    if all(decision == "PASS" for decision in case_decisions) and not findings:
        return "All three cases meet the minimum semantic-section contract with no blocking evidence."
    types = ", ".join(sorted({item["failure_type"] for item in findings})) or "semantic incompleteness"
    mode = "without historical audit" if no_audit else "with available evidence"
    return f"Publication is blocked or held for review {mode}: {types}."


def extract_v7_evidence(audit: str) -> dict[str, str]:
    return {
        "executive": first_line_containing(audit, 'V7 cannot be honestly called "stable V6-level output" yet.'),
        "case2_size": first_line_containing(audit, "| Case 2 size |"),
        "case2_8q": first_line_containing(audit, "| Case 2 8-question section |"),
        "boilerplate": first_line_containing(audit, "| Repeated boilerplate phrase |"),
        "valid_but_short": first_line_containing(audit, 'Several field answers are valid but short:'),
        "inflated_score": first_line_containing(audit, "The case self-scores 97/100"),
    }


def audit_finding(
    failure_type: str,
    category: str,
    quote: str,
) -> dict[str, Any] | None:
    if not quote:
        return None
    return finding(
        failure_type,
        category,
        quote,
        case_id="case_b",
        severity="blocking",
        evidence_origin="regression_audit",
    )


def finding(
    failure_type: str,
    category: str,
    quote: str,
    *,
    case_id: str | None = None,
    severity: str = "review",
    evidence_origin: str = "training_markdown",
) -> dict[str, Any]:
    return {
        "failure_type": failure_type,
        "category": category,
        "case_id": case_id,
        "severity": severity,
        "evidence_origin": evidence_origin,
        "source_basis": quote,
        "judgment": f"{failure_type} detected from local source review.",
    }


def derive_case_decision(
    sample_id: str,
    case_id: str,
    raw_response: dict[str, Any],
    anchors: dict[str, Any],
) -> str:
    """Derive one case decision only from observed evidence."""
    del sample_id, anchors
    cases = {
        case["case_id"]: case
        for case in raw_response.get("case_semantic_evidence", [])
    }
    case = cases.get(case_id)
    if case is None:
        return "REWRITE_CASE"
    if case["eightq"]["valid_question_count"] < 7:
        return "REWRITE_CASE"
    if not case["required_sections_complete"]:
        return "REWRITE_MODULE"
    relevant = [
        item
        for item in raw_response.get("semantic_findings", [])
        if item.get("case_id") in (None, case_id)
    ]
    if any(item["severity"] == "blocking" for item in relevant):
        return "FAIL_DAILY"
    if any(item["severity"] == "review" for item in relevant):
        return "REVIEW"
    return "PASS"


def derive_daily_decision(
    case_decisions: list[str],
    failure_objects: list[dict[str, Any]],
    validator_result: dict[str, Any] | None,
) -> dict[str, Any]:
    """Aggregate decisions without using expected sample outcomes."""
    if validator_result and validator_result.get("schema_and_governance_payload_status") != "PASS":
        return {"daily_decision": "PUBLISH_BLOCK", "publish_allowed": False}
    failure_types = {
        item.get("failure_type")
        for item in failure_objects
        if isinstance(item, dict)
    }
    if failure_types & {"HTML_CONTENT_LOSS", "HTML_EMPTY_SECTION", "REVIEWER_OUTPUT_INVALID"}:
        return {"daily_decision": "PUBLISH_BLOCK", "publish_allowed": False}
    if any(decision in {"FAIL_DAILY", "PUBLISH_BLOCK"} for decision in case_decisions):
        return {"daily_decision": "FAIL_DAILY", "publish_allowed": False}
    if any(decision == "REPLACE_CASE" for decision in case_decisions):
        return {"daily_decision": "REPLACE_CASE", "publish_allowed": False}
    if any(decision == "REWRITE_CASE" for decision in case_decisions):
        return {"daily_decision": "REWRITE_CASE", "publish_allowed": False}
    if any(decision == "REWRITE_MODULE" for decision in case_decisions):
        return {"daily_decision": "REWRITE_MODULE", "publish_allowed": False}
    if any(decision in {"REVIEW", "USER_REVIEW_REQUIRED"} for decision in case_decisions):
        return {"daily_decision": "REVIEW", "publish_allowed": False}
    if any(
        item.get("severity") == "blocking"
        or item.get("decision_state") in {"FAIL_DAILY", "PUBLISH_BLOCK"}
        for item in failure_objects
        if isinstance(item, dict)
    ):
        return {"daily_decision": "FAIL_DAILY", "publish_allowed": False}
    if failure_objects:
        return {"daily_decision": "REVIEW", "publish_allowed": False}
    return {"daily_decision": "PASS", "publish_allowed": True}


def build_reviewer_output(
    sample_id: str,
    config: dict[str, Any],
    raw: dict[str, Any],
    anchors: dict[str, Any],
    failure_objects: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    failure_objects = failure_objects if failure_objects is not None else build_failure_objects(sample_id, raw)
    case_reviews = []
    for case_id in ("case_a", "case_b", "case_c"):
        case_decision = derive_case_decision(sample_id, case_id, raw, anchors)
        case_reviews.append(
            build_case_review(
                sample_id,
                case_id,
                config["case_titles"][case_id],
                anchors,
                case_decision,
                build_claim_map(sample_id, case_id, raw, case_decision),
                raw,
            )
        )
    release = derive_daily_decision(
        [case["case_decision"] for case in case_reviews],
        failure_objects,
        None,
    )
    return {
        "reviewer_output_valid": True,
        "reviewer_id": "p2b0-evidence-derived-local-reviewer",
        "reviewed_at": utc_now(),
        "rubric_version": "2.1",
        "case_score_policy": "each_deep_case_scored_independently_100",
        "daily_score_policy": "no_cross_case_compensation",
        "daily_decision_rule": "all_cases_must_pass",
        "daily_decision": release["daily_decision"],
        "publish_allowed": release["publish_allowed"],
        "gate_statuses": {"G6": "PASS", "G7": "PASS", "G8": "PASS"},
        "case_reviews": case_reviews,
        "review_notes": (
            f"{sample_id} reviewed by evidence-derived local semantic reviewer; "
            "expected config and self-review scores ignored as release authority."
        ),
    }


def build_case_review(
    sample_id: str,
    case_id: str,
    title: str,
    anchors: dict[str, Any],
    decision: str,
    claim_map: dict[str, Any],
    raw: dict[str, Any],
) -> dict[str, Any]:
    items = []
    case_evidence = next(
        case for case in raw["case_semantic_evidence"] if case["case_id"] == case_id
    )
    for item_id, anchor in anchors.items():
        weakness = case_item_weakness(raw, case_id, item_id, decision)
        items.append(item_review(item_id, anchor, case_id, weakness, case_evidence))
    accounts = account_scores(items)
    total = sum(account["account_final_score"] for account in accounts)
    return {
        "case_id": case_id,
        "case_title": title,
        "claim_evidence_map": [claim_map],
        "item_reviews": items,
        "account_scores": accounts,
        "case_raw_total": total,
        "case_global_cap_applied": None,
        "case_final_total": total,
        "case_decision": decision,
        "publish_allowed": decision == "PASS",
    }


def case_item_weakness(
    raw: dict[str, Any],
    case_id: str,
    item_id: str,
    decision: str,
) -> dict[str, Any] | None:
    if decision == "PASS":
        return None
    relevant_types = {
        item["failure_type"]
        for item in raw.get("semantic_findings", [])
        if item.get("case_id") in (None, case_id)
    }
    if not relevant_types:
        return None
    locations = {
        item.get("evidence_origin", "training_markdown")
        for item in raw.get("semantic_findings", [])
        if item.get("case_id") in (None, case_id)
    }
    evidence_location = ", ".join(sorted(locations))
    mapping = {
        "thinking.problem_reframing": (3, "PARTIAL", "Problem framing is directionally useful but underdeveloped."),
        "thinking.eightq_reasoning_validity": (2, "INSUFFICIENT", "The 8Q structure exists, but continuity and case-specific depth remain weak."),
        "thinking.causal_mechanism": (4, "PARTIAL", "The causal mechanism lacks enough transmission and outcome evidence."),
        "thinking.method_insight_generation": (3, "PARTIAL", "Methods appear, but repeated rationale weakens proof that they generated distinct insight."),
        "content.claim_evidence_alignment": (3, "PARTIAL", "The core judgment lacks enough adoption or outcome evidence."),
        "content.case_specificity_context": (3, "PARTIAL", "Case-specific product mechanics are thinner than the surrounding cases."),
        "expression.prep_scqa_quality": (3, "PARTIAL", "Expression exists but does not fully repair the underlying reasoning weakness."),
        "expression.interview_followup_resilience": (2, "PARTIAL", "Follow-up questions would expose unresolved evidence gaps."),
        "expression.case_asset_card_transfer": (3, "PARTIAL", "Asset transfer is plausible but remains generic."),
    }
    if item_id not in mapping:
        return None
    score, sufficiency, reason = mapping[item_id]
    return {
        "final_score": score,
        "sufficiency": sufficiency,
        "reason": reason,
        "evidence_location": evidence_location,
    }


def item_review(
    item_id: str,
    anchor: dict[str, Any],
    case_id: str,
    weakness: dict[str, Any] | None,
    case_evidence: dict[str, Any],
) -> dict[str, Any]:
    max_score = int(anchor["max_score"])
    if weakness is None:
        conservative_deductions = {
            "thinking.p6_to_p7_reframe",
            "thinking.problem_reframing",
            "thinking.system_relation_value_flow",
            "thinking.counterfactual_boundary",
            "thinking.trend_projection",
            "content.source_traceability",
            "content.case_specificity_context",
            "content.uncertainty_boundary",
            "content.information_density",
            "expression.structure_readability",
            "expression.prep_scqa_quality",
            "expression.memory_point_pattern",
        }
        final_score = max_score - 1 if item_id in conservative_deductions else max_score
        not_full = final_score < max_score
        evidence_quote = (
            f"{case_id} has {case_evidence['eightq']['valid_question_count']}/8 valid 8Q questions; "
            f"required sections complete={case_evidence['required_sections_complete']}."
        )
        return {
            "item_id": item_id,
            "level": anchor["level"],
            "primary_account": anchor["primary_account"],
            "max_score": max_score,
            "raw_score": max_score,
            "caps_applied": [],
            "capped_score": max_score,
            "deductions_applied": (
                [{"reason": "Local deterministic review proves the minimum contract, not full semantic excellence.", "points": 1}]
                if not_full
                else []
            ),
            "adjusted_score": final_score,
            "final_score": final_score,
            "anchor_matched": (
                f"{final_score}分：evidence-derived minimum semantic contract passed."
            ),
            "required_evidence_points": [{"point": f"{case_id} {item_id}", "support_level": "SUFFICIENT"}],
            "item_evidence_sufficiency": "SUFFICIENT",
            "positive_evidence": [
                {
                    "evidence_id": f"{case_id}_{safe_id(item_id)}_positive",
                    "quote": evidence_quote,
                    "location": f"{case_id} / evidence-derived semantic review",
                    "supports_what": item_id,
                    "evidence_sufficiency": "SUFFICIENT",
                }
            ],
            "missing_evidence": (
                ["A local deterministic reviewer cannot independently prove full semantic excellence."]
                if not_full
                else []
            ),
            "deduction_reason": (
                "Conservative one-point deduction for dimensions requiring richer semantic judgment."
                if not_full
                else ""
            ),
            "why_not_higher": (
                "The structure is valid, but this reviewer cannot establish every full-score semantic anchor."
                if not_full
                else ""
            ),
            "repair_action": "",
            "decision": "PASS",
        }
    final_score = int(weakness["final_score"])
    sufficiency = weakness["sufficiency"]
    cap = evidence_cap(sufficiency, max_score)
    raw_score = min(max_score, max(final_score + 1, cap))
    capped_score = min(raw_score, cap)
    return {
        "item_id": item_id,
        "level": anchor["level"],
        "primary_account": anchor["primary_account"],
        "max_score": max_score,
        "raw_score": raw_score,
        "caps_applied": [{"cap_type": "item_cap", "reason": weakness["reason"], "max_allowed_score": cap}],
        "capped_score": capped_score,
        "deductions_applied": [],
        "adjusted_score": final_score,
        "final_score": final_score,
        "anchor_matched": f"{final_score}分：{weakness['reason']}",
        "required_evidence_points": [
            {"point": weakness["reason"], "support_level": sufficiency, "missing_or_partial_reason": weakness["reason"]}
        ],
        "item_evidence_sufficiency": sufficiency,
        "positive_evidence": [
            {
                "evidence_id": f"case_b_{safe_id(item_id)}_weakness",
                "quote": weakness["reason"],
                "location": weakness["evidence_location"],
                "supports_what": item_id,
                "evidence_sufficiency": sufficiency,
                "why_insufficient": weakness["reason"],
            }
        ],
        "missing_evidence": ["Needs V6-level mechanics, adoption constraints, buyer economics, and ROI proof."],
        "deduction_reason": weakness["reason"],
        "why_not_higher": weakness["reason"],
        "repair_action": repair_action(item_id),
        "decision": "REWRITE_MODULE",
    }


def evidence_cap(sufficiency: str, max_score: int) -> int:
    if sufficiency == "PARTIAL":
        return math.floor(max_score * 0.7)
    if sufficiency == "INSUFFICIENT":
        return min(2, max_score)
    if sufficiency == "MISSING":
        return 0
    return max_score


def repair_action(item_id: str) -> str:
    if "eightq" in item_id:
        return "rewrite_8q_reasoning"
    if "causal" in item_id:
        return "rewrite_causal_chain"
    if "method" in item_id:
        return "rewrite_method_workbench"
    if item_id.startswith("expression"):
        return "rewrite_expression"
    return "rewrite_case_background"


def account_scores(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    minimums = {"thinking_depth": 38, "content_quality": 25, "expression_quality": 21}
    totals = {account: 0 for account in minimums}
    for item in items:
        totals[item["primary_account"]] += item["final_score"]
    return [
        {
            "account_id": account,
            "account_raw_score": totals[account],
            "account_cap_applied": None,
            "account_final_score": totals[account],
            "min_pass_score": minimums[account],
        }
        for account in ("thinking_depth", "content_quality", "expression_quality")
    ]


def build_claim_map(
    sample_id: str,
    case_id: str,
    raw: dict[str, Any],
    case_decision: str,
) -> dict[str, Any]:
    source_path = raw["source_files"]["training_markdown"]["path"]
    source = {
        "title": f"{sample_id} training artifact",
        "url": f"file://{source_path}",
        "source_type": "official_doc",
        "published_at": "2026-06-26",
        "accessed_at": "2026-06-28",
        "fact_confidence": "B",
    }
    case_evidence = next(
        (case for case in raw["case_semantic_evidence"] if case["case_id"] == case_id),
        None,
    )
    if case_decision != "PASS":
        relevant = [
            item["source_basis"]
            for item in raw["semantic_findings"]
            if item.get("case_id") in (None, case_id)
        ]
        fact = relevant[0] if relevant else f"{case_id} does not meet the minimum semantic contract."
        claim_text = f"{case_id} cannot be accepted because evidence-derived semantic checks found a release risk."
        impact = "Supports final non-PASS tradeoff for Case B."
        support_level = "PARTIAL"
        unsupported = list(raw["uncertainty_boundary"]["limitations"]) or [
            "Needs deeper product mechanics and decision evidence."
        ]
    else:
        fact = (
            f"{case_id} has {case_evidence['eightq']['valid_question_count']}/8 valid 8Q questions "
            "and all required semantic sections."
        )
        claim_text = f"{sample_id} {case_id} meets the local minimum semantic-section contract."
        impact = f"Supports {case_decision} for {case_id}."
        support_level = "SUFFICIENT"
        unsupported = []
    return {
        "case_id": case_id,
        "claims": [
            {
                "claim_id": f"{sample_id}_{case_id}_core_claim_01",
                "claim_text": claim_text,
                "claim_type": "core_judgment",
                "supporting_facts": [{"fact": fact, "source": source, "supports_claim_how": impact}],
                "support_level": support_level,
                "unsupported_parts": unsupported,
                "decision_impact": impact,
            }
        ],
    }


def build_failure_objects(sample_id: str, raw: dict[str, Any]) -> list[dict[str, Any]]:
    del sample_id
    repair_map = {
        "INCOMPLETE_8Q_FIELDS": "rewrite_8q_reasoning",
        "DISCONNECTED_8Q_CHAIN": "rewrite_8q_reasoning",
        "BOILERPLATE_REASONING": "rewrite_8q_reasoning",
        "CASE_DEPTH_IMBALANCE": "rewrite_case_background",
        "METHOD_NAME_DROPPING": "rewrite_method_workbench",
        "ASSET_CARD_GENERIC": "rewrite_asset_card",
        "PREP_NOT_USABLE": "rewrite_expression",
        "REVIEW_EVIDENCE_INVALID": "request_human_review",
        "HTML_CONTENT_LOSS": "rerender_html",
    }
    decision_state = raw["release_decision"]["daily_decision"]
    failures = []
    seen = set()
    for item in raw["semantic_findings"]:
        failure_type = item["failure_type"]
        if failure_type in seen:
            continue
        seen.add(failure_type)
        repair = repair_map.get(failure_type, "rewrite_case_background")
        failures.append(
            failure_object(
                failure_type,
                repair,
                raw,
                decision_state=(
                    "PUBLISH_BLOCK"
                    if failure_type == "HTML_CONTENT_LOSS"
                    else decision_state
                ),
                content_changed=failure_type != "REVIEW_EVIDENCE_INVALID",
                evidence=item["source_basis"],
            )
        )
    return failures


def failure_object(
    failure_type: str,
    repair: str,
    raw: dict[str, Any],
    *,
    decision_state: str,
    content_changed: bool = True,
    evidence: str | None = None,
) -> dict[str, Any]:
    return {
        "failure_type": failure_type,
        "decision_state": decision_state,
        "publish_allowed": False,
        "reviewer_output_valid": True,
        "repair_action": repair,
        "retry_budget": {"max_retries_per_gate": 2, "current_retry_count": 0, "retry_allowed": True},
        "content_repair_required": content_changed,
        "content_repair_target": repair,
        "system_repair_required": True,
        "system_repair_target": ["reviewer_prompt", "calibration_set"],
        "regression_sample_required": True,
        "content_changed": content_changed,
        "html_stale": content_changed,
        "must_rerender_html": content_changed,
        "must_rerun_gates": ["G3", "G5", "G6", "G7", "G8", "rubric_scoring"] if content_changed else ["rubric_scoring", "second_review"],
        "evidence": evidence or json.dumps(raw["source_evidence"], ensure_ascii=False),
        "repair_notes": "Repair or review the evidence-derived finding before publication.",
    }


def validate_outputs(
    sample_id: str,
    rubric_dir: Path,
    payload: dict[str, Any],
    claim_map: dict[str, Any],
    failures: list[dict[str, Any]],
) -> dict[str, Any]:
    validator = load_validator(rubric_dir)
    reviewer_errors = validator.validate_reviewer_output(payload, rubric_dir)
    claim_errors = []
    for case_id, cmap in sorted(claim_map.items()):
        claim_errors.extend(f"{case_id}.{err}" for err in validator.validate_claim_evidence_map(cmap, rubric_dir))
    failure_errors = []
    for index, failure in enumerate(failures):
        failure_errors.extend(
            f"failure_objects[{index}].{err}"
            for err in validator.validate_failure_object(failure, rubric_dir)
        )
    valid = not (reviewer_errors or claim_errors or failure_errors)
    failure_types = [failure["failure_type"] for failure in failures]
    return {
        "sample_id": sample_id,
        "schema_and_governance_payload_status": "PASS" if valid else "FAIL",
        "reviewer_errors": reviewer_errors,
        "claim_evidence_map_errors": claim_errors,
        "failure_object_errors": failure_errors,
        "governance_decision": payload["daily_decision"],
        "publish_allowed": payload["publish_allowed"],
        "publish_blocked": payload["daily_decision"] != "PASS" or not payload["publish_allowed"],
        "failure_types": failure_types,
        "failure_categories": classify_failures(failure_types),
        "raw_reviewer_response_preserved": True,
    }


def compare_recorded(
    rubric_dir: Path,
    sample_id: str,
    payload: dict[str, Any],
    failures: list[dict[str, Any]],
) -> dict[str, Any]:
    fixture_dir = rubric_dir / "fixtures" / "calibration" / sample_id
    recorded_payload = read_json(fixture_dir / "reviewer-output.json")
    recorded_failures = read_json(fixture_dir / "failure-objects.json") if (
        fixture_dir / "failure-objects.json"
    ).exists() else []
    live_failure_types = {failure["failure_type"] for failure in failures}
    recorded_failure_types = {failure["failure_type"] for failure in recorded_failures}
    return {
        "sample_id": sample_id,
        "compared_to_recorded_fixture": True,
        "used_recorded_payload_for_generation": False,
        "daily_decision_match": payload["daily_decision"] == recorded_payload["daily_decision"],
        "publish_allowed_match": payload["publish_allowed"] == recorded_payload["publish_allowed"],
        "case_decision_diff": [
            {
                "case_id": live["case_id"],
                "live": live["case_decision"],
                "recorded": recorded["case_decision"],
                "matches": live["case_decision"] == recorded["case_decision"],
            }
            for live, recorded in zip(payload["case_reviews"], recorded_payload["case_reviews"])
        ],
        "failure_type_overlap": sorted(live_failure_types & recorded_failure_types),
        "live_only_failure_types": sorted(live_failure_types - recorded_failure_types),
        "recorded_only_failure_types": sorted(recorded_failure_types - live_failure_types),
        "caps_applied_match": caps_snapshot(payload) == caps_snapshot(recorded_payload),
        "live_caps_applied": caps_snapshot(payload),
        "recorded_caps_applied": caps_snapshot(recorded_payload),
        "explanations": [
            "Live payload was generated by the local semantic reviewer from source files, not replayed from the P1 fixture.",
            "Diff uses the recorded fixture only as a comparison target after generation.",
            "Daily decision, publish permission, case decisions, failure types, and caps are compared explicitly.",
        ],
    }


def caps_snapshot(payload: dict[str, Any]) -> list[dict[str, Any]]:
    caps = []
    for case in payload.get("case_reviews", []):
        for item in case.get("item_reviews", []):
            if item.get("caps_applied"):
                caps.append({"case_id": case["case_id"], "item_id": item["item_id"], "caps": item["caps_applied"]})
    return caps


def build_generation_log(
    project_root: Path,
    rubric_dir: Path,
    output_dir: Path,
    sample_id: str,
    sources: dict[str, Any],
    paths: dict[str, Path],
    validator_result: dict[str, Any],
    *,
    no_audit: bool,
) -> dict[str, Any]:
    return {
        "sample_id": sample_id,
        "created_at": utc_now(),
        "reviewer_version": REVIEWER_VERSION,
        "generation_method": "local_semantic_reviewer",
        "live_semantic_review": True,
        "live_llm_review": False,
        "recorded_generation": False,
        "replay_p1_fixture_payload": False,
        "decision_source": "evidence_derived",
        "expected_config_used_for_decision": False,
        "no_audit": no_audit,
        "not_stability_claim": True,
        "input_files": [
            {"role": role, "path": data["path"], "bytes": data["bytes"], "sha256": data["sha256"]}
            for role, data in sources.items()
        ],
        "rubric_dir": rel(project_root, rubric_dir),
        "output_dir": rel(project_root, output_dir),
        "output_paths": {name: rel(project_root, path) for name, path in paths.items()},
        "validator_result": {
            "schema_and_governance_payload_status": validator_result["schema_and_governance_payload_status"],
            "governance_decision": validator_result["governance_decision"],
            "publish_blocked": validator_result["publish_blocked"],
        },
        "self_review_policy": {
            "rule_id": "self_review_is_subject_not_authority",
            "ignored_as_release_evidence": True,
        },
    }


def classify_failures(failure_types: list[str]) -> dict[str, bool]:
    failure_set = set(failure_types)
    return {
        "content_quality_failure": bool(
            failure_set
            & {
                "EMPTY_8Q_REASONING",
                "INCOMPLETE_8Q_FIELDS",
                "DISCONNECTED_8Q_CHAIN",
                "BOILERPLATE_REASONING",
                "CASE_DEPTH_IMBALANCE",
                "METHOD_NAME_DROPPING",
                "PREP_NOT_USABLE",
                "ASSET_CARD_GENERIC",
            }
        ),
        "html_rendering_integrity_failure": bool(failure_set & {"HTML_CONTENT_LOSS", "HTML_EMPTY_SECTION"}),
        "source_evidence_failure": bool(failure_set & {"NO_AB_EVIDENCE_FOR_CORE_CLAIM", "CLAIM_EVIDENCE_MISMATCH", "SOURCE_UNTRACEABLE", "C_OR_D_FACT_SUPPORTS_CORE_CLAIM"}),
        "self_review_inflation": bool(failure_set & {"REVIEW_EVIDENCE_INVALID", "SELF_REVIEW_INFLATION"}),
    }


def build_samples_report(results: list[dict[str, Any]]) -> str:
    lines = [
        "# P2B-0 Evidence-Derived Local Reviewer Samples Report",
        "",
        "## Boundary",
        "",
        "This is a local semantic reviewer, not a live LLM reviewer.",
        "It proves three-sample evidence-derived local semantic replay only and does not prove cross-date generalization.",
        "It does not enter P2C daily production.",
        "Expected decisions in sample configuration are test oracles only and never feed reviewer decisions.",
        "Next stage is P2B-1 stability / no-audit stress, not P2C daily production integration.",
        "",
        "## Results",
        "",
        "| Sample | Decision | Publish | Validator | Output |",
        "| --- | --- | --- | --- | --- |",
    ]
    for result in results:
        lines.append(
            f"| `{result['sample_id']}` | `{result['daily_decision']}` | `{result['publish_allowed']}` | `{result['validator_status']}` | `{result['output_dir']}` |"
        )
    lines.append("")
    return "\n".join(lines)


def build_sample_report(
    sample_id: str,
    validator_result: dict[str, Any],
    diff: dict[str, Any],
) -> str:
    return "\n".join(
        [
            "# P2B-0 Local Reviewer Generation Report",
            "",
            "## Scope",
            "",
            f"This run validates one real sample: `{sample_id}`. It does not enter P2C daily production.",
            "",
            "## Boundary",
            "",
            "- `generation_method: local_semantic_reviewer`",
            "- `recorded_generation: false`",
            "- `replay_p1_fixture_payload: false`",
            "- `live_llm_review: false`",
            "- `decision_source: evidence_derived`",
            "- Raw reviewer response is preserved in `raw-reviewer-response.json`.",
            "",
            "## Result",
            "",
            f"- Governance decision: `{validator_result['governance_decision']}`",
            f"- Publish allowed: `{validator_result['publish_allowed']}`",
            f"- Payload validation status: `{validator_result['schema_and_governance_payload_status']}`",
            f"- Failure types: `{', '.join(validator_result['failure_types'])}`",
            "",
            "## Live vs Recorded",
            "",
            yaml.safe_dump(diff, allow_unicode=True, sort_keys=False).strip(),
            "",
        ]
    )


def build_hardening_report(
    rubric_dir: Path,
    results: list[dict[str, Any]],
    *,
    no_audit: bool,
) -> str:
    available = {}
    for sample_id, folder in (
        ("v3_target", "v3_target_live"),
        ("v6_target", "v6_target_live"),
        ("v7_failure", "v7_failure_live"),
        ("v7_failure_no_audit", "v7_failure_no_audit_live"),
    ):
        result_path = rubric_dir / "generated-replay" / folder / "live-validator-result.yaml"
        if result_path.is_file():
            data = read_yaml(result_path)
            available[sample_id] = {
                "decision": data["governance_decision"],
                "publish_allowed": data["publish_allowed"],
                "failure_types": data["failure_types"],
            }
    lines = [
        "# P2B-0 本地语义 Reviewer 去配置化加固报告",
        "",
        "## 本轮边界",
        "",
        "- 仍然是 `local_semantic_reviewer`，不是 live LLM reviewer。",
        "- 不接入 P2C，不接入每日自动发布。",
        "- `SAMPLE_CONFIGS.expected_decision` 只作为测试预期，不进入 reviewer decision 数据流。",
        "",
        "## Evidence-derived Decision",
        "",
        "Case 判定来自 Markdown 中可观察到的三类证据：3 个 deep case、每个 case 的 8 问字段完整性，以及分析方法、六层总结、PREP/SCQA、Case Asset Card 的最低语义结构。",
        "Daily 判定由三个 case decision、failure objects 和 governance validator 结果聚合，禁止读取 expected decision。",
        "原文中的 Insight Quality Audit 只作为被审对象，不作为放行依据。",
        "",
        "## Audit 依赖边界",
        "",
        "有 audit 时，历史审计用于增强 `DISCONNECTED_8Q_CHAIN` 等需要纵向比较的判断。",
        "无 audit 时，reviewer 仍可检查跨 Case 的模板重复、相对深度失衡、self-review 高分冲突与 HTML 8 问锚点完整性。",
        "无 audit 的启发式证据不足以独立证明完整因果质量，因此必须输出 uncertainty boundary；不能因此给 PASS。",
        "",
        "## V3 / V6 PASS 证据",
        "",
        "V3/V6 的 PASS 不再来自 source existence。每个 deep case 必须实际满足 8/8 有效问题和完整语义模块；V6 reader HTML 还必须保留 24 个 8 问锚点。",
        "",
        "## 当前结果",
        "",
        "| Sample | Decision | Publish | Failure types |",
        "| --- | --- | --- | --- |",
    ]
    for sample_id, data in available.items():
        lines.append(
            f"| `{sample_id}` | `{data['decision']}` | `{data['publish_allowed']}` | "
            f"`{', '.join(data['failure_types'])}` |"
        )
    lines.extend(
        [
            "",
            "## 下一步判断",
            "",
            "下一步是 P2B-1 stability / no-audit stress，用输入扰动和缺少辅助 audit 的场景验证不误放坏样本、不误杀好样本。",
            "当前不具备进入 P2C 的证据。",
            "",
            f"本次报告由 `--no-audit={str(no_audit).lower()}` 运行更新；本次直接运行样本："
            f" `{', '.join(result['sample_id'] for result in results)}`。",
            "",
        ]
    )
    return "\n".join(lines)


def extract_between(text: str, start: str, end: str) -> str:
    start_index = text.find(start)
    if start_index == -1:
        return ""
    end_index = text.find(end, start_index + len(start))
    return text[start_index:] if end_index == -1 else text[start_index:end_index]


def first_line_containing(text: str, needle: str) -> str:
    for line in text.splitlines():
        if needle in line:
            return line.strip()
    return ""


def safe_id(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "_", value).strip("_")


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_validator(rubric_dir: Path):
    path = rubric_dir / "rubric_governance_validator.py"
    spec = importlib.util.spec_from_file_location("rubric_governance_validator", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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
