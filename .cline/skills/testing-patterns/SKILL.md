---
name: testing-patterns
description: Padrões de teste para MCP-Projects com foco em qualidade, cobertura útil e registro de bugs/testes por sprint no modelo DOC2.5.
---
# Testing Patterns

## Quando usar
Usar para criar ou revisar testes unitários/integrados/e2e e para organizar evidências de validação de funcionalidades.

## Procedimento
1) Definir escopo do teste: comportamento, regressão e critérios de aceite.
2) Priorizar casos críticos e bordas reais do fluxo.
3) Implementar/ajustar testes no projeto alvo, sem expandir escopo.
4) Registrar bugs/testes no `tests/bugs_log.md` do projeto quando aplicável.

## Restrições DOC2.5
- Não registrar resultados fora do projeto atual.
- Não marcar como concluído sem evidência de execução.
- Commit somente por comando do PO.

## Dependências
- Framework de teste do projeto alvo
- Acesso ao código e aos logs do serviço testado
