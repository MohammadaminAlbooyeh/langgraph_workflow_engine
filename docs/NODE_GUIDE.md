# Node Guide

## Node Types

### Agent Nodes
- `agent` — General AI agent with system prompt
- `planner` — Creates execution plans
- `reasoning` — Step-by-step reasoning
- `tool_agent` — Agent with tool-calling capability

### Decision Nodes
- `conditional` — Branch based on state field value
- `router` — Route to different paths based on field
- `loop` — Iterate over data items
- `switch` — Multi-case branching

### Input Nodes
- `input` — Manual/manual input
- `api_input` — Fetch data from API
- `file_input` — Read from file
- `database_input` — Query database

### Processing Nodes
- `llm` — LLM call with prompt
- `transformer` — Data transformation
- `validator` — Validate data against schema
- `text_processor` — Text manipulation (upper/lower/trim)
- `custom` — User-defined logic

### Output Nodes
- `output` — Return data
- `api_output` — Send to API
- `file_output` — Write to file
- `database_output` — Save to database

### Aggregation Nodes
- `aggregate` — Collect results
- `merge` — Merge multiple inputs
- `combine` — Combine into single output
