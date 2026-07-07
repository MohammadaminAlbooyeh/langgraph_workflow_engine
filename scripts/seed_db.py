"""Seed the database with example workflows."""
import asyncio
import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from backend.models.database import Base, WorkflowModel
from config.database_config import DatabaseConfig


EXAMPLE_WORKFLOWS = [
    {
        "name": "Hello World",
        "description": "A simple hello world workflow",
        "type": "CUSTOM",
        "status": "DRAFT",
        "nodes": [
            {"id": "input", "type": "INPUT", "name": "Input Node", "config": {}, "position": {"x": 0, "y": 0}},
            {"id": "output", "type": "OUTPUT", "name": "Output Node", "config": {}, "position": {"x": 200, "y": 0}},
        ],
        "edges": [
            {"id": "e1", "source_id": "input", "target_id": "output", "type": "DIRECT"},
        ],
    },
    {
        "name": "LLM Chat",
        "description": "Simple LLM chat workflow",
        "type": "CUSTOM",
        "status": "DRAFT",
        "nodes": [
            {"id": "input", "type": "INPUT", "name": "User Input", "config": {}, "position": {"x": 0, "y": 0}},
            {"id": "llm", "type": "LLM", "name": "Chat LLM", "config": {"provider": "openai", "temperature": 0.7}, "position": {"x": 200, "y": 0}},
            {"id": "output", "type": "OUTPUT", "name": "Response", "config": {}, "position": {"x": 400, "y": 0}},
        ],
        "edges": [
            {"id": "e1", "source_id": "input", "target_id": "llm", "type": "DIRECT"},
            {"id": "e2", "source_id": "llm", "target_id": "output", "type": "DIRECT"},
        ],
    },
    {
        "name": "Multi-Agent Research",
        "description": "Multi-agent workflow for research tasks",
        "type": "MULTI_AGENT",
        "status": "DRAFT",
        "nodes": [
            {"id": "input", "type": "INPUT", "name": "Research Query", "config": {}, "position": {"x": 0, "y": 0}},
            {"id": "agent1", "type": "AGENT", "name": "Search Agent", "config": {"type": "tool_agent"}, "position": {"x": 200, "y": -100}},
            {"id": "agent2", "type": "AGENT", "name": "Analysis Agent", "config": {"type": "reasoning_agent"}, "position": {"x": 200, "y": 100}},
            {"id": "output", "type": "OUTPUT", "name": "Final Report", "config": {}, "position": {"x": 400, "y": 0}},
        ],
        "edges": [
            {"id": "e1", "source_id": "input", "target_id": "agent1", "type": "DIRECT"},
            {"id": "e2", "source_id": "input", "target_id": "agent2", "type": "DIRECT"},
            {"id": "e3", "source_id": "agent1", "target_id": "output", "type": "DIRECT"},
            {"id": "e4", "source_id": "agent2", "target_id": "output", "type": "DIRECT"},
        ],
    },
    {
        "name": "Data Processing Pipeline",
        "description": "Pipeline for processing and transforming data",
        "type": "CUSTOM",
        "status": "DRAFT",
        "nodes": [
            {"id": "input", "type": "INPUT", "name": "Data Input", "config": {}, "position": {"x": 0, "y": 0}},
            {"id": "transform", "type": "TRANSFORMER", "name": "Transform Data", "config": {}, "position": {"x": 200, "y": 0}},
            {"id": "validate", "type": "VALIDATOR", "name": "Validate", "config": {}, "position": {"x": 400, "y": 0}},
            {"id": "output", "type": "OUTPUT", "name": "Processed Data", "config": {}, "position": {"x": 600, "y": 0}},
        ],
        "edges": [
            {"id": "e1", "source_id": "input", "target_id": "transform", "type": "DIRECT"},
            {"id": "e2", "source_id": "transform", "target_id": "validate", "type": "DIRECT"},
            {"id": "e3", "source_id": "validate", "target_id": "output", "type": "DIRECT"},
        ],
    },
]


async def seed():
    config = DatabaseConfig()
    engine = create_async_engine(config.url, echo=False)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async with async_session() as session:
            for workflow_data in EXAMPLE_WORKFLOWS:
                workflow = WorkflowModel(
                    id=f"wf_{uuid.uuid4().hex[:12]}",
                    name=workflow_data["name"],
                    description=workflow_data["description"],
                    type=workflow_data["type"],
                    status=workflow_data["status"],
                    nodes=workflow_data["nodes"],
                    edges=workflow_data["edges"],
                    version="0.1.0",
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc),
                )
                session.add(workflow)

            await session.commit()
            print(f"✓ Seeded {len(EXAMPLE_WORKFLOWS)} example workflows to database")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
