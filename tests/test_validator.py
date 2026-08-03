"""
test_validator.py

Unit tests for validator.py
"""

from __future__ import annotations

import pytest

from ai.execution.validator import (
    RequestValidator,
    ValidationResult,
)
from ai.prompts import PromptManager
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
        return ["dummy-model"]

    def default_model(self) -> str:
        return "dummy-model"

    def supports_model(self, model: str) -> bool:
        return model == "dummy-model"

    def health_check(self) -> bool:
        return True

    def validate_config(self) -> bool:
        return True

    def provider_info(self):
        return {}

    def supports_streaming(self) -> bool:
        return True


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
def validator(provider_manager):

    return RequestValidator(
        provider_manager,
        PromptManager(),
    )


@pytest.fixture
def ai_request():

    return AIRequest(
        prompt="Hello MAYDAY",
        provider="dummy",
        model="dummy-model",
    )


# ----------------------------------------------------------------------
# ValidationResult Tests
# ----------------------------------------------------------------------


def test_validation_result_defaults():

    result = ValidationResult()

    assert result.valid is True
    assert result.errors == []
    assert result.warnings == []
    assert result.error_count == 0
    assert result.warning_count == 0


def test_add_error():

    result = ValidationResult()

    result.add_error("Error")

    assert not result.valid
    assert result.has_errors
    assert result.error_count == 1


def test_add_warning():

    result = ValidationResult()

    result.add_warning("Warning")

    assert result.has_warnings
    assert result.warning_count == 1


# ----------------------------------------------------------------------
# Request Validation
# ----------------------------------------------------------------------


def test_valid_request(
    validator,
    ai_request,
):

    result = validator.validate(ai_request)

    assert result.valid


def test_empty_prompt():

    with pytest.raises(ValueError):
        AIRequest(
            prompt="",
            provider="dummy",
            model="dummy-model",
        )

# ----------------------------------------------------------------------
# Provider Validation
# ----------------------------------------------------------------------


def test_missing_provider(validator):

    req = AIRequest(
        prompt="Hello",
        provider=None,
    )

    result = validator.validate(req)

    assert result.has_warnings


def test_validate_or_raise(validator):

    req = AIRequest(
        prompt="Hello",
        provider="unknown",
    )

    with pytest.raises(ValueError):
        validator.validate_or_raise(req)


# ----------------------------------------------------------------------
# Model Validation
# ----------------------------------------------------------------------


def test_missing_model(validator):

    req = AIRequest(
        prompt="Hello",
        provider="dummy",
        model=None,
    )

    result = validator.validate(req)

    assert result.has_warnings


def test_invalid_model(validator):

    req = AIRequest(
        prompt="Hello",
        provider="dummy",
        model="gpt-4",
    )

    result = validator.validate(req)

    assert not result.valid


# ----------------------------------------------------------------------
# Parameter Validation
# ----------------------------------------------------------------------


def test_invalid_temperature():

    with pytest.raises(ValueError):
        AIRequest(
            prompt="Hello",
            provider="dummy",
            model="dummy-model",
            temperature=3.0,
        )


def test_invalid_top_p():

    with pytest.raises(ValueError):
        AIRequest(
            prompt="Hello",
            provider="dummy",
            model="dummy-model",
            top_p=1.5,
        )


def test_invalid_max_tokens():

    with pytest.raises(ValueError):
        AIRequest(
            prompt="Hello",
            provider="dummy",
            model="dummy-model",
            max_tokens=0,
        )


# ----------------------------------------------------------------------
# Streaming
# ----------------------------------------------------------------------


def test_stream_supported(validator):

    req = AIRequest(
        prompt="Hello",
        provider="dummy",
        model="dummy-model",
        stream=True,
    )

    result = validator.validate(req)

    assert result.valid


# ----------------------------------------------------------------------
# validate_or_raise()
# ----------------------------------------------------------------------


def test_validate_or_raise(validator):

    req = AIRequest(
        prompt="Hello MAYDAY",
        provider="unknown",
        model="dummy-model",
    )

    with pytest.raises(ValueError):
        validator.validate_or_raise(req)