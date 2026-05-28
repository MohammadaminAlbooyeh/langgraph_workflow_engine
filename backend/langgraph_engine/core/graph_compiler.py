from __future__ import annotations
from typing import Any, Optional
from backend.langgraph_engine.core.graph_builder import GraphBuilder
from backend.models.node import Node
from backend.models.edge import Edge
from config import langraph_config


class GraphCompiler:
    def __init__(self):
        self._compiled = None

    def compile(self, nodes: list[Node], edges: list[Edge]):
        builder = GraphBuilder()
        graph = builder.build(nodes, edges)
        self._compiled = graph.compile()
        return self._compiled

    async def run(self, initial_state: dict[str, Any]) -> dict[str, Any]:
        if not self._compiled:
            raise RuntimeError("Graph must be compiled before running")
        result = await self._compiled.ainvoke(initial_state)
        return result

    def stream(self, initial_state: dict[str, Any]):
        if not self._compiled:
            raise RuntimeError("Graph must be compiled before running")
        return self._compiled.astream(initial_state)

    def get_compiled_graph(self):
        return self._compiled
