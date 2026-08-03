"""
test_response.py

Unit tests for AIResponse.
"""

import pytest

from ai.response import AIResponse


def test_default_response():
    response = AIResponse(content="Hello")

    assert response.content == "Hello"
    assert response.total_tokens == 0
    assert response.stream is False


def test_custom_response():
    response = AIResponse(
        content="Hello",
        provider="openai",
        model="gpt-4",
        total_tokens=100,
        stream=True,
    )

    assert response.provider == "openai"
    assert response.model == "gpt-4"
    assert response.stream is True


def test_empty_content():
    with pytest.raises(ValueError):
        AIResponse(content="")


def test_negative_prompt_tokens():
    with pytest.raises(ValueError):
        AIResponse(
            content="Hello",
            prompt_tokens=-1,
        )


def test_negative_completion_tokens():
    with pytest.raises(ValueError):
        AIResponse(
            content="Hello",
            completion_tokens=-1,
        )


def test_negative_total_tokens():
    with pytest.raises(ValueError):
        AIResponse(
            content="Hello",
            total_tokens=-1,
        )


def test_copy():
    response = AIResponse(content="Hello")

    clone = response.copy(model="gpt-4")

    assert clone.model == "gpt-4"
    assert response.model is None


def test_to_dict():
    response = AIResponse(content="Hello")

    data = response.to_dict()

    assert data["content"] == "Hello"


def test_from_dict():
    response = AIResponse.from_dict(
        {
            "content": "Hello",
            "provider": "openai",
        }
    )

    assert response.provider == "openai"


def test_token_usage():
    response = AIResponse(
        content="Hello",
        prompt_tokens=20,
        completion_tokens=30,
        total_tokens=50,
    )

    assert response.token_usage["total"] == 50


def test_repr():
    response = AIResponse(content="Hello")

    assert "AIResponse" in repr(response)