---
name: backend-feature-orchestrator-doc25
description: Orquestrador ponta a ponta para desenvolvimento de funcionalidades backend, com governança estrita DOC2.5, aprovação explícita e rastreabilidade rigorosa.
---

# Backend Feature Development Orchestrator (DOC2.5)

## Propósito
Esta skill orquestra o ciclo completo de desenvolvimento de funcionalidades backend, garantindo que o agente atue de forma metodológica desde o entendimento inicial até a validação final, mantendo conformidade absoluta com os padrões de governança, aprovação e rastreabilidade do DOC2.5.

Ela atua como uma "meta-skill" de fluxo, garantindo que o desenvolvimento não pule etapas críticas e não realize modificações destrutivas sem autorização prévia.

## Quando usar
- Quando o PO solicitar o desenvolvimento de uma nova funcionalidade (feature) no backend.
- Quando for necessária uma abordagem estruturada para projetar, implementar e testar endpoints, rotas, lógica de negócios ou integrações.
- Quando o escopo da tarefa for complexo e exigir fases claras de planejamento, aprovação e execução.

## Quando NÃO usar
- Para pequenas correções de sintaxe ou "typos" simples.
- Para alterações puramente de frontend (usar skills apropriadas para frontend).
- Quando o PO expressamente solicitar apenas a execução direta sem análise (aplica-se apenas a comandos seguros).

## Entradas Esperadas
- Descrição da nova funcionalidade backend ou requisitos do negócio.
- Contexto do estado atual (geralmente lido de arquivos do projeto ou do tracking atual).
- Restrições técnicas ou dependências existentes.

## Saídas Esperadas
- Plano de implementação numerado e arquitetura proposta (antes da execução).
- Definição explícita de contratos de API, autenticação, persistência e observabilidade.
- Código backend implementado (rotas, controllers, serviços, repositórios, testes correspondentes).
- Atualização do arquivo de Dev Tracking (ex: `Dev_Tracking_SX.md`).
- Relatório de validação e testes executados.

## Fluxo Interno Sugerido (Fases DOC2.5)

Este fluxo é **obrigatório**:

1. **Understanding & Discovery**: Analise o pedido do PO, verifique as regras de negócio em `rules/`, e busque patterns e outras skills existentes em `.agent/skills` para evitar retrabalho.
2. **Architecture Proposal & Planning**: Desenhe como a funcionalidade se encaixa no código atual. Crie um plano de fases numeradas. O planejamento **deve exigir explicitamente** as seguintes considerações:
   - **Contract Expectations**: Definir body do request, body da response, status codes, error model e idempotência.
   - **Authorization**: Separar autenticação de autorização, definir perfil/role permitido e escopos do tenant.
   - **Observability**: Exigir logs estruturados, métricas, tracing, request ID e sinais pós-deploy.
   - **Persistence**: Especificar dependências de persistência (campos, transações, trilha de auditoria, políticas de retenção e chaves primárias/estrangeiras).
   - **Rollout e Validação**: Definir estratégia de rollout, critérios de rollback, health checks, e feature flags.
3. **Approval Gate**: Apresente a proposta ao PO e AGUARDE APROVAÇÃO EXPLÍCITA ANTES DE ESCREVER CÓDIGO.
   - Pergunta obrigatória: *"Você aprova este plano para execução? Sim / Não"*
4. **Controlled Execution**: Após aprovado, execute fase a fase. Verifique o resultado de cada alteração em vez de executar todas de uma vez (TDD sugerido).
5. **Validation & Report**: Execute os testes rigorosos, não se baseie apenas em retornos nominais. Certifique-se de que a funcionalidade cumpre os requisitos descritos. Adicione as decisões na Seção 4 e o status na Seção 3 do `Dev_Tracking_SX.md`.

## Restrições DOC2.5 & Regras de Aprovação

- **Zero Auto-Execute**: É terminantemente proibido avançar para a fase de Execução sem a aprovação explícita do plano pela fase de Approval Gate.
- **Zero Auto-Commit**: NUNCA crie commits de Git ou sugira commits espontaneamente. Os commits são apenas ordenados pelo PO.
- **Transparência**: Nunca mude as regras do repositório, não oculte dependências adicionadas e nem apague logs sem alertar.
- **Evite Erros Linguísticos**: Certifique-se de escrever "stack traces" e não "staketraces". Descreva explicitamente os testes de integração HTTP real em vez de descrições ambíguas.
- **Doc Compliance**: O desenvolvimento não deve adicionar pastas alienígenas à raiz. Se documentação extra for gerada, o fluxo canônico (Dev_Tracking) deve referenciá-la. `docs/README.md` permanece PROIBIDO.

## Critérios de Validação da Skill

Antes de considerar o uso desta skill completo, o agente deve confirmar:
- [ ] O planejamento contém todos os requisitos rigorosos (API, Auth, Persistência, etc)?
- [ ] O PO aprovou o plano?
- [ ] A feature foi desenvolvida rigorosamente conforme o plano?
- [ ] O arquivo `Dev_Tracking_SX.md` recebeu log das decisões?
- [ ] Nenhuma alteração não prevista correu paralelamente?
- [ ] A observabilidade do componente foi validada no código inserido?

## Exemplos de Uso

**Administração - Modo Strict:** "Projete a nova rota POST de configuração. Separe as fases e cumpra todos os critérios obrigatórios do orquestrador DOC2.5 de backend."

**Agente:** (Aciona esta meta-skill)
1. "Meu entendimento é..."
2. "Em discovery, encontrei `testing-patterns`..."
3. "Proponho o seguinte plano arquitetural, contendo Contratos API, Schema de Autorização e Metadados de Auditoria..."
4. "Você aprova?" *(Aguardando)*

---

## Provenance
- Original name: Backend Feature Development Orchestrator
- Relation: adapted from
- Source: MCP Market
- URL: https://mcpmarket.com/tools/skills/backend-feature-development-orchestrator
- Reference date: 2026-03-13
- Note: adapted for Cindy/DOC2.5 governance, with explicit planning, approval, traceability, and protection against unauthorized execution.
