from __future__ import annotations
from datetime import datetime, timezone
from backend.models.execution import Execution, ExecutionStatus
from backend.langgraph_engine.core.graph_compiler import GraphCompiler
from backend.langgraph_engine.core.state_management import StateManager
from backend.langgraph_engine.execution.error_handler import ErrorHandler
from backend.langgraph_engine.execution.retry_logic import RetryLogic
from backend.langgraph_engine.execution.timeout_manager import TimeoutManager
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class WorkflowExecutor:
    def __init__(self):
        self._compiler = GraphCompiler()
        self._state_manager = StateManager()
        self._error_handler = ErrorHandler()
        self._retry_logic = RetryLogic()
        self._timeout_manager = TimeoutManager()

    async def execute(
        self,
        execution: Execution,
        nodes: list[dict],
        edges: list[dict],
    ) -> Execution:
        from backend.models.node import Node
        from backend.models.edge import Edge

        node_models = [Node(**n) for n in nodes]
        edge_models = [Edge(**e) for e in edges]

        execution.status = ExecutionStatus.RUNNING
        execution.started_at = datetime.now(timezone.utc)

        try:
            self._compiler.compile(node_models, edge_models)
            self._state_manager.initialize(execution.id, execution.inputs)

            result = await self._compiler.run(execution.inputs)

            execution.status = ExecutionStatus.COMPLETED
            execution.outputs = result
            execution.completed_at = datetime.now(timezone.utc)
            execution.duration_ms = (
                (execution.completed_at - execution.started_at).total_seconds() * 1000
                if execution.started_at
                else 0
            )

        except Exception as e:
            logger.error(f"Workflow execution failed: {e}", exc_info=True)
            execution.status = ExecutionStatus.FAILED
            execution.error = str(e)
            execution.completed_at = datetime.now(timezone.utc)

        return execution

    async def cancel(self, execution_id: str) -> bool:
        self._state_manager.clear(execution_id)
        logger.info(f"Cancelled execution {execution_id}")
        return True

    async def pause(self, execution_id: str) -> bool:
        state = self._state_manager.get_state(execution_id)
        if state:
            state["_paused"] = True
            logger.info(f"Paused execution {execution_id}")
            return True
        return False

    async def resume(self, execution_id: str) -> bool:
        state = self._state_manager.get_state(execution_id)
        if state:
            state["_paused"] = False
            logger.info(f"Resumed execution {execution_id}")
            return True
        return False
