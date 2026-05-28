# API Reference

## Workflows

### `POST /api/v1/workflows`
Create a new workflow.

### `GET /api/v1/workflows`
List all workflows. Query params: `status`, `type`.

### `GET /api/v1/workflows/{id}`
Get a workflow by ID.

### `PUT /api/v1/workflows/{id}`
Update a workflow.

### `DELETE /api/v1/workflows/{id}`
Delete a workflow.

## Executions

### `POST /api/v1/executions`
Create a new execution.

### `POST /api/v1/executions/{id}/start`
Start an execution.

### `POST /api/v1/executions/{id}/cancel`
Cancel an execution.

### `POST /api/v1/executions/{id}/pause`
Pause an execution.

### `POST /api/v1/executions/{id}/resume`
Resume a paused execution.

## Tools

### `GET /api/v1/tools`
List registered tools.

### `POST /api/v1/tools/execute`
Execute a tool.

## Monitoring

### `GET /api/v1/monitoring/summary`
Get execution summary.

### `GET /api/v1/monitoring/metrics`
Get detailed metrics.

## Health

### `GET /api/v1/health`
Health check endpoint.
