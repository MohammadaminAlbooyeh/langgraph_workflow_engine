from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        elapsed = (time.time() - start) * 1000
        response.headers["X-Process-Time-Ms"] = str(round(elapsed, 2))
        return response
