import pytest
from backend.models.workflow import Workflow, WorkflowStatus
from backend.models.node import Node, NodeConfig, NodeType
from backend.models.edge import Edge, EdgeCondition, EdgeType
from backend.models.execution import Execution, ExecutionStatus, ExecutionResult


def test_workflow_model():
    wf = Workflow(name="Test", type="custom")
    assert wf.name == "Test"
    assert wf.status == WorkflowStatus.DRAFT
    assert wf.id is not None


def test_node_model():
    node = Node(id="n1", type=NodeType.LLM, name="GPT-4", config=NodeConfig(temperature=0.7))
    assert node.name == "GPT-4"
    assert node.config.temperature == 0.7


def test_edge_model():
    edge = Edge(id="e1", source_id="n1", target_id="n2", type=EdgeType.CONDITIONAL,
                condition=EdgeCondition(field="status", operator="equals", value="done"))
    assert edge.type == EdgeType.CONDITIONAL
    assert edge.condition.field == "status"


def test_execution_model():
    ex = Execution(id="ex_1", workflow_id="wf_1", inputs={"key": "value"})
    assert ex.status == ExecutionStatus.PENDING
    assert ex.inputs["key"] == "value"


def test_execution_result():
    result = ExecutionResult(node_id="n1", node_name="Test", status=ExecutionStatus.COMPLETED, output={"result": "ok"})
    assert result.status == ExecutionStatus.COMPLETED
    assert result.output["result"] == "ok"


def test_execution_status_transitions():
    ex = Execution(id="ex_1", workflow_id="wf_1")
    assert ex.status == ExecutionStatus.PENDING
    ex.status = ExecutionStatus.RUNNING
    assert ex.status == ExecutionStatus.RUNNING
    ex.status = ExecutionStatus.COMPLETED
    assert ex.status == ExecutionStatus.COMPLETED
