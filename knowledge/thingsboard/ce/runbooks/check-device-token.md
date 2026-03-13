# check-device-token.md

## Objective
Confirmar que o token do device está correto antes de testes HTTP.

## When to use
Quando houver falha de autenticação na ingestão.

## Preconditions
- Acesso ao detalhe do device na UI.

## Short steps
1. Abrir device em `Entities > Devices`.
2. Ir em `Credentials`.
3. Confirmar tipo e valor do token usado no teste.

## Common errors
- Token copiado com espaço/quebra de linha.
- Token antigo após rotação de credencial.

## Internal references
- `send-http-telemetry.md`
- `rest-api-auth.md`

## Out of scope
Políticas enterprise de segredo centralizado.
