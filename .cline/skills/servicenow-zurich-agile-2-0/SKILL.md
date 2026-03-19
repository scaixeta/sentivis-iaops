---
name: servicenow-zurich-agile-2-0
description: Skill: ServiceNow Zurich - Agile Development 2.0
---

# Skill: ServiceNow Zurich - Agile Development 2.0
# Status: DRAFT (Based on Zurich 2025)

## Descrição
Referência técnica para o módulo Agile Development 2.0 da Service Now (versão Zurich). Foca na gestão de Sprints, Backlogs unificados e transição do modelo 1.0.

## Estrutura de Modelos de Dados
- **Grupos de Atribuição (Assignment Groups)**: Substituem a antiga entidade "Release Team" do Agile 1.0. Devem possuir o tipo `Equipe ágil`.
- **Sprints**: Vinculados a Grupos de Atribuição (e não obrigatoriamente a uma Release), permitindo backlogs contínuos.
- **Histórias (Stories)**: Entidades fundamentais associadas a Sprints e Épicos.

## Fluxos Operacionais
### Gestão de Backlog
- Suporte a **Backlog Unificado**: Permite priorizar histórias, defeitos, incidentes e problemas em uma única fila.
- **Épicos**: Agrupam histórias relacionadas sob um objetivo comercial comum.

### Planejamento de Sprint
- **Burndown Chart**: Monitoramento de progresso por pontos de história.
- **Velocity**: Cálculo automático da capacidade da equipe baseado no histórico de conclusão.

## Migração (1.0 para 2.0)
- **Script de Diagnóstico**: `Agile_2_0_Upgrade_Diagnostics`.
- **Conversão de Equipes**: Processo síncrono para converter equipes clássicas em grupos de atribuição ágeis.

## Tabelas Principais
| Tabela | Descrição |
| :--- | :--- |
| `rm_story` | Histórias de Usuário |
| `rm_sprint` | Ciclos de Sprint |
| `rm_epic` | Épicos do Projeto |
| `rm_backlog` | Definições de Backlog |

> [!NOTE]
> Esta skill é baseada na documentação "Strategic Portfolio Management Zurich" (Nov/2025).
