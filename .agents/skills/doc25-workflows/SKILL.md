---
name: doc25-workflows
description: Aplicar workflows DOC2.5 (higiene de docs/dev/commit, gate de Dev_Tracking, checklist de encerramento de sprint, commit somente por comando expresso do PO).
---
# Workflows DOC2.5

## Quando usar
Usar quando o usuário pedir para atualizar docs, encerrar sprint, preparar commit, ou "executar o workflow".

## Gate de workflow (estrito)
- Commit/push SOMENTE por comando expresso do PO.
- NUNCA sugerir ou recomendar commits.
- Sempre atualizar Dev_Tracking (append-only) antes de propor ações de commit.
- Manter mudanças localizadas ao projeto atual.

## Procedimento
1) Determinar qual workflow se aplica:
   - `/docs-doc25`: Atualização de documentação canônica
   - `/dev-doc25`: Desenvolvimento completo
   - `/commit-doc25`: Commit (somente por comando do PO)
   - `/init`: Inicialização de contexto
2) Coletar evidência: listar arquivos alterados, resumir edições pretendidas, propor menor conjunto de atualizações.
3) Executar apenas o que o PO solicitou (atualizações de docs, tasks, bug log).
4) Para "encerrar sprint": verificar Dev_Tracking atualizado, tasks atualizadas, bugs conhecidos registrados.
5) Validar checkpoints DOC2.5 obrigatórios antes de declarar conclusão.
