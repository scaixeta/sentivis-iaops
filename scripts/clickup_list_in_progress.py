#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


def load_dotenv(dotenv_path: Path) -> dict[str, str]:
    if not dotenv_path.exists():
        return {}

    env: dict[str, str] = {}
    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            env[key] = value
    return env


def http_json(method: str, url: str, token: str) -> dict:
    req = urllib.request.Request(
        url,
        method=method,
        headers={"Authorization": token, "Accept": "application/json"},
    )
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


def is_in_progress(status_value: str) -> bool:
    value = status_value.strip().lower()
    if not value:
        return False

    patterns = [
        r"\bin\s*progress\b",
        r"\bem\s*progresso\b",
        r"\bdoing\b",
        r"\bprogress\b",
    ]
    return any(re.search(p, value) for p in patterns)


def safe_get(obj: dict, path: list[str], default: str = "") -> str:
    cur = obj
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur if isinstance(cur, str) else default


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Lista tarefas 'em progresso' no ClickUp (filtradas por nome do status)."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Quantidade máxima de tarefas retornadas (após filtrar).",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=3,
        help="Quantidade de páginas a buscar na API (100 tasks/página).",
    )
    parser.add_argument(
        "--workspace-id",
        default="",
        help="Workspace (team) id. Se vazio, tenta ler de `.scr/clickup.config.json`.",
    )
    parser.add_argument(
        "--assignee-me",
        action="store_true",
        help="Filtra por tarefas atribuídas ao usuário autenticado.",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    dotenv = load_dotenv(project_root / ".scr" / ".env")

    token = os.environ.get("CLICKUP_TOKEN") or dotenv.get("CLICKUP_TOKEN")
    if not token:
        print("Faltando CLICKUP_TOKEN (env var ou `.scr/.env`).", file=sys.stderr)
        return 2

    workspace_id = args.workspace_id
    if not workspace_id:
        config_path = project_root / ".scr" / "clickup.config.json"
        if config_path.exists():
            try:
                config = json.loads(config_path.read_text(encoding="utf-8"))
                workspace_id = str(config.get("clickup", {}).get("workspace_id", "")).strip()
            except Exception:
                workspace_id = ""

    if not workspace_id:
        print("Faltando workspace_id. Rode `scripts/clickup_smoke_test.py` primeiro.", file=sys.stderr)
        return 3

    assignee_id = None
    if args.assignee_me:
        me = http_json("GET", "https://api.clickup.com/api/v2/user", token=token)
        assignee_id = me.get("user", {}).get("id")

    collected: list[dict] = []
    for page in range(max(1, args.pages)):
        query: dict[str, object] = {
            "include_closed": "false",
            "page": str(page),
        }
        if assignee_id is not None:
            query["assignees[]"] = [str(assignee_id)]

        url = (
            f"https://api.clickup.com/api/v2/team/{urllib.parse.quote(workspace_id)}/task?"
            + urllib.parse.urlencode(query, doseq=True)
        )
        payload = http_json("GET", url, token=token)
        tasks = payload.get("tasks", [])
        if not tasks:
            break
        collected.extend(tasks)

    in_progress = []
    for t in collected:
        status_name = safe_get(t, ["status", "status"])
        if is_in_progress(status_name):
            in_progress.append(
                {
                    "id": t.get("id"),
                    "name": t.get("name"),
                    "status": status_name,
                    "url": t.get("url"),
                    "list": safe_get(t, ["list", "name"]),
                    "space": safe_get(t, ["space", "name"]),
                }
            )

    in_progress = in_progress[: max(0, args.limit)]
    print(json.dumps({"count": len(in_progress), "tasks": in_progress}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

