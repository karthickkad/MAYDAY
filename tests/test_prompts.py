"""
test_prompts.py

Unit tests for PromptManager.
"""

import pytest

from ai.prompts import (
    PromptManager,
    PromptTemplate,
)


@pytest.fixture
def template():

    return PromptTemplate(
        name="Greeting",
        template="Hello {name}",
    )


@pytest.fixture
def manager():

    return PromptManager()


def test_register(manager, template):

    manager.register(template)

    assert manager.exists("Greeting")


def test_duplicate(manager, template):

    manager.register(template)

    with pytest.raises(ValueError):
        manager.register(template)


def test_get(manager, template):

    manager.register(template)

    assert manager.get("Greeting") is template


def test_unknown(manager):

    with pytest.raises(KeyError):
        manager.get("unknown")


def test_render(manager, template):

    manager.register(template)

    text = manager.render(
        "Greeting",
        name="MAYDAY",
    )

    assert text == "Hello MAYDAY"


def test_missing_variable(manager, template):

    manager.register(template)

    with pytest.raises(KeyError):
        manager.render("Greeting")


def test_variables(template):

    assert template.variables() == ("name",)


def test_unregister(manager, template):

    manager.register(template)

    manager.unregister("Greeting")

    assert not manager.exists("Greeting")


def test_clear(manager, template):

    manager.register(template)

    manager.clear()

    assert len(manager) == 0


def test_contains(manager, template):

    manager.register(template)

    assert "Greeting" in manager


def test_repr(manager, template):

    manager.register(template)

    assert "PromptManager" in repr(manager)