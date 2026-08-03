"""
test_routing.py

Unit tests for routing.py
"""

from __future__ import annotations

import pytest

from ai.execution.routing import (
    ProviderRouter,
    RoutingResult,
)
from ai.providers.base import BaseProvider
from ai.providers.manager import ProviderManager
from ai.request import AIRequest


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

    def generate(self, prompt, model, **kwargs):
        return "OK"

    def stream(self, prompt, model, **kwargs):
        yield "OK"

    def list_models(self) -> list[str]:
        return [
            "dummy-model",
            "dummy-chat",
        ]

    def default_model(self) -> str:
        return "dummy-model"

    def supports_model(self, model: str) -> bool:
        return model in self.list_models()

    def supports_streaming(self) -> bool:
        return True

    def validate_config(self) -> bool:
        return True

    def health_check(self) -> bool:
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
def router(provider_manager):

    return ProviderRouter(provider_manager)


@pytest.fixture
def provider(provider_manager):

    return provider_manager.get("dummy")


# ----------------------------------------------------------------------
# RoutingResult
# ----------------------------------------------------------------------


def test_routing_result(provider):

    result = RoutingResult(
        provider=provider,
        model="dummy-model",
    )

    assert result.provider == provider
    assert result.model == "dummy-model"
    assert result.provider_name == "dummy"
    assert bool(result)


# ----------------------------------------------------------------------
# Default Provider
# ----------------------------------------------------------------------


def test_default_provider(router):

    request = AIRequest(
        prompt="Hello",
    )

    provider = router.select_provider(request)

    assert provider.name == "dummy"


# ----------------------------------------------------------------------
# Explicit Provider
# ----------------------------------------------------------------------


def test_explicit_provider(router):

    request = AIRequest(
        prompt="Hello",
        provider="dummy",
    )

    provider = router.select_provider(request)

    assert provider.name == "dummy"


# ----------------------------------------------------------------------
# Default Model
# ----------------------------------------------------------------------


def test_default_model(router, provider):

    request = AIRequest(
        prompt="Hello",
        provider="dummy",
    )

    model = router.select_model(
        provider,
        request,
    )

    assert model == "dummy-model"


# ----------------------------------------------------------------------
# Explicit Model
# ----------------------------------------------------------------------


def test_explicit_model(router, provider):

    request = AIRequest(
        prompt="Hello",
        provider="dummy",
        model="dummy-chat",
    )

    model = router.select_model(
        provider,
        request,
    )

    assert model == "dummy-chat"


# ----------------------------------------------------------------------
# Unsupported Model
# ----------------------------------------------------------------------


def test_invalid_model(router, provider):

    request = AIRequest(
        prompt="Hello",
        provider="dummy",
        model="invalid-model",
    )

    with pytest.raises(ValueError):
        router.select_model(
            provider,
            request,
        )


# ----------------------------------------------------------------------
# Supports Model
# ----------------------------------------------------------------------


def test_supports_model(router, provider):

    assert router.supports_model(
        provider,
        "dummy-model",
    )


def test_not_supports_model(router, provider):

    assert not router.supports_model(
        provider,
        "abc",
    )


# ----------------------------------------------------------------------
# Route
# ----------------------------------------------------------------------


def test_route(router):

    request = AIRequest(
        prompt="Hello",
    )

    result = router.route(request)

    assert isinstance(result, RoutingResult)
    assert result.provider.name == "dummy"
    assert result.model == "dummy-model"


# ----------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------


def test_route_metadata_default(router):

    request = AIRequest(
        prompt="Hello",
    )

    result = router.route(request)

    assert result.metadata["default_provider"]
    assert result.metadata["default_model"]


def test_route_metadata_explicit(router):

    request = AIRequest(
        prompt="Hello",
        provider="dummy",
        model="dummy-chat",
    )

    result = router.route(request)

    assert not result.metadata["default_provider"]
    assert not result.metadata["default_model"]


# ----------------------------------------------------------------------
# Default Provider Resolution
# ----------------------------------------------------------------------


def test_resolve_default_provider(router):

    provider = router.resolve_default_provider()

    assert provider.name == "dummy"


# ----------------------------------------------------------------------
# Default Model Resolution
# ----------------------------------------------------------------------


def test_resolve_default_model(router, provider):

    assert (
        router.resolve_default_model(provider)
        == "dummy-model"
    )


# ----------------------------------------------------------------------
# repr
# ----------------------------------------------------------------------


def test_repr(router):

    text = repr(router)

    assert "ProviderRouter" in text