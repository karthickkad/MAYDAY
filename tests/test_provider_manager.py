"""
test_provider_manager.py

Unit tests for ProviderManager.
"""

import pytest

from ai.providers.base import BaseProvider
from ai.providers.manager import ProviderManager


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
def manager():
    return ProviderManager()


def test_register_provider(manager):
    provider = manager.register("dummy", DummyProvider)

    assert provider.name == "dummy"
    assert manager.exists("dummy")


def test_duplicate_registration(manager):
    manager.register("dummy", DummyProvider)

    with pytest.raises(ValueError):
        manager.register("dummy", DummyProvider)


def test_get_provider(manager):
    provider = manager.register("dummy", DummyProvider)

    assert manager.get("dummy") is provider


def test_unknown_provider(manager):
    with pytest.raises(KeyError):
        manager.get("unknown")


def test_default_provider(manager):
    provider = manager.register(
        "dummy",
        DummyProvider,
        default=True,
    )

    assert manager.default_provider() is provider


def test_set_default(manager):
    manager.register("dummy", DummyProvider)

    manager.set_default("dummy")

    assert manager.default_provider().name == "dummy"


def test_exists(manager):
    manager.register("dummy", DummyProvider)

    assert manager.exists("dummy")
    assert not manager.exists("openai")


def test_list_providers(manager):
    manager.register("dummy", DummyProvider)

    assert manager.list_providers() == ("dummy",)


def test_health_check(manager):
    manager.register("dummy", DummyProvider)

    status = manager.health_check()

    assert status["dummy"] is True


def test_unregister(manager):
    manager.register("dummy", DummyProvider)

    manager.unregister("dummy")

    assert not manager.exists("dummy")


def test_shutdown(manager):
    manager.register("dummy", DummyProvider)

    manager.shutdown()

    assert len(manager) == 0


def test_len(manager):
    manager.register("dummy", DummyProvider)

    assert len(manager) == 1


def test_contains(manager):
    manager.register("dummy", DummyProvider)

    assert "dummy" in manager
    assert "openai" not in manager


def test_repr(manager):
    manager.register("dummy", DummyProvider)

    text = repr(manager)

    assert "ProviderManager" in text
    assert "dummy" in text