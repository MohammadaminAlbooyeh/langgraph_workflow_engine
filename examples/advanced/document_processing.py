"""Document processing workflow"""
from backend.models.workflow import Workflow
from backend.models.node import Node, NodeConfig, NodeType
from backend.models.edge import Edge, EdgeType

workflow = Workflow(
    name="Document Processor",
    description="Process and analyze documents",
    type="document",
    nodes=[
        Node(id="input", type=NodeType.INPUT, name="Upload Document"),
        Node(id="extract", type=NodeType.TEXT_PROCESSOR, name="Extract Text",
             config=NodeConfig(custom_attributes={"operation": "lowercase"})),
        Node(id="analyze", type=NodeType.LLM, name="Analyze Content",
             config=NodeConfig(prompt_template="Analyze this document: {data}")),
        Node(id="summarize", type=NodeType.AGENT, name="Generate Summary",
             config=NodeConfig(system_prompt="Summarize the analyzed document.")),
        Node(id="output", type=NodeType.OUTPUT, name="Processed Document"),
    ],
    edges=[
        Edge(id="e1", source_id="input", target_id="extract"),
        Edge(id="e2", source_id="extract", target_id="analyze"),
        Edge(id="e3", source_id="analyze", target_id="summarize"),
        Edge(id="e4", source_id="summarize", target_id="output"),
    ],
)
