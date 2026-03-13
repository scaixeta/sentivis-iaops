#!/usr/bin/env python3
"""
mgmt_layer_init.py — Inicializador da Camada de Gestão (DOC2.5)

Le WORKSPACE_RULES.md, extrai parametros MGMT_LAYER_*,
aplica o MODE e escreve o observed-state em .scr/mgmt_layer.github_projects.json

Uso:
    python scripts/mgmt_layer_init.py
    python scripts/mgmt_layer_init.py --dry-run
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

RULES_PATH = Path("rules/WORKSPACE_RULES.md")
SCR_DIR = Path(".scr")
STATE_FILE = SCR_DIR / "mgmt_layer.github_projects.json"

DEFAULTS = {
    "MGMT_LAYER_MODE": "off",
    "MGMT_LAYER_TOOL": "github_projects",
    "MGMT_LAYER_REF": "unset",
    "MGMT_LAYER_SPRINT_FIELD": "Sprint",
    "MGMT_LAYER_STATUS_FIELD": "Status",
    "MGMT_LAYER_PRIORITY_FIELD": "Priority",
    "MGMT_LAYER_AREA_FIELD": "Area",
}


def parse_rules(path: Path) -> dict:
    """Extrai parametros MGMT_LAYER_* da tabela em WORKSPACE_RULES.md."""
    params = dict(DEFAULTS)
    if not path.exists():
        print(f"[ERRO] Arquivo nao encontrado: {path}", file=sys.stderr)
        return params

    content = path.read_text(encoding="utf-8")
    # Procura linhas da tabela: | `PARAM` | ... | `valor` |
    pattern = re.compile(r"\|\s*`(MGMT_LAYER_\w+)`\s*\|[^|]+\|\s*`([^`]+)`\s*\|")
    for match in pattern.finditer(content):
        key, value = match.group(1), match.group(2)
        params[key] = value

    return params


def validate_mode(mode: str) -> bool:
    return mode in ("off", "prompt", "on")


def prompt_user() -> bool:
    """Solicita confirmacao interativa quando MODE=prompt."""
    print("\n[MGMT_LAYER] Modo: prompt")
    print("Deseja operar com a camada externa (GitHub Projects) nesta sessao?")
    resp = input("  [s/n]: ").strip().lower()
    return resp in ("s", "sim", "y", "yes")


def main():
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        print("[DRY-RUN] Nenhum arquivo sera criado ou modificado.")

    # 1. Ler parametros
    params = parse_rules(RULES_PATH)
    mode = params.get("MGMT_LAYER_MODE", "off")
    tool = params.get("MGMT_LAYER_TOOL", "github_projects")

    print(f"[INFO] MGMT_LAYER_MODE  = {mode}")
    print(f"[INFO] MGMT_LAYER_TOOL  = {tool}")
    print(f"[INFO] MGMT_LAYER_REF   = {params.get('MGMT_LAYER_REF', 'unset')}")

    if not validate_mode(mode):
        print(f"[ERRO] Valor invalido para MGMT_LAYER_MODE: '{mode}'", file=sys.stderr)
        sys.exit(1)

    # 2. Avaliar modo
    active = False
    if mode == "off":
        print("[INFO] Camada de gestao DESATIVADA (mode=off). Nenhuma acao externa.")
        return
    elif mode == "prompt":
        if not dry_run:
            active = prompt_user()
            if not active:
                print("[INFO] Sessao sem camada externa. Encerrando.")
                return
        else:
            print("[DRY-RUN] mode=prompt — assumindo 'nao' em dry-run.")
            return
    elif mode == "on":
        active = True
        print("[INFO] Camada de gestao ATIVADA (mode=on).")

    if not active:
        return

    # 3. Verificar token (sem expor valor)
    token = os.environ.get("GITHUB_TOKEN") or _read_env_file()
    if not token:
        print(
            "[AVISO] GITHUB_TOKEN nao encontrado. "
            "Configure em .scr/.env antes de executar o provisioning.",
            file=sys.stderr,
        )

    # 4. Escrever observed-state
    state = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "tool": tool,
        "mgmt_layer_ref": params.get("MGMT_LAYER_REF", "unset"),
        "fields": {
            "sprint":   params.get("MGMT_LAYER_SPRINT_FIELD", "Sprint"),
            "status":   params.get("MGMT_LAYER_STATUS_FIELD", "Status"),
            "priority": params.get("MGMT_LAYER_PRIORITY_FIELD", "Priority"),
            "area":     params.get("MGMT_LAYER_AREA_FIELD", "Area"),
        },
        "project_id": None,
        "project_url": None,
        "field_ids": {},
        "view_ids": {},
        "token_present": bool(token),
    }

    if dry_run:
        print("[DRY-RUN] Estado que seria escrito em .scr/mgmt_layer.github_projects.json:")
        print(json.dumps(state, indent=2, ensure_ascii=False))
        return

    SCR_DIR.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] Observed-state escrito em: {STATE_FILE}")


def _read_env_file() -> str | None:
    """Le GITHUB_TOKEN de .scr/.env sem expor o valor."""
    env_path = SCR_DIR / ".env"
    if not env_path.exists():
        return None
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("GITHUB_TOKEN="):
            value = line.split("=", 1)[1].strip()
            return value if value else None
    return None


if __name__ == "__main__":
    main()
