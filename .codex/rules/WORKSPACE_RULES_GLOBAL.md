# REGRAS DO WORKSPACE (Codex - Cindy - Padrao DOC2.5)

Este documento define como o runtime Codex deve operar dentro da Cindy.

## 1. Precedencia Obrigatoria

O Codex deve obedecer a seguinte ordem:

1. `rules/WORKSPACE_RULES.md` como fonte operacional local obrigatoria
2. `Cindy_Contract.md` como contrato de descoberta e despacho
3. este arquivo como adaptacao de runtime para Codex
4. `README.md`, `Dev_Tracking.md`, `Dev_Tracking_SX.md` e docs canonicos

Se houver conflito, a regra local da raiz prevalece.

## 2. Fluxo DOC2.5 no Codex

O Codex deve seguir este fluxo:

1. Entendimento do pedido
2. Leitura minima de contexto
3. Discovery de skills em `.codex/skills/`
4. Planejamento proporcional ao impacto
5. Aprovacao explicita do PO quando houver gate
6. Execucao com a menor mudanca necessaria
7. Rastreabilidade em `Dev_Tracking_SX.md` e `tests/bugs_log.md` quando aplicavel

## 3. Idioma e Comunicacao

- respostas e documentacao em pt-BR
- comandos, nomes de arquivo, identificadores e codigo em ingles quando necessario
- comunicacao tecnica, direta e objetiva

## 4. Baseline Canonico da Cindy

O Codex deve assumir como baseline da Cindy:

- `README.md` como entry point oficial
- `Cindy_Contract.md` como contrato canonico
- `Dev_Tracking.md` como indice mestre
- `Dev_Tracking_SX.md` como sprint ativa
- `docs/SETUP.md`, `docs/ARCHITECTURE.md`, `docs/DEVELOPMENT.md`, `docs/OPERATIONS.md`
- `tests/bugs_log.md` como log centralizado
- `Templates/` como fonte de geracao documental local

Nao presumir:

- `scripts/` na raiz como dependencia obrigatoria
- `.scr/` como armazenamento obrigatorio
- `.codex/templates/doc25/` como fallback necessario

## 5. Skills do Codex

- `.codex/skills/` e o runtime counterpart do Codex
- `.agents/skills/` permanece a canonical authoring source of truth das skills comuns
- quando houver drift relevante entre `.agents/skills/` e `.codex/skills/`, a Cindy deve avaliar se a divergencia e adaptacao legitima de runtime ou inconsistencia
- o Codex deve priorizar skills antes de improvisar logica paralela

## 6. Gates Obrigatorios

- alteracoes estruturais exigem plano e rastreabilidade
- commit e push apenas com ordem expressa do PO
- conclusao, conformidade ou fechamento de sprint exigem validacao manual conforme `rules/WORKSPACE_RULES.md`
- somente o PO pode encerrar sprint

## 7. Politica Git

- nao usar `git diff` por padrao
- usar `git status`, `git status --short`, `git log` e `git show` para inspecao
- nunca executar `git commit` ou `git push` sem comando expresso do PO

## 8. Seguranca

- nunca versionar credenciais
- nunca documentar segredos
- nao presumir `.scr/.env` ou qualquer storage local de secrets se o artefato nao existir
- se uma skill depender de credenciais, ela deve apontar explicitamente para a fonte real disponivel no contexto atual

## 9. Validacao da Stack Codex

Os scripts internos de `.codex/scripts/` servem apenas para:

- sincronizar `.codex/skills/` com o runtime local do usuario
- validar a integridade minima da stack `.codex/`

Eles nao substituem os gates operacionais definidos em `rules/WORKSPACE_RULES.md`.

## 10. Referencias

- `rules/WORKSPACE_RULES.md`
- `Cindy_Contract.md`
- `README.md`
- `Dev_Tracking.md`
- `Dev_Tracking_SX.md`
- `.codex/skills/`
- `.agents/skills/`
