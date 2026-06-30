# P2C-7p Source Notes - 2026-06-30 v9

## Boundary

- Artifact type: real daily training candidate for P2C-7 Day-3 readiness.
- Not a governance-generated sample.
- Not a replay fixture.
- Not a shadow run.
- No Day-3 execution was performed while writing these notes.

## Source Channels

| Channel | Status | Use | Boundary |
| --- | --- | --- | --- |
| AI HOT | used | `https://aihot.virxact.com/api/public/daily/2026-06-30` was used as a discovery signal pool. | AI HOT summaries are C-level signals only. They do not support final judgment unless traced to official or primary sources. |
| Web Search / official sources | used | Used to verify official Cursor, Anthropic, OpenAI, GitHub and primary pages. | Official sources support final judgment; media and X/social signals are downgraded. |
| GitHub / open-source | used | GitHub API / repository pages were used for open-source candidates and Claude Code release signal. | Star, fork, issue and push data indicate attention and activity, not product-market fit. |

## Deep Case Source Map

### Case A: Cursor for iOS

Source facts:
- Cursor official blog says Cursor for iOS beta is available for paid plans.
- Cursor official blog describes always-on cloud agents, remote desktop agents, voice input, slash commands, model selection, Live Activities, push notifications, isolated VM execution, merge-ready PRs, demos, screenshots and logs.

Links:
- Cursor official blog: https://cursor.com/blog/ios-mobile-app
- AI HOT signal: https://aihot.virxact.com/items/cmqzisfra009asl8hojqmr1k2

Product inference:
- Mobile is positioned as an agent task control surface rather than a complete IDE replacement.

Hypothesis:
- Mobile control will reduce waiting and handoff cost only if review quality, permissions and context transfer are strong.

Downgraded / unverified:
- Adoption, retention, team use and enterprise security acceptance are not verified.

### Case B: Claude apps gateway

Source facts:
- Anthropic official blog says Claude apps gateway is a self-hosted control plane.
- Anthropic official blog says it supports running Claude Code on Amazon Bedrock and Google Cloud.
- Anthropic official blog describes SSO via OIDC, centralized policy, role permissions, routing / failover, usage limits and OTLP telemetry.
- Anthropic official blog says the gateway does not send inference traffic or usage data to Anthropic unless configured to use Claude API.

Links:
- Anthropic official blog: https://claude.com/blog/introducing-the-claude-apps-gateway
- AI HOT signal: https://aihot.virxact.com/items/cmqzq4so7002zslki45ad5xtq

Product inference:
- The gateway is best interpreted as enterprise AI coding control plane, not just a cloud connector.

Hypothesis:
- Gateway value should be measured by security approval speed, budget governance, telemetry coverage and deployment success.

Downgraded / unverified:
- Customer deployment data, approval-cycle reduction and TCO are not verified.

### Case C: OpenAI EU jobs transition report

Source facts:
- OpenAI official site published `Mapping AI jobs transition in the EU`.
- AI HOT surfaced the report as a 2026-06-30 signal.

Links:
- OpenAI official report: https://openai.com/index/mapping-ai-jobs-transition-eu
- AI HOT signal: https://aihot.virxact.com/items/cmqz31dsn003usldyi61f0cgf

Product inference:
- The report is useful for personal career strategy when translated from job labels to task composition and workflow ownership.

Hypothesis:
- The user's best defense is not simply learning more tools, but building reusable AI workflow design, quality judgment and expression assets.

Downgraded / unverified:
- EU findings should not be mechanically generalized to other labor markets or individual industries without local data.

## Radar / Watchlist Sources

- Claude in Microsoft Foundry: https://claude.com/blog/claude-in-microsoft-foundry
- Claude Code v2.1.196: https://github.com/anthropics/claude-code/releases/tag/v2.1.196
- Herdr: https://github.com/ogulcancelik/herdr
- Omnigent: https://github.com/omnigent-ai/omnigent
- Meta Brain2Qwerty v2 signal: https://x.com/AIatMeta/status/2071566924803395741
- EverOS secondary signal: https://www.marktechpost.com/2026/06/29/meet-everos-an-open-source-markdown-first-agent-memory-runtime-with-hybrid-bm25-vector-retrieval-and-self-evolving-skills

## Downgrade Policy Applied

- AI HOT: C-level signal, discovery only.
- X / social signals: C-level unless traced to official pages or papers.
- Media / secondary reporting: B or C depending on credibility; not used as final support for selected deep cases.
- GitHub metadata: A-level for repository metadata itself, but not proof of commercial adoption.
- Product inference: explicitly separated from source facts.
- Hypothesis: explicitly marked as unverified until adoption, customer or longitudinal data exists.
