---
name: github-actions-templates
description: Padrões de CI/CD com GitHub Actions para build, teste e validação segura em projetos MCP.
---
# GitHub Actions Templates

## Quando usar
Usar para criar ou revisar pipelines CI/CD no GitHub com foco em qualidade e previsibilidade.

## Procedimento
1) Mapear jobs mínimos: lint, test, build.
2) Definir gates por branch/PR.
3) Configurar cache e artefatos essenciais.
4) Validar falhas comuns e mensagens de diagnóstico.

## Restrições DOC2.5
- Não acoplar segredos fora dos padrões do repositório.
- Não liberar deploy automático sem aprovação explícita.
- Commits somente por comando do PO.

## Dependências
- Repositório GitHub configurado
- Secrets definidos no projeto
