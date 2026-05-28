"""Hierarchical multi-agent workflow"""
from backend.models.workflow import Workflow
from backend.models.node import Node, NodeConfig, NodeType
from backend.models.edge import Edge, EdgeType

workflow = Workflow(
    name="Hierarchical Agents",
    description="Manager agent delegates to specialized sub-agents",
    nodes=[
        Node(id="input", type=NodeType.INPUT, name="Request"),
        Node(id="manager", type=NodeType.AGENT, name="Manager",
             config=NodeConfig(system_prompt="You are a manager. Delegate tasks to specialists.")),
        Node(id="coder", type=NodeType.AGENT, name="Coder",
             config=NodeConfig(system_prompt="Write code to solve problems.")),
        Node(id="analyst", type=NodeType.AGENT, name="Analyst",
             config=NodeConfig(system_prompt="Analyze data and provide insights.")),
        Node(id="aggregator", type=NodeType.AGGREGATE, name="Combine Results"),
        Node(id="output", type=NodeType.OUTPUT, name="Final Output"),
    ],
    edges=[
        Edge(id="e1", source_id="input", target_id="manager"),
        Edge(id="e2", source_id="manager", target_id="coder"),
        Edge(id="e3", source_id="manager", target_id="analyst"),
        Edge(id="e4", source_id="coder", target_id="aggregator"),
        Edge(id="e5", source_id="analyst", target_id="aggregator"),
        Edge(id="e6", source_id="aggregator", target_id="output"),
    ],
)
