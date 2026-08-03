"""
executor.py

Execution module for MAYDAY.

Responsible for executing routed AI requests.
"""

from __future__ import annotations

import time

from dataclasses import dataclass, field
from typing import Any

from ai.execution.routing import RoutingResult
from ai.request import AIRequest
from ai.response import AIResponse


# ----------------------------------------------------------------------
# Execution Result
# ----------------------------------------------------------------------


@dataclass(slots=True)
class ExecutionResult:
    """
    Result returned by RequestExecutor.
    """

    response: AIResponse

    execution_time: float

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def success(self) -> bool:
        return True

    def __bool__(self) -> bool:
        return self.success

# ----------------------------------------------------------------------
# Request Executor
# ----------------------------------------------------------------------


class RequestExecutor:
    """
    Executes routed AI requests.
    """

    def __init__(self) -> None:
        pass

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def execute(
        self,
        request: AIRequest,
        routing: RoutingResult,
    ) -> ExecutionResult:
        """
        Execute a routed AI request.
        """

        start_time = time.perf_counter()
        
        status = "success"
        
        try:
            response = self._generate(
                request,
                routing,
            )

        except Exception as exc:
            response = self._handle_exception(
                exc,
                routing,
            )

        execution_time = self._measure_time(
            start_time,
        )

        return ExecutionResult(
            response=response,
            execution_time=execution_time,
            metadata={
                "provider": routing.provider.name,
                "model": routing.model,
                "stream": False,
                "tokens": response.total_tokens,
                "latency_ms": round(execution_time * 1000, 3),
                "retry_count": 0,
                "cached": False,
                "status": "status",
            }
        )

    # ------------------------------------------------------------------
    # Internal Execution
    # ------------------------------------------------------------------

    def _generate(
        self,
        request: AIRequest,
        routing: RoutingResult,
    ) -> AIResponse:
        """
        Execute a non-streaming request using the selected provider.
        """

        provider = routing.provider

        result = provider.generate(
            prompt=request.prompt,
            model=routing.model,
            temperature=request.temperature,
            top_p=request.top_p,
            max_tokens=request.max_tokens,
            system_prompt=request.system_prompt,
        )

        return self._create_response(
            request=request,
            routing=routing,
            result=result,
        )

    def _create_response(
        self,
        request: AIRequest,
        routing: RoutingResult,
        result: Any,
    ) -> AIResponse:
        """
        Convert provider output into an AIResponse.
        """

        if isinstance(result, AIResponse):
            return result

        return AIResponse(
            content=str(result),
            provider=routing.provider.name,
            model=routing.model,
            metadata={},
        )

    # ------------------------------------------------------------------
    # Streaming Execution
    # ------------------------------------------------------------------

    def execute_stream(
        self,
        request: AIRequest,
        routing: RoutingResult,
    ):
        """
        Execute a streaming AI request.

        Returns
        -------
        Iterator[AIResponse]
        """

        yield from self._stream(
            request,
            routing,
        )

    def _stream(
        self,
        request: AIRequest,
        routing: RoutingResult,
    ):
        """
        Execute provider streaming.
        """

        provider = routing.provider

        for chunk in provider.stream(
            prompt=request.prompt,
            model=routing.model,
            temperature=request.temperature,
            top_p=request.top_p,
            max_tokens=request.max_tokens,
            system_prompt=request.system_prompt,
        ):

            if isinstance(chunk, AIResponse):
                yield chunk
                continue

            yield AIResponse(
                content=str(chunk),
                provider=provider.name,
                model=routing.model,
                stream=True,
                metadata={
                    "stream": True,
                },
            )

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def _measure_time(
        self,
        start_time: float,
    ) -> float:
        """
        Calculate execution time in seconds.
        """

        return time.perf_counter() - start_time

    # ------------------------------------------------------------------
    # Error Handling
    # ------------------------------------------------------------------

    def _handle_exception(
        self,
        exception: Exception,
        routing: RoutingResult,
    ) -> AIResponse:
        """
        Convert provider exceptions into a standard AIResponse.
        """

        return AIResponse(
            content=f"Execution failed: {exception}",
            provider=routing.provider.name,
            model=routing.model,
            stream=False,
            metadata={
                "status": "failed",
                "exception": type(exception).__name__,
            },
        )

    # ------------------------------------------------------------------
    # Python Methods
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"