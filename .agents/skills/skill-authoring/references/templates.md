# Templates Minimos

## 1. Template de `SKILL.md`

```md
---
name: nome-da-skill
description: Use quando o usuario pedir <gatilhos reais>, incluindo <variacoes>. Nao use para <exclusoes>.
---

# Skill: Nome da Skill

Use esta skill quando...

## Objetivo

Explique o resultado esperado em 1 a 3 linhas.

## Fluxo

1. Identificar escopo e runtime alvo.
2. Ler apenas o contexto necessario.
3. Executar o workflow principal.
4. Validar evidencias e saida.

## Regras

- Limite 1
- Limite 2

## Done when

- criterio 1
- criterio 2

## Referencias

- `references/arquivo-util.md`
```

## 2. Trecho para `AGENTS.md`

```md
## Mandatory skill usage
- Se o pedido envolver criar ou atualizar skills: use `$skill-authoring`.
```

## 3. Trecho para `GEMINI.md`

```md
## Fluxos recomendados
- Para criar ou revisar skills: ver `skill-authoring`
```

## 4. Regra pratica de distribuicao

- `SKILL.md`: workflow sob demanda
- `references/`: detalhe que pode ser lido depois
- `scripts/`: mecanica deterministica
- `assets/`: arquivo usado na entrega
- `AGENTS.md` ou `GEMINI.md`: politica persistente
