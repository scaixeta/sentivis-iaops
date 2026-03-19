---
name: mcp-builder
description: Criar, revisar ou refatorar servidores MCP, incluindo JSON-RPC 2.0, handshake initialize/initialized, tools/resources, transports stdio ou Streamable HTTP, autenticacao e validacao com inspector. Nao use para criar skills genericas.
---

# Skill: MCP Builder

Use esta skill quando o pedido for criar um servidor MCP novo, refatorar um servidor MCP existente, desenhar ferramentas e recursos MCP, ou estabilizar a compatibilidade de um MCP com clientes como Codex, Cline ou Gemini.

## Objetivo

Entregar um servidor MCP correto, seguro e testavel, com contrato claro entre cliente, ferramentas, recursos e sistemas externos.

## Fluxo

1. Confirmar se MCP e realmente a camada certa:
   - se o problema for apenas criar ou organizar skills, use `skill-authoring`
   - se houver integracao externa acionavel por agente, MCP passa a ser candidato forte
2. Escolher o contorno do servidor:
   - sistemas externos envolvidos
   - ferramentas de acao (`tools/*`)
   - recursos legiveis (`resources/*`)
   - runtime e stack alvo
3. Definir o contrato minimo obrigatorio:
   - `JSON-RPC 2.0`
   - handshake `initialize` seguido de `notifications/initialized`
   - transport `stdio` ou `Streamable HTTP`
4. Projetar as ferramentas:
   - nomes orientados a acao e descoberta
   - schemas claros de entrada e saida
   - erros acionaveis
   - exposicao minima necessaria
5. Projetar os recursos:
   - contexto legivel de alto valor
   - leitura simples, paginacao quando necessario
   - sem devolver volume inutil de dados
6. Implementar com separacao limpa:
   - cliente da API externa
   - auth
   - validacao de input
   - handler MCP
7. Tratar seguranca cedo:
   - auth adequada se remoto
   - validacao de origem e menor privilegio
   - filtro de ferramentas quando houver superficie grande
8. Validar localmente:
   - inspector
   - chamadas reais de `tools/list`, `tools/call`, `resources/list` e `resources/read`
   - smoke test do handshake e do transport
9. Fechar com avaliacao operacional:
   - exemplos reais de uso
   - perguntas de eval
   - checklist final em `references/mcp-design-checklist.md`

## Regras

- Nao use esta skill para criar skills genericas; nesse caso use `skill-authoring`.
- Prefira nomes de ferramentas claros e orientados a verbo.
- Nao exponha tudo por padrao; publique somente o necessario.
- Se o MCP for remoto, trate autenticacao e validacao de token como parte do escopo.
- O servidor nao deve misturar protocolo, regras de negocio e cliente externo no mesmo bloco de codigo.

## Done when

- o handshake `initialize` -> `initialized` funciona
- o transport foi definido e validado
- `tools/list` e `tools/call` funcionam para o caso alvo
- `resources/list` e `resources/read` existem quando o caso pede contexto legivel
- ha estrategia de auth e seguranca compativel com o modo de exposicao
- a validacao local confirma funcionamento minimo e erros acionaveis

## Referencias

- `references/mcp-design-checklist.md`
- `references/server-template.md`
