# Docling Docker Context (Repo)

## Arquivos-alvo
- `docling/docker/Dockerfile`
- `docling/docker/compose.yaml`
- `docling/docs/SETUP.md`
- `docling/docs/OPERATIONS.md`
- `docling/Dev_Tracking_S0.md`

## Dockerfile (estado atual)
- Base: `python:3.13-slim`
- ENV:
  - `POETRY_VERSION=1.8.3`
  - `POETRY_VIRTUALENVS_CREATE=false`
  - `POETRY_NO_INTERACTION=1`
  - `PYTHONUNBUFFERED=1`
  - `HF_HOME=/cache/hf`
  - `XDG_CACHE_HOME=/cache/xdg`
  - `PIP_DEFAULT_TIMEOUT=1200`
  - `POETRY_HTTP_TIMEOUT=1200`
- System deps: `build-essential`, `libglib2.0-0`, `libgl1`, `libmagic1`, `tesseract-ocr`, `poppler-utils`
- Poetry: `pip install --upgrade pip setuptools` + `pip install poetry==1.8.3`
- Install: `poetry install --no-root`
- Entry: `python -m docling_pipeline.converter`

## Compose (estado atual)
- Serviço: `docling-pipeline`
- Build: context `..`, dockerfile `docker/Dockerfile`
- Env: `HF_HOME`, `XDG_CACHE_HOME`, `PYTHONUNBUFFERED`
- Volumes:
  - `../input:/app/input:rw`
  - `../output:/app/output:rw`
  - `docling_hf_cache:/cache/hf`
  - `docling_xdg_cache:/cache/xdg`
- Entry: `python -m docling_pipeline.converter`

## Docs relevantes (resumo)
- `docs/SETUP.md`: build via `docker compose -f docker/compose.yaml build` e run via compose; usa `.env` para proxy/CA; destaca que cache HF deve ficar em volumes Linux para evitar symlink no Windows.
- `docs/OPERATIONS.md`: troubleshooting de timeout no download de `torch` (proxy/SSL); recomenda configurar proxy/CA em `docker/.env`, reexecutar build com cache e aumentar timeouts no Dockerfile.

## Observacoes praticas
- Evitar `--no-cache` quando objetivo for reaproveitar downloads.
- Em rede corporativa, priorizar configuracao de proxy/CA via `docker/.env`.
- Cache de HF deve permanecer em volumes Docker (Linux), nao bind mount no NTFS.
