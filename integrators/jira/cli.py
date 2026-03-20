#!/usr/bin/env python3
"""
jira/cli.py - CLI Router para Operações Jira

Router de comandos para operação da camada Jira.

Uso:
    python -m integrators.jira status
    python -m integrators.jira discover
    python -m integrators.jira sync --dry-run
    python -m integrators.jira sync
    python -m integrators.jira reconcile
"""

import sys
from pathlib import Path

# Adiciona raiz ao path para imports relativos
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from integrators.jira.client import JiraClient
from integrators.jira.state import JiraState, load_state, save_state
from integrators.jira.sync_engine import SyncEngine
from integrators.jira.bootstrap import run as bootstrap_run
from integrators.common.doc25_parser import parse_sprint_backlog


def cmd_status():
    """Comando status - mostra estado atual."""
    print("=" * 60)
    print(" STATUS - Jira Integrator")
    print("=" * 60)
    print()

    # Carrega estado
    state = load_state()
    if not state:
        print("[ERRO] Estado nao encontrado.")
        print("Execute primeiro: python -m integrators.jira bootstrap")
        return 1

    # Mostra estado
    print(f"Projeto:     {state.project_key}")
    print(f"ID:          {state.project_id}")
    print(f"Tipo:        {state.project_type}")
    print(f"Observado:   {state.observed_at}")
    print()

    if state.authenticated_user:
        print("Usuario:")
        print(f"  Nome:   {state.authenticated_user.get('display_name')}")
        print(f"  Email:  {state.authenticated_user.get('email')}")
        print()

    print(f"Issue Types: {len(state.issue_type_map)} mapeados")
    print(f"Statuses:    {len(state.status_map)} mapeados")
    print()

    if state.last_sync_fingerprint:
        print(f"Ultima sinc: {state.last_sync_fingerprint}")
    else:
        print("Nenhuma sincronizacao ainda.")

    return 0


def cmd_discover():
    """Comando discover - atualiza metadados do Jira."""
    print("=" * 60)
    print(" DISCOVER - Atualizar Metadados Jira")
    print("=" * 60)
    print()

    # Carrega estado
    state = load_state()
    if not state:
        print("[ERRO] Estado nao encontrado.")
        print("Execute primeiro: python -m integrators.jira bootstrap")
        return 1

    # Executa discover
    try:
        engine = SyncEngine()
        state = JiraState.from_dict(engine.discover())
        save_state(state)
        print()
        print("[OK] Discover concluido!")
    except Exception as e:
        print(f"[ERRO] {e}")
        return 1

    return 0


def cmd_sync(tracking_file: str = "Dev_Tracking_S1.md", dry_run: bool = False):
    """Comando sync - sincroniza tracking com Jira."""
    mode = "DRY-RUN" if dry_run else "SYNC"
    print("=" * 60)
    print(f" {mode} - Sincronizacao DOC2.5 -> Jira")
    print("=" * 60)
    print()
    print(f"Tracking: {tracking_file}")
    print()

    # Carrega estado
    state = load_state()
    if not state:
        print("[ERRO] Estado nao encontrado.")
        print("Execute primeiro: python -m integrators.jira bootstrap")
        return 1

    # Verifica tracking
    tracking_path = Path(tracking_file)
    if not tracking_path.exists():
        print(f"[ERRO] Arquivo nao encontrado: {tracking_file}")
        return 1

    # Executa sync
    try:
        engine = SyncEngine()

        # Carrega itens locais
        result = parse_sprint_backlog(tracking_file)
        print(f"Sprint:    {result['sprint']}")
        print(f"Itens:     {len(result['items'])}")
        print(f"Decisoes:  {len(result['decisions'])}")
        print()

        # Dry-run primeiro
        plan = engine.dry_run(tracking_file)

        if not plan:
            print("[INFO] Nenhuma operacao necessaria.")
            return 0

        print()

        if dry_run:
            print(f"[DRY-RUN] {len(plan)} operacoes pendentes.")
            print("Execute sem --dry-run para aplicar.")
        else:
            # Confirma antes de mutation
            print(f"[ATENCAO] {len(plan)} operacoes serao executadas.")
            resp = input("Continuar? [s/N]: ").strip().lower()
            if resp != "s":
                print("[INFO] Operacao cancelada.")
                return 0

            # Executa sync
            results = engine.sync(plan, dry_run=False)

            # Resume
            success = sum(1 for r in results if r.success)
            failed = sum(1 for r in results if not r.success)
            print()
            print(f"[OK] Sincronizacao concluida: {success} sucesso, {failed} falhas")

    except Exception as e:
        print(f"[ERRO] {e}")
        return 1

    return 0


def cmd_reconcile():
    """Comando reconcile - mostra divergencias."""
    print("=" * 60)
    print(" RECONCILE - Analise de Divergencias")
    print("=" * 60)
    print()

    # Carrega estado
    state = load_state()
    if not state:
        print("[ERRO] Estado nao encontrado.")
        return 1

    # Busca issues Jira
    try:
        client = JiraClient()
        jira_issues = client.get_project_issues(state.project_key, max_results=100)
        issues = jira_issues.get("issues", [])
    except Exception as e:
        print(f"[ERRO] {e}")
        return 1

    # Busca tracking local
    result = parse_sprint_backlog("Dev_Tracking_S1.md")
    local_items = result.get("items", [])

    print(f"Issues Jira:  {len(issues)}")
    print(f"Itens locais: {len(local_items)}")
    print()

    # Analisa divergencias
    local_ids = {item.id for item in local_items}

    jira_tracking = {}
    for issue in issues:
        labels = issue.get("fields", {}).get("labels", [])
        for label in labels:
            if label.startswith("tracking_"):
                jira_tracking[label.replace("tracking_", "")] = issue.get("key")

    # Jira issues sem tracking local (orphan)
    orphans = set(jira_tracking.keys()) - local_ids

    # Tracking local sem Jira (pendentes)
    pending = local_ids - set(jira_tracking.keys())

    print("=== PENDENTES (local sem Jira) ===")
    for item_id in pending:
        print(f"  - {item_id}")
    if not pending:
        print("  Nenhum item pendente.")
    print()

    print("=== ORPHANS (Jira sem tracking local) ===")
    for item_id in orphans:
        key = jira_tracking[item_id]
        print(f"  - {item_id} -> {key}")
    if not orphans:
        print("  Nenhum orphan.")
    print()

    return 0


def main():
    """Router de comandos."""
    if len(sys.argv) < 2:
        print("Uso: integrators.jira <comando>")
        print()
        print("Comandos:")
        print("  bootstrap        - Inicializa a camada Jira (equivale ao init)")
        print("  status           - Mostra estado atual")
        print("  discover         - Atualiza metadados do Jira")
        print("  sync [--dry-run] - Sincroniza tracking com Jira")
        print("  reconcile        - Analisa divergencias")
        return 1

    command = sys.argv[1]

    if command == "status":
        return cmd_status()
    elif command == "discover":
        return cmd_discover()
    elif command == "sync":
        dry_run = "--dry-run" in sys.argv
        return cmd_sync(dry_run=dry_run)
    elif command == "reconcile":
        return cmd_reconcile()
    elif command == "bootstrap":
        dry_run = "--dry-run" in sys.argv
        return bootstrap_run(dry_run=dry_run)
    else:
        print(f"[ERRO] Comando desconhecido: {command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
