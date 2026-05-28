from typing import Any, Optional
from pydantic import BaseModel, Field


class WorkflowCreate(BaseModel):
    name: str
    description: Optional[str] = None
    type: str = "custom"
    nodes: list[dict] = Field(default_factory=list)
    edges: list[dict] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    nodes: Optional[list[dict]] = None
    edges: Optional[list[dict]] = None
    metadata: Optional[dict[str, Any]] = None


class WorkflowResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    type: str
    status: str
    version: str
    nodes: list[dict]
    edges: list[dict]
    metadata: dict[str, Any]
    created_at: str
    updated_at: str
    created_by: Optional[str] = None


class ExecutionCreate(BaseModel):
    workflow_id: str
    inputs: dict[str, Any] = Field(default_factory=dict)


class ExecutionResponse(BaseModel):
    id: str
    workflow_id: str
    status: str
    inputs: dict[str, Any]
    outputs: dict[str, Any]
    current_node_id: Optional[str] = None
    node_results: list[dict]
    error: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    duration_ms: Optional[float] = None
    metadata: dict[str, Any]


class NodeCreate(BaseModel):
    id: str
    type: str
    name: str
    description: Optional[str] = None
    config: dict[str, Any] = Field(default_factory=dict)
    position: dict[str, float] = Field(default_factory=lambda: {"x": 0.0, "y": 0.0})
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)


class EdgeCreate(BaseModel):
    id: str
    source_id: str
    target_id: str
    type: str = "direct"
    label: Optional[str] = None
    condition: Optional[dict] = None
    priority: int = 0


class ApprovalAction(BaseModel):
    approval_id: str
    user: str
    reason: Optional[str] = None


class ToolExecute(BaseModel):
    name: str
    params: dict[str, Any] = Field(default_factory=dict)


class MessageResponse(BaseModel):
    message: str
    status: str = "success"
