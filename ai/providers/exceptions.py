""""
exceptions.py

Provider-specific exceptions for MAYDAY.

Defines the standard exception hierarchy used by all
provider implementations, the provider registry,
factory, manager, router, executor and pipeline.
"""
from __future__ import annotations

from copy import deepcopy

__all__ = (
    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    "DEFAULT_PROVIDER",
    "DEFAULT_TIMEOUT",
    "DEFAULT_RETRY_AFTER",

    # ------------------------------------------------------------------
    # Base
    # ------------------------------------------------------------------
    "ProviderError",

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------
    "ProviderRegistrationError",
    "ProviderAlreadyRegisteredError",
    "ProviderNotFoundError",

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------
    "ProviderConfigurationError",
    "ProviderAuthenticationError",
    "ProviderPermissionError",

    # ------------------------------------------------------------------
    # Connectivity
    # ------------------------------------------------------------------
    "ProviderConnectionError",
    "ProviderTimeoutError",
    "ProviderUnavailableError",

    # ------------------------------------------------------------------
    # Rate Limits
    # ------------------------------------------------------------------
    "ProviderRateLimitError",
    "ProviderQuotaExceededError",

    # ------------------------------------------------------------------
    # Response
    # ------------------------------------------------------------------
    "ProviderResponseError",
    "ProviderStreamingError",
    "ProviderCapabilityError",
    "ProviderModelNotFoundError",

    # ------------------------------------------------------------------
    # Helper Functions
    # ------------------------------------------------------------------
    "is_retryable",
    "get_provider",
    "get_error_code",
    "get_metadata",
    "exception_to_dict",
)

# ----------------------------------------------------------------------
# Module Constants
# ----------------------------------------------------------------------

DEFAULT_PROVIDER = "unknown"

DEFAULT_TIMEOUT = 30.0

DEFAULT_RETRY_AFTER = 0

# ----------------------------------------------------------------------
# Base Exception
# ----------------------------------------------------------------------


class ProviderError(Exception):
    """
    Base exception for all provider-related errors.

    Every provider exception in MAYDAY inherits from this
    class, providing a consistent interface for error
    handling, logging, telemetry and diagnostics.
    """

    def __init__(
        self,
        message: str,
        *,
        provider: str = DEFAULT_PROVIDER,
        error_code: str | None = None,
        retryable: bool = False,
        metadata: dict[str, object] | None = None,
    ) -> None:
        """
        Initialize the provider exception.

        Parameters
        ----------
        message:
            Human-readable error message.

        provider:
            Provider that raised the exception.

        error_code:
            Provider-specific error code.

        retryable:
            Indicates whether the operation may be
            retried safely.

        metadata:
            Additional diagnostic information.
        """

        super().__init__(message)

        self.message = message
        self.provider = provider
        self.error_code = error_code
        self.retryable = retryable
        self.metadata = metadata or {}

    # ------------------------------------------------------------------
    # Convenience Properties
    # ------------------------------------------------------------------

    @property
    def has_error_code(self) -> bool:
        """
        Return True when an error code exists.
        """

        return self.error_code is not None

    @property
    def has_metadata(self) -> bool:
        """
        Return True when diagnostic metadata exists.
        """

        return bool(self.metadata)

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def to_dict(
        self,
    ) -> dict[str, object]:
        """
        Convert the exception into a dictionary.

        Useful for:
        - Logging
        - Telemetry
        - API responses
        - Debugging
        """

        return {
            "type": self.__class__.__name__,
            "provider": self.provider,
            "message": self.message,
            "error_code": self.error_code,
            "retryable": self.retryable,
            "metadata": self.metadata.copy(),
        }

    # ------------------------------------------------------------------
    # Python Methods
    # ------------------------------------------------------------------

    def __str__(self) -> str:

        return self.message

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"provider={self.provider!r}, "
            f"error_code={self.error_code!r}, "
            f"retryable={self.retryable}, "
            f"message={self.message!r})"
        )

# ----------------------------------------------------------------------
# Registration Exceptions
# ----------------------------------------------------------------------


class ProviderRegistrationError(
    ProviderError,
):
    """
    Raised when a provider cannot be registered.
    """

    def __init__(
        self,
        provider: str,
        message: str = "Provider registration failed.",
        *,
        error_code: str | None = None,
        metadata: dict[str, object] | None = None,
    ) -> None:

        super().__init__(
            message=message,
            provider=provider,
            error_code=error_code,
            retryable=False,
            metadata=metadata,
        )


class ProviderAlreadyRegisteredError(
    ProviderRegistrationError,
):
    """
    Raised when attempting to register a provider
    that already exists.
    """

    def __init__(
        self,
        provider: str,
        *,
        metadata: dict[str, object] | None = None,
    ) -> None:

        super().__init__(
            provider=provider,
            message=(
                f"Provider '{provider}' is already "
                f"registered."
            ),
            error_code="PROVIDER_ALREADY_REGISTERED",
            metadata=metadata,
        )


class ProviderNotFoundError(
    ProviderRegistrationError,
):
    """
    Raised when a requested provider
    cannot be found.
    """

    def __init__(
        self,
        provider: str,
        *,
        metadata: dict[str, object] | None = None,
    ) -> None:

        super().__init__(
            provider=provider,
            message=(
                f"Provider '{provider}' was not found."
            ),
            error_code="PROVIDER_NOT_FOUND",
            metadata=metadata,
        )
# ----------------------------------------------------------------------
# Configuration & Authentication Exceptions
# ----------------------------------------------------------------------


class ProviderConfigurationError(
    ProviderError,
):
    """
    Raised when a provider configuration is invalid.
    """

    def __init__(
        self,
        provider: str,
        message: str = "Invalid provider configuration.",
        *,
        configuration_key: str | None = None,
        error_code: str = "PROVIDER_CONFIGURATION_ERROR",
        metadata: dict[str, object] | None = None,
    ) -> None:

        self.configuration_key = configuration_key

        super().__init__(
            message=message,
            provider=provider,
            error_code=error_code,
            retryable=False,
            metadata=metadata,
        )


class ProviderAuthenticationError(
    ProviderError,
):
    """
    Raised when provider authentication fails.
    """

    def __init__(
        self,
        provider: str,
        message: str = "Provider authentication failed.",
        *,
        api_key_name: str | None = None,
        organization: str | None = None,
        error_code: str = "PROVIDER_AUTHENTICATION_ERROR",
        metadata: dict[str, object] | None = None,
    ) -> None:

        self.api_key_name = api_key_name
        self.organization = organization

        super().__init__(
            message=message,
            provider=provider,
            error_code=error_code,
            retryable=False,
            metadata=metadata,
        )


class ProviderPermissionError(
    ProviderError,
):
    """
    Raised when the authenticated user does not have
    permission to perform the requested operation.
    """

    def __init__(
        self,
        provider: str,
        message: str = "Permission denied.",
        *,
        resource: str | None = None,
        operation: str | None = None,
        error_code: str = "PROVIDER_PERMISSION_ERROR",
        metadata: dict[str, object] | None = None,
    ) -> None:

        self.resource = resource
        self.operation = operation

        super().__init__(
            message=message,
            provider=provider,
            error_code=error_code,
            retryable=False,
            metadata=metadata,
        )
# ----------------------------------------------------------------------
# Connectivity & Availability Exceptions
# ----------------------------------------------------------------------


class ProviderConnectionError(
    ProviderError,
):
    """
    Raised when a connection to the provider
    cannot be established.
    """

    def __init__(
        self,
        provider: str,
        message: str = "Unable to connect to provider.",
        *,
        host: str | None = None,
        port: int | None = None,
        error_code: str = "PROVIDER_CONNECTION_ERROR",
        metadata: dict[str, object] | None = None,
    ) -> None:

        self.host = host
        self.port = port

        super().__init__(
            message=message,
            provider=provider,
            error_code=error_code,
            retryable=True,
            metadata=metadata,
        )


class ProviderTimeoutError(
    ProviderError,
):
    """
    Raised when a provider request exceeds
    the allowed timeout.
    """

    def __init__(
        self,
        provider: str,
        timeout: float = DEFAULT_TIMEOUT,
        *,
        error_code: str = "PROVIDER_TIMEOUT",
        metadata: dict[str, object] | None = None,
    ) -> None:

        self.timeout = timeout

        super().__init__(
            message=(
                f"Provider request timed out after "
                f"{timeout:.2f} seconds."
            ),
            provider=provider,
            error_code=error_code,
            retryable=True,
            metadata=metadata,
        )


class ProviderUnavailableError(
    ProviderError,
):
    """
    Raised when a provider is temporarily
    unavailable.
    """

    def __init__(
        self,
        provider: str,
        message: str = "Provider is unavailable.",
        *,
        retry_after: int = DEFAULT_RETRY_AFTER,
        error_code: str = "PROVIDER_UNAVAILABLE",
        metadata: dict[str, object] | None = None,
    ) -> None:

        self.retry_after = retry_after

        super().__init__(
            message=message,
            provider=provider,
            error_code=error_code,
            retryable=True,
            metadata=metadata,
        )
        
# ----------------------------------------------------------------------
# Rate Limit & Quota Exceptions
# ----------------------------------------------------------------------


class ProviderRateLimitError(
    ProviderError,
):
    """
    Raised when a provider rate limit has been exceeded.
    """

    def __init__(
        self,
        provider: str,
        message: str = "Provider rate limit exceeded.",
        *,
        retry_after: int = DEFAULT_RETRY_AFTER,
        requests_per_minute: int | None = None,
        tokens_per_minute: int | None = None,
        error_code: str = "PROVIDER_RATE_LIMIT",
        metadata: dict[str, object] | None = None,
    ) -> None:

        self.retry_after = retry_after
        self.requests_per_minute = requests_per_minute
        self.tokens_per_minute = tokens_per_minute

        super().__init__(
            message=message,
            provider=provider,
            error_code=error_code,
            retryable=True,
            metadata=metadata,
        )


class ProviderQuotaExceededError(
    ProviderError,
):
    """
    Raised when a provider usage quota has been exceeded.
    """

    def __init__(
        self,
        provider: str,
        message: str = "Provider quota exceeded.",
        *,
        quota: int | float | None = None,
        remaining: int | float | None = None,
        reset_time: str | None = None,
        error_code: str = "PROVIDER_QUOTA_EXCEEDED",
        metadata: dict[str, object] | None = None,
    ) -> None:

        self.quota = quota
        self.remaining = remaining
        self.reset_time = reset_time

        super().__init__(
            message=message,
            provider=provider,
            error_code=error_code,
            retryable=False,
            metadata=metadata,
        )
  # ----------------------------------------------------------------------
# Response & Capability Exceptions
# ----------------------------------------------------------------------


class ProviderResponseError(
    ProviderError,
):
    """
    Raised when a provider returns an invalid or
    unexpected response.
    """

    def __init__(
        self,
        provider: str,
        message: str = "Invalid provider response.",
        *,
        status_code: int | None = None,
        response_id: str | None = None,
        finish_reason: str | None = None,
        error_code: str = "PROVIDER_RESPONSE_ERROR",
        metadata: dict[str, object] | None = None,
    ) -> None:

        self.status_code = status_code
        self.response_id = response_id
        self.finish_reason = finish_reason

        super().__init__(
            message=message,
            provider=provider,
            error_code=error_code,
            retryable=False,
            metadata=metadata,
        )


class ProviderStreamingError(
    ProviderError,
):
    """
    Raised when streaming fails during generation.
    """

    def __init__(
        self,
        provider: str,
        message: str = "Streaming failed.",
        *,
        chunk_index: int | None = None,
        response_id: str | None = None,
        error_code: str = "PROVIDER_STREAMING_ERROR",
        metadata: dict[str, object] | None = None,
    ) -> None:

        self.chunk_index = chunk_index
        self.response_id = response_id

        super().__init__(
            message=message,
            provider=provider,
            error_code=error_code,
            retryable=True,
            metadata=metadata,
        )


class ProviderCapabilityError(
    ProviderError,
):
    """
    Raised when a requested capability is not
    supported by a provider.
    """

    def __init__(
        self,
        provider: str,
        capability: str,
        *,
        error_code: str = "PROVIDER_CAPABILITY_ERROR",
        metadata: dict[str, object] | None = None,
    ) -> None:

        self.capability = capability

        super().__init__(
            message=(
                f"Provider '{provider}' does not support "
                f"'{capability}'."
            ),
            provider=provider,
            error_code=error_code,
            retryable=False,
            metadata=metadata,
        )


class ProviderModelNotFoundError(
    ProviderError,
):
    """
    Raised when a requested model is unavailable.
    """

    def __init__(
        self,
        provider: str,
        model: str,
        *,
        error_code: str = "PROVIDER_MODEL_NOT_FOUND",
        metadata: dict[str, object] | None = None,
    ) -> None:

        self.model = model

        super().__init__(
            message=(
                f"Model '{model}' was not found for "
                f"provider '{provider}'."
            ),
            provider=provider,
            error_code=error_code,
            retryable=False,
            metadata=metadata,
        )
# ----------------------------------------------------------------------
# Exception Helpers
# ----------------------------------------------------------------------


def is_retryable(
    exception: Exception,
) -> bool:
    """
    Return True if an exception can be retried.
    """

    return (
        isinstance(exception, ProviderError)
        and exception.retryable
    )


def get_provider(
    exception: Exception,
) -> str:
    """
    Return the provider associated with an exception.
    """

    if isinstance(exception, ProviderError):
        return exception.provider

    return DEFAULT_PROVIDER


def get_error_code(
    exception: Exception,
) -> str | None:
    """
    Return the provider error code.
    """

    if isinstance(exception, ProviderError):
        return exception.error_code

    return None


def get_metadata(
    exception: Exception,
) -> dict[str, object]:
    """
    Return exception metadata.
    """

    if isinstance(exception, ProviderError):
        return exception.metadata

    return {}


def exception_to_dict(
    exception: Exception,
) -> dict[str, object]:
    """
    Convert any exception into a serializable dictionary.
    """

    if isinstance(exception, ProviderError):
        return exception.to_dict()

    return {
        "type": exception.__class__.__name__,
        "provider": DEFAULT_PROVIDER,
        "message": str(exception),
        "error_code": None,
        "retryable": False,
        "metadata": {},
    }  
# ----------------------------------------------------------------------
# Module Utilities
# ----------------------------------------------------------------------

def __dir__() -> list[str]:
    """
    Return the public symbols exported by this module.
    """

    return sorted(__all__)


def __getattr__(
    name: str,
):
    """
    Prevent access to undefined module attributes.
    """

    raise AttributeError(
        f"module '{__name__}' has no attribute "
        f"'{name}'"
    )    
