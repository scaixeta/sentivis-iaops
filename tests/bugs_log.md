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

## 5. Sprint S2

### 4. Bugs Registrados

- `BUG-S2-01` – Bug aberto herdado da S1 para triagem e qualificação funcional
  - Origem: herança direta do `BUG-S1-01` (pendente ao fim da S1)
  - Estado: corrigido
  - Correção: `reconcile` passou a aplicar escopo por label de sprint do tracking (`sprint_sX`), evitando falsos orphans quando o projeto tem issues de outras sprints
  - Evidência: TEST-S2-12 aprovado
  - Referências: `integrators/jira/cli.py`, `Dev_Tracking_S2.md`, `Sprint/Dev_Tracking_S1.md`

- `BUG-S2-02` – Listagem Jira retornando payload mínimo e reconcile preso ao tracking padrão
  - Origem: `search/jql` devolvia somente `id`/paginação sem `fields`, `reconcile` estava acoplado ao tracking ativo e o parser não reconhecia `Pending-S2`
  - Estado: corrigido
  - Correção: `get_project_issues()` agora solicita campos úteis e pagina automaticamente; `reconcile` aceita `--tracking-file`; parser DOC2.5 reconhece `Pending-S2`
  - Evidência: TEST-S2-05, TEST-S2-06 e TEST-S2-07 aprovados
  - Referências: `integrators/jira/client.py`, `integrators/jira/cli.py`, `integrators/common/doc25_parser.py`

### 5. Testes Registrados

- `TEST-S2-01` – Validação de transporte S0 para Jira
  - Escopo: executar sync com --tracking-file Sprint/Dev_Tracking_S0.md
  - Resultado: aprovado
  - Evidências: 10 issues criadas no Jira (STVIA-25 a STVIA-34), labels sprint_s0 e tracking_ST-S0-XX

- `TEST-S2-02` – Validação de transporte S1 para Jira
  - Escopo: executar sync com --tracking-file Sprint/Dev_Tracking_S1.md
  - Resultado: aprovado
  - Evidências: 10 issues criadas no Jira (STVIA-35 a STVIA-44), labels sprint_s1 e tracking_ST-S1-XX

- `TEST-S2-03` – Validação de suporte a --tracking-file
  - Escopo: confirmar que CLI aceita argumento --tracking-file
  - Resultado: aprovado
  - Evidências: sync com arquivo Sprint/Dev_Tracking_S0.md e Sprint/Dev_Tracking_S1.md funcionou

- `TEST-S2-04` – Validação de suporte a --yes para auto-confirmação
  - Escopo: confirmar que CLI aceita --yes para executar sem interação
  - Resultado: aprovado
  - Evidências: sync executado com --yes sem pedir confirmação

- `TEST-S2-05` – Validação da listagem Jira com campos completos
  - Escopo: confirmar que `search/jql` retorna `key`, `summary`, `labels` e `issuetype`
  - Resultado: aprovado
  - Evidências: 20 issues com campos completos visíveis

- `TEST-S2-06` – Validação de reconcile com tracking arquivado
  - Escopo: confirmar que `reconcile` aceita `--tracking-file` para S1 arquivada e S2 ativa
  - Resultado: aprovado
  - Evidências: `python -m integrators.jira reconcile --tracking-file Sprint/Dev_Tracking_S1.md` funciona

- `TEST-S2-07` – Validação de parser DOC2.5 para estados Pending-S2
  - Escopo: confirmar que o parser reconhece backlog com `Pending-S2`
  - Resultado: aprovado
  - Evidências: `python -m integrators.jira reconcile` enxerga os 15 itens locais da S2

- `TEST-S2-08` – Validação de labels de sprint já atribuídas
  - Escopo: confirmar que todas as issues S0 e S1 têm labels sprint_s0 / sprint_s1
  - Resultado: aprovado
  - Evidências:
    - JQL: `project = STVIA` retornou 20 issues com campos completos
    - S0: 10 issues (STVIA-25 a STVIA-34) têm label `sprint_s0`
    - S1: 10 issues (STVIA-35 a STVIA-44) têm label `sprint_s1`
    - Cada issue também tem label `tracking_<ID>`

- `TEST-S2-09` – Validação de correção de CLI sync default para S2
  - Escopo: confirmar que sync default agora usa Dev_Tracking_S2.md
  - Resultado: aprovado
  - Evidências: `python -m integrators.jira sync --dry-run` usa S2 por padrão

- `TEST-S2-10` – Validação de compilação dos módulos após correções
  - Escopo: confirmar que todos os módulos compilam sem erros
  - Resultado: aprovado
  - Evidências: py_compile executado com sucesso em todos os módulos

- `TEST-S2-11` – Validação de documentação de labels vs Sprint nativo
  - Escopo: confirmar que mapper.py documenta claramente que usa labels como fallback
  - Resultado: aprovado
  - Evidências: `integrators/jira/mapper.py` contém nota explicativa sobre labels vs Sprint nativo

- `TEST-S2-12` – Validação de reconcile com escopo por sprint do tracking
  - Escopo: confirmar que `reconcile` não marca como orphan issues de outras sprints quando há label `sprint_sX`
  - Resultado: aprovado
  - Evidências:
    - `python -m integrators.jira reconcile` mostra escopo `sprint_s2` e elimina falsos orphans de S0/S1
    - `python -m integrators.jira reconcile --tracking-file Sprint/Dev_Tracking_S1.md` mostra escopo `sprint_s1` e orphans coerentes com a sprint

- `TEST-S2-13` – Validação de comando sprint dates para definição de datas
  - Escopo: confirmar que o comando `sprint dates` define datas de início e fim em sprints nativos
  - Resultado: aprovado
  - Evidências:
    - Sprint S0: datas definidas (2026-03-10 a 2026-03-13)
    - Sprint S1: datas definidas (2026-03-13 a 2026-03-20)
    - Jira retorna os campos startDate e endDate corretamente
    - Documentação atualizada em docs/OPERATIONS.md

- `TEST-S2-14` – Validação de sincronização de datas de issues com timestamps do tracking
  - Escopo: confirmar que o comando `issue dates` sincroniza datas das issues Jira com timestamps DOC2.5
  - Resultado: aprovado
  - Evidências:
    - Comando: `python -m integrators.jira issue dates --tracking-file Sprint/Dev_Tracking_S0.md --dry-run` e `--yes`
    - Parser extrai timestamps da seção ## 6. Timestamp UTC
    - 18 issues atualizadas com Start Date e Due Date
    - Mapeamento: Start Date = timestamp start (data), Data Limite = timestamp finish (data)
    - Documentação atualizada em docs/ARCHITECTURE.md e docs/OPERATIONS.md

- `TEST-S2-15` – Validação de instrumentação do backlog (SP + Jira) no tracking
  - Escopo: confirmar que os `Dev_Tracking_SX.md` suportam tabela `Status | SP | Jira | Estória` e que o parser extrai `sp` e `jira`
  - Resultado: aprovado
  - Evidências:
    - `parse_sprint_backlog()` retorna `sp_filled` e `jira_filled` completos para S0/S1/S2
    - Entregáveis: `Sprint/Dev_Tracking_S0.md`, `Sprint/Dev_Tracking_S1.md`, `Dev_Tracking_S2.md`

- `TEST-S2-16` – Validação do campo Story Points no Jira (customfield_10016)
  - Escopo: confirmar existência do campo "Story point estimate" para permitir sync de `SP` -> Jira
  - Resultado: aprovado
  - Evidências:
    - `/rest/api/3/field` contém `customfield_10016 | Story point estimate | number`

- `TEST-S2-17` – Validação de reconcile após migração da tabela do backlog
  - Escopo: confirmar que `reconcile` segue operando com o tracking S2 no novo formato de tabela
  - Resultado: aprovado
  - Evidências:
    - `python -m integrators.jira reconcile --tracking-file Dev_Tracking_S2.md` executa com sucesso

- `TEST-S2-18` – Transição de status das estórias S0 para Em andamento via integrator
  - Escopo: usar issue progress (dry-run + apply)
  - Resultado: aprovado
  - Evidências:
    - Comando dry-run: `python -m integrators.jira issue progress --tracking-file Dev_Tracking_S2.md --prefix ST-S0- --target-status "Em progresso" --dry-run`
    - Comando apply: `python -m integrators.jira issue progress --tracking-file Dev_Tracking_S2.md --prefix ST-S0- --target-status "Em progresso" --yes`
    - 8 issues transicionadas de "A Fazer" para "Em progresso"
    - Keys: STVIA-45 a STVIA-52 (ST-S0-03 a ST-S0-10)
  - Entregáveis: `integrators/jira/cli.py` (novo comando issue progress)

- `TEST-S2-19` – Validação de leitura das colunas do board Jira (workflow)
  - Escopo: listar colunas/status do board do projeto STVIA e registrar no estado observado local
  - Resultado: aprovado
  - Evidências:
    - Comando: `python -m integrators.jira board columns --project-key STVIA`
    - Colunas observadas: Backlog, Pendentes, Em progresso, Em Testes, Feito
    - Estado persistido: `.scr/mgmt_layer.jira.json` (campo `board_columns`)
  - Entregáveis: `integrators/jira/client.py`, `integrators/jira/state.py`, `integrators/jira/sync_engine.py`, `integrators/jira/cli.py`

- `TEST-S2-20` – Validação de orientação de estado local a partir das colunas do board Jira
  - Escopo: confirmar que a leitura do board agora tambem produz uma orientacao explicita para o estado local DOC2.5 sem alterar arquivos de tracking
  - Resultado: aprovado
  - Evidências:
    - Comando: `python -m integrators.jira board columns --project-key STVIA --no-save`
    - Saída inclui seção `Orientacao para estado local (somente referencia)`
    - Estado observado suporta o campo `local_status_guidance`
    - Heuristica registrada: `Pendentes -> To-Do/Pending-SX`, `Em progresso -> Doing`, `Em Testes -> Doing`, `Feito -> Done/Accepted`
  - Entregáveis: `integrators/jira/board_reader.py`, `integrators/jira/state.py`, `integrators/jira/sync_engine.py`, `integrators/jira/cli.py`, `docs/OPERATIONS.md`

- `TEST-S2-21` – Validação de transição pontual de issue com comentário opcional
  - Escopo: confirmar que o integrador suporta transicionar uma issue Jira por key e adicionar comentario na mesma operacao
  - Resultado: aprovado em dry-run
  - Evidências:
    - Comando: `python -m integrators.jira issue transition --issue-key STVIA-25 --target-status "Bloqueado" --comment "Blocked temporarily while waiting for state." --dry-run`
    - Dry-run mostrou plano `TRANSITION STVIA-25: Em progresso -> Bloqueado`
    - Dry-run mostrou `COMMENT STVIA-25`
    - Transicoes disponiveis observadas para `STVIA-25`: `Bloqueado`, `Em Testes`, `Em progresso`, `Feito`
  - Entregáveis: `integrators/jira/cli.py`, `docs/OPERATIONS.md`

### 6. Snapshot de Desempenho (observado)

Objetivo: registrar um baseline replicável para análises de desempenho do time, baseado em `Timestamp UTC` (observação) e na calibração Fibonacci.

- Baseline atual (observado): ver `docs/feature_requests/FR-FIBONACCI-VALOR-1-21.md`
- Regra: toda nova validação relevante deve virar `TEST-SX-YY` com evidências e entregáveis (arquivos afetados).

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
BUG-S2-01 | 2026-03-20T01:31:05-ST | 2026-03-20T03:25:00-FN | Closed
BUG-S2-02 | 2026-03-20T01:44:00-ST | 2026-03-20T01:44:00-FN | Closed
TEST-S2-05 | 2026-03-20T01:44:00-ST | 2026-03-20T01:44:30-FN | Passed
TEST-S2-06 | 2026-03-20T01:44:30-ST | 2026-03-20T01:45:00-FN | Passed
TEST-S2-07 | 2026-03-20T01:45:00-ST | 2026-03-20T01:45:30-FN | Passed
TEST-S2-08 | 2026-03-20T02:10:00-ST | 2026-03-20T02:10:30-FN | Passed
TEST-S2-09 | 2026-03-20T02:10:30-ST | 2026-03-20T02:11:00-FN | Passed
TEST-S2-10 | 2026-03-20T02:11:00-ST | 2026-03-20T02:11:30-FN | Passed
TEST-S2-11 | 2026-03-20T02:11:30-ST | 2026-03-20T02:12:00-FN | Passed
TEST-S2-12 | 2026-03-20T03:25:00-ST | 2026-03-20T03:26:00-FN | Passed
TEST-S2-13 | 2026-03-20T04:10:00-ST | 2026-03-20T04:15:00-FN | Passed
TEST-S2-14 | 2026-03-20T04:33:00-ST | 2026-03-20T04:38:00-FN | Passed
TEST-S2-15 | 2026-03-20T23:57:34-ST | 2026-03-20T23:57:34-FN | Passed
TEST-S2-16 | 2026-03-20T23:57:34-ST | 2026-03-20T23:57:34-FN | Passed
TEST-S2-17 | 2026-03-20T23:57:34-ST | 2026-03-20T23:57:34-FN | Passed
TEST-S2-18 | 2026-03-21T10:23:00-ST | 2026-03-21T10:28:40-FN | Passed
TEST-S2-19 | 2026-03-21T13:42:56-ST | 2026-03-21T13:42:56-FN | Passed

## 7. Ressalvas Técnicas

1. Sprint S0 foi encerrada com a base documental, KB local e prova técnica de integração Jira concluídos.
2. Sprint S1 inicia a estruturação formal da camada Jira Cloud subordinada ao DOC2.5 e já nasce com herança de backlog, change requests e bug aberto.
3. Credenciais operacionais permanecem em `.scr/.env` e não devem ser versionadas.
4. A partir de TEST-S1-08, o código foi refatorado para arquitetura `integrators/` com wrappers de compatibilidade em `scripts/`.

## 8. Sprints Futuras

Sprints subsequentes (S3, S4, etc.) serão adicionadas conforme o progresso do projeto.
