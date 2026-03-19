# Checklist de Design de Skill

Use este checklist antes de considerar a skill pronta.

## 1. Roteamento

- O `name` e o nome do diretorio sao coerentes.
- A `description` explica quando usar.
- A `description` explica quando NAO usar, se houver risco de ativacao indevida.
- Os gatilhos citam linguagem que usuarios realmente usam.

## 2. Progressive Disclosure

- O `SKILL.md` ficou enxuto e operacional.
- Detalhes extensos foram movidos para `references/`.
- Conteudo deterministico e repetitivo foi movido para `scripts/`.
- Somente arquivos necessarios foram criados.

## 3. Estrutura

- A skill nao criou documentacao paralela desnecessaria.
- `references/` contem material que faz sentido ler sob demanda.
- `assets/` so existe se houver artefato de saida a reutilizar.
- Qualquer metadata extra foi mantida apenas se o runtime realmente a usa.

## 4. Governanca

- O conteudo respeita os padroes locais do workspace.
- Nao ha duplicacao inutil entre `.agents`, `.codex` e `.cline`.
- O espelhamento foi feito apenas para registries ja existentes.
- O texto separa claramente regra persistente, workflow e execucao real.

## 5. Qualidade

- A skill descreve um caminho feliz claro.
- As restricoes evitam erros comuns.
- Ha exemplos ou templates suficientes para reduzir ambiguidade.
- O `Done when` e verificavel.

## 6. Escalada Correta

Leve algo para `AGENTS.md` ou `GEMINI.md` quando:
- a regra deve valer sempre no repo
- a skill precisa ser obrigatoria em certos cenarios
- a instrucao nao e sob demanda, e sim politica do projeto

Leve algo para MCP ou script quando:
- a acao depende de sistema externo
- a sequencia precisa ser deterministica
- o mesmo codigo seria reescrito varias vezes
