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
import urllib.parse
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
        fields: str = "summary,labels,issuetype,status,project",
    ) -> dict:
        """GET /rest/api/3/search/jql - Busca issues por projeto."""
        jql = f"project = {project_key} ORDER BY created DESC"
        params = {
            "jql": jql,
            "maxResults": str(max_results),
            "startAt": str(start_at),
            "fields": fields,
        }
        query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        response = self._make_request("GET", f"{self.API_BASE}/search/jql?{query}")

        issues = list(response.get("issues", []))
        next_page_token = response.get("nextPageToken")
        is_last = response.get("isLast", True)

        while next_page_token and not is_last:
            next_params = {
                "jql": jql,
                "maxResults": str(max_results),
                "startAt": str(start_at),
                "nextPageToken": next_page_token,
                "fields": fields,
            }
            next_query = urllib.parse.urlencode(next_params, quote_via=urllib.parse.quote)
            page = self._make_request("GET", f"{self.API_BASE}/search/jql?{next_query}")
            issues.extend(page.get("issues", []))
            next_page_token = page.get("nextPageToken")
            is_last = page.get("isLast", True)

        response["issues"] = issues
        response["isLast"] = True
        response.pop("nextPageToken", None)
        return response

    def get_issue(self, issue_key: str) -> dict:
        """GET /rest/api/3/issue/{key} - Obtem issue especifica."""
        return self._make_request("GET", f"{self.API_BASE}/issue/{issue_key}")

    def create_issue(self, project_key: str, summary: str, issue_type: str, description: str = "", labels: list = None, extra_fields: dict = None) -> dict:
        """POST /rest/api/3/issue - Cria nova issue.
        
        Args:
            project_key: Chave do projeto Jira
            summary: Titulo da issue
            issue_type: Tipo de issue (Task, Bug, etc)
            description: Descricao da issue
            labels: Lista de labels
            extra_fields: Campos extras a incluir no payload (ex: customfield_10016 para Story Points)
        """
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
        
        # Adiciona campos extras (SP, etc)
        if extra_fields:
            for key, value in extra_fields.items():
                if key not in data["fields"]:
                    data["fields"][key] = value
        
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

    # === Agile API (Jira Software) ===

    def get_boards(self, project_key_or_id: str, max_results: int = 50) -> dict:
        """GET /rest/agile/1.0/board - Lista boards por projeto."""
        params = {
            "projectKeyOrId": project_key_or_id,
            "maxResults": str(max_results),
        }
        query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        return self._make_request("GET", f"/rest/agile/1.0/board?{query}")

    def get_board_configuration(self, board_id: int) -> dict:
        """GET /rest/agile/1.0/board/{boardId}/configuration - Obtem colunas e configuracao do board."""
        return self._make_request("GET", f"/rest/agile/1.0/board/{board_id}/configuration")

    def get_sprints(self, board_id: int, state: str = "active,future,closed", max_results: int = 100) -> dict:
        """GET /rest/agile/1.0/board/{boardId}/sprint - Lista sprints de um board."""
        params = {
            "state": state,
            "maxResults": str(max_results),
        }
        query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        return self._make_request("GET", f"/rest/agile/1.0/board/{board_id}/sprint?{query}")

    def create_sprint(self, name: str, origin_board_id: int, goal: str = "", start_date: str = None, end_date: str = None) -> dict:
        """POST /rest/agile/1.0/sprint - Cria um novo sprint.
        
        Args:
            name: Nome da sprint
            origin_board_id: ID do board onde criar a sprint
            goal: Objetivo da sprint (opcional)
            start_date: Data de inicio no formato ISO8601 (opcional)
            end_date: Data de fim no formato ISO8601 (opcional)
        """
        data = {
            "name": name,
            "originBoardId": origin_board_id,
        }
        if goal:
            data["goal"] = goal
        if start_date:
            data["startDate"] = start_date
        if end_date:
            data["endDate"] = end_date
        return self._make_request("POST", "/rest/agile/1.0/sprint", data)

    def get_sprint_issues(self, sprint_id: int, max_results: int = 100, fields: str = "summary,labels") -> dict:
        """GET /rest/agile/1.0/sprint/{sprintId}/issue - Lista issues de um sprint."""
        params = {
            "maxResults": str(max_results),
            "fields": fields,
        }
        query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        return self._make_request("GET", f"/rest/agile/1.0/sprint/{sprint_id}/issue?{query}")

    def add_issues_to_sprint(self, sprint_id: int, issue_keys: list[str]) -> dict:
        """POST /rest/agile/1.0/sprint/{sprintId}/issue - Adiciona issues ao sprint."""
        # Jira aceita max 50 issues por request
        results = []
        for i in range(0, len(issue_keys), 50):
            chunk = issue_keys[i:i + 50]
            data = {"issues": chunk}
            result = self._make_request("POST", f"/rest/agile/1.0/sprint/{sprint_id}/issue", data)
            results.append(result)
        return {"chunks": len(results), "results": results}

    def get_sprint(self, sprint_id: int) -> dict:
        """GET /rest/agile/1.0/sprint/{sprintId} - Obtem detalhes de um sprint."""
        return self._make_request("GET", f"/rest/agile/1.0/sprint/{sprint_id}")

    def update_sprint(
        self,
        sprint_id: int,
        name: str,
        start_date: str | None = None,
        end_date: str | None = None,
        state: str | None = None,
        goal: str | None = None,
    ) -> dict:
        """PUT /rest/agile/1.0/sprint/{sprintId} - Atualiza sprint (datas, estado, objetivo)."""
        # Jira requer campo 'name' obrigatório
        data = {"name": name}
        if start_date is not None:
            data["startDate"] = start_date
        if end_date is not None:
            data["endDate"] = end_date
        if state is not None:
            data["state"] = state
        if goal is not None:
            data["goal"] = goal
        return self._make_request("PUT", f"/rest/agile/1.0/sprint/{sprint_id}", data)

    def close_sprint(
        self,
        sprint_id: int,
        name: str,
        goal: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> dict:
        """Fecha uma sprint ativa diretamente na API do Jira.

        Este metodo e de baixo nivel e nao aplica gate de negocio.
        O caller deve validar readiness, itens incompletos e decisao do PO
        antes de invoca-lo.

        Jira exige `startDate` e `endDate` no fechamento da sprint.
        """
        if not start_date or not end_date:
            raise JiraClientError(
                "close_sprint requer start_date e end_date; valide a sprint e "
                "recupere as datas atuais antes de fechar."
            )

        data = {
            "name": name,
            "state": "closed",
            "startDate": start_date,
            "endDate": end_date,
        }
        if goal is not None:
            data["goal"] = goal
        return self._make_request("PUT", f"/rest/agile/1.0/sprint/{sprint_id}", data)


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
