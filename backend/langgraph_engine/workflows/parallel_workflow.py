from __future__ import annotations
from typing import Any
import asyncio
from backend.langgraph_engine.workflows.custom_workflow import CustomWorkflow
from backend.models.execution import Execution, ExecutionStatus
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class ParallelWorkflow(CustomWorkflow):
    async def execute(self, execution: Execution, nodes: list[dict], edges: list[dict]) -> Execution:
        logger.info(f"Executing parallel workflow: {execution.workflow_id}")
        execution.status = ExecutionStatus.RUNNING

        parallel_tasks = []
        for node in nodes:
            task = self._executor.execute(execution, [node], [])
            parallel_tasks.append(task)

        results = await asyncio.gather(*parallel_tasks, return_exceptions=True)
        execution.outputs = {"parallel_results": [str(r) for r in results]}
        execution.status = ExecutionStatus.COMPLETED
        return execution
