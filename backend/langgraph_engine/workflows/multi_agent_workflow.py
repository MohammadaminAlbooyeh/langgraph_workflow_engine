from backend.langgraph_engine.workflows.custom_workflow import CustomWorkflow


class MultiAgentWorkflow(CustomWorkflow):
    async def validate(self, nodes: list[dict], edges: list[dict]) -> list[str]:
        errors = await super().validate(nodes, edges)
        agent_nodes = [n for n in nodes if n.get("type") == "agent"]
        if len(agent_nodes) < 2:
            errors.append("Multi-agent workflow must have at least 2 agent nodes")
        return errors
