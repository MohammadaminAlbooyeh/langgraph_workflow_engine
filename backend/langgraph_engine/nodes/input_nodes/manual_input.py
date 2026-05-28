from backend.langgraph_engine.nodes.base_node import BaseNode
from backend.models.node import NodeType


class ManualInput(BaseNode):
    default_data: dict = {}

    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        return {"data": inputs.get("data", self.default_data), "source": "manual"}

    def _get_node_type(self) -> NodeType:
        return NodeType.INPUT
