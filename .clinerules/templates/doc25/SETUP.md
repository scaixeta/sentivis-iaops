# SETUP

## Proposito

Este documento descreve como preparar o contexto minimo para trabalhar no projeto, quais evidencias ja existem no repositorio e quais limites operacionais devem ser respeitados na fase atual.

## 1. Contexto do repositorio

- Projeto: `{{PROJECT_NAME}}`
- Fase atual: `{{CURRENT_PHASE}}`
- Sprint ativa: `{{ACTIVE_SPRINT}}`
- Escopo aprovado: `{{APPROVED_SCOPE}}`
- Tipo de repositorio: `{{REPOSITORY_TYPE}}`

## 2. Requisitos minimos

- Git
- Bash ou PowerShell
- Editor de texto ou IDE

## 3. Estrutura minima esperada

```text
{{PROJECT_NAME}}/
├── README.md
├── Dev_Tracking.md
├── Dev_Tracking_{{ACTIVE_SPRINT}}.md
├── docs/
│   ├── SETUP.md
│   ├── ARCHITECTURE.md
│   ├── DEVELOPMENT.md
│   └── OPERATIONS.md
├── rules/
├── tests/
└── Sprint/
```

## 4. Fontes de evidencia atuais

### 4.1 Evidencias ja disponiveis

- `{{EVIDENCE_SOURCE_1}}`
- `{{EVIDENCE_SOURCE_2}}`
- `{{EVIDENCE_SOURCE_3}}`

### 4.2 Classificacao inicial das evidencias

- Confirmado: `{{CONFIRMED_EVIDENCE}}`
- Inferido: `{{INFERRED_EVIDENCE}}`
- Pendente de validacao: `{{PENDING_VALIDATION_EVIDENCE}}`

### 4.3 Preservacao de evidencia

- Nao apagar arquivos de evidencia existentes sem justificativa explicita
- Nao sobrescrever conteudo do usuario sem necessidade comprovada
- Tratar arquivos de KB, manuais, notas operacionais e registros do PO como fontes primarias quando presentes

## 5. Preparacao inicial

### 5.1 Clonar o repositorio

```bash
git clone {{REPOSITORY_URL}}
cd {{PROJECT_FOLDER}}
```

### 5.2 Conferir a trilha canonica

```bash
ls
ls docs
ls rules
ls tests
```

Arquivos minimos esperados:

- `README.md`
- `Dev_Tracking.md`
- `Dev_Tracking_{{ACTIVE_SPRINT}}.md`
- `tests/bugs_log.md`
- `rules/WORKSPACE_RULES.md`

### 5.3 Ler antes de executar

1. `rules/WORKSPACE_RULES.md`
2. `.clinerules/WORKSPACE_RULES_GLOBAL.md`
3. `Cindy_Contract.md` quando existir no repositorio
4. `README.md`
5. `docs/SETUP.md`

## 6. Configuracoes locais

- Seguir apenas as configuracoes explicitamente documentadas no proprio repositorio
- Nao presumir `.env`, `.env.example`, pipelines ou automacoes se esses artefatos nao existirem
- Nao instalar dependencias fora do escopo aprovado
- Nao assumir integracoes externas sem evidencia documental ou confirmacao do PO

## 7. Limites atuais do setup

- O setup atual cobre apenas `{{CURRENT_SETUP_BOUNDARY}}`
- O setup atual nao inclui `{{NOT_INCLUDED_1}}`
- O setup atual nao inclui `{{NOT_INCLUDED_2}}`
- O setup atual nao inclui `{{NOT_INCLUDED_3}}`

## 8. O que ainda nao esta configurado

- `{{NOT_CONFIGURED_1}}`
- `{{NOT_CONFIGURED_2}}`
- `{{NOT_CONFIGURED_3}}`

## 9. Caminho esperado para evolucao futura

- Ingestao de novas evidencias deve seguir `{{FUTURE_INGESTION_PATH}}`
- Validacoes futuras devem ser registradas em `Dev_Tracking` e `tests/bugs_log.md`
- Qualquer ampliacao de setup deve respeitar a fase ativa e o gate de aprovacao do PO

## 10. Proximos passos

- Ler `docs/ARCHITECTURE.md`
- Ler `docs/DEVELOPMENT.md`
- Ler `docs/OPERATIONS.md`
