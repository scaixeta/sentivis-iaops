---
name: servicenow-itsm-sla-compliance
description: Skill: ServiceNow ITSM SLA Compliance
---

# Skill: ServiceNow ITSM SLA Compliance

Este skill capacita o agente a monitorar o cumprimento de acordos de nível de serviço (SLA) no ServiceNow, fornecendo métricas de eficiência para o Project Health.

## Tabelas de Referência (Escopo SLA)

- **`task_sla`**: Registros de tempo e status dos SLAs individuais.
- **`contract_sla`**: Definições contratuais de tempo (Response/Resolution).
- **`sys_user_group`**: Times de suporte e sustentação.

## Fluxo de Monitoramento de Eficiência

1. **Real-time**: Verificar tarefas próximas de violar o SLA (*Breach*).
2. **Desempenho**: Avaliar a média de cumprimento de SLA por produto e projeto.
3. **Gargalo**: Identificar times com alto índice de violação.

## Indicadores de Saúde (SLA Compliance)

| Indicador | Dimensão | Tabela/Campo | Descrição |
|-----------|----------|--------------|-----------|
| **SLA Achievement** | Execução | `task_sla.has_breached` | % de tarefas concluídas dentro do prazo contratual. |
| **Business Elapsed Time** | Valor | `business_elapsed_percentage` | Consumo médio do tempo de SLA por tarefa. |
| **Backlog SLA Risk** | Risco | `task_sla.time_left` | Volume de tarefas pendentes em risco iminente. |

## Ferramentas MCP Recomendadas

- `sn_table_query`: Para extrair o status atual dos SLAs de tarefas críticas.
- `ph_project_task_health_summary`: Para correlacionar tarefas de projeto com possíveis atrasos operacionais.

## Exemplo de Query (Grep/Pattern)

Para listar SLAs violados no mês atual:
`sysparm_query=has_breached=true^start_timeONThis%20month@javascript:gs.beginningOfThisMonth()@javascript:gs.endOfThisMonth()`
