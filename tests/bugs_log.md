# bugs_log.md - Log Centralizado de Bugs e Testes

## 1. Propósito

Centralizar o registro de bugs e testes por sprint.

## 2. Regra de Uso

- Registrar bugs e testes por sprint
- Usar formato padronizado de identificação
- Manter referência cruzada com Dev_Tracking_SX.md
- Bugs: `BUG-SX-YY`
- Testes: `TEST-SX-YY`
- Hash (UTC) por item: `SAT03072026023234PMST - SAT03072026033234PMFN`

---

## 3. Sprint S0

### 4. Bugs Registrados

Nenhum bug registrado até o momento.

### 5. Testes Registrados

- `TEST-S0-01` – Validação pós-importação seletiva do KB ThingsBoard CE
  - Escopo: confirmar presença e contagem importada em `api/`, `user-guide/` e `tutorials`
  - Resultado: aprovado (`25` api, `239` user-guide, `5` tutorials; total `269`)
  - Evidências: `third_party/thingsboard-ce/SOURCES.md`, `knowledge/thingsboard/ce/manifests/import_manifest.md`, `knowledge/thingsboard/ce/manifests/mapping_table.csv`
- `TEST-S0-02` – Validação da política de recuperação low-token
  - Escopo: confirmar ordem oficial `topic_index -> runbook -> docs locais -> upstream`
  - Resultado: aprovado
  - Evidências: `knowledge/thingsboard/ce/manifests/reading_priority.md`, `knowledge/thingsboard/ce/manifests/topic_index.md`, `docs/ARCHITECTURE.md`, `docs/DEVELOPMENT.md`
- `TEST-S0-03` – Validação do cenário de atendimento “estação offline no talhão”
  - Escopo: confirmar que a resposta operacional gerada foi convertida em documentação oficial e runbook reutilizável
  - Resultado: aprovado
  - Evidências: `knowledge/thingsboard/ce/runbooks/station-offline-triage.md`, `knowledge/thingsboard/ce/manifests/topic_index.md`, `docs/OPERATIONS.md`, `Sprint/Dev_Tracking_S0.md`
- `TEST-S0-04` – Validação da consistência de nomenclatura oficial
  - Escopo: confirmar alinhamento do nome oficial `Sentivis IAOps` nos documentos canônicos e no board organizacional
  - Resultado: aprovado
  - Evidências: `README.md`, `rules/WORKSPACE_RULES.md`, `docs/SETUP.md`, `docs/ARCHITECTURE.md`, `docs/DEVELOPMENT.md`, `docs/OPERATIONS.md`, `Dev_Tracking.md`, `Sprint/Dev_Tracking_S0.md`
- `TEST-S0-05` – Validação técnica da integração Jira Cloud
  - Escopo: confirmar autenticação, leitura do projeto, criação de issues, transição de status e limpeza remota das issues de teste
  - Resultado: aprovado
  - Evidências: `KB/jira-doc25-workflow-estudo.md`, `Sprint/Dev_Tracking_S0.md`

---

## 4. Sprint S1

### 4. Bugs Registrados

- `BUG-S1-01` – Bug aberto herdado da S0 para triagem e qualificação funcional
  - Origem: herança do placeholder `BUG-S0-01` que permaneceu aberto ao encerramento da S0
  - Estado: aberto
  - Ação esperada: qualificar escopo, impacto e evidências na S1 antes de decidir correção ou encerramento
  - Referências: `Dev_Tracking_S1.md`, `Sprint/Dev_Tracking_S0.md`

### 5. Testes Registrados

Nenhum teste registrado até o momento.

---

## 6. Timestamp UTC

Event | Start | Finish | Status
---|---|---|---
BUG-S0-01 | DDDMMDDYYYYHHMMSSamPMST | DDDMMDDYYYYHHMMSSamPMFN | To-Do
TEST-S0-01 | THU03122026110000PMST | THU03122026111253PMFN | Passed
TEST-S0-02 | FRI03132026120429AMST | FRI03132026120429AMFN | Passed
TEST-S0-03 | FRI03132026121156AMST | FRI03132026121156AMFN | Passed
TEST-S0-04 | FRI03132026011307AMST | FRI03132026011307AMFN | Passed
TEST-S0-05 | FRI03132026032150AMST | FRI03132026040518AMFN | Passed
BUG-S1-01 | FRI03132026041040AMST | DDDMMDDYYYYHHMMSSamPMFN | To-Do
TEST-S1-01 | DDDMMDDYYYYHHMMSSamPMST | DDDMMDDYYYYHHMMSSamPMFN | To-Do

## 7. Ressalvas Técnicas

1. Sprint S0 foi encerrada com a base documental, KB local e prova técnica de integração Jira concluídos.
2. Sprint S1 inicia a estruturação formal da camada Jira Cloud subordinada ao DOC2.5 e já nasce com herança de backlog, change requests e bug aberto.
3. Credenciais operacionais permanecem em `.scr/.env` e não devem ser versionadas.

## 8. Sprints Futuras

Sprints subsequentes (S1, S2, etc.) serão adicionadas conforme o progresso do projeto.
