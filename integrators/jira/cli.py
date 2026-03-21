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
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Adiciona raiz ao path para imports relativos
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from integrators.jira.client import JiraClient
from integrators.jira.state import JiraState, load_state, save_state
from integrators.jira.sync_engine import SyncEngine
from integrators.jira.board_reader import derive_local_status_guidance
from integrators.jira.bootstrap import run as bootstrap_run
from integrators.common.doc25_parser import parse_sprint_backlog, parse_bug_log_for_sprint, timestamp_to_date
from integrators.common.tracking_writer import write_back_jira_keys

# Campos de data do Jira para issues
JIRA_START_DATE_FIELD = "customfield_10015"  # Start date
JIRA_DUE_DATE_FIELD = "duedate"  # Data limite


def _arg_value(argv: list[str], flag: str, default=None):
    """Retorna o valor de uma flag em argv ou o default."""
    for i, arg in enumerate(argv):
        if arg == flag and i + 1 < len(argv):
            return argv[i + 1]
    return default


def _has_flag(argv: list[str], *flags: str) -> bool:
    """Verifica se alguma das flags foi informada."""
    return any(flag in argv for flag in flags)


def _load_tracking_scope_items(tracking_file: str):
    """Carrega itens do tracking e bugs da sprint corrente."""
    result = parse_sprint_backlog(tracking_file)
    items = list(result.get("items", []))
    sprint = result.get("sprint", "")
    if sprint:
        items.extend(parse_bug_log_for_sprint("tests/bugs_log.md", sprint))
    return result, items


def _default_sprint_end_date(start_date: str | None) -> str | None:
    """Retorna a data final padrao da sprint: inicio + 3 dias."""
    if not start_date:
        return None
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
    except ValueError:
        return None
    return (start + timedelta(days=3)).isoformat()


def _iso_to_date_string(value: str | None) -> str | None:
    """Extrai YYYY-MM-DD de uma data ISO8601 do Jira."""
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return value[:10] if len(value) >= 10 else None


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


def cmd_sync(tracking_file: str = "Dev_Tracking_S2.md", dry_run: bool = False, auto_confirm: bool = False, write_back: bool = False):
    """Comando sync - sincroniza tracking com Jira."""
    mode = "DRY-RUN" if dry_run else "SYNC"
    print("=" * 60)
    print(f" {mode} - Sincronizacao DOC2.5 -> Jira")
    print("=" * 60)
    print()
    print(f"Tracking: {tracking_file}")
    if write_back:
        print("[WRITE-BACK] Habilitado")
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
            # Mesmo sem operacoes, pode fazer write-back se houver mapping
            pass

        # Prepara mapping para write-back
        item_to_jira = {}
        for item in result.get("items", []):
            # Se item.jira existe, usa ele
            if item.jira:
                item_to_jira[item.tracking_key] = item.jira
        
        # Adiciona keys resolvidos do plano
        for op in plan:
            if op.issue_key:
                # Extrai ID do item a partir do payload ou usa label
                labels = op.labels or []
                for label in labels:
                    if label.startswith("tracking_"):
                        item_id = label.replace("tracking_", "")
                        item_to_jira[item_id] = op.issue_key

        # Se write-back habilitado, mostra plano
        if write_back and item_to_jira:
            print("\n=== WRITE-BACK PLANEJADO ===")
            wb_result = write_back_jira_keys(tracking_file, item_to_jira, dry_run=True)
            print()

        # Se tem operacoes, processa
        if plan:
            print()

            if dry_run:
                print(f"[DRY-RUN] {len(plan)} operacoes pendentes.")
                if write_back:
                    print("[WRITE-BACK] Execute com --yes para aplicar.")
                else:
                    print("Execute sem --dry-run para aplicar.")
            else:
                # Confirma antes de mutation Jira
                print(f"[ATENCAO] {len(plan)} operacoes Jira serao executadas.")
                if auto_confirm:
                    resp_jira = "s"
                    print("[AUTO] Confirmacao automatica ativada.")
                else:
                    resp_jira = input("Continuar? [s/N]: ").strip().lower()
                
                if resp_jira != "s":
                    print("[INFO] Operacao cancelada.")
                    return 0

                # Executa sync
                results = engine.sync(plan, dry_run=False)

                # Resume Jira
                success = sum(1 for r in results if r.success)
                failed = sum(1 for r in results if not r.success)
                print()
                print(f"[OK] Sincronizacao Jira concluida: {success} sucesso, {failed} falhas")

                # Atualiza mapping com chaves criadas
                for r in results:
                    if r.success and r.issue_key:
                        # Tenta encontrar o item_id
                        for item in result.get("items", []):
                            # Se o item nao tinha jira, agora tem
                            if not item.jira:
                                # Procura na lista de operacoes
                                pass

        # Processa write-back se habilitado
        if write_back and item_to_jira:
            print("\n=== WRITE-BACK ===")
            if dry_run:
                print("[DRY-RUN] Nenhuma escrita foi feita.")
            else:
                # Confirma write-back
                if auto_confirm:
                    resp_wb = "s"
                else:
                    resp_wb = input("Escrever chaves Jira no Dev_Tracking? [s/N]: ").strip().lower()
                
                if resp_wb != "s":
                    print("[INFO] Write-back cancelado.")
                    return 0
                
                wb_result = write_back_jira_keys(tracking_file, item_to_jira, dry_run=False)
                print(f"[OK] Write-back concluido: {wb_result.get('updated', 0)} linhas atualizadas")

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

    result, local_items = _load_tracking_scope_items(str(tracking_path))

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

    # Escopo de reconcile pelo SoT local:
    # considera apenas issues cujos labels tracking_<ID> existam no conjunto local.
    local_ids = {item.tracking_key for item in local_items}
    scoped_issues = []
    for issue in issues:
        labels = issue.get("fields", {}).get("labels", []) or []
        tracking_labels = {
            label.replace("tracking_", "")
            for label in labels
            if label.startswith("tracking_")
        }
        if tracking_labels & local_ids:
            scoped_issues.append(issue)

    print(f"Issues Jira (projeto): {len(issues)}")
    print(f"Issues Jira (escopo source of truth local): {len(scoped_issues)}")
    print(f"Itens locais: {len(local_items)}")
    print()

    # Analisa divergencias
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
    tracking_file: str | None = None,
    sprint_name: str = None,
    sprint_id: int | None = None,
    dry_run: bool = False,
    auto_confirm: bool = False,
):
    """Comando sprint assign - atribui issues a sprint nativo e herda due date da sprint."""
    using_label = label is not None
    using_tracking = tracking_file is not None

    if (not using_label and not using_tracking) or (sprint_name is None and sprint_id is None):
        print("[ERRO] informe --label ou --tracking-file, e um identificador de sprint")
        print("Exemplos:")
        print("  python -m integrators.jira sprint assign --label sprint_s0 --sprint-name 'Sprint S0'")
        print("  python -m integrators.jira sprint assign --tracking-file Dev_Tracking_S2.md --sprint-name 'Sprint S2'")
        return 1

    mode = "DRY-RUN" if dry_run else "ASSIGN"
    print("=" * 60)
    print(f" {mode} - Atribuir Issues ao Sprint Nativo")
    print("=" * 60)
    print()
    print(f"Projeto:    {project_key}")
    if using_label:
        print(f"Label:      {label}")
    if using_tracking:
        print(f"Tracking:   {tracking_file}")
    if sprint_id is not None:
        print(f"Sprint ID:  {sprint_id}")
    elif sprint_name:
        print(f"Sprint:     {sprint_name}")
    print()

    try:
        client = JiraClient()

        boards_resp = client.get_boards(project_key)
        boards = boards_resp.get("values", [])
        if not boards:
            print("[ERRO] Nenhum board encontrado")
            return 1

        board = boards[0]
        board_id = board["id"]

        sprint, _sprints = _resolve_sprint_target(
            client=client,
            board_id=board_id,
            sprint_id=sprint_id,
            sprint_name=sprint_name,
        )

        if not sprint:
            if sprint_id is not None:
                print(f"[ERRO] Sprint ID {sprint_id} nao encontrado no board")
            else:
                print(f"[ERRO] Sprint '{sprint_name}' nao encontrado no board")
            print("Use um sprint existente por nome ou ID.")
            return 1

        sprint_id = sprint["id"]
        sprint_name = sprint.get("name")
        sprint_state = sprint.get("state")
        sprint_details = client.get_sprint(int(sprint_id))
        sprint_end_date = _iso_to_date_string(sprint_details.get("endDate"))
        print(f"Sprint encontrado: {sprint_name} (ID: {sprint_id}, State: {sprint_state})")
        if sprint_end_date:
            print(f"Due date padrao das issues: {sprint_end_date} (herdada da sprint)")
        else:
            print("Due date padrao das issues: (sprint sem endDate definido)")
        print()

        issues_resp = client.get_project_issues(project_key, max_results=100)
        issues = issues_resp.get("issues", [])

        target_issues = []
        if using_tracking:
            _result, tracking_items = _load_tracking_scope_items(tracking_file)
            target_ids = {item.tracking_key for item in tracking_items if item.type in {"ST", "BUG", "CR"}}
            for issue in issues:
                issue_key = issue.get("key")
                labels = issue.get("fields", {}).get("labels", []) or []
                tracking_ids = {
                    entry.replace("tracking_", "")
                    for entry in labels
                    if entry.startswith("tracking_")
                }
                if tracking_ids & target_ids:
                    target_issues.append(issue_key)
            print(f"Issues resolvidas pelo tracking local: {len(target_issues)}")
        else:
            for issue in issues:
                labels = issue.get("fields", {}).get("labels", []) or []
                if label in labels:
                    target_issues.append(issue.get("key"))
            print(f"Issues com label '{label}': {len(target_issues)}")

        if not target_issues:
            print("[INFO] Nenhuma issue encontrada com os criterios informados.")
            return 0

        print()
        if dry_run:
            print(f"[DRY-RUN] {len(target_issues)} issues seriam atribuidas ao sprint {sprint_name}")
            if sprint_end_date:
                print(f"[DRY-RUN] As due dates das issues seriam alinhadas para {sprint_end_date}")
            print("Execute sem --dry-run para aplicar.")
        else:
            print(f"[ATENCAO] {len(target_issues)} issues serao atribuidas ao sprint.")
            if auto_confirm:
                resp = "s"
                print("[AUTO] Confirmacao automatica ativada.")
            else:
                resp = input("Continuar? [s/N]: ").strip().lower()
            if resp != "s":
                print("[INFO] Operacao cancelada.")
                return 0

            result = client.add_issues_to_sprint(sprint_id, target_issues)
            print(f"[OK] {len(target_issues)} issues atribuidas ao sprint {sprint_name}")
            print(f"     Chunks: {result.get('chunks', 1)}")
            if sprint_end_date:
                updated_due_dates = 0
                for issue_key in target_issues:
                    client.update_issue(issue_key, {JIRA_DUE_DATE_FIELD: sprint_end_date})
                    updated_due_dates += 1
                print(f"[OK] Due date alinhada para {updated_due_dates} issues: {sprint_end_date}")
            else:
                print("[WARN] Sprint sem endDate definido; due date das issues nao foi ajustada.")

        return 0

    except Exception as e:
        print(f"[ERRO] {e}")
        return 1

    except Exception as e:
        print(f"[ERRO] {e}")
        return 1



def cmd_sprint_dates(
    project_key: str = "STVIA",
    sprint_name: str = None,
    sprint_id: int | None = None,
    start_date: str = None,
    end_date: str = None,
    dry_run: bool = False,
    auto_confirm: bool = False,
):
    """Comando sprint dates - define datas de inicio e fim de um sprint."""
    if (sprint_name is None and sprint_id is None) or not start_date:
        print("[ERRO] identificador da sprint e --start-date sao obrigatorios")
        print("Exemplo: python -m integrators.jira sprint dates --sprint-name 'Sprint S2' --start-date 2026-03-20 --end-date 2026-03-23")
        print("Exemplo: python -m integrators.jira sprint dates --sprint-id 35 --start-date 2026-03-20")
        return 1

    inferred_end_date = None
    if not end_date:
        inferred_end_date = _default_sprint_end_date(start_date)
        end_date = inferred_end_date
        if not end_date:
            print("[ERRO] nao foi possivel inferir a data final padrao da sprint")
            return 1

    mode = "DRY-RUN" if dry_run else "UPDATE"
    print("=" * 60)
    print(f" {mode} - Definir Datas do Sprint")
    print("=" * 60)
    print()
    print(f"Projeto:    {project_key}")
    if sprint_id is not None:
        print(f"Sprint ID:  {sprint_id}")
    elif sprint_name:
        print(f"Sprint:     {sprint_name}")
    print(f"Inicio:     {start_date}")
    print(f"Fim:        {end_date}")
    if inferred_end_date:
        print("[PADRAO]   end-date inferido automaticamente (+3 dias)")
    print()

    try:
        client = JiraClient()

        boards_resp = client.get_boards(project_key)
        boards = boards_resp.get("values", [])
        if not boards:
            print(f"[ERRO] Nenhum board encontrado")
            return 1

        board = boards[0]
        board_id = board["id"]

        sprint, _sprints = _resolve_sprint_target(
            client=client,
            board_id=board_id,
            sprint_id=sprint_id,
            sprint_name=sprint_name,
        )

        if not sprint:
            if sprint_id is not None:
                print(f"[ERRO] Sprint ID {sprint_id} nao encontrado no board")
            else:
                print(f"[ERRO] Sprint '{sprint_name}' nao encontrado no board")
            return 1

        sprint_id = sprint["id"]
        sprint_name = sprint.get("name")
        current_state = sprint.get("state")

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

        iso_start = f"{start_date}T00:00:00.000Z"
        iso_end = f"{end_date}T23:59:59.999Z"

        print("Datas propostas:")
        print(f"  Inicio:    {iso_start}")
        print(f"  Fim:       {iso_end}")
        print()

        if dry_run:
            print("[DRY-RUN] Execute sem --dry-run para aplicar.")
            return 0

        print("[ATENCAO] As datas do sprint serao atualizadas.")
        if auto_confirm:
            resp = "s"
            print("[AUTO] Confirmacao automatica ativada.")
        else:
            resp = input("Continuar? [s/N]: ").strip().lower()
        if resp != "s":
            print("[INFO] Operacao cancelada.")
            return 0

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


def cmd_sprint_create(
    project_key: str = "STVIA",
    sprint_name: str = None,
    goal: str = None,
    start_date: str = None,
    end_date: str = None,
    dry_run: bool = False,
    auto_confirm: bool = False,
):
    """Comando sprint create - cria uma nova sprint no board."""
    if not sprint_name:
        print("[ERRO] --sprint-name e obrigatorio")
        print("Exemplo: python -m integrators.jira sprint create --sprint-name 'Sprint S2' --start-date 2026-03-20")
        return 1

    inferred_end_date = None
    if start_date and not end_date:
        inferred_end_date = _default_sprint_end_date(start_date)
        end_date = inferred_end_date

    mode = "DRY-RUN" if dry_run else "CREATE"
    print("=" * 60)
    print(f" {mode} - Criar Nova Sprint")
    print("=" * 60)
    print()
    print(f"Projeto:    {project_key}")
    print(f"Sprint:     {sprint_name}")
    if goal:
        print(f"Objetivo:   {goal}")
    if start_date:
        print(f"Inicio:     {start_date}")
    if end_date:
        print(f"Fim:        {end_date}")
    if inferred_end_date:
        print("[PADRAO]   end-date inferido automaticamente (+3 dias)")
    print()

    try:
        client = JiraClient()

        boards_resp = client.get_boards(project_key)
        boards = boards_resp.get("values", [])
        if not boards:
            print(f"[ERRO] Nenhum board encontrado")
            return 1

        board = boards[0]
        board_id = board["id"]
        board_name = board.get("name", "")
        print(f"Board:      {board_name} (ID: {board_id})")
        print()

        # Verifica se ja existe sprint com este nome
        sprints_resp = client.get_sprints(board_id)
        sprints = sprints_resp.get("values", []) or []
        
        for s in sprints:
            if s.get("name") == sprint_name:
                print(f"[ERRO] Ja existe uma sprint com o nome '{sprint_name}' no board.")
                print(f"        ID: {s.get('id')}, Estado: {s.get('state')}")
                return 1

        # Converte datas para ISO8601
        iso_start = None
        iso_end = None
        if start_date:
            iso_start = f"{start_date}T00:00:00.000Z"
        if end_date:
            iso_end = f"{end_date}T23:59:59.999Z"

        print("=== PLANO ===")
        print(f"- Criar sprint '{sprint_name}' no board {board_name}")
        if goal:
            print(f"- Objetivo: {goal}")
        if iso_start:
            print(f"- Start Date: {iso_start}")
        if iso_end:
            print(f"- End Date: {iso_end}")
        print()

        if dry_run:
            print("[DRY-RUN] Execute sem --dry-run para criar a sprint.")
            return 0

        print("[ATENCAO] A sprint sera criada no Jira.")
        if auto_confirm:
            resp = "s"
            print("[AUTO] Confirmacao automatica ativada.")
        else:
            resp = input("Continuar? [s/N]: ").strip().lower()
        if resp != "s":
            print("[INFO] Operacao cancelada.")
            return 0

        result = client.create_sprint(
            name=sprint_name,
            origin_board_id=board_id,
            goal=goal or "",
            start_date=iso_start,
            end_date=iso_end,
        )

        print(f"[OK] Sprint '{result.get('name')}' criada com sucesso!")
        print(f"     ID:     {result.get('id')}")
        print(f"     Nome:   {result.get('name')}")
        print(f"     Estado: {result.get('state')}")
        print(f"     Board:  {result.get('originBoardId')}")
        if result.get('startDate'):
            print(f"     Inicio: {result.get('startDate')}")
        if result.get('endDate'):
            print(f"     Fim:    {result.get('endDate')}")
        
        return 0

    except Exception as e:
        print(f"[ERRO] {e}")
        return 1


def _parse_iso_date(date_str: str):
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00")).date()
    except ValueError:
        return None



def _resolve_sprint_target(
    client: JiraClient,
    board_id: int,
    sprint_id: int | None = None,
    sprint_name: str | None = None,
    active_only: bool = False,
):
    """Resolve sprint por ID, nome ou sprint ativa."""
    sprints_resp = client.get_sprints(board_id)
    sprints = sprints_resp.get("values", []) or []

    if sprint_id is not None:
        for sprint in sprints:
            if int(sprint.get("id", 0)) == sprint_id:
                return sprint, sprints
        return None, sprints

    if sprint_name:
        for sprint in sprints:
            if sprint.get("name") == sprint_name:
                return sprint, sprints
        return None, sprints

    if active_only:
        active = [s for s in sprints if s.get("state") == "active"]
        if active:
            return active[0], sprints

    return None, sprints



def cmd_sprint_open(
    project_key: str = "STVIA",
    sprint_id: int | None = None,
    sprint_name: str | None = None,
    dry_run: bool = False,
    auto_confirm: bool = False,
):
    """Comando sprint open - abre sprint com base no Start Date (UTC)."""
    mode = "DRY-RUN" if dry_run else "OPEN"
    print("=" * 60)
    print(f" {mode} - Abrir Sprint (condicao: Start Date)")
    print("=" * 60)
    print()
    print(f"Projeto:    {project_key}")
    if sprint_id is not None:
        print(f"Sprint ID:  {sprint_id}")
    elif sprint_name:
        print(f"Sprint:     {sprint_name}")
    print()

    try:
        client = JiraClient()

        boards_resp = client.get_boards(project_key)
        boards = boards_resp.get("values", [])
        if not boards:
            print(f"[ERRO] Nenhum board encontrado")
            return 1

        board = boards[0]
        board_id = board["id"]
        print(f"Board:      {board.get('name')} (ID: {board_id})")
        print()

        _target, sprints = _resolve_sprint_target(
            client=client,
            board_id=board_id,
            sprint_id=sprint_id,
            sprint_name=sprint_name,
        )
        if not sprints:
            print("[INFO] Nenhum sprint encontrado.")
            return 0

        active = [s for s in sprints if s.get("state") == "active"]
        if active:
            active_names = ", ".join([s.get("name") for s in active if s.get("name")]) or "(desconhecido)"
            print("[INFO] Ja existe sprint ativa. Nenhuma abertura executada.")
            print(f"Ativa(s): {active_names}")
            return 0

        if sprint_id is not None or sprint_name:
            selected_sprint, _ = _resolve_sprint_target(
                client=client,
                board_id=board_id,
                sprint_id=sprint_id,
                sprint_name=sprint_name,
            )
            if not selected_sprint:
                target_label = f"ID {sprint_id}" if sprint_id is not None else f"'{sprint_name}'"
                print(f"[ERRO] Sprint {target_label} nao encontrada no board.")
                return 1
            if selected_sprint.get("state") != "future":
                print("[ERRO] Apenas sprints futuras podem ser abertas explicitamente.")
                return 1
            selected = client.get_sprint(int(selected_sprint.get("id")))
        else:
            today_utc = datetime.now(timezone.utc).date()
            candidates = []
            for s in sprints:
                if s.get("state") != "future":
                    continue
                candidate_id = s.get("id")
                details = client.get_sprint(candidate_id)
                start = details.get("startDate")
                start_date = _parse_iso_date(start)
                if start_date is None:
                    continue
                if start_date == today_utc:
                    candidates.append((start_date, details))

            if not candidates:
                print("[INFO] Nenhuma sprint futura com Start Date igual ao dia de hoje (UTC).")
                print(f"Hoje (UTC): {today_utc.isoformat()}")
                return 0

            candidates.sort(key=lambda x: x[0])
            selected = candidates[0][1]

        sprint_id = selected.get("id")
        sprint_name = selected.get("name")
        start_date = selected.get("startDate")
        end_date = selected.get("endDate")
        goal = selected.get("goal")

        print("Sprint candidata:")
        print(f"  ID:       {sprint_id}")
        print(f"  Nome:     {sprint_name}")
        print(f"  Estado:   {selected.get('state')}")
        print(f"  Inicio:   {start_date}")
        print(f"  Fim:      {end_date}")
        print(f"  Objetivo: {goal or '(nao definido)'}")
        print()

        if dry_run:
            print("[DRY-RUN] Execute sem --dry-run para abrir a sprint.")
            return 0

        print("[ATENCAO] A sprint sera aberta (state=active).")
        if auto_confirm:
            resp = "s"
            print("[AUTO] Confirmacao automatica ativada.")
        else:
            resp = input("Continuar? [s/N]: ").strip().lower()
        if resp != "s":
            print("[INFO] Operacao cancelada.")
            return 0

        result = client.update_sprint(
            sprint_id=sprint_id,
            name=sprint_name,
            start_date=start_date,
            end_date=end_date,
            state="active",
            goal=goal,
        )

        print(f"[OK] Sprint '{result.get('name')}' aberta com sucesso!")
        print(f"     ID:     {result.get('id')}")
        print(f"     Estado: {result.get('state')}")
        print(f"     Inicio: {result.get('startDate')}")
        print(f"     Fim:    {result.get('endDate')}")
        return 0

    except Exception as e:
        print(f"[ERRO] {e}")
        return 1



def cmd_sprint_close(
    project_key: str = "STVIA",
    sprint_name: str | None = None,
    sprint_id: int | None = None,
    dry_run: bool = False,
    auto_confirm: bool = False,
):
    """Comando sprint close - fecha sprint ativa apenas quando estiver limpa.

    Quando houver itens fora da ultima coluna do board, o comando nao tenta
    fechar a sprint. Em vez disso, ele transforma a analise em um gate
    explicito para o PO/Cindy decidir o destino dos incompletos.
    """
    mode = "DRY-RUN" if dry_run else "CLOSE"
    print("=" * 60)
    print(f" {mode} - Encerrar Sprint")
    print("=" * 60)
    print()
    print(f"Projeto:    {project_key}")
    if sprint_id is not None:
        print(f"Sprint ID:  {sprint_id}")
    elif sprint_name:
        print(f"Sprint:     {sprint_name}")
    else:
        print("Sprint:     (ativa)")
    print()

    try:
        state = load_state()
        client = JiraClient()

        boards_resp = client.get_boards(project_key)
        boards = boards_resp.get("values", [])
        if not boards:
            print("[ERRO] Nenhum board encontrado.")
            return 1

        board = boards[0]
        board_id = int(board["id"])
        board_name = board.get("name", "")
        print(f"Board:      {board_name} (ID: {board_id})")

        cfg = client.get_board_configuration(board_id)
        columns = cfg.get("columnConfig", {}).get("columns", []) or []
        if not columns:
            print("[ERRO] Nenhuma coluna encontrada no board.")
            return 1

        last_column = columns[-1]
        done_status_ids = {
            str(s.get("id"))
            for s in (last_column.get("statuses", []) or [])
            if s.get("id") is not None
        }
        done_column_name = last_column.get("name", "(ultima coluna)")
        print(f"Ultima coluna: {done_column_name}")
        print()

        target_sprint, sprints = _resolve_sprint_target(
            client=client,
            board_id=board_id,
            sprint_id=sprint_id,
            sprint_name=sprint_name,
            active_only=(sprint_id is None and sprint_name is None),
        )

        if not target_sprint:
            print("[ERRO] Sprint alvo nao encontrada.")
            return 1

        sprint_id = int(target_sprint["id"])
        sprint_details = client.get_sprint(sprint_id)
        sprint_name_resolved = sprint_details.get("name", target_sprint.get("name", ""))
        sprint_state = sprint_details.get("state", target_sprint.get("state", ""))
        sprint_goal = sprint_details.get("goal")

        print("Sprint alvo:")
        print(f"  ID:       {sprint_id}")
        print(f"  Nome:     {sprint_name_resolved}")
        print(f"  Estado:   {sprint_state}")
        print(f"  Inicio:   {sprint_details.get('startDate')}")
        print(f"  Fim:      {sprint_details.get('endDate')}")
        print()

        if sprint_state == "closed":
            print("[INFO] A sprint ja esta encerrada.")
            return 0
        if sprint_state != "active":
            print("[ERRO] Apenas sprints ativas podem ser encerradas.")
            return 1

        issues_resp = client.get_sprint_issues(
            sprint_id,
            max_results=100,
            fields="summary,status,subtasks",
        )
        issues = issues_resp.get("issues", []) or []
        print(f"Issues na sprint: {len(issues)}")
        print()

        completed = []
        incomplete = []
        open_subtasks = []

        for issue in issues:
            key = issue.get("key")
            fields = issue.get("fields", {}) or {}
            summary = fields.get("summary", "")
            status = fields.get("status", {}) or {}
            status_name = status.get("name", "")
            status_id = str(status.get("id", ""))

            if status_id in done_status_ids:
                completed.append((key, status_name, summary))
            else:
                incomplete.append((key, status_name, summary))

            for subtask in fields.get("subtasks", []) or []:
                sub_status = subtask.get("fields", {}).get("status", {}) or {}
                sub_status_id = str(sub_status.get("id", ""))
                if sub_status_id not in done_status_ids:
                    open_subtasks.append((
                        subtask.get("key"),
                        sub_status.get("name", ""),
                        subtask.get("fields", {}).get("summary", ""),
                        key,
                    ))

        print("=== CONCLUIDAS NA ULTIMA COLUNA ===")
        if completed:
            for key, status_name, _summary in completed:
                print(f"  {key}: {status_name}")
        else:
            print("  Nenhuma")
        print()

        print("=== INCOMPLETAS NO FECHAMENTO ===")
        if incomplete:
            for key, status_name, _summary in incomplete:
                print(f"  {key}: {status_name}")
        else:
            print("  Nenhuma")
        print()

        print("=== SUBTASKS ABERTAS ===")
        if open_subtasks:
            for key, status_name, _summary, parent_key in open_subtasks:
                print(f"  {key} (parent {parent_key}): {status_name}")
        else:
            print("  Nenhuma")
        print()

        if incomplete or open_subtasks:
            future_sprints = [
                sprint
                for sprint in sprints
                if sprint.get("state") == "future" and int(sprint.get("id", 0)) != sprint_id
            ]

            print("[GATE] JIRA SPRINT CLOSE GATE: ha decisoes pendentes de fechamento; consulta explicita ao PO obrigatoria antes de concluir a sprint.")
            print(f"[GATE] Ultima coluna considerada como concluida: {done_column_name}")
            print("[GATE] O comando nao encerrara a sprint enquanto existirem itens incompletos ou subtasks abertas.")
            print()
            print("=== DECISAO DO PO OBRIGATORIA ===")
            print(f"A sprint '{sprint_name_resolved}' tem pendencias que o Jira trataria como incompletas no fechamento.")
            print("Antes de qualquer tentativa real de encerramento, a Cindy deve perguntar ao PO o que fazer.")
            print()
            print("Perguntas que a Cindy deve levar ao PO:")
            if incomplete:
                print(f"  1. O que fazer com as {len(incomplete)} issue(s) incompleta(s) abaixo?")
                for key, status_name, summary in incomplete:
                    print(f"     - {key}: {status_name} | {summary}")
            else:
                print("  1. Nao ha issues incompletas fora da ultima coluna.")

            if open_subtasks:
                print(f"  2. Existem {len(open_subtasks)} subtask(s) aberta(s). Devemos concluir, mover ou manter a sprint aberta?")
                for key, status_name, summary, parent_key in open_subtasks:
                    print(f"     - {key} (parent {parent_key}): {status_name} | {summary}")
            else:
                print("  2. Nao ha subtasks abertas.")

            print("  3. Qual destino devemos dar aos itens incompletos quando formos concluir a sprint?")
            print("     - Backlog")
            if future_sprints:
                print("     - Sprint futura existente")
                for future in future_sprints:
                    print(f"       * {future.get('name')} (ID: {future.get('id')})")
            else:
                print("     - Nenhuma sprint futura encontrada no board neste momento")
            print("     - Nova sprint a ser criada depois de orientacao do PO")
            print("  4. Deseja manter a sprint aberta por enquanto?")
            print()
            print("[ACAO ESPERADA] Pare aqui e consulte o PO. Nao conclua a sprint ate receber a decisao explicita.")
            return 2

        print("=== PLANO ===")
        print(f"- CLOSE sprint {sprint_name_resolved} (ID: {sprint_id})")
        print(f"- Todas as {len(completed)} issues estao na ultima coluna do board: {done_column_name}")
        print()

        if dry_run:
            print("[DRY-RUN] Execute sem --dry-run para aplicar.")
            return 0

        sprint_start = sprint_details.get("startDate")
        sprint_end = sprint_details.get("endDate")
        if not sprint_start or not sprint_end:
            print("[ERRO] A sprint nao possui startDate/endDate suficientes para fechamento via API.")
            print("[ERRO] Ajuste as datas da sprint antes de tentar encerrar.")
            return 1

        print("[ATENCAO] A sprint sera encerrada no Jira.")
        if auto_confirm:
            resp = "s"
            print("[AUTO] Confirmacao automatica ativada.")
        else:
            resp = input("Continuar? [s/N]: ").strip().lower()
        if resp != "s":
            print("[INFO] Operacao cancelada.")
            return 0

        result = client.close_sprint(
            sprint_id=sprint_id,
            name=sprint_name_resolved,
            goal=sprint_goal,
            start_date=sprint_start,
            end_date=sprint_end,
        )
        print(f"[OK] Sprint '{result.get('name')}' encerrada com sucesso!")
        print(f"     ID:     {result.get('id')}")
        print(f"     Estado: {result.get('state')}")
        print(f"     Fim:    {result.get('completeDate')}")
        return 0

    except Exception as e:
        print(f"[ERRO] {e}")
        return 1


def cmd_sprint_goal(
    project_key: str = "STVIA",
    sprint_name: str | None = None,
    sprint_id: int | None = None,
    goal: str | None = None,
    dry_run: bool = False,
    auto_confirm: bool = False,
):
    """Comando sprint goal - define ou atualiza o objetivo da sprint."""
    if (sprint_name is None and sprint_id is None) or goal is None:
        print("[ERRO] informe --sprint-name ou --sprint-id, e --goal")
        print("Exemplo: python -m integrators.jira sprint goal --sprint-name 'Sprint S2' --goal 'Consolidar visibilidade executiva da entrega no Jira'")
        return 1

    mode = "DRY-RUN" if dry_run else "GOAL"
    print("=" * 60)
    print(f" {mode} - Definir Objetivo da Sprint")
    print("=" * 60)
    print()
    print(f"Projeto:    {project_key}")
    if sprint_id is not None:
        print(f"Sprint ID:  {sprint_id}")
    elif sprint_name:
        print(f"Sprint:     {sprint_name}")
    print(f"Objetivo:   {goal}")
    print()

    try:
        client = JiraClient()

        boards_resp = client.get_boards(project_key)
        boards = boards_resp.get("values", [])
        if not boards:
            print("[ERRO] Nenhum board encontrado")
            return 1

        board = boards[0]
        board_id = board["id"]

        sprint, _sprints = _resolve_sprint_target(
            client=client,
            board_id=board_id,
            sprint_id=sprint_id,
            sprint_name=sprint_name,
        )

        if not sprint:
            if sprint_id is not None:
                print(f"[ERRO] Sprint ID {sprint_id} nao encontrado no board")
            else:
                print(f"[ERRO] Sprint '{sprint_name}' nao encontrado no board")
            return 1

        sprint_id = int(sprint["id"])
        sprint_details = client.get_sprint(sprint_id)
        sprint_name = sprint_details.get("name", sprint.get("name"))
        sprint_state = sprint_details.get("state", sprint.get("state"))
        current_goal = sprint_details.get("goal") or ""
        start_date = sprint_details.get("startDate")
        end_date = sprint_details.get("endDate")

        print("=== SPRINT ===")
        print(f"ID:         {sprint_id}")
        print(f"Nome:       {sprint_name}")
        print(f"Estado:     {sprint_state}")
        print(f"Atual:      {current_goal or '(vazio)'}")
        print(f"Novo:       {goal}")
        print()

        if current_goal == goal:
            print("[INFO] O objetivo da sprint ja esta com este valor.")
            return 0

        print("=== PLANO ===")
        print(f"- UPDATE SPRINT GOAL {sprint_name} (ID: {sprint_id})")
        print(f"- Goal atual: {current_goal or '(vazio)'}")
        print(f"- Goal novo:  {goal}")
        print()

        if dry_run:
            print("[DRY-RUN] Execute sem --dry-run para aplicar.")
            return 0

        print("[ATENCAO] O objetivo da sprint sera atualizado no Jira.")
        if auto_confirm:
            resp = "s"
            print("[AUTO] Confirmacao automatica ativada.")
        else:
            resp = input("Continuar? [s/N]: ").strip().lower()
        if resp != "s":
            print("[INFO] Operacao cancelada.")
            return 0

        result = client.update_sprint(
            sprint_id=sprint_id,
            name=sprint_name,
            start_date=start_date,
            end_date=end_date,
            state=sprint_state,
            goal=goal,
        )

        print(f"[OK] Objetivo da sprint '{result.get('name')}' atualizado com sucesso!")
        print(f"     ID:       {result.get('id')}")
        print(f"     Estado:   {result.get('state')}")
        print(f"     Objetivo: {result.get('goal') or '(vazio)'}")
        return 0

    except Exception as e:
        print(f"[ERRO] {e}")
        return 1



def cmd_sprint(subcommand: str, argv: list):
    """Roteador de comandos sprint."""
    if subcommand == "status":
        return cmd_sprint_status()
    elif subcommand == "assign":
        label = None
        sprint_name = None
        sprint_id = None
        tracking_file = None
        dry_run = "--dry-run" in argv
        auto_confirm = "--yes" in argv or "-y" in argv
        for i, arg in enumerate(argv):
            if arg == "--label" and i + 1 < len(argv):
                label = argv[i + 1]
            if arg == "--tracking-file" and i + 1 < len(argv):
                tracking_file = argv[i + 1]
            if arg == "--sprint-name" and i + 1 < len(argv):
                sprint_name = argv[i + 1]
            if arg == "--sprint-id" and i + 1 < len(argv):
                sprint_id = int(argv[i + 1])
        return cmd_sprint_assign(label=label, sprint_name=sprint_name, sprint_id=sprint_id, tracking_file=tracking_file, dry_run=dry_run, auto_confirm=auto_confirm)
    elif subcommand == "open":
        dry_run = "--dry-run" in argv
        auto_confirm = "--yes" in argv or "-y" in argv
        project_key = "STVIA"
        sprint_name = None
        sprint_id = None
        for i, arg in enumerate(argv):
            if arg == "--project-key" and i + 1 < len(argv):
                project_key = argv[i + 1]
            if arg == "--sprint-name" and i + 1 < len(argv):
                sprint_name = argv[i + 1]
            if arg == "--sprint-id" and i + 1 < len(argv):
                sprint_id = int(argv[i + 1])
        return cmd_sprint_open(project_key=project_key, sprint_name=sprint_name, sprint_id=sprint_id, dry_run=dry_run, auto_confirm=auto_confirm)
    elif subcommand == "close":
        dry_run = "--dry-run" in argv
        auto_confirm = "--yes" in argv or "-y" in argv
        project_key = "STVIA"
        sprint_name = None
        sprint_id = None
        for i, arg in enumerate(argv):
            if arg == "--project-key" and i + 1 < len(argv):
                project_key = argv[i + 1]
            if arg == "--sprint-name" and i + 1 < len(argv):
                sprint_name = argv[i + 1]
            if arg == "--sprint-id" and i + 1 < len(argv):
                sprint_id = int(argv[i + 1])
        return cmd_sprint_close(
            project_key=project_key,
            sprint_name=sprint_name,
            sprint_id=sprint_id,
            dry_run=dry_run,
            auto_confirm=auto_confirm,
        )
    elif subcommand == "dates":
        sprint_name = None
        sprint_id = None
        start_date = None
        end_date = None
        dry_run = "--dry-run" in argv
        auto_confirm = "--yes" in argv or "-y" in argv
        for i, arg in enumerate(argv):
            if arg == "--sprint-name" and i + 1 < len(argv):
                sprint_name = argv[i + 1]
            if arg == "--sprint-id" and i + 1 < len(argv):
                sprint_id = int(argv[i + 1])
            if arg == "--start-date" and i + 1 < len(argv):
                start_date = argv[i + 1]
            if arg == "--end-date" and i + 1 < len(argv):
                end_date = argv[i + 1]
        return cmd_sprint_dates(sprint_name=sprint_name, sprint_id=sprint_id, start_date=start_date, end_date=end_date, dry_run=dry_run, auto_confirm=auto_confirm)
    elif subcommand == "create":
        sprint_name = None
        goal = None
        start_date = None
        end_date = None
        dry_run = "--dry-run" in argv
        auto_confirm = "--yes" in argv or "-y" in argv
        project_key = "STVIA"
        for i, arg in enumerate(argv):
            if arg == "--project-key" and i + 1 < len(argv):
                project_key = argv[i + 1]
            if arg == "--sprint-name" and i + 1 < len(argv):
                sprint_name = argv[i + 1]
            if arg == "--goal" and i + 1 < len(argv):
                goal = argv[i + 1]
            if arg == "--start-date" and i + 1 < len(argv):
                start_date = argv[i + 1]
            if arg == "--end-date" and i + 1 < len(argv):
                end_date = argv[i + 1]
        return cmd_sprint_create(project_key=project_key, sprint_name=sprint_name, goal=goal, start_date=start_date, end_date=end_date, dry_run=dry_run, auto_confirm=auto_confirm)
    elif subcommand == "goal":
        project_key = "STVIA"
        sprint_name = None
        sprint_id = None
        goal = None
        dry_run = "--dry-run" in argv
        auto_confirm = "--yes" in argv or "-y" in argv
        for i, arg in enumerate(argv):
            if arg == "--project-key" and i + 1 < len(argv):
                project_key = argv[i + 1]
            if arg == "--sprint-name" and i + 1 < len(argv):
                sprint_name = argv[i + 1]
            if arg == "--sprint-id" and i + 1 < len(argv):
                sprint_id = int(argv[i + 1])
            if arg == "--goal" and i + 1 < len(argv):
                goal = argv[i + 1]
        return cmd_sprint_goal(
            project_key=project_key,
            sprint_name=sprint_name,
            sprint_id=sprint_id,
            goal=goal,
            dry_run=dry_run,
            auto_confirm=auto_confirm,
        )
    else:
        print(f"[ERRO] Subcomando desconhecido: {subcommand}")
        print()
        print("Comandos sprint:")
        print("  sprint status                     - Lista boards e sprints")
        print("  sprint create --sprint-name X [--goal '...'] [--start-date YYYY-MM-DD] [--end-date YYYY-MM-DD] [--project-key STVIA] - Cria nova sprint (fim padrao = inicio + 3 dias)")
        print("  sprint assign [--tracking-file X|--label Y] [--sprint-name Z|--sprint-id N] - Atribui issues ao sprint nativo")
        print("  sprint goal [--sprint-name X|--sprint-id N] --goal '...' - Define o objetivo da sprint")
        print("  sprint open [--project-key STVIA] [--sprint-name X|--sprint-id N] [--dry-run] [--yes] - Abre sprint futura especifica ou a candidata do dia")
        print("  sprint close [--project-key STVIA] [--sprint-name X|--sprint-id N] [--dry-run] [--yes] - Encerra sprint ativa ou nomeada; se houver incompletas, para e exige decisao do PO")
        print("  sprint dates [--sprint-name X|--sprint-id N] --start-date YYYY-MM-DD [--end-date YYYY-MM-DD] - Define datas do sprint (fim padrao = inicio + 3 dias)")
        return 1



def cmd_board_columns(project_key: str = "STVIA", board_id: int | None = None, save: bool = True):
    """Comando board columns - lista colunas do board e orienta o estado local."""
    print("=" * 60)
    print(" BOARD COLUMNS - Colunas e Status do Board")
    print("=" * 60)
    print()

    state = load_state()
    if not state:
        print("[ERRO] Estado nao encontrado.")
        print("Execute primeiro: python -m integrators.jira bootstrap")
        return 1

    try:
        client = JiraClient()

        # Resolve id -> name de statuses
        statuses = client.get_statuses()
        id_to_name = {}
        for st in statuses:
            sid = st.get("id")
            nm = st.get("name")
            if sid and nm:
                id_to_name[str(sid)] = nm

        # Resolve board
        if board_id is None:
            boards_resp = client.get_boards(project_key)
            boards = boards_resp.get("values", []) or []
            if not boards:
                print(f"[ERRO] Nenhum board encontrado para projeto {project_key}")
                return 1
            board = boards[0]
            board_id = int(board.get("id"))
            state.boards = [
                {"id": b.get("id"), "name": b.get("name"), "type": b.get("type")}
                for b in boards
                if b.get("id") is not None
            ]
            state.board_id = board_id
            state.board_name = board.get("name", "")
            state.board_type = board.get("type", "")
        else:
            state.board_id = int(board_id)

        cfg = client.get_board_configuration(int(state.board_id))
        columns = cfg.get("columnConfig", {}).get("columns", []) or []

        print(f"Projeto: {project_key}")
        print(f"Board:   {state.board_name or '(desconhecido)'} (ID: {state.board_id}, Type: {state.board_type or 'n/a'})")
        print()

        if not columns:
            print("[INFO] Nenhuma coluna encontrada no board.")
            return 0

        state.board_columns = []
        for c in columns:
            col_name = c.get("name", "")
            status_objs = c.get("statuses", []) or []
            status_ids = [str(s.get("id")) for s in status_objs if s.get("id") is not None]
            status_names = [id_to_name.get(sid, f"(id:{sid})") for sid in status_ids]
            status_names = sorted(set(status_names))

            state.board_columns.append({
                "name": col_name,
                "status_ids": status_ids,
                "status_names": [id_to_name.get(sid, "") for sid in status_ids if id_to_name.get(sid, "")],
            })

            print(f"- {col_name}: {', '.join(status_names) if status_names else '(sem status)'}")

        state.local_status_guidance = derive_local_status_guidance(state.board_columns)

        print()
        print("Orientacao para estado local (somente referencia):")
        for item in state.local_status_guidance:
            suggestions = ", ".join(item.get("suggested_local_statuses", [])) or "(sem sugestao direta)"
            jira_statuses = ", ".join(item.get("jira_statuses", [])) or "(sem status)"
            print(f"- {item.get('board_column', '(sem nome)')}: {suggestions}")
            print(f"  Status Jira: {jira_statuses}")
            print(f"  Nota: {item.get('note', '')}")

        print()
        if save:
            save_state(state)
            print("[OK] Colunas do board e orientacao local registradas no estado observado.")
        else:
            print("[INFO] Modo --no-save: nada foi escrito em .scr/.")

        return 0

    except Exception as e:
        print(f"[ERRO] {e}")
        return 1


def cmd_board(subcommand: str, argv: list):
    """Roteador de comandos board."""
    if subcommand == "columns":
        project_key = "STVIA"
        board_id = None
        save = True
        for i, arg in enumerate(argv):
            if arg == "--project-key" and i + 1 < len(argv):
                project_key = argv[i + 1]
            if arg == "--board-id" and i + 1 < len(argv):
                try:
                    board_id = int(argv[i + 1])
                except ValueError:
                    board_id = None
            if arg == "--no-save":
                save = False
        return cmd_board_columns(project_key=project_key, board_id=board_id, save=save)

    print(f"[ERRO] Subcomando desconhecido: {subcommand}")
    print("Use: board columns [--project-key STVIA] [--board-id 1] [--no-save]")
    return 1


def cmd_issue_progress(
    tracking_file: str = "Dev_Tracking_S2.md",
    prefix: str = "ST-S0-",
    target_status: str = "Em andamento",
    dry_run: bool = False,
    auto_confirm: bool = False,
    all_items: bool = False,
):
    """Comando issue progress - transiciona issues do tracking para status especificado."""
    mode = "DRY-RUN" if dry_run else "PROGRESS"
    print("=" * 60)
    print(f" {mode} - Transicionar Issues para '{target_status}'")
    print("=" * 60)
    print()
    print(f"Tracking:   {tracking_file}")
    print(f"Prefix:     {prefix}")
    print(f"Target:     {target_status}")
    if all_items:
        print("[ALL]     Todos os items com prefixo (sem filtro de status)")
    print()

    # Carrega tracking
    tracking_path = Path(tracking_file)
    if not tracking_path.exists():
        print(f"[ERRO] Arquivo nao encontrado: {tracking_file}")
        return 1

    try:
        client = JiraClient()

        # Parse tracking
        result = parse_sprint_backlog(tracking_file)
        items = result.get("items", [])

        # Filtra items por prefixo
        if all_items:
            target_items = [i for i in items if i.tracking_key.startswith(prefix)]
        else:
            target_items = [
                i for i in items
                if i.tracking_key.startswith(prefix) and i.status.lower().startswith("pending")
            ]

        if not target_items:
            print("[INFO] Nenhum item encontrado com os criterios especificados.")
            return 0

        print(f"Itens encontrados: {len(target_items)}")
        print()

        # Monta plano de transicao
        plan = []
        skipped = []

        for item in target_items:
            # Resolve issue key
            issue_key = item.jira if item.jira else None

            # Se nao tem jira key, tenta buscar por label
            if not issue_key:
                # Busca issues com label tracking_<item_id>
                try:
                    jql = f'labels = "tracking_{item.tracking_key}" AND project = STVIA'
                    search_result = client.search_issues(jql, max_results=1)
                    issues = search_result.get("issues", [])
                    if issues:
                        issue_key = issues[0].get("key")
                except Exception:
                    pass

            if not issue_key:
                skipped.append({
                    "item_id": item.tracking_key,
                    "status": item.status,
                    "reason": "Sem Jira key e label nao encontrada",
                })
                continue

            # Busca status atual
            try:
                issue = client.get_issue(issue_key)
                current_status = issue["fields"]["status"]["name"]
            except Exception as e:
                skipped.append({
                    "item_id": item.tracking_key,
                    "issue_key": issue_key,
                    "reason": f"Erro ao buscar issue: {e}",
                })
                continue

            # Se ja esta no status target, skip
            if current_status.lower() == target_status.lower():
                skipped.append({
                    "item_id": item.tracking_key,
                    "issue_key": issue_key,
                    "current_status": current_status,
                    "reason": "Ja no status target",
                })
                continue

            # Busca transicoes disponiveis
            try:
                transitions_resp = client.get_transitions(issue_key)
                transitions = transitions_resp.get("transitions", [])

                # Encontra transicao para target status
                transition_id = None
                for t in transitions:
                    if t["to"]["name"].lower() == target_status.lower():
                        transition_id = t["id"]
                        break

                if not transition_id:
                    skipped.append({
                        "item_id": item.tracking_key,
                        "issue_key": issue_key,
                        "current_status": current_status,
                        "reason": f"Transicao para '{target_status}' nao disponivel",
                    })
                    continue

                plan.append({
                    "item_id": item.tracking_key,
                    "issue_key": issue_key,
                    "current_status": current_status,
                    "target_status": target_status,
                    "transition_id": transition_id,
                })
            except Exception as e:
                skipped.append({
                    "item_id": item.tracking_key,
                    "issue_key": issue_key,
                    "reason": f"Erro ao buscar transicoes: {e}",
                })
                continue

        # Imprime plano
        if skipped:
            print("=== SKIPPED ===")
            for s in skipped:
                print(f"  {s.get('item_id', '?')} ({s.get('issue_key', '?')}): {s.get('reason', 'N/A')}")
            print()

        if not plan:
            print("[INFO] Nenhuma transicao necessaria.")
            return 0

        print("=== PLANO DE TRANSICAO ===")
        print(f"{'Issue Key':<12} {'DOC25 ID':<12} {'Status Atual':<15} -> {'Target':<15} {'Action':<10}")
        print("-" * 80)
        for p in plan:
            print(f"{p['issue_key']:<12} {p['item_id']:<12} {p['current_status']:<15} -> {p['target_status']:<15} TRANSITION")
        print()

        print(f"Total: {len(plan)} transicoes, {len(skipped)} pulados")
        print()

        if dry_run:
            print("[DRY-RUN] Execute sem --dry-run para aplicar.")
            return 0

        # Confirm
        print("[ATENCAO] As transicoes serao executadas no Jira.")
        if auto_confirm:
            resp = "s"
            print("[AUTO] Confirmacao automatica ativada.")
        else:
            resp = input("Continuar? [s/N]: ").strip().lower()
        if resp != "s":
            print("[INFO] Operacao cancelada.")
            return 0

        # Executa transicoes
        success = 0
        failed = 0
        print()
        for p in plan:
            try:
                client.transition_issue(p["issue_key"], p["transition_id"])
                print(f"  [OK] {p['issue_key']}: {p['current_status']} -> {p['target_status']}")
                success += 1
            except Exception as e:
                print(f"  [ERRO] {p['issue_key']}: {e}")
                failed += 1

        print()
        print(f"[OK] Concluido: {success} sucesso, {failed} falhas")
        return 0

    except Exception as e:
        print(f"[ERRO] {e}")
        return 1


def cmd_issue_transition(
    issue_key: str,
    target_status: str,
    dry_run: bool = False,
    auto_confirm: bool = False,
    comment: str | None = None,
):
    """Comando issue transition - transiciona uma issue e opcionalmente comenta."""
    mode = "DRY-RUN" if dry_run else "TRANSITION"
    print("=" * 60)
    print(f" {mode} - Transicionar Issue")
    print("=" * 60)
    print()
    print(f"Issue:      {issue_key}")
    print(f"Target:     {target_status}")
    if comment:
        print(f"Comment:    {comment}")
    print()

    try:
        client = JiraClient()

        issue = client.get_issue(issue_key)
        current_status = issue["fields"]["status"]["name"]
        summary = issue["fields"].get("summary", "")

        transitions_resp = client.get_transitions(issue_key)
        transitions = transitions_resp.get("transitions", [])

        transition_id = None
        available_targets = []
        for transition in transitions:
            to_name = transition.get("to", {}).get("name", "")
            if to_name:
                available_targets.append(to_name)
            if to_name.lower() == target_status.lower():
                transition_id = transition.get("id")

        print("=== ISSUE ===")
        print(f"Summary:    {summary}")
        print(f"Atual:      {current_status}")
        print(f"Disponivel: {', '.join(available_targets) if available_targets else '(nenhuma transicao)'}")
        print()

        if current_status.lower() == target_status.lower():
            print("[INFO] A issue ja esta no status target.")
            if comment:
                print("[INFO] Comentario ainda pode ser adicionado nesta mesma operacao.")
            else:
                return 0

        if current_status.lower() != target_status.lower() and not transition_id:
            print(f"[ERRO] Transicao para '{target_status}' nao disponivel.")
            return 1

        print("=== PLANO ===")
        if current_status.lower() == target_status.lower():
            print(f"- COMMENT {issue_key}")
        else:
            print(f"- TRANSITION {issue_key}: {current_status} -> {target_status}")
            if comment:
                print(f"- COMMENT {issue_key}")
        print()

        if dry_run:
            print("[DRY-RUN] Execute sem --dry-run para aplicar.")
            return 0

        print("[ATENCAO] A operacao sera executada no Jira.")
        if auto_confirm:
            resp = "s"
            print("[AUTO] Confirmacao automatica ativada.")
        else:
            resp = input("Continuar? [s/N]: ").strip().lower()
        if resp != "s":
            print("[INFO] Operacao cancelada.")
            return 0

        if current_status.lower() != target_status.lower() and transition_id:
            client.transition_issue(issue_key, transition_id)
            print(f"[OK] {issue_key}: {current_status} -> {target_status}")

        if comment:
            client.add_comment(issue_key, comment)
            print(f"[OK] Comentario adicionado em {issue_key}")

        return 0

    except Exception as e:
        print(f"[ERRO] {e}")
        return 1


def cmd_issue_bulk(
    project_key: str = "STVIA",
    target_status: str = "Feito",
    exclude_status: str | None = None,
    dry_run: bool = False,
    auto_confirm: bool = False,
):
    """Comando issue bulk - transiciona todas as issues do projeto para status especificado."""
    mode = "DRY-RUN" if dry_run else "BULK"
    print("=" * 60)
    print(f" {mode} - Transicionar Todas as Issues para '{target_status}'")
    print("=" * 60)
    print()
    print(f"Projeto:    {project_key}")
    print(f"Target:     {target_status}")
    if exclude_status:
        print(f"Excluir:    {exclude_status}")
    print()

    try:
        client = JiraClient()

        # Busca todas as issues do projeto
        search_result = client.get_project_issues(project_key, max_results=100)
        issues = search_result.get("issues", [])

        if not issues:
            print("[INFO] Nenhuma issue encontrada no projeto.")
            return 0

        print(f"Issues encontradas no projeto: {len(issues)}")
        print()

        # Monta plano de transicao
        plan = []
        already_done = []
        skipped = []

        for issue in issues:
            issue_key = issue.get("key")
            summary = issue["fields"].get("summary", "")
            current_status = issue["fields"]["status"]["name"]

            # Se ja esta no target, marca como done
            if current_status.lower() == target_status.lower():
                already_done.append({
                    "issue_key": issue_key,
                    "summary": summary,
                    "current_status": current_status,
                })
                continue

            # Se tem status de exclusao, pula
            if exclude_status and current_status.lower() == exclude_status.lower():
                skipped.append({
                    "issue_key": issue_key,
                    "summary": summary,
                    "current_status": current_status,
                    "reason": f"Status '{exclude_status}' excluido",
                })
                continue

            # Busca transicoes disponiveis
            try:
                transitions_resp = client.get_transitions(issue_key)
                transitions = transitions_resp.get("transitions", [])

                # Encontra transicao para target status
                transition_id = None
                for t in transitions:
                    if t["to"]["name"].lower() == target_status.lower():
                        transition_id = t["id"]
                        break

                if not transition_id:
                    skipped.append({
                        "issue_key": issue_key,
                        "summary": summary,
                        "current_status": current_status,
                        "reason": f"Transicao para '{target_status}' nao disponivel",
                    })
                    continue

                plan.append({
                    "issue_key": issue_key,
                    "summary": summary,
                    "current_status": current_status,
                    "target_status": target_status,
                    "transition_id": transition_id,
                })
            except Exception as e:
                skipped.append({
                    "issue_key": issue_key,
                    "summary": summary,
                    "current_status": current_status,
                    "reason": f"Erro ao buscar transicoes: {e}",
                })
                continue

        # Imprime resultado
        print("=== JA NO TARGET ===")
        if already_done:
            for item in already_done:
                print(f"  {item['issue_key']}: {item['current_status']}")
        else:
            print("  Nenhuma")
        print()

        print("=== SKIPPED ===")
        if skipped:
            for item in skipped:
                print(f"  {item['issue_key']}: {item['current_status']} - {item['reason']}")
        else:
            print("  Nenhuma")
        print()

        if not plan:
            print("[INFO] Nenhuma transicao necessaria.")
            return 0

        print("=== PLANO DE TRANSICAO ===")
        print(f"{'Issue Key':<12} {'Status Atual':<15} -> {'Target':<15}")
        print("-" * 60)
        for p in plan:
            print(f"{p['issue_key']:<12} {p['current_status']:<15} -> {p['target_status']:<15}")
        print()

        print(f"Total: {len(plan)} transicoes, {len(already_done)} ja no target, {len(skipped)} puladas")
        print()

        if dry_run:
            print("[DRY-RUN] Execute sem --dry-run para aplicar.")
            return 0

        # Executa transicoes (sem confirmacao adicional se auto_confirm=True)
        if not auto_confirm:
            print("[ATENCAO] As transicoes serao executadas no Jira.")
            resp = input("Continuar? [s/N]: ").strip().lower()
            if resp != "s":
                print("[INFO] Operacao cancelada.")
                return 0

        # Executa transicoes
        success = 0
        failed = 0
        print()
        for p in plan:
            try:
                client.transition_issue(p["issue_key"], p["transition_id"])
                print(f"  [OK] {p['issue_key']}: {p['current_status']} -> {p['target_status']}")
                success += 1
            except Exception as e:
                print(f"  [ERRO] {p['issue_key']}: {e}")
                failed += 1

        print()
        print(f"[OK] Concluido: {success} sucesso, {failed} falhas")
        return 0

    except Exception as e:
        print(f"[ERRO] {e}")
        return 1


def cmd_issue(subcommand: str, argv: list[str]):
    """Roteador de comandos issue."""
    if subcommand == "bulk":
        return cmd_issue_bulk(
            project_key=_arg_value(argv, "--project-key", "STVIA"),
            target_status=_arg_value(argv, "--target-status", "Feito"),
            exclude_status=_arg_value(argv, "--exclude-status"),
            dry_run=_has_flag(argv, "--dry-run"),
            auto_confirm=_has_flag(argv, "--yes", "-y"),
        )

    if subcommand == "progress":
        return cmd_issue_progress(
            tracking_file=_arg_value(argv, "--tracking-file", "Dev_Tracking_S2.md"),
            prefix=_arg_value(argv, "--prefix", "ST-S0-"),
            target_status=_arg_value(argv, "--target-status", "Em andamento"),
            dry_run=_has_flag(argv, "--dry-run"),
            auto_confirm=_has_flag(argv, "--yes", "-y"),
            all_items=_has_flag(argv, "--all"),
        )

    if subcommand == "transition":
        issue_key = _arg_value(argv, "--issue-key", "")
        target_status = _arg_value(argv, "--target-status", "")
        comment = _arg_value(argv, "--comment")
        if not issue_key or not target_status:
            print("[ERRO] Use: issue transition --issue-key STVIA-123 --target-status 'Bloqueado' [--comment '...'] [--dry-run] [--yes]")
            return 1
        return cmd_issue_transition(
            issue_key=issue_key,
            target_status=target_status,
            dry_run=_has_flag(argv, "--dry-run"),
            auto_confirm=_has_flag(argv, "--yes", "-y"),
            comment=comment,
        )

    if subcommand == "dates":
        return cmd_issue_dates(
            tracking_file=_arg_value(argv, "--tracking-file", "Dev_Tracking_S2.md"),
            dry_run=_has_flag(argv, "--dry-run"),
            auto_confirm=_has_flag(argv, "--yes", "-y"),
        )

    print(f"[ERRO] Subcomando desconhecido: {subcommand}")
    print("[ERRO] Use: issue bulk | issue dates | issue progress | issue transition")
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
        print("  sprint open      - Abre sprint com base no Start Date (UTC)")
        print("  sprint close     - Encerra a sprint ativa ou uma sprint nomeada; se houver incompletas, exige decisao do PO")
        print("  board columns    - Lista colunas do board Jira")
        print("  issue bulk       - Transiciona issues do projeto por escopo Jira")
        print("  issue dates      - Sincroniza datas de issues com timestamps")
        print("  issue progress   - Transiciona issues para status especificado")
        print("  issue transition - Transiciona uma issue e opcionalmente comenta")
        print()
        print("Exemplo sprint close:")
        print("  python -m integrators.jira sprint close --project-key STVIA --dry-run")
        print("  python -m integrators.jira sprint close --project-key STVIA --yes")
        print()
        print("Exemplo issue bulk:")
        print("  python -m integrators.jira issue bulk --target-status 'Feito' --dry-run")
        print("  python -m integrators.jira issue bulk --target-status 'Feito' --exclude-status 'Bloqueado' --yes")
        print()
        print("Exemplo issue progress:")
        print("  python -m integrators.jira issue progress --dry-run")
        print("  python -m integrators.jira issue progress --tracking-file Dev_Tracking_S2.md --prefix ST-S0- --target-status 'Em andamento'")
        print("  python -m integrators.jira issue progress --yes  # Apply transitions")
        print()
        print("Exemplo issue transition:")
        print("  python -m integrators.jira issue transition --issue-key STVIA-123 --target-status 'Bloqueado' --dry-run")
        print("  python -m integrators.jira issue transition --issue-key STVIA-123 --target-status 'Bloqueado' --comment 'Bloqueio temporario aguardando definicao de estado.' --yes")
        return 1

    command = sys.argv[1]

    # Sprint subcommand handler
    if command == "sprint":
        if len(sys.argv) < 3:
            print("[ERRO] Faltando subcomando")
            print("Use: sprint status | sprint assign | sprint open | sprint dates ...")
            return 1
        subcommand = sys.argv[2]
        return cmd_sprint(subcommand, sys.argv[3:])

    # Board subcommand handler
    if command == "board":
        if len(sys.argv) < 3:
            print("[ERRO] Faltando subcomando")
            print("Use: board columns ...")
            return 1
        subcommand = sys.argv[2]
        return cmd_board(subcommand, sys.argv[3:])

    if command == "status":
        return cmd_status()
    elif command == "discover":
        return cmd_discover()
    elif command == "sync":
        dry_run = "--dry-run" in sys.argv
        # Parse --tracking-file argument
        tracking_file = "Dev_Tracking_S2.md"  # default - S2 is the active sprint
        auto_confirm = "--yes" in sys.argv or "-y" in sys.argv
        write_back = "--write-back" in sys.argv
        for i, arg in enumerate(sys.argv):
            if arg == "--tracking-file" and i + 1 < len(sys.argv):
                tracking_file = sys.argv[i + 1]
        return cmd_sync(tracking_file=tracking_file, dry_run=dry_run, auto_confirm=auto_confirm, write_back=write_back)
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
        if len(sys.argv) < 3:
            print("[ERRO] Use: issue bulk | issue dates | issue progress | issue transition")
            return 1
        return cmd_issue(sys.argv[2], sys.argv[3:])
    else:
        print(f"[ERRO] Comando desconhecido: {command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
