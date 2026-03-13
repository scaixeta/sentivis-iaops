# station-offline-triage.md

## Objective
Conduzir atendimento N1 quando uma estação de um talhão aparecer offline ou em vermelho no dashboard.

## When to use
Quando o cliente reportar que uma estação parou de responder ou que o talhão está marcado como offline.

## Preconditions
- Acesso ao ThingsBoard CE.
- Nome da estação ou identificação do device.
- Credenciais de tenant ou token de teste quando aplicável.

## Short steps
1. Confirmar qual estação ficou offline e desde quando.
2. Abrir o device em `Entities > Devices` e validar `Latest telemetry`.
3. Confirmar `Credentials` do device e revisar possível rotação de token.
4. Reexecutar telemetria mínima de teste, se o contexto permitir.
5. Revisar dashboard para diferenciar falha real de atraso visual ou alias incorreto.

## Recommended response
“Vamos confirmar se a estação realmente parou de enviar telemetria ou se o dashboard ficou desatualizado. Primeiro validamos o device, o token e a última telemetria recebida. Se necessário, executamos um teste mínimo para identificar se a falha está na conectividade, no cadastro ou apenas na visualização.”

## API checks
```bash
# Autenticação administrativa
curl -X POST http://95.217.16.195:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"scaixeta@gmail.com","password":"<senha>"}'

# Busca do device por nome
curl -X GET "http://95.217.16.195:8080/api/tenant/devices?pageSize=100&page=0&textSearch=<nome-da-estacao>" \
  -H "X-Authorization: Bearer <jwt_token>"

# Telemetria mínima de validação
curl -X POST "http://95.217.16.195:8080/api/v1/<device_token>/telemetry" \
  -H "Content-Type: application/json" \
  -d '{"ts": 1741824300000, "values": {"soil_moisture": 45.2, "soil_temperature": 23.1}}'
```

## Read of evidence
- Se a telemetria nova entrar, o problema tende a ser visualização, alias ou regra.
- Se a telemetria não entrar, o problema tende a ser token, conectividade ou estação parada.
- Se o device não aparecer corretamente, o problema pode estar em cadastro ou modelagem.

## Internal references
- `troubleshooting-ingestion.md`
- `check-device-token.md`
- `send-http-telemetry.md`
- `basic-dashboard-check.md`

## Out of scope
Diagnóstico de hardware de campo, gateway LoRa ou causa agronômica.
