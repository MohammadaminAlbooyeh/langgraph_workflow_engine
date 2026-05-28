"""Export workflows to JSON file."""
import asyncio
import json
import httpx

BASE_URL = "http://localhost:8000/api/v1"


async def export(output_file="workflows_export.json"):
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/workflows")
        workflows = response.json()
        with open(output_file, "w") as f:
            json.dump(workflows, f, indent=2)
        print(f"Exported {len(workflows)} workflows to {output_file}")


if __name__ == "__main__":
    asyncio.run(export())
