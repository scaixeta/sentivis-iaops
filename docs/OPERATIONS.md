# OPERATIONS - Sentivis AIOps

## Propósito

Orientar como operar, validar e manter o projeto Sentivis AIOps.

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

Verificar `Dev_Tracking_S0.md` para contexto atual.

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

Atualizar `Dev_Tracking_S0.md` com:
- Timestamp da correção
- Status do bug
- Referência cruzada

## Verificação de Estrutura DOC2.5

Para validar que o projeto está conforme DOC2.5:

```bash
# Verificar arquivos obrigatórios
ls README.md
ls Dev_Tracking.md
ls Dev_Tracking_S0.md
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

## Referências

- `SETUP.md` - Configuração inicial
- `ARCHITECTURE.md` - Arquitetura técnica
- `DEVELOPMENT.md` - Fluxo de desenvolvimento
- `Dev_Tracking_S0.md` - Sprint ativa
- `tests/bugs_log.md` - Log de bugs
