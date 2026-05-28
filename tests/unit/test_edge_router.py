import pytest
from backend.langgraph_engine.core.edge_router import EdgeRouter
from backend.models.edge import Edge, EdgeCondition, EdgeType


@pytest.mark.asyncio
async def test_direct_route():
    router = EdgeRouter()
    edges = [Edge(id="e1", source_id="a", target_id="b", type=EdgeType.DIRECT)]
    result = router.route(edges, {})
    assert len(result) == 1
    assert result[0].id == "e1"


@pytest.mark.asyncio
async def test_conditional_route_match():
    router = EdgeRouter()
    edges = [
        Edge(id="e1", source_id="a", target_id="b", type=EdgeType.CONDITIONAL,
             condition=EdgeCondition(field="status", operator="equals", value="done"))
    ]
    result = router.route(edges, {"status": "done"})
    assert len(result) == 1


@pytest.mark.asyncio
async def test_conditional_route_no_match():
    router = EdgeRouter()
    edges = [
        Edge(id="e1", source_id="a", target_id="b", type=EdgeType.CONDITIONAL,
             condition=EdgeCondition(field="status", operator="equals", value="done"))
    ]
    result = router.route(edges, {"status": "pending"})
    assert len(result) == 0


@pytest.mark.asyncio
async def test_dynamic_edge():
    router = EdgeRouter()
    edges = [Edge(id="e1", source_id="a", target_id="b", type=EdgeType.DYNAMIC)]
    result = router.route(edges, {})
    assert len(result) == 1


@pytest.mark.asyncio
async def test_event_edge():
    router = EdgeRouter()
    edges = [Edge(id="e1", source_id="a", target_id="b", type=EdgeType.EVENT)]
    result = router.route(edges, {})
    assert len(result) == 1


@pytest.mark.asyncio
async def test_condition_equals():
    router = EdgeRouter()
    assert router.evaluate_condition(EdgeCondition(field="x", operator="equals", value=5), {"x": 5}) is True
    assert router.evaluate_condition(EdgeCondition(field="x", operator="equals", value=5), {"x": 10}) is False


@pytest.mark.asyncio
async def test_condition_contains():
    router = EdgeRouter()
    assert router.evaluate_condition(EdgeCondition(field="text", operator="contains", value="hello"), {"text": "hello world"}) is True
    assert router.evaluate_condition(EdgeCondition(field="text", operator="contains", value="bye"), {"text": "hello"}) is False


@pytest.mark.asyncio
async def test_condition_exists():
    router = EdgeRouter()
    assert router.evaluate_condition(EdgeCondition(field="key", operator="exists"), {"key": "value"}) is True
    assert router.evaluate_condition(EdgeCondition(field="missing", operator="exists"), {}) is False


@pytest.mark.asyncio
async def test_condition_gt():
    router = EdgeRouter()
    assert router.evaluate_condition(EdgeCondition(field="count", operator="gt", value=5), {"count": 10}) is True
    assert router.evaluate_condition(EdgeCondition(field="count", operator="gt", value=5), {"count": 3}) is False


@pytest.mark.asyncio
async def test_edge_priority():
    router = EdgeRouter()
    edges = [
        Edge(id="e1", source_id="a", target_id="b", type=EdgeType.DIRECT, priority=1),
        Edge(id="e2", source_id="a", target_id="c", type=EdgeType.DIRECT, priority=2),
    ]
    result = router.route(edges, {})
    assert result[0].id == "e2"
