---
name: skill-authoring
description: Criar, revisar ou refatorar skills da Cindy, incluindo SKILL.md, description de roteamento, references/scripts/assets, espelhamento entre runtimes e validacao da skill antes da entrega.
---

# Skill: Skill Authoring

Use esta skill quando o pedido envolver criar uma skill nova, atualizar uma skill existente, organizar um catalogo de skills, melhorar o roteamento por `description`, ou ensinar a Cindy a fazer skills com qualidade.

## Objetivo

Entregar uma skill enxuta, ativavel pelos gatilhos certos, facil de manter e coerente com o runtime alvo.

## Fluxo

1. Identificar o job da skill em uma frase:
   - o que ela faz
   - quando deve ser usada
   - quando NAO deve ser usada
2. Inspecionar o workspace antes de criar estrutura nova:
   - procurar skills similares
   - respeitar nomes, pastas e convencoes ja adotadas
   - evitar duplicar catalogos paralelos
3. Definir o pacote minimo:
   - `SKILL.md` obrigatorio
   - `references/` para detalhe que nao precisa ficar sempre em contexto
   - `scripts/` apenas para mecanicas deterministicas ou repetitivas
   - `assets/` apenas para artefatos usados na saida, nao para documentacao
4. Escrever `name` e `description` como contrato de roteamento:
   - `name` deve ser estavel, curto e compativel com o diretorio
   - `description` deve citar gatilhos reais, escopo e exclusoes
   - se o routing estiver fraco, corrigir metadata antes de adicionar mais texto
5. Manter o `SKILL.md` enxuto:
   - explicar workflow, decisoes e restricoes
   - mover exemplos longos, templates e checklists para `references/`
   - nao repetir contexto persistente que pertence a `AGENTS.md` ou `GEMINI.md`
6. Decidir a camada correta para cada tipo de instrucao:
   - regras persistentes do repo em `AGENTS.md` ou `GEMINI.md`
   - workflow sob demanda em `SKILL.md`
   - integracao externa real em scripts ou MCP, nao em texto descritivo
7. Se o pedido for para criar um servidor MCP, complementar com `mcp-builder` em vez de duplicar responsabilidade nesta skill.
8. Se o workspace operar com multiplos runtimes, espelhar a skill apenas nos registries ja existentes e manter o mesmo conteudo base.
9. Validar antes de concluir usando o checklist em `references/skill-design-checklist.md`.

## Regras

- Nao criar `README.md`, changelog ou documentacao auxiliar fora do pacote necessario da skill.
- Nao inflar o `SKILL.md` com teoria generica que o modelo ja sabe.
- Nao duplicar o mesmo conteudo em `SKILL.md` e `references/`.
- Nao criar `scripts/` se um procedimento textual curto resolver.
- Nao prometer compatibilidade com um runtime sem verificar estrutura e precedencia local.
- Quando houver exemplos, use exemplos curtos e diretamente reutilizaveis.

## Entregaveis minimos

- `SKILL.md` com metadata clara e workflow acionavel
- pelo menos uma referencia util quando isso reduzir ambiguidade
- criterio de `Done when` verificavel
- espelhamento consistente quando o workspace ja usar mais de um runtime

## Done when

- a skill tem `name` e `description` bons o suficiente para roteamento
- o `SKILL.md` explica o caminho feliz, limites e onde buscar detalhe
- `references/`, `scripts/` e `assets/` foram usados so quando agregam valor real
- a skill foi colocada nos destinos corretos do workspace sem criar estruturas paralelas
- a validacao final confirma clareza, progressive disclosure e coerencia operacional

## Referencias

- `references/skill-design-checklist.md`
- `references/templates.md`
- `references/runtime-notes.md`
