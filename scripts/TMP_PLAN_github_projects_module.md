# Plano Temporário — Módulo “Camada de Gestão” (GitHub Projects) — Sentivis AIOps

PO: Sergio  
Projeto: Sentivis AIOps  
Idioma: PT-BR (comandos/paths em inglês)  
Modo: Absoluto  
Workflow: Planning → Approval → Execution  

## 0) Objetivo

Adicionar ao projeto um **módulo opcional** de “Camada de Gestão” usando **GitHub Projects (Projects v2)** como organizador central (backlog/status/prioridade/sprint), **sem alterar o modelo canônico DOC2.5** da Cindy. A ativação/desativação e o “prompt” de inicialização serão definidos em `rules/WORKSPACE_RULES.md`.

Requisito-chave: quando ativado, o módulo deve ser **automaticamente configurado/provisionado** via Cindy (criar/descobrir Project, campos e views; vincular items), e **registrar rastreabilidade** nos artefatos DOC2.5.

## 1) Princípios / Guardrails (não negociáveis)

1. **DOC2.5 permanece Source of Truth local**: `README.md`, `docs/*`, `Dev_Tracking_SX.md`, `tests/bugs_log.md`.
2. **Camada externa é opcional e “plugável”** (GitHub Projects / ServiceNow / outra).
3. **Sem segredos versionados**: token GitHub fica em `.scr/.env` (ou cred store), nunca em `rules/`/docs.
4. **Automação não reescreve governança**: qualquer ajuste em `rules/WORKSPACE_RULES.md` deve ser *proposto e confirmado* (gate) se implicar alteração.
5. **Sem dependência de `gh` CLI** (hoje não existe no ambiente): a automação deve suportar fallback via `curl`/Python + GitHub API.

## 2) Estado atual (e gaps)

- Repo Git existe (`.git/`), remote `origin` no GitHub, branch `main`.
- Artefatos DOC2.5 canônicos existem: `README.md`, `docs/*`, `Dev_Tracking.md`, `Dev_Tracking_S0.md`, `tests/bugs_log.md`, `rules/WORKSPACE_RULES.md`.
- Gaps relevantes para o módulo:
  - `Sprint/` ausente (obrigatório pelo workflow DOC2.5).
  - `.github/` ausente (workflows, issue templates, PR template).
  - `gh` CLI ausente (automação deve ser via API).

## 3) “Camada de Gestão” como módulo (design)

### 3.1 Parâmetros de inicialização (definidos em `rules/WORKSPACE_RULES.md`)

Adicionar uma seção (curta) com valores declarativos:

- `MGMT_LAYER_MODE`: `off | prompt | on`
- `MGMT_LAYER_TOOL`: `github_projects | servicenow | clickup`
- `MGMT_LAYER_REF`: `unset | <url/id>` (sem segredos)
- `MGMT_LAYER_SPRINT_FIELD`: nome do campo Sprint no Project (ex.: `Sprint`)
- `MGMT_LAYER_STATUS_FIELD`: normalmente `Status` (Projects v2)
- `MGMT_LAYER_PRIORITY_FIELD`: ex.: `Priority`
- `MGMT_LAYER_AREA_FIELD`: ex.: `Area`

Regra: `prompt` obriga a Cindy a confirmar no início da sessão se vai operar com a camada externa **nesta sessão**.

### 3.2 Observed-state (onde salvar o que foi “auto-configurado”)

Para evitar “churn” em `rules/WORKSPACE_RULES.md`, o módulo registra o resultado do provisioning em:

- `Dev_Tracking_SX.md`: decisão `[D-SX-YY]` com Project URL/ID e campos criados/validados.
- Arquivo local **não versionado** em `.scr/` (ex.: `.scr/mgmt_layer.github_projects.json`) contendo:
  - `project_id`, `project_url`, ids dos fields, views, etc.

`MGMT_LAYER_REF` pode permanecer `unset` (desired-state) ou ser atualizado **somente** via patch aprovado.

## 4) Arquitetura MVP de operação

### 4.1 Fluxo operacional (alto nível)

1. Cindy lê `rules/WORKSPACE_RULES.md`.
2. Se `MGMT_LAYER_MODE=off`: não faz nada externo.
3. Se `MGMT_LAYER_MODE=prompt`: Cindy pergunta e registra decisão em `Dev_Tracking_SX.md`.
4. Se habilitado (`on` ou `prompt` confirmado):
   - Provisiona/descobre o GitHub Project (v2) e valida campos/views mínimos.
   - Cria/atualiza issues para ST/BUG/TEST (quando aplicável) e adiciona ao Project.
   - Sincroniza `Status/Sprint/Priority/Area` entre Project ↔ Dev_Tracking (regras claras de precedência).
   - Registra evidências em `Dev_Tracking_SX.md` e mantém `tests/bugs_log.md` como log central.

### 4.2 Precedência (regras de sincronização)

- **Fonte primária do “feito”**: `Dev_Tracking_SX.md` (DOC2.5).
- **Fonte primária de “triagem/visibilidade”**: GitHub Project (quando habilitado).
- Regra prática:
  - Mudança de status em Project → Cindy *propõe* atualização do backlog local (ou atualiza se o PO autorizou escrita).
  - Conclusão real (Done/Accepted) exige registro no `Dev_Tracking_SX.md`.

## 5) Viabilidade imediata (GitHub Projects)

Sim, é possível automatizar:
- Projects v2 expõem operações via **GitHub GraphQL API** (criar project, criar campos, adicionar itens, setar valores).
- Dependências mínimas:
  - `GITHUB_TOKEN` com permissões adequadas (repo + project do user/org).
  - Identificador do owner (user/org) para localizar/criar o Project.

Limitação atual: sem `gh` CLI, a automação será via Python/`curl`. É viável no curto prazo.

## 6) Plano de implementação (numerado)

### Fase 1 — Preparação e governança (local)
1. Atualizar `rules/WORKSPACE_RULES.md` para incluir seção “Camada de Gestão (Opcional)” com parâmetros acima.
2. Definir política para `.scr/`:
   - `.scr/.env` com `GITHUB_TOKEN` (local, não versionado).
   - `.scr/mgmt_layer.github_projects.json` como estado observado (não versionado).
3. Garantir `Sprint/` (estrutura DOC2.5) e política de arquivamento de sprint.

**Artefatos afetados (fase 1):**
- `rules/WORKSPACE_RULES.md`
- `.scr/.env` (local)
- `Sprint/` (diretório)

**Impacto:** habilita o “switch” e prepara rastreabilidade de provisioning.

### Fase 2 — Implementar o módulo (scripts)
4. Criar script `scripts/mgmt_layer_github_projects.py` com comandos:
   - `provision`: cria/descobre Project + campos + views mínimas.
   - `sync`: sincroniza items (issues) ↔ backlog (Dev_Tracking).
   - `status`: imprime estado atual e valida configuração.
5. Criar script `scripts/mgmt_layer_init.py` (ou integrar no anterior) que:
   - lê `rules/WORKSPACE_RULES.md` (somente a seção do módulo),
   - aplica `MGMT_LAYER_MODE` (off/prompt/on),
   - escreve `.scr/mgmt_layer.github_projects.json`,
   - registra `[D-SX-YY]` em `Dev_Tracking_SX.md` (append-only).

**Artefatos afetados (fase 2):**
- `scripts/mgmt_layer_github_projects.py`
- `scripts/mgmt_layer_init.py` (opcional)
- `.scr/mgmt_layer.github_projects.json` (gerado)
- `Dev_Tracking_S0.md` (registro de decisão)

**Impacto:** provisioning automático e base para sincronização.

### Fase 3 — Padronização de trabalho (Issues/PRs)
6. Criar `.github/ISSUE_TEMPLATE/` com templates:
   - `story.yml` (ST-SX-YY)
   - `bug.yml` (BUG-SX-YY)
   - `test.yml` (TEST-SX-YY)
7. Criar `.github/pull_request_template.md` incluindo:
   - referência a Issue/Project item
   - checklist DOC2.5 (Dev_Tracking atualizado, tests/bugs_log atualizado)

**Artefatos afetados (fase 3):**
- `.github/ISSUE_TEMPLATE/*`
- `.github/pull_request_template.md`

**Impacto:** fluxo consistente entre Project ↔ repo ↔ DOC2.5.

### Fase 4 — MVP de automação CI (opcional, mínima)
8. Adicionar workflow em `.github/workflows/ci.yml` (lint/test/build) sem deploy.

**Artefatos afetados (fase 4):**
- `.github/workflows/ci.yml`

### Fase 5 — Validação e critérios de sucesso
9. Validar provisioning em dry-run (sem criar nada) e depois provisioning real (com aprovação do PO).
10. Validar um ciclo completo:
   - criar 1 Issue “ST-S0-02”
   - adicionar ao Project
   - mover Status no board
   - refletir em `Dev_Tracking_S0.md` (ou registrar proposta)
11. Registrar evidência no `Dev_Tracking_S0.md` e manter `tests/bugs_log.md` coerente.

## 7) Estratégia de validação

- Local:
  - `scripts/audit_doc25.ps1` (estrutura DOC2.5)
  - `scripts/mgmt_layer_github_projects.py status` (config OK)
- Remoto (GitHub):
  - Project criado/descoberto com campos/views esperadas
  - Item de Issue aparece no Project e aceita mudança de Status/Sprint/Priority/Area

## 8) Riscos e dependências

- Permissões insuficientes do `GITHUB_TOKEN` para Projects v2 (owner user vs org).
- Divergência de nomes/idioma dos campos (padronizar nomes e mapear).
- Conflitos de precedência (Project vs Dev_Tracking) se não houver regra clara.
- Ausência de `Sprint/` hoje pode quebrar auditoria/ritual de encerramento.

## 9) Checkpoints DOC2.5

- Manter `docs/` com apenas os 4 docs canônicos.
- Atualizar `Dev_Tracking_S0.md` (append-only) para decisões sobre ativação e provisioning.
- Atualizar `tests/bugs_log.md` quando houver testes/bugs do módulo.
- Commit/push somente quando o PO ordenar e confirmar (workflow `commit-doc25`).

## 10) Pergunta de aprovação (gate)

Você aprova este plano para execução?
- Sim, execute o plano
- Não, cancele ou ajuste

