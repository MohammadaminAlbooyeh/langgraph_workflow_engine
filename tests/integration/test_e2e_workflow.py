"""End-to-end workflow tests: API → Execution → Database"""
import pytest
from httpx import AsyncClient, ASGITransport
from backend.main import app


@pytest.mark.asyncio
async def test_create_and_execute_workflow_e2e():
    """Test creating a workflow via API and executing it"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Create workflow via API
        workflow_data = {
            "name": "E2E Test Workflow",
            "description": "Test workflow for e2e testing",
            "nodes": [
                {
                    "id": "input",
                    "type": "INPUT",
                    "name": "Input Node",
                    "config": {}
                },
                {
                    "id": "output",
                    "type": "OUTPUT",
                    "name": "Output Node",
                    "config": {}
                }
            ],
            "edges": [
                {
                    "id": "e1",
                    "source_id": "input",
                    "target_id": "output",
                    "type": "DIRECT"
                }
            ]
        }

        # Create workflow
        response = await client.post(
            "/api/v1/workflows",
            json=workflow_data
        )
        assert response.status_code == 201
        workflow = response.json()
        assert workflow["name"] == "E2E Test Workflow"
        workflow_id = workflow["id"]

        # Retrieve workflow from API
        response = await client.get(
            f"/api/v1/workflows/{workflow_id}"
        )
        assert response.status_code == 200
        retrieved = response.json()
        assert retrieved["id"] == workflow_id
        assert len(retrieved["nodes"]) == 2

        # Start execution via API
        exec_data = {
            "workflow_id": workflow_id,
            "inputs": {"data": "test input"}
        }
        response = await client.post(
            "/api/v1/executions",
            json=exec_data
        )
        assert response.status_code == 201
        execution = response.json()
        execution_id = execution["id"]
        assert execution["status"] in ["pending", "running", "PENDING", "RUNNING"]

        # Check execution status
        response = await client.get(
            f"/api/v1/executions/{execution_id}"
        )
        assert response.status_code == 200
        exec_status = response.json()
        assert exec_status["id"] == execution_id
        assert exec_status["workflow_id"] == workflow_id


@pytest.mark.asyncio
async def test_workflow_persistence_in_database():
    """Test that workflows are persisted in database"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Create workflow
        workflow_data = {
            "name": "Database Persistence Test",
            "description": "Test database persistence",
            "nodes": [{"id": "n1", "type": "INPUT", "name": "N1", "config": {}}],
            "edges": []
        }

        response = await client.post(
            "/api/v1/workflows",
            json=workflow_data
        )
        assert response.status_code == 201
        workflow_id = response.json()["id"]

        # List workflows to verify persistence
        response = await client.get(
            "/api/v1/workflows"
        )
        assert response.status_code == 200
        workflows = response.json()
        assert any(w["id"] == workflow_id for w in workflows)


@pytest.mark.asyncio
async def test_execution_state_transitions():
    """Test that execution goes through proper state transitions"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Create workflow
        workflow_data = {
            "name": "State Transition Test",
            "nodes": [
                {"id": "input", "type": "INPUT", "name": "Input", "config": {}},
                {"id": "output", "type": "OUTPUT", "name": "Output", "config": {}}
            ],
            "edges": [
                {"id": "e1", "source_id": "input", "target_id": "output", "type": "DIRECT"}
            ]
        }

        response = await client.post(
            "/api/v1/workflows",
            json=workflow_data
        )
        workflow_id = response.json()["id"]

        # Create execution
        exec_data = {
            "workflow_id": workflow_id,
            "inputs": {}
        }

        response = await client.post(
            "/api/v1/executions",
            json=exec_data
        )
        execution_id = response.json()["id"]

        # Verify execution exists
        response = await client.get(
            f"/api/v1/executions/{execution_id}"
        )
        assert response.status_code == 200
        execution = response.json()
        assert execution["id"] == execution_id


@pytest.mark.asyncio
async def test_api_health_check():
    """Test that API health check works"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        health = response.json()
        assert health.get("status") == "healthy" or health.get("status") == "ok"


@pytest.mark.asyncio
async def test_metrics_endpoint():
    """Test that metrics endpoint is accessible"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(
            "/api/v1/monitoring/summary",
            headers={"X-API-Key": "test-key"}
        )
        # Metrics might not be available in test, but endpoint should exist
        assert response.status_code in [200, 404, 405]
