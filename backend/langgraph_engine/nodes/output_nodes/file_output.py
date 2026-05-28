from backend.langgraph_engine.nodes.base_node import BaseNode
from backend.models.node import NodeType


class FileOutput(BaseNode):
    file_path: str = "output.json"
    file_format: str = "json"

    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        return {"output": inputs, "destination": "file", "file_path": self.file_path, "status": "written"}

    def _get_node_type(self) -> NodeType:
        return NodeType.OUTPUT
