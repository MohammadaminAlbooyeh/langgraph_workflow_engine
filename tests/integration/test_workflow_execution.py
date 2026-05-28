import pytest
from backend.services.workflow_service import WorkflowService
from backend.services.execution_service import ExecutionService


@pytest.mark.asyncio
async def test_create_and_get_workflow():
    svc = WorkflowService()
    wf = await svc.create({"name": "Test WF", "type": "custom"})
    assert wf.id is not None

    fetched = await svc.get(wf.id)
    assert fetched is not None
    assert fetched.name == "Test WF"


@pytest.mark.asyncio
async def test_workflow_crud():
    svc = WorkflowService()
    wf = await svc.create({"name": "CRUD Test"})
    assert wf is not None

    updated = await svc.update(wf.id, {"name": "Updated"})
    assert updated.name == "Updated"

    deleted = await svc.delete(wf.id)
    assert deleted is True

    assert await svc.get(wf.id) is None


@pytest.mark.asyncio
async def test_create_and_start_execution():
    wf_svc = WorkflowService()
    ex_svc = ExecutionService()

    wf = await wf_svc.create({
        "name": "Exec Test",
        "nodes": [{"id": "n1", "type": "input", "name": "Input"}],
        "edges": [],
    })

    ex = await ex_svc.create(wf.id, {"data": "test"})
    assert ex.id is not None
    assert ex.status.value == "pending"

    result = await ex_svc.start(ex.id, wf.nodes, wf.edges)
    assert result is not None
    assert result.status.value in ("completed", "failed")


@pytest.mark.asyncio
async def test_list_workflows():
    svc = WorkflowService()
    await svc.create({"name": "WF 1"})
    await svc.create({"name": "WF 2"})
    workflows = await svc.list()
    assert len(workflows) >= 2


@pytest.mark.asyncio
async def test_cancel_execution():
    svc = ExecutionService()
    ex = await svc.create("wf_1", {})
    cancelled = await svc.cancel(ex.id)
    assert cancelled is True

    fetched = await svc.get(ex.id)
    assert fetched.status.value == "cancelled"
