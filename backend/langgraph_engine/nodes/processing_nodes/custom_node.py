from typing import Any
from backend.langgraph_engine.nodes.base_node import BaseNode
from backend.models.node import NodeType


class CustomNode(BaseNode):
    handler_code: str = ""

    async def execute(self, inputs: dict, context: dict | None = None) -> Any:
        return {"result": f"[Custom {self.name}] executed", "input": inputs}

    def _get_node_type(self) -> NodeType:
        return NodeType.CUSTOM
