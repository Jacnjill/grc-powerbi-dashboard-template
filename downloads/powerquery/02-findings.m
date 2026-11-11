// =============================================================================
// Query name: Fact Findings
// Enable load. Grain: one internal-audit finding.
// Rename source columns to the canonical names in docs/01-source-workbook-spec.md
// before the type step, using your column-mapping table.
// =============================================================================

let
    Source = Excel.Workbook(File.Contents(pWorkbookPath), null, true),
    RawSheet = Source{[Item = pFindingsSheet, Kind = "Sheet"]}[Data],
    Promoted = Table.PromoteHeaders(RawSheet, [PromoteAllScalars = true]),

    // Rename this list to match your workbook headings if they differ.
    Renamed = Table.RenameColumns(
        Promoted,
        {
            // {"Your heading", "Finding_ID"},
        },
        MissingField.Ignore
    ),

    Kept = Table.SelectColumns(
        Renamed,
        {
            "Finding_ID",
            "Finding_Title",
            "Finding_Type",
            "Severity",
            "Control_ID",
            "Entity",
            "Owner_ID",
            "Owner_Name",
            "Raised_Date",
            "Target_Date",
            "Status",
            "Closed_Date",
            "Risk_Theme_ID",
            "Risk_Theme",
            "Description",
            "Root_Cause",
            "Source",
            "Auditor",
            "Data_Flag"
        },
        MissingField.Ignore
    ),

    Typed = Table.TransformColumnTypes(
        Kept,
        {
            {"Finding_ID", type text},
            {"Finding_Title", type text},
            {"Finding_Type", type text},
            {"Severity", type text},
            {"Control_ID", type text},
            {"Entity", type text},
            {"Owner_ID", type text},
            {"Owner_Name", type text},
            {"Raised_Date", type date},
            {"Target_Date", type date},
            {"Status", type text},
            {"Closed_Date", type date},
            {"Risk_Theme_ID", type text},
            {"Risk_Theme", type text},
            {"Description", type text},
            {"Root_Cause", type text},
            {"Source", type text},
            {"Auditor", type text},
            {"Data_Flag", type text}
        },
        "en-GB"
    ),

    Trimmed = Table.TransformColumns(
        Typed,
        {
            {"Finding_ID", Text.Trim, type text},
            {"Finding_Type", Text.Trim, type text},
            {"Severity", Text.Trim, type text},
            {"Control_ID", Text.Trim, type text},
            {"Entity", Text.Trim, type text},
            {"Owner_ID", Text.Trim, type text},
            {"Status", Text.Trim, type text},
            {"Risk_Theme_ID", Text.Trim, type text}
        },
        null,
        MissingField.Ignore
    ),

    // Harmonise common synonyms to the canonical lists.
    TypesMapped = Table.TransformColumns(
        Trimmed,
        {{"Finding_Type", each
            let
                v = Text.Upper(Text.Trim(_))
            in
                if List.Contains({"NC", "NONCONFORMITY", "NON-CONFORMITY", "NON CONFORMITY"}, v) then "NC"
                else if List.Contains({"OFI", "OPPORTUNITY FOR IMPROVEMENT", "IMPROVEMENT"}, v) then "OFI"
                else if List.Contains({"GAP", "GAPS"}, v) then "Gap"
                else if List.Contains({"OBS", "OBSERVATION", "OBSERVATIONS"}, v) then "OBS"
                else _,
            type text
        }}
    ),

    SeverityMapped = Table.TransformColumns(
        TypesMapped,
        {{"Severity", each
            let
                v = Text.Upper(Text.Trim(_))
            in
                if List.Contains({"CRITICAL", "CRIT", "SEVERE"}, v) then "Critical"
                else if List.Contains({"HIGH", "MAJOR"}, v) then "High"
                else if List.Contains({"MEDIUM", "MODERATE", "MED"}, v) then "Medium"
                else if List.Contains({"LOW", "MINOR"}, v) then "Low"
                else _,
            type text
        }}
    ),

    StatusMapped = Table.TransformColumns(
        SeverityMapped,
        {{"Status", each
            let
                v = Text.Upper(Text.Trim(_))
            in
                if List.Contains({"OPEN", "NEW", "RAISED"}, v) then "Open"
                else if List.Contains({"IN PROGRESS", "IN-PROGRESS", "PROGRESS", "WIP", "ONGOING"}, v) then "In Progress"
                else if List.Contains({"CLOSED", "COMPLETE", "COMPLETED", "DONE"}, v) then "Closed"
                else _,
            type text
        }}
    ),

    // Harmonise entity short codes to the Dim Entity display names used in the sample.
    // Extend this list to match your own entity catalogue.
    EntityMapped = Table.TransformColumns(
        StatusMapped,
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

    FilteredBlankIds = Table.SelectRows(EntityMapped, each [Finding_ID] <> null and Text.Trim([Finding_ID]) <> ""),

    // In live use you may remove the Data_Flag column, or filter out any leftover sample rows:
    // LiveOnly = Table.SelectRows(FilteredBlankIds, each [Data_Flag] <> "Fictional sample"),

    Result = FilteredBlankIds
in
    Result
