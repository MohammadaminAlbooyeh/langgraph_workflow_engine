"""Multi-agent collaborative workflow"""
from backend.models.workflow import Workflow
from backend.models.node import Node, NodeConfig, NodeType
from backend.models.edge import Edge, EdgeType

workflow = Workflow(
    name="Multi-Agent Collaboration",
    description="Multiple agents working together on a task",
    nodes=[
        Node(id="input", type=NodeType.INPUT, name="Task Input"),
        Node(id="researcher", type=NodeType.AGENT, name="Researcher",
             config=NodeConfig(system_prompt="Research the topic thoroughly.")),
        Node(id="writer", type=NodeType.AGENT, name="Writer",
             config=NodeConfig(system_prompt="Write based on research findings.")),
        Node(id="reviewer", type=NodeType.AGENT, name="Reviewer",
             config=NodeConfig(system_prompt="Review and improve the output.")),
        Node(id="output", type=NodeType.OUTPUT, name="Final Output"),
    ],
    edges=[
        Edge(id="e1", source_id="input", target_id="researcher"),
        Edge(id="e2", source_id="researcher", target_id="writer"),
        Edge(id="e3", source_id="writer", target_id="reviewer"),
        Edge(id="e4", source_id="reviewer", target_id="output"),
    ],
)
