from backend.langgraph_engine.nodes.base_node import BaseNode
from backend.models.node import NodeType


class ApiOutput(BaseNode):
    endpoint: str = ""
    method: str = "POST"

    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        return {"output": inputs, "destination": "api", "endpoint": self.endpoint, "status": "sent"}

    def _get_node_type(self) -> NodeType:
        return NodeType.OUTPUT
