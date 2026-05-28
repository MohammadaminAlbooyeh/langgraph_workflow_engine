import pytest
from backend.api.routes import workflow_service, execution_service


@pytest.mark.asyncio
async def test_health():
    from backend.main import app
    from httpx import AsyncClient, ASGITransport
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_create_workflow_api():
    from backend.main import app
    from httpx import AsyncClient, ASGITransport
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/workflows", json={"name": "API Test", "type": "custom"})
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "API Test"
        assert data["id"] is not None


@pytest.mark.asyncio
async def test_list_workflows_api():
    from backend.main import app
    from httpx import AsyncClient, ASGITransport
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/workflows")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
