# GRC Power BI dashboard template

A reusable Power BI template for an **executive ISO 27001 continual improvement and internal audit dashboard**, fed from a single Excel workbook (typically a *Continual Improvement Plan*).

**Documentation site:** [https://jacnjill.github.io/grc-powerbi-dashboard-template/](https://jacnjill.github.io/grc-powerbi-dashboard-template/)

This repository is a **design and build kit**, not a pre-built `.pbix`. It gives you:

- A source workbook specification and a column-mapping table to complete against your own headings
- A star-schema data model and example Power Query (M) scripts
- A full DAX measure set
- A four-page report specification
- Configurable risk-candidate rules and a heat-map method
- An executive colour theme, including a valid Power BI theme file
- Fictional sample data so you can prototype before connecting a live workbook
- A step-by-step Desktop build, publishing and reuse checklist

All placeholders are generic (`<Entity>`, `<Country>`, `<Owner>`). There is no client or organisation-specific content. Every sample record is clearly marked as fictional.

## Quick start

1. Clone this repository, or browse the [documentation site](https://jacnjill.github.io/grc-powerbi-dashboard-template/).
2. Open `sample-data/Continual_Improvement_Plan_SAMPLE.xlsx` to see the expected shape (four tabs, fictional data only).
3. Copy the **column-mapping table** in `docs/01-source-workbook-spec.md` and fill it in against your real workbook.
4. Open Power BI Desktop, create the parameters from `powerquery/01-parameters.m`, then add the remaining queries in `powerquery/`.
5. Paste the measures from `dax/measures.dax` into the model.
6. Import `theme/powerbi-theme.json` (**View → Browse for themes**).
7. Build the four report pages from `docs/03-report-pages.md`.
8. Work through `docs/06-build-checklist.md` before publishing.

If your column names differ, keep the mapping table as the single source of truth and rename columns in Power Query. Leave the DAX names and page specifications unchanged where you can.

## Repository map

| Path | Purpose |
| --- | --- |
| `docs/` | Documentation (also published as the GitHub Pages site) |
| `docs/01-source-workbook-spec.md` | Expected Excel tabs and columns, plus a mapping table to fill in |
| `docs/02-data-model.md` | Star schema, relationships, Power Query steps, mermaid ER diagram |
| `docs/03-report-pages.md` | Executive Summary, Findings by Type, Ownership, Risk Heat Map |
| `docs/04-risk-candidate-rules.md` | Configurable criteria, scoring, heat-map axes, promotion to the risk register |
| `docs/05-theme-and-style.md` | Executive palette, RAG rules and typography |
| `docs/06-build-checklist.md` | Desktop build, publishing and customisation guide |
| `powerquery/` | Example M scripts (parameters, facts, dimensions, date table) |
| `dax/measures.dax` | Full measure set with comments |
| `theme/powerbi-theme.json` | Importable Power BI theme |
| `sample-data/` | Sample workbook and CSV copies (fictional) |
| `scripts/generate_sample_data.py` | Regenerates the sample workbook and CSVs |

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

## Finding types (abbreviations)

| Code | Meaning |
| --- | --- |
| NC | Nonconformity — a control or requirement is not met |
| OFI | Opportunity for improvement — the control works, but could be stronger |
| Gap | A required control or process is missing or incomplete |
| OBS | Observation — a noteworthy point that is not (yet) an NC or OFI |

These codes are the template default. If your workbook uses different labels, map them in Power Query to these four values so the measures keep working.

## Documentation site

The Markdown in `docs/` is published with MkDocs Material via GitHub Actions to GitHub Pages. Each page has a comment box (giscus) that stores comments as [Discussions](https://github.com/Jacnjill/grc-powerbi-dashboard-template/discussions) in this repository.

To preview the site locally:

```bash
pip install -r requirements-docs.txt
mkdocs serve
```

## Automatic documentation deploys

The documentation site is published to GitHub Pages. The initial site is built with MkDocs Material and published from the `gh-pages` branch.

A GitHub Actions workflow that rebuilds the site on every push to `main` is provided as [`github-actions-docs.yml`](github-actions-docs.yml). It could not be placed in `.github/workflows/` at publish time because the token used to push this repository does not have the `workflow` scope. To enable automatic deploys:

1. Copy `github-actions-docs.yml` to `.github/workflows/docs.yml`.
2. In the repository settings, set Pages **Source** to **GitHub Actions** (or leave it on the `gh-pages` branch if you prefer to deploy the built site yourself).

## Prerequisites

- Power BI Desktop (current monthly release)
- The source Excel workbook, or the sample file in `sample-data/`
- Permission to publish to a Power BI workspace, if you intend to share the report

Python 3 with `openpyxl` is optional and is only needed if you want to regenerate the sample workbook.

## Licence and disclaimer

Released under the MIT Licence (see `LICENSE`).

This template is a technical starting point for a management-system dashboard. It is not legal, audit or certification advice. Sample data is entirely fictional and must not be used as live evidence.
