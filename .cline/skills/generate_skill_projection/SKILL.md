---
name: generate_skill_projection
description: Projetar uma capacidade comum da Cindy para outro runtime mantendo o modelo canonico do projeto.
---

Use apenas quando o PO pedir explicitamente para projetar ou espelhar uma skill entre runtimes.

Execute:

1. Identificar a skill de origem e o runtime de destino
2. Preservar conteudo, governanca e referencias canonicas
3. Ajustar apenas o necessario para o runtime alvo
4. Validar coerencia com `.cline/`, `.codex/`, `.agent/` e `.agents/`

Regras:

- Skill bloqueada por padrao; requer aprovacao explicita do PO
- Nao criar novos modelos de registry ou estruturas paralelas
- Priorizar espelhamento fiel do conteudo canonico

