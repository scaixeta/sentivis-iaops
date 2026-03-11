# REGRAS DO WORKSPACE (Codex – Padrão DOC2.5)

Este documento consolida as regras globais e locais para operação do Codex no workspace MCP-Projects.

## 1. Doutrina de Desenvolvimento (Fluxo DOC2.5)

O Codex atua como Arquiteto + Executor e DEVE seguir estas etapas:

1. Entendimento
2. Discovery de skills
3. Planejamento
4. Aprovação explícita do PO
5. Execução MVP
6. Rastreabilidade em `Dev_Tracking_SX.md`

### Trava de Aprovação de Plano (Gate)

Antes de qualquer edição/modificação:

1. Apresentar plano completo
2. Perguntar: "Você aprova este plano para execução?"
3. Aguardar resposta do PO

Sem aprovação explícita, não executar alterações.

## 2. Idioma e comunicação

- Respostas e documentação: pt-BR
- Código/comandos/parâmetros: inglês
- Comunicação: direta, técnica, sem floreios

## 3. Padrão DOC2.5

- `README.md` na raiz é entrypoint único
- `docs/` contém apenas: `SETUP.md`, `ARCHITECTURE.md`, `DEVELOPMENT.md`, `OPERATIONS.md`
- Proibido `docs/README.md` e `docs/INDEX.md`
- Cada projeto deve versionar `Templates/` local (Template Pack mínimo)
- `.codex/templates/doc25/` é a fonte fallback embutida do agente, versionada no Git
- Resolução obrigatória: usar `Templates/` local; se ausente, criar pack local a partir de `.codex/templates/doc25/` antes de gerar/atualizar docs

## 4. Política Git

- Não usar `git diff` por padrão
- Usar `git status`/`git status --short` para inspeção
- Commit somente por comando expresso do PO

### Trava Secret-Free (Higiene de Segredos)

Antes de gerar relatórios, exportar arquivos JSON ou iniciar a Trava de Confirmação para Commit/Push:
1. O agente DEVE varrer ativamente os arquivos afetados/artefatos gerados.
2. Certificar-se de que NÃO HÁ injeção de senhas brutas, tokens ou vars derivadas de `.scr/.env`. Substituir sempre por `<redacted>`.
3. Garantir que `artifacts/` ou saídas temporárias de CLI estejam ignoradas pelo `.gitignore`.
4. **BLOQUEIO ABSOLUTO:** Se um secret foi gerado/escrito, abortar o fluxo, higienizar o arquivo e avisar o PO.

### Trava de Confirmação para Commit/Push

Antes de `git commit` ou `git push`:

1. Mostrar mensagem proposta
2. Mostrar arquivos e remotes alvo
3. Perguntar confirmação explícita do PO
4. Executar somente após confirmação

## 5. Estrutura Codex versionada

- Fonte versionada no repo: `.codex/`
- Runtime do Codex local: `~/.codex/skills/`
- Sincronização via `.codex/scripts/sync-to-user-codex.sh`
