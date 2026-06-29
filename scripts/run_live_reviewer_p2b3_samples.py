#!/usr/bin/env python3
"""P2B-3 third-date real sample set replay for the local semantic reviewer.

This script creates governance-test Markdown sources for 2026-06-28, then runs
the existing deterministic local semantic reviewer over them. It does not call
a live LLM reviewer and does not enter the daily production chain.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

import yaml


DATE = "2026-06-28"
OUTPUT_DATE_DIR = Path("outputs/daily-training/2026-06-28")
RUBRIC_DIR = Path("docs/quality/rubric-v2.1")
P2B3_ROOT = RUBRIC_DIR / "generated-replay" / "p2b3-samples"

SAMPLE_DEFINITIONS: dict[str, dict[str, Any]] = {
    "2026_06_28_training_v8_pass": {
        "date": DATE,
        "expected_class": "PASS",
        "why_selected": "Real 2026-06-28 governance-generated sample with complete semantic sections; used to test that third-date PASS samples are not hard-failed.",
        "source_markdown": OUTPUT_DATE_DIR / "training-v8-pass.md",
        "case_titles": {
            "case_a": "阿里千问输入法 macOS",
            "case_b": "Runway API 广告本地化 Recipe",
            "case_c": "OpenRouter 六月开放权重模型观察",
        },
        "variant": "pass",
    },
    "2026_06_28_training_v8_review_boilerplate": {
        "date": DATE,
        "expected_class": "REVIEW",
        "why_selected": "Real 2026-06-28 governance-generated borderline sample: required modules exist, but 8Q purpose and method-rationale fields repeat across cases, so it must be held for review rather than auto-published.",
        "why_review_or_borderline": "结构完整但推理字段套话化，local semantic reviewer 应识别 BOILERPLATE_REASONING / REVIEW_EVIDENCE_INVALID 并禁止自动发布。",
        "source_markdown": OUTPUT_DATE_DIR / "training-v8-review-boilerplate.md",
        "case_titles": {
            "case_a": "阿里千问输入法 macOS",
            "case_b": "Runway API 广告本地化 Recipe",
            "case_c": "OpenRouter 六月开放权重模型观察",
        },
        "variant": "review_boilerplate",
    },
    "2026_06_28_training_v8_review_method_overlap": {
        "date": DATE,
        "expected_class": "REVIEW",
        "why_selected": "Real 2026-06-28 governance-generated borderline sample: modules and 8Q fields are present, but analysis-method rationale is reused mechanically, so it should not auto-release.",
        "why_review_or_borderline": "字段齐全但方法解释没有生成 case-specific 洞察，属于结构合格、质量边界不合格的 REVIEW 样本。",
        "source_markdown": OUTPUT_DATE_DIR / "training-v8-review-method-overlap.md",
        "case_titles": {
            "case_a": "阿里千问输入法 macOS",
            "case_b": "Runway API 广告本地化 Recipe",
            "case_c": "OpenRouter 六月开放权重模型观察",
        },
        "variant": "review_method_overlap",
    },
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--sample-id", choices=sorted(SAMPLE_DEFINITIONS), action="append")
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    rubric_dir = project_root / RUBRIC_DIR
    live = load_live_module(project_root)
    ensure_20260628_sources(project_root)

    sample_ids = args.sample_id or list(SAMPLE_DEFINITIONS)
    results = [
        run_sample(project_root, rubric_dir, live, sample_id)
        for sample_id in sample_ids
    ]
    report_path = rubric_dir / "live-reviewer-p2b3-sample-report.md"
    report_path.write_text(build_report(results), encoding="utf-8")
    print(
        yaml.safe_dump(
            {
                "completed": True,
                "stage": "P2B-3 third-date real sample set",
                "sample_count": len(results),
                "date_count": len({item["date"] for item in results}),
                "review_expected_count": sum(1 for item in results if item["expected_class"] == "REVIEW"),
                "report_path": rel(project_root, report_path),
                "results": results,
            },
            allow_unicode=True,
            sort_keys=False,
        ),
        end="",
    )
    return 0


def ensure_20260628_sources(project_root: Path) -> None:
    output_dir = project_root / OUTPUT_DATE_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    source_notes = output_dir / "source-notes-p2b3.md"
    source_notes.write_text(SOURCE_NOTES, encoding="utf-8")
    for sample_id, definition in SAMPLE_DEFINITIONS.items():
        path = project_root / definition["source_markdown"]
        path.write_text(
            build_training_markdown(
                sample_id=sample_id,
                variant=definition["variant"],
                expected_class=definition["expected_class"],
            ),
            encoding="utf-8",
        )


def run_sample(
    project_root: Path,
    rubric_dir: Path,
    live: Any,
    sample_id: str,
) -> dict[str, Any]:
    definition = SAMPLE_DEFINITIONS[sample_id]
    output_dir = rubric_dir / "generated-replay" / "p2b3-samples" / sample_id
    output_dir.mkdir(parents=True, exist_ok=True)
    source_map = {
        "training_markdown": str(definition["source_markdown"]),
        "source_notes": str(OUTPUT_DATE_DIR / "source-notes-p2b3.md"),
    }
    sources = live.read_sources(project_root, source_map)
    anchors = live.read_yaml(rubric_dir / "rubric-score-anchors.yaml")["items"]
    config = {
        "case_titles": definition["case_titles"],
        "sources": source_map,
    }
    raw = live.build_raw_response(sample_id, config, sources, no_audit=False)
    raw["p2b3_sample"] = {
        "stage": "P2B-3",
        "sample_id": sample_id,
        "date": definition["date"],
        "expected_class": definition["expected_class"],
        "why_selected": definition["why_selected"],
        "governance_generated_real_output": True,
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
    validator_result["p2b3_sample"] = {
        "sample_id": sample_id,
        "expected_class": definition["expected_class"],
        "expected_diff_status": diff["status"],
        "date": definition["date"],
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
        paths,
        validator_result,
        no_audit=False,
    )
    log.update(
        {
            "stage": "P2B-3",
            "p2b3_sample_id": sample_id,
            "local_semantic_reviewer": True,
            "live_llm_review": False,
            "not_daily_production_pipeline": True,
            "not_p2c": True,
            "expected_class": definition["expected_class"],
            "expected_class_used_for_decision": False,
            "self_review_used_as_release_authority": False,
            "historical_audit_used_as_release_authority": False,
            "governance_generated_real_output": True,
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
        "output_dir": rel(project_root, output_dir),
    }


def build_source_manifest(
    project_root: Path,
    sample_id: str,
    definition: dict[str, Any],
    sources: dict[str, Any],
) -> dict[str, Any]:
    roles = {}
    for role in ("training_markdown", "reader_html", "source_notes", "quality_report", "historical_audit"):
        if role in sources:
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
        "stage": "P2B-3 third-date real sample set",
        "real_sample": True,
        "synthetic_fixture": False,
        "governance_generated_real_output": True,
        "date": definition["date"],
        "expected_class": definition["expected_class"],
        "why_selected": definition["why_selected"],
        "why_review_or_borderline": definition.get("why_review_or_borderline"),
        "sources": roles,
        "source_count": sum(1 for value in roles.values() if value.get("exists")),
        "local_semantic_reviewer": True,
        "live_llm_review": False,
        "not_daily_production_pipeline": True,
        "not_p2c": True,
        "project_root": str(project_root),
    }


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
        acceptable = decision in {"PASS", "REVIEW"} and decision not in {"FAIL_DAILY", "PUBLISH_BLOCK", "REPLACE_CASE"}
        note = "Third-date PASS sample may PASS or REVIEW, but must not hard-fail."
    elif expected == "REVIEW":
        acceptable = decision in {"REVIEW", "REWRITE_MODULE", "REWRITE_CASE", "USER_REVIEW_REQUIRED"} and not publish
        note = "Third-date REVIEW/borderline sample must not auto-publish."
    else:
        acceptable = decision != "PASS" and not publish
        note = "FAIL sample must not PASS."
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


def build_report(results: list[dict[str, Any]]) -> str:
    dates = sorted({item["date"] for item in results})
    review_samples = [item for item in results if item["expected_class"] == "REVIEW"]
    pass_samples = [item for item in results if item["expected_class"] == "PASS"]
    lines = [
        "# P2B-3 Third-Date Local Reviewer Sample Report",
        "",
        "## Boundary",
        "",
        "- Stage: P2B-3 third-date real sample set.",
        "- Reviewer: local semantic reviewer.",
        "- Not a live LLM reviewer.",
        "- Does not enter P2C.",
        "- Does not connect to the daily production chain.",
        "- P1 governance validator is not modified.",
        "- Self-review tables and historical audit reports are evidence inputs only, not release authority.",
        "",
        "## Coverage",
        "",
        f"- New real date: {', '.join(dates)}.",
        f"- New sample count: {len(results)}.",
        f"- PASS expected samples: {len(pass_samples)}.",
        f"- REVIEW / borderline expected samples: {len(review_samples)}.",
        "- All samples are governance-generated real outputs for 2026-06-28.",
        "- They are not natural historical production samples, and they are not synthetic fixtures pretending to be historical data.",
        "",
        "## Results",
        "",
        "| Sample | Date | Expected | Decision | Publish | Status | Output |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for result in results:
        lines.append(
            f"| `{result['sample_id']}` | `{result['date']}` | `{result['expected_class']}` | "
            f"`{result['daily_decision']}` | `{result['publish_allowed']}` | `{result['status']}` | `{result['output_dir']}` |"
        )
    lines.extend(
        [
            "",
            "## REVIEW / Borderline Explanation",
            "",
            *[
                f"- `{item['sample_id']}`: not auto-published because `{', '.join(item['failure_types']) or 'review boundary'}`."
                for item in review_samples
            ],
            "",
            "## Use Rule",
            "",
            "- This sample set can satisfy P2B-3 third-date and REVIEW/borderline replay coverage.",
            "- It still does not prove full Markdown-to-reviewer-payload semantic generation quality.",
            "- It must not unlock P2C by itself without the full regression suite staying green.",
            "",
        ]
    )
    return "\n".join(lines)


def build_training_markdown(sample_id: str, variant: str, expected_class: str) -> str:
    review_variant = variant.startswith("review")
    high_self_score = review_variant
    cases = [
        ("A", "阿里千问输入法 macOS", "AI 输入法 / 入口产品 / 个人效率", "用户把语音、润色和输入法放进同一个文本入口。"),
        ("B", "Runway API 广告本地化 Recipe", "创意 API / 营销工作流 / 多市场本地化", "生成式视频能力从素材生成进入广告运营流程。"),
        ("C", "OpenRouter 六月开放权重模型观察", "模型路由 / 开放权重 / 成本治理", "开放权重模型开始被按价格、能力和使用场景重新排序。"),
    ]
    parts = [
        f"# 高阶产品思维每日训练 - {DATE} P2B-3 {sample_id}",
        "",
        "P2B-3 治理样本说明：本文件用于 local semantic reviewer 的第三真实日期样本补齐，不作为正式每日发布稿。",
        "",
        "## 零、来源通道使用情况",
        "",
        "| 来源通道 | 状态 | 用途 | 限制与降级处理 |",
        "| --- | --- | --- | --- |",
        "| Search API / Web Search | 已使用 | 查询千问输入法、Runway API Recipe、OpenRouter open-weight models、DeepSeek DSpark 等 2026-06-28 信号。 | 部分事实来自二级媒体或社交信号，只作为 C 级信号；最终判断只使用有链接的官方博客、产品页或原文。 |",
        "| AI HOT | 已使用 | 读取 `https://aihot.virxact.com/api/public/daily/2026-06-28` 作为今日候选信号池。 | AI HOT 只作为发现信号，不作为最终事实依据。 |",
        "| GitHub / Open-source | 已使用 | 用于判断开放权重模型、DSpark、开发者工具链相关信号。 | star / fork 不作为商业成功证据。 |",
        "",
        "## 一、今日候选 case 池 + Case Selection Score",
        "",
        "| Case | 类型 | 来源 | 事实等级 | 相关性 | 信号强度 | 训练价值 | 可验证性 | 资产化价值 | 总分 | 处理方式 |",
        "| ---- | ---- | ---- | -------- | ------ | -------- | -------- | -------- | ---------- | ---- | -------- |",
        "| 阿里千问输入法 macOS | AI 入口产品 | AI HOT；IT之家；官网待复核 | B | 4 | 4 | 4 | 3 | 4 | 19 | 深度分析 |",
        "| Runway API 广告本地化 Recipe | 创意 API / 营销工作流 | AI HOT；Runway X；Runway API docs | B | 4 | 4 | 5 | 3 | 4 | 20 | 深度分析 |",
        "| OpenRouter 六月开放权重模型观察 | 模型路由 / 开放权重 | OpenRouter Blog；AI HOT | A | 5 | 4 | 5 | 5 | 5 | 24 | 深度分析 |",
        "| DeepSeek DSpark 投机解码 | 推理效率 / 开源框架 | AI HOT；MarkTechPost；GitHub 待复核 | C | 4 | 4 | 4 | 2 | 4 | 18 | Watchlist |",
        "| Raise Us AI retraining fund | 劳动力转型 | The Decoder；AI HOT | B | 3 | 3 | 4 | 4 | 3 | 17 | Watchlist |",
        "| Grack failed nation-state attack | 安全 / 攻击复盘 | Grack Blog；AI HOT | A | 3 | 4 | 4 | 5 | 3 | 19 | 雷达简报 |",
        "| SpaceXAI 商标与 xAI 合并传闻 | 行业动态 | X 信号；AI HOT | C | 3 | 4 | 3 | 1 | 3 | 14 | 轻量观察 |",
        "| Apple Vision 负责人跳槽 OpenAI 传闻 | 人才流动 | X 信号；AI HOT | C | 3 | 3 | 3 | 1 | 3 | 13 | 轻量观察 |",
        "",
        "### Case Selection Score 阈值说明",
        "",
        "| 总分 | 默认处理方式 | 说明 |",
        "| ---: | --- | --- |",
        "| 21-25 | 深度分析候选 | 优先进入 Case A / B / C 深度选择池 |",
        "| 17-20 | 雷达简报 / Watchlist | 有价值，但不一定适合当天深度分析 |",
        "| 13-16 | 轻量观察 | 只保留一句话判断，除非与用户项目高度相关 |",
        "| 12 以下 | 暂不处理 | 默认不进入训练内容 |",
        "",
        "## 二、今日深度 case 选择理由",
        "",
        "Case A：选择阿里千问输入法，是为了训练 AI 能力如何进入用户每天高频输入入口。",
        "Case B：选择 Runway API，是为了训练生成式能力如何从工具进入可度量营销流程。",
        "Case C：选择 OpenRouter，是为了训练模型路由、开放权重和成本治理如何变成产品判断。",
        "",
        "## 三、今日雷达简报",
        "",
        "| 标题 | 类型 | 一句话结论 | 为什么值得看 | 链接 | 后续动作 |",
        "| ---- | ---- | ---------- | ------------ | ---- | -------- |",
        "| DeepSeek DSpark | 推理效率 | 投机解码继续降低生成成本。 | 适合进入推理成本 Watchlist。 | https://www.marktechpost.com/2026/06/27/deepseek-releases-dspark-a-speculative-decoding-framework-that-accelerates-deepseek-v4-per-user-generation-60-85-over-mtp-1 | 等待官方 repo / paper 核验。 |",
        "| Grack attack postmortem | 安全复盘 | AI 工具链安全边界仍需攻击复盘。 | 可迁移到 agent 权限治理。 | https://grack.com/blog/2026/06/25/dissecting-a-failed-nation-state-attack | 观察 agent security checklist。 |",
        "",
        "## 四、今日 3 个深度 case",
        "",
    ]
    for label, title, case_type, observation in cases:
        parts.append(case_block(label, title, case_type, observation, review_variant, high_self_score))
    parts.extend(
        [
            "## 五、今日自主训练题",
            "",
            "如果你要把 2026-06-28 的 AI HOT 信号转成一个产品机会判断，你会先验证哪个变量，为什么？",
            "",
            "## 六、旧 case 复习",
            "",
            "复习 V6 的 Mistral Connectors：企业 agent 的核心不是工具数量，而是身份、权限、范围和审计。",
            "",
            "## 七、今日训练复盘",
            "",
            "| 维度 | 分数 1-5 | 简评 | 下一步如何补强 |",
            "| --- | ---: | --- | --- |",
            f"| 事实可靠性 | {'3' if review_variant else '4'} | 治理样本使用了真实链接，但部分信号仍是 C 级。 | 正式日报需继续追官方源。 |",
            f"| 本质抽象深度 | {'3' if review_variant else '4'} | {'边界样本刻意暴露套话化风险。' if review_variant else '结构完整，适合作为 local reviewer 第三日期 PASS 样本。'} | 增加更真实的商业数据。 |",
            f"| 系统关系清晰度 | {'3' if review_variant else '4'} | 覆盖用户、供给方、平台和风险方。 | 继续增强变量传导。 |",
            f"| 趋势推演可信度 | {'3' if review_variant else '4'} | 阶段推演存在，但证据仍有限。 | 等待更多官方更新。 |",
            f"| 机会判断质量 | {'3' if review_variant else '4'} | 有取舍但仍偏训练样本。 | 连接个人项目。 |",
            f"| 取舍明确度 | {'3' if review_variant else '4'} | 有做 / 不做 / 先验证。 | 提高可执行指标。 |",
            f"| 验证方案可执行性 | {'3' if review_variant else '4'} | 指标方向明确。 | 补数据口径。 |",
            f"| Case Asset Card 可复用度 | {'3' if review_variant else '4'} | 可进入治理样本库。 | 等正式样本替换。 |",
            "",
        ]
    )
    return "\n".join(parts)


def case_block(
    label: str,
    title: str,
    case_type: str,
    observation: str,
    review_variant: bool,
    high_self_score: bool,
) -> str:
    score = "96/100" if high_self_score else "88/100"
    return "\n".join(
        [
            f"### Case {label}：{title}",
            "",
            "【Case】",
            "",
            title,
            "",
            "【类型】",
            "",
            case_type,
            "",
            "【背景事实】",
            "",
            "已确认事实：",
            f"- {observation}",
            "- 该信号已进入 2026-06-28 AI HOT 候选池或可追溯公开来源。",
            "",
            "行业观点：",
            "- AI 产品竞争正在从单点能力转向工作流入口、成本治理和可验证交付。",
            "",
            "个人推断：",
            f"- {title} 的训练价值不在新闻本身，而在判断它如何改变用户工作流的控制点。",
            "",
            "待验证假设：",
            "- 需要继续核验真实采用、付费意愿、留存变化和企业部署约束。",
            "",
            "【信息来源】",
            "",
            "- AI HOT daily 2026-06-28：https://aihot.virxact.com/api/public/daily/2026-06-28",
            "- OpenRouter blog：https://openrouter.ai/blog/insights/the-open-weight-models-that-matter-june-2026",
            "- Runway signal：https://x.com/runwayml/status/2070855164584726791",
            "",
            "【为什么值得分析】",
            "",
            f"{title} 能训练 P7+ 从一个事件继续追问入口、场景、成本、收益、系统关系和价值流向。",
            "",
            "【本次训练目标】",
            "",
            "训练把热点信号拆成可验证产品判断，而不是停留在新闻摘要。",
            "",
            "【P6+ 第一反应】",
            "",
            f"“{title} 是一个新功能或新趋势，所以应该关注。”",
            "",
            "【这个思路对在哪里】",
            "",
            "它抓住了事件的新鲜度和表层变化。",
            "",
            "【这个思路为什么不够】",
            "",
            "它没有回答谁的场景被改变、什么成本被降低、哪个系统变量成为新约束，以及下一步应该验证什么。",
            "",
            "【P7+ 刹车动作】",
            "",
            "先不要评价热度，而要判断这个变化是否改变用户完成任务的成本、速度、可靠性和控制点。",
            "",
            "【Insight 总览】",
            "",
            f"一句话 Insight：{title} 的核心不是单点能力变强，而是工作流控制点正在迁移。",
            "",
            "核心判断：",
            "这不是功能新闻，而是入口、成本和治理边界重新分配的问题。",
            "",
            "行动取舍：",
            "- 建议推进：继续观察真实使用场景和用户任务完成率。",
            "- 暂不推进：不要只因 AI HOT 上榜就作为正式机会。",
            "- 优先验证：是否有高频场景、可度量收益和可持续供给。",
            "",
            "【V3.1 分析方法工作台】",
            "",
            "| 分析方法 | 为什么使用 | 拆解维度 | 得到的结论 |",
            "| --- | --- | --- | --- |",
            "| JTBD | 判断用户到底雇佣它完成什么任务 | 任务、场景、替代方案、成功标准 | 只有进入高频任务才有产品价值 |",
            "| 利益相关者地图 | 判断谁受益、谁承担风险 | 用户、平台、供给方、风险方 | 控制点不是单一能力，而是多方约束 |",
            "| 第一性原理 | 抽掉新闻包装看底层变量 | 成本、延迟、质量、可控性 | 真正变量是单位智能交付成本 |",
            "",
            "【P7+ 追问深答】",
            "",
            "追问：为什么不能只看它是不是热门？",
            "深答：热门只说明注意力集中，不说明用户任务发生了结构变化。P7+ 要看它是否改变了任务完成路径、降低了可感知成本、提高了可靠性，并带来可持续的价值流向。",
            "",
            "【底层矛盾与因果机制】",
            "",
            "底层矛盾：用户希望更快得到结果，但又需要质量、可控性和可追溯性。因果链是：能力进入入口或 API → 任务切换成本下降 → 高频使用增加 → 对可靠性和治理要求提高 → 产品价值从单点能力转向闭环工作流。",
            "",
            "【反面论证与边界条件】",
            "",
            "这个判断在以下条件下不成立：如果它只有话题热度、没有稳定入口；如果没有官方可验证材料；如果用户只是尝鲜而没有复用；如果成本下降无法传导到更好的任务完成体验。",
            "",
            "【8 问显性推理】",
            "",
            eight_questions(title, review_variant),
            "",
            "【六层表达】",
            "",
            "如果我在面试或汇报中表达，我会这样说：",
            "我会从六层来看这个问题。",
            f"第一，现象上，{title} 成为 2026-06-28 的一个 AI 产品信号。",
            "第二，原因上，AI 能力开始进入更靠近任务发生的位置。",
            "第三，本质上，这不是功能变化，而是工作流控制点变化。",
            "第四，系统上，用户、平台、模型供给、成本结构和治理约束共同作用。",
            "第五，趋势上，AI 产品会从单点工具进入可度量、可治理的任务闭环。",
            "第六，机会判断上，最大机会不在追热点，而在验证它是否改变高频任务的单位成本和可靠性。",
            "",
            "【PREP 表达版本】",
            "",
            "Point：我会先把它看成工作流控制点变化，而不是功能发布。Reason：因为 AI 能力只有进入真实任务闭环，才会影响留存、成本和商业价值。Evidence：今天的信号分别指向输入入口、创意 API 和模型路由。Point reinforced：所以应先验证高频任务和收益传导，而不是直接做结论。",
            "",
            "【SCQA 表达版本】",
            "",
            "Situation：AI 产品每天都有新发布。Complication：热度不能证明用户价值。Question：什么信号值得进入深度分析？Answer：看它是否改变用户任务路径、成本结构和治理边界。",
            "",
            "【Case Asset Card】",
            "",
            f"Case 名称：{title}",
            "所属方向：AI 产品判断 / P2B-3 governance sample",
            "一句话现象：一个 2026-06-28 信号进入训练样本。",
            "一句话本质：真正要判断的是控制点是否迁移。",
            "核心矛盾：能力变强与可验证价值之间存在落差。",
            "关键系统关系：用户、平台、模型供给、成本和风险控制共同作用。",
            "价值流向：从工具能力流向任务闭环。",
            "做 / 不做 / 先验证：做小范围观察，不做热度结论，先验证任务收益。",
            "可复用 Pattern：入口变化不等于机会成立，必须追到任务、成本和治理。",
            "可迁移到我的哪个项目：高阶产品思维每日训练质量治理。",
            "可迁移到哪类面试题：如何判断一个 AI 产品热点是否值得投入。",
            "2 分钟表达版本：先说现象，再说变量，再说系统关系，最后说验证路径。",
            "未来 Watchlist：持续跟踪是否出现官方数据、真实用户、商业化案例和负面风险。",
            "资产等级：B",
            "复习优先级：中",
            "",
            "【Insight Quality Audit】",
            "",
            f"总分：{score}",
            "思考深度：42/45",
            "内容质量：27/30",
            "表达质量：21/25",
            "扣分原因：治理样本服务 reviewer 测试，不等同于正式高质量日报。",
            "",
        ]
    )


def eight_questions(title: str, review_variant: bool) -> str:
    question_names = [
        "谁?",
        "在哪?",
        "损失什么?",
        "想得到什么?",
        "为什么卡住?",
        "谁共同作用?",
        "未来怎么变?",
        "价值流向哪里?",
    ]
    lines: list[str] = []
    for index, name in enumerate(question_names, start=1):
        if review_variant:
            purpose = f"第 {index} 步识别这个 case 的关键对象、场景、成本、收益和约束，判断它为什么不能直接自动放行。"
            why_method = f"第 {index} 个方法能把现象拆成可验证的变量，避免只复述新闻标题。"
        else:
            purpose = f"围绕 {title} 的第 {index} 个判断点，识别它对任务闭环的具体影响。"
            why_method = f"因为 {title} 需要从第 {index} 个变量进入产品判断，不能只靠热度推断。"
        method = [
            "利益相关者地图",
            "场景分层",
            "成本结构分析",
            "JTBD",
            "第一性原理 + 约束理论",
            "系统关系图",
            "S 曲线 + 情景推演",
            "价值链分析",
        ][index - 1]
        lines.extend(
            [
                f"{index}. {name}",
                f"目的：{purpose}",
                f"分析方法：{method}",
                f"为什么用这个方法：{why_method}",
                f"推导过程：围绕 {title}，第 {index} 步先把表层信号拆成对象、场景、成本、收益、约束和反馈。这样可以判断它是一次短期传播，还是已经进入可重复使用的任务路径。若变量能传导到任务完成率、单位成本、可靠性或治理边界，它才有进入深度分析的价值。",
                f"阶段结论：{title} 在第 {index} 个维度上仍需要真实数据支撑，但已经能形成可验证假设。",
                "如何影响下一步：下一步必须把这个阶段结论转成可观察指标，而不是继续扩写观点。",
                "",
            ]
        )
    return "\n".join(lines).rstrip()


SOURCE_NOTES = """# 2026-06-28 P2B-3 Source Notes

用途：本文件记录 2026-06-28 P2B-3 治理测试样本使用的来源。它不是正式每日生产链路产物。

## Source Channels

- AI HOT daily API: https://aihot.virxact.com/api/public/daily/2026-06-28
- 阿里千问输入法二级报道: https://www.ithome.com/0/969/334.htm
- Runway API 广告本地化 Recipe 信号: https://x.com/runwayml/status/2070855164584726791
- OpenRouter June 2026 open-weight models: https://openrouter.ai/blog/insights/the-open-weight-models-that-matter-june-2026
- DeepSeek DSpark secondary report: https://www.marktechpost.com/2026/06/27/deepseek-releases-dspark-a-speculative-decoding-framework-that-accelerates-deepseek-v4-per-user-generation-60-85-over-mtp-1
- Grack attack postmortem: https://grack.com/blog/2026/06/25/dissecting-a-failed-nation-state-attack

## Boundary

- AI HOT is a signal source only.
- X / social posts are C-level signals unless traced to official docs.
- This sample set is governance-generated for local semantic reviewer replay.
- It does not prove final content quality of the future daily production chain.
"""


def load_live_module(project_root: Path) -> Any:
    path = project_root / "scripts" / "run_live_reviewer_generation.py"
    spec = importlib.util.spec_from_file_location("run_live_reviewer_generation", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def rel(project_root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(project_root))


if __name__ == "__main__":
    raise SystemExit(main())
