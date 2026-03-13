# troubleshooting-ingestion.md

## Objective
Guiar diagnóstico rápido quando telemetry não aparece no ThingsBoard.

## When to use
Sempre que houver suspeita de quebra no fluxo de ingestão.

## Preconditions
- Acesso ao device e aos artefatos operacionais mínimos.

## Short steps
1. Validar token do device.
2. Reenviar payload mínimo HTTP de teste.
3. Conferir `Latest telemetry` e timestamps.
4. Checar dashboard e rule engine, se aplicável.

## Common errors
- Token inválido ou expirado.
- Payload com campo ausente em `values`.
- Delay de visualização confundido com falha de ingestão.

## Internal references
- `check-device-token.md`
- `send-http-telemetry.md`
- `rule-engine-first-check.md`

## Out of scope
Troubleshooting de infraestrutura externa ao projeto.
