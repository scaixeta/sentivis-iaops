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
        r"\|\s*(To-Do|Doing|Done|Accepted|Pending-S(?:\d+|X))\s*\|\s*([A-Z]+-S\d+-\d+)\s*[-–—]\s*([^\|]+)\s*\|",
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


@dataclass
class Doc25Timestamp:
    """Timestamp de um item no tracking DOC2.5."""
    item_id: str
    start: Optional[str]  # YYYY-MM-DDTHH:MM:SS-ST
    finish: Optional[str]  # YYYY-MM-DDTHH:MM:SS-FN ou "-"
    status: str


def extract_timestamps(content: str) -> list[Doc25Timestamp]:
    """Extrai timestamps da secao ## 6. Timestamp UTC."""
    timestamps = []

    # Procura secao de Timestamp UTC
    ts_pattern = re.compile(
        r"##\s*6\.\s*Timestamp UTC.*?(?=##|\Z)",
        re.DOTALL
    )
    ts_section = ts_pattern.search(content)
    if not ts_section:
        return timestamps

    # Processa linha por linha usando split("|")
    for line in ts_section.group(0).split("\n"):
        line = line.strip()
        # Pula linhas vazias, header ou separadores
        if not line or line.startswith("Event") or "---" in line:
            continue
        
        # Parse: ST-S0-01 | 2026-03-11T02:15:56-ST | 2026-03-11T02:15:56-FN | Done
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 4:
            continue
        
        item_id = parts[0]
        # Valida se e um ID valido
        if not re.match(r"^[A-Z]+-S\d+-\d+$", item_id):
            continue
        
        start = parts[1] if parts[1] not in ("", "-") else None
        finish = parts[2] if parts[2] not in ("", "-") else None
        status = parts[3]

        timestamps.append(Doc25Timestamp(
            item_id=item_id,
            start=start,
            finish=finish,
            status=status
        ))

    return timestamps


def timestamp_to_date(ts: Optional[str]) -> Optional[str]:
    """Converte timestamp DOC2.5 para data ISO (YYYY-MM-DD).
    
    Formato entrada: YYYY-MM-DDTHH:MM:SS-ST ou YYYY-MM-DDTHH:MM:SS-FN
    Formato saida: YYYY-MM-DD
    """
    if not ts:
        return None
    # Extrai apenas a parte da data
    match = re.match(r"(\d{4}-\d{2}-\d{2})", ts)
    if match:
        return match.group(1)
    return None


def parse_sprint_backlog(tracking_file: str | Path) -> dict:
    """
    Parser principal do tracking DOC2.5.

    Retorna:
        {
            "sprint": "S1",
            "items": [Doc25Item, ...],
            "decisions": [Doc25Item, ...],
            "objectives": [str, ...],
            "timestamps": [Doc25Timestamp, ...]
        }
    """
    path = Path(tracking_file)
    if not path.exists():
        print(f"[ERRO] Arquivo nao encontrado: {path}")
        return {"sprint": "", "items": [], "decisions": [], "objectives": [], "timestamps": []}

    content = path.read_text(encoding="utf-8")
    sprint = parse_sprint_id(path.name)

    items = extract_items(content, sprint or "S1")
    decisions = extract_decisions(content)
    objectives = extract_objectives(content)
    timestamps = extract_timestamps(content)

    return {
        "sprint": sprint or "S1",
        "items": items,
        "decisions": decisions,
        "objectives": objectives,
        "timestamps": timestamps,
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
