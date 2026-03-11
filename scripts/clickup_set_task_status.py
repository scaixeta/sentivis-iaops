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


def normalize(s: str) -> str:
    return " ".join((s or "").strip().lower().split())


def extract_task_id(task_or_url: str) -> str:
    s = task_or_url.strip()
    if not s:
        return ""
    if re.fullmatch(r"[A-Za-z0-9]+", s):
        return s
    m = re.search(r"/t/([A-Za-z0-9]+)", s)
    return m.group(1) if m else ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Atualiza status de uma task no ClickUp (mapeando pelo nome do status da List)."
    )
    parser.add_argument("task", help="Task ID (ex.: 86a8qyr8t) ou URL do ClickUp.")
    parser.add_argument(
        "--status",
        default="Fechadas",
        help="Nome do status de destino (default: Fechadas).",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    dotenv = load_dotenv(project_root / ".scr" / ".env")
    token = os.environ.get("CLICKUP_TOKEN") or dotenv.get("CLICKUP_TOKEN")
    if not token:
        print("Faltando CLICKUP_TOKEN (env var ou `.scr/.env`).", file=sys.stderr)
        return 2

    task_id = extract_task_id(args.task)
    if not task_id:
        print("Não consegui extrair task_id do input.", file=sys.stderr)
        return 3

    task = http_json("GET", f"https://api.clickup.com/api/v2/task/{urllib.parse.quote(task_id)}", token=token)
    current_status = (task.get("status") or {}).get("status", "")
    list_id = str((task.get("list") or {}).get("id", "")).strip()
    list_name = (task.get("list") or {}).get("name", "")
    task_name = task.get("name", "")

    if not list_id:
        print("Task retornou sem list.id; não é possível mapear statuses.", file=sys.stderr)
        return 4

    lst = http_json("GET", f"https://api.clickup.com/api/v2/list/{urllib.parse.quote(list_id)}", token=token)
    statuses = lst.get("statuses", []) or []

    desired = normalize(args.status)
    target_status = None
    for st in statuses:
        st_name = normalize(str(st.get("status", "")))
        if st_name == desired:
            target_status = st
            break

    if target_status is None:
        # fallback: qualquer status "closed"
        for st in statuses:
            if normalize(str(st.get("type", ""))) == "closed":
                target_status = st
                break

    if target_status is None:
        available = [st.get("status") for st in statuses if st.get("status")]
        print(
            "Não encontrei um status compatível na List.\n"
            f"- List: {list_name} (id={list_id})\n"
            f"- Status desejado: {args.status}\n"
            f"- Disponíveis: {available}",
            file=sys.stderr,
        )
        return 5

    target_name = str(target_status.get("status", "")).strip()
    if not target_name:
        print("Status alvo inválido (sem nome).", file=sys.stderr)
        return 6

    http_json(
        "PUT",
        f"https://api.clickup.com/api/v2/task/{urllib.parse.quote(task_id)}",
        token=token,
        body={"status": target_name},
    )

    updated = http_json(
        "GET",
        f"https://api.clickup.com/api/v2/task/{urllib.parse.quote(task_id)}",
        token=token,
    )
    new_status = (updated.get("status") or {}).get("status", "")

    print("OK: status atualizado.")
    print(f"- Task: {task_name} (id={task_id})")
    print(f"- List: {list_name} (id={list_id})")
    print(f"- Status: {current_status} -> {new_status}")
    print(f"- URL: {updated.get('url', task.get('url', ''))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

