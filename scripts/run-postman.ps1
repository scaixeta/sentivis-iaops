param(
    [Parameter(Mandatory = $true)]
    [string]$Collection,

    [string]$EnvironmentFile = ".scr/.env",

    [string]$ArtifactsRoot = "artifacts/postman-cli-run"
)

$ErrorActionPreference = "Stop"

function Test-Command($Name) {
    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Read-DotEnvFile($Path) {
    $vars = @{}

    foreach ($line in Get-Content -LiteralPath $Path) {
        $trimmed = $line.Trim()
        if ([string]::IsNullOrWhiteSpace($trimmed) -or $trimmed.StartsWith("#")) {
            continue
        }

        $parts = $trimmed -split "=", 2
        if ($parts.Count -ne 2) {
            continue
        }

        $key = $parts[0].Trim()
        $value = $parts[1].Trim().Trim("'`"")
        if ($key) {
            $vars[$key] = $value
        }
    }

    return $vars
}

if (-not (Test-Path -LiteralPath $Collection)) {
    throw "Collection nao encontrada: $Collection"
}

if (-not (Test-Path -LiteralPath $EnvironmentFile)) {
    throw "Arquivo de ambiente nao encontrado: $EnvironmentFile"
}

if (-not (Test-Command "postman-cli")) {
    throw "postman-cli nao encontrado no PATH."
}

$required = @("SNOW_BASE_URL", "SNOW_USERNAME", "SNOW_PASSWORD")
$envVars = Read-DotEnvFile -Path $EnvironmentFile
$missing = $required | Where-Object { -not $envVars.ContainsKey($_) -or [string]::IsNullOrWhiteSpace($envVars[$_]) }

if ($missing.Count -gt 0) {
    throw "Variaveis obrigatorias ausentes no arquivo de ambiente: $($missing -join ', ')"
}

$timestamp = [DateTime]::UtcNow.ToString("yyyyMMdd-HHmmss")
$artifactDir = Join-Path -Path $ArtifactsRoot -ChildPath $timestamp
$null = New-Item -ItemType Directory -Path $artifactDir -Force

$tempEnv = Join-Path -Path $env:TEMP -ChildPath "postman-env-$timestamp.json"
$summaryPath = Join-Path -Path $artifactDir -ChildPath "run-summary.md"
$resultsPath = Join-Path -Path $artifactDir -ChildPath "test-results.json"
$logPath = Join-Path -Path $artifactDir -ChildPath "execution-log.txt"

$values = @()
foreach ($entry in $envVars.GetEnumerator()) {
    $values += @{
        key = $entry.Key
        value = $entry.Value
        enabled = $true
    }
}

$payload = @{
    id = "local-doc25-run"
    name = "DOC2.5 Temporary Environment"
    values = $values
} | ConvertTo-Json -Depth 5

Set-Content -LiteralPath $tempEnv -Value $payload -Encoding UTF8

try {
    $arguments = @(
        "collection", "run", $Collection,
        "--environment", $tempEnv,
        "--reporters", "cli,json",
        "--reporter-json-export", $resultsPath
    )

    & postman-cli @arguments *>&1 | Tee-Object -FilePath $logPath
    $exitCode = $LASTEXITCODE

    $masked = @()
    foreach ($name in $required + @("SNOW_TOKEN", "SNOW_AUTH_METHOD")) {
        if ($envVars.ContainsKey($name) -and -not [string]::IsNullOrWhiteSpace($envVars[$name])) {
            $masked += "- $name: PRESENT"
        } else {
            $masked += "- $name: AUSENTE"
        }
    }

    @(
        "# Postman CLI Run",
        "",
        "- Timestamp UTC: $([DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ'))",
        "- Collection: $Collection",
        "- Environment file: $EnvironmentFile",
        "- Exit code: $exitCode",
        "",
        "## Variaveis validadas",
        $masked,
        "",
        "## Artefatos",
        "- Log: `execution-log.txt`",
        "- Resultados: `test-results.json`"
    ) | Set-Content -LiteralPath $summaryPath -Encoding UTF8

    if ($exitCode -ne 0) {
        exit $exitCode
    }
}
finally {
    if (Test-Path -LiteralPath $tempEnv) {
        Remove-Item -LiteralPath $tempEnv -Force
    }
}
