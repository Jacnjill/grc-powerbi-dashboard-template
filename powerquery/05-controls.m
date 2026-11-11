// =============================================================================
// Query name: Dim Control
// Enable load. One row per ISO 27001:2022 Annex A control, with its primary
// risk theme. Built from the Risk Theme Mapping sheet so control and theme
// stay in step. If you maintain a separate controls catalogue, load that
// instead and join the theme on Control_ID.
// =============================================================================

let
    Source = Excel.Workbook(File.Contents(pWorkbookPath), null, true),
    RawSheet = Source{[Item = pThemesSheet, Kind = "Sheet"]}[Data],
    Promoted = Table.PromoteHeaders(RawSheet, [PromoteAllScalars = true]),
    Kept = Table.SelectColumns(
        Promoted,
        {"Control_ID", "Control_Name", "Annex_Category", "Risk_Theme_ID"},
        MissingField.Ignore
    ),
    Typed = Table.TransformColumnTypes(
        Kept,
        {
            {"Control_ID", type text},
            {"Control_Name", type text},
            {"Annex_Category", type text},
            {"Risk_Theme_ID", type text}
        }
    ),
    Trimmed = Table.TransformColumns(
        Typed,
        {
            {"Control_ID", Text.Trim, type text},
            {"Control_Name", Text.Trim, type text},
            {"Annex_Category", Text.Trim, type text},
            {"Risk_Theme_ID", Text.Trim, type text}
        }
    ),
    Filtered = Table.SelectRows(Trimmed, each [Control_ID] <> null and [Control_ID] <> ""),
    Distinct = Table.Distinct(Filtered, {"Control_ID"}),
    Result = Distinct
in
    Result
