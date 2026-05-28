"""Seed the database with example workflows."""
import json
from pathlib import Path

SEED_WORKFLOWS = [
    {
        "name": "Hello World",
        "description": "A simple hello world workflow",
        "type": "custom",
        "nodes": [
            {"id": "input", "type": "input", "name": "Input"},
            {"id": "output", "type": "output", "name": "Output"},
        ],
        "edges": [
            {"id": "e1", "source_id": "input", "target_id": "output"},
        ],
    },
    {
        "name": "LLM Chat",
        "description": "Simple LLM chat workflow",
        "type": "custom",
        "nodes": [
            {"id": "input", "type": "input", "name": "User Input"},
            {"id": "llm", "type": "llm", "name": "Chat LLM", "config": {"provider": "openai", "temperature": 0.7}},
            {"id": "output", "type": "output", "name": "Response"},
        ],
        "edges": [
            {"id": "e1", "source_id": "input", "target_id": "llm"},
            {"id": "e2", "source_id": "llm", "target_id": "output"},
        ],
    },
]


def seed():
    output_path = Path("data/datasets/workflow_examples.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(SEED_WORKFLOWS, f, indent=2)
    print(f"Seeded {len(SEED_WORKFLOWS)} workflows to {output_path}")


if __name__ == "__main__":
    seed()
