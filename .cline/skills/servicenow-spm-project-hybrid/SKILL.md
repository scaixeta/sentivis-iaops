---
name: servicenow-spm-project-hybrid
description: Skill: ServiceNow SPM Project Hybrid Health
---

# Skill: ServiceNow SPM Project Hybrid Health

Este skill capacita o agente a avaliar a saúde de projetos híbridos (Waterfall + Ágil) no ServiceNow, integrando cronogramas tradicionais com execuções ágeis para gerar o Health Score (0-100).

## Tabelas de Referência (Escopo Híbrido)

- **`pm_project`**: Tabela principal de projetos.
- **`pm_project_task`**: Tarefas de projeto (WBS).
- **`pm_portfolio`**: Agrupador estratégico.
- **`dmn_demand`**: Origem estratégica (business case).

## Metodologia de Saúde (Project Health Score)

A saúde do projeto é calculada observando 4 frentes:

1. **Consistência (Execução)**: `pm_project.percent_complete` vs `planned_duration`.
2. **Sustentabilidade (Recursos)**: `pm_project_task` late/stale.
3. **Governança Formal (ITSM)**: Mudanças vinculadas ao projeto (`change_request`).
4. **Engajamento (Entregas)**: Histórias concluídas vinculadas ao projeto.

## Indicadores de Saúde (Project Hybrid)

| Indicador | Dimensão | Tabela/Campo | Descrição |
|-----------|----------|--------------|-----------|
| **Health Score** | Geral | `pm_project.status` / `score` | Nota quantitativa de saúde do projeto. |
| **Late Tasks** | Execução | `pm_project_task` (Atrasadas) | Volume de tarefas pendentes após a data alvo. |
| **Milestone Health** | Risco | `pm_project_task` (milestone=true) | % de marcos concluídos no prazo. |
| **Demand Alignment** | Valor | `dmn_demand.priority` | Alinhamento com as prioridades da área de negócio. |

## Ferramentas MCP Recomendadas

- `ph_project_health_overview_v1`: Fornece o resumo de saúde e indicadores base.
- `ph_project_task_health_summary`: Dashboard de tarefas em atraso (late) ou sem atualização (stale).
- `sn_project_search`: Localização rápida de projetos para análise.

## Exemplo de Query (Grep/Pattern)

Para identificar tarefas críticas em atraso:
`sysparm_query=parent=SYS_ID_PROJETO^end_date<javascript:gs.beginningOfToday()^percent_complete<100`
