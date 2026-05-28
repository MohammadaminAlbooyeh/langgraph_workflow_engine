from backend.langgraph_engine.nodes.base_node import BaseNode
from backend.models.node import NodeType


class DatabaseOutput(BaseNode):
    table: str = ""
    connection_id: str = "default"

    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        return {"output": inputs, "destination": "database", "table": self.table, "status": "saved"}

    def _get_node_type(self) -> NodeType:
        return NodeType.OUTPUT
