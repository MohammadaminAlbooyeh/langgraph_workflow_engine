# Architecture

## Overview

The LangGraph Workflow Engine is built on a modular architecture with four main layers:

```
Frontend (React) ──→ API (FastAPI) ──→ Engine (LangGraph) ──→ Execution Runtime
```

## Core Components

- **Graph Builder** — Constructs LangGraph `StateGraph` from node/edge definitions
- **Graph Compiler** — Compiles the graph into an executable pipeline
- **Node Executor** — Executes individual node handlers (LLM, agents, transforms)
- **Edge Router** — Evaluates conditions and routes execution along edges
- **State Manager** — Manages execution state across the workflow lifecycle

## Data Flow

1. User defines workflow via API or visual builder
2. Workflow is stored as node + edge definitions
3. On execution, the Graph Compiler builds a LangGraph state graph
4. The executor runs through nodes following edge routes
5. Results are captured per-node and aggregated into the final output
