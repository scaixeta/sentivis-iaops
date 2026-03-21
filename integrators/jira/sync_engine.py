#!/usr/bin/env python3
"""
jira/sync_engine.py - Engine de Sincronização Jira

Executa sincronização entre tracking local e Jira.

Uso:
    from integrators.jira import SyncEngine
    engine = SyncEngine()
    plan = engine.dry_run()
    engine.sync(plan)
"""

import json
from dataclasses import dataclass
from typing import Any

from .board_reader import derive_local_status_guidance
from .client import JiraClient
from .mapper import JiraPayload, build_sync_plan, STORY_POINTS_FIELD
from .state import JiraState, get_fingerprint, load_state, save_state
from ..common.doc25_parser import Doc25Item, parse_sprint_backlog, parse_bug_log_for_sprint


@dataclass
class SyncResult:
    """Resultado de uma operacao de sincronizacao."""
    operation: str
    issue_key: str | None
    success: bool
    error: str | None
    payload: dict | None


class SyncEngine:
    """Engine de sincronizacao entre DOC2.5 e Jira."""

    def __init__(self):
        self.client = JiraClient()
        self.state = load_state()

        if not self.state:
            raise RuntimeError("Estado nao encontrado. Execute mgmt_layer_jira_init.py primeiro.")

    def discover(self) -> dict:
        """Executa discover - busca metadados do Jira."""
        print("[INFO] Executando discover...")

        # Busca usuario
        user = self.client.get_myself()
        self.state.authenticated_user = {
            "account_id": user.get("accountId"),
            "display_name": user.get("displayName"),
            "email": user.get("emailAddress"),
        }

        # Busca projeto
        project = self.client.get_project(self.state.project_key)
        self.state.project_id = project.get("id", "")
        self.state.project_type = project.get("projectTypeKey", "")

        # Mapeia issue types
        issue_types = self.client.get_issue_types()
        self.state.issue_type_map = {}
        for it in issue_types:
            name = it.get("name", "")
            it_id = it.get("id", "")
            # Mapeia por nome para uso posterior
            self.state.issue_type_map[name] = it_id

        # Mapeia statuses
        statuses = self.client.get_statuses()
        self.state.status_map = {}
        for st in statuses:
            name = st.get("name", "")
            st_id = st.get("id", "")
            self.state.status_map[name] = st_id

        # Boards e colunas (Jira Software)
        try:
            boards_resp = self.client.get_boards(self.state.project_key)
            boards = boards_resp.get("values", []) or []
            self.state.boards = [
                {"id": b.get("id"), "name": b.get("name"), "type": b.get("type")}
                for b in boards
                if b.get("id") is not None
            ]

            if boards:
                board = boards[0]
                self.state.board_id = board.get("id")
                self.state.board_name = board.get("name", "")
                self.state.board_type = board.get("type", "")

                cfg = self.client.get_board_configuration(int(self.state.board_id))
                columns = cfg.get("columnConfig", {}).get("columns", []) or []

                # Resolve status ids -> names usando a lista de statuses
                id_to_name = {}
                for st in statuses:
                    sid = st.get("id")
                    nm = st.get("name")
                    if sid and nm:
                        id_to_name[str(sid)] = nm

                self.state.board_columns = []
                for c in columns:
                    col_name = c.get("name", "")
                    status_objs = c.get("statuses", []) or []
                    status_ids = [str(s.get("id")) for s in status_objs if s.get("id") is not None]
                    status_names = [id_to_name.get(sid, "") for sid in status_ids]
                    status_names = [n for n in status_names if n]
                    self.state.board_columns.append({
                        "name": col_name,
                        "status_ids": status_ids,
                        "status_names": status_names,
                    })
                self.state.local_status_guidance = derive_local_status_guidance(self.state.board_columns)
        except Exception:
            # Board configuration may be unavailable depending on Jira permissions or plan.
            pass

        # Atualiza fingerprint
        self.state.last_sync_fingerprint = get_fingerprint(self.state)

        print(f"[OK] Usuario: {self.state.authenticated_user.get('display_name')}")
        print(f"[OK] Projeto: {self.state.project_key} ({self.state.project_id})")
        print(f"[OK] Issue Types: {len(self.state.issue_type_map)}")
        print(f"[OK] Statuses: {len(self.state.status_map)}")

        return self.state.to_dict()

    def get_local_items(self, tracking_file: str = "Dev_Tracking_S1.md") -> list[Doc25Item]:
        """Busca itens do tracking local e bugs da sprint no bugs_log."""
        result = parse_sprint_backlog(tracking_file)
        items = list(result.get("items", []))
        sprint = result.get("sprint", "")
        if sprint:
            bug_items = parse_bug_log_for_sprint("tests/bugs_log.md", sprint)
            items.extend(bug_items)
        return items

    def get_jira_issues(self) -> list[dict]:
        """Busca issues do Jira."""
        response = self.client.get_project_issues(self.state.project_key, max_results=100)
        return response.get("issues", [])

    def dry_run(self, tracking_file: str = "Dev_Tracking_S1.md") -> list[JiraPayload]:
        """
        Executa dry-run - mostra delta sem alterar nada.
        """
        print("[DRY-RUN] Computando delta de sincronizacao...")

        # Carrega itens locais
        local_items = self.get_local_items(tracking_file)
        print(f"[INFO] Itens locais: {len(local_items)}")

        # Carrega issues Jira
        jira_issues = self.get_jira_issues()
        print(f"[INFO] Issues Jira: {len(jira_issues)}")

        # Constroi plano
        plan = build_sync_plan(
            local_items,
            jira_issues,
            self.state.project_key,
            self.state,
            client=self.client,
        )

        print(f"[DRY-RUN] Operacoes a executar: {len(plan)}")
        for i, op in enumerate(plan, 1):
            if op.action == "align_status":
                current_status = op.fields.get("current_status", "?") if op.fields else "?"
                target_status = op.fields.get("target_status", "?") if op.fields else "?"
                effective_target_status = op.fields.get("effective_target_status", target_status) if op.fields else target_status
                next_status = op.fields.get("next_status", "?") if op.fields else "?"
                strategy = op.fields.get("status_strategy") if op.fields else None
                if effective_target_status != target_status:
                    print(f"  {i}. [ALIGN_STATUS] {op.issue_key} {current_status} -> {target_status} (alvo efetivo: {effective_target_status}; proximo passo: {next_status})")
                else:
                    print(f"  {i}. [ALIGN_STATUS] {op.issue_key} {current_status} -> {target_status} (proximo passo: {next_status})")
                if strategy:
                    print(f"      estrategia: {strategy}")
            elif op.action == "status_mismatch":
                current_status = op.fields.get("current_status", "?") if op.fields else "?"
                target_status = op.fields.get("target_status", "?") if op.fields else "?"
                print(f"  {i}. [STATUS_MISMATCH] {op.issue_key} {current_status} -> {target_status} (sem transicao disponivel)")
            else:
                print(f"  {i}. [{op.action.upper()}] {op.issue_key or '(nova)'} - {op.fields.get('summary', 'N/A')[:50] if op.fields else ''}")

        return plan

    def _align_issue_status_naturally(self, issue_key: str, target_status: str, max_hops: int = 10) -> list[str]:
        """
        Transiciona uma issue passo a passo entre as colunas/status do board
        ate atingir o status alvo.
        """
        from .mapper import plan_natural_transition_step

        path: list[str] = []

        for _ in range(max_hops):
            issue = self.client.get_issue(issue_key)
            current_status = issue.get("fields", {}).get("status", {}).get("name", "")
            if current_status.lower() == target_status.lower():
                return path

            transitions_resp = self.client.get_transitions(issue_key)
            transitions = transitions_resp.get("transitions", [])
            transition_id, next_status = plan_natural_transition_step(
                current_status,
                target_status,
                transitions,
                self.state,
            )

            if not transition_id or not next_status:
                raise RuntimeError(
                    f"Sem caminho natural de transicao: {current_status} -> {target_status}"
                )

            self.client.transition_issue(issue_key, transition_id)
            path.append(next_status)

        raise RuntimeError(
            f"Numero maximo de hops excedido ao alinhar {issue_key} para {target_status}"
        )

    def sync(self, plan: list[JiraPayload], dry_run: bool = False) -> list[SyncResult]:
        """
        Executa sincronizacao.
        """
        if dry_run:
            print("[DRY-RUN] Nenhuma alteracao sera feita.")
            return []

        results = []

        for op in plan:
            # Ignora operacoes "none" (itens ja em dia)
            if op.action == "none":
                continue

            result = SyncResult(
                operation=op.action,
                issue_key=op.issue_key,
                success=False,
                error=None,
                payload=None
            )

            try:
                if op.action == "create":
                    print(f"[CREATE] {op.fields.get('summary', 'N/A')[:50]}...")
                    
                    # Usa create_issue com campos extras (incluindo SP)
                    response = self.client.create_issue(
                        project_key=self.state.project_key,
                        summary=op.fields.get("summary", ""),
                        issue_type=op.fields.get("issuetype", {}).get("name", "Task"),
                        description=op.fields.get("summary", ""),
                        labels=op.fields.get("labels", []),
                        extra_fields=op.fields  # Passa campos extras (SP)
                    )
                    result.issue_key = response.get("key")
                    result.success = True
                    print(f"[OK] Criada: {result.issue_key}")

                elif op.action == "update":
                    print(f"[UPDATE] {op.issue_key}...")
                    self.client.update_issue(op.issue_key, op.fields)
                    result.success = True
                    print(f"[OK] Atualizada: {op.issue_key}")

                elif op.action == "align_status":
                    target_status = op.fields.get("effective_target_status", "") if op.fields else ""
                    requested_target_status = op.fields.get("target_status", target_status) if op.fields else target_status
                    current_status = op.fields.get("current_status", "") if op.fields else ""
                    if requested_target_status != target_status:
                        print(f"[ALIGN_STATUS] {op.issue_key} {current_status} -> {requested_target_status} (alvo efetivo: {target_status})...")
                    else:
                        print(f"[ALIGN_STATUS] {op.issue_key} {current_status} -> {target_status}...")
                    path = self._align_issue_status_naturally(op.issue_key, target_status)
                    result.payload = {
                        "path": path,
                        "target_status": target_status,
                        "requested_target_status": requested_target_status,
                        "status_strategy": op.fields.get("status_strategy") if op.fields else None,
                    }
                    result.success = True
                    if path:
                        print(f"[OK] Alinhada: {op.issue_key} via {' -> '.join(path)}")
                    else:
                        print(f"[OK] Alinhada: {op.issue_key}")

                elif op.action == "status_mismatch":
                    current_status = op.fields.get("current_status", "?") if op.fields else "?"
                    target_status = op.fields.get("target_status", "?") if op.fields else "?"
                    result.error = f"Sem transicao disponivel: {current_status} -> {target_status}"
                    result.success = False
                    print(f"[WARN] {op.issue_key}: status divergente sem transicao disponivel ({current_status} -> {target_status})")

                elif op.action == "comment":
                    print(f"[COMMENT] {op.issue_key}...")
                    self.client.add_comment(op.issue_key, op.comment)
                    result.success = True
                    print(f"[OK] Comentario adicionado: {op.issue_key}")

            except Exception as e:
                result.error = str(e)
                result.success = False
                print(f"[ERRO] {op.action} falhou: {e}")

            results.append(result)

        # Atualiza estado
        self.state.last_sync_fingerprint = get_fingerprint(self.state)
        save_state(self.state)

        return results


def main():
    """CLI simples para sync."""
    import sys

    engine = SyncEngine()

    if len(sys.argv) < 2:
        print("Usage: jira_sync_engine.py <tracking_file>")
        sys.exit(1)

    tracking_file = sys.argv[1]

    # Dry-run
    plan = engine.dry_run(tracking_file)

    if not plan:
        print("[INFO] Nenhuma operacao necessaria.")
        return

    print(f"\nTotal: {len(plan)} operacoes pendentes")


if __name__ == "__main__":
    main()
