"""
test_session.py

Unit tests for AISession.
"""

from ai.request import AIRequest
from ai.response import AIResponse
from ai.session import AISession


def create_turn():
    request = AIRequest(prompt="Hello")

    response = AIResponse(
        content="Hi!"
    )

    return request, response


def test_create_session():
    session = AISession()

    assert session.turn_count == 0


def test_add_turn():
    session = AISession()

    request, response = create_turn()

    session.add(request, response)

    assert session.turn_count == 1


def test_last_request():
    session = AISession()

    request, response = create_turn()

    session.add(request, response)

    assert session.last_request() == request


def test_last_response():
    session = AISession()

    request, response = create_turn()

    session.add(request, response)

    assert session.last_response() == response


def test_history():
    session = AISession()

    request, response = create_turn()

    session.add(request, response)

    assert len(session.history()) == 1


def test_clear():
    session = AISession()

    request, response = create_turn()

    session.add(request, response)

    session.clear()

    assert session.turn_count == 0


def test_copy():
    session = AISession()

    request, response = create_turn()

    session.add(request, response)

    clone = session.copy()

    assert clone.turn_count == 1


def test_total_tokens():
    session = AISession()

    request = AIRequest(prompt="Hello")

    response = AIResponse(
        content="Hi!",
        total_tokens=100,
    )

    session.add(request, response)

    assert session.total_tokens == 100


def test_to_dict():
    session = AISession()

    assert isinstance(
        session.to_dict(),
        dict,
    )


def test_repr():
    session = AISession()

    assert "AISession" in repr(session)