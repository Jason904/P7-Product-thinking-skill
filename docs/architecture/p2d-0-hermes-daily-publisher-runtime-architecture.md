# P2D-0 Hermes Daily Publisher Runtime Architecture

## 1. Purpose

This document defines the future runtime architecture for the Hermes P7+ Daily Training Publisher.

The target system is:

```text
Daily scheduled run
-> select worthwhile AI / product / open-source / industry cases
-> generate P7+ product-thinking training
-> run validators and rubric review
-> publish only if quality passes
-> produce one public Daily Site URL
-> Mac mini HermesAgent sends the URL through WeChat
-> on failure, do not publish; generate a failure package
-> MacBook Air uses badcases and feedback to improve the Skill
-> MacBook Air publishes the next stable Skill release
```

Only a public URL is required in the current target. No API is required.

This architecture separates production execution from Skill development. Mac mini runs the stable daily workflow. MacBook Air owns diagnosis, repair, release gates, and stable Skill releases.

## 2. System Roles

### Mac mini

Positioning:

```text
Production Runner / Daily Runner / WeChat Notifier
```

Responsibilities:

- Run HermesAgent on a daily schedule.
- Pull only the latest stable Hermes Skill release.
- Generate the daily training artifact.
- Run validators and rubric review.
- Publish the Daily Site URL only after quality PASS.
- Send WeChat notification.
- Generate failure packages on quality or system failure.
- Write run evidence to Ops Repo or local durable spool.
- Never modify the Skill dev branch.
- Never run unpublished development Skill versions.

### MacBook Air

Positioning:

```text
Development / Triage / Skill Release Owner
```

Responsibilities:

- Develop Hermes Skill, prompts, templates, validators, renderer, publisher, and rubric.
- Pull badcases and failure packages from Ops Repo.
- Triage human feedback.
- Decide whether a defect needs a content patch or Skill improvement.
- Run release gates before publishing a stable Skill release.
- Tag and publish stable releases consumed by Mac mini.

### HermesAgent

Positioning:

```text
Runtime orchestrator on Mac mini
```

Responsibilities:

- Resolve stable Skill version.
- Execute generation.
- Execute quality gates.
- Publish static daily page.
- Write ledgers.
- Send WeChat message.
- Package failures.
- Avoid mutating development branches or historical evidence.

### Daily Site Repo

The Daily Site Repo is the static hosting repository for public reader pages.

Example structure:

```text
daily/
  2026-07-01/
    index.html
archive/
  index.html
```

The Daily Site Repo only needs to produce public URLs. It does not need an API in the current target.

### Ops Repo

The Ops Repo is the evidence and operations repository.

It stores:

```text
runs/
failures/
human-feedback/
publish-ledger/
wechat-notification-ledger/
```

Preferred implementation:

```text
GitHub repo + GitHub Issues
```

The Ops Repo does not need a separate service.

### Skill Release Repo

The Skill Release Repo is the source of truth for durable Hermes system behavior:

```text
Hermes Skill
rubric
validators
generator
renderer
publisher
tests
release tags
changelog
```

MacBook Air owns development and stable release publication. Mac mini only consumes stable releases.

### WeChat

WeChat is a notification channel only.

It must not be treated as evidence storage, source of truth, or an operational ledger.

## 3. Daily Success Path

Success flow:

```text
Mac mini scheduler triggers HermesAgent
-> HermesAgent pulls latest stable Skill release
-> records resolved versions
-> collects source signals
-> generates training Markdown
-> renders reader HTML
-> runs deterministic validators
-> runs rubric / quality review
-> PASS
-> publishes HTML to Daily Site Repo
-> obtains public URL
-> writes run ledger and publish ledger
-> sends WeChat success message with URL
-> writes WeChat notification ledger
-> final state: PASS_PUBLISHED
```

Required success evidence:

- `run-ledger.yaml`
- `source-manifest.yaml` or `source-notes.md`
- generated training Markdown
- rendered HTML
- validator result
- reviewer output
- publish ledger with URL
- WeChat notification ledger
- resolved version fields:
  - `skill_version`
  - `rubric_version`
  - `generator_version`
  - `renderer_version`
  - `publisher_version`

Core invariant:

```text
No quality PASS, no public URL.
```

## 4. Quality Failure Path

Quality failure means generation fails, deterministic validation fails, or rubric review blocks publication.

Failure flow:

```text
generation error or quality review failure
-> do not publish
-> generate failure package
-> write failure package to Ops Repo
-> create GitHub Issue
-> send WeChat quality-blocked summary
-> MacBook Air pulls badcase
-> triage
-> fix content, prompt, template, validator, renderer, publisher, or rubric
-> run release gates
-> publish new stable Skill release when needed
```

Failure package must include at least:

```text
failure-package.yaml
reviewer-output.json
validator-result.yaml
failure-objects.json
source-manifest.yaml
source-notes.md
training-raw.md
repair-suggestion.md
run-log.md
```

Final state:

```text
REVIEW_BLOCKED
```

Publication rule:

```text
A REVIEW_BLOCKED run must not update the Daily Site or produce a public Daily Site URL.
```

The user should receive a short quality-blocked WeChat summary and an Issue link, not a low-quality or partial public reader page.

## 5. System Failure Path

System failure means the content may not be the root problem, but runtime infrastructure, permissions, dependency state, GitHub, hosting, or notification delivery failed.

| Failure | Record | Notify | Backflow | Blocks Publish |
|---|---|---|---|---|
| Mac mini offline / no network | local durable spool, later Ops sync | best-effort WeChat after recovery | Ops Issue when online | yes |
| GitHub push failure for Daily Site | local spool plus publish error log | system exception message | Ops Issue | yes |
| Pages / hosting publish failure | publish-ledger with failed stage | system exception message | Ops Issue | yes |
| WeChat send failure after publish | publish ledger plus notification failure ledger | retry or alternate alert | Ops Issue if repeated | no, URL already exists |
| dependency missing | run ledger plus environment snapshot | system exception message | Ops Issue | yes |
| permission / secret error | redacted run ledger | system exception message | Ops Issue | yes |
| Ops Repo write failure | local durable spool | system exception message if possible | sync later | depends on publish stage |

Mac mini should maintain a local durable spool:

```text
~/.hermes/daily-runs/YYYY-MM-DD/
```

System failure rule:

```text
If the public URL was not produced, final state is SYSTEM_FAILED.
If the public URL exists but WeChat failed, keep publish evidence and mark notification as failed/retryable.
```

When Ops Repo is unavailable, local spool is the temporary evidence source. The next successful network window should sync the spooled package to Ops Repo and create or update the related Issue.

## 6. Human Feedback Path

Human dissatisfaction is possible even after validators pass and the daily page is published.

Human feedback flow:

```text
PASS_PUBLISHED
-> user reads URL
-> user is not satisfied
-> record human feedback
-> final quality label becomes PASS_BUT_UNSATISFACTORY
-> triage on MacBook Air
-> decide content patch or Skill improvement
```

Repair categories:

- `content patch`: fix the specific daily page. This does not necessarily require a Skill change.
- `skill improvement`: fix the generation system, rubric, template, validator, renderer, or publisher.

Content patch flow:

```text
PASS_BUT_UNSATISFACTORY
-> content patch
-> PATCHED_BY_HUMAN
```

Skill improvement flow:

```text
PASS_BUT_UNSATISFACTORY
-> skill defect confirmed
-> SKILL_FIX_REQUIRED
-> new stable release
-> RESOLVED_IN_SKILL_RELEASE
```

Human feedback should be recorded in Ops Repo even when the fix is only a content patch, because the feedback may later reveal a recurring pattern.

## 7. State Machine

| State | Meaning | Published | WeChat Notify | Ops Repo | MacBook Air Needed |
|---|---|---:|---:|---:|---:|
| PASS_PUBLISHED | Quality passed and URL was published | yes | success URL | yes | no by default |
| REVIEW_BLOCKED | Generation completed but validator/rubric failed | no | failure reason + Issue | yes | yes |
| SYSTEM_FAILED | Runtime, infra, permission, dependency, or publish system failed | maybe | failure stage + log location | yes or local spool | yes if not auto-retryable |
| PASS_BUT_UNSATISFACTORY | Published content passed gates but user disliked quality | yes | optional feedback ack | yes | yes |
| PATCHED_BY_HUMAN | Today's page was manually corrected | yes | optional patched URL | yes | maybe |
| SKILL_FIX_REQUIRED | Root cause requires durable Skill change | maybe | issue/status update | yes | yes |
| RESOLVED_IN_SKILL_RELEASE | Fix shipped in a stable release | future runs use fix | optional release note | yes | no after verification |

Core transitions:

```text
SCHEDULED
-> GENERATED
-> REVIEWING
-> PASS_PUBLISHED

REVIEWING
-> REVIEW_BLOCKED
-> SKILL_FIX_REQUIRED
-> RESOLVED_IN_SKILL_RELEASE

PASS_PUBLISHED
-> PASS_BUT_UNSATISFACTORY
-> PATCHED_BY_HUMAN

PASS_BUT_UNSATISFACTORY
-> SKILL_FIX_REQUIRED
-> RESOLVED_IN_SKILL_RELEASE

any runtime stage
-> SYSTEM_FAILED
```

State ownership:

- Mac mini owns runtime state production and evidence capture.
- MacBook Air owns diagnosis, repair, and stable release transitions.
- Ops Repo owns durable state evidence.
- WeChat only mirrors state as a short notification.

## 8. Repository Responsibilities

Three-repo model:

```text
Skill Dev / Release Repo = system behavior
Daily Site Repo = public URL
Ops Repo = evidence, failures, feedback, ledgers
```

| Repo | Owner | Primary Contents | Runtime Role |
|---|---|---|---|
| Skill Dev / Release Repo | MacBook Air | Skill, rubric, validators, generator, renderer, publisher, tests, tags, changelog | Mac mini pulls stable release only |
| Daily Site Repo | Mac mini runtime, with MacBook Air patch authority | static daily HTML pages and archive | produces public URL |
| Ops Repo | both, with Mac mini writing runtime evidence and MacBook Air triaging | run ledgers, failure packages, feedback, issues, notification ledgers | source of operational truth |

Repository boundaries:

- Daily Site Repo should stay lightweight.
- Ops Repo should carry evidence.
- Skill Repo should carry durable system behavior.

Daily Site Repo must not become the place for failure packages, private logs, secrets, or reviewer internals. Ops Repo must not become the place for stable Skill source changes. Skill Repo must not be mutated by Mac mini during production runs.

## 9. Feedback / Badcase Loop

Badcase loop:

```text
Mac mini failure package
-> Ops Repo failure entry
-> GitHub Issue
-> MacBook Air triage
-> classify root cause
-> repair Skill / rubric / validator / renderer / publisher
-> regression test using badcase
-> changelog
-> stable release
-> Mac mini pulls release on next run
```

Human feedback loop:

```text
user feedback
-> Ops Repo human-feedback entry
-> classify as content patch or Skill improvement
-> patch current page or fix Skill
-> record final resolution
```

Root-cause categories:

- source selection failure
- fact confidence failure
- shallow reasoning
- rubric false pass
- validator gap
- renderer content loss
- publisher failure
- WeChat notification failure
- environment / permission failure

Badcases should become regression coverage when they expose durable system weakness. A one-off content patch should still leave a feedback record, but it does not automatically require a new Skill release.

## 10. Skill Release Versioning

Release rules:

- Mac mini only uses stable releases.
- Mac mini must not run local dev branch Skill code.
- MacBook Air owns dev, test, and release.
- Every daily run records:
  - `skill_version`
  - `rubric_version`
  - `generator_version`
  - `renderer_version`
  - `publisher_version`
  - release tag
  - release commit SHA
  - resolved time
- Stable release should include changelog and compatibility notes.
- Badcase fixes should add or update regression coverage before release.
- Mac mini should fetch the latest stable release at run start, verify checksum or commit SHA, then run.

Suggested release flow:

```text
MacBook Air dev branch
-> tests / gates
-> changelog
-> stable tag
-> GitHub Release
-> Mac mini fetches latest stable
-> daily run records resolved versions
```

Version evidence belongs in the run ledger and should also appear in failure packages. This allows MacBook Air to reproduce failures against the exact Skill, rubric, generator, renderer, and publisher versions used by Mac mini.

## 11. WeChat Notification Contract

WeChat messages should be short, actionable, and linked to durable evidence. Do not send full logs through WeChat.

### Success Message

```text
Hermes Daily 已发布
日期: 2026-07-01
URL: <daily_site_url>
Skill: <skill_version>
Review: PASS
```

### Quality Blocked Message

```text
Hermes Daily 质量阻断
日期: 2026-07-01
状态: REVIEW_BLOCKED
原因: <top_failure_reason>
Issue: <github_issue_url>
证据: <ops_failure_package_path>
```

### System Exception Message

```text
Hermes Daily 系统异常
日期: 2026-07-01
阶段: <failed_stage>
状态: SYSTEM_FAILED
日志: <ops_or_local_spool_path>
Issue: <github_issue_url_if_available>
```

Notification ledger should record:

- message type
- target channel
- send timestamp
- send result
- retry count
- related run id
- related URL or Issue link

## 12. Evidence and Privacy Boundaries

Evidence boundaries:

- WeChat is notification only, not evidence storage.
- Ops Repo may contain source notes, reviewer outputs, failures, and logs.
- Daily Site Repo should contain public reader pages only.
- Failure packages should not be published to Daily Site.
- If sources or user feedback contain sensitive data, store them only in private Ops Repo or local spool.

Privacy boundaries:

- Secrets, tokens, cookies, and private credentials must never be written into Ops Repo.
- Secrets, tokens, cookies, and private credentials must never be written into Daily Site Repo.
- Secrets, tokens, cookies, and private credentials must never be sent through WeChat messages.
- Permission / secret errors must be redacted before logging.

Operational boundary:

```text
Public URL = reader artifact only.
Ops evidence = private operational truth.
WeChat = short notification pointer.
Skill Release Repo = durable behavior and release history.
```

## 13. Agent Instruction Loading

The canonical repo-level agent instruction file is `AGENTS.md` at the repository root.

The primary direct audience for repo-root `AGENTS.md` is Codex and other AI coding agents working in this Hermes repository. It provides durable project guidance and operating boundaries for agent-assisted work in the repository.

Codex sessions opened from this repository should read and follow repo-root `AGENTS.md` as the default operating rules for the repository tree, unless a more specific nested `AGENTS.md` applies to the active subtree.

If future subdirectories need more specific rules, they may introduce nested `AGENTS.md` files. A nested file should apply only to its own subtree and should not silently change global Hermes runtime boundaries.

Direct system, developer, or user instructions in the active task override `AGENTS.md`.

HermesAgent is a production runtime component on Mac mini, not automatically equivalent to Codex. HermesAgent must explicitly load `AGENTS.md`, receive equivalent runtime configuration, receive equivalent prompt injection, or consume equivalent packaged stable Skill metadata before relying on these rules in production.

This distinction prevents a false assumption that placing `AGENTS.md` in the repository automatically enforces runtime behavior for non-Codex tools.

## 14. Open Questions / Decisions Needed

- Hosting target: GitHub Pages, Netlify, or another static host?
- Stable release format: GitHub Release asset, tag checkout, package archive, or internal Skill install format?
- WeChat implementation: local Mac mini client automation, webhook bridge, or third-party push service?
- Retry policy: how many retries for GitHub push, Pages deploy, and WeChat send?
- URL immutability: should patched pages overwrite the same URL or create revisioned URLs?
- Ops Repo privacy: should source notes or reviewer output ever contain sensitive data requiring redaction?
- Human feedback UX: should the user reply in WeChat, GitHub Issue, Notion, or manual repo file?
- Failure severity: which failures require immediate WeChat alert versus next-day digest?

## 15. Next Stage Recommendation

Recommended next stage: P2D-1 Mac mini Daily Runner Design.

P2D-1 should start only after this P2D-0 architecture doc and AGENTS.md rules are reviewed and accepted.
