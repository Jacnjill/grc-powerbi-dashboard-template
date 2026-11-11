---
comments: true
---

# Source workbook specification

The dashboard is designed around one Excel workbook, typically called **Continual Improvement Plan**. The template expects **four worksheets**. Two are required for the core model; two are strongly recommended and are used for the risk heat map and ownership page.

All names below are **canonical names**. Your live workbook may differ. Use the [column-mapping table](#column-mapping-table) to record the actual headings and rename to these names in Power Query.

Placeholder tokens used in this kit:

- `<Entity>` — the organisational unit the finding or maturity score belongs to (country, region, business unit or legal entity)
- `<Country>` — used in the sample as the entity grain (United Kingdom, Spain, France, Germany). Replace with whatever grain you report on.
- `<Owner>` — the person accountable for closing the finding
- `<Control ID>` — an ISO 27001:2022 Annex A control identifier such as `8.5`

Sample files in `sample-data/` are **fictional** and labelled as such in every row (`Data_Flag = Fictional sample`).

---

## Sheet 1 — Internal Audit Findings (required)

This is the main fact table. One row equals one finding.

| Canonical column | Type | Required | Notes |
| --- | --- | --- | --- |
| Finding_ID | Text | Yes | Unique identifier, for example `IA-2026-014` |
| Finding_Title | Text | Yes | Short name shown in tables and tooltips |
| Finding_Type | Text | Yes | One of `NC`, `OFI`, `Gap`, `OBS` (see README) |
| Severity | Text | Yes | One of `Critical`, `High`, `Medium`, `Low` |
| Control_ID | Text | Yes | ISO 27001:2022 Annex A id, for example `5.19` or `8.8` |
| Entity | Text | Yes | `<Entity>` / `<Country>` the finding was raised against |
| Owner_ID | Text | Yes | Key to the Owners sheet |
| Owner_Name | Text | No | Convenience copy; the Owners dimension is authoritative |
| Raised_Date | Date | Yes | Date the finding was raised |
| Target_Date | Date | Yes | Agreed closure date |
| Status | Text | Yes | One of `Open`, `In Progress`, `Closed` |
| Closed_Date | Date | Conditional | Required when Status = `Closed`; leave blank otherwise |
| Risk_Theme_ID | Text | Yes | Key to the Risk Theme Mapping sheet (or a theme code you maintain) |
| Risk_Theme | Text | No | Convenience copy of the theme name |
| Description | Text | No | Longer narrative; useful in tooltips and drill-through |
| Root_Cause | Text | No | If captured |
| Source | Text | No | For example `Internal audit`, `Surveillance audit`, `Management review`, `Incident review` |
| Auditor | Text | No | Person or team who raised it |
| Data_Flag | Text | Sample only | In the sample file this is always `Fictional sample`. Remove or ignore in live use. |

**Validation rules (recommend enforcing in Excel or Power Query):**

- `Finding_ID` is unique and not blank.
- `Finding_Type`, `Severity` and `Status` use only the allowed values (or a documented synonym that you map).
- `Closed_Date` is blank if Status is not `Closed`, and is on or after `Raised_Date`.
- `Target_Date` is on or after `Raised_Date`.
- Every `Control_ID` exists in Annex A (or in your Statement of Applicability).
- Every `Owner_ID` exists on the Owners sheet.
- Every `Risk_Theme_ID` exists on the Risk Theme Mapping sheet.

---

## Sheet 2 — Control Maturity (required)

One **row per control**. Maturity and related evidence are **repeated as country (or entity) blocks** side by side. This is the layout most improvement-plan workbooks already use. Power Query unpivots the blocks into a tall fact table (one row per control per entity). See `powerquery/03-control-maturity.m` and `docs/02-data-model.md`.

### Shared columns (left-hand side)

| Canonical column | Type | Required | Notes |
| --- | --- | --- | --- |
| Control_ID | Text | Yes | ISO 27001:2022 Annex A id |
| Control_Name | Text | Yes | Short control title |
| Annex_Category | Text | No | `Organizational`, `People`, `Physical` or `Technological` |

### Repeated block for each `<Country>` / `<Entity>`

Repeat the following columns once per entity. In the sample the prefixes are `UK_`, `Spain_`, `France_` and `Germany_`. Replace prefixes with your own entity codes, and update the unpivot list in Power Query.

| Canonical suffix | Type | Required | Notes |
| --- | --- | --- | --- |
| `_Maturity` | Whole number | Yes | Integer 1–5 (see scale below) |
| `_Open_NC` | Whole number | Yes | Count of open or in-progress nonconformities for this control in this entity. Prefer a formula that counts from the Findings sheet so the two tabs cannot drift. |
| `_Open_OFI` | Whole number | Yes | Count of open or in-progress opportunities for improvement |
| `_Linked_Risk` | Text | No | Existing risk-register id if one is already linked, for example `R-014`. Leave blank if none. |

Optional suffixes you may add and unpivot in the same way: `_Open_Gap`, `_Open_OBS`, `_Last_Assessed`, `_Assessor`, `_Comments`.

### Maturity scale (template default)

| Score | Rating | Meaning |
| --- | --- | --- |
| 1 | Informal | Ad hoc practice; little or no documentation |
| 2 | Documented | Policy or process exists, but operation is inconsistent |
| 3 | Implemented | Operated consistently in the entity |
| 4 | Measured | Operated and monitored, with evidence and KRIs |
| 5 | Improving | Measured, reviewed and demonstrably improving |

Risk-candidate rule 3 treats a score of **2 or below** plus an open NC as a candidate. If you use a different scale, change the threshold in `docs/04-risk-candidate-rules.md` and in the DAX.

---

## Sheet 3 — Risk Theme Mapping (recommended)

Maps each Annex A control to one **strategic risk theme**. The heat map and the risk-candidate rules aggregate at this grain, not at individual control level (although control-level drill-through is still available).

If your workbook does not yet have this sheet, create it. Assigning a theme after the fact in Power Query is possible but harder to govern.

| Canonical column | Type | Required | Notes |
| --- | --- | --- | --- |
| Control_ID | Text | Yes | Annex A id (one row per control in the simple mapping) |
| Control_Name | Text | No | Convenience copy |
| Annex_Category | Text | No | Organizational / People / Physical / Technological |
| Risk_Theme_ID | Text | Yes | Stable code, for example `RT-01` |
| Risk_Theme | Text | Yes | Display name, for example `Access control and identity` |
| Theme_Description | Text | No | One-sentence definition of the theme |
| Default_Likelihood | Whole number | No | 1–5 planning value used when a theme is promoted to the risk register |
| Default_Impact | Whole number | No | 1–5 planning value |
| Data_Flag | Text | Sample only | `Fictional sample` in the sample file |

A control should map to **one primary theme**. If you genuinely need many-to-many, add a bridge table rather than duplicating fact rows.

### Suggested theme catalogue (edit freely)

These are generic information-security themes suitable for most ISO 27001 programmes. Rename or replace them to match your risk-management framework.

| ID | Theme |
| --- | --- |
| RT-01 | Access control and identity |
| RT-02 | Third-party and supply chain |
| RT-03 | Data protection and confidentiality |
| RT-04 | Vulnerability and technical hygiene |
| RT-05 | Human factor and awareness |
| RT-06 | Incident response and resilience |
| RT-07 | Asset and change management |
| RT-08 | Cloud and emerging technology |
| RT-09 | Physical and environmental security |
| RT-10 | Compliance and assurance |

---

## Sheet 4 — Owners (recommended)

Lookup of finding owners. Used on the Ownership page (open / overdue / on-time performance) and for escalation labels.

| Canonical column | Type | Required | Notes |
| --- | --- | --- | --- |
| Owner_ID | Text | Yes | Unique key, referenced by Findings |
| Owner_Name | Text | Yes | Display name (`<Owner>`) |
| Role | Text | Yes | For example `Information Security Lead`, `IT Operations`, `Data Protection Officer` |
| Entity | Text | Yes | Home `<Entity>` / `<Country>`, or `Group` for a central function |
| Function | Text | No | For example `Information security`, `IT`, `People`, `Procurement`, `Internal audit` |
| Email | Text | No | Use a generic address pattern in examples |
| Line_Manager | Text | No | Name or id of the person overdue items escalate to |
| Data_Flag | Text | Sample only | `Fictional sample` in the sample file |

---

## Optional extra columns and tabs

The four tabs above are enough to build every page in this template. If your workbook already has further sheets (corrective actions, exceptions, incidents, training), leave them out of this model unless you have a clear visual that needs them. Do not relate those facts directly to Findings or Control Maturity; add them as additional facts on the same dimensions.

---

## Column-mapping table

Copy this table into your own notes or a worksheet called `Column Map` and fill the **Your workbook** column. Power Query should rename **Your workbook** headings to the **Canonical name**.

### Internal Audit Findings

| Canonical name | Your workbook | Transform / notes |
| --- | --- | --- |
| Finding_ID | | |
| Finding_Title | | |
| Finding_Type | | Map synonyms to `NC` / `OFI` / `Gap` / `OBS` |
| Severity | | Map synonyms to `Critical` / `High` / `Medium` / `Low` |
| Control_ID | | |
| Entity | | Harmonise spellings (`UK` vs `United Kingdom`) |
| Owner_ID | | |
| Owner_Name | | |
| Raised_Date | | Ensure type is Date, not DateTime or Text |
| Target_Date | | |
| Status | | Map synonyms to `Open` / `In Progress` / `Closed` |
| Closed_Date | | Blank if not closed |
| Risk_Theme_ID | | |
| Risk_Theme | | |
| Description | | |
| Root_Cause | | |
| Source | | |
| Auditor | | |

### Control Maturity

| Canonical name | Your workbook | Transform / notes |
| --- | --- | --- |
| Control_ID | | |
| Control_Name | | |
| Annex_Category | | |
| `<Entity>_Maturity` (repeat) | | List every entity prefix you use |
| `<Entity>_Open_NC` (repeat) | | Prefer a COUNTIFS back to Findings |
| `<Entity>_Open_OFI` (repeat) | | |
| `<Entity>_Linked_Risk` (repeat) | | |

Entity prefixes in this workbook:

| Entity display name | Column prefix in maturity sheet | Your prefix |
| --- | --- | --- |
| United Kingdom | UK_ | |
| Spain | Spain_ | |
| France | France_ | |
| Germany | Germany_ | |
| *(add rows)* | | |

### Risk Theme Mapping

| Canonical name | Your workbook | Transform / notes |
| --- | --- | --- |
| Control_ID | | |
| Control_Name | | |
| Annex_Category | | |
| Risk_Theme_ID | | |
| Risk_Theme | | |
| Theme_Description | | |
| Default_Likelihood | | 1–5 |
| Default_Impact | | 1–5 |

### Owners

| Canonical name | Your workbook | Transform / notes |
| --- | --- | --- |
| Owner_ID | | |
| Owner_Name | | |
| Role | | |
| Entity | | |
| Function | | |
| Email | | |
| Line_Manager | | |

---

## File handling notes

- Keep a single current workbook path (or SharePoint URL) and store it in the `pWorkbookPath` parameter, not hard-coded in every query.
- If the workbook is on SharePoint or OneDrive, use the SharePoint folder or Web connector rather than a personal `C:\Users\...` path, otherwise refresh will fail for everyone else.
- Do not merge cells, and keep row 1 as a header row with no banner above it. Put the “fictional sample” warning in a column (`Data_Flag`) or in this documentation, not in a title row that breaks ingest.
- Dates should be true Excel dates. The sample uses the ISO format `yyyy-mm-dd` in the CSV copies.
