# P2B-6 Commit Readiness Report

Created at: 2026-06-29

## Summary

可以进入用户确认 commit 阶段，但本轮仍未 commit、未 push、未进入 P2C、未接每日生产链路、未更新官网、未发送用户通知。

本轮完成：

- 已按 P2B-5 audit 更新 `.gitignore`。
- 已按 7 个 batch 精确执行 `git add`，未使用 `git add .`。
- 已 stage Rubric v2.1 / P2A / P2B / P2B-4 shadow run 所需源文件、测试文件、P1 fixtures、recorded golden fixtures、2026-06-28 source fixtures。
- 已排除 zip 包、runtime generated replay、shadow run artifacts、`.DS_Store`、`__pycache__`。
- 已运行完整 146 tests，通过。

当前 staged 集合在生成本报告前为 99 个文件；本报告按目标要求加入 staged 后，总计应为 100 个 staged 文件。

## Gitignore Changes

本轮 `.gitignore` 新增：

```gitignore
# Release / external replay packages
*.zip

# Rubric v2.1 runtime replay outputs
docs/quality/rubric-v2.1/generated-replay/*_live/
docs/quality/rubric-v2.1/generated-replay/v7_failure_no_audit_live/
docs/quality/rubric-v2.1/generated-replay/stability/
docs/quality/rubric-v2.1/generated-replay/cross-samples/
docs/quality/rubric-v2.1/generated-replay/p2b3-samples/
docs/quality/rubric-v2.1/shadow-runs/

# Temporary package extraction dirs
rubric-v2.1-*-extract/
```

目的：

- 防止外部交付 zip 误入 git。
- 防止 runtime replay / shadow run 产物误入 git。
- 保留可纳管的 golden fixtures：`v3_target`、`v6_target`、`v7_failure`。

## Staged Files Summary

### Rubric Core

已 stage 25 个 `docs/quality/rubric-v2.1/` 根层治理文件，包括：

- `rubric-v2.1.md`
- `rubric-enums.yaml`
- `rubric-score-anchors.yaml`
- `reviewer-output.schema.json`
- `claim-evidence-map.schema.json`
- `failure-object.schema.json`
- `calibration-tests.yaml`
- `repair-rerun-map.yaml`
- `validator-check-map.yaml`
- `rubric_governance_validator.py`

### Calibration Fixtures

已 stage：

```text
docs/quality/rubric-v2.1/fixtures/calibration/
```

数量：32 个文件。

### Human-Readable Docs / Reports

已 stage：

- `P1_REPLAY_PACKAGE_README.md`
- `P1_REPLAY_PACKAGE_MANIFEST.yaml`
- `P2B3_P2B4_COMPLETION_REPORT.md`
- `P2B3_P2B4_PACKAGE_MANIFEST.yaml`
- `P2B5_GIT_READINESS_AUDIT.md`
- `P2B6_COMMIT_READINESS_REPORT.md`
- `calibration-replay-report.md`
- `reviewer-generation-protocol.md`
- `reviewer-payload-generator.md`
- `reviewer-generation-report.md`
- `p2b0-local-reviewer-hardening-report.md`
- `live-reviewer-samples-report.md`
- `live-reviewer-stability-report.md`
- `live-reviewer-cross-sample-report.md`
- `live-reviewer-p2b3-sample-report.md`
- `shadow-run-report.md`

### Golden Fixtures

已 stage 三个最小 recorded golden fixture 目录：

```text
docs/quality/rubric-v2.1/generated-replay/v3_target/
docs/quality/rubric-v2.1/generated-replay/v6_target/
docs/quality/rubric-v2.1/generated-replay/v7_failure/
```

数量：15 个文件。

### Scripts

已 stage 8 个脚本：

```text
scripts/generate_reviewer_payload.py
scripts/run_reviewer_generation_replay.py
scripts/run_live_reviewer_generation.py
scripts/run_live_reviewer_generation_v7.py
scripts/run_live_reviewer_stability.py
scripts/run_live_reviewer_cross_samples.py
scripts/run_live_reviewer_p2b3_samples.py
scripts/run_daily_shadow_review.py
```

确认：`skill/scripts/render_training_reader_html.py` 和 `skill/scripts/validate_training_reader_html.py` 已是 tracked 且本轮无 modified 状态，未混入本轮 staging。

### Tests

已 stage 13 个 Rubric v2.1 测试文件：

```text
tests/test_rubric_v21_governance.py
tests/test_rubric_v21_adversarial.py
tests/test_rubric_v21_anchor_quality.py
tests/test_rubric_v21_calibration_replay.py
tests/test_rubric_v21_reviewer_generator.py
tests/test_rubric_v21_p2b0_local_reviewer.py
tests/test_rubric_v21_live_reviewer_samples.py
tests/test_rubric_v21_live_reviewer_v7.py
tests/test_rubric_v21_live_reviewer_stability.py
tests/test_rubric_v21_live_reviewer_cross_samples.py
tests/test_rubric_v21_live_reviewer_p2b3.py
tests/test_rubric_v21_live_reviewer_p2b3_samples.py
tests/test_rubric_v21_shadow_review.py
```

### 2026-06-28 Source Fixtures

已 stage 5 个文件：

```text
outputs/daily-training/2026-06-28/aihot-daily-2026-06-28.json
outputs/daily-training/2026-06-28/source-notes-p2b3.md
outputs/daily-training/2026-06-28/training-v8-pass.md
outputs/daily-training/2026-06-28/training-v8-review-boilerplate.md
outputs/daily-training/2026-06-28/training-v8-review-method-overlap.md
```

### Gitignore

已 stage：

```text
.gitignore
```

## Excluded Files

已确认 staged 中未包含：

- zip 包
- `generated-replay/*_live`
- `generated-replay/v7_failure_no_audit_live`
- `generated-replay/stability`
- `generated-replay/cross-samples`
- `generated-replay/p2b3-samples`
- `shadow-runs`
- `.DS_Store`
- `__pycache__`

检查命令：

```bash
git diff --cached --name-only | rg '\.zip$|(^|/)\.DS_Store$|__pycache__|docs/quality/rubric-v2\.1/generated-replay/.*_live/|docs/quality/rubric-v2\.1/generated-replay/v7_failure_no_audit_live/|docs/quality/rubric-v2\.1/generated-replay/stability/|docs/quality/rubric-v2\.1/generated-replay/cross-samples/|docs/quality/rubric-v2\.1/generated-replay/p2b3-samples/|docs/quality/rubric-v2\.1/shadow-runs/'
```

结果：无匹配。

Ignored 边界样例：

```text
!! docs/quality/rubric-v2.1/generated-replay/cross-samples/
!! docs/quality/rubric-v2.1/generated-replay/p2b3-samples/
!! docs/quality/rubric-v2.1/generated-replay/stability/
!! docs/quality/rubric-v2.1/generated-replay/v3_target_live/
!! docs/quality/rubric-v2.1/generated-replay/v6_target_live/
!! docs/quality/rubric-v2.1/generated-replay/v7_failure_live/
!! docs/quality/rubric-v2.1/generated-replay/v7_failure_no_audit_live/
!! docs/quality/rubric-v2.1/shadow-runs/
```

## Test Result

完整回归命令：

```bash
python3 -m unittest \
  tests.test_rubric_v21_governance \
  tests.test_rubric_v21_adversarial \
  tests.test_rubric_v21_anchor_quality \
  tests.test_rubric_v21_calibration_replay \
  tests.test_rubric_v21_reviewer_generator \
  tests.test_rubric_v21_p2b0_local_reviewer \
  tests.test_rubric_v21_live_reviewer_samples \
  tests.test_rubric_v21_live_reviewer_v7 \
  tests.test_rubric_v21_live_reviewer_stability \
  tests.test_rubric_v21_live_reviewer_cross_samples \
  tests.test_rubric_v21_live_reviewer_p2b3 \
  tests.test_rubric_v21_live_reviewer_p2b3_samples \
  tests.test_rubric_v21_shadow_review
```

结果：

```text
Ran 146 tests in 465.016s
OK
```

Additional check:

```bash
git diff --cached --check
```

结果：通过，无输出。

## Clean Clone Risk Assessment

当前 staged 集合足以支持 clean clone 运行 146 tests，前提是 commit 时包含本报告列出的 staged 文件。

理由：

- Rubric core / schemas / validator 已 stage。
- P1 calibration fixtures 已 stage。
- Recorded golden fixtures `v3_target` / `v6_target` / `v7_failure` 已 stage。
- P2A/P2B/P2B-4 scripts 已 stage。
- Rubric v2.1 tests 已 stage。
- 2026-06-28 source fixtures 已 stage，避免单独运行 P2B-4 shadow test 时缺默认输入。
- Runtime generated replay / shadow run artifacts 已通过 `.gitignore` 排除，可以在测试运行时生成。

仍需注意：

- 本阶段验证的是 local semantic reviewer / recorded replay / shadow harness，不是 live LLM reviewer。
- 本阶段不证明 P2C 每日生产链路可直接启用。

## Commit Recommendation

建议 commit message：

```text
feat(rubric): add v2.1 governance replay and shadow review harness
```

## Remaining Risks

- 仍不是 P2C。
- 仍不是 live LLM reviewer。
- P2B-3 第三日期是 governance-generated sample，不是自然历史生产样本。
- Shadow run 不发布、不通知用户、不更新官网。
- Commit 前应让用户确认是否接受当前 generated artifact policy：只纳管 recorded golden fixtures，不纳管 runtime generated replay / shadow output。
- 如果未来希望提交外部 replay zip，应走 release artifact，而不是主仓库 git commit。

## Next Step

等待用户确认后再 commit。

建议下一步：

1. 用户审核 staged scope。
2. 如同意，进入 commit confirmation。
3. commit 前再跑一次 `git status --short` 与必要测试。
4. 仍然不要进入 P2C，除非用户另行确认。
