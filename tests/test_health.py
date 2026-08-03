"""
test_health.py

Unit tests for health.py
"""

from __future__ import annotations

from datetime import datetime

import pytest

from ai.providers.health import (
    DEFAULT_FAILURE_COUNT,
    DEFAULT_LATENCY_MS,
    DEFAULT_RETRY_COUNT,
    DEFAULT_SUCCESS_RATE,
    HealthStatus,
    ProviderHealth,
    health_from_dict,
    health_to_dict,
    is_provider_available,
    is_provider_healthy,
    is_provider_online,
)


# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------


@pytest.fixture
def provider_health():

    return ProviderHealth(
        provider="openai",
        status=HealthStatus.HEALTHY,
        available=True,
        latency_ms=125.5,
        success_rate=99.5,
        failure_count=0,
        retry_count=0,
        circuit_open=False,
        last_success=datetime.utcnow(),
        last_failure=None,
        last_check=datetime.utcnow(),
        metadata={
            "region": "global",
        },
    )
    
# ----------------------------------------------------------------------
# Constructor Tests
# ----------------------------------------------------------------------


def test_provider_health_type(provider_health):

    assert isinstance(
        provider_health,
        ProviderHealth,
    )


def test_provider_name(provider_health):

    assert provider_health.provider == "openai"


def test_default_status():

    health = ProviderHealth(
        provider="test",
    )

    assert (
        health.status
        == HealthStatus.UNKNOWN
    )


def test_default_latency():

    health = ProviderHealth(
        provider="test",
    )

    assert (
        health.latency_ms
        == DEFAULT_LATENCY_MS
    )


def test_default_success_rate():

    health = ProviderHealth(
        provider="test",
    )

    assert (
        health.success_rate
        == DEFAULT_SUCCESS_RATE
    )


def test_default_failure_count():

    health = ProviderHealth(
        provider="test",
    )

    assert (
        health.failure_count
        == DEFAULT_FAILURE_COUNT
    )


def test_default_retry_count():

    health = ProviderHealth(
        provider="test",
    )

    assert (
        health.retry_count
        == DEFAULT_RETRY_COUNT
    )


def test_default_metadata():

    health = ProviderHealth(
        provider="test",
    )

    assert health.metadata == {}
    
# ----------------------------------------------------------------------
# Validation Tests
# ----------------------------------------------------------------------


def test_empty_provider():

    with pytest.raises(
        ValueError,
    ):

        ProviderHealth(
            provider="",
        )


def test_negative_latency():

    with pytest.raises(
        ValueError,
    ):

        ProviderHealth(
            provider="test",
            latency_ms=-1,
        )


def test_invalid_success_rate():

    with pytest.raises(
        ValueError,
    ):

        ProviderHealth(
            provider="test",
            success_rate=101,
        )


def test_negative_failure_count():

    with pytest.raises(
        ValueError,
    ):

        ProviderHealth(
            provider="test",
            failure_count=-1,
        )


def test_negative_retry_count():

    with pytest.raises(
        ValueError,
    ):

        ProviderHealth(
            provider="test",
            retry_count=-1,
        )


def test_provider_normalization():

    health = ProviderHealth(
        provider=" OpenAI ",
    )

    assert health.provider == "openai"

# ----------------------------------------------------------------------
# Property Tests
# ----------------------------------------------------------------------


def test_is_healthy(provider_health):

    assert provider_health.is_healthy


def test_is_available(provider_health):

    assert provider_health.is_available


def test_is_online(provider_health):

    assert provider_health.is_online


def test_has_failures(provider_health):

    assert not provider_health.has_failures


def test_needs_retry(provider_health):

    assert not provider_health.needs_retry


def test_circuit_closed(provider_health):

    assert provider_health.circuit_closed
    
# ----------------------------------------------------------------------
# Serialization Tests
# ----------------------------------------------------------------------


def test_to_dict(provider_health):

    assert isinstance(
        provider_health.to_dict(),
        dict,
    )


def test_to_dict_provider(provider_health):

    assert (
        provider_health.to_dict()["provider"]
        == "openai"
    )


def test_from_dict(provider_health):

    restored = ProviderHealth.from_dict(
        provider_health.to_dict(),
    )

    assert restored == provider_health


def test_copy(provider_health):

    copied = provider_health.copy()

    assert copied == provider_health

    assert copied is not provider_health


def test_copy_update(provider_health):

    copied = provider_health.copy(
        latency_ms=50,
    )

    assert copied.latency_ms == 50

    assert provider_health.latency_ms == 125.5

# ----------------------------------------------------------------------
# Utility Method Tests
# ----------------------------------------------------------------------


def test_get_metadata(provider_health):

    assert (
        provider_health.get_metadata(
            "region",
        )
        == "global"
    )


def test_get_missing_metadata(provider_health):

    assert (
        provider_health.get_metadata(
            "missing",
        )
        is None
    )


def test_has_metadata(provider_health):

    assert provider_health.has_metadata(
        "region",
    )


def test_record_success(provider_health):

    updated = provider_health.record_success()

    assert updated.failure_count == 0

    assert (
        updated.status
        == HealthStatus.HEALTHY
    )


def test_record_failure(provider_health):

    updated = provider_health.record_failure()

    assert updated.failure_count == 1

    assert (
        updated.status
        == HealthStatus.DEGRADED
    )


def test_update_latency(provider_health):

    updated = provider_health.update_latency(
        42.5,
    )

    assert updated.latency_ms == 42.5


def test_reset_failures(provider_health):

    failed = provider_health.copy(
        failure_count=5,
        retry_count=2,
    )

    reset = failed.reset_failures()

    assert reset.failure_count == 0

    assert reset.retry_count == 0
    
# ----------------------------------------------------------------------
# Utility Method Tests
# ----------------------------------------------------------------------


def test_get_metadata(provider_health):

    assert (
        provider_health.get_metadata(
            "region",
        )
        == "global"
    )


def test_get_missing_metadata(provider_health):

    assert (
        provider_health.get_metadata(
            "missing",
        )
        is None
    )


def test_has_metadata(provider_health):

    assert provider_health.has_metadata(
        "region",
    )


def test_record_success(provider_health):

    updated = provider_health.record_success()

    assert updated.failure_count == 0

    assert (
        updated.status
        == HealthStatus.HEALTHY
    )


def test_record_failure(provider_health):

    updated = provider_health.record_failure()

    assert updated.failure_count == 1

    assert (
        updated.status
        == HealthStatus.DEGRADED
    )


def test_update_latency(provider_health):

    updated = provider_health.update_latency(
        42.5,
    )

    assert updated.latency_ms == 42.5


def test_reset_failures(provider_health):

    failed = provider_health.copy(
        failure_count=5,
        retry_count=2,
    )

    reset = failed.reset_failures()

    assert reset.failure_count == 0

    assert reset.retry_count == 0

# ----------------------------------------------------------------------
# Helper Function Tests
# ----------------------------------------------------------------------


def test_health_from_dict(
    provider_health,
):

    restored = health_from_dict(
        provider_health.to_dict(),
    )

    assert restored == provider_health


def test_health_to_dict(
    provider_health,
):

    data = health_to_dict(
        provider_health,
    )

    assert isinstance(
        data,
        dict,
    )


def test_is_provider_healthy(
    provider_health,
):

    assert is_provider_healthy(
        provider_health,
    )


def test_is_provider_available(
    provider_health,
):

    assert is_provider_available(
        provider_health,
    )


def test_is_provider_online(
    provider_health,
):

    assert is_provider_online(
        provider_health,
    )


def test_health_to_dict_matches_method(
    provider_health,
):

    assert (

        health_to_dict(
            provider_health,
        )

        ==

        provider_health.to_dict()

    )

# ----------------------------------------------------------------------
# Python Special Method Tests
# ----------------------------------------------------------------------


def test_str(
    provider_health,
):

    assert (
        str(provider_health)
        == "openai"
    )


def test_repr(
    provider_health,
):

    text = repr(
        provider_health,
    )

    assert (
        "ProviderHealth"
        in text
    )

    assert (
        "openai"
        in text
    )


def test_bool(
    provider_health,
):

    assert bool(
        provider_health,
    )


def test_unhealthy_bool(
    provider_health,
):

    unhealthy = provider_health.copy(
        status=HealthStatus.OFFLINE,
    )

    assert not bool(
        unhealthy,
    )


def test_repr_returns_string(
    provider_health,
):

    assert isinstance(
        repr(provider_health),
        str,
    )


def test_str_returns_string(
    provider_health,
):

    assert isinstance(
        str(provider_health),
        str,
    )

# ----------------------------------------------------------------------
# Stress & Stability Tests
# ----------------------------------------------------------------------


def test_hundred_health_objects():

    health_objects = [

        ProviderHealth(
            provider=f"provider{i}",
        )

        for i in range(100)

    ]

    assert len(
        health_objects,
    ) == 100


def test_health_object_uniqueness():

    health_objects = [

        ProviderHealth(
            provider=f"provider{i}",
        )

        for i in range(100)

    ]

    assert (

        len(
            {
                id(obj)
                for obj in health_objects
            }
        )

        == 100

    )


def test_to_dict_stability(
    provider_health,
):

    expected = provider_health.to_dict()

    for _ in range(100):

        assert (
            provider_health.to_dict()
            == expected
        )


def test_copy_stability(
    provider_health,
):

    for _ in range(100):

        copied = provider_health.copy()

        assert copied == provider_health


def test_serialization_stability(
    provider_health,
):

    for _ in range(100):

        restored = ProviderHealth.from_dict(
            provider_health.to_dict(),
        )

        assert restored == provider_health


def test_metadata_isolation(
    provider_health,
):

    copied = provider_health.copy()

    copied.metadata["new"] = "value"

    assert (
        "new"
        not in provider_health.metadata
    )


def test_helper_consistency(
    provider_health,
):

    for _ in range(100):

        assert (

            health_from_dict(
                provider_health.to_dict(),
            )

            ==

            provider_health

        )


def test_bool_stability(
    provider_health,
):

    for _ in range(100):

        assert bool(
            provider_health,
        )


def test_repr_stability(
    provider_health,
):

    expected = repr(
        provider_health,
    )

    for _ in range(100):

        assert (
            repr(provider_health)
            == expected
        )


def test_str_stability(
    provider_health,
):

    expected = str(
        provider_health,
    )

    for _ in range(100):

        assert (
            str(provider_health)
            == expected
        )
        