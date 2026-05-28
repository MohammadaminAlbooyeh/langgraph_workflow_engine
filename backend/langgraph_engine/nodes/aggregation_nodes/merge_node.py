from backend.langgraph_engine.nodes.base_node import BaseNode
from backend.models.node import NodeType


class MergeNode(BaseNode):
    strategy: str = "dict_merge"

    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        return {"merged": inputs, "strategy": self.strategy}

    def _get_node_type(self) -> NodeType:
        return NodeType.MERGE
