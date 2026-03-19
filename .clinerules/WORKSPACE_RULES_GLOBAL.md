# REGRAS DO WORKSPACE (Cline - Cindy - Padrão DOC2.5)

Este documento define como o runtime Cline deve operar dentro da Cindy.

## 1. Precedência Obrigatória

O Cline deve obedecer a seguinte ordem:

1. `rules/WORKSPACE_RULES.md` como fonte operacional local obrigatória
2. este arquivo como adaptação de runtime para Cline
3. `Cindy_Contract.md` como contrato de descoberta e despacho
4. `README.md`, `Dev_Tracking.md`, `Dev_Tracking_SX.md` e docs canônicos

Se houver conflito, a regra local da raiz prevalece.

## 2. Estrutura Oficial do Cline no Workspace

Conforme a documentação oficial do Cline:

- arquivos `.md` ou `.txt` em `.clinerules/` funcionam como regras sempre ativas
- workflows podem ser mantidos versionados no repositório e acionados explicitamente
- skills ficam em `.cline/skills/`, cada uma em sua pasta, com `SKILL.md` e frontmatter válido

Portanto:

- `.clinerules/` e `.cline/` têm papéis diferentes e ambos são necessários
- `.clinerules/` não deve ser usado para duplicar skills
- `.cline/skills/` não deve ser usado como depósito de regras globais

## 3. Fluxo DOC2.5 no Cline

O Cline deve seguir este fluxo:

1. Entendimento do pedido
2. Executar o gate de inicializacao (`.clinerules/workflows/init.md` ou skill `doc25-init`)
3. Classificar o workspace como `repo materializado` ou `baseline de geracao`
4. Leitura mínima de contexto adequada ao modo do workspace
5. Discovery de skills em `.cline/skills/`
6. Planejamento proporcional ao impacto
7. Aprovação explícita do PO quando houver gate
8. Execução com a menor mudança necessária
9. Rastreabilidade em `Dev_Tracking_SX.md` e `tests/bugs_log.md` quando aplicável

## 4. Idioma e Comunicação

- respostas e documentação em pt-BR
- comandos, nomes de arquivo, identificadores e código em inglês quando necessário
- comunicação técnica, direta e objetiva
- em workspace Windows-only, exemplos operacionais devem ser PowerShell-first
- evitar exemplos `ls`, `cat`, `pwd` ou caminhos híbridos quando a plataforma ativa for Windows

## 5. Baseline Canônico da Cindy

O Cline deve assumir como baseline da Cindy:

- `README.md` como entry point oficial
- `Cindy_Contract.md` como contrato canônico
- `Dev_Tracking.md` como índice mestre
- `Dev_Tracking_SX.md` como sprint ativa
- `docs/SETUP.md`, `docs/ARCHITECTURE.md`, `docs/DEVELOPMENT.md`, `docs/OPERATIONS.md`
- `tests/bugs_log.md` como log centralizado
- `Templates/` como fonte principal de geração documental
- `.clinerules/templates/doc25/` como fallback local do runtime Cline
- `.clinerules/workflows/` como conjunto local de workflows explícitos

Não presumir:

- `scripts/` na raiz como dependência obrigatória
- `.scr/` como armazenamento obrigatório
- `.agent/` como source of truth atual da Cindy

## 6. Templates e Workflows

- usar `Templates/` do projeto como fonte principal
- usar `.clinerules/templates/doc25/` apenas como fallback
- manter o fallback alinhado aos templates canônicos da Cindy
- não gerar documentação fora dos caminhos canônicos do DOC2.5
- manter os workflows de `.clinerules/workflows/` coerentes com as regras locais da raiz
- em `baseline de geracao`, ler `Templates/README.md` antes de qualquer template adicional
- em `baseline de geracao`, nao ler `README.md`, `Dev_Tracking.md` ou `docs/` como se ja existissem
- em pedido amplo de projeto novo, explicar antes da escrita: o que sera criado, o que esta indefinido e o que ficara `Pendente de validacao`
- em geracao documental, preferir a menor quantidade de secoes que ainda preserve coerencia DOC2.5
- nao copiar boilerplate do template para o documento final sem ganho informacional
- para bootstrap de projeto novo, ativar a skill `project-bootstrap` (disponivel em `.cline/skills/project-bootstrap/`)
- em ambiente Windows, NUNCA usar `cat`, `ls`, `rm`, `pwd` ou qualquer comando Bash; usar read_file ou PowerShell

## 7. Skills do Cline

- `.cline/skills/` é o runtime counterpart do Cline
- `.agents/skills/` permanece a canonical authoring source of truth das skills comuns
- quando houver drift relevante entre `.agents/skills/`, `.cline/skills/` e `.codex/skills/`, a Cindy deve avaliar se a divergência é adaptação legítima de runtime ou inconsistência
- cada skill em `.cline/skills/` deve ter `SKILL.md` com frontmatter válido
- skills DOC2.5 centrais devem permanecer alinhadas ao baseline atual da Cindy

## 8. Gates Obrigatórios

- alterações estruturais exigem plano e rastreabilidade
- commit e push apenas com ordem expressa do PO
- conclusão, conformidade ou fechamento de sprint exigem validação manual conforme `rules/WORKSPACE_RULES.md`
- somente o PO pode encerrar sprint
- bootstrap estrutural ou projeto novo exigem passagem pelo gate de init antes da primeira escrita
- qualidade deve ser tratada em escala `0-100`, com alvo minimo de `80`
- budget contextual alvo: ate `30%`; acima disso, resumir antes de expandir leitura

## 9. Política Git

- não usar `git diff` por padrão
- usar `git status`, `git status --short`, `git log` e `git show` para inspeção
- nunca executar `git commit` ou `git push` sem comando expresso do PO

## 10. Segurança

- nunca versionar credenciais
- nunca documentar segredos
- não presumir `.scr/.env` ou qualquer storage local de secrets se o artefato não existir
- se uma skill depender de credenciais, ela deve apontar explicitamente para a fonte real disponível no contexto atual

## 11. Referências

- `rules/WORKSPACE_RULES.md`
- `Cindy_Contract.md`
- `README.md`
- `Dev_Tracking.md`
- `Dev_Tracking_SX.md`
- `.clinerules/workflows/`
- `.clinerules/templates/doc25/`
- `.cline/skills/`
- `.agents/skills/`
