<#
.SYNOPSIS
    Inicializa um novo projeto com estrutura DOC2.5.

.DESCRIPTION
    Este script cria um novo projeto com a estrutura canônica DOC2.5,
    incluindo templates, docs/, Sprint/, tests/, e outros artefatos.

.PARAMETER ProjectName
    Nome do novo projeto.

.PARAMETER TargetPath
    Caminho onde o projeto será criado.

.PARAMETER Scope
    Descrição curta do escopo do projeto.

.PARAMETER Mode
    Modo de operação: 'standalone' (padrão) ou 'workspace-linked'.

.EXAMPLE
    .\init_project.ps1 -ProjectName "MeuProjeto" -TargetPath "C:\MCP-Projects" -Scope "descrição"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectName,

    [Parameter(Mandatory=$true)]
    [string]$TargetPath,

    [Parameter(Mandatory=$false)]
    [string]$Scope = "Projeto novo",

    [Parameter(Mandatory=$false)]
    [ValidateSet('standalone', 'workspace-linked')]
    [string]$Mode = 'standalone'
)

$ErrorActionPreference = "Stop"

# Paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CindyRoot = Split-Path -Parent $ScriptDir
$TemplatesPath = Join-Path $CindyRoot "Templates"
$TargetProjectPath = Join-Path $TargetPath $ProjectName

Write-Host "=== Inicializando projeto DOC2.5: $ProjectName ===" -ForegroundColor Cyan
Write-Host "Caminho: $TargetProjectPath"
Write-Host "Modo: $Mode"
Write-Host ""

# Verificar se projeto já existe
if (Test-Path $TargetProjectPath) {
    Write-Error "Projeto já existe: $TargetProjectPath"
    exit 1
}

# Criar diretório do projeto
Write-Host "[1/8] Criando diretório do projeto..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path $TargetProjectPath -Force | Out-Null

# Copiar Templates/
Write-Host "[2/8] Copiando Templates/..." -ForegroundColor Yellow
$DestTemplates = Join-Path $TargetProjectPath "Templates"
Copy-Item -Path $TemplatesPath -Destination $DestTemplates -Recurse -Force

# Criar docs/ com 4 arquivos canônicos
Write-Host "[3/8] Criando docs/..." -ForegroundColor Yellow
$DocsPath = Join-Path $TargetProjectPath "docs"
New-Item -ItemType Directory -Path $DocsPath -Force | Out-Null

$DocFiles = @("SETUP.md", "ARCHITECTURE.md", "DEVELOPMENT.md", "OPERATIONS.md")
foreach ($DocFile in $DocFiles) {
    $SrcDoc = Join-Path $TemplatesPath $DocFile
    if (Test-Path $SrcDoc) {
        Copy-Item -Path $SrcDoc -Destination $DocsPath -Force
    }
}

# Criar Sprint/ folder
Write-Host "[4/8] Criando Sprint/..." -ForegroundColor Yellow
$SprintPath = Join-Path $TargetProjectPath "Sprint"
New-Item -ItemType Directory -Path $SprintPath -Force | Out-Null

# Criar tests/bugs_log.md
Write-Host "[5/8] Criando tests/bugs_log.md..." -ForegroundColor Yellow
$TestsPath = Join-Path $TargetProjectPath "tests"
New-Item -ItemType Directory -Path $TestsPath -Force | Out-Null
$BugLogContent = @"
# Bugs Log — Testes e Bugs

Este arquivo centraliza todos os testes e bugs do projeto, organizados por sprint.

## Sprint S0

### Bugs

- [BUG-S0-01] — [título curto]
  - Descrição:
  - Status: [Aberto/Fechado]
  - Referência: ver Dev_Tracking_S0.md

### Testes

- [TEST-S0-01] — [descrição de teste]
  - Resultado: [Passou/Falhou]
  - Referência: ver Dev_Tracking_S0.md
"@
$BugLogContent | Out-File -FilePath (Join-Path $TestsPath "bugs_log.md") -Encoding UTF8

# Criar Dev_Tracking_S0.md
Write-Host "[6/8] Criando Dev_Tracking_S0.md..." -ForegroundColor Yellow
$DevTrackingContent = @"
# Dev_Tracking – Sprint S0 ($ProjectName)

## 1. Identificação da Sprint

- Sprint: S0
- Projeto: $ProjectName
- Período: $(Get-Date -Format "yyyy-MM-dd")
- Contexto inicial:
  - $Scope

---

## 2. Objetivos da Sprint

- [OBJ-S0-01] Estruturar projeto com DOC2.5
- [OBJ-S0-02] Definir escopo inicial

---

## 3. Backlog da Sprint (STATUS | ESTÓRIA)

- To-Do | ST-S0-01 – Configuração inicial do projeto
- To-Do | ST-S0-02 – Definir requisitos

---

## 4. Interações e Decisões Relevantes da Sprint

- [D-S0-01] $(Get-Date -Format "yyyy-MM-dd") – Inicialização do projeto via init_project.ps1
  - Impacto: Estrutura DOC2.5 criada
  - Arquivos afetados: todos

---

## 5. Referências a Testes e Bugs (resumo)

- Inicial: ver tests/bugs_log.md

---

## 6. Política de Commits

- Nenhum commit sem autorização explícita do PO

---

## 7. Estado final da Sprint

(Preencher ao encerrar a sprint S0.)

---

## 8. Commit de Fechamento

- `S0-END: inicialização do projeto`
"@
$DevTrackingContent | Out-File -FilePath (Join-Path $TargetProjectPath "Dev_Tracking_S0.md") -Encoding UTF8

# Criar Dev_Tracking.md (índice)
Write-Host "[7/8] Criando Dev_Tracking.md..." -ForegroundColor Yellow
$IndexContent = @"
# Dev_Tracking — Índice de Sprints

## Sprints Encerradas

- Nenhuma sprint encerrada

## Sprint Ativa

- Dev_Tracking_S0.md - S0: Inicialização

## Como Usar

1. Sprint ativa: Dev_Tracking_SX.md na raiz
2. Encerradas: Sprint/Dev_Tracking_SX.md
3. Testes/Bugs: tests/bugs_log.md
"@
$IndexContent | Out-File -FilePath (Join-Path $TargetProjectPath "Dev_Tracking.md") -Encoding UTF8

# Criar README.md
Write-Host "[8/8] Criando README.md..." -ForegroundColor Yellow
$ReadmeContent = @"
# $ProjectName

> Projeto inicializado com estrutura DOC2.5

## Escopo

$Scope

## Controle de Sprints

| Nome da Sprint | Objetivo | Entregas | Bugs | Estado |
|----------------|----------|----------|------|--------|
| S0 | Inicialização | Estrutura inicial | - | Ativa |

## Estrutura

- `docs/` — Documentação canônica (SETUP, ARCHITECTURE, DEVELOPMENT, OPERATIONS)
- `Templates/` — Pack de templates
- `Sprint/` — Sprints arquivadas
- `tests/bugs_log.md` — Log de testes e bugs
- `Dev_Tracking_S0.md` — Sprint ativa

## Próximos Passos

1. Ajustar README.md com informações do projeto
2. Preencher docs/ com conteúdo específico
3. Executar scripts/audit_doc25.ps1 para validar estrutura
"@
$ReadmeContent | Out-File -FilePath (Join-Path $TargetProjectPath "README.md") -Encoding UTF8

Write-Host ""
Write-Host "=== Projeto criado com sucesso! ===" -ForegroundColor Green
Write-Host "Local: $TargetProjectPath"
Write-Host ""
Write-Host "Próximos passos:" -ForegroundColor Cyan
Write-Host "1. cd $TargetProjectPath"
Write-Host "2. Ajustar README.md e docs/"
Write-Host "3. Executar audit: scripts\audit_doc25.ps1 -ProjectPath `"$TargetProjectPath`""
