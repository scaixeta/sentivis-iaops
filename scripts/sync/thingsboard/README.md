# sync_thingsboard_ce.ps1

## Purpose

Executar a importação seletiva do ThingsBoard CE para a Knowledge Layer local, mantendo o escopo aprovado do projeto.

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `-SourcePath` | Yes | Local path do repositório upstream materializado |
| `-ProjectPath` | No | Root do projeto (default: current directory) |
| `-DryRun` | No | Simula ações sem escrita |

## Dry-run usage

```powershell
.\scripts\sync\thingsboard\sync_thingsboard_ce.ps1 -SourcePath "C:\repos\thingsboard.github.io" -ProjectPath "C:\01 - Sentivis\Sentivis SIM" -DryRun
```

## Imported source groups

- `_includes/docs/reference/**/*.md` -> `knowledge/thingsboard/ce/api/`
- `_includes/docs/user-guide/**/*.md` -> `knowledge/thingsboard/ce/user-guide/`
- `_includes/docs/tutorials/**/*.md` -> `knowledge/thingsboard/ce/tutorials/`

## Managed folders

- `third_party/thingsboard-ce/upstream/`
- `knowledge/thingsboard/ce/manifests/`
- `knowledge/thingsboard/ce/reference/`
- `knowledge/thingsboard/ce/runbooks/`
- `knowledge/thingsboard/ce/api/`
- `knowledge/thingsboard/ce/user-guide/`
- `knowledge/thingsboard/ce/tutorials/`

## Safety rules

- Valida `SourcePath` e `ProjectPath` antes de qualquer ação.
- Falha se o clone local não estiver materializado com `_includes/docs/`.
- Não remove conteúdo fora das pastas gerenciadas.
- Mantém o import estritamente em markdown CE aprovado.

## Exclusions

- `**/pe/**`
- `**/cloud/**`
- `**/edge/**`
- assets não markdown (`png`, `jpg`, `svg`)
- scripts de apoio (`*.sh`)
- wrappers de navegação não substantivos

## Current limitation

- O script depende de um clone local já materializado do upstream.
