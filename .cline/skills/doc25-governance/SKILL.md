---
name: doc25-governance
description: Guardrails de governança DOC2.5 (paths canônicos, evitar docs duplicados, Dev_Tracking append-only, mudanças mínimas, política de commits PO-exclusiva).
---
# Governança DOC2.5

## Quando usar
Usar quando o usuário mencionar DOC2.5, localização canônica de arquivos, arquivos duplicados, disciplina de Dev_Tracking, normalização/padronização de artefatos de sprint, ou política de commits.

## Regras operacionais (estritas)
1) **Escopo dinâmico**: Operar dentro do projeto atual conforme contexto do workspace.
2) **Canonicalização**: Antes de criar/renomear qualquer arquivo, buscar equivalentes existentes para evitar duplicatas.
3) **Append-only**: Se Dev_Tracking existe, adicionar entradas curtas (sem reescritas).
4) **Footprint mínimo**: Não criar novos arquivos "auxiliares" sem solicitação explícita.
5) **Commit é decisão do PO**: NUNCA sugerir ou recomendar commits. Aguardar comando expresso.
6) **Proibições DOC2.5**: Sem "Lições aprendidas", sem "PO AI:", sem "Épico", sem tabelas complexas.

## Procedimento
1) Identificar artefato(s) relevante(s): Dev_Tracking*, rules/WORKSPACE_RULES.md, tests/bugs_log.md, docs/* (apenas se presente).
2) Verificar duplicatas (mesma intenção, locais diferentes). Preferir localização canônica do projeto.
3) Aplicar a menor mudança que resolva o problema.
4) Registrar entrada concisa no Dev_Tracking: o que mudou + por quê + arquivos afetados.
5) Validar checkpoints DOC2.5 antes de declarar fase completa.
