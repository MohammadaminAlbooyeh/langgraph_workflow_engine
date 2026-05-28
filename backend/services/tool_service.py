from __future__ import annotations
from typing import Any, Optional
from backend.langgraph_engine.tools.tool_registry import ToolRegistry
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class ToolService:
    def __init__(self):
        self._registry = ToolRegistry()

    def list_tools(self) -> list[dict]:
        return self._registry.list_tools()

    def get_tool(self, name: str) -> Optional[dict]:
        return self._registry.get_tool(name)

    def execute_tool(self, name: str, **params) -> Any:
        return self._registry.execute(name, **params)

    def register_tool(self, name: str, handler: callable, description: str = "", parameters: Optional[list] = None):
        self._registry.register_custom(name, handler, description, parameters)

    def unregister_tool(self, name: str) -> bool:
        return self._registry.unregister_custom(name)
