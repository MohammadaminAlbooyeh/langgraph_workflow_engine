"""Single agent workflow"""
from backend.models.workflow import Workflow
from backend.models.node import Node, NodeConfig, NodeType
from backend.models.edge import Edge, EdgeType

workflow = Workflow(
    name="Single Agent",
    description="A workflow with one autonomous agent",
    nodes=[
        Node(id="input", type=NodeType.INPUT, name="User Query"),
        Node(id="agent", type=NodeType.AGENT, name="AI Assistant",
             config=NodeConfig(
                 provider="openai", model="gpt-4-turbo-preview",
                 system_prompt="You are a helpful assistant that answers questions.",
             )),
        Node(id="output", type=NodeType.OUTPUT, name="Response"),
    ],
    edges=[
        Edge(id="e1", source_id="input", target_id="agent"),
        Edge(id="e2", source_id="agent", target_id="output"),
    ],
)
