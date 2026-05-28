import pytest
from backend.langgraph_engine.core.state_management import StateManager


@pytest.mark.asyncio
async def test_state_initialization():
    sm = StateManager()
    state = sm.initialize("ex_1", {"key": "value"})
    assert state["key"] == "value"
    assert state["_execution_id"] == "ex_1"


@pytest.mark.asyncio
async def test_state_update():
    sm = StateManager()
    sm.initialize("ex_1", {"key": "value"})
    updated = sm.update_state("ex_1", {"key": "new_value"})
    assert updated["key"] == "new_value"


@pytest.mark.asyncio
async def test_state_get():
    sm = StateManager()
    sm.initialize("ex_1", {"key": "value"})
    state = sm.get_state("ex_1")
    assert state is not None
    assert state["key"] == "value"


@pytest.mark.asyncio
async def test_state_not_found():
    sm = StateManager()
    assert sm.get_state("nonexistent") is None


@pytest.mark.asyncio
async def test_state_clear():
    sm = StateManager()
    sm.initialize("ex_1", {})
    sm.clear("ex_1")
    assert sm.get_state("ex_1") is None


@pytest.mark.asyncio
async def test_node_result():
    sm = StateManager()
    sm.initialize("ex_1", {})
    sm.set_node_result("ex_1", "node_a", {"result": "ok"})
    state = sm.get_state("ex_1")
    assert state["_node_results"]["node_a"] == {"result": "ok"}


@pytest.mark.asyncio
async def test_state_clear_all():
    sm = StateManager()
    sm.initialize("ex_1", {})
    sm.initialize("ex_2", {})
    sm.clear_all()
    assert sm.get_state("ex_1") is None
    assert sm.get_state("ex_2") is None
