from backend.langgraph_engine.nodes.base_node import BaseNode
from backend.models.node import NodeType


class AgentNode(BaseNode):
    system_prompt: str = "You are a helpful AI assistant."

    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        return {
            "agent_id": self.id,
            "response": f"[{self.name}] processed input with system prompt",
            "reasoning": "Simulated agent reasoning",
        }

    def _get_node_type(self) -> NodeType:
        return NodeType.AGENT


class PlannerAgent(AgentNode):
    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        return {"plan": f"[Planner {self.name}] created execution plan", "steps": []}


class ReasoningAgent(AgentNode):
    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        return {"reasoning": f"[Reasoning {self.name}] analyzed inputs", "conclusion": "Simulated conclusion"}


class ToolAgent(AgentNode):
    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        return {"tool_calls": [], "tool_results": {}, "agent_output": f"[ToolAgent {self.name}] completed"}
