import pytest
from backend.langgraph_engine.workflows.custom_workflow import CustomWorkflow
from backend.langgraph_engine.workflows.data_pipeline_workflow import DataPipelineWorkflow
from backend.langgraph_engine.workflows.decision_tree_workflow import DecisionTreeWorkflow
from backend.langgraph_engine.workflows.multi_agent_workflow import MultiAgentWorkflow


@pytest.mark.asyncio
async def test_custom_workflow_validate():
    wf = CustomWorkflow()
    errors = await wf.validate([], [])
    assert len(errors) > 0


@pytest.mark.asyncio
async def test_custom_workflow_validate_valid():
    wf = CustomWorkflow()
    nodes = [{"id": "n1"}, {"id": "n2"}]
    edges = [{"source_id": "n1", "target_id": "n2"}]
    errors = await wf.validate(nodes, edges)
    assert len(errors) == 0


@pytest.mark.asyncio
async def test_data_pipeline_workflow_validation():
    wf = DataPipelineWorkflow()
    errors = await wf.validate([{"id": "n1", "type": "llm"}], [])
    has_input_error = any("input node" in e for e in errors)
    has_output_error = any("output node" in e for e in errors)
    assert has_input_error
    assert has_output_error


@pytest.mark.asyncio
async def test_decision_tree_workflow_validation():
    wf = DecisionTreeWorkflow()
    errors = await wf.validate([{"id": "n1", "type": "llm"}], [])
    has_decision_error = any("decision" in e for e in errors)
    assert has_decision_error


@pytest.mark.asyncio
async def test_multi_agent_workflow_validation():
    wf = MultiAgentWorkflow()
    errors = await wf.validate([{"id": "n1", "type": "agent"}], [])
    has_multi_agent_error = any("2 agent" in e for e in errors)
    assert has_multi_agent_error
