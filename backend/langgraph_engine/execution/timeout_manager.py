from __future__ import annotations
import asyncio
from typing import Optional, Any
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class TimeoutManager:
    def __init__(self, default_timeout: int = 300):
        self._default_timeout = default_timeout
        self._timeouts: dict[str, asyncio.Task] = {}

    async def run_with_timeout(self, coro, timeout: Optional[int] = None, task_id: Optional[str] = None) -> Any:
        timeout = timeout or self._default_timeout
        try:
            result = await asyncio.wait_for(coro, timeout=timeout)
            if task_id and task_id in self._timeouts:
                del self._timeouts[task_id]
            return result
        except asyncio.TimeoutError:
            logger.error(f"Task {task_id or 'unknown'} timed out after {timeout}s")
            if task_id:
                self._timeouts.pop(task_id, None)
            raise TimeoutError(f"Execution timed out after {timeout} seconds")

    def cancel_task(self, task_id: str) -> bool:
        if task_id in self._timeouts:
            self._timeouts[task_id].cancel()
            del self._timeouts[task_id]
            return True
        return False

    def cancel_all(self):
        for task_id in list(self._timeouts.keys()):
            self.cancel_task(task_id)
