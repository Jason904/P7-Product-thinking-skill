#!/usr/bin/env python3
"""Compatibility wrapper for the generic P2B-0 evidence-derived reviewer."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

import yaml


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    generic = load_generic(project_root)
    rubric_dir = project_root / "docs" / "quality" / "rubric-v2.1"
    result = generic.run_sample(project_root, rubric_dir, "v7_failure")
    print(yaml.safe_dump({"completed": True, "samples": [result]}, allow_unicode=True, sort_keys=False), end="")
    return 0


def load_generic(project_root: Path):
    path = project_root / "scripts" / "run_live_reviewer_generation.py"
    spec = importlib.util.spec_from_file_location("run_live_reviewer_generation", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    raise SystemExit(main())
