from __future__ import annotations
from enum import Enum
from typing import Optional, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class ExecutionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    APPROVAL_REQUIRED = "approval_required"


class ExecutionResult(BaseModel):
    node_id: str
    node_name: str
    status: ExecutionStatus
    output: Any = None
    error: Optional[str] = None
    duration_ms: float = 0.0
    tokens_used: Optional[int] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Execution(BaseModel):
    id: str
    workflow_id: str
    status: ExecutionStatus = ExecutionStatus.PENDING
    inputs: dict[str, Any] = Field(default_factory=dict)
    outputs: dict[str, Any] = Field(default_factory=dict)
    current_node_id: Optional[str] = None
    node_results: list[ExecutionResult] = Field(default_factory=list)
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_ms: Optional[float] = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    def to_dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        for key in ("started_at", "completed_at", "timestamp"):
            if isinstance(d.get(key), datetime):
                d[key] = d[key].isoformat()
        return d
