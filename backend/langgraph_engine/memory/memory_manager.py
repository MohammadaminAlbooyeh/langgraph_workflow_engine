from __future__ import annotations
from typing import Any, Optional
from backend.langgraph_engine.memory.checkpoint import CheckpointManager
from backend.langgraph_engine.memory.context_store import ContextStore
from backend.langgraph_engine.memory.state_persistence import StatePersistence
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class MemoryManager:
    def __init__(self):
        self.checkpoint_manager = CheckpointManager()
        self.context_store = ContextStore()
        self.state_persistence = StatePersistence()

    def save_context(self, key: str, value: Any, ttl: Optional[int] = None):
        self.context_store.set(key, value, ttl)

    def get_context(self, key: str, default: Any = None) -> Any:
        return self.context_store.get(key, default)

    def save_checkpoint(self, execution_id: str, state: dict, label: Optional[str] = None) -> str:
        return self.checkpoint_manager.save_checkpoint(execution_id, state, label)

    def restore_checkpoint(self, execution_id: str, checkpoint_id: str) -> Optional[dict]:
        return self.checkpoint_manager.restore_checkpoint(execution_id, checkpoint_id)

    def clear(self, execution_id: str):
        self.checkpoint_manager.clear(execution_id)

    def clear_all(self):
        self.checkpoint_manager.clear_all()
        self.context_store.clear()
