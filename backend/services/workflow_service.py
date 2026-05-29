from __future__ import annotations
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.workflow import Workflow, WorkflowStatus
from backend.db.repositories import WorkflowRepository
from backend.db.session import get_session_sync
from backend.utils.helpers import generate_id
from backend.utils.logger import get_logger
from backend.utils.validators import validate_workflow

logger = get_logger(__name__)


class WorkflowService:
    def __init__(self, session: Optional[AsyncSession] = None):
        self._session = session
        self._workflows: dict[str, Workflow] = {}

    def _get_repo(self) -> Optional[WorkflowRepository]:
        if self._session is not None:
            return WorkflowRepository(self._session)
        return None

    async def create(self, data: dict) -> Workflow:
        errors = validate_workflow(data)
        if errors:
            raise ValueError(f"Validation failed: {', '.join(errors)}")

        workflow = Workflow(
            id=f"wf_{generate_id()}",
            name=data["name"],
            description=data.get("description"),
            type=data.get("type", "custom"),
            nodes=data.get("nodes", []),
            edges=data.get("edges", []),
            metadata=data.get("metadata", {}),
            created_by=data.get("created_by"),
        )

        repo = self._get_repo()
        if repo:
            workflow = await repo.create(data | {"id": workflow.id})
        else:
            self._workflows[workflow.id] = workflow

        logger.info(f"Created workflow: {workflow.id}")
        return workflow

    async def get(self, workflow_id: str) -> Optional[Workflow]:
        repo = self._get_repo()
        if repo:
            return await repo.get(workflow_id)
        return self._workflows.get(workflow_id)

    async def update(self, workflow_id: str, data: dict) -> Optional[Workflow]:
        repo = self._get_repo()
        if repo:
            return await repo.update(workflow_id, data)

        workflow = self._workflows.get(workflow_id)
        if not workflow:
            return None

        for field in ("name", "description", "type", "status", "nodes", "edges", "metadata"):
            if field in data:
                setattr(workflow, field, data[field])

        workflow.updated_at = datetime.now(timezone.utc)
        logger.info(f"Updated workflow: {workflow_id}")
        return workflow

    async def delete(self, workflow_id: str) -> bool:
        repo = self._get_repo()
        if repo:
            return await repo.delete(workflow_id)
        return self._workflows.pop(workflow_id, None) is not None

    async def list(self, status: Optional[str] = None, type_: Optional[str] = None) -> list[Workflow]:
        repo = self._get_repo()
        if repo:
            return await repo.list(status, type_)

        results = list(self._workflows.values())
        if status:
            results = [w for w in results if w.status.value == status]
        if type_:
            results = [w for w in results if w.type.value == type_]
        return results

    async def add_node(self, workflow_id: str, node: dict) -> Optional[Workflow]:
        workflow = await self.get(workflow_id)
        if not workflow:
            return None
        nodes = list(workflow.nodes)
        nodes.append(node)
        return await self.update(workflow_id, {"nodes": nodes})

    async def add_edge(self, workflow_id: str, edge: dict) -> Optional[Workflow]:
        workflow = await self.get(workflow_id)
        if not workflow:
            return None
        edges = list(workflow.edges)
        edges.append(edge)
        return await self.update(workflow_id, {"edges": edges})

    async def update_status(self, workflow_id: str, status: WorkflowStatus) -> Optional[Workflow]:
        return await self.update(workflow_id, {"status": status.value})
