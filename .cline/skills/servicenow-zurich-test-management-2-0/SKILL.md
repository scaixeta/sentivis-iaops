---
name: servicenow-zurich-test-management-2-0
description: Skill: ServiceNow Zurich - Test Management 2.0
---

# Skill: ServiceNow Zurich - Test Management 2.0
# Status: DRAFT (Based on Zurich 2025)

## Descrição
Gestão de testes de software e sistemas na Service Now Zurich. Melhora a qualidade das entregas integrando-se diretamente com o ciclo de vida de Projetos e Agile.

## Estrutura de Teste
- **Plano de Teste (Test Plan)**: Define o escopo, cronograma e ambiente para o ciclo de teste.
- **Versão de Teste (Test Build)**: Representa uma versão específica do software sendo testada.
- **Ciclo de Teste (Test Cycle)**: Agrupa execuções de teste em janelas temporais específicas.

## Execução e Defeitos
- **Caso de Teste (Test Case)**: Descrição dos passos, dados e resultados esperados.
- **Execução de Teste (Test Run)**: Instância de execução de um caso de teste (Passou, Falhou, Bloqueado).
- **Gestão de Defeitos**: Integração nativa para criação de registros de defeito a partir de falhas identificadas durante a execução.

## Integrações
- **Project Management**: Criação de fases de teste dentro de projetos Waterfall ou Híbridos.
- **Agile 2.0**: Associação de testes a Histórias de Usuário ou Sprints.

## Tabelas Principais
| Tabela | Descrição |
| :--- | :--- |
| `sn_test_management_test_plan` | Planos de Teste |
| `sn_test_management_test_case` | Casos de Teste |
| `sn_test_management_test_run` | Resultados de Execução |

> [!TIP]
> Use a barra de progresso no Plano de Teste para monitorar em tempo real a cobertura e os resultados de aprovação dos ciclos ativos.
