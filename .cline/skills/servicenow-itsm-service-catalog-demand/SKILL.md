---
name: servicenow-itsm-service-catalog-demand
description: Skill: ServiceNow ITSM Service Catalog Demand
---

# Skill: ServiceNow ITSM Service Catalog Demand

Este skill capacita o agente a rastrear demandas originadas no Catálogo de Serviços do ServiceNow, integrando o fluxo de Requisições com a evolução do Produto.

## Tabelas de Referência (Escopo Catálogo)

- **`sc_req_item`**: Itens solicitados no catálogo (RITM).
- **`sc_request`**: Cabeçalho da requisição (REQ).
- **`sc_task`**: Tarefas operacionais de catálogo.

## Fluxo de Valor do Catálogo

1. **Captura**: Identificar solicitações recorrentes de novos campos ou fluxos em produtos.
2. **Triagem**: Verificar se a requisição é operacional (Run) ou se deve se tornar um item de evolução de produto (Change/Agile).
3. **Entrega**: Monitorar o tempo de ciclo para entrega de itens de valor imediato.

## Indicadores de Saúde (Catalog Demand)

| Indicador | Dimensão | Tabela/Campo | Descrição |
|-----------|----------|--------------|-----------|
| **Request Cycle Time** | Execução | `opened_at` vs `closed_at` | Tempo total para entrega de uma requisição. |
| **Volume per Product** | Valor | `cmdb_ci` | Concentração de demandas por aplicação/sistema. |
| **Request Satisfactor** | Valor | `survey_response` (opcional) | Nível de satisfação com a entrega do catálogo. |

## Ferramentas MCP Recomendadas

- `sn_table_query`: Para extrair e filtrar itens de requisição (`RITM`).

## Exemplo de Query (Grep/Pattern)

Para listar itens de requisição ativos vinculados a um serviço de negócio:
`sysparm_query=business_service=SYS_ID_SERVICO^state!=3^state!=4`
