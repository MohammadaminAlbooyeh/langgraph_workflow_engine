from __future__ import annotations
from typing import Any, Optional
from datetime import datetime, timezone
from backend.models.execution import ExecutionResult, ExecutionStatus
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class NodeExecutor:
    def __init__(self):
        self._llm_factory = None

    def _get_llm_factory(self):
        if self._llm_factory is None:
            from backend.llm.llm_factory import LLMFactory
            self._llm_factory = LLMFactory()
        return self._llm_factory

    async def execute(
        self,
        node_id: str,
        node_config: dict,
        inputs: dict[str, Any],
        context: Optional[dict] = None,
    ) -> ExecutionResult:
        start_time = datetime.now(timezone.utc)
        logger.info(f"Executing node {node_id}", node_id=node_id)

        try:
            output = await self._run_node(node_id, node_config, inputs, context or {})
            duration = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000

            return ExecutionResult(
                node_id=node_id,
                node_name=node_config.get("name", node_id),
                status=ExecutionStatus.COMPLETED,
                output=output,
                duration_ms=duration,
            )
        except Exception as e:
            duration = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000
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
        provider = config.get("provider")
        prompt_template = config.get("prompt_template", "")
        system_prompt = config.get("system_prompt", "You are a helpful AI assistant.")
        formatted = prompt_template.format(**inputs) if inputs else prompt_template

        llm = self._get_llm_factory().create(provider)
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if formatted:
            messages.append({"role": "user", "content": formatted})
        elif inputs:
            messages.append({"role": "user", "content": str(inputs)})

        response = await llm.invoke(messages)
        return {"response": response, "provider": provider or "openai"}

    async def _handle_agent(self, node_id: str, config: dict, inputs: dict, context: dict) -> Any:
        provider = config.get("provider")
        system_prompt = config.get("system_prompt", "You are a helpful AI assistant.")
        user_input = str(inputs.get("input", inputs))

        llm = self._get_llm_factory().create(provider)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ]
        response = await llm.invoke(messages)
        return {"agent_output": response, "reasoning": f"Processed by {provider or 'default'} LLM"}

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
