# Tool Guide

## Built-in Tools

- `current_datetime` — Get current UTC time
- `calculate` — Evaluate math expressions
- `format_text` — Transform text case

## Custom Tools

Register custom tools via the API or code:

```python
registry.register_custom(
    name="my_tool",
    handler=my_function,
    description="Does something useful",
    parameters=[{"name": "input", "type": "string", "required": True}],
)
```

## Using Tools

Tools can be:
- Called directly via the API
- Attached to agent nodes for autonomous use
- Chained in workflow nodes
