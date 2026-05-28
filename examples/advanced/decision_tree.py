"""Decision tree workflow for classification"""
from backend.models.workflow import Workflow
from backend.models.node import Node, NodeConfig, NodeType
from backend.models.edge import Edge, EdgeType, EdgeCondition

workflow = Workflow(
    name="Decision Tree Classifier",
    description="Classify input using a decision tree",
    type="decision_tree",
    nodes=[
        Node(id="input", type=NodeType.INPUT, name="Input Data"),
        Node(id="classifier", type=NodeType.CONDITIONAL, name="Classify",
             config=NodeConfig(custom_attributes={"condition_field": "type", "operator": "equals"})),
        Node(id="cat_a", type=NodeType.LLM, name="Category A Handler",
             config=NodeConfig(prompt_template="Handle category A: {data}")),
        Node(id="cat_b", type=NodeType.LLM, name="Category B Handler",
             config=NodeConfig(prompt_template="Handle category B: {data}")),
        Node(id="output", type=NodeType.OUTPUT, name="Result"),
    ],
    edges=[
        Edge(id="e1", source_id="input", target_id="classifier"),
        Edge(id="e2", source_id="classifier", target_id="cat_a", type=EdgeType.CONDITIONAL,
             condition=EdgeCondition(field="type", operator="equals", value="A")),
        Edge(id="e3", source_id="classifier", target_id="cat_b", type=EdgeType.CONDITIONAL,
             condition=EdgeCondition(field="type", operator="equals", value="B")),
        Edge(id="e4", source_id="cat_a", target_id="output"),
        Edge(id="e5", source_id="cat_b", target_id="output"),
    ],
)
