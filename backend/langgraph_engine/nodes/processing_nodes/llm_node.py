from backend.langgraph_engine.nodes.base_node import BaseNode
from backend.models.node import NodeType


class LLMNode(BaseNode):
    prompt_template: str = ""
    system_prompt: str = ""
    provider: str = "openai"
    model: str = "gpt-4-turbo-preview"

    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        formatted_prompt = self.prompt_template.format(**inputs) if inputs else self.prompt_template
        return {
            "response": f"[LLM response for: {formatted_prompt[:50]}...]",
            "provider": self.provider,
            "model": self.model,
        }

    def _get_node_type(self) -> NodeType:
        return NodeType.LLM
