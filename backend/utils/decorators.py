from __future__ import annotations
import time
import asyncio
import functools
from typing import Any, Callable, TypeVar
from backend.utils.logger import get_logger

F = TypeVar("F", bound=Callable[..., Any])
logger = get_logger(__name__)


def log_execution(func: F = None, *, level: str = "INFO"):
    def decorator(f: F) -> F:
        @functools.wraps(f)
        async def async_wrapper(*args, **kwargs):
            logger.log(level, f"Executing {f.__name__}")
            try:
                result = await f(*args, **kwargs)
                logger.log(level, f"Completed {f.__name__}")
                return result
            except Exception as e:
                logger.error(f"Failed {f.__name__}: {e}")
                raise

        @functools.wraps(f)
        def sync_wrapper(*args, **kwargs):
            logger.log(level, f"Executing {f.__name__}")
            try:
                result = f(*args, **kwargs)
                logger.log(level, f"Completed {f.__name__}")
                return result
            except Exception as e:
                logger.error(f"Failed {f.__name__}: {e}")
                raise

        if asyncio.iscoroutinefunction(f):
            return async_wrapper
        return sync_wrapper

    if func:
        return decorator(func)
    return decorator


def measure_time(func: F = None, *, log_level: str = "DEBUG"):
    def decorator(f: F) -> F:
        @functools.wraps(f)
        async def async_wrapper(*args, **kwargs):
            start = time.time()
            result = await f(*args, **kwargs)
            duration = (time.time() - start) * 1000
            logger.log(log_level, f"{f.__name__} took {duration:.2f}ms")
            return result

        @functools.wraps(f)
        def sync_wrapper(*args, **kwargs):
            start = time.time()
            result = f(*args, **kwargs)
            duration = (time.time() - start) * 1000
            logger.log(log_level, f"{f.__name__} took {duration:.2f}ms")
            return result

        if asyncio.iscoroutinefunction(f):
            return async_wrapper
        return sync_wrapper

    if func:
        return decorator(func)
    return decorator


def retry_on_failure(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(delay * (backoff ** attempt))
            raise last_exception

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(delay * (backoff ** attempt))
            raise last_exception

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator
