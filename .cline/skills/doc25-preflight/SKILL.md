---
name: doc25-preflight
description: Executar o gate DOC2.5 de preflight antes de alegar conformidade, conclusão de fase ou fechamento de sprint.
---

Use quando houver mudanca estrutural, atualizacao de docs, validacao de sprint, fechamento de fase ou qualquer declaracao de conformidade DOC2.5.

Execute:

1. Ler `rules/WORKSPACE_RULES.md` como fonte operacional obrigatoria
2. Identificar a sprint ativa na raiz
3. Executar validacao manual do baseline canonico:
   - `README.md`
   - `Dev_Tracking.md`
   - `Dev_Tracking_SX.md` ativo
   - `tests/bugs_log.md`
   - os 4 docs canonicos em `docs/`
   - ausencia de `docs/README.md` e `docs/INDEX.md`
4. Corrigir qualquer bloqueio antes de reportar conclusao
5. Registrar referencias de teste e rastreabilidade no `Dev_Tracking_SX.md` ativo e em `tests/bugs_log.md`

Gate obrigatorio:

- Nao declarar conclusao, conformidade ou encerramento sem validacao cruzada satisfatoria
- Somente o PO pode encerrar sprint
- Validacao cruzada entre `README.md`, `Dev_Tracking.md`, `Dev_Tracking_SX.md` e `tests/bugs_log.md` e mandatoria
- Timestamp UTC fora do formato canonico bloqueia a conformidade

Mensagem esperada:

`DOC2.5 CHECK: sprint ativa identificada, artefatos canonicos verificados, gate do PO obrigatorio, validacao cruzada executada antes da conclusao.`
