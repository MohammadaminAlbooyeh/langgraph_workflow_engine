from __future__ import annotations
from typing import Any, Optional
from backend.langgraph_engine.core.state_management import StateManager
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class StateService:
    def __init__(self):
        self._state_manager = StateManager()

    def get_state(self, execution_id: str) -> Optional[dict]:
        return self._state_manager.get_state(execution_id)

    def update_state(self, execution_id: str, updates: dict) -> dict:
        return self._state_manager.update_state(execution_id, updates)

    def clear_state(self, execution_id: str):
        self._state_manager.clear(execution_id)
