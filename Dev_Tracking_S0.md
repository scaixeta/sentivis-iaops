# Dev_Tracking – Sprint S0 (Sentivis AIOps)

## 1. Identificação da Sprint

- Sprint: S0
- Projeto: Sentivis AIOps
- Período: 2026-03-10 – em andamento
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

| Status | Estória |
|--------|---------|
| Done | ST-S0-01 – Validar estrutura DOC2.5 do projeto |
| Done | ST-S0-02 – Consolidar documentação ThingsBoard CE |
| To-Do | ST-S0-03 – Definir contrato de mock telemetry |
| To-Do | ST-S0-04 – Mapear device/profile modeling |
| To-Do | ST-S0-05 – Documentar configuração post-setup |
| To-Do | ST-S0-06 – Definir baseline de dashboard |
| To-Do | ST-S0-07 – Avaliar uso do Rule Engine |
| To-Do | ST-S0-08 – Validar VS Code como workstation |
| To-Do | ST-S0-09 – Documentar trilha de evidência |
| To-Do | ST-S0-10 – Preparar baseline para hardware real |
| Done | ST-S0-11 – Normalizar estrutura base do ThingsBoard Knowledge Layer (MVP-1) |
| Done | ST-S0-12 – Criar navegação low-token (topic index + reading priority) |
| Done | ST-S0-13 – Criar runbooks operacionais curtos para tarefas críticas |
| Done | ST-S0-14 – Normalizar script de sync seguro sem ingestão real |
| Done | ST-S0-15 – Atualizar docs canônicos e rastreabilidade DOC2.5 do MVP-1 |
| Done | ST-S0-16 – Documentar triagem N1 para estação offline em talhão |

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
  - Nota de governança: na próxima atualização documental, normalizar nomenclatura entre `Sentivis SIM` e `Sentivis AIOps`

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
  - `Dev_Tracking_S0.md`
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
  - Normalizar nomenclatura do projeto (`Sentivis SIM` vs `Sentivis AIOps`) na próxima atualização documental.

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
  - `Dev_Tracking_S0.md`
  - `tests/bugs_log.md`
- Resultado:
  - fluxo N1 documentado
  - comandos de confirmação registrados
  - fallback explícito para KB local preservado

---

## 5. Referências a Testes e Bugs (resumo)

Os detalhes de testes e bugs relacionados a esta sprint devem ser registrados em:
- `tests/bugs_log.md`, na seção correspondente à Sprint S0

---

## 6. Timestamp UTC

Event | Start | Finish | Status
---|---|---|---
ST-S0-01 | WED03112026021556AMST | WED03112026021556AMFN | Done
ST-S0-02 | THU03122026110000PMST | THU03122026111253PMFN | Done
ST-S0-03 | DDDMMDDYYYYHHMMSSamPMST | DDDMMDDYYYYHHMMSSamPMFN | To-Do
ST-S0-04 | DDDMMDDYYYYHHMMSSamPMST | DDDMMDDYYYYHHMMSSamPMFN | To-Do
ST-S0-05 | DDDMMDDYYYYHHMMSSamPMST | DDDMMDDYYYYHHMMSSamPMFN | To-Do
ST-S0-06 | DDDMMDDYYYYHHMMSSamPMST | DDDMMDDYYYYHHMMSSamPMFN | To-Do
ST-S0-07 | DDDMMDDYYYYHHMMSSamPMST | DDDMMDDYYYYHHMMSSamPMFN | To-Do
ST-S0-08 | DDDMMDDYYYYHHMMSSamPMST | DDDMMDDYYYYHHMMSSamPMFN | To-Do
ST-S0-09 | DDDMMDDYYYYHHMMSSamPMST | DDDMMDDYYYYHHMMSSamPMFN | To-Do
ST-S0-10 | DDDMMDDYYYYHHMMSSamPMST | DDDMMDDYYYYHHMMSSamPMFN | To-Do
ST-S0-11 | WED03112026110000PMST | WED03112026111000PMFN | Done
ST-S0-12 | WED03112026111000PMST | WED03112026112000PMFN | Done
ST-S0-13 | WED03112026112000PMST | WED03112026113500PMFN | Done
ST-S0-14 | WED03112026113500PMST | WED03112026114500PMFN | Done
ST-S0-15 | WED03112026114500PMST | WED03112026115500PMFN | Done
ST-S0-16 | FRI03132026121156AMST | FRI03132026121156AMFN | Done
D-S0-01 | TUE03102026103000PMST | TUE03102026103100PMFN | Logged
D-S0-02 | TUE03102026103000PMST | TUE03102026103100PMFN | Logged
D-S0-03 | TUE03102026103000PMST | TUE03102026103100PMFN | Logged
D-S0-04 | WED03112026021556AMST | WED03112026021556AMFN | Logged
D-S0-05 | WED03112026030000AMST | WED03112026033000AMFN | Logged
D-S0-06 | WED03112026113000PMST | WED03112026113200PMFN | Logged
D-S0-07 | WED03112026113200PMST | WED03112026113400PMFN | Logged
D-S0-08 | WED03112026120000PMST | WED03112026120200PMFN | Logged
D-S0-09 | THU03122026110000PMST | THU03122026111253PMFN | Logged
D-S0-10 | FRI03132026120429AMST | FRI03132026120429AMFN | Logged
D-S0-11 | FRI03132026121156AMST | FRI03132026121156AMFN | Logged

---

## 7. Política de Commits, Tasks/ e Testes (DOC2.5)

### Política de Commits
- **Nenhum commit sem autorização explícita do usuário**: o agente não deve executar `git commit` ou `git push` sem autorização textual explícita do usuário.
- **Commits concentrados no final da sprint**: Preferencialmente realizados ao final da sprint (commit S0-END), agrupando o trabalho da sprint.
- **Dev_Tracking como gate obrigatório**: Dev_Tracking_S0.md é o arquivo obrigatório de conclusão de trabalho; nenhuma tarefa é considerada concluída se o Dev_Tracking não refletir o que foi feito.

### Uso de tasks/
- **tasks/ como apoio de planejamento**: A pasta `tasks/` pode ser usada como espaço de planejamento interno da IA (listas, planos, rascunhos).
- **Não é fonte de verdade**: O conteúdo relevante deve ser sempre refletido no Dev_Tracking_S0.md, README e documentação oficial.
- **Migração obrigatória**: Informações relevantes de `tasks/` devem ser migradas para os documentos oficiais antes do final da sprint.

### Requisitos de Teste
- **Mudanças estruturais**: Mudanças em templates, regras, workflows ou lógica central devem ter pelo menos:
  - Uma estória de teste no backlog da sprint.
  - Entradas correspondentes em `tests/bugs_log.md` (TEST-S0-XX, BUG-S0-XX).
- **Validação mínima**: Cada sprint que alterar algo estrutural deve incluir pelo menos uma validação/documentação dos testes em `tests/bugs_log.md`.

---

## 8. Estado final da Sprint

(Preencher ao encerrar a sprint S0.)

- Itens concluídos:
  - MVP-1 (Fase 0-4) da camada local ThingsBoard Knowledge Layer executado no escopo aprovado.
  - Estrutura base, navegação low-token, runbooks operacionais e sync pipeline mínimo normalizados.
  - Importação seletiva CE concluída para `api`, `user-guide` e `tutorials`.
  - Atendimento N1 para estação offline documentado no KB e em operação oficial.
- Itens pendentes e realocados:
  - Validação runtime do script de sync pendente em ambiente com PowerShell.
  - Revisão curada futura da camada `reference/` e refinamento semântico do KB.
  - Normalização de nomenclatura do projeto (`Sentivis SIM` e `Sentivis AIOps`) na próxima atualização documental.
- Observações finais:
  - Execução sem commit/push, sem simulação de conteúdo importado e sem criação de LICENSE/NOTICE placeholder.

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
  - Detalhes da sprint: `Dev_Tracking_S0.md`
  - Log de testes e bugs: `tests/bugs_log.md`
