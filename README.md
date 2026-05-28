# LangGraph Workflow Engine

Build, execute, and monitor AI agent workflows using LangGraph.

## Features

- **Visual Workflow Builder** — Drag-and-drop canvas for designing workflows
- **Multi-Agent Orchestration** — Coordinate multiple AI agents in complex workflows
- **LLM Integration** — Built-in support for OpenAI, Anthropic Claude, and local models
- **Conditional Routing** — Branching logic with dynamic edge routing
- **Human-in-the-Loop** — Approval gates and manual review steps
- **Memory & State** — Persistent state and checkpoint management
- **Monitoring** — Real-time execution tracking with Prometheus/Grafana
- **Docker/K8s** — Containerized deployment ready

## Quick Start

```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Open http://localhost:8000/docs for API docs.

## Project Structure

```
backend/           — FastAPI backend + LangGraph engine
frontend/src/      — React dashboard
config/            — Application configuration
docs/              — Documentation
kubernetes/        — K8s deployment manifests
monitoring/        — Prometheus/Grafana configs
tests/             — Unit, integration, load tests
```

## API Endpoints

- `GET /api/v1/health` — Health check
- `POST /api/v1/workflows` — Create workflow
- `GET /api/v1/workflows` — List workflows
- `POST /api/v1/executions` — Create execution
- `GET /api/v1/monitoring/summary` — Metrics summary
