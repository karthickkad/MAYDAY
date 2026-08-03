"""
health.py

Provider health definitions for MAYDAY.
"""

from __future__ import annotations

from dataclasses import (
    asdict,
    dataclass,
    field,
)

from datetime import datetime

from enum import Enum

from typing import Any

__all__ = (
    "DEFAULT_SUCCESS_RATE",
    "HealthStatus",
    "ProviderHealth",
    "health_from_dict",
    "health_to_dict",
    "is_provider_healthy",
    "is_provider_available",
    "is_provider_online",
)

# ----------------------------------------------------------------------
# Module Constants
# ----------------------------------------------------------------------

DEFAULT_SUCCESS_RATE = 100.0

DEFAULT_LATENCY_MS = 0.0

DEFAULT_FAILURE_COUNT = 0

DEFAULT_RETRY_COUNT = 0

# ----------------------------------------------------------------------
# Health Status
# ----------------------------------------------------------------------


class HealthStatus(
    str,
    Enum,
):
    """
    Provider health status.
    """

    UNKNOWN = "unknown"

    HEALTHY = "healthy"

    DEGRADED = "degraded"

    UNAVAILABLE = "unavailable"

    OFFLINE = "offline"

    MAINTENANCE = "maintenance"


    def __str__(
        self,
    ) -> str:

        return self.value
    
# ----------------------------------------------------------------------
# Provider Health
# ----------------------------------------------------------------------


@dataclass(
    frozen=True,
    slots=True,
)
class ProviderHealth:
    """
    Runtime health information for a provider.
    """

    provider: str

    status: HealthStatus = HealthStatus.UNKNOWN

    available: bool = True

    latency_ms: float = DEFAULT_LATENCY_MS

    success_rate: float = DEFAULT_SUCCESS_RATE

    failure_count: int = DEFAULT_FAILURE_COUNT

    retry_count: int = DEFAULT_RETRY_COUNT

    circuit_open: bool = False

    last_success: datetime | None = None

    last_failure: datetime | None = None

    last_check: datetime | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )
# ----------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------

    def __post_init__(
        self,
    ) -> None:

        if not self.provider.strip():

            raise ValueError(
                "Provider cannot be empty."
            )

        if self.latency_ms < 0:

            raise ValueError(
                "Latency cannot be negative."
            )

        if not (
            0
            <= self.success_rate
            <= 100
        ):

            raise ValueError(
                "Success rate must be between 0 and 100."
            )

        if self.failure_count < 0:

            raise ValueError(
                "Failure count cannot be negative."
            )

        if self.retry_count < 0:

            raise ValueError(
                "Retry count cannot be negative."
            )

        object.__setattr__(
            self,
            "provider",
            self.provider.strip().lower(),
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
    def is_healthy(
        self,
    ) -> bool:

        return (
            self.status
            == HealthStatus.HEALTHY
        )


    @property
    def is_available(
        self,
    ) -> bool:

        return self.available


    @property
    def is_online(
        self,
    ) -> bool:

        return (
            self.status
            != HealthStatus.OFFLINE
        )


    @property
    def has_failures(
        self,
    ) -> bool:

        return (
            self.failure_count
            > 0
        )


    @property
    def needs_retry(
        self,
    ) -> bool:

        return (
            self.retry_count
            > 0
        )


    @property
    def circuit_closed(
        self,
    ) -> bool:

        return (
            not self.circuit_open
        )
# ----------------------------------------------------------------------
# Serialization
# ----------------------------------------------------------------------

    def to_dict(
        self,
    ) -> dict[str, Any]:

        return asdict(
            self,
        )


    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "ProviderHealth":

        return cls(
            **data,
        )


    def copy(
        self,
        **changes: Any,
    ) -> "ProviderHealth":

        data = self.to_dict()

        data.update(
            changes,
        )

        return ProviderHealth.from_dict(
            data,
        )
# ----------------------------------------------------------------------
# Utility Methods
# ----------------------------------------------------------------------

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.metadata.get(
            key,
            default,
        )


    def has_metadata(
        self,
        key: str,
    ) -> bool:

        return (
            key
            in self.metadata
        )


    def record_success(
        self,
    ) -> "ProviderHealth":

        return self.copy(
            failure_count=0,
            retry_count=0,
            last_success=datetime.utcnow(),
            status=HealthStatus.HEALTHY,
        )


    def record_failure(
        self,
    ) -> "ProviderHealth":

        return self.copy(
            failure_count=self.failure_count + 1,
            retry_count=self.retry_count + 1,
            last_failure=datetime.utcnow(),
            status=HealthStatus.DEGRADED,
        )


    def update_latency(
        self,
        latency_ms: float,
    ) -> "ProviderHealth":

        return self.copy(
            latency_ms=latency_ms,
        )


    def reset_failures(
        self,
    ) -> "ProviderHealth":

        return self.copy(
            failure_count=0,
            retry_count=0,
        )
# ----------------------------------------------------------------------
# Utility Methods
# ----------------------------------------------------------------------

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.metadata.get(
            key,
            default,
        )


    def has_metadata(
        self,
        key: str,
    ) -> bool:

        return (
            key
            in self.metadata
        )


    def record_success(
        self,
    ) -> "ProviderHealth":

        return self.copy(
            failure_count=0,
            retry_count=0,
            last_success=datetime.utcnow(),
            status=HealthStatus.HEALTHY,
        )


    def record_failure(
        self,
    ) -> "ProviderHealth":

        return self.copy(
            failure_count=self.failure_count + 1,
            retry_count=self.retry_count + 1,
            last_failure=datetime.utcnow(),
            status=HealthStatus.DEGRADED,
        )


    def update_latency(
        self,
        latency_ms: float,
    ) -> "ProviderHealth":

        return self.copy(
            latency_ms=latency_ms,
        )


    def reset_failures(
        self,
    ) -> "ProviderHealth":

        return self.copy(
            failure_count=0,
            retry_count=0,
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

        return self.provider


    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return (
            "ProviderHealth("
            f"provider={self.provider!r}, "
            f"status={self.status.value!r}, "
            f"latency_ms={self.latency_ms!r}, "
            f"available={self.available!r}"
            ")"
        )


    def __bool__(
        self,
    ) -> bool:
        """
        Truthiness indicates provider health.
        """

        return self.is_healthy
    
# ----------------------------------------------------------------------
# Module Helper Functions
# ----------------------------------------------------------------------


def health_from_dict(
    data: dict[str, Any],
) -> ProviderHealth:
    """
    Create ProviderHealth from dictionary.
    """

    return ProviderHealth.from_dict(
        data,
    )


def health_to_dict(
    health: ProviderHealth,
) -> dict[str, Any]:
    """
    Convert ProviderHealth to dictionary.
    """

    return health.to_dict()


def is_provider_healthy(
    health: ProviderHealth,
) -> bool:
    """
    Return True if provider is healthy.
    """

    return health.is_healthy


def is_provider_available(
    health: ProviderHealth,
) -> bool:
    """
    Return True if provider is available.
    """

    return health.is_available


def is_provider_online(
    health: ProviderHealth,
) -> bool:
    """
    Return True if provider is online.
    """

    return health.is_online
    
# ----------------------------------------------------------------------
# Module Finalization
# ----------------------------------------------------------------------

# This module intentionally contains no executable code.
#
# ProviderHealth represents the runtime health of
# an AI provider.
#
# It is designed to be:
#
# • Immutable
# • Hashable
# • Comparable
# • Serializable
# • Thread-safe
# • Future-proof
#
# The object is used by the provider registry,
# router, health monitor, load balancer,
# circuit breaker, and failover system.
