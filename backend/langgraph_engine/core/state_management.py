from __future__ import annotations
from typing import Any, Optional
from copy import deepcopy


class StateManager:
    def __init__(self):
        self._states: dict[str, dict[str, Any]] = {}

    def initialize(self, execution_id: str, initial_state: dict[str, Any]) -> dict[str, Any]:
        state = deepcopy(initial_state)
        state["_execution_id"] = execution_id
        state["_node_results"] = {}
        state["_errors"] = []
        state["_current_node"] = None
        self._states[execution_id] = state
        return state

    def get_state(self, execution_id: str) -> Optional[dict[str, Any]]:
        return self._states.get(execution_id)

    def update_state(self, execution_id: str, updates: dict[str, Any]) -> dict[str, Any]:
        if execution_id not in self._states:
            raise KeyError(f"Execution {execution_id} not found")
        self._states[execution_id].update(updates)
        return self._states[execution_id]

    def set_node_result(self, execution_id: str, node_id: str, result: Any):
        if execution_id in self._states:
            self._states[execution_id].setdefault("_node_results", {})[node_id] = result

    def set_current_node(self, execution_id: str, node_id: str):
        if execution_id in self._states:
            self._states[execution_id]["_current_node"] = node_id

    def add_error(self, execution_id: str, error: str):
        if execution_id in self._states:
            self._states[execution_id].setdefault("_errors", []).append(error)

    def clear(self, execution_id: str):
        self._states.pop(execution_id, None)

    def clear_all(self):
        self._states.clear()
