#!/usr/bin/env python3
"""
mgmt_layer_jira.py - CLI Wrapper Jira DOC2.5

Wrapper de compatibilidade para operacao da camada Jira.
Este arquivo delega para o modulo integrators/jira/.

Uso:
    python scripts/mgmt_layer_jira.py status
    python scripts/mgmt_layer_jira.py discover
    python scripts/mgmt_layer_jira.py sync --dry-run
    python scripts/mgmt_layer_jira.py sync
    python scripts/mgmt_layer_jira.py reconcile

Nota: Este wrapper mantem compatibilidade com a interface anterior.
Para nova API, use: python -m integrators.jira <comando>
"""

import sys
from pathlib import Path

# Adiciona raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Importa do novo modulo
from integrators.jira.cli import (
    cmd_status,
    cmd_discover,
    cmd_sync,
    cmd_reconcile,
)


def main():
    """Router de comandos (compatibilidade)."""
    if len(sys.argv) < 2:
        print("Uso: mgmt_layer_jira.py <comando>")
        print()
        print("Comandos:")
        print("  status            - Mostra estado atual")
        print("  discover          - Atualiza metadados do Jira")
        print("  sync [--dry-run]  - Sincroniza tracking com Jira")
        print("  reconcile         - Analisa divergencias")
        sys.exit(1)

    command = sys.argv[1]

    if command == "status":
        sys.exit(cmd_status())
    elif command == "discover":
        sys.exit(cmd_discover())
    elif command == "sync":
        dry_run = "--dry-run" in sys.argv
        sys.exit(cmd_sync(dry_run=dry_run))
    elif command == "reconcile":
        sys.exit(cmd_reconcile())
    else:
        print(f"[ERRO] Comando desconhecido: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
