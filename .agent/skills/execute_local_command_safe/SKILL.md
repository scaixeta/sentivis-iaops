---
name: execute_local_command_safe
description: Executar apenas comandos locais de leitura e inspecao segura para levantar contexto do projeto.
---

Use quando precisar obter fatos do workspace sem alterar estado.

Execute:

1. Priorizar comandos de leitura como `git status`, `git log`, `git show`, `git branch`, `rg`, `ls` e leitura de arquivos
2. Reunir apenas a evidencia necessaria para responder ao pedido
3. Resumir o resultado em linguagem direta e objetiva

Regras:

- Esta skill cobre somente leitura
- Nao executar comandos destrutivos ou mutacoes de Git
- Se o proximo passo exigir alteracao, voltar ao gate de aprovacao correspondente

