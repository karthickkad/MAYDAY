"""
test_exceptions.py

Unit tests for provider exceptions.
"""

from __future__ import annotations

import pytest

from ai.providers.exceptions import (
    DEFAULT_PROVIDER,
    DEFAULT_RETRY_AFTER,
    DEFAULT_TIMEOUT,
    ProviderError,
    ProviderRegistrationError,
    ProviderAlreadyRegisteredError,
    ProviderNotFoundError,
    ProviderConfigurationError,
    ProviderAuthenticationError,
    ProviderPermissionError,
    ProviderConnectionError,
    ProviderTimeoutError,
    ProviderUnavailableError,
    ProviderRateLimitError,
    ProviderQuotaExceededError,
    ProviderResponseError,
    ProviderStreamingError,
    ProviderCapabilityError,
    ProviderModelNotFoundError,
    is_retryable,
    get_provider,
    get_error_code,
    get_metadata,
    exception_to_dict,
)


# ----------------------------------------------------------------------
# Test Fixtures
# ----------------------------------------------------------------------


@pytest.fixture
def provider_name() -> str:
    """
    Sample provider name.
    """

    return "openai"


@pytest.fixture
def sample_metadata() -> dict[str, object]:
    """
    Sample metadata used by multiple tests.
    """

    return {
        "request_id": "req_12345",
        "model": "gpt-5",
    }


@pytest.fixture
def provider_error(
    provider_name: str,
    sample_metadata: dict[str, object],
) -> ProviderError:
    """
    Standard ProviderError instance.
    """

    return ProviderError(
        message="Test provider error.",
        provider=provider_name,
        error_code="TEST_ERROR",
        retryable=True,
        metadata=sample_metadata,
    )

# ----------------------------------------------------------------------
# ProviderError Tests
# ----------------------------------------------------------------------


def test_provider_error_type(
    provider_error,
):
    """
    ProviderError should inherit from Exception.
    """

    assert isinstance(
        provider_error,
        Exception,
    )


def test_provider_error_message(
    provider_error,
):
    """
    Verify stored message.
    """

    assert (
        provider_error.message
        == "Test provider error."
    )


def test_provider_error_provider(
    provider_error,
    provider_name,
):
    """
    Verify provider name.
    """

    assert (
        provider_error.provider
        == provider_name
    )


def test_provider_error_error_code(
    provider_error,
):
    """
    Verify error code.
    """

    assert (
        provider_error.error_code
        == "TEST_ERROR"
    )


def test_provider_error_retryable(
    provider_error,
):
    """
    Verify retryable flag.
    """

    assert provider_error.retryable is True


def test_provider_error_metadata(
    provider_error,
    sample_metadata,
):
    """
    Verify metadata.
    """

    assert (
        provider_error.metadata
        == sample_metadata
    )


def test_provider_error_has_error_code(
    provider_error,
):
    """
    Verify has_error_code property.
    """

    assert (
        provider_error.has_error_code
        is True
    )


def test_provider_error_has_metadata(
    provider_error,
):
    """
    Verify has_metadata property.
    """

    assert (
        provider_error.has_metadata
        is True
    )


def test_provider_error_to_dict(
    provider_error,
):
    """
    Verify dictionary conversion.
    """

    data = provider_error.to_dict()

    assert (
        data["type"]
        == "ProviderError"
    )

    assert (
        data["provider"]
        == "openai"
    )

    assert (
        data["message"]
        == "Test provider error."
    )

    assert (
        data["error_code"]
        == "TEST_ERROR"
    )

    assert (
        data["retryable"]
        is True
    )


def test_provider_error_str(
    provider_error,
):
    """
    Verify __str__.
    """

    assert (
        str(provider_error)
        == "Test provider error."
    )


def test_provider_error_repr(
    provider_error,
):
    """
    Verify __repr__.
    """

    text = repr(
        provider_error,
    )

    assert (
        "ProviderError"
        in text
    )

    assert (
        "openai"
        in text
    )

    assert (
        "TEST_ERROR"
        in text
    )


def test_provider_error_defaults():
    """
    Verify default constructor values.
    """

    exc = ProviderError(
        message="Default",
    )

    assert (
        exc.provider
        == DEFAULT_PROVIDER
    )

    assert (
        exc.error_code
        is None
    )

    assert (
        exc.retryable
        is False
    )

    assert (
        exc.metadata
        == {}
    )


def test_provider_error_without_metadata():
    """
    Metadata should default to an empty dict.
    """

    exc = ProviderError(
        message="Error",
    )

    assert (
        exc.has_metadata
        is False
    )


def test_provider_error_without_error_code():
    """
    Error code should default to None.
    """

    exc = ProviderError(
        message="Error",
    )

    assert (
        exc.has_error_code
        is False
    )

# ----------------------------------------------------------------------
# Registration Exception Tests
# ----------------------------------------------------------------------


def test_provider_registration_error_type(
    provider_name,
):
    """
    ProviderRegistrationError should inherit from
    ProviderError.
    """

    exc = ProviderRegistrationError(
        provider=provider_name,
    )

    assert isinstance(
        exc,
        ProviderError,
    )


def test_provider_registration_error_provider(
    provider_name,
):
    """
    Verify provider name.
    """

    exc = ProviderRegistrationError(
        provider=provider_name,
    )

    assert (
        exc.provider
        == provider_name
    )


def test_provider_registration_error_retryable(
    provider_name,
):
    """
    Registration errors should not be retryable.
    """

    exc = ProviderRegistrationError(
        provider=provider_name,
    )

    assert (
        exc.retryable
        is False
    )


def test_provider_registration_error_error_code(
    provider_name,
):
    """
    Verify custom error code.
    """

    exc = ProviderRegistrationError(
        provider=provider_name,
        error_code="REGISTRATION_FAILED",
    )

    assert (
        exc.error_code
        == "REGISTRATION_FAILED"
    )


def test_provider_registration_error_metadata(
    provider_name,
):
    """
    Verify metadata.
    """

    metadata = {
        "registry": "default",
    }

    exc = ProviderRegistrationError(
        provider=provider_name,
        metadata=metadata,
    )

    assert (
        exc.metadata
        == metadata
    )


def test_provider_already_registered_type(
    provider_name,
):
    """
    Verify inheritance.
    """

    exc = ProviderAlreadyRegisteredError(
        provider_name,
    )

    assert isinstance(
        exc,
        ProviderRegistrationError,
    )


def test_provider_already_registered_message(
    provider_name,
):
    """
    Verify message.
    """

    exc = ProviderAlreadyRegisteredError(
        provider_name,
    )

    assert (
        str(exc)
        == f"Provider '{provider_name}' is already registered."
    )


def test_provider_already_registered_provider(
    provider_name,
):
    """
    Verify provider.
    """

    exc = ProviderAlreadyRegisteredError(
        provider_name,
    )

    assert (
        exc.provider
        == provider_name
    )


def test_provider_already_registered_error_code(
    provider_name,
):
    """
    Verify error code.
    """

    exc = ProviderAlreadyRegisteredError(
        provider_name,
    )

    assert (
        exc.error_code
        == "PROVIDER_ALREADY_REGISTERED"
    )


def test_provider_not_found_type(
    provider_name,
):
    """
    Verify inheritance.
    """

    exc = ProviderNotFoundError(
        provider_name,
    )

    assert isinstance(
        exc,
        ProviderRegistrationError,
    )


def test_provider_not_found_message(
    provider_name,
):
    """
    Verify message.
    """

    exc = ProviderNotFoundError(
        provider_name,
    )

    assert (
        str(exc)
        == f"Provider '{provider_name}' was not found."
    )


def test_provider_not_found_provider(
    provider_name,
):
    """
    Verify provider.
    """

    exc = ProviderNotFoundError(
        provider_name,
    )

    assert (
        exc.provider
        == provider_name
    )


def test_provider_not_found_error_code(
    provider_name,
):
    """
    Verify error code.
    """

    exc = ProviderNotFoundError(
        provider_name,
    )

    assert (
        exc.error_code
        == "PROVIDER_NOT_FOUND"
    )


def test_provider_not_found_metadata(
    provider_name,
):
    """
    Verify metadata.
    """

    metadata = {
        "requested": provider_name,
    }

    exc = ProviderNotFoundError(
        provider_name,
        metadata=metadata,
    )

    assert (
        exc.metadata
        == metadata
    )
    
# ----------------------------------------------------------------------
# Configuration & Authentication Exception Tests
# ----------------------------------------------------------------------


def test_provider_configuration_error_type(
    provider_name,
):
    """
    ProviderConfigurationError should inherit from
    ProviderError.
    """

    exc = ProviderConfigurationError(
        provider=provider_name,
    )

    assert isinstance(
        exc,
        ProviderError,
    )


def test_provider_configuration_error_provider(
    provider_name,
):
    """
    Verify provider.
    """

    exc = ProviderConfigurationError(
        provider=provider_name,
    )

    assert (
        exc.provider
        == provider_name
    )


def test_provider_configuration_error_configuration_key(
    provider_name,
):
    """
    Verify configuration key.
    """

    exc = ProviderConfigurationError(
        provider=provider_name,
        configuration_key="api_key",
    )

    assert (
        exc.configuration_key
        == "api_key"
    )


def test_provider_configuration_error_error_code(
    provider_name,
):
    """
    Verify error code.
    """

    exc = ProviderConfigurationError(
        provider=provider_name,
    )

    assert (
        exc.error_code
        == "PROVIDER_CONFIGURATION_ERROR"
    )


def test_provider_configuration_error_retryable(
    provider_name,
):
    """
    Configuration errors should not be retryable.
    """

    exc = ProviderConfigurationError(
        provider=provider_name,
    )

    assert (
        exc.retryable
        is False
    )


def test_provider_configuration_error_metadata(
    provider_name,
):
    """
    Verify metadata.
    """

    metadata = {
        "field": "api_key",
    }

    exc = ProviderConfigurationError(
        provider=provider_name,
        metadata=metadata,
    )

    assert (
        exc.metadata
        == metadata
    )


def test_provider_authentication_error_type(
    provider_name,
):
    """
    ProviderAuthenticationError should inherit from
    ProviderError.
    """

    exc = ProviderAuthenticationError(
        provider=provider_name,
    )

    assert isinstance(
        exc,
        ProviderError,
    )


def test_provider_authentication_error_provider(
    provider_name,
):
    """
    Verify provider.
    """

    exc = ProviderAuthenticationError(
        provider=provider_name,
    )

    assert (
        exc.provider
        == provider_name
    )


def test_provider_authentication_error_api_key(
    provider_name,
):
    """
    Verify API key name.
    """

    exc = ProviderAuthenticationError(
        provider=provider_name,
        api_key_name="OPENAI_API_KEY",
    )

    assert (
        exc.api_key_name
        == "OPENAI_API_KEY"
    )


def test_provider_authentication_error_organization(
    provider_name,
):
    """
    Verify organization.
    """

    exc = ProviderAuthenticationError(
        provider=provider_name,
        organization="OpenAI",
    )

    assert (
        exc.organization
        == "OpenAI"
    )


def test_provider_authentication_error_error_code(
    provider_name,
):
    """
    Verify error code.
    """

    exc = ProviderAuthenticationError(
        provider=provider_name,
    )

    assert (
        exc.error_code
        == "PROVIDER_AUTHENTICATION_ERROR"
    )


def test_provider_authentication_error_retryable(
    provider_name,
):
    """
    Authentication failures should not be retryable.
    """

    exc = ProviderAuthenticationError(
        provider=provider_name,
    )

    assert (
        exc.retryable
        is False
    )


def test_provider_permission_error_type(
    provider_name,
):
    """
    ProviderPermissionError should inherit from
    ProviderError.
    """

    exc = ProviderPermissionError(
        provider=provider_name,
    )

    assert isinstance(
        exc,
        ProviderError,
    )


def test_provider_permission_error_provider(
    provider_name,
):
    """
    Verify provider.
    """

    exc = ProviderPermissionError(
        provider=provider_name,
    )

    assert (
        exc.provider
        == provider_name
    )


def test_provider_permission_error_resource(
    provider_name,
):
    """
    Verify protected resource.
    """

    exc = ProviderPermissionError(
        provider=provider_name,
        resource="gpt-5",
    )

    assert (
        exc.resource
        == "gpt-5"
    )


def test_provider_permission_error_operation(
    provider_name,
):
    """
    Verify operation.
    """

    exc = ProviderPermissionError(
        provider=provider_name,
        operation="generate",
    )

    assert (
        exc.operation
        == "generate"
    )


def test_provider_permission_error_error_code(
    provider_name,
):
    """
    Verify error code.
    """

    exc = ProviderPermissionError(
        provider=provider_name,
    )

    assert (
        exc.error_code
        == "PROVIDER_PERMISSION_ERROR"
    )


def test_provider_permission_error_retryable(
    provider_name,
):
    """
    Permission errors should not be retryable.
    """

    exc = ProviderPermissionError(
        provider=provider_name,
    )

    assert (
        exc.retryable
        is False
    )


def test_provider_permission_error_metadata(
    provider_name,
):
    """
    Verify metadata.
    """

    metadata = {
        "scope": "chat.completions",
    }

    exc = ProviderPermissionError(
        provider=provider_name,
        metadata=metadata,
    )

    assert (
        exc.metadata
        == metadata
    )
# ----------------------------------------------------------------------
# Connectivity & Availability Exception Tests
# ----------------------------------------------------------------------


def test_provider_connection_error_type(
    provider_name,
):
    """
    ProviderConnectionError should inherit from
    ProviderError.
    """

    exc = ProviderConnectionError(
        provider=provider_name,
    )

    assert isinstance(
        exc,
        ProviderError,
    )


def test_provider_connection_error_provider(
    provider_name,
):
    """
    Verify provider.
    """

    exc = ProviderConnectionError(
        provider=provider_name,
    )

    assert (
        exc.provider
        == provider_name
    )


def test_provider_connection_error_host(
    provider_name,
):
    """
    Verify host.
    """

    exc = ProviderConnectionError(
        provider=provider_name,
        host="api.openai.com",
    )

    assert (
        exc.host
        == "api.openai.com"
    )


def test_provider_connection_error_port(
    provider_name,
):
    """
    Verify port.
    """

    exc = ProviderConnectionError(
        provider=provider_name,
        port=443,
    )

    assert (
        exc.port
        == 443
    )


def test_provider_connection_error_error_code(
    provider_name,
):
    """
    Verify error code.
    """

    exc = ProviderConnectionError(
        provider=provider_name,
    )

    assert (
        exc.error_code
        == "PROVIDER_CONNECTION_ERROR"
    )


def test_provider_connection_error_retryable(
    provider_name,
):
    """
    Connection errors should be retryable.
    """

    exc = ProviderConnectionError(
        provider=provider_name,
    )

    assert (
        exc.retryable
        is True
    )


def test_provider_timeout_error_type(
    provider_name,
):
    """
    ProviderTimeoutError should inherit from
    ProviderError.
    """

    exc = ProviderTimeoutError(
        provider=provider_name,
    )

    assert isinstance(
        exc,
        ProviderError,
    )


def test_provider_timeout_error_timeout(
    provider_name,
):
    """
    Verify timeout value.
    """

    exc = ProviderTimeoutError(
        provider=provider_name,
        timeout=60.0,
    )

    assert (
        exc.timeout
        == 60.0
    )


def test_provider_timeout_error_default_timeout(
    provider_name,
):
    """
    Verify default timeout.
    """

    exc = ProviderTimeoutError(
        provider=provider_name,
    )

    assert (
        exc.timeout
        == DEFAULT_TIMEOUT
    )


def test_provider_timeout_error_error_code(
    provider_name,
):
    """
    Verify error code.
    """

    exc = ProviderTimeoutError(
        provider=provider_name,
    )

    assert (
        exc.error_code
        == "PROVIDER_TIMEOUT"
    )


def test_provider_timeout_error_retryable(
    provider_name,
):
    """
    Timeout errors should be retryable.
    """

    exc = ProviderTimeoutError(
        provider=provider_name,
    )

    assert (
        exc.retryable
        is True
    )


def test_provider_unavailable_error_type(
    provider_name,
):
    """
    ProviderUnavailableError should inherit from
    ProviderError.
    """

    exc = ProviderUnavailableError(
        provider=provider_name,
    )

    assert isinstance(
        exc,
        ProviderError,
    )


def test_provider_unavailable_error_provider(
    provider_name,
):
    """
    Verify provider.
    """

    exc = ProviderUnavailableError(
        provider=provider_name,
    )

    assert (
        exc.provider
        == provider_name
    )


def test_provider_unavailable_error_retry_after(
    provider_name,
):
    """
    Verify retry_after.
    """

    exc = ProviderUnavailableError(
        provider=provider_name,
        retry_after=30,
    )

    assert (
        exc.retry_after
        == 30
    )


def test_provider_unavailable_error_default_retry_after(
    provider_name,
):
    """
    Verify default retry_after.
    """

    exc = ProviderUnavailableError(
        provider=provider_name,
    )

    assert (
        exc.retry_after
        == DEFAULT_RETRY_AFTER
    )


def test_provider_unavailable_error_error_code(
    provider_name,
):
    """
    Verify error code.
    """

    exc = ProviderUnavailableError(
        provider=provider_name,
    )

    assert (
        exc.error_code
        == "PROVIDER_UNAVAILABLE"
    )


def test_provider_unavailable_error_retryable(
    provider_name,
):
    """
    ProviderUnavailableError should be retryable.
    """

    exc = ProviderUnavailableError(
        provider=provider_name,
    )

    assert (
        exc.retryable
        is True
    )


def test_provider_unavailable_error_metadata(
    provider_name,
):
    """
    Verify metadata.
    """

    metadata = {
        "server": "primary",
    }

    exc = ProviderUnavailableError(
        provider=provider_name,
        metadata=metadata,
    )

    assert (
        exc.metadata
        == metadata
    )
# ----------------------------------------------------------------------
# Rate Limit & Quota Exception Tests
# ----------------------------------------------------------------------


def test_provider_rate_limit_error_type(
    provider_name,
):
    """
    ProviderRateLimitError should inherit from
    ProviderError.
    """

    exc = ProviderRateLimitError(
        provider=provider_name,
    )

    assert isinstance(
        exc,
        ProviderError,
    )


def test_provider_rate_limit_error_provider(
    provider_name,
):
    """
    Verify provider.
    """

    exc = ProviderRateLimitError(
        provider=provider_name,
    )

    assert (
        exc.provider
        == provider_name
    )


def test_provider_rate_limit_error_retry_after(
    provider_name,
):
    """
    Verify retry_after.
    """

    exc = ProviderRateLimitError(
        provider=provider_name,
        retry_after=60,
    )

    assert (
        exc.retry_after
        == 60
    )


def test_provider_rate_limit_error_default_retry_after(
    provider_name,
):
    """
    Verify default retry_after.
    """

    exc = ProviderRateLimitError(
        provider=provider_name,
    )

    assert (
        exc.retry_after
        == DEFAULT_RETRY_AFTER
    )


def test_provider_rate_limit_error_requests_per_minute(
    provider_name,
):
    """
    Verify requests per minute.
    """

    exc = ProviderRateLimitError(
        provider=provider_name,
        requests_per_minute=500,
    )

    assert (
        exc.requests_per_minute
        == 500
    )


def test_provider_rate_limit_error_tokens_per_minute(
    provider_name,
):
    """
    Verify tokens per minute.
    """

    exc = ProviderRateLimitError(
        provider=provider_name,
        tokens_per_minute=90000,
    )

    assert (
        exc.tokens_per_minute
        == 90000
    )


def test_provider_rate_limit_error_error_code(
    provider_name,
):
    """
    Verify error code.
    """

    exc = ProviderRateLimitError(
        provider=provider_name,
    )

    assert (
        exc.error_code
        == "PROVIDER_RATE_LIMIT"
    )


def test_provider_rate_limit_error_retryable(
    provider_name,
):
    """
    Rate limit errors should be retryable.
    """

    exc = ProviderRateLimitError(
        provider=provider_name,
    )

    assert (
        exc.retryable
        is True
    )


def test_provider_rate_limit_error_metadata(
    provider_name,
):
    """
    Verify metadata.
    """

    metadata = {
        "tier": "premium",
    }

    exc = ProviderRateLimitError(
        provider=provider_name,
        metadata=metadata,
    )

    assert (
        exc.metadata
        == metadata
    )


def test_provider_quota_exceeded_error_type(
    provider_name,
):
    """
    ProviderQuotaExceededError should inherit from
    ProviderError.
    """

    exc = ProviderQuotaExceededError(
        provider=provider_name,
    )

    assert isinstance(
        exc,
        ProviderError,
    )


def test_provider_quota_exceeded_error_provider(
    provider_name,
):
    """
    Verify provider.
    """

    exc = ProviderQuotaExceededError(
        provider=provider_name,
    )

    assert (
        exc.provider
        == provider_name
    )


def test_provider_quota_exceeded_error_quota(
    provider_name,
):
    """
    Verify quota.
    """

    exc = ProviderQuotaExceededError(
        provider=provider_name,
        quota=1_000_000,
    )

    assert (
        exc.quota
        == 1_000_000
    )


def test_provider_quota_exceeded_error_remaining(
    provider_name,
):
    """
    Verify remaining quota.
    """

    exc = ProviderQuotaExceededError(
        provider=provider_name,
        remaining=0,
    )

    assert (
        exc.remaining
        == 0
    )


def test_provider_quota_exceeded_error_reset_time(
    provider_name,
):
    """
    Verify reset time.
    """

    exc = ProviderQuotaExceededError(
        provider=provider_name,
        reset_time="2026-08-03T12:00:00Z",
    )

    assert (
        exc.reset_time
        == "2026-08-03T12:00:00Z"
    )


def test_provider_quota_exceeded_error_error_code(
    provider_name,
):
    """
    Verify error code.
    """

    exc = ProviderQuotaExceededError(
        provider=provider_name,
    )

    assert (
        exc.error_code
        == "PROVIDER_QUOTA_EXCEEDED"
    )


def test_provider_quota_exceeded_error_retryable(
    provider_name,
):
    """
    Quota exceeded errors should not be retryable.
    """

    exc = ProviderQuotaExceededError(
        provider=provider_name,
    )

    assert (
        exc.retryable
        is False
    )


def test_provider_quota_exceeded_error_metadata(
    provider_name,
):
    """
    Verify metadata.
    """

    metadata = {
        "plan": "free",
    }

    exc = ProviderQuotaExceededError(
        provider=provider_name,
        metadata=metadata,
    )

    assert (
        exc.metadata
        == metadata
    )
    
# ----------------------------------------------------------------------
# Response & Capability Exception Tests
# ----------------------------------------------------------------------


def test_provider_response_error_type(
    provider_name,
):
    """
    ProviderResponseError should inherit from
    ProviderError.
    """

    exc = ProviderResponseError(
        provider=provider_name,
    )

    assert isinstance(
        exc,
        ProviderError,
    )


def test_provider_response_error_provider(
    provider_name,
):
    """
    Verify provider.
    """

    exc = ProviderResponseError(
        provider=provider_name,
    )

    assert (
        exc.provider
        == provider_name
    )


def test_provider_response_error_status_code(
    provider_name,
):
    """
    Verify status code.
    """

    exc = ProviderResponseError(
        provider=provider_name,
        status_code=500,
    )

    assert (
        exc.status_code
        == 500
    )


def test_provider_response_error_response_id(
    provider_name,
):
    """
    Verify response ID.
    """

    exc = ProviderResponseError(
        provider=provider_name,
        response_id="resp_12345",
    )

    assert (
        exc.response_id
        == "resp_12345"
    )


def test_provider_response_error_finish_reason(
    provider_name,
):
    """
    Verify finish reason.
    """

    exc = ProviderResponseError(
        provider=provider_name,
        finish_reason="stop",
    )

    assert (
        exc.finish_reason
        == "stop"
    )


def test_provider_response_error_error_code(
    provider_name,
):
    """
    Verify error code.
    """

    exc = ProviderResponseError(
        provider=provider_name,
    )

    assert (
        exc.error_code
        == "PROVIDER_RESPONSE_ERROR"
    )


def test_provider_response_error_retryable(
    provider_name,
):
    """
    Response errors should not be retryable.
    """

    exc = ProviderResponseError(
        provider=provider_name,
    )

    assert (
        exc.retryable
        is False
    )


def test_provider_streaming_error_type(
    provider_name,
):
    """
    ProviderStreamingError should inherit from
    ProviderError.
    """

    exc = ProviderStreamingError(
        provider=provider_name,
    )

    assert isinstance(
        exc,
        ProviderError,
    )


def test_provider_streaming_error_chunk_index(
    provider_name,
):
    """
    Verify chunk index.
    """

    exc = ProviderStreamingError(
        provider=provider_name,
        chunk_index=10,
    )

    assert (
        exc.chunk_index
        == 10
    )


def test_provider_streaming_error_response_id(
    provider_name,
):
    """
    Verify response ID.
    """

    exc = ProviderStreamingError(
        provider=provider_name,
        response_id="stream_001",
    )

    assert (
        exc.response_id
        == "stream_001"
    )


def test_provider_streaming_error_error_code(
    provider_name,
):
    """
    Verify error code.
    """

    exc = ProviderStreamingError(
        provider=provider_name,
    )

    assert (
        exc.error_code
        == "PROVIDER_STREAMING_ERROR"
    )


def test_provider_streaming_error_retryable(
    provider_name,
):
    """
    Streaming errors should be retryable.
    """

    exc = ProviderStreamingError(
        provider=provider_name,
    )

    assert (
        exc.retryable
        is True
    )


def test_provider_capability_error_type(
    provider_name,
):
    """
    ProviderCapabilityError should inherit from
    ProviderError.
    """

    exc = ProviderCapabilityError(
        provider=provider_name,
        capability="vision",
    )

    assert isinstance(
        exc,
        ProviderError,
    )


def test_provider_capability_error_capability(
    provider_name,
):
    """
    Verify capability.
    """

    exc = ProviderCapabilityError(
        provider=provider_name,
        capability="vision",
    )

    assert (
        exc.capability
        == "vision"
    )


def test_provider_capability_error_error_code(
    provider_name,
):
    """
    Verify error code.
    """

    exc = ProviderCapabilityError(
        provider=provider_name,
        capability="vision",
    )

    assert (
        exc.error_code
        == "PROVIDER_CAPABILITY_ERROR"
    )


def test_provider_capability_error_retryable(
    provider_name,
):
    """
    Capability errors should not be retryable.
    """

    exc = ProviderCapabilityError(
        provider=provider_name,
        capability="vision",
    )

    assert (
        exc.retryable
        is False
    )


def test_provider_model_not_found_error_type(
    provider_name,
):
    """
    ProviderModelNotFoundError should inherit from
    ProviderError.
    """

    exc = ProviderModelNotFoundError(
        provider=provider_name,
        model="gpt-5",
    )

    assert isinstance(
        exc,
        ProviderError,
    )


def test_provider_model_not_found_error_model(
    provider_name,
):
    """
    Verify model.
    """

    exc = ProviderModelNotFoundError(
        provider=provider_name,
        model="gpt-5",
    )

    assert (
        exc.model
        == "gpt-5"
    )


def test_provider_model_not_found_error_provider(
    provider_name,
):
    """
    Verify provider.
    """

    exc = ProviderModelNotFoundError(
        provider=provider_name,
        model="gpt-5",
    )

    assert (
        exc.provider
        == provider_name
    )


def test_provider_model_not_found_error_error_code(
    provider_name,
):
    """
    Verify error code.
    """

    exc = ProviderModelNotFoundError(
        provider=provider_name,
        model="gpt-5",
    )

    assert (
        exc.error_code
        == "PROVIDER_MODEL_NOT_FOUND"
    )


def test_provider_model_not_found_error_retryable(
    provider_name,
):
    """
    Model not found errors should not be retryable.
    """

    exc = ProviderModelNotFoundError(
        provider=provider_name,
        model="gpt-5",
    )

    assert (
        exc.retryable
        is False
    )


def test_provider_response_error_metadata(
    provider_name,
):
    """
    Verify metadata.
    """

    metadata = {
        "request_id": "req_001",
    }

    exc = ProviderResponseError(
        provider=provider_name,
        metadata=metadata,
    )

    assert (
        exc.metadata
        == metadata
    )


def test_provider_streaming_error_metadata(
    provider_name,
):
    """
    Verify metadata.
    """

    metadata = {
        "stream": True,
    }

    exc = ProviderStreamingError(
        provider=provider_name,
        metadata=metadata,
    )

    assert (
        exc.metadata
        == metadata
    )
# ----------------------------------------------------------------------
# Exception Helper Function Tests
# ----------------------------------------------------------------------


def test_is_retryable_true(
    provider_name,
):
    """
    Verify retryable exception.
    """

    exc = ProviderConnectionError(
        provider=provider_name,
    )

    assert is_retryable(
        exc,
    ) is True


def test_is_retryable_false(
    provider_name,
):
    """
    Verify non-retryable exception.
    """

    exc = ProviderConfigurationError(
        provider=provider_name,
    )

    assert is_retryable(
        exc,
    ) is False


def test_is_retryable_standard_exception():
    """
    Verify normal exceptions are not retryable.
    """

    exc = ValueError(
        "Invalid value.",
    )

    assert is_retryable(
        exc,
    ) is False


def test_get_provider(
    provider_name,
):
    """
    Verify provider extraction.
    """

    exc = ProviderTimeoutError(
        provider=provider_name,
    )

    assert (
        get_provider(
            exc,
        )
        == provider_name
    )


def test_get_provider_default():
    """
    Verify default provider for
    standard exceptions.
    """

    exc = RuntimeError(
        "Runtime error.",
    )

    assert (
        get_provider(
            exc,
        )
        == DEFAULT_PROVIDER
    )


def test_get_error_code(
    provider_name,
):
    """
    Verify error code extraction.
    """

    exc = ProviderConnectionError(
        provider=provider_name,
    )

    assert (
        get_error_code(
            exc,
        )
        == "PROVIDER_CONNECTION_ERROR"
    )


def test_get_error_code_none():
    """
    Verify standard exceptions
    return None.
    """

    exc = RuntimeError(
        "Runtime error.",
    )

    assert (
        get_error_code(
            exc,
        )
        is None
    )


def test_get_metadata(
    provider_name,
):
    """
    Verify metadata extraction.
    """

    metadata = {
        "request_id": "12345",
    }

    exc = ProviderResponseError(
        provider=provider_name,
        metadata=metadata,
    )

    assert (
        get_metadata(
            exc,
        )
        == metadata
    )


def test_get_metadata_empty():
    """
    Verify empty metadata for
    standard exceptions.
    """

    exc = RuntimeError(
        "Runtime error.",
    )

    assert (
        get_metadata(
            exc,
        )
        == {}
    )


def test_exception_to_dict_provider_error(
    provider_name,
):
    """
    Verify ProviderError conversion.
    """

    metadata = {
        "model": "gpt-5",
    }

    exc = ProviderTimeoutError(
        provider=provider_name,
        metadata=metadata,
    )

    data = exception_to_dict(
        exc,
    )

    assert (
        data["type"]
        == "ProviderTimeoutError"
    )

    assert (
        data["provider"]
        == provider_name
    )

    assert (
        data["error_code"]
        == "PROVIDER_TIMEOUT"
    )

    assert (
        data["retryable"]
        is True
    )

    assert (
        data["metadata"]
        == metadata
    )


def test_exception_to_dict_standard_exception():
    """
    Verify standard exception conversion.
    """

    exc = RuntimeError(
        "Runtime error.",
    )

    data = exception_to_dict(
        exc,
    )

    assert (
        data["type"]
        == "RuntimeError"
    )

    assert (
        data["provider"]
        == DEFAULT_PROVIDER
    )

    assert (
        data["message"]
        == "Runtime error."
    )

    assert (
        data["retryable"]
        is False
    )

    assert (
        data["error_code"]
        is None
    )


def test_exception_to_dict_metadata_empty():
    """
    Verify metadata defaults to
    an empty dictionary.
    """

    exc = ValueError(
        "Value error.",
    )

    data = exception_to_dict(
        exc,
    )

    assert (
        data["metadata"]
        == {}
    )


def test_helper_functions_consistency(
    provider_name,
):
    """
    Verify all helper functions
    return consistent values.
    """

    metadata = {
        "endpoint": "/chat",
    }

    exc = ProviderConnectionError(
        provider=provider_name,
        metadata=metadata,
    )

    assert (
        get_provider(exc)
        == provider_name
    )

    assert (
        get_error_code(exc)
        == "PROVIDER_CONNECTION_ERROR"
    )

    assert (
        get_metadata(exc)
        == metadata
    )

    assert (
        is_retryable(exc)
        is True
    )
# ----------------------------------------------------------------------
# Edge Cases & Robustness Tests
# ----------------------------------------------------------------------


def test_provider_error_empty_message():
    """
    ProviderError should allow an empty message.
    """

    exc = ProviderError(
        message="",
    )

    assert exc.message == ""
    assert str(exc) == ""


def test_provider_error_empty_provider():
    """
    Verify empty provider name.
    """

    exc = ProviderError(
        message="Error",
        provider="",
    )

    assert exc.provider == ""


def test_provider_error_none_metadata():
    """
    Metadata should default to an empty dictionary.
    """

    exc = ProviderError(
        message="Error",
        metadata=None,
    )

    assert exc.metadata == {}
    assert exc.has_metadata is False


def test_provider_error_empty_metadata():
    """
    Empty metadata should be supported.
    """

    exc = ProviderError(
        message="Error",
        metadata={},
    )

    assert exc.metadata == {}
    assert exc.has_metadata is False


def test_provider_error_large_metadata():
    """
    Verify large metadata dictionaries.
    """

    metadata = {
        f"key_{i}": i
        for i in range(100)
    }

    exc = ProviderError(
        message="Large metadata",
        metadata=metadata,
    )

    assert exc.metadata == metadata
    assert exc.has_metadata is True


def test_to_dict_returns_new_dictionary(
    provider_error,
):
    """
    to_dict() should return a new dictionary.
    """

    data1 = provider_error.to_dict()
    data2 = provider_error.to_dict()

    assert data1 == data2
    assert data1 is not data2


def test_metadata_isolation(
    provider_error,
):
    """
    Returned metadata should not affect
    the original exception.
    """

    data = provider_error.to_dict()

    data["metadata"]["new"] = "value"

    assert (
        "new"
        not in provider_error.metadata
    )


def test_multiple_provider_errors_are_unique():
    """
    Each exception should be a unique object.
    """

    exc1 = ProviderError(
        message="Error",
    )

    exc2 = ProviderError(
        message="Error",
    )

    assert exc1 is not exc2


def test_repr_returns_string(
    provider_error,
):
    """
    __repr__ should always return a string.
    """

    assert isinstance(
        repr(provider_error),
        str,
    )


def test_str_returns_string(
    provider_error,
):
    """
    __str__ should always return a string.
    """

    assert isinstance(
        str(provider_error),
        str,
    )


def test_exception_to_dict_contains_expected_keys(
    provider_error,
):
    """
    Verify serialized dictionary keys.
    """

    data = provider_error.to_dict()

    expected = {
        "type",
        "provider",
        "message",
        "error_code",
        "retryable",
        "metadata",
    }

    assert set(data.keys()) == expected


def test_exception_to_dict_serializable(
    provider_error,
):
    """
    Verify dictionary values are serializable.
    """

    import json

    json.dumps(
        provider_error.to_dict(),
    )


def test_error_code_optional():
    """
    Error code may be omitted.
    """

    exc = ProviderError(
        message="Error",
    )

    assert exc.error_code is None


def test_retryable_default():
    """
    Retryable defaults to False.
    """

    exc = ProviderError(
        message="Error",
    )

    assert exc.retryable is False


def test_provider_default():
    """
    Provider defaults correctly.
    """

    exc = ProviderError(
        message="Error",
    )

    assert exc.provider == DEFAULT_PROVIDER


def test_has_metadata_false():
    """
    Empty metadata should report False.
    """

    exc = ProviderError(
        message="Error",
    )

    assert exc.has_metadata is False


def test_has_error_code_false():
    """
    Missing error code should report False.
    """

    exc = ProviderError(
        message="Error",
    )

    assert exc.has_error_code is False

# ----------------------------------------------------------------------
# Integration & Consistency Tests
# ----------------------------------------------------------------------


def test_exception_inheritance_chain():
    """
    Verify every exception inherits from ProviderError.
    """

    exceptions = [
        ProviderRegistrationError("openai"),
        ProviderAlreadyRegisteredError("openai"),
        ProviderNotFoundError("openai"),
        ProviderConfigurationError("openai"),
        ProviderAuthenticationError("openai"),
        ProviderPermissionError("openai"),
        ProviderConnectionError("openai"),
        ProviderTimeoutError("openai"),
        ProviderUnavailableError("openai"),
        ProviderRateLimitError("openai"),
        ProviderQuotaExceededError("openai"),
        ProviderResponseError("openai"),
        ProviderStreamingError("openai"),
        ProviderCapabilityError(
            "openai",
            capability="vision",
        ),
        ProviderModelNotFoundError(
            "openai",
            model="gpt-5",
        ),
    ]

    for exc in exceptions:

        assert isinstance(
            exc,
            ProviderError,
        )


def test_to_dict_consistency():
    """
    Every ProviderError should return
    the same dictionary structure.
    """

    exc = ProviderConnectionError(
        provider="openai",
    )

    expected = {
        "type",
        "provider",
        "message",
        "error_code",
        "retryable",
        "metadata",
    }

    assert (
        set(exc.to_dict().keys())
        == expected
    )


def test_exception_to_dict_matches_to_dict():
    """
    exception_to_dict() should delegate
    to ProviderError.to_dict().
    """

    exc = ProviderTimeoutError(
        provider="openai",
    )

    assert (
        exception_to_dict(exc)
        == exc.to_dict()
    )


def test_multiple_exception_objects_are_unique():
    """
    Exception objects should never
    share identity.
    """

    exceptions = [

        ProviderError(
            message=f"Error {i}",
        )

        for i in range(100)

    ]

    assert (

        len(
            {
                id(exc)
                for exc in exceptions
            }
        )

        == 100

    )


def test_multiple_metadata_objects_are_unique():
    """
    Metadata dictionaries should not
    be shared between exceptions.
    """

    exc1 = ProviderError(
        message="A",
    )

    exc2 = ProviderError(
        message="B",
    )

    exc1.metadata["id"] = 1

    assert (
        "id"
        not in exc2.metadata
    )


def test_repr_contains_class_name():
    """
    __repr__ should include the
    exception class name.
    """

    exc = ProviderConnectionError(
        provider="openai",
    )

    assert (
        exc.__class__.__name__
        in repr(exc)
    )


def test_str_matches_message():
    """
    __str__ should return the
    stored message.
    """

    exc = ProviderConnectionError(
        provider="openai",
        message="Connection failed.",
    )

    assert (
        str(exc)
        == exc.message
    )


def test_retryable_consistency():
    """
    Retryable exceptions should
    always report True.
    """

    retryable = [

        ProviderConnectionError("openai"),

        ProviderTimeoutError("openai"),

        ProviderUnavailableError("openai"),

        ProviderRateLimitError("openai"),

        ProviderStreamingError("openai"),

    ]

    for exc in retryable:

        assert exc.retryable is True


def test_non_retryable_consistency():
    """
    Non-retryable exceptions should
    always report False.
    """

    non_retryable = [

        ProviderConfigurationError("openai"),

        ProviderAuthenticationError("openai"),

        ProviderPermissionError("openai"),

        ProviderQuotaExceededError("openai"),

        ProviderCapabilityError(
            "openai",
            capability="vision",
        ),

        ProviderModelNotFoundError(
            "openai",
            model="gpt-5",
        ),

    ]

    for exc in non_retryable:

        assert exc.retryable is False
        
# ----------------------------------------------------------------------
# Stress, Performance & Stability Tests
# ----------------------------------------------------------------------


def test_hundred_provider_errors():
    """
    Create 100 ProviderError instances.
    """

    errors = [

        ProviderError(
            message=f"Error {i}",
            provider="openai",
        )

        for i in range(100)

    ]

    assert len(errors) == 100


def test_hundred_unique_provider_errors():
    """
    Every ProviderError should be unique.
    """

    errors = [

        ProviderError(
            message=f"Error {i}",
        )

        for i in range(100)

    ]

    assert (

        len(
            {
                id(error)
                for error in errors
            }
        )

        == 100

    )


def test_to_dict_stability():
    """
    Repeated to_dict() calls should
    return identical results.
    """

    exc = ProviderConnectionError(
        provider="openai",
    )

    first = exc.to_dict()

    for _ in range(100):

        assert (
            exc.to_dict()
            == first
        )


def test_exception_to_dict_stability():
    """
    exception_to_dict() should remain
    stable across repeated calls.
    """

    exc = ProviderTimeoutError(
        provider="openai",
    )

    first = exception_to_dict(exc)

    for _ in range(100):

        assert (
            exception_to_dict(exc)
            == first
        )


def test_helper_function_stability():
    """
    Helper functions should return
    consistent values.
    """

    exc = ProviderRateLimitError(
        provider="openai",
    )

    for _ in range(100):

        assert (
            get_provider(exc)
            == "openai"
        )

        assert (
            get_error_code(exc)
            == "PROVIDER_RATE_LIMIT"
        )

        assert (
            is_retryable(exc)
            is True
        )


def test_metadata_isolation_between_instances():
    """
    Metadata should never be shared
    between exception instances.
    """

    exc1 = ProviderError(
        message="A",
    )

    exc2 = ProviderError(
        message="B",
    )

    exc1.metadata["request"] = 1

    assert (
        "request"
        not in exc2.metadata
    )


def test_multiple_to_dict_objects_are_unique():
    """
    Every to_dict() call should
    return a new dictionary.
    """

    exc = ProviderError(
        message="Error",
    )

    dictionaries = [

        exc.to_dict()

        for _ in range(100)

    ]

    assert (

        len(
            {
                id(d)
                for d in dictionaries
            }
        )

        == 100

    )


def test_multiple_exception_to_dict_objects_are_unique():
    """
    exception_to_dict() should
    return new dictionaries.
    """

    exc = ProviderTimeoutError(
        provider="openai",
    )

    dictionaries = [

        exception_to_dict(exc)

        for _ in range(100)

    ]

    assert (

        len(
            {
                id(d)
                for d in dictionaries
            }
        )

        == 100

    )


def test_exception_repr_stability():
    """
    __repr__ should remain stable.
    """

    exc = ProviderConnectionError(
        provider="openai",
    )

    first = repr(exc)

    for _ in range(100):

        assert (
            repr(exc)
            == first
        )


def test_exception_str_stability():
    """
    __str__ should remain stable.
    """

    exc = ProviderConnectionError(
        provider="openai",
    )

    first = str(exc)

    for _ in range(100):

        assert (
            str(exc)
            == first
        )