---
name: openclaw_delegate_task
description: Declarar explicitamente que delegacao para OpenClaw esta fora do escopo atual da Cindy.
---

Use quando houver pedido para integrar, delegar ou depender de OpenClaw.

Execute:

1. Verificar as regras locais e globais aplicaveis
2. Informar que OpenClaw permanece fora do escopo atual
3. Redirecionar o trabalho para uma alternativa canonicamente suportada, quando existir

Regras:

- Skill bloqueada no estado atual
- Nao criar codigo, dependencia ou documentacao que introduza OpenClaw
- Manter aderencia a `rules/WORKSPACE_RULES.md`

