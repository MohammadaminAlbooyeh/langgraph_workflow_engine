import pytest
from backend.langgraph_engine.tools.tool_registry import ToolRegistry
from backend.langgraph_engine.tools.tool_executor import ToolExecutor


@pytest.mark.asyncio
async def test_tool_executor_builtin():
    executor = ToolExecutor()
    result = await executor.execute("calculate", expression="2 + 2")
    assert result == 4


@pytest.mark.asyncio
async def test_tool_executor_registry():
    executor = ToolExecutor()
    reg = executor.get_registry()
    reg.register_custom("multiply", lambda a, b: a * b, "Multiplies two numbers")
    result = await executor.execute("multiply", a=3, b=4)
    assert result == 12


@pytest.mark.asyncio
async def test_tool_executor_not_found():
    executor = ToolExecutor()
    with pytest.raises(ValueError):
        await executor.execute("nonexistent_tool")


@pytest.mark.asyncio
async def test_tool_registry_list():
    reg = ToolRegistry()
    tools = reg.list_tools()
    assert len(tools) >= 3
