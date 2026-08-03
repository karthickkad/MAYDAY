"""
test_provider_info.py

Unit tests for provider_info.py
"""

from __future__ import annotations

import pytest

from ai.providers.provider_info import (
    DEFAULT_PROVIDER_VERSION,
    ProviderInfo,
    provider_from_dict,
    provider_to_dict,
    is_provider_available,
    is_provider_enabled,
    is_provider_active,
)


# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------


@pytest.fixture
def provider_info() -> ProviderInfo:

    return ProviderInfo(
        name="openai",
        display_name="OpenAI",
        version="1.0",
        description="OpenAI Provider",
        website="https://openai.com",
        documentation_url="https://platform.openai.com/docs",
        api_base_url="https://api.openai.com/v1",
        supported_models=(
            "gpt-4o",
            "gpt-5",
        ),
        capabilities=(
            "chat",
            "vision",
        ),
        available=True,
        enabled=True,
        default_model="gpt-5",
        priority=10,
        timeout=30.0,
        max_retries=3,
        metadata={
            "region": "global",
        },
    )
# ----------------------------------------------------------------------
# Constructor Tests
# ----------------------------------------------------------------------


def test_provider_info_type(
    provider_info,
):

    assert isinstance(
        provider_info,
        ProviderInfo,
    )


def test_provider_name(
    provider_info,
):

    assert provider_info.name == "openai"


def test_display_name(
    provider_info,
):

    assert provider_info.display_name == "OpenAI"


def test_provider_version(
    provider_info,
):

    assert provider_info.version == "1.0"


def test_default_version():

    provider = ProviderInfo(
        name="test",
        display_name="Test",
    )

    assert (
        provider.version
        == DEFAULT_PROVIDER_VERSION
    )


def test_default_timeout():

    provider = ProviderInfo(
        name="test",
        display_name="Test",
    )

    assert provider.timeout == 30.0


def test_default_priority():

    provider = ProviderInfo(
        name="test",
        display_name="Test",
    )

    assert provider.priority == 100


def test_default_retries():

    provider = ProviderInfo(
        name="test",
        display_name="Test",
    )

    assert provider.max_retries == 3


def test_default_metadata():

    provider = ProviderInfo(
        name="test",
        display_name="Test",
    )

    assert provider.metadata == {}

# ----------------------------------------------------------------------
# Validation Tests
# ----------------------------------------------------------------------


def test_empty_name():

    with pytest.raises(ValueError):

        ProviderInfo(
            name="",
            display_name="Test",
        )


def test_empty_display_name():

    with pytest.raises(ValueError):

        ProviderInfo(
            name="test",
            display_name="",
        )


def test_negative_priority():

    with pytest.raises(ValueError):

        ProviderInfo(
            name="test",
            display_name="Test",
            priority=-1,
        )


def test_zero_timeout():

    with pytest.raises(ValueError):

        ProviderInfo(
            name="test",
            display_name="Test",
            timeout=0,
        )


def test_negative_timeout():

    with pytest.raises(ValueError):

        ProviderInfo(
            name="test",
            display_name="Test",
            timeout=-1,
        )


def test_negative_retries():

    with pytest.raises(ValueError):

        ProviderInfo(
            name="test",
            display_name="Test",
            max_retries=-1,
        )


def test_name_normalization():

    provider = ProviderInfo(
        name=" OpenAI ",
        display_name="OpenAI",
    )

    assert provider.name == "openai"


def test_display_name_trim():

    provider = ProviderInfo(
        name="openai",
        display_name=" OpenAI ",
    )

    assert provider.display_name == "OpenAI"

# ----------------------------------------------------------------------
# Property Tests
# ----------------------------------------------------------------------


def test_model_count(
    provider_info,
):

    assert provider_info.model_count == 2


def test_capability_count(
    provider_info,
):

    assert provider_info.capability_count == 2


def test_is_available(
    provider_info,
):

    assert provider_info.is_available is True


def test_is_enabled(
    provider_info,
):

    assert provider_info.is_enabled is True


def test_is_active(
    provider_info,
):

    assert provider_info.is_active is True


def test_supports_models(
    provider_info,
):

    assert provider_info.supports_models is True


def test_supports_capabilities(
    provider_info,
):

    assert provider_info.supports_capabilities is True


def test_empty_models():

    provider = ProviderInfo(
        name="test",
        display_name="Test",
    )

    assert provider.supports_models is False


def test_empty_capabilities():

    provider = ProviderInfo(
        name="test",
        display_name="Test",
    )

    assert provider.supports_capabilities is False
    
# ----------------------------------------------------------------------
# Serialization Tests
# ----------------------------------------------------------------------


def test_to_dict(
    provider_info,
):

    data = provider_info.to_dict()

    assert isinstance(
        data,
        dict,
    )


def test_to_dict_name(
    provider_info,
):

    data = provider_info.to_dict()

    assert data["name"] == "openai"


def test_to_dict_version(
    provider_info,
):

    data = provider_info.to_dict()

    assert data["version"] == "1.0"


def test_from_dict(
    provider_info,
):

    data = provider_info.to_dict()

    restored = ProviderInfo.from_dict(
        data,
    )

    assert restored == provider_info


def test_copy(
    provider_info,
):

    copied = provider_info.copy()

    assert copied == provider_info

    assert copied is not provider_info


def test_copy_change_name(
    provider_info,
):

    copied = provider_info.copy(
        name="anthropic",
    )

    assert copied.name == "anthropic"

    assert provider_info.name == "openai"


def test_serialization_round_trip(
    provider_info,
):

    restored = ProviderInfo.from_dict(
        provider_info.to_dict(),
    )

    assert restored == provider_info

# ----------------------------------------------------------------------
# Serialization Tests
# ----------------------------------------------------------------------


def test_to_dict(
    provider_info,
):

    data = provider_info.to_dict()

    assert isinstance(
        data,
        dict,
    )


def test_to_dict_name(
    provider_info,
):

    data = provider_info.to_dict()

    assert data["name"] == "openai"


def test_to_dict_version(
    provider_info,
):

    data = provider_info.to_dict()

    assert data["version"] == "1.0"


def test_from_dict(
    provider_info,
):

    data = provider_info.to_dict()

    restored = ProviderInfo.from_dict(
        data,
    )

    assert restored == provider_info


def test_copy(
    provider_info,
):

    copied = provider_info.copy()

    assert copied == provider_info

    assert copied is not provider_info


def test_copy_change_name(
    provider_info,
):

    copied = provider_info.copy(
        name="anthropic",
    )

    assert copied.name == "anthropic"

    assert provider_info.name == "openai"


def test_serialization_round_trip(
    provider_info,
):

    restored = ProviderInfo.from_dict(
        provider_info.to_dict(),
    )

    assert restored == provider_info
    
# ----------------------------------------------------------------------
# Comparison Method Tests
# ----------------------------------------------------------------------


def test_equal(provider_info):

    other = provider_info.copy()

    assert provider_info == other


def test_not_equal(provider_info):

    other = provider_info.copy(
        version="2.0",
    )

    assert provider_info != other


def test_less_than(provider_info):

    other = provider_info.copy(
        priority=20,
    )

    assert provider_info < other


def test_greater_than(provider_info):

    other = provider_info.copy(
        priority=5,
    )

    assert provider_info > other


def test_less_equal(provider_info):

    other = provider_info.copy()

    assert provider_info <= other


def test_greater_equal(provider_info):

    other = provider_info.copy()

    assert provider_info >= other


def test_hash(provider_info):

    assert isinstance(
        hash(provider_info),
        int,
    )


def test_hash_equality(provider_info):

    other = provider_info.copy()

    assert (
        hash(provider_info)
        == hash(other)
    )
    
# ----------------------------------------------------------------------
# Module Helper Function Tests
# ----------------------------------------------------------------------


def test_provider_from_dict(
    provider_info,
):

    restored = provider_from_dict(
        provider_info.to_dict(),
    )

    assert restored == provider_info


def test_provider_to_dict(
    provider_info,
):

    data = provider_to_dict(
        provider_info,
    )

    assert isinstance(
        data,
        dict,
    )


def test_is_provider_available(
    provider_info,
):

    assert is_provider_available(
        provider_info,
    )


def test_is_provider_enabled(
    provider_info,
):

    assert is_provider_enabled(
        provider_info,
    )


def test_is_provider_active(
    provider_info,
):

    assert is_provider_active(
        provider_info,
    )


def test_provider_to_dict_matches_method(
    provider_info,
):

    assert (

        provider_to_dict(
            provider_info,
        )

        ==

        provider_info.to_dict()

    )

# ----------------------------------------------------------------------
# Python Special Method Tests
# ----------------------------------------------------------------------


def test_str(provider_info):

    assert (
        str(provider_info)
        == "OpenAI"
    )


def test_repr(provider_info):

    text = repr(
        provider_info,
    )

    assert (
        "ProviderInfo"
        in text
    )

    assert (
        "openai"
        in text
    )


def test_bool(provider_info):

    assert bool(
        provider_info,
    )


def test_inactive_bool(provider_info):

    inactive = provider_info.copy(
        enabled=False,
    )

    assert not bool(
        inactive,
    )


def test_repr_returns_string(
    provider_info,
):

    assert isinstance(
        repr(provider_info),
        str,
    )


def test_str_returns_string(
    provider_info,
):

    assert isinstance(
        str(provider_info),
        str,
    )

# ----------------------------------------------------------------------
# Stress, Stability & Consistency Tests
# ----------------------------------------------------------------------


def test_hundred_provider_infos():

    providers = [

        ProviderInfo(
            name=f"provider{i}",
            display_name=f"Provider {i}",
        )

        for i in range(100)

    ]

    assert len(providers) == 100


def test_provider_info_uniqueness():

    providers = [

        ProviderInfo(
            name=f"provider{i}",
            display_name=f"Provider {i}",
        )

        for i in range(100)

    ]

    assert (

        len(
            {
                id(p)
                for p in providers
            }
        )

        == 100

    )


def test_to_dict_stability(
    provider_info,
):

    first = provider_info.to_dict()

    for _ in range(100):

        assert (
            provider_info.to_dict()
            == first
        )


def test_copy_stability(
    provider_info,
):

    for _ in range(100):

        copied = provider_info.copy()

        assert copied == provider_info


def test_serialization_stability(
    provider_info,
):

    for _ in range(100):

        restored = ProviderInfo.from_dict(
            provider_info.to_dict(),
        )

        assert restored == provider_info


def test_metadata_isolation(
    provider_info,
):

    copied = provider_info.copy()

    copied.metadata["new"] = 1

    assert (
        "new"
        not in provider_info.metadata
    )


def test_helper_function_consistency(
    provider_info,
):

    for _ in range(100):

        assert (
            provider_from_dict(
                provider_info.to_dict(),
            )

            ==

            provider_info

        )


def test_bool_stability(
    provider_info,
):

    for _ in range(100):

        assert bool(
            provider_info,
        )


def test_repr_stability(
    provider_info,
):

    first = repr(
        provider_info,
    )

    for _ in range(100):

        assert (
            repr(provider_info)
            == first
        )


def test_str_stability(
    provider_info,
):

    first = str(
        provider_info,
    )

    for _ in range(100):

        assert (
            str(provider_info)
            == first
        )
