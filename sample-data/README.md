# Sample data

These files are **fictional sample data** for the GRC Power BI dashboard template. They are not from a real organisation and must not be used as live evidence. Every row in the workbook and CSVs is flagged `Fictional sample`.

| File | Contents |
| --- | --- |
| `Continual_Improvement_Plan_SAMPLE.xlsx` | Four tabs: Internal Audit Findings, Control Maturity, Risk Theme Mapping, Owners |
| `findings.csv` | CSV copy of Internal Audit Findings |
| `control_maturity.csv` | CSV copy of Control Maturity (wide layout) |
| `risk_theme_mapping.csv` | CSV copy of Risk Theme Mapping |
| `owners.csv` | CSV copy of Owners |

Regenerate from the repository root with:

```bash
pip install -r scripts/requirements.txt
python3 scripts/generate_sample_data.py
```
