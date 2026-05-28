import pytest
from backend.langgraph_engine.workflows.multi_agent_workflow import MultiAgentWorkflow


@pytest.mark.asyncio
async def test_multi_agent_validation_passes():
    wf = MultiAgentWorkflow()
    nodes = [
        {"id": "agent_1", "type": "agent", "name": "Agent 1"},
        {"id": "agent_2", "type": "agent", "name": "Agent 2"},
        {"id": "output", "type": "output", "name": "Output"},
    ]
    edges = [{"source_id": "agent_1", "target_id": "agent_2"}, {"source_id": "agent_2", "target_id": "output"}]
    errors = await wf.validate(nodes, edges)
    assert len(errors) == 0


@pytest.mark.asyncio
async def test_multi_agent_validation_fails():
    wf = MultiAgentWorkflow()
    nodes = [{"id": "agent_1", "type": "agent", "name": "Agent 1"}]
    errors = await wf.validate(nodes, [])
    assert len(errors) > 0
