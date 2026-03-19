# Notas por Runtime

Estas notas ajudam a Cindy a posicionar a skill no lugar certo sem inventar novos registries.

## Canonico da Cindy

- `.agents/skills/<skill-name>/` e a fonte primaria de autoria das skills comuns.
- `.codex/skills/<skill-name>/` e `.cline/skills/<skill-name>/` sao counterparts de runtime.

## Regra de espelhamento

- Primeiro identifique qual registry e canonico no projeto atual.
- Depois replique somente para os registries que realmente existem.
- Se houver diferenca de runtime, ajuste apenas o minimo necessario.
- Se nao houver diferenca real, mantenha os arquivos iguais.

## Nota de complementaridade

- Use `skill-authoring` para criar ou revisar a skill.
- Use `mcp-builder` quando o trabalho for construir o servidor MCP que a skill pode acionar.
