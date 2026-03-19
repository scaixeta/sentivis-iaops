---
description: Workflow para criação e atualização de documentação oficial (DOC2.5).
---

# Workflow de Documentação (DOC2.5)

Objetivo:

- gerar ou ajustar documentação canônica com o minimo de texto util
- usar templates como guia de estrutura, nao como boilerplate a ser copiado
- preservar coerencia entre `README.md`, tracking, `docs/` e `tests/bugs_log.md`

Sequência obrigatória:

1. Ler `rules/WORKSPACE_RULES.md`
2. Ler `.clinerules/WORKSPACE_RULES_GLOBAL.md`
3. Ler `Cindy_Contract.md`
4. Classificar o workspace:
   - `repo materializado`
   - `baseline de geracao`
5. Ler apenas o template alvo e os artefatos estritamente necessarios
6. Explicar o plano curto antes da escrita quando houver mudanca estrutural

Regras de escrita:

- preferir o menor documento que ainda seja util
- nao copiar texto explicativo do template sem necessidade
- quando o dado nao existir, usar somente `Pendente de validacao`
- nao repetir a mesma governanca em todos os documentos
- cada documento deve ter papel distinto
- em Windows-only, usar exemplos PowerShell e evitar `ls`, `cat`, `pwd` e similares
- se a plataforma nao estiver validada, usar linguagem neutra
- se faltar informacao real, omitir detalhe em vez de inventar

Critério de qualidade:

- nota minima esperada: `80/100`
- se o resultado estiver prolixo, repetitivo, genérico ou com plataforma errada, revisar antes de concluir
