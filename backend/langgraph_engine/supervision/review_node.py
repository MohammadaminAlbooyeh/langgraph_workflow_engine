from __future__ import annotations
from typing import Any, Optional
from pydantic import BaseModel, Field


class ReviewNode(BaseModel):
    id: str
    execution_id: str
    node_id: str
    status: str = "pending"
    reviewer: Optional[str] = None
    comments: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)
