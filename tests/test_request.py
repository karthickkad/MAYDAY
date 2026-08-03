import pytest

from ai.request import AIRequest


def test_default_request():
    request = AIRequest(prompt="Hello")

    assert request.prompt == "Hello"
    assert request.temperature == 0.7
    assert request.stream is False


def test_custom_request():
    request = AIRequest(
        prompt="Hello",
        provider="openai",
        model="gpt-4",
        temperature=0.3,
        stream=True,
    )

    assert request.provider == "openai"
    assert request.model == "gpt-4"
    assert request.stream is True


def test_empty_prompt():
    with pytest.raises(ValueError):
        AIRequest(prompt="")


def test_invalid_temperature():
    with pytest.raises(ValueError):
        AIRequest(prompt="Hello", temperature=5)


def test_invalid_top_p():
    with pytest.raises(ValueError):
        AIRequest(prompt="Hello", top_p=2)


def test_invalid_max_tokens():
    with pytest.raises(ValueError):
        AIRequest(prompt="Hello", max_tokens=0)


def test_copy():
    request = AIRequest(prompt="Hello")

    clone = request.copy(model="gpt-4")

    assert clone.model == "gpt-4"
    assert request.model is None


def test_to_dict():
    request = AIRequest(prompt="Hello")

    data = request.to_dict()

    assert data["prompt"] == "Hello"


def test_from_dict():
    request = AIRequest.from_dict(
        {
            "prompt": "Hello",
            "provider": "openai",
        }
    )

    assert request.provider == "openai"


def test_repr():
    request = AIRequest(prompt="Hello")

    assert "AIRequest" in repr(request)