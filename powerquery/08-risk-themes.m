// =============================================================================
// Query name: Dim Risk Theme
// Enable load. Distinct strategic risk themes, with default likelihood and
// impact planning values for the register (not the derived heat-map axes).
// =============================================================================

let
    Source = Excel.Workbook(File.Contents(pWorkbookPath), null, true),
    RawSheet = Source{[Item = pThemesSheet, Kind = "Sheet"]}[Data],
    Promoted = Table.PromoteHeaders(RawSheet, [PromoteAllScalars = true]),
    Kept = Table.SelectColumns(
        Promoted,
        {"Risk_Theme_ID", "Risk_Theme", "Theme_Description", "Default_Likelihood", "Default_Impact"},
        MissingField.Ignore
    ),
    Typed = Table.TransformColumnTypes(
        Kept,
        {
            {"Risk_Theme_ID", type text},
            {"Risk_Theme", type text},
            {"Theme_Description", type text},
            {"Default_Likelihood", Int64.Type},
            {"Default_Impact", Int64.Type}
        }
    ),
    Trimmed = Table.TransformColumns(
        Typed,
        {
            {"Risk_Theme_ID", Text.Trim, type text},
            {"Risk_Theme", Text.Trim, type text}
        }
    ),
    Filtered = Table.SelectRows(Trimmed, each [Risk_Theme_ID] <> null and [Risk_Theme_ID] <> ""),
    Distinct = Table.Distinct(Filtered, {"Risk_Theme_ID"}),
    Result = Distinct
in
    Result
