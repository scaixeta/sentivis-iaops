---
name: servicenow-zurich-demand-management
description: Skill: ServiceNow Zurich - Demand Management
---

# Skill: ServiceNow Zurich - Demand Management
# Status: DRAFT (Based on Zurich 2025)

## Descrição
Gestão do ciclo de vida de demandas estratégicas e operacionais na Service Now (Zurich). Cobre desde a captura da necessidade até a conversão em projetos ou outros artefatos.

## Ciclo de Vida da Demanda
- **Estados Principais**: Rascunho (Draft) -> Enviado (Submitted) -> Triagem (Screening) -> Qualificado (Qualified) -> Aprovado (Approved) -> Concluído (Completed).
- **Workbench de Demanda**: Ferramenta visual com gráfico de bolha (Risco vs Valor vs Tamanho) para avaliação e seleção.
- **Roadmap**: Visualização 2D/3D das demandas ativas ao longo do tempo.

## Conversão de Artefatos
Dependendo da **Categoria** e **Tipo**, uma demanda aprovada pode ser convertida em:
- **Estratégico**: Projeto, Épico (Agile/SAFe), História, Iniciativa de Melhoria.
- **Operacional**: Mudança (Change), Defeito.

## Gestão Financeira e de Recursos
- **Planos de Custo e Benefícios**: Suporte a moedas múltiplas (Multicurrency).
- **Linhas de Despesa (Expense Lines)**: Registro de gastos reais durante a fase de demanda.
- **Atribuição de Recursos**: Planejamento de esforço e disponibilidade pré-projeto.

## Tabelas Principais
| Tabela | Descrição |
| :--- | :--- |
| `dmn_demand` | Registro principal de Demanda |
| `dmn_demand_task` | Tarefas vinculadas à Demanda |

> [!TIP]
> Use o link relacionado "Criar Projeto" no formulário de demanda para transferir automaticamente planos financeiros e de recursos.
