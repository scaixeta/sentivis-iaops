---
name: validate_doc25_structure
description: Validar conformidade estrutural do projeto com o padrao DOC2.5 usando os caminhos canonicos existentes.
---

Use quando precisar conferir se a Cindy esta aderente ao padrao DOC2.5.

Execute:

1. Verificar `README.md`, `rules/WORKSPACE_RULES.md`, `Dev_Tracking.md`, `Dev_Tracking_SX.md` e `tests/bugs_log.md`
2. Confirmar a presenca e a ordem canonica dos docs em `docs/`
3. Validar backlog, decisoes e `Timestamp UTC` nos artefatos de sprint
4. Registrar gaps objetivos antes de propor qualquer alteracao

Regras:

- Nao criar estrutura nova fora do modelo canonico
- Considerar `docs/README.md` e `docs/INDEX.md` como proibidos
- Tratar `Timestamp UTC` como parte obrigatoria da validacao

