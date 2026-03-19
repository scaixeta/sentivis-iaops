# bugs_log.md - Log Centralizado de Bugs e Testes

## 1. Proposito

Centralizar o registro de bugs e testes por sprint com rastreabilidade suficiente para sustentar decisoes, correcoes e validacoes estruturais do projeto.

## 2. Regra de Uso

- Registrar bugs e testes por sprint
- Usar formato padronizado de identificacao
- Manter referencia cruzada com `Dev_Tracking_SX.md`
- Bugs: `BUG-SX-YY`
- Testes: `TEST-SX-YY`
- Registrar fatos observaveis, nao suposicoes
- Explicitar status e impacto de cada bug
- Registrar resultado real dos testes, sem citar validacoes inexistentes

---

## 3. Sprint {{SPRINT_ID}}

### 4. Bugs Registrados

- `BUG-{{SPRINT_ID}}-01` - `{{BUG_TITLE_1}}`
  - Evidencia: `{{BUG_EVIDENCE_1}}`
  - Impacto: `{{BUG_IMPACT_1}}`
  - Referencias: `{{BUG_REFERENCES_1}}`
  - Status: `{{BUG_STATUS_1}}`

### 5. Testes Registrados

- `TEST-{{SPRINT_ID}}-01` - `{{TEST_TITLE_1}}`
  - Escopo: `{{TEST_SCOPE_1}}`
  - Resultado: `{{TEST_RESULT_1}}`
  - Status: `{{TEST_STATUS_1}}`

---

## 6. Timestamp UTC

Event | Start | Finish | Status
---|---|---|---
BUG-{{SPRINT_ID}}-01 | {{BUG_TS_START_1}} | {{BUG_TS_FINISH_1}} | {{BUG_STATUS_1}}
TEST-{{SPRINT_ID}}-01 | {{TEST_TS_START_1}} | {{TEST_TS_FINISH_1}} | {{TEST_STATUS_1}}

## 7. Regras de Qualidade do Log

- Cada bug deve apontar para pelo menos uma evidencia observavel
- Cada teste deve descrever o escopo realmente validado
- O `Timestamp UTC` deve refletir eventos ja executados
- O log deve permanecer coerente com `README.md`, `Dev_Tracking.md` e `Dev_Tracking_SX.md`
- Itens historicos nao devem ser apagados sem justificativa formal

---

## 8. Sprints Futuras

Sprints subsequentes (`S2`, `S3`, etc.) devem ser adicionadas conforme a evolucao do projeto, preservando a ordem historica do log.
