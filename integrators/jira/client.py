#!/usr/bin/env python3
"""
jira/client.py - Cliente HTTP Seguro para Jira

Wrapper para chamadas REST API do Jira Cloud.
Credenciais carregadas internamente do .scr/.env.

Uso:
    from integrators.jira import JiraClient
    client = JiraClient()
    user = client.get_myself()
    project = client.get_project("STVIA")
"""

import base64
import json
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


class JiraClientError(Exception):
    """Erro do cliente Jira."""
    pass


class JiraClient:
    """Cliente HTTP para Jira Cloud."""

    BASE_URL = "https://sentivisiaops.atlassian.net"
    API_BASE = "/rest/api/3"

    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or self.BASE_URL
        self._token: str | None = None
        self._email: str | None = None
        self._load_credentials()

    def _load_credentials(self) -> None:
        """Carrega credenciais do .scr/.env sem expor valores."""
        env_path = Path(".scr/.env")
        if not env_path.exists():
            raise JiraClientError("Arquivo .scr/.env nao encontrado")

        content = env_path.read_text(encoding="utf-8")
        token = None
        email = None

        for line in content.splitlines():
            line = line.strip()
            if line.startswith("JIRA_API_TOKEN="):
                token = line.split("=", 1)[1].strip()
            elif line.startswith("JIRA_EMAIL="):
                email = line.split("=", 1)[1].strip()

        if not token or not email:
            raise JiraClientError("Credenciais Jira incompletas em .scr/.env")

        self._token = token
        self._email = email

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: dict | None = None,
        retry: int = 3,
    ) -> dict:
        """Executa requisicao HTTP com retry e tratamento de erros."""
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        auth = base64.b64encode(f"{self._email}:{self._token}".encode()).decode()
        headers["Authorization"] = f"Basic {auth}"

        request = urllib.request.Request(url, headers=headers, method=method)

        if data:
            request.data = json.dumps(data).encode("utf-8")

        last_error = None
        for attempt in range(retry):
            try:
                with urllib.request.urlopen(request, timeout=30) as response:
                    if response.status == 204:
                        return {}
                    return json.load(response)
            except urllib.error.HTTPError as e:
                last_error = e
                if e.code == 429:
                    wait_time = (attempt + 1) * 2
                    print(f"[WARN] Rate limited. Aguardando {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                elif e.code >= 500:
                    wait_time = (attempt + 1) * 3
                    print(f"[WARN] Erro servidor {e.code}. Retry em {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    body = e.read().decode() if e.fp else ""
                    raise JiraClientError(f"HTTP {e.code}: {body}")
            except urllib.error.URLError as e:
                last_error = e
                if attempt < retry - 1:
                    time.sleep(1)
                    continue
                raise JiraClientError(f"Erro de conexao: {e}")

        raise JiraClientError(f"Falha apos {retry} tentativas: {last_error}")

    def get_myself(self) -> dict:
        """GET /rest/api/3/myself - Obtem usuario autenticado."""
        return self._make_request("GET", f"{self.API_BASE}/myself")

    def get_project(self, key: str) -> dict:
        """GET /rest/api/3/project/{key} - Obtem projeto."""
        return self._make_request("GET", f"{self.API_BASE}/project/{key}")

    def get_project_issues(
        self,
        project_key: str,
        max_results: int = 50,
        start_at: int = 0,
    ) -> dict:
        """GET /rest/api/3/search/jql - Busca issues por projeto."""
        jql = f"project = {project_key} ORDER BY created DESC"
        params = f"jql={urllib.parse.quote(jql)}&maxResults={max_results}&startAt={start_at}"
        return self._make_request("GET", f"{self.API_BASE}/search/jql?{params}")

    def get_issue(self, issue_key: str) -> dict:
        """GET /rest/api/3/issue/{key} - Obtem issue especifica."""
        return self._make_request("GET", f"{self.API_BASE}/issue/{issue_key}")

    def create_issue(self, project_key: str, summary: str, issue_type: str, description: str = "", labels: list = None) -> dict:
        """POST /rest/api/3/issue - Cria nova issue."""
        data = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "issuetype": {"name": issue_type},
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {"type": "text", "text": description or summary}
                            ]
                        }
                    ]
                },
            }
        }
        if labels:
            data["fields"]["labels"] = labels
        return self._make_request("POST", f"{self.API_BASE}/issue", data)

    def update_issue(self, issue_key: str, fields: dict) -> dict:
        """PUT /rest/api/3/issue/{key} - Atualiza issue."""
        data = {"fields": fields}
        return self._make_request("PUT", f"{self.API_BASE}/issue/{issue_key}", data)

    def add_comment(self, issue_key: str, comment: str) -> dict:
        """POST /rest/api/3/issue/{key}/comment - Adiciona comentario."""
        data = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": comment}]
                    }
                ]
            }
        }
        return self._make_request("POST", f"{self.API_BASE}/issue/{issue_key}/comment", data)

    def get_transitions(self, issue_key: str) -> dict:
        """GET /rest/api/3/issue/{key}/transitions - Lista transicoes."""
        return self._make_request("GET", f"{self.API_BASE}/issue/{issue_key}/transitions")

    def transition_issue(self, issue_key: str, transition_id: str) -> dict:
        """POST /rest/api/3/issue/{key}/transitions - Transiciona issue."""
        data = {"transition": {"id": transition_id}}
        return self._make_request("POST", f"{self.API_BASE}/issue/{issue_key}/transitions", data)

    def get_issue_types(self) -> dict:
        """GET /rest/api/3/issuetype - Lista tipos de issue."""
        return self._make_request("GET", f"{self.API_BASE}/issuetype")

    def get_statuses(self) -> dict:
        """GET /rest/api/3/status - Lista statuses."""
        return self._make_request("GET", f"{self.API_BASE}/status")


def test_connection() -> bool:
    """Testa conexao com Jira."""
    try:
        client = JiraClient()
        user = client.get_myself()
        print(f"[OK] Conectado como: {user.get('displayName', 'unknown')}")
        return True
    except JiraClientError as e:
        print(f"[ERRO] Falha na conexao: {e}")
        return False


if __name__ == "__main__":
    test_connection()
