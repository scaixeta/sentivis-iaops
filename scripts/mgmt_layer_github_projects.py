#!/usr/bin/env python3
"""
mgmt_layer_github_projects.py — Operacoes GitHub Projects v2 (GraphQL API)

Comandos:
    status      Imprime estado atual e valida configuracao
    provision   Cria/descobre Project, campos e views minimas
    sync        Sincroniza items (issues) com Dev_Tracking_S1.md

Uso:
    python scripts/mgmt_layer_github_projects.py status
    python scripts/mgmt_layer_github_projects.py provision --dry-run
    python scripts/mgmt_layer_github_projects.py sync --dry-run

Dependencias:
    - GITHUB_TOKEN em .scr/.env (ou variavel de ambiente)
    - Python 3.9+
    - Sem dependencias externas (usa urllib padrao)
"""

import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

SCR_DIR       = Path(".scr")
STATE_FILE    = SCR_DIR / "mgmt_layer.github_projects.json"
RULES_PATH    = Path("rules/WORKSPACE_RULES.md")
TRACKING_FILE = Path("Dev_Tracking_S1.md")

GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

# ---------------------------------------------------------------------------
# Helpers de autenticacao
# ---------------------------------------------------------------------------

def get_token() -> str:
    """Carrega GITHUB_TOKEN sem expor o valor nos logs."""
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        env_path = SCR_DIR / ".env"
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("GITHUB_TOKEN="):
                    token = line.split("=", 1)[1].strip()
                    break
    if not token:
        print(
            "[ERRO] GITHUB_TOKEN nao encontrado.\n"
            "  Configure em .scr/.env ou exporte a variavel antes de executar.",
            file=sys.stderr,
        )
        sys.exit(1)
    return token


# ---------------------------------------------------------------------------
# Cliente GraphQL minimo (sem dependencias externas)
# ---------------------------------------------------------------------------

def graphql(query: str, variables: dict, token: str) -> dict:
    """Executa uma query/mutation GraphQL contra a API do GitHub."""
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(
        GITHUB_GRAPHQL_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github+json",
            "X-Github-Next-Global-ID": "1",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        print(f"[ERRO HTTP {exc.code}] {exc.reason}", file=sys.stderr)
        sys.exit(1)

    if "errors" in body:
        for err in body["errors"]:
            print(f"[ERRO GraphQL] {err.get('message', err)}", file=sys.stderr)
        sys.exit(1)

    return body.get("data", {})


# ---------------------------------------------------------------------------
# Queries e Mutations
# ---------------------------------------------------------------------------

QUERY_VIEWER = """
query {
  viewer { login }
}
"""

QUERY_USER_PROJECTS = """
query($login: String!, $first: Int!) {
  user(login: $login) {
    projectsV2(first: $first) {
      nodes { id title url number }
    }
  }
}
"""

MUTATION_CREATE_PROJECT = """
mutation($ownerId: ID!, $title: String!) {
  createProjectV2(input: { ownerId: $ownerId, title: $title }) {
    projectV2 { id title url number }
  }
}
"""

QUERY_PROJECT_FIELDS = """
query($projectId: ID!) {
  node(id: $projectId) {
    ... on ProjectV2 {
      fields(first: 20) {
        nodes {
          ... on ProjectV2Field { id name }
          ... on ProjectV2SingleSelectField { id name options { id name } }
          ... on ProjectV2IterationField { id name }
        }
      }
    }
  }
}
"""

MUTATION_CREATE_FIELD = """
mutation($projectId: ID!, $dataType: ProjectV2CustomFieldType!, $name: String!) {
  createProjectV2Field(input: {
    projectId: $projectId
    dataType: $dataType
    name: $name
  }) {
    projectV2Field {
      ... on ProjectV2Field { id name }
      ... on ProjectV2SingleSelectField { id name }
      ... on ProjectV2IterationField { id name }
    }
  }
}
"""

QUERY_USER_ID = """
query($login: String!) {
  user(login: $login) { id }
}
"""


# ---------------------------------------------------------------------------
# Carrega configuracao local
# ---------------------------------------------------------------------------

def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def save_state(state: dict):
    SCR_DIR.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def load_rules_params() -> dict:
    """Extrai MGMT_LAYER_* de WORKSPACE_RULES.md (mesma logica do mgmt_layer_init.py)."""
    import re
    params = {}
    if not RULES_PATH.exists():
        return params
    content = RULES_PATH.read_text(encoding="utf-8")
    pattern = re.compile(r"\|\s*`(MGMT_LAYER_\w+)`\s*\|[^|]+\|\s*`([^`]+)`\s*\|")
    for m in pattern.finditer(content):
        params[m.group(1)] = m.group(2)
    return params


# ---------------------------------------------------------------------------
# Comandos
# ---------------------------------------------------------------------------

def cmd_status():
    """Imprime estado atual e valida configuracao."""
    params = load_rules_params()
    state = load_state()

    print("=== Camada de Gestao — Status ===")
    print(f"  MGMT_LAYER_MODE   : {params.get('MGMT_LAYER_MODE', 'N/A')}")
    print(f"  MGMT_LAYER_TOOL   : {params.get('MGMT_LAYER_TOOL', 'N/A')}")
    print(f"  MGMT_LAYER_REF    : {params.get('MGMT_LAYER_REF', 'N/A')}")
    print()

    if state:
        print("  Observed-state (local):")
        print(f"    project_id      : {state.get('project_id', 'N/A')}")
        print(f"    project_url     : {state.get('project_url', 'N/A')}")
        print(f"    token_present   : {state.get('token_present', False)}")
        print(f"    generated_at    : {state.get('generated_at', 'N/A')}")
        fids = state.get("field_ids", {})
        if fids:
            print(f"    field_ids       : {fids}")
    else:
        print("  Observed-state: ausente (execute 'provision' primeiro)")

    mode = params.get("MGMT_LAYER_MODE", "off")
    if mode == "off":
        print("\n  [INFO] Modulo desativado (MGMT_LAYER_MODE=off).")
    else:
        print(f"\n  [OK] Modulo configurado no modo '{mode}'.")


def cmd_provision(dry_run: bool = False):
    """Cria/descobre Project + campos + views minimas."""
    params = load_rules_params()
    mode = params.get("MGMT_LAYER_MODE", "off")
    if mode == "off":
        print("[INFO] MGMT_LAYER_MODE=off. Nada a provisionar.")
        return

    token = get_token()

    # 1. Identificar viewer
    data = graphql(QUERY_VIEWER, {}, token)
    login = data["viewer"]["login"]
    print(f"[INFO] Autenticado como: {login}")

    # 2. Descobrir ou criar Project
    proj_title = "Sentivis AIOps — Camada de Gestao"
    ref = params.get("MGMT_LAYER_REF", "unset")

    # Buscar projetos existentes
    data = graphql(QUERY_USER_PROJECTS, {"login": login, "first": 20}, token)
    projects = data.get("user", {}).get("projectsV2", {}).get("nodes", [])
    project = next((p for p in projects if p["title"] == proj_title), None)

    if project:
        print(f"[OK] Project encontrado: {project['url']}")
    else:
        if dry_run:
            print(f"[DRY-RUN] Criaria Project '{proj_title}'.")
            return
        # Obter owner ID
        data = graphql(QUERY_USER_ID, {"login": login}, token)
        owner_id = data["user"]["id"]
        data = graphql(MUTATION_CREATE_PROJECT, {"ownerId": owner_id, "title": proj_title}, token)
        project = data["createProjectV2"]["projectV2"]
        print(f"[OK] Project criado: {project['url']}")

    project_id = project["id"]

    # 3. Validar/criar campos obrigatorios
    desired_fields = {
        params.get("MGMT_LAYER_SPRINT_FIELD", "Sprint"):    "ITERATION",
        params.get("MGMT_LAYER_STATUS_FIELD", "Status"):    None,   # campo built-in
        params.get("MGMT_LAYER_PRIORITY_FIELD", "Priority"): "SINGLE_SELECT",
        params.get("MGMT_LAYER_AREA_FIELD", "Area"):          "TEXT",
    }

    data = graphql(QUERY_PROJECT_FIELDS, {"projectId": project_id}, token)
    existing = {f.get("name"): f.get("id") for f in data["node"]["fields"]["nodes"] if f}

    field_ids = dict(existing)
    for fname, ftype in desired_fields.items():
        if fname in existing:
            print(f"[OK] Campo '{fname}' ja existe (id={existing[fname]}).")
        elif ftype is None:
            print(f"[INFO] Campo '{fname}' e built-in, ignorado.")
        elif dry_run:
            print(f"[DRY-RUN] Criaria campo '{fname}' (tipo={ftype}).")
        else:
            data = graphql(
                MUTATION_CREATE_FIELD,
                {"projectId": project_id, "dataType": ftype, "name": fname},
                token,
            )
            created = data.get("createProjectV2Field", {}).get("projectV2Field", {})
            field_ids[fname] = created.get("id")
            print(f"[OK] Campo '{fname}' criado (id={field_ids[fname]}).")

    # 4. Salvar observed-state
    state = load_state()
    state.update({
        "project_id": project_id,
        "project_url": project.get("url"),
        "project_number": project.get("number"),
        "field_ids": field_ids,
        "token_present": True,
    })

    if dry_run:
        print("[DRY-RUN] Estado que seria salvo:")
        print(json.dumps(state, indent=2, ensure_ascii=False))
    else:
        save_state(state)
        print(f"[OK] Observed-state atualizado em: {STATE_FILE}")


def cmd_sync(dry_run: bool = False):
    """
    Sincroniza items entre GitHub Project e Dev_Tracking_S1.md.
    MVP: lista itens do tracking local marcados como 'To-Do' ou 'Doing'
    e informa o que seria criado como Issue.
    """
    if not TRACKING_FILE.exists():
        print(f"[ERRO] {TRACKING_FILE} nao encontrado.", file=sys.stderr)
        sys.exit(1)

    state = load_state()
    if not state.get("project_id"):
        print("[ERRO] Project nao provisionado. Execute 'provision' primeiro.", file=sys.stderr)
        sys.exit(1)

    import re
    content = TRACKING_FILE.read_text(encoding="utf-8")
    pattern = re.compile(r"\|\s*(To-Do|Doing)\s*\|\s*(ST-S\d+-\d+[^|]*)\|")
    items = [(m.group(1).strip(), m.group(2).strip()) for m in pattern.finditer(content)]

    if not items:
        print("[INFO] Nenhum item 'To-Do' ou 'Doing' encontrado no Dev_Tracking.")
        return

    print(f"[INFO] {len(items)} item(s) candidatos a sincronizacao:")
    for status, title in items:
        print(f"  [{status}] {title}")

    if dry_run:
        print("\n[DRY-RUN] Nenhuma Issue criada.")
        return

    print("\n[INFO] Criacao de Issues via API requer implementacao da Fase 5.")
    print("       Execute com '--dry-run' para pre-visualizar ou aguarde aprovacao do PO.")


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

COMMANDS = {
    "status":    cmd_status,
    "provision": cmd_provision,
    "sync":      cmd_sync,
}


def main():
    args = sys.argv[1:]
    if not args or args[0] not in COMMANDS:
        print(f"Uso: python {sys.argv[0]} <status|provision|sync> [--dry-run]")
        sys.exit(1)

    cmd = args[0]
    dry_run = "--dry-run" in args

    if cmd == "status":
        cmd_status()
    elif cmd == "provision":
        cmd_provision(dry_run=dry_run)
    elif cmd == "sync":
        cmd_sync(dry_run=dry_run)


if __name__ == "__main__":
    main()
