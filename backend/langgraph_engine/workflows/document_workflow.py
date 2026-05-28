from backend.langgraph_engine.workflows.custom_workflow import CustomWorkflow


class DocumentWorkflow(CustomWorkflow):
    async def validate(self, nodes: list[dict], edges: list[dict]) -> list[str]:
        errors = await super().validate(nodes, edges)
        has_llm = any(n.get("type") in ("llm", "agent") for n in nodes)
        if not has_llm:
            errors.append("Document workflow should have at least one LLM or agent node")
        return errors
