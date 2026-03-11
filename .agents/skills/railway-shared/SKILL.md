---
name: railway-shared
description: Referencias e scripts compartilhados do pack Railway para suporte a outras skills do ecossistema Railway.
---

# Railway Shared

## Quando usar

Usar quando outra skill Railway precisar consultar referencias comuns ou reutilizar os scripts locais do pack Railway.

## Papel desta skill

Esta skill nao e um fluxo de acao isolado para o usuario final. Ela funciona como base compartilhada para:

- referencias em `references/`
- scripts de suporte em `scripts/`
- padroes comuns reutilizados por skills Railway

## Conteudo compartilhado

- `references/environment-config.md`
- `references/monorepo.md`
- `references/railpack.md`
- `references/variables.md`
- `scripts/railway-api.sh`
- `scripts/railway-common.sh`

## Regras de uso

- usar esta skill como apoio para outras skills Railway
- nao assumir deploy, alteracao de ambiente ou push sem pedido explicito do PO
- priorizar leitura das referencias antes de executar qualquer script relacionado
