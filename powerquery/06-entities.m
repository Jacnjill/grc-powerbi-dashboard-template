// =============================================================================
// Query name: Dim Entity
// Enable load. Small lookup of reporting entities. The sample uses four
// countries plus a Group row for central owners. Extend EntityCatalogue
// to match your organisation; do not leave short-code aliases only in
// Fact Findings — keep this table as the authority for display names.
// =============================================================================

let
    EntityCatalogue = #table(
        type table [
            Entity = text,
            Entity_Code = text,
            Entity_Sort = Int64.Type
        ],
        {
            {"United Kingdom", "UK",      1},
            {"Spain",          "Spain",   2},
            {"France",         "France",  3},
            {"Germany",        "Germany", 4},
            {"Group",          "Group",   9}
        }
    ),

    // Optionally union any entity values found in Findings or Owners that
    // are not already in the catalogue, so unmatched keys still appear.
    FromFindings = Table.SelectColumns(
        Table.Distinct(Table.SelectColumns(#"Fact Findings", {"Entity"})),
        {"Entity"}
    ),
    FromOwners = Table.SelectColumns(
        Table.Distinct(Table.SelectColumns(#"Dim Owner", {"Entity"})),
        {"Entity"}
    ),
    CombinedKeys = Table.Distinct(Table.Combine({FromFindings, FromOwners})),
    NewOnly = Table.SelectRows(
        CombinedKeys,
        each [Entity] <> null
            and [Entity] <> ""
            and List.Contains(EntityCatalogue[Entity], [Entity]) = false
    ),
    NewRows = Table.AddColumn(
        Table.AddColumn(NewOnly, "Entity_Code", each [Entity], type text),
        "Entity_Sort",
        each 100,
        Int64.Type
    ),
    Result = Table.Combine({EntityCatalogue, Table.SelectColumns(NewRows, {"Entity", "Entity_Code", "Entity_Sort"})})
in
    Result
