# OPERATIONS

## Proposito

Este documento descreve como o projeto deve ser operado no estado atual, quais gates devem ser respeitados, como as evidencias devem ser tratadas e como registrar falhas, validacoes e decisoes recorrentes.

## 1. Modelo operacional atual

- Ambiente principal: `{{PRIMARY_EXECUTION_ENVIRONMENT}}`
- Modo de operacao: `{{CURRENT_OPERATING_MODEL}}`
- Sprint ativa: `{{ACTIVE_SPRINT}}`
- Escopo operacional aprovado: `{{APPROVED_OPERATIONAL_SCOPE}}`

O projeto opera com base em:

- leitura obrigatoria do contexto antes de agir
- execucao guiada por plano quando aplicavel
- aprovacao do PO para mudancas fora do escopo corrente
- rastreabilidade em `Dev_Tracking`
- registro de inconsistencias em `tests/bugs_log.md`

## 2. Read-First

Antes de qualquer execucao, ler na seguinte ordem:

1. `rules/WORKSPACE_RULES.md`
2. `.clinerules/WORKSPACE_RULES_GLOBAL.md`
3. `Cindy_Contract.md` quando existir no repositorio
4. `README.md`
5. `docs/SETUP.md`
6. `docs/ARCHITECTURE.md`
7. `docs/DEVELOPMENT.md`
8. `docs/OPERATIONS.md`
9. `Dev_Tracking.md`
10. `Dev_Tracking_{{ACTIVE_SPRINT}}.md`

## 3. Plan-First

- Planejar antes de executar quando a mudanca alterar estrutura, governanca, KB, processos ou comportamento relevante
- Nao assumir que ausencia de comentario equivale a aprovacao
- Manter o trabalho dentro do escopo aprovado para a fase e sprint correntes
- Quando houver inferencia, registrar explicitamente como inferencia

## 4. Approval-Gated Execution

- Mudancas fora do escopo ativo exigem aprovacao explicita do PO
- Fechamento de sprint exige comando explicito do PO
- Commit e push exigem comando explicito do PO
- Nao expandir a arquitetura, automacao ou integracoes sem gate formal

## 5. Evidencias e classificacao

### 5.1 Tipos de evidencia

- Evidencia primaria: documentos oficiais, KBs, manuais, registros do PO, configuracoes reais do repositorio
- Evidencia secundaria: sinteses, anotacoes, consolidacoes e observacoes operacionais
- Inferencia: conclusao derivada de evidencias, ainda nao confirmada pelo PO
- Pendente de validacao: dado plausivel, mas sem prova suficiente para promocao a verdade canonica

### 5.2 Regras de tratamento

- Preservar arquivos de evidencia existentes
- Nao inventar fluxo, criterio ou configuracao nao evidenciados
- Manter unknowns explicitos
- Promover informacao a canonica apenas quando houver base documental suficiente ou confirmacao do PO

## 6. Reconciliação de Evidências

### 6.1 Fontes consideradas

- `{{SOURCE_DOCS}}`
- `{{INFERRED_PROFILE_SOURCE}}`
- `{{PO_CONFIRMATION_SOURCE}}`

### 6.2 Regra de reconciliacao

- Source docs iniciam a base observavel
- Perfil inferido permanece rotulado como inferido
- Confirmacoes do PO prevalecem sobre inferencias
- A verdade canonica deve ser atualizada apenas com trilha explicita em `Dev_Tracking`

### 6.3 Saidas esperadas

- contradicoes registradas em `tests/bugs_log.md`
- decisoes registradas em `Dev_Tracking`
- documentos canonicos atualizados com o minimo de alteracao necessaria

## 7. Rotinas operacionais

### 7.1 Validacoes manuais minimas

- validar `README.md`
- validar os 4 documentos canonicos em `docs/`
- validar `Dev_Tracking.md` e `Dev_Tracking_{{ACTIVE_SPRINT}}.md`
- validar `tests/bugs_log.md`
- validar coerencia entre escopo aprovado, sprint ativa e documentacao corrente

### 7.2 Higiene documental

- manter `README.md` como entry point unico
- nao criar `docs/README.md` ou `docs/INDEX.md`
- evitar duplicacao de regras ou inventario desnecessario
- atualizar apenas o artefato minimo necessario

### 7.3 Captura de observacoes para aprendizado futuro

- registrar padroes recorrentes de decisao
- registrar preferencias estaveis e dependentes de contexto
- registrar criterios de review e desvios aceitaveis
- separar claramente fato, inferencia e pendencia de validacao

## 8. Rotinas de teste

### Testes manuais minimos

- validar `README.md`
- validar `docs/`
- validar tracking e `bugs_log`

### Testes automatizados

- documentar o comando real do projeto
- nao citar testes inexistentes

## 9. Fluxo de confirmacao com o PO

- apresentar mudancas estruturais de forma objetiva
- explicitar o que esta confirmado, inferido e pendente
- pedir confirmacao apenas quando houver impacto real no canonico
- apos confirmacao, refletir a verdade canonica nos documentos e no tracking

## 10. Seguranca operacional

- nunca versionar credenciais
- nunca documentar segredos
- mascarar valores sensiveis
- nao presumir acesso a sistemas externos sem prova documental
- manter alteracoes dentro do menor raio de impacto possivel

## 11. Resposta a falhas

1. confirmar contexto da sprint
2. registrar bug ou teste
3. corrigir o artefato minimo necessario
4. atualizar `Timestamp UTC`
5. registrar a decisao ou observacao relevante em `Dev_Tracking`
6. revalidar o que foi afetado

## 12. Referencias minimas

- `README.md`
- `docs/SETUP.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT.md`
- `Dev_Tracking.md`
- `Dev_Tracking_{{ACTIVE_SPRINT}}.md`
- `tests/bugs_log.md`
