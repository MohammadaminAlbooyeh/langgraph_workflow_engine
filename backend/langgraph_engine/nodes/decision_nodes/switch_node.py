from backend.langgraph_engine.nodes.base_node import BaseNode
from backend.models.node import NodeType


class SwitchNode(BaseNode):
    switch_field: str = "choice"
    cases: dict[str, str] = {}
    default_case: str | None = None

    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        value = str(inputs.get(self.switch_field, ""))
        matched_case = self.cases.get(value, self.default_case)
        return {"matched_case": matched_case, "switch_value": value}

    def _get_node_type(self) -> NodeType:
        return NodeType.SWITCH
