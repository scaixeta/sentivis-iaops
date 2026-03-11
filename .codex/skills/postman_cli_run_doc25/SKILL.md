---
name: postman_cli_run_doc25
description: Executa Postman CLI com collection local, gera artefatos e valida variáveis de ambiente. Segue padrão DOC2.5.
---

# Postman CLI Run - DOC2.5

## Quando Usar

Usar para executar collections Postman via CLI no ambiente Windows, gerar relatórios de execução e validar variáveis de ambiente necessárias.

## Procedimento

### 1. Preparação

1. Verificar se Postman CLI está instalado:
   ```powershell
   postman-cli --version
   ```

2. Localizar a collection e arquivo .env:
   - Collection: `<path>` (informado pelo usuário)
   - Env: `<path>` (informado pelo usuário)

### 2. Execução Segura via Wrapper
**REGRA CRÍTICA DE EXECUÇÃO**: É estritamente proibido criar arquivos JSON de ambiente permanentes em `artifacts/` contendo segredos ou passá-los inline no terminal onde podem vazar nos logs. 

Você **DEVE** utilizar o script wrapper seguro localizado no projeto:
```powershell
# Execução Segura recomendada
.\scripts\run-postman.ps1
```
Este script lerá as variáveis de `.scr/.env`, criará um arquivo temporário no diretório `%TEMP%`, executará a collection e deletará o JSON temporário imediatamente, mitigando o risco de vazamento em `artifacts/`.

### 3. Validação de Variáveis

Antes de executar, validar se todas as chaves requeridas existem no .env:

| Variável | Obrigatório | Propósito |
|----------|-------------|-----------|
| SNOW_BASE_URL | Sim | URL base do ServiceNow |
| SNOW_USERNAME | Sim | Usuário para autenticação |
| SNOW_PASSWORD | Sim | Senha para autenticação Basic |
| SNOW_TOKEN | Opcional | Token/API Key |
| SNOW_AUTH_METHOD | Opcional | basic, bearer, oauth2 |

### 4. Geração de Artefatos

A skill gera os seguintes artefatos em `<artifacts>/postman-cli-run/<timestamp>/`:

- `run-summary.md` - Resumo da execução
- `test-results.json` - Resultados dos testes
- `execution-log.txt` - Log completo

### 5. Mascaramento de Segredos

**REGRA CRÍTICA**: Nunca expor tokens, senhas ou credenciais em logs ou relatórios.

- Valores em `.env` devem ser mascarados: `SNOW_PASSWORD=******`
- Em relatórios, usar: `PRESENT` ou `AUSENTE` - nunca o valor real

## Restrições DOC2.5

- Não sugerir commit/push sem comando explícito do PO
- Não versionar credenciais ou segredos
- Artefatos gerados em `artifacts/` do projeto (não versionar)
- Manter execução mínima e rastreável

## Dependências

- Postman CLI 1.16.0+
- Collection JSON válida
- Arquivo .env com variáveis necessárias

## Exemplo de Uso

```powershell
> .\scripts\run-postman.ps1
```

## Observações

- A execução direta do comando CLI só deve ser feita se o Postman estiver lendo variáveis locais ausentes de segredos.
- Para qualquer injenção de `.scr/.env`, **recorra sempre ao PowerShell wrapper** (`run-postman.ps1`).
- O Postman CLI usa `postman-cli` (não `postman`) no Windows.
