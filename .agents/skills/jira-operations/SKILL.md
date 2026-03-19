---
name: jira-operations
description: Operar Jira ou Atlassian Jira de ponta a ponta em tarefas de engenharia, produto e operacao, incluindo busca, leitura, triagem, backlog, sprint, boards, comentarios, criacao, edicao, transicoes, labels, dependencias, relatorios e acompanhamento. Nao use para construir servidores MCP; para isso use mcp-builder. Nao altere Jira sem pedido explicito.
---

# Skill: Jira Operations

Use esta skill quando o pedido envolver trabalhar com Jira no dia a dia de entrega, produto, suporte tecnico, coordenacao de sprint, organizacao de backlog ou atualizacao operacional.

## Objetivo

Executar operacoes Jira com clareza, rastreabilidade e minimo risco, cobrindo o dominio operacional completo sem espalhar a logica em varias skills concorrentes.

## Fluxo

1. Identificar o modo de trabalho:
   - leitura e analise
   - triagem e planejamento
   - atualizacao operacional
   - criacao ou refinamento de issue
   - acompanhamento e relatorio
2. Confirmar o contexto minimo:
   - projeto ou board
   - chave da issue, sprint, assignee ou filtro
   - se o pedido e read-only ou mutavel
   - se ha workflow, tipos de issue ou convencoes locais que precisam ser respeitados
3. Escolher a operacao principal:
   - buscar issues
   - ler issue em detalhe
   - listar backlog, sprint ou fila
   - comentar, transicionar, atualizar campos ou criar issue
   - analisar board, dependencias, gargalos ou risco de entrega
   - montar relatorio operacional
4. Resumir o plano antes de qualquer acao com side effect:
   - o que sera lido
   - o que sera alterado
   - o que ficara apenas como sugestao
5. Trazer somente o contexto util:
   - status
   - prioridade
   - assignee
   - labels
   - sprint
   - dependencias
   - comentarios e historico relevantes
6. Ao operar Jira, manter o foco em workflows comuns:
   - triagem de backlog
   - refinamento de issue
   - acompanhamento de sprint
   - registro de comentario tecnico
   - organizacao por labels, prioridades e dependencias
   - mapeamento de bloqueios e relacionamentos
   - consolidacao de status para produto, engenharia ou gestao
7. Se o pedido exigir integracao tecnica nova com Jira, complementar com `mcp-builder` em vez de improvisar protocolo.

## Operacoes Comuns

- localizar issue por chave, texto, projeto, status, sprint, label ou assignee
- ler descricao, comentarios, links, subtarefas e dependencias
- inspecionar boards, sprints, filas e resultados de busca
- resumir uma issue para engenharia, produto ou gestao
- montar fila de triagem e destacar bloqueios
- sugerir proxima acao para backlog ou sprint
- criar issue ou subtarefa bem estruturada
- refinar titulo, descricao, criterios e contexto tecnico
- comentar com contexto objetivo e tecnico
- atualizar status, prioridade, labels, assignee ou campos combinados
- analisar dependencias, impedimentos, aging e risco
- montar relatorio de backlog, sprint, squad ou release
- identificar trabalho parado, mal especificado ou sem dono
- apoiar coordenacao operacional sem executar mutacoes indevidas

## Modos de Operacao

- `read-only`: investigar, resumir e recomendar sem alterar nada
- `guided-update`: propor as mudancas e aguardar aprovacao explicita antes de executar
- `authorized-mutation`: executar criacao, edicao ou transicao somente quando o usuario tiver autorizado de forma clara

## Escopo Coberto

Esta skill deve ser tratada como a skill unica de dominio Jira para a Cindy.

Ela cobre:

- investigacao e leitura
- organizacao de backlog
- acompanhamento de sprint
- refinamento de issue
- comentarios e atualizacoes
- criacao de itens
- relatorios e resumos operacionais
- analise de bloqueios, dependencias e prioridades

Ela nao substitui:

- `skill-authoring`, quando o trabalho for criar skills
- `mcp-builder`, quando o trabalho for construir o servidor MCP ou a integracao tecnica

## Regras

- Nao alterar nada no Jira sem pedido explicito do usuario.
- Quando o pedido for apenas investigar, trabalhar em modo read-only.
- No modo read-only, nao comentar, nao criar, nao transicionar e nao editar nenhum campo.
- Antes de mutacoes, listar claramente quais campos ou issues serao afetados.
- Nao inventar workflow, transicao ou nomenclatura do board sem evidencia.
- Nao usar esta skill para construir MCP; nesse caso usar `mcp-builder`.
- Se o pedido for criar uma skill nova para Jira, usar `skill-authoring`.

## Done when

- o escopo Jira foi entendido com projeto, issue ou filtro suficientes
- a operacao escolhida ficou clara como leitura, triagem ou atualizacao
- o contexto retornado e suficiente sem excesso de ruido
- qualquer mudanca potencial foi explicitada antes da execucao
- o resultado final ajuda a proxima decisao do usuario

## Referencias

- `references/jira-workflows.md`
- `references/capabilities-matrix.md`
- `references/read-only-prompt-template.md`
