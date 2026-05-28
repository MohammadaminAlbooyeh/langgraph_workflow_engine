"""Create example workflows in the database."""
import asyncio
import httpx

BASE_URL = "http://localhost:8000/api/v1"

EXAMPLE_WORKFLOWS = [
    {
        "name": "Hello World",
        "description": "Simple input/output workflow",
        "type": "custom",
        "nodes": [{"id": "n1", "type": "input", "name": "Input"}, {"id": "n2", "type": "output", "name": "Output"}],
        "edges": [{"id": "e1", "source_id": "n1", "target_id": "n2"}],
    },
    {
        "name": "LLM Chat",
        "description": "Chat with an LLM",
        "type": "custom",
        "nodes": [
            {"id": "n1", "type": "input", "name": "User Input"},
            {"id": "n2", "type": "llm", "name": "LLM", "config": {"provider": "openai", "temperature": 0.7}},
            {"id": "n3", "type": "output", "name": "Response"},
        ],
        "edges": [
            {"id": "e1", "source_id": "n1", "target_id": "n2"},
            {"id": "e2", "source_id": "n2", "target_id": "n3"},
        ],
    },
]


async def main():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        for wf in EXAMPLE_WORKFLOWS:
            response = await client.post("/workflows", json=wf)
            print(f"Created: {response.json()['name']} (ID: {response.json()['id']})")


if __name__ == "__main__":
    asyncio.run(main())
