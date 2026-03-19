---
name: servicenow-itsm-change-risk-governance
description: Skill: ServiceNow ITSM Change & Risk Governance
---

# Skill: ServiceNow ITSM Change & Risk Governance

Este skill capacita o agente a avaliar o risco e a conformidade das mudanças no ServiceNow, integrando a governança formal de TI com a saúde dos projetos (Project Health).

## Tabelas de Referência (Escopo Mudança)

- **`change_request`**: Gestão formal de mudanças.
- **`change_request_imac`**: Mudanças de infraestrutura (específicas Iguá).
- **`change_task`**: Tarefas operacionais de implementação de mudanças.

## Fluxo de Governança de Risco

1. **Aderência**: Verificar se o projeto possui mudanças abertas para suas entregas de produção.
2. **Sucesso**: Avaliar o índice de `change_failures` (mudanças que geraram incidentes).
3. **Janela**: Monitorar conflitos de agenda e aprovações do CAB.

## Indicadores de Saúde (Change Governance)

| Indicador | Dimensão | Tabela/Campo | Descrição |
|-----------|----------|--------------|-----------|
| **Change Success Rate** | Qualidade | `change_request.close_code` | % de mudanças fechadas com sucesso. |
| **Unplanned Growth** | Risco | `change_request.type` | Volume de mudanças emergenciais vs planejadas. |
| **Project Alignment** | Governança | `change_request.parent` | Correlação entre mudanças e projetos ativos. |
| **Lead Time** | Execução | `sys_created_on` vs `start_date` | Antecedência na solicitação de mudanças. |

## Ferramentas MCP Recomendadas

- `sn_table_query`: Para validar o status de mudanças e identificar falhas técnicas.
- `ph_project_health_overview_v1`: Para cruzar o score de risco da mudança com a saúde do projeto.

## Exemplo de Query (Grep/Pattern)

Para listar mudanças falhas (que geraram incidentes) recentes:
`sysparm_query=close_code=successful_issues^ORclose_code=unsuccessful^sys_created_on>=javascript:gs.daysAgo(30)`
