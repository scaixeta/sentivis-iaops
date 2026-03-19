---
description: Workflow de inicializacao do Cline para leitura de regras e contexto DOC2.5.
---

Este workflow deve ser executado ao iniciar um novo chat, quando houver mudanca significativa de rumo ou quando o pedido envolver projeto novo/bootstrap.

// turbo-all
1. Ler a regra local obrigatoria da raiz (usar read_file, NAO usar `cat`):
   `rules/WORKSPACE_RULES.md`

2. Ler a regra global do runtime Cline (usar read_file, NAO usar `cat`):
   `.clinerules/WORKSPACE_RULES_GLOBAL.md`

3. Ler `Cindy_Contract.md` (usar read_file).

4. Classificar o workspace:
   - `repo materializado` se `README.md`, `Dev_Tracking.md`, `Dev_Tracking_SX.md`, `docs/` e `tests/bugs_log.md` existirem
   - `baseline de geracao` se os artefatos finais nao existirem, mas `Templates/` estiver presente

5. Se for `repo materializado`:
   - ler `README.md`
   - ler `Dev_Tracking.md`
   - localizar e ler a sprint ativa

6. Se for `baseline de geracao`:
   - ler `Templates/README.md`
   - ler apenas os templates adicionais necessarios ao pedido
   - nao presumir stack, arquitetura, hardware, protocolo ou integracoes
   - se o pedido for de projeto novo ou bootstrap, ativar a skill `project-bootstrap`

7. Refrasear o entendimento e classificar em:
   - confirmado
   - inferido
   - `Pendente de validacao`

8. Antes da primeira escrita em pedido estrutural, explicar:
   - o que sera criado
   - o que ficou indefinido
   - o que ficara `Pendente de validacao`

9. Trabalhar com budget contextual alvo de ate `30%` e meta de qualidade minima `80/100`.

IMPORTANTE: Em ambiente Windows, NUNCA usar `cat`, `ls`, `rm`, `pwd`, `grep` ou qualquer comando Bash/Unix. Usar SOMENTE ferramentas de leitura do runtime (read_file) ou comandos PowerShell quando comando de terminal for necessario.
