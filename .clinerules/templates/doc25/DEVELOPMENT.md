# DEVELOPMENT

## Proposito

Descrever como o desenvolvimento deve ser conduzido neste projeto seguindo DOC2.5.

## Principios

- uma sprint ativa por vez
- tracking obrigatorio
- mudanca minima necessaria
- plano antes de execucao
- sem estruturas paralelas fora do modelo canonico

## Fluxo geral

### 1. Ler contexto

- `README.md`
- `rules/WORKSPACE_RULES.md`
- `Dev_Tracking.md`
- `Dev_Tracking_SX.md`
- `tests/bugs_log.md`

### 2. Planejar

- resumir entendimento
- propor plano
- aguardar aprovacao explicita do PO

### 3. Executar

- atualizar backlog em tabela `Status | Estoria`
- registrar decisoes como `[D-SX-YY] - descricao`
- referenciar bugs e testes em `tests/bugs_log.md`

### 4. Atualizar rastreabilidade

- manter `Dev_Tracking_SX.md` coerente
- atualizar `Dev_Tracking.md` quando necessario
- sincronizar docs canonicos se a realidade do projeto mudou

## Politica de leitura vs alteracao

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

## Tests e bugs

- log centralizado em `tests/bugs_log.md`
- `Timestamp UTC` nas tabelas de tracking
- `Dev_Tracking_SX.md` recebe resumo e referencias cruzadas
