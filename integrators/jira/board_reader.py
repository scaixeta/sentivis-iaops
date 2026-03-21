#!/usr/bin/env python3
"""
jira/board_reader.py - Leitura do workflow observado no board Jira

Transforma a configuracao do board em uma orientacao legivel para o
estado local DOC2.5, sem alterar arquivos de tracking.
"""

from __future__ import annotations


def _normalize(value: str) -> str:
    return (value or "").strip().lower()


def derive_local_status_guidance(board_columns: list[dict]) -> list[dict]:
    """Deriva orientacao de status local a partir das colunas observadas."""
    guidance = []

    for column in board_columns or []:
        column_name = column.get("name", "")
        normalized = _normalize(column_name)

        suggested_local_statuses: list[str] = []
        note = "Coluna observada sem heuristica definida; usar apenas como referencia."

        if "backlog" in normalized:
            note = "Coluna de entrada do board; nao corresponde diretamente a um status operacional do tracking."
        elif "pendent" in normalized or "todo" in normalized or "to do" in normalized:
            suggested_local_statuses = ["To-Do", "Pending-SX"]
            note = "Use To-Do para item planejado na sprint atual; use Pending-SX quando o item ficar carregado para outra sprint."
        elif "progresso" in normalized or "andamento" in normalized or "doing" in normalized or "progress" in normalized:
            suggested_local_statuses = ["Doing"]
            note = "Coluna de execucao ativa; no tracking local a orientacao e marcar como Doing."
        elif "teste" in normalized or "homolog" in normalized or "review" in normalized:
            suggested_local_statuses = ["Doing"]
            note = "Coluna intermediaria de validacao; no tracking local continua representada como Doing ate a conclusao."
        elif "feito" in normalized or "done" in normalized or "conclu" in normalized:
            suggested_local_statuses = ["Done", "Accepted"]
            note = "Use Done para implementacao concluida; use Accepted quando houver aceite ou validacao final registrada."

        guidance.append({
            "board_column": column_name,
            "jira_statuses": column.get("status_names", []) or [],
            "suggested_local_statuses": suggested_local_statuses,
            "note": note,
        })

    return guidance
