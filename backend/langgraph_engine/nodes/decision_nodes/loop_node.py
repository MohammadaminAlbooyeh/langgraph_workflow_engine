from backend.langgraph_engine.nodes.base_node import BaseNode
from backend.models.node import NodeType


class LoopNode(BaseNode):
    max_iterations: int = 10
    loop_field: str = "data"

    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        items = inputs.get(self.loop_field, [])
        if isinstance(items, list):
            iteration_count = min(len(items), self.max_iterations)
        else:
            iteration_count = 1
        return {
            "iteration_count": iteration_count,
            "max_iterations": self.max_iterations,
            "items_processed": iteration_count,
            "should_continue": iteration_count > 0,
        }

    def _get_node_type(self) -> NodeType:
        return NodeType.LOOP
