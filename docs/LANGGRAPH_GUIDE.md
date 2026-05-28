# LangGraph Guide

LangGraph is a library for building stateful, multi-actor applications with LLMs.

## Key Concepts

- **StateGraph** — The core graph structure. Nodes are functions, edges define transitions.
- **State** — A shared dictionary passed through the graph as it executes.
- **Nodes** — Python async functions that receive state and return updates.
- **Edges** — Define how execution flows between nodes. Can be conditional.

## In This Project

The LangGraph engine wraps `StateGraph` to provide:
- Declarative node/edge definitions via the API
- Conditional routing with field-based conditions
- Checkpoint/restore for long-running workflows
- Human-in-the-loop pause points
