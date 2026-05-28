from __future__ import annotations
from typing import Any, Optional
from backend.langgraph_engine.execution.executor import WorkflowExecutor
from backend.models.execution import Execution
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class CustomWorkflow:
    def __init__(self):
        self._executor = WorkflowExecutor()

    async def execute(self, execution: Execution, nodes: list[dict], edges: list[dict]) -> Execution:
        logger.info(f"Executing custom workflow: {execution.workflow_id}")
        return await self._executor.execute(execution, nodes, edges)

    async def validate(self, nodes: list[dict], edges: list[dict]) -> list[str]:
        from backend.utils.graph_utils import validate_graph
        return validate_graph(nodes, edges)
