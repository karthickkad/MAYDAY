"""
test_executor.py

Unit tests for executor.py
"""

from __future__ import annotations

import pytest

from ai.execution.executor import (
    ExecutionResult,
    RequestExecutor,
)
from ai.execution.routing import RoutingResult

from ai.providers.base import BaseProvider
from ai.providers.manager import ProviderManager

from ai.request import AIRequest
from ai.response import AIResponse


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
        yield "Hello"
        yield "MAYDAY"

    def list_models(self):
        return ["dummy-model"]

    def default_model(self):
        return "dummy-model"

    def supports_model(self, model):
        return True

    def supports_streaming(self):
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
def provider(provider_manager):

    return provider_manager.get("dummy")


@pytest.fixture
def executor():

    return RequestExecutor()


@pytest.fixture
def ai_request():

    return AIRequest(
        prompt="Hello",
        provider="dummy",
        model="dummy-model",
    )


@pytest.fixture
def routing(provider):

    return RoutingResult(
        provider=provider,
        model="dummy-model",
    )


# ----------------------------------------------------------------------
# ExecutionResult
# ----------------------------------------------------------------------


def test_execution_result(response):

    result = ExecutionResult(
        response=response,
        execution_time=0.25,
    )

    assert result.response == response
    assert result.execution_time == 0.25
    assert result.success


@pytest.fixture
def response():

    return AIResponse(
        content="Hello",
        provider="dummy",
        model="dummy-model",
    )


# ----------------------------------------------------------------------
# Execute
# ----------------------------------------------------------------------


def test_execute(
    executor,
    ai_request,
    routing,
):

    result = executor.execute(
        ai_request,
        routing,
    )

    assert isinstance(result, ExecutionResult)
    assert result.response.content == "Hello MAYDAY"


def test_execution_time(
    executor,
    ai_request,
    routing,
):

    result = executor.execute(
        ai_request,
        routing,
    )

    assert result.execution_time >= 0


# ----------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------


def test_metadata_provider(
    executor,
    ai_request,
    routing,
):

    result = executor.execute(
        ai_request,
        routing,
    )

    assert result.metadata["provider"] == "dummy"


def test_metadata_model(
    executor,
    ai_request,
    routing,
):

    result = executor.execute(
        ai_request,
        routing,
    )

    assert result.metadata["model"] == "dummy-model"


def test_metadata_stream(
    executor,
    ai_request,
    routing,
):

    result = executor.execute(
        ai_request,
        routing,
    )

    assert result.metadata["stream"] is False


def test_metadata_cached(
    executor,
    ai_request,
    routing,
):

    result = executor.execute(
        ai_request,
        routing,
    )

    assert result.metadata["cached"] is False


def test_metadata_retry(
    executor,
    ai_request,
    routing,
):

    result = executor.execute(
        ai_request,
        routing,
    )

    assert result.metadata["retry_count"] == 0


# ----------------------------------------------------------------------
# Generate
# ----------------------------------------------------------------------


def test_generate(
    executor,
    ai_request,
    routing,
):

    response = executor._generate(
        ai_request,
        routing,
    )

    assert isinstance(response, AIResponse)


# ----------------------------------------------------------------------
# Streaming
# ----------------------------------------------------------------------


def test_execute_stream(
    executor,
    ai_request,
    routing,
):

    chunks = list(
        executor.execute_stream(
            ai_request,
            routing,
        )
    )

    assert len(chunks) == 2


def test_stream_response_type(
    executor,
    ai_request,
    routing,
):

    chunks = list(
        executor.execute_stream(
            ai_request,
            routing,
        )
    )

    assert isinstance(
        chunks[0],
        AIResponse,
    )


# ----------------------------------------------------------------------
# Measure Time
# ----------------------------------------------------------------------


def test_measure_time(executor):

    import time

    start = time.perf_counter()

    elapsed = executor._measure_time(start)

    assert elapsed >= 0


# ----------------------------------------------------------------------
# repr
# ----------------------------------------------------------------------


def test_repr(executor):

    assert "RequestExecutor" in repr(executor)