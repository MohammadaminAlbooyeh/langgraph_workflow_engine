__all__ = [
    "DEFAULT_WORKFLOW_VERSION",
    "MAX_NODE_INPUTS",
    "MAX_NODE_OUTPUTS",
    "MAX_WORKFLOW_DEPTH",
    "DEFAULT_TIMEOUT_SECONDS",
    "MAX_RETRY_COUNT",
    "MAX_CONCURRENT_NODES",
    "NODE_TYPE_CATEGORIES",
    "WORKFLOW_TYPE_DESCRIPTIONS",
    "API_VERSIONS",
    "EVENT_TYPES",
]

DEFAULT_WORKFLOW_VERSION = "0.1.0"
MAX_NODE_INPUTS = 50
MAX_NODE_OUTPUTS = 50
MAX_WORKFLOW_DEPTH = 100
DEFAULT_TIMEOUT_SECONDS = 300
MAX_RETRY_COUNT = 5
MAX_CONCURRENT_NODES = 10

NODE_TYPE_CATEGORIES = {
    "agent": ["agent", "planner", "reasoning", "tool_agent"],
    "decision": ["conditional", "router", "loop", "switch"],
    "processing": ["llm", "transformer", "validator", "text_processor", "custom"],
    "input": ["manual", "api", "file", "database"],
    "output": ["api", "file", "database", "display"],
    "aggregation": ["aggregate", "merge", "combine"],
}

WORKFLOW_TYPE_DESCRIPTIONS = {
    "custom": "Free-form workflow with any node configuration",
    "data_pipeline": "ETL-style data processing pipeline",
    "decision_tree": "Branching logic for decision-making workflows",
    "document": "Document processing and generation workflows",
    "multi_agent": "Orchestrate multiple AI agents",
    "parallel": "Execute nodes in parallel for high throughput",
}

API_VERSIONS = {
    "v1": "/api/v1",
}

EVENT_TYPES = [
    "workflow.created",
    "workflow.updated",
    "workflow.deleted",
    "workflow.started",
    "workflow.completed",
    "workflow.failed",
    "node.started",
    "node.completed",
    "node.failed",
    "execution.created",
    "execution.completed",
]
