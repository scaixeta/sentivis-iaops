# DEVELOPMENT - Sentivis IAOps

## Propósito

Descrever como o desenvolvimento deve ser conduzido neste projeto seguindo DOC2.5.

## Princípios

- Uma sprint ativa por vez
- Tracking obrigatório
- Mudança mínima necessária
- Plano antes de execução
- Sem estruturas paralelas fora do modelo canônico

## Estimativas (Fibonacci 1-21) - Padrao Local

Este projeto adota pontuacao em Fibonacci como padrao local do time (Sentivis IAOps) para estimar tamanho/valor do trabalho.

- Escala: `1, 2, 3, 5, 8, 13, 21`
- Calibracao por observacao (fonte de evidencia): `docs/feature_requests/FR-FIBONACCI-VALOR-1-21.md`
- Nota: nao presumir este padrao como regra global para outros workspaces ou times.

Heuristica inicial (ancoras do time):

| Pontos | Regra pratica (resumo) |
|---:|---|
| 1 | Operacao atomica, baixo risco, 1 passo |
| 2 | Pequeno ajuste com 1 verificacao |
| 3 | Mudanca pequena com 2+ passos/arquivos, evidencias minimas |
| 5 | Decisao + ajuste + validacao (moderado) |
| 8 | Integracao/fluxo com superficie maior, chance de retrabalho |
| 13 | Coordenacao/incerteza, preferir decompor se repetivel |
| 21 | Alto risco/abrangencia ou tende a atravessar sprint; fatiamento recomendado |

## Fluxo Geral

### 1. Ler Contexto

Antes de qualquer trabalho:

- `README.md` - Visão geral
- `rules/WORKSPACE_RULES.md` - Regras locais
- `Dev_Tracking.md` - Índice de sprints
- `Dev_Tracking_SX.md` - Sprint ativa
- `tests/bugs_log.md` - Log de bugs

### 2. Planejar

- Resumir entendimento
- Propor plano
- Aguardar aprovação explícita do PO

### 3. Executar

- Atualizar backlog em tabela `Status | SP | Jira | Estória`
- Declarar no tracking o objetivo de negócio / valor para cliente da sprint
- Quando houver sprint nativa no Jira, refletir esse objetivo via `Sprint goal`
- Quando aplicável, preferir `Jira Key` como identificador principal visível da estória, preservando a rastreabilidade local durante a transição
- Aceitar status local em dois modos:
  - modelo DOC2.5 legado (`To-Do`, `Doing`, `Done`, `Pending-SX`)
  - modelo nativo do Jira (`Pendentes`, `Em Progresso`, `Em Testes`, `Feito`, `Bloqueado`, `Backlog`)
- Registrar decisões como `[D-SX-YY]`
- Referenciar bugs e testes em `tests/bugs_log.md`

### 4. Atualizar Rastreabilidade

- Manter `Dev_Tracking_SX.md` coerente
- Atualizar `Dev_Tracking.md` quando necessário
- Sincronizar docs canônicos se a realidade mudou

## Como Trabalhar com Mock Telemetry

### Criar Script de Mock

1. Criar arquivo em `scripts/mock-telemetry.js`

```javascript
// scripts/mock-telemetry.js
const TB_URL = process.env.TB_URL || 'http://95.217.16.195:8080';
const DEVICE_TOKEN = process.env.DEVICE_TOKEN;

function generateSoilData() {
  return {
    ts: Date.now(),
    values: {
      soil_moisture: (Math.random() * 30 + 30).toFixed(2), // 30-60%
      soil_temperature: (Math.random() * 10 + 18).toFixed(2) // 18-28°C
    }
  };
}

function generateClimateData() {
  return {
    ts: Date.now(),
    values: {
      air_temperature: (Math.random() * 10 + 20).toFixed(2), // 20-30°C
      air_humidity: (Math.random() * 40 + 40).toFixed(2),   // 40-80%
      luminosity: Math.floor(Math.random() * 500 + 500),       // 500-1000 lux
      rainfall: (Math.random() * 2).toFixed(2)                // 0-2 mm
    }
  };
}

async function sendTelemetry(data) {
  const response = await fetch(`${TB_URL}/api/v1/${DEVICE_TOKEN}/telemetry`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  return response.json();
}

// Loop a cada 60 segundos
setInterval(async () => {
  const soilData = generateSoilData();
  const climateData = generateClimateData();
  
  console.log('Sending soil data:', soilData);
  console.log('Sending climate data:', climateData);
  
  await sendTelemetry(soilData);
  await sendTelemetry(climateData);
}, 60000);
```

### Executar Mock

```bash
# Definir variável de ambiente
export DEVICE_TOKEN="<device_access_token>"
export TB_URL="http://95.217.16.195:8080"

# Executar
node scripts/mock-telemetry.js
```

## Como Testar APIs

### Usando cURL

```bash
# 1. Autenticar (obter token JWT)
curl -X POST http://95.217.16.195:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"scaixeta@gmail.com","password":"<senha>"}'

# 2. Consultar dispositivos
curl -X GET http://95.217.16.195:8080/api/devices \
  -H "X-Authorization: Bearer <jwt_token>"

# 3. Enviar telemetria (com access token do device)
curl -X POST http://95.217.16.195:8080/api/v1/<device_token>/telemetry \
  -H "Content-Type: application/json" \
  -d '{"ts":1646925123000,"values":{"temperature":25.5,"humidity":60.0}}'
```

### Usando VS Code REST Client

Criar arquivo `.http`:

```http
# authentication.http
@host = http://95.217.16.195:8080
@username = scaixeta@gmail.com
@password = <senha>

### Login
POST {{host}}/api/auth/login
Content-Type: application/json

{
  "username": "{{username}}",
  "password": "{{password}}"
}

### Get Devices
GET {{host}}/api/devices
X-Authorization: Bearer <jwt_token>
```

## Como Validar Payloads

### Estrutura Obrigatória

```json
{
  "ts": 1646925123000,
  "values": {
    "key": value
  }
}
```

- `ts`: Unix timestamp em milissegundos (opcional)
- `values`: Objeto com pares key-value

### Keys Válidas

| Key | Tipo | Descrição |
|-----|------|----------|
| soil_moisture | double | Umidade do solo (%) |
| soil_temperature | double | Temperatura do solo (°C) |
| air_temperature | double | Temperatura do ar (°C) |
| air_humidity | double | Umidade relativa (%) |
| luminosity | double | Luminosidade (lux) |
| rainfall | double | Precipitação (mm) |

## Políticas de Leitura vs Alteração

### Leitura Permitida

- `git status`
- `git log`
- `git show`
- Leitura de arquivos

### Alteração Exige Gate

- `git add`
- `git commit`
- `git push`
- Criação/remoção de arquivos
- Instalação de dependências

## Tests e Bugs

- Log centralizado em `tests/bugs_log.md`
- `Timestamp UTC` nas tabelas de tracking
- `Dev_Tracking_SX.md` recebe resumo e referências cruzadas
- Cada iteração de validação que gere entregável consistente deve virar `TEST-SX-YY` com:
  - escopo
  - resultado
  - evidências (comandos/saída relevante)
  - entregáveis (arquivos afetados)
- Para análises de desempenho do time (consumo), manter `SP` no backlog e registrar snapshots observados em `tests/bugs_log.md` (baseline em `docs/feature_requests/FR-FIBONACCI-VALOR-1-21.md`)

## Workflow: Sincronização de Documentação ThingsBoard

### Quando Usar

Este workflow executa a importação seletiva do ThingsBoard CE para a Knowledge Layer local.

### Pré-requisitos

1. Clone local de `thingsboard.github.io`
2. Execute `git clone https://github.com/thingsboard/thingsboard.github.io.git` em algum diretório

### Executar Preparação

```powershell
# No diretório do projeto
.\scripts\sync\thingsboard\sync_thingsboard_ce.ps1 -SourcePath "C:\caminho\para\thingsboard.github.io"
```

### Preview (Dry Run)

```powershell
.\scripts\sync\thingsboard\sync_thingsboard_ce.ps1 -SourcePath "C:\caminho\para\thingsboard.github.io" -DryRun
```

### O que acontece

1. Valida que `SourcePath` existe.
2. Valida que `ProjectPath` existe.
3. Localiza `_includes/docs/reference`, `_includes/docs/user-guide` e `_includes/docs/tutorials`.
4. Copia apenas arquivos markdown CE para a camada local.
5. Atualiza `SOURCES.md`, `import_manifest.md`, `exclusions.md` e `mapping_table.csv`.

## Política de Uso do KB

Antes de decidir uma ação em ThingsBoard:

1. Consultar `knowledge/thingsboard/ce/manifests/topic_index.md`.
2. Ler o runbook mínimo aplicável.
3. Expandir apenas para `api/`, `user-guide/` ou `tutorials/` se necessário.
4. Se a intenção estiver ambígua ou o próximo passo não estiver claro, pesquisar primeiro no KB local.
5. Usar upstream official docs apenas quando o KB local não cobrir a necessidade.

Critérios:
- Menor consumo de tokens.
- Melhor cobertura operacional.
- Melhor precisão prática para execução.

### Estado após execução

Após execução:
- Conteúdo CE markdown é importado seletivamente.
- `third_party/thingsboard-ce/SOURCES.md` registra source path, commit e contagem.
- `import_manifest.md` e `exclusions.md` registram o estado executado.
- `mapping_table.csv` passa a listar o mapeamento completo importado.

## VS Code como Workstation

### Extensões Recomendadas

| Extensão | Propósito |
|----------|-----------|
| REST Client | Testar APIs |
| Thunder Client | Alternativa ao Postman |
| GitLens | Visualização Git |
| ESLint | Linting |
| Prettier | Formatação |

### Tarefas Úteis

```json
// .vscode/tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run Mock Telemetry",
      "type": "shell",
      "command": "node scripts/mock-telemetry.js",
      "problemMatcher": []
    }
  ]
}
```

## Próximos Passos

1. Executar mock telemetry
2. Validar dados no ThingsBoard
3. Criar dashboard
4. Registrar evidência em `tests/bugs_log.md`
