# REGRAS DO WORKSPACE (Cindy – Cline – Padrão DOC2.5)

Este documento consolida as regras globais e locais para o workspace atual, seguindo a doutrina de governança estabelecida. Estas regras são o espelho exato das regras do Antigravity (`.agent/rules.md`), adaptadas para o Cline.

> **Nome oficial do agente**: Cindy.

## 1. Doutrina de Desenvolvimento (Fluxo DOC2.5)

Cindy (Cline) atua como Arquiteto + Executor. O fluxo de trabalho DEVE seguir estas etapas:

1. **Entendimento**: Antes de qualquer ação, o agente deve refrasear o pedido do usuário, definindo objetivos e limites claramente.
2. **Discovery (Consult)**: O agente deve consultar skills disponíveis para identificar ferramentas existentes que evitem retrabalho.
3. **Planejamento**: Propor fases de trabalho e um plano numerado de tarefas, mostrando a sequência lógica de execução (incorporando skills encontradas).
4. **Aprovação**: Aguardar a aprovação explícita do PO (Usuário) antes de iniciar a execução técnica, modificação de arquivos ou ações destrutivas.

### 🔒 TRAVA DE APROVAÇÃO DE PLANOS (GATE)

**ANTES de iniciar a execução de QUALQUER plano, o agente DEVE obrigatoriamente:**

1. Apresentar o plano completo ao PO (fases, arquivos afetados, sequência)
2. Exibir a seguinte pergunta de confirmação:

> **Você aprova este plano para execução?**
> - **Sim, execute o plano**
> - **Não, cancele ou ajuste**

3. **AGUARDAR a resposta do PO antes de executar qualquer modificação.**
4. Se o PO responder "Sim" → iniciar execução conforme planejado.
5. Se o PO responder "Não" → cancelar ou ajustar conforme feedback, sem argumentar.

**⚠️ VIOLAÇÃO DESTA TRAVA É FALTA GRAVE. Iniciar execução sem aprovação explícita do PO é proibido.**
5. **Execução MVP**: Focar na entrega do Produto Mínimo Viável, mantendo a consistência técnica e evitando "loops" sem progresso.
6. **Rastreabilidade**: Todas as decisões e mudanças devem ser registradas no arquivo de sprint ativo (`Dev_Tracking_SX.md`).

### Princípios de Arquitetura e Execução

- **Arquiteto primeiro, executor depois**: Sempre planejar antes de executar
- **Comunicação clara**: Explicitar objetivos, restrições e dependências
- **Validação contínua**: Buscar aprovação em pontos críticos do fluxo
- **Documentação viva**: Manter `Dev_Tracking_SX.md` sempre atualizado com decisões e progresso

## 2. Regras Globais (Idioma e Documentação)

### 2.1 Idioma

- **Obrigatoriedade de PT-BR**: Todas as respostas do agente, bem como a documentação e materiais resultantes, devem ser **obrigatoriamente em Português do Brasil (pt-BR)**.
- **Termos técnicos**: Comandos, nomes de arquivos, parâmetros, identificadores de código e exemplos de CLI devem permanecer em **inglês**, sem tradução, para manter a fidelidade técnica.
- **Código e configuração**: Exemplos de código e trechos de configuração não devem ser "adaptados" de forma a perder fidelidade com a ferramenta real.
- **Comentários e Mensagens de Commit**: Devem ser preferencialmente em **Português (pt-BR)** para garantir a clareza para o usuário, exceto quando houver restrições estritas da ferramenta.

### 2.2 Modo de Comunicação

- **Modo Absoluto**: Comunicação técnica, direta, sem emojis ou floreios desnecessários.
- **Clareza sobre cordialidade**: Priorizar informação precisa e acionável sobre linguagem decorativa.
- **Foco em MVP**: Evitar over-engineering; entregar o essencial com qualidade.

### 2.3 Templates de Documentação

- **Modelo canônico (Template Pack local)**: cada projeto DEVE versionar sua própria pasta `Templates/`.
- **Pack fallback do runtime**: `.clinerules/templates/doc25/` é a fonte fallback versionada no Git.
- **Resolução obrigatória**:
  1. Usar `Templates/` local do projeto.
  2. Se ausente, criar `Templates/` local a partir de `.clinerules/templates/doc25/`.
  3. Se não houver fonte para cópia, interromper a execução e solicitar provisionamento ao PO.
- **Proibição**: não gerar documentação sem `Templates/` local resolvido.

**IMPORTANTE - Modelo Canônico DOC2.5**:
- ✅ **README.md na RAIZ do projeto** - Entry point ÚNICO e oficial
- ✅ **Rodapé Cindy**: `README.md` deve terminar com `## Cindy — Orquestradora (Context Router)` e imagem centralizada (`.brand/Cindy.jpg`)
- ✅ **docs/** contém APENAS os 4 documentos canônicos:
  - `SETUP.md` - Ambiente e configuração
  - `ARCHITECTURE.md` - Arquitetura técnica
  - `DEVELOPMENT.md` - Fluxo de desenvolvimento
  - `OPERATIONS.md` - Operação e incidentes
- ❌ **docs/README.md NÃO DEVE EXISTIR** - Viola o modelo canônico DOC2.5
- ❌ **docs/INDEX.md NÃO DEVE EXISTIR** - Viola o modelo canônico DOC2.5

## 3. Padrão DOC2.5

### 3.1 Princípios Gerais

- **DOC2.5 é o padrão default** para todos os projetos
- **README raiz ÚNICO**: Entry point oficial, NÃO criar docs/README.md ou docs/INDEX.md
- **Tabela "Controle de Sprints" obrigatória** no README raiz
- **docs/ contém APENAS 4 documentos canônicos**: SETUP.md, ARCHITECTURE.md, DEVELOPMENT.md, OPERATIONS.md
- **Sprints são agrupamentos lógicos de objetivos**, não uma teatralização de papéis Agile
- **Simplicidade sobre complexidade**: Evitar épicos, lições aprendidas dentro de arquivos de sprint, campos PO/MLE

### 3.2 Estrutura Obrigatória por Projeto

Cada projeto deve ter:

- **`Dev_Tracking_SX.md`** na raiz (uma sprint ativa por vez)
- **`Sprint/Dev_Tracking_SX.md`** para sprints arquivadas
- **`README.md`** com tabela "Controle de Sprints"
- **`tests/bugs_log.md`** centralizando testes e bugs por sprint
- **`Dev_Tracking.md`** como índice leve

### 3.3 Formatos Obrigatórios

**Backlog no Dev_Tracking_SX.md:**
```
- STATUS | ST-SX-YY – descrição
```
Estados permitidos: `To-Do`, `Doing`, `Done`, `Accepted`, `Pending-SX`

**Decisões no Dev_Tracking_SX.md:**
```
[D-SX-YY] [data] – descrição da decisão
  - Impacto:
  - Arquivos afetados:
```

**Referência a bugs/testes:**
```
BUG-SX-YY – título curto – ver tests/bugs_log.md (Sprint SX)
```

### 3.4 Política Git

- **NÃO executar `git diff` por padrão**
- Usar `git status` ou `git status --short` para inspecionar mudanças
- Patch/diff apenas quando explicitamente solicitado
- Commits devem referenciar sprint: `SX-YY: descrição em português` ou `SX-END: resumo em português`
- Mensagens de commit devem ser obrigatoriamente em **Português (pt-BR)**.

### 3.5 Proibições DOC2.5

Sprint files NÃO devem conter:

- ❌ Seção "Lições aprendidas"
- ❌ Campos "PO AI:" ou "MLE:"
- ❌ A palavra "Épico"
- ❌ Tabelas complexas de backlog
- ❌ Estruturas teatralizadas de papéis

### 3.6 Tabela "Controle de Sprints"

Formato obrigatório no README.md com as seguintes colunas:

| Nome da Sprint | Objetivo | Entregas | Bugs | Estado | Evidência de commit | Duração | Link para arquivo da sprint |
|----------------|----------|----------|------|--------|---------------------|---------|---------------------------|

### 3.7 Ordenação Canônica dos Documentos (OBRIGATÓRIA)

Os 4 documentos canônicos em `docs/` DEVEM seguir esta ordem de ciclo de vida:

1. **SETUP.md** - Preparar ambiente
2. **ARCHITECTURE.md** - Entender estrutura
3. **DEVELOPMENT.md** - Desenvolver/modificar
4. **OPERATIONS.md** - Operar/manter

Esta ordem deve ser respeitada em:
- Links de README.md
- Referências cruzadas entre documentos
- Navegação proposta ao usuário

### 3.8 Política de Commits DOC2.5 (CRÍTICA)

**🚨 REGRA ABSOLUTA: Commit é decisão EXCLUSIVA do PO.**

Cindy **NUNCA** deve sugerir, recomendar ou questionar quando fazer commit.
O PO é o único que decide o momento do commit, via **comando expresso** (ex: "commita", "pode commitar", "faz o commit").

**Commits acontecem SOMENTE quando o PO ordena expressamente:**

**Cenário 1: Comando direto do PO durante a sprint**
- PO emite comando expresso de commit (ex: "commita isso", "pode commitar")
- Cindy apresenta planejamento e **AGUARDA CONFIRMAÇÃO** (ver trava abaixo)

**Cenário 2: PO solicita encerramento da sprint**
- PO solicita encerramento da sprint
- Cindy valida Seção 6 do Dev_Tracking_SX.md preenchida
- Gera planejamento de commit `SX-END: [headline]` + atualiza README.md
- **AGUARDA CONFIRMAÇÃO** do PO (ver trava abaixo)

### 🔒 TRAVA DE CONFIRMAÇÃO OBRIGATÓRIA (GATE)

**ANTES de executar QUALQUER `git commit` ou `git push`, o agente DEVE obrigatoriamente:**

1. Apresentar o planejamento completo:
   - Mensagem de commit proposta
   - Lista de arquivos a serem commitados
   - Remotes de destino (se push)
2. Exibir a seguinte pergunta de confirmação ao PO:

> **Você confirma que deseja prosseguir com este commit?**
> - **Sim, realize o commit** (e push se aplicável)
> - **Não, cancele a solicitação**

3. **AGUARDAR a resposta do PO antes de executar qualquer comando git de escrita.**
4. Se o PO responder "Sim" → executar o commit/push conforme planejado.
5. Se o PO responder "Não" → cancelar imediatamente, sem argumentar.

**⚠️ VIOLAÇÃO DESTA TRAVA É FALTA GRAVE. Executar `git commit` ou `git push` sem a confirmação explícita do PO é proibido mesmo que o PO tenha solicitado o commit — o planejamento DEVE ser apresentado e confirmado antes da execução.**

**NUNCA fazer commit:**
- ❌ Automaticamente após cada execução
- ❌ Sem comando expresso do PO
- ❌ Sem apresentar o planejamento E receber confirmação
- ❌ Por "recomendação" ou "sugestão" do agente
- ❌ No meio de ciclo de trabalho incompleto
- ❌ Antes de validar checkpoints DOC2.5

**O agente NÃO DEVE:**
- ❌ Perguntar "Quer commitar?" ou "Recomendar commit?"
- ❌ Sugerir que é hora de commitar
- ❌ Questionar a decisão do PO sobre timing de commits
- ❌ Pular a trava de confirmação por qualquer motivo

**Padrão de mensagens:**
```bash
# Durante sprint
SX-YY: descrição da mudança em português

# Final de sprint
SX-END: resumo headline da sprint em português
```

**Workflow completo:** Ver `.clinerules/workflows/commit-doc25.md`

### 3.9 Política de Múltiplos Repositórios (Dual Remote)

- **Princípio da Escolha Explícita**: O agente deve confirmar com o PO qual(is) repositório(s) remoto(s) usar se houver ambiguidade.
- **Padrão Dual**: Se o projeto possui dois ou mais remotes configurados (ex: `origin` e `gitlab`) para o mesmo código:
  - Se o PO solicitar "commit" ou "push" de forma genérica (sem especificar destino): **Planejar e executar para TODOS os remotes configurados**.
  - Se o PO especificar um destino (ex: "apenas no github"): **Obedecer estritamente a restrição**.
- **Incerteza**: Na dúvida sobre quais remotes estão configurados ou qual usar, **questione o PO** antes de executar qualquer comando de push.

## 4. Regras Específicas: MCP ServiceNow

- **Localização**: As ferramentas estão em `mcp/servicenow-server/`
- **Credenciais**: Use o arquivo `.scr\.env` (nunca versione credenciais)
- **Git**: NÃO use `git diff` por padrão. Use `git status --short`. Patch/diff apenas sob demanda
- **Commits**: Mensagens devem seguir o padrão `SX-YY: descrição` ou `SX-END: resumo`

## 5. Workflows do Agente

- **Localização**: `.clinerules/workflows/`
- **Workflows disponíveis**:
  - `/commit-doc25`: Workflow de commit DOC2.5
  - `/dev-doc25`: Workflow de desenvolvimento DOC2.5
  - `/docs-doc25`: Workflow de documentação oficial DOC2.5
  - `/init`: Workflow de inicialização

### 5.1 Uso de Workflows

- Workflows são instruções detalhadas para tarefas específicas
- Cada workflow pode ser invocado via `/workflow-name` no chat
- Workflows seguem padrão DOC2.5

### 5.2 Localização de Skills

As habilidades para este workspace estão em:
- **Caminho padrão**: `.cline/skills/`
- **Uso**: O agente deve priorizar a busca de habilidades (arquivos `SKILL.md`) neste diretório para automação e expansão de capacidades.
- **Organização**: As habilidades estão organizadas em subdiretórios por nome.

## 6. Boas Práticas para o Cline

### 6.1 Relação com Templates e Documentação

- Não inventar estruturas totalmente novas quando já existe template apropriado
- Ao criar ou atualizar documentação:
  1. Garantir que `.clinerules/templates/doc25/` está disponível
  2. Ler o template relevante no pack canônico
  3. Se o pack canônico estiver ausente, pausar e solicitar provisionamento ao PO
  4. Respeitar seções estruturais definidas (não remover seções obrigatórias)
  5. Ajustar apenas conteúdo específico do projeto, mantendo formato base

### 6.2 Fluxo de Trabalho e Loops

- Uma solicitação do usuário deve resultar em **um fluxo de trabalho coerente**
- Evitar "loops de ação" sem valor
- Se perceber repetição da mesma ação sem progresso:
  1. Parar
  2. Explicar o que está acontecendo
  3. Pedir direção explícita do usuário antes de continuar

### 6.3 Mensagens Informativas do Usuário

- Quando usuário envia mensagem claramente informativa/confirmatória (ex: "ok", "entendi", "vamos seguir depois"):
  - Responder em linguagem natural se necessário
  - NÃO modificar arquivos nem executar comandos a menos que haja pedido explícito

### 6.4 Ordem de Leitura de Regras

Quando trabalhando em projeto dentro deste workspace, seguir ordem lógica:

1. Ler regras globais em `.clinerules/WORKSPACE_RULES_GLOBAL.md` (este arquivo)
2. Ler regras locais do projeto (ex: `rules/WORKSPACE_RULES.md`)
3. Somente depois propor plano de ação, leitura de templates, leitura de `Dev_Tracking_SX.md` e alterações

Regras locais podem detalhar:
- Estrutura específica de `docs/` daquele projeto
- Caminho exato de `Dev_Tracking_SX.md`
- Papéis especiais (projetos que funcionam como hubs de templates ou dados)

### 6.5 Segurança e Aprovação

**Política de Execução de Comandos (Baseada em Criticidade):**

**✅ Comandos de LEITURA (Auto-executar):**
- `git status`, `git log`, `git show`, `git branch`
- `ls`, `dir`, `cat`, `Get-Content`, `Get-ChildItem`
- `pwd`, `echo`, `Write-Host`
- Qualquer comando que apenas consulta/lê informações

**⚠️ Comandos de ALTERAÇÃO (Perguntar antes):**
- `git add`, `git commit`, `git push`, `git reset`, `git rebase`
- `rm`, `Remove-Item`, `mv`, `Move-Item`, `cp`, `Copy-Item`
- `mkdir`, `New-Item`, `touch`
- Instalação de dependências (`npm install`, `pip install`, etc.)
- Modificação de arquivos de configuração
- Qualquer comando que ALTERA estado do sistema

**❌ Commits (NUNCA sem comando expresso do PO):**
- `git commit` - Ver Seção 3.8 (Política de Commits DOC2.5)

**Princípios:**
- **Agente decide:** Comandos de leitura são seguros, executar automaticamente
- **Questionar alterações:** Propor comando exato e aguardar aprovação
- **Resumir resultados:** Não despejar logs brutos, sintetizar informações relevantes
- **Proteção máxima:** Nunca comandos destrutivos sem aprovação explícita

### 6.6 🔐 PROTEÇÃO DE CREDENCIAIS (CRÍTICO - SEGURANÇA)

**🚨 REGRA ABSOLUTA: NUNCA, EM NENHUMA CIRCUNSTÂNCIA, EXPOR CREDENCIAIS EM DOCUMENTAÇÃO**

**Tipos de informações sensíveis (NUNCA documentar):**
- ❌ Senhas
- ❌ Tokens de API
- ❌ API Keys
- ❌ Client Secrets
- ❌ Chaves privadas
- ❌ Connection strings com credenciais
- ❌ Cookies de sessão
- ❌ Certificados privados

**Locais onde credenciais SÃO permitidas:**
- ✅ Arquivos `.env` (NUNCA versionados)
- ✅ Arquivos em `.scr/` ou `.secrets/` (NUNCA versionados)
- ✅ Gerenciadores de senha/segredos

**Locais onde credenciais NÃO PODEM aparecer:**
- ❌ `tests/bugs_log.md`
- ❌ `Dev_Tracking_SX.md`
- ❌ `README.md`
- ❌ `docs/` (SETUP, ARCHITECTURE, DEVELOPMENT, OPERATIONS)
- ❌ Código fonte versionado
- ❌ Scripts de exemplo
- ❌ Mensagens de commit
- ❌ QUALQUER arquivo versionado no Git

**Como documentar configurações sem expor credenciais:**

❌ **ERRADO:**
```
SNOW_PASSWORD=EXEMPLO_NAO_REAL
API_KEY=EXEMPLO_NAO_REAL
```

✅ **CORRETO:**
```
SNOW_PASSWORD=<sua_senha_aqui>
Ou melhor ainda:
```
Configuração armazenada em `.scr/.env` (credenciais protegidas)
```

**Validação obrigatória antes de commit (TRAVA SECRET-FREE):**
Antes de qualquer solicitação de commit, gerar diff/status ou exportar JSONs com requests estruturados, o agente DEVE:
- [ ] Validar ativamente com ferramentas (`grep` ou similar) se senhas, tokens ou dados do `.scr/.env` estão presentes em `.json`, `.txt`, `.md`, ou scripts de execução.
- [ ] Certificar que `artifacts/` está no `.gitignore`.
- [ ] Certificar que arquivos em `docs/` e de tracking contêm apenas placeholders (ex: `<redacted>`, `<obter_de_.scr/.env>`).
- [ ] **BLOQUEIO ABSOLUTO:** Caso um secret seja detectado, abortar o processo imediatamente e higienizá-lo.

**Em caso de exposição acidental:**
1. 🚨 PARAR IMEDIATAMENTE qualquer commit/push
2. Remover credencial da documentação
3. Rotacionar/regenerar a credencial exposta
4. Avisar o PO sobre o incidente de segurança
5. Documentar lição aprendida (sem expor a credencial)

### 6.7 Checkpoints DOC2.5 Obrigatórios

Antes de marcar qualquer fase como completa, validar:

**Estrutura:**
- [ ] README.md na raiz do projeto
- [ ] Dev_Tracking.md (índice) existe
- [ ] Dev_Tracking_SX.md (sprint atual) existe
- [ ] Sprint/ folder existe
- [ ] docs/ contém EXATAMENTE 4 arquivos: SETUP, ARCHITECTURE, DEVELOPMENT, OPERATIONS
- [ ] ❌ docs/README.md NÃO existe (proibido)
- [ ] rules/WORKSPACE_RULES.md existe
- [ ] tests/bugs_log.md existe

**Nomenclatura:**
- [ ] Nenhum ARCHITECTURE_AND_LOGIC.md (legado → renomear para ARCHITECTURE.md)
- [ ] Nenhum DEPLOYMENT.md (legado → renomear para OPERATIONS.md)

### 6.8 Comportamento de Atualização de Documentação

**Quando atualizar cada documento canônico:**

**SETUP.md:**
- Mudança de pré-requisitos
- Alteração em estrutura de pastas principal
- Novas variáveis de ambiente

**ARCHITECTURE.md:**
- Novo componente principal
- Mudança em fluxos de trabalho fundamentais
- Novas integrações com sistemas externos

**DEVELOPMENT.md:**
- Mudança no workflow de desenvolvimento
- Novas convenções de código/arquivos
- Alteração no formato de Dev_Tracking

**OPERATIONS.md:**
- Novos procedimentos de teste
- Mudanças em deployment
- Novos procedimentos de segurança operacional

**Dev_Tracking_SX.md (SEMPRE):**
- Após cada fase de execução
- Decisões significativas (Seção 4)
- Status de backlog (Seção 3)
- Testes/bugs (Seção 5)

**NÃO atualizar docs canônicos para:**
- ❌ Features pontuais (vai em Dev_Tracking)
- ❌ Correções de bugs (vai em Dev_Tracking + tests/bugs_log.md)
- ❌ Decisões táticas de implementação

## 7. Referências Cruzadas

- **Templates canônicos runtime**: `.clinerules/templates/doc25/`
- **Templates fallback (legado)**: `Templates/` (somente compatibilidade)
- **Regras Antigravity (espelho)**: `.agent/rules.md`
- **Regras Cline (este arquivo)**: `.clinerules/WORKSPACE_RULES_GLOBAL.md`

---

*Este arquivo é a fonte de verdade para a atuação do Cline neste workspace.*

**Versão**: DOC2.5  
**Última atualização**: 2026-02-09  
**Origem**: Espelho de `.agent/rules.md` (Antigravity)
