# Dev_Tracking – Sprint S1 (Sentivis IAOps)

## 1. Identificação da Sprint

- Sprint: S1
- Projeto: Sentivis IAOps
- Período: 2026-03-13 – 2026-03-20 (encerrada)
- Contexto inicial:
  - Sprint aberta após o encerramento da S0, que consolidou a base DOC2.5, o KB local e a prova técnica de integração Jira Cloud.
  - O projeto segue com ThingsBoard CE como backbone validado e com o Jira tratado como camada externa opcional.
  - O foco desta sprint é estruturar a integração Jira corretamente, sem depender de Sprint nativa, Epic ou campos inexistentes no projeto atual.
  - A sprint nasce herdando objetivos pendentes da S0, estórias `Pending-S1`, change requests de integração Jira e bugs abertos ainda não qualificados.

---

## 2. Objetivos da Sprint

- [OBJ-S1-01] Herdar e concluir os objetivos pendentes da S0 relacionados ao backbone funcional da Fase 1
- [OBJ-S1-02] Herdar e tratar as estórias `Pending-S1` originadas na S0 sem perda de rastreabilidade
- [OBJ-S1-03] Mapear o modelo real do projeto Jira STVIA para operação DOC2.5
- [OBJ-S1-04] Definir o mapeamento canônico entre backlog local, change requests, bugs e entidades Jira
- [OBJ-S1-05] Implementar bootstrap local seguro da camada `mgmt_layer_jira`
- [OBJ-S1-06] Implementar leitura e reconciliação Jira em modo `status` e `dry-run`
- [OBJ-S1-07] Implementar sincronização controlada do backlog da sprint para o Jira
- [OBJ-S1-08] Atualizar documentação operacional e rastreabilidade da camada Jira
- [OBJ-S1-09] Abrir a sprint já com bugs e change requests herdados no modelo canônico

---

## 3. Backlog da Sprint (STATUS | ESTÓRIA)

| Status | SP | Jira | Estória |
|---|---:|---|---|
| Pending-S1 | 8 | STVIA-45 | ST-S0-03 – Definir contrato de mock telemetry |
| Pending-S1 | 13 | STVIA-46 | ST-S0-04 – Mapear device/profile modeling |
| Pending-S1 | 5 | STVIA-47 | ST-S0-05 – Documentar configuração post-setup |
| Pending-S1 | 13 | STVIA-48 | ST-S0-06 – Definir baseline de dashboard |
| Pending-S1 | 8 | STVIA-49 | ST-S0-07 – Avaliar uso do Rule Engine |
| Pending-S1 | 3 | STVIA-50 | ST-S0-08 – Validar VS Code como workstation |
| Pending-S1 | 5 | STVIA-51 | ST-S0-09 – Documentar trilha de evidência |
| Pending-S1 | 13 | STVIA-52 | ST-S0-10 – Preparar baseline para hardware real |
| Done | 3 | STVIA-35 | ST-S1-01 – Levantar campos, issue types e transições reais do projeto Jira STVIA |
| Done | 5 | STVIA-36 | ST-S1-02 – Definir mapeamento DOC2.5 para labels, status e identificadores Jira |
| Done | 8 | STVIA-37 | ST-S1-03 – Criar bootstrap local da camada `mgmt_layer_jira` com estado observado em `.scr/` |
| Done | 3 | STVIA-38 | ST-S1-04 – Implementar comando de leitura `status/discover` para o Jira |
| Done | 5 | STVIA-39 | ST-S1-05 – Implementar sincronização `dry-run` da sprint ativa para o Jira |
| Done | 5 | STVIA-40 | ST-S1-06 – Refatorar código para arquitetura integrators/ com wrappers de compatibilidade |
| Done | 3 | STVIA-41 | ST-S1-07 – Atualizar documentação canônica e KB com o fluxo definitivo de operação Jira |
| To-Do | 21 | STVIA-42 | ST-S1-08 – Validar ciclo completo de criação, transição e limpeza controlada no Jira |
| To-Do | 21 | STVIA-43 | CR-S1-01 – Modelar a integração Jira sem Sprint nativa, Epic ou campos inexistentes |
| To-Do | 13 | STVIA-44 | CR-S1-02 – Definir política de sincronização, limpeza e reexecução segura no Jira |

---

## 4. Interações e Decisões Relevantes da Sprint

[D-S1-01] – 2026-03-13 – Decisão: Iniciar a S1 com foco exclusivo na camada Jira Cloud subordinada ao DOC2.5
  - Precedência: `Dev_Tracking_S1.md` permanece como source of truth local
  - Regra: o Jira só deve refletir a sprint após mapeamento correto de campos, labels e workflow do projeto
  - Origem: prova técnica de integração concluída e ambiente remoto limpo ao fim da S0

[D-S1-02] – 2026-03-13 – Decisão: A S1 herda objetivos pendentes, estórias `Pending-S1`, change requests e bugs abertos da S0
  - Regra: os IDs herdados da S0 permanecem preservados para rastreabilidade histórica
  - Complemento: change requests passam a ser tratados no backlog desta sprint com identificadores `CR-S1-XX`
  - Bug aberto: a S1 nasce com o `BUG-S1-01` em estado `To-Do`, herdado do placeholder aberto na S0

---

## 5. Referências a Testes e Bugs (resumo)

Os detalhes de testes e bugs relacionados a esta sprint devem ser registrados em:
- `tests/bugs_log.md`, na seção correspondente à Sprint S1

Aqui devem constar apenas resumos e referências cruzadas, por exemplo:
- BUG-S1-01 – Bug aberto herdado da S0 para triagem e qualificação – ver `tests/bugs_log.md`
- TEST-S1-01 – [descrição de teste] – ver `tests/bugs_log.md`
- CR-S1-01 – Modelagem da integração Jira no escopo DOC2.5 – ver backlog desta sprint
- CR-S1-02 – Política de sincronização e limpeza segura no Jira – ver backlog desta sprint

---

## 6. Timestamp UTC

Event | Start | Finish | Status
---|---|---|---
ST-S0-03 | 2026-03-13T00:00:00-ST | - | Pending-S1
ST-S0-04 | 2026-03-13T00:00:00-ST | - | Pending-S1
ST-S0-05 | 2026-03-13T00:00:00-ST | - | Pending-S1
ST-S0-06 | 2026-03-13T00:00:00-ST | - | Pending-S1
ST-S0-07 | 2026-03-13T00:00:00-ST | - | Pending-S1
ST-S0-08 | 2026-03-13T00:00:00-ST | - | Pending-S1
ST-S0-09 | 2026-03-13T00:00:00-ST | - | Pending-S1
ST-S0-10 | 2026-03-13T00:00:00-ST | - | Pending-S1
ST-S1-01 | 2026-03-19T21:00:00-ST | 2026-03-19T21:05:00-FN | Done
ST-S1-02 | 2026-03-19T21:05:00-ST | 2026-03-19T21:10:00-FN | Done
ST-S1-03 | 2026-03-19T21:10:00-ST | 2026-03-19T21:15:00-FN | Done
ST-S1-04 | 2026-03-19T21:15:00-ST | 2026-03-19T21:20:00-FN | Done
ST-S1-05 | 2026-03-19T21:20:00-ST | 2026-03-19T21:30:00-FN | Done
ST-S1-06 | 2026-03-19T21:53:00-ST | 2026-03-19T21:57:00-FN | Done
ST-S1-07 | 2026-03-20T00:16:00-ST | 2026-03-20T00:17:00-FN | Done
TEST-S1-10 | 2026-03-20T00:04:00-ST | 2026-03-20T00:05:00-FN | Passed
TEST-S1-11 | 2026-03-20T00:16:00-ST | 2026-03-20T00:17:00-FN | Passed
ST-S1-08 | 2026-03-19T21:30:00-ST | - | To-Do
CR-S1-01 | 2026-03-19T21:30:00-ST | - | To-Do
CR-S1-02 | 2026-03-19T21:30:00-ST | - | To-Do
D-S1-01 | 2026-03-13T00:40:18-ST | 2026-03-13T00:40:18-FN | Logged
D-S1-02 | 2026-03-13T00:41:00-ST | 2026-03-13T00:41:00-FN | Logged

---

## 7. Política de Commits, Tasks/ e Testes (DOC2.5)

### Política de Commits
- **Nenhum commit sem autorização explícita do usuário**: o agente não deve executar `git commit` ou `git push` sem autorização textual explícita do usuário.
- **Commits concentrados no final da sprint**: Preferencialmente realizados ao final da sprint (commit S1-END), agrupando o trabalho da sprint.
- **Dev_Tracking como gate obrigatório**: `Dev_Tracking_S1.md` é o arquivo obrigatório de conclusão de trabalho; nenhuma tarefa é considerada concluída se o Dev_Tracking não refletir o que foi feito.

### Uso de tasks/
- **tasks/ como apoio de planejamento**: A pasta `tasks/` pode ser usada como espaço de planejamento interno da IA (listas, planos, rascunhos).
- **Não é fonte de verdade**: O conteúdo relevante deve ser sempre refletido no `Dev_Tracking_S1.md`, `README.md` e documentação oficial.
- **Migração obrigatória**: Informações relevantes de `tasks/` devem ser migradas para os documentos oficiais antes do final da sprint.

### Requisitos de Teste
- **Mudanças estruturais**: Mudanças em templates, regras, workflows ou lógica central devem ter pelo menos:
  - Uma estória de teste no backlog da sprint.
  - Entradas correspondentes em `tests/bugs_log.md` (`TEST-S1-XX`, `BUG-S1-XX`).
- **Validação mínima**: Cada sprint que alterar algo estrutural deve incluir pelo menos uma validação/documentação dos testes em `tests/bugs_log.md`.

---

## 8. Estado final da Sprint

- Itens concluídos:
  - ST-S1-01 a ST-S1-07
  - TEST-S1-01 a TEST-S1-11 (evidências registradas)
  - BUG-S1-02 corrigido
- Itens pendentes e realocados:
  - ST-S1-08
  - CR-S1-01
  - CR-S1-02
  - ST-S0-03 a ST-S0-10
  - BUG-S1-01 (aberto)
- Observações finais:
  - Sprint encerrada com a arquitetura `integrators/` consolidada e documentação canônica revisada.
  - Pendências realocadas para a S2 com foco no transporte completo de S0 e S1 para o Jira.

---

## 9. Commit de Fechamento da Sprint (referência futura)

Título sugerido (quando a sprint S1 for encerrada):

- `S1-END: Estruturação da camada Jira Cloud no modelo DOC2.5`

Corpo sugerido:

- Principais entregas:
  - mapeamento Jira do projeto STVIA
  - bootstrap local da camada de gestão Jira
  - sincronização controlada da sprint ativa
  - documentação operacional da integração

- Referências:
  - Detalhes da sprint: `Dev_Tracking_S1.md`
  - Log de testes e bugs: `tests/bugs_log.md`