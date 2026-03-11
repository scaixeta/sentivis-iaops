# Dev_Tracking – Sprint {{SPRINT_ID}} ({{PROJECT_NAME}})

## 1. Identificação da Sprint

- Sprint: {{SPRINT_ID}} (ex.: S0, S1, S2)
- Projeto: {{PROJECT_NAME}}
- Período: {{PERIODO}} (ex.: 2025-11-18 – 2025-11-19)
- Contexto inicial:
  - [Breve contexto do projeto e da sprint]
  - [Principais objetivos ou mudanças esperadas]
  - [Referências a sprints anteriores, se aplicável]

---

## 2. Objetivos da Sprint

- [OBJ-{{SPRINT_ID}}-01] [Descrição do objetivo 1]
- [OBJ-{{SPRINT_ID}}-02] [Descrição do objetivo 2]
- [OBJ-{{SPRINT_ID}}-03] [Descrição do objetivo 3]

---

## 3. Backlog da Sprint (STATUS | ESTÓRIA)

| Status | Estória |
|---|---|
| To-Do | ST-{{SPRINT_ID}}-01 – [Descrição da primeira entrega] |
| To-Do | ST-{{SPRINT_ID}}-02 – [Descrição da segunda entrega] |
| To-Do | ST-{{SPRINT_ID}}-03 – [Descrição da terceira entrega] |

Estados possíveis:
- To-Do, Doing, Done, Accepted, Pending-SX (caso algum item seja movido para próxima sprint).

---

## 4. Interações e Decisões Relevantes da Sprint

[D-{{SPRINT_ID}}-01] – [Descrever decisão relevante]

(Adicionar novas decisões aqui ao longo da sprint.)

---

## 5. Referências a Testes e Bugs (resumo)

Os detalhes de testes e bugs relacionados a esta sprint devem ser registrados em:
- `tests/bugs_log.md`, na seção correspondente à Sprint {{SPRINT_ID}} (a ser criada/ajustada quando houver testes/bugs).

Aqui devem constar apenas resumos e referências cruzadas, por exemplo:
- BUG-{{SPRINT_ID}}-01 – [título curto] – ver tests/bugs_log.md (Sprint {{SPRINT_ID}}).
- TEST-{{SPRINT_ID}}-01 – [descrição de teste] – ver tests/bugs_log.md (Sprint {{SPRINT_ID}}).
No `tests/bugs_log.md`, a seção `Timestamp UTC` deve conter a tabela unificada de eventos (BUG/TEST).

---

## 6. Timestamp UTC

Event | Start | Finish | Status
---|---|---|---
ST-{{SPRINT_ID}}-01 | DDDMMDDYYYYHHMMSSamPMST | DDDMMDDYYYYHHMMSSamPMFN | To-Do
ST-{{SPRINT_ID}}-02 | DDDMMDDYYYYHHMMSSamPMST | DDDMMDDYYYYHHMMSSamPMFN | To-Do
ST-{{SPRINT_ID}}-03 | DDDMMDDYYYYHHMMSSamPMST | DDDMMDDYYYYHHMMSSamPMFN | To-Do
D-{{SPRINT_ID}}-01 | DDDMMDDYYYYHHMMSSamPMST | DDDMMDDYYYYHHMMSSamPMFN | Logged

---

## 7. Política de Commits, Tasks/ e Testes (DOC2.5)

### Política de Commits
- **Nenhum commit sem autorização explícita do usuário**: o agente não deve executar `git commit` ou `git push` sem autorização textual explícita do usuário.
- **Commits concentrados no final da sprint**: Preferencialmente realizados ao final da sprint (commit {{SPRINT_ID}}-END), agrupando o trabalho da sprint.
- **Dev_Tracking como gate obrigatório**: Dev_Tracking_SX.md é o arquivo obrigatório de conclusão de trabalho; nenhuma tarefa é considerada concluída se o Dev_Tracking não refletir o que foi feito.

### Uso de tasks/
- **tasks/ como apoio de planejamento**: A pasta `tasks/` pode ser usada como espaço de planejamento interno da IA (listas, planos, rascunhos).
- **Não é fonte de verdade**: O conteúdo relevante deve ser sempre refletido no Dev_Tracking_SX.md, README e documentação oficial.
- **Migração obrigatória**: Informações relevantes de `tasks/` devem ser migradas para os documentos oficiais antes do final da sprint.

### Requisitos de Teste
- **Mudanças estruturais**: Mudanças em templates, regras, workflows ou lógica central devem ter pelo menos:
  - Uma estória de teste no backlog da sprint.
  - Entradas correspondentes em `tests/bugs_log.md` (TEST-{{SPRINT_ID}}-XX, BUG-{{SPRINT_ID}}-XX).
- **Validação mínima**: Cada sprint que alterar algo estrutural deve incluir pelo menos uma validação/documentação dos testes em `tests/bugs_log.md`.

---

## 8. Estado final da Sprint

(Preencher ao encerrar a sprint {{SPRINT_ID}}.)

- Itens concluídos:
- Itens pendentes e realocados:
- Observações finais:

---

## 9. Commit de Fechamento da Sprint (referência futura)

Título sugerido (quando a sprint {{SPRINT_ID}} for encerrada):

- `{{SPRINT_ID}}-END: [resumo das entregas principais]`

Corpo sugerido:

- Principais entregas:
  - [Principais entregas da sprint {{SPRINT_ID}}]
  - [Referências a decisões e arquivos afetados]

- Referências:
  - Detalhes da sprint: `Dev_Tracking_{{SPRINT_ID}}.md`
  - Log de testes e bugs: `tests/bugs_log.md`
