from __future__ import annotations
from typing import Any, Optional
from backend.langgraph_engine.memory.memory_manager import MemoryManager
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class MemoryService:
    def __init__(self):
        self._memory_manager = MemoryManager()

    def save_context(self, key: str, value: Any, ttl: Optional[int] = None):
        self._memory_manager.save_context(key, value, ttl)

    def get_context(self, key: str, default: Any = None) -> Any:
        return self._memory_manager.get_context(key, default)

    def save_checkpoint(self, execution_id: str, state: dict, label: Optional[str] = None) -> str:
        return self._memory_manager.save_checkpoint(execution_id, state, label)

    def restore_checkpoint(self, execution_id: str, checkpoint_id: str) -> Optional[dict]:
        return self._memory_manager.restore_checkpoint(execution_id, checkpoint_id)

    def list_checkpoints(self, execution_id: str) -> list[dict]:
        return self._memory_manager.checkpoint_manager.list_checkpoints(execution_id)
