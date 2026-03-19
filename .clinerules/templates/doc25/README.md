# {{PROJECT_NAME}}

## {{WORKSTREAM_NAME}}

Resumo executivo do projeto em pt-BR, com foco no objetivo atual, no valor esperado e no limite de escopo da sprint/fase em vigor.

---

## 1. Visao geral

O `{{PROJECT_NAME}}` e o repositorio raiz para:

- {{PRIMARY_SCOPE_1}}
- {{PRIMARY_SCOPE_2}}
- {{PRIMARY_SCOPE_3}}

Objetivos principais:

- {{MAIN_OBJECTIVE_1}}
- {{MAIN_OBJECTIVE_2}}
- {{MAIN_OBJECTIVE_3}}

## 2. Estado atual

- Sprint ativa: `{{ACTIVE_SPRINT}}`
- Estado da sprint: `{{SPRINT_STATUS}}`
- Fase atual: `{{CURRENT_PHASE}}`
- Escopo aprovado: `{{APPROVED_SCOPE}}`

## 3. Controle de sprints

| Sprint | Periodo | Estado | Tracking | Observacoes |
| --- | --- | --- | --- | --- |
| {{ACTIVE_SPRINT}} | {{SPRINT_PERIOD}} | {{SPRINT_STATUS}} | `Dev_Tracking_{{ACTIVE_SPRINT}}.md` | {{SPRINT_NOTES}} |

## 4. Estrutura canonica do projeto

- `README.md` -> entry point unico do projeto
- `Dev_Tracking.md` -> indice leve das sprints
- `Dev_Tracking_{{ACTIVE_SPRINT}}.md` -> sprint ativa
- `docs/SETUP.md` -> preparo de contexto, ambiente e fontes
- `docs/ARCHITECTURE.md` -> arquitetura e modelo conceitual
- `docs/DEVELOPMENT.md` -> roadmap, backlog e modo de evolucao
- `docs/OPERATIONS.md` -> operacao corrente, gates e governanca
- `tests/bugs_log.md` -> bugs, inconsistencias e evidencias de teste
- `Sprint/` -> arquivo historico de sprints encerradas

## 5. Leitura recomendada

1. `rules/WORKSPACE_RULES.md`
2. `.clinerules/WORKSPACE_RULES_GLOBAL.md`
3. `Cindy_Contract.md` quando o contrato estiver presente no repositorio
4. `README.md`
5. `docs/SETUP.md`
6. `docs/ARCHITECTURE.md`
7. `docs/DEVELOPMENT.md`
8. `docs/OPERATIONS.md`
9. `Dev_Tracking.md`
10. `Dev_Tracking_{{ACTIVE_SPRINT}}.md`

## 6. Regras operacionais

- Seguir DOC2.5 como modelo canonico de documentacao e rastreabilidade
- Manter apenas os caminhos canonicos do projeto
- Registrar decisoes e mudancas relevantes em `Dev_Tracking`
- Nao criar automacao, integracao ou scripts fora do escopo aprovado
- Tratar inferencias como inferencias e manter unknowns explicitos
- Commit e push apenas sob ordem explicita do PO

## 7. Documentacao canonica

O modelo canonico do projeto deve manter apenas os quatro documentos oficiais em `docs/`:

- `docs/SETUP.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT.md`
- `docs/OPERATIONS.md`

> `docs/README.md` e `docs/INDEX.md` nao fazem parte do modelo canonico DOC2.5.

## 8. Como comecar

1. Ler as regras locais e globais do workspace.
2. Confirmar a sprint ativa em `Dev_Tracking.md`.
3. Ler a sprint ativa em `Dev_Tracking_{{ACTIVE_SPRINT}}.md`.
4. Seguir a ordem dos quatro documentos canonicos em `docs/`.
5. Executar apenas o escopo explicitamente aprovado para a fase atual.

---

## Cindy - Orquestradora (Context Router)

A Cindy atua como agente principal do projeto. Em cada run, ela identifica o contexto ativo, descobre as skills e workflows disponiveis no runtime atual e respeita os gates DOC2.5 antes de qualquer execucao.

<p align="center">
  <img src=".brand/Cindy.jpg" alt="Cindy - Agent Orchestrator" width="320" />
</p>

*Este repositorio e orquestrado pela Cindy sob a doutrina DOC2.5.*
