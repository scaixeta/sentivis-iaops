# FR - Gate de Decisao do PO para Fechamento de Sprint no Jira

- Projeto: Sentivis IAOps (Sentivis SIM workspace)
- Artefato: Feature Request (FR)
- Status: Proposto
- Data (UTC): 2026-03-21

## 1. Objetivo

Garantir que qualquer tentativa de fechamento de sprint no Jira passe por um gate explicito de decisao do PO quando existirem condicoes que exijam escolha operacional.

O Jira possui regras proprias para fechamento de sprint, mas essas regras nao substituem a governanca do PO no contexto DOC2.5.

## 2. Problema Observado

Ao concluir uma sprint no Jira, a plataforma pode exigir ou inferir decisoes sobre:

- quais itens contam como concluidos
- quais itens serao tratados como incompletos
- para onde itens incompletos devem ir
- como story points serao contabilizados
- como subtasks abertas afetam o fechamento

Se a Cindy apenas reagir aos prompts do Jira sem interromper para consulta ao PO, existe risco de:

- encerrar sprint com interpretacao errada de entregue vs incompleto
- mover trabalho para destino nao aprovado
- reportar story points de forma inconsistente com a expectativa do PO
- transformar uma validacao tecnica do Jira em decisao operacional sem autorizacao

## 3. Requisito Funcional

Antes de encerrar uma sprint Jira, a Cindy deve obrigatoriamente:

1. identificar a sprint alvo
2. mostrar o board e a ultima coluna mapeada como conclusao
3. listar itens que contam como concluidos
4. listar itens que ficariam incompletos
5. verificar subtasks abertas, quando houver
6. explicar impacto em story points concluidos e carregados
7. perguntar ao PO o destino dos incompletos, se existir qualquer item fora da ultima coluna

## 4. Regra de Decisao

As situacoes abaixo exigem pausa obrigatoria para consulta ao PO:

- existe item fora da ultima coluna do board
- existe item que parece concluido, mas nao esta mapeado para a ultima coluna
- existem subtasks abertas
- o Jira exige definicao de destino para incompletos
- ha ambiguidade sobre backlog, sprint futura ou nova sprint
- ha duvida sobre o que deve contar como entregue na sprint

## 5. Comportamento Esperado da Cindy

Ao detectar qualquer uma dessas condicoes, a Cindy deve responder em linguagem objetiva, por exemplo:

`JIRA SPRINT CLOSE GATE: encontrei itens que nao contam como concluidos na sprint. Preciso da sua decisao, PO, sobre o destino dos incompletos antes de continuar.`

Ela nao deve:

- concluir automaticamente
- assumir backlog como destino padrao
- criar nova sprint sem autorizacao do PO
- interpretar aviso do Jira como autorizacao automatica

## 6. Beneficio Esperado

- governanca mais segura no fechamento de sprint
- menor risco de fechar sprint com leitura errada de concluido
- alinhamento entre Jira, PO e rastreabilidade DOC2.5
- reducao de erros de portfolio e de comunicacao executiva

## 7. Relacao com Regras Locais

Este FR deve ser lido em conjunto com:

- `rules/WORKSPACE_RULES.md`
- especialmente a regra local de gate do PO para fechamento de sprint no Jira

## 8. Criterio de Aceite

O comportamento sera considerado atendido quando:

1. a Cindy interromper qualquer fechamento de sprint Jira diante de condicao decisoria
2. a Cindy pedir decisao explicita do PO antes de concluir
3. a Cindy nao assumir destino de incompletos por conta propria
4. a mensagem de gate ficar clara e reproduzivel
