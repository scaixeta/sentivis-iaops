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

---

## 3. Backlog da Sprint (STATUS | ESTÓRIA)

| Status | Estória |
|--------|---------|
| Done | ST-S0-01 – Validar estrutura DOC2.5 do projeto |
| To-Do | ST-S0-02 – Consolidar documentação ThingsBoard CE |
| To-Do | ST-S0-03 – Definir contrato de mock telemetry |
| To-Do | ST-S0-04 – Mapear device/profile modeling |
| To-Do | ST-S0-05 – Documentar configuração post-setup |
| To-Do | ST-S0-06 – Definir baseline de dashboard |
| To-Do | ST-S0-07 – Avaliar uso do Rule Engine |
| To-Do | ST-S0-08 – Validar VS Code como workstation |
| To-Do | ST-S0-09 – Documentar trilha de evidência |
| To-Do | ST-S0-10 – Preparar baseline para hardware real |

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

---

## 5. Referências a Testes e Bugs (resumo)

Os detalhes de testes e bugs relacionados a esta sprint devem ser registrados em:
- `tests/bugs_log.md`, na seção correspondente à Sprint S0

---

## 6. Timestamp UTC

Event | Start | Finish | Status
---|---|---|---
ST-S0-01 | WED03112026021556AMST | WED03112026021556AMFN | Done
ST-S0-02 | DDDMMDDYYYYHHMMSSamPMST | DDDMMDDYYYYHHMMSSamPMFN | To-Do
ST-S0-03 | DDDMMDDYYYYHHMMSSamPMST | DDDMMDDYYYYHHMMSSamPMFN | To-Do
ST-S0-04 | DDDMMDDYYYYHHMMSSamPMST | DDDMMDDYYYYHHMMSSamPMFN | To-Do
ST-S0-05 | DDDMMDDYYYYHHMMSSamPMST | DDDMMDDYYYYHHMMSSamPMFN | To-Do
ST-S0-06 | DDDMMDDYYYYHHMMSSamPMST | DDDMMDDYYYYHHMMSSamPMFN | To-Do
ST-S0-07 | DDDMMDDYYYYHHMMSSamPMST | DDDMMDDYYYYHHMMSSamPMFN | To-Do
ST-S0-08 | DDDMMDDYYYYHHMMSSamPMST | DDDMMDDYYYYHHMMSSamPMFN | To-Do
ST-S0-09 | DDDMMDDYYYYHHMMSSamPMST | DDDMMDDYYYYHHMMSSamPMFN | To-Do
ST-S0-10 | DDDMMDDYYYYHHMMSSamPMST | DDDMMDDYYYYHHMMSSamPMFN | To-Do
D-S0-01 | TUE03102026103000PMST | TUE03102026103100PMFN | Logged
D-S0-02 | TUE03102026103000PMST | TUE03102026103100PMFN | Logged
D-S0-03 | TUE03102026103000PMST | TUE03102026103100PMFN | Logged
D-S0-04 | WED03112026021556AMST | WED03112026021556AMFN | Logged

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
- Itens pendentes e realocados:
- Observações finais:

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
