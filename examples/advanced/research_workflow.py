"""Research workflow with multiple agents"""
from backend.models.workflow import Workflow
from backend.models.node import Node, NodeConfig, NodeType
from backend.models.edge import Edge, EdgeType

workflow = Workflow(
    name="Research Workflow",
    description="Multi-step research and report generation",
    type="multi_agent",
    nodes=[
        Node(id="query", type=NodeType.INPUT, name="Research Query"),
        Node(id="planner", type=NodeType.AGENT, name="Research Planner",
             config=NodeConfig(system_prompt="Plan the research approach.")),
        Node(id="gatherer", type=NodeType.AGENT, name="Information Gatherer",
             config=NodeConfig(system_prompt="Gather relevant information.")),
        Node(id="analyst", type=NodeType.AGENT, name="Data Analyst",
             config=NodeConfig(system_prompt="Analyze gathered data.")),
        Node(id="writer", type=NodeType.AGENT, name="Report Writer",
             config=NodeConfig(system_prompt="Write the final report.")),
        Node(id="output", type=NodeType.OUTPUT, name="Research Report"),
    ],
    edges=[
        Edge(id="e1", source_id="query", target_id="planner"),
        Edge(id="e2", source_id="planner", target_id="gatherer"),
        Edge(id="e3", source_id="gatherer", target_id="analyst"),
        Edge(id="e4", source_id="analyst", target_id="writer"),
        Edge(id="e5", source_id="writer", target_id="output"),
    ],
)
