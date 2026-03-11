---
description: Guia de Desenvolvimento de Servidores MCP (Anthropic Protocol)
---

# MCP Builder Skill

## Overview
Use esta skill para orientar a construção e refinamento de servidores Model Context Protocol (MCP). Seu objetivo é capacitar LLMs a interagir com serviços externos por meio de ferramentas bem desenhadas, combinando endpoints de APIs robustos com fluxos de trabalho especializados.

## Fases de Desenvolvimento MCP

### Fase 1: Pesquisa e Planejamento (Deep Research)
- **API Coverage vs. Workflow Tools:** Balanceie a cobertura de API (crucial para flexibilidade) com ferramentas de workflow (tarefas específicas). Na dúvida, priorize a cobertura ampla de API.
- **Nomenclatura (Discoverability):** Use nomes claros e orientados à ação (ex: `github_create_issue`, `github_list_repos`). Padronize os prefixos.
- **Management de Contexto:** Devolva apenas os dados relevantes. Use paginação e descrições concisas.
- **Pilha Recomendada (Tech Stack):** TypeScript (SDK completo) ou Python (FastMCP). Prefira HTTP Streamable ou Stdio para servidores locais (JSON stateless).

### Fase 2: Implementação
- **Estruturação:** Estabeleça utilitários como `API Client com auth`, tratamento de erro e paginação.
- **Input/Output Schema:** Use Zod (TypeScript) ou Pydantic (Python).
  - Inclua limites explícitos e descrições textuais nos inputs.
  - O Output deve retornar `structuredContent` junto com o texto para os clientes MCP formatarem o dado.
- **Erros:** Devolva mensagens que orientem o agente com próximos passos de correção ("actionable error messages").

### Fase 3: Code Review e Testes
- **Inspector:** Use `npx @modelcontextprotocol/inspector` ou `mcp-inspector` (Python) para testar os endpoints localmente antes do deploy.
- **Code Quality:** Garanta tipagem completa (TypeScript) e ausência de código duplicado (DRY).

### Fase 4: Avaliação (Evaluations / Evals)
Defina até 10 questões realistas, focadas e verificáveis, para avaliar se um LLM seria capaz de usar suas ferramentas de forma autônoma para resolver a demanda. Idealmente, cada questão deve forçar o acesso "Read-Only" e complexo de múltiplas chamadas de ferramentas.

## Referências Úteis
- Sitemap: `https://modelcontextprotocol.io/sitemap.xml`
- Especificação atual: `https://modelcontextprotocol.io/specification/draft.md`
