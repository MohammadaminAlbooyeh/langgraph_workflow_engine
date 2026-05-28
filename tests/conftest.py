import pytest


@pytest.fixture
def sample_workflow_data():
    return {
        "name": "Test Workflow",
        "description": "A test workflow",
        "type": "custom",
        "nodes": [
            {"id": "node_1", "type": "input", "name": "Input Node", "position": {"x": 0, "y": 0}},
            {"id": "node_2", "type": "llm", "name": "LLM Node", "config": {"provider": "openai", "temperature": 0.7}},
            {"id": "node_3", "type": "output", "name": "Output Node", "position": {"x": 200, "y": 200}},
        ],
        "edges": [
            {"id": "edge_1", "source_id": "node_1", "target_id": "node_2", "type": "direct"},
            {"id": "edge_2", "source_id": "node_2", "target_id": "node_3", "type": "direct"},
        ],
    }


@pytest.fixture
def sample_execution_data():
    return {
        "workflow_id": "wf_test_001",
        "inputs": {"data": "test input"},
    }


@pytest.fixture
def sample_node_config():
    return {
        "type": "llm",
        "name": "Test LLM",
        "config": {"provider": "openai", "model": "gpt-4", "temperature": 0.7},
    }
