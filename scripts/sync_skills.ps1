<#
.SYNOPSIS
    Sincroniza skills entre runtimes de agentes (Cline, Codex, Antigravity).

.DESCRIPTION
    Copia skills do diretório fonte para os diretórios alvo,
    mantendo o pack curado sincronizado entre os 3 runtimes.

    Por padrão, sincroniza de .cline/skills/ para .agents/skills/ e .codex/skills/
    Nunca sobrescreve .agent/skills/ (catálogo completo Antigravity — upstream openclaw).

.PARAMETER Source
    Diretório runtime fonte. Padrão: ".cline"
    Valores válidos: ".cline", ".agents", ".codex"

.PARAMETER Targets
    Array de diretórios runtime alvo.
    Padrão: @(".agents", ".codex")
    Valores válidos: ".cline", ".agents", ".codex"
    NUNCA use ".agent" como target (catálogo completo — não sincronizar sobre ele).

.PARAMETER WorkspaceRoot
    Caminho raiz do workspace. Padrão: detecta automaticamente (2 níveis acima de scripts/).

.PARAMETER DryRun
    Simula a sincronização sem copiar arquivos. Útil para validação prévia.

.EXAMPLE
    # Sincronização padrão: .cline -> .agents e .codex
    .\sync_skills.ps1

.EXAMPLE
    # Simular sem copiar
    .\sync_skills.ps1 -DryRun

.EXAMPLE
    # Fonte alternativa
    .\sync_skills.ps1 -Source ".codex" -Targets ".cline", ".agents"

.EXAMPLE
    # Workspace customizado
    .\sync_skills.ps1 -WorkspaceRoot "D:\MeuWorkspace"
#>

param(
    [ValidateSet(".cline", ".agents", ".codex")]
    [string]$Source = ".cline",

    [ValidateSet(".cline", ".agents", ".codex")]
    [string[]]$Targets = @(".agents", ".codex"),

    [string]$WorkspaceRoot = "",

    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

# Cores
$Green  = [ConsoleColor]::Green
$Red    = [ConsoleColor]::Red
$Yellow = [ConsoleColor]::Yellow
$Cyan   = [ConsoleColor]::Cyan
$Gray   = [ConsoleColor]::Gray
$White  = [ConsoleColor]::White

# Detectar workspace root automaticamente
if (-not $WorkspaceRoot) {
    $ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $WorkspaceRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)
}

Write-Host ""
Write-Host "=== SYNC SKILLS ===" -ForegroundColor $Cyan
Write-Host "Workspace: $WorkspaceRoot"
Write-Host "Fonte:     $Source/skills/"
Write-Host "Alvos:     $($Targets -join ', ')/skills/"
if ($DryRun) {
    Write-Host "[DRY RUN] Nenhum arquivo será copiado." -ForegroundColor $Yellow
}
Write-Host ""

# Validar que .agent não está nos targets
if ($Targets -contains ".agent") {
    Write-Host "ERRO: '.agent/skills/' é o catálogo completo Antigravity (upstream openclaw)." -ForegroundColor $Red
    Write-Host "      Nunca sincronize sobre ele. Use apenas: .cline, .agents, .codex" -ForegroundColor $Red
    exit 1
}

# Verificar source
$SourceSkillsPath = Join-Path $WorkspaceRoot "$Source\skills"
if (-not (Test-Path $SourceSkillsPath)) {
    Write-Host "ERRO: Diretório fonte não encontrado: $SourceSkillsPath" -ForegroundColor $Red
    exit 1
}

$SourceSkills = Get-ChildItem -Path $SourceSkillsPath -Directory -ErrorAction SilentlyContinue
$SkillCount = ($SourceSkills | Measure-Object).Count
Write-Host "Skills encontradas na fonte: $SkillCount" -ForegroundColor $White

if ($SkillCount -eq 0) {
    Write-Host "WARN: Nenhuma skill encontrada em $SourceSkillsPath" -ForegroundColor $Yellow
    exit 0
}

Write-Host ""

# Sincronizar para cada target
$TotalCopied = 0
$TotalSkipped = 0
$TotalErrors = 0

foreach ($Target in $Targets) {
    $TargetSkillsPath = Join-Path $WorkspaceRoot "$Target\skills"
    
    Write-Host "--- Sincronizando para $Target/skills/ ---" -ForegroundColor $Cyan
    
    # Criar diretório target se não existir
    if (-not (Test-Path $TargetSkillsPath)) {
        if (-not $DryRun) {
            New-Item -ItemType Directory -Path $TargetSkillsPath -Force | Out-Null
        }
        Write-Host "  Criado: $TargetSkillsPath" -ForegroundColor $Yellow
    }
    
    foreach ($SkillDir in $SourceSkills) {
        $SourceSkillPath = $SkillDir.FullName
        $TargetSkillPath = Join-Path $TargetSkillsPath $SkillDir.Name
        
        # Verificar se skill já existe no target
        $SkillExists = Test-Path $TargetSkillPath
        
        # Verificar se precisa atualizar (comparar SKILL.md)
        $SourceSkillMd = Join-Path $SourceSkillPath "SKILL.md"
        $TargetSkillMd = Join-Path $TargetSkillPath "SKILL.md"
        
        $NeedsUpdate = $false
        if ($SkillExists -and (Test-Path $SourceSkillMd) -and (Test-Path $TargetSkillMd)) {
            $SourceHash = (Get-FileHash $SourceSkillMd -Algorithm MD5).Hash
            $TargetHash = (Get-FileHash $TargetSkillMd -Algorithm MD5).Hash
            $NeedsUpdate = ($SourceHash -ne $TargetHash)
        } elseif (-not $SkillExists) {
            $NeedsUpdate = $true
        }
        
        if ($NeedsUpdate) {
            if (-not $DryRun) {
                try {
                    Copy-Item -Path $SourceSkillPath -Destination $TargetSkillPath -Recurse -Force
                    Write-Host "  COPIADO: $($SkillDir.Name)" -ForegroundColor $Green
                    $TotalCopied++
                } catch {
                    Write-Host "  ERRO ao copiar $($SkillDir.Name): $_" -ForegroundColor $Red
                    $TotalErrors++
                }
            } else {
                Write-Host "  [DRY] Seria copiado: $($SkillDir.Name)" -ForegroundColor $Yellow
                $TotalCopied++
            }
        } else {
            Write-Host "  OK (sem mudanças): $($SkillDir.Name)" -ForegroundColor $Gray
            $TotalSkipped++
        }
    }
    
    Write-Host ""
}

# Resumo
Write-Host "=== RESUMO ===" -ForegroundColor $Cyan
if ($DryRun) {
    Write-Host "Seriam copiados: $TotalCopied skills" -ForegroundColor $Yellow
} else {
    Write-Host "Copiados:  $TotalCopied" -ForegroundColor $Green
}
Write-Host "Sem mudanças: $TotalSkipped" -ForegroundColor $Gray
if ($TotalErrors -gt 0) {
    Write-Host "Erros:     $TotalErrors" -ForegroundColor $Red
    exit 1
}

Write-Host ""
Write-Host "Sync concluído." -ForegroundColor $Green
exit 0
