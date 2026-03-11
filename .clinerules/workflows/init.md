---
description: Workflow de inicialização do Cline para leitura de regras e contexto DOC2.5.
---

Este workflow deve ser executado ao iniciar um novo chat ou quando houver uma mudança significativa de rumos no projeto.

// turbo-all
1. Ler as regras globais do workspace:
   `cat .clinerules/WORKSPACE_RULES_GLOBAL.md`

2. Verificar se o projeto atual possui regras locais e lê-las, se existirem:
   `ls rules/WORKSPACE_RULES.md` (se existir, ler com cat)

3. Localizar a Sprint atual via `Dev_Tracking_SX.md` e ler o progresso atual.

4. Refrasear o entendimento e aguardar declaração de escopo do PO.

5. Verificar a seção SoT (Seção 0 de WORKSPACE_RULES_GLOBAL.md) antes de tomar qualquer decisão sobre paths de skills ou autoridade de runtime.
