class WorkflowEngineException(Exception):
    def __init__(self, message: str, code: str = "UNKNOWN_ERROR", status_code: int = 500):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class WorkflowNotFoundError(WorkflowEngineException):
    def __init__(self, workflow_id: str):
        super().__init__(
            message=f"Workflow '{workflow_id}' not found",
            code="WORKFLOW_NOT_FOUND",
            status_code=404,
        )


class NodeExecutionError(WorkflowEngineException):
    def __init__(self, node_id: str, message: str):
        super().__init__(
            message=f"Node '{node_id}' execution failed: {message}",
            code="NODE_EXECUTION_ERROR",
            status_code=500,
        )


class InvalidGraphError(WorkflowEngineException):
    def __init__(self, message: str):
        super().__init__(
            message=f"Invalid graph: {message}",
            code="INVALID_GRAPH",
            status_code=400,
        )


class ToolExecutionError(WorkflowEngineException):
    def __init__(self, tool_name: str, message: str):
        super().__init__(
            message=f"Tool '{tool_name}' execution failed: {message}",
            code="TOOL_EXECUTION_ERROR",
            status_code=500,
        )


class ConfigurationError(WorkflowEngineException):
    def __init__(self, message: str):
        super().__init__(
            message=f"Configuration error: {message}",
            code="CONFIGURATION_ERROR",
            status_code=500,
        )
