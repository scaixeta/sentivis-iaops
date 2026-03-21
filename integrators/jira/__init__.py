# integrators/jira/__init__.py
"""
Integrador Jira para o modelo DOC2.5.

Módulos:
    - client: Cliente HTTP para Jira Cloud
    - state: Persistência de estado observado
    - mapper: Mapeamento DOC2.5 -> Jira
    - sync_engine: Engine de sincronização
    - bootstrap: Inicialização e discovery
    - cli: Router de comandos CLI
"""

__version__ = "1.0.0"

from .board_reader import derive_local_status_guidance
from .client import JiraClient, JiraClientError
from .state import JiraState, load_state, save_state
from .mapper import JiraMapper, create_create_payload
from .sync_engine import SyncEngine, SyncResult

__all__ = [
    "derive_local_status_guidance",
    "JiraClient",
    "JiraClientError",
    "JiraState",
    "load_state",
    "save_state",
    "JiraMapper",
    "create_create_payload",
    "SyncEngine",
    "SyncResult",
]
