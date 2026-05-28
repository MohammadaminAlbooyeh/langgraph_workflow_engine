from __future__ import annotations
from typing import Optional
from datetime import datetime, timezone
from backend.models.execution import Execution, ExecutionStatus
from backend.langgraph_engine.execution.executor import WorkflowExecutor
from backend.utils.helpers import generate_id
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class ExecutionService:
    def __init__(self):
        self._executions: dict[str, Execution] = {}
        self._executor = WorkflowExecutor()

    async def create(self, workflow_id: str, inputs: dict) -> Execution:
        execution = Execution(
            id=f"ex_{generate_id()}",
            workflow_id=workflow_id,
            inputs=inputs,
        )
        self._executions[execution.id] = execution
        logger.info(f"Created execution: {execution.id} for workflow: {workflow_id}")
        return execution

    async def start(self, execution_id: str, nodes: list[dict], edges: list[dict]) -> Execution:
        execution = self._executions.get(execution_id)
        if not execution:
            raise ValueError(f"Execution {execution_id} not found")

        return await self._executor.execute(execution, nodes, edges)

    async def get(self, execution_id: str) -> Optional[Execution]:
        return self._executions.get(execution_id)

    async def cancel(self, execution_id: str) -> bool:
        execution = self._executions.get(execution_id)
        if execution and execution.status in (ExecutionStatus.PENDING, ExecutionStatus.RUNNING):
            execution.status = ExecutionStatus.CANCELLED
            execution.completed_at = datetime.now(timezone.utc)
            await self._executor.cancel(execution_id)
            return True
        return False

    async def pause(self, execution_id: str) -> bool:
        execution = self._executions.get(execution_id)
        if execution and execution.status == ExecutionStatus.RUNNING:
            execution.status = ExecutionStatus.PAUSED
            return await self._executor.pause(execution_id)
        return False

    async def resume(self, execution_id: str) -> bool:
        execution = self._executions.get(execution_id)
        if execution and execution.status == ExecutionStatus.PAUSED:
            execution.status = ExecutionStatus.RUNNING
            return await self._executor.resume(execution_id)
        return False

    async def list(self, workflow_id: Optional[str] = None) -> list[Execution]:
        if workflow_id:
            return [e for e in self._executions.values() if e.workflow_id == workflow_id]
        return list(self._executions.values())
