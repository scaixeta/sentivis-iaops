# Sentivis IAOps

## Visão Geral do Projeto

| Item | Descrição |
|------|-----------|
| **Nome do Projeto** | Sentivis IAOps |
| **Plataforma IoT** | ThingsBoard Community Edition |
| **Fase Atual** | Sprint S2 - Transporte de S0 e S1 para Jira com rastreabilidade completa |
| **Versão** | 1.0.0-S2 |

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
├── Dev_Tracking_SX.md           # Sprint ativa
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
| S0 | Validar data backbone ThingsBoard CE | Encerrada | `Sprint/Dev_Tracking_S0.md` |
| S1 | Estruturar integração Jira Cloud subordinada ao DOC2.5 | Encerrada | `Sprint/Dev_Tracking_S1.md` |
| S2 | Transportar S0 e S1 para Jira com detalhes completos | Em andamento | `Dev_Tracking_S2.md` |

## Camada Jira DOC2.5

A sprint S2 consolidou uma camada de integração Jira para refletir o backlog local no projeto `STVIA`, mantendo `Dev_Tracking_S2.md` como source of truth.

### Arquitetura atual

- Implementação principal em `integrators/jira/`
- Módulos compartilhados em `integrators/common/`
- Wrappers de compatibilidade em `scripts/mgmt_layer_jira.py` e `scripts/mgmt_layer_jira_init.py`
- Estado observado persistido em `.scr/mgmt_layer.jira.json`

### Fluxo operacional

- `bootstrap`: valida credenciais, usuário e projeto Jira
- `status`: mostra o estado observado da integração
- `discover`: atualiza metadados do projeto Jira
- `sync --dry-run`: calcula o delta entre `Dev_Tracking_S2.md` e o Jira sem mutação remota
- `issue dates`: sincroniza datas das issues com timestamps do tracking

### Mapeamento de Datas

O integrator suporta sincronização de datas entre timestamps DOC2.5 e campos Jira:

| Campo Jira | Fonte DOC2.5 | Descrição |
|------------|--------------|-----------|
| Start Date | Timestamp `start` (data) | Data de início do item |
| Data Limite (Due date) | Timestamp `finish` (data) | Data de conclusão do item |

Comando para sincronizar datas:
```bash
python -m integrators.jira issue dates --tracking-file Sprint/Dev_Tracking_S0.md --dry-run
python -m integrators.jira issue dates --tracking-file Sprint/Dev_Tracking_S0.md --yes
```

### Sprints Nativas

O integrator suporta sprints nativas do Jira Software:
- `sprint status`: lista boards e sprints
- `sprint assign`: atribui issues a sprint por label
- `sprint dates`: define datas de início e fim

### Princípios

- `Dev_Tracking_S2.md` é a verdade local (sprint ativa)
- Jira funciona como espelho operacional
- `dry-run` é o modo padrão recomendado antes de qualquer escrita
- A arquitetura `integrators/<provider>/` prepara o repositório para futuros providers

## Documentação de Referência

1. [SETUP.md](docs/SETUP.md) - Pré-requisitos e configuração
2. [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Arquitetura técnica
3. [DEVELOPMENT.md](docs/DEVELOPMENT.md) - Fluxo de desenvolvimento
4. [OPERATIONS.md](docs/OPERATIONS.md) - Operação e manutenção
5. [KB/jira-doc25-workflow-estudo.md](KB/jira-doc25-workflow-estudo.md) - Estudo e decisões da integração Jira

## ThingsBoard CE

- **URL**: `http://95.217.16.195:8080`
- **Usuário**: `scaixeta@gmail.com` (Tenant Administrator)
- **Dispositivo existente**: `Sentivis | 0001` (default profile, Inactive)

## Notas Importantes

- Este projeto está em **Sprint S2** - fase de transporte de S0 e S1 para o Jira com rastreabilidade completa
- A integração Jira já possui arquitetura provider-oriented em `integrators/` com compatibilidade preservada em `scripts/`
- Telemetria é gerada por **mock**, não por hardware real
- O objetivo é estabelecer a base para futura integração com ESP32/LoRa
- A Sprint S0 foi encerrada com o backbone documental e o teste técnico de integração Jira concluídos
- A Sprint S1 foi encerrada com a arquitetura `integrators/` consolidada e documentação canônica atualizada
- Toda a documentação está em **Português (pt-BR)**, exceto comandos e APIs
- Nome oficial do projeto: **Sentivis IAOps**
- `Sentivis SIM` permanece como nome do diretório local de trabalho nesta fase

---

Este repositorio e orquestrado pela Cindy sob a doutrina DOC2.5.

## Cindy — Orquestradora (Context Router)

A Cindy é o agente principal do projeto. Em cada run, ela identifica o orchestrator ativo (Cline/Codex/Antigravity), a superfície de execução (VSCode/CLI) e o workspace root; em seguida, descobre e seleciona as skills/workflows disponíveis no contexto atual, respeitando os gates DOC2.5 (plano aprovado antes de execução; commit/push apenas sob ordem explícita do PO).

<p align="center">
  <img src=".brand/Cindy.jpg" alt="Cindy — Orquestradora" width="220" />
</p>
