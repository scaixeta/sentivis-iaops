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
from integrators.common.doc25_parser import parse_sprint_backlog, timestamp_to_date

# Campos de data do Jira para issues
JIRA_START_DATE_FIELD = "customfield_10015"  # Start date
JIRA_DUE_DATE_FIELD = "duedate"  # Data limite


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


def cmd_sync(tracking_file: str = "Dev_Tracking_S2.md", dry_run: bool = False, auto_confirm: bool = False):
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
            if auto_confirm:
                resp = "s"
                print("[AUTO] Confirmacao automatica ativada.")
            else:
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


def cmd_reconcile(tracking_file: str = "Dev_Tracking_S2.md"):
    """Comando reconcile - mostra divergencias."""
    print("=" * 60)
    print(" RECONCILE - Analise de Divergencias")
    print("=" * 60)
    print()
    print(f"Tracking: {tracking_file}")
    print()

    # Carrega estado
    state = load_state()
    if not state:
        print("[ERRO] Estado nao encontrado.")
        return 1

    # Busca tracking local
    tracking_path = Path(tracking_file)
    if not tracking_path.exists():
        print(f"[ERRO] Arquivo nao encontrado: {tracking_file}")
        return 1

    result = parse_sprint_backlog(tracking_path)
    local_items = result.get("items", [])
    tracking_sprint = result.get("sprint", "").lower()
    sprint_label = f"sprint_{tracking_sprint}" if tracking_sprint else ""

    # Busca issues Jira
    try:
        client = JiraClient()
        jira_issues = client.get_project_issues(
            state.project_key,
            max_results=100,
            fields=f"summary,labels,{JIRA_START_DATE_FIELD},{JIRA_DUE_DATE_FIELD}",
        )
        issues = jira_issues.get("issues", [])
    except Exception as e:
        print(f"[ERRO] {e}")
        return 1

    # Escopo de reconcile por sprint do tracking para evitar orphans falsos
    scoped_issues = issues
    if sprint_label:
        scoped_issues = []
        for issue in issues:
            labels = issue.get("fields", {}).get("labels", [])
            if sprint_label in labels:
                scoped_issues.append(issue)

    print(f"Issues Jira (projeto): {len(issues)}")
    if sprint_label:
        print(f"Issues Jira (escopo {sprint_label}): {len(scoped_issues)}")
    else:
        print("Issues Jira (escopo sprint): N/A")
    print(f"Itens locais: {len(local_items)}")
    print()

    # Analisa divergencias
    local_ids = {item.id for item in local_items}

    jira_tracking = {}
    for issue in scoped_issues:
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


def cmd_sprint_status(project_key: str = "STVIA"):
    """Comando sprint status - mostra boards e sprints."""
    print("=" * 60)
    print(" SPRINT STATUS - Boards e Sprints")
    print("=" * 60)
    print()

    try:
        client = JiraClient()

        # Get boards
        boards_resp = client.get_boards(project_key)
        boards = boards_resp.get("values", [])

        if not boards:
            print(f"[ERRO] Nenhum board encontrado para projeto {project_key}")
            return 1

        board = boards[0]
        board_id = board["id"]
        print(f"Board: {board.get('name')} (ID: {board_id}, Type: {board.get('type')})")
        print()

        # Get sprints
        sprints_resp = client.get_sprints(board_id)
        sprints = sprints_resp.get("values", [])

        if not sprints:
            print("Nenhum sprint encontrado.")
            return 0

        print(f"Sprints ({len(sprints)}):")
        for s in sprints:
            sid = s.get("id")
            name = s.get("name")
            state = s.get("state")
            # Get issue count
            try:
                issues_resp = client.get_sprint_issues(sid, max_results=1)
                total = issues_resp.get("total", 0)
            except:
                total = "?"
            print(f"  - {name} (ID: {sid}, State: {state}, Issues: {total})")

        print()
        return 0

    except Exception as e:
        print(f"[ERRO] {e}")
        return 1


def cmd_sprint_assign(
    project_key: str = "STVIA",
    label: str = None,
    sprint_name: str = None,
    dry_run: bool = False,
    auto_confirm: bool = False,
):
    """Comando sprint assign - atribui issues a sprint nativo por label."""
    if not label or not sprint_name:
        print("[ERRO] --label e --sprint-name sao obrigatorios")
        print("Exemplo: python -m integrators.jira sprint assign --label sprint_s0 --sprint-name 'Sprint S0'")
        return 1

    mode = "DRY-RUN" if dry_run else "ASSIGN"
    print("=" * 60)
    print(f" {mode} - Atribuir Issues ao Sprint Nativo")
    print("=" * 60)
    print()
    print(f"Projeto:    {project_key}")
    print(f"Label:      {label}")
    print(f"Sprint:     {sprint_name}")
    print()

    try:
        client = JiraClient()

        # Get board
        boards_resp = client.get_boards(project_key)
        boards = boards_resp.get("values", [])
        if not boards:
            print(f"[ERRO] Nenhum board encontrado")
            return 1

        board = boards[0]
        board_id = board["id"]

        # Find or create sprint
        sprints_resp = client.get_sprints(board_id)
        sprints = sprints_resp.get("values", [])
        sprint = None
        for s in sprints:
            if s.get("name") == sprint_name:
                sprint = s
                break

        if not sprint:
            print(f"[ERRO] Sprint '{sprint_name}' nao encontrado no board")
            print("Crie o sprint primeiro no Jira ou use um nome existente.")
            return 1

        sprint_id = sprint["id"]
        sprint_state = sprint.get("state")
        print(f"Sprint encontrado: {sprint_name} (ID: {sprint_id}, State: {sprint_state})")
        print()

        # Get project issues
        issues_resp = client.get_project_issues(project_key, max_results=100)
        issues = issues_resp.get("issues", [])

        # Filter by label
        target_issues = []
        for issue in issues:
            labels = issue.get("fields", {}).get("labels", []) or []
            if label in labels:
                target_issues.append(issue.get("key"))

        print(f"Issues com label '{label}': {len(target_issues)}")
        if not target_issues:
            print("[INFO] Nenhuma issue encontrada com esta label.")
            return 0

        print()
        if dry_run:
            print(f"[DRY-RUN] {len(target_issues)} issues seriam atribuidas ao sprint {sprint_name}")
            print("Execute sem --dry-run para aplicar.")
        else:
            # Confirm
            print(f"[ATENCAO] {len(target_issues)} issues serao atribuidas ao sprint.")
            if auto_confirm:
                resp = "s"
                print("[AUTO] Confirmacao automatica ativada.")
            else:
                resp = input("Continuar? [s/N]: ").strip().lower()
            if resp != "s":
                print("[INFO] Operacao cancelada.")
                return 0

            # Assign
            result = client.add_issues_to_sprint(sprint_id, target_issues)
            print(f"[OK] {len(target_issues)} issues atribuidas ao sprint {sprint_name}")
            print(f"     Chunks: {result.get('chunks', 1)}")

        return 0

    except Exception as e:
        print(f"[ERRO] {e}")
        return 1


def cmd_sprint_dates(
    project_key: str = "STVIA",
    sprint_name: str = None,
    start_date: str = None,
    end_date: str = None,
    dry_run: bool = False,
    auto_confirm: bool = False,
):
    """Comando sprint dates - define datas de inicio e fim de um sprint."""
    if not sprint_name or not start_date or not end_date:
        print("[ERRO] --sprint-name, --start-date e --end-date sao obrigatorios")
        print("Exemplo: python -m integrators.jira sprint dates --sprint-name 'Sprint S2' --start-date 2026-03-20 --end-date 2026-04-03")
        return 1

    mode = "DRY-RUN" if dry_run else "UPDATE"
    print("=" * 60)
    print(f" {mode} - Definir Datas do Sprint")
    print("=" * 60)
    print()
    print(f"Projeto:    {project_key}")
    print(f"Sprint:     {sprint_name}")
    print(f"Inicio:     {start_date}")
    print(f"Fim:        {end_date}")
    print()

    try:
        client = JiraClient()

        # Get board
        boards_resp = client.get_boards(project_key)
        boards = boards_resp.get("values", [])
        if not boards:
            print(f"[ERRO] Nenhum board encontrado")
            return 1

        board = boards[0]
        board_id = board["id"]

        # Find sprint
        sprints_resp = client.get_sprints(board_id)
        sprints = sprints_resp.get("values", [])
        sprint = None
        for s in sprints:
            if s.get("name") == sprint_name:
                sprint = s
                break

        if not sprint:
            print(f"[ERRO] Sprint '{sprint_name}' nao encontrado no board")
            return 1

        sprint_id = sprint["id"]
        current_state = sprint.get("state")

        # Get current sprint details
        sprint_details = client.get_sprint(sprint_id)
        current_start = sprint_details.get("startDate")
        current_end = sprint_details.get("endDate")

        print(f"Sprint ID:   {sprint_id}")
        print(f"Estado:      {current_state}")
        print()
        print("Datas atuais:")
        print(f"  Inicio:    {current_start or '(nao definido)'}")
        print(f"  Fim:       {current_end or '(nao definido)'}")
        print()

        # Convert dates to ISO8601 UTC
        iso_start = f"{start_date}T00:00:00.000Z"
        iso_end = f"{end_date}T23:59:59.999Z"

        print("Datas propostas:")
        print(f"  Inicio:    {iso_start}")
        print(f"  Fim:       {iso_end}")
        print()

        if dry_run:
            print("[DRY-RUN] Execute sem --dry-run para aplicar.")
            return 0

        # Confirm
        print("[ATENCAO] As datas do sprint serao atualizadas.")
        if auto_confirm:
            resp = "s"
            print("[AUTO] Confirmacao automatica ativada.")
        else:
            resp = input("Continuar? [s/N]: ").strip().lower()
        if resp != "s":
            print("[INFO] Operacao cancelada.")
            return 0

        # Update sprint
        result = client.update_sprint(
            sprint_id=sprint_id,
            name=sprint_name,
            state=current_state,
            start_date=iso_start,
            end_date=iso_end,
        )

        print(f"[OK] Sprint '{sprint_name}' atualizado com sucesso!")
        print(f"     ID:     {result.get('id')}")
        print(f"     Nome:   {result.get('name')}")
        print(f"     Estado: {result.get('state')}")
        print(f"     Inicio: {result.get('startDate')}")
        print(f"     Fim:    {result.get('endDate')}")

        return 0

    except Exception as e:
        print(f"[ERRO] {e}")
        return 1


def cmd_sprint(subcommand: str, argv: list):
    """Roteador de comandos sprint."""
    if subcommand == "status":
        return cmd_sprint_status()
    elif subcommand == "assign":
        # Parse args
        label = None
        sprint_name = None
        dry_run = "--dry-run" in argv
        auto_confirm = "--yes" in argv or "-y" in argv
        for i, arg in enumerate(argv):
            if arg == "--label" and i + 1 < len(argv):
                label = argv[i + 1]
            if arg == "--sprint-name" and i + 1 < len(argv):
                sprint_name = argv[i + 1]
        return cmd_sprint_assign(label=label, sprint_name=sprint_name, dry_run=dry_run, auto_confirm=auto_confirm)
    elif subcommand == "dates":
        # Parse args
        sprint_name = None
        start_date = None
        end_date = None
        dry_run = "--dry-run" in argv
        auto_confirm = "--yes" in argv or "-y" in argv
        for i, arg in enumerate(argv):
            if arg == "--sprint-name" and i + 1 < len(argv):
                sprint_name = argv[i + 1]
            if arg == "--start-date" and i + 1 < len(argv):
                start_date = argv[i + 1]
            if arg == "--end-date" and i + 1 < len(argv):
                end_date = argv[i + 1]
        return cmd_sprint_dates(sprint_name=sprint_name, start_date=start_date, end_date=end_date, dry_run=dry_run, auto_confirm=auto_confirm)
    else:
        print(f"[ERRO] Subcomando desconhecido: {subcommand}")
        print()
        print("Comandos sprint:")
        print("  sprint status                     - Lista boards e sprints")
        print("  sprint assign --label X --sprint-name Y - Atribui issues por label")
        print("  sprint dates --sprint-name X --start-date YYYY-MM-DD --end-date YYYY-MM-DD - Define datas do sprint")
        return 1


def cmd_issue_dates(tracking_file: str = "Dev_Tracking_S2.md", dry_run: bool = False, auto_confirm: bool = False):
    """Comando issue dates - sincroniza datas das issues com timestamps do tracking."""
    mode = "DRY-RUN" if dry_run else "SYNC"
    print("=" * 60)
    print(f" {mode} - Sincronizar Datas de Issues")
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
        print(f"[ERRO] Arquivo nao encontrado: {tracking_path}")
        return 1

    # Parse tracking
    result = parse_sprint_backlog(tracking_file)
    timestamps = result.get("timestamps", [])
    sprint = result.get("sprint", "")

    if not timestamps:
        print("[ERRO] Nenhum timestamp encontrado no tracking.")
        return 1

    print(f"Sprint:    {sprint}")
    print(f"Timestamps: {len(timestamps)}")
    print()

    # Busca issues Jira
    try:
        client = JiraClient()
        jira_issues = client.get_project_issues(
            state.project_key,
            max_results=100,
            fields=f"summary,labels,{JIRA_START_DATE_FIELD},{JIRA_DUE_DATE_FIELD}",
        )
        issues = jira_issues.get("issues", [])
    except Exception as e:
        print(f"[ERRO] {e}")
        return 1

    # Mapeia issues por label tracking_
    jira_by_tracking = {}
    for issue in issues:
        labels = issue.get("fields", {}).get("labels", []) or []
        for label in labels:
            if label.startswith("tracking_"):
                tracking_id = label.replace("tracking_", "")
                jira_by_tracking[tracking_id] = issue

    print(f"Issues Jira: {len(issues)}")
    print(f"Mapeadas por tracking_: {len(jira_by_tracking)}")
    print()

    # Planeja atualizacoes
    updates = []
    warnings = []
    for ts in timestamps:
        # So processa se tem finish (item concluido)
        if not ts.finish:
            continue

        if ts.item_id not in jira_by_tracking:
            warnings.append(f"  - {ts.item_id}: issue nao encontrada no Jira")
            continue

        issue = jira_by_tracking[ts.item_id]
        issue_key = issue.get("key")
        fields = issue.get("fields", {})

        # Converte timestamps para datas
        start_date = timestamp_to_date(ts.start)
        due_date = timestamp_to_date(ts.finish)

        # Verifica se ha mudanca
        current_start = fields.get(JIRA_START_DATE_FIELD)
        current_due = fields.get(JIRA_DUE_DATE_FIELD)

        # Formata datas atuais
        current_start_str = current_start[:10] if current_start else None
        current_due_str = current_due[:10] if current_due else None

        # Verifica se ha mudanca
        if start_date == current_start_str and due_date == current_due_str:
            continue  # Ja atualizado

        updates.append({
            "issue_key": issue_key,
            "item_id": ts.item_id,
            "start_date": start_date,
            "due_date": due_date,
            "current_start": current_start_str,
            "current_due": current_due_str,
        })

    if warnings:
        print("=== WARNINGS (itens sem issue no Jira) ===")
        for w in warnings:
            print(w)
        print()

    if not updates:
        print("[INFO] Nenhuma atualizacao necessaria.")
        return 0

    print("=== ATUALIZACOES PLANEJADAS ===")
    for u in updates:
        print(f"  {u['issue_key']} ({u['item_id']}):")
        print(f"    Start: {u['current_start'] or '(vazio)'} -> {u['start_date']}")
        print(f"    Due:   {u['current_due'] or '(vazio)'} -> {u['due_date']}")
    print()

    print(f"Total: {len(updates)} issues para atualizar")
    print()

    if dry_run:
        print("[DRY-RUN] Execute sem --dry-run para aplicar.")
        return 0

    # Confirm
    print("[ATENCAO] As datas das issues serao atualizadas.")
    if auto_confirm:
        resp = "s"
        print("[AUTO] Confirmacao automatica ativada.")
    else:
        resp = input("Continuar? [s/N]: ").strip().lower()
    if resp != "s":
        print("[INFO] Operacao cancelada.")
        return 0

    # Executa atualizacoes
    success = 0
    failed = 0
    for u in updates:
        try:
            # Monta payload
            payload = {}
            if u["start_date"]:
                payload[JIRA_START_DATE_FIELD] = u["start_date"]
            if u["due_date"]:
                payload[JIRA_DUE_DATE_FIELD] = u["due_date"]

            if payload:
                client.update_issue(u["issue_key"], payload)
                print(f"  [OK] {u['issue_key']}: atualizada")
                success += 1
            else:
                print(f"  [--] {u['issue_key']}: sem mudanca")
        except Exception as e:
            print(f"  [ERRO] {u['issue_key']}: {e}")
            failed += 1

    print()
    print(f"[OK] Concluido: {success} sucesso, {failed} falhas")
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
        print("  sprint status    - Lista boards e sprints")
        print("  sprint assign    - Atribui issues a sprint nativo")
        print("  issue dates      - Sincroniza datas de issues com timestamps")
        return 1

    command = sys.argv[1]

    # Sprint subcommand handler
    if command == "sprint":
        if len(sys.argv) < 3:
            print("[ERRO] Faltando subcomando")
            print("Use: sprint status ou sprint assign ...")
            return 1
        subcommand = sys.argv[2]
        return cmd_sprint(subcommand, sys.argv[3:])

    if command == "status":
        return cmd_status()
    elif command == "discover":
        return cmd_discover()
    elif command == "sync":
        dry_run = "--dry-run" in sys.argv
        # Parse --tracking-file argument
        tracking_file = "Dev_Tracking_S2.md"  # default - S2 is the active sprint
        auto_confirm = "--yes" in sys.argv or "-y" in sys.argv
        for i, arg in enumerate(sys.argv):
            if arg == "--tracking-file" and i + 1 < len(sys.argv):
                tracking_file = sys.argv[i + 1]
        return cmd_sync(tracking_file=tracking_file, dry_run=dry_run, auto_confirm=auto_confirm)
    elif command == "reconcile":
        tracking_file = "Dev_Tracking_S2.md"
        for i, arg in enumerate(sys.argv):
            if arg == "--tracking-file" and i + 1 < len(sys.argv):
                tracking_file = sys.argv[i + 1]
        return cmd_reconcile(tracking_file=tracking_file)
    elif command == "bootstrap":
        dry_run = "--dry-run" in sys.argv
        return bootstrap_run(dry_run=dry_run)
    elif command == "issue":
        if len(sys.argv) < 3 or sys.argv[2] != "dates":
            print("[ERRO] Use: issue dates")
            return 1
        # Parse args for issue dates
        tracking_file = "Dev_Tracking_S2.md"
        dry_run = "--dry-run" in sys.argv
        auto_confirm = "--yes" in sys.argv or "-y" in sys.argv
        for i, arg in enumerate(sys.argv):
            if arg == "--tracking-file" and i + 1 < len(sys.argv):
                tracking_file = sys.argv[i + 1]
        return cmd_issue_dates(tracking_file=tracking_file, dry_run=dry_run, auto_confirm=auto_confirm)
    elif command == "issue dates":
        tracking_file = "Dev_Tracking_S2.md"
        dry_run = "--dry-run" in sys.argv
        auto_confirm = "--yes" in sys.argv or "-y" in sys.argv
        for i, arg in enumerate(sys.argv):
            if arg == "--tracking-file" and i + 1 < len(sys.argv):
                tracking_file = sys.argv[i + 1]
        return cmd_issue_dates(tracking_file=tracking_file, dry_run=dry_run, auto_confirm=auto_confirm)
    else:
        print(f"[ERRO] Comando desconhecido: {command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
