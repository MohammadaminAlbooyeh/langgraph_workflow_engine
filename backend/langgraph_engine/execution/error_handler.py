from __future__ import annotations
from typing import Optional, Any
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class ErrorHandler:
    def __init__(self):
        self._error_handlers: dict[str, callable] = {}

    def register_handler(self, error_type: str, handler: callable):
        self._error_handlers[error_type] = handler

    async def handle(self, error: Exception, context: Optional[dict] = None) -> dict[str, Any]:
        error_type = type(error).__name__
        handler = self._error_handlers.get(error_type, self._default_handler)
        return await handler(error, context or {})

    async def _default_handler(self, error: Exception, context: dict) -> dict[str, Any]:
        logger.error(f"Unhandled error: {error}", exc_info=True)
        return {
            "handled": True,
            "error": str(error),
            "error_type": type(error).__name__,
            "action": "fail",
        }

    def clear_handlers(self):
        self._error_handlers.clear()
