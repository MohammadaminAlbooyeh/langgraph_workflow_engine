import pytest
from backend.langgraph_engine.core.graph_builder import GraphBuilder
from backend.models.node import Node, NodeConfig, NodeType
from backend.models.edge import Edge, EdgeType, EdgeCondition


@pytest.mark.asyncio
async def test_graph_builder_creates_graph():
    builder = GraphBuilder()
    nodes = [
        Node(id="n1", type=NodeType.INPUT, name="Input", config=NodeConfig()),
        Node(id="n2", type=NodeType.AGENT, name="Agent", config=NodeConfig()),
        Node(id="n3", type=NodeType.OUTPUT, name="Output", config=NodeConfig()),
    ]
    edges = [
        Edge(id="e1", source_id="n1", target_id="n2"),
        Edge(id="e2", source_id="n2", target_id="n3"),
    ]
    graph = builder.build(nodes, edges)
    assert graph is not None


@pytest.mark.asyncio
async def test_graph_builder_with_conditional_edge():
    builder = GraphBuilder()
    nodes = [
        Node(id="n1", type=NodeType.INPUT, name="Input", config=NodeConfig()),
        Node(id="n2", type=NodeType.CONDITIONAL, name="Decision", config=NodeConfig()),
        Node(id="n3", type=NodeType.OUTPUT, name="Output", config=NodeConfig()),
    ]
    edges = [
        Edge(id="e1", source_id="n1", target_id="n2"),
        Edge(id="e2", source_id="n2", target_id="n3", type=EdgeType.CONDITIONAL,
             condition=EdgeCondition(field="data", operator="exists", value=True)),
    ]
    graph = builder.build(nodes, edges)
    assert graph is not None


@pytest.mark.asyncio
async def test_graph_builder_empty():
    builder = GraphBuilder()
    graph = builder.build([], [])
    assert graph is not None


@pytest.mark.asyncio
async def test_graph_builder_single_node():
    builder = GraphBuilder()
    nodes = [Node(id="n1", type=NodeType.INPUT, name="Input", config=NodeConfig())]
    graph = builder.build(nodes, [])
    assert graph is not None
