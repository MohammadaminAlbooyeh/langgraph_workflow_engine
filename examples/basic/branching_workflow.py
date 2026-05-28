"""Branching workflow with conditional routing"""
from backend.models.workflow import Workflow
from backend.models.node import Node, NodeConfig, NodeType
from backend.models.edge import Edge, EdgeType, EdgeCondition

workflow = Workflow(
    name="Branching Workflow",
    description="Routes to different paths based on input value",
    nodes=[
        Node(id="start", type=NodeType.INPUT, name="Start"),
        Node(id="decision", type=NodeType.CONDITIONAL, name="Check Value",
             config=NodeConfig(custom_attributes={"condition_field": "score"})),
        Node(id="high", type=NodeType.LLM, name="High Score Path", config=NodeConfig(prompt_template="High: {data}")),
        Node(id="low", type=NodeType.LLM, name="Low Score Path", config=NodeConfig(prompt_template="Low: {data}")),
        Node(id="end", type=NodeType.OUTPUT, name="End"),
    ],
    edges=[
        Edge(id="e1", source_id="start", target_id="decision"),
        Edge(id="e2_high", source_id="decision", target_id="high", type=EdgeType.CONDITIONAL,
             condition=EdgeCondition(field="score", operator="gt", value=50)),
        Edge(id="e2_low", source_id="decision", target_id="low", type=EdgeType.CONDITIONAL,
             condition=EdgeCondition(field="score", operator="lte", value=50)),
        Edge(id="e3", source_id="high", target_id="end"),
        Edge(id="e4", source_id="low", target_id="end"),
    ],
)
