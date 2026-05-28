import pytest
from backend.langgraph_engine.nodes.agent_nodes.agent_node import AgentNode, PlannerAgent, ReasoningAgent, ToolAgent
from backend.models.node import NodeConfig, NodeType


@pytest.mark.asyncio
async def test_agent_node_execute():
    agent = AgentNode(id="a1", name="Test Agent")
    result = await agent.execute({"input": "test"})
    assert "response" in result
    assert "reasoning" in result


@pytest.mark.asyncio
async def test_planner_agent_execute():
    agent = PlannerAgent(id="a1", name="Planner")
    result = await agent.execute({"goal": "test"})
    assert "plan" in result
    assert "steps" in result


@pytest.mark.asyncio
async def test_reasoning_agent_execute():
    agent = ReasoningAgent(id="a1", name="Reasoner")
    result = await agent.execute({"question": "why?"})
    assert "reasoning" in result
    assert "conclusion" in result


@pytest.mark.asyncio
async def test_tool_agent_execute():
    agent = ToolAgent(id="a1", name="Tool Agent")
    result = await agent.execute({"tool": "search"})
    assert "tool_calls" in result
    assert "tool_results" in result


@pytest.mark.asyncio
async def test_agent_node_type():
    agent = AgentNode(id="a1", name="Test")
    assert agent._get_node_type() == NodeType.AGENT


@pytest.mark.asyncio
async def test_agent_to_node_model():
    agent = AgentNode(id="a1", name="Test", system_prompt="Be helpful.")
    model = agent.to_node_model()
    assert model.id == "a1"
    assert model.name == "Test"
    assert model.type == NodeType.AGENT
