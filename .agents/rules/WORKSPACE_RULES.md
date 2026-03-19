# WORKSPACE_RULES.md - Regras Locais do Projeto

## Identificação do Projeto

- **Nome**: Cindy
- **Objetivo**: Base portátil para agentes com governança DOC2.5

## Regras de Governança

### Regra 1: Uma Sprint Ativa por Vez

Apenas um arquivo `Dev_Tracking_SX.md` pode estar ativo na raiz do projeto. Quando uma sprint termina, o arquivo deve ser movido para a pasta `Sprint/`.

### Regra 2: Estrutura Obrigatória do Projeto

O projeto deve seguir a estrutura DOC2.5:

```
Cindy/
├── README.md                 # Entry point oficial
├── Dev_Tracking.md           # Índice de sprints
├── Dev_Tracking_SX.md        # Sprint ativa
├── docs/                     # Documentação canônica
│   ├── SETUP.md
│   ├── ARCHITECTURE.md
│   ├── DEVELOPMENT.md
│   └── OPERATIONS.md
├── rules/                    # Regras locais
│   └── WORKSPACE_RULES.md
├── tests/
│   └── bugs_log.md
└── Sprint/                   # Sprints arquivadas
```

### Regra 3: Ordem Canônica dos 4 Docs

Sequência obrigatória da documentação canônica:
1. **SETUP.md** – preparar ambiente
2. **ARCHITECTURE.md** – entender estrutura
3. **DEVELOPMENT.md** – desenvolver/modificar
4. **OPERATIONS.md** – operar/manter

### Regra 4: Backlog em Tabela Markdown

O backlog em `Dev_Tracking_SX.md` deve usar tabela simples:

```
| Status | Estória |
|---|---|
| To-Do | ST-SX-01 – descrição |
| Done  | ST-SX-02 – descrição |
```

Estados permitidos: To-Do, Doing, Done, Accepted, Pending-SX.

### Regra 5: Formato de Decisões

Decisões devem ser registradas apenas como texto:

```
[D-SX-YY] – descrição da decisão
```

`Hash (UTC)`, impacto e tempos ficam na seção `6. Timestamp UTC`.

### Regra 6: Timestamp UTC (Dev_Tracking)

O `Dev_Tracking` deve conter a seção de timestamp em tabela com **4 colunas**: `Event | Start | Finish | Status`.

Formato canônico do campo de data/hora:
```
DDD  MMDDYYYY  HHMMSS  AM/PM  ST    ← Start
DDD  MMDDYYYY  HHMMSS  AM/PM  FN    ← Finish
```

- `DDD` = dia da semana abreviado em maiúsculas (SUN, MON, TUE, WED, THU, FRI, SAT)
- `MMDDYYYY` = mês, dia e ano colados (ex: `03072026` = 07 de março de 2026)
- `HHMMSS` = horas, minutos e segundos (ex: `023234` = 02h32m34s)
- `AM/PM` = meridiem
- `ST` = sufixo de início / `FN` = sufixo de fim

Exemplo real:
```
## 6. Timestamp UTC
Event | Start | Finish | Status
---|---|---|---
ST-S2-01 | SAT03072026023234PMST | SAT03072026070959PMFN | Done
D-S2-01  | SAT03072026071000PMST | SAT03072026071200PMFN | Logged
```

No `Dev_Tracking.md`, a coluna `Finish` da sprint ativa representa o ultimo carimbo de reconciliacao do indice. Ela nao autoriza encerramento da sprint e nao substitui ordem explicita do PO.

### Regra 7: Política de Leitura Automática

Comandos de leitura são seguros e podem ser executados automaticamente:
- `git status`, `git log`, `git show`, `git branch`
- Leitura de arquivos de documentação
- `python3 scripts/doc25_preflight.py`
- `python3 scripts/doc25_context_check.py --step <etapa>`

### Regra 8: Política de Alteração

Comandos de alteração requerem aprovação prévia do PO:
- `git add`, `git commit`, `git push`
- Criação de novos arquivos ou diretórios
- Instalação de dependências

### Regra 9: Política de Commits

**REGRA ABSOLUTA: Commit apenas com ordem expressa do PO.**

- Nunca sugerir commit
- Nunca executar commit sem autorização textual explícita
- Apresentar planejamento antes de executar
- Mensagem no formato: `SX-XX: descrição` ou `SX-END: resumo`
- Operar em `single remote` por padrao
- Usar `dual remote` apenas quando o PO determinar explicitamente
- Se nao houver remote identificavel no repositorio atual, parar e perguntar antes de commit/push

### Regra 10: Proibição de Credenciais

**REGRA ABSOLUTA: NUNCA expor credenciais em documentação.**

- Secrets em `.env` ou `.scr/.env`
- Nunca versionar arquivos com secrets
- Nunca documentar senhas, tokens ou chaves

### Regra 11: OpenClaw Bridge - Fora do Escopo

**REGRA EXPLÍCITA**: OpenClaw Bridge é integração futura (MVP-3), fora do escopo atual.

- Não configurar dependências do OpenClaw
- Não criar código relacionado ao OpenClaw nesta fase
- Não mencionar como dependência na documentação

### Regra 12: Bootstrap Não Autoriza Implementação

**REGRA EXPLÍCITA**: O bootstrap atual cria estrutura e especificações, mas não autoriza implementação do núcleo.

- Apenas estrutura, documentação e especificações
- Implementação requer nova aprovação do PO
- Próxima etapa: implementação do MVP-1 mediante aprovação

### Regra 13: Proibições DOC2.5

Arquivos de sprint NÃO devem conter:
- Seção "Lições aprendidas"
- Campos "PO AI:" ou "MLE:"
- A palavra "Épico"
- Tabelas complexas fora do padrão `Status | Estória`
- Estruturas teatralizadas de papéis

### Regra 14: Arquivos Proibidos

Não devem existir:
- `docs/README.md` (viola o modelo canônico)
- `docs/INDEX.md` (viola o modelo canônico)
- `ARCHITECTURE_AND_LOGIC.md` (legado)
- `DEPLOYMENT.md` (legado; deve ser `OPERATIONS.md`)

### Regra 15: Rodapé Cindy no README (Root)

O `README.md` (root) deve terminar com:

- a seção `## Cindy — Orquestradora (Context Router)`
- a imagem centralizada via `.brand/Cindy.jpg`
- o texto curto canonico `*Este repositório é orquestrado pela Cindy sob a doutrina DOC2.5, com inteligência centralizada em .agents/.*`

### Regra 16: Gate DOC2.5 de Preflight (Obrigatório)

Antes de alegar conformidade DOC2.5, concluir fase ou reportar "feito", o runtime DEVE:

1. Ler `rules/WORKSPACE_RULES.md` e `.agents/rules` como fontes operacionais obrigatorias
2. Identificar a sprint ativa real na raiz
3. Executar `python3 scripts/doc25_preflight.py`
4. Validar presenca exata de `README.md`, `Dev_Tracking.md`, `Dev_Tracking_SX.md` ativo e `tests/bugs_log.md`
5. Validar presenca exata dos 4 docs canonicos em `docs/`
6. Confirmar ausencia de `docs/README.md` e `docs/INDEX.md`
7. Exigir validacao cruzada entre `README.md`, `Dev_Tracking.md`, `Dev_Tracking_SX.md` e `tests/bugs_log.md`
8. Reforcar que somente o PO pode encerrar sprint

Mensagem de referencia:
`DOC2.5 PREFLIGHT: sprint ativa identificada, artefatos canônicos verificados, gate do PO obrigatório, encerramento de sprint proibido sem ordem explícita, validação cruzada exigida antes da conclusão.`

### Regra 17: Timestamp UTC, Linguagem de Encerramento e Evidencia Minima

- Formato UTC canonico e bloqueante: `DDDMMDDYYYYHHMMSSAM/PMST` ou `DDDMMDDYYYYHHMMSSAM/PMFN`
- O valor deve conter: dia abreviado (`DDD`), `MMDDYYYY`, `HHMMSS`, `AM/PM` e sufixo `ST`/`FN`
- Se o timestamp estiver fora do padrao, a conformidade DOC2.5 nao pode ser alegada
- Linguagem de encerramento prematuro deve ser bloqueada ou sinalizada: `concluded`, `sprint concluded`, `closed`, `finalizada`, `encerrada`, `final state`
- Mudanca estrutural exige ao menos 1 teste estrutural registrado em `tests/bugs_log.md` e resumido no `Dev_Tracking_SX.md` ativo
- Antes do relatorio final, executar passe editorial minimo (typos, nomes de arquivo, mistura PT-BR/EN) e autoauditoria do que mudou, coerencia dos artefatos, riscos de governanca e dependencias do PO

### Regra 18: Projetos Derivados Devem Adaptar Identidade e Contexto

Ao inicializar ou documentar um projeto derivado a partir da Cindy:

- o nome do projeto, objetivo e estrutura raiz devem refletir o projeto de destino
- referencias a `Cindy` so podem permanecer quando se referirem explicitamente ao orchestrator, ao rodape oficial ou ao contrato de orquestracao
- `rules/WORKSPACE_RULES.md`, `README.md`, `Dev_Tracking*.md`, `tests/bugs_log.md`, templates e docs canonicos nao podem declarar o projeto derivado como se fosse a propria Cindy
- placeholders, secoes editoriais soltas e linguagem de encerramento de sprint nao devem permanecer como estado final do bootstrap

### Regra 19: Bootstrap Oficial Deve Usar os Scripts Disponiveis

Quando o objetivo for inicializar um novo projeto DOC2.5 derivado da Cindy:

- o caminho oficial e preferencial e `scripts/init_project.ps1`
- bootstrap manual so e aceitavel como fallback quando o ambiente impedir o uso do script
- se o bootstrap for manual, os artefatos finais devem reproduzir o resultado canonico esperado do script, incluindo rodape completo, tracking inicial e contrato adaptado
- nao alegar "fundacao concluida" se o projeto nao refletir o baseline canonico que os scripts e templates ja definem

## Camada de Gestão (Opcional)

Este módulo é plugável e opcional. Não altera o modelo canônico DOC2.5.
DOC2.5 permanece Source of Truth local.

### Parâmetros (desired-state)

| Parâmetro | Valores possíveis | Valor atual |
|---|---|---|
| `MGMT_LAYER_MODE` | `off \| prompt \| on` | `off` |
| `MGMT_LAYER_TOOL` | `github_projects \| servicenow \| clickup` | `github_projects` |
| `MGMT_LAYER_REF` | `unset \| <url/id>` | `unset` |
| `MGMT_LAYER_SPRINT_FIELD` | nome do campo Sprint no Project | `Sprint` |
| `MGMT_LAYER_STATUS_FIELD` | nome do campo Status no Project | `Status` |
| `MGMT_LAYER_PRIORITY_FIELD` | nome do campo Priority no Project | `Priority` |
| `MGMT_LAYER_AREA_FIELD` | nome do campo Area no Project | `Area` |

### Política de operação

- `off`: nenhuma ação externa é executada.
- `prompt`: Cindy confirma no início da sessão se operará com a camada externa.
- `on`: provisioning e sincronização automáticos.

### Observed-state (gerado, não versionado)

- `.scr/mgmt_layer.github_projects.json` — estado real do Project (IDs, fields, views).
- `.scr/.env` — `GITHUB_TOKEN` (nunca versionado).

### Precedência

- **Source of Truth do "feito"**: `Dev_Tracking_SX.md` ativo (DOC2.5).
- **Source of Truth de "triagem/visibilidade"**: GitHub Project (quando habilitado).
- Mudança de Status no Project → Cindy *propõe* atualização local.
- Conclusão (Done/Accepted) exige registro obrigatório no `Dev_Tracking_SX.md`.

### Scripts do módulo

| Script | Função |
|---|---|
| `scripts/mgmt_layer_init.py` | Lê WORKSPACE_RULES.md, aplica MODE, escreve observed-state |
| `scripts/mgmt_layer_github_projects.py` | `provision` / `sync` / `status` via GitHub GraphQL API |

### Riscos conhecidos

- Permissões insuficientes do `GITHUB_TOKEN` para Projects v2 (scope `project`).
- Divergência de nomes/idioma dos campos no Project.
- `GITHUB_TOKEN` **NUNCA** deve ser versionado — apenas em `.scr/.env`.

---

## Relação com Regras Globais

Este arquivo complementa as regras globais do workspace (`.clinerules/WORKSPACE_RULES_GLOBAL.md`). Em caso de conflito, as regras locais prevalecem para o projeto Cindy.

## Referências

- Template DOC2.5: `.clinerules/templates/doc25/`
- Regras globais: `.clinerules/WORKSPACE_RULES_GLOBAL.md` e `~/.gemini/GEMINI.md`
- Regras de Workspace: `.agents/rules` e `rules/WORKSPACE_RULES.md`
- Skills: `.agents/skills/*/SKILL.md` (e counterparts)
