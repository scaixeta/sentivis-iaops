#!/usr/bin/env python3
"""
jira/mapper.py - Mapeamento DOC2.5 -> Jira

Converte itens do tracking local em payloads Jira.

Uso:
    from integrators.jira import create_create_payload
    payload = create_create_payload(item, project_key, state)
"""

from dataclasses import dataclass
from typing import Any

from ..common.doc25_parser import Doc25Item
from .state import JiraState


@dataclass
class JiraPayload:
    """Payload para operacao Jira."""
    action: str          # create, update, transition, comment
    issue_key: str | None
    fields: dict | None
    transition_id: str | None
    comment: str | None
    labels: list


# Nota: O Jira Cloud pode ter Sprint nativo (via Jira Software).
# Este integrator usa LABELS como fallback quando Sprint nativo nao esta disponivel.
# Labels usadas:
#   - sprint_s0, sprint_s1, sprint_s2: indicativo de sprint via label
#   - tracking_<ID>: rastreabilidade unica do item DOC2.5
#   - type_<TYPE>: tipo do item (ST, BUG, CR, etc)
# Se o projeto STVIA tiver board/sprint nativo, isso deve ser verificado via discover.

def build_labels(item: Doc25Item, state: JiraState) -> list[str]:
    """Constrói labels para issue Jira."""
    labels = list(state.labels_base)

    # Label de sprint (LABEL FALLBACK - nao e campo Sprint nativo)
    labels.append(f"sprint_{item.sprint.lower()}")

    # Label de tracking (identificador unico)
    labels.append(f"tracking_{item.id}")

    # Label de tipo
    labels.append(f"type_{item.type.lower()}")

    return labels


def build_description(item: Doc25Item, include_marker: bool = True) -> dict:
    """
    Constrói description em formato Atlassian Document Format (ADF).
    """
    content = []

    if include_marker:
        content.append({
            "type": "paragraph",
            "content": [{"type": "text", "text": f"DOC25_ID: {item.id}"}]
        })

    content.append({
        "type": "paragraph",
        "content": [{"type": "text", "text": item.title}]
    })

    # Adicionar contexto da sprint
    content.append({
        "type": "paragraph",
        "content": [{"type": "text", "text": f"Sprint: {item.sprint} | Status: {item.status}"}]
    })

    return {
        "type": "doc",
        "version": 1,
        "content": content
    }


def map_item_type(doc25_type: str, state: JiraState) -> str:
    """Mapeia tipo DOC2.5 para tipo Jira."""
    # Mapeamento por nome (em portugues do Jira)
    name_map = {
        "ST": "Tarefa",
        "BUG": "Bug",
        "TEST": "Tarefa",
        "CR": "Tarefa",
        "D": "Tarefa",
    }
    
    # Primeiro verifica se tem mapeamento customizado no estado
    target_name = name_map.get(doc25_type, "Tarefa")
    if target_name in state.issue_type_map:
        return target_name

    # Fallback para mapeamento padrao
    return name_map.get(doc25_type, "Tarefa")


def map_status(doc25_status: str, state: JiraState) -> str:
    """Mapeia status DOC2.5 para status Jira."""
    # Mapeamento por nome (em portugues do Jira)
    name_map = {
        "To-Do": "Tarefas pendentes",
        "Doing": "Em andamento",
        "Done": "Concluído",
        "Accepted": "Concluído",
        "Pending-SX": "Tarefas pendentes",
    }
    
    # Primeiro verifica se tem mapeamento customizado no estado
    target_name = name_map.get(doc25_status, "Tarefas pendentes")
    if target_name in state.status_map:
        return target_name

    # Fallback para mapeamento padrao
    return name_map.get(doc25_status, "Tarefas pendentes")


def create_create_payload(item: Doc25Item, project_key: str, state: JiraState) -> dict:
    """
    Cria payload para criacao de issue.
    """
    issue_type = map_item_type(item.type, state)
    labels = build_labels(item, state)
    description = build_description(item)

    fields = {
        "project": {"key": project_key},
        "summary": f"[{item.id}] {item.title}",
        "issuetype": {"name": issue_type},
        "description": description,
        "labels": labels,
    }

    # Adiciona Story Points se presente
    if item.sp is not None:
        fields[STORY_POINTS_FIELD] = item.sp

    return {"fields": fields}


def create_update_payload(item: Doc25Item, current_issue: dict, state: JiraState) -> dict | None:
    """
    Cria payload para atualizacao de issue.
    Retorna None se nao houver mudanca.
    """
    changes = {}

    # Verifica summary
    expected_summary = f"[{item.id}] {item.title}"
    current_summary = current_issue.get("fields", {}).get("summary", "")
    if expected_summary != current_summary:
        changes["summary"] = expected_summary

    # Verifica labels
    expected_labels = build_labels(item, state)
    current_labels = current_issue.get("fields", {}).get("labels", [])
    if set(expected_labels) != set(current_labels):
        changes["labels"] = expected_labels

    # Verifica Story Points
    current_sp = current_issue.get("fields", {}).get(STORY_POINTS_FIELD)
    if item.sp is not None and current_sp != item.sp:
        changes[STORY_POINTS_FIELD] = item.sp

    if not changes:
        return None

    return {"fields": changes}


def create_comment_payload(comment: str) -> dict:
    """Cria payload para comentario."""
    return {
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


def find_transition_id(current_status: str, target_status: str, transitions: list[dict], state: JiraState) -> str | None:
    """
    Encontra ID de transicao para mover issue de current_status para target_status.
    """
    # Primeiro tenta usando o mapeamento local
    status_key = f"{current_status}->{target_status}"
    if status_key in state.transitions_map:
        return state.transitions_map[status_key]

    # Fallback: procura transicao no Jira
    for transition in transitions:
        to_status = transition.get("to", {}).get("name", "")
        if to_status.lower() == target_status.lower():
            return transition.get("id")

    return None


# Campo Story Points no Jira
STORY_POINTS_FIELD = "customfield_10016"


def build_sync_plan(
    local_items: list[Doc25Item],
    jira_issues: list[dict],
    project_key: str,
    state: JiraState
) -> list[JiraPayload]:
    """
    Constrói plano de sincronizacao entre tracking local e Jira.

    Retorna lista de operacoes a serem executadas.
    """
    plan = []

    # Indexa issues Jira por label de tracking
    jira_by_tracking = {}
    # Indexa issues Jira por chave (STVIA-123)
    jira_by_key = {}
    for issue in jira_issues:
        key = issue.get("key")
        if key:
            jira_by_key[key.upper()] = issue
        labels = issue.get("fields", {}).get("labels", [])
        for label in labels:
            if label.startswith("tracking_"):
                jira_by_tracking[label.replace("tracking_", "")] = issue

    # Processa cada item local
    for item in local_items:
        # PRIORIDADE 1: Se item.jira existe, usa como chave direta
        resolved_key = None
        if item.jira:
            resolved_key = item.jira.upper()
            if resolved_key in jira_by_key:
                jira_issue = jira_by_key[resolved_key]
            else:
                # Jira key fornecido mas issue nao existe no Jira
                # Marca para criar (ou erro?)
                jira_issue = None
        # PRIORIDADE 2: Busca por tracking label
        elif item.id in jira_by_tracking:
            jira_issue = jira_by_tracking[item.id]
            resolved_key = jira_issue.get("key")
        else:
            jira_issue = None

        if jira_issue:
            # Issue ja existe - verifica se precisa update (SP ou outros campos)
            update_payload = create_update_payload(item, jira_issue, state)

            if update_payload:
                plan.append(JiraPayload(
                    action="update",
                    issue_key=resolved_key,
                    fields=update_payload.get("fields"),
                    transition_id=None,
                    comment=None,
                    labels=build_labels(item, state)
                ))
            else:
                # Issue existe mas sem mudancas - ainda assim adiciona ao plano
                # para fins de write-back (precisamos saber qual key resolver)
                plan.append(JiraPayload(
                    action="none",
                    issue_key=resolved_key,
                    fields=None,
                    transition_id=None,
                    comment=None,
                    labels=build_labels(item, state)
                ))
        else:
            # Issue nao existe - cria
            plan.append(JiraPayload(
                action="create",
                issue_key=None,
                fields=create_create_payload(item, project_key, state).get("fields"),
                transition_id=None,
                comment=None,
                labels=build_labels(item, state)
            ))

    return plan


class JiraMapper:
    """Classe utilitaria para mapeamento Jira."""
    
    def __init__(self, state: JiraState):
        self.state = state
    
    def map_item(self, item: Doc25Item, project_key: str) -> dict:
        """Mapeia item DOC2.5 para payload Jira."""
        return create_create_payload(item, project_key, self.state)
