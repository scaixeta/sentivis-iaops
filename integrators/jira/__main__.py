#!/usr/bin/env python3
"""
integrators/jira/__main__.py - Entry Point para python -m integrators.jira

Permite execução via:
    python -m integrators.jira status
    python -m integrators.jira discover
    python -m integrators.jira sync --dry-run
    python -m integrators.jira bootstrap --dry-run
"""

import sys
from pathlib import Path

# Adiciona raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from integrators.jira.cli import main

if __name__ == "__main__":
    sys.exit(main())
