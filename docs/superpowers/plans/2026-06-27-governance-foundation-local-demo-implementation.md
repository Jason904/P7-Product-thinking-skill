# 治理基础与本机双仓库演示实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在不连接真实 GitHub、Mac mini 和微信的前提下，建立项目级治理规则，并在 MacBook Air 上完整演示成功发布、失败阻断、保留上一期、生成失败包和修复恢复。

**Architecture:** 在项目根目录增加独立的 `ops` Python 包，负责运行状态、门禁结果、重试策略、失败包、通知文案和本机发布模拟。现有 Skill 与校验脚本保持内容职责，`ops` 只负责编排，不复制内容生成规则。

**Tech Stack:** Python 3 标准库、`unittest`、现有校验脚本、临时目录、本机文件系统、Git。

---

## 1. 文件结构

本阶段创建：

```text
hermes-p7-product-thinking-package/
├── AGENTS.md
├── .gitignore
├── ops/
│   ├── __init__.py
│   ├── models.py
│   ├── policy.py
│   ├── failure_package.py
│   ├── local_publish.py
│   ├── notifications.py
│   ├── pipeline.py
│   └── demo.py
├── templates/
│   └── public-site/
│       └── AGENTS.md
├── docs/
│   └── operations/
│       └── local-demo.md
└── tests/
    ├── test_project_governance.py
    ├── test_ops_models.py
    ├── test_ops_policy.py
    ├── test_ops_failure_package.py
    ├── test_ops_local_publish.py
    ├── test_ops_notifications.py
    ├── test_ops_pipeline.py
    └── test_ops_demo.py
```

职责边界：

- `skill/`：内容搜索、推理、模板、渲染和已有确定性校验。
- `ops/`：每日任务的状态、门禁编排、重试、发布和失败处理。
- `templates/public-site/`：未来公开网站仓库的项目级约束模板。
- `tests/`：治理和本机演示的回归测试。

## 2. 实施约束

- 本阶段不调用真实 AI。
- 本阶段不创建真实 GitHub 仓库。
- 本阶段不发送真实微信。
- 本阶段不修改现有 V7 输出作为演示结果。
- 本阶段只模拟“门禁已经给出结果”后的编排行为。
- 独立 AI 评审本身在阶段二 A 实现。
- 真实 GitHub 和 Pages 在阶段三实现。

### Task 1: 建立 Git 仓库边界和项目级 `AGENTS.md`

**Files:**
- Create: `.gitignore`
- Create: `AGENTS.md`
- Create: `templates/public-site/AGENTS.md`
- Create: `tests/test_project_governance.py`

- [ ] **Step 1: 编写失败测试**

创建 `tests/test_project_governance.py`：

```python
#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ProjectGovernanceTests(unittest.TestCase):
    def test_control_repository_agents_file_defines_non_negotiables(self) -> None:
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        for phrase in (
            "高阶产品思维每日训练",
            "用户本人是唯一人工质量负责人",
            "每个失败环节最多进行 2 次定向重试",
            "未通过门禁的训练正文不得进入公开网站仓库",
            "MacBook Air",
            "Mac mini",
            "Bad Case",
        ):
            self.assertIn(phrase, text)

    def test_public_site_agents_file_blocks_private_artifacts(self) -> None:
        text = (ROOT / "templates" / "public-site" / "AGENTS.md").read_text(encoding="utf-8")
        for phrase in (
            "只接收通过全部门禁的训练正文",
            "失败包",
            "内部质量报告",
            "不得直接手改单日 HTML",
        ):
            self.assertIn(phrase, text)

    def test_gitignore_excludes_local_noise_and_secrets(self) -> None:
        text = (ROOT / ".gitignore").read_text(encoding="utf-8")
        for pattern in (".DS_Store", ".env", "__pycache__/", ".playwright-cli/"):
            self.assertIn(pattern, text)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 运行测试并确认失败**

Run:

```bash
python3 -m unittest tests.test_project_governance -v
```

Expected: FAIL，因为 `AGENTS.md`、公开站点约束和 `.gitignore` 尚不存在。

- [ ] **Step 3: 创建 `.gitignore`**

写入：

```gitignore
.DS_Store
.env
.env.*
!.env.example
__pycache__/
*.py[cod]
.playwright-cli/
.pytest_cache/
.coverage
htmlcov/
tmp/
dist/
build/
```

- [ ] **Step 4: 创建私有控制仓库 `AGENTS.md`**

文件必须明确：

```markdown
# 高阶产品思维每日训练项目规则

## 项目目标
本项目用于每日稳定生产三个 Insight 级高阶产品思维训练 Case。

## 角色
- MacBook Air：开发和质量治理中心。
- Mac mini：Hermes 每日生产中心，不是规则源头。
- 用户本人是唯一人工质量负责人。

## 不可绕过的规则
- 每个失败环节最多进行 2 次定向重试。
- 未通过门禁的训练正文不得进入公开网站仓库。
- 失败时保留上一期合格内容，只允许公开“今日内容审核中”状态。
- 生成者自评没有放行权。
- 严重 Bad Case 必须回流产品标准、治理规则或回归测试。

## 仓库边界
- 私有控制仓库保存 Skill、草稿、评审、失败包和复测证据。
- 公开网站仓库只保存通过门禁的 HTML 和公开状态。

## 修改原则
- 长期问题必须修规则、生成器、门禁或测试，不能只手改单日产物。
- 不得删除或覆盖用户已有内容。
- 修改后运行相关单元测试、Skill 验证和输出校验。
```

- [ ] **Step 5: 创建公开站点 `AGENTS.md` 模板**

文件必须明确：

```markdown
# 高阶产品思维每日训练公开站点规则

## 仓库职责
本仓库只接收通过全部门禁的训练正文和公开网站资源。

## 禁止提交
- 失败包
- 未通过草稿
- 用户批注
- 内部质量报告
- 访问凭证和密钥

## 发布规则
- 失败时不得更新训练正文，只能更新“今日内容审核中”状态。
- 不得直接手改单日 HTML 作为长期修复。
- 重复问题必须回到私有控制仓库修生成器、模板或设计系统。
- 发布前必须通过 HTML 完整性和桌面端、移动端检查。
```

- [ ] **Step 6: 运行测试并确认通过**

Run:

```bash
python3 -m unittest tests.test_project_governance -v
```

Expected: 3 tests PASS。

- [ ] **Step 7: 初始化 Git 并提交**

仅在项目仍不是 Git 仓库时运行：

```bash
git init -b main
git add .gitignore AGENTS.md templates/public-site/AGENTS.md tests/test_project_governance.py
git commit -m "chore: establish project governance rules"
```

Expected: 创建 `main` 分支和第一个治理提交。

### Task 2: 建立运行状态和门禁结果模型

**Files:**
- Create: `ops/__init__.py`
- Create: `ops/models.py`
- Create: `tests/test_ops_models.py`

- [ ] **Step 1: 编写失败测试**

创建 `tests/test_ops_models.py`：

```python
#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest

from ops.models import GateResult, GateStatus, RetryRecord, RunManifest, RunState


class OpsModelTests(unittest.TestCase):
    def test_manifest_serializes_enums_and_nested_records(self) -> None:
        manifest = RunManifest(
            run_id="run-2026-06-27",
            training_date="2026-06-27",
            skill_version="1.0.0",
            renderer_version="1.0.0",
        )
        manifest.transition(RunState.REVIEWING)
        manifest.gates.append(
            GateResult(
                gate_id="G5",
                name="Insight 质量",
                status=GateStatus.FAIL,
                reason="Case B 论据不足",
                failed_scope="case-b",
            )
        )
        manifest.retries.append(
            RetryRecord(gate_id="G5", attempt=1, reason="Case B 论据不足")
        )

        payload = manifest.to_dict()
        self.assertEqual("reviewing", payload["state"])
        self.assertEqual("fail", payload["gates"][0]["status"])
        self.assertEqual(1, payload["retries"][0]["attempt"])
        json.dumps(payload, ensure_ascii=False)

    def test_manifest_records_state_history(self) -> None:
        manifest = RunManifest(
            run_id="run-1",
            training_date="2026-06-27",
            skill_version="1.0.0",
            renderer_version="1.0.0",
        )
        manifest.transition(RunState.GENERATING)
        manifest.transition(RunState.REVIEWING)
        self.assertEqual(
            ["waiting", "generating", "reviewing"],
            [state.value for state in manifest.state_history],
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 运行测试并确认失败**

Run:

```bash
python3 -m unittest tests.test_ops_models -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'ops'`。

- [ ] **Step 3: 创建模型实现**

创建空的 `ops/__init__.py`，并在 `ops/models.py` 实现：

```python
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class RunState(str, Enum):
    WAITING = "waiting"
    GENERATING = "generating"
    REVIEWING = "reviewing"
    RETRYING = "retrying"
    READY = "ready"
    PUBLISHED = "published"
    BLOCKED = "blocked"


class GateStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    REVIEW = "review"


@dataclass(frozen=True)
class GateResult:
    gate_id: str
    name: str
    status: GateStatus
    reason: str
    failed_scope: str = ""
    retryable: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate_id": self.gate_id,
            "name": self.name,
            "status": self.status.value,
            "reason": self.reason,
            "failed_scope": self.failed_scope,
            "retryable": self.retryable,
        }


@dataclass(frozen=True)
class RetryRecord:
    gate_id: str
    attempt: int
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate_id": self.gate_id,
            "attempt": self.attempt,
            "reason": self.reason,
        }


@dataclass
class RunManifest:
    run_id: str
    training_date: str
    skill_version: str
    renderer_version: str
    state: RunState = RunState.WAITING
    state_history: list[RunState] = field(default_factory=lambda: [RunState.WAITING])
    gates: list[GateResult] = field(default_factory=list)
    retries: list[RetryRecord] = field(default_factory=list)
    failure_id: str = ""
    published_path: str = ""
    last_good_path: str = ""

    def transition(self, state: RunState) -> None:
        self.state = state
        self.state_history.append(state)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "training_date": self.training_date,
            "skill_version": self.skill_version,
            "renderer_version": self.renderer_version,
            "state": self.state.value,
            "state_history": [state.value for state in self.state_history],
            "gates": [gate.to_dict() for gate in self.gates],
            "retries": [retry.to_dict() for retry in self.retries],
            "failure_id": self.failure_id,
            "published_path": self.published_path,
            "last_good_path": self.last_good_path,
        }
```

- [ ] **Step 4: 运行测试并确认通过**

Run:

```bash
python3 -m unittest tests.test_ops_models -v
```

Expected: 2 tests PASS。

- [ ] **Step 5: 提交**

```bash
git add ops/__init__.py ops/models.py tests/test_ops_models.py
git commit -m "feat: add daily run state models"
```

### Task 3: 实现每个门禁最多两次定向重试

**Files:**
- Create: `ops/policy.py`
- Create: `tests/test_ops_policy.py`

- [ ] **Step 1: 编写失败测试**

```python
#!/usr/bin/env python3
from __future__ import annotations

import unittest

from ops.models import GateResult, GateStatus
from ops.policy import Action, RetryPolicy


class RetryPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = RetryPolicy(max_retries_per_gate=2)

    def test_pass_continues(self) -> None:
        result = GateResult("G3", "Markdown", GateStatus.PASS, "完整")
        self.assertEqual(Action.CONTINUE, self.policy.decide(result, 0))

    def test_first_and_second_failures_retry(self) -> None:
        result = GateResult("G5", "Insight", GateStatus.FAIL, "浅")
        self.assertEqual(Action.RETRY, self.policy.decide(result, 0))
        self.assertEqual(Action.RETRY, self.policy.decide(result, 1))

    def test_third_failure_blocks(self) -> None:
        result = GateResult("G5", "Insight", GateStatus.FAIL, "仍然浅")
        self.assertEqual(Action.BLOCK, self.policy.decide(result, 2))

    def test_non_retryable_failure_blocks_immediately(self) -> None:
        result = GateResult(
            "G0", "版本", GateStatus.FAIL, "稳定版缺失", retryable=False
        )
        self.assertEqual(Action.BLOCK, self.policy.decide(result, 0))

    def test_review_status_requests_human_review(self) -> None:
        result = GateResult("G5", "Insight", GateStatus.REVIEW, "双评审冲突")
        self.assertEqual(Action.REVIEW, self.policy.decide(result, 0))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 运行测试并确认失败**

Run:

```bash
python3 -m unittest tests.test_ops_policy -v
```

Expected: FAIL，因为 `ops.policy` 尚不存在。

- [ ] **Step 3: 实现重试策略**

创建 `ops/policy.py`：

```python
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from ops.models import GateResult, GateStatus


class Action(str, Enum):
    CONTINUE = "continue"
    RETRY = "retry"
    BLOCK = "block"
    REVIEW = "review"


@dataclass(frozen=True)
class RetryPolicy:
    max_retries_per_gate: int = 2

    def decide(self, result: GateResult, retries_used: int) -> Action:
        if result.status is GateStatus.PASS:
            return Action.CONTINUE
        if result.status is GateStatus.REVIEW:
            return Action.REVIEW
        if not result.retryable:
            return Action.BLOCK
        if retries_used < self.max_retries_per_gate:
            return Action.RETRY
        return Action.BLOCK
```

- [ ] **Step 4: 运行测试并确认通过**

Run:

```bash
python3 -m unittest tests.test_ops_policy -v
```

Expected: 5 tests PASS。

- [ ] **Step 5: 提交**

```bash
git add ops/policy.py tests/test_ops_policy.py
git commit -m "feat: enforce two targeted retries per gate"
```

### Task 4: 生成结构化失败包

**Files:**
- Create: `ops/failure_package.py`
- Create: `tests/test_ops_failure_package.py`

- [ ] **Step 1: 编写失败测试**

测试必须验证失败包分开保存用户判断、系统发现和 AI 分析：

```python
#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from ops.failure_package import create_failure_package
from ops.models import RunManifest, RunState


class FailurePackageTests(unittest.TestCase):
    def test_create_failure_package_preserves_evidence_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            markdown = root / "training.md"
            html = root / "training.html"
            markdown.write_text("# draft", encoding="utf-8")
            html.write_text("<h1>draft</h1>", encoding="utf-8")
            manifest = RunManifest("run-1", "2026-06-27", "1.0.0", "1.0.0")
            manifest.transition(RunState.BLOCKED)

            package = create_failure_package(
                inbox_root=root / "failure-inbox",
                manifest=manifest,
                artifacts=[markdown, html],
                user_judgment="用户认为 Case B 缺乏论据",
                system_findings=["G5 两次重试后失败"],
                ai_analysis=["可能需要补充价值链证据"],
            )

            self.assertTrue((package / "manifest.json").exists())
            self.assertTrue((package / "failure-report.md").exists())
            self.assertTrue((package / "artifacts" / "training.md").exists())
            payload = json.loads((package / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual("blocked", payload["state"])
            report = (package / "failure-report.md").read_text(encoding="utf-8")
            self.assertIn("用户原始判断", report)
            self.assertIn("系统自动发现", report)
            self.assertIn("AI 补充分析", report)
            self.assertIn("用户认为 Case B 缺乏论据", report)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 运行测试并确认失败**

```bash
python3 -m unittest tests.test_ops_failure_package -v
```

Expected: FAIL，因为实现尚不存在。

- [ ] **Step 3: 实现失败包**

创建完整的 `ops/failure_package.py`：

```python
from __future__ import annotations

import json
import shutil
from pathlib import Path

from ops.models import RunManifest


def _bullet_list(items: list[str]) -> str:
    if not items:
        return "- 无"
    return "\n".join(f"- {item}" for item in items)


def create_failure_package(
    *,
    inbox_root: Path,
    manifest: RunManifest,
    artifacts: list[Path],
    user_judgment: str = "",
    system_findings: list[str] | None = None,
    ai_analysis: list[str] | None = None,
) -> Path:
    failure_id = f"QF-{manifest.training_date}-{manifest.run_id}"
    manifest.failure_id = failure_id
    package = inbox_root / failure_id
    artifact_root = package / "artifacts"
    artifact_root.mkdir(parents=True, exist_ok=True)

    for source in artifacts:
        if source.exists() and source.is_file():
            shutil.copy2(source, artifact_root / source.name)

    (package / "manifest.json").write_text(
        json.dumps(manifest.to_dict(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    report = (
        f"# 失败报告：{failure_id}\n\n"
        "## 用户原始判断\n\n"
        f"{user_judgment or '无用户判断，失败由系统自动发现。'}\n\n"
        "## 系统自动发现\n\n"
        f"{_bullet_list(system_findings or [])}\n\n"
        "## AI 补充分析\n\n"
        f"{_bullet_list(ai_analysis or [])}\n"
    )
    (package / "failure-report.md").write_text(report, encoding="utf-8")
    return package
```

- [ ] **Step 4: 运行测试并确认通过**

```bash
python3 -m unittest tests.test_ops_failure_package -v
```

Expected: 1 test PASS。

- [ ] **Step 5: 提交**

```bash
git add ops/failure_package.py tests/test_ops_failure_package.py
git commit -m "feat: create structured failure packages"
```

### Task 5: 模拟公开仓库发布和保留上一期

**Files:**
- Create: `ops/local_publish.py`
- Create: `tests/test_ops_local_publish.py`

- [ ] **Step 1: 编写失败测试**

```python
#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from ops.local_publish import mark_under_review, publish_html
from ops.models import RunManifest, RunState


class LocalPublishTests(unittest.TestCase):
    def test_publish_ready_manifest_updates_current_pointer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            html = root / "training.html"
            html.write_text("<h1>approved</h1>", encoding="utf-8")
            manifest = RunManifest("run-1", "2026-06-27", "1.0.0", "1.0.0")
            manifest.transition(RunState.READY)

            published = publish_html(html, root / "public", manifest)

            self.assertTrue(published.exists())
            current = json.loads(
                (root / "public" / "current.json").read_text(encoding="utf-8")
            )
            self.assertEqual("daily/2026-06-27/index.html", current["path"])

    def test_blocked_run_keeps_previous_content_and_only_updates_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            public = root / "public"
            previous = public / "daily" / "2026-06-26" / "index.html"
            previous.parent.mkdir(parents=True)
            previous.write_text("<h1>last good</h1>", encoding="utf-8")
            (public / "current.json").write_text(
                json.dumps({"date": "2026-06-26", "path": "daily/2026-06-26/index.html"}),
                encoding="utf-8",
            )

            mark_under_review(public, "2026-06-27")

            self.assertEqual("<h1>last good</h1>", previous.read_text(encoding="utf-8"))
            current = json.loads((public / "current.json").read_text(encoding="utf-8"))
            status = json.loads((public / "status.json").read_text(encoding="utf-8"))
            self.assertEqual("2026-06-26", current["date"])
            self.assertEqual("under_review", status["status"])
            self.assertEqual("2026-06-27", status["date"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 运行测试并确认失败**

```bash
python3 -m unittest tests.test_ops_local_publish -v
```

Expected: FAIL。

- [ ] **Step 3: 实现本机发布器**

创建完整的 `ops/local_publish.py`。`mark_under_review` 只能写
`status.json`，不得修改 `current.json` 或已有 HTML：

```python
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from ops.models import RunManifest, RunState


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def publish_html(source_html: Path, public_root: Path, manifest: RunManifest) -> Path:
    if manifest.state is not RunState.READY:
        raise ValueError("Only READY runs may publish training HTML")
    destination = public_root / "daily" / manifest.training_date / "index.html"
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_html, destination)
    _write_json(
        public_root / "current.json",
        {
            "date": manifest.training_date,
            "path": f"daily/{manifest.training_date}/index.html",
        },
    )
    _write_json(
        public_root / "status.json",
        {"date": manifest.training_date, "status": "published"},
    )
    manifest.published_path = str(destination)
    return destination


def mark_under_review(public_root: Path, training_date: str) -> None:
    public_root.mkdir(parents=True, exist_ok=True)
    _write_json(
        public_root / "status.json",
        {"date": training_date, "status": "under_review"},
    )
```

- [ ] **Step 4: 运行测试并确认通过**

```bash
python3 -m unittest tests.test_ops_local_publish -v
```

Expected: 2 tests PASS。

- [ ] **Step 5: 提交**

```bash
git add ops/local_publish.py tests/test_ops_local_publish.py
git commit -m "feat: preserve last good publication on failure"
```

### Task 6: 生成微信通知预览

**Files:**
- Create: `ops/notifications.py`
- Create: `tests/test_ops_notifications.py`

- [ ] **Step 1: 编写失败测试**

```python
#!/usr/bin/env python3
from __future__ import annotations

import unittest

from ops.models import GateResult, GateStatus, RunManifest
from ops.notifications import render_failure_message, render_success_message


class NotificationTests(unittest.TestCase):
    def test_success_message_contains_date_and_url(self) -> None:
        text = render_success_message("2026-06-27", "https://example.com/2026-06-27/")
        self.assertIn("今日训练已发布", text)
        self.assertIn("2026-06-27", text)
        self.assertIn("https://example.com/2026-06-27/", text)

    def test_failure_message_contains_decision_context(self) -> None:
        manifest = RunManifest("run-1", "2026-06-27", "1.0.0", "1.0.0")
        manifest.failure_id = "QF-2026-06-27-run-1"
        manifest.gates.append(
            GateResult("G5", "Insight 质量", GateStatus.FAIL, "Case B 论据不足")
        )
        text = render_failure_message(
            manifest,
            issue_url="https://github.com/example/control/issues/1",
            retries_used=2,
        )
        for phrase in (
            "今日训练发布受阻",
            "Insight 质量",
            "2 次",
            "官网保留上一期内容",
            "QF-2026-06-27-run-1",
            "https://github.com/example/control/issues/1",
        ):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 运行测试并确认失败**

```bash
python3 -m unittest tests.test_ops_notifications -v
```

Expected: FAIL。

- [ ] **Step 3: 实现通知文案**

接口：

```python
def render_success_message(training_date: str, public_url: str) -> str:
    return (
        "【今日训练已发布】\n"
        f"日期：{training_date}\n"
        "质量状态：全部通过\n"
        f"线上链接：{public_url}"
    )


def render_failure_message(
    manifest: RunManifest,
    *,
    issue_url: str,
    retries_used: int,
) -> str:
    failed_gate = next(
        (gate for gate in reversed(manifest.gates) if gate.status is not GateStatus.PASS),
        None,
    )
    gate_name = failed_gate.name if failed_gate else "未知门禁"
    reason = failed_gate.reason if failed_gate else "未记录"
    return (
        "【今日训练发布受阻，需要审核】\n"
        f"日期：{manifest.training_date}\n"
        f"失败环节：{gate_name}\n"
        f"失败原因：{reason}\n"
        f"自动重试：{retries_used} 次，仍未通过\n"
        "官网状态：官网保留上一期内容\n"
        f"失败编号：{manifest.failure_id}\n"
        f"GitHub 问题单：{issue_url}"
    )
```

- [ ] **Step 4: 运行测试并确认通过**

```bash
python3 -m unittest tests.test_ops_notifications -v
```

Expected: 2 tests PASS。

- [ ] **Step 5: 提交**

```bash
git add ops/notifications.py tests/test_ops_notifications.py
git commit -m "feat: render production notification previews"
```

### Task 7: 编排成功、失败和人工审核状态

**Files:**
- Create: `ops/pipeline.py`
- Create: `tests/test_ops_pipeline.py`

- [ ] **Step 1: 编写成功和失败集成测试**

测试使用脚本化门禁结果，不调用真实 AI：

```python
#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from ops.models import GateResult, GateStatus, RunState
from ops.pipeline import LocalPipeline


def passing_gate(gate_id: str) -> list[GateResult]:
    return [GateResult(gate_id, gate_id, GateStatus.PASS, "通过")]


class PipelineTests(unittest.TestCase):
    def test_successful_run_publishes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            markdown = root / "training.md"
            html = root / "training.html"
            markdown.write_text("# approved", encoding="utf-8")
            html.write_text("<h1>approved</h1>", encoding="utf-8")
            scenario = {f"G{i}": passing_gate(f"G{i}") for i in range(9)}

            manifest = LocalPipeline(root / "control", root / "public").run(
                training_date="2026-06-27",
                skill_version="1.0.0",
                renderer_version="1.0.0",
                markdown=markdown,
                html=html,
                scenario=scenario,
            )

            self.assertEqual(RunState.PUBLISHED, manifest.state)
            self.assertTrue(
                (root / "public" / "daily" / "2026-06-27" / "index.html").exists()
            )

    def test_third_failure_blocks_and_creates_failure_package(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            markdown = root / "training.md"
            html = root / "training.html"
            markdown.write_text("# shallow", encoding="utf-8")
            html.write_text("<h1>shallow</h1>", encoding="utf-8")
            previous = root / "public" / "daily" / "2026-06-26" / "index.html"
            previous.parent.mkdir(parents=True)
            previous.write_text("<h1>last good</h1>", encoding="utf-8")
            (root / "public" / "current.json").write_text(
                json.dumps({"date": "2026-06-26", "path": "daily/2026-06-26/index.html"}),
                encoding="utf-8",
            )
            scenario = {f"G{i}": passing_gate(f"G{i}") for i in range(9)}
            scenario["G5"] = [
                GateResult("G5", "Insight 质量", GateStatus.FAIL, "初次失败"),
                GateResult("G5", "Insight 质量", GateStatus.FAIL, "重试一失败"),
                GateResult("G5", "Insight 质量", GateStatus.FAIL, "重试二失败"),
            ]

            manifest = LocalPipeline(root / "control", root / "public").run(
                training_date="2026-06-27",
                skill_version="1.0.0",
                renderer_version="1.0.0",
                markdown=markdown,
                html=html,
                scenario=scenario,
            )

            self.assertEqual(RunState.BLOCKED, manifest.state)
            self.assertEqual(2, len(manifest.retries))
            self.assertEqual("<h1>last good</h1>", previous.read_text(encoding="utf-8"))
            self.assertTrue(
                any((root / "control" / "failure-inbox").iterdir())
            )

    def test_review_result_blocks_without_retrying(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            markdown = root / "training.md"
            html = root / "training.html"
            markdown.write_text("# review", encoding="utf-8")
            html.write_text("<h1>review</h1>", encoding="utf-8")
            scenario = {f"G{i}": passing_gate(f"G{i}") for i in range(9)}
            scenario["G5"] = [
                GateResult("G5", "Insight 质量", GateStatus.REVIEW, "双评审冲突")
            ]

            manifest = LocalPipeline(root / "control", root / "public").run(
                training_date="2026-06-27",
                skill_version="1.0.0",
                renderer_version="1.0.0",
                markdown=markdown,
                html=html,
                scenario=scenario,
            )

            self.assertEqual(RunState.BLOCKED, manifest.state)
            self.assertEqual([], manifest.retries)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 运行测试并确认失败**

```bash
python3 -m unittest tests.test_ops_pipeline -v
```

Expected: FAIL。

- [ ] **Step 3: 实现 `LocalPipeline`**

创建完整的 `ops/pipeline.py`：

```python
from __future__ import annotations

import json
from pathlib import Path

from ops.failure_package import create_failure_package
from ops.local_publish import mark_under_review, publish_html
from ops.models import GateResult, RetryRecord, RunManifest, RunState
from ops.policy import Action, RetryPolicy


GATE_ORDER = tuple(f"G{index}" for index in range(9))


class LocalPipeline:
    def __init__(self, control_root: Path, public_root: Path) -> None:
        self.control_root = control_root
        self.public_root = public_root
        self.policy = RetryPolicy(max_retries_per_gate=2)

    def _save_manifest(self, manifest: RunManifest) -> None:
        path = self.control_root / "runs" / manifest.run_id / "run-manifest.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(manifest.to_dict(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _block(
        self,
        manifest: RunManifest,
        markdown: Path,
        html: Path,
        result: GateResult,
    ) -> RunManifest:
        manifest.transition(RunState.BLOCKED)
        mark_under_review(self.public_root, manifest.training_date)
        create_failure_package(
            inbox_root=self.control_root / "failure-inbox",
            manifest=manifest,
            artifacts=[markdown, html],
            system_findings=[f"{result.gate_id} {result.name}: {result.reason}"],
        )
        self._save_manifest(manifest)
        return manifest

    def run(
        self,
        *,
        training_date: str,
        skill_version: str,
        renderer_version: str,
        markdown: Path,
        html: Path,
        scenario: dict[str, list[GateResult]],
    ) -> RunManifest:
        manifest = RunManifest(
            run_id=f"run-{training_date}",
            training_date=training_date,
            skill_version=skill_version,
            renderer_version=renderer_version,
        )
        manifest.transition(RunState.GENERATING)
        manifest.transition(RunState.REVIEWING)

        for gate_id in GATE_ORDER:
            results = scenario.get(gate_id)
            if not results:
                raise ValueError(f"Scenario is missing results for {gate_id}")
            retries_used = 0
            while True:
                result = results[min(retries_used, len(results) - 1)]
                manifest.gates.append(result)
                action = self.policy.decide(result, retries_used)
                if action is Action.CONTINUE:
                    break
                if action is Action.RETRY:
                    retries_used += 1
                    manifest.retries.append(
                        RetryRecord(
                            gate_id=gate_id,
                            attempt=retries_used,
                            reason=result.reason,
                        )
                    )
                    manifest.transition(RunState.RETRYING)
                    manifest.transition(RunState.REVIEWING)
                    continue
                return self._block(manifest, markdown, html, result)

        manifest.transition(RunState.READY)
        publish_html(html, self.public_root, manifest)
        manifest.transition(RunState.PUBLISHED)
        self._save_manifest(manifest)
        return manifest
```

当脚本结果数量不足时，使用最后一个结果，确保第三次失败稳定阻断。

- [ ] **Step 4: 运行测试并确认通过**

```bash
python3 -m unittest tests.test_ops_pipeline -v
```

Expected: 3 tests PASS。

- [ ] **Step 5: 运行全部新增测试**

```bash
python3 -m unittest \
  tests.test_project_governance \
  tests.test_ops_models \
  tests.test_ops_policy \
  tests.test_ops_failure_package \
  tests.test_ops_local_publish \
  tests.test_ops_notifications \
  tests.test_ops_pipeline -v
```

Expected: 全部 PASS。

- [ ] **Step 6: 提交**

```bash
git add ops/pipeline.py tests/test_ops_pipeline.py
git commit -m "feat: orchestrate local quality-gated publishing"
```

### Task 8: 提供可视化的三场景命令行演示

**Files:**
- Create: `ops/demo.py`
- Create: `tests/test_ops_demo.py`
- Create: `docs/operations/local-demo.md`

- [ ] **Step 1: 编写失败测试**

`tests/test_ops_demo.py`：

```python
#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DemoCliTests(unittest.TestCase):
    def run_demo(self, scenario: str, workspace: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                "-m",
                "ops.demo",
                "--scenario",
                scenario,
                "--workspace",
                str(workspace),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_pass_scenario_publishes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_demo("pass", Path(tmp))
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("今日训练已发布", result.stdout)
            self.assertTrue(
                (Path(tmp) / "public" / "daily" / "2026-06-27" / "index.html").exists()
            )

    def test_fail_scenario_preserves_last_good(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_demo("fail", Path(tmp))
            self.assertEqual(2, result.returncode)
            self.assertIn("今日训练发布受阻", result.stdout)
            self.assertIn("官网保留上一期内容", result.stdout)
            self.assertTrue(
                (Path(tmp) / "public" / "daily" / "2026-06-26" / "index.html").exists()
            )

    def test_recover_scenario_fails_then_publishes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_demo("recover", Path(tmp))
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("首次运行：BLOCKED", result.stdout)
            self.assertIn("修复后运行：PUBLISHED", result.stdout)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 运行测试并确认失败**

```bash
python3 -m unittest tests.test_ops_demo -v
```

Expected: FAIL。

- [ ] **Step 3: 实现 `ops.demo`**

命令：

```bash
python3 -m ops.demo --scenario pass --workspace /tmp/hermes-local-demo
python3 -m ops.demo --scenario fail --workspace /tmp/hermes-local-demo
python3 -m ops.demo --scenario recover --workspace /tmp/hermes-local-demo
```

创建完整的 `ops/demo.py`：

```python
from __future__ import annotations

import argparse
import json
from pathlib import Path

from ops.models import GateResult, GateStatus, RunManifest
from ops.notifications import render_failure_message, render_success_message
from ops.pipeline import LocalPipeline


TRAINING_DATE = "2026-06-27"
PUBLIC_URL = "https://example.github.io/daily-training/2026-06-27/"
ISSUE_URL = "https://github.com/example/private-control/issues/1"


def passing_scenario() -> dict[str, list[GateResult]]:
    return {
        f"G{index}": [
            GateResult(f"G{index}", f"G{index}", GateStatus.PASS, "通过")
        ]
        for index in range(9)
    }


def failing_scenario() -> dict[str, list[GateResult]]:
    scenario = passing_scenario()
    scenario["G5"] = [
        GateResult("G5", "Insight 质量", GateStatus.FAIL, "初次评审不通过"),
        GateResult("G5", "Insight 质量", GateStatus.FAIL, "第一次重试仍不通过"),
        GateResult("G5", "Insight 质量", GateStatus.FAIL, "第二次重试仍不通过"),
    ]
    return scenario


def prepare_workspace(workspace: Path, *, seed_last_good: bool) -> tuple[Path, Path]:
    control = workspace / "control"
    public = workspace / "public"
    draft = control / "drafts" / TRAINING_DATE
    draft.mkdir(parents=True, exist_ok=True)
    markdown = draft / "training.md"
    html = draft / "training.html"
    markdown.write_text("# 本机演示训练稿\n", encoding="utf-8")
    html.write_text("<h1>本机演示训练稿</h1>\n", encoding="utf-8")

    if seed_last_good:
        previous = public / "daily" / "2026-06-26" / "index.html"
        previous.parent.mkdir(parents=True, exist_ok=True)
        previous.write_text("<h1>上一期合格内容</h1>\n", encoding="utf-8")
        (public / "current.json").write_text(
            json.dumps(
                {
                    "date": "2026-06-26",
                    "path": "daily/2026-06-26/index.html",
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    return markdown, html


def run_once(
    workspace: Path,
    scenario: dict[str, list[GateResult]],
    *,
    seed_last_good: bool,
) -> RunManifest:
    markdown, html = prepare_workspace(workspace, seed_last_good=seed_last_good)
    pipeline = LocalPipeline(workspace / "control", workspace / "public")
    return pipeline.run(
        training_date=TRAINING_DATE,
        skill_version="local-demo-1.0.0",
        renderer_version="local-demo-1.0.0",
        markdown=markdown,
        html=html,
        scenario=scenario,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", choices=("pass", "fail", "recover"), required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    args.workspace.mkdir(parents=True, exist_ok=True)

    if args.scenario == "pass":
        manifest = run_once(args.workspace, passing_scenario(), seed_last_good=False)
        print(render_success_message(TRAINING_DATE, PUBLIC_URL))
        return 0

    if args.scenario == "fail":
        manifest = run_once(args.workspace, failing_scenario(), seed_last_good=True)
        print(
            render_failure_message(
                manifest,
                issue_url=ISSUE_URL,
                retries_used=len(manifest.retries),
            )
        )
        return 2

    first = run_once(args.workspace, failing_scenario(), seed_last_good=True)
    print(f"首次运行：{first.state.name}")
    second = run_once(args.workspace, passing_scenario(), seed_last_good=False)
    print(f"修复后运行：{second.state.name}")
    print(render_success_message(TRAINING_DATE, PUBLIC_URL))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

模拟 URL 只能用于本机演示，禁止写入后续真实生产配置。

- [ ] **Step 4: 编写演示说明**

`docs/operations/local-demo.md` 必须说明：

- 本演示验证什么。
- 哪些能力仍然是模拟。
- 三个命令如何运行。
- 成功后看哪些目录。
- 失败后如何确认上一期未被覆盖。
- 如何查看失败包、manifest 和通知文案。
- 为什么本阶段不能代表 AI Insight 质量已经稳定。

- [ ] **Step 5: 运行演示测试**

```bash
python3 -m unittest tests.test_ops_demo -v
```

Expected: 3 tests PASS。

- [ ] **Step 6: 手工运行三个场景**

```bash
PASS_WORKSPACE="$(mktemp -d /tmp/hermes-local-demo-pass.XXXXXX)"
python3 -m ops.demo --scenario pass --workspace "$PASS_WORKSPACE"
```

Expected: 打印“今日训练已发布”，存在当日公开 HTML。

```bash
FAIL_WORKSPACE="$(mktemp -d /tmp/hermes-local-demo-fail.XXXXXX)"
python3 -m ops.demo --scenario fail --workspace "$FAIL_WORKSPACE"
```

Expected: 退出码 2，打印失败通知，上期 HTML 保持不变，私有目录出现失败包。

```bash
RECOVER_WORKSPACE="$(mktemp -d /tmp/hermes-local-demo-recover.XXXXXX)"
python3 -m ops.demo --scenario recover --workspace "$RECOVER_WORKSPACE"
```

Expected: 先显示 `BLOCKED`，再显示 `PUBLISHED`。

- [ ] **Step 7: 提交**

```bash
git add ops/demo.py tests/test_ops_demo.py docs/operations/local-demo.md
git commit -m "feat: add local pass fail recovery demo"
```

### Task 9: 完成阶段一回归验证

**Files:**
- Create: `tests/verify_project.py`
- Modify: `docs/operations/local-demo.md`

- [ ] **Step 1: 扩展项目验证**

创建独立的 `tests/verify_project.py`，避免改变原有 Skill 验证语义：

```python
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


REQUIRED = (
    "AGENTS.md",
    "ops/models.py",
    "ops/policy.py",
    "ops/failure_package.py",
    "ops/local_publish.py",
    "ops/notifications.py",
    "ops/pipeline.py",
    "ops/demo.py",
    "templates/public-site/AGENTS.md",
)


def verify_project_root(root: Path) -> list[str]:
    return [relative for relative in REQUIRED if not (root / relative).exists()]


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    root = Path(args[0]).resolve() if args else Path(__file__).resolve().parents[1]
    missing = verify_project_root(root)
    if missing:
        print("FAIL: missing project governance files:", file=sys.stderr)
        for relative in missing:
            print(f"- {relative}", file=sys.stderr)
        return 1
    print("PASS: project governance foundation is complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: 运行全部项目测试**

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: 所有现有测试和新增测试 PASS。

- [ ] **Step 3: 运行 Skill 验证**

```bash
python3 tests/verify_hermes_skill.py skill
python3 tests/verify_project.py .
```

Expected: 两个命令均 PASS；原有 Skill 包没有因项目编排代码退坡。

- [ ] **Step 4: 运行现有失败回流校验**

```bash
python3 skill/scripts/validate_failure_feedback.py skill/references/failure-cases.md
```

Expected: PASS。

- [ ] **Step 5: 检查模拟失败没有泄漏到公开目录**

```bash
FAIL_CHECK="$(mktemp -d /tmp/hermes-public-leak-check.XXXXXX)"
python3 -m ops.demo --scenario fail --workspace "$FAIL_CHECK" || test "$?" -eq 2
find "$FAIL_CHECK/public" -type f -print
```

Expected: 只出现上一期 HTML、`current.json` 和 `status.json`；不得出现失败 Markdown、质量报告或失败包。

- [ ] **Step 6: 在演示说明记录验证证据**

添加实际命令、日期、通过数量和三个场景的最终状态。不得写“已通过”而没有真实命令结果。

- [ ] **Step 7: 最终提交**

```bash
git add tests/verify_project.py docs/operations/local-demo.md
git commit -m "test: verify governance foundation and local demo"
```

## 3. 阶段一完成定义

只有同时满足以下条件，阶段一才算完成：

- 项目已经使用 Git 管理。
- 私有控制仓库和公开站点的 `AGENTS.md` 规则已通过测试。
- 运行状态可序列化并可追踪。
- 每个门禁最多两次定向重试。
- 第三次失败会阻断发布。
- 失败包能区分用户判断、系统发现和 AI 分析。
- 失败时上一期 HTML 不被覆盖。
- 失败时只更新公开审核状态。
- 成功和失败微信文案可预览。
- 成功、失败、恢复三个演示都可重复运行。
- 原有 Skill 测试和失败回流测试全部通过。

## 4. 阶段一不证明什么

本阶段通过不代表：

- AI 已经能稳定生成 V3/V6 级 Insight。
- 独立 AI 评审标准已经有效。
- GitHub 自动发布已经可用。
- Mac mini 已经完成无人值守运行。
- 微信已经真实发送通知。
- HTML 视觉体验已经达到最终正式版。

这些结论分别由后续阶段证明。
