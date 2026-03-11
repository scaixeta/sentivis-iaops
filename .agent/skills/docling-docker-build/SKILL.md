---
name: docling-docker-build
description: Dockerizacao do projeto Docling, build e troubleshooting da imagem/compose com foco em timeouts do torch, proxy/SSL corporativo e cache do HuggingFace. Use quando houver falhas em `docker compose build`, necessidade de ajustar `docker/Dockerfile` ou `docker/compose.yaml`, ou para orientar a execucao via Docker do Docling.
---

# Docling Docker Build

## Visao geral
Orientar build, troubleshooting e execucao do Docling via Docker/Compose com foco em estabilidade de downloads (torch), proxy/SSL corporativo e cache do HuggingFace.

## Workflow recomendado
1. **Coletar contexto Docker**
   - Ler `docker/Dockerfile`, `docker/compose.yaml`, `docs/SETUP.md`, `docs/OPERATIONS.md`.
   - Usar `references/docling-docker-context.md` para resumo rapido.

2. **Diagnosticar falha de build**
   - Identificar host do download e tipo de erro (timeout, SSL, proxy auth).
   - Evitar `--no-cache` quando o objetivo for reaproveitar downloads.

3. **Propor ajustes minimos**
   - A: Instalar `torch` via indice CPU oficial antes do `poetry install`.
   - B: Habilitar BuildKit e cache de pip para reduzir re-download.
   - C: Suporte a `HTTP_PROXY/HTTPS_PROXY/NO_PROXY` e `REQUESTS_CA_BUNDLE` via `.env`.

4. **Garantir cache HF em volume Linux**
   - Manter `HF_HOME`/`XDG_CACHE_HOME` apontando para volumes nomeados.
   - Evitar bind mount do cache em NTFS para nao disparar erro de symlink.

5. **Validar execucao**
   - `docker compose -f docker/compose.yaml build`
   - `docker compose -f docker/compose.yaml run --rm docling-pipeline /app/input/<arquivo>`
   - Verificar `output/<arquivo>.md` e `output/<arquivo>.json`.

6. **Rastreabilidade DOC2.5**
   - Atualizar `Dev_Tracking_S0.md` (append-only) com evidencias e decisoes.
   - Registrar falhas e testes em `tests/bugs_log.md`.

## Decisoes e guardrails
- Nao expor credenciais em docs; usar placeholders e `.env`.
- Nao alterar fora de `docling/` sem autorizacao.
- Commits apenas por comando expresso do PO.

## Referencias
- `references/docling-docker-context.md`
