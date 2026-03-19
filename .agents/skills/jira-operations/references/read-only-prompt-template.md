# Prompt Template Read-Only

Use este modelo quando quiser que a Cindy opere Jira sem qualquer alteracao.

```text
Use a skill `jira-operations` em modo estritamente read-only.

Objetivo:
- Investigar o estado atual de issues no Jira sem modificar nada.

Escopo:
- Projeto/board: <preencher>
- Filtro ou issues-alvo: <preencher>

Regras:
- Nao criar issues
- Nao comentar
- Nao transicionar status
- Nao editar campos
- Nao alterar labels
- Nao atribuir assignee
- Apenas ler e resumir

Entregue:
- resumo do estado atual
- bloqueios
- prioridades percebidas
- proxima acao sugerida sem executar nada
```
