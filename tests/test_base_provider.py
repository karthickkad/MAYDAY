"""
test_base_provider.py

Unit tests for BaseProvider.
"""

import pytest

from ai.providers.base import BaseProvider


def test_base_provider_is_abstract():
    """
    BaseProvider should not be instantiated directly.
    """
    with pytest.raises(TypeError):
        BaseProvider()