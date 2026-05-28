from __future__ import annotations
from typing import Any, Optional
from backend.langgraph_engine.tools.built_in_tools import BuiltInTools
from backend.langgraph_engine.tools.custom_tools import CustomTools
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class ToolRegistry:
    def __init__(self):
        self._builtin = BuiltInTools()
        self._custom = CustomTools()

    def list_tools(self) -> list[dict]:
        return self._builtin.list_tools() + self._custom.list_tools()

    def get_tool(self, name: str) -> dict | None:
        tool = self._builtin.get_tool(name)
        if tool:
            return tool
        for t in self._custom.list_tools():
            if t["name"] == name:
                return t
        return None

    def execute(self, name: str, **kwargs) -> Any:
        try:
            return self._builtin.execute(name, **kwargs)
        except ValueError:
            return self._custom.execute(name, **kwargs)

    def register_custom(self, name: str, handler: callable, description: str = "", parameters: Optional[list] = None):
        self._custom.register(name, handler, description, parameters)

    def unregister_custom(self, name: str) -> bool:
        return self._custom.unregister(name)
