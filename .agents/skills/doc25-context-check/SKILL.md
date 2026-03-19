---
name: doc25-context-check
description: Reduzir desperdicio de contexto DOC2.5 com leitura incremental, arquivos minimos por etapa e resumo das pendencias ativas.
---

Use quando iniciar discovery, planejamento, execucao, validacao ou relatorio em ciclos DOC2.5.

Execute:

1. Ler `rules/WORKSPACE_RULES.md` como fonte operacional obrigatoria
2. Rodar `python3 scripts/doc25_context_check.py --step <discovery|planning|execution|validation|report>`
3. Informar extras apenas quando a correcao atual exigir contexto temporario
4. Reutilizar contexto permanente e da sprint ativa sem reler arquivos inalterados
5. Preferir resumos incrementais e validacao cruzada curta antes de reprocessar todos os artefatos

Categorias operacionais:

- Contexto permanente: `README.md`, `rules/WORKSPACE_RULES.md`, `Dev_Tracking.md`, `tests/bugs_log.md`
- Contexto da sprint ativa: `Dev_Tracking_SX.md`
- Contexto temporario de correcao: apenas arquivos diretamente afetados

Sinais de desperdicio:

- reabrir muitos docs sem mudancas
- reler todo o repositorio para uma correcao localizada
- reportar conclusao sem resumo incremental das pendencias
