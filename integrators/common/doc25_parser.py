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
    id: str          # identificador lido na historia; pode ser Jira key no modelo novo
    type: str        # ST, BUG, TEST, CR, D
    status: str      # To-Do, Doing, Done, etc.
    title: str       # titulo/descricao
    sprint: str      # S1, S2, etc.
    raw_line: str    # linha original
    sp: Optional[int] = None      # Story Points (Fibonacci) - opcional
    jira: Optional[str] = None    # Chave da issue no Jira (ex: STVIA-123) - opcional
    tracking_id: Optional[str] = None  # identificador local legado (ST-Sx-yy / CR-Sx-yy / BUG-Sx-yy)

    @property
    def primary_id(self) -> str:
        """Identificador principal do item para exibicao local."""
        return self.jira or self.id

    @property
    def tracking_key(self) -> str:
        """Chave de rastreabilidade estavel usada internamente no integrador."""
        return self.tracking_id or self.id


def parse_sprint_id(filename: str) -> Optional[str]:
    """Extrai ID da sprint do nome do arquivo."""
    match = re.search(r"Dev_Tracking_S(\d+)\.md", filename)
    return f"S{match.group(1)}" if match else None


def extract_items(content: str, sprint: str) -> list[Doc25Item]:
    """Extrai todos os items do backlog da sprint."""
    items = []

    def is_allowed_status(value: str) -> bool:
        v = (value or "").strip()
        if not v:
            return False
        if re.fullmatch(r"Pending-S(\d+|X)", v, flags=re.IGNORECASE):
            return True
        return v.lower() in {
            "to-do",
            "doing",
            "done",
            "accepted",
            "pendentes",
            "em progresso",
            "em testes",
            "feito",
            "bloqueado",
            "backlog",
        }

    lines = content.splitlines()

    # Encontrar a primeira tabela de backlog (header: | Status | ... | Estoria |)
    header = None
    header_idx = None
    for i, line in enumerate(lines):
        if re.match(r"^\|\s*Status\s*\|", line, flags=re.IGNORECASE) and re.search(r"Est", line, flags=re.IGNORECASE):
            header = [c.strip().lower() for c in line.strip().strip("|").split("|")]
            header_idx = i
            break

    if header is None or header_idx is None:
        return items

    def idx_of(pred) -> Optional[int]:
        for j, name in enumerate(header or []):
            if pred(name):
                return j
        return None

    status_idx = idx_of(lambda n: n == "status") or 0
    sp_idx = idx_of(lambda n: n == "sp")
    jira_idx = idx_of(lambda n: n == "jira")
    story_idx = idx_of(lambda n: n.startswith("est"))  # Estoria/Estória
    if story_idx is None:
        story_idx = len(header) - 1

    # Linhas da tabela: pula header + separador
    for line in lines[header_idx + 2:]:
        if not line.strip().startswith("|"):
            break
        if "---" in line:
            continue

        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) <= max(status_idx, story_idx):
            continue

        status = cols[status_idx].strip()
        if not is_allowed_status(status):
            continue

        sp_val = None
        if sp_idx is not None and sp_idx < len(cols):
            sp_raw = cols[sp_idx].strip()
            if sp_raw.isdigit():
                sp_val = int(sp_raw)

        jira_key = None
        if jira_idx is not None and jira_idx < len(cols):
            jira_raw = cols[jira_idx].strip()
            if jira_raw:
                jira_key = jira_raw

        story_cell = cols[story_idx].strip()

        tracking_id = None

        # Modelo legado: ST-S1-01 - Titulo
        story_match = re.match(r"^([A-Z]+-S\d+-\d+)\s*[-–—]\s*(.+)$", story_cell)
        if story_match:
            tracking_id = story_match.group(1).strip()
            item_id = jira_key or tracking_id
            title = story_match.group(2).strip()
        else:
            id_match = re.match(r"^([A-Z]+-S\d+-\d+)\s*(.*)$", story_cell)
            if id_match:
                tracking_id = id_match.group(1).strip()
                item_id = jira_key or tracking_id
                title = id_match.group(2).lstrip(" -–—").strip()
            else:
                # Modelo novo/transicional: story cell com Jira key
                jira_story_match = re.match(r"^([A-Z][A-Z0-9]+-\d+)\s*[-–—]\s*(.+)$", story_cell)
                if jira_story_match:
                    item_id = jira_story_match.group(1).strip().upper()
                    title = jira_story_match.group(2).strip()
                else:
                    jira_id_match = re.match(r"^([A-Z][A-Z0-9]+-\d+)\s*(.*)$", story_cell)
                    if not jira_id_match:
                        continue
                    item_id = jira_id_match.group(1).strip().upper()
                    title = jira_id_match.group(2).lstrip(" -–—").strip()
                if not jira_key:
                    jira_key = item_id

        type_source = tracking_id or item_id
        id_type = type_source.split("-")[0].upper()
        if id_type.startswith("STVIA") or re.fullmatch(r"[A-Z][A-Z0-9]+", id_type):
            # Se a linha usar apenas Jira key, preserva compatibilidade operacional
            # assumindo Estoria como tipo padrao ate que exista coluna de tipo no tracking.
            id_type = "ST"
        sprint_from_id = tracking_id.split("-")[1] if tracking_id and len(tracking_id.split("-")) > 1 else sprint

        items.append(Doc25Item(
            id=item_id,
            type=id_type,
            status=status,
            title=title,
            sprint=sprint_from_id,
            raw_line=line,
            sp=sp_val,
            jira=jira_key,
            tracking_id=tracking_id,
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


def _map_bug_state_to_doc25_status(value: str) -> str:
    raw = (value or "").strip().lower()
    if raw in {"corrigido", "closed", "fechado", "resolvido", "resolved"}:
        return "Done"
    if raw in {"em testes", "in test", "in tests", "testing", "teste", "test"}:
        return "Em Testes"
    if raw in {"em andamento", "doing", "in progress"}:
        return "Doing"
    return "To-Do"


def extract_bugs_from_log(content: str, sprint: str) -> list[Doc25Item]:
    """Extrai bugs da sprint a partir do bugs_log."""
    items: list[Doc25Item] = []

    sprint_section_pattern = re.compile(
        rf"##\s*\d+\.\s*Sprint\s+{re.escape(sprint)}\s*(.*?)(?=\n##\s*\d+\.\s*Sprint\s+S\d+|\Z)",
        re.IGNORECASE | re.DOTALL,
    )
    sprint_section = sprint_section_pattern.search(content)
    if not sprint_section:
        return items

    bug_section_pattern = re.compile(
        r"###\s*4\.\s*Bugs Registrados\s*(.*?)(?=\n###\s*5\.\s*Testes Registrados|\Z)",
        re.IGNORECASE | re.DOTALL,
    )
    bug_section = bug_section_pattern.search(sprint_section.group(1))
    if not bug_section:
        return items

    entry_pattern = re.compile(
        r"-\s*`(BUG-S\d+-\d+)`\s*[–-]\s*(.+?)(?=\n-\s*`BUG-S\d+-\d+`|\Z)",
        re.IGNORECASE | re.DOTALL,
    )

    for match in entry_pattern.finditer(bug_section.group(1)):
        item_id = match.group(1).strip().upper()
        body = match.group(2).strip()
        lines = [line.strip() for line in body.splitlines() if line.strip()]
        if not lines:
            continue

        title = lines[0].strip()
        state_text = ""
        jira_key = None

        for line in lines[1:]:
            normalized = line.lstrip("-").strip()
            lower = normalized.lower()
            if lower.startswith("estado:"):
                state_text = normalized.split(":", 1)[1].strip()
            if "stv" in normalized.upper():
                key_match = re.search(r"\b([A-Z][A-Z0-9]+-\d+)\b", normalized.upper())
                if key_match:
                    jira_key = key_match.group(1)

        items.append(Doc25Item(
            id=item_id,
            type="BUG",
            status=_map_bug_state_to_doc25_status(state_text),
            title=title,
            sprint=sprint,
            raw_line=match.group(0),
            jira=jira_key,
        ))

    return items


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


def parse_bug_log_for_sprint(bugs_log_file: str | Path, sprint: str) -> list[Doc25Item]:
    """Extrai bugs de uma sprint a partir do arquivo `tests/bugs_log.md`."""
    path = Path(bugs_log_file)
    if not path.exists():
        return []

    content = path.read_text(encoding="utf-8")
    return extract_bugs_from_log(content, sprint)


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
        "To-Do": "Pendentes",
        "Doing": "Em Progresso",
        "Done": "Feito",
        "Accepted": "Feito",
        "Pending-SX": "Pendentes",
        "Pendentes": "Pendentes",
        "Em progresso": "Em Progresso",
        "Em Progresso": "Em Progresso",
        "Em Testes": "Em Testes",
        "Feito": "Feito",
        "Bloqueado": "Bloqueado",
        "Backlog": "Backlog",
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
