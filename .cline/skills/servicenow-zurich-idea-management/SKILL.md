---
name: servicenow-zurich-idea-management
description: Skill: ServiceNow Zurich - Idea Management (Innovation Management)
---

# Skill: ServiceNow Zurich - Idea Management (Innovation Management)
# Status: DRAFT (Based on Zurich 2025)

## Descrição
Captura e gestão de ideias via Portal de Ideias (Innovation Management) na Service Now Zurich. Foca na colaboração, votação e triagem inicial de inovações.

## Portal de Ideias
- **Submissão**: Usuários podem enviar ideias, votar e comentar.
- **Colaboração**: Assinatura de ideias para receber notificações de mudanças de estado.
- **Categorias Dinâmicas**: Organização por produtos, departamentos ou unidades de negócio.

## Fluxo de Estados (Zurich)
Novos estados para melhor rastreabilidade:
- Enviado -> Em Análise -> Backlog -> Planejado -> Em Desenvolvimento -> Concluído.
- Estados de rejeição: Implementação improvável, Duplicata, Já existe.

## Inteligência Preditiva (ML)
- **Similar Ideas**: Uso de modelos de semelhança (Semelhança de Solução) para identificar ideias duplicadas ou relacionadas automaticamente durante a submissão.

## Integrações
- **Demand/Project**: Conversão direta de Ideias aceitas em Demandas, Projetos, Épicos ou Histórias.
- **Universal Request**: Criação de ideias a partir de solicitações universais para centralizar a inovação departamental.

## Tabelas Principais
| Tabela | Descrição |
| :--- | :--- |
| `im_idea_core` | Tabela base de Ideias |
| `im_category` | Categorias de Ideia |

> [!IMPORTANT]
> A partir da versão Zurich, os estados são recuperados da tabela `im_idea_core`. Recomenda-se migrar estados customizados da aplicação legada para este novo padrão.
