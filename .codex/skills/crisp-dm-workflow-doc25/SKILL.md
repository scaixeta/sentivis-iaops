---
name: crisp-dm-workflow-doc25
description: Integração do ciclo de vida CRISP-DM ao processo DOC2.5 para orquestração ágil e segura de projetos de Inteligência Artificial e Machine Learning.
---

# CRISP-DM Workflow Orchestrator (DOC2.5)

## Propósito
Esta skill define e garante a aplicação do framework padrão da indústria **CRISP-DM** (Cross-Industry Standard Process for Data Mining) encapsulado dentro da governança e fluxo do **DOC2.5**. O objetivo é orquestrar iniciativas de IA/ML com o mesmo rigor de rastreabilidade, planejamento e aprovação aplicados ao desenvolvimento tradicional de software, sem criar governanças paralelas.

## Quando usar (Activation Criteria)
Esta skill **deve** ser ativada obrigatoriamente se a solicitação do PO envolver uma ou mais das seguintes disciplinas:
- Machine Learning (Aprendizado de Máquina)
- Modelos de Predição (Predictive Models)
- Classificação, Clusterização ou Ranking
- Sistemas de Recomendação
- Treinamento, Fine-Tuning ou Avaliação de Modelos
- Feature Engineering
- Preparação de Datasets / Curadoria de Dados
- Monitoramento de Drift de Dados ou Reciclagens (Retraining)
- Avaliação de sistemas RAG (Retrieval-Augmented Generation) quando houver avaliação de qualidade do modelo além do mero encanamento de recuperação (plumbing).

## Quando NÃO usar
Não invoque esta skill (use orquestradores tradicionais) para:
- Trabalhos puros de backend/API sem ciclo de vida de modelos.
- Trabalhos de interface de usuário (UI/Frontend).
- Tarefas exclusivamente de infraestrutura ou automação (sem fase de modelagem/avaliação).
- Criação base de documentação apenas.

## Entradas Esperadas
- Problema de negócio a ser resolvido via IA/ML.
- Origens de dados e eventuais restrições.
- Critérios de sucesso qualitativos/quantitativos pretendidos.

## Saídas Esperadas
- Plano de implementação sequencial faseado via CRISP-DM.
- Definição clara do objetivo, baseline approach, métricas e pipeline de dados.
- Modelos treinados, avaliados, validados contra baselines e documentados (na execução).
- Relatório de validação referenciado no `Dev_Tracking_SX.md`.

## Integração CRISP-DM x DOC2.5

O mapeamento do processo de desenvolvimento seguro DOC2.5 com as fases metodológicas do CRISP-DM se dá da seguinte forma:

1. **DOC2.5 Understanding & Discovery**
   - *CRISP-DM Phase 1: Business Understanding* (Definir objetivo de negócio, KPIs de sucesso e go/no-go).
   - *CRISP-DM Phase 2: Data Understanding* (Mapear fontes de dados, aferir qualidade e viabilidade).

2. **DOC2.5 Proposal & Implementation Plan**
   - Desenhar o plano explicitando as próximas fases. Exigências estritas de ML: Target variable, estratégia de feature engineering, e pipeline baseline.

3. **DOC2.5 Approval Gate**
   - Apresentar o plano consolidado.
   - Pergunta obrigatória: *"Você aprova este plano para execução? Sim / Não"*
   - **ZERO Auto-Execute**.

4. **DOC2.5 Controlled Execution**
   - *CRISP-DM Phase 3: Data Preparation* (Limpeza, transformações, pipelines de feature).
   - *CRISP-DM Phase 4: Modeling* (Seleção arquitetural, treinamento e otimização).

5. **DOC2.5 Validation & Report**
   - *CRISP-DM Phase 5: Evaluation* (Validar o output formalmente sob os critérios de negócio).
   - *CRISP-DM Phase 6: Deployment* (Estratégia de rollout da solução e monitoramento de drift).
   - Registrar as decisões e histórico no `Dev_Tracking_SX.md`.

## Regras de Planejamento Obrigatório para IA/ML

Qualquer plano de implementação gerado por esta skill deve iterar e exigir os seguintes fatores de projeto:
- Business objective e KPIs de sucesso.
- Designação da Variável Target (ou definição formal da tarefa alvo).
- Fontes de dados, qualidade e avaliações de disponibilidade.
- Estratégia de preparação de dados.
- Abordagem *baseline* pragmática (ex: modelo aleatório ou heurística de negócios simples).
- Estratégia da modelagem (principais tipos algorítmicos ou topologias arquiteturais propostas).
- Critérios de Evaluation e Go/No-Go para lançamento da pipeline de inferência.
- Estratégia de Deployment.
- Considerações de Monitoramento contínuo / Concept Drift / Retraining triggers.

## Regras de Aprovação e Restrições DOC2.5

- **Zero Auto-Execute / Zero Auto-Commit**: Nenhuma extração de dados dispendiosa, treino em loop longo ou script modificado no Git pode ser injetado automaticamente sem a Approval Gate.
- **Single Source of Truth**: Não crie instâncias de documentação alienígenas ("ML_README.md", "EXPERIMENTS.md"). Os modelos e metodologias habitam as *4 Pastas Canônicas* (`SETUP.md`, `ARCHITECTURE.md`, `DEVELOPMENT.md`, `OPERATIONS.md`).
- **Nenhum bypass de governança**: Mantenha rastreabilidade obrigatória no Dev Tracking ativo para a sprint de Data Science vigente.

## Critérios de Validação da Skill

Antes de apresentar "Concluído", avalie internamente:
- [ ] O planejamento contém o mapeamento de todas as 6 fases do CRISP-DM sob o Workflow DOC2.5?
- [ ] Os KPIs de negócio foram traçados com rigor e critério de aceite (baseline explícita)?
- [ ] O PO aprovou o plan via Approval Gate (Sim/Não)?
- [ ] O `Dev_Tracking` listou as decisões algorítmicas de negócio em sua respectiva aba?
- [ ] Nenhum documento proibido fora de `docs/` foi introduzido via skill?

## Exemplo de Uso

**PO**: "Gostaria que você projetasse um sistema inteligente para ranquear nossos tickets de suporte e treine o modelo nos CSVs anexos."

**Agente:** (Acionando a meta-skill CRISP-DM + DOC2.5)
1. "Meu Business e Data Understanding revelam..."
2. "Proponho o seguinte de plano integrando as fases CRISP-DM de Data Preparation, Modeling e Deployment ao doc2.5 approval flow..."
3. "Você aprova este plano para execução? Sim/Não."
*(Aguarda comando de execução seguro e logado do Product Owner)*
