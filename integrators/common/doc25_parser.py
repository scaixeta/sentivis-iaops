#!/usr/bin/env python3
"""
integrators/common/doc25_parser.py - Parser do DOC2.5 Tracking

Extrai itens do Dev_Tracking_SX.md para sincronizacao com integradores.

Uso:
    from integrators.common import Doc25Parser, parse_sprint_backlog
    items = parse_sprint_backlog("Dev_Tracking_S1.md")
"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Doc25Item:
    """Item do tracking DOC2.5."""
    id: str          # ex: ST-S1-01
    type: str        # ST, BUG, TEST, CR, D
    status: str      # To-Do, Doing, Done, etc.
    title: str       # titulo/descricao
    sprint: str      # S1, S2, etc.
    raw_line: str    # linha original


def parse_sprint_id(filename: str) -> Optional[str]:
    """Extrai ID da sprint do nome do arquivo."""
    match = re.search(r"Dev_Tracking_S(\d+)\.md", filename)
    return f"S{match.group(1)}" if match else None


def extract_items(content: str, sprint: str) -> list[Doc25Item]:
    """Extrai todos os items do backlog da sprint."""
    items = []

    # Padrao: | Status | Estoria |
    # Exemplo: | To-Do | ST-S1-01 - Levantar campos, issue types... |
    # Aceita tanto - (hifen) quanto – (travessao)
    backlog_pattern = re.compile(
        r"\|\s*(To-Do|Doing|Done|Accepted|Pending-SX)\s*\|\s*([A-Z]+-S\d+-\d+)\s*[-–—]\s*([^\|]+)\s*\|",
        re.IGNORECASE
    )

    for match in backlog_pattern.finditer(content):
        status = match.group(1).strip()
        item_id = match.group(2).strip()  # ID completo como ST-S1-01
        title = match.group(3).strip()
        
        # Extrai tipo do ID (ST, BUG, TEST, CR, D)
        id_type = item_id.split("-")[0].upper()
        # Extrai sprint do ID
        sprint_from_id = item_id.split("-")[1] if len(item_id.split("-")) > 1 else sprint

        items.append(Doc25Item(
            id=item_id,
            type=id_type,
            status=status,
            title=title,
            sprint=sprint_from_id,
            raw_line=match.group(0)
        ))

    return items


def extract_decisions(content: str) -> list[Doc25Item]:
    """Extrai decisoes do tracking."""
    decisions = []

    # Padrao: [D-S1-YY] - descricao
    decision_pattern = re.compile(
        r"\[(D-S\d+-\d+)\]\s*[-–]\s*([^\n]+)",
        re.IGNORECASE
    )

    for match in decision_pattern.finditer(content):
        item_id = match.group(1)
        title = match.group(2).strip()

        sprint_match = re.search(r"S(\d+)", item_id)
        sprint = f"S{sprint_match.group(1)}" if sprint_match else "S1"

        decisions.append(Doc25Item(
            id=item_id,
            type="D",
            status="Logged",
            title=title,
            sprint=sprint,
            raw_line=match.group(0)
        ))

    return decisions


def extract_objectives(content: str) -> list[str]:
    """Extrai objetivos da sprint."""
    objectives = []

    # Procura secao de Objetivos
    obj_pattern = re.compile(
        r"##\s*2\.\s*Objetivos da Sprint.*?(?=##|\Z)",
        re.DOTALL
    )
    obj_section = obj_pattern.search(content)
    if not obj_section:
        return objectives

    # Extrai linhas de objetivo: - [OBJ-...]
    goal_pattern = re.compile(r"\[\s*OBJ-(S\d+-\d+)\s*\]\s*([^\n]+)")
    for match in goal_pattern.finditer(obj_section.group(0)):
        objectives.append(f"[{match.group(1)}] {match.group(2).strip()}")

    return objectives


def parse_sprint_backlog(tracking_file: str | Path) -> dict:
    """
    Parser principal do tracking DOC2.5.

    Retorna:
        {
            "sprint": "S1",
            "items": [Doc25Item, ...],
            "decisions": [Doc25Item, ...],
            "objectives": [str, ...]
        }
    """
    path = Path(tracking_file)
    if not path.exists():
        print(f"[ERRO] Arquivo nao encontrado: {path}")
        return {"sprint": "", "items": [], "decisions": [], "objectives": []}

    content = path.read_text(encoding="utf-8")
    sprint = parse_sprint_id(path.name)

    items = extract_items(content, sprint or "S1")
    decisions = extract_decisions(content)
    objectives = extract_objectives(content)

    return {
        "sprint": sprint or "S1",
        "items": items,
        "decisions": decisions,
        "objectives": objectives,
    }


def get_item_type_mapping() -> dict:
    """Retorna mapeamento padrao de tipo DOC2.5 para tipo Jira."""
    return {
        "ST": "Task",
        "BUG": "Bug",
        "TEST": "Task",
        "CR": "Task",
        "D": "Task",  # Decisoes viram comentarios ou tasks
    }


def get_status_mapping() -> dict:
    """Retorna mapeamento padrao de status DOC2.5 para Jira."""
    return {
        "To-Do": "To Do",
        "Doing": "In Progress",
        "Done": "Done",
        "Accepted": "Done",
        "Pending-SX": "To Do",
    }


if __name__ == "__main__":
    # Teste rapido
    import sys
    if len(sys.argv) > 1:
        result = parse_sprint_backlog(sys.argv[1])
        print(f"Sprint: {result['sprint']}")
        print(f"Itens: {len(result['items'])}")
        print(f"Decisoes: {len(result['decisions'])}")
        for item in result['items'][:5]:
            print(f"  - {item.id}: {item.status} | {item.title[:50]}")
