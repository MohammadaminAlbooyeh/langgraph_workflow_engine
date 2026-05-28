"""Import workflows from JSON file."""
import asyncio
import json
import httpx

BASE_URL = "http://localhost:8000/api/v1"


async def import_workflows(input_file="workflows_export.json"):
    with open(input_file) as f:
        workflows = json.load(f)

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        for wf in workflows:
            response = await client.post("/workflows", json=wf)
            print(f"Imported: {response.json()['name']}")


if __name__ == "__main__":
    asyncio.run(import_workflows())
