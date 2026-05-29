from __future__ import annotations
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.execution import Execution, ExecutionStatus
from backend.langgraph_engine.execution.executor import WorkflowExecutor
from backend.db.repositories import ExecutionRepository
from backend.utils.helpers import generate_id
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class ExecutionService:
    def __init__(self, session: Optional[AsyncSession] = None):
        self._session = session
        self._executions: dict[str, Execution] = {}
        self._executor = WorkflowExecutor()

    def _get_repo(self) -> Optional[ExecutionRepository]:
        if self._session is not None:
            return ExecutionRepository(self._session)
        return None

    async def create(self, workflow_id: str, inputs: dict) -> Execution:
        execution = Execution(
            id=f"ex_{generate_id()}",
            workflow_id=workflow_id,
            inputs=inputs,
        )

        repo = self._get_repo()
        if repo:
            execution = await repo.create({
                "id": execution.id,
                "workflow_id": workflow_id,
                "inputs": inputs,
            })
        else:
            self._executions[execution.id] = execution

        logger.info(f"Created execution: {execution.id} for workflow: {workflow_id}")
        return execution

    async def start(self, execution_id: str, nodes: list[dict], edges: list[dict]) -> Execution:
        execution = await self.get(execution_id)
        if not execution:
            raise ValueError(f"Execution {execution_id} not found")

        execution = await self._executor.execute(execution, nodes, edges)

        repo = self._get_repo()
        if repo:
            await repo.update(execution_id, {
                "status": execution.status.value,
                "outputs": execution.outputs,
                "error": execution.error,
                "started_at": execution.started_at,
                "completed_at": execution.completed_at,
                "duration_ms": execution.duration_ms,
            })

        return execution

    async def get(self, execution_id: str) -> Optional[Execution]:
        repo = self._get_repo()
        if repo:
            return await repo.get(execution_id)
        return self._executions.get(execution_id)

    async def cancel(self, execution_id: str) -> bool:
        execution = await self.get(execution_id)
        if execution and execution.status in (ExecutionStatus.PENDING, ExecutionStatus.RUNNING):
            execution.status = ExecutionStatus.CANCELLED
            execution.completed_at = datetime.now(timezone.utc)
            await self._executor.cancel(execution_id)
            repo = self._get_repo()
            if repo:
                await repo.update(execution_id, {"status": "cancelled", "completed_at": execution.completed_at})
            return True
        return False

    async def pause(self, execution_id: str) -> bool:
        execution = await self.get(execution_id)
        if execution and execution.status == ExecutionStatus.RUNNING:
            execution.status = ExecutionStatus.PAUSED
            paused = await self._executor.pause(execution_id)
            repo = self._get_repo()
            if repo:
                await repo.update(execution_id, {"status": "paused"})
            return paused
        return False

    async def resume(self, execution_id: str) -> bool:
        execution = await self.get(execution_id)
        if execution and execution.status == ExecutionStatus.PAUSED:
            execution.status = ExecutionStatus.RUNNING
            resumed = await self._executor.resume(execution_id)
            repo = self._get_repo()
            if repo:
                await repo.update(execution_id, {"status": "running"})
            return resumed
        return False

    async def list(self, workflow_id: Optional[str] = None) -> list[Execution]:
        repo = self._get_repo()
        if repo:
            return await repo.list(workflow_id)
        if workflow_id:
            return [e for e in self._executions.values() if e.workflow_id == workflow_id]
        return list(self._executions.values())
