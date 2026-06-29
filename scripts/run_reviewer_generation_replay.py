#!/usr/bin/env python3
"""Run P2A reviewer payload generation replay for V3/V6/V7."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
from typing import Any

import yaml


SAMPLE_IDS = ("v3_target", "v6_target", "v7_failure")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    rubric_dir = project_root / "docs" / "quality" / "rubric-v2.1"
    generated_dir = rubric_dir / "generated-replay"
    generator = load_generator(project_root)

    results: list[dict[str, Any]] = []
    for sample_id in SAMPLE_IDS:
        output_dir = generated_dir / sample_id
        result = generator.generate_payload(project_root, rubric_dir, sample_id, output_dir)
        results.append(result)

    report = build_report(project_root, rubric_dir, results)
    report_path = rubric_dir / "reviewer-generation-report.md"
    report_path.write_text(report, encoding="utf-8")

    summary = {
        "completed": True,
        "report_path": rel(project_root, report_path),
        "samples": results,
    }
    print(yaml.safe_dump(summary, allow_unicode=True, sort_keys=False), end="")
    return 0


def load_generator(project_root: Path):
    path = project_root / "scripts" / "generate_reviewer_payload.py"
    spec = importlib.util.spec_from_file_location("generate_reviewer_payload", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def build_report(project_root: Path, rubric_dir: Path, results: list[dict[str, Any]]) -> str:
    lines = [
        "# Reviewer Generation Report",
        "",
        "## Scope",
        "",
        "P2A validates the reviewer-payload generation boundary for real historical samples. It does not connect the daily publishing pipeline and does not claim live semantic reviewer stability.",
        "",
        "## Generation Mode",
        "",
        "- `recorded_generation: true`",
        "- `not_live_llm_review: true`",
        "- Method: read real source files, record file hashes, replay P1 calibration payloads, then run the existing Rubric v2.1 governance validator.",
        "- Self-review / Insight Quality Audit text is treated as reviewed content, not as release authority.",
        "",
        "## Sample Results",
        "",
        "| Sample | Decision | Publish | Validator | Output |",
        "| --- | --- | --- | --- | --- |",
    ]
    for result in results:
        output_dir = result["output_dir"]
        lines.append(
            f"| `{result['sample_id']}` | `{result['daily_decision']}` | `{result['publish_allowed']}` | `{result['validator_status']}` | `{output_dir}` |"
        )

    lines.extend(
        [
            "",
            "## Real Samples",
            "",
            "- `v3_target`: reads `outputs/daily-training/2026-06-25/training-v3.md` and should PASS.",
            "- `v6_target`: reads `training-v6-raw.md`, `training-v6-reader.html`, source notes and quality report; should PASS.",
            "- `v7_failure`: reads `training-v7-raw.md`, `training-v7-reader.html`, source notes and regression audit; must not PASS.",
            "",
            "## Generated Artifacts",
            "",
            "Each sample directory under `docs/quality/rubric-v2.1/generated-replay/` contains:",
            "",
            "- `reviewer-output.json`",
            "- `claim-evidence-map.json`",
            "- `failure-objects.json`",
            "- `generation-log.yaml`",
            "- `validator-result.yaml`",
            "",
            "## Semantic Boundary",
            "",
            "The current generator is a recorded/mock generator. It proves file ingestion, trace logging, payload materialization, validator execution, and golden comparison wiring. It does not prove that a live LLM can independently read Markdown/HTML and generate the same payload.",
            "",
            "## Human Confirmation Still Needed",
            "",
            "- Whether the recorded P1 fixture judgments remain semantically acceptable after future Rubric updates.",
            "- Whether live Markdown-to-payload generation can match the recorded judgments across more unseen days.",
            "- Whether P2B should broaden the replay set before P2C daily pipeline integration.",
            "",
            "## Next Gate",
            "",
            "Proceed to P2B only after live or semi-live reviewer generation can reproduce V3/V6 PASS and V7 non-PASS without relying on recorded fixture payloads.",
            "",
        ]
    )
    return "\n".join(lines)


def rel(root: Path, path: Path) -> str:
    try:
        return str(Path(path).resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
