from backend.langgraph_engine.nodes.base_node import BaseNode
from backend.models.node import NodeType


class ConditionalNode(BaseNode):
    condition_field: str = "input"
    condition_value: object = True
    operator: str = "equals"

    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        field_value = inputs.get(self.condition_field)
        if self.operator == "equals":
            result = field_value == self.condition_value
        elif self.operator == "contains":
            result = self.condition_value in str(field_value)
        elif self.operator == "exists":
            result = field_value is not None
        else:
            result = True
        return {"condition_result": result, "matched": result}

    def _get_node_type(self) -> NodeType:
        return NodeType.CONDITIONAL
