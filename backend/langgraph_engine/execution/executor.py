from __future__ import annotations
import asyncio
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
        self._pause_events: dict[str, asyncio.Event] = {}
        self._cancel_events: dict[str, asyncio.Event] = {}

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

        exec_id = execution.id
        self._pause_events[exec_id] = asyncio.Event()
        self._cancel_events[exec_id] = asyncio.Event()

        try:
            self._compiler.compile(node_models, edge_models)
            self._state_manager.initialize(exec_id, execution.inputs)

            if self._cancel_events[exec_id].is_set():
                raise asyncio.CancelledError("Execution cancelled")

            stream = self._compiler.stream(execution.inputs)
            final_output = {}
            async for event in stream:
                if self._cancel_events[exec_id].is_set():
                    raise asyncio.CancelledError("Execution cancelled")

                while self._pause_events[exec_id].is_set():
                    if self._cancel_events[exec_id].is_set():
                        raise asyncio.CancelledError("Execution cancelled")
                    await asyncio.sleep(0.1)

                if isinstance(event, dict):
                    final_output.update(event)

            execution.status = ExecutionStatus.COMPLETED
            execution.outputs = final_output
            execution.completed_at = datetime.now(timezone.utc)
            execution.duration_ms = (
                (execution.completed_at - execution.started_at).total_seconds() * 1000
                if execution.started_at
                else 0
            )

        except asyncio.CancelledError:
            execution.status = ExecutionStatus.CANCELLED
            execution.completed_at = datetime.now(timezone.utc)
            logger.info(f"Execution {exec_id} cancelled")
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}", exc_info=True)
            execution.status = ExecutionStatus.FAILED
            execution.error = str(e)
            execution.completed_at = datetime.now(timezone.utc)
        finally:
            self._pause_events.pop(exec_id, None)
            self._cancel_events.pop(exec_id, None)

        return execution

    async def cancel(self, execution_id: str) -> bool:
        event = self._cancel_events.get(execution_id)
        if event:
            event.set()
        self._state_manager.clear(execution_id)
        logger.info(f"Cancelled execution {execution_id}")
        return True

    async def pause(self, execution_id: str) -> bool:
        event = self._pause_events.get(execution_id)
        if event is None:
            return False
        event.set()
        logger.info(f"Paused execution {execution_id}")
        return True

    async def resume(self, execution_id: str) -> bool:
        event = self._pause_events.get(execution_id)
        if event is None:
            return False
        event.clear()
        logger.info(f"Resumed execution {execution_id}")
        return True
