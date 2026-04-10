# TELEMETRY CONTRACT - Sentivis SIM

## Proposito

Definir o contrato de telemetria entre a camada de ingestiao e o ThingsBoard CE.

## Payload Canonico

```json
{"temperature": 25.5, "humidity": 60.0, "ts": 1775826691734}
```

| Campo | Tipo | Descricao |
|---|---|---|
| temperature | float | Temperatura em Celsius |
| humidity | float | Humidade relativa em percentagem |
| ts | integer | Timestamp em milissegundos Unix |

## Endpoints

| Plataforma | Endpoint | Metodo |
|---|---|---|
| ThingsBoard CE | `/api/v1/{DEVICE_TOKEN}/telemetry` | POST |
| n8n Webhook | `/webhook/device-telemetry` | POST |

## Validacao

- TEST-S3-T2: Telemetria NIMBUS-AERO confirmada
- TEST-GATE-S3-F0: Gateway ThingsBoard validado
