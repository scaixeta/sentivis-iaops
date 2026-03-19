---
name: servicenow-itsm-operational-stability
description: Skill: ServiceNow ITSM Operational Stability
---

# Skill: ServiceNow ITSM Operational Stability

Este skill capacita o agente a avaliar a estabilidade operacional de produtos e sistemas no ServiceNow, focando no impacto de Incidentes e Problemas na saúde do Project Health.

## Tabelas de Referência (Escopo Estabilidade)

- **`incident`**: Registros de interrupção ou redução de qualidade de serviço.
- **`problem`**: Identificação de causas raiz para incidentes recorrentes.
- **`sys_user_group`**: Times responsáveis pela resolução.

## Fluxo de Análise de Estabilidade

1. **Impacto**: Avaliar o volume de incidentes críticos vinculados a um Produto (`rm_product`) ou CI.
2. **Recorrência**: Verificar se existem Problemas abertos sem solução definitiva para o produto.
3. **Escalonamento**: Monitorar reaberturas e tempos de resolução (MTTR).

## Indicadores de Saúde (Stability)

| Indicador | Dimensão | Tabela/Campo | Descrição |
|-----------|----------|--------------|-----------|
| **Incident Volume** | Qualidade | `incident` | Contagem total de incidentes por período. |
| **MTTR** | Execução | `incident.u_resolution_time` | Tempo médio para restaurar o serviço. |
| **Problem Coverage** | Estabilidade | `problem` | % de incidentes críticos com problemas vinculados. |
| **Reopen Rate** | Qualidade | `incident.reopen_count` | Índice de retrabalho na resolução de falhas. |

## Ferramentas MCP Recomendadas

- `sn_table_query`: Para extrair a lista de incidentes ativos e correlação com problemas.
- `sn_project_search`: Para identificar o contexto do projeto que pode estar gerando instabilidade.

## Exemplo de Query (Grep/Pattern)

Para buscar incidentes críticos ativos de um produto específico:
`sysparm_query=cmdb_ci=SYS_ID_PRODUTO^priority=1^state!=7^ORDERBYDESCsys_created_on`
