# SETUP

## Proposito

Orientar como preparar o ambiente local para trabalhar com este projeto.

## Requisitos minimos

- Git
- Bash ou PowerShell
- Editor de texto ou IDE

## Requisitos opcionais

- PowerShell 7+ para scripts `.ps1`
- Python 3.10+ se o projeto usar utilitarios Python

## Instalacao

### 1. Clonar o repositorio

```bash
git clone [URL_DO_REPOSITORIO]
cd [NOME_DO_PROJETO]
```

### 2. Validar a estrutura base

```bash
ls
ls docs
ls rules
ls tests
```

### 3. Configuracoes locais

Se o projeto possuir arquivo de ambiente versionado como exemplo, seguir a convencao definida pelo proprio repositorio. Nao presumir `.env.example` se o arquivo nao existir.

## Estrutura inicial do projeto

```
[NOME_DO_PROJETO]/
├── README.md
├── Dev_Tracking.md
├── Dev_Tracking_SX.md
├── docs/
├── rules/
├── tests/
├── Templates/
└── Sprint/
```

## Proximos passos

- Ler `ARCHITECTURE.md`
- Ler `DEVELOPMENT.md`
- Ler `OPERATIONS.md`
