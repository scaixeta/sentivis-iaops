# Dev_Tracking – Sprint S0 (Sentivis IAOps)

## 1. Identificação da Sprint

- Sprint: S0
- Projeto: Sentivis IAOps
- Período: 2026-03-10 – 2026-03-13
- Contexto inicial:
  - Projeto inicializado para validar backbone de dados ThingsBoard CE
  - Fase 1 utiliza dispositivos mock para simulação de telemetria
  - Hardware real (ESP32/LoRa) será integrado em fases posteriores

---

## 2. Objetivos da Sprint

- [OBJ-S0-01] Consolidar manual operacional ThingsBoard CE para este projeto
- [OBJ-S0-02] Definir contrato de mock telemetry (payload JSON)
- [OBJ-S0-03] Validar estratégia de ingestão inicial (HTTP/MQTT)
- [OBJ-S0-04] Estruturar device/profile modeling em ThingsBoard
- [OBJ-S0-05] Documentar configuração post-setup mínima
- [OBJ-S0-06] Entregar dashboard baseline para Fase 1
- [OBJ-S0-07] Avaliar uso mínimo do Rule Engine
- [OBJ-S0-08] Validar VS Code como estação de trabalho
- [OBJ-S0-09] Definir trilha de evidência para Fase 1
- [OBJ-S0-10] Preparar baseline para substituição de mock por hardware real
- [OBJ-S0-11] Criar estrutura de repositório para documentação ThingsBoard CE
- [OBJ-S0-12] Criar script de sincronização de documentação
- [OBJ-S0-13] Atualizar documentação canônica DOC2.5
- [OBJ-S0-14] Executar MVP-1 aprovado para ThingsBoard Knowledge Layer local (Fase 0-4)

---

## 3. Backlog da Sprint (STATUS | ESTÓRIA)

| Status | SP | Jira | Estória |
|--------|---:|---|---------|
| Done | 2 | STVIA-25 | ST-S0-01 – Validar estrutura DOC2.5 do projeto |
| Done | 8 | STVIA-26 | ST-S0-02 – Consolidar documentação ThingsBoard CE |
| Pending-S1 | 8 | STVIA-45 | ST-S0-03 – Definir contrato de mock telemetry |
| Pending-S1 | 13 | STVIA-46 | ST-S0-04 – Mapear device/profile modeling |
| Pending-S1 | 5 | STVIA-47 | ST-S0-05 – Documentar configuração post-setup |
| Pending-S1 | 13 | STVIA-48 | ST-S0-06 – Definir baseline de dashboard |
| Pending-S1 | 8 | STVIA-49 | ST-S0-07 – Avaliar uso do Rule Engine |
| Pending-S1 | 3 | STVIA-50 | ST-S0-08 – Validar VS Code como workstation |
| Pending-S1 | 5 | STVIA-51 | ST-S0-09 – Documentar trilha de evidência |
| Pending-S1 | 13 | STVIA-52 | ST-S0-10 – Preparar baseline para hardware real |
| Done | 8 | STVIA-27 | ST-S0-11 – Normalizar estrutura base do ThingsBoard Knowledge Layer (MVP-1) |
| Done | 5 | STVIA-28 | ST-S0-12 – Criar navegação low-token (topic index + reading priority) |
| Done | 8 | STVIA-29 | ST-S0-13 – Criar runbooks operacionais curtos para tarefas críticas |
| Done | 5 | STVIA-30 | ST-S0-14 – Normalizar script de sync seguro sem ingestão real |
| Done | 5 | STVIA-31 | ST-S0-15 – Atualizar docs canônicos e rastreabilidade DOC2.5 do MVP-1 |
| Done | 3 | STVIA-32 | ST-S0-16 – Documentar triagem N1 para estação offline em talhão |
| Done | 3 | STVIA-33 | ST-S0-17 – Normalizar nomenclatura oficial para Sentivis IAOps |
| Done | 8 | STVIA-34 | ST-S0-18 – Produzir estudo operacional da camada Jira Cloud integrada ao DOC2.5 |

---

## 4. Interações e Decisões Relevantes da Sprint

[D-S0-01] – 2026-03-10 – Decisão: Usar HTTP como protocolo de ingestão MVP
  - Impacto: Simplifica integração inicial, acesso via REST API
  - Alternativa: MQTT seria mais adequado para produção com alta frequência

[D-S0-02] – 2026-03-10 – Decisão: Access Token como modelo de autenticação (ThingsBoard CE default)
  - Impacto: Autenticação por dispositivo via token, UI para gerenciamento

[D-S0-03] – 2026-03-10 – Decisão: Estrutura de device separada para Solo e Clima
  - Impacto: devices "Sentivis | Soil | 001" e "Sentivis | Climate | 001"
  - Permite separação lógica de métricas

[D-S0-04] – 2026-03-11 – Decisão: Normalizar artefatos DOC2.5 (timestamps e tabelas)
  - Impacto: reduz ambiguidade e melhora rastreabilidade mínima (Timestamp UTC no modelo do template)
  - Escopo: `README.md`, `rules/WORKSPACE_RULES.md`, `Dev_Tracking.md`, `tests/bugs_log.md`

[D-S0-05] – 2026-03-11 – Decisão: Criar estrutura de repositório para documentação ThingsBoard CE (Etapa A)
  - Impacto: estrutura preparada para ingestão, LICENSE/NOTICE pendentes até source path fornecido
  - Escopo: `third_party/thingsboard-ce/`, `knowledge/thingsboard/ce/`, `scripts/sync/thingsboard/`
  - Status: Etapa A concluída, Etapa B (ingestão real) pendente

[D-S0-06] – 2026-03-11 – Decisão: Ordem hierárquica oficial de leitura para Cindy no Knowledge Layer
  - Ordem: `topic_index.md` -> runbook -> referência curada -> upstream oficial (se necessário)
  - Impacto: menor consumo de tokens e resposta operacional mais rápida

[D-S0-07] – 2026-03-11 – Decisão: Ingestão real depende de upstream source path validado e aprovado pelo PO
  - Impacto: MVP-1 permanece em modo fundação local sem importação real
  - Guardrail: não criar LICENSE/NOTICE placeholder e não simular conteúdo importado

[D-S0-08] – 2026-03-11 – Decisão: MVP-1 aceito como concluído no nível estrutural
  - Aceite: fundação local da ThingsBoard Knowledge Layer aprovada pelo PO
  - Estado: ingestão real ainda não iniciada
  - Pendente: validação runtime do `sync_thingsboard_ce.ps1` no ambiente com PowerShell disponível
  - Próxima fase: B1 (inventário do upstream) após PO fornecer o caminho local do clone `thingsboard.github.io`
  - Nota de governança: na próxima atualização documental, normalizar nomenclatura entre `Sentivis SIM` e o nome oficial do projeto

[D-S0-09] – 2026-03-12 – Decisão: Executar importação seletiva CE a partir do upstream oficial
  - Source path informado pelo PO: `C:\repos\thingsboard.github.io`
  - Escopo executado: `_includes/docs/reference/**/*.md`, `_includes/docs/user-guide/**/*.md`, `_includes/docs/tutorials/**/*.md`
  - Exclusões aplicadas: `pe`, `cloud`, `edge`, assets não markdown e scripts auxiliares
  - Resultado: `269` arquivos importados para a camada local (`25` api, `239` user-guide, `5` tutorials)
  - Observação operacional: o clone local informado continha apenas `.git`; a importação efetiva foi materializada seletivamente a partir do upstream oficial e o script canônico foi atualizado para reruns com clone local materializado

[D-S0-10] – 2026-03-13 – Decisão: Tornar o KB local o fallback padrão para tarefas ambíguas
  - Objetivo: menor consumo de tokens com maior precisão operacional
  - Ordem oficial: `topic_index.md` -> runbook -> docs curados locais -> upstream oficial
  - Regra: quando a IA não souber o que executar, deve buscar primeiro no KB local antes de inferir ou recorrer ao upstream
  - Impacto: melhora a eficiência da Cindy e reduz respostas genéricas

[D-S0-11] – 2026-03-13 – Decisão: Formalizar atendimento N1 para estação offline usando o KB local
  - Cenário validado: cliente reporta talhão em vermelho e estação offline
  - Resposta padrão: confirmar device, token, última telemetria e dashboard antes de escalar
  - Evidência operacional: comandos `curl` e runbook dedicados documentados no KB e em `OPERATIONS.md`
  - Impacto: reduz ambiguidade de atendimento e acelera confirmação operacional

[D-S0-12] – 2026-03-13 – Decisão: Normalizar a nomenclatura oficial do projeto para `Sentivis IAOps`
  - Impacto: documentação canônica, board organizacional e repositório devem convergir para o mesmo nome oficial
  - Regra: referências legadas a `Sentivis SIM` passam a ser tratadas como nome de diretório local, não como nome oficial do projeto
  - Preservação: IDs de sprint, estórias, testes e bugs permanecem inalterados

[D-S0-13] – 2026-03-13 – Decisão: Definir Jira Cloud como camada de gestão externa opcional, subordinada ao DOC2.5
  - Precedência: `Dev_Tracking_SX.md` permanece como source of truth do trabalho executado
  - Reflexo operacional: backlog, status, prioridade, comentários e evidências podem ser sincronizados para o Jira
  - Entrega desta etapa: estudo detalhado registrado em `KB/jira-doc25-workflow-estudo.md`

[D-S0-14] – 2026-03-13 – Decisão: Encerrar a Sprint S0 e abrir a Sprint S1 com foco na integração Jira corretamente modelada
  - Motivo: a prova técnica de integração foi concluída, mas o modelo operacional correto ainda depende de mapeamento real de campos e workflow
  - Realocação: itens pendentes da S0 permanecem como referência histórica e a sprint ativa passa a ser a S1
  - Evidência: ambiente Jira limpo, `Dev_Tracking.md` atualizado, `Dev_Tracking_S1.md` criado

### Registro de execução MVP-1 (aprovado)

- Objetivo executado: fundação local do ThingsBoard Knowledge Layer (Fase 0-4), sem expansão de escopo.
- Aprovação aplicada: execução direta com base na aprovação prévia explícita do PO para MVP-1.
- Arquivos/pastas afetados:
  - `third_party/thingsboard-ce/`
  - `knowledge/thingsboard/ce/`
  - `scripts/sync/thingsboard/`
  - `docs/ARCHITECTURE.md`
  - `docs/DEVELOPMENT.md`
  - `docs/OPERATIONS.md`
  - `docs/SETUP.md`
  - `Sprint/Dev_Tracking_S0.md`
- Validações executadas:
  - Estrutura canônica `docs/` preservada (4 arquivos).
  - `docs/README.md` inexistente.
  - `SOURCES.md`, `import_manifest.md`, `exclusions.md` em estado pendente.
  - `mapping_table.csv` apenas com header.
  - 8 runbooks presentes.
  - Script e README de sync presentes no caminho canônico.
- Pendências para fase futura:
  - Definir upstream source path oficial.
  - Executar validação runtime do script de sync em ambiente com PowerShell.
  - Iniciar fase B1 (inventário do upstream) após recebimento do caminho local do clone.
  - Popular camadas `reference/`, `api/`, `user-guide/`, `tutorials/` com conteúdo real.
  - Normalizar nomenclatura do projeto entre nome oficial e diretório local na próxima atualização documental.

### Registro de execução da importação seletiva CE

- Objetivo executado: importar seletivamente a documentação CE planejada para a Knowledge Layer local.
- Fonte utilizada: `thingsboard.github.io` (`master`, commit `ace54d00e592ca747b7e789e2d6f45b8f66e93c8`).
- Resultado consolidado:
  - `knowledge/thingsboard/ce/api/`: `25` arquivos
  - `knowledge/thingsboard/ce/user-guide/`: `239` arquivos
  - `knowledge/thingsboard/ce/tutorials/`: `5` arquivos
  - Total: `269` arquivos importados
- Artefatos atualizados:
  - `third_party/thingsboard-ce/SOURCES.md`
  - `knowledge/thingsboard/ce/manifests/import_manifest.md`
  - `knowledge/thingsboard/ce/manifests/exclusions.md`
  - `knowledge/thingsboard/ce/manifests/mapping_table.csv`
  - `scripts/sync/thingsboard/sync_thingsboard_ce.ps1`
  - `scripts/sync/thingsboard/README.md`
  - `docs/ARCHITECTURE.md`
  - `docs/DEVELOPMENT.md`
  - `docs/OPERATIONS.md`
  - `docs/SETUP.md`

### Registro de execução do atendimento N1 documentado

- Objetivo executado: transformar a resposta operacional de estação offline em documentação oficial e reutilizável.
- Artefatos atualizados:
  - `knowledge/thingsboard/ce/runbooks/station-offline-triage.md`
  - `knowledge/thingsboard/ce/manifests/topic_index.md`
  - `docs/OPERATIONS.md`
  - `Sprint/Dev_Tracking_S0.md`
  - `tests/bugs_log.md`
- Resultado:
  - fluxo N1 documentado
  - comandos de confirmação registrados
  - fallback explícito para KB local preservado

### Registro de execução da normalização de nomenclatura

- Objetivo executado: alinhar documentação canônica, board organizacional e repositório ao nome oficial `Sentivis IAOps`.
- Escopo:
  - atualização documental em `README.md`, `rules/WORKSPACE_RULES.md`, `docs/` e tracking
  - atualização do board no GitHub Projects
  - preparação de consistência entre nome oficial e diretório local
- Observação:
  - `Sentivis SIM` permanece como nome do diretório local neste workspace

### Registro de execução do estudo Jira Cloud + DOC2.5

- Objetivo executado: especificar um workflow alternativo para operar o projeto com Jira Cloud sem romper a governança DOC2.5.
- Escopo:
  - documentação detalhada das operações Jira confirmadas
  - cruzamento entre backlog/decisões/timestamps do `Dev_Tracking` e entidades Jira
  - definição de precedência `DOC2.5 > Jira`
  - proposta de módulo futuro `mgmt_layer_jira`
- Artefato gerado:
  - `KB/jira-doc25-workflow-estudo.md`
- Resultado:
  - estudo pronto para orientar implementação futura da sincronização de sprint para Jira

### Registro de execução do teste técnico e limpeza Jira

- Objetivo executado: validar a integração técnica com Jira Cloud e limpar as issues de teste ao final do experimento.
- Escopo:
  - autenticação, leitura de projeto, criação de issues, transição de status e consulta por JQL
  - exclusão remota das issues geradas para manter o projeto STVIA limpo
- Resultado:
  - prova técnica concluída com sucesso
  - modelagem funcional final adiada para a S1

---

## 5. Referências a Testes e Bugs (resumo)

Os detalhes de testes e bugs relacionados a esta sprint devem ser registrados em:
- `tests/bugs_log.md`, na seção correspondente à Sprint S0

---

## 6. Timestamp UTC

Event | Start | Finish | Status
---|---|---|---
ST-S0-01 | 2026-03-11T02:15:56-ST | 2026-03-11T02:15:56-FN | Done
ST-S0-02 | 2026-03-12T23:00:00-ST | 2026-03-12T23:12:53-FN | Done
ST-S0-03 | 2026-03-13T00:00:00-ST | 2026-03-13T00:40:18-FN | Pending-S1
ST-S0-04 | 2026-03-13T00:00:00-ST | 2026-03-13T00:40:18-FN | Pending-S1
ST-S0-05 | 2026-03-13T00:00:00-ST | 2026-03-13T00:40:18-FN | Pending-S1
ST-S0-06 | 2026-03-13T00:00:00-ST | 2026-03-13T00:40:18-FN | Pending-S1
ST-S0-07 | 2026-03-13T00:00:00-ST | 2026-03-13T00:40:18-FN | Pending-S1
ST-S0-08 | 2026-03-13T00:00:00-ST | 2026-03-13T00:40:18-FN | Pending-S1
ST-S0-09 | 2026-03-13T00:00:00-ST | 2026-03-13T00:40:18-FN | Pending-S1
ST-S0-10 | 2026-03-13T00:00:00-ST | 2026-03-13T00:40:18-FN | Pending-S1
ST-S0-11 | 2026-03-11T23:00:00-ST | 2026-03-11T23:10:00-FN | Done
ST-S0-12 | 2026-03-11T23:10:00-ST | 2026-03-11T23:20:00-FN | Done
ST-S0-13 | 2026-03-11T23:20:00-ST | 2026-03-11T23:35:00-FN | Done
ST-S0-14 | 2026-03-11T23:35:00-ST | 2026-03-11T23:45:00-FN | Done
ST-S0-15 | 2026-03-11T23:45:00-ST | 2026-03-11T23:55:00-FN | Done
ST-S0-16 | 2026-03-13T01:11:56-ST | 2026-03-13T01:11:56-FN | Done
ST-S0-17 | 2026-03-13T00:13:07-ST | 2026-03-13T00:13:07-FN | Done
ST-S0-18 | 2026-03-13T00:21:50-ST | 2026-03-13T00:21:50-FN | Done
D-S0-01 | 2026-03-10T10:30:00-ST | 2026-03-10T10:31:00-FN | Logged
D-S0-02 | 2026-03-10T10:30:00-ST | 2026-03-10T10:31:00-FN | Logged
D-S0-03 | 2026-03-10T10:30:00-ST | 2026-03-10T10:31:00-FN | Logged
D-S0-04 | 2026-03-11T02:15:56-ST | 2026-03-11T02:15:56-FN | Logged
D-S0-05 | 2026-03-11T03:00:00-ST | 2026-03-11T03:30:00-FN | Logged
D-S0-06 | 2026-03-11T23:30:00-ST | 2026-03-11T23:32:00-FN | Logged
D-S0-07 | 2026-03-11T23:32:00-ST | 2026-03-11T23:34:00-FN | Logged
D-S0-08 | 2026-03-11T23:00:00-ST | 2026-03-11T23:02:00-FN | Logged
D-S0-09 | 2026-03-12T23:00:00-ST | 2026-03-12T23:12:53-FN | Logged
D-S0-10 | 2026-03-13T01:04:29-ST | 2026-03-13T01:04:29-FN | Logged
D-S0-11 | 2026-03-13T01:11:56-ST | 2026-03-13T01:11:56-FN | Logged
D-S0-12 | 2026-03-13T00:13:07-ST | 2026-03-13T00:13:07-FN | Logged
D-S0-13 | 2026-03-13T00:21:50-ST | 2026-03-13T00:21:50-FN | Logged
D-S0-14 | 2026-03-13T00:40:18-ST | 2026-03-13T00:40:18-FN | Logged

---

## 7. Política de Commits, Tasks/ e Testes (DOC2.5)

### Política de Commits
- **Nenhum commit sem autorização explícita do usuário**: o agente não deve executar `git commit` ou `git push` sem autorização textual explícita do usuário.
- **Commits concentrados no final da sprint**: Preferencialmente realizados ao final da sprint (commit S0-END), agrupando o trabalho da sprint.
- **Dev_Tracking como gate obrigatório**: `Sprint/Dev_Tracking_S0.md` é o registro oficial desta sprint encerrada; nenhuma tarefa é considerada concluída se o tracking não refletir o que foi feito.

### Uso de tasks/
- **tasks/ como apoio de planejamento**: A pasta `tasks/` pode ser usada como espaço de planejamento interno da IA (listas, planos, rascunhos).
- **Não é fonte de verdade**: O conteúdo relevante deve ser sempre refletido no tracking oficial da sprint, README e documentação oficial.
- **Migração obrigatória**: Informações relevantes de `tasks/` devem ser migradas para os documentos oficiais antes do final da sprint.

### Requisitos de Teste
- **Mudanças estruturais**: Mudanças em templates, regras, workflows ou lógica central devem ter pelo menos:
  - Uma estória de teste no backlog da sprint.
  - Entradas correspondentes em `tests/bugs_log.md` (TEST-S0-XX, BUG-S0-XX).
- **Validação mínima**: Cada sprint que alterar algo estrutural deve incluir pelo menos uma validação/documentação dos testes em `tests/bugs_log.md`.

---

## 8. Estado final da Sprint

- Itens concluídos:
  - MVP-1 (Fase 0-4) da camada local ThingsBoard Knowledge Layer executado no escopo aprovado.
  - Estrutura base, navegação low-token, runbooks operacionais e sync pipeline mínimo normalizados.
  - Importação seletiva CE concluída para `api`, `user-guide` e `tutorials`.
  - Atendimento N1 para estação offline documentado no KB e em operação oficial.
  - Estudo detalhado da camada Jira Cloud subordinada ao DOC2.5 produzido.
  - Prova técnica de integração Jira executada com sucesso e ambiente remoto limpo ao final.
- Itens pendentes e realocados:
  - Mapeamento correto do projeto Jira STVIA ficou realocado para a S1.
  - Validação runtime do script de sync pendente em ambiente com PowerShell.
  - Revisão curada futura da camada `reference/` e refinamento semântico do KB.
  - Diretório local ainda permanece como `Sentivis SIM` e poderá ser normalizado em fase futura, se o PO desejar.
- Observações finais:
  - Execução sem commit/push, sem simulação de conteúdo importado e sem criação de LICENSE/NOTICE placeholder.
  - Projeto Jira STVIA ficou limpo ao término da sprint.

---

## 9. Commit de Fechamento da Sprint (referência futura)

Título sugerido (quando a sprint S0 for encerrada):

- `S0-END: Validação inicial do data backbone ThingsBoard CE`

Corpo sugerido:

- Principais entregas:
  - Estrutura DOC2.5 do projeto
  - Documentação ThingsBoard CE
  - Contrato de mock telemetry
  - Baseline de dashboard

- Referências:
  - Detalhes da sprint: `Sprint/Dev_Tracking_S0.md`
  - Log de testes e bugs: `tests/bugs_log.md`