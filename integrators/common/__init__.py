# integrators/common/__init__.py
"""
Módulos comuns para integradores DOC2.5.

Este pacote contém utilitários e parsers compartilhados entre
diferentes provedores de integração (Jira, GitHub Projects, etc).
"""

__version__ = "1.0.0"

from .doc25_parser import (
    Doc25Item,
    parse_sprint_backlog,
    extract_items,
    extract_decisions,
    extract_objectives,
)

__all__ = [
    "Doc25Item",
    "parse_sprint_backlog",
    "extract_items",
    "extract_decisions",
    "extract_objectives",
]
