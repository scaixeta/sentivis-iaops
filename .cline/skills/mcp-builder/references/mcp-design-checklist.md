# Checklist de Design MCP

## 1. Contrato Minimo

- Usa `JSON-RPC 2.0`.
- Implementa `initialize` e `notifications/initialized`.
- Define `stdio` ou `Streamable HTTP` de forma explicita.

## 2. Ferramentas

- `tools/list` descreve apenas ferramentas necessarias.
- `tools/call` tem schemas claros de entrada.
- Os nomes sao orientados a descoberta e acao.
- Os erros ajudam o agente a corrigir a chamada.

## 3. Recursos

- `resources/list` existe quando ha contexto legivel relevante.
- `resources/read` devolve contexto util e nao excesso de dados.
- Ha paginacao ou recorte quando o volume puder crescer.

## 4. Seguranca

- O servidor remoto tem estrategia de autenticacao.
- Tokens, issuer, audience e expiram corretamente quando aplicavel.
- Validacao de origem e menor privilegio foram considerados.
- So o necessario foi exposto.

## 5. Validacao

- O inspector conseguiu conectar.
- O handshake passou.
- Ha pelo menos uma chamada real de ferramenta testada.
- Ha pelo menos uma leitura real de recurso testada, se existir recurso.

## 6. Complementaridade

- `skill-authoring` cuida da skill que ensina o workflow.
- `mcp-builder` cuida do servidor MCP em si.
- Se o pedido envolver os dois, usar ambas sem duplicar papel.
