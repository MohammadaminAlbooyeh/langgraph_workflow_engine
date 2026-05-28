from __future__ import annotations
from langgraph.graph import StateGraph, END
from backend.models.node import Node
from backend.models.edge import Edge


class GraphBuilder:
    def __init__(self):
        self._graph = StateGraph(dict)

    def build(self, nodes: list[Node], edges: list[Edge]):
        for node in nodes:
            if node.type in ("input",):
                self._graph.add_node(node.id, self._create_input_handler(node))
            elif node.type in ("output",):
                self._graph.add_node(node.id, self._create_output_handler(node))
            else:
                self._graph.add_node(node.id, self._create_default_handler(node))

        for edge in edges:
            if edge.type == "conditional" and edge.condition:
                fn = self._create_condition_fn(edge)
                self._graph.add_conditional_edges(
                    edge.source_id,
                    fn,
                    {edge.target_id: edge.target_id, END: END},
                )
            else:
                self._graph.add_edge(edge.source_id, edge.target_id)

        if nodes:
            self._graph.set_entry_point(nodes[0].id)

        return self._graph

    def _create_input_handler(self, node: Node):
        async def handler(state: dict) -> dict:
            return {"input": state.get("input", {})}
        return handler

    def _create_output_handler(self, node: Node):
        async def handler(state: dict) -> dict:
            return {"output": state.get("result", {})}
        return handler

    def _create_default_handler(self, node: Node):
        async def handler(state: dict) -> dict:
            return {f"{node.id}_result": state.get("data", {})}
        return handler

    def _create_condition_fn(self, edge: Edge):
        def condition(state: dict) -> str:
            if not edge.condition:
                return edge.target_id
            field_val = state.get(edge.condition.field)
            matched = False
            if edge.condition.operator == "equals":
                matched = field_val == edge.condition.value
            elif edge.condition.operator == "contains":
                matched = edge.condition.value in str(field_val)
            elif edge.condition.operator == "gt":
                matched = field_val is not None and field_val > edge.condition.value
            elif edge.condition.operator == "exists":
                matched = field_val is not None
            return edge.target_id if matched else END
        return condition

    def get_graph(self):
        return self._graph
