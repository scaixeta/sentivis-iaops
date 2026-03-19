# Contrato Cindy Context Router (DOC2.5)

## 1. Contexto de Runtime

Este contrato define o contexto discoverable da Cindy no inicio de cada run.

| Componente | Valor | Fonte de Verdade |
|---|---|---|
| `orchestrator` | `auto-detect` | Estrutura do workspace |
| `execution_surface` | `vscode` / `cli` | Ambiente de execucao |
| `workspace_root` | `{{WORKSPACE_ROOT}}` | CWD |
| `doutrina` | `DOC2.5` | `rules/WORKSPACE_RULES.md` |

## 2. Orquestradores Validos

| Orchestrator | Entry Point | Rules | Skills |
|---|---|---|---|
| `codex` | `.codex/` | `.codex/rules/WORKSPACE_RULES_GLOBAL.md` | `.codex/skills/` |
| `cline` | `.clinerules/` | `.clinerules/WORKSPACE_RULES_GLOBAL.md` | `.cline/skills/` |
| `antigravity` | `.agents/` | `.agents/rules/` | `.agents/skills/` |

Notas operacionais:

- `.clinerules/` e `.cline/` possuem papeis diferentes e complementares no runtime Cline
- `.agents/skills/` permanece a canonical authoring source of truth das skills comuns
- `rules/WORKSPACE_RULES.md` prevalece sobre este contrato quando houver conflito

---

## 3. Registro de Skills

A Cindy deve consultar o registro de skills antes de propor execucao.

### Localizacao de Skills

1. `.agents/skills/` como source of truth canônica
2. `.clinerules/workflows/` quando a necessidade for de workflow DOC2.5 explicito
3. `.cline/skills/` como runtime counterpart do Cline
4. `.codex/skills/` como runtime counterpart do Codex
5. `mcp/` quando existir

### Regra de Selecao

```text
RANKING_DE_SKILLS:
  1. Skill canônica em .agents/skills/
  2. Workflow DOC2.5 em .clinerules/workflows/
  3. Skill do runtime ativo (.cline/skills/ ou .codex/skills/)
  4. MCP server quando existir
  5. Execucao direta como fallback
```

---

## 4. Regras de Despacho

### Gates Obrigatorios

| Gate | Quando | Regra |
|---|---|---|
| Aprovacao de Plano | Antes de executar | Plano aprovado pelo PO |
| Confirmacao de Escrita | Antes de alterar arquivos | Planejamento e aprovacao |
| Commit/Push | Antes de `git commit`/`git push` | Ordem expressa do PO |

### Regras de Despacho

```text
DISPATCH_REGRAS:
  - README.md: entry point oficial
  - rules/WORKSPACE_RULES.md: fonte operacional obrigatoria
  - Cindy_Contract.md: contrato canonico de descoberta
  - baseline de geracao: quando README.md/tracking/docs finais ainda nao existirem, usar Templates/README.md como ponto de partida
  - docs/: apenas 4 documentos canonicos
  - Templates/: fonte principal de geracao documental
  - commits: apenas por ordem expressa do PO
```

---

## 5. Contrato de Descoberta

### Entry Flow

```text
CINDY_ENTRY:
  1. Ler rules/WORKSPACE_RULES.md
  2. Identificar orchestrator e superficie de execucao
  3. Ler a regra global do runtime ativo
  4. Classificar workspace como repo materializado ou baseline de geracao
  5. Consultar skill registry
  6. Validar gates obrigatorios
  7. Propor plano ao PO
```

### Markers Canonicos

| Marker | Tipo | Significado |
|---|---|---|
| `.clinerules/` | Diretorio | Runtime Cline disponivel |
| `.cline/skills/` | Diretorio | Skills do runtime Cline |
| `.codex/skills/` | Diretorio | Skills do runtime Codex |
| `.agents/rules/` | Diretorio | Regras do Antigravity |
| `.agents/skills/` | Diretorio | Skills canônicas comuns |
| `README.md` | Arquivo | Entry point oficial |
| `Templates/README.md` | Arquivo | Entry point de bootstrap quando o projeto ainda nao foi materializado |
| `rules/WORKSPACE_RULES.md` | Arquivo | Fonte operacional obrigatoria |
| `Cindy_Contract.md` | Arquivo | Contrato canonico do workspace |

---

## 6. Portabilidade de Skills

A arquitetura de habilidades da Cindy adota o modelo de portabilidade cruzada:

- `.agents/skills/` e a fonte primaria de autoria das skills comuns
- `.cline/skills/` e `.codex/skills/` sao runtimes counterparts legitimos
- adaptacoes de runtime sao permitidas quando nao alterarem a governanca canônica
- qualquer drift relevante deve ser tratado como adaptacao justificada ou inconsistencia a corrigir

### Pre-Flight Contratual

```text
PRE_FLIGHT_CHECK:
  [ ] Runtime context identificado
  [ ] Regras locais lidas
  [ ] Regras do runtime ativo lidas
  [ ] Skills consultadas no registry
  [ ] Gates obrigatorios claros
  [ ] Aprovacao do PO quando houver alteracao
```

---

Versao: 1.2
Template: Portavel
Doutrina: DOC2.5
