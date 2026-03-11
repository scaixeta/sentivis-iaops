# ARCHITECTURE

## Proposito

Descrever como o sistema esta organizado em termos de governanca, componentes, fluxos e integracoes.

## Visao geral da arquitetura

- papel do projeto
- camadas principais
- limites do que faz parte do modelo canonico

## Componentes principais

- regras e governanca
- runtime de skills
- workflows
- documentacao canonica
- utilitarios e scripts

## Fluxos principais

### Fluxo 1: Descoberta e planejamento

- identificar orchestrator ou runtime
- carregar regras e tracking
- consultar skills e workflows
- propor plano ao PO

### Fluxo 2: Execucao e rastreabilidade

- executar a menor mudanca necessaria
- atualizar tracking e testes
- registrar `Timestamp UTC`

## Integracoes externas

- listar apenas integracoes reais do projeto
- remover referencias a ferramentas ou projetos externos que nao facam parte da base

## Decisoes arquiteturais relevantes

- registrar apenas decisoes reais e ja tomadas
- referenciar `Dev_Tracking_SX.md` quando houver decisao de sprint

## Relacao com outros artefatos

- `DEVELOPMENT.md`
- `OPERATIONS.md`
- `Dev_Tracking.md`
- `Dev_Tracking_SX.md`
- `tests/bugs_log.md`
