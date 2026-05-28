from __future__ import annotations
from enum import Enum
from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field


class WorkflowStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"
    ERROR = "error"


class WorkflowType(str, Enum):
    CUSTOM = "custom"
    DATA_PIPELINE = "data_pipeline"
    DECISION_TREE = "decision_tree"
    DOCUMENT = "document"
    MULTI_AGENT = "multi_agent"
    PARALLEL = "parallel"


class Workflow(BaseModel):
    id: str = Field(default_factory=lambda: f"wf_{datetime.utcnow().timestamp()}")
    name: str
    description: Optional[str] = None
    type: WorkflowType = WorkflowType.CUSTOM
    status: WorkflowStatus = WorkflowStatus.DRAFT
    version: str = "0.1.0"
    nodes: list[dict[str, Any]] = Field(default_factory=list)
    edges: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None

    def to_dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        if isinstance(d.get("created_at"), datetime):
            d["created_at"] = d["created_at"].isoformat()
        if isinstance(d.get("updated_at"), datetime):
            d["updated_at"] = d["updated_at"].isoformat()
        return d
