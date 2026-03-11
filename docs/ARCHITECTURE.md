# ARCHITECTURE - Sentivis AIOps

## Propósito

Descrever como o sistema está organizado em termos de governança, componentes, fluxos e integrações.

## Visão Geral da Arquitetura

### Posicionamento do Projeto

| Camada | Descrição |
|--------|-----------|
| **Coleta** | Sensores (mock na Fase 1) |
| **Transmissão** | LoRa + Gateway (futuro) |
| **Plataforma** | ThingsBoard CE |
| **Visualização** | Dashboards |
| **Automação** | Rule Engine |

### Escopo da Fase 1

- **Validação**: Backbone de dados em ThingsBoard CE
- **Dispositivos**: Mock (simulados)
- **Objetivo**: Estabelecer baseline para integração futura com hardware real

## Componentes Principais

### 1. ThingsBoard CE

| Componente | Descrição |
|------------|-----------|
| **Device Profiles** | Definem comportamento e transport type |
| **Devices** | Entidades que enviam telemetria |
| **Attributes** | Dados estáticos (metadata) |
| **Telemetry** | Dados time-series |
| **Dashboards** | Visualização de dados |
| **Rule Engine** | Processamento de eventos |
| **REST API** | Integração e automação |

### 2. Dispositivos Mock

Na Fase 1, os dispositivos são simulados via scripts:

| Dispositivo | Métricas |
|-------------|----------|
| **Soil Sensor** | soil_moisture, soil_temperature |
| **Climate Sensor** | air_temperature, air_humidity, luminosity, rainfall |

### 3. VS Code como Workstation

- Editor para scripts de mock
- Terminal para chamadas API (curl, HTTP client)
- Controle de versão (Git)
- Documentação

## Fluxos Principais

### Fluxo 1: Ingestão de Telemetria

```
[Mock Script] --> [HTTP POST] --> [ThingsBoard API] --> [Telemetry Storage]
                                    |
                              (Access Token)
```

**Endpoint**: `http://95.217.16.195:8080/api/v1/{device_token}/telemetry`

**Método**: POST

**Headers**:
```
Content-Type: application/json
```

**Body**:
```json
{
  "ts": 1646925123000,
  "values": {
    "temperature": 25.5,
    "humidity": 60.0
  }
}
```

### Fluxo 2: Consulta de Telemetria

```
[Client] --> [REST API] --> [ThingsBoard] --> [Time-series DB]
```

**Endpoint**: `http://95.217.16.195:8080/api/plugins/telemetry/DEVICE/{deviceId}/values/timeseries`

**Autenticação**: Bearer JWT Token

## Decisões Arquiteturais

### D-S0-01: Protocolo de Ingestão

| Decisão | Valor |
|---------|-------|
| Protocolo | HTTP |
| Motivação | Simplicidade para MVP |
| Alternativa | MQTT (para alta frequência) |

### D-S0-02: Autenticação

| Decisão | Valor |
|---------|-------|
| Modelo | Access Token |
| Motivação | ThingsBoard CE default |
| Escopo | Por dispositivo |

### D-S0-03: Estrutura de Dispositivos

| Decisão | Valor |
|---------|-------|
| Padrão | Separado por domínio |
| Soil | `Sentivis | Soil | 001` |
| Climate | `Sentivis | Climate | 001` |

## Contrato de Telemetria

### Payload JSON (Mock)

```json
{
  "device_id": "sentivis-soil-001",
  "timestamp": 1646925123000,
  "metrics": {
    "soil_moisture": 45.2,
    "soil_temperature": 22.5,
    "air_temperature": 25.0,
    "air_humidity": 58.5,
    "luminosity": 450,
    "rainfall": 0.0
  }
}
```

### Keys Definidas

| Categoria | Key | Tipo | Unidade |
|-----------|-----|------|--------|
| Solo | soil_moisture | double | % |
| Solo | soil_temperature | double | °C |
| Clima | air_temperature | double | °C |
| Clima | air_humidity | double | % |
| Clima | luminosity | double | lux |
| Clima | rainfall | double | mm |
| Backlog | atmospheric_pressure | double | hPa |
| Backlog | wind_speed | double | m/s |
| Backlog | wind_direction | double | graus |

## Integrações

### APIs Utilizadas

| API | Endpoint | Propósito |
|-----|----------|----------|
| Auth | `/api/auth/login` | Autenticação JWT |
| Telemetry | `/api/v1/{token}/telemetry` | Ingestão de dados |
| Devices | `/api/device` | Gerenciamento |
| Attributes | `/api/plugins/telemetry` | Consulta |
| Dashboards | `/api/dashboard` | Gerenciamento |

## Limitações da Community Edition

| Feature | CE | PE |
|---------|----|----|
| Multi-tenant | Não | Sim |
| Audit Log | Limitado | Completo |
| RBAC Avançado | Básico | Avançado |
| OTA Updates | Básico | Completo |
| Rule Engine | Standard | Enterprise |

## Próximas Fases

1. **Fase 2**: Integração com ESP32 real
2. **Fase 3**: Gateway LoRa
3. **Fase 4**: Alertas e regras advanced

## Referências

- `DEVELOPMENT.md` - Fluxo de desenvolvimento
- `OPERATIONS.md` - Operação e manutenção
- `Dev_Tracking_S0.md` - Backlog da sprint
