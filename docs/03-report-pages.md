---
comments: true
---

# Report pages

Four pages, in this order. The theme in `theme/powerbi-theme.json` and the RAG rules in `docs/05-theme-and-style.md` apply to all of them.

Common conventions:

- **Page size:** 16:9 (1280 × 720) unless you are designing for a specific wallboard.
- **Global slicers** (sync across pages): Entity, Year (from Raised Date), Finding Type, Severity, Risk Theme. Put them in a slim left rail or a top bar and keep the same position on every page.
- **As-at date:** show a small label “As at \<today\>” using the `As At Date` measure, so a printed or exported pack is dated.
- **Tooltips:** every chart should have a report-page or default tooltip that includes Finding Type, Severity, Entity, Owner and Target Date where it is meaningful.
- **Drill-through:** pages 1–3 drill through to a hidden **Finding Detail** layout (specified at the bottom of this file). Page 4 also drills through to the same layout, filtered to the theme or control.
- **No client branding** in the template. Add your organisation header later if you need it.

---

## Page 1 — Executive Summary

**Purpose.** A single leadership view: are we closing findings, is maturity acceptable, and where should attention go this quarter?

### Layout sketch (16:9)

```
┌──────── Title: Continual improvement — executive summary     As at dd mmm yyyy ──┐
│ [Entity] [Year] [Type] [Severity] [Theme]                                         │
├────────┬────────┬────────┬────────┬───────────────────────────────────────────────┤
│ Open   │Overdue │% closed│ Avg    │  Maturity by entity (clustered bar, 1–5)      │
│ findings│findings│on time │days to │                                               │
│        │        │        │ close  │                                               │
├────────┴────────┴────────┴────────┼───────────────────────────────────────────────┤
│ Open findings by type and entity  │  Raised vs closed by month (line + column)    │
│ (stacked bar: type × entity)      │  (Raised = column, Closed = line)             │
├───────────────────────────────────┴───────────────────────────────────────────────┤
│ Open findings by severity (donut or stacked bar)   │  Attention list (table)      │
│                                                    │  overdue / critical /        │
│                                                    │  risk candidates             │
└───────────────────────────────────────────────────────────────────────────────────┘
```

### Cards (KPI row)

| Visual | Measure | RAG |
| --- | --- | --- |
| Open findings | `Open Findings` | Neutral count; optional colour if above a threshold you set |
| Overdue findings | `Overdue Findings` | Green = 0; Amber = 1–4; Red = 5+ (adjust in the theme or conditional formatting) |
| % closed on time | `% Closed On Time` | Green ≥ 80%; Amber 60–79%; Red < 60% |
| Average days to close | `Avg Days to Close` | Green ≤ 45; Amber 46–90; Red > 90 (targets are configurable) |

### Other visuals

| Visual | Fields / measures | Notes |
| --- | --- | --- |
| Clustered bar — maturity by entity | Axis: `Dim Entity[Entity]`; Value: `Avg Maturity Score`; optional reference line at 3 | Sort by `Entity_Sort`. Tooltip: `% Controls Mature`, `Controls Below Target`, `Open NC (maturity fact)` |
| Stacked bar — open findings by type and entity | Axis: Entity; Legend: Finding Type; Value: `Open Findings` | Keep the type colour map in the theme (NC red, Gap orange, OFI amber, OBS slate) |
| Combination — raised vs closed by month | Axis: `Dim Date[YearMonth]` via the active Raised relationship for one series; use the closed-date measures with `USERELATIONSHIP` for the other | Add a tooltip with net movement (`Raised in Period − Closed in Period`) |
| Donut or stacked bar — open findings by severity | Legend: Severity; Value: `Open Findings` | |
| Table — attention list | Finding ID, Title, Type, Severity, Entity, Owner, Target Date, `Days Overdue`, `Is Risk Candidate` | Filter to overdue, or Critical/High and open, or risk candidates. Top N 10 by days overdue. Enable drill-through |

**Filters on this page:** Status is *not* hard-filtered at page level (cards already handle open vs closed). Sync slicers as above.

---

## Page 2 — Findings by Type

**Purpose.** Break the portfolio down by type, severity and age, then drill to the list.

### Layout sketch

```
┌──────── Title: Findings by type                                                      ┐
│ Slicers (synced)                                                                      │
├───────────────────────────────┬───────────────────────────────────────────────────────┤
│ Cards: Open NC | Open OFI |   │  Matrix: Type (rows) × Severity (columns) × Entity    │
│ Open Gap | Open OBS           │  values = Open Findings; subtotals on                 │
├───────────────────────────────┴───────────────────────────────────────────────────────┤
│ Ageing of open items (stacked bar)                                                    │
│ Axis: Ageing bucket (0–30, 31–60, 61–90, Over 90)  Legend: Type  Value: Open Findings │
├───────────────────────────────────────────────────────────────────────────────────────┤
│ Detail table (all findings in context)                                                │
│ ID, Title, Type, Severity, Control, Entity, Owner, Raised, Target, Status, Age days   │
└───────────────────────────────────────────────────────────────────────────────────────┘
```

### Visuals

| Visual | Fields / measures | Notes |
| --- | --- | --- |
| Four cards | `Open NC`, `Open OFI`, `Open Gap`, `Open OBS` | Also show a small comparison to closed counts in the tooltip |
| Matrix | Rows: Finding Type; Columns: Severity; Values: `Open Findings`; Show values as: optional % of row | Add Entity as a second row level, or as a slicer only, if the matrix becomes crowded. Conditional format cells on count (white → navy) |
| Stacked bar — ageing | Axis: `Ageing Bucket` (sort with `Ageing Bucket Sort`); Legend: Finding Type; Value: `Open Findings` | Closed items are excluded by the measure. Over-90 should visually dominate if the “slow change” problem is present |
| Detail table | See sketch | Conditional format: Status, Severity, Ageing. Right-click drill-through to Finding Detail |

**Page or visual filter:** none required; measures already distinguish open vs closed. Offer a Status slicer on this page only if reviewers want to inspect closed items in the table.

---

## Page 3 — Ownership

**Purpose.** Show whether named owners are closing work to target. This is the page that makes slow change visible.

### Layout sketch

```
┌──────── Title: Ownership and accountability                                          ┐
│ Slicers (synced)                                                                      │
├────────────────────────────────────┬──────────────────────────────────────────────────┤
│ Owner scorecard (table)            │  Top 10 overdue owners (bar)                     │
│ Owner, Role, Entity, Open,         │  Value: Overdue Findings                         │
│ Overdue, % on time, Avg days       │  Axis: Owner Name                                │
├────────────────────────────────────┴──────────────────────────────────────────────────┤
│ Overdue findings by owner and type (stacked bar)                                      │
├────────────────────────────────────┬──────────────────────────────────────────────────┤
│ Ageing by owner (matrix)           │  Escalation table: overdue > 60 days             │
│ Owner × Ageing bucket              │  Owner, Line manager, Finding, Target, Days over │
└────────────────────────────────────┴──────────────────────────────────────────────────┘
```

### Visuals

| Visual | Fields / measures | Notes |
| --- | --- | --- |
| Owner scorecard table | `Dim Owner[Owner_Name]`, Role, Entity, `Open Findings`, `Overdue Findings`, `Owner % On Time`, `Avg Days to Close`, `Closed Findings` | Conditional format `% On Time` and Overdue with the same RAG as page 1. Sort by Overdue desc, then Open desc |
| Top 10 overdue owners | Axis: Owner Name; Value: `Overdue Findings` | Filter out zeros. This is the “change is not happening” visual |
| Stacked bar — overdue by owner and type | Axis: Owner; Legend: Type; Value: `Overdue Findings` | |
| Matrix — ageing by owner | Rows: Owner; Columns: Ageing bucket; Values: `Open Findings` | Colour the Over 90 column red when > 0 |
| Escalation table | Owner, Line Manager, Finding ID, Title, Entity, Target Date, `Days Overdue` | Visual-level filter: `Days Overdue` ≥ 60 (threshold is configurable; see risk-candidate rules). Intended as a pack you can export for the management review |

Do not use “unassigned” as a hidden bucket. Findings with a missing owner should appear as `(Unassigned)` so the gap is visible.

---

## Page 4 — Risk Heat Map and Risk Candidates

**Purpose.** Aggregate findings into strategic risk themes, place each theme on a likelihood × impact heat map, and list which themes or controls are **candidates** for the risk register. Candidates are a recommendation, not an automatic register entry. See `docs/04-risk-candidate-rules.md`.

### Layout sketch

```
┌──────── Title: Risk heat map and risk candidates                                     ┐
│ Slicers (synced) + optional “Candidates only” slicer                                  │
├─────────────────────────────────────┬─────────────────────────────────────────────────┤
│ Heat map matrix                     │  Cards: Candidate themes | Candidate findings   │
│ Rows: Risk Theme                    │         | Themes with no linked risk            │
│ Columns: Impact (1–5)  — or a 5×5   │                                                 │
│ of Likelihood (rows) × Impact (cols)│                                                 │
│ Values: Heat Map Score / count      │                                                 │
│ Colour: RAG bands                   │                                                 │
├─────────────────────────────────────┴─────────────────────────────────────────────────┤
│ Candidate table                                                                       │
│ Theme or Control, Entities affected, Open NC, Repeat flag, Age flag, Maturity flag,   │
│ Cluster flag, Candidate Score, Linked Risk, Recommended action                        │
├───────────────────────────────────────────────────────────────────────────────────────┤
│ Supporting bar: open findings by theme (stacked by type)                              │
└───────────────────────────────────────────────────────────────────────────────────────┘
```

### Heat map construction

Two valid layouts; pick one and stay consistent.

**Option A (recommended for executives).** One row per risk theme. Columns: `Derived Likelihood`, `Derived Impact`, `Heat Map Score`, `Open Findings`, `Open NC`, `Is Risk Candidate`, `Linked Risk Count`. Conditional-format the score column on the 1–25 scale (see RAG in the theme document). This is easier to read than a sparse 5×5.

**Option B (classic 5×5).** Matrix with Likelihood 1–5 on rows (or columns) and Impact 1–5 on the other axis. Value = count of themes (or `Heat Map Score`) falling in that cell. Put a theme table next to it so a cell can be selected and the list filters. Derived likelihood and impact come from the measures in `dax/measures.dax`, not from a manual plot unless you override them.

Derived axes (defaults, documented in the rules file):

- **Likelihood** rises with recurrence (open findings in the theme, and whether the same NC appears in two or more entities).
- **Impact** rises with severity (weighted: Critical 4, High 3, Medium 2, Low 1) and with low maturity.

### Candidate table

| Column | Source |
| --- | --- |
| Risk Theme (and/or Control ID + name) | Dimensions |
| Entities affected | `Entities With Open NC` |
| Open NC / Open OFI / Open OBS | Type measures |
| Repeat NC (≥ 2 entities) | `Flag Repeat NC` |
| Open > 90 days or overdue | `Flag Ageing` |
| Maturity ≤ 2 and open NC | `Flag Low Maturity NC` |
| ≥ 3 OFI/OBS in theme | `Flag Cluster` |
| Candidate score (0–100) | `Risk Candidate Score` |
| Already on register? | `Linked Risk` from the maturity fact, or a count |
| Recommended action | `Candidate Recommendation` (text measure) |

A theme or control is a candidate when **any** of the four flags is true. Score is a weighted combination, so a theme can be a mild or a strong candidate. Sort this table by score descending.

**Governance note on the page itself.** Add a static text box:

> Risk-candidate flags are decision support for the risk workshop. Promoting a candidate to the risk register remains a management decision, with an owner, treatment and review date.

---

## Hidden page — Finding Detail (drill-through)

Create a hidden page with drill-through filters on `Finding_ID` (and keep Entity, Theme and Control as extra drill-through fields so cards on pages 1–4 can also land here).

Layout: a single-finding card (title, type, severity, status, dates, owner, line manager, control, theme, description, root cause) plus a small context visual (“other open findings on this control / this owner / this theme”).

Enable “Keep all filters” if you want the source slicers to travel with the drill-through; otherwise leave it off so the context visuals can show the wider picture.

---

## Interaction and usability notes

- Turn off cross-highlight on the KPI cards so selecting a bar does not blank the cards unexpectedly; use cross-filter from the heat map and type visuals onto the tables.
- Use a tool-tip page (optional) that shows the top five open findings in the hovered context.
- Bookmark a “reset slicers” button if you have many synced slicers.
- Export: the owner scorecard and the escalation table should be easy to export to Excel for the management review pack.
