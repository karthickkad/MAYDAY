"""
provider_info.py

Provider metadata definitions for MAYDAY.
"""

from __future__ import annotations

from dataclasses import (
    asdict,
    dataclass,
    field,
)

from typing import Any

__all__ = (
    "provider_from_dict",
    "provider_to_dict",
    "is_provider_available",
    "is_provider_enabled",
    "is_provider_active",
)

# ----------------------------------------------------------------------
# Module Constants
# ----------------------------------------------------------------------

DEFAULT_PROVIDER_VERSION = "1.0"

# ----------------------------------------------------------------------
# Provider Information
# ----------------------------------------------------------------------


@dataclass(
    frozen=True,
    slots=True,
)
class ProviderInfo:
    """
    Immutable metadata describing an AI provider.
    """

    # --------------------------------------------------------------
    # Identity
    # --------------------------------------------------------------

    name: str

    display_name: str

    version: str = DEFAULT_PROVIDER_VERSION

    description: str = ""

    # --------------------------------------------------------------
    # Provider Details
    # --------------------------------------------------------------

    website: str = ""

    documentation_url: str = ""

    api_base_url: str = ""

    # --------------------------------------------------------------
    # Features
    # --------------------------------------------------------------

    supported_models: tuple[str, ...] = ()

    capabilities: tuple[str, ...] = ()

    # --------------------------------------------------------------
    # Runtime
    # --------------------------------------------------------------

    available: bool = True

    enabled: bool = True

    default_model: str | None = None

    priority: int = 100

    timeout: float = 30.0

    max_retries: int = 3

    # --------------------------------------------------------------
    # Custom Metadata
    # --------------------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )
    
# ----------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------

    def __post_init__(
        self,
    ) -> None:
        """
        Validate and normalize provider information.
        """

        # --------------------------------------------------------------
        # Required Fields
        # --------------------------------------------------------------

        if not self.name.strip():

            raise ValueError(
                "Provider name cannot be empty."
            )

        if not self.display_name.strip():

            raise ValueError(
                "Provider display_name cannot be empty."
            )

        # --------------------------------------------------------------
        # Numeric Validation
        # --------------------------------------------------------------

        if self.priority < 0:

            raise ValueError(
                "priority must be >= 0."
            )

        if self.timeout <= 0:

            raise ValueError(
                "timeout must be greater than 0."
            )

        if self.max_retries < 0:

            raise ValueError(
                "max_retries must be >= 0."
            )

        # --------------------------------------------------------------
        # Normalize Strings
        # --------------------------------------------------------------

        object.__setattr__(
            self,
            "name",
            self.name.strip().lower(),
        )

        object.__setattr__(
            self,
            "display_name",
            self.display_name.strip(),
        )

        object.__setattr__(
            self,
            "version",
            self.version.strip(),
        )

        object.__setattr__(
            self,
            "description",
            self.description.strip(),
        )

        object.__setattr__(
            self,
            "website",
            self.website.strip(),
        )

        object.__setattr__(
            self,
            "documentation_url",
            self.documentation_url.strip(),
        )

        object.__setattr__(
            self,
            "api_base_url",
            self.api_base_url.strip(),
        )

        # --------------------------------------------------------------
        # Normalize Collections
        # --------------------------------------------------------------

        object.__setattr__(
            self,
            "supported_models",
            tuple(self.supported_models),
        )

        object.__setattr__(
            self,
            "capabilities",
            tuple(self.capabilities),
        )

        object.__setattr__(
            self,
            "metadata",
            dict(self.metadata),
        )
# ----------------------------------------------------------------------
# Computed Properties
# ----------------------------------------------------------------------

    @property
    def model_count(
        self,
    ) -> int:
        """
        Return the number of supported models.
        """

        return len(
            self.supported_models,
        )


    @property
    def capability_count(
        self,
    ) -> int:
        """
        Return the number of supported capabilities.
        """

        return len(
            self.capabilities,
        )


    @property
    def is_available(
        self,
    ) -> bool:
        """
        Return whether the provider is available.
        """

        return self.available


    @property
    def is_enabled(
        self,
    ) -> bool:
        """
        Return whether the provider is enabled.
        """

        return self.enabled


    @property
    def is_active(
        self,
    ) -> bool:
        """
        Return True when the provider can
        receive requests.
        """

        return (
            self.available
            and self.enabled
        )


    @property
    def supports_models(
        self,
    ) -> bool:
        """
        Return True if models are available.
        """

        return bool(
            self.supported_models,
        )


    @property
    def supports_capabilities(
        self,
    ) -> bool:
        """
        Return True if capabilities exist.
        """

        return bool(
            self.capabilities,
        )
# ----------------------------------------------------------------------
# Serialization
# ----------------------------------------------------------------------

    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Convert the provider information
        into a dictionary.
        """

        return asdict(
            self,
        )


    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "ProviderInfo":
        """
        Create a ProviderInfo instance
        from a dictionary.
        """

        return cls(
            **data,
        )


    def copy(
        self,
        **changes: Any,
    ) -> "ProviderInfo":
        """
        Return a copy with updated fields.
        """

        data = self.to_dict()

        data.update(
            changes,
        )

        return ProviderInfo.from_dict(
            data,
        )
# ----------------------------------------------------------------------
# Utility Methods
# ----------------------------------------------------------------------

    def supports_model(
        self,
        model: str,
    ) -> bool:
        """
        Return True if the provider supports
        the specified model.
        """

        return (
            model in self.supported_models
        )


    def supports_capability(
        self,
        capability: str,
    ) -> bool:
        """
        Return True if the provider supports
        the specified capability.
        """

        return (
            capability in self.capabilities
        )


    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Return a metadata value.
        """

        return self.metadata.get(
            key,
            default,
        )


    def has_metadata(
        self,
        key: str,
    ) -> bool:
        """
        Return True if metadata contains
        the specified key.
        """

        return (
            key in self.metadata
        )


    def supports(
        self,
        *,
        model: str | None = None,
        capability: str | None = None,
    ) -> bool:
        """
        Generic support check.
        """

        if (
            model is not None
            and not self.supports_model(model)
        ):
            return False

        if (
            capability is not None
            and not self.supports_capability(capability)
        ):
            return False

        return True
# ----------------------------------------------------------------------
# Comparison Methods
# ----------------------------------------------------------------------

    def __eq__(
        self,
        other: object,
    ) -> bool:
        """
        Compare providers by name and version.
        """

        if not isinstance(
            other,
            ProviderInfo,
        ):
            return NotImplemented

        return (

            self.name == other.name

            and

            self.version == other.version

        )


    def __lt__(
        self,
        other: "ProviderInfo",
    ) -> bool:
        """
        Lower priority value has higher precedence.
        """

        if not isinstance(
            other,
            ProviderInfo,
        ):
            return NotImplemented

        return (
            self.priority
            < other.priority
        )


    def __le__(
        self,
        other: "ProviderInfo",
    ) -> bool:

        return (
            self == other
            or self < other
        )


    def __gt__(
        self,
        other: "ProviderInfo",
    ) -> bool:

        if not isinstance(
            other,
            ProviderInfo,
        ):
            return NotImplemented

        return (
            self.priority
            > other.priority
        )


    def __ge__(
        self,
        other: "ProviderInfo",
    ) -> bool:

        return (
            self == other
            or self > other
        )


    def __hash__(
        self,
    ) -> int:
        """
        Hash by provider identity.
        """

        return hash(
            (
                self.name,
                self.version,
            )
        )
    # ------------------------------------------------------------------
    # Python Special Methods
    # ------------------------------------------------------------------

    def __str__(
        self,
    ) -> str:
        """
        Human-readable provider name.
        """

        return self.display_name


    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return (
            "ProviderInfo("
            f"name={self.name!r}, "
            f"display_name={self.display_name!r}, "
            f"version={self.version!r}, "
            f"enabled={self.enabled!r}, "
            f"available={self.available!r}, "
            f"priority={self.priority!r}"
            ")"
        )


    def __bool__(
        self,
    ) -> bool:
        """
        Truthiness indicates whether the
        provider is active.
        """

        return self.is_active
    
# ----------------------------------------------------------------------
# Module Helper Functions
# ----------------------------------------------------------------------


def provider_from_dict(
    data: dict[str, Any],
) -> ProviderInfo:
    """
    Create a ProviderInfo instance
    from a dictionary.
    """

    return ProviderInfo.from_dict(
        data,
    )


def provider_to_dict(
    provider: ProviderInfo,
) -> dict[str, Any]:
    """
    Convert ProviderInfo into
    a dictionary.
    """

    return provider.to_dict()


def is_provider_available(
    provider: ProviderInfo,
) -> bool:
    """
    Return whether the provider
    is available.
    """

    return provider.is_available


def is_provider_enabled(
    provider: ProviderInfo,
) -> bool:
    """
    Return whether the provider
    is enabled.
    """

    return provider.is_enabled


def is_provider_active(
    provider: ProviderInfo,
) -> bool:
    """
    Return whether the provider
    is active.
    """

    return provider.is_active

# ----------------------------------------------------------------------
# Module Finalization
# ----------------------------------------------------------------------

# This module intentionally contains no executable code.
#
# ProviderInfo is designed to be:
#
# • Immutable
# • Hashable
# • Comparable
# • Serializable
# • Memory efficient
# • Safe for concurrent use
#
# It serves as the canonical metadata object for all
# AI providers within the MAYDAY framework.
    
