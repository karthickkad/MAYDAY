"""
manager.py

Provider manager for MAYDAY.

Coordinates the provider registry and provider factory.
"""

from __future__ import annotations

from threading import RLock

from ai.providers.base import BaseProvider
from ai.providers.factory import ProviderFactory
from ai.providers.registry import ProviderRegistry


class ProviderManager:
    """
    High-level manager for AI providers.
    """

    def __init__(self) -> None:
        self._registry = ProviderRegistry()
        self._factory = ProviderFactory()
        self._default_provider: str | None = None
        self._lock = RLock()

    # ------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------

    def register(
        self,
        name: str,
        constructor,
        *,
        default: bool = False,
        **kwargs,
    ) -> BaseProvider:
        """
        Register a provider constructor and create an instance.
        """
        with self._lock:

            self._factory.register(name, constructor)

            provider = self._factory.create(name, **kwargs)

            provider.initialize()

            self._registry.register(provider)

            if default or self._default_provider is None:
                self._default_provider = name.lower()

            return provider

    def unregister(self, name: str) -> None:
        """
        Remove a provider.
        """
        with self._lock:

            provider = self._registry.get(name)

            provider.shutdown()

            self._registry.unregister(name)

            self._factory.unregister(name)

            if self._default_provider == name.lower():
                self._default_provider = None

    # ------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------

    def get(self, name: str) -> BaseProvider:
        return self._registry.get(name)

    def exists(self, name: str) -> bool:
        return self._registry.exists(name)

    def list_providers(self) -> tuple[str, ...]:
        return self._registry.list_providers()

    # ------------------------------------------------------------
    # Default Provider
    # ------------------------------------------------------------

    def default_provider(self) -> BaseProvider:
        """
        Return the default provider.
        """
        if self._default_provider is None:
            raise RuntimeError("No default provider configured.")

        return self._registry.get(self._default_provider)

    def set_default(self, name: str) -> None:
        """
        Set the default provider.
        """
        if not self.exists(name):
            raise KeyError(
                f"Provider '{name}' is not registered."
            )

        self._default_provider = name.lower()

    # ------------------------------------------------------------
    # Health
    # ------------------------------------------------------------

    def health_check(self) -> dict[str, bool]:
        """
        Check every provider.
        """
        status = {}

        for provider in self._registry:
            status[provider.name] = provider.health_check()

        return status

    # ------------------------------------------------------------
    # Shutdown
    # ------------------------------------------------------------

    def shutdown(self) -> None:
        """
        Shutdown all providers.
        """
        for provider in self._registry:
            provider.shutdown()

        self._registry.clear()
        self._factory.clear()
        self._default_provider = None

    # ------------------------------------------------------------
    # Python Methods
    # ------------------------------------------------------------

    def __contains__(self, name: str) -> bool:
        return self.exists(name)

    def __len__(self) -> int:
        return len(self._registry)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(providers={self.list_providers()})"
        )