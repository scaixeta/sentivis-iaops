---
name: workflow-patterns
description: Aplicação de workflows operacionais (init, docs, dev, commit) com checkpoints de qualidade e governança DOC2.5.
---
# Workflow Patterns

## Quando usar
Usar para conduzir execução por etapas com checkpoints claros e evidência de conclusão.

## Procedimento
1) Identificar workflow aplicável e objetivo.
2) Confirmar pré-condições (contexto, arquivos-alvo, critérios de aceite).
3) Executar por fases com validação intermediária.
4) Registrar resultado e pendências do ciclo.

## Restrições DOC2.5
- Não misturar workflows sem necessidade.
- Não avançar fase sem validação da anterior.
- Commit/push somente com comando do PO.

## Dependências
- Regras em `.clinerules/workflows/`
- Documentação do projeto alvo
