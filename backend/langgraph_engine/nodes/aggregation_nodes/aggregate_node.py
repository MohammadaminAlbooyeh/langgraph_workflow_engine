from backend.langgraph_engine.nodes.base_node import BaseNode
from backend.models.node import NodeType


class AggregateNode(BaseNode):
    aggregation_field: str = "results"

    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        return {"aggregated": inputs, "count": len(inputs)}

    def _get_node_type(self) -> NodeType:
        return NodeType.AGGREGATE
