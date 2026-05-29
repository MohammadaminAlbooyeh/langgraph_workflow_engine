from backend.langgraph_engine.nodes.base_node import BaseNode
from backend.models.node import NodeType


class AgentNode(BaseNode):
    system_prompt: str = "You are a helpful AI assistant."

    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        from backend.llm.llm_factory import LLMFactory
        provider = self.config.provider if self.config else None
        user_input = str(inputs.get("input", inputs))
        llm = LLMFactory.create(provider)
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_input},
        ]
        response = await llm.invoke(messages)
        return {
            "agent_id": self.id,
            "response": response,
            "reasoning": f"Processed by {provider or 'default'} LLM",
        }

    def _get_node_type(self) -> NodeType:
        return NodeType.AGENT


class PlannerAgent(AgentNode):
    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        from backend.llm.llm_factory import LLMFactory
        provider = self.config.provider if self.config else None
        goal = str(inputs.get("goal", inputs))
        llm = LLMFactory.create(provider)
        messages = [
            {"role": "system", "content": "You are a planner. Break down the given goal into steps."},
            {"role": "user", "content": goal},
        ]
        response = await llm.invoke(messages)
        return {"plan": response, "steps": [s.strip() for s in response.split("\n") if s.strip()]}


class ReasoningAgent(AgentNode):
    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        from backend.llm.llm_factory import LLMFactory
        provider = self.config.provider if self.config else None
        problem = str(inputs.get("problem", inputs))
        llm = LLMFactory.create(provider)
        messages = [
            {"role": "system", "content": "You are a reasoning agent. Analyze the problem step by step."},
            {"role": "user", "content": problem},
        ]
        response = await llm.invoke(messages)
        return {"reasoning": response, "conclusion": response.split(". ")[-1] if ". " in response else response}


class ToolAgent(AgentNode):
    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        from backend.llm.llm_factory import LLMFactory
        provider = self.config.provider if self.config else None
        task = str(inputs.get("task", inputs))
        llm = LLMFactory.create(provider)
        messages = [
            {"role": "system", "content": "You are a tool-using agent. Determine which tools to use and respond."},
            {"role": "user", "content": task},
        ]
        response = await llm.invoke(messages)
        return {"tool_calls": [], "tool_results": {}, "agent_output": response}
