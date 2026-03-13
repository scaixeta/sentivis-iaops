# bugs_log.md - Log Centralizado de Bugs e Testes

## 1. Propósito

Centralizar o registro de bugs e testes por sprint.

## 2. Regra de Uso

- Registrar bugs e testes por sprint
- Usar formato padronizado de identificação
- Manter referência cruzada com Dev_Tracking_S0.md
- Bugs: `BUG-S0-YY`
- Testes: `TEST-S0-YY`
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
  - Evidências: `knowledge/thingsboard/ce/runbooks/station-offline-triage.md`, `knowledge/thingsboard/ce/manifests/topic_index.md`, `docs/OPERATIONS.md`, `Dev_Tracking_S0.md`

---

## 6. Timestamp UTC

Event | Start | Finish | Status
---|---|---|---
BUG-S0-01 | DDDMMDDYYYYHHMMSSamPMST | DDDMMDDYYYYHHMMSSamPMFN | To-Do
TEST-S0-01 | THU03122026110000PMST | THU03122026111253PMFN | Passed
TEST-S0-02 | FRI03132026120429AMST | FRI03132026120429AMFN | Passed
TEST-S0-03 | FRI03132026121156AMST | FRI03132026121156AMFN | Passed

## 7. Ressalvas Técnicas

1. Sprint S0 é a sprint inicial - Fase de configuração e validação do data backbone
2. Bugs e testes serão registrados conforme o progresso da sprint
3. Credenciais ThingsBoard armazenadas em `.scr/.env` - não versionar

## 8. Sprints Futuras

Sprints subsequentes (S1, S2, etc.) serão adicionadas conforme o progresso do projeto.
