"""
capabilities.py

Capability definitions for MAYDAY.
"""

from __future__ import annotations

from enum import Enum
from typing import Final

__all__ = (
    "Capability",
    "ALL_CAPABILITIES",
    "CORE_CAPABILITIES",
    "MULTIMODAL_CAPABILITIES",
    "AUDIO_CAPABILITIES",
    "is_valid_capability",
    "validate_capability",
    "validate_capabilities",
    "has_capability",
    "has_all_capabilities",
    "has_any_capability",
)

# ----------------------------------------------------------------------
# Module Constants
# ----------------------------------------------------------------------

DEFAULT_CAPABILITY_SEPARATOR: Final[str] = ","

# ----------------------------------------------------------------------
# Capability Enumeration
# ----------------------------------------------------------------------


class Capability(
    str,
    Enum,
):
    """
    Supported provider capabilities.
    """

    CHAT = "chat"

    COMPLETION = "completion"

    STREAMING = "streaming"

    EMBEDDING = "embedding"

    FUNCTION_CALLING = "function_calling"

    TOOLS = "tools"

    JSON_MODE = "json_mode"

    VISION = "vision"

    IMAGE_GENERATION = "image_generation"

    IMAGE_EDITING = "image_editing"

    AUDIO_TRANSCRIPTION = "audio_transcription"

    TEXT_TO_SPEECH = "text_to_speech"

    SPEECH_TO_TEXT = "speech_to_text"

    MODERATION = "moderation"

    RERANKING = "reranking"

    def __str__(
        self,
    ) -> str:

        return self.value
    
# ----------------------------------------------------------------------
# Capability Groups
# ----------------------------------------------------------------------

ALL_CAPABILITIES = tuple(
    Capability,
)

CORE_CAPABILITIES = (
    Capability.CHAT,
    Capability.COMPLETION,
    Capability.STREAMING,
)

MULTIMODAL_CAPABILITIES = (
    Capability.VISION,
    Capability.IMAGE_GENERATION,
    Capability.IMAGE_EDITING,
)

AUDIO_CAPABILITIES = (
    Capability.AUDIO_TRANSCRIPTION,
    Capability.TEXT_TO_SPEECH,
    Capability.SPEECH_TO_TEXT,
)

# ----------------------------------------------------------------------
# Validation Functions
# ----------------------------------------------------------------------


def is_valid_capability(
    capability: str | Capability,
) -> bool:
    """
    Return True if capability is valid.
    """

    try:

        Capability(
            capability,
        )

        return True

    except ValueError:

        return False


def validate_capability(
    capability: str | Capability,
) -> Capability:
    """
    Validate and normalize a capability.
    """

    if isinstance(
        capability,
        Capability,
    ):
        return capability

    return Capability(
        capability.strip().lower(),
    )


def validate_capabilities(
    capabilities: tuple[
        str | Capability,
        ...,
    ],
) -> tuple[
    Capability,
    ...,
]:
    """
    Validate multiple capabilities.
    """

    return tuple(

        validate_capability(
            capability,
        )

        for capability in capabilities

    )
# ----------------------------------------------------------------------
# Query Functions
# ----------------------------------------------------------------------


def has_capability(
    capabilities: tuple[
        Capability,
        ...,
    ],
    capability: Capability,
) -> bool:
    """
    Return True if capability exists.
    """

    return (
        capability
        in capabilities
    )


def has_all_capabilities(
    capabilities: tuple[
        Capability,
        ...,
    ],
    required: tuple[
        Capability,
        ...,
    ],
) -> bool:
    """
    Return True if all capabilities exist.
    """

    return all(

        capability
        in capabilities

        for capability in required

    )


def has_any_capability(
    capabilities: tuple[
        Capability,
        ...,
    ],
    required: tuple[
        Capability,
        ...,
    ],
) -> bool:
    """
    Return True if any capability exists.
    """

    return any(

        capability
        in capabilities

        for capability in required

    )
# ----------------------------------------------------------------------
# Conversion Functions
# ----------------------------------------------------------------------


def capability_to_string(
    capability: Capability,
) -> str:
    """
    Convert a capability into a string.
    """

    return capability.value


def capability_from_string(
    capability: str,
) -> Capability:
    """
    Convert a string into a Capability.
    """

    return validate_capability(
        capability,
    )


def capabilities_to_strings(
    capabilities: tuple[
        Capability,
        ...,
    ],
) -> tuple[
    str,
    ...,
]:
    """
    Convert capabilities into strings.
    """

    return tuple(

        capability.value

        for capability in capabilities

    )


def capabilities_from_strings(
    capabilities: tuple[
        str,
        ...,
    ],
) -> tuple[
    Capability,
    ...,
]:
    """
    Convert strings into capabilities.
    """

    return validate_capabilities(
        capabilities,
    )
# ----------------------------------------------------------------------
# Utility Functions
# ----------------------------------------------------------------------


def unique_capabilities(
    capabilities: tuple[
        Capability,
        ...,
    ],
) -> tuple[
    Capability,
    ...,
]:
    """
    Remove duplicate capabilities.
    """

    return tuple(

        dict.fromkeys(
            capabilities,
        )

    )


def sort_capabilities(
    capabilities: tuple[
        Capability,
        ...,
    ],
) -> tuple[
    Capability,
    ...,
]:
    """
    Sort capabilities alphabetically.
    """

    return tuple(

        sorted(
            capabilities,
            key=lambda capability: capability.value,
        )

    )


def merge_capabilities(
    *groups: tuple[
        Capability,
        ...,
    ],
) -> tuple[
    Capability,
    ...,
]:
    """
    Merge multiple capability groups.
    """

    merged = ()

    for group in groups:

        merged += group

    return unique_capabilities(
        merged,
    )
# ----------------------------------------------------------------------
# Capability Registry
# ----------------------------------------------------------------------

CAPABILITY_REGISTRY = {

    capability.value: capability

    for capability in Capability

}


CAPABILITY_GROUPS = {

    "all": ALL_CAPABILITIES,

    "core": CORE_CAPABILITIES,

    "multimodal": MULTIMODAL_CAPABILITIES,

    "audio": AUDIO_CAPABILITIES,

}
# ----------------------------------------------------------------------
# Public Helper Functions
# ----------------------------------------------------------------------


def get_capability(
    name: str,
) -> Capability:
    """
    Return a capability by name.
    """

    return validate_capability(
        name,
    )


def get_all_capabilities(
) -> tuple[
    Capability,
    ...,
]:
    """
    Return every capability.
    """

    return ALL_CAPABILITIES


def get_capability_group(
    name: str,
) -> tuple[
    Capability,
    ...,
]:
    """
    Return a predefined capability group.
    """

    try:

        return CAPABILITY_GROUPS[
            name.lower()
        ]

    except KeyError as error:

        raise ValueError(
            f"Unknown capability group: {name}"
        ) from error

# ----------------------------------------------------------------------
# Module Finalization
# ----------------------------------------------------------------------

# This module intentionally contains no executable code.
#
# Capability provides the canonical feature definitions
# used throughout MAYDAY.
#
# Every provider advertises its supported capabilities
# using this enumeration.
#
# The helper functions in this module provide validation,
# conversion, grouping, querying, and registry access.
