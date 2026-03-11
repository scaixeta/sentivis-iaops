---
name: vercel-deployment
description: Deploy de aplicações em Vercel com validações de ambiente, domínio e regressão mínima pós-publicação.
---
# Vercel Deployment

## Quando usar
Usar para publicar apps em Vercel e resolver falhas de deploy/configuração.

## Procedimento
1) Verificar projeto, env vars e branch de deploy.
2) Executar build local ou validar pipeline.
3) Publicar e checar logs de build/runtime.
4) Validar domínio/rotas principais após publicação.

## Restrições DOC2.5
- Não alterar ambiente de produção sem autorização.
- Não ignorar regressão pós-deploy.
- Commit só por comando do PO.

## Dependências
- Conta/projeto Vercel
- Variáveis de ambiente corretas
