from __future__ import annotations
from typing import Any, Optional
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class StatePersistence:
    def __init__(self):
        self._store: dict[str, dict] = {}

    def persist(self, execution_id: str, state: dict[str, Any]) -> bool:
        self._store[execution_id] = state.copy()
        logger.debug(f"Persisted state for execution {execution_id}")
        return True

    def load(self, execution_id: str) -> Optional[dict]:
        state = self._store.get(execution_id)
        if state:
            return state.copy()
        return None

    def delete(self, execution_id: str) -> bool:
        return self._store.pop(execution_id, None) is not None

    def list_persisted(self) -> list[str]:
        return list(self._store.keys())

    def clear(self):
        self._store.clear()
