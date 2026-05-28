"""Customer support ticket triage workflow"""
from backend.models.workflow import Workflow
from backend.models.node import Node, NodeConfig, NodeType
from backend.models.edge import Edge, EdgeType, EdgeCondition

workflow = Workflow(
    name="Customer Support Triage",
    description="Automated support ticket classification and routing",
    nodes=[
        Node(id="ticket", type=NodeType.INPUT, name="Support Ticket"),
        Node(id="classifier", type=NodeType.AGENT, name="Ticket Classifier",
             config=NodeConfig(system_prompt="Classify the ticket by category and urgency.")),
        Node(id="billing", type=NodeType.AGENT, name="Billing Specialist",
             config=NodeConfig(system_prompt="Handle billing inquiries.")),
        Node(id="tech", type=NodeType.AGENT, name="Technical Support",
             config=NodeConfig(system_prompt="Resolve technical issues.")),
        Node(id="general", type=NodeType.AGENT, name="General Support",
             config=NodeConfig(system_prompt="Handle general inquiries.")),
        Node(id="output", type=NodeType.OUTPUT, name="Resolution"),
    ],
    edges=[
        Edge(id="e1", source_id="ticket", target_id="classifier"),
        Edge(id="e2", source_id="classifier", target_id="billing", type=EdgeType.CONDITIONAL,
             condition=EdgeCondition(field="category", operator="equals", value="billing")),
        Edge(id="e3", source_id="classifier", target_id="tech", type=EdgeType.CONDITIONAL,
             condition=EdgeCondition(field="category", operator="equals", value="technical")),
        Edge(id="e4", source_id="classifier", target_id="general", type=EdgeType.CONDITIONAL,
             condition=EdgeCondition(field="category", operator="equals", value="general")),
        Edge(id="e5", source_id="billing", target_id="output"),
        Edge(id="e6", source_id="tech", target_id="output"),
        Edge(id="e7", source_id="general", target_id="output"),
    ],
)
