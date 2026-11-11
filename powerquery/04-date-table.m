// =============================================================================
// Query name: Dim Date
// Enable load. Mark as a date table on the Date column after load.
// Fiscal year starts 1 April (common in the UK). Change FiscalYearStartMonth
// if your organisation uses a different year-end.
//
// If pStartDate / pEndDate parameters exist, they are used. Otherwise the
// range is 1 January of the earliest Findings[Raised_Date] year, through
// 31 December of next calendar year.
// =============================================================================

let
    FiscalYearStartMonth = 4,

    // Safe read of optional parameters. If you did not create pStartDate /
    // pEndDate, comment this block and set StartDate / EndDate literally.
    HasStart = (try pStartDate is date otherwise false),
    HasEnd   = (try pEndDate   is date otherwise false),

    MinRaised = List.Min(Table.Column(#"Fact Findings", "Raised_Date")),
    DerivedStart = #date(Date.Year(MinRaised), 1, 1),
    DerivedEnd = #date(Date.Year(DateTime.Date(DateTime.LocalNow())) + 1, 12, 31),

    StartDate = if HasStart then pStartDate else DerivedStart,
    EndDate   = if HasEnd   then pEndDate   else DerivedEnd,

    DayCount = Duration.Days(EndDate - StartDate) + 1,
    DateList = List.Dates(StartDate, DayCount, #duration(1, 0, 0, 0)),
    AsTable = Table.FromList(DateList, Splitter.SplitByNothing(), {"Date"}, null, ExtraValues.Error),
    TypedDate = Table.TransformColumnTypes(AsTable, {{"Date", type date}}),

    AddYear = Table.AddColumn(TypedDate, "Year", each Date.Year([Date]), Int64.Type),
    AddQuarter = Table.AddColumn(AddYear, "Quarter", each Date.QuarterOfYear([Date]), Int64.Type),
    AddQuarterName = Table.AddColumn(
        AddQuarter,
        "QuarterName",
        each "Q" & Number.ToText([Quarter]),
        type text
    ),
    AddMonthNumber = Table.AddColumn(AddQuarterName, "MonthNumber", each Date.Month([Date]), Int64.Type),
    AddMonthName = Table.AddColumn(
        AddMonthNumber,
        "MonthName",
        each Date.ToText([Date], "MMMM", "en-GB"),
        type text
    ),
    AddMonthShort = Table.AddColumn(
        AddMonthName,
        "MonthShort",
        each Date.ToText([Date], "MMM", "en-GB"),
        type text
    ),
    AddYearMonth = Table.AddColumn(
        AddMonthShort,
        "YearMonth",
        each Date.ToText([Date], "yyyy-MM"),
        type text
    ),
    AddYearMonthSort = Table.AddColumn(
        AddYearMonth,
        "YearMonthSort",
        each [Year] * 100 + [MonthNumber],
        Int64.Type
    ),
    AddWeekOfYear = Table.AddColumn(
        AddYearMonthSort,
        "WeekOfYear",
        each Date.WeekOfYear([Date], Day.Monday),
        Int64.Type
    ),
    AddDayOfWeek = Table.AddColumn(
        AddWeekOfYear,
        "DayOfWeek",
        each Date.DayOfWeek([Date], Day.Monday) + 1,
        Int64.Type
    ),
    AddDayName = Table.AddColumn(
        AddDayOfWeek,
        "DayName",
        each Date.ToText([Date], "dddd", "en-GB"),
        type text
    ),
    AddIsWorkingDay = Table.AddColumn(
        AddDayName,
        "IsWorkingDay",
        each [DayOfWeek] <= 5,
        type logical
    ),

    // Fiscal year starting 1 April: 15 May 2026 → FY 2026/27, label "2026/27".
    AddFiscalYearNumber = Table.AddColumn(
        AddIsWorkingDay,
        "FiscalYearNumber",
        each if [MonthNumber] >= FiscalYearStartMonth then [Year] else [Year] - 1,
        Int64.Type
    ),
    AddFiscalYear = Table.AddColumn(
        AddFiscalYearNumber,
        "FiscalYear",
        each
            Number.ToText([FiscalYearNumber])
            & "/"
            & Text.End(Number.ToText([FiscalYearNumber] + 1), 2),
        type text
    ),
    AddFiscalMonth = Table.AddColumn(
        AddFiscalYear,
        "FiscalMonthNumber",
        each
            let
                offset = [MonthNumber] - FiscalYearStartMonth
            in
                if offset >= 0 then offset + 1 else offset + 13,
        Int64.Type
    ),
    AddFiscalQuarter = Table.AddColumn(
        AddFiscalMonth,
        "FiscalQuarter",
        each Number.RoundUp([FiscalMonthNumber] / 3, 0),
        Int64.Type
    ),
    AddFiscalQuarterName = Table.AddColumn(
        AddFiscalQuarter,
        "FiscalQuarterName",
        each "FQ" & Number.ToText([FiscalQuarter]),
        type text
    ),

    Result = AddFiscalQuarterName
in
    Result
