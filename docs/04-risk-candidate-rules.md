---
comments: true
---

# Risk-candidate rules

These rules decide when a **control** or a **strategic risk theme** is a good candidate to discuss as a risk — typically at a risk workshop or management review — rather than leaving it only as an audit finding.

They are **decision support**, not an automatic posting to the risk register. A candidate still needs an owner, a treatment, a likelihood and impact that management accepts, and a review date, before it becomes a live risk.

All thresholds below are parameters. Keep the numeric values in one place in DAX (`_Param *` measures in `dax/measures.dax`) so you can change them without rewriting the rules.

## Why findings are not automatically risks

A finding is evidence about a control at a point in time. A risk is an uncertain event or condition that could affect objectives, with a treatment plan. Promote a finding (or a cluster of them) when the evidence suggests the issue is **systemic**, **persistent**, or **material** — not when it is a one-off documentation slip that is already being closed.

## The four default criteria

A control or theme is a **risk candidate** if **any** of the following is true. The candidate score (0–100) then reflects how many criteria fire and how severe they are.

### 1. Repeat nonconformities across entities

**Rule.** There is an open or in-progress **NC** against the same `Control_ID` (theme-level: against controls in the same theme) in **two or more** entities.

**Default threshold.** `≥ 2` entities (`_Param Repeat Entity Threshold`).

**Rationale.** The same NC in more than one `<Entity>` is a strong signal that the issue is in the management system, not in a single local process. These are usually the best candidates.

**Flag measure.** `Flag Repeat NC`

### 2. Persistent or overdue findings

**Rule.** There is at least one open or in-progress **NC** that is either:

- past its `Target_Date` (overdue), or
- open for longer than **90 days** from `Raised_Date`, even if the target is still in the future.

**Default thresholds.** Overdue = target date &lt; today; ageing = **90** days (`_Param Persistent Days`).

**Rationale.** Slow closure is itself a risk: the original control weakness remains, and the improvement process is not working at the pace the ISMS claims.

**Flag measure.** `Flag Ageing`

You may tighten this to “any finding type, not only NC” if your appetite is low. The default stays on NCs so observations and OFIs do not inflate the register.

### 3. Low maturity with an open nonconformity

**Rule.** For a given control and entity, **Maturity ≤ 2** (Documented or Informal) **and** `Open_NC ≥ 1`.

**Default threshold.** Maturity **≤ 2** (`_Param Low Maturity`).

**Rationale.** A documented-but-not-operated control that already has an NC is exactly the “compliant on paper, not in practice” pattern. At theme level, the flag fires if any in-scope control–entity pair meets the rule.

**Flag measure.** `Flag Low Maturity NC`

This is the one rule that needs the Control Maturity fact. If maturity data is missing for a control, do not fire the flag; report the gap in a data-quality measure instead.

### 4. Clustered opportunities and observations

**Rule.** There are **three or more** open or in-progress **OFI** or **OBS** (combined) in the same risk theme.

**Default threshold.** `≥ 3` (`_Param Cluster Threshold`). Gaps may be included by adding them to the measure; the default leaves Gaps out, because a Gap is often already treated as closer to an NC and should be considered under rules 1–3 if it is one.

**Rationale.** A single OFI is a local improvement. A cluster on one theme usually means a systemic weakness that nobody has yet called a nonconformity.

**Flag measure.** `Flag Cluster`

## Candidate score

The score is a 0–100 index used to sort the candidate table, not a likelihood or impact rating.

Default weights (must sum to 100):

| Criterion | Weight | Additional severity bump |
| --- | --- | --- |
| Repeat NC across entities | 35 | +5 if 3+ entities, +5 if any Critical NC |
| Persistent / overdue NC | 25 | +5 if any item is more than 180 days open or more than 60 days overdue |
| Low maturity + open NC | 25 | +5 if any maturity is 1 (Informal) |
| Clustered OFI / OBS | 15 | +5 if 6 or more in the theme |

Capped at 100. A score of 0 means no criterion fired. Interpret roughly as:

| Score | Meaning |
| --- | --- |
| 0 | Not a candidate under current rules |
| 1–40 | Mild candidate — discuss, often treat as a grouped action rather than a new risk |
| 41–70 | Firm candidate — take to the risk workshop with a proposed owner |
| 71–100 | Strong candidate — typically already overdue or repeating; escalate if not already on the register |

The text measure `Candidate Recommendation` returns one of: `Not a candidate`, `Discuss as grouped action`, `Workshop — propose risk`, `Escalate — strong candidate`.

## Likelihood and impact for the heat map

Do not confuse the candidate **score** with heat-map **likelihood** and **impact**. The heat map is a 5×5 plot of themes, using derived values so a first draft exists even before the risk workshop.

### Derived likelihood (1–5)

Based on recurrence and persistence of open items in the theme:

| Condition (evaluated top-down; first match wins) | Likelihood |
| --- | --- |
| Repeat NC in 3 or more entities, or 5+ open NCs in the theme | 5 |
| Repeat NC in 2 entities, or 3–4 open NCs, or any NC open > 90 days | 4 |
| 1–2 open NCs, or a cluster of OFI/OBS (≥ 3) | 3 |
| Open findings exist, but no NC and no cluster | 2 |
| No open findings in the theme | 1 |

If you prefer a formula instead of bands: start at 1, add 1 for any open finding, add 1 for any open NC, add 1 for repeat-entity NCs, add 1 for persistent/overdue NCs, cap at 5.

### Derived impact (1–5)

Based on severity mix and the worst relevant maturity:

| Condition (top-down) | Impact |
| --- | --- |
| Any open Critical finding, or maturity 1 with an open NC | 5 |
| Any open High finding, or maturity ≤ 2 with an open NC | 4 |
| Medium is the highest open severity, or 3+ open findings | 3 |
| Only Low open findings | 2 |
| No open findings | 1 |

Alternatively, a weighted severity average (Critical 5, High 4, Medium 3, Low 2) rounded to the nearest integer, then raised by 1 if the low-maturity-plus-NC flag is true, capped at 5.

`Default_Likelihood` and `Default_Impact` on Dim Risk Theme are **planning values for the register**, not the derived heat-map axes. Use them as a starting point in the workshop if you disagree with the derived figures.

### Heat map score

`Heat Map Score = Derived Likelihood × Derived Impact` (range 1–25).

| Score | Band | Colour |
| --- | --- | --- |
| 1–4 | Low | Green |
| 5–9 | Moderate | Amber |
| 10–16 | High | Orange / dark amber |
| 17–25 | Extreme | Red |

These bands should match your organisation’s risk matrix if you already have one. Change the breaks once, in DAX and in the theme documentation.

## Already on the register

If `Linked_Risk` is populated on the maturity fact (or you later add a risk-register id on the finding), the candidate is labelled **Already on register** rather than “new candidate”. Keep it visible: the workshop should check that the treatment is actually moving, especially when flags are still firing.

## Promoting a candidate — governance

When a candidate is accepted:

1. Assign a risk owner (often the theme owner, not necessarily the finding owner).
2. Agree likelihood and impact (start from the derived values; record any override and the reason).
3. Record the treatment, due date and expected evidence.
4. Link the risk id back to the Control Maturity sheet (`Linked_Risk`) and, if you use it, to the finding.
5. Leave the original findings open until their own closure criteria are met. Closing a finding because a risk was raised hides the control failure.
6. Review overdue treatments at the same forum that reviews overdue findings, so the slow-change problem cannot be moved to a different register and forgotten.

When a candidate is rejected, record a short reason (for example “single-site issue, already in closure, residual accepted”). That record belongs in the workshop minutes, not in this dashboard, unless you add an exclusions table later.

## Tuning the rules

Change the `_Param *` measures first, then review the sample workbook to see whether the flags still tell a sensible story. Signs you need to retune:

- Almost every theme is a candidate — thresholds are too tight, or the source data is messy (status not closed, dates missing).
- Almost nothing is a candidate, despite known systemic issues — repeat-entity matching may be failing on inconsistent `Control_ID` or `Entity` spellings.
- Clusters of OFIs never appear — check that type labels were mapped to `OFI` and `OBS`.

Revisit the parameters at least at each management review.
