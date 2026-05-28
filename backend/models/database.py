from datetime import datetime
from sqlalchemy import Column, String, Text, Float, Integer, DateTime, JSON, Enum as SAEnum
from sqlalchemy.orm import DeclarativeBase
from backend.models.workflow import WorkflowStatus, WorkflowType
from backend.models.node import NodeType
from backend.models.edge import EdgeType
from backend.models.execution import ExecutionStatus


class Base(DeclarativeBase):
    pass


class WorkflowModel(Base):
    __tablename__ = "workflows"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    type = Column(SAEnum(WorkflowType), default=WorkflowType.CUSTOM)
    status = Column(SAEnum(WorkflowStatus), default=WorkflowStatus.DRAFT)
    version = Column(String, default="0.1.0")
    nodes = Column(JSON, default=list)
    edges = Column(JSON, default=list)
    metadata_ = Column("metadata", JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String, nullable=True)


class NodeModel(Base):
    __tablename__ = "nodes"

    id = Column(String, primary_key=True)
    workflow_id = Column(String, nullable=False, index=True)
    type = Column(SAEnum(NodeType), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    config = Column(JSON, default=dict)
    position = Column(JSON, default=dict)
    inputs = Column(JSON, default=list)
    outputs = Column(JSON, default=list)
    metadata_ = Column("metadata", JSON, default=dict)


class EdgeModel(Base):
    __tablename__ = "edges"

    id = Column(String, primary_key=True)
    workflow_id = Column(String, nullable=False, index=True)
    source_id = Column(String, nullable=False)
    target_id = Column(String, nullable=False)
    type = Column(SAEnum(EdgeType), default=EdgeType.DIRECT)
    label = Column(String, nullable=True)
    condition = Column(JSON, nullable=True)
    priority = Column(Integer, default=0)
    metadata_ = Column("metadata", JSON, default=dict)


class ExecutionModel(Base):
    __tablename__ = "executions"

    id = Column(String, primary_key=True)
    workflow_id = Column(String, nullable=False, index=True)
    status = Column(SAEnum(ExecutionStatus), default=ExecutionStatus.PENDING)
    inputs = Column(JSON, default=dict)
    outputs = Column(JSON, default=dict)
    current_node_id = Column(String, nullable=True)
    node_results = Column(JSON, default=list)
    error = Column(Text, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    duration_ms = Column(Float, nullable=True)


__all__ = ["Base", "WorkflowModel", "NodeModel", "EdgeModel", "ExecutionModel"]
