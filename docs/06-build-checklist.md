---
comments: true
---

# Build checklist

Follow this once to stand the report up in Power BI Desktop, then use the reuse section when you point it at a different workbook.

Tick as you go. The sample workbook in `sample-data/` is the safest first pass; switch the path parameter to a live file only after the model and pages look right.

## A. Prepare the source

- [ ] Read `docs/01-source-workbook-spec.md` and fill in the **column-mapping table** against your workbook (or confirm the sample already matches the canonical names).
- [ ] Confirm the workbook has the two required tabs (Internal Audit Findings, Control Maturity) and, ideally, Risk Theme Mapping and Owners.
- [ ] Check there is **no banner row** above the header, no merged cells in the used range, and that dates are true Excel dates.
- [ ] Harmonise entity spellings (`UK` vs `United Kingdom`) and type/status synonyms, or plan to map them in Power Query.
- [ ] If the live file will be refreshed by other people, place it on SharePoint or OneDrive, not a personal drive letter.

## B. Create the Power BI file

- [ ] Open Power BI Desktop and save the file as `grc-continual-improvement-dashboard.pbix` (or your own generic name) **outside** this repository. `.pbix` files are git-ignored on purpose.
- [ ] **File → Options → Current file → Data load**: disable auto date/time tables (you will use Dim Date).
- [ ] **View → Browse for themes** and import `theme/powerbi-theme.json`. Confirm the theme name appears.

## C. Parameters and queries

- [ ] **Home → Transform data → Manage parameters → New parameter** for each entry in `powerquery/01-parameters.m`:
  - `pWorkbookPath` (Text) — full path or SharePoint URL of the Excel file
  - `pFindingsSheet` (Text) — default `Internal Audit Findings`
  - `pMaturitySheet` (Text) — default `Control Maturity`
  - `pThemesSheet` (Text) — default `Risk Theme Mapping`
  - `pOwnersSheet` (Text) — default `Owners`
  - `pStartDate` / `pEndDate` (Date) — optional; otherwise the date table script derives them
- [ ] Create a blank query for each script in `powerquery/`, paste the M, and name the queries exactly as in `docs/02-data-model.md` (`Fact Findings`, `Fact Control Maturity`, `Dim Date`, `Dim Control`, `Dim Entity`, `Dim Owner`, `Dim Risk Theme`).
- [ ] Point any staging queries at the parameters, not at hard-coded paths.
- [ ] For Control Maturity, confirm the entity **prefix list** in `03-control-maturity.m` matches your column prefixes. Adjust and close the unpivot preview: you should see one row per control per entity, with `Maturity`, `Open_NC`, `Open_OFI` and `Linked_Risk` as columns.
- [ ] Set data types (Date, Whole Number, Text) and rename any remaining source columns to canonical names.
- [ ] Disable load on staging / helper queries. Enable load on the two facts and five dimensions.
- [ ] **Close & Apply**. Fix any type or relationship errors before going further.

## D. Model view

- [ ] Create the relationships listed in `docs/02-data-model.md`. Only the Raised Date relationship to Dim Date should be active; Target Date and Closed Date are inactive.
- [ ] Mark `Dim Date` as a date table (**Table tools → Mark as date table**), using the `Date` column.
- [ ] Hide technical foreign keys from Report view, except `Finding_ID` if you want it on drill-through.
- [ ] Confirm there is **no** relationship between the two fact tables.

## E. Measures and columns

- [ ] Create a measures table (empty table named `_Measures` is a common pattern) and paste groups from `dax/measures.dax` into display folders: `_Parameters`, `_Base`, `Ageing`, `Types`, `Maturity`, `Ownership`, `Risk`.
- [ ] Add the calculated columns described in the DAX file (ageing bucket, overdue flag, closed-on-time) if you prefer columns over the equivalent measures for slicers and sorts.
- [ ] Check the parameter measures (`_Param Repeat Entity Threshold`, `_Param Persistent Days`, `_Param Low Maturity`, `_Param Cluster Threshold`, and the KPI RAG thresholds) and change them if your policy differs from the defaults.
- [ ] Put a few slicers on a scratch page and sanity-check:
  - `Open Findings` + `Closed Findings` equals `Findings Count` (when no status filter is applied).
  - `Overdue Findings` only includes open or in-progress items with `Target_Date` before today.
  - `% Closed On Time` only uses closed rows and compares `Closed_Date` to `Target_Date`.
  - Maturity averages change when you slice Entity, and stay blank rather than zero when a context has no rows.
  - Risk-candidate flags on the sample data fire for repeat NCs, aged NCs, low-maturity + NC, and clustered OFI/OBS (the sample is written so each rule has at least one hit).

## F. Report pages

Build in this order, following `docs/03-report-pages.md`:

- [ ] Page 1 — Executive Summary (KPI cards, maturity by entity, type × entity, raised vs closed, attention list).
- [ ] Page 2 — Findings by Type (type cards, type × severity matrix, ageing bar, detail table).
- [ ] Page 3 — Ownership (scorecard, top overdue owners, escalation table with line manager).
- [ ] Page 4 — Risk Heat Map and Risk Candidates (heat map or theme score table, candidate table, findings-by-theme bar, governance note).
- [ ] Hidden page — Finding Detail, with drill-through on `Finding_ID` (plus Control, Entity, Theme if you want).
- [ ] Sync the global slicers (Entity, Year, Type, Severity, Theme) across pages 1–4.
- [ ] Apply RAG conditional formatting from `docs/05-theme-and-style.md`. Lock NC / OFI / Gap / OBS colours so they do not shuffle.
- [ ] Add the “As at” label and a “Reset slicers” bookmark if you have more than two slicers.
- [ ] Turn off visual headers (filter / focus icons) on the executive page if you will present it full-screen.

## G. Quality pass

- [ ] Refresh from the sample file and from a copy of your live file (data removed or anonymised if needed) and compare counts to Excel (`COUNTA` / `COUNTIFS` on open, overdue, closed).
- [ ] Test a year slicer and a month on the raised-versus-closed visual: closed counts must use the inactive Closed Date relationship, not Raised Date.
- [ ] Test drill-through from a bar, a matrix cell and a table row.
- [ ] Publish a test to a non-production workspace and open the report in the service: confirm the theme, the date table and the slicer sync survived publish.
- [ ] If the source is on SharePoint, configure a scheduled refresh and confirm the gateway or cloud connection succeeds.
- [ ] Remove any remaining sample-only columns (`Data_Flag`) from visuals. Keep them in the model only if you need to stop sample and live rows being mixed.

## H. Publish

- [ ] Agree the workspace, audience and whether the report is a workspace app or a shared report.
- [ ] Sensitivity label and endorsement (if your tenant uses them): this is typically **internal** management information, not public.
- [ ] Set refresh (daily is usually enough for an audit tracker; do not promise real-time).
- [ ] Share with view access first. Keep build permission to the people who own the ISMS reporting.
- [ ] Add a short “how to read this” note on page 1 or in the workspace description, including the point that risk candidates are not automatically raised on the register.

## Reuse and customisation

To reuse this as a template for another programme or another entity set:

1. **Copy the `.pbix`** (once you have one) or start from this repository again.
2. **Change `pWorkbookPath`** and, if needed, the four sheet-name parameters.
3. **Update the column map** and the rename steps in Power Query. Do not rename measures to match an idiosyncratic source heading.
4. **Update the entity prefix list** in the maturity unpivot. Add or remove entities in Dim Entity, including a `Group` row if you have central owners.
5. **Retune `_Param *` measures** if the other programme uses a different maturity scale, SLA or clustering rule. Record the values you chose in the management-review pack.
6. **Replace the theme** only if the other programme already has a mandated palette; otherwise keep this one so RAG language stays consistent.
7. **Do not paste live data into the sample workbook.** Keep `sample-data/` fictional so it remains a safe demo.
8. If you need a fifth page (for example incidents or supplier findings), add a new fact on the same dimensions. Do not merge those rows into Fact Findings unless they truly share the same grain and type list.

## Regenerating the sample data

From the repository root, with Python 3 and `openpyxl` installed:

```bash
python3 scripts/generate_sample_data.py
```

This overwrites `sample-data/Continual_Improvement_Plan_SAMPLE.xlsx` and the CSV copies. All generated rows are flagged `Fictional sample`.

## Common problems

| Symptom | Likely cause | What to do |
| --- | --- | --- |
| Closed-in-month is always blank or equals raised-in-month | Closed Date relationship is missing or still inactive in the measure | Use `USERELATIONSHIP` as in `Closed Findings In Period` |
| Maturity does not filter by theme | Dim Risk Theme is not related via Dim Control | Add the theme-to-control relationship |
| Unpivot exploded into unreadable columns | Unexpected prefix or a comment column in the block | Restrict the unpivot to known prefixes; park odd columns in a leftovers query |
| `% Closed On Time` is blank | No closed rows, or `Closed_Date` stored as text | Set the type to Date; check Status mapping |
| Repeat-NC flag never fires | Entity names differ between Findings and Maturity (`UK` vs `United Kingdom`) | Harmonise in Power Query using Dim Entity |
| Refresh fails for colleagues | Path is a local `C:\Users\...` file | Move the workbook to SharePoint and change the parameter |
| Theme import rejected | Invalid JSON | Re-validate `theme/powerbi-theme.json` (no comments, no trailing commas) |
