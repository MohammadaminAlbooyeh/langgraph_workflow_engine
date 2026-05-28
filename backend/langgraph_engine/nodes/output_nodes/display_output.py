from backend.langgraph_engine.nodes.base_node import BaseNode
from backend.models.node import NodeType


class DisplayOutput(BaseNode):
    format: str = "json"

    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        return {"output": inputs, "destination": "display", "format": self.format}

    def _get_node_type(self) -> NodeType:
        return NodeType.OUTPUT
