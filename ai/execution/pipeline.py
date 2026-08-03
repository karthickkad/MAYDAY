"""
pipeline.py

Execution pipeline for MAYDAY.

Coordinates validation, routing and execution.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Any

from ai.execution.executor import (
    ExecutionResult,
    RequestExecutor,
)
from ai.execution.routing import (
    ProviderRouter,
    RoutingResult,
)
from ai.execution.validator import (
    RequestValidator,
    ValidationResult,
)
from ai.request import AIRequest
from ai.response import AIResponse

from collections.abc import Iterator

from typing import final

__all__ = (
    "PipelineResult",
    "ExecutionPipeline",
)

# ----------------------------------------------------------------------
# Pipeline Result
# ----------------------------------------------------------------------


@dataclass(slots=True)
class PipelineResult:
    """
    Result returned by ExecutionPipeline.
    """

    validation: ValidationResult

    routing: RoutingResult

    execution: ExecutionResult

    metadata: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------
    # Convenience Properties
    # ------------------------------------------------------------

    @property
    def response(self) -> AIResponse:
        """
        Return the final AI response.
        """
        return self.execution.response

    @property
    def provider(self) -> str:
        """
        Return the selected provider.
        """
        return self.routing.provider.name

    @property
    def model(self) -> str:
        """
        Return the selected model.
        """
        return self.routing.model

    @property
    def execution_time_sec(self) -> float:
        """
        Return total execution time.
        """
        return self.execution.execution_time

    @property
    def success(self) -> bool:
        """
        Return True if pipeline execution succeeded.
        """
        return (
            self.validation.valid
            and self.execution.success
        )

    # ------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------

    @property
    def error_count(self) -> int:
        """
        Number of validation errors.
        """
        return self.validation.error_count

    @property
    def warning_count(self) -> int:
        """
        Number of validation warnings.
        """
        return self.validation.warning_count

    # ------------------------------------------------------------
    # Metadata Helpers
    # ------------------------------------------------------------

    @property
    def has_metadata(self) -> bool:
        """
        Return True if pipeline metadata exists.
        """
        return bool(self.metadata)

    # ------------------------------------------------------------
    # Python Methods
    # ------------------------------------------------------------

    def __bool__(self) -> bool:
        return self.success

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"provider={self.provider!r}, "
            f"model={self.model!r}, "
            f"success={self.success}, "
            f"execution_time={self.execution_time_sec:.3f}s)"
        )
# ----------------------------------------------------------------------
# Execution Pipeline
# ----------------------------------------------------------------------

@final
class ExecutionPipeline:

    PIPELINE_VERSION = "1.0"

    SUPPORTS_STREAMING = True
    SUPPORTS_VALIDATION = True
    SUPPORTS_ROUTING = True
    SUPPORTS_EXECUTION = True
    
    __slots__ = (
        "_validator",
        "_router",
        "_executor",
        )
    
    """
    Coordinates validation, routing and execution.

    The pipeline itself contains no business logic.
    Each stage is delegated to its respective component.

    Components
    ----------
    RequestValidator
        Validates incoming requests.

    ProviderRouter
        Selects the provider and model.

    RequestExecutor
        Executes the routed request.
    """

    def __init__(
        self,
        validator: RequestValidator,
        router: ProviderRouter,
        executor: RequestExecutor,
    ) -> None:
        """
        Initialize the execution pipeline.
        """

        if validator is None:
            raise ValueError(
                "validator cannot be None."
            )

        if router is None:
            raise ValueError(
                "router cannot be None."
            )

        if executor is None:
            raise ValueError(
                "executor cannot be None."
            )

        self._validator = validator
        self._router = router
        self._executor = executor

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    
    def execute(
        self,
        request: AIRequest,
    ) -> PipelineResult:
        """
        Execute an AI request through the complete pipeline.

        Flow
        ----
        1. Before Execute Hook
        2. Validate Request
        3. Route Request
        4. Execute Request
        5. Build Pipeline Result
        6. After Execute Hook
        """

        # ----------------------------------------------------------
        # Before Execution
        # ----------------------------------------------------------

        pipeline_start = time.perf_counter()

        self.before_execute(
            request,
        )
        
        # ----------------------------------------------------------
        # Validation
        # ----------------------------------------------------------

        self.before_validation(request)

        validation_start = time.perf_counter()

        validation = self.validate(request)

        validation_time_ms = (
            time.perf_counter() - validation_start
        ) * 1000

        if validation.has_errors:
            self.on_validation_failed(
                request,
                validation,
            )

        # ----------------------------------------------------------
        # Routing
        # ----------------------------------------------------------

        route_start = time.perf_counter()

        routing = self.route(request)

        route_time_ms = (
            time.perf_counter() - route_start
        ) * 1000

        # ----------------------------------------------------------
        # Execution
        # ----------------------------------------------------------

        try:

            execution = self.execute_request(
                request,
                routing,
            )

        except Exception as exc:

            self.on_execution_failed(
                request,
                routing,
                exc,
            )

            raise

        # ----------------------------------------------------------
        # Build Result
        # ----------------------------------------------------------
        pipeline_time_ms = (
            time.perf_counter() - pipeline_start
        ) * 1000
        
        result = self._build_pipeline_result(
            validation,
            routing,
            execution,
            route_time_ms,
            validation_time_ms,
            pipeline_time_ms,
        )

        # ----------------------------------------------------------
        # After Execution
        # ----------------------------------------------------------

        self.after_execute(result)

        return result

    def execute_stream(
        self,
        request: AIRequest,
    ) -> Iterator[AIResponse]:
        """
        Execute a streaming AI request through the pipeline.

        Returns
        -------
        Iterator[AIResponse]
        """

        # ----------------------------------------------------------
        # Before Execution
        # ----------------------------------------------------------

        pipeline_start = time.perf_counter()

        self.before_execute(
            request,
        )

        # ----------------------------------------------------------
        # Validation
        # ----------------------------------------------------------

        self.before_validation(request)

        validation_start = time.perf_counter()

        validation = self.validate(request)

        validation_time_ms = (
            time.perf_counter() - validation_start
        ) * 1000

        if validation.has_errors:
            self.on_validation_failed(
                request,
                validation,
            )

        # ----------------------------------------------------------
        # Routing
        # ----------------------------------------------------------

        routing = self.route(request)

        # ----------------------------------------------------------
        # Streaming
        # ----------------------------------------------------------

        try:

            for response in self._stream(
                request,
                routing,
            ):
                yield response

        except Exception as exc:

            self.on_execution_failed(
                request,
                routing,
                exc,
            )

            raise

        finally:

            self.after_execute(None)

    # ------------------------------------------------------------------
    # Pipeline Stages
    # ------------------------------------------------------------------

    def validate(
        self,
        request: AIRequest,
    ) -> ValidationResult:
        """
        Validate an AI request.
        """

        return self._validator.validate(
            request,
        )

    def route(
        self,
        request: AIRequest,
    ) -> RoutingResult:
        """
        Route a validated AI request.

        Future Extension Points
        -----------------------
        - Dynamic provider selection
        - Load balancing
        - Provider fallback
        - Cost optimization
        - Metrics
        - Tracing
        """

        self.before_route(request)

        routing = self._router.route(
            request,
        )

        self.after_route(
            request,
            routing,
        )

        return routing

    def execute_request(
        self,
        request: AIRequest,
        routing: RoutingResult,
    ) -> ExecutionResult:
        """
        Execute a routed AI request.
        """

        if request.stream:
            raise RuntimeError(
                "Streaming requests must use "
                "'execute_stream()'."
            )

        return self._executor.execute(
            request,
            routing,
        )

    def _stream(
        self,
        request: AIRequest,
        routing: RoutingResult,
    ) -> Iterator[AIResponse]:
        """
        Execute a routed streaming request.

        Reserved for future middleware integration.
        """

        for response in self._executor.execute_stream(
            request,
            routing,
        ):

            #
            # Middleware
            #

            #
            # Token Counter
            #

            #
            # Event Publisher
            #

            #
            # Metrics
            #

            #
            # Logging
            #
            
            #
            # Response Transformation
            #

            yield response
        
    # ------------------------------------------------------------------
    # Lifecycle Hooks
    # ------------------------------------------------------------------

    def before_execute(
        self,
        request: AIRequest,
    ) -> None:
        """
        Hook executed before pipeline execution.

        Future Uses
        -----------
        - Authentication
        - Authorization
        - Rate limiting
        - Logging
        - Metrics
        - Middleware
        """

        return None
    
    def before_validation(
        self,
        request: AIRequest,
    ) -> None:
        """
        Hook executed immediately before validation.

        Future Uses
        -----------
        - Prompt normalization
        - Request preprocessing
        - Authentication
        - Quota validation
        """

        return None

    def before_route(
        self,
        request: AIRequest,
    ) -> None:
        """
        Hook executed immediately before routing.

        Future Uses
        -----------
        - Dynamic provider selection
        - Request rewriting
        - Cost optimization
        - A/B routing
        """

        return None

    def after_route(
        self,
        request: AIRequest,
        routing: RoutingResult,
    ) -> None:
        """
        Hook executed immediately after routing.

        Future Uses
        -----------
        - Logging
        - Metrics
        - Tracing
        - Route auditing
        """
        return None

    def after_execute(
        self,
        result: PipelineResult | None = None,
    ) -> None:
        """
        Hook executed after successful execution.

        Future Uses
        -----------
        - Logging
        - Metrics
        - Event publishing
        - Response caching
        """

        return None

    def on_validation_failed(
        self,
        request: AIRequest,
        validation: ValidationResult,
    ) -> None:
        """
        Handle validation failures.

        Default behaviour raises a ValueError.
        """

        raise ValueError(
            "\n".join(validation.errors)
        )

    def on_execution_failed(
        self,
        request: AIRequest,
        routing: RoutingResult,
        exception: Exception,
    ) -> None:
        """
        Handle execution failures.

        Default behaviour re-raises the exception.

        Future Uses
        -----------
        - Retry logic
        - Provider fallback
        - Error logging
        - Notifications
        """

        raise exception

    # ------------------------------------------------------------------
    # Internal Helpers
    # ------------------------------------------------------------------

    def _build_pipeline_result(
        self,
        validation: ValidationResult,
        routing: RoutingResult,
        execution: ExecutionResult,
        route_time_ms: float,
        validation_time_ms: float,
        pipeline_time_ms: float,
    ) -> PipelineResult:
        """
        Build the final PipelineResult.
        """

        result  = PipelineResult(
            validation=validation,
            routing=routing,
            execution=execution,
            metadata=self._build_metadata(
                validation,
                routing,
                execution,
                route_time_ms,
                validation_time_ms,
                pipeline_time_ms,
            ),
        )
        
        return result

    def _build_metadata(
        self,
        validation: ValidationResult,
        routing: RoutingResult,
        execution: ExecutionResult,
        route_time_ms: float,
        validation_time_ms: float,
        pipeline_time_ms: float,
    ) -> dict[str, Any]:
        """
        Build pipeline metadata.

        This method is reserved for future expansion without
        changing the public pipeline API.
        """

        return {
            "provider": routing.provider.name,
            "route_provider": routing.provider.name,
            "model": routing.model,
            "success": execution.success,

            "stream": False,

            "execution_time_ms": round(
                execution.execution_time * 1000,
                3,
            ),
            
            "pipeline_time_ms": round(
                pipeline_time_ms,
                3,
            ),
            
           "validation_time_ms": round(validation_time_ms, 3),

            "validation_errors": validation.error_count,
            "validation_warnings": validation.warning_count,

            "retry_count": 0,

            "cached": False,

            "fallback": False,
            "fallback_provider": None,

            "trace_id": None,
            "request_id": None,

            "middleware_count": 0,

           "pipeline_version": self.PIPELINE_VERSION, 
            
            "route_time_ms": round(route_time_ms, 3),
            
            "status": (
                "success"
                if execution.success
                else "failed"
            ),
            
        }

    def pipeline_info(
        self,
    ) -> dict[str, Any]:
        """
        Return information about the configured pipeline.
        """

        return {
            "version": self.PIPELINE_VERSION,
            "validator": self._validator.__class__.__name__,
            "router": self._router.__class__.__name__,
            "executor": self._executor.__class__.__name__,
            "supports_streaming": self.SUPPORTS_STREAMING,
            "supports_validation": self.SUPPORTS_VALIDATION,
            "supports_routing": self.SUPPORTS_ROUTING,
            "supports_execution": self.SUPPORTS_EXECUTION,
            "hooks": {
                "before_execute": True,
                "before_validation": True,
                "before_route": True,
                "after_route": True,
                "after_execute": True,
                "on_validation_failed": True,
                "on_execution_failed": True,
            },
        }
        
    # ------------------------------------------------------------------
    # Python Methods
    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"validator={self._validator.__class__.__name__}, "
            f"router={self._router.__class__.__name__}, "
            f"executor={self._executor.__class__.__name__}, "
            f"streaming={self.SUPPORTS_STREAMING}, "
            f"version={self.PIPELINE_VERSION!r})"
        )

    def __str__(self) -> str:
        """
        Return a human-readable representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"validator={self._validator.__class__.__name__}, "
            f"router={self._router.__class__.__name__}, "
            f"executor={self._executor.__class__.__name__}, "
            f"version={self.PIPELINE_VERSION})"
        )

    def __bool__(self) -> bool:
        """
        Pipeline is valid when all required components exist.
        """

        return all(
            (
                self._validator,
                self._router,
                self._executor,
            )
        )


