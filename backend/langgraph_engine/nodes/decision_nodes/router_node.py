from backend.langgraph_engine.nodes.base_node import BaseNode
from backend.models.node import NodeType


class RouterNode(BaseNode):
    routing_field: str = "category"
    routes: dict[str, str] = {}

    async def execute(self, inputs: dict, context: dict | None = None) -> dict:
        route_key = str(inputs.get(self.routing_field, ""))
        selected_route = self.routes.get(route_key, list(self.routes.values())[0] if self.routes else None)
        return {"selected_route": selected_route, "route_key": route_key}

    def _get_node_type(self) -> NodeType:
        return NodeType.ROUTER
