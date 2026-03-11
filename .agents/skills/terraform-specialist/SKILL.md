---
name: terraform-specialist
description: Práticas de IaC com Terraform/OpenTofu para infra reproduzível, segura e auditável no contexto MCP.
---
# Terraform Specialist

## Quando usar
Usar para criação/revisão de infraestrutura declarativa e gestão de estado.

## Procedimento
1) Revisar módulos e variáveis por ambiente.
2) Validar `fmt`, `validate` e plano antes de aplicar.
3) Revisar impacto do `plan` com foco em risco.
4) Aplicar somente sob autorização explícita.

## Restrições DOC2.5
- Não aplicar mudanças em produção sem autorização.
- Não versionar credenciais/segredos.
- Commit só por ordem do PO.

## Dependências
- Terraform/OpenTofu
- Backend de estado configurado
