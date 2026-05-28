"""Agent workflow with tool integration"""
from backend.models.workflow import Workflow
from backend.models.node import Node, NodeConfig, NodeType
from backend.models.edge import Edge, EdgeType

workflow = Workflow(
    name="Agent with Tools",
    description="Agent that can use built-in tools",
    nodes=[
        Node(id="input", type=NodeType.INPUT, name="Query Input"),
        Node(id="tool_agent", type=NodeType.AGENT, name="Tool Agent",
             config=NodeConfig(
                 system_prompt="Use tools to answer the user's question.",
                 custom_attributes={"tools": ["calculate", "current_datetime", "format_text"]},
             )),
        Node(id="output", type=NodeType.OUTPUT, name="Answer"),
    ],
    edges=[
        Edge(id="e1", source_id="input", target_id="tool_agent"),
        Edge(id="e2", source_id="tool_agent", target_id="output"),
    ],
)
