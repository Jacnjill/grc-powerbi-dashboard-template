// =============================================================================
// Query name: Dim Owner
// Enable load. Lookup of finding owners, from the Owners sheet.
// =============================================================================

let
    Source = Excel.Workbook(File.Contents(pWorkbookPath), null, true),
    RawSheet = Source{[Item = pOwnersSheet, Kind = "Sheet"]}[Data],
    Promoted = Table.PromoteHeaders(RawSheet, [PromoteAllScalars = true]),
    Kept = Table.SelectColumns(
        Promoted,
        {"Owner_ID", "Owner_Name", "Role", "Entity", "Function", "Email", "Line_Manager", "Data_Flag"},
        MissingField.Ignore
    ),
    Typed = Table.TransformColumnTypes(
        Kept,
        {
            {"Owner_ID", type text},
            {"Owner_Name", type text},
            {"Role", type text},
            {"Entity", type text},
            {"Function", type text},
            {"Email", type text},
            {"Line_Manager", type text},
            {"Data_Flag", type text}
        }
    ),
    Trimmed = Table.TransformColumns(
        Typed,
        {
            {"Owner_ID", Text.Trim, type text},
            {"Owner_Name", Text.Trim, type text},
            {"Role", Text.Trim, type text},
            {"Entity", Text.Trim, type text},
            {"Function", each if _ = null then null else Text.Trim(_), type text},
            {"Email", each if _ = null then null else Text.Trim(_), type text},
            {"Line_Manager", each if _ = null then null else Text.Trim(_), type text}
        },
        null,
        MissingField.Ignore
    ),
    EntityMapped = Table.TransformColumns(
        Trimmed,
        {{"Entity", each
            let
                v = Text.Trim(_)
            in
                if List.Contains({"UK", "GB", "United Kingdom", "Great Britain"}, v) then "United Kingdom"
                else if List.Contains({"ES", "Spain", "España", "Espana"}, v) then "Spain"
                else if List.Contains({"FR", "France"}, v) then "France"
                else if List.Contains({"DE", "Germany", "Deutschland"}, v) then "Germany"
                else v,
            type text
        }}
    ),
    Filtered = Table.SelectRows(EntityMapped, each [Owner_ID] <> null and [Owner_ID] <> ""),
    Distinct = Table.Distinct(Filtered, {"Owner_ID"}),
    Result = Distinct
in
    Result
