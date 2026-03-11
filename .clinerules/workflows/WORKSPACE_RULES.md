# WORKSPACE RULES — Cindy

Este arquivo resume os caminhos canonicos que o Cline deve usar ao operar a Cindy pura.

## Escopo

- Projeto: `Cindy`
- Fonte local de governanca: `rules/WORKSPACE_RULES.md`
- Regras globais complementares: `.clinerules/WORKSPACE_RULES_GLOBAL.md`

## Caminhos canonicos

- Documentacao raiz: `README.md`
- Documentacao tecnica: `docs/SETUP.md`, `docs/ARCHITECTURE.md`, `docs/DEVELOPMENT.md`, `docs/OPERATIONS.md`
- Tracking: `Dev_Tracking.md`, `Dev_Tracking_S1.md`, `tests/bugs_log.md`
- Templates: `Templates/`
- Templates fallback: `.clinerules/templates/doc25/`
- Skills runtime:
  - Antigravity: `.agent/skills/` e `.agents/skills/`
  - Cline: `.cline/skills/`
  - Codex: `.codex/skills/`

## Regras operacionais minimas

1. Ler `rules/WORKSPACE_RULES.md` antes de alterar documentacao, tracking, skills ou workflows.
2. Manter o modelo canônico da Cindy; nao importar estrutura especifica de outros projetos.
3. Usar `Templates/` como fonte principal de formato; usar `.clinerules/templates/doc25/` apenas como fallback local.
4. Atualizar `Dev_Tracking.md`, `Dev_Tracking_S1.md` e `tests/bugs_log.md` com `Timestamp UTC` quando houver evolucao relevante.
5. Nao criar commits ou push sem comando expresso do PO.

## Relacao com workflows

- `init.md` inicializa contexto e leitura de regras.
- `docs-doc25.md` cobre documentacao canônica.
- `dev-doc25.md` cobre execucao com rastreabilidade.
- `commit-doc25.md` cobre gate de commit/push.
