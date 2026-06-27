# Hermes HTML Pro Max Option E MVP Wireframe

## 1. Purpose

This document turns the recommended design direction into an MVP wireframe.

Recommended direction:

```text
Hybrid Insight Learning Workspace
```

Core promise:

```text
先快速建立认知，再深入学习推导，再演练表达，最后沉淀资产。
```

This MVP should prove the HTML can serve Hermes' learning loop without changing or thinning the Markdown content.

## 2. MVP Scope

### Included

1. Daily overview.
2. Three case Insight cards.
3. Source status strip.
4. Case workspace.
5. Insight Board.
6. Evidence layer.
7. Method Workbench.
8. 8-question timeline.
9. Expression tabs.
10. Asset Card panel.
11. Desktop and mobile responsive layout.

### Not Included Yet

1. Cross-day case database.
2. Full search.
3. Notion / Obsidian export.
4. Copy buttons.
5. Speech self-score.
6. User account state.
7. Complex animations.

Reason:

The first prototype should validate information architecture and reading flow before adding productivity features.

## 3. Desktop Layout

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ Hermes P7+ Daily Training                         2026-06-25  V6  Avg 94.7 │
│ Sources: Web 已使用 | AI HOT 已使用 | GitHub 已使用 | Primary 已核验         │
├───────────────┬──────────────────────────────────────────────┬───────────────┤
│ LEFT NAV      │ MAIN                                         │ RIGHT RAIL    │
│               │                                              │               │
│ Overview      │ TODAY AT A GLANCE                            │ Current Case  │
│ Candidate     │ ┌─────────────┬─────────────┬─────────────┐  │ Score         │
│ Radar         │ │ Case A      │ Case B      │ Case C      │  │ Weak Point    │
│ Case A        │ │ Insight     │ Insight     │ Insight     │  │ Source Level  │
│  Insight      │ │ Score       │ Score       │ Score       │  │ Mode          │
│  Evidence     │ └─────────────┴─────────────┴─────────────┘  │               │
│  Methods      │                                              │ Read          │
│  8Q           │ CASE WORKSPACE                               │ Reason        │
│  Expression   │ ┌──────────────────────────────────────────┐ │ Rehearse      │
│  Asset        │ │ Case Header                              │ │ Asset         │
│ Case B        │ │ Insight Board                            │ │               │
│ Case C        │ │ Evidence / Methods / 8Q / Expression     │ │               │
│ Practice      │ │ Asset Card                               │ │               │
│ Review        │ └──────────────────────────────────────────┘ │               │
└───────────────┴──────────────────────────────────────────────┴───────────────┘
```

### Design Notes

- Left nav solves navigation.
- Main area solves learning.
- Right rail solves context and mode switching.
- Top bar solves trust and orientation.
- The first screen must include the three case cards without requiring deep scroll.

## 4. Mobile Layout

```text
┌──────────────────────────────┐
│ Hermes Daily  V6  Avg 94.7  │
│ Web | AI HOT | GitHub OK    │
├──────────────────────────────┤
│ Case A | Case B | Case C    │
├──────────────────────────────┤
│ Today At A Glance            │
│ ┌──────────────────────────┐ │
│ │ Case Insight Card        │ │
│ └──────────────────────────┘ │
│ ┌──────────────────────────┐ │
│ │ Case Insight Card        │ │
│ └──────────────────────────┘ │
│ ┌──────────────────────────┐ │
│ │ Case Insight Card        │ │
│ └──────────────────────────┘ │
├──────────────────────────────┤
│ Case Workspace               │
│ [Insight] [Reason] [Speak]   │
│ Collapsible sections         │
└──────────────────────────────┘
```

### Mobile Rules

- No fixed right rail.
- Case tabs stay near the top.
- Tables scroll horizontally.
- Deep sections collapse by default.
- Insight Board and score summary stay visible.
- No hover-only interaction.

## 5. First Screen Structure

### Top Status Bar

Fields:

| Field | Purpose |
| --- | --- |
| Date | orient the daily folder |
| Version | show source artifact, such as V6 |
| Deep case count | prove 3 complete cases |
| Average Insight score | quick quality signal |
| Source channel badges | trust status |

### Today At A Glance

Contains:

- daily strongest Pattern
- three case Insight cards
- source completeness
- today's primary training ability

Recommended copy logic:

```text
今天训练的不是“看新闻”，而是：
从基础设施、企业治理、推理训练三个角度，判断 AI 产品能力如何进入真实工作流并转化为个人壁垒。
```

The exact text should be generated from the Markdown, not hard-coded.

## 6. Case Insight Card

### Card Fields

```text
Case Type: A / B / C
Case Name
One-sentence phenomenon
One-sentence Insight
Score
Source confidence
Main weak point
Primary action: Read / Rehearse / Asset
```

### Example Shape

```text
┌──────────────────────────────────────┐
│ Case B · Product / Business          │
│ Mistral Connectors                   │
│                                      │
│ Insight                              │
│ 企业 agent 的门槛不是能连接，         │
│ 而是能被组织权限、身份和调试治理。    │
│                                      │
│ Score 96/100   Sources A-level       │
│ Weak point: adoption data incomplete │
│ [Read] [Rehearse] [Asset]            │
└──────────────────────────────────────┘
```

### Acceptance

- The card should be readable in 15 seconds.
- It should not hide the core Insight behind a click.
- It should not become a decorative oversized card.

## 7. Case Workspace

Each case workspace has four modes:

```text
Read -> Reason -> Rehearse -> Asset
```

These are not separate pages. They are filters / anchors over the same complete content.

### 7.1 Read Mode

Default mode.

Open by default:

- Case Header
- Insight Board
- Final judgment summary
- score summary

Collapsed:

- full source table
- full method workbench
- full 8Q
- full audit table

### 7.2 Reason Mode

For deep learning.

Open by default:

- Evidence Layer
- Method Workbench
- P7+ 追问深答
- 8Q timeline
- mechanism / system / counterargument

Collapsed:

- expression versions
- asset card detail

### 7.3 Rehearse Mode

For speaking.

Open by default:

- 2-minute expression
- PREP
- SCQA
- follow-up answers

Collapsed:

- source tables
- audit tables

### 7.4 Asset Mode

For reuse.

Open by default:

- Case Asset Card
- reusable Pattern
- migration project
- interview question mapping
- Watchlist
- review priority

Collapsed:

- full 8Q
- full expression sections

## 8. Insight Board

The Insight Board is the most important component.

### Content

```text
一句话 Insight
核心判断
做 / 不做 / 先验证
最大机会
最大风险
主要扣分点
下一步补强
```

### Layout

```text
┌─────────────────────────────────────────────────────┐
│ Insight                                             │
│ [one-sentence Insight]                              │
├────────────────────┬────────────────────────────────┤
│ Do                 │ Don't                          │
│ Validate First     │ Key Risk                       │
├────────────────────┴────────────────────────────────┤
│ Weak point / next improvement                       │
└─────────────────────────────────────────────────────┘
```

### Rule

This board must be visible before the full reasoning details.

## 9. Evidence Layer

### Purpose

Make fact confidence visible.

### Fields

- 已确认事实
- 行业观点
- 个人推断
- 待验证假设
- Fact Confidence Table
- source links

### Visual States

| Fact Level | Visual Treatment | Meaning |
| --- | --- | --- |
| A | teal badge | can support final judgment |
| B | blue badge | usable with caution |
| C | amber badge | signal only |
| D | red outline | cannot support final judgment |

## 10. Method Workbench

### Purpose

Teach the user how analysis methods create Insight.

### Layout

```text
┌──────────────┬────────────┬─────────────┬──────────────┬──────────────┐
│ Method       │ Why Used   │ Dimensions  │ Finding      │ Supports     │
├──────────────┼────────────┼─────────────┼──────────────┼──────────────┤
│ JTBD         │ ...        │ ...         │ ...          │ ...          │
└──────────────┴────────────┴─────────────┴──────────────┴──────────────┘
```

### Expanded Row

```text
What contradiction did this method reveal?
What conclusion did it produce?
What would be lost if this method were removed?
```

### Rule

If a method does not affect the final Insight, it should not be visually emphasized.

## 11. 8Q Timeline

### Purpose

Show how the thinking moves.

### Layout

```text
1 谁
  Purpose
  Method
  Derivation
  Stage conclusion
  Impact on next step

2 在哪
  ...
```

### Interaction

- default: show question + stage conclusion
- expand: show full derivation

This avoids the user being overwhelmed by all eight detailed blocks at once.

## 12. Expression Rehearsal Tabs

### Tabs

```text
2 min | PREP | SCQA | Follow-up
```

### Design

- The 2-minute version should read like a speaking script.
- PREP should use four labeled rows.
- SCQA should use four labeled rows.
- Follow-up should show question / answer pairs.

### Future Feature

Later, add:

- copy button
- "practice from memory" toggle
- self-score after speaking

Do not add these in MVP unless the base reading experience is already stable.

## 13. Asset Panel

### Purpose

Make the Case Asset Card reusable.

### Layout

```text
┌──────────────────────────────────────┐
│ Asset Grade: A                       │
│ Pattern: ...                         │
│ Core contradiction: ...              │
│ Transfer to project: ...             │
│ Interview question type: ...         │
│ Watchlist: next week review          │
│ Review priority: high                │
└──────────────────────────────────────┘
```

### Rule

The Asset Panel must not replace the full Case Asset Card. It summarizes and links to it.

## 14. Visual Direction

### Recommended

```text
Professional Minimalist Knowledge Workspace
```

### Visual Keywords

- calm
- precise
- dense
- trustworthy
- readable
- executive
- methodical

### Avoid

- AI purple gradient
- decorative hero
- glassmorphism as dominant style
- gamified score celebrations
- too many floating cards
- dark dashboard as default

## 15. Color Tokens

```css
:root {
  --bg: #f7f7f4;
  --surface: #ffffff;
  --surface-muted: #f1f3f5;
  --ink: #18202f;
  --muted: #687385;
  --line: #d9dee7;

  --accent-blue: #2458c8;
  --accent-teal: #0f766e;
  --accent-amber: #b7791f;
  --accent-red: #b42318;
  --accent-slate: #40506a;
}
```

## 16. Component Priority

Build in this order:

1. structured extraction for case metadata
2. top status bar
3. daily overview
4. case insight cards
5. case workspace shell
6. Insight Board
7. expression tabs
8. asset panel
9. method workbench formatting
10. 8Q timeline formatting
11. mobile adaptation
12. screenshot QA

Reason:

The first four steps create immediate user-visible value. The later steps add depth and polish.

## 17. Implementation Risk

| Risk | Why It Matters | Mitigation |
| --- | --- | --- |
| Markdown parsing becomes brittle | Hermes content is long and structured by headings | Use exact headings from templates; fail gracefully to raw rendering |
| HTML hides too much | User values quality over brevity | Keep all content in DOM; use progressive disclosure only |
| Summary cards distort meaning | One-sentence Insight may lose nuance | Extract from explicit `一句话 Insight` fields only |
| Mobile becomes unreadable | Tables and long blocks are dense | Use horizontal table scroll and collapsed deep sections |
| Visual polish distracts | Hermes is a serious training tool | Keep restrained palette and minimal motion |

## 18. MVP Acceptance Checklist

The MVP passes if:

1. The first screen shows 3 case cards and source status.
2. Each case's core Insight is visible without deep scrolling.
3. The full Markdown content is still accessible.
4. The user can switch between Read / Reason / Rehearse / Asset.
5. PREP and SCQA are easier to find than in raw Markdown.
6. Case Asset Card is visually reusable.
7. Tables do not break desktop or mobile layout.
8. The page works at 375px, 768px, 1024px, and 1440px.
9. No text overlaps.
10. Renderer tests pass.

## 19. Open Decisions

Before implementation, the user should decide:

1. Should the MVP have a right rail on desktop, or keep only left nav + main content for simplicity?
2. Should all three case Insight Boards be open by default, or only the selected case?
3. Should expression tabs be visible inside each case by default, or behind Rehearse mode?
4. Should Asset summary cards appear once in Daily Overview, or only inside each case?
5. Should V6 be used as the only prototype input, or should V5 also be rendered to test generality?

## 20. Recommended Answers

My recommended choices:

1. Use right rail on desktop, remove it on mobile.
2. Show all three case Insight Boards in overview; inside workspace, open selected case only.
3. Keep expression tabs visible inside each case on desktop; collapse on mobile.
4. Show Asset summary cards in both places: overview summary and full case detail.
5. Prototype with V6 first, then regression render V5.
