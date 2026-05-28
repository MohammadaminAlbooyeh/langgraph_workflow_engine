# Agent Guide

## Configuration

Agents are configured with:
- `provider` — LLM provider (openai, anthropic, local)
- `model` — Model name
- `temperature` — Creativity (0.0 to 2.0)
- `max_tokens` — Max response length
- `system_prompt` — System instructions
- `capabilities` — List of agent capabilities
- `tools` — List of available tool names

## Agent Types

- **Single Agent** — One agent handling the entire workflow
- **Multi-Agent** — Multiple specialized agents collaborating
- **Hierarchical** — Manager agent delegating to sub-agents
- **Tool-Using** — Agent with external tool access
