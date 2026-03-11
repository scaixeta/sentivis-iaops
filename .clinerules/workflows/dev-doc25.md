---
description: Workflow de desenvolvimento genérico (padrão DOC2.5).
---

# Workflow de Desenvolvimento (DOC2.5)

Use este workflow para executar tarefas completas de desenvolvimento, sempre respeitando as regras de workspace e atualizando a sprint ativa.

## Escopo do Projeto

- **Workspace root**: `[Pasta Atual do Usuário]`
- **Projeto principal**: `[Nome do Projeto Atual]`
- **Sprint ativa**: `Dev_Tracking_SX.md` (onde SX é a sprint atual, ex: S1)
- **Arquivo de sprints**: `Sprint/Dev_Tracking_SX.md` (arquivadas)
- **Log de testes/bugs**: `tests/bugs_log.md`
- **Controle de Sprints**: `README.md` seção "Controle de Sprints"
- **Regras globais**: `.clinerules/WORKSPACE_RULES_GLOBAL.md`
- **Regras locais**: `rules/WORKSPACE_RULES.md`
- **Pasta de docs**: `docs/` (4 documentos canônicos)
- **Pasta de templates**: `.clinerules/templates/doc25/` (fonte canônica, acessada diretamente via workflow)

## Objetivos

- Planejar e executar o conjunto mínimo de mudanças de código/config/docs necessárias
- Manter tudo rastreável no `Dev_Tracking_SX.md` ativo com:
  - Atualizações de backlog: `STATUS | ST-SX-YY – descrição`
  - Decisões: `[D-SX-YY] [data] – descrição da decisão`
  - Referências de bug/teste: `BUG-SX-YY – título curto – ver tests/bugs_log.md (Sprint SX)`
- Referenciar mudanças da sprint na tabela "Controle de Sprints" do README.md
- Nunca pular aprovação do usuário para ações perigosas

## Inputs Necessários do Usuário

Antes de começar, pergunte e confirme:

1. Título curto para a tarefa (será reutilizado no backlog da sprint e mensagens de commit)
2. A pasta principal do projeto se não for óbvia
3. O escopo:
   - Quais arquivos ou áreas estão no escopo
   - Quaisquer restrições rígidas (não tocar em X, Y, Z)
   - Se testes ou scripts devem ser executados no final

Se algo for ambíguo, pergunte para esclarecer antes de editar.

## Sequência de Execução

### 1. Carregar Regras e Contexto (DOC2.5)
- Leia `.clinerules/WORKSPACE_RULES_GLOBAL.md` e obedeça todas as restrições
- Leia `rules/WORKSPACE_RULES.md` para regras específicas do projeto (se existir)
- Verifique `README.md` seção "Controle de Sprints" para identificar sprint ativa
- Localize e leia `Dev_Tracking_SX.md` (sprint ativa)
- Leia `tests/bugs_log.md` se relevante para a tarefa atual
- Consultar `.clinerules/templates/doc25/` como fonte canônica quando a tarefa incluir documentação
- Entenda backlog atual, objetivos e decisões recentes

### 2. Resumir e Planejar (DOC2.5)
- Reafirme o objetivo do usuário com suas próprias palavras
- Proponha um plano curto com passos numerados, por exemplo:
  - Passo 1: Inspecionar arquivos A, B, C
  - Passo 2: Implementar mudança no arquivo X
  - Passo 3: Atualizar backlog em Dev_Tracking_SX.md (marcar item como Done/Accepted)
  - Passo 4: Adicionar registro de decisão `[D-SX-YY]` se necessário
  - Passo 5: Atualizar README.md "Controle de Sprints" se mudanças significativas
  - Passo 6: Executar testes/scripts se solicitado
- Apresente este plano ao usuário e aguarde aprovação explícita antes de executar

### 3. Inspecionar e Projetar Mudanças
- Use ferramentas de busca e leitura para:
  - Localizar código, configs ou docs relevantes
  - Entender padrões existentes no projeto
- Se um padrão ou exemplo existente já resolve problema similar, proponha reutilizá-lo
- Antes de editar, descreva:
  - Quais arquivos você irá mudar
  - Que tipo de mudanças (nova função, refatoração, config, ajuste pequeno de doc)
  - Como backlog e decisões serão atualizados

### 4. Aplicar Mudanças Incrementalmente
- Edite arquivos em passos pequenos e revisáveis
- Após cada edição não trivial, mostre resumo conciso usando `git status` (**NÃO `git diff` por padrão**)
- Evite tocar em arquivos fora do escopo
- Não modifique `.clinerules/` ou regras globais a menos que explicitamente solicitado

### 5. Executar Verificações e Testes
- Se o usuário solicitou verificações (lint, testes unitários, scripts), proponha o(s) comando(s) exato(s) que planeja executar
- Execute comandos somente após aprovação do usuário
- Resuma resultados ao invés de despejar logs brutos

### 6. Atualizar Dev_Tracking_SX.md (DOC2.5)

**Atualizações do Backlog:**
- Atualizar status: `To-Do | ST-SX-YY – descrição` → `Done | ST-SX-YY – descrição`
- Adicionar novos items: `To-Do | ST-SX-YY – descrição do novo item`

**Registro de Decisões:**
- Adicionar: `[D-SX-YY] [data] – descrição da decisão`
  - Impacto:
  - Arquivos afetados:

**Referências de Bug/Teste:**
- Adicionar: `BUG-SX-YY – título curto – ver tests/bugs_log.md (Sprint SX)`
- Referenciar resultados de testes ou incidentes

**Atualizações de Status:**
- Manter rastreamento da conclusão de objetivos
- Adicionar contexto para próxima sprint se items forem movidos

### 7. Atualizar README.md "Controle de Sprints" (se mudanças significativas)
- Atualizar status ou duração da sprint se aplicável
- Adicionar evidência de commit (hash/refs) quando mudanças são commitadas
- Garantir que colunas da tabela permaneçam consistentes com formato DOC2.5

### 8. Critérios de Conclusão (DOC2.5)
- As edições planejadas foram aplicadas e revisadas com o usuário
- Todas as verificações acordadas foram executadas e resumidas
- Backlog em `Dev_Tracking_SX.md` foi atualizado com status atual
- Decisões estão registradas no formato correto
- Referências de bug/teste estão devidamente cross-referenciadas
- README.md "Controle de Sprints" atualizado se mudanças significativas ocorreram
- Você confirma explicitamente que o workflow de dev está completo

## Política Git (DOC2.5)

**NÃO use `git diff` por padrão**
- Use `git status` ou `git status --short` para inspecionar mudanças
- Mostre diffs apenas se explicitamente solicitado pelo usuário
- Mensagens de commit devem referenciar sprint: `SX-YY: descrição em português` ou `SX-END: resumo em português`

## Proteções e Segurança (DOC2.5)

- Nunca busque documentação externa ou navegue na internet neste workflow
- Sempre pergunte antes de:
  - Executar comandos shell
  - Instalar dependências
  - Realizar operações git
- Se algo falhar ou não estiver claro, pare, explique a situação e pergunte ao usuário como proceder
- Respeite proibições DOC2.5:
  - Sem seções "Lições aprendidas" em arquivos de sprint
  - Sem campos "PO AI:" ou "MLE:" em arquivos de sprint
  - Sem referências a "Épico"
  - Backlog como linhas simples, não tabelas complexas
