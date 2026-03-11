#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


def load_dotenv(dotenv_path: Path) -> dict[str, str]:
    if not dotenv_path.exists():
        return {}

    env: dict[str, str] = {}
    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            env[key] = value
    return env


def http_json(method: str, url: str, token: str, body: dict | None = None) -> dict:
    data = None
    headers = {"Authorization": token, "Accept": "application/json"}

    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, method=method, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = resp.read().decode("utf-8")
            return json.loads(payload) if payload else {}
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = e.read().decode("utf-8")
        except Exception:
            detail = ""
        raise RuntimeError(f"HTTP {e.code} {e.reason} ({url})\n{detail}".rstrip()) from e


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gera config mínima do ClickUp via API e executa smoke test (auth + /team)."
    )
    parser.add_argument(
        "--out",
        default=".scr/clickup.config.json",
        help="Arquivo de saída (relativo ao root do projeto).",
    )
    parser.add_argument(
        "--workspace-id",
        default="",
        help="Workspace (team) id. Se vazio, escolhe o primeiro retornado por /team.",
    )
    parser.add_argument(
        "--workspace-name",
        default="",
        help="Workspace (team) name. Usado para selecionar o workspace quando houver múltiplos.",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    dotenv_path = project_root / ".scr" / ".env"
    dotenv = load_dotenv(dotenv_path)

    token = os.environ.get("CLICKUP_TOKEN") or dotenv.get("CLICKUP_TOKEN")
    if not token:
        print(
            "Faltando CLICKUP_TOKEN.\n"
            "- Opção A: export CLICKUP_TOKEN=\"pk_...\"\n"
            "- Opção B: adicionar CLICKUP_TOKEN=pk_... em `.scr/.env` (local; não versionar)\n",
            file=sys.stderr,
        )
        return 2

    teams = http_json("GET", "https://api.clickup.com/api/v2/team", token=token).get(
        "teams", []
    )
    if not teams:
        print("API respondeu sem workspaces em /team.", file=sys.stderr)
        return 3

    selected = None
    if args.workspace_id:
        selected = next((t for t in teams if str(t.get("id")) == args.workspace_id), None)
        if selected is None:
            print(
                f"workspace-id `{args.workspace_id}` não encontrado. Disponíveis: "
                + ", ".join(str(t.get("id")) for t in teams),
                file=sys.stderr,
            )
            return 4
    elif args.workspace_name:
        selected = next((t for t in teams if t.get("name") == args.workspace_name), None)
        if selected is None:
            print(
                f"workspace-name `{args.workspace_name}` não encontrado. Disponíveis: "
                + ", ".join(str(t.get("name")) for t in teams),
                file=sys.stderr,
            )
            return 5
    else:
        selected = teams[0]

    config = {
        "clickup": {
            "workspace_id": selected.get("id"),
            "workspace_name": selected.get("name"),
        }
    }

    out_path = project_root / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    workspace_count = len(teams)
    msg_extra = ""
    if workspace_count > 1 and not (args.workspace_id or args.workspace_name):
        msg_extra = (
            f" (atenção: {workspace_count} workspaces encontrados; usando o primeiro — "
            "passe --workspace-id ou --workspace-name para fixar)"
        )

    print("OK: autenticação e leitura de workspaces funcionaram.")
    print(f"- Workspace selecionado: {selected.get('name')} (id={selected.get('id')}){msg_extra}")
    print(f"- Config gerada em: {out_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

