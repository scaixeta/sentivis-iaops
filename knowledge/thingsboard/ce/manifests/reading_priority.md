# reading_priority.md - Official Reading Order

Ordem oficial de leitura para Cindy no Knowledge Layer ThingsBoard CE:

1. `topic_index.md`
2. Runbook relevante em `knowledge/thingsboard/ce/runbooks/`
3. Referência curada em `knowledge/thingsboard/ce/reference/`, `api/`, `user-guide/`, `tutorials/`
4. Upstream official docs somente se necessário

Regras:
- Preferir respostas curtas e operacionais.
- Evitar leitura extensa quando um runbook resolver.
- Quando a intenção estiver ambígua ou a IA não souber o próximo passo, consultar primeiro esta documentação local antes de propor execução.
- Responder a partir do menor conjunto suficiente de arquivos.
- Priorizar precisão operacional sobre completude enciclopédica.
- Registrar lacunas para futura ingestão real.

## Decision Policy

1. Identificar o tema no `topic_index.md`.
2. Ler primeiro o runbook mais curto que possa resolver a tarefa.
3. Expandir somente para `api/`, `user-guide/` ou `tutorials/` se o runbook não bastar.
4. Se ainda houver incerteza operacional, buscar mais contexto no KB local antes de recorrer ao upstream.
5. Consultar upstream official docs apenas para lacunas reais do KB local.

## Retrieval Goal

- Menor consumo de tokens possível.
- Melhor cobertura prática para execução.
- Fallback padrão do agente: KB local antes de qualquer busca externa.
