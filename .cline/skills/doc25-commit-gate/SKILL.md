---
name: doc25-commit-gate
description: Controlar commits e push no DOC2.5 com confirmação obrigatória. Use quando o PO emitir comando expresso de commit/push.
---

Pré-condição:

- Commit/push só por comando expresso do PO

Fluxo:

1. Inspecionar estado atual
2. Propor mensagem e arquivos
3. Perguntar confirmação do PO
4. Executar staging/commit/push apenas após confirmação

Regras:

- Não sugerir commit espontaneamente
- Não executar `git commit`/`git push` sem confirmação explícita

Referências:
- `references/commit-gate.md`
