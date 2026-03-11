---
name: e2e-testing-patterns
description: Estratégias E2E para fluxos críticos de MCP-Projects, com foco em estabilidade, diagnóstico de falhas e regressão controlada.
---
# E2E Testing Patterns

## Quando usar
Usar para validar jornadas ponta a ponta e regressões entre integrações (MCP, APIs, UI e automações).

## Procedimento
1) Selecionar cenários críticos de negócio.
2) Definir dados de teste isolados e repetíveis.
3) Executar fluxo completo e coletar logs/evidências.
4) Reportar falhas com causa provável e impacto.

## Restrições DOC2.5
- Evitar cenários frágeis sem valor de negócio.
- Não alterar ambiente sem autorização explícita.
- Commit/push só com ordem do PO.

## Dependências
- Runner E2E do projeto
- Ambiente de execução validado em `docs/OPERATIONS.md`
