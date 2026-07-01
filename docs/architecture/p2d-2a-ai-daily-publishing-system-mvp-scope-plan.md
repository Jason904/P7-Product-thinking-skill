# P2D-2a AI Daily Publishing System MVP Scope Plan

Status: `P2D-2a_MVP_SCOPE_PLAN`

This is a documentation-only MVP scope plan. It defines the first implementation cut for the AI Daily Publishing System; it does not implement runtime code, Adapters, evaluators, publishers, notifiers, schedulers, deployment, or external service calls.

Source of truth:

- `docs/architecture/p2d-1-ai-daily-publishing-system-context-pack-r2.md`
- `docs/architecture/p2d-1-ai-daily-publishing-system-core-and-adapter-architecture.md`

Historical boundary reference:

- `docs/architecture/p2d-0-hermes-daily-publisher-runtime-architecture.md`

P2D-1 is authoritative for naming, system positioning, Core / Adapter boundary, Hermes boundary, runtime context, gates, artifacts, repository boundary, and state model. P2D-0 is historical context only. If P2D-0 conflicts with P2D-1, P2D-1 wins.

---

## 1. MVP Goal

The first MVP is not a complete production system. It is the smallest auditable vertical loop for the AI Daily Publishing System.

MVP positioning:

```text
manual / local / noop-first MVP
```

The MVP validates that the system can run its core governance loop without live external services:

- runtime context is complete;
- local runtime profile can be loaded;
- Adapter preflight can block unsafe configuration;
- artifact contracts can be written;
- Daily Publish Gate can decide publish / no-publish;
- reader HTML can be generated as a local artifact;
- noop publisher can complete without fabricating a public URL;
- failure package can be generated;
- badcase record can be created;
- iteration ledger and lessons learned can be referenced;
- public / private evidence boundaries can be enforced.

The core invariant remains:

```text
No quality PASS, no public URL.
```

This invariant is not weakened by local mode, noop mode, manual inputs, review stubs, or lack of a real publisher.

Noop semantics:

- `NOOP_COMPLETED` means the declared local / noop runtime path completed.
- `NOOP_COMPLETED` is not equivalent to `PASS_PUBLISHED`.
- noop mode must not create, fake, reserve, or imply a real public URL.
- `public_url` must remain `null`.
- local preview paths and noop references may be recorded separately from `public_url`.

---

## 2. MVP In Scope

The MVP implements the minimum local / manual / noop loop while preserving real contracts and future extension points.

1. Runtime Context Contract: required run evidence with `run_id`, `run_date`, trigger metadata, `agent_driver`, `runtime_host`, `runtime_profile`, timezone, mode, attempt, `idempotency_key`, stable release reference, and `config_snapshot_hash`.
2. Local Runtime Profile: explicit profile selecting local manual source, local artifact sink, noop publisher, noop notification, no live model provider, deterministic validation, and review stub contracts.
3. Adapter Contract Skeleton: common contract fields for Adapter identity, type, enablement, provider, version, credentials, capabilities, inputs, outputs, failure modes, preflight, noop support, redaction, evidence policy, and public output policy.
4. Credential / Config Preflight: Adapter Configuration Gate checks selected profile and blocks missing, invalid, unsafe, or real-without-credentials configuration before retrieval, generation, render, publish, or notification.
5. Local / Manual Source Adapter: first Source Adapter behavior is local manual source input, normalized into `source-manifest.yaml` and private `source-notes.md`.
6. Markdown Report Artifact Contract: `training-report.md` is the canonical Markdown report artifact; MVP may use local or manual content but must record validation and hashes.
7. Source Notes Artifact Contract: `source-notes.md` is private evidence by default and must not enter public output unless explicitly approved by public artifact policy.
8. Reader HTML Local Render Artifact: `reader.html` is generated locally as a reader artifact, not as a deployed public page.
9. Deterministic Validator Skeleton: minimal non-AI checks for required artifacts, non-empty Markdown / HTML, artifact hashes, no private evidence markers in HTML, and `public_url: null` in noop mode.
10. Minimal Rubric Review Stub / Contract: `rubric-review.stub.json` or `rubric-review.json` with explicit `PASS`, `BLOCKED`, or `NOT_RUN`.
11. Minimal Audit Review Stub / Contract: `audit-review.stub.json` or `audit-review.json` with explicit `PASS`, `BLOCKED`, or `NOT_RUN`.
12. Daily Publish Gate Decision: real MVP hard gate that blocks unless sources, Markdown, HTML, validators, rubric review, audit review, evidence, risk flags, and privacy boundary all pass.
13. Noop Publisher Adapter: records skipped external deployment after `PUBLISH_ALLOWED`; writes `public_url: null`, `public_url_created: false`, and separate local preview / noop reference fields.
14. Noop Notification Adapter: records notification intent without sending IM, WeChat, Slack, Telegram, Email, or any other external message.
15. Evidence Ledger: records runtime context, profile, preflight result, artifact paths / hashes, validator result, review results, gate decision, publish result, notification result, failures, and badcases.
16. Failure Package: redacted `failure-package.yaml` for blocked or failed runs, with terminal state, failed gate / Adapter, missing artifacts, evidence pointers, and recommended next action.
17. Badcase Record: local `badcase-record.yaml` for `REVIEW_BLOCKED`, `SYSTEM_FAILED`, `ADAPTER_FAILED`, persistent or user-reported `CONFIG_BLOCKED`, and later `PASS_BUT_UNSATISFACTORY`.
18. Idempotency Key: derived from run date, runtime profile, stable release version, source manifest hash, training report hash, and publish target / noop publish target.
19. Repository Boundary Enforcement: classify public candidate artifacts separately from private evidence and source / behavior artifacts.
20. State Transitions: record MVP runtime states and keep `PASS_PUBLISHED` contract-only until real public deployment exists.

Review stub rule:

- rubric-review stub and audit-review stub are gate inputs, not default PASS switches.
- File presence alone is not a PASS.
- Missing, ambiguous, `NOT_RUN`, or `BLOCKED` review status blocks Daily Publish Gate.

---

## 3. MVP Out of Scope

The following are not rejected; they are intentionally deferred from the first MVP and preserved through contracts, noop behavior, local artifacts, or future milestones:

- real Web search;
- real GitHub search;
- real RSS ingestion;
- real Notion integration;
- real GitHub Pages deploy;
- real Netlify / Vercel / Cloudflare Pages deploy;
- real WeChat / Slack / Telegram / Email notification;
- live LLM calls;
- external API calls;
- complex multi-model routing;
- complex AI evaluator;
- complex independent audit agent;
- automatic badcase issue creation;
- automatic regression suite execution;
- full golden set;
- production scheduler;
- multi-user dashboard;
- public API;
- database-backed Ops backend;
- complete SaaS product.

MVP does not depend on real external services. It validates the Core governance loop before adding provider complexity.

---

## 4. MVP Architecture Cut

| Capability | MVP Decision | Reason | Artifact / Contract | Deferred Risk |
|---|---|---|---|---|
| System naming as AI Daily Publishing System | Implement in MVP | Prevent agent, host, model, or channel naming regression | Documented naming boundary | Hermes naming regression |
| Runtime Context Contract | Implement in MVP | Every run needs reproducible context | `runtime-context.yaml` | Later schedulers may emit incomplete context |
| Local Runtime Profile | Implement in MVP | MVP behavior must be explicit | profile contract and config hash | Silent fallback behavior |
| Adapter Contract Skeleton | Implement in MVP | Preserve replaceability without weakening Core | Adapter contract schema | Adapter explosion |
| Adapter Configuration Gate | Implement in MVP | Missing config must block before side effects | `adapter-preflight-result.yaml` | Credential leakage or unsafe fallback |
| Model Provider Adapter | Contract Only in MVP | No live LLM calls in first cut | `ModelProviderAdapter`, `ModelRoleBinding`, optional no-call trace | Integration assumptions untested |
| Source Adapter | Implement local manual in MVP | Proves source contract without external search | `source-manifest.yaml`, `source-notes.md` | Freshness and retrieval complexity deferred |
| Web / GitHub / RSS / Notion source providers | Defer After MVP | External retrieval expands credentials and scope | future Source Adapter contracts | Real source variability untested |
| Markdown Report Artifact | Implement in MVP | Canonical report precedes render and gate | `training-report.md` | Generation quality remains manual/local |
| Reader HTML Local Render | Implement in MVP | Delivery target is reader HTML, but no deployment yet | `reader.html` | Hosting and browser edge cases deferred |
| Deterministic Validator | Implement skeleton in MVP | Gate needs non-AI checks first | `validator-result.yaml` | Initial validator coverage narrow |
| Rubric Review | Contract Only in MVP | No live evaluator in first cut | `rubric-review.stub.json` or `rubric-review.json` | Stub misuse as fake PASS |
| Audit Review | Contract Only in MVP | Full audit agent is post-MVP | `audit-review.stub.json` or `audit-review.json` | Audit depth deferred |
| Daily Publish Gate | Implement in MVP | Core invariant must be real from day one | gate decision in ledgers | Gate bypass invalidates MVP |
| Publisher Adapter | Implement noop in MVP | Proves publish boundary without deployment | `publish-ledger.yaml` with `public_url: null` | Real deploy failures deferred |
| Real hosting providers | Defer After MVP | They require credentials and public side effects | future Publisher Adapter contracts | Deployment behavior untested |
| Notification Adapter | Implement noop in MVP | Records intent without external send | `notification-ledger.yaml` | Delivery failures deferred |
| Real IM / Email channels | Defer After MVP | External messages can leak private evidence | future Notification Adapter contracts | Channel payload constraints deferred |
| Artifact Sink Adapter | Implement local file sink in MVP | Local evidence is sufficient for first audit loop | local artifact sink contract | Remote durability deferred |
| Ops / Feedback Adapter | Implement local failure and badcase first | Governance loop must exist before external Ops | `failure-package.yaml`, `badcase-record.yaml` | Threaded triage deferred |
| Evidence Ledger | Implement in MVP | MVP success is auditability | `run-ledger.yaml`, `artifact-hash.yaml` | Evidence incompleteness |
| Failure Package | Implement in MVP | Blocked and failed runs must be useful | `failure-package.yaml` | Repair automation deferred |
| Badcase Record | Implement in MVP | Failures must feed iteration memory | `badcase-record.yaml` | Regression replay deferred |
| Iteration Ledger / Lessons Learned references | Contract Only in MVP | Link future learning without building release governance | ledger references | Learning loop remains manual |
| Human Patch Gate | Contract Only in MVP | Patch governance matters but is not first loop | states and gate contract | Patch ambiguity |
| Stable Release Gate | Defer After MVP | Requires regression and golden set evidence | future release gate contract | Premature stable release claims |
| Production Scheduler | Defer After MVP | Triggering is outside Core | runtime trigger fields | Schedule drift untested |
| Public API / Dashboard / DB backend | Defer After MVP | Current target is URL-first reader output | future product surface notes | SaaS scope creep |

---

## 5. Adapter MVP Strategy

| Adapter | MVP Behavior | Required Config | Credential Handling | Failure Behavior | Future Upgrade Path |
|---|---|---|---|---|---|
| Model Provider Adapter | Contract only; no generation, eval, audit, repair, summarization, live LLM, or external API call | roles disabled, noop, manual, or not configured; real provider only as blocked config | no credential values read, printed, stored, or copied; real provider without required config is `CONFIG_BLOCKED` | attempted live call in MVP is policy failure; malformed contract blocks | provider-specific model Adapters, role binding, model traces, model governance |
| Source Adapter | local manual source first | local source path or manual source identifier, source type, freshness note, selection reason, citation permission | no external credential for local source; real source provider without credentials blocks | missing local input blocks or review-blocks depending on stage; malformed source manifest review-blocks | Web, GitHub, RSS, official-site, Notion source Adapters |
| Publisher Adapter | noop publisher only after `PUBLISH_ALLOWED`; no external deployment | `mode: noop`, local preview policy, noop reference policy, idempotency target | no deployment token in noop; real publisher without credentials blocks | publisher must not run before `PUBLISH_ALLOWED`; non-null noop `public_url` blocks | GitHub Pages, Netlify, Vercel, Cloudflare Pages, patch / duplicate URL policy |
| Notification Adapter | noop notification only; records intent; sends nothing | `mode: noop` or `none`, intent type, evidence pointer policy | no webhook or bot token in noop; real channel without credentials blocks | attempted real send in MVP is policy failure | WeChat, Slack, Telegram, Email Adapters with redaction and payload policy |
| Artifact Sink Adapter | local file sink first; records paths and hashes | local artifact root, run / failure / badcase path templates, classification policy | local permission only; remote sink credentials deferred | write failure is `SYSTEM_FAILED`; classification conflict blocks or fails | Git repo, private Ops repo, Notion, object storage |
| Ops / Feedback Adapter | local failure package and badcase only | local failure path, badcase path, run-to-badcase link, redaction policy | no external credentials; external Ops backend without credentials blocks | failure / badcase write failure is `SYSTEM_FAILED`; unredacted secret must not be promoted | GitHub Issues, Notion database, Linear, threaded feedback, automated regression linkage |

---

## 6. Gate MVP Strategy

| Gate | MVP Type | MVP Behavior | Blocking State | Deferred Upgrade |
|---|---|---|---|---|
| Adapter Configuration Gate | MVP hard gate | Preflight selected profile and Adapters before runtime work | `CONFIG_BLOCKED` | reachability, quota, permission-scope checks |
| Daily Publish Gate | MVP hard gate | Decide publish eligibility from sources, artifacts, validators, rubric stub, audit stub, evidence, risk, and privacy checks | `REVIEW_BLOCKED` | full evaluator, full audit agent, richer source quality checks |
| Human Patch Gate | MVP manual / contract gate | Preserve states and evidence requirements; no patch tooling yet | `PATCHED_BY_HUMAN` or `SKILL_FIX_REQUIRED` | patch workflow and feedback tooling |
| Stable Release Gate | Deferred gate | Contract language only; no release governance execution | future `STABLE_RELEASE_HELD` | golden set, regression suite, badcase replay |

Adapter Configuration Gate must block before retrieval, generation, rendering, publish, notification, or external calls if selected Adapters are missing required configuration, missing required noop support, or unsafe for the MVP profile.

Daily Publish Gate must be real even though the Publisher Adapter is noop. Passing this gate means the local artifact is eligible for a publish attempt; in MVP the attempt is noop and still must not create a public URL.

Daily Publish Gate passes only when:

```text
required sources present
training-report.md present
reader.html present
validator-result PASS
rubric-review explicit PASS
audit-review explicit PASS
required evidence complete
no blocking risk flag
no private evidence leak
noop publish public_url remains null
```

Human Patch Gate remains manual / contract-only. Human patch authority must never override failed validator, rubric, audit, evidence, credential, or privacy checks.

Stable Release Gate is deferred. MVP completion does not imply stable release readiness.

---

## 7. Artifact MVP Strategy

The MVP is evidence-first. Every terminal outcome should be explainable from durable local artifacts.

Successful local/noop run must produce:

```text
run-ledger.yaml
runtime-context.yaml
adapter-preflight-result.yaml
source-manifest.yaml
source-notes.md
training-report.md
reader.html
validator-result.yaml
rubric-review.stub.json or rubric-review.json
audit-review.stub.json or audit-review.json
publish-ledger.yaml
notification-ledger.yaml
artifact-hash.yaml
```

The successful local/noop terminal state is:

```text
NOOP_COMPLETED
```

not:

```text
PASS_PUBLISHED
```

`publish-ledger.yaml` must record:

```yaml
public_url: null
public_url_created: false
mode: noop
```

Failed or blocked runs must produce:

```text
run-ledger.yaml
runtime-context.yaml
adapter-preflight-result.yaml
failure-package.yaml
artifact-hash.yaml
```

When available by stage, failed or blocked runs should also include:

```text
source-manifest.yaml
source-notes.md
training-report.md
reader.html
validator-result.yaml
rubric-review.stub.json or rubric-review.json
audit-review.stub.json or audit-review.json
publish-ledger.yaml
notification-ledger.yaml
badcase-record.yaml
```

Artifacts that may be stubs in MVP:

- `rubric-review.stub.json`;
- `audit-review.stub.json`;
- `model-run-trace.yaml`;
- iteration ledger reference;
- lessons learned reference.

Stub rules:

- stubs identify themselves as stubs;
- stubs contain explicit status;
- stubs do not imply PASS by existence;
- stubs are consumed by gates as evidence inputs;
- missing, `NOT_RUN`, ambiguous, or `BLOCKED` required review blocks publication eligibility.

Artifacts that must not enter public output:

- source notes;
- validator results;
- rubric reviews;
- audit reviews;
- publish and notification ledgers;
- failure packages;
- badcase records;
- model traces;
- runtime logs;
- environment snapshots;
- credential errors;
- repair suggestions;
- private feedback entries.

Public candidates are limited to `reader.html`, safe public static assets, and a future real public URL only after a real Publisher Adapter succeeds.

---

## 8. State Machine MVP Strategy

MVP runtime states:

```text
SCHEDULED_OR_STARTED
CONFIG_BLOCKED
RETRIEVING
GENERATING
RENDERING
VALIDATING
EVALUATING
AUDITING
PUBLISH_ALLOWED
REVIEW_BLOCKED
SYSTEM_FAILED
ADAPTER_FAILED
NOOP_COMPLETED
BADCASE_CREATED
```

Successful local/noop path:

```text
SCHEDULED_OR_STARTED -> RETRIEVING -> GENERATING -> RENDERING -> VALIDATING -> EVALUATING -> AUDITING -> PUBLISH_ALLOWED -> NOOP_COMPLETED
```

Config blocked path:

```text
SCHEDULED_OR_STARTED -> CONFIG_BLOCKED
```

Quality blocked path:

```text
SCHEDULED_OR_STARTED -> RETRIEVING -> GENERATING -> RENDERING -> VALIDATING -> EVALUATING -> AUDITING -> REVIEW_BLOCKED -> BADCASE_CREATED
```

Runtime or Adapter failure path:

```text
any runtime stage -> SYSTEM_FAILED -> BADCASE_CREATED
any adapter stage -> ADAPTER_FAILED -> BADCASE_CREATED
```

`CONFIG_BLOCKED` creates `BADCASE_CREATED` only when persistent or user-reported.

MVP contract-only state:

- `PASS_PUBLISHED` is contract-only until a real Publisher Adapter deploys approved HTML and records a real public URL.
- MVP must not map `NOOP_COMPLETED` to `PASS_PUBLISHED`.

MVP governance states available as manual or contract references:

```text
PASS_BUT_UNSATISFACTORY
PATCHED_BY_HUMAN
SKILL_FIX_REQUIRED
```

Post-MVP release governance states:

```text
TRIAGE_IN_PROGRESS
FIX_IN_PROGRESS
REGRESSION_TESTING
STABLE_RELEASE_CANDIDATE
STABLE_RELEASE_APPROVED
STABLE_RELEASE_HELD
RESOLVED_IN_STABLE_RELEASE
```

---

## 9. Folder / File Plan

This is a future implementation layout recommendation only. P2D-2a does not create these directories or files.

Suggested future source layout:

```text
src/
  ai_daily_publishing_system/
    core/
    adapters/
    contracts/
    artifacts/
    gates/
    state/
    rendering/
    validation/
```

Suggested future documentation layout:

```text
docs/
  architecture/
  governance/
  evals/
```

Suggested future runtime layout:

```text
runtime/
  profiles/
  examples/
```

Suggested future artifact layout:

```text
artifacts/
  runs/
  failures/
  badcases/
```

Suggested future test layout:

```text
tests/
  contracts/
  gates/
  artifacts/
  state/
```

P2D-2a creates none of these planned directories or files. The only allowed repository change in this task is this planning document.

---

## 10. MVP Milestones

| Milestone | Goal | Scope | Non-goals | Output | Acceptance Criteria |
|---|---|---|---|---|---|
| P2D-2b Runtime Contract and Artifact Schema Plan | Freeze runtime context and artifact schemas | runtime context, ledgers, preflight, publish / notification ledgers, failure package, badcase record | runtime implementation, external services, live model calls | plan or schema target | required artifacts have fields, classification, and terminal-state obligations |
| P2D-2c Local Noop Runtime Plan | Define local/manual/noop execution flow | local profile, manual source, noop publisher, noop notification, local sink | real publisher, real notification, scheduler | plan or implementation target | flow can run locally without external credentials or calls |
| P2D-2d Gate and State Machine Plan | Specify gate logic and transitions | Adapter Configuration Gate, Daily Publish Gate, review stubs, state transitions | full evaluator, full audit, stable release implementation | plan or implementation target | Daily Publish Gate hard, stubs not default PASS, `NOOP_COMPLETED != PASS_PUBLISHED` |
| P2D-2e Local Artifact and Failure Package Plan | Define local evidence persistence | artifact paths, hashes, failure package, badcase, redaction checks | remote Ops, issue creation, Notion | plan or implementation target | success, blocked, and failed runs leave auditable local evidence |
| P2D-2f Minimal HTML Render and Noop Publish Plan | Define local reader render and noop publish ledger | Markdown to `reader.html`, validators, noop publish result | real URL, real deploy, hosting integration | plan or implementation target | `reader.html` can be produced; noop publish keeps `public_url: null` |
| P2D-2g Badcase / Iteration Memory Plan | Define failure-to-learning loop | badcase schema, failure links, iteration ledger refs, lessons learned refs | automatic regression execution, full release workflow | plan or implementation target | governed failures can be traced to future repair and regression planning |
| P2D-2h MVP Implementation Readiness Review | Decide whether MVP implementation can start | review P2D-2b through P2D-2g for consistency, scope, and safety | writing runtime code during review, external integrations | readiness review document | no unresolved scope conflict; safety boundary preserved; implementation tasks are small |

---

## 11. Risk and Scope Control

| Risk | Why It Matters | MVP Control |
|---|---|---|
| Adapter explosion | Too many provider-specific paths obscure the Core contract | local-first, noop-first, contract-first |
| Credential leakage | Real providers require tokens, webhooks, and deploy keys | no live external calls, redacted preflight evidence only |
| Gate bypass | Noop mode could be mistaken for skipping quality gates | Daily Publish Gate is MVP hard gate |
| Fake production | Local HTML or noop references could be mislabeled as public delivery | `public_url: null`, `NOOP_COMPLETED != PASS_PUBLISHED` |
| Eval overbuild | Complex evaluator before artifacts and gates stabilizes expands scope | deterministic validator first, review contracts first |
| Badcase governance underbuild | Happy path without learning loop is not auditable | failure package and badcase record are in scope |
| Public/private evidence mix-up | Private review, source, trace, or credential evidence could leak | artifact classification and public/private boundary checks |
| Mac mini / system identity confusion | Host could be mistaken for product system | AI Daily Publishing System is system; Mac mini is reference runtime host |
| Hermes naming regression | External agent could be written back as system identity | Hermes / Codex / Claude Code / OpenClaw are External AI Agent Drivers |
| Too many real external dependencies | Search, LLM, hosting, notification, and Ops integrations make MVP fragile | no live LLM, no external API, no real deploy, no real notification |

MVP control principles:

```text
local-first
noop-first
contract-first
evidence-first
gate-first
no live external calls
no real publish
```

---

## 12. Definition of Done

P2D-2a is done when this planning document clearly defines:

- MVP total goal;
- MVP In Scope;
- MVP Out of Scope;
- Implement / Contract Only / Defer architecture cut;
- Adapter MVP strategy;
- Gate MVP strategy;
- Artifact MVP strategy;
- State Machine MVP strategy;
- folder / file plan without creating planned directories;
- P2D-2b through P2D-2h milestones;
- risk and scope controls;
- safety boundary.

P2D-2a is not done by implementing runtime capability. It is done by freezing the MVP scope boundary so later implementation phases remain small and auditable.

---

## 13. Safety Boundary

This P2D-2a task is documentation only.

Allowed:

- read repository documentation;
- create this planning document;
- run `git status`;
- run `git diff`;
- inspect this document.

Forbidden:

- writing code;
- adding scripts;
- creating `src/`, `runtime/`, or `artifacts/` directories;
- implementing runtime behavior;
- implementing Adapters;
- implementing evaluator behavior;
- implementing publisher behavior;
- implementing notifier behavior;
- calling live LLMs;
- calling external APIs;
- deploying;
- publishing;
- generating a real public URL;
- sending IM, WeChat, Slack, Telegram, or Email notifications;
- modifying P2C outputs;
- modifying P2C ledgers;
- modifying source package files;
- modifying `AGENTS.md`;
- modifying P2D-0 documents;
- modifying P2D-1 documents;
- running `git add`;
- committing;
- pushing.

The only allowed repository change for P2D-2a is:

```text
docs/architecture/p2d-2a-ai-daily-publishing-system-mvp-scope-plan.md
```
