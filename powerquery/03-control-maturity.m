// =============================================================================
// Query name: Fact Control Maturity
// Enable load. Grain after unpivot: one Annex A control per entity.
//
// Source layout (wide): Control_ID, Control_Name, Annex_Category,
// then repeating blocks   <Prefix>_Maturity, <Prefix>_Open_NC,
//                         <Prefix>_Open_OFI, <Prefix>_Linked_Risk
//
// Edit EntityBlocks to match the prefixes in your workbook. The mapper
// EntityCodeToName must agree with Dim Entity display names.
// =============================================================================

let
    Source = Excel.Workbook(File.Contents(pWorkbookPath), null, true),
    RawSheet = Source{[Item = pMaturitySheet, Kind = "Sheet"]}[Data],
    Promoted = Table.PromoteHeaders(RawSheet, [PromoteAllScalars = true]),

    // Prefixes used in the sample workbook. Replace or extend for your entities.
    EntityBlocks = {
        [Code = "UK",      Name = "United Kingdom"],
        [Code = "Spain",   Name = "Spain"],
        [Code = "France",  Name = "France"],
        [Code = "Germany", Name = "Germany"]
    },

    SharedColumns = {"Control_ID", "Control_Name", "Annex_Category"},

    KeptShared = Table.SelectColumns(
        Promoted,
        List.Distinct(
            SharedColumns
            & List.Select(Table.ColumnNames(Promoted), each List.Contains(SharedColumns, _) = false)
        ),
        MissingField.Ignore
    ),

    Unpivoted = Table.UnpivotOtherColumns(KeptShared, SharedColumns, "Attribute", "Value"),

    // Split "UK_Maturity" → Entity_Code = "UK", Metric = "Maturity".
    // Split on the first underscore so entity codes themselves may not contain "_".
    Split = Table.AddColumn(
        Unpivoted,
        "Split",
        each
            let
                t = Text.Trim([Attribute]),
                i = Text.PositionOf(t, "_"),
                code = if i >= 0 then Text.Start(t, i) else t,
                metric = if i >= 0 then Text.Range(t, i + 1) else t
            in
                [Entity_Code = code, Metric = metric],
        type record
    ),
    Expanded = Table.ExpandRecordColumn(Split, "Split", {"Entity_Code", "Metric"}),
    RemovedAttribute = Table.RemoveColumns(Expanded, {"Attribute"}),

    EntityCodeToName = (code as text) as text =>
        let
            match = List.First(List.Select(EntityBlocks, each [Code] = code), null)
        in
            if match = null then code else match[Name],

    Named = Table.AddColumn(
        RemovedAttribute,
        "Entity",
        each EntityCodeToName(Text.Trim([Entity_Code])),
        type text
    ),
    RemovedCode = Table.RemoveColumns(Named, {"Entity_Code"}),

    // Keep only the metrics this model uses. Park unexpected leftovers out of the pivot.
    KnownMetrics = {"Maturity", "Open_NC", "Open_OFI", "Linked_Risk"},
    KnownOnly = Table.SelectRows(RemovedCode, each List.Contains(KnownMetrics, [Metric])),

    Pivoted = Table.Pivot(
        KnownOnly,
        List.Distinct(KnownOnly[Metric]),
        "Metric",
        "Value"
    ),

    Typed = Table.TransformColumnTypes(
        Pivoted,
        {
            {"Control_ID", type text},
            {"Control_Name", type text},
            {"Annex_Category", type text},
            {"Entity", type text},
            {"Maturity", Int64.Type},
            {"Open_NC", Int64.Type},
            {"Open_OFI", Int64.Type},
            {"Linked_Risk", type text}
        }
    ),

    Trimmed = Table.TransformColumns(
        Typed,
        {
            {"Control_ID", Text.Trim, type text},
            {"Entity", Text.Trim, type text},
            {"Linked_Risk", each if _ = null then null else Text.Trim(_), type text}
        },
        null,
        MissingField.Ignore
    ),

    // Drop rows with no control id (blank footer rows in Excel).
    Result = Table.SelectRows(Trimmed, each [Control_ID] <> null and Text.Trim([Control_ID]) <> "")
in
    Result
