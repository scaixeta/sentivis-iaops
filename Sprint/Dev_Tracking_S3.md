# Dev_Tracking – Sprint S3 (Sentivis IAOps)

## 1. Identificação da Sprint

- Sprint: S3
- Projeto: Sentivis IAOps
- Período: 2026-03-22 – 2026-03-25
- Contexto inicial:
  - Sprint aberta localmente após o encerramento da S2, que consolidou a camada Jira no modelo DOC2.5.
  - O foco desta sprint deixa de ser a integração Jira e volta para a base funcional do projeto Mock ThingsBoard.
  - O backlog desta sprint é composto pelas estórias herdadas da base S0 que haviam sido carregadas indevidamente na S2.
  - No Jira, a `Sprint S3` já está ativa com as estórias base atribuídas.

---

## 2. Objetivos da Sprint

### Objetivo de Negócio da Sprint

- Objetivo executivo / valor para cliente: `Retomar a base funcional do projeto com o backlog Mock ThingsBoard, consolidando contrato, modelagem, dashboard e trilha operacional para a próxima etapa de produto.`
- Sprint goal no Jira: `Retomar a base funcional do projeto com o backlog Mock ThingsBoard, consolidando contrato, modelagem, dashboard e trilha operacional para a próxima etapa de produto.`

- [OBJ-S3-01] Retomar o backlog funcional do Mock ThingsBoard sem misturar esse escopo com a camada Jira
- [OBJ-S3-02] Consolidar contrato de telemetria, modelagem de devices/profiles e baseline operacional da plataforma
- [OBJ-S3-03] Preparar o backlog para a próxima etapa funcional, incluindo trilha de evidência e baseline para hardware real

---

## 3. Backlog da Sprint (STATUS | ESTÓRIA)

| Status | SP | Jira | Estória |
|---|---:|---|---|
| Pending-S3 | 8 | STVIA-45 | ST-S0-03 – Definir contrato de mock telemetry |
| Pending-S3 | 13 | STVIA-46 | ST-S0-04 – Mapear device/profile modeling |
| Pending-S3 | 5 | STVIA-47 | ST-S0-05 – Documentar configuração post-setup |
| Pending-S3 | 13 | STVIA-48 | ST-S0-06 – Definir baseline de dashboard |
| Pending-S3 | 8 | STVIA-49 | ST-S0-07 – Avaliar uso do Rule Engine |
| Pending-S3 | 3 | STVIA-50 | ST-S0-08 – Validar VS Code como workstation |
| Pending-S3 | 5 | STVIA-51 | ST-S0-09 – Documentar trilha de evidência |
| Pending-S3 | 13 | STVIA-52 | ST-S0-10 – Preparar baseline para hardware real |

---

## 4. Interações e Decisões Relevantes da Sprint

[D-S3-01] – 2026-03-21 - Decisão: Abrir a S3 local para retomar apenas o backlog base do Mock ThingsBoard
  - Origem: encerramento local da S2 com escopo Jira consolidado
  - Regra: a S3 passa a concentrar somente o backlog funcional/base do projeto
  - Evidência: `Sprint S3` criada no Jira como sprint futura e `STVIA-45` a `STVIA-52` atribuídas a ela

---

## 5. Referências a Testes e Bugs (resumo)

Os detalhes de testes e bugs relacionados a esta sprint devem ser registrados em:
- `tests/bugs_log.md`, na seção correspondente à Sprint S3

Aqui devem constar apenas resumos e referências cruzadas.

- `BUG-S3-01` / `STVIA-60` – Correção do board Jira para `Pendentes` x `Em Progresso` – ver `tests/bugs_log.md`
- `TEST-S3-01` – Validação do sync da S3 após correção do board – ver `tests/bugs_log.md`
- `TEST-S3-02` – Validação do espelhamento do bug `BUG-S3-01` em `Em Testes` no Jira – ver `tests/bugs_log.md`

---

## 6. Timestamp UTC

Event | Start | Finish | Status
---|---|---|---
ST-S0-03 | 2026-03-13T00:00:00-ST | - | Pending-S3
ST-S0-04 | 2026-03-13T00:00:00-ST | - | Pending-S3
ST-S0-05 | 2026-03-13T00:00:00-ST | - | Pending-S3
ST-S0-06 | 2026-03-13T00:00:00-ST | - | Pending-S3
ST-S0-07 | 2026-03-13T00:00:00-ST | - | Pending-S3
ST-S0-08 | 2026-03-13T00:00:00-ST | - | Pending-S3
ST-S0-09 | 2026-03-13T00:00:00-ST | - | Pending-S3
ST-S0-10 | 2026-03-13T00:00:00-ST | - | Pending-S3
D-S3-01 | 2026-03-21T16:59:36-ST | 2026-03-21T16:59:36-FN | Logged
BUG-S3-01 | 2026-03-21T17:00:00-ST | - | In Test
TEST-S3-01 | 2026-03-21T17:01:00-ST | 2026-03-21T17:01:00-FN | Passed
TEST-S3-02 | 2026-03-21T17:35:00-ST | 2026-03-21T17:35:00-FN | Passed

---

## 7. Política de Commits, Tasks/ e Testes (DOC2.5)

### Política de Commits
- **Nenhum commit sem autorização explícita do usuário**: o agente não deve executar `git commit` ou `git push` sem autorização textual explícita do usuário.
- **Commits concentrados no final da sprint**: Preferencialmente realizados ao final da sprint (commit S3-END), agrupando o trabalho da sprint.
- **Dev_Tracking como gate obrigatório**: `Dev_Tracking_S3.md` é o arquivo obrigatório de conclusão de trabalho; nenhuma tarefa é considerada concluída se o Dev_Tracking não refletir o que foi feito.

### Uso de tasks/
- **tasks/ como apoio de planejamento**: A pasta `tasks/` pode ser usada como espaço de planejamento interno da IA (listas, planos, rascunhos).
- **Não é fonte de verdade**: O conteúdo relevante deve ser sempre refletido no `Dev_Tracking_S3.md`, `README.md` e documentação oficial.
- **Migração obrigatória**: Informações relevantes de `tasks/` devem ser migradas para os documentos oficiais antes do final da sprint.

### Requisitos de Teste
- **Mudanças estruturais**: Mudanças em templates, regras, workflows ou lógica central devem ter pelo menos:
  - Uma estória de teste no backlog da sprint.
  - Entradas correspondentes em `tests/bugs_log.md` (`TEST-S3-XX`, `BUG-S3-XX`).
- **Validação mínima**: Cada sprint que alterar algo estrutural deve incluir pelo menos uma validação/documentação dos testes em `tests/bugs_log.md`.

---

## 8. Estado final da Sprint

(Preencher ao encerrar a sprint S3.)

- Itens concluídos:
- Itens pendentes e realocados:
- Observações finais:

---

## 9. Commit de Fechamento da Sprint (referência futura)

Título sugerido (quando a sprint S3 for encerrada):

- `S3-END: Retomada da base funcional do Mock ThingsBoard`

Corpo sugerido:

- Principais entregas:
  - retomada das estórias base do projeto
  - consolidação do backlog funcional Mock ThingsBoard
  - preparação da próxima etapa de produto

- Referências:
  - Detalhes da sprint: `Dev_Tracking_S3.md`
  - Log de testes e bugs: `tests/bugs_log.md`
