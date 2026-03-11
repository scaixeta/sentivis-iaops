<#
.SYNOPSIS
    Audit de conformidade DOC2.5.

.DESCRIPTION
    Este script valida a estrutura de um projeto contra o padrão DOC2.5,
    gerando um relatório PASS/FAIL sem modificar nada.

.PARAMETER ProjectPath
    Caminho do projeto a ser auditado.

.EXAMPLE
    .\audit_doc25.ps1 -ProjectPath "C:\MCP-Projects\MeuProjeto"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectPath
)

$ErrorActionPreference = "Stop"

# Cores
$Green = [ConsoleColor]::Green
$Red = [ConsoleColor]::Red
$Yellow = [ConsoleColor]::Yellow
$Cyan = [ConsoleColor]::Cyan
$White = [ConsoleColor]::White

# Resultados
$Results = @()

function Test-Item {
    param(
        [string]$Name,
        [string]$Path,
        [bool]$Required = $true,
        [string]$TestType = "exists"
    )
    
    $FullPath = Join-Path $ProjectPath $Path
    $Exists = Test-Path $FullPath
    
    $Status = "PASS"
    $Note = ""
    
    if ($Required) {
        if ($Exists -and $TestType -eq "exists") {
            $Status = "PASS"
            $Note = "OK"
        } elseif ($Exists -and $TestType -eq "not_exists") {
            $Status = "FAIL"
            $Note = "Não deveria existir"
        } else {
            $Status = "FAIL"
            $Note = "Ausente"
        }
    } else {
        if ($Exists) {
            $Status = "PASS"
            $Note = "OK (opcional)"
        } else {
            $Status = "WARN"
            $Note = "Ausente (opcional)"
        }
    }
    
    return @{
        Name = $Name
        Path = $Path
        Status = $Status
        Note = $Note
        Required = $Required
    }
}

Write-Host ""
Write-Host "=== AUDIT DOC2.5 ===" -ForegroundColor $Cyan
Write-Host "Projeto: $ProjectPath"
Write-Host "Data: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host ""

# Testes de estrutura
Write-Host "[1/5] Verificando estrutura básica..." -ForegroundColor $Yellow

$Results += Test-Item -Name "README.md na raiz" -Path "README.md" -Required $true
$Results += Test-Item -Name "Dev_Tracking.md (índice)" -Path "Dev_Tracking.md" -Required $true
$Results += Test-Item -Name "Dev_Tracking_SX.md (ativa)" -Path "Dev_Tracking_S*.md" -Required $true
$Results += Test-Item -Name "docs/ (pasta)" -Path "docs" -Required $true
$Results += Test-Item -Name "Templates/ (pasta)" -Path "Templates" -Required $true
$Results += Test-Item -Name "Sprint/ (pasta)" -Path "Sprint" -Required $true
$Results += Test-Item -Name "tests/ (pasta)" -Path "tests" -Required $true
$Results += Test-Item -Name "rules/ (pasta)" -Path "rules" -Required $false

# Testes de docs/
Write-Host "[2/5] Verificando docs/ (4 arquivos canônicos)..." -ForegroundColor $Yellow

$DocsPath = Join-Path $ProjectPath "docs"
$RequiredDocs = @("SETUP.md", "ARCHITECTURE.md", "DEVELOPMENT.md", "OPERATIONS.md")
$ActualDocs = @()

if (Test-Path $DocsPath) {
    $ActualDocs = Get-ChildItem -Path $DocsPath -Filter "*.md" | Select-Object -ExpandProperty Name
}

$DocsOk = $true
foreach ($ReqDoc in $RequiredDocs) {
    if ($ActualDocs -contains $ReqDoc) {
        $Results += @{
            Name = "docs/$ReqDoc"
            Path = "docs/$ReqDoc"
            Status = "PASS"
            Note = "OK"
            Required = $true
        }
    } else {
        $Results += @{
            Name = "docs/$ReqDoc"
            Path = "docs/$ReqDoc"
            Status = "FAIL"
            Note = "Ausente"
            Required = $true
        }
        $DocsOk = $false
    }
}

# Verificar docs/README.md não existe
$Results += Test-Item -Name "docs/README.md não existe" -Path "docs/README.md" -Required $true -TestType "not_exists"

# Verificar docs/INDEX.md não existe
$Results += Test-Item -Name "docs/INDEX.md não existe" -Path "docs/INDEX.md" -Required $true -TestType "not_exists"

# Verificar subpastas em docs/
$HasSubfolders = $false
if (Test-Path $DocsPath) {
    $Subfolders = Get-ChildItem -Path $DocsPath -Directory -ErrorAction SilentlyContinue
    if ($Subfolders) {
        $HasSubfolders = $true
    }
}

if ($HasSubfolders) {
    $Results += @{
        Name = "docs/ sem subpastas"
        Path = "docs/"
        Status = "FAIL"
        Note = "Contém subpastas (violação)"
        Required = $true
    }
} else {
    $Results += @{
        Name = "docs/ sem subpastas"
        Path = "docs/"
        Status = "PASS"
        Note = "OK"
        Required = $true
    }
}

# Testes de Templates/
Write-Host "[3/5] Verificando Templates/..." -ForegroundColor $Yellow

$TemplatesPath = Join-Path $ProjectPath "Templates"
$RequiredTemplates = @("SETUP.md", "ARCHITECTURE.md", "DEVELOPMENT.md", "OPERATIONS.md")

if (Test-Path $TemplatesPath) {
    $Results += @{
        Name = "Templates/ existe"
        Path = "Templates"
        Status = "PASS"
        Note = "OK"
        Required = $true
    }
    
    $ActualTemplates = Get-ChildItem -Path $TemplatesPath -Filter "*.md" | Select-Object -ExpandProperty Name
    
    foreach ($ReqTemplate in $RequiredTemplates) {
        if ($ActualTemplates -contains $ReqTemplate) {
            $Results += @{
                Name = "Templates/$ReqTemplate"
                Path = "Templates/$ReqTemplate"
                Status = "PASS"
                Note = "OK"
                Required = $true
            }
        }
    }
} else {
    $Results += @{
        Name = "Templates/ existe"
        Path = "Templates"
        Status = "FAIL"
        Note = "Ausente"
        Required = $true
    }
}

# Testes de tests/
Write-Host "[4/5] Verificando tests/..." -ForegroundColor $Yellow

$TestsPath = Join-Path $ProjectPath "tests"
$Results += Test-Item -Name "tests/bugs_log.md" -Path "tests\bugs_log.md" -Required $true

# Verificar README na raiz com tabela de sprints
Write-Host "[5/5] Verificando README com tabela de sprints..." -ForegroundColor $Yellow

$ReadmePath = Join-Path $ProjectPath "README.md"
$HasTable = $false

if (Test-Path $ReadmePath) {
    $Content = Get-Content $ReadmePath -Raw -ErrorAction SilentlyContinue
    if ($Content -match "Controle de Sprints") {
        $HasTable = $true
    }
}

if ($HasTable) {
    $Results += @{
        Name = "README com tabela de sprints"
        Path = "README.md"
        Status = "PASS"
        Note = "Tabela encontrada"
        Required = $true
    }
} else {
    $Results += @{
        Name = "README com tabela de sprints"
        Path = "README.md"
        Status = "FAIL"
        Note = "Tabela ausente"
        Required = $true
    }
}

# Resumo
Write-Host ""
Write-Host "=== RESULTADO DO AUDIT ===" -ForegroundColor $Cyan
Write-Host ""

$PassCount = ($Results | Where-Object { $_.Status -eq "PASS" }).Count
$FailCount = ($Results | Where-Object { $_.Status -eq "FAIL" }).Count
$WarnCount = ($Results | Where-Object { $_.Status -eq "WARN" }).Count
$Total = $Results.Count

Write-Host "Total de testes: $Total" -ForegroundColor $White
Write-Host "PASS: $PassCount" -ForegroundColor $Green
Write-Host "FAIL: $FailCount" -ForegroundColor $Red
Write-Host "WARN: $WarnCount" -ForegroundColor $Yellow
Write-Host ""

# Matriz detalhada
Write-Host "=== MATRIZ DETALHADA ===" -ForegroundColor $Cyan
Write-Host ""

$Results | ForEach-Object {
    $Color = $White
    if ($_.Status -eq "PASS") { $Color = $Green }
    elseif ($_.Status -eq "FAIL") { $Color = $Red }
    elseif ($_.Status -eq "WARN") { $Color = $Yellow }
    
    $Req = ""
    if ($_.Required) { $Req = "[REQ]" } else { $Req = "[OPT]" }
    
    Write-Host "$($_.Status) $Req $($_.Name)" -ForegroundColor $Color
    Write-Host "       $($_.Note)" -ForegroundColor $Gray
    Write-Host ""
}

# Veredicto final
Write-Host "=== VEREDITO ===" -ForegroundColor $Cyan

if ($FailCount -eq 0) {
    Write-Host "PASS - Projeto conforme DOC2.5" -ForegroundColor $Green
    exit 0
} else {
    Write-Host "FAIL - Projeto não conforme DOC2.5" -ForegroundColor $Red
    Write-Host ""
    Write-Host "Ações necessárias:" -ForegroundColor $Yellow
    $FailItems = $Results | Where-Object { $_.Status -eq "FAIL" }
    $FailItems | ForEach-Object {
        Write-Host "  - $($_.Name): $($_.Note)" -ForegroundColor $White
    }
    exit 1
}
