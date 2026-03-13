# WORKSPACE RULES - Sentivis IAOps

## Escopo

- Projeto: Sentivis IAOps
- Fonte local de governança: Este arquivo
- Regras globais complementares: `.clinerules/WORKSPACE_RULES_GLOBAL.md`

## Caminhos Canônicos

| Tipo | Caminho |
|------|---------|
| Documentação raiz | `README.md` |
| Documentação técnica | `docs/SETUP.md`, `docs/ARCHITECTURE.md`, `docs/DEVELOPMENT.md`, `docs/OPERATIONS.md` |
| Tracking | `Dev_Tracking.md`, `Dev_Tracking_SX.md`, `tests/bugs_log.md` |
| Templates | `Templates/` |
| Templates fallback | `.clinerules/templates/doc25/` |

## Regras Operacionais Mínimas

1. Ler este arquivo antes de alterar documentação, tracking, skills ou workflows
2. Manter o modelo canônico do projeto
3. Usar `Templates/` como fonte principal de formato
4. Atualizar `Dev_Tracking.md`, `Dev_Tracking_SX.md` e `tests/bugs_log.md` com `Timestamp UTC`
5. Não criar commits ou push sem comando expresso do PO
6. Credenciais ficam em `.scr/.env` - nunca versionar
7. `README.md` (root) deve terminar com `## Cindy — Orquestradora (Context Router)` e imagem centralizada (`.brand/Cindy.jpg`)

## Estrutura Obrigatória

```
Sentivis SIM/
├── README.md                    # Entry point oficial
├── Dev_Tracking.md              # Índice de sprints
├── Dev_Tracking_SX.md           # Sprint ativa
├── docs/
│   ├── SETUP.md
│   ├── ARCHITECTURE.md
│   ├── DEVELOPMENT.md
│   └── OPERATIONS.md
├── rules/
│   └── WORKSPACE_RULES.md
├── tests/
│   └── bugs_log.md
├── Sprint/                     # Sprints arquivadas
└── .scr/
    └── .env                    # Credenciais (não versionar)
```

## Coisas a Evitar

- Criar `docs/README.md` (proibido)
- Criar `docs/INDEX.md` (proibido)
- Usar nomes legados como `DEPLOYMENT.md` ou `ARCHITECTURE_AND_LOGIC.md`
- Versionar credenciais
- Criar commits sem aprovação

## Coisas a Fazer

- Manter PT-BR na documentação
- Manter comandos/técnicos em inglês
- Usar `Timestamp UTC` em tracking
- Registrar bugs em `tests/bugs_log.md`

## ThingsBoard Específico

- URL: `http://95.217.16.195:8080`
- Credenciais: `.scr/.env`
- Usuário: Tenant Administrator

---

*Versão: 1.0 | Última atualização: 2026-03-11*
