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
    action: str          # create, update, transition, align_status, comment
    issue_key: str | None
    fields: dict | None
    transition_id: str | None
    comment: str | None
    labels: list


# Labels canonicas do integrador:
#   - tracking_<ID>: rastreabilidade unica do item DOC2.5
#   - estoria | bug | change_request: tipos operacionais da Cindy no Jira
# Decisoes (D-*) permanecem apenas no source of truth local.


def _type_label(item_type: str) -> str:
    mapping = {
        "ST": "estoria",
        "BUG": "bug",
        "CR": "change_request",
    }
    return mapping.get((item_type or "").upper(), "estoria")

def build_labels(item: Doc25Item, state: JiraState) -> list[str]:
    """Constrói labels para issue Jira."""
    labels = list(state.labels_base)

    # Label de tracking (identificador unico)
    labels.append(f"tracking_{item.tracking_key}")

    # Label de tipo no contrato Cindy
    labels.append(_type_label(item.type))

    return labels


def build_description(item: Doc25Item, include_marker: bool = True) -> dict:
    """
    Constrói description em formato Atlassian Document Format (ADF).
    """
    content = []

    if include_marker:
        content.append({
            "type": "paragraph",
            "content": [{"type": "text", "text": f"DOC25_ID: {item.tracking_key}"}]
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
    # Mapeamento por nome aceito no projeto Jira atual.
    # O contrato Cindy continua expresso pelos labels (`estoria`, `bug`,
    # `change_request`), enquanto o issuetype precisa ser um dos tipos
    # realmente disponiveis no projeto STVIA.
    name_map = {
        "ST": "História",
        "BUG": "Tarefa",
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
    if doc25_status in (state.status_map or {}):
        return doc25_status

    in_progress_name = _prefer_known_status_name("Em Progresso", state, "Em progresso")
    pending_name = _prefer_known_status_name("Pendentes", state)
    testing_name = _prefer_known_status_name("Em Testes", state)
    done_name = _prefer_known_status_name("Feito", state)
    blocked_name = _prefer_known_status_name("Bloqueado", state)
    backlog_name = _prefer_known_status_name("Backlog", state)

    # Mapeamento por nome (em portugues do Jira)
    name_map = {
        "To-Do": pending_name,
        "Doing": in_progress_name,
        "Done": done_name,
        "Accepted": done_name,
        "Pending-SX": pending_name,
        "Pendentes": pending_name,
        "Em progresso": in_progress_name,
        "Em Progresso": in_progress_name,
        "Em Testes": testing_name,
        "Feito": done_name,
        "Bloqueado": blocked_name,
        "Backlog": backlog_name,
    }

    target_name = name_map.get(doc25_status, pending_name)
    if target_name in (state.status_map or {}):
        return target_name

    return target_name


def create_create_payload(item: Doc25Item, project_key: str, state: JiraState) -> dict:
    """
    Cria payload para criacao de issue.
    """
    issue_type = map_item_type(item.type, state)
    labels = build_labels(item, state)
    description = build_description(item)

    fields = {
        "project": {"key": project_key},
        "summary": f"[{item.tracking_key}] {item.title}",
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
    expected_summary = f"[{item.tracking_key}] {item.title}"
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


def _board_status_sequence(state: JiraState) -> list[str]:
    """Retorna a sequencia linear de statuses conforme o board."""
    ordered: list[str] = []
    for column in state.board_columns or []:
        for status_name in column.get("status_names", []) or []:
            if status_name and status_name not in ordered:
                ordered.append(status_name)
    return ordered


def _normalize_status_name(value: str) -> str:
    return (value or "").strip().lower()


def _prefer_known_status_name(preferred: str, state: JiraState, *aliases: str) -> str:
    candidates = (preferred, *aliases)
    status_map = state.status_map or {}

    for candidate in candidates:
        if candidate in status_map:
            return candidate

    for candidate in candidates:
        normalized = _normalize_status_name(candidate)
        for known in status_map.keys():
            if _normalize_status_name(known) == normalized:
                return known

    return preferred


def _reachable_statuses_from(
    start_status: str,
    transitions_provider,
    max_depth: int = 10,
) -> set[str]:
    """Explora statuses alcancaveis a partir de um status via transitions_provider."""
    visited = {start_status}
    frontier = [start_status]

    for _ in range(max_depth):
        if not frontier:
            break
        next_frontier: list[str] = []
        for status_name in frontier:
            try:
                transitions = transitions_provider(status_name) or []
            except Exception:
                transitions = []
            for transition in transitions:
                to_status = transition.get("to", {}).get("name", "")
                if to_status and to_status not in visited:
                    visited.add(to_status)
                    next_frontier.append(to_status)
        frontier = next_frontier

    return visited


def _effective_target_status(
    current_status: str,
    target_status: str,
    transitions: list[dict],
    state: JiraState,
) -> tuple[str, str | None]:
    """
    Resolve o alvo operacional efetivo.

    Regra de negocio:
    - quando o local pede `Pendentes`, mas o workflow do Jira nao permite
      voltar ate essa coluna a partir do estado atual, usamos `Em progresso`
      como menor estado retornavel.
    """
    if not current_status or not target_status:
        return target_status, None

    transitions_by_from = {current_status: transitions}
    ordered_statuses = _board_status_sequence(state)

    def transitions_provider(status_name: str) -> list[dict]:
        return transitions_by_from.get(status_name, [])

    reachable = _reachable_statuses_from(current_status, transitions_provider, max_depth=1)

    if target_status in reachable:
        return target_status, None

    if _normalize_status_name(target_status) == _normalize_status_name("Pendentes"):
        in_progress_name = _prefer_known_status_name("Em Progresso", state, "Em progresso")
        for reachable_status in reachable:
            if _normalize_status_name(reachable_status) == _normalize_status_name(in_progress_name):
                return reachable_status, "workflow_jira_sem_retorno_para_pendentes"

    # Para o planner, usamos a melhor aproximacao pela ordem do board.
    status_to_index = {name: idx for idx, name in enumerate(ordered_statuses)}
    current_idx = status_to_index.get(current_status)
    target_idx = status_to_index.get(target_status)
    if current_idx is not None and target_idx is not None:
        candidates = []
        for transition in transitions:
            to_status = transition.get("to", {}).get("name", "")
            if not to_status or to_status == current_status:
                continue
            to_idx = status_to_index.get(to_status)
            if to_idx is None:
                continue
            candidates.append((abs(target_idx - to_idx), to_status))
        if candidates:
            candidates.sort(key=lambda item: item[0])
            return candidates[0][1], "workflow_jira_sem_alvo_exato"

    return target_status, None


def plan_natural_transition_step(
    current_status: str,
    target_status: str,
    transitions: list[dict],
    state: JiraState,
) -> tuple[str | None, str | None]:
    """
    Planeja o proximo passo de transicao respeitando a ordem natural do board.

    Retorna (transition_id, next_status).
    """
    if not current_status or not target_status or current_status.lower() == target_status.lower():
        return None, None

    # Se a transicao direta existe e o alvo e' adjacente no board, usa direto.
    ordered_statuses = _board_status_sequence(state)
    status_to_index = {name: idx for idx, name in enumerate(ordered_statuses)}
    current_idx = status_to_index.get(current_status)
    target_idx = status_to_index.get(target_status)

    transitions_by_status = {}
    for transition in transitions:
        to_status = transition.get("to", {}).get("name", "")
        if to_status and to_status.lower() != current_status.lower():
            transitions_by_status[to_status] = transition.get("id")

    # Target direto sempre e' aceito se for o vizinho imediato na direcao correta.
    if current_idx is not None and target_idx is not None and current_idx != target_idx:
        step = 1 if target_idx > current_idx else -1
        next_idx = current_idx + step
        if 0 <= next_idx < len(ordered_statuses):
            next_status = ordered_statuses[next_idx]
            transition_id = transitions_by_status.get(next_status)
            if transition_id:
                return transition_id, next_status

    # Fallback 1: se existir transicao direta para o target, usa.
    direct_id = transitions_by_status.get(target_status)
    if direct_id:
        return direct_id, target_status

    # Fallback 2: escolhe a transicao disponivel que mais aproxima o item do target.
    if current_idx is not None and target_idx is not None:
        best_status = None
        best_distance = None
        for to_status, transition_id in transitions_by_status.items():
            to_idx = status_to_index.get(to_status)
            if to_idx is None:
                continue
            distance = abs(target_idx - to_idx)
            if best_distance is None or distance < best_distance:
                best_distance = distance
                best_status = to_status
        if best_status:
            return transitions_by_status.get(best_status), best_status

    return None, None


# Campo Story Points no Jira
STORY_POINTS_FIELD = "customfield_10016"


def build_sync_plan(
    local_items: list[Doc25Item],
    jira_issues: list[dict],
    project_key: str,
    state: JiraState,
    client=None,
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
        elif item.tracking_key in jira_by_tracking:
            jira_issue = jira_by_tracking[item.tracking_key]
            resolved_key = jira_issue.get("key")
        else:
            jira_issue = None

        if jira_issue:
            # Issue ja existe - verifica se precisa update (SP ou outros campos)
            update_payload = create_update_payload(item, jira_issue, state)
            current_status = jira_issue.get("fields", {}).get("status", {}).get("name", "")
            target_status = map_status(item.status, state)

            if update_payload:
                plan.append(JiraPayload(
                    action="update",
                    issue_key=resolved_key,
                    fields=update_payload.get("fields"),
                    transition_id=None,
                    comment=None,
                    labels=build_labels(item, state)
                ))

            transition_id = None
            next_status = None
            effective_target_status = target_status
            status_strategy = None
            if current_status and target_status and current_status.lower() != target_status.lower() and client is not None:
                try:
                    transitions_resp = client.get_transitions(resolved_key)
                    transitions = transitions_resp.get("transitions", [])
                    effective_target_status, status_strategy = _effective_target_status(
                        current_status,
                        target_status,
                        transitions,
                        state,
                    )
                    transition_id, next_status = plan_natural_transition_step(
                        current_status,
                        effective_target_status,
                        transitions,
                        state,
                    )
                except Exception:
                    transition_id = None
                    next_status = None

            if effective_target_status and current_status.lower() == effective_target_status.lower():
                if not update_payload:
                    plan.append(JiraPayload(
                        action="none",
                        issue_key=resolved_key,
                        fields=None,
                        transition_id=None,
                        comment=None,
                        labels=build_labels(item, state)
                    ))
            elif transition_id:
                plan.append(JiraPayload(
                    action="align_status",
                    issue_key=resolved_key,
                    fields={
                        "current_status": current_status,
                        "target_status": target_status,
                        "effective_target_status": effective_target_status,
                        "next_status": next_status,
                        "status_strategy": status_strategy,
                        "summary": f"[{item.tracking_key}] {item.title}",
                    },
                    transition_id=transition_id,
                    comment=None,
                    labels=build_labels(item, state)
                ))
            elif current_status and target_status and current_status.lower() != target_status.lower():
                plan.append(JiraPayload(
                    action="status_mismatch",
                    issue_key=resolved_key,
                    fields={
                        "current_status": current_status,
                        "target_status": target_status,
                        "effective_target_status": effective_target_status,
                        "status_strategy": status_strategy,
                        "summary": f"[{item.tracking_key}] {item.title}",
                    },
                    transition_id=None,
                    comment=None,
                    labels=build_labels(item, state)
                ))
            elif not update_payload:
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
