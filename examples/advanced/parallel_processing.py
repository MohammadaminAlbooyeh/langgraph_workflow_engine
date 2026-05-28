"""Parallel processing workflow"""
from backend.models.workflow import Workflow
from backend.models.node import Node, NodeConfig, NodeType
from backend.models.edge import Edge, EdgeType

workflow = Workflow(
    name="Parallel Processing",
    description="Execute multiple nodes concurrently",
    type="parallel",
    nodes=[
        Node(id="input", type=NodeType.INPUT, name="Input"),
        Node(id="branch_a", type=NodeType.LLM, name="Branch A",
             config=NodeConfig(prompt_template="Process in branch A: {data}")),
        Node(id="branch_b", type=NodeType.LLM, name="Branch B",
             config=NodeConfig(prompt_template="Process in branch B: {data}")),
        Node(id="branch_c", type=NodeType.LLM, name="Branch C",
             config=NodeConfig(prompt_template="Process in branch C: {data}")),
        Node(id="merge", type=NodeType.MERGE, name="Merge Results",
             config=NodeConfig(custom_attributes={"strategy": "dict_merge"})),
        Node(id="output", type=NodeType.OUTPUT, name="Combined Output"),
    ],
    edges=[
        Edge(id="e1", source_id="input", target_id="branch_a"),
        Edge(id="e2", source_id="input", target_id="branch_b"),
        Edge(id="e3", source_id="input", target_id="branch_c"),
        Edge(id="e4", source_id="branch_a", target_id="merge"),
        Edge(id="e5", source_id="branch_b", target_id="merge"),
        Edge(id="e6", source_id="branch_c", target_id="merge"),
        Edge(id="e7", source_id="merge", target_id="output"),
    ],
)
