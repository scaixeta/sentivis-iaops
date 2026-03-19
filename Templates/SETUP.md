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
- PowerShell
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

## 5. Conferir a trilha canonica

Exemplos Windows (PowerShell):

```powershell
Get-ChildItem
Get-ChildItem docs
Get-ChildItem rules
Get-ChildItem tests
```

Arquivos minimos esperados:

- `README.md`
- `Dev_Tracking.md`
- `Dev_Tracking_{{ACTIVE_SPRINT}}.md`
- `tests/bugs_log.md`
- `rules/WORKSPACE_RULES.md`

## 6. Leitura minima antes de agir

1. `rules/WORKSPACE_RULES.md`
2. regra global do runtime ativo
3. `Cindy_Contract.md` quando existir no repositorio
4. `README.md`
5. `Dev_Tracking.md`
6. `Dev_Tracking_{{ACTIVE_SPRINT}}.md`
7. apenas os docs canonicos necessarios

## 7. Configuracoes locais

- Seguir apenas as configuracoes explicitamente documentadas no proprio repositorio
- Nao presumir `.env`, `.env.example`, pipelines ou automacoes se esses artefatos nao existirem
- Nao instalar dependencias fora do escopo aprovado
- Nao assumir integracoes externas sem evidencia documental ou confirmacao do PO

## 8. Limites atuais do setup

- O setup atual cobre apenas `{{CURRENT_SETUP_BOUNDARY}}`
- O setup atual nao inclui `{{NOT_INCLUDED_1}}`
- O setup atual nao inclui `{{NOT_INCLUDED_2}}`
- O setup atual nao inclui `{{NOT_INCLUDED_3}}`

## 9. O que ainda nao esta configurado

- `{{NOT_CONFIGURED_1}}`
- `{{NOT_CONFIGURED_2}}`
- `{{NOT_CONFIGURED_3}}`

## 10. Proximos passos

- Ler `docs/ARCHITECTURE.md`
- Ler `docs/DEVELOPMENT.md`
- Ler `docs/OPERATIONS.md`
