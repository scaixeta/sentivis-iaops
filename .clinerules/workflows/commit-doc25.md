---
description: Workflow de commit genérico seguindo o padrão DOC2.5.
---

# Workflow de Commit (DOC2.5)

Use este workflow quando um ciclo de desenvolvimento e documentação estiver completo e o PO emitir comando expresso de commit.

**Política de Commits:** Ver `.clinerules/WORKSPACE_RULES_GLOBAL.md` Seção 3.8  
**Commit é decisão EXCLUSIVA do PO via comando expresso. Agente NUNCA sugere ou questiona.**

## Escopo do Projeto

- **Workspace root**: `[Pasta Atual do Usuário]` (Dinâmico - Derive do contexto)
- **Projeto**: `[Nome do Projeto Atual]` (Dinâmico)
- **Sprint ativa**: `Dev_Tracking_SX.md` (raiz do projeto)
- **Arquivo de sprints**: `Sprint/Dev_Tracking_SX.md` (arquivadas)
- **Controle de Sprints**: `README.md` seção "Controle de Sprints"
- **Regras globais**: `.clinerules/WORKSPACE_RULES_GLOBAL.md`

## Objetivos

- Criar commits seguros e organizados alinhados com a sprint ativa
- Usar mensagens no padrão `SX-YY: descrição em português` ou `SX-END: resumo em português`
- Atualizar `Dev_Tracking_SX.md` com informações de commit
- Atualizar tabela "Controle de Sprints" no `README.md`
- **NUNCA** executar comandos git sem aprovação explícita do usuário

## Sequência de Execução

### 1. Carregar Contexto (DOC2.5)
- Leia `.clinerules/WORKSPACE_RULES_GLOBAL.md` para entender todas as regras DOC2.5
- Verifique `README.md` seção "Controle de Sprints" para identificar sprint ativa
- Abra `Dev_Tracking_SX.md` e entenda:
  - Items do backlog e seus status
  - Decisões recentes que podem afetar commits
  - Objetivos da sprint e status de conclusão

### 2. Inspecionar Status Git (Somente Leitura)
- Proponha o comando exato: `git status` ou `git status --short`
- **NÃO use `git diff` por padrão** (apenas se explicitamente solicitado)
- Após aprovação do usuário, execute e resuma:
  - Arquivos rastreados modificados
  - Arquivos novos não rastreados
  - Arquivos deletados
  - Branch atual e estado ahead/behind
- Pergunte ao usuário quais arquivos devem ser incluídos

### 3. Planejar Commits e Mensagens (DOC2.5)
- Com base nas escolhas do usuário, agrupe arquivos logicamente:
  - Atualizações de templates DOC2.5
  - Mudanças de documentação (`docs/`)
  - Atualizações de regras (`.clinerules/`, `rules/`)
  - Atualizações de tracking de sprint
- Para cada commit planejado, proponha mensagem no padrão DOC2.5:
  - `SX-YY: alinhamento de template ao DOC2.5`
  - `SX-YY: atualização de documentação DOC2.5`
  - `SX-YY: atualização de regras para conformidade DOC2.5`
  - `SX-END: resumo de encerramento da sprint`
- Mostre o mapeamento: Commit 1: mensagem + lista de arquivos
- **Aguarde aprovação explícita antes de fazer staging ou commit**

### 4. Staging de Arquivos (DOC2.5)
- Para cada commit planejado:
  - Prepare lista de arquivos para staging
  - Proponha o comando exato `git add` que será executado
- Após aprovação do usuário, execute os comandos de staging
- Opcionalmente mostre `git status --short` para verificação

### 5. Criar Commits (DOC2.5)
- Para cada commit:
  - Apresente a mensagem final seguindo padrão DOC2.5
  - Peça aprovação final
  - Execute `git commit -m "<mensagem>"` SOMENTE após aprovação
- Após todos os commits, execute `git status` e resuma o resultado

### 6. Atualizar Dev_Tracking_SX.md (DOC2.5)

**Atualizações do Backlog:**
- Marque items completos: `To-Do | ST-SX-YY – descrição` → `Done | ST-SX-YY – descrição`
- Referencie commits: `Done | ST-SX-YY – descrição (commits: abc123, def456)`

**Registro de Decisões:**
- Adicione: `[D-SX-YY] [data] – decisão de consolidação de commit`
  - Impacto: Mudanças commitadas com mensagens baseadas em sprint
  - Arquivos afetados: [lista de arquivos commitados]

**Atualizações de Status:**
- Rastreie progresso de conclusão da sprint
- Adicione evidência de commits para encerramento de sprint

### 7. Atualizar README.md "Controle de Sprints" (DOC2.5)
Para commits significativos ou conclusão de sprint:
- Atualize status da sprint para "Encerrada" se apropriado
- Adicione evidência de commit (hash/refs) na coluna apropriada
- Atualize duração se a sprint estiver sendo encerrada
- Garanta formato da tabela conforme DOC2.5:
  - Nome da Sprint, Objetivo, Entregas, Bugs, Estado, Evidência de commit, Duração, Link para arquivo da sprint

### 8. Opcional: Push para Remoto (Politica de Remotes)
Somente se o usuário explicitamente solicitar ou confirmar:
- **Identifique Remotes**: Execute `git remote -v`.
- **Lógica de Decisão:**
  - Se houver apenas um remote identificavel: **Planeje push para ele**.
  - Se houver multiplos remotes:
    - Operar em `single remote` por padrao
    - Usar `dual remote` apenas se o PO determinar explicitamente
    - Se PO especificou um destino: **Planeje push apenas para o solicitado**
  - Se nao houver remote identificavel ou houver ambiguidade: **Questione o PO antes de prosseguir**
- **Execução:**
  - Proponha os comandos exatos (ex: `git push origin <branch>; git push gitlab <branch>`).
  - Peça aprovação e execute.
- **Registro:**
  - Atualize `Dev_Tracking_SX.md` informando que commits foram enviados (e para quais remotes).

## Política Git (DOC2.5)

**NÃO use `git diff` por padrão**
- Use `git status` ou `git status --short` para inspecionar mudanças
- Mostre diffs apenas se explicitamente solicitado
- Mensagens de commit devem referenciar sprint: `SX-YY: descrição em português` ou `SX-END: resumo em português`

## Proteções e Segurança (DOC2.5)

- Nunca adivinhe o repo root: se houver ambiguidade, pergunte ao usuário. **Confirme sempre o caminho atual.**
- Nunca faça staging ou commit de mais arquivos do que o usuário aprovou
- Nunca reescreva histórico (sem `git reset --hard`, `git push --force`, etc.) a menos que o usuário claramente peça
- Não modifique `.clinerules/` ou regras de workspace deste workflow a menos que explicitamente instruído
- Respeite padrões e proibições DOC2.5 durante processo de commit

## Critérios de Conclusão

- Todas as mudanças pretendidas foram staged e commitadas com mensagens DOC2.5 aprovadas pelo usuário
- `git status` mostra o estado limpo esperado
- Backlog em `Dev_Tracking_SX.md` reflete items completos com referências de commit
- Tabela "Controle de Sprints" do README.md atualizada com evidência de commit se significativo
- Nenhuma operação git foi executada sem aprovação prévia do usuário
