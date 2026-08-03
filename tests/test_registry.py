"""
test_registry.py

Unit tests for ProviderRegistry.
"""

import pytest

from ai.providers.base import BaseProvider
from ai.providers.registry import ProviderRegistry


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

    def generate(self, prompt: str, model: str, **kwargs):
        return "response"

    def stream(self, prompt: str, model: str, **kwargs):
        yield "response"

    def list_models(self) -> list[str]:
        return ["dummy-model"]

    def default_model(self) -> str:
        return "dummy-model"

    def supports_model(self, model: str) -> bool:
        return True

    def health_check(self) -> bool:
        return True

    def validate_config(self) -> bool:
        return True

    def provider_info(self) -> dict:
        return {}

    @property
    def supports_streaming(self) -> bool:
        return True


@pytest.fixture
def registry():
    return ProviderRegistry()


@pytest.fixture
def provider():
    return DummyProvider()


def test_register_provider(registry, provider):
    registry.register(provider)
    assert registry.exists("dummy")


def test_duplicate_registration(registry, provider):
    registry.register(provider)

    with pytest.raises(ValueError):
        registry.register(provider)


def test_get_provider(registry, provider):
    registry.register(provider)

    assert registry.get("dummy") is provider


def test_get_unknown_provider(registry):
    with pytest.raises(KeyError):
        registry.get("unknown")


def test_unregister_provider(registry, provider):
    registry.register(provider)

    registry.unregister("dummy")

    assert not registry.exists("dummy")


def test_unregister_unknown_provider(registry):
    with pytest.raises(KeyError):
        registry.unregister("unknown")


def test_exists(registry, provider):
    registry.register(provider)

    assert registry.exists("dummy")
    assert not registry.exists("openai")


def test_list_providers(registry, provider):
    registry.register(provider)

    assert registry.list_providers() == ("dummy",)


def test_clear_registry(registry, provider):
    registry.register(provider)

    registry.clear()

    assert len(registry) == 0


def test_contains(registry, provider):
    registry.register(provider)

    assert "dummy" in registry
    assert "openai" not in registry


def test_len(registry, provider):
    registry.register(provider)

    assert len(registry) == 1


def test_iter(registry, provider):
    registry.register(provider)

    providers = list(registry)

    assert len(providers) == 1
    assert providers[0] is provider


def test_repr(registry, provider):
    registry.register(provider)

    text = repr(registry)

    assert "ProviderRegistry" in text
    assert "dummy" in text