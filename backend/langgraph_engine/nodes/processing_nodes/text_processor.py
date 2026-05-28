from backend.langgraph_engine.nodes.base_node import BaseNode
from backend.models.node import NodeType


class TextProcessor(BaseNode):
    operation: str = "lowercase"

    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        text = str(inputs.get("text", ""))
        if self.operation == "lowercase":
            result = text.lower()
        elif self.operation == "uppercase":
            result = text.upper()
        elif self.operation == "title":
            result = text.title()
        elif self.operation == "trim":
            result = text.strip()
        else:
            result = text
        return {"processed_text": result, "operation": self.operation}

    def _get_node_type(self) -> NodeType:
        return NodeType.TEXT_PROCESSOR
