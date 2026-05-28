import pytest
from backend.langgraph_engine.execution.error_handler import ErrorHandler
from backend.langgraph_engine.execution.retry_logic import RetryLogic
from backend.langgraph_engine.execution.timeout_manager import TimeoutManager


@pytest.mark.asyncio
async def test_error_handler_default():
    handler = ErrorHandler()
    result = await handler.handle(ValueError("test error"))
    assert result["handled"] is True
    assert result["error"] == "test error"
    assert result["action"] == "fail"


@pytest.mark.asyncio
async def test_error_handler_registered():
    handler = ErrorHandler()

    async def custom_handler(error, context):
        return {"handled": True, "action": "retry", "error": str(error)}

    handler.register_handler("ValueError", custom_handler)
    result = await handler.handle(ValueError("test"))
    assert result["action"] == "retry"


@pytest.mark.asyncio
async def test_retry_logic_success():
    retry = RetryLogic()
    call_count = 0

    async def succeed():
        nonlocal call_count
        call_count += 1
        return "success"

    result = await retry.execute_with_retry(succeed)
    assert result == "success"
    assert call_count == 1


@pytest.mark.asyncio
async def test_retry_logic_failure():
    retry = RetryLogic(default_max_retries=2, default_delay=0.01)
    call_count = 0

    async def always_fail():
        nonlocal call_count
        call_count += 1
        raise ValueError("fail")

    with pytest.raises(ValueError):
        await retry.execute_with_retry(always_fail)
    assert call_count == 2


@pytest.mark.asyncio
async def test_timeout_manager_success():
    import asyncio
    tm = TimeoutManager(default_timeout=10)

    async def quick():
        await asyncio.sleep(0.01)
        return "done"

    result = await tm.run_with_timeout(quick())
    assert result == "done"


@pytest.mark.asyncio
async def test_timeout_manager_timeout():
    import asyncio
    tm = TimeoutManager(default_timeout=0.01)

    async def slow():
        await asyncio.sleep(10)

    with pytest.raises(TimeoutError):
        await tm.run_with_timeout(slow())
