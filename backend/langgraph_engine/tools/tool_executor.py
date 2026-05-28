from __future__ import annotations
from typing import Any, Optional
from backend.langgraph_engine.tools.tool_registry import ToolRegistry
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class ToolExecutor:
    def __init__(self):
        self._registry = ToolRegistry()

    async def execute(self, tool_name: str, **params) -> Any:
        logger.info(f"Executing tool: {tool_name}")
        try:
            result = self._registry.execute(tool_name, **params)
            logger.info(f"Tool {tool_name} completed successfully")
            return result
        except Exception as e:
            logger.error(f"Tool {tool_name} failed: {e}")
            raise

    def get_registry(self) -> ToolRegistry:
        return self._registry
