---
name: servicenow-automation
description: Automação de operações ServiceNow no workspace MCP-Projects com foco em validação de MCP, evidências e conformidade DOC2.5.
---
# ServiceNow Automation

## Quando usar
Usar para tarefas de integração ServiceNow, validação de servidor MCP ServiceNow, coleta de evidências operacionais e troubleshooting inicial.

## Procedimento
1) Validar contexto do projeto em `Servicenow/` e documentação em `Servicenow/docs/`.
2) Confirmar estado do servidor MCP em `Servicenow/mcp/servicenow-server`.
3) Executar smoke checks solicitados pelo PO e registrar evidências em `docs/evidence/`.
4) Para mudanças, limitar ao escopo solicitado e atualizar tracking do projeto correspondente.

## Restrições DOC2.5
- Não sugerir commit/push sem comando explícito do PO.
- Evitar arquivos duplicados; preferir docs canônicos.
- Manter mudanças mínimas e rastreáveis.

## Dependências
- Node.js 18+
- Credenciais ServiceNow em `.scr/.env`
