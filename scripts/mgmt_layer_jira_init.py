#!/usr/bin/env python3
"""
mgmt_layer_jira_init.py - Wrapper de Bootstrap Jira DOC2.5

Wrapper de compatibilidade para inicialização da camada Jira.
Este arquivo delega para o modulo integrators/jira/.

Uso:
    python scripts/mgmt_layer_jira_init.py
    python scripts/mgmt_layer_jira_init.py --dry-run

Nota: Este wrapper mantem compatibilidade com a interface anterior.
Para nova API, use: python -m integrators.jira bootstrap
"""

import sys
from pathlib import Path

# Adiciona raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Importa do novo modulo
from integrators.jira.bootstrap import run as bootstrap_run


def main():
    """Wrapper de bootstrap (compatibilidade)."""
    dry_run = "--dry-run" in sys.argv
    sys.exit(bootstrap_run(dry_run=dry_run))


if __name__ == "__main__":
    main()
