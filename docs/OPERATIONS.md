# OPERATIONS - Sentivis IAOps

## Propósito

Orientar como operar, validar e manter o projeto Sentivis IAOps.

## Visão Geral de Operação

### Ambiente

| Item | Valor |
|------|-------|
| Plataforma | ThingsBoard CE |
| URL | http://95.217.16.195:8080 |
| Porta HTTP | 8080 |
| Usuário Admin | scaixeta@gmail.com |

### Artefatos que Precisam Permanecer Saudáveis

1. **Dispositivos**: `Sentivis | 0001` (existente), novos devices
2. **Device Profiles**: default e profiles customizados
3. **Dashboards**: Visualizações operacionais
4. **Telemetry**: Dados time-series armazenados
5. **API**: Endpoints REST respondendo

## Rotinas de Teste

### Testes Manuais Mínimos

1. **Validar acesso ThingsBoard**
   - URL: http://95.217.16.195:8080
   - Login com credenciais

2. **Validar dispositivos**
   - Menu: Entidades > Dispositivos
   - Verificar device "Sentivis | 0001"

3. **Validar telemetria**
   - Selecionar device
   - Verificar "Última telemetry"

4. **Validar dashboards**
   - Menu: Dashboards
   - Abrir dashboard criado

### Testes Automatizados

```bash
# Testar API de autenticação
curl -X POST http://95.217.16.195:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"scaixeta@gmail.com","password":"<senha>"}'

# Testar listagem de dispositivos
curl -X GET http://95.217.16.195:8080/api/devices \
  -H "X-Authorization: Bearer <jwt_token>"
```

## Rotinas Operacionais

### Verificar Status do Sistema

1. Acessar ThingsBoard
2. Verificar "API Usage" no menu
3. Confirmar que todos os serviços estão "ENABLED"

### Validar Telemetria Chegando

1. Acessar device details
2. Clicar na aba "Últimos dados"
3. Verificar timestamps recentes

### Inspecionar Histórico

1. Menu: Entidades > Dispositivos
2. Selecionar device
3. Aba "Dados" > "Timeseries"

### Atendimento N1: Estação Offline no Talhão

Quando o cliente informar que um talhão está em vermelho ou que uma estação ficou offline:

1. Confirmar qual estação está afetada e desde quando.
2. Abrir o device correspondente e verificar `Latest telemetry`.
3. Validar `Credentials` do device e possível rotação de token.
4. Se aplicável, reenviar telemetria mínima de teste.
5. Revisar o dashboard para diferenciar falha real de atraso visual, alias incorreto ou regra.

Mensagem recomendada ao cliente:

“Vamos confirmar se a estação realmente parou de enviar telemetria ou se houve apenas perda de atualização no dashboard. Primeiro validamos o device, o token e a última telemetria recebida. Se necessário, executamos um teste mínimo para identificar se a falha está na conectividade, no cadastro ou somente na visualização.”

Comandos de confirmação:

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

Referência KB:
- `knowledge/thingsboard/ce/runbooks/station-offline-triage.md`
- `knowledge/thingsboard/ce/runbooks/troubleshooting-ingestion.md`

## Como Registrar Problemas

1. Documentar em `tests/bugs_log.md`
2. Incluir:
   - Descrição do problema
   - Passos para reproduzir
   - Evidência (prints, logs)
   - Impacto

## Segurança Operacional

### Regras

- Nunca versionar credenciais
- Nunca documentar segredos
- Usar `.scr/.env` para configurações sensíveis
- Mascarar valores sensíveis em documentação

### Credenciais (.scr/.env)

```bash
# ThingsBoard
TB_HOST=95.217.16.195
TB_PORT=8080
TB_URL=http://95.217.16.195:8080
TB_USERNAME=scaixeta@gmail.com
TB_PASSWORD=<obter_do_arquivo_local>
```

## Resposta a Falhas

### 1. Confirmar Contexto da Sprint

Verificar `Dev_Tracking_SX.md` para contexto atual.

### 2. Registrar Bug

Criar entrada em `tests/bugs_log.md`:

```markdown
BUG-S0-01 – Título curto
  - Evidência: [descrição]
  - Impacto: [impacto]
  - Referências: [links]
  - Status: [Open/In Progress]
```

### 3. Corrigir Artefato Mínimo

- Identificar arquivo que precisa correção
- Aplicar mudança mínima necessária
- Testar a correção

### 4. Atualizar Tracking

Atualizar `Dev_Tracking_SX.md` com:
- Timestamp da correção
- Status do bug
- Referência cruzada

## Procedimentos: thingsboard Documentation Sync

### Refresh de Documentação

Para preparar a base local do ThingsBoard Knowledge Layer no MVP-1:

1. **Fornecer source path**: Clone `thingsboard.github.io` localmente
2. **Executar sync**:
   ```powershell
   .\scripts\sync\thingsboard\sync_thingsboard_ce.ps1 -SourcePath "C:\caminho\para\thingsboard.github.io"
   ```
3. **Verificar resultados**:
   - Pastas gerenciadas presentes em `third_party/thingsboard-ce/` e `knowledge/thingsboard/ce/`
   - `SOURCES.md` com status de importação executada
   - Manifestos atualizados com contagem e exclusões aplicadas

### Validação Pós-Execução

1. Verificar que `third_party/thingsboard-ce/SOURCES.md` existe com status executado.
2. Verificar que `knowledge/thingsboard/ce/manifests/import_manifest.md` indica `executed`.
3. Verificar que `knowledge/thingsboard/ce/manifests/exclusions.md` lista as exclusões aplicadas.
4. Verificar que `knowledge/thingsboard/ce/manifests/mapping_table.csv` contém o mapeamento importado.

### Verificação de Atribuição

Para garantir conformidade com licenciamento:

1. Confirmar que não foi criado LICENSE placeholder local.
2. Confirmar que não foi criado NOTICE placeholder local.
3. Confirmar que `SOURCES.md` explicita o source path e o commit utilizados.
4. Confirmar que o escopo segue CE-only e seletivo.

### Rollback (se necessário)

Se algo der errado:
- Reexecutar com `-DryRun` para diagnosticar caminho/escopo.
- Corrigir parâmetros e reexecutar no mesmo escopo gerenciado.
- Não executar ingestão real até source path aprovado pelo PO.

## Verificação de Estrutura DOC2.5

Para validar que o projeto está conforme DOC2.5:

```bash
# Verificar arquivos obrigatórios
ls README.md
ls Dev_Tracking.md
ls Dev_Tracking_S1.md
ls docs/SETUP.md
ls docs/ARCHITECTURE.md
ls docs/DEVELOPMENT.md
ls docs/OPERATIONS.md
ls rules/WORKSPACE_RULES.md
ls tests/bugs_log.md
```

## Manutenção de Disco

### ThingsBoard

- Verificar espaço em disco periodicamente
- Monitorar retention de telemetria
- Limpar dados de teste se necessário

## Checklist Operacional Diário

- [ ] ThingsBoard acessível
- [ ] Login funcionando
- [ ] Dispositivos visíveis
- [ ] Telemetria atualizando
- [ ] Dashboards carregando

## Contato de Suporte

Em caso de problemas com ThingsBoard:
- Consultar documentação oficial
- Verificar logs do servidor
- Reportar via canal apropriado

## Procedimentos: Jira Integration

### Visão Geral

A camada Jira permite sincronizar o backlog DOC2.5 (Dev_Tracking) com o projeto STVIA no Jira Cloud. O Jira funciona como espelho, não como source of truth.

### Configuração de Credenciais

1. Criar arquivo `.scr/.env` na raiz do projeto:
```bash
JIRA_EMAIL=scaixeta@gmail.com
JIRA_API_TOKEN=<token_api_jira>
JIRA_PROJECT_KEY=STVIA
```

2. Nunca versionar este arquivo
3. O token pode ser gerado em: https://id.atlassian.com/manage-profile/security/api-tokens
4. Na implementação atual, o host Jira está parametrizado no cliente da integração e o projeto é definido por `JIRA_PROJECT_KEY`

### Comandos de Operação

#### Bootstrap (Inicialização)

```bash
# Modo dry-run (sem criar arquivos)
python -m integrators.jira bootstrap --dry-run

# Execução real
python -m integrators.jira bootstrap
```

O bootstrap:
1. Valida credenciais via `/rest/api/3/myself`
2. Busca projeto STVIA via `/rest/api/3/project/STVIA`
3. Mapeia issue types disponíveis
4. Mapeia statuses disponíveis
5. Persiste estado em `.scr/mgmt_layer.jira.json`

#### Status (Verificar Estado)

```bash
# Via módulo
python -m integrators.jira status

# Via wrapper legado
python scripts/mgmt_layer_jira.py status
```

Mostra:
- Projeto, ID, tipo
- Usuário autenticado
- Issue types e statuses mapeados
- Última sincronização (fingerprint)

#### Discover (Atualizar Metadados)

```bash
python -m integrators.jira discover
python scripts/mgmt_layer_jira.py discover
```

Atualiza metadados do Jira sem sincronizar backlog.

#### Sync (Sincronizar Backlog)

```bash
# Dry-run: mostra operações sem executar
python -m integrators.jira sync --dry-run
python scripts/mgmt_layer_jira.py sync --dry-run

# Execução real (PEDE CONFIRMAÇÃO)
python -m integrators.jira sync
python scripts/mgmt_layer_jira.py sync
```

O sync:
1. Parseia Dev_Tracking_SX.md (padrão: Dev_Tracking_S1.md)
2. Calcula delta entre local e Jira
3. Cria, atualiza ou remove issues conforme necessário
4. Labels são usadas para rastreabilidade: `doc25`, `sentivis`, `tracking_ST-S1-01`

#### Reconcile (Analisar Divergências)

```bash
python -m integrators.jira reconcile
```

Mostra:
- Itens pendentes (local sem Jira)
- Orphans (Jira sem tracking local)

### Modo Dry-Run

O modo dry-run é o padrão recomendado:
- **NUNCA** cria issues no Jira
- **NUNCA** modifica estado persistido
- Mostra plano de operações
- Safe para executar repetidamente

### Validação de Operação

```bash
# 1. Validar entrada
python -m integrators.jira status

# 2. Verificar sincronização (dry-run)
python -m integrators.jira sync --dry-run

# 3. Analisar divergências
python -m integrators.jira reconcile

# 4. Executar sync real APENAS se necessário
```

### Tratamento de Falhas

| Sintoma | Causa Provável | Solução |
|---------|----------------|---------|
| "Estado não encontrado" | Bootstrap não executado | Executar `bootstrap` primeiro |
| "Credenciais inválidas" | Token expirado ou errado | Regenerar token em id.atlassian.com |
| "Projeto não encontrado" | STVIA não existe ou sem acesso | Verificar permissões |
| Zero issues no Jira | Nenhuma sincronização feita | Executar `sync` |
| ImportError: No module | Path incorreto | Executar da raiz do projeto |

### Limitações Conhecidas

1. **Sem Epic**: STVIA não tem Epic configurado, usa-se "Tarefa"
2. **Sprint nativa**: Implementada via comando `sprint assign` (labels como fallback)
3. **Unidirecional**: Sync local -> Jira apenas (sem write-back)
4. **Labels fixed**: `doc25`, `sentivis`, `tracking_<id>` são fixas

### Sprint Nativo (Comandos)

O integrator agora suporta atribuição de issues a sprints nativos do Jira Software:

```bash
# Verificar boards e sprints
python -m integrators.jira sprint status

# Atribuir issues por label (dry-run)
python -m integrators.jira sprint assign --label sprint_s0 --sprint-name "Sprint S0" --dry-run

# Atribuir issues por label (execução)
python -m integrators.jira sprint assign --label sprint_s0 --sprint-name "Sprint S0" --yes
```

Fluxo:
1. `sprint status` lista boards e sprints existentes com contagem de issues
2. `sprint assign` filtra issues por label (`sprint_s0`, `sprint_s1`, etc.)
3. Atribui issues ao campo Sprint nativo do Jira
4. Labels permanecem como metadata de fallback

Exemplo de mapeamento:
- Label `sprint_s0` → Sprint nativo "Sprint S0"
- Label `sprint_s1` → Sprint nativo "Sprint S1"

### Sprint Dates (Comandos)

O integrator suporta definição de datas de início e fim para sprints nativos:

```bash
# Verificar datas atuais (dry-run)
python -m integrators.jira sprint dates --sprint-name "Sprint S0" --start-date 2026-03-20 --end-date 2026-04-02 --dry-run

# Definir datas do sprint (execução)
python -m integrators.jira sprint dates --sprint-name "Sprint S0" --start-date 2026-03-20 --end-date 2026-04-02 --yes
```

Formato de datas:
- Entrada: `YYYY-MM-DD` (ex: `2026-03-20`)
- Saída (ISO8601 UTC):
  - startDate: `YYYY-MM-DDT00:00:00.000Z`
  - endDate: `YYYY-MM-DDT23:59:59.999Z`

Notas:
- O comando requer `--sprint-name`, `--start-date` e `--end-date`
- O `--yes` pula a confirmação
- O `--dry-run` mostra as datas atuais vs propostas sem mutation
- O Jira Agile API requer `name` e `state` no payload de update

### Issue Dates Sync (Sincronização de Datas de Issues)

O integrator suporta sincronização de datas das issues com os timestamps do tracking DOC2.5.

#### Mapeamento de Campos

| Campo Jira | Fonte DOC2.5 | Descrição |
|------------|--------------|-----------|
| Start Date (customfield_10015) | Timestamp `start` (data) | Data de início do item |
| Data Limite (duedate) | Timestamp `finish` (data) | Data de conclusão do item |

#### Lógica de Sincronização

1. O parser extrai timestamps da seção `## 6. Timestamp UTC` do Dev_Tracking_SX.md
2. Para cada item com timestamp `finish`, busca a issue correspondente no Jira pela label `tracking_<id>`
3. Converte timestamps para datas (YYYY-MM-DD):
   - Start: data do timestamp `start` (se existir)
   - Due: data do timestamp `finish`
4. Compara com valores atuais na issue
5. Atualiza apenas se houver diferença

#### Comando

```bash
# Verificar atualizações planejadas (dry-run)
python -m integrators.jira issue dates --tracking-file Sprint/Dev_Tracking_S0.md --dry-run

# Executar sincronização
python -m integrators.jira issue dates --tracking-file Sprint/Dev_Tracking_S0.md --yes
```

#### Exemplos de Datas Aplicadas

| Tracking ID | Jira Key | Start Date | Due Date |
|------------|----------|------------|----------|
| ST-S0-01 | STVIA-25 | 2026-03-11 | 2026-03-11 |
| ST-S0-02 | STVIA-26 | 2026-03-12 | 2026-03-12 |
| ST-S0-03 | STVIA-45 | 2026-03-13 | 2026-03-13 |

#### Fallback

- Se `start` estiver vazio, usa apenas `finish` para Data Limite
- Se `finish` estiver vazio, ignora o item (não concluído)
- Itens de decisão (D-SX-YY) não são sincronizados (não são issues no Jira)

#### Sprints Reais Aplicadas

| Sprint | Período | Issues Atualizadas |
|--------|---------|-------------------|
| Sprint S0 | 2026-03-10 a 2026-03-13 | 18 (STVIA-25 a STVIA-34, STVIA-27 a STVIA-31) |
| Sprint S1 | 2026-03-13 a 2026-03-20 | 7 (STVIA-35 a STVIA-41) |

#### Warnings Registrados

- **D-S0-XX** (14 itens): Decisões não são sincronizadas (não são issues no Jira)
- **D-S1-XX** (2 itens): Decisões não são sincronizadas
- **TEST-S1-10, TEST-S1-11**: Itens de teste não são sincronizados

#### Status de Atualização

- S0: 18 issues atualizadas com Start Date e Due Date
- S1: 7 issues atualizadas com Start Date e Due Date
- Dry-run subsequente mostra "(vazio) -> data" - comportamento esperado quando timestamp start é nulo (usa finish como fallback)

### Segurança

- **NUNCA** imprimir tokens em logs
- **NUNCA** commitar `.scr/.env`
- **NUNCA** usar credenciais de produção em testes
- Usar `--dry-run` antes de qualquer operação real

## Referências

- `SETUP.md` - Configuração inicial
- `ARCHITECTURE.md` - Arquitetura técnica
- `DEVELOPMENT.md` - Fluxo de desenvolvimento
- `Dev_Tracking_SX.md` - Sprint ativa
- `tests/bugs_log.md` - Log de bugs
- `KB/jira-doc25-workflow-estudo.md` - Workflow de estudo Jira
