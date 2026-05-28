"""Code review automation workflow"""
from backend.models.workflow import Workflow
from backend.models.node import Node, NodeConfig, NodeType
from backend.models.edge import Edge, EdgeType

workflow = Workflow(
    name="Code Review Pipeline",
    description="Automated code review with AI agents",
    nodes=[
        Node(id="input", type=NodeType.INPUT, name="Code Submission"),
        Node(id="linter", type=NodeType.TRANSFORMER, name="Lint Check",
             config=NodeConfig(custom_attributes={"transformation": "validate_syntax"})),
        Node(id="reviewer", type=NodeType.AGENT, name="Code Reviewer",
             config=NodeConfig(system_prompt="Review the code for bugs, style issues, and security concerns.")),
        Node(id="suggester", type=NodeType.AGENT, name="Improvement Suggester",
             config=NodeConfig(system_prompt="Suggest specific improvements.")),
        Node(id="output", type=NodeType.OUTPUT, name="Review Report"),
    ],
    edges=[
        Edge(id="e1", source_id="input", target_id="linter"),
        Edge(id="e2", source_id="linter", target_id="reviewer"),
        Edge(id="e3", source_id="reviewer", target_id="suggester"),
        Edge(id="e4", source_id="suggester", target_id="output"),
    ],
)
