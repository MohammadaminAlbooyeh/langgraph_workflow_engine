from __future__ import annotations
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from backend.api.schemas import (
    WorkflowCreate, WorkflowUpdate, WorkflowResponse,
    ExecutionCreate, ExecutionResponse,
    NodeCreate, EdgeCreate, ApprovalAction, ToolExecute, MessageResponse,
)
from backend.services.workflow_service import WorkflowService
from backend.services.execution_service import ExecutionService
from backend.services.tool_service import ToolService
from backend.services.memory_service import MemoryService
from backend.services.monitoring_service import MonitoringService
from backend.services.orchestration_service import OrchestrationService
from backend.utils.logger import get_logger
from backend.models.workflow import WorkflowStatus
from backend.api.websocket_manager import manager
from backend.api.metrics import metrics_endpoint

logger = get_logger(__name__)

router = APIRouter()
workflow_service = WorkflowService()
execution_service = ExecutionService()
tool_service = ToolService()
memory_service = MemoryService()
monitoring_service = MonitoringService()
orchestration_service = OrchestrationService()


@router.post("/workflows", response_model=WorkflowResponse, status_code=201)
async def create_workflow(data: WorkflowCreate):
    workflow = await workflow_service.create(data.dict())
    return _workflow_to_response(workflow)


@router.get("/workflows", response_model=list[WorkflowResponse])
async def list_workflows(status: str | None = None, type: str | None = None):
    workflows = await workflow_service.list(status, type)
    return [_workflow_to_response(w) for w in workflows]


@router.get("/workflows/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(workflow_id: str):
    workflow = await workflow_service.get(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return _workflow_to_response(workflow)


@router.put("/workflows/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(workflow_id: str, data: WorkflowUpdate):
    workflow = await workflow_service.update(workflow_id, data.dict(exclude_unset=True))
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return _workflow_to_response(workflow)


@router.delete("/workflows/{workflow_id}", status_code=204)
async def delete_workflow(workflow_id: str):
    deleted = await workflow_service.delete(workflow_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Workflow not found")


@router.post("/workflows/{workflow_id}/nodes", response_model=WorkflowResponse)
async def add_node(workflow_id: str, node: NodeCreate):
    workflow = await workflow_service.add_node(workflow_id, node.dict())
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return _workflow_to_response(workflow)


@router.post("/workflows/{workflow_id}/edges", response_model=WorkflowResponse)
async def add_edge(workflow_id: str, edge: EdgeCreate):
    workflow = await workflow_service.add_edge(workflow_id, edge.dict())
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return _workflow_to_response(workflow)


@router.patch("/workflows/{workflow_id}/status", response_model=WorkflowResponse)
async def update_workflow_status(workflow_id: str, status: str):
    try:
        workflow_status = WorkflowStatus(status)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    workflow = await workflow_service.update_status(workflow_id, workflow_status)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return _workflow_to_response(workflow)


@router.post("/executions", response_model=ExecutionResponse, status_code=201)
async def create_execution(data: ExecutionCreate):
    execution = await execution_service.create(data.workflow_id, data.inputs)
    return _execution_to_response(execution)


@router.post("/executions/{execution_id}/start", response_model=ExecutionResponse)
async def start_execution(execution_id: str, nodes: list[dict] = [], edges: list[dict] = []):
    execution = await execution_service.get(execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    workflow = await workflow_service.get(execution.workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    execution = await execution_service.start(execution_id, nodes or workflow.nodes, edges or workflow.edges)
    return _execution_to_response(execution)


@router.get("/executions", response_model=list[ExecutionResponse])
async def list_executions(workflow_id: str | None = None):
    executions = await execution_service.list(workflow_id)
    return [_execution_to_response(e) for e in executions]


@router.get("/executions/{execution_id}", response_model=ExecutionResponse)
async def get_execution(execution_id: str):
    execution = await execution_service.get(execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    return _execution_to_response(execution)


@router.websocket("/ws/{workflow_id}")
async def workflow_websocket(websocket: WebSocket, workflow_id: str):
    await manager.connect(workflow_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(workflow_id, websocket)


@router.post("/executions/{execution_id}/cancel", response_model=MessageResponse)
async def cancel_execution(execution_id: str):
    cancelled = await execution_service.cancel(execution_id)
    if not cancelled:
        raise HTTPException(status_code=400, detail="Cannot cancel execution")
    return MessageResponse(message="Execution cancelled")


@router.post("/executions/{execution_id}/pause", response_model=MessageResponse)
async def pause_execution(execution_id: str):
    paused = await execution_service.pause(execution_id)
    if not paused:
        raise HTTPException(status_code=400, detail="Cannot pause execution")
    return MessageResponse(message="Execution paused")


@router.post("/executions/{execution_id}/resume", response_model=MessageResponse)
async def resume_execution(execution_id: str):
    resumed = await execution_service.resume(execution_id)
    if not resumed:
        raise HTTPException(status_code=400, detail="Cannot resume execution")
    return MessageResponse(message="Execution resumed")


@router.get("/tools", response_model=list[dict])
async def list_tools():
    return tool_service.list_tools()


@router.post("/tools/execute", response_model=dict)
async def execute_tool(data: ToolExecute):
    try:
        result = tool_service.execute_tool(data.name, **data.params)
        return {"result": result}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/tools/register", response_model=MessageResponse)
async def register_tool(name: str, description: str = "", parameters: list = []):
    tool_service.register_tool(name, lambda **kw: kw, description, parameters)
    return MessageResponse(message=f"Tool '{name}' registered")


@router.get("/approvals/pending", response_model=list[dict])
async def get_pending_approvals():
    return orchestration_service.get_pending_approvals()


@router.post("/approvals/approve", response_model=MessageResponse)
async def approve_action(data: ApprovalAction):
    approved = await orchestration_service.approve(data.approval_id, data.user)
    if not approved:
        raise HTTPException(status_code=400, detail="Cannot approve")
    return MessageResponse(message="Approved")


@router.post("/approvals/reject", response_model=MessageResponse)
async def reject_action(data: ApprovalAction):
    rejected = await orchestration_service.reject(data.approval_id, data.user, data.reason)
    if not rejected:
        raise HTTPException(status_code=400, detail="Cannot reject")
    return MessageResponse(message="Rejected")


@router.get("/monitoring/metrics", response_model=dict)
async def get_metrics(type: str | None = None):
    return monitoring_service.get_metrics(type)


@router.get("/monitoring/summary", response_model=dict)
async def get_summary():
    return monitoring_service.get_summary()


@router.get("/metrics")
async def get_metrics():
    return await metrics_endpoint()


@router.get("/health", response_model=dict)
async def health_check():
    return {"status": "healthy", "service": "langgraph-workflow-engine", "version": "0.1.0"}


def _workflow_to_response(w):
    return WorkflowResponse(
        id=w.id,
        name=w.name,
        description=w.description,
        type=w.type.value if hasattr(w.type, "value") else str(w.type),
        status=w.status.value if hasattr(w.status, "value") else str(w.status),
        version=w.version,
        nodes=w.nodes,
        edges=w.edges,
        metadata=w.metadata,
        created_at=w.created_at.isoformat() if hasattr(w.created_at, "isoformat") else str(w.created_at),
        updated_at=w.updated_at.isoformat() if hasattr(w.updated_at, "isoformat") else str(w.updated_at),
        created_by=w.created_by,
    )


def _execution_to_response(e):
    return ExecutionResponse(
        id=e.id,
        workflow_id=e.workflow_id,
        status=e.status.value if hasattr(e.status, "value") else str(e.status),
        inputs=e.inputs,
        outputs=e.outputs,
        current_node_id=e.current_node_id,
        node_results=[r.dict() if hasattr(r, "dict") else r for r in e.node_results],
        error=e.error,
        started_at=e.started_at.isoformat() if e.started_at and hasattr(e.started_at, "isoformat") else str(e.started_at) if e.started_at else None,
        completed_at=e.completed_at.isoformat() if e.completed_at and hasattr(e.completed_at, "isoformat") else str(e.completed_at) if e.completed_at else None,
        duration_ms=e.duration_ms,
        metadata=e.metadata,
    )
