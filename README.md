# Sentivis AIOps

## Visão Geral do Projeto

| Item | Descrição |
|------|-----------|
| **Nome do Projeto** | Sentivis AIOps |
| **Plataforma IoT** | ThingsBoard Community Edition |
| **Fase Atual** | Sprint S0 - Fase 1: Validação do Data Backbone |
| **Versão** | 1.0.0-S0 |

## Escopo do Projeto

### O que este projeto valida

- **Validação de backbone de dados** em ThingsBoard CE
- **Fluxo de telemetria** controlado via mock
- **Integração e persistência** de dados time-series
- **Dashboards** para visualização operacional
- **API REST** para automação e configuração

### O que este projeto NÃO valida

- Hardware de campo real (ESP32, LoRa)
- Gateway LoRa
- Validação agronômica
- Implantação em produção
- Piloto comercial

## Fase 1: Mock Telemetry Validation

### Contexto

Esta fase utiliza dispositivos simulados (mock) para validar o fluxo de dados até ThingsBoard. Os dispositivos reais (ESP32 + sensores de solo/clima) serão integrados em fases posteriores.

### Dados Planejados

| Categoria | Métricas |
|-----------|----------|
| **Solo (Soil)** | soil_moisture, soil_temperature |
| **Clima (Climate)** | air_temperature, air_humidity, luminosity, rainfall |
| **Backlog** | atmospheric_pressure, wind_speed, wind_direction |

## Estrutura do Projeto

```
Sentivis SIM/
├── README.md                    # Este arquivo
├── Dev_Tracking.md              # Índice de sprints
├── Dev_Tracking_S0.md           # Sprint ativa
├── docs/
│   ├── SETUP.md                # Pré-requisitos e configuração
│   ├── ARCHITECTURE.md         # Arquitetura da Fase 1
│   ├── DEVELOPMENT.md          # Fluxo de desenvolvimento
│   └── OPERATIONS.md           # Operação e validação
├── rules/
│   └── WORKSPACE_RULES.md      # Regras locais do projeto
├── tests/
│   └── bugs_log.md             # Log de bugs e testes
├── Sprint/                     # Sprints arquivadas
└── Templates/                 # Templates locais
```

## Controle de Sprints

| Sprint | Objetivo | Estado | Link |
|--------|----------|--------|------|
| S0 | Validar data backbone ThingsBoard CE | Em andamento | `Dev_Tracking_S0.md` |

## Documentação de Referência

1. [SETUP.md](docs/SETUP.md) - Pré-requisitos e configuração
2. [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Arquitetura técnica
3. [DEVELOPMENT.md](docs/DEVELOPMENT.md) - Fluxo de desenvolvimento
4. [OPERATIONS.md](docs/OPERATIONS.md) - Operação e manutenção

## ThingsBoard CE

- **URL**: `http://95.217.16.195:8080`
- **Usuário**: `scaixeta@gmail.com` (Tenant Administrator)
- **Dispositivo existente**: `Sentivis | 0001` (default profile, Inactive)

## Notas Importantes

- Este projeto está em **Sprint S0** - Fase de configuração e validação inicial
- Telemetria é gerada por **mock**, não por hardware real
- O objetivo é estabelecer a base para futura integração com ESP32/LoRa
- Toda a documentação está em **Português (pt-BR)**, exceto comandos e APIs

---

## Cindy — Orquestradora (Context Router)

A Cindy é o agente principal do projeto. Em cada run, ela identifica o orchestrator ativo (Cline/Codex/Antigravity), a superfície de execução (VSCode/CLI) e o workspace root; em seguida, descobre e seleciona as skills/workflows disponíveis no contexto atual, respeitando os gates DOC2.5 (plano aprovado antes de execução; commit/push apenas sob ordem explícita do PO).

<p align="center">
  <img src=".brand/Cindy.jpg" alt="Cindy — Orquestradora" width="220" />
</p>

*Versão: 1.0.0-S0 | Última atualização: 2026-03-11 | Modelo: DOC2.5*
