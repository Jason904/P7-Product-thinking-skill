# Hermes Agent Operating Rules

## Instruction Loading and Scope

- This file is the repo-root agent instruction file for Codex and other AI coding agents working in this Hermes repository.
- It provides durable repository-level operating rules for the repository tree.
- Codex sessions opened from this repository should treat this file as the default project guidance unless a more specific nested `AGENTS.md` applies.
- More-specific `AGENTS.md` files may be added in subdirectories later and should override this file only for their own subtree.
- Direct system, developer, or user instructions in the active task take precedence over this file.
- HermesAgent runtime on Mac mini is not automatically equivalent to Codex and must not assume this file is loaded by default.
- If HermesAgent needs to follow these rules in production, the runtime must explicitly load this file or receive equivalent policy through runtime configuration, prompt injection, or packaged stable Skill metadata.

## Runtime Boundaries

- Mac mini is the production Daily Runner and WeChat notifier.
- MacBook Air is the Skill development, triage, and release owner.
- Mac mini must run only stable Hermes Skill releases.
- Mac mini must not run unpublished development Skill versions.
- Mac mini must not modify the Skill dev branch.

## Publishing Rules

- Do not publish a Daily Site URL unless validators and rubric review pass.
- On quality failure, do not publish. Generate a failure package and create an Ops issue.
- On system failure, preserve evidence in Ops Repo or local durable spool before retrying.
- WeChat is notification only. It is not the evidence store.
- Current target requires a URL only; no API output is required.

## Evidence Rules

- Every daily run must record skill_version, rubric_version, generator_version, renderer_version, and publisher_version.
- Runtime evidence belongs in Ops Repo.
- Public daily HTML belongs in Daily Site Repo.
- Durable Skill changes belong in Skill Dev / Release Repo.
- Do not write secrets, tokens, cookies, or private credentials into Ops Repo, Daily Site Repo, or WeChat messages.

## Human Feedback Rules

- If a published page passes gates but the user is dissatisfied, record PASS_BUT_UNSATISFACTORY.
- Classify feedback as content patch or Skill improvement.
- Content patches may update the specific daily page.
- Skill improvements require tests, changelog, and a new stable release.

## Release Rules

- Stable releases are produced from MacBook Air after gates pass.
- Badcase fixes should become regression coverage before release.
- Mac mini should fetch the latest stable release at run start and record the resolved version.
