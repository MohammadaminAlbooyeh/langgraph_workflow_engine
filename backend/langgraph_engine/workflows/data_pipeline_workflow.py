from backend.langgraph_engine.workflows.custom_workflow import CustomWorkflow


class DataPipelineWorkflow(CustomWorkflow):
    async def validate(self, nodes: list[dict], edges: list[dict]) -> list[str]:
        errors = await super().validate(nodes, edges)
        has_input = any(n.get("type") in ("input", "api_input", "file_input") for n in nodes)
        has_output = any(n.get("type") == "output" or n.get("type", "").endswith("_output") for n in nodes)
        if not has_input:
            errors.append("Data pipeline must have at least one input node")
        if not has_output:
            errors.append("Data pipeline must have at least one output node")
        return errors
