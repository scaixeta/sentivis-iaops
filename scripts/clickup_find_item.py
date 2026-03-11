#!/usr/bin/env python3
import argparse
import json
import os
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


def http_json(url: str, token: str) -> dict:
    req = urllib.request.Request(
        url,
        method="GET",
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


def normalize(s: str) -> str:
    return " ".join((s or "").strip().lower().split())


def match(name: str, needle: str) -> bool:
    return needle in normalize(name)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Localiza item no ClickUp (Space/Folder/List) por nome (substring)."
    )
    parser.add_argument("name", help="Texto para buscar (ex.: 'Sentivis Marketing').")
    parser.add_argument(
        "--workspace-id",
        default="",
        help="Workspace (team) id. Se vazio, tenta ler de `.scr/clickup.config.json`.",
    )
    parser.add_argument(
        "--include-archived",
        action="store_true",
        help="Inclui itens arquivados (quando o endpoint suportar).",
    )
    parser.add_argument(
        "--views",
        action="store_true",
        help="Também busca Views (ex.: board) no Everything level e em Spaces.",
    )
    parser.add_argument(
        "--view-type",
        default="board",
        help="Tipo de view para filtrar quando usar --views (ex.: board, list, calendar, gantt).",
    )
    parser.add_argument(
        "--tasks",
        action="store_true",
        help="Também busca Tasks no workspace (pode ser mais lento).",
    )
    parser.add_argument(
        "--task-pages",
        type=int,
        default=5,
        help="Número de páginas para varrer no endpoint de tasks (100 tasks/página).",
    )
    parser.add_argument(
        "--tasks-include-closed",
        action="store_true",
        help="Inclui tasks fechadas na busca (--tasks).",
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

    needle = normalize(args.name)
    archived_flag = "true" if args.include_archived else "false"

    results: list[dict] = []

    if args.tasks:
        include_closed = "true" if args.tasks_include_closed else "false"
        for page in range(max(1, args.task_pages)):
            team_tasks_url = (
                f"https://api.clickup.com/api/v2/team/{urllib.parse.quote(workspace_id)}/task?"
                + urllib.parse.urlencode({"include_closed": include_closed, "page": str(page)})
            )
            payload = http_json(team_tasks_url, token=token)
            tasks = payload.get("tasks", [])
            if not tasks:
                break
            for t in tasks:
                t_name = t.get("name", "")
                if not match(t_name, needle):
                    continue
                results.append(
                    {
                        "type": "task",
                        "id": t.get("id"),
                        "name": t_name,
                        "status": (t.get("status") or {}).get("status", ""),
                        "url": t.get("url", ""),
                        "list": (t.get("list") or {}).get("name", ""),
                        "folder": (t.get("folder") or {}).get("name", ""),
                        "space": (t.get("space") or {}).get("name", ""),
                    }
                )

    if args.views:
        view_type = normalize(args.view_type)

        # Everything level (Workspace) views
        team_views_url = f"https://api.clickup.com/api/v2/team/{urllib.parse.quote(workspace_id)}/view"
        team_views = http_json(team_views_url, token=token).get("views", [])
        for v in team_views:
            v_id = str(v.get("id", "")).strip()
            v_name = v.get("name", "")
            v_type = normalize(str(v.get("type", "")))
            if v_id and match(v_name, needle) and (not view_type or v_type == view_type):
                results.append(
                    {
                        "type": "view",
                        "id": v_id,
                        "name": v_name,
                        "view_type": v.get("type", ""),
                        "parent_type": "team",
                        "parent_id": workspace_id,
                    }
                )

    # Spaces
    spaces_url = (
        f"https://api.clickup.com/api/v2/team/{urllib.parse.quote(workspace_id)}/space?"
        + urllib.parse.urlencode({"archived": archived_flag})
    )
    spaces = http_json(spaces_url, token=token).get("spaces", [])
    for space in spaces:
        space_id = str(space.get("id", "")).strip()
        space_name = space.get("name", "")
        if space_id and match(space_name, needle):
            results.append({"type": "space", "id": space_id, "name": space_name})

        if not space_id:
            continue

        if args.views:
            view_type = normalize(args.view_type)
            space_views_url = f"https://api.clickup.com/api/v2/space/{urllib.parse.quote(space_id)}/view"
            space_views = http_json(space_views_url, token=token).get("views", [])
            for v in space_views:
                v_id = str(v.get("id", "")).strip()
                v_name = v.get("name", "")
                v_type = normalize(str(v.get("type", "")))
                if v_id and match(v_name, needle) and (not view_type or v_type == view_type):
                    results.append(
                        {
                            "type": "view",
                            "id": v_id,
                            "name": v_name,
                            "view_type": v.get("type", ""),
                            "parent_type": "space",
                            "parent_id": space_id,
                            "space": space_name,
                        }
                    )

        # Folders in space
        folders_url = (
            f"https://api.clickup.com/api/v2/space/{urllib.parse.quote(space_id)}/folder?"
            + urllib.parse.urlencode({"archived": archived_flag})
        )
        folders = http_json(folders_url, token=token).get("folders", [])
        for folder in folders:
            folder_id = str(folder.get("id", "")).strip()
            folder_name = folder.get("name", "")
            if folder_id and match(folder_name, needle):
                results.append(
                    {
                        "type": "folder",
                        "id": folder_id,
                        "name": folder_name,
                        "space": space_name,
                        "space_id": space_id,
                    }
                )

            if not folder_id:
                continue

            # Lists in folder
            lists_url = (
                f"https://api.clickup.com/api/v2/folder/{urllib.parse.quote(folder_id)}/list?"
                + urllib.parse.urlencode({"archived": archived_flag})
            )
            lists = http_json(lists_url, token=token).get("lists", [])
            for lst in lists:
                list_id = str(lst.get("id", "")).strip()
                list_name = lst.get("name", "")
                if list_id and match(list_name, needle):
                    results.append(
                        {
                            "type": "list",
                            "id": list_id,
                            "name": list_name,
                            "folder": folder_name,
                            "folder_id": folder_id,
                            "space": space_name,
                            "space_id": space_id,
                            "url": lst.get("url", ""),
                        }
                    )

        # Lists directly in space (no folder)
        lists_url = (
            f"https://api.clickup.com/api/v2/space/{urllib.parse.quote(space_id)}/list?"
            + urllib.parse.urlencode({"archived": archived_flag})
        )
        lists = http_json(lists_url, token=token).get("lists", [])
        for lst in lists:
            list_id = str(lst.get("id", "")).strip()
            list_name = lst.get("name", "")
            if list_id and match(list_name, needle):
                results.append(
                    {
                        "type": "list",
                        "id": list_id,
                        "name": list_name,
                        "space": space_name,
                        "space_id": space_id,
                        "url": lst.get("url", ""),
                    }
                )

    print(json.dumps({"query": args.name, "count": len(results), "results": results}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
