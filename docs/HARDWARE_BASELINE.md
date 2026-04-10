# HARDWARE REAL BASELINE - Sentivis SIM

## 1. Fonte: Cirrus Lab

Portal: `https://portal.cirrus-lab.com/`

## 2. Autenticacao

| Campo | Valor |
|---|---|
| Tipo | CUSTOMER_USER |
| Utilizador | contateste@cirruslab.com |
| Issuer | thingsboard.cloud |
| Tenant ID | 2a75a5c0-ba4f-11ee-a124-0d00bef77fcc |
| Customer ID | f23b9a70-1d8e-11f1-88f8-7daa5068de06 |

JWT: `THINGSBOARD_CIRRUS_JWT_Token` em `.scr/.env`

## 3. Devices Cirrus Lab

| Device | ID | Telemetria |
|---|---|---|
| NIMBUS-AERO 1-09821699 | 27ad32e0 | temperature, humidity, lat/long |
| ATMOS-WIND 1-09821699 | 9c5178a0 | lat/long |
| ATMOS-LINK 1-09821699 | bdda85a0 | lat/long |
| NIMBUS-ECHO-R1 0860228052083660 | cbec4881 | lat/long |

## 4. Telemetria NIMBUS-AERO (validada)

```json
{
  "temperature": [{"ts": 1775763452767, "value": "25"}],
  "humidity": [{"ts": 1775828144000, "value": "62.109375"}],
  "latitude": [{"ts": 1775828954460, "value": "-22.59467"}],
  "longitude": [{"ts": 1775828954460, "value": "-48.80054"}]
}
```

## 5. Localizacao

SP, Brasil (-22.59467, -48.80054)

## 6. Proximos Passos

- [ ] Mapear devices Cirrus para assets no ThingsBoard local
- [ ] Configurar fluxo Cirrus -> ThingsBoard local
- [ ] Validar telemetria em dashboard
- [ ] Configurar alarmes
