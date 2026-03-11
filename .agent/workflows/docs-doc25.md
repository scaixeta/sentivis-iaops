---
description: Workflow para criação e atualização de documentação oficial (DOC2.5).
---

# Workflow de Documentação (DOC2.5)

Este workflow garante que a documentação siga os templates canônicos DOC2.5 e as regras de governança ao criar ou atualizar documentação do projeto.

## Escopo do Projeto

- **Workspace root**: `[Pasta Atual do Usuário]`
- **Projeto**: `[Nome do Projeto Atual]`
- **Raiz de docs**: `docs/`
  - **Docs oficiais** (alvo deste workflow):
    - `docs/SETUP.md` (estrutura inicial DOC2.5)
    - `docs/ARCHITECTURE.md` (arquitetura de governança DOC2.5)
    - `docs/DEVELOPMENT.md` (fluxo DOC2.5)
    - `docs/OPERATIONS.md` (registro de incidentes DOC2.5)
  - **Nota**: `docs/README.md` NÃO é doc oficial por modelo canônico DOC2.5. Ponto de entrada é `README.md` (raiz)
- **Templates** (modelos DOC2.5): `.clinerules/templates/doc25/` (fonte canônica, usada diretamente via workflow)
- **Sprint ativa**: `Dev_Tracking_SX.md`
- **Arquivo de sprints**: `Sprint/Dev_Tracking_SX.md` (arquivadas)
- **Log de testes/bugs**: `tests/bugs_log.md`
- **Regras globais**: `.clinerules/WORKSPACE_RULES_GLOBAL.md`
- **Regras locais**: `rules/WORKSPACE_RULES.md`

## Objetivos

- Atualizar um ou mais docs em `docs/` para refletir realidade atual do projeto
- Seguir estilo e estrutura de documentação DOC2.5 definidos em templates e regras de workspace
- Usar templates como fonte canônica para estrutura
- Derivar conteúdo primariamente de:
  - Arquivo de sprint ativa (`Dev_Tracking_SX.md`)
  - Docs existentes
  - Estrutura do projeto
  - Instruções do usuário
- Manter tudo rastreável no `Dev_Tracking_SX.md` ativo
- Atualizar tabela "Controle de Sprints" do README.md para mudanças significativas de documentação

## Inputs Necessários do Usuário

Pergunte e confirme:

1. Qual(is) documento(s) em `docs/` deve(m) ser atualizado(s) (nomes e paths)
2. O foco principal para cada doc (por exemplo):
   - README: escopo, narrativa de alto nível e tabela "Controle de Sprints"
   - SETUP: ambiente, pré-requisitos, setup passo-a-passo + estrutura DOC2.5
   - DEVELOPMENT: como trabalhar no código, executar ferramentas, workflows, etc. (DOC2.5)
   - ARCHITECTURE: arquitetura de alto nível, componentes chave, fluxo de dados + governança DOC2.5
   - OPERATIONS: como operar, monitorar e manter a solução + registro de incidentes
3. Se a atualização é:
   - uma pequena mudança incremental, ou
   - uma grande reescrita baseada na realidade atual usando templates DOC2.5

## Sequência de Execução

### 1. Carregar Regras e Contexto (DOC2.5)
- Leia `.clinerules/WORKSPACE_RULES_GLOBAL.md` e obedeça todas as restrições DOC2.5
- Leia `rules/WORKSPACE_RULES.md` para regras específicas do projeto (se existir)
- Verifique `README.md` seção "Controle de Sprints" para identificar sprint ativa
- Localize e leia `Dev_Tracking_SX.md` (sprint ativa) para contexto recente
- Resolva templates obrigatoriamente nesta ordem:
  1. Usar `.clinerules/templates/doc25/` como fonte canônica de templates
  2. Se o projeto legado tiver `Templates/` local, consultar o PO sobre qual usar
  3. Se `.clinerules/templates/doc25/` estiver ausente, interromper e solicitar provisionamento ao PO
- Leia os templates relevantes diretamente de `.clinerules/templates/doc25/` para orientação de estrutura
- Para cada doc alvo, leia o arquivo atual em `docs/`

### 2. Derivar Plano de Documentação (DOC2.5)
- Para cada documento solicitado, compare conteúdo atual com template DOC2.5
- Proponha:
  - Seções para manter que se alinham com estrutura DOC2.5
  - Seções para adicionar baseadas em requisitos de template DOC2.5
  - Seções para atualizar ou mover para alinhar com DOC2.5
- Para cada seção, mapeie explicitamente para fonte de template DOC2.5:
  - "Esta seção será baseada na estrutura DOC2.5 de Templates/<arquivo>.md"
  - "Esta seção refletirá contexto atual da sprint de Dev_Tracking_SX.md"
- Mostre o plano ao usuário em lista de bullets concisa e aguarde aprovação

### 3. Rascunhar Documentação Atualizada (DOC2.5)
- Trabalhe doc-por-doc usando templates DOC2.5 como referência de estrutura
- Para cada doc:
  - Use a estrutura aprovada alinhada com templates DOC2.5
  - Preserve qualquer conteúdo validado importante que ainda esteja correto
  - Substitua ou remova seções que não se alinham com proibições DOC2.5:
    - Sem referências a "Épico"
    - Sem seções "Lições aprendidas"
    - Sem campos "PO AI:" ou "MLE:" em referências de sprint
    - Sem tabelas complexas em seções de backlog
  - Garanta que tabela "Controle de Sprints" use formato de colunas DOC2.5
- Quando precisar de informação que não está presente em:
  - Os docs
  - `Dev_Tracking_SX.md`
  - A estrutura do projeto
  - A mensagem do usuário
  
  Pergunte ao usuário ao invés de inventar

### 4. Revisar com Usuário Antes de Escrever
- Para cada doc, gere resumo de mudanças:
  - Adições chave baseadas em templates DOC2.5
  - Remoções chave para alinhar com proibições DOC2.5
  - Mudanças chave em referências de sprint e estrutura de tabela
- Mostre resumo de git status (**NÃO `git diff` por padrão**)
- Peça ao usuário para aprovar ou solicitar ajustes antes de finalizar as edições
- Escreva a versão final em disco somente após aprovação

### 5. Aplicar Edições aos Docs
- Edite cada doc alvo no lugar
- Garanta que cabeçalhos, listas e seções sejam consistentes com templates DOC2.5
- Evite duplicar o mesmo conteúdo longo em múltiplos docs; ao invés, faça referência cruzada lógica
- Mantenha consistência com requisitos de formato DOC2.5

### 6. Atualizar Dev_Tracking_SX.md (DOC2.5)

**Atualizações do Backlog:**
- Atualizar status: `To-Do | ST-SX-YY – descrição` → `Done | ST-SX-YY – descrição`
- Adicionar novos items: `To-Do | ST-SX-YY – descrição de atualização de documentação`

**Registro de Decisões:**
- Adicionar: `[D-SX-YY] [data] – decisão de atualização de documentação`
  - Impacto:
  - Arquivos afetados: docs/SETUP.md, docs/ARCHITECTURE.md, docs/DEVELOPMENT.md, docs/OPERATIONS.md (conforme aplicável)

**Referências de Bug/Teste:**
- Adicionar: `BUG-SX-YY – inconsistência de doc encontrada – ver tests/bugs_log.md (Sprint SX)`
- Referenciar testes de documentação ou problemas de validação

**Atualizações de Status:**
- Manter rastreamento da conclusão de objetivos de documentação
- Adicionar contexto para próxima sprint se items forem movidos

### 7. Atualizar README.md "Controle de Sprints" (se mudanças significativas)
- Atualizar status ou duração da sprint se mudanças de documentação forem significativas
- Adicionar evidência de commit (hash/refs) quando mudanças de documentação são commitadas
- Garantir que colunas da tabela permaneçam consistentes com formato DOC2.5:
  - Nome da Sprint, Objetivo, Entregas, Bugs, Estado, Evidência de commit, Duração, Link para arquivo da sprint

### 8. Critérios de Conclusão (DOC2.5)

- Todos os docs solicitados em `docs/` estão atualizados e consistentes com:
  - Regras de workspace DOC2.5
  - Templates DOC2.5
  - Contexto atual da sprint
  - Intenção do usuário
- Templates canônicos em `.clinerules/templates/doc25/` estão acessíveis e foram usados como referência
- Nenhuma fonte externa foi usada
- Backlog em `Dev_Tracking_SX.md` foi atualizado com status de documentação
- Tabela "Controle de Sprints" do README.md reflete quaisquer mudanças significativas
- Você confirma explicitamente que o workflow de docs está completo

## Política Git (DOC2.5)

**NÃO use `git diff` por padrão**
- Use `git status` ou `git status --short` para inspecionar mudanças
- Mostre diffs apenas se explicitamente solicitado pelo usuário
- Mensagens de commit devem referenciar sprint: `SX-YY: descrição em português` ou `SX-DOC: atualização de documentação em português`

## Proteções e Segurança (DOC2.5)

- Não navegue na internet neste workflow
- Não mude `.clinerules/` ou outros arquivos de regras a menos que explicitamente solicitado
- Não toque em código ou configs a menos que o usuário explicitamente peça pequenos ajustes
- Se o usuário pedir algo que contradiz regras de workspace DOC2.5, explique o conflito
- Respeite proibições DOC2.5:
  - Sem seções "Lições aprendidas" em qualquer documentação
  - Sem campos "PO AI:" ou "MLE:" em arquivos de sprint
  - Sem referências a "Épico" em backlog ou planejamento
  - Backlog como linhas simples, não tabelas complexas
- Sempre use templates para orientação de estrutura
