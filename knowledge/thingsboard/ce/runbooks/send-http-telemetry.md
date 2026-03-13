# send-http-telemetry.md

## Objective
Validar ingestão de telemetria via endpoint HTTP do device token.

## When to use
Quando o time precisa confirmar fluxo mínimo `device -> telemetry storage`.

## Preconditions
- Device token válido.
- Endpoint HTTP acessível.

## Short steps
1. Montar payload JSON com `ts` e `values`.
2. Fazer `POST /api/v1/{deviceToken}/telemetry`.
3. Verificar atualização em `Latest telemetry` do device.

## Common errors
- `401` por token inválido.
- Payload fora do formato aceito.

## Internal references
- `check-device-token.md`
- `validate-attributes.md`

## Out of scope
Benchmark de throughput e tuning de retenção.
