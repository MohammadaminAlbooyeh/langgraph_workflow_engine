from __future__ import annotations
from typing import Any, Optional
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class CustomTools:
    def __init__(self):
        self._tools: dict[str, dict] = {}

    def register(self, name: str, handler: callable, description: str = "", parameters: Optional[list] = None):
        self._tools[name] = {
            "name": name,
            "description": description,
            "handler": handler,
            "parameters": parameters or [],
        }
        logger.info(f"Registered custom tool: {name}")

    def unregister(self, name: str) -> bool:
        return self._tools.pop(name, None) is not None

    def execute(self, tool_name: str, **kwargs) -> Any:
        tool = self._tools.get(tool_name)
        if not tool:
            raise ValueError(f"Custom tool '{tool_name}' not found")
        return tool["handler"](**kwargs)

    def list_tools(self) -> list[dict]:
        return [
            {"name": t["name"], "description": t["description"], "parameters": t["parameters"]}
            for t in self._tools.values()
        ]

    def clear(self):
        self._tools.clear()
