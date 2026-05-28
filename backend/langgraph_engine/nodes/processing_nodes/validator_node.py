from backend.langgraph_engine.nodes.base_node import BaseNode
from backend.models.node import NodeType


class ValidatorNode(BaseNode):
    validation_schema: dict = {}

    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        is_valid = bool(inputs.get("data")) if "data" in inputs else True
        return {
            "valid": is_valid,
            "errors": [] if is_valid else ["Validation failed"],
            "validated_data": inputs,
        }

    def _get_node_type(self) -> NodeType:
        return NodeType.VALIDATOR
