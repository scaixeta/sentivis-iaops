# DEVELOPMENT

## Proposito

Este documento descreve como a evolucao do projeto deve ser conduzida seguindo DOC2.5, quais limites de fase devem ser respeitados, como o backlog deve ser instrumentado e como o trabalho deve permanecer rastreavel ao longo das sprints.

## 1. Principios de desenvolvimento

- uma sprint ativa por vez
- tracking obrigatorio
- mudanca minima necessaria
- plano antes de execucao
- sem estruturas paralelas fora do modelo canonico
- escopo aprovado prevalece sobre ambicao tecnica
- fato, inferencia e pendencia devem permanecer separados

## 2. Estado atual de desenvolvimento

- Fase atual: `{{CURRENT_PHASE}}`
- Sprint ativa: `{{ACTIVE_SPRINT}}`
- Escopo de desenvolvimento aprovado: `{{APPROVED_DEVELOPMENT_SCOPE}}`
- Fora do escopo atual: `{{OUT_OF_SCOPE_NOW}}`

## 3. Roadmap por fases

### 3.1 Fase atual

- `{{CURRENT_PHASE}}`
- Objetivo: `{{CURRENT_PHASE_OBJECTIVE}}`
- Entregas esperadas: `{{CURRENT_PHASE_DELIVERABLES}}`
- Limites explicitos: `{{CURRENT_PHASE_LIMITS}}`

### 3.2 Proxima fase

- `{{NEXT_PHASE_NAME}}`
- Objetivo: `{{NEXT_PHASE_OBJECTIVE}}`
- Dependencias para iniciar: `{{NEXT_PHASE_DEPENDENCIES}}`

### 3.3 Fases posteriores

- `{{FUTURE_PHASE_1}}`
- `{{FUTURE_PHASE_2}}`
- `{{FUTURE_PHASE_3}}`

## 4. Fluxo de desenvolvimento

### 4.1 Ler contexto

- `README.md`
- `rules/WORKSPACE_RULES.md`
- `Dev_Tracking.md`
- `Dev_Tracking_{{ACTIVE_SPRINT}}.md`
- `tests/bugs_log.md`
- `docs/SETUP.md`
- `docs/ARCHITECTURE.md`
- `docs/OPERATIONS.md`

### 4.2 Planejar

- resumir entendimento
- propor plano
- explicitar o que esta confirmado, inferido e pendente
- aguardar aprovacao explicita do PO quando a mudanca extrapolar o escopo corrente ou alterar a estrutura

### 4.3 Executar

- atualizar backlog em tabela `Status | Estoria`
- registrar decisoes como `[D-SX-YY] - descricao`
- referenciar bugs e testes em `tests/bugs_log.md`
- aplicar a menor mudanca necessaria para atingir o objetivo
- nao expandir arquitetura, automacao ou integracao sem gate formal

### 4.4 Atualizar rastreabilidade

- manter `Dev_Tracking_{{ACTIVE_SPRINT}}.md` coerente
- atualizar `Dev_Tracking.md` quando necessario
- sincronizar docs canonicos se a realidade do projeto mudou
- manter coerencia entre `README.md`, docs canonicos, tracking e `tests/bugs_log.md`

## 5. Backlog e instrumentacao da sprint

- backlog da sprint em tabela `Status | Estoria`
- decisoes em formato `[D-SX-YY] - descricao`
- referencias cruzadas para bugs e testes sempre que houver impacto relevante
- `Timestamp UTC` deve registrar eventos efetivamente executados
- fechamento de sprint so ocorre sob comando explicito do PO

## 6. Politica de leitura vs alteracao

### Leitura permitida

- `git status`
- `git log`
- `git show`
- `git branch`
- leitura de arquivos

### Alteracao exige gate

- `git add`
- `git commit`
- `git push`
- criacao/remocao de arquivos
- instalacao de dependencias

## 7. Mudancas permitidas na fase atual

- `{{ALLOWED_CHANGE_1}}`
- `{{ALLOWED_CHANGE_2}}`
- `{{ALLOWED_CHANGE_3}}`

## 8. Mudancas explicitamente bloqueadas nesta fase

- `{{BLOCKED_CHANGE_1}}`
- `{{BLOCKED_CHANGE_2}}`
- `{{BLOCKED_CHANGE_3}}`

## 9. Tests e bugs

- log centralizado em `tests/bugs_log.md`
- `Timestamp UTC` nas tabelas de tracking
- `Dev_Tracking_{{ACTIVE_SPRINT}}.md` recebe resumo e referencias cruzadas
- nao citar testes inexistentes
- quando nao houver automacao, registrar a validacao manual realmente executada

## 10. Referencias minimas

- `README.md`
- `docs/SETUP.md`
- `docs/ARCHITECTURE.md`
- `docs/OPERATIONS.md`
- `Dev_Tracking.md`
- `Dev_Tracking_{{ACTIVE_SPRINT}}.md`
- `tests/bugs_log.md`
