# basic-dashboard-check.md

## Objective
Fazer verificação rápida de dashboard para confirmar visibilidade da telemetria.

## When to use
Após ingestão inicial ou em investigação de visualização.

## Preconditions
- Dashboard existente com widgets conectados ao device.

## Short steps
1. Abrir dashboard alvo.
2. Verificar se widgets carregam sem erro.
3. Conferir atualização de valores recentes.

## Common errors
- Alias de entidade apontando para device errado.
- Widget sem datasource configurado.

## Internal references
- `send-http-telemetry.md`
- `troubleshooting-ingestion.md`

## Out of scope
Design de dashboard e otimização de UX.
