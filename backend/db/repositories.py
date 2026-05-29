from __future__ import annotations
from typing import Optional, Any
from datetime import datetime, timezone
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.database import WorkflowModel, NodeModel, EdgeModel, ExecutionModel
from backend.models.workflow import Workflow, WorkflowStatus
from backend.models.execution import Execution, ExecutionStatus
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class WorkflowRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, data: dict) -> Workflow:
        model = WorkflowModel(
            id=data.get("id", f"wf_{datetime.now(timezone.utc).timestamp()}"),
            name=data["name"],
            description=data.get("description"),
            type=data.get("type", "custom"),
            status=data.get("status", "draft"),
            version=data.get("version", "0.1.0"),
            nodes=data.get("nodes", []),
            edges=data.get("edges", []),
            metadata_=data.get("metadata", {}),
            created_by=data.get("created_by"),
        )
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return self._model_to_pydantic(model)

    async def get(self, workflow_id: str) -> Optional[Workflow]:
        result = await self._session.execute(select(WorkflowModel).where(WorkflowModel.id == workflow_id))
        model = result.scalar_one_or_none()
        return self._model_to_pydantic(model) if model else None

    async def update(self, workflow_id: str, data: dict) -> Optional[Workflow]:
        result = await self._session.execute(select(WorkflowModel).where(WorkflowModel.id == workflow_id))
        model = result.scalar_one_or_none()
        if not model:
            return None
        for field in ("name", "description", "type", "status", "version"):
            if field in data:
                setattr(model, field, data[field])
        if "nodes" in data:
            model.nodes = data["nodes"]
        if "edges" in data:
            model.edges = data["edges"]
        if "metadata" in data:
            model.metadata_ = data["metadata"]
        model.updated_at = datetime.now(timezone.utc)
        await self._session.commit()
        await self._session.refresh(model)
        return self._model_to_pydantic(model)

    async def delete(self, workflow_id: str) -> bool:
        result = await self._session.execute(select(WorkflowModel).where(WorkflowModel.id == workflow_id))
        model = result.scalar_one_or_none()
        if not model:
            return False
        await self._session.delete(model)
        await self._session.commit()
        return True

    async def list(self, status: Optional[str] = None, type_: Optional[str] = None) -> list[Workflow]:
        query = select(WorkflowModel)
        if status:
            query = query.where(WorkflowModel.status == status)
        if type_:
            query = query.where(WorkflowModel.type == type_)
        result = await self._session.execute(query)
        models = result.scalars().all()
        return [self._model_to_pydantic(m) for m in models]

    def _model_to_pydantic(self, model: WorkflowModel) -> Workflow:
        return Workflow(
            id=model.id,
            name=model.name,
            description=model.description,
            type=model.type,
            status=model.status,
            version=model.version,
            nodes=model.nodes,
            edges=model.edges,
            metadata=model.metadata_,
            created_at=model.created_at,
            updated_at=model.updated_at,
            created_by=model.created_by,
        )


class ExecutionRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, data: dict) -> Execution:
        model = ExecutionModel(
            id=data["id"],
            workflow_id=data["workflow_id"],
            status=data.get("status", "pending"),
            inputs=data.get("inputs", {}),
            outputs=data.get("outputs", {}),
        )
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return self._model_to_pydantic(model)

    async def get(self, execution_id: str) -> Optional[Execution]:
        result = await self._session.execute(select(ExecutionModel).where(ExecutionModel.id == execution_id))
        model = result.scalar_one_or_none()
        return self._model_to_pydantic(model) if model else None

    async def update(self, execution_id: str, data: dict) -> Optional[Execution]:
        result = await self._session.execute(select(ExecutionModel).where(ExecutionModel.id == execution_id))
        model = result.scalar_one_or_none()
        if not model:
            return None
        for field in ("status", "inputs", "outputs", "current_node_id", "node_results", "error", "started_at", "completed_at", "duration_ms"):
            if field in data:
                setattr(model, field, data[field])
        await self._session.commit()
        await self._session.refresh(model)
        return self._model_to_pydantic(model)

    async def list(self, workflow_id: Optional[str] = None) -> list[Execution]:
        query = select(ExecutionModel)
        if workflow_id:
            query = query.where(ExecutionModel.workflow_id == workflow_id)
        query = query.order_by(ExecutionModel.started_at.desc().nullslast())
        result = await self._session.execute(query)
        models = result.scalars().all()
        return [self._model_to_pydantic(m) for m in models]

    def _model_to_pydantic(self, model: ExecutionModel) -> Execution:
        return Execution(
            id=model.id,
            workflow_id=model.workflow_id,
            status=model.status,
            inputs=model.inputs,
            outputs=model.outputs,
            current_node_id=model.current_node_id,
            node_results=[
                {"node_id": r["node_id"], "status": r["status"], "output": r.get("output"), "duration_ms": r.get("duration_ms", 0)}
                for r in (model.node_results or [])
            ],
            error=model.error,
            started_at=model.started_at,
            completed_at=model.completed_at,
            duration_ms=model.duration_ms,
        )
