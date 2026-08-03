"""
test_factory.py

Unit tests for ProviderFactory.
"""

import pytest

from ai.providers.base import BaseProvider
from ai.providers.factory import ProviderFactory


class DummyProvider(BaseProvider):

    @property
    def name(self):
        return "dummy"

    @property
    def version(self):
        return "1.0"

    def initialize(self):
        return True

    def shutdown(self):
        pass

    def generate(self, prompt, model, **kwargs):
        return "response"

    def stream(self, prompt, model, **kwargs):
        yield "response"

    def list_models(self):
        return ["dummy-model"]

    def default_model(self):
        return "dummy-model"

    def supports_model(self, model):
        return True

    def health_check(self):
        return True

    def validate_config(self):
        return True

    def provider_info(self):
        return {}

    @property
    def supports_streaming(self):
        return True


@pytest.fixture
def factory():
    return ProviderFactory()


def test_register(factory):
    factory.register("dummy", DummyProvider)

    assert "dummy" in factory


def test_duplicate_registration(factory):
    factory.register("dummy", DummyProvider)

    with pytest.raises(ValueError):
        factory.register("dummy", DummyProvider)


def test_create(factory):
    factory.register("dummy", DummyProvider)

    provider = factory.create("dummy")

    assert isinstance(provider, DummyProvider)


def test_unknown_provider(factory):
    with pytest.raises(KeyError):
        factory.create("unknown")


def test_unregister(factory):
    factory.register("dummy", DummyProvider)

    factory.unregister("dummy")

    assert "dummy" not in factory


def test_exists(factory):
    factory.register("dummy", DummyProvider)

    assert factory.exists("dummy")


def test_list_providers(factory):
    factory.register("dummy", DummyProvider)

    assert factory.list_providers() == ("dummy",)


def test_len(factory):
    factory.register("dummy", DummyProvider)

    assert len(factory) == 1


def test_clear(factory):
    factory.register("dummy", DummyProvider)

    factory.clear()

    assert len(factory) == 0


def test_iter(factory):
    factory.register("dummy", DummyProvider)

    providers = list(factory)

    assert len(providers) == 1


def test_repr(factory):
    factory.register("dummy", DummyProvider)

    assert "ProviderFactory" in repr(factory)