from pydantic import BaseModel, Field
from typing import Any, Optional
from backend.models.edge import Edge, EdgeType


class BaseEdge(BaseModel):
    id: str
    source_id: str
    target_id: str
    label: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    def to_edge_model(self) -> Edge:
        return Edge(
            id=self.id,
            source_id=self.source_id,
            target_id=self.target_id,
            type=EdgeType.DIRECT,
            label=self.label,
            metadata=self.metadata,
        )
