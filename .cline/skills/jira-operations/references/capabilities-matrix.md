# Capabilities Matrix

## O que esta skill cobre

- busca por issue, board, sprint, assignee, status, label e texto
- leitura detalhada de issue
- backlog review
- sprint review
- resumo operacional
- criacao de issue
- refinamento de issue
- comentarios
- transicoes
- atualizacao de campos
- mapeamento de bloqueios, links e dependencias

## Modos de seguranca

### Read-only

- permitido: buscar, listar, ler, resumir, analisar
- proibido: criar, editar, comentar, transicionar, atribuir, alterar labels

### Guided-update

- permitido: preparar a mudanca, mostrar o plano e pedir autorizacao
- proibido: executar mutacao antes da autorizacao

### Authorized-mutation

- permitido: executar a mudanca pedida
- obrigatorio: explicitar o alvo e o impacto antes da execucao

## Complementaridade com outras skills

- `jira-operations`: dominio Jira
- `skill-authoring`: criar skills
- `mcp-builder`: criar integracoes MCP
