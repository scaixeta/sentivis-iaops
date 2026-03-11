---
name: doc25-dual-remote-policy
description: Validar a politica de remotes do repositorio antes de qualquer commit/push; operar em single remote por padrao e usar dual remote apenas quando o PO determinar.
---
# Politica de Remotes DOC2.5

## Quando usar
Usar quando o usuario mencionar commitabilidade, dual remote, remote faltando, push bloqueado, ou pedir para preparar um commit/push.

## Procedimento
1) Executar: `git remote -v`
2) Identificar os remotes realmente configurados no repositorio atual.
3) Gerar relatório curto de "Commitabilidade":
   - Branch atual
   - Resumo de arquivos alterados
   - Status dos remotes
   - BLOQUEADO / OK
   - Comandos de remediação (não executar sem autorização do PO)
4) NÃO alterar remotes sem autorização explícita do PO.
5) Se houver apenas um remote identificavel: operar em `single remote`.
6) Se houver mais de um remote:
   - usar `single remote` por padrao
   - usar `dual remote` apenas quando o PO determinar explicitamente
7) Se PO especificar destino: obedecer estritamente.
8) Se nao houver remote identificavel: parar e perguntar ao PO antes de prosseguir.
