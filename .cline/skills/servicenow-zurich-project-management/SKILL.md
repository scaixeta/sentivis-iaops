---
name: servicenow-zurich-project-management
description: Skill: ServiceNow Zurich - Project Management
---

# Skill: ServiceNow Zurich - Project Management
# Status: DRAFT (Based on Zurich 2025)

## Descrição
Gestão do ciclo de vida de projetos na Service Now Zurich. Suporta metodologias Cascata (Waterfall), Ágil e Híbrida.

## Planejamento de Projeto
- **Top-down vs Bottom-up**: Suporte a estimativas de alto nível que se desdobram em tarefas, ou detalhamento de tarefas que se acumulam no projeto. 
- **Console de Planejamento (Gantt)**: Interface principal para gestão de cronograma, dependências (FS, SS, FF, SF) e caminhos críticos.
- **Linhas de Base (Baselines)**: Snapshots para comparação entre o planejado vs realizado.

## Finanças do Projeto (Zurich)
- **Várias Moedas (Multicurrency)**: Capacidade de gerenciar projetos em moedas locais diferentes da moeda funcional da instância.
- **Plano de Custos (Cost Plan)**: Estimativas de despesas operacionais (Opex) e de capital (Capex).
- **Linhas de Despesa (Expense Lines)**: Registro de gastos reais integrando com registros de horas ou compras.
- **Plano de Benefícios**: Captura de retornos financeiros e não-financeiros (monetários e não-monetários).

## Inteligência Preditiva (ML)
- **Similar Projects**: Uso de Machine Learning (solução de semelhança) para identificar projetos passados similares baseados em nome e descrição, auxiliando na estimativa e evitando duplicidade.

## Tabelas Principais
| Tabela | Descrição |
| :--- | :--- |
| `pm_project` | Registro principal do Projeto |
| `pm_project_task` | Tarefas do Projeto |
| `fm_cost_plan` | Planos de Custo |

> [!IMPORTANT]
> Ao alterar o estado do projeto para "Trabalho em Andamento", as datas reais são preenchidas automaticamente com base nas planejadas se não houver registros prévios.
