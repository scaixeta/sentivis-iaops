---
name: gitlab-ci-patterns
description: Padrões de pipeline GitLab CI para build/test/deploy com estágios rastreáveis e execução confiável.
---
# GitLab CI Patterns

## Quando usar
Usar para definir ou ajustar `.gitlab-ci.yml` em fluxos de integração e entrega contínua.

## Procedimento
1) Definir estágios e regras de execução.
2) Encadear jobs com artefatos e dependências.
3) Validar comportamento por branch e merge request.
4) Medir tempo de pipeline e gargalos principais.

## Restrições DOC2.5
- Não alterar estratégia de release sem alinhamento do PO.
- Não introduzir jobs sem objetivo claro.
- Commit/push apenas sob ordem do PO.

## Dependências
- Runner GitLab disponível
- Variáveis CI configuradas
