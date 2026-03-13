# validate-attributes.md

## Objective
Verificar presença e consistência de attributes do device.

## When to use
Após criação de device ou ajuste de metadata operacional.

## Preconditions
- Device existente.
- Permissão de leitura no tenant.

## Short steps
1. Abrir detalhe do device.
2. Conferir `Server attributes` e `Shared attributes`.
3. Validar formato esperado das chaves críticas.

## Common errors
- Chave criada no escopo errado.
- Tipo de valor inconsistente.

## Internal references
- `create-device.md`
- `troubleshooting-ingestion.md`

## Out of scope
Modelagem avançada de schema e versionamento de metadata.
