from backend.langgraph_engine.nodes.base_node import BaseNode
from backend.models.node import NodeType


class CombineNode(BaseNode):
    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        combined = {}
        for key, value in inputs.items():
            if isinstance(value, dict):
                combined.update(value)
            else:
                combined[key] = value
        return {"combined": combined}

    def _get_node_type(self) -> NodeType:
        return NodeType.COMBINE
