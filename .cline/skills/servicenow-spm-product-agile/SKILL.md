---
name: servicenow-spm-product-agile
description: Skill: ServiceNow SPM Product Agile Evolution
---

# Skill: ServiceNow SPM Product Agile Evolution

Este skill capacita o agente a rastrear a evolução de um produto no ServiceNow desde a sua concepção (Ideia) até a entrega ágil (Stories/Sprints), focando em indicadores de Valor e Velocidade conforme a metodologia Project Health.

## Tabelas de Referência (Escopo Ágil)

- **`idea`**: Ponto de entrada (Inovação).
- **`rm_product`**: Definição do sistema/produto.
- **`rm_feature`**: Agrupador de funcionalidades.
- **`rm_story`**: Unidade de entrega ágil.
- **`rm_sprint`**: Ciclo de trabalho.
- **`rm_epic`**: Iniciativa estratégica de médio/longo prazo.

## Fluxo de Rastreabilidade

1. **Origem**: `idea` -> `dmn_demand` (quando aprovada).
2. **Planejamento**: `dmn_demand` -> `rm_epic`.
3. **Execução**: `rm_epic` -> `rm_feature` -> `rm_story`.
4. **Timebox**: `rm_story` atribuída a uma `rm_sprint`.

## Indicadores de Saúde (Product Agile)

| Indicador | Dimensão | Tabela/Campo | Descrição |
|-----------|----------|--------------|-----------|
| **Throughput** | Execução | `rm_story` (Estado=Concluído) | Volume de estórias entregues por período. |
| **Backlog Age** | Valor | `rm_story` (sys_created_on) | Idade média dos itens pendentes de alta prioridade. |
| **Sprint Variance** | Risco | `rm_story` (Sprint Planejada vs Real) | Desvio entre o planejado no início da sprint e o entregue. |
| **Idea Engagement** | Estratégia | `cf_feedback` / `cf_comment` | Nível de interesse/curtidas no backlog inicial. |

## Ferramentas MCP Recomendadas

- `sn_table_query`: Para extrair listas de histórias e feedbacks.
- `ph_idea_engagement_summary_v1`: Para métricas de curtidas/comentários em ideias específicas.
- `ph_idea_inventory_v1`: Para listar o backlog de inovação pendente.

## Exemplo de Query (Grep/Pattern)

Para buscar histórias de um Épico específico vinculadas a um Produto:
`sysparm_query=product=SYS_ID_PRODUTO^epic=SYS_ID_EPICO^ORDERBYDESCsys_created_on`
