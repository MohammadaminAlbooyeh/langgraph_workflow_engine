from __future__ import annotations
import asyncio
from typing import Optional, Any
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class RetryLogic:
    def __init__(self, default_max_retries: int = 3, default_delay: float = 1.0, backoff: float = 2.0):
        self._default_max_retries = default_max_retries
        self._default_delay = default_delay
        self._backoff = backoff

    async def execute_with_retry(
        self,
        func: callable,
        max_retries: Optional[int] = None,
        delay: Optional[float] = None,
        **kwargs,
    ) -> Any:
        max_retries = max_retries or self._default_max_retries
        delay = delay or self._default_delay
        last_exception = None

        for attempt in range(max_retries):
            try:
                return await func(**kwargs)
            except Exception as e:
                last_exception = e
                logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt < max_retries - 1:
                    wait_time = delay * (self._backoff ** attempt)
                    await asyncio.sleep(wait_time)
        raise last_exception

    def should_retry(self, attempt: int, max_retries: int) -> bool:
        return attempt < max_retries
