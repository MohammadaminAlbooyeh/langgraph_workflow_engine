"""Test a workflow execution via the API."""
import asyncio
import httpx

BASE_URL = "http://localhost:8000/api/v1"


async def test_workflow():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        wf = await client.post("/workflows", json={
            "name": "Test Workflow",
            "nodes": [
                {"id": "n1", "type": "input", "name": "Input"},
                {"id": "n2", "type": "output", "name": "Output"},
            ],
            "edges": [{"id": "e1", "source_id": "n1", "target_id": "n2"}],
        })
        wf_id = wf.json()["id"]
        print(f"Created workflow: {wf_id}")

        exec_ = await client.post("/executions", json={"workflow_id": wf_id})
        exec_id = exec_.json()["id"]
        print(f"Created execution: {exec_id}")

        result = await client.post(f"/executions/{exec_id}/start")
        print(f"Execution result: {result.json()}")


if __name__ == "__main__":
    asyncio.run(test_workflow())
