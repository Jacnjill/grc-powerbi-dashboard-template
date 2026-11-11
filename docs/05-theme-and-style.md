---
comments: true
---

# Theme and style

The template uses a calm executive palette: deep navy for structure, a restrained set of data colours, and a strict red–amber–green (RAG) language for status. Import `theme/powerbi-theme.json` in Power BI Desktop via **View → Browse for themes**. The JSON is a valid Power BI report theme (named colours, text classes and a starter set of visual styles).

Do not add organisation or client branding to the shared template. You can fork the theme file later with a logo or extra colours if a specific report needs it.

## Colour palette

### Structure

| Token | Hex | Use |
| --- | --- | --- |
| Navy | `#1B365D` | Titles, axis text, primary KPI colour, table accent |
| Ink | `#3D4F61` | Body labels, secondary text |
| Muted | `#6B7C8A` | Axis lines, hints, footnotes |
| Line | `#D0D5DA` | Gridlines, card borders |
| Paper | `#FFFFFF` | Page and card background |
| Wash | `#F4F6F8` | Alternating table rows, slicer well, page background tint if you prefer off-white |

### Data colours (applied in order)

| Order | Hex | Suggested meaning |
| --- | --- | --- |
| 1 | `#1B365D` | Navy — default series |
| 2 | `#2E6B8A` | Steel blue |
| 3 | `#4A9BB4` | Teal |
| 4 | `#7C9A6E` | Sage |
| 5 | `#C4A35A` | Gold |
| 6 | `#C05640` | Rust |
| 7 | `#6B7C8A` | Slate |
| 8 | `#8B6B9A` | Plum |

### Finding type (lock these, do not rely on series order)

| Type | Hex | Notes |
| --- | --- | --- |
| NC | `#C62828` | Red — nonconformity |
| Gap | `#E65100` | Deep orange |
| OFI | `#F9A825` | Amber |
| OBS | `#546E7A` | Blue-grey |

Set these explicitly in the visuals (or in `visualStyles` for column/bar charts) so a missing type does not cause colours to shuffle.

### Severity

| Severity | Hex |
| --- | --- |
| Critical | `#7B1113` |
| High | `#C62828` |
| Medium | `#F9A825` |
| Low | `#546E7A` |

### RAG and diverging scales

| Token | Hex | Theme key | Use |
| --- | --- | --- | --- |
| Good / Low risk | `#2E7D32` | `good`, `minimum` | On track, closed on time, maturity ≥ 4, heat map 1–4 |
| Neutral / Moderate | `#F9A825` | `neutral`, `center` | Watch, on-time rate 60–79%, maturity = 3, heat map 5–9 |
| High (heat map mid-high) | `#E65100` | — | Heat map 10–16; use as a manual conditional-format colour |
| Bad / Extreme | `#C62828` | `bad`, `maximum` | Overdue, on-time rate &lt; 60%, maturity ≤ 2, heat map 17–25 |

Power BI theme files expose `good`, `neutral`, `bad` and the diverging `minimum` / `center` / `maximum` keys. The extra orange for “high” (as opposed to “extreme”) is documented here for conditional formatting; it is also included in `dataColors` as rust/gold so it is available to the report.

## RAG rules (conditional formatting)

Apply these consistently on every page. Thresholds match the defaults in `docs/04-risk-candidate-rules.md` and `docs/03-report-pages.md`; if you change a parameter in DAX, change the rule here and on the visual.

### KPI cards

| Measure | Green | Amber | Red |
| --- | --- | --- | --- |
| Overdue Findings | 0 | 1–4 | 5+ |
| % Closed On Time | ≥ 80% | 60–79% | &lt; 60% |
| Avg Days to Close | ≤ 45 | 46–90 | &gt; 90 |
| Open Findings | No colour by default | Optional: amber above your agreed workload, red above a hard cap | |

### Maturity

| Score | Rating | Colour |
| --- | --- | --- |
| 1 | Informal | Red |
| 2 | Documented | Red |
| 3 | Implemented | Amber |
| 4 | Measured | Green |
| 5 | Improving | Green |

### Ageing buckets (open items)

| Bucket | Colour |
| --- | --- |
| 0–30 days | Green |
| 31–60 days | Amber |
| 61–90 days | Deep orange `#E65100` |
| Over 90 days | Red |

### Heat map score

| Score | Band | Colour |
| --- | --- | --- |
| 1–4 | Low | Green |
| 5–9 | Moderate | Amber |
| 10–16 | High | Deep orange `#E65100` |
| 17–25 | Extreme | Red |

### Candidate score

| Score | Colour |
| --- | --- |
| 0 | No fill (not a candidate) |
| 1–40 | Amber |
| 41–70 | Deep orange |
| 71–100 | Red |

## Typography

The theme file sets:

| Class | Font | Size | Colour | Use |
| --- | --- | --- | --- | --- |
| Callout | Segoe UI Semibold | 44 | Navy | KPI values |
| Title | Segoe UI Semibold | 16 | Navy | Visual titles |
| Header | Segoe UI Semibold | 12 | Navy | Table / matrix headers |
| Label | Segoe UI | 10 | Ink | Axes, card labels, slicers |

If Segoe UI is not available (for example on some macOS authoring machines), Power BI falls back to a sans-serif system font. Do not use decorative or condensed fonts on an executive pack.

Page title: 20 pt Semibold, navy, top-left. “As at” date: 10 pt, muted, top-right.

## Visual style conventions

- **Backgrounds:** white visuals on a white or wash page. Hairline `#D0D5DA` border, 4 px corner radius, no drop shadow.
- **Gridlines:** horizontal only, `#D0D5DA`, 1 px. No vertical gridlines on bar charts.
- **Legends:** top-centre or bottom-centre, 9–10 pt, ink.
- **Data labels:** prefer labels on KPI-adjacent bars; avoid labelling every point on a dense line.
- **Slicers:** dropdown or tile, navy selected state, no search box unless a field is long (Owner, Control).
- **Tables:** header navy text on wash; alternating rows `#F4F6F8`; totals in Semibold. Do not use total rows on the attention or escalation lists.
- **Empty states:** “No items in this context” rather than a blank visual.

## Accessibility

- Do not rely on colour alone: overdue tables also show a `Days Overdue` number; candidate tables show flags as Yes/No, not only a colour.
- Maintain contrast of at least 4.5:1 for body text (navy or ink on white meets this; muted grey on wash may not — use muted only for non-essential hints).
- The NC red (`#C62828`) and OFI amber (`#F9A825`) are distinguishable by hue and brightness; test in greyscale if the pack will be printed in monochrome (type labels must remain visible).

## Importing and maintaining the theme

1. In Power BI Desktop: **View → Themes → Browse for themes** and select `theme/powerbi-theme.json`.
2. Confirm the theme name **ISO 27001 Continual Improvement — Executive** appears in the theme gallery.
3. After import, still set the locked type and severity colours on the first visual of each kind; some chart types do not pick categorical mappings from the theme file alone.
4. If you edit the JSON, keep it valid UTF-8 JSON (no comments, no trailing commas) and re-import. A short checklist is in `docs/06-build-checklist.md`.
