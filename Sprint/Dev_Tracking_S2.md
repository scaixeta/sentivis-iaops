# Dev_Tracking – Sprint S2 (Sentivis IAOps)

## 1. Identificação da Sprint

- Sprint: S2
- Projeto: Sentivis IAOps
- Período: 2026-03-20 – 2026-03-21 18:00
- Contexto inicial:
  - Sprint aberta após o encerramento da S1, que consolidou a arquitetura `integrators/` e a documentação canônica da integração Jira.
  - O foco desta sprint é transportar os detalhes das Sprints S0 e S1 para o Jira, mantendo rastreabilidade completa.
  - Pendências herdadas: itens `Pending-S2`, change requests e bug aberto da S1.
  - Data-alvo de entrega da sprint e das estórias desta sprint: 2026-03-21 18:00 (`America/Sao_Paulo`).

---

## 2. Objetivos da Sprint

### Objetivo de Negócio da Sprint

- Objetivo executivo / valor para cliente: `Estabelecer a visibilidade executiva do projeto com rastreabilidade confiável entre planejamento local e operação no Jira.`
- Sprint goal no Jira: `Estabelecer a visibilidade executiva do projeto com rastreabilidade confiável entre planejamento local e operação no Jira.`

- [OBJ-S2-01] Transportar backlog e detalhes da Sprint S0 para o Jira com rastreabilidade completa
- [OBJ-S2-02] Transportar backlog e detalhes da Sprint S1 para o Jira com rastreabilidade completa
- [OBJ-S2-03] Executar sincronização real com reconciliação controlada e evidências registradas
- [OBJ-S2-04] Validar ciclo completo de criação, transição e limpeza controlada no Jira
- [OBJ-S2-05] Tratar bug herdado e change requests pendentes
- [OBJ-S2-06] Corrigir a listagem Jira para retornar campos completos e suportar reconciliação por tracking arquivado

---

## 3. Backlog da Sprint (STATUS | ESTÓRIA)

| Status | SP | Jira | Estória |
|---|---:|---|---|
| Backlog | 8 | STVIA-45 | ST-S0-03 – Definir contrato de mock telemetry |
| Backlog | 13 | STVIA-46 | ST-S0-04 – Mapear device/profile modeling |
| Backlog | 5 | STVIA-47 | ST-S0-05 – Documentar configuração post-setup |
| Backlog | 13 | STVIA-48 | ST-S0-06 – Definir baseline de dashboard |
| Backlog | 8 | STVIA-49 | ST-S0-07 – Avaliar uso do Rule Engine |
| Backlog | 3 | STVIA-50 | ST-S0-08 – Validar VS Code como workstation |
| Backlog | 5 | STVIA-51 | ST-S0-09 – Documentar trilha de evidência |
| Backlog | 13 | STVIA-52 | ST-S0-10 – Preparar baseline para hardware real |
| Done | 2 | STVIA-54 | ST-S2-01 – Transportar Sprint S0 para o Jira com todos os detalhes e rastreabilidade |
| Done | 1 | STVIA-55 | ST-S2-02 – Transportar Sprint S1 para o Jira com todos os detalhes e rastreabilidade |
| Done | 1 | STVIA-56 | ST-S2-03 – Executar sincronização real com reconciliação controlada (S0/S1) |
| Done | 21 | STVIA-42 | ST-S1-08 – Validar ciclo completo de criação, transição e limpeza controlada no Jira |
| Done | 21 | STVIA-43 | CR-S1-01 – Modelar a integração Jira sem Sprint nativa, Epic ou campos inexistentes |
| Done | 13 | STVIA-44 | CR-S1-02 – Definir política de sincronização, limpeza e reexecução segura no Jira |
| Done | 2 | STVIA-57 | ST-S2-04 – Corrigir a listagem Jira para retornar campos completos e suportar reconciliação por tracking arquivado |

---

## 4. Interações e Decisões Relevantes da Sprint

[D-S2-01] – 2026-03-20 - Decisão: Priorizar transporte completo das Sprints S0 e S1 para o Jira com rastreabilidade total
  - Precedência: `Dev_Tracking_S2.md` permanece como source of truth local
  - Regra: o Jira deve espelhar as sprints anteriores com labels e evidências completas

[D-S2-02] – 2026-03-20 - Decisão: CLI sync default alterado para S2 (correção de risco operacional)
  - Alteração: `python -m integrators.jira sync` agora usa `Dev_Tracking_S2.md` por padrão
  - Motivo: evitar risco de sync acidental em S1
  - Evidência: TEST-S2-09 aprovado

[D-S2-03] – 2026-03-20 - Decisão: Documentar estratégia de labels vs Sprint nativo
  - Estratégia atual: LABELS FALLBACK (sprint_s0, sprint_s1, sprint_s2 via labels)
  - Motivo: projeto STVIA é Jira Software mas nativo Sprint field requer board específico
  - Regra: manter labels como fallback e documentar claramente
  - Evidência: TEST-S2-11 aprovado, `integrators/jira/mapper.py` contém nota explicativa

[D-S2-05] – 2026-03-20 - Decisão: Corrigir reconcile para escopo da sprint do tracking
  - Correção: `reconcile` passa a comparar itens locais com issues Jira filtradas por `sprint_sX`
  - Motivo: evitar falsos orphans quando o projeto contém issues de múltiplas sprints
  - Evidência: TEST-S2-12 aprovado, `integrators/jira/cli.py` atualizado

[D-S2-06] – 2026-03-20 - Decisão: Implementar suporte a Sprint Nativo via Agile API
  - Implementação: Adicionados métodos `get_boards`, `get_sprints`, `add_issues_to_sprint` em `client.py`
  - CLI: Novos comandos `sprint status` e `sprint assign` adicionados
  - Execução: 18 issues atribuídas a Sprint S0, 10 issues atribuídas a Sprint S1
  - Evidência: `integrators/jira/client.py` e `integrators/jira/cli.py` atualizados

[D-S2-07] – 2026-03-20 - Decisão: Implementar comando sprint dates para definição de datas
  - Implementação: Adicionados métodos `get_sprint` e `update_sprint` em `client.py`
  - CLI: Novo comando `sprint dates` adicionado com suporte a --start-date e --end-date
  - Formato: YYYY-MM-DD convertido para ISO8601 UTC (start: T00:00:00.000Z, end: T23:59:59.999Z)
  - Execução: Sprint S0 (2026-03-10 a 2026-03-13), Sprint S1 (2026-03-13 a 2026-03-20)
  - Evidência: `integrators/jira/client.py` e `integrators/jira/cli.py` atualizados, docs/OPERATIONS.md atualizado

[D-S2-08] – 2026-03-20 - Decisão: Implementar sincronização de datas de issues com timestamps do tracking
  - Implementação: Adicionado parser de timestamps em `doc25_parser.py` e comando `issue dates` em `cli.py`
  - Mapeamento: Start Date = timestamp start (data), Data Limite = timestamp finish (data)
  - CLI: Novo comando `issue dates` adicionado com suporte a --tracking-file, --dry-run e --yes
  - Execução: 18 issues da S0 atualizadas com datas (STVIA-25 a STVIA-34, STVIA-27 a STVIA-31)
  - Evidência: `integrators/common/doc25_parser.py` e `integrators/jira/cli.py` atualizados, docs/ARCHITECTURE.md e docs/OPERATIONS.md atualizados, TEST-S2-14 aprovado

[D-S2-09] – 2026-03-21 - Decisão: Manter o source of truth local acima do estado remoto do Jira
  - Regra: `Dev_Tracking_S2.md` continua sendo a sprint ativa local e a referência canônica para o projeto
  - Estado remoto observado: Jira com `Sprint S0` e `Sprint S1` encerradas e sem sprint ativa no board
  - Interpretação correta: o Jira registra a execução remota, mas não substitui o planejamento e a governança do SoT local
  - Ação: `README.md` e `Dev_Tracking.md` passam a refletir explicitamente essa relação

[D-S2-10] – 2026-03-21 - Decisão: Remover da Sprint S2 as estórias base do ThingsBoard e devolvê-las ao backlog
  - Escopo removido da sprint atual: `STVIA-45` a `STVIA-52`
  - Motivo: essas estórias pertencem ao backlog base do projeto (Mock ThingsBoard) e não ao fechamento da camada Jira
  - Ação: issues removidas da `Sprint S2` no Jira e reclassificadas como `Backlog` no tracking local

---

## 5. Referências a Testes e Bugs (resumo)

Os detalhes de testes e bugs relacionados a esta sprint devem ser registrados em:
- `tests/bugs_log.md`, na seção correspondente à Sprint S2

Aqui devem constar apenas resumos e referências cruzadas, por exemplo:
- BUG-S2-01 – Bug herdado daDOC2.5 – ver backlog desta sprint
- CR-S1-02 – Política de sincronização e limpeza segura no Jira – ver backlog desta sprint
- TEST-S2-15 – Instrumentação do backlog (SP + Jira) no tracking – ver `tests/bugs_log.md`
- TEST-S2-16 – Campo Story Points no Jira (customfield_10016) validado – ver `tests/bugs_log.md`
- TEST-S2-17 – Reconcile validado após migração da tabela do backlog – ver `tests/bugs_log.md`
- TEST-S2-18 – Transição de status das estórias S0 para "Em progresso" via integrator – ver `tests/bugs_log.md`
- TEST-S2-19 – Leitura das colunas do board Jira (workflow) – ver `tests/bugs_log.md`
- TEST-S2-20 – Orientação de estado local derivada das colunas do board Jira – ver `tests/bugs_log.md`
- TEST-S2-21 – Transição pontual de issue Jira com comentário opcional validada em dry-run – ver `tests/bugs_log.md`

---

## 6. Timestamp UTC

Event | Start | Finish | Status
---|---|---|---
ST-S0-03 | 2026-03-13T00:00:00-ST | - | Backlog
ST-S0-04 | 2026-03-13T00:00:00-ST | - | Backlog
ST-S0-05 | 2026-03-13T00:00:00-ST | - | Backlog
ST-S0-06 | 2026-03-13T00:00:00-ST | - | Backlog
ST-S0-07 | 2026-03-13T00:00:00-ST | - | Backlog
ST-S0-08 | 2026-03-13T00:00:00-ST | - | Backlog
ST-S0-09 | 2026-03-13T00:00:00-ST | - | Backlog
ST-S0-10 | 2026-03-13T00:00:00-ST | - | Backlog
D-S2-10 | 2026-03-21T16:53:10-ST | 2026-03-21T16:53:10-FN | Logged
ST-S2-01 | 2026-03-20T01:31:05-ST | 2026-03-20T01:39:48-FN | Done
ST-S2-02 | 2026-03-20T01:39:48-ST | 2026-03-20T01:40:18-FN | Done
ST-S2-03 | 2026-03-20T01:40:18-ST | 2026-03-20T01:40:18-FN | Done
ST-S2-04 | 2026-03-20T01:40:18-ST | 2026-03-20T01:44:00-FN | Done
ST-S1-08 | 2026-03-19T21:30:00-ST | 2026-03-20T03:45:00-FN | Done
CR-S1-01 | 2026-03-19T21:30:00-ST | 2026-03-20T03:46:00-FN | Done
CR-S1-02 | 2026-03-19T21:30:00-ST | 2026-03-21T16:51:09-FN | Done
D-S2-01 | 2026-03-20T01:31:05-ST | 2026-03-20T01:31:05-FN | Logged
D-S2-02 | 2026-03-20T01:44:00-ST | 2026-03-20T01:44:00-FN | Logged
D-S2-03 | 2026-03-20T02:10:00-ST | 2026-03-20T02:10:00-FN | Logged
D-S2-04 | 2026-03-20T02:11:00-ST | 2026-03-20T02:11:00-FN | Logged
D-S2-05 | 2026-03-20T03:25:00-ST | 2026-03-20T03:25:00-FN | Logged
D-S2-06 | 2026-03-20T03:47:00-ST | 2026-03-20T03:50:00-FN | Logged
D-S2-07 | 2026-03-20T04:10:00-ST | 2026-03-20T04:15:00-FN | Logged
D-S2-08 | 2026-03-20T04:33:00-ST | 2026-03-20T04:38:00-FN | Logged
D-S2-09 | 2026-03-21T17:45:00-ST | 2026-03-21T17:48:00-FN | Logged

---

## 7. Política de Commits, Tasks/ e Testes (DOC2.5)

### Política de Commits
- **Nenhum commit sem autorização explícita do usuário**: o agente não deve executar `git commit` ou `git push` sem autorização textual explícita do usuário.
- **Commits concentrados no final da sprint**: Preferencialmente realizados ao final da sprint (commit S2-END), agrupando o trabalho da sprint.
- **Dev_Tracking como gate obrigatório**: `Dev_Tracking_S2.md` é o arquivo obrigatório de conclusão de trabalho; nenhuma tarefa é considerada concluída se o Dev_Tracking não refletir o que foi feito.

### Uso de tasks/
- **tasks/ como apoio de planejamento**: A pasta `tasks/` pode ser usada como espaço de planejamento interno da IA (listas, planos, rascunhos).
- **Não é fonte de verdade**: O conteúdo relevante deve ser sempre refletido no `Dev_Tracking_S2.md`, `README.md` e documentação oficial.
- **Migração obrigatória**: Informações relevantes de `tasks/` devem ser migradas para os documentos oficiais antes do final da sprint.

### Requisitos de Teste
- **Mudanças estruturais**: Mudanças em templates, regras, workflows ou lógica central devem ter pelo menos:
  - Uma estória de teste no backlog da sprint.
  - Entradas correspondentes em `tests/bugs_log.md` (`TEST-S2-XX`, `BUG-S2-XX`).
- **Validação mínima**: Cada sprint que alterar algo estrutural deve incluir pelo menos uma validação/documentação dos testes em `tests/bugs_log.md`.

---

## 8. Estado final da Sprint

- Itens concluídos:
  - `STVIA-54` (`ST-S2-01`)
  - `STVIA-55` (`ST-S2-02`)
  - `STVIA-56` (`ST-S2-03`)
  - `STVIA-57` (`ST-S2-04`)
  - `STVIA-42` (`ST-S1-08`)
  - `STVIA-43` (`CR-S1-01`)
  - `STVIA-44` (`CR-S1-02`)
  - `BUG-S2-01` e `BUG-S2-02` corrigidos
- Itens pendentes e realocados:
  - `STVIA-45` a `STVIA-52` movidas para a `Sprint S3` no Jira e materializadas na `S3` local
- Observações finais:
  - A `S2` foi encerrada localmente com o objetivo de consolidar a camada Jira subordinada ao DOC2.5.
  - O backlog base do Mock ThingsBoard foi retirado do escopo da `S2` e transferido para a `S3`.

---

## 9. Commit de Fechamento da Sprint (referência futura)

Título sugerido (quando a sprint S2 for encerrada):

- `S2-END: Transporte completo das sprints S0 e S1 para o Jira`

Corpo sugerido:

- Principais entregas:
  - transporte completo de S0 para Jira
  - transporte completo de S1 para Jira
  - validação do ciclo completo no Jira

- Referências:
  - Detalhes da sprint: `Dev_Tracking_S2.md`
  - Log de testes e bugs: `tests/bugs_log.md`
