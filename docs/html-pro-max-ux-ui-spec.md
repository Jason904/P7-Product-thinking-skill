# Hermes HTML Pro Max UX/UI Spec

## 1. Design Goal

Hermes HTML Pro Max is not a prettier Markdown page. It is a reading and deliberate-practice workspace for long-form P7+ Insight training.

The page must help the user do four things:

1. **Understand quickly**: know today's cases, why they were selected, and what the core Insight is.
2. **Read deeply**: follow evidence, methods, 8 questions, counterarguments, tradeoffs, and validation logic without getting lost.
3. **Speak clearly**: rehearse 2-minute, PREP, SCQA, and follow-up answers.
4. **Assetize reliably**: turn each case into reusable interview material, project methods, and review cards.

The source of truth remains Markdown. HTML is the comprehension layer.

## 2. Product Type

This interface should be designed as:

```text
Professional knowledge-work reading workspace
```

Not as:

- Landing page.
- Marketing hero.
- Blog article template.
- Decorative dashboard.
- News summary page.

The user is not browsing casually. The user is training judgment, expression, and reusable product-thinking assets.

## 3. Design Principles

### 3.1 Insight First

The first screen should answer:

- What are today's 3 deep cases?
- What is the strongest Insight from each case?
- Which case matters most for my personal growth?
- Are sources complete enough to trust the analysis?
- What is the quality score and weak point?

Do not force the user to scroll through source tables before seeing why today's training matters.

### 3.2 Progressive Disclosure

The Markdown is long by design. The HTML should not shorten it. It should reveal it in layers:

1. Daily overview.
2. Case Insight summary.
3. Evidence and source confidence.
4. Analysis method workbench.
5. 8-question reasoning path.
6. Expression rehearsal.
7. Asset Card and Watchlist.
8. Full raw content if needed.

### 3.3 Reasoning Traceability

Every major conclusion should be visually traceable to:

```text
source -> fact confidence -> method dimension -> reasoning step -> conclusion -> tradeoff -> validation
```

The UI should make this chain easier to follow than raw Markdown.

### 3.4 Training Over Reading

This is not only a document viewer. It should support practice:

- "I want to understand."
- "I want to rehearse."
- "I want to review later."
- "I want to extract a reusable Pattern."

Reading modes should map to these jobs.

### 3.5 Calm, Dense, Professional

The visual system should feel like an executive research desk:

- clear hierarchy
- restrained color
- high legibility
- dense but organized tables
- precise source and score signals
- no decorative gradients or oversized marketing hero

## 4. Current Renderer Assessment

Current `render_training_html.py` already provides:

- left side navigation
- hero summary
- source badges
- case panels
- table rendering
- basic responsive layout

Current limitations:

- It still reads like a Markdown conversion page.
- It does not distinguish reading modes.
- It does not surface each case's Insight before the long body.
- It does not turn PREP / SCQA into rehearsal tools.
- It does not visually connect source confidence, method output, and final judgment.
- It does not provide a right-side "current case context" or progress map.
- It does not make Asset Cards feel like reusable assets.

## 5. Target Information Architecture

### 5.1 Page Shell

Recommended layout on desktop:

```text
┌──────────────────────────────────────────────────────────────┐
│ Top Bar: Date / Training Version / Source Status / Quality   │
├───────────────┬───────────────────────────────┬──────────────┤
│ Left Nav      │ Main Reading Area             │ Right Rail   │
│ Sections      │ Daily Overview + Cases        │ Case Context │
│ Case anchors  │                               │ Progress     │
│ Modes         │                               │ Actions      │
└───────────────┴───────────────────────────────┴──────────────┘
```

On mobile:

- top compact header
- horizontal case tabs
- collapsible section nav
- no fixed right rail
- sticky bottom mode switcher if useful

### 5.2 First Screen

The first viewport should show:

- date and version
- `3 deep cases`
- average Insight score
- source-channel status
- three case summary cards
- one daily strongest pattern

Each case summary card should include:

- Case title
- Case type: A / B / C
- one-sentence phenomenon
- one-sentence Insight
- score
- main weak point
- primary action: `Read`, `Rehearse`, `Asset`

### 5.3 Daily Overview Sections

Recommended order:

1. **Today At A Glance**
   - 3 selected cases
   - why selected
   - source completeness
   - quality score overview

2. **Candidate Pool**
   - compact table
   - source links
   - score explanation
   - treatment label
   - Watchlist status

3. **Deep Case Workspace**
   - Case A / B / C tabs or stacked panels
   - each case has its own internal navigation

4. **Practice And Review**
   - autonomous question
   - old case recall
   - daily review
   - next review prompt

## 6. Deep Case Layout

Each deep case should be rendered as a structured workspace, not one long stream.

### 6.1 Case Header

The case header should show:

- Case name
- Case type
- source confidence status
- Insight score
- asset grade
- Watchlist status
- `Read`, `Reason`, `Rehearse`, `Asset` mode buttons

### 6.2 Insight Board

Default-open section.

Contents:

- 一句话 Insight
- 核心判断
- 做 / 不做 / 先验证
- 最大机会
- 最大风险
- main weak point from Insight Audit

Visual treatment:

- Use a restrained "judgment card".
- Avoid giant quote styling.
- Use clear labels and strong text hierarchy.

### 6.3 Evidence Layer

Contents:

- confirmed facts
- industry opinions
- personal inferences
- hypotheses to verify
- Fact Confidence Table
- source links

Visual treatment:

- source badges by level: A / B / C / D
- A-level facts can support judgment
- C-level facts should visually read as signal only
- unverified claims should be amber, not red

### 6.4 Analysis Method Workbench

This is a key Hermes-specific section.

Recommended display:

```text
Method -> Why used -> Dimensions -> Key finding -> Supported Insight
```

Interaction:

- method rows expandable
- each expanded row shows:
  - what it decomposed
  - what contradiction it found
  - what conclusion it produced
  - how it supports final judgment

Design goal:

The user should be able to learn how to use the method, not only see that the method was used.

### 6.5 P7+ Deep Questions

P7+ 追问 should be shown as a reasoning drill.

Each question block should include:

- question
- deep answer
- derivation basis
- possible objection
- response
- stage conclusion
- impact on final judgment

Interaction:

- default show question + stage conclusion
- expand to see full answer and objection
- provide `Practice this answer` affordance later

### 6.6 8-Question Reasoning Path

Render as a vertical reasoning timeline:

1. 谁
2. 在哪
3. 损失什么
4. 想得到什么
5. 为什么卡住
6. 谁共同作用
7. 未来怎么变
8. 价值流向哪里

Each step should show:

- purpose
- method
- derivation
- stage conclusion
- how it affects next step

Design goal:

The user should see "how the thought moves", not just "what the final answer is".

### 6.7 Mechanism And System Section

This should visually group:

- 底层矛盾与因果机制
- 系统关系与价值迁移
- 反面论证与边界条件

Recommended component:

- three-column relationship board on desktop
- stacked cards on mobile

The section should highlight:

- core contradiction
- causal chain
- push force
- resistance
- bottleneck
- amplifier
- value capture point
- falsification condition

### 6.8 Expression Rehearsal

This should become a tabbed rehearsal cockpit:

- `2 min`
- `PREP`
- `SCQA`
- `Follow-up`

Design behavior:

- default tab: `2 min`
- PREP and SCQA use labeled rows
- follow-up answers show question/answer pairs
- optional future feature: copy button for each expression version

Design goal:

The user can directly practice speaking, not just read the written analysis.

### 6.9 Insight Quality Audit

Render the score table as:

- compact score summary first
- detailed rubric expandable
- deduction reasons highlighted
- improvement actions highlighted

Do not visually over-celebrate high scores. The purpose is quality governance, not self-praise.

### 6.10 Case Asset Card

Render as a reusable knowledge card.

Important fields:

- 一句话本质
- 核心矛盾
- 可复用 Pattern
- 可迁移到我的哪个项目
- 可迁移到哪类面试题
- Watchlist status
- asset grade
- review priority

Interaction:

- `Asset view` condenses the full case into this card.
- Future option: export/copy asset card.

## 7. Reading Modes

### 7.1 Scan Mode

For first pass.

Shows:

- daily overview
- case cards
- Insight Board
- score summary
- source status

Hides:

- full 8 questions
- full audit table
- full source details

### 7.2 Deep Read Mode

For learning.

Shows:

- all reasoning sections
- evidence
- method workbench
- 8-question timeline
- counterarguments

### 7.3 Rehearsal Mode

For interview / discussion practice.

Shows:

- 2-minute expression
- PREP
- SCQA
- follow-up answers
- memory cues

### 7.4 Asset Mode

For knowledge-base capture.

Shows:

- Case Asset Card
- reusable Pattern
- migration fields
- Watchlist and review priority

### 7.5 Review Mode

For forgetting-curve learning.

Shows:

- old case recall
- daily review
- tomorrow review recommendation
- weak points from audits

## 8. Visual System

### 8.1 Style Direction

Recommended style:

```text
Professional Minimalism + Data-Dense Knowledge Workspace
```

Secondary influence:

```text
Research Notebook + Executive Briefing
```

Avoid:

- glassmorphism as dominant style
- dark dashboard look
- AI purple/pink gradient
- decorative blobs/orbs
- marketing-style hero
- oversized cards that waste reading space

### 8.2 Color Palette

Use a quiet multi-accent palette:

```css
:root {
  --bg: #f7f7f4;
  --surface: #ffffff;
  --surface-muted: #f1f3f5;
  --ink: #18202f;
  --muted: #687385;
  --line: #d9dee7;

  --accent-blue: #2458c8;   /* navigation / links / primary structure */
  --accent-teal: #0f766e;   /* verified / source OK / value flow */
  --accent-amber: #b7791f;  /* hypothesis / watchlist / caution */
  --accent-red: #b42318;    /* risk / invalid / D-level */
  --accent-slate: #40506a;  /* method / system relationship */
}
```

Rationale:

- Blue gives structure and trust.
- Teal marks verified / constructive signals.
- Amber marks uncertainty without panic.
- Red is reserved for real risk.
- Neutral background keeps long reading comfortable.

### 8.3 Typography

Recommended:

```css
font-family:
  -apple-system,
  BlinkMacSystemFont,
  "SF Pro Text",
  "PingFang SC",
  "Microsoft YaHei",
  "Segoe UI",
  sans-serif;
```

Rules:

- No negative letter spacing.
- No viewport-scaled text.
- Main body around 16px / 1.72.
- Tables can use 13-14px but must preserve readability.
- Headings should be compact, not hero-sized inside case panels.

### 8.4 Density

Hermes content is naturally long. The UI should be dense but not cramped:

- case cards: compact
- tables: scrollable and sticky header where useful
- sections: clear spacing
- long sections: collapsible
- no nested decorative cards

## 9. Core Components

### 9.1 Source Status Strip

Shows:

- Search / Web
- AI HOT
- GitHub / Open-source
- Primary sources

States:

- used
- unavailable
- partially verified
- claims downgraded

### 9.2 Case Summary Card

Fields:

- type
- title
- one-sentence description
- one-sentence Insight
- score
- source confidence
- treatment
- weak point

### 9.3 Insight Score Bar

Shows:

- total score
- thinking depth
- content quality
- expression quality
- deduction reason

No gamified trophies. This is quality governance.

### 9.4 Method Workbench Table

This is a signature Hermes component.

Columns:

- method
- why used
- dimensions
- key finding
- supported insight

Expanded detail:

- contradiction found
- decision impact
- what would be lost if removed

### 9.5 Reasoning Timeline

For the 8 questions.

Each step:

- number
- question
- method
- derivation
- conclusion
- next-step effect

### 9.6 Expression Tabs

Tabs:

- 2 min
- PREP
- SCQA
- follow-up

Later:

- copy button
- practice checklist
- self-score after speaking

### 9.7 Asset Card

Compact reusable card with:

- Pattern
- transfer project
- interview question type
- Watchlist
- asset grade
- review priority

## 10. Interaction Rules

### 10.1 Defaults

Default page state:

- daily overview open
- all case headers visible
- Insight Board open for all cases
- deep reasoning collapsed inside each case
- active case highlighted in left nav

### 10.2 Expand/Collapse

Use expand/collapse for:

- source details
- full candidate pool
- method rows
- 8-question details
- full audit table
- raw Asset Card details

Do not collapse:

- case title
- one-sentence Insight
- core judgment
- source status
- score summary
- do / don't / validate-first

### 10.3 Anchors

Every major section needs anchors:

- daily overview
- candidate pool
- radar
- each case
- each case subsection
- practice
- review

### 10.4 Keyboard And Accessibility

Required:

- visible focus states
- native buttons or accessible controls
- `aria-expanded` for collapsible sections
- `aria-controls` where applicable
- contrast >= WCAG AA
- respects `prefers-reduced-motion`

## 11. Responsive Behavior

### Desktop >= 1200px

- three-column shell
- left nav fixed
- right rail fixed
- main content max width controlled

### Tablet 768-1199px

- left nav becomes top section nav
- right rail becomes inline case context
- case tabs remain visible

### Mobile <= 767px

- single column
- sticky top case selector
- compact score chips
- tables horizontally scroll
- long text uses clear section dividers
- no hover-only interactions

## 12. Anti-Patterns

Do not:

- shorten Markdown content to make HTML look cleaner
- use a marketing hero
- make a dashboard that hides the actual reading
- use decorative gradients/orbs/blobs
- overuse purple AI styling
- make everything a card
- nest cards inside cards
- turn score into gamification
- make source confidence visually ambiguous
- hide final judgment behind too many clicks
- let PREP / SCQA become plain paragraphs with no practice affordance
- make mobile tables unreadable
- use icons without text where meaning is not obvious

## 13. Implementation Plan

### Phase 1: Parser And Data Extraction

Extend `render_training_html.py` to extract:

- date / title
- source channel statuses
- candidate table
- case names
- case types
- one-sentence Insights
- total scores
- sub-scores
- asset grades
- Watchlist statuses
- section blocks per case

No visual redesign yet. First make content addressable.

### Phase 2: HTML Structure Upgrade

Add semantic components:

- daily overview
- case summary cards
- source status strip
- case workspace
- Insight Board
- Method Workbench
- 8-question timeline
- Expression Tabs
- Asset Card panel

### Phase 3: Visual System

Apply:

- professional minimal palette
- clear density rules
- readable table styling
- score bars
- source badges
- responsive shell

### Phase 4: Interaction

Add:

- section collapse
- case mode tabs
- sticky nav
- current case context
- copy-ready expression blocks if low risk

### Phase 5: QA

Verify with:

- `training-v6-raw.md`
- desktop screenshot
- mobile screenshot
- no overlapping text
- tables readable
- keyboard navigation
- validator still passes for Markdown
- renderer unit tests updated

### Phase 6: Skill Integration

After renderer works:

- update Hermes skill Daily HTML Artifact Workflow
- add HTML Pro Max rendering rules
- add QA checklist
- keep chat reply behavior: only HTML link for daily mode unless user asks for logs

## 14. Acceptance Criteria

HTML Pro Max is acceptable only if:

1. It preserves all Markdown content.
2. The first screen makes today's training value clear.
3. The user can jump to each case and each major subsection.
4. Each case exposes Insight before long details.
5. Source confidence is visible and understandable.
6. Method Workbench teaches how analysis methods generated Insight.
7. 8-question reasoning is easier to follow than raw Markdown.
8. PREP / SCQA / 2-minute versions feel like rehearsal tools.
9. Case Asset Card feels reusable, not buried.
10. Desktop and mobile layouts are readable.
11. No decorative UI hurts comprehension.
12. Renderer tests pass.
13. Browser screenshot QA confirms no major overlap or blank rendering.

## 15. Recommended Next Action

Next implementation should not start by changing colors.

Start with:

```text
extract structured case metadata -> build daily overview -> build case summary cards -> build case workspace layout
```

Once information architecture is working, then apply visual polish.

The strongest first prototype target is:

```text
training-v6-raw.html -> training-v6-pro-max.html
```

Use V6 because it is long enough to stress-test reading density and contains all critical sections.
