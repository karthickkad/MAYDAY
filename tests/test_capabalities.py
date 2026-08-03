"""
test_capabilities.py

Unit tests for capabilities.py
"""

from __future__ import annotations

import pytest

from ai.providers.capabilities import (
    Capability,
    ALL_CAPABILITIES,
    CORE_CAPABILITIES,
    MULTIMODAL_CAPABILITIES,
    AUDIO_CAPABILITIES,
    is_valid_capability,
    validate_capability,
    validate_capabilities,
    has_capability,
    has_all_capabilities,
    has_any_capability,
    capability_to_string,
    capability_from_string,
    capabilities_to_strings,
    capabilities_from_strings,
    unique_capabilities,
    sort_capabilities,
    merge_capabilities,
    CAPABILITY_REGISTRY,
    CAPABILITY_GROUPS,
    get_capability,
    get_all_capabilities,
    get_capability_group,
)


# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------


@pytest.fixture
def sample_capabilities():

    return (
        Capability.CHAT,
        Capability.STREAMING,
        Capability.VISION,
    )
    
# ----------------------------------------------------------------------
# Capability Enum Tests
# ----------------------------------------------------------------------


def test_capability_type():

    assert isinstance(
        Capability.CHAT,
        Capability,
    )


def test_capability_value():

    assert (
        Capability.CHAT.value
        == "chat"
    )


def test_capability_string():

    assert (
        str(
            Capability.CHAT,
        )
        == "chat"
    )


def test_all_capabilities_not_empty():

    assert len(
        ALL_CAPABILITIES,
    ) > 0


def test_core_capabilities():

    assert (
        Capability.CHAT
        in CORE_CAPABILITIES
    )


def test_multimodal_capabilities():

    assert (
        Capability.VISION
        in MULTIMODAL_CAPABILITIES
    )


def test_audio_capabilities():

    assert (
        Capability.TEXT_TO_SPEECH
        in AUDIO_CAPABILITIES
    )
    
# ----------------------------------------------------------------------
# Validation Tests
# ----------------------------------------------------------------------


def test_valid_capability():

    assert is_valid_capability(
        "chat",
    )


def test_invalid_capability():

    assert not is_valid_capability(
        "invalid",
    )


def test_validate_capability_string():

    capability = validate_capability(
        "chat",
    )

    assert (
        capability
        == Capability.CHAT
    )


def test_validate_capability_enum():

    capability = validate_capability(
        Capability.CHAT,
    )

    assert (
        capability
        == Capability.CHAT
    )


def test_validate_invalid_capability():

    with pytest.raises(
        ValueError,
    ):

        validate_capability(
            "abc",
        )


def test_validate_capabilities():

    capabilities = validate_capabilities(
        (
            "chat",
            "vision",
        ),
    )

    assert capabilities == (
        Capability.CHAT,
        Capability.VISION,
    )
# ----------------------------------------------------------------------
# Query Function Tests
# ----------------------------------------------------------------------


def test_has_capability(
    sample_capabilities,
):

    assert has_capability(
        sample_capabilities,
        Capability.CHAT,
    )


def test_has_missing_capability(
    sample_capabilities,
):

    assert not has_capability(
        sample_capabilities,
        Capability.EMBEDDING,
    )


def test_has_all_capabilities(
    sample_capabilities,
):

    assert has_all_capabilities(
        sample_capabilities,
        (
            Capability.CHAT,
            Capability.VISION,
        ),
    )


def test_missing_all_capabilities(
    sample_capabilities,
):

    assert not has_all_capabilities(
        sample_capabilities,
        (
            Capability.CHAT,
            Capability.EMBEDDING,
        ),
    )


def test_has_any_capability(
    sample_capabilities,
):

    assert has_any_capability(
        sample_capabilities,
        (
            Capability.EMBEDDING,
            Capability.VISION,
        ),
    )


def test_has_no_matching_capability(
    sample_capabilities,
):

    assert not has_any_capability(
        sample_capabilities,
        (
            Capability.EMBEDDING,
            Capability.JSON_MODE,
        ),
    )
# ----------------------------------------------------------------------
# Conversion Function Tests
# ----------------------------------------------------------------------


def test_capability_to_string():

    assert (
        capability_to_string(
            Capability.CHAT,
        )
        == "chat"
    )


def test_capability_from_string():

    assert (
        capability_from_string(
            "vision",
        )
        == Capability.VISION
    )


def test_capabilities_to_strings():

    values = capabilities_to_strings(
        (
            Capability.CHAT,
            Capability.VISION,
        ),
    )

    assert values == (
        "chat",
        "vision",
    )


def test_capabilities_from_strings():

    capabilities = capabilities_from_strings(
        (
            "chat",
            "vision",
        ),
    )

    assert capabilities == (
        Capability.CHAT,
        Capability.VISION,
    )


def test_conversion_round_trip():

    original = (
        Capability.CHAT,
        Capability.STREAMING,
    )

    restored = capabilities_from_strings(
        capabilities_to_strings(
            original,
        ),
    )

    assert restored == original
    
# ----------------------------------------------------------------------
# Utility Function Tests
# ----------------------------------------------------------------------


def test_unique_capabilities():

    capabilities = unique_capabilities(
        (
            Capability.CHAT,
            Capability.CHAT,
            Capability.VISION,
        ),
    )

    assert capabilities == (
        Capability.CHAT,
        Capability.VISION,
    )


def test_sort_capabilities():

    capabilities = sort_capabilities(
        (
            Capability.VISION,
            Capability.CHAT,
            Capability.EMBEDDING,
        ),
    )

    assert capabilities == (
        Capability.CHAT,
        Capability.EMBEDDING,
        Capability.VISION,
    )


def test_merge_capabilities():

    merged = merge_capabilities(
        CORE_CAPABILITIES,
        MULTIMODAL_CAPABILITIES,
    )

    assert Capability.CHAT in merged

    assert Capability.VISION in merged


def test_merge_duplicates():

    merged = merge_capabilities(
        CORE_CAPABILITIES,
        CORE_CAPABILITIES,
    )

    assert len(merged) == len(set(merged))


def test_unique_returns_tuple():

    assert isinstance(
        unique_capabilities(
            (
                Capability.CHAT,
            ),
        ),
        tuple,
    )


def test_sort_returns_tuple():

    assert isinstance(
        sort_capabilities(
            (
                Capability.CHAT,
            ),
        ),
        tuple,
    )
# ----------------------------------------------------------------------
# Capability Registry Tests
# ----------------------------------------------------------------------


def test_registry_type():

    assert isinstance(
        CAPABILITY_REGISTRY,
        dict,
    )


def test_registry_contains_chat():

    assert (
        "chat"
        in CAPABILITY_REGISTRY
    )


def test_registry_value():

    assert (
        CAPABILITY_REGISTRY["chat"]
        == Capability.CHAT
    )


def test_groups_type():

    assert isinstance(
        CAPABILITY_GROUPS,
        dict,
    )


def test_group_exists():

    assert (
        "core"
        in CAPABILITY_GROUPS
    )


def test_group_contents():

    assert (
        Capability.CHAT
        in CAPABILITY_GROUPS["core"]
    )
# ----------------------------------------------------------------------
# Public Helper Function Tests
# ----------------------------------------------------------------------


def test_get_capability():

    assert (
        get_capability(
            "chat",
        )
        == Capability.CHAT
    )


def test_get_all_capabilities():

    assert (
        get_all_capabilities()
        == ALL_CAPABILITIES
    )


def test_get_group():

    assert (
        get_capability_group(
            "core",
        )
        == CORE_CAPABILITIES
    )


def test_unknown_group():

    with pytest.raises(
        ValueError,
    ):

        get_capability_group(
            "unknown",
        )


def test_get_capability_invalid():

    with pytest.raises(
        ValueError,
    ):

        get_capability(
            "invalid",
        )
# ----------------------------------------------------------------------
# Python Special Method Tests
# ----------------------------------------------------------------------


def test_capability_str():

    assert (
        str(
            Capability.CHAT,
        )
        == "chat"
    )


def test_capability_repr():

    assert (
        "CHAT"
        in repr(
            Capability.CHAT,
        )
    )


def test_capability_hash():

    assert isinstance(
        hash(
            Capability.CHAT,
        ),
        int,
    )


def test_capability_equality():

    assert (
        Capability.CHAT
        == Capability.CHAT
    )


def test_capability_inequality():

    assert (
        Capability.CHAT
        != Capability.VISION
    )


def test_enum_iteration():

    assert len(
        list(
            Capability,
        )
    ) > 0
# ----------------------------------------------------------------------
# Stress, Stability & Consistency Tests
# ----------------------------------------------------------------------


def test_validation_stability():

    for _ in range(100):

        assert (
            validate_capability(
                "chat",
            )
            == Capability.CHAT
        )


def test_conversion_stability():

    original = (
        Capability.CHAT,
        Capability.VISION,
    )

    for _ in range(100):

        restored = capabilities_from_strings(
            capabilities_to_strings(
                original,
            ),
        )

        assert restored == original


def test_registry_stability():

    registry = CAPABILITY_REGISTRY.copy()

    for _ in range(100):

        assert (
            registry
            == CAPABILITY_REGISTRY
        )


def test_group_stability():

    groups = CAPABILITY_GROUPS.copy()

    for _ in range(100):

        assert (
            groups
            == CAPABILITY_GROUPS
        )


def test_merge_stability():

    expected = merge_capabilities(
        CORE_CAPABILITIES,
        AUDIO_CAPABILITIES,
    )

    for _ in range(100):

        assert (
            merge_capabilities(
                CORE_CAPABILITIES,
                AUDIO_CAPABILITIES,
            )
            == expected
        )


def test_unique_stability():

    expected = unique_capabilities(
        (
            Capability.CHAT,
            Capability.CHAT,
            Capability.VISION,
        ),
    )

    for _ in range(100):

        assert (
            unique_capabilities(
                (
                    Capability.CHAT,
                    Capability.CHAT,
                    Capability.VISION,
                ),
            )
            == expected
        )


def test_sort_stability():

    expected = sort_capabilities(
        (
            Capability.VISION,
            Capability.CHAT,
        ),
    )

    for _ in range(100):

        assert (
            sort_capabilities(
                (
                    Capability.VISION,
                    Capability.CHAT,
                ),
            )
            == expected
        )


def test_enum_uniqueness():

    values = [

        capability.value

        for capability in Capability

    ]

    assert len(values) == len(set(values))


def test_all_capabilities_unique():

    assert len(
        ALL_CAPABILITIES,
    ) == len(
        set(
            ALL_CAPABILITIES,
        ),
    )


def test_registry_consistency():

    for capability in Capability:

        assert (

            CAPABILITY_REGISTRY[
                capability.value
            ]

            ==

            capability

        )
    
