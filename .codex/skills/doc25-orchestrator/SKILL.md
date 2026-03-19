---
name: doc25-orchestrator
description: Orquestrar o fluxo DOC2.5 no Codex. Use quando for necessário decidir e encaminhar entre skills de inicialização, desenvolvimento, documentação e commit com gates de aprovação.
---

Selecione a skill correta com base na intenção do PO:

- Inicialização de contexto: usar `doc25-init`
- Higiene de contexto: usar `doc25-context-check`
- Desenvolvimento: usar `doc25-dev-workflow`
- Documentação: usar `doc25-docs-workflow`
- Validação de conformidade: usar `doc25-preflight`
- Commit/push: usar `doc25-commit-gate`

Aplicar sempre:

1. Entendimento
2. Discovery enxuto
3. Planejamento
4. Aprovação explícita
5. Execução
6. Preflight + rastreabilidade

Referências:
- `references/rules-map.md`
- `references/skill-routing.md`
