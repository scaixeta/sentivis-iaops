# Guia de Preenchimento de Campos dos Templates

Este guia orienta como preencher os placeholders `{{VAR}}` dos templates canonicos DOC2.5.

## Regra Geral

- Se o PO disse: use o valor real.
- Se nao disse e nao da para inferir: use `Pendente de validacao`.
- Se da para inferir com seguranca: use o valor e registre como `inferido`.
- NUNCA invente detalhes tecnicos (sensores, protocolos, frameworks, hardware) sem confirmacao.

## Campos Compartilhados (aparecem em varios templates)

| Placeholder | O que e | Fonte |
|---|---|---|
| `{{PROJECT_NAME}}` | Nome do projeto | PO ou nome do repositorio |
| `{{ACTIVE_SPRINT}}` | Identificador da sprint (ex: `S1`) | Sempre `S1` no bootstrap |
| `{{SPRINT_STATUS}}` | Estado da sprint | Sempre `Aberta` no bootstrap |
| `{{CURRENT_PHASE}}` | Fase atual do projeto | Sempre `Iniciacao` no bootstrap |
| `{{APPROVED_SCOPE}}` | Escopo aprovado pelo PO | Se vago: `Pendente de validacao` |
| `{{SPRINT_PERIOD}}` | Periodo da sprint | Se indefinido: `Pendente` |

## Campos por Template

### README.md
| Placeholder | Regra |
|---|---|
| `{{WORKSTREAM_NAME}}` | `Sprint Ativa: S1` no bootstrap |
| `{{PRIMARY_SCOPE_1..3}}` | Extrair do pedido do PO. Se vago, usar 1 item com `Pendente de validacao` |
| `{{MAIN_OBJECTIVE_1..3}}` | Idem ao scope |
| `{{PENDING_ITEM_1..3}}` | Listar o que ficou indefinido |

### Dev_Tracking_SX.md
| Placeholder | Regra |
|---|---|
| `{{SPRINT_CONTEXT_1..3}}` | Contexto factual do pedido. Nao inventar |
| `{{SPRINT_OBJECTIVE_1..2}}` | Derivar do pedido. Se vago: `Pendente de validacao` |
| `{{SPRINT_STORY_1..2}}` | Historias minimas. Primeira sempre: `Criar estrutura basica do projeto` |
| `{{SPRINT_DECISION_1}}` | Se nao houve decisao: `Aguardando definicao do escopo com PO` |
| `{{TS_X_START}}` | Timestamp real no formato DOC2.5 |
| `{{TS_X_FINISH}}` | `-` se ainda nao terminou |

### SETUP.md
| Placeholder | Regra |
|---|---|
| `{{REPOSITORY_TYPE}}` | `baseline de geracao` ou `repo materializado` |
| `{{EVIDENCE_SOURCE_1..3}}` | Apenas evidencias reais no repositorio |
| `{{CONFIRMED/INFERRED/PENDING}}` | Classificar honestamente |
| `{{CURRENT_SETUP_BOUNDARY}}` | O que o setup cobre de fato |
| `{{NOT_INCLUDED/CONFIGURED}}` | O que nao esta pronto |

### ARCHITECTURE.md
| Placeholder | Regra |
|---|---|
| `{{PROJECT_ROLE}}` | Papel real do projeto. Se vago: `Pendente de validacao` |
| `{{ARCHITECTURE_TYPE}}` | Nao inventar tipo sem confirmacao |
| `{{GOVERNANCE/CORE/KNOWLEDGE/OPS}}` | Preencher so o que e factual |

### bugs_log.md
| Placeholder | Regra |
|---|---|
| `{{BUG/TEST_TITLE}}` | No bootstrap: registrar pelo menos `TEST-S1-01 - Validacao estrutural DOC2.5` |
| `{{BUG/TEST_EVIDENCE}}` | Resultado real da validacao |
| `{{BUG/TEST_STATUS}}` | `Passed` ou `Failed` baseado na checklist |
