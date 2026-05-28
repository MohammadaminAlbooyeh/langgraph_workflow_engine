from backend.langgraph_engine.nodes.base_node import BaseNode
from backend.models.node import NodeType


class DataTransformer(BaseNode):
    transformation: str = "identity"

    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        return {"transformed": inputs.get("data", inputs), "transformation": self.transformation}

    def _get_node_type(self) -> NodeType:
        return NodeType.TRANSFORMER
