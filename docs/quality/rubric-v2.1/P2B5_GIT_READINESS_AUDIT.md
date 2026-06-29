# P2B-5 Git Readiness Audit

Created at: 2026-06-29

## Summary

结论：当前还不应该直接进入 commit。可以进入 `git add` 准备阶段，但需要先按本报告拆分纳管范围，避免把可再生的大量 replay / shadow 产物和交付 zip 一起混入主提交。

当前工作树的核心问题不是 Rubric 逻辑失败，而是 Git 纳管边界尚未确定：

- `docs/quality/` 全部 untracked，里面既有必须纳管的治理源文件，也有大量可再生 replay artifacts。
- `scripts/` 全部 untracked，但 P2A/P2B/P2B-4 测试和外部复验都依赖这些脚本。
- 新增 Rubric v2.1 测试文件全部 untracked。
- `outputs/daily-training/2026-06-28/` 全部 untracked；P2B-3 脚本可以生成它，但 P2B-4 shadow run 默认也会读取其中的训练稿。
- 当前项目根目录没有 `rubric-v2.1-p2b3-p2b4-shadow-package.zip`，所以本轮不能从当前 worktree 直接证明 zip 自包含，只能审计 manifest 和依赖路径。

建议：进入 P2B-6 commit package preparation 前，先按本报告的 A/B/C/D 分类执行分批 `git add`，并补 `.gitignore` 建议，但本轮不执行 `git add`、不 commit、不 push。

## Current Git Status

### Commands Run

本轮已运行：

```bash
git status --short
git status --ignored --short
git diff --stat
git diff --name-only
git ls-files docs/quality/rubric-v2.1
git ls-files scripts
git ls-files tests
git ls-files outputs/daily-training/2026-06-25 outputs/daily-training/2026-06-26 outputs/daily-training/2026-06-28
```

### `git status --short`

关键结果：

```text
?? docs/quality/
?? outputs/daily-training/2026-06-28/
?? scripts/
?? tests/test_rubric_v21_adversarial.py
?? tests/test_rubric_v21_anchor_quality.py
?? tests/test_rubric_v21_calibration_replay.py
?? tests/test_rubric_v21_governance.py
?? tests/test_rubric_v21_live_reviewer_cross_samples.py
?? tests/test_rubric_v21_live_reviewer_p2b3.py
?? tests/test_rubric_v21_live_reviewer_p2b3_samples.py
?? tests/test_rubric_v21_live_reviewer_samples.py
?? tests/test_rubric_v21_live_reviewer_stability.py
?? tests/test_rubric_v21_live_reviewer_v7.py
?? tests/test_rubric_v21_p2b0_local_reviewer.py
?? tests/test_rubric_v21_reviewer_generator.py
?? tests/test_rubric_v21_shadow_review.py
```

### `git diff`

`git diff --stat` 和 `git diff --name-only` 当前为空。

解释：当前没有 tracked file modification；主要待处理项都是 untracked 文件/目录。

### Tracked Status

`git ls-files docs/quality/rubric-v2.1`：无输出。

`git ls-files scripts`：无输出。

`git ls-files tests` 仅包含旧测试：

```text
tests/test_failure_feedback_loop.py
tests/test_hermes_output_validator.py
tests/test_render_training_html.py
tests/test_render_training_reader_html.py
tests/verify_hermes_skill.py
```

`outputs/daily-training/2026-06-25` 和 `outputs/daily-training/2026-06-26` 的 Markdown/HTML/report 文本文件已 tracked；PNG 截图被 ignore。`outputs/daily-training/2026-06-28/` 当前 untracked。

### Ignored Files

当前 `.gitignore` 已覆盖：

```text
.DS_Store
.env
.env.*
__pycache__/
*.py[cod]
.playwright-cli/
.pytest_cache/
.coverage
htmlcov/
tmp/
dist/
build/
.worktrees/
outputs/**/*.png
outputs/playwright/
```

`git status --ignored --short` 还显示：

- `.DS_Store` 和多处目录级 `.DS_Store` 已 ignored。
- `outputs/**/*.png` 已 ignored，覆盖 2026-06-25/26 的截图类产物。
- `outputs/playwright/` 已 ignored。

当前 `.gitignore` 没有忽略 `*.zip`，但当前项目根目录也没有 zip 文件。

### Status Categorization

| 类别 | 当前状态 |
| --- | --- |
| tracked modified | 无。`git diff --stat` 与 `git diff --name-only` 均为空。 |
| untracked source files | `docs/quality/rubric-v2.1` core files、`scripts/*.py`、`tests/test_rubric_v21*.py` 均未纳管。 |
| untracked generated artifacts | `docs/quality/rubric-v2.1/generated-replay/`、`docs/quality/rubric-v2.1/shadow-runs/` 在 untracked `docs/quality/` 内。 |
| untracked package / zip files | 当前项目根目录无 zip 文件；`find . -maxdepth 3 -name '*.zip'` 无输出。 |
| ignored files | `.DS_Store`、`.playwright-cli/`、`.worktrees/`、`outputs/**/*.png`、`outputs/playwright/` 等已被 ignore。 |

## Required Tracked Files

### A. 必须纳入 Git 的治理源文件

这些文件是 Rubric v2.1 治理系统的源协议、枚举、schema、validator、评分锚点、校准定义和人类可读报告。建议纳入 git：

```text
docs/quality/rubric-v2.1/rubric-v2.1.md
docs/quality/rubric-v2.1/rubric-enums.yaml
docs/quality/rubric-v2.1/rubric-score-anchors.yaml
docs/quality/rubric-v2.1/reviewer-output.schema.json
docs/quality/rubric-v2.1/claim-evidence-map.schema.json
docs/quality/rubric-v2.1/failure-object.schema.json
docs/quality/rubric-v2.1/calibration-tests.yaml
docs/quality/rubric-v2.1/repair-rerun-map.yaml
docs/quality/rubric-v2.1/validator-check-map.yaml
docs/quality/rubric-v2.1/rubric_governance_validator.py
docs/quality/rubric-v2.1/reviewer-generation-protocol.md
docs/quality/rubric-v2.1/reviewer-payload-generator.md
docs/quality/rubric-v2.1/P1_REPLAY_PACKAGE_README.md
docs/quality/rubric-v2.1/P1_REPLAY_PACKAGE_MANIFEST.yaml
docs/quality/rubric-v2.1/P2B3_P2B4_COMPLETION_REPORT.md
docs/quality/rubric-v2.1/P2B3_P2B4_PACKAGE_MANIFEST.yaml
docs/quality/rubric-v2.1/P2B5_GIT_READINESS_AUDIT.md
docs/quality/rubric-v2.1/calibration-replay-report.md
docs/quality/rubric-v2.1/reviewer-generation-report.md
docs/quality/rubric-v2.1/p2b0-local-reviewer-hardening-report.md
docs/quality/rubric-v2.1/live-reviewer-samples-report.md
docs/quality/rubric-v2.1/live-reviewer-stability-report.md
docs/quality/rubric-v2.1/live-reviewer-cross-sample-report.md
docs/quality/rubric-v2.1/live-reviewer-p2b3-sample-report.md
docs/quality/rubric-v2.1/shadow-run-report.md
```

必须同时纳入 P1 calibration fixtures，因为 P1 replay tests 直接读取它们：

```text
docs/quality/rubric-v2.1/fixtures/calibration/
```

### B. 必须纳入 Git 的 Scripts

这些脚本是 P2A/P2B/P2B-4 测试与 replay 的执行器。建议全部纳入 git：

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

P2B-4 外部复验和 shadow tests 还依赖下面两个 skill script。它们当前已 tracked，但必须在 commit 计划中确认不要漏掉：

```text
skill/scripts/render_training_reader_html.py
skill/scripts/validate_training_reader_html.py
```

### C. 必须纳入 Git 的 Tests

Rubric v2.1 的新测试当前全部 untracked。建议全部纳入 git：

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

## Generated Artifacts Policy

本节对应 D / E 两类文件。

### D. 是否纳入 Git 需要判断的 Generated Artifacts

#### Should Enter Git As Regression Fixtures

建议纳入 git 的 generated fixtures：

```text
docs/quality/rubric-v2.1/generated-replay/v3_target/
docs/quality/rubric-v2.1/generated-replay/v6_target/
docs/quality/rubric-v2.1/generated-replay/v7_failure/
```

理由：

- `scripts/run_live_reviewer_generation.py` 会把 live output 与这些 recorded fixture 做 golden comparison。
- 如果只运行 P2B live reviewer tests，而没有先运行 P2A generator，这些 recorded fixtures 缺失会导致 clean clone 下的局部测试不稳定。
- 它们是小体积、稳定、可解释的 golden baseline。

建议纳入 git 的 2026-06-28 source fixture：

```text
outputs/daily-training/2026-06-28/aihot-daily-2026-06-28.json
outputs/daily-training/2026-06-28/source-notes-p2b3.md
outputs/daily-training/2026-06-28/training-v8-pass.md
outputs/daily-training/2026-06-28/training-v8-review-boilerplate.md
outputs/daily-training/2026-06-28/training-v8-review-method-overlap.md
```

理由：

- 这 5 个文件体积小，合计约 156K。
- P2B-3 script 可以生成它们，但 P2B-4 shadow run 默认会读取 `outputs/daily-training/2026-06-28/`。
- 如果只运行 `tests.test_rubric_v21_shadow_review`，而没有先运行 P2B-3 sample generator，这些文件缺失会导致 shadow test 不稳定。

#### Should Be Generated At Test Runtime, Not Tracked

建议不纳入 git、由测试/脚本运行时生成：

```text
docs/quality/rubric-v2.1/generated-replay/v3_target_live/
docs/quality/rubric-v2.1/generated-replay/v6_target_live/
docs/quality/rubric-v2.1/generated-replay/v7_failure_live/
docs/quality/rubric-v2.1/generated-replay/v7_failure_no_audit_live/
docs/quality/rubric-v2.1/generated-replay/stability/
docs/quality/rubric-v2.1/generated-replay/cross-samples/
docs/quality/rubric-v2.1/generated-replay/p2b3-samples/
docs/quality/rubric-v2.1/shadow-runs/
```

理由：

- 这些目录是 local reviewer / stability / cross-sample / shadow run 的运行结果。
- 当前数量较多：`generated-replay` 有 176 个文件，约 3.7M；`shadow-runs` 有 17 个文件，约 592K。
- 它们适合作为外部复验包或 CI artifact 保留，不适合作为每次迭代都更新的主仓库源文件。
- 对于需要长期复验的结论，应保留 sample manifest、golden fixture 或报告，而不是完整运行目录。

#### Already Tracked / Keep Tracked

`outputs/daily-training/2026-06-25` 与 `outputs/daily-training/2026-06-26` 中的 Markdown/HTML/report 文本文件已经 tracked，应继续保留，因为 P2A/P2B replay 脚本直接读取它们。

PNG 截图类产物当前已被 `.gitignore` 忽略，不建议纳入 git：

```text
outputs/daily-training/**/*.png
```

### E. 不建议纳入 Git 的交付压缩包

当前项目根目录没有发现 zip：

```text
find . -maxdepth 3 -type f -name '*.zip' -> no output
```

后续如果重新生成以下交付包，不建议纳入 git：

```text
rubric-v2.1-p1-replay-package.zip
rubric-v2.1-p2b3-p2b4-shadow-package.zip
```

建议处理方式：

- 作为 GitHub Release artifact、外部交付包或本地归档保存。
- 在 `.gitignore` 中加入 `*.zip`。
- 如果需要可复验，应纳管的是生成 zip 的 source files、manifest、tests 和 scripts，而不是 zip 本身。

## Test Fixture Dependency Map

### 1. 运行 146 Tests 最小需要哪些文件

最小依赖分为五层：

1. Rubric core：

```text
docs/quality/rubric-v2.1/rubric-v2.1.md
docs/quality/rubric-v2.1/rubric-enums.yaml
docs/quality/rubric-v2.1/rubric-score-anchors.yaml
docs/quality/rubric-v2.1/*.schema.json
docs/quality/rubric-v2.1/calibration-tests.yaml
docs/quality/rubric-v2.1/repair-rerun-map.yaml
docs/quality/rubric-v2.1/validator-check-map.yaml
docs/quality/rubric-v2.1/rubric_governance_validator.py
```

2. P1 calibration fixtures：

```text
docs/quality/rubric-v2.1/fixtures/calibration/
```

3. Recorded golden fixtures：

```text
docs/quality/rubric-v2.1/generated-replay/v3_target/
docs/quality/rubric-v2.1/generated-replay/v6_target/
docs/quality/rubric-v2.1/generated-replay/v7_failure/
```

4. Source daily-training files：

```text
outputs/daily-training/2026-06-25/*.md
outputs/daily-training/2026-06-25/*.html
outputs/daily-training/2026-06-26/*.md
outputs/daily-training/2026-06-26/*.html
outputs/daily-training/2026-06-28/*.md
outputs/daily-training/2026-06-28/*.json
```

5. Execution scripts and tests：

```text
scripts/*.py
tests/test_rubric_v21*.py
skill/scripts/render_training_reader_html.py
skill/scripts/validate_training_reader_html.py
```

### 2. 哪些 generated-replay 文件其实是测试 fixture

应视为 regression fixtures：

```text
docs/quality/rubric-v2.1/generated-replay/v3_target/
docs/quality/rubric-v2.1/generated-replay/v6_target/
docs/quality/rubric-v2.1/generated-replay/v7_failure/
```

这些用于 recorded/golden comparison。

其余 `generated-replay/*_live`、`generated-replay/stability`、`generated-replay/cross-samples`、`generated-replay/p2b3-samples` 更像运行产物，不建议 git 纳管。

### 3. 哪些 shadow-run 文件是测试 fixture

`docs/quality/rubric-v2.1/shadow-runs/2026-06-28/` 当前是 P2B-4 运行产物，不建议直接纳入 git。

原因：

- `tests/test_rubric_v21_shadow_review.py` 会运行 `scripts/run_daily_shadow_review.py` 重新生成该目录。
- 应纳管的是 shadow run 脚本、HTML renderer/validator、输入源文件、以及人类可读报告。
- 完整 shadow run 目录适合作为外部 replay package 或 release artifact。

### 4. Clean Clone 后运行测试会不会缺文件

如果只使用当前 tracked 文件，clean clone 会缺文件。

缺失原因：

- `docs/quality/rubric-v2.1/` 当前完全 untracked。
- `scripts/` 当前完全 untracked。
- Rubric v2.1 新测试当前完全 untracked。
- `outputs/daily-training/2026-06-28/` 当前 untracked。

如果按本报告 Recommended Git Add Plan 纳管后：

- 完整 146 tests 应具备必要源文件。
- 局部运行 `tests.test_rubric_v21_shadow_review` 也更稳，因为 2026-06-28 source fixture 会存在。

### 5. 如果缺，应该纳入 git 还是改测试为运行时生成

建议：

- Governance source / scripts / tests / P1 fixtures：必须纳入 git。
- 2026-06-28 source fixture：建议纳入 git，确保 shadow test 可单独运行。
- Large generated replay / shadow outputs：不纳入 git，运行时生成。
- 若未来希望更严格控制仓库体积，可以改 `test_rubric_v21_shadow_review.py` 在 setUpClass 里先调用 P2B-3 source generator；但本轮不改测试。

## External Replay Package Dependency Check

当前 worktree 中没有 `rubric-v2.1-p2b3-p2b4-shadow-package.zip`，所以无法直接从当前 zip 文件复验 self-contained。

当前已检查 manifest 所声明的外部复验依赖，相关本地文件都存在：

```text
OK skill/scripts/render_training_reader_html.py
OK skill/scripts/validate_training_reader_html.py
OK scripts/run_daily_shadow_review.py
OK scripts/run_live_reviewer_generation.py
OK docs/quality/rubric-v2.1/rubric-v2.1.md
OK tests/test_rubric_v21_shadow_review.py
OK outputs/daily-training/2026-06-28/training-v8-pass.md
OK outputs/daily-training/2026-06-28/training-v8-review-boilerplate.md
OK outputs/daily-training/2026-06-28/training-v8-review-method-overlap.md
```

Current-state package result：

```yaml
external_package_self_contained: false
missing_dependencies:
  - "rubric-v2.1-p2b3-p2b4-shadow-package.zip is not present in current worktree, so package contents cannot be inspected."
local_manifest_dependency_files_missing: []
```

解释：

- `local_manifest_dependency_files_missing: []` 表示 manifest 中列出的本地依赖文件当前都存在。
- 但因为当前根目录没有 zip 文件，不能声称当前 zip self-contained；因此 current-state 结论必须是 `external_package_self_contained: false`。
- 若重新打包，必须包含 manifest 的 `external_replay_dependencies` 中列出的两个 skill scripts。

## Recommended Git Add Plan

不要直接 `git add .`。

建议分批：

### Batch 1: Rubric Core + Calibration Fixtures

```bash
git add \
  docs/quality/rubric-v2.1/rubric-v2.1.md \
  docs/quality/rubric-v2.1/rubric-enums.yaml \
  docs/quality/rubric-v2.1/rubric-score-anchors.yaml \
  docs/quality/rubric-v2.1/reviewer-output.schema.json \
  docs/quality/rubric-v2.1/claim-evidence-map.schema.json \
  docs/quality/rubric-v2.1/failure-object.schema.json \
  docs/quality/rubric-v2.1/calibration-tests.yaml \
  docs/quality/rubric-v2.1/repair-rerun-map.yaml \
  docs/quality/rubric-v2.1/validator-check-map.yaml \
  docs/quality/rubric-v2.1/rubric_governance_validator.py \
  docs/quality/rubric-v2.1/fixtures/calibration
```

### Batch 2: Human-Readable Governance Docs / Reports

```bash
git add \
  docs/quality/rubric-v2.1/P1_REPLAY_PACKAGE_README.md \
  docs/quality/rubric-v2.1/P1_REPLAY_PACKAGE_MANIFEST.yaml \
  docs/quality/rubric-v2.1/P2B3_P2B4_COMPLETION_REPORT.md \
  docs/quality/rubric-v2.1/P2B3_P2B4_PACKAGE_MANIFEST.yaml \
  docs/quality/rubric-v2.1/P2B5_GIT_READINESS_AUDIT.md \
  docs/quality/rubric-v2.1/calibration-replay-report.md \
  docs/quality/rubric-v2.1/reviewer-generation-protocol.md \
  docs/quality/rubric-v2.1/reviewer-payload-generator.md \
  docs/quality/rubric-v2.1/reviewer-generation-report.md \
  docs/quality/rubric-v2.1/p2b0-local-reviewer-hardening-report.md \
  docs/quality/rubric-v2.1/live-reviewer-samples-report.md \
  docs/quality/rubric-v2.1/live-reviewer-stability-report.md \
  docs/quality/rubric-v2.1/live-reviewer-cross-sample-report.md \
  docs/quality/rubric-v2.1/live-reviewer-p2b3-sample-report.md \
  docs/quality/rubric-v2.1/shadow-run-report.md
```

### Batch 3: Recorded Golden Fixtures

```bash
git add \
  docs/quality/rubric-v2.1/generated-replay/v3_target \
  docs/quality/rubric-v2.1/generated-replay/v6_target \
  docs/quality/rubric-v2.1/generated-replay/v7_failure
```

### Batch 4: Scripts

```bash
git add \
  scripts/generate_reviewer_payload.py \
  scripts/run_reviewer_generation_replay.py \
  scripts/run_live_reviewer_generation.py \
  scripts/run_live_reviewer_generation_v7.py \
  scripts/run_live_reviewer_stability.py \
  scripts/run_live_reviewer_cross_samples.py \
  scripts/run_live_reviewer_p2b3_samples.py \
  scripts/run_daily_shadow_review.py
```

`skill/scripts/render_training_reader_html.py` and `skill/scripts/validate_training_reader_html.py` are already tracked. If they ever show modified, include them in a separate renderer/validator commit rather than bundling with generated artifacts.

### Batch 5: Tests

```bash
git add \
  tests/test_rubric_v21_governance.py \
  tests/test_rubric_v21_adversarial.py \
  tests/test_rubric_v21_anchor_quality.py \
  tests/test_rubric_v21_calibration_replay.py \
  tests/test_rubric_v21_reviewer_generator.py \
  tests/test_rubric_v21_p2b0_local_reviewer.py \
  tests/test_rubric_v21_live_reviewer_samples.py \
  tests/test_rubric_v21_live_reviewer_v7.py \
  tests/test_rubric_v21_live_reviewer_stability.py \
  tests/test_rubric_v21_live_reviewer_cross_samples.py \
  tests/test_rubric_v21_live_reviewer_p2b3.py \
  tests/test_rubric_v21_live_reviewer_p2b3_samples.py \
  tests/test_rubric_v21_shadow_review.py
```

### Batch 6: 2026-06-28 Source Fixtures

```bash
git add \
  outputs/daily-training/2026-06-28/aihot-daily-2026-06-28.json \
  outputs/daily-training/2026-06-28/source-notes-p2b3.md \
  outputs/daily-training/2026-06-28/training-v8-pass.md \
  outputs/daily-training/2026-06-28/training-v8-review-boilerplate.md \
  outputs/daily-training/2026-06-28/training-v8-review-method-overlap.md
```

## Recommended Gitignore Changes

本轮不修改 `.gitignore`，但建议后续新增：

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

注意：如果使用上述 `generated-replay` ignore 策略，必须确保不误忽略下面三个 golden dirs：

```text
docs/quality/rubric-v2.1/generated-replay/v3_target/
docs/quality/rubric-v2.1/generated-replay/v6_target/
docs/quality/rubric-v2.1/generated-replay/v7_failure/
```

不能忽略：

```text
docs/quality/rubric-v2.1/fixtures/calibration/
docs/quality/rubric-v2.1/*.yaml
docs/quality/rubric-v2.1/*.json
docs/quality/rubric-v2.1/*.schema.json
docs/quality/rubric-v2.1/*.py
scripts/
tests/test_rubric_v21*.py
outputs/daily-training/2026-06-28/*.md
outputs/daily-training/2026-06-28/*.json
```

## Risks Before Commit

1. **Over-adding generated artifacts**

   如果直接 `git add docs/quality/`，会把大量 runtime replay / shadow run 结果纳入 git，未来每次测试都可能产生 churn。

2. **Under-adding source fixtures**

   如果不纳入 `generated-replay/v3_target/v6_target/v7_failure`，局部 live reviewer tests 可能缺 recorded comparison fixture。

3. **Shadow test isolated run risk**

   如果不纳入 `outputs/daily-training/2026-06-28/`，单独运行 `tests.test_rubric_v21_shadow_review` 可能缺默认输入。完整 146 tests 可能因先运行 P2B-3 generator 而绕过该问题，但这不是稳健的测试依赖设计。

4. **Zip artifact policy unclear**

   当前根目录没有 zip。后续如果重新生成，应作为 release artifact 或外部交付包保留，不建议 commit 到主仓库。

5. **`.DS_Store` in untracked docs tree**

   `find docs/quality/rubric-v2.1 -maxdepth 2` 可见 `.DS_Store`，但它已被 ignore。不要强制 add。

6. **Reports may contain historical claims**

   P2B reports是治理证据，应纳管；但 commit 前应确认文案仍符合当前边界：不进入 P2C、不接正式发布、不通知用户。

## Next Step

建议下一步进入 **P2B-6 commit package preparation**，但不要直接 commit。

P2B-6 应做：

1. 先按本报告建议更新 `.gitignore`。
2. 按 Batch 1-6 分批执行 `git add`。
3. 用 `git status --short` 复查 staged/untracked/ignored 边界。
4. 运行完整 146 tests。
5. 生成 commit readiness report。
6. 等用户确认后再 commit。

当前是否可以进入 P2B-6：可以，但前提是先确认 generated artifacts policy，尤其是：

- 是否接受只纳管 `generated-replay/v3_target/v6_target/v7_failure` 作为 golden fixtures。
- 是否接受不纳管 `generated-replay/*_live`、`cross-samples`、`stability`、`p2b3-samples`、`shadow-runs`。
- 是否接受把 zip 放 release artifact，不放 git。
