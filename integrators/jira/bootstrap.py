#!/usr/bin/env python3
"""
jira/bootstrap.py - Bootstrap da Camada Jira DOC2.5

Inicializa a camada de gestão Jira:
- Valida credenciais
- Autentica no Jira
- Descobre projeto e metadados
- Persiste estado observado

Uso:
    from integrators.jira import bootstrap
    bootstrap.run()
    bootstrap.run(dry_run=True)
"""

import sys
from pathlib import Path

from .client import JiraClient
from .state import JiraState, load_state, save_state, validate_state


def discover_jira(client: JiraClient, project_key: str) -> JiraState:
    """Executa discovery e retorna estado observado."""
    state = JiraState()
    state.project_key = project_key

    # 1. Autentica usuario
    print("[1/4] Validando credenciais...")
    user = client.get_myself()
    state.authenticated_user = {
        "account_id": user.get("accountId"),
        "display_name": user.get("displayName"),
        "email": user.get("emailAddress"),
    }
    print(f"    Usuario: {state.authenticated_user.get('display_name')}")

    # 2. Busca projeto
    print("[2/4] Buscando projeto...")
    project = client.get_project(project_key)
    state.project_id = project.get("id", "")
    state.project_type = project.get("projectTypeKey", "")
    state.project_name = project.get("name", "")
    print(f"    Projeto: {project_key} ({state.project_name})")

    # 3. Busca issue types
    print("[3/4] Mapeando issue types...")
    issue_types = client.get_issue_types()
    state.issue_type_map = {}
    for it in issue_types:
        name = it.get("name", "")
        it_id = it.get("id", "")
        state.issue_type_map[name] = it_id
    print(f"    Encontrados: {len(state.issue_type_map)} tipos")

    # 4. Busca statuses
    print("[4/4] Mapeando statuses...")
    statuses = client.get_statuses()
    state.status_map = {}
    for st in statuses:
        name = st.get("name", "")
        st_id = st.get("id", "")
        state.status_map[name] = st_id
    print(f"    Encontrados: {len(state.status_map)} statuses")

    return state


def run(dry_run: bool = False) -> int:
    """
    Executa o bootstrap da camada Jira.
    
    Args:
        dry_run: Se True, apenas simula sem criar arquivos
        
    Returns:
        0 para sucesso, 1 para erro
    """
    if dry_run:
        print("[DRY-RUN] Modo de simulacao - nenhum arquivo sera criado.\n")

    print("=" * 60)
    print(" Integrators/Jira Bootstrap")
    print("=" * 60)
    print()

    # 1. Verifica credenciais
    print("[INFO] Verificando credenciais em .scr/.env...")
    try:
        client = JiraClient()
        print("[OK] Credenciais carregadas\n")
    except Exception as e:
        print(f"[ERRO] {e}")
        return 1

    # 2. Carrega project key do .env ou usa padrao
    env_path = Path(".scr/.env")
    project_key = "STVIA"  # padrao

    if env_path.exists():
        content = env_path.read_text()
        for line in content.splitlines():
            if line.startswith("JIRA_PROJECT_KEY="):
                project_key = line.split("=", 1)[1].strip()
                break

    print(f"[INFO] Projeto alvo: {project_key}\n")

    # 3. Verifica se estado ja existe
    existing_state = load_state()
    state = None

    if existing_state and existing_state.project_key == project_key:
        print("[INFO] Estado existente encontrado.")
        print(f"    Projeto: {existing_state.project_key}")
        print(f"    Ultima observacao: {existing_state.observed_at}")
        print()
        
        if dry_run:
            print("[DRY-RUN] Estado existente sera usado para simulacao.")
            print("[DRY-RUN] Nenhum arquivo sera sobrescrito.")
            state = existing_state
        else:
            resp = input("Deseja sobrescrever? [s/N]: ").strip().lower()
            if resp != "s":
                print("[INFO] Operacao cancelada.")
                return 0
            state = None

    # 4. Executa discovery apenas se necessario
    if state is None:
        try:
            state = discover_jira(client, project_key)
        except Exception as e:
            print(f"[ERRO] Discovery falhou: {e}")
            return 1

    print()
    print("[INFO] Validando estado...")
    issues = validate_state(state)
    if issues:
        print("[AVISO] Problemas encontrados:")
        for issue in issues:
            print(f"    - {issue}")
    else:
        print("[OK] Estado valido")

    # 5. Salva estado
    print()
    if dry_run:
        print("[DRY-RUN] Estado que seria salvo:")
        import json
        print(json.dumps(state.to_dict(), indent=2, ensure_ascii=False))
    else:
        save_state(state)
        print("[OK] Bootstrap concluido!")
        print(f"    Estado salvo em: .scr/mgmt_layer.jira.json")

    return 0


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    sys.exit(run(dry_run=dry_run))
