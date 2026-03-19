---
name: doc25-preflight
description: Executar o gate DOC2.5 de preflight antes de alegar conformidade, conclusão de fase ou fechamento de sprint.
---

Use quando houver mudanca estrutural, atualizacao de docs, validacao de sprint, fechamento de fase ou qualquer declaracao de conformidade DOC2.5.

Execute:

1. Ler `rules/WORKSPACE_RULES.md` como fonte operacional obrigatoria
2. Identificar a sprint ativa na raiz
3. Rodar `python3 scripts/doc25_preflight.py`
4. Corrigir qualquer bloqueio antes de reportar conclusao
5. Registrar referencias de teste e rastreabilidade no `Dev_Tracking_SX.md` ativo e em `tests/bugs_log.md`

Gate obrigatorio:

- Nao declarar conclusao, conformidade ou encerramento sem `PASS`
- Somente o PO pode encerrar sprint
- Validacao cruzada entre `README.md`, `Dev_Tracking.md`, `Dev_Tracking_SX.md` e `tests/bugs_log.md` e mandatória
- Timestamp UTC fora do formato canonico bloqueia a conformidade

Mensagem esperada:

`DOC2.5 PREFLIGHT: sprint ativa identificada, artefatos canônicos verificados, gate do PO obrigatório, encerramento de sprint proibido sem ordem explícita, validação cruzada exigida antes da conclusão.`
