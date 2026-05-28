from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from backend.utils.logger import get_logger
import time

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        return response
