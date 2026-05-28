from typing import Any, Optional
from backend.langgraph_engine.edges.base_edge import BaseEdge
from backend.models.edge import Edge, EdgeType


class DynamicEdge(BaseEdge):
    resolver_function: Optional[str] = None

    def resolve_target(self, state: dict[str, Any]) -> str:
        if self.resolver_function and "target_key" in state:
            resolved = state.get(state["target_key"])
            if resolved:
                return resolved
        return self.target_id

    def to_edge_model(self) -> Edge:
        return Edge(
            id=self.id,
            source_id=self.source_id,
            target_id=self.target_id,
            type=EdgeType.DYNAMIC,
            label=self.label,
            metadata={**self.metadata, "resolver_function": self.resolver_function} if self.resolver_function else self.metadata,
        )
