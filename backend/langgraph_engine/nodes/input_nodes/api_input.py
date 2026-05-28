from backend.langgraph_engine.nodes.base_node import BaseNode
from backend.models.node import NodeType


class ApiInput(BaseNode):
    endpoint: str = ""
    method: str = "GET"

    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        return {"data": inputs, "source": "api", "endpoint": self.endpoint}

    def _get_node_type(self) -> NodeType:
        return NodeType.INPUT
