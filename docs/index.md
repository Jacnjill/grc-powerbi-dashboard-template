---
comments: true
hide:
  - footer
---

# GRC Power BI dashboard template

A reusable Power BI template for an **executive ISO 27001 continual improvement and internal audit dashboard**, fed from a single Excel workbook (typically a *Continual Improvement Plan*).

This site is the documentation for a **design and build kit**, not a pre-built `.pbix`. Use it to stand up a four-page executive report from a well-structured workbook, then point the same model at your own data.

All placeholders are generic (`<Entity>`, `<Country>`, `<Owner>`). There is no client or organisation-specific content. Every sample record is clearly marked as fictional.

## What you get

- A [source workbook specification](01-source-workbook-spec.md) and a column-mapping table to complete against your own headings
- A [star-schema data model](02-data-model.md) and example Power Query (M) scripts
- A full [DAX measure set](downloads.md)
- A [four-page report specification](03-report-pages.md)
- Configurable [risk-candidate rules](04-risk-candidate-rules.md) and a heat-map method
- An [executive colour theme](05-theme-and-style.md), including a valid Power BI theme file
- [Fictional sample data](downloads.md) so you can prototype before connecting a live workbook
- A step-by-step [Desktop build, publishing and reuse checklist](06-build-checklist.md)

## Quick start

1. Download the [sample workbook](downloads/Continual_Improvement_Plan_SAMPLE.xlsx) (or clone the [repository](https://github.com/Jacnjill/grc-powerbi-dashboard-template)).
2. Fill in the **column-mapping table** in the [source workbook specification](01-source-workbook-spec.md) against your real workbook.
3. Open Power BI Desktop, create the parameters from the [Power Query examples](downloads.md), and add the remaining queries.
4. Paste the measures from [`measures.dax`](downloads/measures.dax) into the model.
5. Import [`powerbi-theme.json`](downloads/powerbi-theme.json) (**View → Browse for themes**).
6. Build the four report pages from the [page specification](03-report-pages.md).
7. Work through the [build checklist](06-build-checklist.md) before publishing.

If your column names differ, keep the mapping table as the single source of truth and rename columns in Power Query. Leave the DAX names and page specifications unchanged where you can.

## What the dashboard is for

Leadership should be able to see, at a glance:

- How many findings are open, overdue and closed on time
- Where findings sit by type (nonconformity, opportunity for improvement, gap, observation), severity and entity
- Whether named owners are closing actions to target — a direct measure of whether change is actually happening
- Which strategic risk themes are accumulating findings, and which are credible **candidates** for the risk register
- How control maturity compares across entities, and where low maturity coincides with open nonconformities

ISO 27001 asks whether a process exists. This dashboard is designed to show whether the process is changing anything.

## Design principles

- **Generic and reusable.** Swap the workbook path, sheet names and column map. Leave measures and page layouts alone where possible.
- **Star schema.** Fact tables connect through shared dimensions (Date, Control, Entity, Owner, Risk Theme). Do not relate the two fact tables to each other.
- **Evidence over assertion.** Measures prefer dates and status over narrative fields.
- **Promotion, not automation.** Risk-candidate flags are decision support. A person still decides whether to raise an item on the risk register.

## Finding types

| Code | Meaning |
| --- | --- |
| NC | Nonconformity — a control or requirement is not met |
| OFI | Opportunity for improvement — the control works, but could be stronger |
| Gap | A required control or process is missing or incomplete |
| OBS | Observation — a noteworthy point that is not (yet) an NC or OFI |

These codes are the template default. If your workbook uses different labels, map them in Power Query to these four values so the measures keep working.

## Licence and disclaimer

Released under the [MIT Licence](https://github.com/Jacnjill/grc-powerbi-dashboard-template/blob/main/LICENSE).

This template is a technical starting point for a management-system dashboard. It is not legal, audit or certification advice. Sample data is entirely fictional and must not be used as live evidence.

Comments on each page of this site are stored as [GitHub Discussions](https://github.com/Jacnjill/grc-powerbi-dashboard-template/discussions) (via giscus).
