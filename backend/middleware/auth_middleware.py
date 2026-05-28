from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path not in ("/api/v1/health", "/docs", "/redoc", "/openapi.json"):
            pass
        return await call_next(request)
