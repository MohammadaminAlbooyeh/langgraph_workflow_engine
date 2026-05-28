"""Looping workflow processing items in a list"""
from backend.models.workflow import Workflow
from backend.models.node import Node, NodeConfig, NodeType
from backend.models.edge import Edge, EdgeType

workflow = Workflow(
    name="Looping Workflow",
    description="Processes items in a list iteratively",
    nodes=[
        Node(id="start", type=NodeType.INPUT, name="Start"),
        Node(id="loop", type=NodeType.LOOP, name="Process Items",
             config=NodeConfig(custom_attributes={"loop_field": "items", "max_iterations": 10})),
        Node(id="process", type=NodeType.TRANSFORMER, name="Transform Item"),
        Node(id="end", type=NodeType.OUTPUT, name="End"),
    ],
    edges=[
        Edge(id="e1", source_id="start", target_id="loop"),
        Edge(id="e2", source_id="loop", target_id="process"),
        Edge(id="e3", source_id="process", target_id="end"),
    ],
)
