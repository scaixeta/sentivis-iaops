# Dev_Tracking - Indice de Sprints

## Projeto

- Nome: `{{PROJECT_NAME}}`
- Objetivo: `{{PROJECT_OBJECTIVE}}`
- Fase atual: `{{CURRENT_PHASE}}`
- Escopo aprovado: `{{APPROVED_SCOPE}}`

## Sprint Ativa

- **`{{ACTIVE_SPRINT}}`** - `{{ACTIVE_SPRINT_STATUS}}`

## Lista de Sprints

| Sprint | Periodo | Estado | Link |
|---|---|---|---|
| `{{ACTIVE_SPRINT}}` | `{{SPRINT_PERIOD}}` | `{{ACTIVE_SPRINT_STATUS}}` | `Dev_Tracking_{{ACTIVE_SPRINT}}.md` |

## Registros

- `{{DATE_UTC_1}}` - `{{TRACKING_ENTRY_1}}`
- `{{DATE_UTC_2}}` - `{{TRACKING_ENTRY_2}}`
- `{{DATE_UTC_3}}` - `{{TRACKING_ENTRY_3}}`

## Observacoes

- Sprints encerradas devem ser movidas para `Sprint/Dev_Tracking_SX.md`
- O arquivo ativo permanece na raiz (`Dev_Tracking_SX.md`)
- Manter este indice sincronizado com `README.md` e `tests/bugs_log.md`
- Manter apenas uma sprint ativa por vez
- Registrar aqui apenas mudancas de estado, marcos relevantes e correcoes estruturais do projeto
- Decisoes detalhadas e backlog pertencem ao `Dev_Tracking_SX.md` da sprint ativa

## Regras de atualizacao

- Atualizar este indice quando a sprint ativa mudar de estado
- Atualizar este indice quando uma nova sprint for aberta
- Atualizar este indice quando houver correcao estrutural relevante no projeto
- Nao duplicar aqui o backlog detalhado da sprint
- Garantir coerencia entre este arquivo, `README.md`, `Dev_Tracking_{{ACTIVE_SPRINT}}.md` e `tests/bugs_log.md`

---

## Timestamp UTC

Event | Start | Finish | Status
---|---|---|---
`{{ACTIVE_SPRINT}}` | `{{TIMESTAMP_START}}` | `{{TIMESTAMP_FINISH}}` | `{{ACTIVE_SPRINT_STATUS}}`
