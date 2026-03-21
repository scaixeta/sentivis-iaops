#!/usr/bin/env python3
"""
jira/state.py - Persistência de Estado Observado do Jira

Contrato formal para estado observado da integração Jira.
Arquivo: .scr/mgmt_layer.jira.json

Uso:
    from integrators.jira import JiraState, load_state, save_state
    state = load_state()
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCR_DIR = Path(".scr")
STATE_FILE = SCR_DIR / "mgmt_layer.jira.json"
SCHEMA_VERSION = "1.2.0"


class JiraState:
    """Estado observado da integração Jira."""

    def __init__(self):
        self.connector: str = "jira"
        self.observed_at: str = ""
        self.authenticated_user: dict = {}
        self.project_key: str = ""
        self.project_id: str = ""
        self.project_type: str = ""
        self.boards: list[dict] = []
        self.board_id: int | None = None
        self.board_name: str = ""
        self.board_type: str = ""
        self.board_columns: list[dict] = []  # [{name: str, status_ids: [str], status_names: [str]}]
        self.local_status_guidance: list[dict] = []
        self.issue_type_map: dict = {}
        self.status_map: dict = {}
        self.transitions_map: dict = {}
        self.last_sync_fingerprint: str = ""
        self.schema_version: str = SCHEMA_VERSION
        self.labels_base: list = ["doc25", "sentivis"]

    def to_dict(self) -> dict:
        return {
            "connector": self.connector,
            "observed_at": self.observed_at,
            "authenticated_user": self.authenticated_user,
            "project_key": self.project_key,
            "project_id": self.project_id,
            "project_type": self.project_type,
            "boards": self.boards,
            "board_id": self.board_id,
            "board_name": self.board_name,
            "board_type": self.board_type,
            "board_columns": self.board_columns,
            "local_status_guidance": self.local_status_guidance,
            "issue_type_map": self.issue_type_map,
            "status_map": self.status_map,
            "transitions_map": self.transitions_map,
            "last_sync_fingerprint": self.last_sync_fingerprint,
            "schema_version": self.schema_version,
            "labels_base": self.labels_base,
        }

    @staticmethod
    def from_dict(data: dict) -> "JiraState":
        state = JiraState()
        state.connector = data.get("connector", "jira")
        state.observed_at = data.get("observed_at", "")
        state.authenticated_user = data.get("authenticated_user", {})
        state.project_key = data.get("project_key", "")
        state.project_id = data.get("project_id", "")
        state.project_type = data.get("project_type", "")
        state.boards = data.get("boards", []) or []
        state.board_id = data.get("board_id", None)
        state.board_name = data.get("board_name", "")
        state.board_type = data.get("board_type", "")
        state.board_columns = data.get("board_columns", []) or []
        state.local_status_guidance = data.get("local_status_guidance", []) or []
        state.issue_type_map = data.get("issue_type_map", {})
        state.status_map = data.get("status_map", {})
        state.transitions_map = data.get("transitions_map", {})
        state.last_sync_fingerprint = data.get("last_sync_fingerprint", "")
        state.schema_version = data.get("schema_version", SCHEMA_VERSION)
        state.labels_base = data.get("labels_base", ["doc25", "sentivis"])
        return state


def load_state() -> JiraState | None:
    """Carrega estado observado do arquivo local."""
    if not STATE_FILE.exists():
        return None
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        return JiraState.from_dict(data)
    except (json.JSONDecodeError, KeyError) as e:
        print(f"[WARN] Estado corrompido: {e}")
        return None


def save_state(state: JiraState, dry_run: bool = False) -> bool:
    """Salva estado observado no arquivo local."""
    state.observed_at = datetime.now(timezone.utc).isoformat()

    if dry_run:
        print("[DRY-RUN] Estado que seria escrito:")
        print(json.dumps(state.to_dict(), indent=2, ensure_ascii=False))
        return True

    SCR_DIR.mkdir(exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(state.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"[OK] Estado salvo em: {STATE_FILE}")
    return True


def validate_state(state: JiraState) -> list[str]:
    """Valida estado e retorna lista de problemas."""
    issues = []

    if not state.authenticated_user:
        issues.append("authenticated_user vazio")
    if not state.project_key:
        issues.append("project_key vazio")
    if not state.project_id:
        issues.append("project_id vazio")
    if not state.observed_at:
        issues.append("observed_at vazio")

    return issues


def get_fingerprint(state: JiraState) -> str:
    """Gera fingerprint do estado para detecção de mudanças."""
    import hashlib
    data = json.dumps({
        "project_key": state.project_key,
        "project_id": state.project_id,
        "issue_type_map": state.issue_type_map,
        "status_map": state.status_map,
        "board_id": state.board_id,
        "board_columns": state.board_columns,
        "local_status_guidance": state.local_status_guidance,
    }, sort_keys=True)
    return hashlib.sha256(data.encode()).hexdigest()[:16]
