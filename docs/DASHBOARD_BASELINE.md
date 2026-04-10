# DASHBOARD BASELINE - Sentivis SIM

## 1. Dashboards Operacionais

### 1.1 Dashboard Tenant - Visao Completa Sentivis

- Responsavel: TENANT_ADMIN
- Widgets: cards agregados, mapa territorial, telemetria real-time, alarmes

### 1.2 Dashboard Territorial - Mapa Agronegocio

- Responsavel: TENANT_ADMIN
- Widgets: mapa Brasil, marcadores por tipo, filtros temporais

### 1.3 Dashboard Device - Operacao de Sensores

- Responsavel: TENANT_ADMIN / CUSTOMER_USER
- Widgets: status, telemetria, serie temporal, client attributes

## 2. Dashboards por Perfil

### 2.1 Dashboard Customer - Fazenda

- Entity View: apenas telemetria permitida

### 2.2 Dashboard Cooperative

- Entity View: recorte parcial

## 3. Aliases Recomendados

| Alias | Filtro |
|---|---|
| all_devices | type = Device |
| all_farms | type = Farm |
| devices_by_customer | owner = customer |

## 4. Alarmes Baseline

| Alarme | Condicao | Severidade |
|---|---|---|
| Device Offline | Sem telemetria > 5 min | Critical |
| Temperature High | temperature > 40C | Warning |
| Temperature Low | temperature < 5C | Warning |
| Humidity Low | humidity < 20% | Critical |

## 5. Baseline Actual

Device `Sentivis | 0001` existente. Dashboard operacional pendente de implementacao.
