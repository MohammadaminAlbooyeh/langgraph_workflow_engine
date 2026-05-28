"""Simple linear workflow: Input -> Process -> Output"""
from backend.models.workflow import Workflow
from backend.models.node import Node, NodeConfig, NodeType
from backend.models.edge import Edge, EdgeType

workflow = Workflow(
    name="Simple Workflow",
    description="A basic linear workflow with input, processing, and output",
    nodes=[
        Node(id="input", type=NodeType.INPUT, name="User Input", config=NodeConfig()),
        Node(id="process", type=NodeType.LLM, name="LLM Processor", config=NodeConfig(
            provider="openai", temperature=0.7, prompt_template="Process: {data}"
        )),
        Node(id="output", type=NodeType.OUTPUT, name="Final Output", config=NodeConfig()),
    ],
    edges=[
        Edge(id="e1", source_id="input", target_id="process"),
        Edge(id="e2", source_id="process", target_id="output"),
    ],
)
