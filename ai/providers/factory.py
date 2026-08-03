"""
factory.py

Provider factory for MAYDAY.

Responsible for registering provider constructors and creating
provider instances on demand.
"""

from __future__ import annotations

from threading import RLock
from typing import Callable, Dict, Iterator

from ai.providers.base import BaseProvider

ProviderConstructor = Callable[..., BaseProvider]
ProviderFactoryMap = Dict[str, ProviderConstructor]


class ProviderFactory:
    """
    Factory responsible for creating AI provider instances.
    """

    def __init__(self) -> None:
        self._providers: ProviderFactoryMap = {}
        self._lock = RLock()

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(
        self,
        name: str,
        constructor: ProviderConstructor,
    ) -> None:
        """
        Register a provider constructor.

        Raises:
            ValueError:
                If already registered.
        """
        name = name.lower()

        with self._lock:
            if name in self._providers:
                raise ValueError(
                    f"Provider '{name}' is already registered."
                )

            self._providers[name] = constructor

    def unregister(self, name: str) -> None:
        """
        Remove a provider constructor.

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
    # Factory
    # ------------------------------------------------------------------

    def create(
        self,
        name: str,
        *args,
        **kwargs,
    ) -> BaseProvider:
        """
        Create a provider instance.

        Additional positional and keyword arguments are passed
        directly to the provider constructor.

        Raises:
            KeyError:
                If the provider is unknown.
        """
        name = name.lower()

        with self._lock:
            if name not in self._providers:
                raise KeyError(
                    f"Provider '{name}' is not registered."
                )

            constructor = self._providers[name]

        return constructor(*args, **kwargs)

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def exists(self, name: str) -> bool:
        """
        Check whether a provider constructor exists.
        """
        with self._lock:
            return name.lower() in self._providers

    def list_providers(self) -> tuple[str, ...]:
        """
        Return registered provider names.
        """
        with self._lock:
            return tuple(sorted(self._providers.keys()))

    # ------------------------------------------------------------------
    # Registry Management
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """
        Remove all registered provider constructors.
        """
        with self._lock:
            self._providers.clear()

    # ------------------------------------------------------------------
    # Python Special Methods
    # ------------------------------------------------------------------

    def __contains__(self, name: str) -> bool:
        return self.exists(name)

    def __len__(self) -> int:
        with self._lock:
            return len(self._providers)

    def __iter__(self) -> Iterator[ProviderConstructor]:
        with self._lock:
            return iter(tuple(self._providers.values()))

    def __repr__(self) -> str:
        providers = ", ".join(self.list_providers())

        return (
            f"{self.__class__.__name__}"
            f"(providers=[{providers}])"
        )