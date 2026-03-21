# Estudo Operacional - Jira Cloud + DOC2.5 + Cindy

## 1. Objetivo

Este documento registra, com rigor operacional, como o projeto `Sentivis IAOps` usa o Jira Cloud como camada operacional externa sem romper o modelo canônico DOC2.5.

Objetivos deste estudo:

- documentar o modelo de precedência entre `Dev_Tracking` e Jira;
- registrar o comportamento real observado da API e do board;
- consolidar o que já foi implementado no integrador local;
- descrever regras, exceções e limites para reprodução futura;
- reduzir ambiguidade para Cindy, PO e futuros mantenedores.

Escopo deste documento:

- workflow local do projeto;
- integrador local em `integrators/jira/`;
- board Jira do projeto `STVIA`;
- uso da sprint ativa, backlog, bugs, CRs, datas e transições.

Fora de escopo:

- alteração de `.clinerules/`;
- alteração do contrato canônico global da Cindy;
- uso do Jira como fonte primária de verdade.

---

## 2. Princípio Canônico

### 2.1 Precedência

Regra oficial do projeto:

1. o `Dev_Tracking_SX.md` ativo continua sendo a fonte primária de verdade local;
2. o Jira é um alvo operacional e de visibilidade;
3. a Cindy é a orquestradora do workflow local;
4. o Jira não substitui aceite, governança nem rastreabilidade local;
5. mudanças diretas no Jira precisam ser reconciliadas com o SoT local.
6. backlog, bugs e testes devem manter espelhamento de estado entre local e Jira, com criacao da issue quando necessario.

### 2.2 Papel da Cindy

A Cindy, neste contexto, deve:

- ler o SoT local antes de operar o Jira;
- usar o integrador local em `integrators/jira/`;
- aplicar `dry-run` antes de mutações relevantes;
- respeitar gates de PO quando houver decisão ambígua;
- reportar divergências entre local e Jira;
- nunca assumir que o Jira venceu o tracking local.

### 2.3 Escopo local vs canônico global

As regras e workflows descritos aqui são **locais ao projeto**.

Isso significa:

- podem ser implementados em `KB/`, `rules/WORKSPACE_RULES.md` e `integrators/`;
- não devem ser promovidos automaticamente para `.clinerules/`;
- não redefinem o baseline global da Cindy.

---

## 3. Estado Atual da Integração

## 3.1 Projeto Jira

- Instância: `https://sentivisiaops.atlassian.net`
- Projeto: `STVIA`
- Board operacional observado: `DEV board`

## 3.2 Sprints observadas

No estado atual observado durante os testes:

- `Sprint S0` - encerrada
- `Sprint S1` - encerrada
- `Sprint S2` - ativa

## 3.3 Arquivos locais relevantes

Fontes locais obrigatórias para o workflow:

- `README.md`
- `Dev_Tracking.md`
- `Dev_Tracking_S2.md` ou outro `Dev_Tracking_SX.md` ativo
- `tests/bugs_log.md`
- `rules/WORKSPACE_RULES.md`
- `KB/local-jira-sync-doc25-workflow.md`

## 3.4 Estado observado em `.scr/`

O integrador usa estado local observado, não canônico, em:

- `.scr/.env`
- `.scr/mgmt_layer.jira.json`

Esse estado serve para:

- autenticação;
- metadados do projeto;
- mapeamento de board/colunas/status;
- otimização de sync e reconciliação.

## 3.5 Objetivo de negocio da sprint

No modelo local adotado no projeto, cada sprint deve declarar explicitamente um objetivo de negocio / valor para cliente no `Dev_Tracking_SX.md`.

Regra operacional:

- o texto nasce localmente
- o texto deve ser curto e orientado a entrega de valor, nao a detalhe tecnico
- quando a sprint for refletida no Jira, esse texto deve ser propagado ao atributo `goal` da entidade Sprint
- o `Sprint goal` nao substitui o objetivo local; ele o espelha operacionalmente

Exemplo aplicado na S2:

- `Estabelecer a visibilidade executiva do projeto com rastreabilidade confiavel entre planejamento local e operacao no Jira.`

---

## 4. Modelo de Dados Local

## 4.1 O que existe hoje no `Dev_Tracking`

Na tabela de backlog, hoje trabalhamos com:

- `Status`
- `SP`
- `Jira`
- `Estória`

Historicamente, a célula `Estória` carregava algo como:

- `ST-S0-03 – Definir contrato de mock telemetry`

E a coluna `Jira` carregava algo como:

- `STVIA-45`

## 4.2 Decisão evolutiva do modelo

O modelo local foi ajustado para suportar:

- a chave do Jira como identificador principal;
- status nativo do Jira no tracking;
- compatibilidade com IDs locais legados.

### Resultado prático

O parser local agora suporta dois formatos:

Formato legado:

- `ST-S0-03 – Definir contrato de mock telemetry`

Formato novo/transicional:

- `STVIA-45 – Definir contrato de mock telemetry`

## 4.3 Compatibilidade interna

Mesmo quando a chave Jira passa a ser o identificador principal, o integrador preserva internamente:

- `tracking_key`

Esse `tracking_key` continua sendo usado para:

- labels `tracking_<ID>`;
- match estável com issues já existentes;
- write-back e reconcile;
- compatibilidade com o backlog histórico.

### Exemplo

Para uma linha atual da S2:

- Jira: `STVIA-45`
- Estória legada: `ST-S0-03 – Definir contrato...`

O item lido fica assim, conceitualmente:

- `id = STVIA-45`
- `primary_id = STVIA-45`
- `tracking_key = ST-S0-03`

Essa compatibilidade permite migracao gradual da linguagem local sem perder reconciliacao com o historico anterior.

---

## 5. Tipos, Labels e Rastreabilidade

## 5.1 Tipos operacionais da Cindy

No modelo local do projeto, os tipos operacionais são:

- `Estória`
- `BUG`
- `Change Request`
- `Decisão`

Regra:

- `Decisão` permanece local-only;
- `Estória`, `BUG` e `Change Request` podem refletir no Jira.

## 5.2 Labels Jira adotadas

Labels canônicas atualmente usadas nas issues sincronizadas:

- `doc25`
- `sentivis`
- `estoria`
- `bug`
- `change_request`
- `tracking_<ID>`

### Observação

O label `tracking_<ID>` continua baseado no identificador estável de rastreabilidade, não necessariamente no ID principal visível no tracking.

Exemplo:

- `tracking_ST-S0-03`
- `tracking_CR-S1-02`
- `tracking_BUG-S2-01`

## 5.3 Mapeamento de tipo local -> issuetype Jira

O projeto `STVIA` não expõe `Bug` como issue type válido.

Tipos realmente observados no Jira:

- `História`
- `Tarefa`
- `Subtask`
- `Epic`

Por isso, o mapeamento local implementado ficou:

| Tipo local | Issue Type Jira |
|---|---|
| `ST` | `História` |
| `BUG` | `Tarefa` |
| `CR` | `Tarefa` |
| `TEST` | `Tarefa` |

### Importante

O tipo de negócio é preservado pelos labels da Cindy, mesmo quando o Jira não oferece o issuetype ideal.

---

## 6. Status e Colunas do Board

## 6.1 Colunas observadas no board

Configuração relevante observada do board:

| Ordem | Coluna |
|---|---|
| 1 | `Backlog` |
| 2 | `Pendentes` |
| 3 | `Em Progresso` |
| 4 | `Em Testes` |
| 5 | `Feito` |

## 6.2 Mapeamento de status local -> Jira

Mapeamento implementado:

| Status local | Jira |
|---|---|
| `To-Do` | `Pendentes` |
| `Pending-SX` | `Pendentes` |
| `Doing` | `Em Progresso` |
| `Done` | `Feito` |
| `Accepted` | `Feito` |

Além disso, o parser local agora aceita status nativo do Jira diretamente:

- `Pendentes`
- `Em Progresso`
- `Em Testes`
- `Feito`
- `Bloqueado`
- `Backlog`

### Regra importante

Se o status no tracking já for um status nativo do Jira, o integrador o usa diretamente, sem remapeamento intermediário.

---

## 7. Comportamento Real do Workflow Jira

## 7.1 Transições diretas não são suficientes

Foi confirmado que o workflow do board não deve ser interpretado só por transições diretas para o alvo.

Exemplo real:

- um item em `Feito` pode não ter transição direta para `Pendentes`
- mas pode voltar parcialmente por:
  - `Feito -> Em Testes`
  - `Em Testes -> Em Progresso`

## 7.2 Regra implementada no integrador

O integrador foi ajustado para:

- planejar o próximo passo natural conforme a ordem do board;
- alinhar status passo a passo;
- não assumir que só existe sync se houver transição direta para o alvo final.

## 7.3 Limitação observada e correção posterior

Durante os testes, foi observado um período em que a configuração do board causava comportamento anômalo ao tentar retornar itens para `Pendentes`.

Diagnóstico histórico:

- a coluna/status de `Pendentes` estava desalinhada no board
- isso fazia o integrador precisar usar `Em Progresso` como alvo efetivo mínimo em alguns cenários

Depois, o board foi corrigido manualmente no Jira.

Estado atual esperado:

- itens locais `Pending-SX` voltam a refletir normalmente como `Pendentes`
- o fallback deixa de ser comportamento principal

Contingência preservada:

- usar `Em Progresso` como **alvo efetivo minimo** quando `Pendentes` nao for alcancavel pelo workflow real do Jira

### Resultado operacional

Se o local pedir `Pendentes` e o Jira não permitir chegar lá:

- o integrador usa `Em Progresso` como alvo efetivo;
- isso aparece explicitamente no dry-run;
- a interpretação não fica escondida.

---

## 8. Sprints

## 8.1 Regras atuais

Capacidades implementadas:

- listar sprints
- abrir sprint
- fechar sprint
- definir datas da sprint
- criar sprint
- atribuir issues a sprint
- usar `--sprint-name` ou `--sprint-id`

## 8.2 Regra de duração padrão

Regra local implementada:

- uma sprint criada com `start-date` e sem `end-date` explícito assume:
  - `end-date = start-date + 3 dias`

Essa regra foi aplicada em:

- `sprint create`
- `sprint dates`

### Exemplo

Comando:

```powershell
python -m integrators.jira sprint create --sprint-name "Sprint TEST-3D" --start-date 2026-03-21 --dry-run
```

Resultado esperado:

- início: `2026-03-21`
- fim inferido: `2026-03-24`

## 8.3 Regra de due date das issues da sprint

Regra operacional fixada:

- a `due date` das issues da sprint deve herdar por padrão a data limite da sprint

Essa regra foi implementada em:

- `sprint assign`

Quando as issues são atribuídas a uma sprint com `endDate`, o integrador:

1. adiciona as issues à sprint;
2. alinha `duedate` das issues para a data final da sprint.

### Observação

Isso não impede ajuste manual posterior. A regra vale como default de criação/atribuição.

---

## 9. Datas de Sprint e Estórias

## 9.1 Comportamento do Jira

Foi validado:

- a sprint aceita `startDate` e `endDate` com data e hora;
- a issue usa `duedate` apenas com data, sem hora;
- portanto:
  - sprint pode terminar `2026-03-21 18:00`
  - issues ficam com `duedate = 2026-03-21`

## 9.2 Regra prática adotada

Quando o PO pedir:

- "a sprint termina hoje às 18h"

Aplicação correta no Jira:

- `endDate` da sprint em UTC equivalente a `18:00` local;
- `duedate` das issues em `YYYY-MM-DD` do mesmo dia.

## 9.3 Exemplo real aplicado

Na `Sprint S2`, foi aplicado:

- `endDate = 2026-03-22T02:59:59.999Z`

Equivalência:

- fim do dia `21/03/2026` em `America/Sao_Paulo`

E as issues da sprint receberam:

- `duedate = 2026-03-21`

---

## 10. Fechamento de Sprint

## 10.1 Regra de segurança local

O fechamento de sprint no integrador foi protegido por gate local.

Antes de fechar, o integrador:

- identifica a sprint alvo;
- identifica a última coluna do board;
- lista itens concluídos;
- lista itens incompletos;
- lista subtasks abertas;
- exige decisão do PO quando houver ambiguidade.

## 10.2 Descoberta importante sobre a API do Jira

Foi confirmado experimentalmente:

- a API do Jira pode aceitar fechamento de sprint mesmo com itens incompletos;
- ao fechar via API, itens incompletos podem permanecer presos na sprint fechada;
- isso não reproduz automaticamente o mesmo fluxo protetivo da UI.

### Consequência

O gate local não é perfumaria:

- ele protege contra fechamento perigoso e silencioso.

---

## 11. Bugs, CRs e Decisões

## 11.1 Bugs

Os bugs da sprint são lidos de:

- `tests/bugs_log.md`

O parser local já consegue:

- extrair bugs por sprint;
- mapear estado para status DOC2.5;
- criar/refletir esses bugs no Jira.

## 11.2 Change Requests

Os CRs presentes no backlog local entram no mesmo fluxo de sync operacional do sprint.

## 11.3 Decisões

Decisões:

- não devem virar issues automaticamente;
- permanecem locais;
- podem gerar comentário Jira somente quando houver necessidade operacional explícita.

---

## 12. Operações Confirmadas no Integrador

## 12.1 Estado e descoberta

- `bootstrap`
- `status`
- `discover`
- `board columns`

## 12.2 Sync e reconciliação

- `sync`
- `sync --write-back`
- `reconcile`

## 12.3 Issues

- `issue dates`
- `issue progress`
- `issue transition`
- `issue bulk`

## 12.4 Sprints

- `sprint status`
- `sprint assign`
- `sprint open`
- `sprint close`
- `sprint dates`
- `sprint create`

---

## 13. Workflow Local Recomendado

## 13.1 Ordem operacional

1. ler fontes locais obrigatórias
2. validar integridade do integrador
3. executar `sync --dry-run`
4. revisar plano
5. executar `sync --yes`
6. executar `sprint assign --dry-run`
7. executar `sprint assign --yes`
8. validar `sprint status`
9. reportar divergências

## 13.2 Fontes obrigatórias

1. `rules/WORKSPACE_RULES.md`
2. `.clinerules/WORKSPACE_RULES_GLOBAL.md`
3. `Cindy_Contract.md`
4. `README.md`
5. `Dev_Tracking.md`
6. `Dev_Tracking_SX.md` ativo
7. `tests/bugs_log.md`
8. `KB/local-jira-sync-doc25-workflow.md`

---

## 14. Procedimento de Reprodução

## 14.1 Validar integrador

```powershell
python -m py_compile integrators/jira/cli.py integrators/jira/client.py integrators/jira/sync_engine.py integrators/common/doc25_parser.py integrators/jira/mapper.py
```

## 14.2 Inspecionar sprint ativa

```powershell
python -m integrators.jira sprint status
```

## 14.3 Dry-run do sync da sprint ativa local

```powershell
python -m integrators.jira sync --tracking-file Dev_Tracking_S2.md --dry-run
```

## 14.4 Aplicar sync real

```powershell
python -m integrators.jira sync --tracking-file Dev_Tracking_S2.md --yes
```

## 14.5 Dry-run de atribuição ao sprint

```powershell
python -m integrators.jira sprint assign --tracking-file Dev_Tracking_S2.md --sprint-name "Sprint S2" --dry-run
```

## 14.6 Aplicar atribuição ao sprint

```powershell
python -m integrators.jira sprint assign --tracking-file Dev_Tracking_S2.md --sprint-name "Sprint S2" --yes
```

## 14.7 Ajustar datas da sprint explicitamente

```powershell
python -m integrators.jira sprint dates --sprint-name "Sprint S2" --start-date 2026-03-20 --end-date 2026-03-21 --yes
```

## 14.8 Criar sprint nova com duração padrão

```powershell
python -m integrators.jira sprint create --sprint-name "Sprint S3" --start-date 2026-03-24 --dry-run
```

---

## 15. Riscos, Limites e Observações

## 15.1 Limites reais do Jira

- o workflow do board pode impedir retorno completo até `Pendentes`
- a API de fechamento de sprint pode aceitar operação perigosa sem o mesmo cuidado da UI
- o projeto pode não expor issue types ideais, como `Bug`

## 15.2 Limites do modelo local atual

- se o tracking migrar totalmente para usar só `Jira Key`, o tipo semântico pode ficar implícito demais
- para uma migração total futura, o ideal é avaliar:
  - coluna explícita `Tipo`, ou
  - leitura do tipo direto do Jira, ou
  - convenção formal revisada do tracking

## 15.3 Ponto de atenção com bugs

O parser de bugs parte do `tests/bugs_log.md`.

Se um bug estiver marcado localmente como `Done`, o sync pode levá-lo a `Feito` mesmo que alguém espere mantê-lo em `Pendentes` no Jira.

Ou seja:

- a verdade continua sendo o estado local registrado;
- se o comportamento parecer estranho, o primeiro lugar a verificar é o log local.

---

## 16. Recomendação Final

O desenho atual é viável e reproduzível se estas regras forem respeitadas:

1. o SoT permanece local;
2. o Jira é camada operacional;
3. a Cindy orquestra;
4. o integrador local aplica o protocolo;
5. datas da sprint e das issues seguem regra padrão clara;
6. fallbacks de workflow ficam documentados, nunca implícitos.

Recomendação prática:

- manter este modelo local;
- continuar endurecendo o integrador;
- evitar promover regras de projeto para `.clinerules/`;
- usar este documento como referência operacional para reprodução futura.

---

## 17. Resumo Executivo

Este projeto já possui:

- integração Jira funcional;
- sync local -> Jira;
- reconcile por rastreabilidade;
- suporte a bugs/CRs;
- controle de sprint;
- proteção no fechamento;
- alinhamento de datas;
- fallback operacional quando o workflow Jira não entrega exatamente o estado local desejado.

O que foi aprendido:

- a API do Jira é útil, mas precisa de guardrails locais;
- o board real manda mais que a intuição;
- o integrador precisa interpretar o workflow de forma natural e não simplista;
- documentação operacional rigorosa é obrigatória para manter previsibilidade.
