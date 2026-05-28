# Workflow Guide

## Workflow Types

### Custom
Free-form workflow. Any combination of nodes and edges.

### Data Pipeline
ETL-style with input → process → output flow.
Validates that input and output nodes exist.

### Decision Tree
Branching logic workflows. Must include conditional/decision nodes.

### Document Processing
Document-centric workflows. Should include LLM nodes.

### Multi-Agent
Orchestrates multiple AI agents. Must have 2+ agent nodes.

### Parallel
Executes nodes concurrently for high-throughput processing.

## Defining a Workflow

A workflow consists of:
- **Nodes** — Individual processing steps
- **Edges** — Connections between nodes
- **Metadata** — Optional key-value pairs

## State

Each execution maintains state as a dictionary that flows through the graph.
Nodes read from and write to this shared state.
