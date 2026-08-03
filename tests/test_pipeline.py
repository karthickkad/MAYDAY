"""
test_pipeline.py

Unit tests for pipeline.py
"""

from __future__ import annotations

import pytest

from ai.execution.pipeline import (
    ExecutionPipeline,
    PipelineResult,
)

from ai.execution.validator import (
    RequestValidator,
)

from ai.execution.routing import (
    ProviderRouter,
)

from ai.execution.executor import (
    RequestExecutor,
)

from ai.providers.base import BaseProvider
from ai.providers.manager import ProviderManager

from ai.request import AIRequest
from ai.response import AIResponse

from ai.prompts import PromptManager

# ----------------------------------------------------------------------
# Dummy Provider
# ----------------------------------------------------------------------


class DummyProvider(BaseProvider):

    @property
    def name(self) -> str:
        return "dummy"

    @property
    def version(self) -> str:
        return "1.0"

    def initialize(self) -> bool:
        return True

    def shutdown(self) -> None:
        pass

    def generate(self, **kwargs):
        return "Hello MAYDAY"

    def stream(self, **kwargs):
        yield "Hello "
        yield "MAYDAY"

    def list_models(self):
        return ["dummy-model"]

    def default_model(self):
        return "dummy-model"

    def supports_model(
        self,
        model: str,
    ) -> bool:
        return True

    def supports_streaming(self) -> bool:
        return True

    def validate_config(self):
        return True

    def health_check(self):
        return True

    def provider_info(self):
        return {}
    
# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------


@pytest.fixture
def provider_manager():

    manager = ProviderManager()

    manager.register(
        "dummy",
        DummyProvider,
        default=True,
    )

    return manager


@pytest.fixture
def prompt_manager():

    return PromptManager()


@pytest.fixture
def validator(
    provider_manager,
    prompt_manager,
):

    return RequestValidator(
        provider_manager,
        prompt_manager,
    )


@pytest.fixture
def router(
    provider_manager,
):

    return ProviderRouter(
        provider_manager,
    )


@pytest.fixture
def executor():

    return RequestExecutor()


@pytest.fixture
def pipeline(
    validator,
    router,
    executor,
):

    return ExecutionPipeline(
        validator,
        router,
        executor,
    )


@pytest.fixture
def ai_request():

    return AIRequest(
        prompt="Hello",
        provider="dummy",
        model="dummy-model",
    )
    
# ----------------------------------------------------------------------
# PipelineResult
# ----------------------------------------------------------------------


@pytest.fixture
def pipeline_result(
    pipeline,
    ai_request,
):

    return pipeline.execute(
        ai_request,
    )


def test_pipeline_result_type(
    pipeline_result,
):

    assert isinstance(
        pipeline_result,
        PipelineResult,
    )


def test_pipeline_result_success(
    pipeline_result,
):

    assert pipeline_result.success is True


def test_pipeline_result_bool(
    pipeline_result,
):

    assert bool(
        pipeline_result
    )


def test_pipeline_result_provider(
    pipeline_result,
):

    assert (
        pipeline_result.provider
        == "dummy"
    )


def test_pipeline_result_model(
    pipeline_result,
):

    assert (
        pipeline_result.model
        == "dummy-model"
    )


def test_pipeline_result_execution_time(
    pipeline_result,
):

    assert (
        pipeline_result.execution_time_sec
        >= 0
    )


def test_pipeline_result_response(
    pipeline_result,
):

    assert isinstance(
        pipeline_result.response,
        AIResponse,
    )


def test_pipeline_result_metadata(
    pipeline_result,
):

    assert isinstance(
        pipeline_result.metadata,
        dict,
    )


def test_pipeline_result_repr(
    pipeline_result,
):

    assert (
        "PipelineResult"
        in repr(pipeline_result)
    )


def test_pipeline_result_str(
    pipeline_result,
):

    assert (
        "PipelineResult"
        in str(pipeline_result)
    )
    
# ----------------------------------------------------------------------
# Execute
# ----------------------------------------------------------------------


def test_execute_returns_pipeline_result(
    pipeline,
    ai_request,
):

    result = pipeline.execute(
        ai_request,
    )

    assert isinstance(
        result,
        PipelineResult,
    )


def test_execute_validation_success(
    pipeline,
    ai_request,
):

    result = pipeline.execute(
        ai_request,
    )

    assert result.validation.valid


def test_execute_routing(
    pipeline,
    ai_request,
):

    result = pipeline.execute(
        ai_request,
    )

    assert (
        result.routing.provider.name
        == "dummy"
    )


def test_execute_model(
    pipeline,
    ai_request,
):

    result = pipeline.execute(
        ai_request,
    )

    assert (
        result.routing.model
        == "dummy-model"
    )


def test_execute_response(
    pipeline,
    ai_request,
):

    result = pipeline.execute(
        ai_request,
    )

    assert (
        result.response.content
        == "Hello MAYDAY"
    )


def test_execute_success(
    pipeline,
    ai_request,
):

    result = pipeline.execute(
        ai_request,
    )

    assert result.execution.success


def test_execute_metadata_provider(
    pipeline,
    ai_request,
):

    result = pipeline.execute(
        ai_request,
    )

    assert (
        result.metadata["provider"]
        == "dummy"
    )


def test_execute_metadata_model(
    pipeline,
    ai_request,
):

    result = pipeline.execute(
        ai_request,
    )

    assert (
        result.metadata["model"]
        == "dummy-model"
    )


def test_execute_metadata_success(
    pipeline,
    ai_request,
):

    result = pipeline.execute(
        ai_request,
    )

    assert (
        result.metadata["success"]
        is True
    )


def test_execute_execution_time(
    pipeline,
    ai_request,
):

    result = pipeline.execute(
        ai_request,
    )

    assert (
        result.execution.execution_time
        >= 0
    )


def test_execute_route_time(
    pipeline,
    ai_request,
):

    result = pipeline.execute(
        ai_request,
    )

    assert (
        result.metadata["route_time_ms"]
        >= 0
    )
# ----------------------------------------------------------------------
# Streaming
# ----------------------------------------------------------------------


def test_execute_stream_returns_iterator(
    pipeline,
    ai_request,
):

    stream = pipeline.execute_stream(
        ai_request,
    )

    assert hasattr(
        stream,
        "__iter__",
    )


def test_execute_stream_chunks(
    pipeline,
    ai_request,
):

    chunks = list(
        pipeline.execute_stream(
            ai_request,
        )
    )

    assert len(chunks) == 2


def test_execute_stream_response_type(
    pipeline,
    ai_request,
):

    chunks = list(
        pipeline.execute_stream(
            ai_request,
        )
    )

    assert all(
        isinstance(
            chunk,
            AIResponse,
        )
        for chunk in chunks
    )


def test_execute_stream_content(
    pipeline,
    ai_request,
):

    chunks = list(
        pipeline.execute_stream(
            ai_request,
        )
    )

    assert (
        "".join(
            chunk.content
            for chunk in chunks
        )
        == "Hello MAYDAY"
    )


def test_execute_stream_provider(
    pipeline,
    ai_request,
):

    chunks = list(
        pipeline.execute_stream(
            ai_request,
        )
    )

    assert all(
        chunk.provider == "dummy"
        for chunk in chunks
    )


def test_execute_stream_model(
    pipeline,
    ai_request,
):

    chunks = list(
        pipeline.execute_stream(
            ai_request,
        )
    )

    assert all(
        chunk.model == "dummy-model"
        for chunk in chunks
    )


def test_execute_stream_metadata(
    pipeline,
    ai_request,
):

    chunks = list(
        pipeline.execute_stream(
            ai_request,
        )
    )

    assert all(
        chunk.metadata.get("stream")
        is True
        for chunk in chunks
    )


def test_execute_stream_is_streaming(
    pipeline,
    ai_request,
):

    chunks = list(
        pipeline.execute_stream(
            ai_request,
        )
    )

    assert all(
        chunk.is_streaming
        for chunk in chunks
    )


def test_execute_stream_chunk_count(
    pipeline,
    ai_request,
):

    count = sum(
        1
        for _ in pipeline.execute_stream(
            ai_request,
        )
    )

    assert count == 2
    
# ----------------------------------------------------------------------
# Lifecycle Hooks
# ----------------------------------------------------------------------


class HookPipeline(ExecutionPipeline):

    def __init__(
        self,
        validator,
        router,
        executor,
    ) -> None:

        super().__init__(
            validator,
            router,
            executor,
        )

        self.calls: list[str] = []

    def before_execute(
        self,
        request: AIRequest,
    ) -> None:

        self.calls.append(
            "before_execute"
        )

    def before_validation(
        self,
        request: AIRequest,
    ) -> None:

        self.calls.append(
            "before_validation"
        )
    
    def after_route(
        self,
        request,
        routing,
    ):
        self.calls.append("after_route")

    def before_route(
        self,
        request: AIRequest,
    ) -> None:

        self.calls.append(
            "before_route"
        )

    def after_execute(
        self,
        result,
    ):
        self.calls.append(
            "after_execute"
        )


    def on_validation_failed(
        self,
        request,
        validation,
    ) -> None:

        self.calls.append(
            "validation_failed"
        )

    def on_execution_failed(
        self,
        request,
        routing,
        exception,
    ) -> None:

        self.calls.append(
            "execution_failed"
        )


@pytest.fixture
def hook_pipeline(
    validator,
    router,
    executor,
):

    return HookPipeline(
        validator,
        router,
        executor,
    )


def test_before_execute_hook(
    hook_pipeline,
    ai_request,
):

    hook_pipeline.execute(
        ai_request,
    )

    assert (
        "before_execute"
        in hook_pipeline.calls
    )


def test_before_validation_hook(
    hook_pipeline,
    ai_request,
):

    hook_pipeline.execute(
        ai_request,
    )

    assert (
        "before_validation"
        in hook_pipeline.calls
    )


def test_before_route_hook(
    hook_pipeline,
    ai_request,
):

    hook_pipeline.execute(
        ai_request,
    )

    assert (
        "before_route"
        in hook_pipeline.calls
    )


def test_after_route_hook(
    hook_pipeline,
    ai_request,
):

    hook_pipeline.execute(
        ai_request,
    )

    assert (
        "after_route"
        in hook_pipeline.calls
    )


def test_after_execute_hook(
    hook_pipeline,
    ai_request,
):

    hook_pipeline.execute(
        ai_request,
    )

    assert (
        "after_execute"
        in hook_pipeline.calls
    )


def test_hook_order(
    hook_pipeline,
    ai_request,
):

    hook_pipeline.execute(
        ai_request,
    )

    assert hook_pipeline.calls == [
        "before_execute",
        "before_validation",
        "before_route",
        "after_route",
        "after_execute",
    ]
    
# ----------------------------------------------------------------------
# Failure Handling
# ----------------------------------------------------------------------


class FailingExecutor(RequestExecutor):

    def execute(
        self,
        request: AIRequest,
        routing,
    ):
        raise RuntimeError(
            "Execution failed."
        )


@pytest.fixture
def failing_pipeline(
    validator,
    router,
):

    return ExecutionPipeline(
        validator,
        router,
        FailingExecutor(),
    )


def test_validation_failure():

    manager = ProviderManager()

    manager.register(
        "dummy",
        DummyProvider,
        default=True,
    )

    validator = RequestValidator(
        manager,
    )

    router = ProviderRouter(
        manager,
    )

    executor = RequestExecutor()

    pipeline = ExecutionPipeline(
        validator,
        router,
        executor,
    )

    invalid_request = AIRequest(
        prompt="Hello",
        provider="unknown-provider",
        model="dummy-model",
    )

    with pytest.raises(
        ValueError,
    ):

        pipeline.execute(
            invalid_request,
        )


def test_execution_failure(
    failing_pipeline,
    ai_request,
):

    with pytest.raises(
        RuntimeError,
    ):

        failing_pipeline.execute(
            ai_request,
        )


def test_on_execution_failed_hook(
    validator,
    router,
    ai_request,
):

    class TestPipeline(
        ExecutionPipeline,
    ):

        def __init__(
            self,
            validator,
            router,
            executor,
        ):

            super().__init__(
                validator,
                router,
                executor,
            )

            self.called = False

        def on_execution_failed(
            self,
            request,
            routing,
            exception,
        ):

            self.called = True

            raise exception

    pipeline = TestPipeline(
        validator,
        router,
        FailingExecutor(),
    )

    with pytest.raises(
        RuntimeError,
    ):

        pipeline.execute(
            ai_request,
        )

    assert pipeline.called


def test_on_validation_failed_hook():

    manager = ProviderManager()

    manager.register(
        "dummy",
        DummyProvider,
        default=True,
    )

    validator = RequestValidator(
        manager,
    )

    router = ProviderRouter(
        manager,
    )

    executor = RequestExecutor()

    class TestPipeline(
        ExecutionPipeline,
    ):

        def __init__(
            self,
            validator,
            router,
            executor,
        ):

            super().__init__(
                validator,
                router,
                executor,
            )

            self.called = False

        def on_validation_failed(
            self,
            request,
            validation,
        ):

            self.called = True

            raise ValueError(
                "\n".join(
                    validation.errors
                )
            )

    pipeline = TestPipeline(
        validator,
        router,
        executor,
    )

    invalid_request = AIRequest(
        prompt="Hello",
        provider="unknown-provider",
        model="dummy-model",
    )

    with pytest.raises(
        ValueError,
    ):

        pipeline.execute(
            invalid_request,
        )

    assert pipeline.called
    
# ----------------------------------------------------------------------
# Metadata & Python Methods
# ----------------------------------------------------------------------


def test_pipeline_info(
    pipeline,
):

    info = pipeline.pipeline_info()

    assert isinstance(
        info,
        dict,
    )

    assert (
        info["validator"]
        == "RequestValidator"
    )

    assert (
        info["router"]
        == "ProviderRouter"
    )

    assert (
        info["executor"]
        == "RequestExecutor"
    )

    assert (
        info["version"]
        == pipeline.PIPELINE_VERSION
    )

    assert (
        info["supports_streaming"]
        == pipeline.SUPPORTS_STREAMING
    )


def test_build_metadata(
    pipeline,
    ai_request,
):

    result = pipeline.execute(
        ai_request,
    )

    metadata = result.metadata

    assert (
        metadata["provider"]
        == "dummy"
    )

    assert (
        metadata["model"]
        == "dummy-model"
    )

    assert (
        metadata["success"]
        is True
    )

    assert (
        metadata["status"]
        == "success"
    )

    assert (
        metadata["retry_count"]
        == 0
    )

    assert (
        metadata["cached"]
        is False
    )

    assert (
        metadata["fallback"]
        is False
    )

    assert (
        metadata["fallback_provider"]
        is None
    )

    assert (
        metadata["route_time_ms"]
        >= 0
    )

    assert (
        metadata["execution_time_ms"]
        >= 0
    )

    assert (
        metadata["pipeline_version"]
        == pipeline.PIPELINE_VERSION
    )


def test_build_pipeline_result(
    pipeline,
    ai_request,
):

    result = pipeline.execute(
        ai_request,
    )

    assert isinstance(
        result,
        PipelineResult,
    )

    assert (
        result.validation.valid
    )

    assert (
        result.routing.provider.name
        == "dummy"
    )

    assert (
        result.execution.success
    )


def test_repr(
    pipeline,
):

    assert (
        "ExecutionPipeline"
        in repr(pipeline)
    )


def test_str(
    pipeline,
):

    assert (
        "ExecutionPipeline"
        in str(pipeline)
    )


def test_bool(
    pipeline,
):

    assert bool(
        pipeline
    )


def test_pipeline_constants(
    pipeline,
):

    assert (
        pipeline.PIPELINE_VERSION
        == "1.0"
    )

    assert (
        pipeline.SUPPORTS_STREAMING
        is True
    )

    assert (
        pipeline.SUPPORTS_VALIDATION
        is True
    )

    assert (
        pipeline.SUPPORTS_ROUTING
        is True
    )

    assert (
        pipeline.SUPPORTS_EXECUTION
        is True
    )


def test_metadata_contains_expected_keys(
    pipeline,
    ai_request,
):

    result = pipeline.execute(
        ai_request,
    )

    expected = {
        "provider",
        "model",
        "success",
        "status",
        "route_time_ms",
        "execution_time_ms",
        "retry_count",
        "cached",
        "fallback",
        "fallback_provider",
        "trace_id",
        "request_id",
        "middleware_count",
        "pipeline_version",
    }

    assert expected.issubset(
        result.metadata.keys()
    )
# ----------------------------------------------------------------------
# Edge Cases & Regression Tests
# ----------------------------------------------------------------------


def test_multiple_execute_calls(
    pipeline,
    ai_request,
):

    first = pipeline.execute(
        ai_request,
    )

    second = pipeline.execute(
        ai_request,
    )

    assert first.success
    assert second.success

    assert (
        first.response.content
        == second.response.content
    )


def test_multiple_stream_calls(
    pipeline,
    ai_request,
):

    first = list(
        pipeline.execute_stream(
            ai_request,
        )
    )

    second = list(
        pipeline.execute_stream(
            ai_request,
        )
    )

    assert len(first) == 2
    assert len(second) == 2


def test_pipeline_metadata_isolation(
    pipeline,
    ai_request,
):

    first = pipeline.execute(
        ai_request,
    )

    second = pipeline.execute(
        ai_request,
    )

    assert (
        first.metadata
        is not second.metadata
    )


def test_stream_metadata_isolation(
    pipeline,
    ai_request,
):

    chunks = list(
        pipeline.execute_stream(
            ai_request,
        )
    )

    assert (
        chunks[0].metadata
        is not chunks[1].metadata
    )


def test_pipeline_result_objects_are_unique(
    pipeline,
    ai_request,
):

    first = pipeline.execute(
        ai_request,
    )

    second = pipeline.execute(
        ai_request,
    )

    assert first is not second


def test_response_objects_are_unique(
    pipeline,
    ai_request,
):

    first = pipeline.execute(
        ai_request,
    )

    second = pipeline.execute(
        ai_request,
    )

    assert (
        first.response
        is not second.response
    )


def test_execution_time_non_negative(
    pipeline,
    ai_request,
):

    result = pipeline.execute(
        ai_request,
    )

    assert (
        result.execution.execution_time
        >= 0
    )


def test_route_time_non_negative(
    pipeline,
    ai_request,
):

    result = pipeline.execute(
        ai_request,
    )

    assert (
        result.metadata["route_time_ms"]
        >= 0
    )


def test_pipeline_result_truthiness(
    pipeline,
    ai_request,
):

    result = pipeline.execute(
        ai_request,
    )

    assert result


def test_pipeline_repr_contains_class_name(
    pipeline,
):

    assert (
        pipeline.__class__.__name__
        in repr(pipeline)
    )
    
# ----------------------------------------------------------------------
# Integration Tests
# ----------------------------------------------------------------------


def test_complete_pipeline_flow(
    pipeline,
    ai_request,
):

    result = pipeline.execute(
        ai_request,
    )

    assert result.validation.valid
    assert result.routing.provider.name == "dummy"
    assert result.execution.success
    assert result.response.content == "Hello MAYDAY"


def test_sync_and_stream_consistency(
    pipeline,
    ai_request,
):

    sync = pipeline.execute(
        ai_request,
    )

    stream = "".join(
        chunk.content
        for chunk in pipeline.execute_stream(
            ai_request,
        )
    )

    assert sync.response.content == stream


def test_pipeline_can_be_reused(
    pipeline,
    ai_request,
):

    for _ in range(10):

        result = pipeline.execute(
            ai_request,
        )

        assert result.success


def test_stream_can_be_reused(
    pipeline,
    ai_request,
):

    for _ in range(10):

        chunks = list(
            pipeline.execute_stream(
                ai_request,
            )
        )

        assert len(chunks) == 2


def test_pipeline_metadata_consistency(
    pipeline,
    ai_request,
):

    result = pipeline.execute(
        ai_request,
    )

    assert (
        result.metadata["provider"]
        == result.provider
    )

    assert (
        result.metadata["model"]
        == result.model
    )

    assert (
        result.metadata["success"]
        == result.success
    )
# ----------------------------------------------------------------------
# Stress Tests
# ----------------------------------------------------------------------

def test_hundred_requests(
    pipeline,
    ai_request,
):

    for _ in range(100):

        result = pipeline.execute(
            ai_request,
        )

        assert result.success


def test_hundred_streams(
    pipeline,
    ai_request,
):

    for _ in range(100):

        chunks = list(
            pipeline.execute_stream(
                ai_request,
            )
        )

        assert len(chunks) == 2


def test_pipeline_metadata_stability(
    pipeline,
    ai_request,
):

    for _ in range(50):

        result = pipeline.execute(
            ai_request,
        )

        assert result.metadata["provider"] == "dummy"
        assert result.metadata["model"] == "dummy-model"
        assert result.metadata["status"] == "success"


def test_pipeline_execution_time(
    pipeline,
    ai_request,
):

    result = pipeline.execute(
        ai_request,
    )

    assert result.execution.execution_time < 1.0