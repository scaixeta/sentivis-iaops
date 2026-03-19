---
name: servicenow-zurich-portfolio-management
description: Skill: ServiceNow Zurich - Portfolio Management
---

# Skill: ServiceNow Zurich - Portfolio Management
# Status: DRAFT (Based on Zurich 2025)

## Descrição
Gestão de Portfólios de Projetos (PPM) na Service Now Zurich. Permite o agrupamento de projetos, demandas e programas para alinhamento estratégico e controle financeiro centralizado.

## Componentes de Portfólio
- **Partes Interessadas (Stakeholders)**: Gestão de registros de pessoas interessadas no portfólio. Partes interessadas do portfólio são herdadas automaticamente pelas demandas/projetos vinculados.
- **Gráficos de Bolha de Portfólio**: Visualização similar ao workbench de demanda, mas focada na saúde e valor do portfólio completo.
- **Linhas de Base de Portfólio (Baselines)**: Snapshots financeiros e de cronograma para comparação histórica.

## Planejamento e Finanças
- **Custo Total Planejado**: Acúmulo de todos os projetos e demandas subjacentes.
- **Previsão de Benefícios**: Estimativas de retorno sobre o investimento do portfólio.
- **Metas do Portfólio**: Definição de objetivos de alto nível que orientam a seleção de demandas.

## Tabelas Principais
| Tabela | Descrição |
| :--- | :--- |
| `pm_portfolio` | Registro de Portfólio |
| `pm_portfolio_project` | Relacionamento M2M Portfólio-Projeto |

> [!NOTE]
> O Portfólio é o nível mais alto de agregação no SPM, permitindo visibilidade Cross-Project e Cross-Program.
