# Estudo - Workflow Alternativo Jira Cloud + DOC2.5 + Cindy

## 1. Objetivo

Definir como o projeto pode operar com uma camada externa Jira Cloud sem quebrar o modelo canônico DOC2.5, mantendo a Cindy como orquestradora e o `Dev_Tracking_SX.md` como fonte primária de verdade local.

Meta operacional:

- permitir que a equipe trabalhe no fluxo DOC2.5 normal;
- refletir o estado operacional no Jira;
- permitir que atualizações de sprint no tracking local atualizem o Jira de forma controlada;
- evitar duplicidade de governança entre workspace e ferramenta externa.

## 2. Premissas e Guardrails

### 2.1 Fonte primária de verdade

O modelo oficial continua sendo local:

- `README.md`
- `docs/SETUP.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT.md`
- `docs/OPERATIONS.md`
- `Dev_Tracking.md`
- `Dev_Tracking_SX.md`
- `tests/bugs_log.md`

O Jira passa a ser camada externa de gestão e visibilidade, nunca substituto do DOC2.5.

### 2.2 Guardrails obrigatórios

- Nenhum segredo pode ser versionado.
- Credenciais Jira permanecem em `.scr/.env`.
- O `Dev_Tracking_SX.md` continua sendo o gate do "feito".
- Mudanças no Jira não podem invalidar o tracking local.
- Conclusão real de estória exige registro no tracking local.
- A Cindy só opera a camada Jira quando o modo estiver habilitado.

### 2.3 Papel da Cindy

A Cindy atua como roteadora de contexto:

- lê regras do workspace;
- identifica se a camada Jira está desativada, condicionada ou ativa;
- executa ou propõe sincronizações;
- preserva os gates DOC2.5 de plano, escrita e rastreabilidade.

## 3. Operações Jira Cloud Confirmadas

Com base nos testes realizados, as seguintes operações estão confirmadas para o projeto `STVIA`.

### 3.1 Autenticação e contexto do usuário

| Operação | Endpoint | Uso no workflow |
|---|---|---|
| GET `myself` | `/rest/api/3/myself` | validar credenciais, descobrir `accountId`, validar contexto do operador |

### 3.2 Projetos

| Operação | Endpoint | Uso no workflow |
|---|---|---|
| GET `project/{key}` | `/rest/api/3/project/STVIA` | validar projeto alvo, tipos de issue, roles e metadados |
| GET `project` | `/rest/api/3/project` | descobrir projetos acessíveis e validar chave correta |

### 3.3 Issues

| Operação | Endpoint | Uso no workflow |
|---|---|---|
| GET `search/jql` | `/rest/api/3/search/jql` | localizar issues por sprint, status, labels, tipo e chaves DOC2.5 |
| GET `issue/{id}` | `/rest/api/3/issue/STVIA-1` | ler issue detalhada antes de decidir update |
| POST `issue` | `/rest/api/3/issue` | criar issue a partir de estória, bug ou teste do tracking |
| PUT `issue/{id}` | `/rest/api/3/issue/{id}` | atualizar resumo, descrição, labels, prioridade, due date, componentes |
| DELETE `issue/{id}` | `/rest/api/3/issue/{id}` | uso administrativo e excepcional |
| POST `issue/{id}/comment` | `/rest/api/3/issue/{id}/comment` | anexar evidência, contexto de sprint e comentários de operação |

Campos suportados já observados:

- `summary`
- `description`
- `priority`
- `status`
- `assignee`
- `duedate`
- `labels`
- `components`

### 3.4 Workflow e transições

| Operação | Endpoint | Uso no workflow |
|---|---|---|
| GET `issue/{id}/transitions` | `/rest/api/3/issue/{id}/transitions` | validar transições permitidas antes de sincronizar status |
| POST `issue/{id}/transitions` | `/rest/api/3/issue/{id}/transitions` | mover issue entre estados do fluxo Jira |

### 3.5 Boards e sprints

| Operação | Endpoint | Observação |
|---|---|---|
| GET `board` | `/rest/api/3/board` | suporte limitado |
| GET `board/{id}/sprint` | `/rest/api/3/board/{id}/sprint` | suporte limitado |

Limite operacional atual:

- o projeto `STVIA` foi descrito como "Next-Gen";
- não devemos depender de boards/sprints tradicionais como pivô da integração;
- o vínculo de sprint deve ser modelado principalmente por campos locais do DOC2.5 e, se necessário, por `labels`, `components` ou campos Jira validados.

## 4. Cruzamento entre Jira e Dev_Tracking

## 4.1 Entidades DOC2.5 relevantes

O `Dev_Tracking_SX.md` hoje carrega quatro blocos úteis para sincronização:

| Bloco DOC2.5 | Papel | Reflexo Jira recomendado |
|---|---|---|
| Objetivos da sprint | direção e escopo | comentário de contexto ou epic lógico |
| Backlog `Status | Estória` | trabalho operacional | issues Jira |
| Decisões `[D-SX-YY]` | governança e arquitetura | comentários em issues ou issue específica de decisão |
| Timestamp UTC | rastreabilidade temporal | comentário, due date, auditoria, ou campo auxiliar |

## 4.2 Mapeamento sugerido

### Backlog de estórias

| Dev_Tracking | Jira |
|---|---|
| `ST-S0-18` | chave lógica no `summary`, `description` e `labels` |
| texto da estória | `summary` |
| contexto detalhado | `description` |
| `To-Do`, `Doing`, `Done` | status Jira equivalente |
| sprint `S0` | `label` `sprint:S0` ou componente `Sprint-S0` |
| tipo implícito `ST` | `issueType` Task ou Story |

### Bugs

| DOC2.5 | Jira |
|---|---|
| `BUG-S0-XX` | issue type Bug |
| status no log | status Jira |
| evidência | comentário |
| impacto | descrição |

### Testes

| DOC2.5 | Jira |
|---|---|
| `TEST-S0-XX` | Task, Subtask ou issue type custom se existir |
| resultado de validação | comentário |
| referência cruzada | label e descrição |

### Decisões

As decisões `[D-SX-YY]` não devem virar issue automaticamente por padrão. Melhor estratégia:

- registrar a decisão no `Dev_Tracking_SX.md` primeiro;
- refletir no Jira como comentário na issue impactada;
- criar issue dedicada somente quando a decisão gerar trabalho rastreável.

## 4.3 Campos auxiliares recomendados no Jira

Para manter o vínculo entre DOC2.5 e Jira, o mínimo recomendado é:

- label `doc25`
- label `sentivis`
- label `sprint:S0`
- label com identificador lógico, por exemplo `tracking:ST-S0-18`
- componente opcional por área funcional

Se houver campo customizado disponível, o ideal é adicionar:

- `DOC25 Tracking ID`
- `DOC25 Sprint`
- `DOC25 Source`

Se não houver campo customizado, labels já resolvem o acoplamento mínimo.

## 5. Modelo de Precedência

## 5.1 Regra principal

Precedência proposta:

1. `Dev_Tracking_SX.md` define o trabalho oficial.
2. Jira reflete e amplia visibilidade operacional.
3. Mudanças feitas direto no Jira precisam ser reconciliadas no tracking local.
4. `Done` só é verdadeiro quando o tracking local estiver atualizado.

## 5.2 Regras de conflito

### Cenário A - Mudança no tracking local

Quando o backlog local mudar:

- a Cindy identifica delta;
- atualiza ou cria issue no Jira;
- registra evidência mínima no tracking, se a mudança for estrutural.

### Cenário B - Mudança direta no Jira

Quando alguém mudar status, prioridade ou descrição direto no Jira:

- a Cindy trata isso como sinal externo;
- propõe reconciliação no `Dev_Tracking_SX.md`;
- nunca assume conclusão local sem evidência no tracking.

### Cenário C - Divergência

Quando `Dev_Tracking` e Jira divergirem:

- prevalece o tracking local para aceite e governança;
- Jira é corrigido ou marcado com comentário de divergência;
- a diferença deve ser registrada como decisão curta ou comentário operacional.

## 6. Workflow Alternativo Proposto

## 6.1 Modo de operação

Seguir o mesmo padrão já pensado para a camada de gestão opcional:

- `MGMT_LAYER_MODE=off`
- `MGMT_LAYER_MODE=prompt`
- `MGMT_LAYER_MODE=on`

E trocar a ferramenta:

- `MGMT_LAYER_TOOL=jira`

## 6.2 Estado observado local

Criar arquivo não versionado em `.scr/`, por exemplo:

- `.scr/mgmt_layer.jira.json`

Conteúdo esperado:

- `jira_base_url`
- `project_key`
- `project_id`
- `user_account_id`
- `status_map`
- `priority_map`
- `issue_type_map`
- `last_sync_at`
- `sync_mode`

Esse arquivo guarda o estado observado, não a configuração canônica.

## 6.3 Ciclo operacional da Cindy

### Etapa 1 - Inicialização

1. Ler `rules/WORKSPACE_RULES.md`.
2. Verificar se a camada Jira está `off`, `prompt` ou `on`.
3. Carregar `.scr/.env`.
4. Validar acesso com `GET /myself`.
5. Validar projeto com `GET /project/STVIA`.

### Etapa 2 - Descoberta de estado

1. Ler `Dev_Tracking_SX.md`.
2. Ler `tests/bugs_log.md` quando houver bug/teste.
3. Buscar issues relevantes via JQL.
4. Montar mapa local `tracking ID -> issue Jira`.

### Etapa 3 - Sincronização

1. Identificar novas estórias no backlog local.
2. Criar issues Jira para itens ainda não refletidos.
3. Atualizar campos quando houver delta.
4. Aplicar transição Jira quando o status local mudar.
5. Adicionar comentário quando houver decisão, evidência ou contexto operacional.

### Etapa 4 - Rastreabilidade

1. Registrar no `Dev_Tracking_SX.md` apenas o necessário.
2. Não inflar o tracking com espelhamento excessivo.
3. Usar decisões curtas para mudanças de política, precedência e integração.

## 6.4 Quando a sprint atualiza o Jira

Regra proposta:

- toda atualização material no backlog da sprint pode disparar sincronização Jira;
- a atualização de texto livre no tracking não precisa gerar update remoto;
- somente mudanças em estória, status, prioridade, prazo, responsável ou decisão relacionada devem refletir no Jira.

Disparadores recomendados:

- inclusão de nova estória;
- mudança de `To-Do` para `Doing`;
- mudança de `Doing` para `Done`;
- criação de bug/teste;
- alteração de prioridade;
- inclusão de observação operacional relevante.

## 7. Operações que Devemos Implementar

## 7.1 Fase 1 - Especificação e governança

1. Formalizar a camada Jira nas regras do workspace.
2. Definir se o modo padrão será `prompt` ou `on`.
3. Declarar o Jira como camada externa opcional, não canônica.
4. Definir mapeamento de status DOC2.5 -> Jira.

## 7.2 Fase 2 - Estado local e bootstrap

1. Criar `scripts/mgmt_layer_jira_init.py`.
2. Validar `.scr/.env` sem expor segredos.
3. Descobrir usuário, projeto e metadados do Jira.
4. Persistir estado observado em `.scr/mgmt_layer.jira.json`.

## 7.3 Fase 3 - Leitura e reconciliação

1. Criar `scripts/mgmt_layer_jira.py status`.
2. Criar `scripts/mgmt_layer_jira.py discover`.
3. Implementar busca via JQL por labels e sprint lógica.
4. Mapear issue existente para item do tracking.

## 7.4 Fase 4 - Escrita controlada

1. Criar `scripts/mgmt_layer_jira.py sync`.
2. Suportar criação de issue.
3. Suportar update de summary, description, priority, due date, labels e components.
4. Suportar transição de status.
5. Suportar comentário de evidência.

## 7.5 Fase 5 - Regras de reconciliação

1. Implementar dry-run.
2. Mostrar delta antes de escrever.
3. Evitar exclusão automática de issue por padrão.
4. Tratar conflito de status entre Jira e tracking.
5. Nunca marcar local como concluído com base só no Jira.

## 7.6 Fase 6 - Operação da sprint

1. Ao atualizar `Dev_Tracking_SX.md`, executar rotina de sync Jira.
2. Ao detectar mudança remota relevante, propor atualização local.
3. Registrar decisão no tracking quando a política mudar.
4. Registrar bugs/testes no log canônico e refletir no Jira quando aplicável.

## 8. Proposta de Mapeamento Inicial

## 8.1 Status

| DOC2.5 | Jira |
|---|---|
| `To-Do` | `To Do` |
| `Doing` ou `In Progress` | `In Progress` |
| `Done` | `Done` |

## 8.2 Prioridade

| Sentido operacional | Jira |
|---|---|
| baixa | `Low` |
| média | `Medium` |
| alta | `High` |
| crítica | `Highest` |

## 8.3 Tipos

| Prefixo | Tipo Jira sugerido |
|---|---|
| `ST-` | Task |
| `BUG-` | Bug |
| `TEST-` | Task ou Subtask |
| `D-` | comentário ou Task, conforme impacto |

## 9. Exemplo de fluxo desejado

Exemplo:

1. A sprint recebe `ST-S0-18 - Especificar camada Jira`.
2. A Cindy detecta item novo no backlog.
3. O módulo Jira cria uma issue no projeto `STVIA`.
4. A issue recebe:
   - `summary` com o título da estória;
   - `label` `tracking:ST-S0-18`;
   - `label` `sprint:S0`;
   - `label` `doc25`;
   - descrição com contexto da sprint.
5. Quando o backlog local muda para `Doing`, a Cindy consulta transições e move a issue.
6. Quando a estória vira `Done`, a issue é movida para `Done` e recebe comentário com evidência.

## 10. Riscos e Limites

- Dependência de mapeamento correto de transições Jira.
- Projeto `Next-Gen` reduz utilidade de board/sprint clássico.
- Mudanças diretas no Jira podem gerar divergência sem reconciliação.
- Update automático demais pode poluir o histórico.
- Exclusão remota via API deve ser tratada como operação administrativa, não padrão.

## 11. Recomendação Final

A recomendação é adotar o Jira como camada externa opcional de gestão, com este desenho:

1. DOC2.5 continua local e canônico.
2. A Cindy opera a integração.
3. O `Dev_Tracking_SX.md` dispara a sincronização.
4. O Jira recebe reflexo do backlog, status, prioridade e evidências.
5. A conclusão oficial continua dependendo do tracking local.

## 12. Próximas Ações Recomendadas

1. Aprovar o modelo de precedência `DOC2.5 > Jira`.
2. Aprovar a criação do módulo `mgmt_layer_jira`.
3. Definir se a sincronização será `manual`, `prompt` ou `auto`.
4. Validar o mapeamento real de status e issue types do projeto `STVIA`.
5. Implementar primeiro `status` e `dry-run`.
6. Implementar `sync` somente após validação de leitura e reconciliação.
