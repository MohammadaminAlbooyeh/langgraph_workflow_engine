from typing import Any, Optional
from backend.langgraph_engine.edges.base_edge import BaseEdge
from backend.models.edge import Edge, EdgeType


class EventEdge(BaseEdge):
    event_type: str = "*"

    def matches_event(self, event_type: str) -> bool:
        return self.event_type == "*" or self.event_type == event_type

    def to_edge_model(self) -> Edge:
        return Edge(
            id=self.id,
            source_id=self.source_id,
            target_id=self.target_id,
            type=EdgeType.EVENT,
            label=self.label,
            metadata={**self.metadata, "event_type": self.event_type},
        )
