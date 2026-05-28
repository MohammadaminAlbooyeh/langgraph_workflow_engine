from __future__ import annotations
from typing import Any, Optional
from backend.langgraph_engine.execution.executor import WorkflowExecutor
from backend.langgraph_engine.execution.scheduler import WorkflowScheduler
from backend.langgraph_engine.supervision.approval_manager import ApprovalManager
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class OrchestrationService:
    def __init__(self):
        self._executor = WorkflowExecutor()
        self._scheduler = WorkflowScheduler()
        self._approval_manager = ApprovalManager()

    async def execute_workflow(self, execution_id: str, nodes: list[dict], edges: list[dict]) -> Any:
        from backend.services.execution_service import ExecutionService
        svc = ExecutionService()
        execution = await svc.get(execution_id)
        if not execution:
            raise ValueError(f"Execution {execution_id} not found")
        return await self._executor.execute(execution, nodes, edges)

    def schedule_workflow(self, workflow_id: str, cron: str, config: Optional[dict] = None) -> str:
        return self._scheduler.schedule(workflow_id, cron, config)

    def cancel_schedule(self, schedule_id: str) -> bool:
        return self._scheduler.cancel_schedule(schedule_id)

    def get_pending_approvals(self) -> list[dict]:
        return self._approval_manager.get_pending()

    async def approve(self, approval_id: str, user: str) -> bool:
        return await self._approval_manager.approve(approval_id, user)

    async def reject(self, approval_id: str, user: str, reason: Optional[str] = None) -> bool:
        return await self._approval_manager.reject(approval_id, user, reason)
