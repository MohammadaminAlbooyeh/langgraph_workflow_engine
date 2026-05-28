from backend.langgraph_engine.nodes.base_node import BaseNode
from backend.models.node import NodeType


class FileInput(BaseNode):
    file_path: str = ""
    file_format: str = "json"

    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        return {"data": inputs, "source": "file", "file_path": self.file_path}

    def _get_node_type(self) -> NodeType:
        return NodeType.INPUT
