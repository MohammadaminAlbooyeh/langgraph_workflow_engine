from __future__ import annotations
from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field


class EdgeType(str, Enum):
    DIRECT = "direct"
    CONDITIONAL = "conditional"
    DYNAMIC = "dynamic"
    EVENT = "event"


class EdgeCondition(BaseModel):
    field: str
    operator: str = "equals"
    value: Any = None
    expression: Optional[str] = None


class Edge(BaseModel):
    id: str
    source_id: str
    target_id: str
    type: EdgeType = EdgeType.DIRECT
    label: Optional[str] = None
    condition: Optional[EdgeCondition] = None
    priority: int = 0
    metadata: dict[str, Any] = Field(default_factory=dict)
