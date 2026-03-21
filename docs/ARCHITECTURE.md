# ARCHITECTURE - Sentivis IAOps

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

## Camada de Conhecimento Externo

### Visão Geral

O projeto mantém uma camada local de conhecimento ThingsBoard CE para leitura hierárquica de baixo consumo de tokens.

| Camada | Local | Descrição |
|--------|-------|-----------|
| **Upstream (pending)** | `third_party/thingsboard-ce/upstream/` | Área reservada para futura ingestão oficial |
| **Origem** | `third_party/thingsboard-ce/SOURCES.md` | Estado da fonte e rastreabilidade |
| **Knowledge Layer local** | `knowledge/thingsboard/ce/` | Navegação curta + runbooks + referência curada futura |

### Estrutura de Conhecimento

```
knowledge/thingsboard/ce/
├── manifests/           # Metadados, índice de tópicos e ordem de leitura
│   ├── import_manifest.md
│   ├── mapping_table.csv
│   └── exclusions.md
│   ├── topic_index.md
│   └── reading_priority.md
├── runbooks/            # Guias operacionais curtos (primeira leitura)
├── reference/           # Camada de suporte (futura população)
├── api/                 # Referência API (futura população)
├── user-guide/          # Guias curados (futura população)
└── tutorials/           # Tutoriais curados (futura população)
```

### Políticas de Importação

- **MVP-1**: fundação local concluída.
- **Estado atual**: importação seletiva CE concluída a partir do upstream oficial.
- **Rastreabilidade**: manifestos e `SOURCES.md` atualizados com contagem e source path.
- **Escopo atual**: apenas `reference`, `user-guide` e `tutorials` em markdown.

### Política de Recuperação

- **Objetivo**: minimizar consumo de tokens sem perder precisão operacional.
- **Ordem padrão**: `topic_index.md` -> runbook -> documentação curada local -> upstream oficial.
- **Fallback obrigatório**: quando a IA não souber o que executar, pesquisar primeiro no KB local.
- **Expansão progressiva**: ler somente a próxima camada se a anterior não resolver a tarefa.

### Script de Sincronização

| Script | Local | Propósito |
|--------|-------|-----------|
| `sync_thingsboard_ce.ps1` | `scripts/sync/thingsboard/` | Executar importação seletiva CE a partir de clone local |

## Próximas Fases

1. **Fase 2**: Integração com ESP32 real
2. **Fase 3**: Gateway LoRa
3. **Fase 4**: Alertas e regras advanced

## Camada de Integração Jira

### Visão Geral

O projeto Sentivis IAOps utiliza uma camada de integração com Jira Cloud para sincronização de artefatos de rastreabilidade DOC2.5. Esta camada permite que o backlog local (`Dev_Tracking`) seja refletido no Jira como issues e sprints, mantendo rastreabilidade operacional por labels, reconciliação local e gates de segurança antes de mutações sensíveis. Ela tambem permite refletir no Jira o objetivo de negocio da sprint local por meio do atributo nativo `goal` da entidade Sprint, sem transferir a precedencia do source of truth local.

### Arquitetura de Integração

```
integrators/
├── jira/                    # Provider Jira
│   ├── __init__.py         # Exports públicos
│   ├── __main__.py         # Entry point -m
│   ├── client.py           # Cliente HTTP Jira REST API
│   ├── state.py            # Persistência de estado observado
│   ├── mapper.py           # Mapeamento DOC2.5 -> Jira
│   ├── sync_engine.py      # Engine de sincronização
│   ├── bootstrap.py        # Inicialização e discovery
│   └── cli.py              # Router de comandos
└── common/                  # Módulos compartilhados
    └── doc25_parser.py     # Parser de tracking DOC2.5
```

### Padrão Provider-Oriented

A arquitetura segue um padrão provider-oriented que permite adicionar novos integradores:

| Provider | Local | Status |
|----------|-------|--------|
| Jira | `integrators/jira/` | Implementado |

### Atributos de sprint refletidos no Jira

Quando a sprint local e operada no Jira, o integrador pode refletir:

- `name`
- `startDate`
- `endDate`
- `goal`

O `goal` deve nascer no tracking local como objetivo de negocio / valor para cliente e ser propagado ao Jira apenas como espelho operacional.
| Outros providers | `integrators/<provider>/` | Padrão arquitetural preparado |

**Princípios:**
1. Cada provider vive em `integrators/<provider>/`
2. Lógica compartilhada vai para `integrators/common/`
3. Wrappers em `scripts/` apenas quando necessário para compatibilidade

### Módulos e Responsabilidades

| Módulo | Responsabilidade |
|--------|------------------|
| `client.py` | HTTP client para Jira Cloud REST API v3 |
| `state.py` | Persistência do estado observado em `.scr/mgmt_layer.jira.json` |
| `mapper.py` | Conversão de itens DOC2.5 para payloads Jira |
| `sync_engine.py` | Cálculo de delta e execução de sync |
| `bootstrap.py` | Discovery inicial de projeto, issue types, statuses |
| `cli.py` | Router de comandos CLI |

### Wrappers de Compatibilidade

Os wrappers em `scripts/` mantêm compatibilidade retroativa:

| Wrapper | Delega para | Propósito |
|---------|-------------|-----------|
| `scripts/mgmt_layer_jira.py` | `integrators.jira.cli` | Interface legado |
| `scripts/mgmt_layer_jira_init.py` | `integrators.jira.bootstrap` | Init legado |

### Fluxo de Sincronização

```
Dev_Tracking_SX.md (local)
        |
        v
doc25_parser.py (parse_sprint_backlog)
        |
        v
sync_engine.py (dry_run -> calcula delta)
        |
        v
mapper.py (payloads + estrategia de status)
        |
        v
client.py (POST /rest/api/3/issue)
        |
        v
Jira Cloud (STVIA project)
```

### Estado Observado

O bootstrap persiste um estado observado em `.scr/mgmt_layer.jira.json`:

```json
{
  "connector": "jira",
  "project_key": "STVIA",
  "project_id": "10000",
  "authenticated_user": {
    "account_id": "...",
    "display_name": "Sergio Caixeta"
  },
  "issue_type_map": {"Tarefa": "10003", ...},
  "status_map": {"To-Do": "10000", ...},
  "labels_base": ["doc25", "sentivis"]
}
```

### Decisões de Design

| Decisão | Valor | Motivação |
|---------|-------|-----------|
| Source of Truth | Dev_Tracking_SX.md local | Jira é espelho operacional, não origem |
| Modo Padrão | dry-run | Segurança contra mutation acidental |
| Labels Base | `doc25` + `sentivis` | Identificação de origem |
| Labels de Tipo | `estoria`, `bug`, `change_request` | Contrato operacional da Cindy |
| Rastreabilidade | `tracking_<ID>` | Match estável entre local e Jira |
| Issue Type | `História` para ST; `Tarefa` para BUG/CR | Tipos válidos observados no projeto STVIA |
| Sincronização | Unidirecional (local -> Jira) | Write-back apenas para coluna Jira quando explicitamente usado |

### Mapeamento de Datas (Issue Dates Sync)

O integrator sincroniza timestamps DOC2.5 com campos de data das issues Jira:

| Campo Jira | Fonte DOC2.5 | Formato |
|------------|--------------|---------|
| Start Date (customfield_10015) | Timestamp `start` | YYYY-MM-DD |
| Data Limite (duedate) | Timestamp `finish` ou data da sprint | YYYY-MM-DD |

#### Fluxo de Sincronização

```
Dev_Tracking_SX.md (## 6. Timestamp UTC)
        |
        v
doc25_parser.py (extract_timestamps)
        |
        v
timestamp_to_date (converte ISO8601 para YYYY-MM-DD)
        |
        v
cli.py cmd_issue_dates (compara com valores atuais)
        |
        v
client.py (PUT /rest/api/3/issue/{key})
        |
        v
Jira Cloud (campos Start Date e Due Date atualizados)
```

#### Regras de Reconciliação

1. **Item com finish**: Sincroniza data de início (se start existir) e data limite
2. **Item sem finish**: Ignora (item não concluído no tracking)
3. **Start vazio**: Usa apenas finish para Data Limite
4. **Decisões (D-SX-YY)**: Não sincroniza (não são issues no Jira)
5. **Atribuição ao sprint**: por padrão, a `due date` das issues herda a data final da sprint

### Regras de Sprint Nativa

O integrador local suporta sprints nativas do Jira e aplica as seguintes regras:

| Regra | Comportamento |
|------|----------------|
| Criação sem `end-date` | infere `start-date + 3 dias` |
| Atualização sem `end-date` | infere `start-date + 3 dias` |
| Atribuição ao sprint | replica a data final da sprint para `duedate` das issues |
| Fechamento | passa por gate local antes de chamar a API |

### Estratégia de Status

O integrador não depende apenas de transições diretas.

Quando o tracking local exige mudança de status, o planner:

1. lê a ordem real das colunas do board;
2. calcula o próximo passo natural do item;
3. executa transição passo a passo quando necessário.

Contingencia implementada:

- se o tracking pede `Pendentes`, mas o workflow do Jira não permite retorno completo a essa coluna, o alvo efetivo mínimo passa a ser `Em Progresso`;
- esse fallback é explícito no dry-run.

#### Fallback e Tratamento de Erros

- Se campo não existir no Jira, retorna erro mas continua com outros itens
- Se issue não encontrada por label, registra warning e continua
- Comparação é feita truncando para data (YYYY-MM-DD) para evitar falses positives

## Referências

- `DEVELOPMENT.md` - Fluxo de desenvolvimento
- `OPERATIONS.md` - Operação e manutenção
- `Dev_Tracking_SX.md` - Backlog da sprint ativa
- `scripts/sync/thingsboard/README.md` - Documentação do sync
- `knowledge/thingsboard/ce/manifests/` - Metadados de importação
