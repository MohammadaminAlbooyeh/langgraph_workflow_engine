from backend.langgraph_engine.workflows.custom_workflow import CustomWorkflow


class DecisionTreeWorkflow(CustomWorkflow):
    async def validate(self, nodes: list[dict], edges: list[dict]) -> list[str]:
        errors = await super().validate(nodes, edges)
        has_decision = any(n.get("type") in ("conditional", "decision", "router", "switch") for n in nodes)
        if not has_decision:
            errors.append("Decision tree must have at least one decision/conditional node")
        return errors
