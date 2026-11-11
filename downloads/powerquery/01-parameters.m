// =============================================================================
// Parameters
// Create these in Power BI Desktop: Home → Transform data → Manage parameters.
// Each block below is the M expression for that parameter (a single literal).
// Do not hard-code paths inside the other queries; always reference these names.
// =============================================================================

// -----------------------------------------------------------------------------
// Name:        pWorkbookPath
// Type:        Text
// Suggested:   Required
// Description: Full path or SharePoint URL of the Continual Improvement Plan
//              workbook. Prefer a SharePoint URL so refresh works for others.
// Examples:
//   "https://<tenant>.sharepoint.com/sites/<Site>/Shared%20Documents/Continual_Improvement_Plan.xlsx"
//   "C:\Data\Continual_Improvement_Plan.xlsx"
// -----------------------------------------------------------------------------
"C:\Data\Continual_Improvement_Plan.xlsx" meta [
    IsParameterQuery = true,
    Type = type text,
    IsParameterQueryRequired = true
]

// -----------------------------------------------------------------------------
// Name:        pFindingsSheet
// Type:        Text
// Default:     Internal Audit Findings
// -----------------------------------------------------------------------------
// "Internal Audit Findings" meta [IsParameterQuery = true, Type = type text, IsParameterQueryRequired = true]

// -----------------------------------------------------------------------------
// Name:        pMaturitySheet
// Type:        Text
// Default:     Control Maturity
// -----------------------------------------------------------------------------
// "Control Maturity" meta [IsParameterQuery = true, Type = type text, IsParameterQueryRequired = true]

// -----------------------------------------------------------------------------
// Name:        pThemesSheet
// Type:        Text
// Default:     Risk Theme Mapping
// -----------------------------------------------------------------------------
// "Risk Theme Mapping" meta [IsParameterQuery = true, Type = type text, IsParameterQueryRequired = true]

// -----------------------------------------------------------------------------
// Name:        pOwnersSheet
// Type:        Text
// Default:     Owners
// -----------------------------------------------------------------------------
// "Owners" meta [IsParameterQuery = true, Type = type text, IsParameterQueryRequired = true]

// -----------------------------------------------------------------------------
// Name:        pStartDate   (optional)
// Type:        Date
// Description: First date in Dim Date. Leave unset to derive from Raised_Date.
// Default example:
// -----------------------------------------------------------------------------
// #date(2024, 1, 1) meta [IsParameterQuery = true, Type = type date, IsParameterQueryRequired = false]

// -----------------------------------------------------------------------------
// Name:        pEndDate     (optional)
// Type:        Date
// Description: Last date in Dim Date. Leave unset to use 31 December of next year.
// -----------------------------------------------------------------------------
// #date(2027, 12, 31) meta [IsParameterQuery = true, Type = type date, IsParameterQueryRequired = false]

// -----------------------------------------------------------------------------
// Staging query name: Source Workbook
// Disable load. Other queries reference this so the connector is in one place.
//
// For a local or OneDrive-synced file:
// -----------------------------------------------------------------------------
/*
let
    Source = Excel.Workbook(File.Contents(pWorkbookPath), null, true)
in
    Source
*/

// For a SharePoint-hosted file, prefer the SharePoint folder connector and
// then navigate to the file, or use:
/*
let
    Source = Excel.Workbook(Web.Contents(pWorkbookPath), null, true)
in
    Source
*/
// You may need an organizational account and a privacy level of Organizational.
