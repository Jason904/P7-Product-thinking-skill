# P2D-2b AI Daily Publishing System Runtime Contract and Artifact Schema Plan

Status: `P2D-2b_RUNTIME_CONTRACT_AND_ARTIFACT_SCHEMA_PLAN`

This is a documentation-only schema and contract plan for the first MVP of the
AI Daily Publishing System. It defines runtime contracts, artifact schemas,
ledger schemas, failure and badcase schemas, artifact classification rules,
terminal state obligations, and schema acceptance cases.

Source of truth:

- `docs/architecture/p2d-1-ai-daily-publishing-system-context-pack-r2.md`
- `docs/architecture/p2d-1-ai-daily-publishing-system-core-and-adapter-architecture.md`
- `docs/architecture/p2d-2a-ai-daily-publishing-system-mvp-scope-plan.md`

P2D-1 remains authoritative for system architecture, Core / Adapter boundaries,
gate semantics, public / private artifact boundaries, repository boundaries, and
state naming. P2D-2a remains authoritative for MVP scope:

```text
manual / local / noop-first MVP
```

P2D-2b must not expand that scope.

---

## 1. P2D-2b Goal

P2D-2b freezes the MVP runtime contract and artifact schema surface needed by
later local / manual / noop implementation stages.

P2D-2b defines:

- Runtime Context Contract.
- Runtime Profile Snapshot Schema.
- Adapter Preflight Result Schema.
- Source Manifest Schema.
- Source Notes Contract.
- Training Report Contract.
- Reader HTML Contract.
- Validator Result Schema.
- Rubric Review Stub Schema.
- Audit Review Stub Schema.
- Publish Ledger Schema.
- Notification Ledger Schema.
- Run Ledger Schema.
- Artifact Hash Schema.
- Failure Package Schema.
- Badcase Record Schema.
- Artifact classification rules.
- Terminal state artifact obligations.
- Schema acceptance cases.

P2D-2b only defines schemas, contracts, and acceptance cases. It does not
implement runtime behavior, create schema files, create artifact examples, create
runtime directories, create artifact directories, call external services, publish,
or notify.

The core invariant is unchanged:

```text
No quality PASS, no public URL.
```

MVP noop semantics are unchanged:

```text
NOOP_COMPLETED != PASS_PUBLISHED
public_url: null
public_url_created: false
```

---

## 2. Runtime Context Schema: `runtime-context.yaml`

Recommended schema:

```yaml
runtime_context:
  run_id:
  run_date:
  triggered_at:
  trigger_type:
  trigger_source:
  agent_driver:
  runtime_host:
  runtime_profile:
  timezone:
  mode:
    publish:
    notification:
    eval:
  attempt:
  idempotency_key:
  stable_release_version:
  stable_release_commit:
  config_snapshot_hash:
```

Field rules:

| Field | Required | Provider | Ledger / Hash Rule | Secret Rule |
|---|---:|---|---|---|
| `run_id` | yes | External runtime or Core at run start | Required in run ledger and all artifacts | Must not encode secrets |
| `run_date` | yes | External runtime | Required in ledger; idempotency input | Date only; no secret material |
| `triggered_at` | yes | External runtime | Required in ledger | Timestamp only |
| `trigger_type` | yes | External runtime | Required in ledger | Allowed values include `manual`, `scheduled`, `retry`, `dry_run`, `noop_publish`, `external_agent` |
| `trigger_source` | yes | External runtime | Required in ledger | Redact private caller payloads |
| `agent_driver` | yes | External runtime | Required in ledger | Identity only; no prompt or token |
| `runtime_host` | yes | External runtime | Required in ledger | Host label only; no local secrets |
| `runtime_profile` | yes | External runtime / config loader | Required in ledger; idempotency input through profile snapshot | Profile name only |
| `timezone` | yes | External runtime | Required in ledger | No secrets |
| `mode.publish` | yes | External runtime / profile | Required in ledger; idempotency input through profile snapshot | MVP default `noop` |
| `mode.notification` | yes | External runtime / profile | Required in ledger | MVP default `noop` or `none` |
| `mode.eval` | yes | External runtime / profile | Required in ledger | MVP default `noop` or manual review stub mode |
| `attempt` | yes | External runtime or Core | Required in ledger | Attempt counter only |
| `idempotency_key` | yes | Core | Required in ledger and publish ledger | Hash only; no raw secrets |
| `stable_release_version` | yes | External runtime / release resolver | Required in ledger; idempotency input | Version string only |
| `stable_release_commit` | yes | External runtime / release resolver | Required in ledger | Commit hash only |
| `config_snapshot_hash` | yes | Core after profile snapshot | Required in ledger; idempotency input | Hash only |

Required by ledger close:

```text
all fields in runtime_context
```

Optional extension fields are allowed only under a future explicit namespace,
for example `runtime_context.extensions`, and must not affect MVP gate behavior.

Runtime context must never contain:

- API keys.
- Tokens.
- Cookies.
- Webhooks.
- Secret values.
- Full prompt traces.
- Raw model inputs or outputs.
- Private source notes.
- Credential values.

Idempotency inputs for the MVP are:

```text
run_date
runtime_profile_snapshot.profile_name
runtime_profile_snapshot.profile_version
stable_release_version
config_snapshot_hash
source_manifest_hash
training_report_hash
publish target or noop publish target
```

---

## 3. Runtime Profile Snapshot Schema

The runtime profile snapshot freezes the effective runtime configuration that
was selected for the run. It is evidence, not executable configuration.

Recommended schema:

```yaml
runtime_profile_snapshot:
  profile_name:
  profile_version:
  profile_mode:
  source_adapter:
    adapter_id:
    mode:
    enabled:
    required:
  model_provider:
    adapter_id:
    mode:
    enabled:
    required:
  publisher:
    adapter_id:
    mode:
    enabled:
    required:
  notification:
    adapter_id:
    mode:
    enabled:
    required:
  artifact_sink:
    adapter_id:
    mode:
    enabled:
    required:
  ops_backend:
    adapter_id:
    mode:
    enabled:
    required:
  gates:
    adapter_configuration_gate:
    daily_publish_gate:
    human_patch_gate:
    stable_release_gate:
  review_mode:
    rubric:
    audit:
  noop_policy:
    publish_noop_required:
    notification_noop_or_none_required:
    public_url_must_be_null:
    public_url_created_must_be_false:
  credential_policy:
    credential_values_allowed:
    missing_credential_names_allowed:
    real_provider_without_credentials:
```

MVP default:

```yaml
runtime_profile_snapshot:
  profile_name: local-manual-noop
  profile_mode: manual_local_noop
```

MVP rules:

- Source adapter is local / manual first.
- Model provider is disabled, manual, stub, or contract-only.
- Publisher is noop.
- Notification is noop or none.
- Artifact sink is local.
- Ops backend is local.
- Rubric and audit are explicit stub or manual review contracts.
- Real providers in MVP must be disabled or produce `CONFIG_BLOCKED`.
- Real provider credential values must never appear in the snapshot.

The snapshot must enter:

- `run-ledger.yaml`.
- `artifact-hash.yaml`.
- `config_snapshot_hash`.
- Idempotency key calculation through `config_snapshot_hash`.

---

## 4. Adapter Preflight Result Schema: `adapter-preflight-result.yaml`

Recommended schema:

```yaml
adapter_preflight_result:
  run_id:
  status: PASS | BLOCKED
  checked_at:
  profile_name:
  adapters:
    - adapter_id:
      adapter_type:
      enabled:
      required:
      mode:
      credential_status:
      capability_status:
      noop_supported:
      result:
      reason_codes:
      redacted_message:
  blocking_adapters:
  public_url_created:
```

Field rules:

- `status` is required and must be `PASS` or `BLOCKED`.
- `credential_status` may be `not_required`, `present`, `missing`, `invalid`,
  `insufficient`, `disabled`, or `not_checked`.
- `capability_status` may be `supported`, `unsupported`, `disabled`,
  `not_required`, or `not_checked`.
- `result` must be `PASS`, `BLOCKED`, or `SKIPPED`.
- `reason_codes` must use stable identifiers, for example
  `MISSING_CREDENTIAL_NAME`, `REAL_PROVIDER_DISABLED_IN_MVP`,
  `NOOP_NOT_SUPPORTED`, `UNSAFE_REAL_PROVIDER_IN_MVP`.
- `blocking_adapters` lists only adapter ids and reason codes.
- `public_url_created` must be `false` for every preflight result.

Credential boundary:

- Credential values must never appear.
- Missing credential names may appear.
- Redacted error messages may appear.
- Provider tokens, webhooks, cookies, and secret-derived values must not appear.

State mapping:

```text
adapter_preflight_result.status == BLOCKED -> CONFIG_BLOCKED
```

`CONFIG_BLOCKED` occurs before retrieval, generation, rendering, publish, or
notification.

---

## 5. Source Manifest Schema: `source-manifest.yaml`

Recommended schema:

```yaml
source_manifest:
  run_id:
  source_mode:
  source_items:
    - source_id:
      source_type:
      title:
      uri:
      local_path:
      retrieval_time:
      freshness:
      authority:
      citation_allowed:
      selection_reason:
      risk_flags:
  source_manifest_hash:
```

MVP rules:

- `source_mode` is `local_manual` by default.
- `source_items` must be non-empty for a successful local / noop run.
- `uri` is optional for local-only sources.
- `local_path` is optional for URI-only future sources, but MVP local/manual
  sources should identify the local evidence pointer when available.
- `citation_allowed` must be explicit.
- `risk_flags` must be explicit, even when empty.
- `source_manifest_hash` is required before Daily Publish Gate can pass.

The source manifest is gate evidence. Missing `source-manifest.yaml` produces
`REVIEW_BLOCKED`, not a silent default.

---

## 6. Source Notes Contract: `source-notes.md`

`source-notes.md` stores private evidence used by the run. It may contain
working notes, source excerpts, selection notes, unresolved source caveats, and
private reviewer context.

Rules:

- `source-notes.md` is private evidence by default.
- It must not be copied into `reader.html`.
- It must not be published.
- It must not enter notification payloads.
- It must not be treated as a reader-facing citation list.
- It may be referenced by private evidence pointers.
- It may be absent only when the terminal state records the stage as skipped or
  absent before source collection.

If `reader.html` contains a private source notes marker or source-notes content,
Daily Publish Gate must block with `REVIEW_BLOCKED`.

---

## 7. Training Report Contract: `training-report.md`

`training-report.md` is the canonical Markdown report artifact.

Minimum content requirements:

```text
title
date
summary
main content
source references or private source evidence refs
MVP metadata block or metadata reference
```

Rules:

- The file must be non-empty for a successful run.
- The title and date must be reader-appropriate.
- The summary must be public-safe if rendered into `reader.html`.
- The main content must be valid enough Markdown for local rendering.
- Source references may be public citations only when `citation_allowed` permits.
- Private source evidence refs may point to private evidence without exposing the
  private evidence itself.
- Credential values, model traces, private audit internals, and private ledgers
  must not appear.
- `training_report_hash` is an idempotency input.

---

## 8. Reader HTML Contract: `reader.html`

`reader.html` is the local reader preview artifact for the MVP. It is not a
deployed public page and must not be described as a real public URL.

Minimum content requirements:

```text
safe rendered Markdown content
public-facing title
public-facing summary
no secrets
no source notes
no rubric internals
no audit internals
no model trace
no private ledgers
```

Rules:

- The file must be non-empty for a successful run.
- It must be renderable enough for local preview.
- It may contain only public-safe report content and public-safe static assets.
- It must not contain credential values, private source notes, model traces,
  raw review outputs, audit internals, failure package content, badcase triage,
  runtime logs, or private ledgers.
- In MVP, `reader.html` can be referenced by `local_preview_path`.
- In MVP, `reader.html` does not imply `public_url`.

---

## 9. Validator Result Schema: `validator-result.yaml`

Recommended schema:

```yaml
validator_result:
  run_id:
  status: PASS | BLOCKED
  checked_at:
  checks:
    - check_id:
      status:
      severity:
      evidence:
      reason_code:
  blocking_checks:
  public_private_boundary_pass:
  artifact_integrity_pass:
```

Minimum MVP checks:

| Check | Blocking | Expected Evidence |
|---|---:|---|
| Required artifact exists | yes | Required artifact path list |
| Markdown non-empty | yes | `training-report.md` path and size/hash |
| HTML non-empty | yes | `reader.html` path and size/hash |
| HTML renderable enough for local preview | yes | Local render check summary |
| Source manifest exists | yes | `source-manifest.yaml` path and hash |
| Artifact hash exists | yes | `artifact-hash.yaml` path |
| Public/private leak check | yes | Redacted leak check result |
| Noop public URL null check | yes | `publish-ledger.yaml` field evidence |
| Noop `public_url_created: false` check | yes | `publish-ledger.yaml` field evidence |

Rules:

- `status: PASS` requires all blocking checks to pass.
- `status: BLOCKED` blocks Daily Publish Gate and maps to `REVIEW_BLOCKED`.
- `evidence` must be redacted and must not contain secret values or private
  source notes.
- Missing validator result blocks Daily Publish Gate.

---

## 10. Rubric Review Stub Schema: `rubric-review.stub.json`

Recommended schema:

```json
{
  "run_id": "",
  "mode": "stub | manual",
  "status": "PASS | BLOCKED | NOT_RUN",
  "rubric_version": "",
  "reviewed_at": "",
  "reason_codes": [],
  "evidence_refs": [],
  "summary": ""
}
```

Rules:

- The file exists as a review input, not as a default PASS switch.
- File existence does not equal `PASS`.
- `PASS` must be explicit.
- `NOT_RUN` blocks Daily Publish Gate.
- `BLOCKED` blocks Daily Publish Gate.
- Missing, ambiguous, or unparseable status blocks Daily Publish Gate.
- Evidence refs must point to allowed evidence and must not inline private
  source notes, secrets, model traces, or full audit internals.

MVP may use `rubric-review.json` for a manual review with the same required
fields. Stub and manual modes share gate semantics.

---

## 11. Audit Review Stub Schema: `audit-review.stub.json`

Recommended schema:

```json
{
  "run_id": "",
  "mode": "stub | manual",
  "status": "PASS | BLOCKED | NOT_RUN",
  "audit_version": "",
  "reviewed_at": "",
  "private_evidence_checked": true,
  "public_private_boundary_checked": true,
  "reason_codes": [],
  "evidence_refs": [],
  "summary": ""
}
```

Rules:

- The audit stub is a gate input, not a default PASS switch.
- File existence does not equal `PASS`.
- `PASS` must be explicit.
- `NOT_RUN` blocks Daily Publish Gate.
- `BLOCKED` blocks Daily Publish Gate.
- `private_evidence_checked` must be explicitly true for PASS.
- `public_private_boundary_checked` must be explicitly true for PASS.
- Evidence refs must be redacted pointers, not private evidence dumps.

MVP may use `audit-review.json` for a manual review with the same required
fields. Stub and manual modes share gate semantics.

---

## 12. Publish Ledger Schema: `publish-ledger.yaml`

Recommended MVP noop schema:

```yaml
publish_ledger:
  run_id:
  mode: noop
  status: skipped | noop_completed | blocked
  publish_allowed:
  public_url: null
  public_url_created: false
  local_preview_path:
  noop_reference:
  artifact_hash:
  idempotency_key:
  reason_codes:
```

Rules:

- MVP `mode` must be `noop`.
- `public_url` must be `null`.
- `public_url_created` must be `false`.
- `local_preview_path` may point to `reader.html`.
- `noop_reference` may identify the noop publish target or run-local preview.
- `status: noop_completed` means the noop boundary completed.
- `noop_completed` must not be mapped to `PASS_PUBLISHED`.
- Non-null `public_url` in noop mode is a blocking schema violation.
- `publish_allowed: true` may appear only after Daily Publish Gate PASS.
- The ledger must not contain deployment tokens or provider credentials.

---

## 13. Notification Ledger Schema: `notification-ledger.yaml`

Recommended MVP noop / none schema:

```yaml
notification_ledger:
  run_id:
  mode: noop | none
  status:
  notification_intent:
  channel:
  sent: false
  external_message_id: null
  evidence_pointer:
  reason_codes:
```

Rules:

- MVP notification mode is `noop` or `none`.
- No real IM, WeChat, Slack, Telegram, Email, webhook, bot, or external message
  may be sent.
- `sent` must be `false`.
- `external_message_id` must be `null`.
- `notification_intent` may describe what would have been sent.
- `evidence_pointer` may point to private run evidence.
- The ledger must not contain full private evidence, source notes, review
  internals, audit internals, or credential values.

---

## 14. Run Ledger Schema: `run-ledger.yaml`

Recommended schema:

```yaml
run_ledger:
  run_id:
  started_at:
  ended_at:
  terminal_state:
  state_transitions:
    - from:
      to:
      at:
      reason:
  runtime_context_path:
  profile_snapshot_path:
  preflight_result_path:
  artifacts:
  gate_decisions:
  failure_package_path:
  badcase_record_path:
  idempotency_key:
```

Rules:

- The run ledger is the terminal index of the run.
- `terminal_state` must be one of the Core states defined by P2D-1 / P2D-2a.
- `state_transitions` must record every terminally relevant transition.
- `artifacts` must list present, skipped, and absent required artifacts.
- `gate_decisions` must record Adapter Configuration Gate and Daily Publish Gate
  outcomes when those gates were reached.
- `failure_package_path` is required for blocked and failed terminal states.
- `badcase_record_path` is required for `REVIEW_BLOCKED`, `SYSTEM_FAILED`, and
  `ADAPTER_FAILED`.
- `CONFIG_BLOCKED` requires a badcase only when persistent or user-reported.

Terminal state and artifact obligations are inseparable: the terminal state is
valid only when the ledger records the required artifacts and the explicit
skipped / absent reason for artifacts from stages that did not run.

---

## 15. Artifact Hash Schema: `artifact-hash.yaml`

Recommended schema:

```yaml
artifact_hash:
  run_id:
  algorithm:
  artifacts:
    - path:
      type:
      visibility:
      hash:
      required_for:
  aggregate_hash:
```

Rules:

- `algorithm` should be stable for the run, for example `sha256`.
- Every required artifact present at terminal state must be listed.
- Missing or skipped required artifacts must be represented in `run-ledger.yaml`
  and `failure-package.yaml`; they must not receive fabricated hashes.
- `visibility` must be `public_candidate`, `private_evidence`, `ledger`,
  `failure_evidence`, or `governance`.
- `required_for` should identify `daily_publish_gate`, `noop_publish`,
  `failure_package`, `badcase`, `idempotency`, or `audit`.
- `aggregate_hash` summarizes the present artifacts listed in this file.

Artifacts or artifact-derived values entering MVP idempotency:

```text
runtime profile snapshot through config_snapshot_hash
source-manifest.yaml through source_manifest_hash
training-report.md through training_report_hash
publish-ledger noop target through noop_reference or publish target
```

`reader.html` is integrity evidence and may be hashed, but it is not the primary
MVP idempotency input unless a later plan explicitly adds rendered output to the
idempotency policy.

---

## 16. Failure Package Schema: `failure-package.yaml`

Recommended schema:

```yaml
failure_package:
  run_id:
  terminal_state:
  failed_stage:
  failed_gate:
  failed_adapter:
  summary:
  reason_codes:
  missing_required_artifacts:
  skipped_stages:
  available_evidence:
  redaction_status:
  recommended_next_action:
```

Rules:

- The failure package must be redacted before storage.
- It must not contain credential values, tokens, cookies, webhooks, raw private
  source notes, or full model traces.
- It may name missing credential names.
- It must list missing required artifacts.
- It must list skipped stages and absent evidence.
- It must not fabricate evidence from stages that did not run.
- `failed_gate` is required for `CONFIG_BLOCKED` or `REVIEW_BLOCKED`.
- `failed_adapter` is required for `ADAPTER_FAILED`.
- `redaction_status` must be explicit.

---

## 17. Badcase Record Schema: `badcase-record.yaml`

Recommended schema:

```yaml
badcase_record:
  badcase_id:
  run_id:
  created_at:
  entry_type:
  severity:
  symptom:
  public_url_status:
  html_url_if_any:
  human_feedback:
  evidence_refs:
  suspected_root_cause:
  owner:
  status:
  linked_iteration:
  linked_lesson:
```

MVP rules:

- `entry_type` must support `CONFIG_BLOCKED`, `REVIEW_BLOCKED`,
  `SYSTEM_FAILED`, `ADAPTER_FAILED`, `PASS_BUT_UNSATISFACTORY`, and
  `HUMAN_REPORTED`.
- `REVIEW_BLOCKED` must generate a badcase.
- `SYSTEM_FAILED` must generate a badcase.
- `ADAPTER_FAILED` must generate a badcase.
- `CONFIG_BLOCKED` generates a badcase only when persistent or user-reported.
- `public_url_status` must be explicit, for example `none`, `not_created`,
  `existing_preserved`, or `invalid_unexpected`.
- `html_url_if_any` must be null for MVP noop runs unless referencing a future
  already-existing real URL outside the noop run.
- `evidence_refs` must point to redacted evidence.
- `status` must distinguish open, triaged, resolved, duplicate, or closed with
  explicit reason.

---

## 18. Artifact Classification Matrix

| Artifact | Required on Success | Required on CONFIG_BLOCKED | Required on REVIEW_BLOCKED | Required on SYSTEM_FAILED / ADAPTER_FAILED | Visibility | Stub Allowed | Public Output Allowed |
|---|---:|---:|---:|---:|---|---:|---:|
| `runtime-context.yaml` | yes | yes | yes | yes | ledger | no | no |
| `run-ledger.yaml` | yes | yes | yes | yes | ledger | no | no |
| `adapter-preflight-result.yaml` | yes | yes | yes | yes | ledger | no | no |
| `source-manifest.yaml` | yes | no, unless reached | yes, if source stage reached; otherwise absent recorded | if reached; otherwise absent recorded | private_evidence / gate_evidence | no | no |
| `source-notes.md` | yes | no, unless reached | if reached; otherwise absent recorded | if reached; otherwise absent recorded | private_evidence | no | no |
| `training-report.md` | yes | no | if generated; otherwise absent recorded | if generated; otherwise absent recorded | canonical_report / public_candidate_source | no | no, not directly |
| `reader.html` | yes | no | if rendered; otherwise absent recorded | if rendered; otherwise absent recorded | local_public_candidate | no | local preview only |
| `validator-result.yaml` | yes | no | yes, if validation reached; otherwise absent recorded | if validation reached; otherwise absent recorded | private_evidence / gate_evidence | no | no |
| `rubric-review.stub.json` | yes, or manual equivalent | no | yes, if evaluation reached; otherwise absent recorded | if evaluation reached; otherwise absent recorded | private_evidence / gate_evidence | yes | no |
| `audit-review.stub.json` | yes, or manual equivalent | no | yes, if audit reached; otherwise absent recorded | if audit reached; otherwise absent recorded | private_evidence / gate_evidence | yes | no |
| `publish-ledger.yaml` | yes | no | no, unless publish boundary was evaluated as blocked | if publish boundary reached; otherwise absent recorded | ledger | no | no |
| `notification-ledger.yaml` | yes | no | optional intent ledger if outcome notification intent evaluated | if notification stage reached; otherwise absent recorded | ledger | no | no |
| `failure-package.yaml` | no | yes | yes | yes | failure_evidence | no | no |
| `badcase-record.yaml` | no | only when persistent or user-reported | yes | yes | governance | no | no |
| `artifact-hash.yaml` | yes | yes | yes | yes | ledger | no | no |

Success means successful local / noop terminal state `NOOP_COMPLETED`, not
`PASS_PUBLISHED`.

---

## 19. Terminal State Artifact Obligations

| Terminal State | Must Exist | Must Not Exist or Must Not Claim | Badcase | Public URL Policy |
|---|---|---|---|---|
| `CONFIG_BLOCKED` | `runtime-context.yaml`, `run-ledger.yaml`, `adapter-preflight-result.yaml`, `failure-package.yaml`, `artifact-hash.yaml` | Must not claim retrieval, generation, render, publish, notification, or quality PASS; must not include credential values | Only if persistent or user-reported | `public_url` absent or null; `public_url_created: false` |
| `REVIEW_BLOCKED` | `runtime-context.yaml`, `run-ledger.yaml`, `adapter-preflight-result.yaml`, `failure-package.yaml`, `badcase-record.yaml`, `artifact-hash.yaml`, plus available stage artifacts | Must not publish; must not claim `NOOP_COMPLETED` or `PASS_PUBLISHED`; must not fake missing evidence | Required | `public_url: null`; no new public URL |
| `SYSTEM_FAILED` | `runtime-context.yaml`, `run-ledger.yaml`, `adapter-preflight-result.yaml`, `failure-package.yaml`, `badcase-record.yaml`, `artifact-hash.yaml`, plus available evidence | Must not create or update public URL after failure; must not erase earlier ledger evidence | Required | No new public URL; preserve any pre-existing publish ledger if failure happened after a future publish boundary |
| `ADAPTER_FAILED` | `runtime-context.yaml`, `run-ledger.yaml`, `adapter-preflight-result.yaml`, `failure-package.yaml`, `badcase-record.yaml`, `artifact-hash.yaml`, adapter failure evidence | Must not relabel provider failure as success; must not retry silently; must not expose credentials | Required | No new public URL unless failure is post-publication in a future non-MVP run and prior ledger is preserved |
| `NOOP_COMPLETED` | `runtime-context.yaml`, `run-ledger.yaml`, `adapter-preflight-result.yaml`, `source-manifest.yaml`, `source-notes.md`, `training-report.md`, `reader.html`, `validator-result.yaml`, rubric review stub/manual result, audit review stub/manual result, `publish-ledger.yaml`, `notification-ledger.yaml`, `artifact-hash.yaml` | Must not claim `PASS_PUBLISHED`; must not create/fake/reserve/imply real public URL; must not send real notification | Not required unless later human feedback reports dissatisfaction | `public_url: null`; `public_url_created: false`; local preview path allowed |

Terminal states are valid only when required artifacts exist or are explicitly
recorded as skipped / absent with reason in `run-ledger.yaml` and, for blocked or
failed runs, `failure-package.yaml`.

---

## 20. Schema Acceptance Cases

### Case 1: Valid noop successful run

- Input condition: local/manual source exists; preflight PASS; Markdown and HTML
  artifacts exist; validator PASS; rubric PASS; audit PASS; noop publish ledger
  has `public_url: null` and `public_url_created: false`.
- Expected terminal state: `NOOP_COMPLETED`.
- Required artifacts: all success artifacts in the classification matrix.
- Must not happen: no `PASS_PUBLISHED`, no real URL, no real notification, no
  external publish, no credential values.

### Case 2: Real provider enabled with missing credential

- Input condition: selected MVP profile enables a real provider and required
  credential name is missing.
- Expected terminal state: `CONFIG_BLOCKED`.
- Required artifacts: `runtime-context.yaml`, `run-ledger.yaml`,
  `adapter-preflight-result.yaml`, `failure-package.yaml`,
  `artifact-hash.yaml`; badcase only if persistent or user-reported.
- Must not happen: no retrieval, generation, render, publish, notification, live
  LLM call, external API call, or credential value exposure.

### Case 3: Rubric `NOT_RUN`

- Input condition: `rubric-review.stub.json` exists but status is `NOT_RUN`.
- Expected terminal state: `REVIEW_BLOCKED`.
- Required artifacts: available run artifacts, `validator-result.yaml` if
  reached, rubric stub, `failure-package.yaml`, `badcase-record.yaml`,
  `artifact-hash.yaml`.
- Must not happen: file existence must not count as PASS; no publish; no
  `NOOP_COMPLETED`.

### Case 4: Audit `BLOCKED`

- Input condition: `audit-review.stub.json` or `audit-review.json` status is
  `BLOCKED`.
- Expected terminal state: `REVIEW_BLOCKED`.
- Required artifacts: available run artifacts, audit result,
  `failure-package.yaml`, `badcase-record.yaml`, `artifact-hash.yaml`.
- Must not happen: no publish; no `NOOP_COMPLETED`; no hidden override by manual
  patch authority.

### Case 5: HTML contains private evidence marker

- Input condition: `reader.html` includes private evidence marker, private
  source notes, review internals, audit internals, model trace, or ledger content.
- Expected terminal state: `REVIEW_BLOCKED`.
- Required artifacts: `validator-result.yaml` with blocking leak check,
  `failure-package.yaml`, `badcase-record.yaml`, `artifact-hash.yaml`, plus
  available source/report/render artifacts.
- Must not happen: no public output, no notification with leaked content, no
  real URL.

### Case 6: Noop publish ledger has non-null `public_url`

- Input condition: `publish-ledger.yaml` is `mode: noop` but `public_url` is
  non-null or `public_url_created` is true.
- Expected terminal state: `REVIEW_BLOCKED` if caught by gate / validator before
  terminal close, or `SYSTEM_FAILED` if detected as a runtime contract violation.
- Required artifacts: `failure-package.yaml`, `artifact-hash.yaml`, and
  `badcase-record.yaml` when terminal state is `REVIEW_BLOCKED` or
  `SYSTEM_FAILED`.
- Must not happen: no `NOOP_COMPLETED`, no `PASS_PUBLISHED`, no acceptance of
  fake or reserved URL.

### Case 7: Source manifest missing

- Input condition: source stage was required or reached, but
  `source-manifest.yaml` is missing.
- Expected terminal state: `REVIEW_BLOCKED`.
- Required artifacts: `failure-package.yaml`, `badcase-record.yaml`,
  `artifact-hash.yaml`, and ledger record marking source manifest missing.
- Must not happen: no fabricated source manifest hash; no publish; no
  `NOOP_COMPLETED`.

### Case 8: Artifact hash missing

- Input condition: required `artifact-hash.yaml` is missing or does not list
  required present artifacts.
- Expected terminal state: `REVIEW_BLOCKED`.
- Required artifacts: `failure-package.yaml`, `badcase-record.yaml`,
  `run-ledger.yaml` with missing hash evidence.
- Must not happen: no publish; no `NOOP_COMPLETED`; no unverifiable artifact
  integrity claim.

### Case 9: Local artifact sink write failure

- Input condition: local artifact sink cannot write a required artifact or
  ledger file.
- Expected terminal state: `SYSTEM_FAILED`.
- Required artifacts: best-effort `runtime-context.yaml`, `run-ledger.yaml`,
  `adapter-preflight-result.yaml` if available, `failure-package.yaml`,
  `badcase-record.yaml`, and any durable evidence successfully written.
- Must not happen: no fake success, no public URL, no notification claiming
  completion.

### Case 10: Adapter execution failure

- Input condition: an enabled adapter passes preflight but fails during execution.
- Expected terminal state: `ADAPTER_FAILED`.
- Required artifacts: `runtime-context.yaml`, `run-ledger.yaml`,
  `adapter-preflight-result.yaml`, `failure-package.yaml`,
  `badcase-record.yaml`, `artifact-hash.yaml`, and redacted adapter failure
  evidence.
- Must not happen: no relabeling as generic success, no silent retry, no
  credential leakage, no new public URL.

---

## 21. Non-Goals

P2D-2b does not:

- write code;
- create schema files;
- create runtime profile files;
- create artifact example files;
- create directories;
- implement runtime behavior;
- implement Adapters;
- implement validators;
- implement gates;
- implement publisher behavior;
- implement notifier behavior;
- run tests;
- call live LLMs;
- call external APIs;
- deploy;
- publish;
- generate a real public URL;
- send IM, WeChat, Slack, Telegram, Email, webhook, or bot notifications;
- modify P2C outputs;
- modify P2C ledgers;
- modify source packages;
- modify `AGENTS.md`;
- modify P2D-0 documents;
- modify P2D-1 documents;
- modify P2D-2a documents;
- run `git add`;
- commit;
- push.

---

## 22. Definition of Done

P2D-2b is done when this planning document defines:

- runtime context schema;
- profile snapshot schema;
- preflight schema;
- source manifest schema;
- source notes contract;
- training report contract;
- reader HTML contract;
- validator schema;
- rubric review stub schema;
- audit review stub schema;
- publish ledger schema;
- notification ledger schema;
- run ledger schema;
- artifact hash schema;
- failure package schema;
- badcase record schema;
- artifact classification matrix;
- terminal state obligations;
- schema acceptance cases;
- non-goals;
- safety boundary.

P2D-2b is not done by implementing runtime capability. It is done by freezing
the MVP contract surface so later implementation stages can remain local,
manual, noop-first, auditable, and small.

---

## 23. Safety Boundary

Allowed in P2D-2b:

- read repository documentation;
- create this planning document;
- inspect this planning document;
- run `git status`;
- run `git diff`.

Forbidden in P2D-2b:

- writing code;
- adding scripts;
- creating `src/`, `runtime/`, or `artifacts/` directories;
- creating real `.yaml` or `.json` schema files;
- creating artifact example files;
- implementing runtime behavior;
- implementing Adapters;
- implementing evaluators;
- implementing validators;
- implementing gates;
- implementing publisher behavior;
- implementing notifier behavior;
- calling live LLMs;
- calling external APIs;
- deploying;
- publishing;
- generating a real public URL;
- sending notifications;
- modifying P2C outputs;
- modifying P2C ledgers;
- modifying source package files;
- modifying `AGENTS.md`;
- modifying P2D-0 documents;
- modifying P2D-1 documents;
- modifying P2D-2a documents;
- running `git add`;
- committing;
- pushing.

The only allowed repository change for P2D-2b is:

```text
docs/architecture/p2d-2b-ai-daily-publishing-system-runtime-contract-and-artifact-schema-plan.md
```
