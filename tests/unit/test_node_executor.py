import pytest
from backend.langgraph_engine.core.node_executor import NodeExecutor


@pytest.mark.asyncio
async def test_execute_llm_node():
    executor = NodeExecutor()
    config = {"type": "llm", "name": "test_llm", "provider": "openai", "prompt_template": "Hello {name}"}
    result = await executor.execute("n1", config, {"name": "World"})
    assert result.status.value == "completed"
    assert result.node_id == "n1"


@pytest.mark.asyncio
async def test_execute_input_node():
    executor = NodeExecutor()
    config = {"type": "input", "name": "test_input"}
    result = await executor.execute("n1", config, {"data": {"key": "value"}})
    assert result.status.value == "completed"


@pytest.mark.asyncio
async def test_execute_output_node():
    executor = NodeExecutor()
    config = {"type": "output", "name": "test_output"}
    result = await executor.execute("n1", config, {"result": "done"})
    assert result.status.value == "completed"


@pytest.mark.asyncio
async def test_execute_agent_node():
    executor = NodeExecutor()
    config = {"type": "agent", "name": "test_agent"}
    result = await executor.execute("n1", config, {})
    assert result.status.value == "completed"
    assert "agent_output" in result.output


@pytest.mark.asyncio
async def test_execute_transformer_node():
    executor = NodeExecutor()
    config = {"type": "transformer", "name": "test_transformer"}
    result = await executor.execute("n1", config, {"data": {"value": 42}})
    assert result.status.value == "completed"


@pytest.mark.asyncio
async def test_execute_validator_node():
    executor = NodeExecutor()
    config = {"type": "validator", "name": "test_validator"}
    result = await executor.execute("n1", config, {"data": {"value": 42}})
    assert result.status.value == "completed"
    assert result.output.get("valid") is True


@pytest.mark.asyncio
async def test_execute_default_node():
    executor = NodeExecutor()
    config = {"type": "unknown", "name": "test_default"}
    result = await executor.execute("n1", config, {"foo": "bar"})
    assert result.status.value == "completed"
