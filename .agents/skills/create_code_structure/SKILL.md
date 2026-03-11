---
name: create_code_structure
description: Criar ou ajustar estrutura de codigo somente quando houver aprovacao explicita e o modelo canonico permitir.
---

Use quando o PO autorizar criacao de estrutura de codigo ou reorganizacao tecnica controlada.

Execute:

1. Confirmar que a demanda exige estrutura de codigo, nao apenas documentacao
2. Validar regras locais, sprint ativa e artefatos impactados
3. Propor a menor estrutura compativel com o modelo canonico
4. Executar apenas apos aprovacao explicita do PO

Regras:

- Considerar risco medio
- Bootstrap ou alinhamento documental nao autorizam implementacao por si so
- Registrar o trabalho em `Dev_Tracking_SX.md` e `tests/bugs_log.md` quando aplicavel

