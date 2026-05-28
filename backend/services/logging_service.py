from __future__ import annotations
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class LoggingService:
    def log_event(self, event_type: str, data: dict):
        logger.info(f"Event: {event_type}", event_type=event_type, data=data)

    def log_error(self, error: Exception, context: dict | None = None):
        logger.error(str(error), exc_info=True, context=context or {})
