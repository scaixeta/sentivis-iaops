# Dev_Tracking - Sprint {{SPRINT_ID}} ({{PROJECT_NAME}})

## 1. Identificacao da Sprint

- Sprint: `{{SPRINT_ID}}`
- Projeto: `{{PROJECT_NAME}}`
- Periodo: `{{SPRINT_PERIOD}}`
- Escopo aprovado: `{{APPROVED_SCOPE}}`
- Contexto inicial:
  - `{{SPRINT_CONTEXT_1}}`
  - `{{SPRINT_CONTEXT_2}}`
  - `{{SPRINT_CONTEXT_3}}`

---

## 2. Objetivos da Sprint

- `[OBJ-{{SPRINT_ID}}-01] {{SPRINT_OBJECTIVE_1}}`
- `[OBJ-{{SPRINT_ID}}-02] {{SPRINT_OBJECTIVE_2}}`

---

## 3. Backlog da Sprint (STATUS | ESTORIA)

| Status | Estoria |
|---|---|
| To-Do | `ST-{{SPRINT_ID}}-01 - {{SPRINT_STORY_1}}` |
| To-Do | `ST-{{SPRINT_ID}}-02 - {{SPRINT_STORY_2}}` |

Estados possiveis:
- `To-Do`, `Doing`, `Done`, `Accepted`, `Pending-SX`

---

## 4. Interacoes e Decisoes Relevantes da Sprint

`[D-{{SPRINT_ID}}-01] - {{SPRINT_DECISION_1}}`

Adicionar novas decisoes aqui ao longo da sprint, mantendo impacto e arquivos afetados quando necessario.

---

## 5. Referencias a Testes e Bugs (resumo)

Os detalhes de testes e bugs da sprint devem ser registrados em `tests/bugs_log.md`.

Registrar aqui apenas o minimo necessario:

- `BUG-{{SPRINT_ID}}-01 - {{BUG_SUMMARY_1}} - ver tests/bugs_log.md`

---

## 6. Timestamp UTC

Usar formato DOC2.5 (ISO 8601, 24h): `YYYY-MM-DDTHH:MM:SS-ST` para inicio e `YYYY-MM-DDTHH:MM:SS-FN` para fim.

Event | Start | Finish | Status
---|---|---|---
`ST-{{SPRINT_ID}}-01` | `{{TS_1_START}}` | `{{TS_1_FINISH}}` | `To-Do`
`ST-{{SPRINT_ID}}-02` | `{{TS_2_START}}` | `{{TS_2_FINISH}}` | `To-Do`
`D-{{SPRINT_ID}}-01` | `{{TD_1_START}}` | `{{TD_1_FINISH}}` | `Logged`

---

## 7. Politica de Commits e Testes (DOC2.5)

### Politica de Commits

- Nenhum `git commit` ou `git push` sem autorizacao explicita do PO
- `Dev_Tracking_{{SPRINT_ID}}.md` e gate obrigatorio de rastreabilidade
- Fechamento de sprint so ocorre sob comando explicito do PO

### Requisitos de Teste

- Mudancas estruturais devem deixar evidencia minima em `tests/bugs_log.md`
- Validacoes manuais devem ser registradas quando nao houver automacao real
- O resumo desta sprint deve permanecer coerente com `README.md`, `Dev_Tracking.md` e `tests/bugs_log.md`

---

## 8. Estado final da Sprint

Preencher ao encerrar a sprint `{{SPRINT_ID}}`.

- Itens concluidos:
- Itens pendentes e realocados:
- Observacoes finais:

---

## 9. Referencia de Fechamento da Sprint

- `{{SPRINT_ID}}-END: {{SPRINT_CLOSE_SUMMARY}}`

Referencias:

- Detalhes da sprint: `Dev_Tracking_{{SPRINT_ID}}.md`
- Log de testes e bugs: `tests/bugs_log.md`
