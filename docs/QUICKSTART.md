# Quickstart Guide

## Installation

```bash
git clone <repo>
cd langgraph_workflow_engine
pip install -r requirements.txt
```

## Running the Server

```bash
uvicorn backend.main:app --reload
```

The API will be available at http://localhost:8000

## Creating Your First Workflow

```python
import httpx

client = httpx.Client(base_url="http://localhost:8000/api/v1")

# Create a workflow
wf = client.post("/workflows", json={
    "name": "Hello World",
    "nodes": [
        {"id": "input", "type": "input", "name": "Input"},
        {"id": "llm", "type": "llm", "name": "LLM"},
        {"id": "output", "type": "output", "name": "Output"},
    ],
    "edges": [
        {"id": "e1", "source_id": "input", "target_id": "llm"},
        {"id": "e2", "source_id": "llm", "target_id": "output"},
    ],
})

# Execute it
exec = client.post("/executions", json={"workflow_id": wf.json()["id"]})
client.post(f"/executions/{exec.json()['id']}/start")
```
