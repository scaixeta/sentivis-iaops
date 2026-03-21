# Workflow Local - Sync do SoT para Jira (DOC2.5)

## Princípio

- a Cindy é a orquestradora
- este workflow é local ao projeto
- o source of truth é local
- o Jira é apenas alvo operacional deste workflow
- decisões permanecem locais e não devem ser criadas no Jira

## Fontes obrigatórias

1. `rules/WORKSPACE_RULES.md`
2. `.clinerules/WORKSPACE_RULES_GLOBAL.md`
3. `Cindy_Contract.md`
4. `README.md`
5. `Dev_Tracking.md`
6. `Dev_Tracking_SX.md` ativo
7. `tests/bugs_log.md`

## Regra de interpretação

- o tracking local determina a sprint ativa
- o tracking local tambem deve declarar o objetivo de negocio da sprint como entrega de valor ao cliente
- o backlog local determina o que deve existir no Jira
- `To-Do` e `Pending-SX` locais devem refletir `Pendentes` no Jira
- `Doing` local deve refletir `Em Progresso`
- `Done` e `Accepted` locais devem refletir `Feito`
- `ST` deve refletir label `estoria`
- `BUG` deve refletir label `bug`
- `CR` deve refletir label `change_request`
- `D-*` não devem ser criadas no Jira
- `tracking_<ID>` deve permanecer como label de rastreabilidade
- bugs e testes registrados localmente devem ser espelhados no Jira com o mesmo estado operacional, incluindo criacao da issue quando necessario
- a sprint tem duração padrão esperada de `3 dias` quando criada sem `end-date` explícito
- a data limite das issues da sprint deve herdar por padrao a data limite da sprint
- a sprint pode terminar antes do prazo, mas o prazo inicial deve nascer coerente no local e no Jira
- a due date das issues pode ser ajustada manualmente depois, mas a criação/atribuição parte desse padrão

## Ordem de execução

1. Validar integridade local do integrador
2. Ler o SoT local e resumir a sprint ativa
3. Ler o objetivo de negocio da sprint no tracking local
4. Rodar `dry-run` do sync
5. Revisar plano de updates e creates
6. Aplicar `sync --yes` se coerente
7. Rodar `dry-run` de `sprint goal`
8. Aplicar `sprint goal --yes` se coerente
9. Rodar `dry-run` de `sprint assign`
10. Aplicar `sprint assign --yes` se coerente
11. Validar no Jira o reflexo final
12. Reportar resultado em pt-BR

## Comandos-base

Validação do integrador:

```powershell
python -m py_compile integrators/jira/mapper.py integrators/jira/cli.py integrators/jira/sync_engine.py integrators/common/doc25_parser.py
```

Dry-run do sync:

```powershell
python -m integrators.jira sync --tracking-file Dev_Tracking_S2.md --dry-run
```

Sync real:

```powershell
python -m integrators.jira sync --tracking-file Dev_Tracking_S2.md --yes
```

Dry-run do objetivo da sprint:

```powershell
python -m integrators.jira sprint goal --sprint-name "Sprint S2" --goal "<objetivo de negocio da sprint>" --dry-run
```

Aplicacao do objetivo da sprint:

```powershell
python -m integrators.jira sprint goal --sprint-name "Sprint S2" --goal "<objetivo de negocio da sprint>" --yes
```

Dry-run de atribuição ao sprint:

```powershell
python -m integrators.jira sprint assign --tracking-file Dev_Tracking_S2.md --sprint-name "Sprint S2" --dry-run
```

Atribuição real ao sprint:

```powershell
python -m integrators.jira sprint assign --tracking-file Dev_Tracking_S2.md --sprint-name "Sprint S2" --yes
```

Validação final:

```powershell
python -m integrators.jira sprint status
```

## Checklist de validação

- a sprint ativa local foi identificada corretamente
- o objetivo de negocio da sprint foi identificado corretamente no tracking
- backlog local, bugs e CR foram considerados
- decisões foram excluídas da operação Jira
- labels Cindy foram aplicadas:
  - `estoria`
  - `bug`
  - `change_request`
- labels `tracking_<ID>` permanecem presentes
- itens `To-Do` locais aparecem como `Pendentes` no Jira
- os itens esperados foram atribuídos ao sprint Jira correto

## Saída esperada

O relatório final deve responder:

1. o que o source of truth local exigiu
2. qual objetivo de negocio da sprint foi refletido como `Sprint goal` no Jira
3. o que foi refletido no Jira
4. o que ficou divergente
5. se `To-Do -> Pendentes` foi confirmado
6. se `BUG`, `CR` e `estoria` foram refletidos corretamente
7. se decisões permaneceram locais
