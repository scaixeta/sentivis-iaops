# SETUP - Sentivis IAOps

## Propósito

Orientar como preparar o ambiente local para trabalhar com o projeto Sentivis IAOps e ThingsBoard CE.

## Requisitos Mínimos

| Ferramenta | Versão | Propósito |
|------------|--------|-----------|
| Git | 2.x+ | Controle de versão |
| VS Code | 1.75+ | Editor e terminal |
| Node.js | 18+ | Runtime para scripts |
| npm ou yarn | 8+ | Gerenciador de pacotes |
| curl | latest | Teste de APIs HTTP |
| Python | 3.10+ | Scripts utilitários |

## Requisitos Opcionais

| Ferramenta | Versão | Propósito |
|------------|--------|-----------|
| Docker | 24+ | Containerização |
| ThingsBoard CLI | - | Automação advanced |

## Configuração do Ambiente ThingsBoard

### Acesso ao ThingsBoard CE

| Configuração | Valor |
|-------------|-------|
| URL | `http://95.217.16.195:8080` |
| Usuário | `scaixeta@gmail.com` |
| Perfil | Tenant Administrator |
| Credenciais | Arquivo `.scr/.env` |

### Credenciais (.scr/.env)

O arquivo `.scr/.env` contém as configurações sensíveis do projeto:

```bash
# ThingsBoard
TB_HOST=95.217.16.195
TB_PORT=8080
TB_URL=http://95.217.16.195:8080
TB_USERNAME=scaixeta@gmail.com
TB_PASSWORD=<obter_de_.scr/.env>
```

**Nota**: Nunca versionar este arquivo. Ele está no `.gitignore`.

## Estrutura Inicial do Projeto

```
Sentivis SIM/
├── README.md                    # Entry point oficial
├── Dev_Tracking.md              # Índice de sprints
├── Dev_Tracking_SX.md           # Sprint ativa
├── docs/
│   ├── SETUP.md                # Este arquivo
│   ├── ARCHITECTURE.md         # Arquitetura técnica
│   ├── DEVELOPMENT.md          # Fluxo de desenvolvimento
│   └── OPERATIONS.md          # Operação e validação
├── rules/
│   └── WORKSPACE_RULES.md      # Regras locais
├── tests/
│   └── bugs_log.md             # Log de bugs
├── Sprint/                     # Sprints arquivadas
└── Templates/                  # Templates locais
```

## Como Validar Acesso ao ThingsBoard

### 1. Acessar a UI

```
http://95.217.16.195:8080
```

Fazer login com as credenciais fornecidas.

### 2. Verificar dispositivo existente

Navegar para: **Entidades > Dispositivos**

Deve existir um dispositivo:
- Nome: `Sentivis | 0001`
- Profile: `default`
- Estado: `Inactive`

### 3. Testar API REST

```bash
# Autenticar (obter JWT token)
curl -X POST http://95.217.16.195:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"scaixeta@gmail.com","password":"<senha>"}'
```

## Ferramentas Recomendadas no VS Code

### Extensões Úteis

| Extensão | Propósito |
|----------|-----------|
| REST Client | Testar APIs REST |
| Thunder Client | Alternativa ao Postman |
| GitLens | Visualização Git |
| Portuguese (Brazil) | Interface PT-BR |
| Python | Suporte Python |
| ESLint | Linting JS/TS |

### Configurações Recomendadas

No `.vscode/settings.json`:

```json
{
  "files.exclude": {
    "**/.scr": true
  },
  "files.associations": {
    "*.env": "dotenv"
  }
}
```

## ThingsBoard Knowledge Layer (Opcional)

### Para que serve

Se você precisar preparar a base local de sincronização da documentação ThingsBoard CE:

1. Clone o repositório `thingsboard.github.io` localmente
2. Execute o script de sincronização:

```powershell
# No diretório do projeto
.\scripts\sync\thingsboard\sync_thingsboard_ce.ps1 -SourcePath "C:\caminho\para\thingsboard.github.io"
```

### Pré-requisitos

- Clone local de `thingsboard.github.io`
- PowerShell 5.1+

### Notas

- Este fluxo é opcional e não é pré-requisito para operar o projeto.
- O script de sync seletivo requer clone local materializado de `thingsboard.github.io`.
- A importação atual cobre apenas markdown CE das trilhas `reference`, `user-guide` e `tutorials`.

## Próximos Passos

1. Validar acesso ao ThingsBoard (UI)
2. Consultar `ARCHITECTURE.md` para entender a arquitetura
3. Consultar `DEVELOPMENT.md` para fluxo de trabalho
4. Consultar `OPERATIONS.md` para validação operacional
