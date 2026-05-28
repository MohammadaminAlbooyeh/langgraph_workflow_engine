from __future__ import annotations
from typing import Any, Optional
from datetime import datetime
from backend.models.execution import ExecutionResult, ExecutionStatus
from backend.utils.logger import get_logger
from backend.utils.decorators import measure_time

logger = get_logger(__name__)


class NodeExecutor:
    async def execute(
        self,
        node_id: str,
        node_config: dict,
        inputs: dict[str, Any],
        context: Optional[dict] = None,
    ) -> ExecutionResult:
        start_time = datetime.utcnow()
        logger.info(f"Executing node {node_id}", node_id=node_id)

        try:
            output = await self._run_node(node_id, node_config, inputs, context or {})
            duration = (datetime.utcnow() - start_time).total_seconds() * 1000

            return ExecutionResult(
                node_id=node_id,
                node_name=node_config.get("name", node_id),
                status=ExecutionStatus.COMPLETED,
                output=output,
                duration_ms=duration,
            )
        except Exception as e:
            duration = (datetime.utcnow() - start_time).total_seconds() * 1000
            logger.error(f"Node {node_id} failed: {e}", exc_info=True)
            return ExecutionResult(
                node_id=node_id,
                node_name=node_config.get("name", node_id),
                status=ExecutionStatus.FAILED,
                error=str(e),
                duration_ms=duration,
            )

    async def _run_node(
        self,
        node_id: str,
        config: dict,
        inputs: dict[str, Any],
        context: dict,
    ) -> Any:
        node_type = config.get("type", "processing")
        handler_map = {
            "llm": self._handle_llm,
            "agent": self._handle_agent,
            "transformer": self._handle_transformer,
            "validator": self._handle_validator,
            "input": self._handle_input,
            "output": self._handle_output,
        }

        handler = handler_map.get(node_type, self._handle_default)
        return await handler(node_id, config, inputs, context)

    async def _handle_llm(self, node_id: str, config: dict, inputs: dict, context: dict) -> Any:
        prompt = config.get("prompt_template", "")
        system_prompt = config.get("system_prompt", "")
        formatted = prompt.format(**inputs) if inputs else prompt
        return {"response": f"[LLM response for: {formatted[:50]}...]", "provider": config.get("provider", "openai")}

    async def _handle_agent(self, node_id: str, config: dict, inputs: dict, context: dict) -> Any:
        return {"agent_output": f"[Agent {node_id} processed]", "reasoning": "Simulated agent reasoning"}

    async def _handle_transformer(self, node_id: str, config: dict, inputs: dict, context: dict) -> Any:
        return {"transformed": inputs}

    async def _handle_validator(self, node_id: str, config: dict, inputs: dict, context: dict) -> Any:
        is_valid = bool(inputs.get("data")) if "data" in inputs else True
        return {"valid": is_valid, "errors": [] if is_valid else ["Validation failed"]}

    async def _handle_input(self, node_id: str, config: dict, inputs: dict, context: dict) -> Any:
        return {"input_data": inputs.get("data", {})}

    async def _handle_output(self, node_id: str, config: dict, inputs: dict, context: dict) -> Any:
        return {"output_data": inputs}

    async def _handle_default(self, node_id: str, config: dict, inputs: dict, context: dict) -> Any:
        return {"result": inputs}
