"""Content generation workflow"""
from backend.models.workflow import Workflow
from backend.models.node import Node, NodeConfig, NodeType
from backend.models.edge import Edge, EdgeType

workflow = Workflow(
    name="Content Generation",
    description="Multi-stage content creation pipeline",
    nodes=[
        Node(id="brief", type=NodeType.INPUT, name="Content Brief"),
        Node(id="outline", type=NodeType.AGENT, name="Outline Creator",
             config=NodeConfig(system_prompt="Create a detailed outline.")),
        Node(id="draft", type=NodeType.AGENT, name="Draft Writer",
             config=NodeConfig(system_prompt="Write the first draft.")),
        Node(id="editor", type=NodeType.AGENT, name="Editor",
             config=NodeConfig(system_prompt="Edit and improve the draft.")),
        Node(id="formatter", type=NodeType.TEXT_PROCESSOR, name="Format Output",
             config=NodeConfig(custom_attributes={"operation": "title"})),
        Node(id="output", type=NodeType.OUTPUT, name="Final Content"),
    ],
    edges=[
        Edge(id="e1", source_id="brief", target_id="outline"),
        Edge(id="e2", source_id="outline", target_id="draft"),
        Edge(id="e3", source_id="draft", target_id="editor"),
        Edge(id="e4", source_id="editor", target_id="formatter"),
        Edge(id="e5", source_id="formatter", target_id="output"),
    ],
)
