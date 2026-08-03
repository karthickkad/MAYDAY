"""
registry.py

Provider registry for MAYDAY.

Responsible for registering, retrieving, listing,
and managing AI providers.
"""

from __future__ import annotations

from threading import RLock
from typing import Dict, Iterator

from ai.providers.base import BaseProvider


ProviderMap = Dict[str, BaseProvider]


class ProviderRegistry:
    """
    Registry for AI providers.

    The registry maintains a unique collection of providers and
    supports registration, lookup, removal, iteration, and inspection.
    """

    def __init__(self) -> None:
        self._providers: ProviderMap = {}
        self._lock = RLock()

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, provider: BaseProvider) -> None:
        """
        Register a provider.

        Raises:
            ValueError:
                If the provider is already registered.
        """
        name = provider.name.lower()

        with self._lock:
            if name in self._providers:
                raise ValueError(
                    f"Provider '{provider.name}' is already registered."
                )

            self._providers[name] = provider

    def unregister(self, name: str) -> None:
        """
        Remove a provider.

        Raises:
            KeyError:
                If the provider is not registered.
        """
        name = name.lower()

        with self._lock:
            if name not in self._providers:
                raise KeyError(
                    f"Provider '{name}' is not registered."
                )

            del self._providers[name]

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get(self, name: str) -> BaseProvider:
        """
        Retrieve a provider.

        Raises:
            KeyError:
                If the provider is not registered.
        """
        name = name.lower()

        with self._lock:
            if name not in self._providers:
                raise KeyError(
                    f"Provider '{name}' is not registered."
                )

            return self._providers[name]

    def exists(self, name: str) -> bool:
        """
        Check whether a provider exists.
        """
        with self._lock:
            return name.lower() in self._providers

    # ------------------------------------------------------------------
    # Registry Management
    # ------------------------------------------------------------------

    def list_providers(self) -> tuple[str, ...]:
        """
        Return all registered provider names.
        """
        with self._lock:
            return tuple(sorted(self._providers.keys()))

    def clear(self) -> None:
        """
        Remove every registered provider.
        """
        with self._lock:
            self._providers.clear()

    # ------------------------------------------------------------------
    # Python Special Methods
    # ------------------------------------------------------------------

    def __contains__(self, name: str) -> bool:
        """
        Enable:

            "openai" in registry
        """
        return self.exists(name)

    def __len__(self) -> int:
        """
        Enable:

            len(registry)
        """
        with self._lock:
            return len(self._providers)

    def __iter__(self) -> Iterator[BaseProvider]:
        """
        Enable:

            for provider in registry:
                ...
        """
        with self._lock:
            return iter(tuple(self._providers.values()))

    def __repr__(self) -> str:
        """
        Developer-friendly representation.
        """
        providers = ", ".join(self.list_providers())

        return (
            f"{self.__class__.__name__}"
            f"(providers=[{providers}])"
        )