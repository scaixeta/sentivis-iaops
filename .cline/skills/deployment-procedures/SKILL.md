---
name: deployment-procedures
description: Procedimentos de deploy seguro para serviços MCP com validação pré/pós-deploy, rollback e evidências operacionais.
---
# Deployment Procedures

## Quando usar
Usar para planejar ou executar deploy controlado com risco reduzido.

## Procedimento
1) Validar readiness: build, teste, configuração.
2) Definir janela, plano de rollback e check pós-deploy.
3) Executar deploy conforme fluxo do projeto.
4) Confirmar saúde do serviço e registrar evidência.

## Restrições DOC2.5
- Não fazer deploy sem critérios de aceite.
- Não pular validação pós-deploy.
- Commit/push apenas com comando do PO.

## Dependências
- Pipeline CI/CD operacional
- Checklists em `docs/OPERATIONS.md`
