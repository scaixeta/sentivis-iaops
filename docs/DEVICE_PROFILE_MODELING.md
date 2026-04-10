# DEVICE & PROFILE MODELING - Sentivis SIM

## 1. Hierarquia de Entidades

```
Tenant (Sentivis)
  +-- Asset Profiles
  |     +-- State, City, Farm, RegionalOffice, Cooperative, OperationalArea
  +-- Device Profiles
  |     +-- SoilSensor, WeatherStation, Gateway, Meter, Actuator
  +-- Assets
  +-- Devices
  +-- Customers
  +-- Relations
  +-- Dashboards
```

## 2. Asset Profiles

| Profile | Uso |
|---|---|
| State | UF do Brasil |
| City | Municipio |
| Farm | Fazenda operacional |
| RegionalOffice | Sede regional |
| Cooperative | Cooperativa |

## 3. Device Profiles

| Profile | Telemetria tipica |
|---|---|
| SoilSensor | humidity, temperature, moisture |
| WeatherStation | temperature, humidity, wind, rain |
| Gateway | status, rssi, uptime |
| Meter | consumption, power, voltage |

## 4. Device Cirrus Lab

| Device | ID | Telemetria |
|---|---|---|
| NIMBUS-AERO 1-09821699 | 27ad32e0 | temperature, humidity, lat/long |
| ATMOS-WIND 1-09821699 | 9c5178a0 | lat/long |
| ATMOS-LINK 1-09821699 | bdda85a0 | lat/long |
| NIMBUS-ECHO-R1 | cbec4881 | lat/long |

## 5. Proximos Passos

- Criar Asset Profiles no ThingsBoard
- Mapear devices Cirrus para assets
- Configurar Entity Views
