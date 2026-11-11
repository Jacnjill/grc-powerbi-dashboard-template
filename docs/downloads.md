---
comments: true
---

# Downloads

All of the build artefacts can be downloaded from this page, or browsed in the [repository](https://github.com/Jacnjill/grc-powerbi-dashboard-template). The sample workbook and CSVs are **fictional** and must not be used as live evidence.

## Sample data

| File | Description |
| --- | --- |
| [Continual_Improvement_Plan_SAMPLE.xlsx](downloads/Continual_Improvement_Plan_SAMPLE.xlsx) | Four-tab sample workbook: Internal Audit Findings (~60 fictional findings), Control Maturity (ISO 27001:2022 Annex A, 93 controls × four example countries), Risk Theme Mapping, and Owners |
| [findings.csv](downloads/findings.csv) | CSV copy of Internal Audit Findings |
| [control_maturity.csv](downloads/control_maturity.csv) | CSV copy of Control Maturity (wide layout, before the Power Query unpivot) |
| [risk_theme_mapping.csv](downloads/risk_theme_mapping.csv) | CSV copy of Risk Theme Mapping |
| [owners.csv](downloads/owners.csv) | CSV copy of Owners |
| [generate_sample_data.py](downloads/generate_sample_data.py) | Script that regenerates the workbook and CSVs |

To regenerate the sample files from the repository root (Python 3 with `openpyxl`):

```bash
pip install -r scripts/requirements.txt
python3 scripts/generate_sample_data.py
```

The four example entities in the sample are United Kingdom, Spain, France and Germany. Treat them as placeholders for any `<Entity>` grain you report on.

## Power BI theme

| File | Description |
| --- | --- |
| [powerbi-theme.json](downloads/powerbi-theme.json) | Importable Power BI theme (**View → Browse for themes**). Palette and RAG rules are described in [Theme and style](05-theme-and-style.md). |

## DAX measures

| File | Description |
| --- | --- |
| [measures.dax](downloads/measures.dax) | Full measure set (open, overdue, on-time closure, ageing, type counts, maturity, ownership, risk-candidate flags and heat-map scores), with comments. Paste into a measures table in Power BI Desktop. |

## Power Query (M) scripts

Copy these into blank queries in Power BI Desktop after creating the parameters. Details are in the [data model](02-data-model.md) and the [build checklist](06-build-checklist.md).

| File | Query name |
| --- | --- |
| [01-parameters.m](downloads/powerquery/01-parameters.m) | Parameters and a source-workbook staging note |
| [02-findings.m](downloads/powerquery/02-findings.m) | Fact Findings |
| [03-control-maturity.m](downloads/powerquery/03-control-maturity.m) | Fact Control Maturity (unpivots entity blocks) |
| [04-date-table.m](downloads/powerquery/04-date-table.m) | Dim Date |
| [05-controls.m](downloads/powerquery/05-controls.m) | Dim Control |
| [06-entities.m](downloads/powerquery/06-entities.m) | Dim Entity |
| [07-owners.m](downloads/powerquery/07-owners.m) | Dim Owner |
| [08-risk-themes.m](downloads/powerquery/08-risk-themes.m) | Dim Risk Theme |

The same files live in [`powerquery/`](https://github.com/Jacnjill/grc-powerbi-dashboard-template/tree/main/powerquery) in the repository.
