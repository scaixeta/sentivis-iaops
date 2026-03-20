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

from .client import JiraClient
from .mapper import JiraPayload, build_sync_plan
from .state import JiraState, get_fingerprint, load_state, save_state
from ..common.doc25_parser import Doc25Item, parse_sprint_backlog


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

        # Atualiza fingerprint
        self.state.last_sync_fingerprint = get_fingerprint(self.state)

        print(f"[OK] Usuario: {self.state.authenticated_user.get('display_name')}")
        print(f"[OK] Projeto: {self.state.project_key} ({self.state.project_id})")
        print(f"[OK] Issue Types: {len(self.state.issue_type_map)}")
        print(f"[OK] Statuses: {len(self.state.status_map)}")

        return self.state.to_dict()

    def get_local_items(self, tracking_file: str = "Dev_Tracking_S1.md") -> list[Doc25Item]:
        """Busca itens do tracking local."""
        result = parse_sprint_backlog(tracking_file)
        return result.get("items", [])

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
            self.state
        )

        print(f"[DRY-RUN] Operacoes a executar: {len(plan)}")
        for i, op in enumerate(plan, 1):
            print(f"  {i}. [{op.action.upper()}] {op.issue_key or '(nova)'} - {op.fields.get('summary', 'N/A')[:50] if op.fields else ''}")

        return plan

    def sync(self, plan: list[JiraPayload], dry_run: bool = False) -> list[SyncResult]:
        """
        Executa sincronizacao.
        """
        if dry_run:
            print("[DRY-RUN] Nenhuma alteracao sera feita.")
            return []

        results = []

        for op in plan:
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
                    response = self.client.create_issue(
                        project_key=self.state.project_key,
                        summary=op.fields.get("summary", ""),
                        issue_type=op.fields.get("issuetype", {}).get("name", "Task"),
                        description=op.fields.get("summary", ""),
                        labels=op.fields.get("labels", [])
                    )
                    result.issue_key = response.get("key")
                    result.success = True
                    print(f"[OK] Criada: {result.issue_key}")

                elif op.action == "update":
                    print(f"[UPDATE] {op.issue_key}...")
                    self.client.update_issue(op.issue_key, op.fields)
                    result.success = True
                    print(f"[OK] Atualizada: {op.issue_key}")

                elif op.action == "transition":
                    print(f"[TRANSITION] {op.issue_key} -> {op.transition_id}...")
                    self.client.transition_issue(op.issue_key, op.transition_id)
                    result.success = True
                    print(f"[OK] Transicionada: {op.issue_key}")

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
