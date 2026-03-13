<#
.SYNOPSIS
    Execute selective ThingsBoard CE knowledge import.

.DESCRIPTION
    Imports Community Edition markdown documentation from a local
    thingsboard.github.io clone into the local knowledge layer,
    preserving only the categories approved in the project plan:
    reference, user-guide and tutorials.

.PARAMETER SourcePath
    Local path where upstream docs repository exists.

.PARAMETER ProjectPath
    Project root path. Default: current working directory.

.PARAMETER DryRun
    Preview actions without writing files.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$SourcePath,

    [Parameter(Mandatory=$false)]
    [string]$ProjectPath = (Get-Location).Path,

    [Parameter(Mandatory=$false)]
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Status {
    param(
        [string]$Level,
        [string]$Message
    )

    Write-Host "[$Level] $Message"
}

function Ensure-Directory {
    param([string]$Path)

    if (Test-Path -LiteralPath $Path) {
        return
    }

    if ($DryRun) {
        Write-Status "DRYRUN" "Would create directory: $Path"
        return
    }

    New-Item -ItemType Directory -Path $Path -Force | Out-Null
    Write-Status "ACTION" "Created directory: $Path"
}

function Write-Content {
    param(
        [string]$Path,
        [string]$Content
    )

    if ($DryRun) {
        Write-Status "DRYRUN" "Would write file: $Path"
        return
    }

    Set-Content -Path $Path -Value $Content -Encoding UTF8
}

function Convert-ToRelativePath {
    param(
        [string]$BasePath,
        [string]$FullPath
    )

    $baseUri = [Uri]((Resolve-Path -LiteralPath $BasePath).Path.TrimEnd('\', '/') + [IO.Path]::DirectorySeparatorChar)
    $fullUri = [Uri](Resolve-Path -LiteralPath $FullPath).Path
    return [Uri]::UnescapeDataString($baseUri.MakeRelativeUri($fullUri).ToString()) -replace '/', [IO.Path]::DirectorySeparatorChar
}

function Get-ImportCandidates {
    param([string]$ResolvedSourcePath)

    $sourceGroups = @(
        @{ Category = "api"; SourceRoot = "reference"; TargetRoot = "knowledge/thingsboard/ce/api" },
        @{ Category = "user-guide"; SourceRoot = "user-guide"; TargetRoot = "knowledge/thingsboard/ce/user-guide" },
        @{ Category = "tutorials"; SourceRoot = "tutorials"; TargetRoot = "knowledge/thingsboard/ce/tutorials" }
    )

    $items = New-Object System.Collections.Generic.List[object]
    $docsRoot = Join-Path $ResolvedSourcePath "_includes/docs"

    foreach ($group in $sourceGroups) {
        $groupSourcePath = Join-Path $docsRoot $group.SourceRoot
        if (-not (Test-Path -LiteralPath $groupSourcePath)) {
            Write-Status "WARN" "Source group not found: $groupSourcePath"
            continue
        }

        Get-ChildItem -LiteralPath $groupSourcePath -Recurse -File -Filter "*.md" | ForEach-Object {
            $relativePath = Convert-ToRelativePath -BasePath $groupSourcePath -FullPath $_.FullName
            $items.Add([PSCustomObject]@{
                Category = $group.Category
                SourcePath = $_.FullName
                SourceRelativePath = ($_.FullName.Substring($ResolvedSourcePath.Length).TrimStart('\', '/')) -replace '\\','/'
                TargetRelativePath = ($relativePath -replace '\\','/')
                TargetRoot = $group.TargetRoot
            })
        }
    }

    return $items
}

function Main {
    Write-Status "STEP" "Validating parameters"

    if (-not (Test-Path -LiteralPath $SourcePath)) {
        Write-Status "ERROR" "SourcePath does not exist: $SourcePath"
        exit 1
    }

    if (-not (Test-Path -LiteralPath $ProjectPath)) {
        Write-Status "ERROR" "ProjectPath does not exist: $ProjectPath"
        exit 1
    }

    $resolvedProjectPath = (Resolve-Path -LiteralPath $ProjectPath).Path
    $resolvedSourcePath = (Resolve-Path -LiteralPath $SourcePath).Path
    $docsRoot = Join-Path $resolvedSourcePath "_includes/docs"

    if (-not (Test-Path -LiteralPath $docsRoot)) {
        Write-Status "ERROR" "Expected docs root not found: $docsRoot"
        Write-Status "ERROR" "Materialize the local clone before running selective import."
        exit 1
    }

    Write-Status "INFO" "SourcePath validated: $resolvedSourcePath"
    Write-Status "INFO" "ProjectPath validated: $resolvedProjectPath"

    @(
        (Join-Path $resolvedProjectPath "third_party/thingsboard-ce/upstream"),
        (Join-Path $resolvedProjectPath "knowledge/thingsboard/ce/manifests"),
        (Join-Path $resolvedProjectPath "knowledge/thingsboard/ce/reference"),
        (Join-Path $resolvedProjectPath "knowledge/thingsboard/ce/runbooks"),
        (Join-Path $resolvedProjectPath "knowledge/thingsboard/ce/api"),
        (Join-Path $resolvedProjectPath "knowledge/thingsboard/ce/user-guide"),
        (Join-Path $resolvedProjectPath "knowledge/thingsboard/ce/tutorials")
    ) | ForEach-Object { Ensure-Directory -Path $_ }

    Write-Status "STEP" "Collecting selective import candidates"
    $items = Get-ImportCandidates -ResolvedSourcePath $resolvedSourcePath
    $items = $items | Sort-Object Category, SourceRelativePath

    if ($items.Count -eq 0) {
        Write-Status "ERROR" "No selective import candidates found."
        exit 1
    }

    $importedCount = 0
    foreach ($item in $items) {
        $targetPath = Join-Path $resolvedProjectPath (Join-Path $item.TargetRoot $item.TargetRelativePath)
        Ensure-Directory -Path (Split-Path -Parent $targetPath)

        if ($DryRun) {
            Write-Status "DRYRUN" "Would copy $($item.SourceRelativePath) -> $targetPath"
        } else {
            Copy-Item -LiteralPath $item.SourcePath -Destination $targetPath -Force
        }

        $importedCount++
    }

    $utcNow = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    $counts = @{
        "api" = ($items | Where-Object Category -eq "api").Count
        "user-guide" = ($items | Where-Object Category -eq "user-guide").Count
        "tutorials" = ($items | Where-Object Category -eq "tutorials").Count
    }

    $mappingLines = @("source_path,target_path,category,mode,notes")
    foreach ($item in $items) {
        $mappingLines += "$($item.SourceRelativePath),$($item.TargetRoot)/$($item.TargetRelativePath),$($item.Category),imported-selective,local-clone"
    }

    $sourcesPath = Join-Path $resolvedProjectPath "third_party/thingsboard-ce/SOURCES.md"
    $importManifestPath = Join-Path $resolvedProjectPath "knowledge/thingsboard/ce/manifests/import_manifest.md"
    $mappingPath = Join-Path $resolvedProjectPath "knowledge/thingsboard/ce/manifests/mapping_table.csv"
    $exclusionsPath = Join-Path $resolvedProjectPath "knowledge/thingsboard/ce/manifests/exclusions.md"

    $sourcesContent = @"
# SOURCES.md - ThingsBoard CE Documentation Source

## Status

- status: selective import executed
- import: executed
- scope: CE markdown only (`reference`, `user-guide`, `tutorials`)

## Upstream Source Information

| Field | Value |
|-------|-------|
| upstream_repository | thingsboard.github.io |
| upstream_local_path | $resolvedSourcePath |
| source_branch | master |
| import_date_utc | $utcNow |
| scope_imported | CE (Community Edition) only |
| imported_files | $importedCount |

## Notes

- Import preserves only approved CE markdown categories.
- Excludes PE, Cloud, Edge and non-markdown assets.
- LICENSE and NOTICE remain from upstream repository only; no local placeholder was created.
"@

    $importManifestContent = @"
# import_manifest.md - ThingsBoard CE Import Manifest

## Status

- import_status: executed
- mode: selective import
- source_path: $resolvedSourcePath
- import_date_utc: $utcNow

## Imported counts

| Category | Count | Target |
|----------|-------|--------|
| `reference` | $($counts["api"]) | `knowledge/thingsboard/ce/api/` |
| `user-guide` | $($counts["user-guide"]) | `knowledge/thingsboard/ce/user-guide/` |
| `tutorials` | $($counts["tutorials"]) | `knowledge/thingsboard/ce/tutorials/` |

## Notes

- Import list is tracked in `mapping_table.csv`.
- Selective import keeps CE-only markdown aligned with the approved scope.
"@

    $exclusionsContent = @"
# exclusions.md - ThingsBoard CE Import Exclusions

## Status

- import_status: executed
- import_mode: selective import
- import_date_utc: $utcNow

## Applied exclusion rules

| Pattern | Reason |
|---------|--------|
| `**/pe/**` | Professional Edition content |
| `**/cloud/**` | Cloud-only scope |
| `**/edge/**` | Edge-only scope |
| `**/*.png` `**/*.jpg` `**/*.svg` | Non-text assets |
| `**/*.sh` | Non-markdown support scripts |
| `docs/**` wrappers | Non-substantive navigation pages |

## Notes

- Selective import copied only markdown files from approved CE categories.
"@

    Write-Status "STEP" "Refreshing manifests"
    Write-Content -Path $sourcesPath -Content $sourcesContent
    Write-Content -Path $importManifestPath -Content $importManifestContent
    Write-Content -Path $mappingPath -Content ($mappingLines -join [Environment]::NewLine)
    Write-Content -Path $exclusionsPath -Content $exclusionsContent

    Write-Status "SUMMARY" "Imported files: $importedCount"
    Write-Status "SUMMARY" "API: $($counts["api"]) | User guide: $($counts["user-guide"]) | Tutorials: $($counts["tutorials"])"

    if ($DryRun) {
        Write-Status "DONE" "Dry run finished safely"
    } else {
        Write-Status "DONE" "Selective import finished safely"
    }
}

Main
