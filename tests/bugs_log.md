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
- `TEST-S0-03` – Validação do cenário de atendimento "estação offline no talhão"
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

- `BUG-S1-02` – EOFError em mgmt_layer_jira_init.py --dry-run com estado existente
  - Origem: script pedia input() interativo mesmo em modo dry-run quando estado ja existia
  - Estado: corrigido
  - Correção: em modo dry-run, o script agora usa o estado existente para simulação sem pedir confirmação
  - Evidência: TEST-S1-06 aprovado
  - Referências: `scripts/mgmt_layer_jira_init.py`, `Dev_Tracking_S1.md`

### 5. Testes Registrados

- `TEST-S1-01` – Validação de bootstrap mgmt_layer_jira_init.py
  - Escopo: executar init com --dry-run e confirmar carga de credenciais, discovery de usuario e projeto
  - Resultado: aprovado
  - Evidências: modo dry-run usa estado existente, não cria arquivos, usuario autenticado (Sergio Caixeta), projeto STVIA mapeado com 4 issue types e 3 statuses

- `TEST-S1-02` – Validação de comando status
  - Escopo: executar mgmt_layer_jira.py status e confirmar exibicao de estado observado
  - Resultado: aprovado
  - Evidências: saida mostra projeto, ID, tipo, issue types mapeados, statuses mapeados

- `TEST-S1-03` – Validação de comando discover
  - Escopo: executar mgmt_layer_jira.py discover e confirmar atualizacao de metadados
  - Resultado: aprovado
  - Evidências: estado atualizado em `.scr/mgmt_layer.jira.json`, fingerprint alterado

- `TEST-S1-04` – Validação de parser DOC2.5
  - Escopo: confirmar extração de itens do backlog Dev_Tracking_S1.md
  - Resultado: aprovado
  - Evidências: 10 itens extraidos corretamente (ST-S1-XX, CR-S1-XX), itens herdados da S0 movidos para Pending-S1

- `TEST-S1-05` – Validação de sync --dry-run
  - Escopo: executar sync --dry-run e confirmar plano de criacao
  - Resultado: aprovado
  - Evidências: delta calculado corretamente, 10 operacoes CREATE identificadas

- `TEST-S1-06` – Validação de correção do bug EOFError em init --dry-run
  - Escopo: executar init --dry-run com estado existente e confirmar que nao pede interacao
  - Resultado: aprovado
  - Evidências: comando executado sem EOFError, usa estado existente para simulacao
  - Referência: BUG-S1-02

- `TEST-S1-07` – Validação de compilação dos módulos Jira
  - Escopo: executar py_compile em todos os módulos do mgmt_layer_jira
  - Resultado: aprovado
  - Evidências: integrators/jira/client.py, integrators/jira/state.py, integrators/jira/mapper.py, integrators/jira/sync_engine.py, integrators/common/doc25_parser.py, scripts/mgmt_layer_jira.py, scripts/mgmt_layer_jira_init.py compilados com sucesso

- `TEST-S1-08` – Validação de refatoração para arquitetura integrators/
  - Escopo: migrar código para integrators/jira/ e integrators/common/, manter wrappers de compatibilidade
  - Resultado: aprovado
  - Evidências: 
    - `integrators/jira/__init__.py` - pacote principal
    - `integrators/jira/client.py` - cliente HTTP
    - `integrators/jira/state.py` - persistência de estado
    - `integrators/jira/mapper.py` - mapeamento DOC2.5 -> Jira
    - `integrators/jira/sync_engine.py` - engine de sincronização
    - `integrators/jira/bootstrap.py` - inicialização
    - `integrators/jira/cli.py` - router CLI
    - `integrators/common/__init__.py` - módulo comum
    - `integrators/common/doc25_parser.py` - parser DOC2.5

- `TEST-S1-09` – Validação de compatibilidade dos wrappers
  - Escopo: confirmar que comandos antigos continuam funcionando
  - Resultado: aprovado
  - Evidências:
    - `python scripts/mgmt_layer_jira.py status` ✓
    - `python scripts/mgmt_layer_jira.py sync --dry-run` ✓
    - `python scripts/mgmt_layer_jira_init.py --dry-run` ✓

- `TEST-S1-10` – Validação de novo entrypoint python -m integrators.jira
  - Escopo: confirmar que comando via módulo funciona
  - Resultado: aprovado
  - Evidências:
    - `python -m integrators.jira status` ✓
    - `python -m integrators.jira sync --dry-run` ✓
    - `python -m integrators.jira bootstrap --dry-run` ✓

- `TEST-S1-11` – Validação de documentação canônica Jira
  - Escopo: confirmar atualização de docs/ARCHITECTURE.md e docs/OPERATIONS.md
  - Resultado: aprovado
  - Evidências:
    - docs/ARCHITECTURE.md contém seção "Camada de Integração Jira" com arquitetura, padrões e decisões de design
    - docs/OPERATIONS.md contém seção "Procedimentos: Jira Integration" com comandos, troubleshooting e limitações
    - README.md passou a refletir a camada Jira como entry point da sprint ativa
    - Dev_Tracking_S1.md atualizado com ST-S1-07 Done

---

## 6. Timestamp UTC

Event | Start | Finish | Status
---|---|---|---
BUG-S0-01 | 2026-03-07T02:32:34-ST | 2026-03-07T02:33:34-FN | To-Do
TEST-S0-01 | 2026-03-12T23:00:00-ST | 2026-03-12T23:12:53-FN | Passed
TEST-S0-02 | 2026-03-13T01:04:29-ST | 2026-03-13T01:04:29-FN | Passed
TEST-S0-03 | 2026-03-13T01:11:56-ST | 2026-03-13T01:11:56-FN | Passed
TEST-S0-04 | 2026-03-13T00:13:07-ST | 2026-03-13T00:13:07-FN | Passed
TEST-S0-05 | 2026-03-13T00:21:50-ST | 2026-03-13T00:40:18-FN | Passed
BUG-S1-01 | 2026-03-13T00:41:00-ST | - | To-Do
TEST-S1-01 | 2026-03-19T21:00:00-ST | 2026-03-19T21:05:00-FN | Passed
TEST-S1-02 | 2026-03-19T21:05:00-ST | 2026-03-19T21:10:00-FN | Passed
TEST-S1-03 | 2026-03-19T21:10:00-ST | 2026-03-19T21:15:00-FN | Passed
TEST-S1-04 | 2026-03-19T21:15:00-ST | 2026-03-19T21:20:00-FN | Passed
TEST-S1-05 | 2026-03-19T21:20:00-ST | 2026-03-19T21:25:00-FN | Passed
TEST-S1-06 | 2026-03-19T21:30:00-ST | 2026-03-19T21:31:00-FN | Passed
TEST-S1-07 | 2026-03-19T21:31:00-ST | 2026-03-19T21:32:00-FN | Passed
TEST-S1-08 | 2026-03-19T21:53:00-ST | 2026-03-19T21:55:00-FN | Passed
TEST-S1-09 | 2026-03-19T21:55:00-ST | 2026-03-19T21:57:00-FN | Passed
TEST-S1-10 | 2026-03-20T00:04:00-ST | 2026-03-20T00:05:00-FN | Passed
TEST-S1-11 | 2026-03-20T00:16:00-ST | 2026-03-20T00:17:00-FN | Passed
BUG-S1-02 | 2026-03-19T21:30:00-ST | 2026-03-19T21:31:00-FN | Closed

## 7. Ressalvas Técnicas

1. Sprint S0 foi encerrada com a base documental, KB local e prova técnica de integração Jira concluídos.
2. Sprint S1 inicia a estruturação formal da camada Jira Cloud subordinada ao DOC2.5 e já nasce com herança de backlog, change requests e bug aberto.
3. Credenciais operacionais permanecem em `.scr/.env` e não devem ser versionadas.
4. A partir de TEST-S1-08, o código foi refatorado para arquitetura `integrators/` com wrappers de compatibilidade em `scripts/`.

## 8. Sprints Futuras

Sprints subsequentes (S1, S2, etc.) serão adicionadas conforme o progresso do projeto.
