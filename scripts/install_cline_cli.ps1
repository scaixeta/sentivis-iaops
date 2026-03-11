<#
.SYNOPSIS
    Instala e configura o Cline CLI 2.0 (cli/) no workspace.

.DESCRIPTION
    O Cline CLI 2.0 permite executar agentes de IA diretamente no terminal,
    sem dependência do VS Code. Os agentes ficam em .agents/ e são acessíveis
    tanto pelo VSCode (extensão Cline) quanto pelo CLI.

    Este script:
      1. Verifica pré-requisitos (Node.js 18+, npm 9+)
      2. Instala dependências npm
      3. Compila o TypeScript
      4. Faz npm link para disponibilizar o comando `cline` globalmente
      5. Verifica a instalação com `cline --help`
      6. Copia Cindy_Contract.md para o diretório esperado pelo CLI

.PARAMETER WorkspaceRoot
    Caminho raiz do workspace. Padrão: detecta automaticamente.

.PARAMETER SkipLink
    Pula o npm link (não registra o comando `cline` globalmente).
    Útil em ambientes onde npm link não é permitido.

.PARAMETER ContractSource
    Caminho para o Cindy_Contract.md a ser usado pelo CLI.
    Padrão: <WorkspaceRoot>/Cindy/Cindy_Contract.md

.EXAMPLE
    # Instalação padrão (recomendada)
    .\install_cline_cli.ps1

.EXAMPLE
    # Sem link global
    .\install_cline_cli.ps1 -SkipLink

.EXAMPLE
    # Workspace customizado
    .\install_cline_cli.ps1 -WorkspaceRoot "D:\MeuWorkspace"
#>

param(
    [string]$WorkspaceRoot = "",
    [switch]$SkipLink,
    [string]$ContractSource = ""
)

$ErrorActionPreference = "Stop"

# Cores
$Green  = [ConsoleColor]::Green
$Red    = [ConsoleColor]::Red
$Yellow = [ConsoleColor]::Yellow
$Cyan   = [ConsoleColor]::Cyan
$Gray   = [ConsoleColor]::Gray
$White  = [ConsoleColor]::White

# Detectar workspace root
if (-not $WorkspaceRoot) {
    $ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $WorkspaceRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)
}

$CliPath     = Join-Path $WorkspaceRoot "cli"
$CliDistPath = Join-Path $CliPath "dist"

Write-Host ""
Write-Host "=== INSTALL CLINE CLI 2.0 ===" -ForegroundColor $Cyan
Write-Host "Workspace:  $WorkspaceRoot"
Write-Host "CLI Path:   $CliPath"
Write-Host ""

# --- 1. Verificar pré-requisitos ---
Write-Host "[1/6] Verificando pré-requisitos..." -ForegroundColor $Yellow

# Node.js
try {
    $NodeVersion = node --version 2>&1
    $NodeMajor = [int]($NodeVersion -replace "v(\d+)\..*", '$1')
    if ($NodeMajor -lt 18) {
        Write-Host "ERRO: Node.js $NodeVersion detectado. Requer Node.js 18+." -ForegroundColor $Red
        exit 1
    }
    Write-Host "  Node.js: $NodeVersion" -ForegroundColor $Green
} catch {
    Write-Host "ERRO: Node.js nao encontrado. Instale Node.js 18+ antes de continuar." -ForegroundColor $Red
    Write-Host "  Download: https://nodejs.org/" -ForegroundColor $White
    exit 1
}

# npm
try {
    $NpmVersion = npm --version 2>&1
    $NpmMajor = [int]($NpmVersion -split "\.")[0]
    if ($NpmMajor -lt 9) {
        Write-Host "WARN: npm $NpmVersion detectado. Recomendado npm 9+." -ForegroundColor $Yellow
    } else {
        Write-Host "  npm: $NpmVersion" -ForegroundColor $Green
    }
} catch {
    Write-Host "ERRO: npm nao encontrado." -ForegroundColor $Red
    exit 1
}

# Verificar diretório cli/
if (-not (Test-Path $CliPath)) {
    Write-Host "ERRO: Diretório cli/ não encontrado em $CliPath" -ForegroundColor $Red
    Write-Host "  O cli/ deve estar na raiz do workspace: $WorkspaceRoot" -ForegroundColor $White
    exit 1
}

Write-Host "  cli/: OK" -ForegroundColor $Green

# --- 2. Instalar dependências ---
Write-Host ""
Write-Host "[2/6] Instalando dependências npm..." -ForegroundColor $Yellow

Push-Location $CliPath
try {
    npm install 2>&1 | ForEach-Object { Write-Host "  $_" -ForegroundColor $Gray }
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERRO: npm install falhou." -ForegroundColor $Red
        exit 1
    }
    Write-Host "  Dependências instaladas." -ForegroundColor $Green
} finally {
    Pop-Location
}

# --- 3. Compilar TypeScript ---
Write-Host ""
Write-Host "[3/6] Compilando TypeScript (npm run build)..." -ForegroundColor $Yellow

Push-Location $CliPath
try {
    npm run build 2>&1 | ForEach-Object { Write-Host "  $_" -ForegroundColor $Gray }
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERRO: npm run build falhou." -ForegroundColor $Red
        exit 1
    }

    if (-not (Test-Path $CliDistPath)) {
        Write-Host "ERRO: dist/ nao foi gerado após build." -ForegroundColor $Red
        exit 1
    }
    Write-Host "  Build concluído: $CliDistPath" -ForegroundColor $Green
} finally {
    Pop-Location
}

# --- 4. npm link (global) ---
Write-Host ""
if ($SkipLink) {
    Write-Host "[4/6] npm link ignorado (-SkipLink)." -ForegroundColor $Yellow
    Write-Host "  Para usar o CLI sem link global:"
    Write-Host "    node $CliPath\bin\cli.js --help" -ForegroundColor $White
} else {
    Write-Host "[4/6] Registrando comando `cline` globalmente (npm link)..." -ForegroundColor $Yellow
    Push-Location $CliPath
    try {
        npm link 2>&1 | ForEach-Object { Write-Host "  $_" -ForegroundColor $Gray }
        if ($LASTEXITCODE -ne 0) {
            Write-Host "WARN: npm link falhou. Tente com -SkipLink ou execute como administrador." -ForegroundColor $Yellow
        } else {
            Write-Host "  Comando `cline` registrado globalmente." -ForegroundColor $Green
        }
    } finally {
        Pop-Location
    }
}

# --- 5. Copiar Cindy_Contract.md para o fallback canônico do CLI ---
Write-Host ""
Write-Host "[5/6] Configurando Cindy_Contract.md para o CLI..." -ForegroundColor $Yellow

$CliContractPath = Join-Path $CliPath "Cindy_Contract.md"

if (-not $ContractSource) {
    $ContractSource = Join-Path $WorkspaceRoot "Cindy\Cindy_Contract.md"
}

if (Test-Path $ContractSource) {
    Copy-Item -Path $ContractSource -Destination $CliContractPath -Force
    Write-Host "  Contrato copiado: $ContractSource -> $CliContractPath" -ForegroundColor $Green
} elseif (Test-Path $CliContractPath) {
    Write-Host "  Contrato já existente em cli/Cindy_Contract.md — mantido." -ForegroundColor $Gray
} else {
    Write-Host "  WARN: Cindy_Contract.md não encontrado. O CLI usará find-up ou pedirá --contract." -ForegroundColor $Yellow
}

# --- 6. Verificar instalação ---
Write-Host ""
Write-Host "[6/6] Verificando instalação..." -ForegroundColor $Yellow

if (-not $SkipLink) {
    try {
        $HelpOutput = cline --help 2>&1
        if ($LASTEXITCODE -eq 0 -or $HelpOutput -match "cline") {
            Write-Host "  cline --help: OK" -ForegroundColor $Green
        } else {
            Write-Host "  WARN: cline --help retornou código $LASTEXITCODE" -ForegroundColor $Yellow
        }
    } catch {
        Write-Host "  WARN: Comando `cline` não disponível no PATH atual." -ForegroundColor $Yellow
        Write-Host "        Reinicie o terminal e tente novamente." -ForegroundColor $White
    }
}

# Verificar subagents DOC2.5
try {
    if (-not $SkipLink) {
        $ListOutput = cline doc25 list 2>&1
        Write-Host "  Subagents DOC2.5:" -ForegroundColor $White
        $ListOutput | ForEach-Object { Write-Host "    $_" -ForegroundColor $Gray }
    }
} catch {
    Write-Host "  WARN: `cline doc25 list` não disponível (normal se link foi ignorado)." -ForegroundColor $Yellow
}

# --- Resumo ---
Write-Host ""
Write-Host "=== INSTALAÇÃO CONCLUÍDA ===" -ForegroundColor $Cyan
Write-Host ""
Write-Host "Próximos passos:" -ForegroundColor $White
Write-Host "  1. Reiniciar o terminal (para que o PATH seja atualizado)" -ForegroundColor $Gray
Write-Host "  2. Testar: cline --help" -ForegroundColor $Gray
Write-Host "  3. Listar agentes: cline agent list" -ForegroundColor $Gray
Write-Host "  4. Validar DOC2.5: cline doc25 validate --project <caminho-do-projeto>" -ForegroundColor $Gray
Write-Host ""
Write-Host "Agentes disponíveis em: $WorkspaceRoot\.agents\" -ForegroundColor $Green
Write-Host "Contrato ativo: $CliContractPath" -ForegroundColor $Green
Write-Host ""
exit 0
