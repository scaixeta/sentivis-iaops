# Contrato Cindy Context Router (DOC2.5)

## 1. Runtime Context

Este contrato define o contexto de execucao discoverable pela Cindy no inicio de cada run.

| Componente | Valor | Fonte de Verdade |
|------------|-------|------------------|
| `orchestrator` | `auto-detect` | Estrutura do workspace |
| `execution_surface` | `vscode` / `cli` | Ambiente de execucao |
| `workspace_root` | `{{WORKSPACE_ROOT}}` | CWD |
| `doutrina` | `DOC2.5` | Regras do workspace |

### Orquestradores Validos

| Orchestrator | Entry Point | Rules | Skills |
|--------------|-------------|-------|--------|
| `codex` | `.codex/` | `.codex/` | `.codex/skills/` |
| `cline` | `.clinerules/` | `.clinerules/WORKSPACE_RULES_GLOBAL.md` | `.cline/skills/` |
| `antigravity` | `.agent/` | `.agent/rules.md` | `.agents/skills/` |

---

## 2. Skill Registry

A Cindy DEVE consultar o registro de skills antes de propor qualquer execucao.

### Localizacao de Skills (Ordem de Prioridade)

1. `.cline/skills/`
2. `.clinerules/workflows/`
3. `.agents/skills/`
4. `.codex/skills/`
5. `mcp/` (quando existir)

### Selecao de Skills

```text
RANKING_DE_SKILLS:
  1. Skill especifica no orchestrator atual
  2. Workflow DOC2.5 em .clinerules/workflows/
  3. Skills de outros orchestrators (se aplicavel)
  4. MCP server em mcp/
  5. Execucao direta (fallback)
```

---

## 3. Dispatch Rules

### Gates Obrigatorios (DOC2.5)

| Gate | Quando | Regra |
|------|--------|-------|
| Aprovacao de Plano | Antes de executar | Plano aprovado pelo PO |
| Commit/Push | Antes de git commit/push | Ordem expressa do PO |
| Confirmacao de Escrita | Antes de alterar arquivos | Planejamento + aprovacao |

### Regras de Despacho

```text
DISPATCH_REGRAS:
  - CLI > VSCode: CLI executa tudo, VSCode delega
  - README.md: entry point oficial
  - docs/: apenas 4 canonicos (quando existir)
  - commits: padrao definido pelo PO
```

---

## 4. Contrato de Descoberta

### Entry Point da Cindy

```text
CINDY_ENTRY:
  1. Ler regras do orchestrator ativo
  2. Identificar orchestrator e superficie de execucao
  3. Consultar skill registry
  4. Validar gates obrigatorios
  5. Propor plano ao PO
```

### Markers Canonicos

| Marker | Tipo | Significado |
|--------|------|-------------|
| `.clinerules/` | Diretorio | Orchestrator Cline disponivel |
| `.agent/rules.md` | Arquivo | Orchestrator Antigravity disponivel |
| `.codex/skills/` | Diretorio | Skills Codex disponiveis |
| `README.md` | Arquivo | Entry point oficial |
| `Cindy_Contract.md` | Arquivo | Contrato canonico do workspace |
| `Cindy_Contract.md` | Arquivo | Fonte unica de verdade do contrato |

---

## 5. Validacao de Compliance

A cada run, a Cindy DEVE validar:

```text
PRE_FLIGHT_CHECK:
  [ ] Runtime context identificado
  [ ] Skills consultadas no registry
  [ ] Gates obrigatorios claros
  [ ] Aprovacao do PO (quando houver alteracao)
```

---

Versao: 1.1
Template: Portavel
Doutrina: DOC2.5
