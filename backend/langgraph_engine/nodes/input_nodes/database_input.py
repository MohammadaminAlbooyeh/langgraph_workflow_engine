from backend.langgraph_engine.nodes.base_node import BaseNode
from backend.models.node import NodeType


class DatabaseInput(BaseNode):
    query: str = ""
    connection_id: str = "default"

    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        return {"data": inputs, "source": "database", "query": self.query}

    def _get_node_type(self) -> NodeType:
        return NodeType.INPUT
